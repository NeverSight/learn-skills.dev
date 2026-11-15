---
name: routeros-dns
description: DNS on MikroTik RouterOS 7. Covers using the router as the network's resolver and cache, upstream and dynamic servers, static entries (A, AAAA, CNAME, MX, TXT, NXDOMAIN, FWD, regular expressions), forwarders and per-domain forwarding, address lists filled from DNS names, ad blocking with adlists, DNS over HTTPS, the mDNS repeater, VRF, cache and timeout settings, closing the open-resolver hole, and the RFC 2136 DNS update tool. Use when clients cannot resolve names, when setting upstream or local names, blocking or redirecting domains, using domain names in firewall or routing rules, or hardening a router that answers DNS.
---

# RouterOS DNS

The resolver is configured in `/ip/dns`. It answers the router's own lookups and, with `allow-remote-requests=yes`, queries from clients
on UDP and TCP 53. Default configurations already do this and hand out the router as DNS server via DHCP.

## Resolver in five lines

```ros
/ip/dns/set servers=1.1.1.1,9.9.9.9 allow-remote-requests=yes cache-size=4096     # cache-size is in KiB
/ip/dns/print                                     # servers (yours) and dynamic-servers (from DHCP client, PPP, ...)
:put [:resolve mikrotik.com]                      # test from the router
/ip/dns/cache/print
/ip/dns/cache/flush
```

- Order: your `servers` first, then `dynamic-servers`. The router waits `query-server-timeout` for an answer, then tries the next
  server; with no answer in `query-total-timeout` the client gets `SERVFAIL`. When `max-concurrent-queries` upstream queries are pending,
  new queries (even cacheable ones) are dropped.
- Clients need the router's address as DNS server: `dns-server` in `/ip/dhcp-server/network` (`routeros-dhcp`).
- **Do not run an open resolver.** With `allow-remote-requests=yes` drop UDP and TCP 53 from the WAN in `input` (the default firewall does).
  If the router needs no clients, set `allow-remote-requests=no` (`routeros-initial-setup` hardening).
- Status words: `NOERROR` (name exists, possibly without records of that type), `NXDOMAIN`, `SERVFAIL`.
- Logs: `/log/print where topics~"dns"` (DoH errors, adlist import problems).

## Static entries

```ros
/ip/dns/static/add name=nas.lan address=192.168.88.20
/ip/dns/static/add name=example.lan address=192.168.88.30 match-subdomain=yes          # also www.example.lan
/ip/dns/static/add name=files.lan type=CNAME cname=nas.lan
/ip/dns/static/add name=tracker.example.com type=NXDOMAIN                                # make a name not exist
/ip/dns/static/add name=corp.example.com type=FWD forward-to=10.0.0.53 match-subdomain=yes   # send a domain elsewhere
/ip/dns/static/add regexp="^host[0-9]+\\.lan\$" address=192.168.88.40                  # lower-case regex; escape \ and $
```

- An IPv6 address makes AAAA; the router answers PTR for static addresses. Other record types come from upstream; if upstream has none the
  answer is `NOERROR` without records.
- One entry per name and record type: when several entries match (for example `match-subdomain` plus a more specific name), list order does
  not decide.
- `FWD` without `forward-to` sends to the normal upstream and also exempts a name from adlists (the way to unblock one name).
- Forwarders are named groups of DNS or DoH servers for FWD entries: `/ip/dns/forwarders/add name=branch dns-servers=10.1.0.53,10.1.1.53`,
  `forward-to=branch`. Servers take turns; a dead one is not skipped, queries to it fail.
- `address-list=NAME` on an entry fills a firewall address list with the addresses the router answers; only client queries add entries, not
  `:resolve`; entries expire with the TTL plus `address-list-extra-time`. Use the list in filter, mangle or raw rules (`routeros-firewall`).
- DHCP server and neighbor discovery can add dynamic static entries (`add-dns-entries`).

## Ad blocking and DoH

```ros
/ip/dns/set cache-size=16384
/ip/dns/adlist/add url=https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
/ip/dns/adlist/print
/ip/dns/static/add name=ads.example.net type=FWD          # unblock one name
/ip/dns/set use-doh-server=https://cloudflare-dns.com/dns-query verify-doh-cert=yes
```

- Blocked names answer `0.0.0.0` (A) and `::` (AAAA) with a 2 second TTL. An adlist of about 75,000 names needs about 6 MiB of cache; if the
  cache fills, the import stops (`adlist read: max cache size reached`) and must be removed and re-added after raising `cache-size`.
  Disabling a list does not free its memory; removing it does. Lists are rechecked every 4 hours (`adlist/reload` forces it). Up to 64 lists.
- With DoH set, **all** upstream queries go to that one server over TCP 443 and there is no fallback to plain DNS (clients get `SERVFAIL`
  if it is unreachable); keep `servers` or a static entry so the router can resolve the DoH host name. HTTP/2-only services (Quad9,
  Mullvad, UncensoredDNS) work only on ARM64 and x86.
- The `vrf` property chooses which VRF's clients are served; upstream servers in another VRF are written `address@vrf`.

## mDNS repeater

`/ip/dns/set mdns-repeat-ifaces=bridge,vlan20` passes IPv4 mDNS between networks (printers, AirPlay, Chromecast). Not IPv6, not over L3
tunnels such as WireGuard. The input chain must accept UDP 5353 on the listed interfaces.

## DNS update (RFC 2136)

`/tool/dns-update dns-server=192.0.2.53 zone=example.com name=office address=198.51.100.20 ttl=300 key-name=dns-update-key key="BASE64SECRET"`
points a name in your own zone at one IPv4 address with an hmac-md5 TSIG key (the only algorithm supported). Keep the router clock within
5 minutes of the server (NTP), allow TCP 53 to the server, and send updates only when the address changed. The key is visible to anyone
who can read the script. For a name that follows the router's public address without your own DNS server use IP Cloud DDNS
(`routeros-network-services`); HTTP-based dynamic DNS services are updated with `/tool/fetch` (`routeros-system-utilities`).

## Where to look

| Need | Open |
| --- | --- |
| Everything about the resolver, entries, adlists, DoH, mDNS, technical details | `references/guides/network-management/dns.md` |
| RFC 2136 updates and error messages | `references/guides/diagnostics-monitoring-and-troubleshooting/dynamic-dns.md` |
| Properties | `references/cli/ip/dns.md` and `references/cli/ip/dns/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-dhcp`, `routeros-firewall`, `routeros-network-services`, `routeros-certificates` (DoH trust), `routeros-routing`
(domain-based policy routing).
