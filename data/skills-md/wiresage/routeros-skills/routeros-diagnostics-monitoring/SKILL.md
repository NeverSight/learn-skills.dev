---
name: routeros-diagnostics-monitoring
description: Diagnostics and monitoring on MikroTik RouterOS 7. Covers the system log (topics, logging rules and actions, debug buffers, disk, syslog over UDP, TCP and TLS, CEF, email and script actions), ping and path MTU discovery, traceroute, torch, the packet sniffer with TZSP streaming and pcapng files, interface counters and monitor-traffic, Netwatch probes and scripts, SNMP agent, communities, SNMPv3 and traps, Traffic Flow (NetFlow and IPFIX), graphing, resource and CPU views, profiler, health sensors, watchdog, Detect Internet, bandwidth test and speed test, IP scan, and the traffic generator. Use when a link, host or service misbehaves and you need to find where, when collecting logs or metrics from a router, setting up alerts, or measuring throughput.
---

# RouterOS diagnostics and monitoring

Start with the cheapest tool that can answer the question. Most tools below change router behavior while they run (sniffer and torch turn off fast
path and FastTrack, bandwidth test saturates the link), so say so before running them on a production router and stop them afterwards.

| Question | Tool |
| --- | --- |
| Is the host or the internet reachable? | `/ping` (add `src-address`, `interface`, `vrf`, `count`) |
| Where does the path break, loop or slow down? | `/tool/traceroute` (use `use-dns=yes` for names) |
| What happened and when? | `/log/print`, `/system/logging` |
| Who uses the bandwidth right now? | `/tool/torch <interface>` |
| What exactly is on the wire? | `/tool/sniffer` (save to pcapng for Wireshark) |
| Is a host or service down (and act on it)? | `/tool/netwatch` |
| Long-term metrics | SNMP, `/ip/traffic-flow`, `/tool/graphing`, syslog |
| How fast is the link? | `/tool/speed-test`, `/tool/bandwidth-test` |
| CPU, memory, temperature, voltage | `/system/resource`, `/tool/profile`, `/system/health` |
| Router hangs or lost uplink must reboot it | `/system/watchdog` |

## Ping and traceroute

```ros
/ping 1.1.1.1 count=3                                # internet; then a name to test DNS
/ping 198.51.100.10 size=1500 do-not-fragment count=2  # path MTU: lower size until replies arrive
/ping 192.168.2.10 src-address=192.168.88.1 count=3   # needed for IPsec or policy-routed tests
/tool/traceroute 198.51.100.10 count=3 use-dns=yes
```

- `size` counts the whole IP packet (1500 equals `ping -l 1472` on Windows). Without `do-not-fragment` a large ping is fragmented and hides
  an MTU problem. A firewall that drops "fragmentation needed" messages turns the symptom into plain timeouts. Fix with an MSS clamp
  (`routeros-firewall`).
- Status words: `timeout` (host down, ICMP filtered or reply slower than `interval`), `net unreachable` and `host unreachable` (the router
  in `HOST` has no route or rejects), `admin prohibited` (reject-with rule), `TTL exceeded` (usually a routing loop).
- `interface=` is needed for ARP ping (hosts that block ICMP), ND ping and link-local IPv6. `vrf=` accepts only real VRFs.
- Traceroute is `mtr`-like: ICMP probes, up to 30 hops, statistics per hop. Loss at one hop that does not continue at later hops is ICMP rate
  limiting, not path loss. The same router repeating means a loop; a silent tail after one hop means a missing route or a missing route back.

## Log

Rules (`/system/logging`) select by topics and send to an action (`/system/logging/action`): memory (1000 lines, lost at reboot), disk,
echo, remote (syslog), email, script. Defaults keep `info`, `error`, `warning` in memory and print `critical`. Debug is off.

```ros
/log/print where topics~"interface|dhcp"
/log/print follow-only where message~"login failure"
/system/logging/action/add name=dhcpdebug target=memory memory-lines=2000    # debug into its own buffer
/system/logging/add topics=dhcp,debug action=dhcpdebug
/log/print where buffer=dhcpdebug
/system/logging/action/set remote remote=192.0.2.10 remote-log-format=syslog
/system/logging/add topics=info action=remote
```

- A rule matches entries that have **all** its topics: `topics=info,warning` matches nothing. Use one rule per topic. `!` excludes a topic.
- Debug logs can contain secrets (`ssh,debug` logs session keys). Keep them in a local buffer, never send them to syslog or email.
- Syslog formats: `default`, `syslog` (RFC 3164 only), `cef`. Over TCP and TLS use `cef` (the others have no message delimiter). TLS
  `check-certificate=yes` verifies the CA but not the server name. Set `syslog-time-format=iso8601` across time zones and keep NTP right
  (`routeros-system-utilities`). Action names accept only letters and digits.
- Email actions send one mail per entry; a brute-force attack floods the mailbox, so stop attacks in the firewall. A script action reads
  `$topics` and `$message`; the manual's example collects failed-login sources into an address list.
- Entries show twice in `/log/print` when several actions store them: add `where buffer=memory`.

## Sniffer and torch

```ros
/tool/sniffer/start interface=bridge ip-address=192.168.88.50/32      # capture on the LAN side, before NAT hides the host
/tool/sniffer/stop
/tool/sniffer/save file-name=capture.pcap                            # pcapng, open in Wireshark
/tool/sniffer/quick interface=ether1 port=bootps,bootpc duration=10s
/tool/torch bridge src-address=192.168.88.21/32
```

- The sniffer sees received packets before the firewall and sent packets after it, so drops show as received only. Hardware-offloaded bridge
  traffic never reaches the CPU, so it is invisible to both tools (`routeros-bridging-switching`). Filters combine with AND across different
  filters. Memory is 100 KiB by default; `memory-scroll=yes` keeps the newest packets. Captures contain user traffic: treat files as private.
- TZSP streaming (`streaming-enabled=yes streaming-server=... filter-stream=yes`) sends frames unencrypted over UDP 37008.
- Torch: `src-address` is the far side of the watched interface, so on a LAN interface filter hosts with `src-address`. `RX` is what the
  interface receives from that address. It shows traffic the firewall drops (input side), which helps decide whether a rule or the path is at fault.

## Netwatch

```ros
/tool/netwatch/add name=wan-dns host=1.1.1.1 type=icmp thr-avg=100ms interval=10s \
    up-script=":log info \"wan up\"" down-script=":log warning \"wan down\""
/tool/netwatch/print stats
```

Types: `simple` (default interval 60 s), `icmp`, `tcp-conn`, `http-get`, `https-get`, `dns`. Scripts run as a restricted internal user with
only `read`, `write`, `test`, `reboot` policies and have private globals. ICMP probes have default thresholds (for example `thr-avg=100ms`), so
a slow link reports down. `http-get` is down on a redirect unless `http-codes=100-399`. After a reboot probes wait `startup-delay` (5 m).

## SNMP

```ros
/snmp/set enabled=yes contact="NOC" location="Server room"
/snmp/community/add name=monit addresses=192.0.2.0/24 security=none read-access=yes
/snmp/community/set [find name=public] addresses=192.0.2.0/24     # or remove it
/snmp/set trap-target=192.0.2.50 trap-community=monit trap-version=2 trap-generators=interfaces
```

The default `public` community is readable from any address. `security=authorized|private` means SNMPv3 (v1/v2c polls get no reply), with
passwords of at least 8 characters. A request from outside `addresses` gets no answer. `write-access=yes` allows changing the identity,
running scripts and rebooting: only on v3 or a narrow subnet. `print oid` at any menu lists OIDs. Test with `/tool/snmp-get`.

## Flow export, graphs, resources

```ros
/ip/traffic-flow/set enabled=yes
/ip/traffic-flow/target/add dst-address=192.168.0.2 port=2055 version=9
/ip/traffic-flow/monitor duration=3
/tool/graphing/interface/add interface=ether1 allow-address=192.168.88.10/32
/tool/graphing/resource/add allow-address=192.168.88.10/32
/system/resource/print
/tool/profile cpu=all freeze-frame-interval=1 duration=5
```

- Traffic Flow exports NetFlow v1, v5, v9 or IPFIX over UDP; hardware-offloaded traffic is not counted. Graphs live at `http://router/graphs/`
  with no login: always set `allow-address` (default is every IPv4 address) and keep the page off WAN.
- Interface counters: `/interface/print stats`, `monitor-traffic`, and `/tool/traffic-monitor` to run a script when a rate crosses a threshold.
  Rising regular counters with flat `fp-*` counters mean traffic leaves the fast path.
- Health (`/system/health`) shows temperature, voltage, fans; threshold traps need `trap-generators=temp-exception`.

## Throughput tests

`/tool/speed-test address=<peer> test-duration=5s` (latency, jitter, TCP and UDP both ways) and `/tool/bandwidth-test` need a RouterOS peer
with `/tool/bandwidth-server` on, a user in a group with the `test` and `winbox` policies, device mode `bandwidth-test` enabled, TCP 2000 and
UDP 2000-65535 allowed, and for UDP receive the client must accept the server's packets. Limit `local-tx-speed` and `remote-tx-speed` on
live links. Remove the test user and firewall rules afterwards. `flood-ping` and the traffic generator need the `traffic-gen` device-mode flag.

## Watchdog and Detect Internet

`/system/watchdog` reboots a hung router (`watchdog-timer=yes`) and, when `watch-address` is set, a router whose uplink address stops
answering six pings. Pick an address inside the tunnel or on the far side of the link, set `ping-start-after-boot` longer than the link needs,
and keep another way in: a bad address means a reboot every few minutes. `/interface/detect-internet` fills dynamic lists (`internet`, `wan`,
`lan`) from route and MikroTik cloud checks; the lists change by themselves, so do not use them in accept rules.

## Where to look

| Need | Open |
| --- | --- |
| Log topics list, TLS syslog, disk files, script actions | `references/guides/diagnostics-monitoring-and-troubleshooting/log.md` |
| Ping, traceroute, torch, sniffer | `ping.md`, `traceroute.md`, `torch.md`, `packet-sniffer.md` in the same folder |
| Netwatch, SNMP, traffic flow, graphing | `netwatch.md`, `snmp.md`, `traffic-flow.md`, `graphing.md` |
| Bandwidth test, speed test, traffic generator | `bandwidth-test.md`, `speed-test.md`, `traffic-generator.md` |
| Resource, profiler, health, watchdog, detect internet | `resource.md`, `profiler.md`, `health.md`, `watchdog.md`, `detect-internet.md` |
| Properties | `references/cli/tool/`, `references/cli/system/logging/`, `references/cli/snmp/`, `references/cli/ip/traffic-flow/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-troubleshooting` (supout.rif and support), `routeros-system-utilities` (clock, scheduler, email), `routeros-firewall`
(counters, logging rules), `routeros-scripting`, `routeros-hardware` (sensors and PoE), `routeros-queues` (graphing queues).
