---
name: routeros-routing
description: IP routing on MikroTik RouterOS 7. Covers the routing table and route selection, static routes and default gateways, gateway checks and failover by distance, ECMP, blackhole routes, recursive gateways and scope and target-scope, custom routing tables, routing rules and mangle-based policy routing, VRF and VRF-lite, script-style route filters, router ID, BFD, RIP, IS-IS, IGMP proxy and PIM-SM multicast, routing multi-core behaviour, and migrating routing configuration from v6 to v7. Use when adding or debugging routes, steering traffic over several uplinks, isolating networks with VRFs, writing route filters, or when a destination is unreachable although a route exists.
---

# RouterOS routing

In RouterOS 7 routes live in routing **tables**; `main` is the default one. The router builds a RIB (all candidate routes), picks the
best route per destination (lowest `distance` among reachable candidates), and installs it in the FIB used for forwarding. OSPF, BGP
and MPLS have their own skills (`routeros-ospf`, `routeros-bgp`, `routeros-mpls`); this one covers everything they share.

## Static routes and gateway checks

```ros
/ip/route/print where dst-address=0.0.0.0/0
/ip/route/add dst-address=0.0.0.0/0 gateway=192.0.2.1 distance=1 check-gateway=ping comment=primary
/ip/route/add dst-address=0.0.0.0/0 gateway=198.51.100.1 distance=2 comment=backup
/ip/route/add dst-address=203.0.113.0/24 blackhole
```

- A route is a candidate only if it is enabled and its gateway is reachable. `gateway` may be an address, an interface name, or
  `address%interface`. `gateway=192.0.2.1@main` resolves the gateway in another table.
- Failover is by distance: the backup is used when the preferred route becomes inactive. A dead next hop on an Ethernet link is
  not detected without `check-gateway` (`ping`, `arp` or `bfd`; probes every 10 seconds, the gateway is considered down after two
  timeouts). See also `routeros-high-availability`.
- Equal-cost routes with the same distance form an **ECMP** group (flag `+`); the hash uses layer 3 by default and can be changed
  in `/ip/settings` and `/ipv6/settings` to layer 4 or inner layer 3.
- Connected routes are created from `/ip/address`; their preferred source is chosen from the outgoing interface.
- `scope` and `target-scope` restrict which routes may resolve a gateway (a route whose scope is above the target-scope is not used).
  Defaults only allow connected routes, except iBGP, which may also resolve through IGP and static routes. Check actual values in
  `/routing/nexthop`. Changing them on one route does not affect others because they belong to the nexthop object.
- Never remove or replace the default route over the session you are using; add the new route first, test, then remove the old.

## Several tables, rules and policy routing

Create a table before you reference it, with `fib` if it should install routes for forwarding. Then steer traffic with routing rules or
with mangle, not both:

```ros
/routing/table/add name=wan2 fib
/ip/route/add dst-address=0.0.0.0/0 gateway=198.51.100.1 routing-table=wan2
/routing/rule/add src-address=192.168.88.50/32 action=lookup table=wan2
/routing/rule/add dst-address=8.8.8.8 action=lookup-only-in-table table=wan2
```

- `lookup` falls back to `main` when the table has no match, `lookup-only-in-table` does not (the destination becomes unreachable when
  the gateway fails), `drop` and `unreachable` discard.
- Mangle (`mark-routing`) runs before routing rules and wins when both match. A mangle rule that also marks traffic to the router's
  own addresses breaks local access: add `!dst-address-type=local` or move the `action=mangle` rule below `lookup table=local`
  in `/routing/rule`.
- Up to 4096 tables. Rules replace the v6 `/ip route rule` menu.
- Multi-WAN load balancing and failover patterns: `routeros-high-availability` (PCC and WAN backup).

## VRF

A VRF is created in `/ip/vrf` with a list of interfaces; each active VRF gets a routing table of the same name. Entries match top-down
like firewall rules and the built-in `main` VRF matches all interfaces, so move your VRF above it (`move 1 0`). Connected routes of the
interfaces land in the VRF table. Services only use a VRF if they support it and you configure it (for example SSH `vrf=`, WireGuard
`vrf=`). Route leaking, VPNv4 and route targets: `references/guides/user-guides/routing-and-networking-protocols/vrf.md`
and `route-distinguisher-and-route-target.md`.

## Route filters (v7 syntax)

Filters are script-like rules in named chains; protocols reference the chain as input or output filter. The default action at the end
of a chain is `reject`, so end useful chains with an explicit `accept`.

```ros
/routing/filter/rule/add chain=ospf_in rule="if (dst==0.0.0.0/0 && protocol static) { accept }"
/routing/filter/rule/add chain=bgp_out rule="if (dst-len>13 && dst-len<31 && dst in 172.16.0.0/16) { set bgp-med 20; set bgp-path-prepend 2; accept }"
```

Readable-only properties (`dst`, `dst-len`, `protocol`, `bgp-as-path`, `rpki`, `ospf-type`, `origin` ...) can only be matched; writable ones
(`distance`, `bgp-med`, `bgp-local-pref`, `bgp-path-prepend`, communities, ...) can also be set. Prefix lists from v6 are gone. Full property
tables: `references/guides/user-guides/routing-and-networking-protocols/route-selection-and-filtering.md`. Test filters on a lab or with
`/routing/filter/test-as-path-regexp` before putting them on a production BGP session.

## Other protocols in this skill

- **RIP**: v2 only. `/routing/rip/instance/add name=r1 redistribute=connected,static`, then
  `/routing/rip/interface-template/add instance=r1 interfaces=ether1` (no network statements in v7; neighbours appear only when there
  are routes to exchange).
- **IS-IS**: `/routing/isis/instance/add name=i1 afi=ip areas=49.2222 system-id=1111.2222.cded` and
  `/routing/isis/interface-template/add instance=i1 interfaces=ether1 levels=l1,l2`.
- **BFD**: `/routing/bfd/configuration` selects interfaces or addresses; enable it per protocol with `use-bfd=yes` (BGP connection,
  OSPF interface template) and check `/routing/bfd/session`.
- **Multicast**: IGMP proxy (`/routing/igmp-proxy/interface` with one `upstream=yes`), PIM-SM (`/routing/pimsm`, no separate package in v7).
- **Router ID**: `/routing/id` elects or sets it for all protocols.
- **Multi-core**: BGP and routing table updates run in parallel; see `routing-protocol-multi-core-support.md`.

## From v6 to v7

Tables must exist in `/routing/table` before use; `/ip route rule` became `/routing/rule`; the Rules, VRF and Nexthop tabs left the IP
route menu (`/routing/rule`, `/ip/vrf`, `/routing/nexthop`); BGP, OSPF and filters were redesigned (see their skills); PIM-SM configuration
is not converted. Full examples and the nexthop lookup change: `moving-from-rosv6-to-rosv7.md`.

## Where to look

| Need | Open |
| --- | --- |
| RIB, FIB, ECMP, route selection, scope, hardware offload | `references/help/ip-routing.md` and `references/guides/user-guides/routing-and-networking-protocols/routing-decision.md` |
| Policy routing with tables and rules | `references/guides/user-guides/routing-and-networking-protocols/policy-routing.md` |
| Overview of routing feature status by protocol | `references/help/routing-protocol-overview.md` |
| Filters | `references/guides/user-guides/routing-and-networking-protocols/route-selection-and-filtering.md` |
| Properties of `/ip/route`, `/routing/*` | `references/cli/ip/route.md`, `references/cli/routing/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-ospf`, `routeros-bgp`, `routeros-mpls`, `routeros-firewall` (mangle), `routeros-high-availability`,
`routeros-ip-addressing`, `routeros-vpn`.
