---
name: routeros-vpn
description: Building VPNs and tunnels on MikroTik RouterOS 7. Covers WireGuard (site to site, road warrior, client configuration export, multi-WAN), L2TP, SSTP, OpenVPN and PPTP servers and clients with PPP secrets and profiles, PPPoE, Layer 2 tunnels (EoIP, L2TP-Ether), GRE, IPIP, 6to4 and ZeroTier, with the firewall, routing and MTU steps each one needs. Use when creating or debugging a site-to-site or remote-access tunnel, choosing a VPN protocol, issuing client configurations, or when a tunnel is up but no traffic passes.
---

# RouterOS VPN and tunnels

A tunnel needs four things: the tunnel interface (or PPP session), addresses on both ends, routes that send traffic into it,
and firewall rules that let the carrier traffic in and the inner traffic through. Most "the tunnel is up but nothing passes"
problems are a missing route, a firewall rule in the wrong place, or MTU. For IPsec policies and IKE see `routeros-ipsec`.

## Choose the protocol

| Need | Use |
| --- | --- |
| Modern site-to-site or remote access between RouterOS, Linux, phones, laptops | **WireGuard** (UDP, key pairs, fast, no user database) |
| Native clients on Windows, macOS, iOS, Android without extra software | **L2TP with IPsec** (`use-ipsec` on the client; server side needs IPsec) |
| Must pass restrictive firewalls over TCP 443 | **SSTP** (TLS; certificate needed for Microsoft clients) or OpenVPN over TCP |
| Existing OpenVPN clients | **OpenVPN** (limited implementation, see below) |
| Extend a Layer 2 segment between sites | **EoIP** (RouterOS to RouterOS), L2TP-Ether, or a bridge over VXLAN (`routeros-bridging-switching`) |
| Plain IP-in-IP / GRE interop with other vendors | **GRE**, **IPIP**, protected with IPsec |
| Overlay network without opening ports | **ZeroTier** (`zerotier` package) |
| PPPoE to or from an ISP | **PPPoE client or server** |

PPTP is legacy and insecure: the manual itself limits it to compatibility and tests. Do not recommend it for anything that matters.

## WireGuard

An interface holds a key pair (generated when you create it) and a listen port; each remote device is a **peer** with a public key
and `allowed-address`, which is both the filter for incoming traffic and the routing table for outgoing traffic. Only
public keys are exchanged; never move or paste a private key.

```ros
/interface/wireguard/add name=wg0 listen-port=13231
:put [/interface/wireguard/get [find name=wg0] public-key]          # give this to the other side
/interface/wireguard/peers/add interface=wg0 public-key="REMOTE-PUBLIC-KEY" \
    allowed-address=10.1.101.0/24,10.255.255.2/32 endpoint-address=198.51.100.2 endpoint-port=13231
/ip/address/add address=10.255.255.1/30 interface=wg0
/ip/route/add dst-address=10.1.101.0/24 gateway=wg0
```

Road warrior: no `endpoint-address` on the peer, `allowed-address=192.168.100.2/32`, an address like `192.168.100.1/24` on the interface, and
`responder=yes` so the router answers instead of repeatedly initiating. `persistent-keepalive=25s` helps peers behind NAT.
`/interface/wireguard/peers/show-client-config` produces a client configuration or QR code from the peer's `client-address`,
`client-dns`, `client-endpoint` and related properties (default client address `192.168.177.2/24`); `wg-import` and `wg-export`
convert to and from the standard `.conf` format. Treat generated client configurations and exports as secrets.

Firewall: accept UDP to the listen port in `input` before the drop rule (`place-before=[find ...]`, see `routeros-firewall`), accept
the tunnel subnets in `forward`, and for access to the router itself accept `in-interface=wg0` or add `wg0` to the `LAN` interface list
(that grants VPN peers whatever LAN rules grant). Behind another NAT router, forward the UDP port. With several WANs the reply may
leave through another uplink; the manual shows mangle rules plus `responder` to pin replies to the incoming route. The `vrf` property
applies to the UDP socket, not to the interface.

## PPP-based servers (L2TP, SSTP, OpenVPN, PPTP)

Users are PPP secrets with a profile (`/ppp/secret`, `/ppp/profile`); the server interface is enabled and bound to a profile and,
for TLS-based ones, a certificate (see `routeros-certificates`).

```ros
/ppp/secret/add name=user1 password="REPLACE-ME" service=l2tp profile=default-encryption local-address=10.0.0.1 remote-address=10.0.0.5
/interface/l2tp-server/server/set enabled=yes default-profile=default-encryption use-ipsec=required ipsec-secret="REPLACE-ME"
/interface/sstp-server/server/set enabled=yes certificate=server-cert default-profile=default-encryption
/interface/l2tp-client/add name=l2tp-out1 connect-to=198.51.100.2 user=user1 password="REPLACE-ME" use-ipsec=yes ipsec-secret="REPLACE-ME" disabled=no
/interface/sstp-client/add name=sstp-out1 connect-to=198.51.100.2 user=user1 password="REPLACE-ME" disabled=no
```

- L2TP uses UDP 1701 for setup and has no encryption of its own; pair it with IPsec. SSTP uses TCP 443; for Microsoft clients use
  mschap authentication and a certificate chain the client trusts. TLS SNI is available from 7.15.
- OpenVPN in RouterOS has no LZO compression and no NCP cipher negotiation (the cipher must be in the client file); user names are
  limited to 27 characters. UDP and TCP are supported; `tls-crypt` from 7.17. Certificates for server and clients are required; the
  server can export a client configuration (`/interface/ovpn-server/server/export-client-configuration`).
- `ppp/profile` supplies addresses (`local-address`, `remote-address` or a pool) and the encryption policy. Use the same user name in
  `/ppp/secret` and on the client. Passwords with special characters need escaping in scripts.
- The server creates dynamic interfaces per session; reference sessions by `service` and profile in firewall rules, or add the
  dynamic interfaces to an interface list with `/interface/list/member` after a connection (dynamic names change).
- To reach the LAN behind a client, add a route on the server (`gateway=<interface or remote-address>`) and, for NAT, masquerade on
  the client's `out-interface=<tunnel>`.

## Layer 3 and Layer 2 tunnels

```ros
/interface/gre/add name=gre1 local-address=192.168.80.1 remote-address=192.168.90.1       # then address + route as for WireGuard
/interface/ipip/add name=ipip1 local-address=10.0.0.1 remote-address=22.63.11.6
/interface/eoip/add name=eoip1 remote-address=10.0.0.2 tunnel-id=0                       # tunnel-id unique per tunnel
/interface/bridge/port/add bridge=bridge1 interface=eoip1
```

EoIP adds at least 42 bytes; set the underlying path or the tunnel MTU so that full Ethernet frames fit, or clamp MSS. GRE, IPIP and
EoIP do not encrypt: wrap them in IPsec when they cross untrusted networks. PPTP and GRE need protocol 47 and TCP 1723 allowed
through firewalls. 6to4 and `ipipv6`, `gre6`, `eoipv6` cover IPv6 transport.

## Checks when it does not work

1. Is the tunnel `R` (running)? `/interface/print where name=wg0`, `/interface/wireguard/peers/print` (`last-handshake`, `rx`, `tx`),
   `/ppp/active/print`, `/log/print where topics~"ppp|l2tp|wireguard|ipsec"`.
2. Is the carrier traffic allowed in `input` (UDP 13231, UDP 1701, TCP 443, TCP 1723, protocol 47) and not NATed wrongly?
3. Is there a route for the remote subnet through the tunnel, and does the remote side have one back? For WireGuard, does
   `allowed-address` contain the destination (it is also the routing filter)?
4. Are both firewalls forwarding the inner traffic, and is there a masquerade rule that should not touch tunnel traffic
   (`ipsec-policy=out,none` or `out-interface-list=WAN` keeps it away)?
5. MTU: pings succeed but large transfers hang. Lower the tunnel MTU or clamp MSS in mangle (`action=change-mss`).

## Where to look

| Need | Open |
| --- | --- |
| WireGuard recipes, client export, multi-WAN, HotSpot 2FA | `references/guides/virtual-private-networks/wireguard.md` |
| L2TP, L2TP-Ether, LAC and LNS with Cisco | `references/guides/virtual-private-networks/l2tp.md` and `l2tp/` |
| SSTP certificates, OpenVPN files and limitations | `references/guides/virtual-private-networks/sstp.md`, `openvpn.md` |
| PPPoE, IPv6 PD over PPP, MLPPP | `references/guides/virtual-private-networks/pppoe.md` and `pppoe/` |
| EoIP, GRE, IPIP, 6to4, ZeroTier | the matching file next to them |
| Every property of the interfaces and of `/ppp` | `references/cli/interface/` and `references/cli/ppp/` |
| WireGuard over IPv6 (knowledge base) | `references/help/wireguard-ipv6.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-ipsec`, `routeros-firewall`, `routeros-certificates`, `routeros-users-aaa` (RADIUS for PPP, `/ppp/aaa`),
`routeros-routing`, `routeros-bridging-switching`.
