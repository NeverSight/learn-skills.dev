---
name: routeros-ospf
description: Configuring and troubleshooting OSPF (v2 for IPv4, v3 for IPv6) on MikroTik RouterOS 7. Covers instances, areas and area types (standard, stub, totally stubby, NSSA), interface templates, network types (broadcast, point-to-point, NBMA, point-to-multipoint), cost, passive interfaces, authentication, redistribution through routing filters, default route origination, BFD, virtual links, route summarization, and neighbours stuck in Init or flapping. Use when bringing up OSPF between routers, redistributing routes, designing areas, migrating OSPF from v6, or when adjacencies or routes are missing.
---

# RouterOS OSPF

In RouterOS 7 OSPFv2 and OSPFv3 share one menu, `/routing/ospf`. There is **no default instance and no default area**: you create an
instance (one per version), add an area to it, then tell the router on which interfaces to run OSPF with an **interface template**.
Templates only match; `/routing/ospf/interface` and `/routing/ospf/neighbor` are read-only status.

```ros
/routing/ospf/instance/add name=v2inst version=2 router-id=10.255.0.1
/routing/ospf/area/add name=backbone area-id=0.0.0.0 instance=v2inst
/routing/ospf/interface-template/add area=backbone networks=192.168.0.0/24 type=broadcast
/routing/ospf/interface-template/add area=backbone interfaces=lo passive            # advertise a loopback without hellos
/routing/ospf/neighbor/print
/routing/ospf/interface/print
/ip/route/print where ospf
```

- The matchers are `networks=` (every interface with an address inside) and `interfaces=` (names or an interface list). The overview
  page writes `network=`; the property is `networks`.
- Give every router a unique `router-id` (an IP-formatted ID, normally a loopback address). Duplicates are the first cause of
  neighbours stuck in Init or flapping.
- For IPv6 run a version 3 instance with its own area and template; the area ID is the same notation as for v2.

## Interface settings that matter

| Property | Use |
| --- | --- |
| `type` | `broadcast` (Ethernet, elects DR/BDR), `ptp`, `ptp-unnumbered`, `nbma`, `ptmp`, `ptmp-broadcast`. Use `ptp` on routed point-to-point links to skip DR election; use NBMA or PTMP where multicast is unreliable |
| `cost` | Output metric; derive it from link speed so that the intended path wins |
| `passive` | No OSPF traffic on the matching interfaces; still advertises their prefix. Use it on LAN-facing ports |
| `hello-interval`, `dead-interval` | Must match on both ends |
| `auth`, `auth-key`, `auth-id` | `simple`, `md5` or `sha1..sha512` authentication; same key and ID on all routers of the segment |
| `priority` | DR election on broadcast networks; 0 means never DR |
| `use-bfd` | Fast failure detection with a BFD session (`/routing/bfd/configuration`) |

## Areas

`type=default` is a standard area; `stub` blocks external LSAs; `nssa` allows a local ASBR in a stub-like area; `no-summaries` makes a
stub totally stubby. The backbone `0.0.0.0` must exist and every other area must connect to it, directly or through a virtual link. An
ABR summarises between areas. The guide explains LSA types, stub, totally stubby and NSSA behaviour, default-route injection and
virtual links with examples (`areas-and-virtual-links.md`).

## Redistribution and default route

v7 has no separate "redistribute with filter" menu: select what to import with `redistribute=` on the instance and decide inside a
routing filter chain. The default action of a filter chain is `reject`, so end the chain with `accept`.

```ros
/routing/ospf/instance/set v2inst redistribute=static out-filter-chain=ospf_out originate-default=if-installed
/routing/filter/rule/add chain=ospf_out rule="if (protocol static && dst in 192.168.0.0/16) { accept }"
```

`originate-default` is `never`, `always` or `if-installed`. Filters are covered in `routeros-routing`.

## When the adjacency does not come up

1. `router-id` is not unique.
2. A firewall drops OSPF (IP protocol 89) or the multicast addresses it uses, or NAT rewrites the packets. Accept protocol `ospf` in
   `input` and, with connection tracking trouble, exempt it with raw `action=notrack` for prerouting and output (the manual's raw example).
3. Hello and dead intervals, area ID, authentication, MTU or network type differ between neighbours.
4. An L2 device blocks multicast, or the link is wireless: switch the template to `nbma` and configure neighbours, or use `ptmp`.
5. The interface is covered by no template or by one for the wrong area; check `/routing/ospf/interface/print`.
6. States: Down, Init (hello seen one way), 2-Way, ExStart, Exchange, Loading, Full; stuck in ExStart or Exchange is usually an MTU mismatch.

Process-level status for all routing protocols: `/routing/stats/process/print`.

## Migrating from v6

v6 `/routing ospf` and `/routing ospf-v3` became `/routing/ospf` with `version=2|3`; v6 `network` statements became interface
templates; instances and areas must be created explicitly; the configuration upgrade from v6 converts known setups automatically
and runs once (`routeros-install-upgrade`).

## Where to look

| Need | Open |
| --- | --- |
| Configuration overview and redistribution | `references/guides/user-guides/routing-and-networking-protocols/unicast/ospf.md` |
| Concepts and terminology | `.../ospf/understanding-ospf.md` |
| Neighbour discovery, DR election, database synchronisation | `.../ospf/neighbour-relationship.md` |
| Areas, LSA types, summarisation, virtual links | `.../ospf/areas-and-virtual-links.md` |
| SPF and route calculation | `.../ospf/routing-calculation.md` |
| Flapping neighbours | `.../ospf/faq.md` |
| Properties of `/routing/ospf/*` | `references/cli/routing/ospf/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-routing` (filters, router ID, BFD), `routeros-bgp`, `routeros-mpls` (LDP uses an IGP), `routeros-firewall`.
