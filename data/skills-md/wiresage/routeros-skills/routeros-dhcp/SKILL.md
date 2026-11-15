---
name: routeros-dhcp
description: DHCP on MikroTik RouterOS 7. Covers the DHCPv4 server (servers, pools, networks, leases, static leases, rate limits, options and option sets, DNS entries for clients, RADIUS, rogue-server alerts), the DHCPv4 client (default route, peer DNS and NTP, scripts for multi-WAN), DHCP relay, and DHCPv6 client and server with prefix delegation and router advertisements. Use when handing out or obtaining addresses, reserving an address for a host, sending custom options, relaying across routers, requesting an IPv6 prefix from an ISP, or when clients do not get an address or get the wrong settings.
---

# RouterOS DHCP

DHCPv4 server settings are split across three menus that must agree: the **server** (`/ip/dhcp-server`: which interface, which pool, lease
time), the **network** (`/ip/dhcp-server/network`: gateway, DNS, NTP, domain, options sent to clients in that subnet) and the **pool**
(`/ip/pool`: which addresses exist). The server's interface must have an IP address in the network, or the server is invalid.

## Server

```ros
/ip/address/add address=192.168.88.1/24 interface=bridge1
/ip/pool/add name=dhcp_pool ranges=192.168.88.10-192.168.88.254
/ip/dhcp-server/add name=dhcp1 interface=bridge1 address-pool=dhcp_pool lease-time=30m disabled=no
/ip/dhcp-server/network/add address=192.168.88.0/24 gateway=192.168.88.1 dns-server=192.168.88.1
/ip/dhcp-server/lease/print
```

- `/ip/dhcp-server/setup` does the same interactively; do not use it from non-interactive channels.
- One server per interface for directly connected clients. More servers on one interface are for relayed clients, each with its own `relay`.
- If `dns-server` or `ntp-server` is not set in the network entry the server sends the router's own; `dns-none` / `ntp-none` send none.
- `authoritative=yes` (default) answers requests for unknown addresses with a NAK so clients restart quickly. With a primary and a backup
  server on one segment use `delay-threshold` on the backup.
- Address choice: a static lease wins (not conflict checked); otherwise a free pool address, checked with ARP and ICMP first
  (`conflict-detection`, about half a second extra). A found conflict is kept as a `conflict` lease for the lease time.
- Fixed address for a host: make an existing lease static (`/ip/dhcp-server/lease/make-static 0`) or add one
  (`/ip/dhcp-server/lease/add address=192.168.88.50 mac-address=AA:BB:CC:DD:EE:FF server=dhcp1`). Static leases outside the pool work.
- Rate limit per host: set `rate-limit=10M/10M` on a **static** lease; the server creates a dynamic simple queue. FastTracked traffic is
  not limited (`routeros-queues`).
- Name resolution for clients: `add-dns-entries=yes` creates A records `hostname.lan` (suffix `add-dns-entries-suffix`) with the lease time as TTL.
- Leases are written to disk every 5 minutes by default (`/ip/dhcp-server/config`), so a power loss can lose the newest ones.
- Find rogue servers with `/ip/dhcp-server/alert` (new alerts start disabled; do not run it on an interface where this router is a DHCP client).

### Options

`/ip/dhcp-server/option` defines extra options; set them on the network, server, lease or per option set (option sets and the matcher
let you answer by client vendor class or other options). Precedence: RADIUS, lease, server, network. The server only sends options the
client lists in its parameter request list (option 55); `force=yes` on the option overrides that. Values can contain text, hex (`0x`), or
variables; see the option reference and the examples in `server.md`.

## Client

```ros
/ip/dhcp-client/add interface=ether1 disabled=no
/ip/dhcp-client/print detail
```

Defaults add a default route (distance 1) and use the server's DNS and NTP (`use-peer-dns`, `use-peer-ntp`). On a second WAN set
`add-default-route=no` or a higher `default-route-distance` and create the route in a script (the `script=` property runs on status
changes with variables such as `$bound` and `$"gateway-address"`; the guide has a multi-WAN example with routing tables). A client
that uses `use-peer-dns=yes` rewrites `/ip/dns` servers: take that into account in DNS troubleshooting (`routeros-dns`).

## Relay

A relay forwards broadcast requests from a local interface to a server elsewhere:
`/ip/dhcp-relay/add name=r1 interface=Local1 dhcp-server=192.168.0.1 local-address=192.168.1.1 disabled=no`. On the server, the matching
`/ip/dhcp-server` entry carries `relay=192.168.1.1` (the relay's `local-address`) or `255.255.255.255` for any relay, and its own pool and
network.

## DHCPv6

```ros
# Ask the ISP for a delegated prefix and keep it in a pool
/ipv6/dhcp-client/add interface=ether1 request=prefix pool-name=isp-pd pool-prefix-length=64 add-default-route=no
# Delegate /62 prefixes to downstream routers
/ipv6/pool/add name=myPool prefix=2001:db8:7501::/60 prefix-length=62
/ipv6/dhcp-server/add name=pd1 interface=local prefix-pool=myPool lease-time=3d
# Use the received prefix on a LAN and announce it
/ipv6/address/add interface=bridge1 from-pool=isp-pd advertise=yes
```

- `request` can combine `prefix`, `address` and `info`. DHCPv6 gives no default gateway; `add-default-route=yes` uses the server's link-local address.
- The client's pool follows the lifetime of the delegated prefix. The server's bindings are `/ipv6/dhcp-server/binding` (`make-static`); the server
  installs a dynamic route to each delegated prefix via the client's link-local address. IPv6 firewall rules are needed for delegated networks (`routeros-firewall`).
- Router advertisements, SLAAC and address-from-pool: `routeros-ip-addressing`.

## Troubleshooting

1. `/ip/dhcp-server/print` flag `I` (invalid): interface without address, or the pool missing.
2. Client gets nothing: server disabled, wrong bridge port membership or VLAN (`routeros-bridging-switching`), a firewall input rule dropping UDP 67
   on the bridge, another server answers first (check the alert).
3. Wrong gateway or DNS: the network entry for that subnet is missing or has another prefix.
4. Pool exhausted: `/ip/pool/used/print`, shorter `lease-time`.
5. `/log/print where topics~"dhcp"` shows server and client events and rogue-server alerts.

## Where to look

| Need | Open |
| --- | --- |
| Concepts, DHCPv4 versus DHCPv6 | `references/guides/network-management/dhcp.md` |
| Server: setup, leases, rate limits, RADIUS, alerts, options | `references/guides/network-management/dhcp/server.md` |
| Client and its script variables | `references/guides/network-management/dhcp/client.md` |
| Relay example | `references/guides/network-management/dhcp/relay.md` |
| DHCPv6 client and server, prefix delegation | `references/guides/network-management/dhcp/dhcpv6-client.md`, `dhcpv6-server.md` |
| Properties | `references/cli/ip/dhcp-server/`, `references/cli/ip/dhcp-client/`, `references/cli/ipv6/dhcp-*` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-ip-addressing` (pools, ARP, IPv6 addresses), `routeros-dns`, `routeros-initial-setup`, `routeros-queues`,
`routeros-bridging-switching` (DHCP snooping, option 82), `routeros-firewall`.
