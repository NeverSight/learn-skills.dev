---
name: routeros-ip-addressing
description: IP addressing on MikroTik RouterOS 7. Covers IPv4 addresses and the connected routes they create, secondary addresses and unnumbered links, IP pools and used addresses, ARP (static entries, proxy ARP, reply-only, published entries), system-wide IP settings (forwarding, rp-filter, redirects, neighbor table size, ECMP hashing), IPv6 addresses (global, link-local, from a pool, EUI-64), router advertisements and SLAAC, neighbor discovery and RA proxying, and IPv6 settings. Use when assigning or fixing addresses, planning subnets, building IP pools, tuning ARP, enabling IPv6 on a LAN, or when hosts cannot reach the router or each other at Layer 3.
---

# RouterOS IP addressing

An address on an interface does two things: it makes the router reachable at that address, and it creates a **connected route** for the
network (flag `DAc`). If an expected connected route is missing, the address, its interface or the interface state is wrong. Addresses and
routes are separate lists, so check both (`/ip/address/print`, `/ip/route/print where connect`).

## IPv4

```ros
/ip/address/add address=192.168.88.1/24 interface=bridge1 comment=LAN
/ip/address/print detail
/ip/pool/add name=guests ranges=192.168.90.10-192.168.90.200
/ip/pool/used/print where pool=guests
```

- `address` is `host/prefix`; network and broadcast are derived. Put the address on the **bridge** (or VLAN interface), not on a port that
  is a bridge slave; `actual-interface` shows where it really lives. Several addresses on one interface are normal.
- Removing or disabling the address that carries your session cuts you off: add the new address first, reconnect on it, then remove the old
  one (`routeros-fundamentals`).
- Pools: comma-separated, non-overlapping ranges; exclude gateway and server addresses by leaving them out of the ranges. `next-pool`
  moves clients to another pool when one is full. The same client keeps the same address where possible. Consumers: DHCP servers (`routeros-dhcp`),
  PPP profiles (`routeros-vpn`), HotSpot (`routeros-hotspot`).
- `/ip/settings`: `ip-forward` (routing between interfaces, resets related options to defaults when toggled), `rp-filter` (`no`, `strict`,
  `loose`; strict breaks asymmetric routing), `send-redirects` (routers), `accept-redirects` (hosts, not routers), `accept-source-route`
  (leave off), `tcp-syncookies`, `max-neighbor-entries` (ARP table size, depends on RAM), `allow-fast-path`, ECMP hash policy
  (`ipv4-multipath-hash-policy`: `l3`, `l4`, `l3-inner`; see `routeros-routing`).

## ARP

```ros
/ip/arp/print
/ip/arp/add address=192.168.88.50 mac-address=AA:BB:CC:DD:EE:FF interface=bridge1
/interface/set bridge1 arp=reply-only        # only hosts with an ARP entry (static or DHCP-added) are answered
```

- Interface `arp` modes: `enabled`, `disabled`, `proxy-arp`, `local-proxy-arp`, `reply-only`. `reply-only` together with `add-arp=yes` on the
  DHCP server (a permanent ARP entry per bound lease, flag `H`) restricts a segment to leased hosts; hosts with static addresses then
  need ARP entries of their own.
- A `published` ARP entry makes the router answer for one address with its own MAC without enabling proxy ARP on the whole interface.
- Status values: `permanent`, `reachable`, `stale`, `delay`, `probe`, `incomplete`, `failed`. `incomplete` and `failed` mean the host does
  not answer: wrong VLAN or bridge membership, firewall on the host, or wrong subnet.
- Proxy ARP lets a router answer ARP for hosts behind it (hosts with a too-wide mask). Gratuitous ARP and the model of ARP in routed
  networks are explained in `references/guides/getting-started/networking-fundamentals.md`.

## IPv6

Every IPv6-capable interface gets a link-local address automatically; `/ipv6/settings` has the system-wide switches.

```ros
/ipv6/address/add address=2001:db8:1::1/64 interface=bridge1 advertise=yes      # advertise=yes sends the prefix in RAs (SLAAC)
/ipv6/address/add from-pool=isp-pd interface=bridge1 advertise=yes              # prefix taken from a delegated pool (routeros-dhcp)
/ipv6/settings/set accept-router-advertisements=yes                             # WAN side: learn address and default route via SLAAC
/ipv6/nd/set [find interface=bridge1] advertise-dns=yes dns=2001:db8::53 managed-address-configuration=no
/ipv6/neighbor/print
```

- Flags: `G` global, `L` link-local, `D` dynamic. An address added by SLAAC is dynamic and global, and the router also installs a default
  route towards the advertising router with the limits (hop limit, MTU) from the RA. `accept-router-advertisements` is `no`,
  `yes-if-forwarding-disabled` (the default behaviour for hosts) or `yes`.
- `advertise=yes` creates a dynamic `/ipv6/nd/prefix` entry; `/ipv6/nd` controls RA interval, lifetime, preference, MTU, the M and O flags
  for stateful DHCPv6, and DNS information (RDNSS). Use `/ipv6/nd/proxy` to relay ND where a segment cannot be routed.
- Pools (`/ipv6/pool`) hold prefixes handed out as `prefix-length` pieces; the DHCPv6 client fills them dynamically.
- IPv6 clients are globally reachable unless the firewall stops them: configure `/ipv6/firewall/filter` before you advertise a prefix
  (`routeros-firewall`).
- `disable-ipv6=yes` in `/ipv6/settings` turns IPv6 off for the whole system (also link-local generation).

## Where to look

| Need | Open |
| --- | --- |
| OSI/TCP-IP primer, IPv4 addressing, ARP and proxy ARP | `references/guides/getting-started/networking-fundamentals.md` |
| IPv6 address types, EUI-64, configuration, SLAAC | `references/guides/getting-started/networking-fundamentals/ipv6-addresses.md` |
| Neighbor discovery and RA examples | `references/guides/getting-started/networking-fundamentals/ipv6-neighbor-discovery.md` |
| Pools and used addresses | `references/help/ip-pools.md` and `references/cli/ip/pool.md` |
| Properties | `references/cli/ip/address.md`, `arp.md`, `settings.md`, `references/cli/ipv6/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-dhcp`, `routeros-routing`, `routeros-firewall`, `routeros-bridging-switching`, `routeros-ethernet`.
