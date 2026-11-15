---
name: routeros-ipsec
description: Configuring IPsec on MikroTik RouterOS 7. Covers IKE phases, profiles, proposals, peers, identities, policies and templates, mode-config, IKEv1 and IKEv2, pre-shared keys, certificates and EAP, site-to-site tunnels, GRE over IPsec, road warrior setups with Windows, macOS, iOS, Android and strongSwan clients, L2TP over IPsec, NAT and FastTrack bypass, hardware acceleration, and reading IPsec logs. Use when building, debugging or hardening an IPsec tunnel or remote-access server, when phase 1 or phase 2 fails, or when tunnel traffic is unencrypted, dropped or very slow.
---

# RouterOS IPsec

IPsec on RouterOS is configured with a chain of menus under `/ip/ipsec`. Know which one holds what before you change anything:

| Menu | Role |
| --- | --- |
| `profile` | Phase 1 (IKE) parameters: hash, encryption, DH group, lifetime, NAT-T, DPD |
| `peer` | The remote end: address, `exchange-mode` (`main`, `aggressive`, `ike2`), `profile`, `passive`, `send-initial-contact` |
| `identity` | How the peer is authenticated: `auth-method` (`pre-shared-key`, `digital-signature`, `eap`, `rsa-key` ...), secrets, certificates |
| `proposal` | Phase 2 (ESP/AH) parameters: algorithms, PFS group, lifetime |
| `policy` (and `policy/group`) | Which traffic is encrypted (`src-address`, `dst-address`, `tunnel=yes`, `action=encrypt`), or a template for dynamic peers |
| `mode-config` | Addresses, DNS and so on pushed to road warrior clients |
| `active-peers`, `installed-sa`, `statistics` | Read-only state |

Both ends must agree on every phase 1 and phase 2 setting. Time must be right on both ends (IPsec breaks when clocks drift:
see NTP in `routeros-system-utilities`).

## Site-to-site (pre-shared key, from the manual, with IKEv2)

Use separate profile, proposal and peer entries per remote peer so each can change on its own. Prefer IKEv2 (`exchange-mode=ike2`)
and avoid a pre-shared key where certificates are possible: the manual warns that PSK is open to offline attacks in all
exchange modes. Use a long random secret.

```ros
/ip/ipsec/profile/add name=ike-site2 dh-group=modp2048 enc-algorithm=aes-128 hash-algorithm=sha256
/ip/ipsec/proposal/add name=ike-site2 enc-algorithms=aes-128-cbc pfs-group=modp2048
/ip/ipsec/peer/add name=ike-site2 address=192.0.2.2/32 profile=ike-site2 exchange-mode=ike2
/ip/ipsec/identity/add peer=ike-site2 auth-method=pre-shared-key secret="REPLACE-WITH-A-LONG-RANDOM-SECRET"
/ip/ipsec/policy/add src-address=10.1.202.0/24 dst-address=10.1.101.0/24 tunnel=yes action=encrypt proposal=ike-site2 peer=ike-site2
/ip/ipsec/active-peers/print
/ip/ipsec/installed-sa/print
```

The other router mirrors the addresses. The peer address must be reachable on UDP 500 and 4500 (accept both in `input`; ESP
protocol 50 too when there is no NAT).

### What breaks a working configuration

1. **NAT.** A masquerade rule rewrites the source before the packet reaches the policy, so it no longer matches. Put an accept
   rule at the top of the srcnat chain for the tunnel subnets:
   `/ip/firewall/nat/add chain=srcnat action=accept src-address=10.1.202.0/24 dst-address=10.1.101.0/24 place-before=0`
   and clear the stale connection entries afterwards.
2. **FastTrack.** FastTracked packets bypass IPsec policy checking, causing random drops or very slow transfers. Exclude the
   tunnel traffic from FastTrack with accept rules before it, or bypass connection tracking with
   `/ip/firewall/raw/add chain=prerouting action=notrack src-address=... dst-address=...` in both directions (the manual says this
   cuts CPU load by about 30 percent compared with filter-rule exceptions).
3. **Firewall forward chain** that allows new connections in one direction only: pings work one way. Accept the tunnel subnets.
4. **Different `local-address` or routing tables.** With several addresses or VRFs set `local-address` on the peer; see the manual's
   pages on specifying it.
5. Policies are checked in order; templates (`template=yes`) belong to dynamic peers such as road warriors.

## Road warrior (IKEv2)

Server: a certificate for the router, a `mode-config` that hands out an address pool and DNS, a policy group and template, an
identity that matches the client (certificate or EAP), and a peer with `passive=yes` and `exchange-mode=ike2`. The manual walks
through RSA authentication and through EAP-MSCHAPv2 with User Manager, with client steps for Windows, macOS, iOS, Android
(strongSwan) and Linux (strongSwan). Open `references/guides/virtual-private-networks/ipsec.md` at "Road Warrior setup using IKEv2".

- X.509 certificates must carry the SubjectKeyIdentifier extension; ed25519 and AES-GCM for IKEv2 authentication are not supported.
  Certificate creation: `routeros-certificates`.
- Keep strongSwan reauthentication off: RouterOS does not support RFC 4478.
- Allow only encrypted traffic with the policy matcher (`ipsec-policy=in,ipsec` / `out,ipsec`) or generic policies; the guide has examples.
- L2TP/IPsec for native clients: `routeros-vpn` (the `use-ipsec` setting generates the transport-mode policy and peer).

## Reading failures

Enable IPsec logging, reproduce, then read the log:

```ros
/system/logging/add topics=ipsec,!debug
/log/print where topics~"ipsec"
```

| Message | Meaning |
| --- | --- |
| `no suitable proposal found` / `failed to get valid proposal` | Algorithm mismatch. The debug log lists local:remote values (before and after the colon); align hash, encryption, DH and PFS |
| `phase1 negotiation failed due to time up` | Peers do not talk: wrong address, UDP 500/4500 blocked, NAT problem, wrong `local-address` |
| `NO-PROPOSAL-CHOSEN` notify | Remote refused the proposed algorithms; read the remote debug log |
| Phase 1 never re-keys | DPD is disabled; Phase 1 is only re-keyed with DPD on |

Also check `installed-sa` for SAs and byte counters, and `/ip/ipsec/statistics`.

## Algorithms and performance

ESP supports AES (CBC, CTR, GCM), ChaCha20-Poly1305, Camellia, Blowfish, Twofish, 3DES and DES, with MD5, SHA1 and SHA2 for
authentication; AH is authentication only. The manual's DH table runs from group 1 to 21; it recommends group 19 (`ecp256`) as fast
and secure and says to avoid group 2 and PSK for new deployments. Hardware acceleration depends on the CPU and algorithm (table in
the guide); software encryption is a common bottleneck on small routers. For IPsec to protect a GRE or EoIP tunnel see the GRE-over-IPsec
example and `routeros-vpn`.

## Where to look

| Need | Open |
| --- | --- |
| Concepts, DH groups, ESP/AH, acceleration, all examples, FAQ | `references/guides/virtual-private-networks/ipsec.md` |
| IKEv2 EAP with a third-party provider | `references/guides/virtual-private-networks/ipsec/ikev2-eap-between-nordvpn-and-routeros.md` |
| Post-quantum pre-shared keys (QKD) | `references/guides/virtual-private-networks/ipsec/qkd-integration-in-routeros-ipsec-ppk.md` |
| Property reference for each menu | `references/cli/ip/ipsec/` |
| Interop notes (Fortinet, Oracle Cloud) | `references/help/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-vpn`, `routeros-certificates`, `routeros-firewall`, `routeros-user-manager` (EAP users),
`routeros-users-aaa` (RADIUS).
