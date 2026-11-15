---
name: routeros-system-utilities
description: Everyday system features of MikroTik RouterOS 7. Covers the system clock, time zone and NTP client and server, the scheduler (nightly backups, startup scripts), the /ip/service management listeners and what the router listens on, device mode restrictions and their physical confirmation, files and the flash directory, fetch (downloads, uploads, webhooks, certificate checks), email through SMTP, system identity and login note, neighbor discovery (MNDP, CDP, LLDP), TFTP, Wake on LAN, UPS monitoring, IP packing, partitions and PTP. Use when time or time zone is wrong, scheduling a task, restricting or auditing management services, a feature is blocked by device mode, moving files or calling web endpoints from a router, or sending alerts by email.
---

# RouterOS system utilities

## Clock, time zone, NTP

Time matters for logs, the scheduler, certificates, IPsec and RADIUS. RouterOS keeps UTC and applies the zone. Without a time source a router
that boots without saved time shows **1970-01-02**.

```ros
/system/clock/print
/system/clock/set time-zone-autodetect=no time-zone-name=Europe/Riga
/system/ntp/client/set enabled=yes servers=pool.ntp.org
/system/ntp/client/print                         # status: synchronized, synced-server, system-offset
/system/ntp/server/set enabled=yes               # serve time to the LAN (allow UDP 123 in input)
```

- Sources: NTP client (precise), MikroTik cloud (once at startup, only when the NTP client is off and `update-time=yes`; approximate), GPS
  (`set-system-time=yes`), manual. NTP servers can be names (resolved through `/ip/dns`, so DNS must work first).
- Zone autodetection uses the location of the public IP address, which providers sometimes register elsewhere: turn it off and set a named
  zone. A manually entered zone is replaced shortly after boot while autodetect is on, which looks like an hour offset after reboots.
- Set the date and the time in two separate commands; together they use the old GMT offset across a DST change. The current time is never part of
  an export. A manual (non-named) zone does not repeat its DST rules next year.
- NTP uses powers-of-two polling between `min-poll` and `max-poll` (64 to 1024 s by default) with an initial burst (`iburst`). Modes
  `broadcast`, `multicast` and `manycast` exist besides `unicast`. Symmetric key authentication is supported; PTP (IEEE 1588, hardware timestamping on
  some models) is a separate feature.

## Scheduler

```ros
/system/script/add name=nightly-backup source={ /system/backup/save name=nightly password="REPLACE-ME"; /export file=nightly }
/system/scheduler/add name=nightly-backup start-time=03:00:00 interval=1d on-event=nightly-backup
/system/scheduler/print detail                    # next-run, run-count, policy
```

- `on-event` takes a script name or commands. `start-time=startup` runs at every boot **before interfaces are up**, so wait for the default route
  or DHCP in the script. `days=` limits weekdays, `disabled` pauses an entry.
- The entry runs with the owner's policy set; give scripts that change configuration the policies they need (`write`, `policy`, `reboot`...) and no more.
- Not available in device mode `home` (enable it with `/system/device-mode/update scheduler=yes`), and entries cannot be created while the device is flagged. For rollback tricks see `routeros-fundamentals`.
- Scripting syntax: `routeros-scripting`.

## Services and exposure

`/ip/service` lists `ftp`(21), `ssh`(22), `telnet`(23), `www`(80), `www-ssl`(443), `winbox`(8291), `api`(8728), `api-ssl`(8729) and `reverse-proxy`, each
with `port`, `address` (`available-from`), `vrf` and, for TLS ones, `certificate`. Dynamic entries show every port a feature listens on and the open
connections:

```ros
/ip/service/print where dynamic                  # resolver, btest, discover, cloud ports and active sessions
/ip/service/disable telnet,ftp,www,api
/ip/service/set winbox,ssh available-from=192.168.88.0/24,10.8.0.0/24
```

A port opened by another feature (DNS on 53 with `allow-remote-requests`, bandwidth test on 2000, discovery on 5678, SOCKS, proxy) is not in this
list as an editable service; close those with the feature's own setting and the firewall.

## Device mode

`/system/device-mode/print` shows the mode (`advanced`, `home`, `basic`, `rose`) and per-feature switches (`scheduler`, `fetch`, `email`, `socks`,
`proxy`, `hotspot`, `container`, `sniffer`, `romon`, `zerotier`, ...). A tool that fails with a device-mode message needs its flag, and changing
it requires **physical confirmation** (reset or mode button within 5 minutes, or a cold power cycle; a normal reboot cancels), followed by a reboot:
`/system/device-mode/update mode=advanced` or per-feature `container=yes`. Never tell the user a restricted feature is "enabled" without checking the
flag. The `flagged` state blocks scheduler entries and other features until resolved.

## Files, fetch, email

```ros
/file/print detail
/tool/fetch url="https://example.com/file.rsc" dst-path=file.rsc check-certificate=yes
/tool/fetch mode=sftp address=192.0.2.5 user=backup src-path=nightly.backup dst-path=/backups/nightly.backup upload=yes
/tool/fetch url="https://hooks.example.com/notify" http-method=post http-data="router up" check-certificate=yes output=none
/tool/e-mail/set server=smtp.example.com port=587 tls=starttls certificate-verification=yes from=router@example.com user=router password="REPLACE-ME"
/tool/e-mail/send to=admin@example.com subject="backup" body="done"
```

- Files outside `flash` live in RAM on devices with a `flash` directory and vanish at reboot (not `.npk` upgrade files). Uploading a file does not apply it.
- `fetch` verifies nothing unless `check-certificate=yes`; SFTP checks host keys against `/ip/ssh/known-hosts` (`routeros-management-tools`). Credentials in
  a URL or `password=` end up in scripts and history: prefer keys and a restricted account. `upload=yes` works for `ftp` and `sftp`; an HTTP POST uses `http-data`.
- Email: port 587 uses `tls=starttls`, 465 uses `tls=yes`, 25 plain only inside your network (mixing them gives handshake errors or timeouts).
  `certificate-verification` defaults to `no`. Gmail needs an app password.
- Device mode `home` blocks `fetch`, `email`, the scheduler, proxy, SOCKS, hotspot, bandwidth test and ZeroTier by default (`basic` allows email, fetch, scheduler).

## Smaller tools

- **Identity** (`/system/identity/set name=...`, up to 64 characters) shows in the prompt, neighbor discovery, SNMP and the DHCP host name. **Note**
  (`/system/note/set note="..."`) is shown at login.
- **Neighbor discovery** (`/ip/neighbor`, `/ip/neighbor/discovery-settings`): MNDP, CDP and LLDP on `discover-interface-list`; announcements every 30 s. Disable it on
  untrusted interfaces (`routeros-initial-setup`).
- **TFTP server** (`/ip/tftp`) runs while an enabled rule exists; no authentication, so limit `ip-addresses` and `req-filename`. **Wake on LAN**: always give
  `interface` (`/tool/wol mac=... interface=bridge`). **UPS** (package `ups`, APC smart protocol over serial or USB): monitoring, hibernate and safe reboot.
- **IP packing** aggregates and compresses packets over a link between two RouterOS devices; TCP sessions that the packing router itself opens
  fail. **Partitions** (NAND devices): primary and fallback RouterOS installs.

## Where to look

| Need | Open |
| --- | --- |
| Clock, NTP, PTP | `references/guides/system-information-and-utilities/clock.md`, `ntp.md`, `precision-time-protocol.md` |
| Scheduler examples (startup script, LEDs at night) | `.../scheduler.md` |
| Services and listening ports | `.../services.md` |
| Device mode | `.../device-mode.md` |
| Fetch, email, files | `.../fetch.md`, `e-mail.md`, `files.md` |
| Everything else | `references/INDEX.md` |
| Monitoring UPS (knowledge base) | `references/help/monitoring-ups.md` |

Related skills: `routeros-scripting`, `routeros-initial-setup`, `routeros-diagnostics-monitoring`, `routeros-management-tools`, `routeros-certificates`,
`routeros-dns`, `routeros-storage`.
