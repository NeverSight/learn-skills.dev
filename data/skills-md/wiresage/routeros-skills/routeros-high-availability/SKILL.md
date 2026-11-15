---
name: routeros-high-availability
description: High availability and redundancy on MikroTik RouterOS 7. Covers VRRP (virtual IP, IPv4 and IPv6, priority, preemption, authentication, connection tracking sync, group authority for LAN and WAN pairs), bonding (802.3ad LACP, balance-xor, active-backup and other modes, ARP and MII link monitoring, transmit hash policy, hardware offload), MLAG across two switches with ICCP, WAN failover with check-gateway and recursive routes, per-connection load balancing with PCC, ECMP and Nth. Use when two routers must share a gateway address, when a link or uplink must fail over automatically, when aggregating ports, or when spreading connections over several WANs.
---

# RouterOS high availability

Pick the mechanism by what must survive: a router (VRRP), a cable or port (bonding), a switch (MLAG), an uplink (failover routes), or you
want to use several uplinks at once (load balancing). Test every design by unplugging things.

## VRRP: shared gateway address

```ros
# router 1 (higher priority becomes master)
/ip/address/add address=192.168.1.2/24 interface=ether1
/interface/vrrp/add name=vrrp1 interface=ether1 vrid=1 priority=200
/ip/address/add address=192.168.1.1/32 interface=vrrp1
# router 2
/ip/address/add address=192.168.1.3/24 interface=ether1
/interface/vrrp/add name=vrrp1 interface=ether1 vrid=1 priority=100
/ip/address/add address=192.168.1.1/32 interface=vrrp1
```

- Clients use the virtual address (192.168.1.1) as gateway. RouterOS implements VRRPv2 and v3 (protocol 112, multicast 224.0.0.18 or
  FF02::12, TTL 255). Defaults: `vrid=1`, `priority=100`, `authentication=none`. Same `vrid`, same virtual addresses and the same advertisement
  `interval` on all members, or advertisements are dropped. Keep the same RouterOS version on the members.
- RouterOS cannot be the "owner" (priority 255); use a pure virtual address. The address on the VRRP interface needs `/32` when its subnet
  also exists on another interface. The virtual MAC is `00:00:5E:00:01:<VRID>` and cannot be changed; only the master answers ARP for it.
- A higher-priority backup takes over again when `preemption-mode` is on. Turn it off to avoid flapping back. Intervals below 1 s give
  unpredictable master changes. Use `authentication=ah` when you do not control the segment (`simple` only guards against mistakes).
- IPv6: `version=3 v3-protocol=ipv6` and an address with `advertise=yes` on the VRRP interface.
- `on-master`, `on-backup`, `on-fail` run scripts on state changes (`routeros-scripting`); `/log` topic `vrrp`.
- **Connection tracking sync:** `/interface/vrrp/set vrrp1 sync-connection-tracking=yes` (and tracking enabled) copies entries from master to
  backup so that sessions survive failover. With several VRRP interfaces between two units enable it on one only, ideally the `group-authority`.
- **LAN and WAN VRRP pairs with NAT:** group them so both are master or backup together:
  `/interface/vrrp/set [find] group-authority=vrrp-lan`. Only the authority sends advertisements.
- VRRP advertisements are IP protocol 112 sent to the router itself, so a restrictive input chain must not drop them (`routeros-firewall`).

## Bonding (link aggregation)

```ros
/interface/bonding/add name=bond1 slaves=ether1,ether2 mode=802.3ad lacp-rate=1sec transmit-hash-policy=layer-2-and-3
/ip/address/add address=172.16.0.1/24 interface=bond1          # no addresses on the slaves
/interface/bonding/monitor [find]
```

- Bonding does not create a faster single link: it spreads flows. One TCP stream still uses one member (except `balance-rr`).
- **Always enable link monitoring**: without it a failed member keeps receiving traffic. `link-monitoring=mii` reacts to local link state;
  `arp` (with `arp-ip-targets`, ideally several, `arp-interval`) checks reachability end to end but does not work when two routers are directly
  connected back to back (use `mii` or put a switch between). ARP probes go untagged.
- Modes: `802.3ad` (LACP, needs the peer in LACP mode, all members same speed), `balance-xor` (static LAG), `active-backup` (best for two switches
  without MLAG, `primary` chooses the preferred member), `balance-rr` (only mode that splits one connection over members; reordering risk),
  `broadcast`, `balance-tlb`, `balance-alb`.
- Hardware offload in bridges only for `802.3ad`, `balance-xor` and `active-backup` on supported chips (Prestera, 88E6393X, 88E6191X, 88E6190);
  other modes use the CPU. Prestera uses layer-2+3+4 hashing, the 88E6 chips layer-2 only, regardless of `transmit-hash-policy`. `layer-3-and-4`
  is not fully LACP compatible.
- A bond takes a few seconds to come up. MTU must not exceed the smallest member L2MTU (`routeros-ethernet`).

## MLAG

Two switches present one LACP partner to a client. Create a bond with the same `mlag-id` on both peers, enable it on the bridge with
`vlan-filtering=yes mlag-peer-port=<port>` and `mlag-priority` (lower is primary), and make the peer port a tagged member of every VLAN that spans
both switches. ICCP runs as untagged layer 2 over the peer port (EtherType 0x88B5), no IP needed. Use identical STP settings on both peers
(same bridge priority, `edge=yes` on dual-attached ports with no other bridges). Software MLAG works on any RouterOS device; hardware offload needs
Prestera; L3 hardware offload must be off. Large host tables load single-core MIPSBE switches (about 1000 hosts is the stated limit). Details
and VLAN examples: `references/guides/high-availability-solutions/multi-chassis-link-aggregation-group.md`.

## WAN failover and load balancing

| Goal | Method |
| --- | --- |
| Backup uplink | Two default routes with different `distance`, `check-gateway=ping` on the preferred one |
| Reliable detection | Recursive routes: host routes to monitored addresses with `scope=10`, default routes via those hosts with `target-scope=11 check-gateway=ping` |
| Equal use of links | ECMP: several default routes with the same distance (per connection) |
| Weighted per-connection spread | Mangle with `per-connection-classifier` (PCC) marking connections, routing marks to per-ISP tables |
| Per-packet spread | Mangle `nth` or bonding, only when both ends are yours |

```ros
/ip/route/add gateway=192.168.1.1 distance=1 check-gateway=ping
/ip/route/add gateway=192.168.2.1 distance=2
```

Masquerade out of every uplink (`routeros-firewall`). The recursive design: `dst-address=8.8.8.8 scope=10 gateway=<ISP1 gw>` and a second host via ISP2,
then `gateway=8.8.8.8 distance=1 target-scope=11 check-gateway=ping` and the same for the second host at `distance=2`; two monitored hosts per link
make the check tolerate one outage, and failover is complete only when all of a link's hosts are unreachable. PCC syntax is
`[!]<fields>:<denominator>/<remainder>` (for example `both-addresses-and-ports:3/0`); it only matches, routing marks do the steering. Always accept
traffic to directly connected ISP subnets in mangle before PCC rules to avoid loops, and PCC does not work with HotSpot. Full examples:
`load-balancing/per-connection-classifier.md`, `load-balancing/failover-wan-backup.md`.

## Where to look

| Need | Open |
| --- | --- |
| VRRP state machine, groups, tracking sync, IPv6 | `references/guides/high-availability-solutions/vrrp.md` |
| VRRP examples (master and backup, load sharing) | `.../user-guides/vrrp-configuration-examples.md` |
| Bonding modes, monitoring, hash policy | `.../bonding.md`, `.../user-guides/bonding-examples.md` |
| MLAG | `.../multi-chassis-link-aggregation-group.md` |
| Failover and PCC | `.../load-balancing.md`, `.../load-balancing/` |
| Properties | `references/cli/interface/vrrp.md`, `references/cli/interface/bonding.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-routing` (distance, scope, check-gateway, ECMP, routing tables), `routeros-firewall` (mangle, protocol 112),
`routeros-bridging-switching` (STP, VLANs, hardware offload), `routeros-switch-chip` (hardware bonding and MLAG limits), `routeros-ethernet`, `routeros-diagnostics-monitoring` (Netwatch for custom failover).
