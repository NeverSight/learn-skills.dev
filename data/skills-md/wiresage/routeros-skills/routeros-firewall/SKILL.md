---
name: routeros-firewall
description: Writing and reviewing the MikroTik RouterOS firewall. Covers the filter, NAT, mangle and raw tables and their chains, packet flow, connection tracking and states, FastTrack, address lists, IPv6 filtering, port forwarding, masquerade versus src-nat, safe rule ordering for the input chain, brute-force and DoS protection recipes, and UPnP, NAT-PMP and Kid Control. Use when adding, ordering, debugging or auditing firewall or NAT rules, publishing a service, blocking addresses, protecting the router or LAN, or when traffic is unexpectedly dropped or not translated.
---

# RouterOS firewall

The firewall is four rule tables (filter, NAT, mangle, raw) evaluated at fixed points of the packet path. Rules in a chain
run top to bottom and the first matching terminal action wins, so **order is the configuration**. IPv4 lives under
`/ip/firewall`, IPv6 under `/ipv6/firewall`; they are separate tables with separate address lists.

## Know where each table acts

Path of a routed packet: raw prerouting, connection tracking, mangle prerouting, **dstnat**, routing decision, mangle forward,
**filter forward**, mangle postrouting, **srcnat**, queues. A packet for the router itself goes to mangle input and **filter
input** instead of forward; a packet from the router goes through raw/mangle/filter output. Consequences:

- Filter `input` protects the router, `forward` protects what is behind it, `output` rarely needs rules.
- A dstnat rule rewrites the destination before the forward chain, so forward rules must match the translated (inner) address.
- NAT sees only the first packet of a connection; connection tracking applies the result to the rest. After you add or change
  NAT rules, existing connections keep the old behaviour until they expire or you clear them (`/ip/firewall/connection/remove
  [find]` drops all tracked sessions, including your own SSH session if it is tracked; ask first).
- Raw rules run before connection tracking: use them to drop floods early or to exclude traffic with `action=notrack`. They
  cannot match on connection state or layer7.
- Mangle only marks and rewrites headers (connection, packet and routing marks, DSCP, TTL, MSS). Marks exist only inside the
  router; at most 4096 packet marks.
- Detail and diagrams: `references/guides/firewall-and-quality-of-service/packet-flow-in-routeros.md`.

## Connection tracking and states

States: `new`, `established`, `related`, `invalid`, `untracked`. The first rules of a chain should accept
`established,related,untracked` and drop `invalid`, so the rest of the chain only handles new connections. Do not drop
`invalid` on routers with asymmetric routing: legitimate packets look invalid there.

**FastTrack** (`action=fasttrack-connection` on established/related in `forward`, followed by an identical accept rule) sends
packets of a connection around the firewall, connection tracking, simple queues, queue trees with `parent=global`, IPsec policies
and more. Anything that must see every packet (queues, mangle, accounting, filter rules) is not applied to FastTracked traffic.
Details and conditions: `references/guides/firewall-and-quality-of-service/connection-tracking.md`.

## A safe input chain

Do not drop traffic until the accept rules for your own access exist, and put new rules before the catch-all drop with
`place-before` (a plain `add` appends after it, where it never matches). The default configuration has a rule with the comment
`defconf: drop all not coming from LAN`; look at the real chain first:

```ros
/ip/firewall/filter/print                 # find the rule order and the defconf comments
/ip/firewall/filter/print stats           # bytes and packets per rule (shows what is actually matching)
```

Skeleton for a router without a firewall (interface list `LAN` holds the trusted ports; add your management source first):

```ros
/interface/list/add name=LAN
/interface/list/member/add list=LAN interface=bridge1
/ip/firewall/filter
add chain=input action=accept connection-state=established,related,untracked comment="accept established,related,untracked"
add chain=input action=drop connection-state=invalid comment="drop invalid"
add chain=input action=accept protocol=icmp comment="accept ICMP"
add chain=input action=accept in-interface-list=LAN comment="accept from LAN"
add chain=input action=drop comment="drop everything else"
```

For a forward chain use the same first two rules, then accept what should cross (LAN to WAN), accept dst-natted connections
(`connection-nat-state=dstnat`), and drop the rest. Interface lists (`in-interface-list=WAN`) survive interface changes better
than interface names. When the session itself depends on the rule you are about to change, work in safe mode or schedule a
rollback (`routeros-fundamentals`).

## NAT

```ros
# Internet access for the LAN. masquerade when the public address can change (DHCP, PPPoE, LTE)
/ip/firewall/nat/add chain=srcnat out-interface-list=WAN ipsec-policy=out,none action=masquerade
# Fixed public address: src-nat keeps tracking entries across a link flap
/ip/firewall/nat/add chain=srcnat src-address=10.0.0.0/24 out-interface=WAN action=src-nat to-addresses=203.0.113.10
# Publish a service (destination NAT), optionally limited to a source
/ip/firewall/nat/add chain=dstnat action=dst-nat protocol=tcp dst-port=443 in-interface-list=WAN to-addresses=192.168.88.10 to-ports=443
```

A published service also needs an accept rule in the `forward` chain when that chain drops by default. Masquerade clears
the tracked connections of an interface when it goes down or its address changes; with unstable links and failover this can
leak private addresses, so see the blackhole-route advice in the NAT guide. RouterOS has no NAT64; v7 has IPv6 NAT. In v7 NAT
also has `input` and `output` chains for traffic to and from the router itself.

## Address lists

A named set of addresses, prefixes, ranges (IPv4) or DNS names that filter, NAT, mangle and raw rules match with
`src-address-list` and `dst-address-list` (`!` negates). Rules can fill lists dynamically with
`action=add-src-to-address-list address-list=NAME address-list-timeout=1h`. A DNS name in a list is resolved by the router and
shown as a dynamic entry. Blocking by list is cheapest in raw:

```ros
/ip/firewall/address-list/add list=blocked address=203.0.113.0/24 comment="abuse reports"
/ip/firewall/raw/add chain=prerouting action=drop in-interface-list=WAN src-address-list=blocked
```

Duplicate entries fail (`already have such entry`), which stops an `.rsc` import. For IPv6 list whole prefixes (/64 or larger).

## IPv6

IPv6 clients are normally reachable from outside because there is no NAT, so a forward filter is mandatory, not optional.
Allow `icmpv6` (IPv6 needs it), established/related, then new connections from the LAN only, and drop the rest. In `input`,
allow link-local DHCPv6 and traceroute ports as the guide shows. Complete examples:
`references/guides/firewall-and-quality-of-service/firewall/filter.md`.

## Brute force, DoS, port knocking

Prefer not exposing management services at all (use a VPN). If SSH must be reachable, `/ip/ssh/set password-authentication=no`
with key login removes password guessing. The brute-force guide counts new connections per source through staged address lists
and blocks the fourth within an hour; the DDoS guide, connection-rate, port-knocking and advanced-firewall pages are in
`references/guides/firewall-and-quality-of-service/user-guides/`. Logging with `log=yes log-prefix=...` costs CPU under attack.

## Debugging checklist

1. `print stats` on the table: is the counter of the expected rule moving?
2. Is a rule above it matching first? Is the rule disabled (`X`) or invalid (`I`)?
3. For NAT: is the connection older than the rule? Is `out-interface` the real egress (PPPoE, LTE, VLAN)?
4. `/ip/firewall/connection/print where dst-address~"192.0.2."` shows how the router tracked the flow and whether it was NATed
   or FastTracked.
5. Add a temporary `action=log` rule or use `/tool/torch` and `/tool/sniffer` (`routeros-diagnostics-monitoring`).

## Where to look

| Need | Open |
| --- | --- |
| Filter rules and the example rule sets | `references/guides/firewall-and-quality-of-service/firewall/filter.md` |
| NAT types, masquerade, CGNAT, helpers | `references/guides/firewall-and-quality-of-service/firewall/nat.md` |
| Matchers and actions shared by all tables, stats | `references/guides/firewall-and-quality-of-service/firewall/common-firewall-matchers-and-actions.md` |
| Mangle, MSS clamping, marks | `references/guides/firewall-and-quality-of-service/firewall/mangle.md` |
| Address lists (timeouts, DNS names) | `references/guides/firewall-and-quality-of-service/firewall/address-lists.md` |
| Layer7 matching | `references/guides/firewall-and-quality-of-service/firewall/layer7.md` |
| Every property of a table | `references/cli/ip/firewall/` and `references/cli/ipv6/firewall/` |
| Kid Control, UPnP, NAT-PMP | `references/guides/firewall-and-quality-of-service/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-queues` (marks feed queues), `routeros-routing` (policy routing uses routing marks),
`routeros-vpn`, `routeros-ipsec`, `routeros-initial-setup` (default configuration), `routeros-hotspot`.
