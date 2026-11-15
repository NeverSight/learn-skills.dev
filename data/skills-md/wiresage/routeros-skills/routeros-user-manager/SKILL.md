---
name: routeros-user-manager
description: User Manager on MikroTik RouterOS 7, the built-in RADIUS server and user database. Covers enabling it and its package and licence limits, registering routers (NAS devices) with shared secrets and RadSec, users and groups, allowed outer and inner authentication methods (PAP, CHAP, MS-CHAP, EAP-TLS, TTLS, PEAP), profiles with limitations (rate, traffic, uptime, time windows), assigning profiles to users, RADIUS attributes (static IP, address pool, rate limit), sessions and accounting, vouchers and batch users, TOTP, the /um web interface and PayPal payments, and migration from RouterOS 6. Use when a RouterOS device should act as the RADIUS server for HotSpot, PPP, wireless 802.1X or DHCP, or when selling or limiting access by time and volume.
---

# RouterOS User Manager

User Manager (UM) is a RADIUS server (UDP 1812 authentication, 1813 accounting) with its own database, a per-user web page at `/um/`, profiles,
limitations and optional PayPal sales. It is a separate package (`user-manager`), available on all architectures except SMIPS, and the licence level
limits the number of active sessions. The router that runs UM is the RADIUS **server**; the routers that authenticate users against it are
its **clients** (NAS), configured with `/radius` (`routeros-users-aaa`).

## Quick start

```ros
/user-manager/set enabled=yes
/user-manager/router/add name=local address=127.0.0.1 shared-secret="REPLACE-ME"      # the router itself as NAS
/user-manager/user/add name=alice password="REPLACE-ME" shared-users=1
/radius/add service=hotspot address=127.0.0.1 secret="REPLACE-ME"                    # client side, on the NAS
```

- Add every NAS under `/user-manager/router` (`address`, `shared-secret`, `coa-port` default 3799, `protocol=udp|radsec`) with the same secret
  as on the NAS client entry. A NAS that is not registered gets no answers. Run `/user-manager/set enabled=yes` and allow UDP 1812 and 1813 from the NAS addresses.
- On the NAS, set the service to use RADIUS: `use-radius=yes` in the HotSpot profile (`routeros-hotspot`), the PPP profile or secrets (`routeros-vpn`),
  or the RADIUS option of the wireless/802.1X configuration (`routeros-wireless`). Enable RADIUS accounting and interim updates if limits or
  session disconnects matter.
- With `use-profiles=no` (default) only users are needed. Turn `use-profiles=yes` to enforce profiles and limitations.
- Settings: `authentication-port` 1812, `accounting-port` 1813, `certificate` for EAP-TLS methods, `radsec-certificate` for RadSec.
- The database is separate from the router configuration and from `/export`/backups: `/user-manager/database/save name=backup` and `load` handle `.umb` files;
  `db-path` can point to external storage.

## Users and groups

```ros
/user-manager/user/group/add name=staff outer-auths=pap,chap,mschap2,eap-peap inner-auths=peap-mschap2 attributes=Framed-Pool:pool1
/user-manager/user/add name=bob password="REPLACE-ME" group=staff shared-users=2
/user-manager/user/set [find name=carol] attributes=Framed-IP-Address:192.168.1.4 shared-users=1
/user-manager/user/add-batch-users number-of-users=3 password-characters=lowercase,numbers,uppercase password-length=6 username-characters=lowercase username-length=6
```

- Groups `default` and `default-anonymous` exist. A group lists allowed `outer-auths` (`pap`, `chap`, `mschap1`, `mschap2`, `eap-tls`, `eap-ttls`,
  `eap-peap`, `eap-mschap2`) and `inner-auths` (`ttls-pap`, `ttls-chap`, `ttls-mschap1`, `ttls-mschap2`, `peap-mschap2`) plus RADIUS attributes.
  A method that is not listed is refused.
- `Framed-IP-Address` needs `shared-users=1`. `Framed-Pool` names a pool that must exist on the NAS. Other predefined attributes include
  `Mikrotik-Rate-Limit`, `Mikrotik-Group` (HotSpot or PPP profile), `Mikrotik-Address-List`, `Mikrotik-Wireless-VLANID`, `Session-Timeout`, `Idle-Timeout`;
  custom attributes go in `/user-manager/attribute` (vendor id, type id, value type).
- `caller-id` restricts a user to one `Calling-Station-Id`. TOTP: set `otp-secret` and append the current 6-digit code to the password (the clock must be right).
- Vouchers: `generate-voucher voucher-template=printable_vouchers.html [find where name=alice]` writes under `/um/PRIVATE/GENERATED/vouchers/`
  (set `web-private-username` and `web-private-password` in `/user-manager/advanced` to open it); `export.csv` or `export.xml` exports all users.
  Reports: `/user-manager/generate-report report-template=report_default.html columns=username,uptime,download,upload`.

## Profiles and limitations

```ros
/user-manager/limitation/add name=lim-5m download-limit=0 upload-limit=0 transfer-limit=10000000000 uptime-limit=30d \
    rate-limit-rx=2M rate-limit-tx=10M reset-counters-interval=monthly
/user-manager/profile/add name=monthly validity=30d starts-when=first-auth name-for-users="Monthly" price=10
/user-manager/profile-limitation/add profile=monthly limitation=lim-5m from-time=00:00:00 till-time=23:59:59
/user-manager/user-profile/add user=alice profile=monthly
```

- A **limitation** holds limits: `download-limit`, `upload-limit`, `transfer-limit` (bytes, 0 is unlimited), `uptime-limit`, rate limit parts
  (`rate-limit-rx`, `rate-limit-tx`, burst fields) and periodic counter resets. A **profile** has `validity`, `starts-when` (`assigned` or `first-auth`),
  `price`, `override-shared-users`. **profile-limitation** links them with `from-time`, `till-time` and `weekdays`; when a profile has several limitations the user must satisfy
  all of them.
- A user can hold several **user-profile** entries; only one is active, and the next takes over when it expires, without dropping the session.
  `activate-user-profile` forces one.
- Limits and disconnects need RADIUS accounting and interim updates on the NAS, and `/radius/incoming/set accept=yes` on the NAS so UM can disconnect active sessions (port `coa-port` of the router entry, default 3799). When a
  shared-users limit is reached the older session is disconnected first, so use `/radius` `timeout=1s` in such setups. IPsec does not support rate limitations.
- Sessions: `/user-manager/session/print` (only recorded when the NAS sends accounting), per-user `monitor`.

## Web interface and payments

Users sign in at `http://<router>/um/` (served by the `www`/`www-ssl` services; assign a certificate for HTTPS) to see sessions, profiles and, when a profile has a `price`, buy it with PayPal
(`paypal-allow=yes`, `paypal-user`, `paypal-password`, `paypal-signature`, `paypal-currency`, `paypal-use-sandbox` for testing in
`/user-manager/advanced`). Only transactions with status `approved` are complete. Login pages and CSS can be replaced (`css/`, `user/login_dynamic.html`, and others
listed in the guide). Restrict `/um/` to the networks that need it in `/ip/service` and the firewall.

## Migration and cautions

- After moving from RouterOS 6, UM 7 starts empty. Copy the old files and run `/user-manager/database/migrate-legacy-db`; it converts users, profiles,
  limitations, routers and sessions.
- Secrets, passwords and PayPal credentials are sensitive; do not publish exports. A weak `shared-secret` lets anyone who can reach UDP 1812 forge a NAS.
- Check UM is reachable before blaming the service: log topics `manager` and `radius` (`routeros-diagnostics-monitoring`).

## Where to look

| Need | Open |
| --- | --- |
| Attributes table, database, limitations, profiles, routers, sessions, settings, users, groups, web interface, application guides | `references/guides/authentication-authorization-accounting/user-manager.md` |
| Properties | `references/cli/user-manager.md` and the sub-menus `references/cli/user-manager/` (router, user, user/group, limitation, profile, profile-limitation, user-profile, session, payment, attribute, database, advanced) |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-hotspot`, `routeros-users-aaa` (RADIUS client, 802.1X, PPP accounts), `routeros-vpn` (PPP with RADIUS), `routeros-wireless` (WPA-EAP),
`routeros-certificates` (EAP-TLS, RadSec), `routeros-queues`, `routeros-install-upgrade` (packages and licence).
