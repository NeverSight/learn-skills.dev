---
name: routeros-initial-setup
description: First-time setup and configuration management for a MikroTik RouterOS device. Covers reaching a new or reset router, the factory default configuration, building the network by hand when there is none (bridge, LAN address, DHCP server), WAN setup with DHCP client, static address or PPPoE, source NAT and port forwarding, the hardening checklist (users, passwords, services, MAC access, neighbor discovery), backup and restore, export and import, undo, safe mode, and configuration reset. Use when setting up, resetting, hardening, backing up or cloning a router, or when asked how a router should be configured out of the box.
---

# RouterOS initial setup and configuration management

Work in this order: find out what you have, secure access, get the WAN up, give the LAN addresses, harden, back up.
Read the router before you change it (`/system/resource/print`, `/system/default-configuration/print`, `/export`). Rules for
not losing the session are in `routeros-fundamentals`; they apply to every step here.

## 1. Know the starting point

- Most routers ship with a default configuration: a bridge for the LAN ports, `192.168.88.1/24` as the LAN address, a DHCP
  server, NAT on the WAN port, and a firewall that blocks management access from the WAN. `/system/default-configuration/print`
  shows the exact commands applied to this model. The families (CPE, AP, switch, CAP and so on) are in
  `references/guides/getting-started/configuration-management/default-configurations.md`.
- Some professional models (for example CCR) ship with little or no configuration. Then build the LAN by hand (section 4).
- Keep the default firewall. Remove it only if you will replace it with something you have designed.
- Login is `admin`. The password is empty, or printed on the device label on models that have one. Connect from a port other
  than `ether1` (the WAN port in the defaults). WinBox finds routers by MAC address under Neighbors when there is no IP yet.

## 2. Secure access first

```ros
/user/add name=ops password="REPLACE-WITH-A-LONG-PASSWORD" group=full
/user/disable admin
```

- Use a unique name and a password of at least 12 characters. In a quoted password escape `"`, `\` and `$` with a backslash:
  an unescaped `$` starts a variable and the password silently ends up shorter.
- Prefer one account per administrator in a group with only the policies needed (the built-in `read` group can reboot the
  router and see sensitive settings). With an SSH public key assigned, password login over SSH is disabled for that user.
- Check that the new account works in a second session before you disable `admin`. A lost password cannot be recovered; the
  only way out is a configuration reset or reinstall.

## 3. WAN

Ask which kind of uplink it is. Verify with `/ping 8.8.8.8` and then `/ping example.com` (the second tests DNS).

```ros
# DHCP from the ISP (most common): address, DNS, NTP and default route come from the server
/ip/dhcp-client/add interface=ether1 disabled=no

# Static address from the ISP (documentation addresses shown)
/ip/address/add address=192.0.2.100/24 interface=ether1
/ip/route/add gateway=192.0.2.1
/ip/dns/set servers=192.0.2.53

# PPPoE: afterwards the WAN interface is pppoe-out1, not ether1
/interface/pppoe-client/add interface=ether1 user=ISP-USER password=ISP-PASSWORD add-default-route=yes use-peer-dns=yes disabled=no
```

Source NAT so that LAN hosts can reach the internet (the default configuration already has it). The `out-interface` must be
the real uplink (`pppoe-out1`, an LTE interface and so on) or nothing is translated:

```ros
/interface/list/add name=WAN
/interface/list/member/add list=WAN interface=ether1
/ip/firewall/nat/add chain=srcnat out-interface-list=WAN ipsec-policy=out,none action=masquerade
```

Port forwarding is a `dst-nat` rule; with a strict forward chain it also needs an accept rule there:

```ros
/ip/firewall/nat/add chain=dstnat action=dst-nat protocol=tcp dst-port=3389 to-addresses=192.168.88.254 to-ports=3389
```

Do not publish management services. If you need remote access to the router, use a VPN (WireGuard, see `routeros-vpn`).

## 4. LAN when there is no default configuration

Starting clean wipes everything and reboots, so ask the user first: `/system/reset-configuration no-defaults=yes skip-backup=yes`.
Then bridge, address and DHCP:

```ros
/interface/bridge/add name=bridge1
/interface/bridge/port/add interface=ether2 bridge=bridge1
/ip/address/add address=192.168.88.1/24 interface=bridge1
/ip/pool/add name=dhcp_pool ranges=192.168.88.10-192.168.88.254
/ip/dhcp-server/add name=dhcp1 interface=bridge1 address-pool=dhcp_pool lease-time=30m disabled=no
/ip/dhcp-server/network/add address=192.168.88.0/24 gateway=192.168.88.1 dns-server=192.168.88.1
```

`/ip/dhcp-server/setup` does the same interactively, but it asks questions, so do not use it from a non-interactive channel.
Every wireless interface that should serve the LAN must be a port of the bridge too (see `routeros-wireless`).
Without a firewall on this router, add one before connecting it to the internet (`routeros-firewall`).

## 5. Hardening checklist

All commands are from the manual's "Securing your router" page; the file has the reasoning.

```ros
/ip/service/disable telnet,ftp,www,api               # keep only what you use
/ip/service/set winbox available-from=192.168.88.0/24  # optional: limit a service to source addresses
/ip/ssh/set strong-crypto=yes
/tool/mac-server/set allowed-interface-list=none
/tool/mac-server/mac-winbox/set allowed-interface-list=none
/tool/mac-server/ping/set enabled=no
/ip/neighbor/discovery-settings/set discover-interface-list=none
/tool/bandwidth-server/set enabled=no
/ip/dns/set allow-remote-requests=no                  # unless this router is the LAN's DNS server
/ip/proxy/set enabled=no
/ip/socks/set enabled=no
/ip/upnp/set enabled=no
```

Disabling MAC access and neighbor discovery removes the way to reach the router when its IP configuration breaks, so do it
on production routers, not on a device you are still setting up. Disable unused interfaces with
`/interface/set [find where name=ether5] disabled=yes`. Keep RouterOS current (`routeros-install-upgrade`).

## 6. Back up, export, restore, reset

```ros
/export file=before-change                                         # readable, no passwords, one menu: /ip/firewall/export
/system/backup/save name=before-change password="REPLACE-ME"       # binary, whole device, encrypted
/system/backup/load name=before-change password="REPLACE-ME"       # asks "Restore and reboot? [y/N]"
/import file-name=before-change.rsc verbose=yes dry-run            # syntax check only
/system/reset-configuration no-defaults=yes skip-backup=yes        # asks "Dangerous! Reset anyway? [y/N]"
```

- A binary backup restores reliably only on the same device and RouterOS version (it carries the MAC addresses). Moving a
  configuration to another device is done with export and import. A v6 backup needs `force-v6-to-v7-configuration-upgrade=yes`.
- An export holds no user passwords, certificates, SSH keys, or the Dude and User Manager databases. Check an exported file
  before importing it on another model: renamed `ether` ports and a different port count break the import.
- `/system/reset-configuration` options: `keep-users`, `no-defaults`, `skip-backup`, `run-after-reset=file.rsc` (the script
  must finish within 2 minutes), `caps-mode`. The reset button does the same from hardware: hold during power-up until the
  LED flashes. Safe mode does not protect a reset or a restore.
- `scripts/export-config.sh` (PowerShell: `scripts/export-config.ps1 -HostName ...`) saves a timestamped export over SSH
  with key authentication: `scripts/export-config.sh --host 192.0.2.1 --user ops --out ./backups`. Add `--terse` for a
  diff-friendly file. It never reads a password; `--show-sensitive` is opt-in and writes the file private.

## Where to look

| Need | Open |
| --- | --- |
| Step-by-step first configuration, WAN types, NAT, wireless basics | `references/guides/getting-started/first-time-configuration.md` |
| Bridge, IP address and DHCP by hand | `references/guides/getting-started/manual-network-setup.md` |
| Full hardening list | `references/guides/getting-started/securing-your-router.md` |
| Export, import, undo, safe mode, reset parameters | `references/guides/getting-started/configuration-management.md` |
| Backup and restore | `references/guides/getting-started/configuration-management/backup.md` |
| What a model's default configuration contains | `references/guides/getting-started/configuration-management/default-configurations.md` |
| Which menus hold sensitive values | `references/guides/getting-started/configuration-management/list-of-menus-with-sensitive-parameters.md` |
| Reset button behaviour and LED sequences | `references/guides/getting-started/configuration-management/routeros-configuration-reset.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-fundamentals`, `routeros-firewall`, `routeros-dhcp`, `routeros-install-upgrade`, `routeros-wireless`,
`routeros-vpn`, `routeros-troubleshooting` (lost password, reboot loop).
