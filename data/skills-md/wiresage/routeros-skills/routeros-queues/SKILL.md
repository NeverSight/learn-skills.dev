---
name: routeros-queues
description: Bandwidth limiting and quality of service on MikroTik RouterOS. Covers simple queues, queue trees, the HTB model (limit-at, max-limit, priority, parent), queue types (PFIFO, BFIFO, SFQ, RED, PCQ, CoDel, FQ-CoDel, CAKE), bursts, queue size, interface queues, and how queues interact with FastTrack and mangle packet marks. Use when limiting or guaranteeing bandwidth for hosts or networks, sharing a link fairly, fighting bufferbloat, prioritising traffic, or when a queue shows no traffic or limits the wrong direction.
---

# RouterOS queues

Queues in RouterOS are built on HTB (Hierarchical Token Bucket). Two menus configure them: `/queue/simple` for everyday
per-target limits, and `/queue/tree` for one-directional queues on marked traffic or on a specific interface. Packet scheduling
inside a queue is decided by its **queue type** (`/queue/type`). Queues only act on traffic that reaches them: see "Why a queue
does nothing" below.

## Choose the tool

| Goal | Use |
| --- | --- |
| Limit or guarantee one host or subnet (upload and download) | Simple queue |
| Share a link equally among many hosts with little administration | Simple queue or tree with a PCQ type |
| Reduce latency under load on a shared uplink (bufferbloat) | `fq-codel` or `cake` queue type on a queue |
| Global priority policy, limits per application or per user group | Queue tree with mangle packet marks |
| One queue on a specific interface (for example WAN egress) | Queue tree with `parent=<interface>` |

Rates: `limit-at` (CIR, guaranteed) and `max-limit` (MIR, ceiling). In a simple queue every pair is **upload/download** from the
target's point of view: `max-limit=20M/100M` means 20 Mbit/s up, 100 Mbit/s down. Keep the sum of children's `limit-at` at or
below the parent's `max-limit`, and every child's `max-limit` at or below the parent's.

## Simple queue

```ros
/queue/simple/add name=office target=192.168.88.0/24 max-limit=20M/100M
/queue/simple/add name=server target=192.168.88.251/32 limit-at=5M/5M max-limit=15M/15M
/queue/simple/print stats
```

- Simple queues are checked **in order**; a packet is served by the first queue that fits. Put specific queues before general
  ones and keep the list short (a packet for the last of 1000 queues passes 999 others).
- The target decides direction: a source address matching the target is upload, a destination address matching it is download.
  If both match, the packet counts as download. Do not let a flow match the target in both directions, and do not set `target`
  and `interface` to opposite directions.
- Children use `parent=<name>`; `priority` (1 highest, 8 lowest) only applies to leaf queues and decides who reaches
  `max-limit` first.
- Time-limited queues: `time=18h-23h,mon,tue,...` (needs a correct clock, see `routeros-system-utilities`).
- Marks from mangle must be set in `prerouting`, before the global-in HTB, or download limits by `packet-marks` will not work.

## Queue tree

```ros
/ip/firewall/mangle/add chain=forward action=mark-packet dst-address-list=Youtube in-interface-list=LAN new-packet-mark=pmark-Youtube passthrough=yes
/queue/tree/add name=Limiting-Youtube parent=global packet-mark=pmark-Youtube max-limit=5M
/queue/tree/print stats
```

A tree queue is one-directional and the tree is not ordered: all traffic passes it together. `parent=global` attaches to the
global HTB; an interface name attaches to that interface's egress (the only way to queue on a specific interface). Marking
connections first and then packets saves CPU (`mark-connection` once, `mark-packet` by connection mark); see
`routeros-firewall` for mangle.

## Queue types

```ros
/queue/type/add name=fq-codel-default kind=fq-codel
/queue/type/add name=cake-default kind=cake cake-bandwidth=0 cake-nat=yes
/queue/type/add name=PCQ_download kind=pcq pcq-rate=64000 pcq-classifier=dst-address
/queue/type/add name=PCQ_upload kind=pcq pcq-rate=32000 pcq-classifier=src-address
/queue/simple/add target=192.168.0.0/24 queue=PCQ_upload/PCQ_download
```

- A queue type is a template; creating one does nothing until a simple queue, tree entry or interface queue uses it
  (`queue=<up-type>/<down-type>` in simple queues).
- Kinds: `pfifo`, `bfifo`, `mq-pfifo` (plain FIFO, head-of-line blocking), `sfq` (stochastic fairness), `red`, `pcq`
  (per-connection equalising), `codel`, `fq-codel` (good default for latency and fairness), `cake` (per-host fairness,
  shaper, overhead compensation, DiffServ, ACK filter), `none`.
- With CAKE under HTB (simple queue or tree), keep `cake-bandwidth=0` so HTB sets the rate; set it only when CAKE should shape
  by itself, and then avoid a second HTB limit. Behind NAT set `cake-nat=yes`. Details and tuning table:
  `references/guides/firewall-and-quality-of-service/queues/queue-types/cake.md`.
- Default types: `default`, `ethernet-default` (pfifo 50), `wireless-default` and `hotspot-default` (sfq), `synchronous-default`
  (red), `pcq-upload-default`, `pcq-download-default`, `only-hardware-queue` (kind none: only the hardware ring buffer),
  `multi-queue-ethernet-default`, `default-small`. The improvement of the hardware-only types disappears when a tree entry uses
  that interface as `parent`.
- Queue size decides drop versus delay: with no buffer everything over the rate is dropped (a "100% shaper", no added delay),
  with an unlimited buffer nothing is dropped but packets wait (a "100% scheduler"). The size is a property of the queue type
  (for example `pfifo-limit`, `pcq-limit`). See `queues/queue-size.md`.

## Why a queue does nothing

1. **FastTrack.** FastTracked traffic bypasses simple queues and queue trees with `parent=global`. Disable the FastTrack rule
   for the traffic you want to shape (or scope the rule), or queue on an interface (a tree entry with an interface parent is
   still applied).
2. Packets never reach it: wrong `target`, marks set in the wrong chain, `packet-mark` typo, a queue above it in the simple
   list catching the traffic first.
3. Direction mix-up (upload/download order), or both directions match the target.
4. `print stats` shows `bytes`, `packets`, `rate`, `queued-packets` and `dropped`; zero bytes means the traffic is not matched.
5. The CPU is the bottleneck: shaping happens in software; check `/system/resource/print` (`routeros-diagnostics-monitoring`).

## Bursts

`burst-limit`, `burst-time` (the averaging window, not the burst length) and `burst-threshold` let a flow exceed `max-limit`
briefly while its average rate is below the threshold. Set the threshold above `limit-at` and below `max-limit`. Full model and
worked examples: `references/guides/firewall-and-quality-of-service/queues/queue-burst.md`.

## Where to look

| Need | Open |
| --- | --- |
| Simple queue and queue tree properties, statistics, examples | `references/guides/firewall-and-quality-of-service/queues.md` |
| How HTB shares bandwidth between parents and children | `references/guides/firewall-and-quality-of-service/queues/htb-hierarchical-token-bucket.md` |
| PCQ walkthrough | `references/guides/firewall-and-quality-of-service/queues/pcq-example.md` |
| Queue type overview, FIFO kinds, CAKE | `references/guides/firewall-and-quality-of-service/queues/queue-types.md` and `queue-types/` |
| Every property of `/queue/*` | `references/cli/queue/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-firewall` (mangle marks, FastTrack), `routeros-switch-chip` (hardware QoS on switch chips),
`routeros-bridging-switching` (VLAN priority), `routeros-wireless`, `routeros-hotspot` (per-user rate limits).
