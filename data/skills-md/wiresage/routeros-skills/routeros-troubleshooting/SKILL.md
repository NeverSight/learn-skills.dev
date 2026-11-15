---
name: routeros-troubleshooting
description: Troubleshooting and support workflow for MikroTik RouterOS 7. Covers a symptom-to-skill routing table, collecting evidence safely (read-only triage bundle script, supout.rif and autosupout.rif), recovery when access is lost (reset button sequences, backup bootloader, Netinstall, lost password), reboot loops, unclassified CPU load, default passwords and what to send to MikroTik support. Use when something on a MikroTik router is broken and the cause is unknown, when a device is unreachable or boot-looping, when a password is lost, or when preparing a support request.
---

# RouterOS troubleshooting and support

Work from evidence, not from guesses. Read before you change anything, change one thing at a time, and keep a way back (a backup or
`/export`, safe mode, a console route). `routeros-fundamentals` explains safe mode and the CLI; `routeros-diagnostics-monitoring` has the tools.

## Method

1. State the symptom precisely: what fails, from where, since when, what changed (upgrade, new rule, new provider, hardware swap).
2. Collect facts without changing the router: version and uptime (`/system/resource/print`), recent log (`/log/print`), interface state and
   counters, addresses and routes. The bundled script saves this in one file:

   ```bash
   bash scripts/collect-diagnostics.sh --host 192.0.2.1 --user admin --out ./diag
   ```

   ```powershell
   ./scripts/collect-diagnostics.ps1 -HostName 192.0.2.1 -User admin -OutDirectory ./diag
   ```

   It runs print and monitor commands only. The file contains addresses, routes and log lines: treat it as private.
3. Test layer by layer, from the bottom: link (`/interface/ethernet/monitor`), addressing (`/ip/address/print`, ARP), routing (`/ip/route/print`,
   `/tool/traceroute`), name resolution (`/ping` by name versus by address), then firewall and NAT counters (`/ip/firewall/filter/print stats`).
4. Change one thing, test, record the result; roll back if it did not help.

## Symptom to skill

| Symptom | Start with |
| --- | --- |
| No internet from the LAN, router itself is online | `routeros-firewall` (masquerade, forward chain), `routeros-dhcp`, `routeros-dns` |
| Router has no internet | `routeros-ip-addressing`, `routeros-routing`, `routeros-dhcp` (client), `routeros-mobile-networking` |
| Some sites hang or pages half-load | MTU and MSS: `routeros-diagnostics-monitoring` (path MTU), `routeros-firewall` (MSS clamp) |
| Link down, wrong speed, SFP not detected | `routeros-ethernet`, `routeros-hardware` |
| VLAN traffic missing, loops, wrong port | `routeros-bridging-switching` |
| Traffic bypasses the firewall or queues, offloading stops, switch ACL or QoS on a CRS | `routeros-switch-chip` |
| Wi-Fi clients cannot connect or roam | `routeros-wireless` |
| VPN does not establish | `routeros-vpn`, `routeros-ipsec`, `routeros-certificates` |
| Slow or uneven bandwidth | `routeros-queues`, `routeros-diagnostics-monitoring` (torch, bandwidth test) |
| High CPU, reboots, overheating | `/tool/profile`, `/system/resource`, `/system/health` (see below), `routeros-hardware` |
| Cannot log in or reach the router | `routeros-management-tools`, `routeros-users-aaa`, `routeros-initial-setup` |
| Wrong time, certificates fail, scheduler idle | `routeros-system-utilities` (NTP), `routeros-certificates` |
| Upgrade failed or package missing | `routeros-install-upgrade` |
| A feature is blocked or refuses to enable | device mode in `routeros-system-utilities` |

## Support output (supout.rif)

`/system/sup-output` writes a diagnostic snapshot for MikroTik support: configuration, logs, process state and, after a crash, crash data. The
file is encoded and opened with the Supout.rif viewer in your MikroTik account.

```ros
/system/sup-output name=flash/supout          # on devices with a flash folder, other files are lost at reboot
```

- Create it while the problem is present and before you upgrade or reboot again. After a crash also send `autosupout.rif` and
  `autosupout.old.rif`, which the watchdog writes by itself (`automatic-supout=yes`). A watchdog reboot caused by the ping watchdog does not write one.
- Download with `scp admin@192.168.88.1:supout.rif .`, WinBox or WebFig Files. If the viewer shows cut outputs, use `output-width=300`.
- To catch a problem at a known time, schedule the command with the scheduler and remove the entry afterwards.
- Send the supout with the problem description through the MikroTik support portal; it keeps the history of your requests. Say what you changed
  before the problem began and what you already tried.

## Recover access

| Situation | What to do |
| --- | --- |
| IP configuration broken | Reach the router by MAC (WinBox neighbors or MAC Telnet) or serial console and fix it (`routeros-management-tools`) |
| Lost or forgotten password | There is no password recovery. The only way is a reset to factory defaults, which erases the configuration. Be wary of anyone selling "recovery tools": they do not exist |
| Reset to defaults | Router off, hold the reset button, power on, release when the user LED starts flashing (about 5 s). `/system/reset-configuration` from the CLI. Holding about 5 s longer after the LED flashes (until it is solid) enables CAPs mode. Buttons differ by model, see the product page in `routeros-hardware` |
| Device boot-loops or will not boot | Load the backup bootloader: hold reset, power on, release after 1 to 3 s; then run `/system/routerboard/upgrade` and reboot. If it still fails, reinstall with Netinstall |
| Need to reinstall | Netinstall: hold reset while powering on until the LED sequence (blinking, solid, off) completes, then run Netinstall on a PC connected directly to the port, same subnet, firewalls off (`routeros-install-upgrade`) |
| Default password unknown on a new device | Newer models have a factory password on the sticker, the packaging or the quick guide sheet; older ones use `admin` with an empty password. After Netinstall or reset see the same places |

If Protected RouterBOOT is enabled (`/system/routerboard/settings`), the reset button, the RouterBOOT serial menu and Netinstall are all disabled, so
none of the rows above work without the admin password; the only way out is the emergency reformat described in `routeros-hardware`, which erases
everything.

Back up with `/export` and a binary backup before a reset (`routeros-initial-setup`). A reset removes users, passwords and the configuration; after it, set a
new password first.

## Common findings

- **High "unclassified" CPU in `/tool/profile`:** upgrade RouterOS and the firmware (`/system/routerboard/upgrade`), reboot, and if it persists
  send a supout with when it appears and how long after boot. New process classes are added in each release.
- **Watchdog reboots in a loop:** a bad `watch-address` in `/system/watchdog` reboots a healthy router; set it to `none` during the window after boot.
- **Clock at 1970:** no time source; enable NTP (`routeros-system-utilities`).
- **Remote access request:** allow only the needed port from a known address list, put the accept rule above the default drop rule, prefer a VPN
  (`routeros-firewall`).

## Where to look

| Need | Open |
| --- | --- |
| Creating, scheduling and downloading supout.rif | `references/guides/getting-started/supout-rif.md` |
| Command parameters | `references/cli/system/sup-output.md` |
| Lost password, default password, reset the password | `references/help/lost-password.md`, `default-password.md`, `reset-the-password.md` |
| Reboot loop and unclassified load | `references/help/reboot-loop.md`, `high-unclassified-load.md` |
| Support portal and consultants | `references/help/registering-in-the-support-portal.md`, `how-to-apply-for-official-mikrotik-consultant.md` |
| Everything else | `references/INDEX.md` |

The `help/` pages are from the frozen help.mikrotik.com site; some are in Latvian or older than the manual. The reset procedure is documented in `routeros-initial-setup`
(configuration reset page) and Netinstall problems in `routeros-install-upgrade` (the "Problems with Netinstall" article).

Related skills: `routeros-diagnostics-monitoring`, `routeros-fundamentals`, `routeros-initial-setup`, `routeros-install-upgrade`, `routeros-hardware`,
`routeros-management-tools`, `routeros-system-utilities`.
