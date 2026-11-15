---
name: routeros-network-services
description: Optional network services on MikroTik RouterOS 7. Covers the MikroTik cloud (IP Cloud DDNS, time update, cloud backup, Back To Home VPN, File Share) and which connections RouterOS makes to MikroTik servers, the web proxy and transparent proxy, the HTTPS reverse proxy, the SOCKS server and Socksify, and OpenFlow. Use when giving a router a dynamic DNS name, reaching a router behind NAT, storing a cloud backup, publishing web servers by host name, filtering or caching web requests, running or consuming a SOCKS proxy, or disabling cloud and proxy services during hardening.
---

# RouterOS network services

These services are off or limited by default. Each one opens a listener or contacts external servers, so enable only what is needed and
restrict who can reach it (`routeros-firewall`).

## MikroTik cloud (`/ip/cloud`)

| Service | Default | Menu | Purpose |
| --- | --- | --- | --- |
| DDNS | off | `/ip/cloud` | A name under `sn.mynetname.net` that follows the router's public address |
| Time update | on | `/ip/cloud`, `/system/clock` | Sets clock and time zone at start unless the NTP client is on |
| Cloud backup | off | `/system/backup/cloud` | One encrypted backup stored on MikroTik's servers |
| Back To Home | off | `/ip/cloud` | WireGuard VPN server reachable from the phone app, also behind NAT through a MikroTik relay |
| File Share | off | `/ip/cloud/back-to-home-file` | Share a directory or file through an HTTPS link |

```ros
/ip/cloud/set ddns-enabled=yes
/ip/cloud/print                         # dns-name, public-address, status
/ip/cloud/force-update
/ip/cloud/set update-time=no            # stop asking the cloud for the time (and /system/clock time-zone-autodetect=no)
/ip/cloud/set ddns-enabled=auto         # off, unless Back To Home needs it
```

- The router always initiates the connection (encrypted requests to `cloud2.mikrotik.com`, UDP 15252), so no port forwarding is needed. The
  name only makes the router findable; it opens nothing, and the default firewall still drops management access from the internet.
- `public-address` behind NAT is the NAT device's address. `use-local-address=yes` under `/ip/cloud/advanced` makes the name resolve to the
  router's LAN address instead.
- Cloud services work on MikroTik devices and CHR with a paid license, not on RouterOS x86. Back To Home needs ARM, ARM64 or TILE and 7.12+.
- Back To Home users are WireGuard clients managed by the app; for fine control configure WireGuard yourself (`routeros-vpn`). Guest
  shares can be limited to internet access and an expiry date. Do not create or share tunnels on a router unless the user asked for it.
- A Let's Encrypt certificate for the DDNS name uses the DNS-01 challenge (`routeros-certificates`).
- `references/guides/network-management/cloud/communication-mikrotik-cloud-servers.md` lists every connection RouterOS makes to
  MikroTik servers and how to switch each off; read it when hardening or auditing egress.

## Web proxy (`/ip/proxy`)

```ros
/ip/proxy/set enabled=yes port=8080
/ip/proxy/access/add dst-host=*.ads.example action=deny
/ip/firewall/filter/add chain=input protocol=tcp dst-port=8080 in-interface-list=!LAN action=drop    # never run an open proxy
```

- Regular mode: clients are configured for the router and port. Transparent mode: a NAT rule redirects plain HTTP port 80 to the proxy
  (HTTPS cannot be intercepted this way). The proxy only relays HTTPS: it can allow or deny by host, address and port but cannot see paths
  or cache content. Path filtering and caching are for plain HTTP.
- Not available in the `home` and `basic` device modes (`routeros-system-utilities`). Parent proxies, cache rules (`/ip/proxy/cache`,
  `direct`) and statistics are in the guide.

## Reverse proxy (`/ip/reverse-proxy`)

Terminates HTTPS on port 443, picks a rule by the TLS server name, and forwards plain HTTP to the server behind the router; several
servers can share one public address. Container apps get rules automatically. Not on SMIPS devices.

```ros
/certificate/import file-name=nas.crt name=nas passphrase=""
/certificate/import file-name=nas.key passphrase=""
/ip/reverse-proxy/add sni=nas.example.com ip-address=192.168.88.10 port=8080 certificate=nas
```

DNS for the name must point at the router and port 443 must be accepted in `input`.

## SOCKS and Socksify

```ros
/ip/socks/set version=5 enabled=yes                 # default version=4 refuses SOCKS5 clients; listens on TCP 1080
/ip/socks/access/add src-address=192.168.0.0/24 action=allow
/ip/socks/access/add action=deny                    # no match means allow, so end with an explicit deny
```

An open SOCKS proxy is abused for spam and anonymisation: always set the access list or a firewall rule. Password authentication (users in
`/ip/socks/users`) needs version 5. **Socksify** goes the other way: a dst-nat rule with `action=socksify` sends selected connections
through an upstream SOCKS5 server for applications without SOCKS support. Always add `dst-address-type=!local` to that NAT rule or the
router's own SSH and WebFig get redirected and you lose management access. LAN destinations (RFC 1918) are refused by the service; new
records are created disabled and need a disable/enable after changes.

## OpenFlow

`/openflow` makes the router an OpenFlow 1.0 or 1.3 agent for an SDN controller (separate `openflow` package). Ports that belong to an
OpenFlow switch bypass the normal networking stack unless the controller installs flows for them, so a wrong setup can cut management
access. Configure it with a console connection or an out-of-band port available.

## Where to look

| Need | Open |
| --- | --- |
| Cloud overview, DDNS, time update | `references/guides/network-management/cloud.md` |
| Back To Home, cloud backup, File Share | `references/guides/network-management/cloud/` |
| Web proxy | `references/guides/network-management/proxy/web-proxy.md` |
| Reverse proxy | `references/guides/network-management/proxy/reverse-proxy.md` |
| SOCKS and Socksify (including a Tor example) | `references/guides/network-management/socks.md`, `socks/socksify.md` |
| OpenFlow | `references/guides/network-management/openflow.md` |
| Properties | `references/cli/ip/cloud*`, `references/cli/ip/proxy*`, `references/cli/ip/socks*`, `references/cli/openflow*` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-dns` (DDNS alternatives), `routeros-vpn`, `routeros-firewall`, `routeros-initial-setup` (disable unused
services), `routeros-system-utilities` (device modes, clock), `routeros-containers` (reverse proxy for apps).
