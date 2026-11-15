---
name: routeros-users-aaa
description: Authentication, authorization and accounting on MikroTik RouterOS. Covers router administrator accounts, groups and policies, password rules and expiry, SSH public keys, inactivity timeouts, RADIUS client setup (including RadSec) for management logins, PPP, HotSpot and wireless, PPP profiles and secrets, PPP AAA and 802.1X (Dot1X) authenticator and supplicant. Use when creating or hardening admin accounts, giving someone limited rights, moving logins to RADIUS, setting up PPP users for VPN servers, or configuring port-based access control.
---

# RouterOS users, RADIUS and PPP AAA

Three separate things share the "AAA" name: the **router's own users** (`/user`, for people who manage the device), **PPP
users** (`/ppp/secret` and `/ppp/profile`, for VPN and PPPoE clients), and the **RADIUS client** (`/radius`) that can answer for
either of them and for HotSpot, wireless, DHCP and IPsec. Local entries win over RADIUS in all cases.

## Router users and groups

```ros
/user/group/add name=ops policy=ssh,read,write,password,test
/user/add name=alice group=ops password="REPLACE-WITH-A-LONG-PASSWORD" address=192.168.88.0/24
/user/print
```

- Each user is in exactly one group; the group's policies decide the rights, and a policy not listed is revoked. The built-in
  groups `read`, `write` and `full` cannot be deleted, and **`read` still contains `reboot` and `sensitive`**: do not give it to
  untrusted people; make a custom group instead. Policies of interest: `ssh`, `winbox`, `web`, `api`, `rest-api`, `ftp`,
  `reboot`, `read`, `write`, `policy` (manage users), `sensitive` (see and export secrets), `sniff`, `test`, `local`.
- `address=` limits the login to source prefixes. Names accept letters, digits and `_ . # - @` and must end with a letter or digit.
- Passwords accept any characters, but in scripts and quoted strings escape `"`, `\` and `$` (an unescaped `$` starts a variable
  and silently shortens the password). `password=""` allows blank logins; never do that.
- Users change their own password with `/password` (needs the `password` policy). An administrator can force a change with
  `/user/expire-password alice`. `/user/settings` sets `minimum-password-length` and `minimum-categories`.
- Idle sessions: `inactivity-timeout` and `inactivity-policy=logout|lockscreen` per user.
- Check who is logged in with `/user/active/print` and end a session with `/user/active/remove`.
- Replace the default `admin`: create a named account, test it in a second session, then `/user/disable admin`. A lost password cannot
  be recovered (see `routeros-troubleshooting`).

### SSH keys

```ros
/user/ssh-keys/import public-key-file=alice.pub user=alice info="alice laptop"
/ip/ssh/set password-authentication=no          # key-only logins (default yes-if-no-key)
```

When a user has a key, SSH password login is disabled for that user. Imports accept OpenSSH one-line, PKCS#1 and PKCS#8 public
keys. Router-side private keys (`/user/ssh-keys/private`) accept PKCS#1/PKCS#8 only, not the OpenSSH private format.

## RADIUS

```ros
/radius/add service=login address=192.0.2.36 secret="REPLACE-ME"
/user/aaa/set use-radius=yes default-group=read
/radius/add service=ppp,hotspot address=192.0.2.3 secret="REPLACE-ME"
/radius/monitor 0
```

- `service` selects the consumers: `login`, `ppp`, `hotspot`, `wireless`, `dhcp`, `ipsec`, `dot1x`. The order of entries matters.
- RADIUS is asked only for names that do not exist locally. Users from RADIUS get `default-group` (`read` by default) unless the
  server returns `Mikrotik-Group` with a local group name; `exclude-groups` lists groups the server may never grant.
- For CHAP and MS-CHAP the shared secret is only checked in the reply, so a wrong secret looks like a server that accepts and a router
  that rejects: look at `/radius/monitor` for bad responses.
- RadSec (`protocol=radsec`, a `certificate=`) uses TCP 2083 and the fixed shared secret `radsec`.
- A RouterOS RADIUS server is User Manager (`routeros-user-manager`). Disconnect requests arrive through `/radius/incoming`.
- Attribute reference and numeric values: `references/guides/authentication-authorization-accounting/radius.md`.

## PPP users and profiles

```ros
/ppp/profile/add name=vpn local-address=10.0.0.1 remote-address=vpn-pool use-encryption=yes
/ppp/secret/add name=user1 password="REPLACE-ME" profile=vpn service=l2tp
/ppp/aaa/set use-radius=no accounting=yes
```

A user's effective settings combine the secret, its profile, and the default profile for the service; single addresses beat pools.
`only-one` limits a user to one session. A profile can add the session interface to a bridge, an address list, filters
(`incoming-filter`, `outgoing-filter`), rate limits and IPv6 pools. The server menus that use this are in `routeros-vpn`.

## 802.1X

`/interface/dot1x/server` makes a port an authenticator: it blocks everything except EAPOL until the client has been authenticated
by a RADIUS server (`auth-types=dot1x,mac-auth`, optional `guest-vlan-id`). On a bridge port the bridge must run RSTP/MSTP or EAP
packets are not accepted. `/interface/dot1x/client` makes the router a supplicant with EAP-TLS, EAP-TTLS, EAP-PEAP or EAP-MSCHAPv2
(certificates: `routeros-certificates`). Not supported on SMIPS devices (hAP lite, hAP lite TC, hAP mini). The guide has complete
authenticator and supplicant examples.

## Where to look

| Need | Open |
| --- | --- |
| Users, groups, password policy, SSH keys, RADIUS logins | `references/guides/authentication-authorization-accounting/user.md` |
| RADIUS client properties, RadSec, attributes | `references/guides/authentication-authorization-accounting/radius.md` |
| PPP profiles, secrets, active sessions | `references/guides/authentication-authorization-accounting/ppp-aaa.md` |
| 802.1X client and server | `references/guides/authentication-authorization-accounting/dot1x.md` |
| All properties | `references/cli/user.md`, `references/cli/radius.md`, `references/cli/ppp/aaa.md`, `references/cli/interface/dot1x/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-initial-setup` (hardening), `routeros-vpn`, `routeros-hotspot`, `routeros-user-manager`,
`routeros-certificates`, `routeros-management-tools` (SSH, WinBox, API access).
