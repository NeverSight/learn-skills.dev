---
name: nic-diagnostics-tuning-for-af-xdp
description: Use this skill when diagnosing, configuring, or monitoring NICs for AF_XDP / XDP workloads. Covers driver detection, hardware queue configuration, ring buffer sizing, RSS indirection table management, interrupt coalesce tuning, offload control (GSO/GRO/TSO/LRO), VLAN offloads, Flow Director (FDIR) rules with loc pinning and ixgbe wipe bug workaround, RPS/XPS queue CPU mapping, sysctl network tuning, CPU core pinning and NUMA awareness, hardware queue and drop monitoring, softirq and rx_missed_errors analysis, BPF program inspection with bpftool (prog dump xlated, net show), kernel tracing via ftrace and dmesg, perf profiling and flamegraphs, IRQ-to-queue-to-core mapping, bonding interface diagnostics, socket inspection, and a quick diagnostic checklist.
---

# NIC Diagnostics for XDP

Comprehensive reference for diagnosing, configuring, and monitoring NICs in AF_XDP / XDP workloads.

---

## 1. Driver Detection & NIC Identification

### Identify the NIC and driver in use
```bash
# PCI device listing — find your NIC's bus address
lspci

# Driver name, version, firmware, bus-info
ethtool -i <iface>

# Link state, speed, duplex negotiation
ethtool <iface>
ethtool <iface> | egrep -i 'link|speed|duplex'

# Confirm interface is up and check for attached XDP program
ip link show dev <iface>
ip link show dev <iface> | grep xdp
```

### Why it matters
XDP zero-copy support is driver-specific. Only certain drivers (ice, i40e, mlx5, etc.) support `XDP_DRV` mode and AF_XDP zero-copy. Knowing the driver tells you what features are available and what quirks to expect.

---

## 2. Hardware Queue Configuration

### View and set combined queue count
```bash
# Show current and max queue count
ethtool -l <iface>

# Set combined queues (must match or exceed XDP queue IDs you bind to)
ethtool -L <iface> combined <N>

# List all queues exposed by the NIC
ls -1 /sys/class/net/<iface>/queues
```

### Ring buffer sizes
```bash
# Show current and max ring buffer depths (rx/tx)
ethtool -g <iface>

# Increase ring buffer sizes to absorb bursts
ethtool -G <iface> rx 4096 tx 4096
```

### Why it matters
Each AF_XDP socket binds to a specific hardware queue. You need enough queues for your workload, and the ring buffer depth affects burst absorption. Too few queues = contention; too shallow rings = drops under burst.

---

## 3. Offload Control — GSO, GRO, TSO, LRO

### Inspect current offload state
```bash
ethtool -k <iface>
ethtool -k <iface> | grep -E 'generic-receive|large-receive|scatter-gather|tcp-segmentation'
```

### Disable offloads for XDP
```bash
# XDP requires offloads disabled — aggregated/segmented frames break XDP processing
ethtool -K <iface> gro off lro off tso off gso off
```

### Why it matters
GRO/LRO aggregate multiple packets into a single large buffer. TSO/GSO do the same on the TX side. XDP programs operate on individual frames at the driver level — aggregated super-frames will either be rejected or cause undefined behavior. **Always disable these before attaching XDP programs.**

---

## 4. VLAN Offload Control

### Inspect and toggle VLAN offloads
```bash
ethtool -k <iface> | grep -i vlan

# Disable VLAN tag stripping (keep tags in packet data for XDP inspection)
ethtool -K <iface> rxvlan off
ethtool -K <iface> txvlan off

# Or via the longer form
ethtool -K <iface> rx-vlan-offload off
ethtool -K <iface> rx-vlan-filter off

# Re-enable if needed
ethtool -K <iface> rxvlan on
ethtool -K <iface> rx-vlan-filter on
```

### Why it matters
When VLAN offload is on, the NIC strips the 802.1Q tag before the packet reaches XDP. If your XDP program needs to inspect or filter on VLAN IDs, you must disable `rxvlan` so the tag remains in the Ethernet header.

---

## 5. Flow Director (FDIR) / ntuple Rules

### Check ntuple support
```bash
ethtool -k <iface> | grep -i ntuple
```

### View existing flow rules
```bash
ethtool -n <iface>
ethtool -u <iface>
```

### Add FDIR rules — steer traffic to a specific hardware queue
```bash
# Steer UDP traffic matching a 5-tuple → queue 3
sudo ethtool -U <iface> flow-type udp4 \
  src-ip <src> dst-ip <dst> dst-port <port> action 3

# Steer TCP traffic to a specific dst-port → queue 0
sudo ethtool -U <iface> flow-type tcp4 \
  src-ip 0.0.0.0 dst-ip <dst> dst-port <port> action 0
```

### FDIR rule locations and lifecycle
```bash
# Add FDIR rule at a specific location (deterministic rule ID)
ethtool -U <iface> flow-type tcp4 dst-port 22 action 0 loc 2045
ethtool -U <iface> flow-type udp4 dst-port 20000 action 3 loc 2044

# Delete a specific FDIR rule by location/ID
ethtool -U <iface> delete 2045
ethtool -N <iface> delete 2045

# Idempotent rule setup pattern (delete-then-recreate)
ethtool -U <iface> delete 2045 2>/dev/null || true
ethtool -U <iface> flow-type tcp4 dst-port 22 action 0 loc 2045
```

### FDIR stats monitoring
```bash
# Check FDIR match/miss statistics
ethtool -S <iface> | grep -i fdir

# Monitor FDIR + specific queue together
ethtool -S <iface> | grep -E 'rx_queue_3|fdir'
```

### KNOWN BUG: ixgbe FDIR wipe on XDP attach

The ixgbe driver (82599-based NICs) **wipes all FDIR/ntuple rules when an XDP program attaches**. This means SSH steering rules disappear and SSH traffic gets distributed randomly by RSS, often causing SSH lockout.

```bash
# Workaround: FDIR watchdog that re-adds rules after XDP attach
(
    while true; do
        ethtool -n <iface> 2>/dev/null | grep -q "loc 2045" || {
            ethtool -U <iface> delete 2045 2>/dev/null || true
            ethtool -U <iface> flow-type tcp4 dst-port 22 action 0 loc 2045
        }
        ethtool -n <iface> 2>/dev/null | grep -q "loc 2044" || {
            ethtool -U <iface> delete 2044 2>/dev/null || true
            ethtool -U <iface> flow-type udp4 dst-port 20000 action 3 loc 2044
        }
        sleep 2
    done
) &
WATCHDOG_PID=$!
```

### Why it matters
FDIR rules let you pin specific flows to specific hardware queues. Since each AF_XDP socket binds to one queue, FDIR is how you guarantee that your target traffic lands on the queue your XDP program is listening on. Without FDIR, RSS hashing distributes packets unpredictably across all queues. Using explicit `loc` values makes rules deterministic and deletable by ID. On ixgbe, always run a FDIR watchdog.

---

## 6. RSS Indirection Table Management

### View and manipulate the RSS hash-to-queue mapping
```bash
# View RSS indirection table (shows which queue each hash bucket maps to)
ethtool -x <iface>
ethtool -x <iface> | head -20

# Restore RSS to default distribution
ethtool -X <iface> default

# Set RSS to distribute evenly across N queues
ethtool -X <iface> equal <N>

# Concentrate all RSS traffic to a single queue (e.g., queue 3)
# Weight array: one entry per queue, only queue 3 gets weight 1
ethtool -X <iface> weight 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

# RSS + start offset (steer to specific queue range)
ethtool -X <iface> equal 1 start 3
```

### Why it matters
RSS distributes incoming traffic across hardware queues using a hash of packet headers. When FDIR rules are unavailable or get wiped (e.g., ixgbe XDP attach bug), RSS indirection table manipulation is the fallback for steering traffic to specific queues. You can weight all traffic to a single queue or distribute evenly across a subset.

---

## 7. Interrupt Coalesce Settings

```bash
# View current coalesce/interrupt moderation settings
ethtool -c <iface>

# Set coalesce parameters (reduce interrupt rate for throughput, or lower for latency)
ethtool -C <iface> rx-usecs <N> tx-usecs <N>
```

### Why it matters
Coalesce settings control how aggressively the NIC batches interrupts. Lower values = lower latency but higher CPU overhead. Higher values = better throughput but more latency. When running mixed XDP + kernel-stack workloads, coalesce settings affect latency for non-XDP traffic (like SSH) sharing the same NIC.

---

## 8. Private Flags & Loopback

```bash
# Show driver-specific private flags
ethtool --show-priv-flags <iface>

# Enable hardware loopback (useful for testing without a second machine)
sudo ethtool --set-priv-flags <iface> loopback on
sudo ethtool -s <iface> loopback on

# Check loopback support
sudo ethtool --show-features <iface> | grep loopback
```

---

## 9. RPS/XPS Queue CPU Mapping

### Receive Packet Steering (RPS)
```bash
# Check current RPS CPU mask for a queue
cat /sys/class/net/<iface>/queues/rx-0/rps_cpus

# Disable RPS for all RX queues (let hardware queues handle it — required for XDP)
for f in /sys/class/net/<iface>/queues/rx-*/rps_cpus; do
    echo 0 > "$f"
done
```

### Transmit Packet Steering (XPS)
```bash
# Set XPS for TX queues
for f in /sys/class/net/<iface>/queues/tx-*/xps_cpus; do
    echo <cpumask> > "$f"
done
```

### Why it matters
RPS is software-level receive steering. It should be disabled on queues that XDP is using, since XDP bypasses the kernel RX path entirely. Leaving RPS enabled can cause unnecessary overhead and confusing behavior.

---

## 10. Sysctl Network Tuning for XDP Workloads

```bash
# Buffer sizes for UDP-heavy workloads
sysctl -qw net.core.rmem_max=268435456
sysctl -qw net.core.wmem_max=268435456
sysctl -qw net.core.rmem_default=262144
sysctl -qw net.core.wmem_default=262144

# Increase backlog for high-PPS workloads
sysctl -qw net.core.netdev_max_backlog=250000
```

### Why it matters
Even with XDP handling the fast path, non-XDP traffic still passes through the kernel networking stack. These sysctls ensure the kernel side doesn't become a bottleneck for UDP-heavy workloads or drop packets due to insufficient buffer space.

---

## 11. Detecting Idle CPU Cores for Pinning

### Map the CPU topology
```bash
# Full CPU topology: CPU ID, physical core, socket, NUMA node
lscpu -e=CPU,CORE,SOCKET,NODE,ONLINE
```

### Find NUMA node for the NIC
```bash
# Critical: pin XDP threads to cores on the same NUMA node as the NIC
cat /sys/class/net/<iface>/device/numa_node
```

### Find which cores are busy vs idle
```bash
# Per-CPU utilization — look for cores near 0% usage
mpstat -P ALL 1 5

# Check what's pinned to each core already
ps -eo pid,comm,psr --sort=psr | awk '{count[$3]++; procs[$3]=procs[$3] " " $2} END {for (c in count) print "CPU " c ": " count[c] " procs:" procs[c]}'

# Check IRQ affinity — which cores handle which NIC interrupts
cat /proc/interrupts | grep <iface>
awk '/<iface>-TxRx/{print $1,$NF}' /proc/interrupts | sed 's/://'
grep . /proc/irq/*/smp_affinity_list
```

### Disable irqbalance (prevents the OS from moving IRQs to your pinned cores)
```bash
sudo systemctl stop irqbalance
systemctl status irqbalance
```

### Pin IRQs to specific cores
```bash
# Check current IRQ CPU affinity
cat /proc/irq/<irq_num>/smp_affinity_list

# Pin an IRQ to a specific core
echo <core_id> | sudo tee /proc/irq/<irq_num>/smp_affinity_list
```

### MSI-X IRQ vector enumeration
```bash
# List all MSI-X vectors for the NIC's PCI device
ls /sys/devices/pci<domain>/<bus>/<device>/msi_irqs
```

### Why it matters
XDP busy-poll loops are CPU-bound. Pinning them to an idle core on the correct NUMA node eliminates cross-node memory latency and prevents the scheduler from preempting your hot loop. Always:
1. Find the NIC's NUMA node
2. Pick idle cores on that node
3. Stop irqbalance
4. Pin NIC IRQs away from your XDP cores
5. Pin your XDP threads to the chosen cores

---

## 12. Hardware Queue & Drop Monitoring

### Live NIC statistics
```bash
# Full stats dump
ethtool -S <iface>

# XDP/XSK specific counters
ethtool -S <iface> | grep -i xdp

# Filter for drops, errors, misses
ethtool -S <iface> | egrep -i 'rx|drop|err|xdp|xsk' | head -n 50

# Per-queue packet counts
ethtool -S <iface> | grep -E "rx_queue"
ethtool -S <iface> | grep "rx_queue_<N>_packets:"
```

### Live monitoring dashboards
```bash
# Watch queue counters in real time
watch -n 1 'ethtool -S <iface> | grep -E "rx_queue"'

# Watch drops and errors
watch -n1 "ethtool -S <iface> | grep -E 'rx_packets|rx_dropped|rx_queue'"

# Combined NIC + XDP socket status
watch -n 1 "echo '=== NIC ===' && ethtool -S <iface> | grep -iE 'drop|miss|err|full' && echo '=== XDP ===' && cat /proc/net/xdp 2>/dev/null"

# Full drop monitoring loop
IFACE=<iface>; QUEUE=<N>
while true; do
    echo "--- $(date) ---"
    echo "NIC Drops:"
    ethtool -S $IFACE 2>/dev/null | grep -E "drop|miss|error|discard" | head -10
    echo -e "\nQueue $QUEUE:"
    ethtool -S $IFACE 2>/dev/null | grep -i "queue_${QUEUE}"
    echo -e "\nXDP Sockets:"
    cat /proc/net/xdp 2>/dev/null || echo "No XDP sockets found"
    echo -e "\nInterface Totals:"
    cat /proc/net/dev | awk -v iface=$IFACE '$1 ~ iface {print "RX pkts:", $2, "RX drop:", $5}'
    sleep 5
done
```

### Softirq and rx_missed_errors monitoring
```bash
# Monitor softirq distribution across CPUs
cat /proc/softirqs
watch -n 1 'cat /proc/softirqs'

# Check rx_missed_errors (sign of ring buffer overflow — hardware is dropping)
ethtool -S <iface> | grep rx_missed_errors

# Interface-level packet and drop counts
cat /proc/net/dev
cat /proc/net/dev | awk -v iface=<iface> '$1 ~ iface {print "RX pkts:", $2, "RX drop:", $5}'
```

### AF_XDP socket status
```bash
# Kernel's view of active XDP sockets
cat /proc/net/xdp
cat /proc/net/xdp 2>/dev/null || ss -ax | grep -i xdp
```

### Socket inspection in XDP context
```bash
# Check if SSH is listening and connected
ss -tnp | grep :22

# Check UDP listeners (verify XDP isn't blocking expected ports)
ss -ulnp

# Check for XDP sockets
ss -ax | grep -i xdp
```

---

## 13. BPF Program Inspection & Profiling

### bpftool — inspect loaded XDP/BPF programs and maps
```bash
# List all loaded BPF programs
bpftool prog show
bpftool prog list | grep -A3 "xdp\|dispatcher\|redirect"

# Details on a specific program
bpftool prog show id <prog_id>

# Profile a BPF program (cycles, instructions over 5 seconds)
bpftool prog profile id <prog_id> duration 5 cycles instructions

# Dump the translated (verified) bytecode of a loaded XDP program
bpftool prog dump xlated name xdp_redirect
bpftool prog dump xlated id <prog_id>

# Show all BPF programs attached to network devices
bpftool net show

# List all BPF maps
bpftool map show
bpftool map show | grep -i xsk

# Dump map contents (debug maps, XSK maps)
bpftool map dump name <map_name>
bpftool map dump pinned /sys/fs/bpf/xsks_map
bpftool map dump id <map_id>
```

### Why it matters
`bpftool` is the primary way to verify your XDP program is loaded, attached to the right interface, and that its maps (especially XSK maps) are populated correctly. `prog dump xlated` lets you inspect the verified bytecode to confirm program logic. `bpftool net show` gives a quick view of which XDP programs are attached to which interfaces. Map dumps let you verify that socket file descriptors are registered in the XSKMAP.

---

## 14. Kernel Tracing — ftrace / trace_pipe

### Capture XDP trace events from the kernel
```bash
# Stream trace output (Ctrl+C to stop)
cat /sys/kernel/debug/tracing/trace_pipe

# Background capture to a file
cat /sys/kernel/debug/tracing/trace_pipe > /tmp/xdp_trace.log &

# Read the log
cat /tmp/xdp_trace.log

# Tail live
tail -f /sys/kernel/debug/tracing/trace_pipe

# Stop background trace capture
pkill -f trace_pipe
fuser -k /sys/kernel/debug/tracing/trace_pipe
```

### Watch dmesg for XDP and driver events
```bash
watch -n1 "dmesg | grep xdp"

# Check for XDP-related kernel messages, driver errors, firmware warnings
dmesg | grep -i -E 'xdp|bpf|ixgbe|ice|mlx5|driver'
dmesg | tail -80
```

### Why it matters
When XDP programs call `bpf_trace_printk()`, output goes to `trace_pipe`. This is the primary printf-style debugging mechanism for eBPF/XDP programs. Use it to trace packet paths, verify filter logic, and debug drop reasons.

---

## 15. perf — CPU-Level Performance Profiling

### Stat counters (lightweight, no recording)
```bash
# Core hardware counters for your XDP process
sudo perf stat -e cycles,instructions,cache-misses,LLC-load-misses,branches,branch-misses \
  -p $(pgrep <process>) -- sleep 10

# Extended counters (-d -d -d = most detail)
sudo perf stat -d -d -d -p $(pgrep <process>)
```

### Record + flamegraph workflow
```bash
# Record with DWARF call graphs (most accurate stacks)
sudo perf record --call-graph dwarf -e cycles \
  -p $(pgrep <process>) -- sleep 10

# Record on a specific CPU core
sudo perf record -F 997 -g --call-graph dwarf -C <core> -o perf.data -- sleep 60

# Record multiple event types
sudo perf record -e cycles,stalled-cycles-frontend,stalled-cycles-backend,cache-misses,branch-misses \
  -g -p $(pgrep <process>)

# Interactive report
sudo perf report

# Generate flamegraph (requires inferno)
sudo perf script -i perf.data | inferno-collapse-perf | inferno-flamegraph > flamegraph.svg

# Live top-like view
sudo perf top -p $(pgrep <process>) -g
```

### Why it matters
`perf stat` answers "is my hot loop efficient?" — watch IPC (instructions per cycle), cache miss rates, and branch mispredictions. `perf record` + flamegraphs show exactly where CPU time is spent in your rx/tx loop, revealing bottlenecks in ring operations, packet parsing, or syscalls.

---

## 16. IRQ-to-Queue-to-Core Mapping

### Full mapping workflow
```bash
# 1. Find which IRQs belong to your NIC
cat /proc/interrupts | grep <iface>
awk '/<iface>-TxRx/{print $1,$NF}' /proc/interrupts | sed 's/://'

# 2. Check current CPU affinity for each IRQ
cat /proc/irq/<irq_num>/smp_affinity_list

# 3. Pin queue IRQs to specific cores (avoid your XDP poll cores)
echo <core_id> | sudo tee /proc/irq/<irq_num>/smp_affinity_list
```

### Why it matters
Each NIC queue generates interrupts on a specific IRQ line. If the kernel delivers that IRQ to the same core running your XDP busy-poll, you get contention. Map out which IRQ serves which queue, then pin IRQs to cores that are **not** running your XDP threads.

---

## 17. Bonding Interface Diagnostics

```bash
# Check bonding status (active slave, mode, LACP)
cat /proc/net/bonding/bond0
cat /proc/net/bonding/<bond_iface>

# Per-port stats on bond members
ethtool -S <bond_member_iface> | egrep 'rx_queue_|tx_queue_'
```

### Why it matters
When XDP workloads run on a NIC that is also a member of a bonding group, you need to inspect the bond state and per-member statistics separately. XDP attaches to the physical interface, not the bond, so diagnostics must target the underlying member NIC.

---

## 18. Driver Info Fallback

```bash
# When ethtool -i fails, fall back to sysfs
ethtool -i <iface> 2>/dev/null || cat /sys/class/net/<iface>/device/uevent
```

---

## 19. Quick Diagnostic Checklist

Run this sequence when setting up or debugging an XDP workload:

| Step | Command | Looking For |
|------|---------|-------------|
| 1 | `ethtool -i <iface>` | Driver supports XDP (ice, i40e, mlx5, ixgbe) |
| 2 | `ethtool -l <iface>` | Enough combined queues |
| 3 | `ethtool -g <iface>` | Ring buffer depth adequate |
| 4 | `ethtool -G <iface> rx 4096 tx 4096` | Resize if too shallow |
| 5 | `ethtool -k <iface> \| grep -E 'gro\|tso\|gso\|lro'` | All OFF |
| 6 | `ethtool -k <iface> \| grep ntuple` | ntuple ON for FDIR |
| 7 | `ethtool -n <iface>` | FDIR rules steering to correct queues |
| 8 | `ethtool -x <iface>` | RSS indirection table sane |
| 9 | `ethtool -c <iface>` | Coalesce settings appropriate |
| 10 | `cat /sys/class/net/<iface>/device/numa_node` | NUMA node for core selection |
| 11 | `lscpu -e=CPU,CORE,SOCKET,NODE,ONLINE` | Available cores on correct NUMA |
| 12 | `systemctl status irqbalance` | Should be STOPPED |
| 13 | `cat /proc/interrupts \| grep <iface>` | IRQs pinned away from XDP cores |
| 14 | `cat /sys/class/net/<iface>/queues/rx-*/rps_cpus` | RPS disabled (0) on XDP queues |
| 15 | `bpftool prog show` | XDP program loaded and attached |
| 16 | `bpftool net show` | XDP attached to correct interface |
| 17 | `cat /proc/net/xdp` | AF_XDP sockets active |
| 18 | `ethtool -S <iface> \| grep -i drop` | Zero or stable drop counters |
| 19 | `ethtool -S <iface> \| grep rx_missed_errors` | Zero (nonzero = ring overflow) |
| 20 | `cat /proc/softirqs` | Softirqs balanced across cores |
