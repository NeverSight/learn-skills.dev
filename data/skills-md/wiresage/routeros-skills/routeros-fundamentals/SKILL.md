---
name: routeros-fundamentals
description: Core knowledge for working with MikroTik RouterOS 7, the entry point to the other routeros-* skills. Covers CLI syntax and the menu hierarchy, item names versus numbers, print and find filters, argument types, safe mode, undo and redo, export and import, and the rules for changing a live router without locking yourself out. Use when starting any RouterOS or MikroTik task, when unsure which RouterOS skill applies, when asked what a console command or argument type means, or before running configuration commands on a real device.
---

# RouterOS fundamentals

RouterOS is MikroTik's network operating system. Everything it can do is reachable from one command tree (the console, also exposed by SSH, the API and the REST API). This skill teaches the shared conventions; the other `routeros-*` skills cover one feature area each. The reference pages are the manual from manual.mikrotik.com, written for RouterOS 7 (snapshot date in `references/INDEX.md`).

## Read the router before you touch it

1. Identify the device and version first. Behaviour differs between RouterOS 6 and 7 and between architectures.

```ros
/system/resource/print
/system/routerboard/print
/system/package/print
```

2. Read the current state with `print` and `export`, never assume it.
3. Make a rollback point before a change (see "Changing a live router" below).

## The console in six rules

1. **Paths.** Menus nest: `/ip/firewall/filter`. Write the full path with `/` (preferred in scripts) or with spaces (`/ip firewall filter`). `/` jumps to the top, `..` goes up one level, and a command can use a path from anywhere: `/ping 10.0.0.1`.
2. **Common commands.** Most menus accept `add`, `set`, `remove`, `print`, `find`, `get`, `enable`, `disable`, `move`, `comment`, `edit`, `reset`, `export`. Menus that hold a single configuration only have `set` and `print`.
3. **Arguments** are `name=value` pairs. Quote values with spaces or special characters. A trailing `\` continues a command on the next line.
4. **Items have names and numbers.** Numbers come from the last `print` in your session and change between prints. Names are properties of the item and stay stable. Never use numbers in scripts: select with `find`.

```ros
/ip/firewall/filter/add chain=forward place-before=[find where comment=CommentX]
/interface/set [find where name=ether1] mtu=1460
```

5. **Filter prints** with `where`; `~` matches a regular expression:

```ros
/log/print where topics~"interface|dhcp"
/file/print where name~"config-before"
/ip/address/print detail
/interface/print count-only
```

6. **Flags** in the first columns describe state (`X` disabled, `I` invalid, `D` dynamic, `R` running, `*` system default). Dynamic and default items cannot be removed by hand. Argument types (`enum`, `time`, `ipPrefix`, `multi`, ...) are explained in `references/guides/cli-reference.md`.

Tab completes, a second Tab lists options, F1 shows context help, Ctrl+C interrupts. Abbreviations work (`pin 10.1 c 3` is a ping) but write full names in anything that is saved or shared.

## Changing a live router

The goal is to never lose the management session.

- **Back up and export first.** `/export file=before-change` writes readable text (user-edited settings only, sensitive values hidden unless you add `show-sensitive`). `/system/backup/save name=before-change password=...` writes a binary backup that only restores reliably on the same device. See `routeros-initial-setup`.
- **Safe mode** (Ctrl+X or F4 in an interactive terminal) undoes everything done in the session if the connection drops (TCP timeout about 9 minutes) or if you leave with Ctrl+D. `/quit` keeps the changes. It remembers the last 100 actions, so work in small steps. It does nothing for commands that need a reboot, such as a configuration reset or a backup restore.
- **Undo and redo.** Every action is recorded in `/system/history`; `/undo` and `/redo` replay it.
- **Non-interactive channels** (SSH one-liners, API, REST, MCP tools) cannot use safe mode. Prefer small reversible steps, keep one working session open while testing from a second one, and for risky network changes schedule a rollback (an entry in `/system/scheduler` that restores the export or backup) that you remove once the change is proven.
- **Order matters for access.** Do not add a drop rule in the `input` chain or change the address or bridge the session depends on before the accept rule for your own connection exists (see `routeros-firewall`).
- **Destructive commands** need an explicit yes from the user: `/system/reset-configuration`, `/system/backup/load`, `/system/reboot`, `/system/shutdown`, removing users or interfaces, `/file/remove`, package changes. A reset asks `Dangerous! Reset anyway? [y/N]`.
- **Secrets.** Do not print or store passwords, private keys, WireGuard keys or backup passwords. Export without `show-sensitive` unless the user asks, and treat any file made with it like a password.

## Export and import

```ros
/export file=router-full                     # whole configuration, compact by default
/ip/firewall/export file=firewall            # only one menu and its sub-menus
/export path=/ip/firewall,!/ip/firewall/nat  # include and exclude menus
/export terse                                # one full command per line, easy to diff
/import file-name=firewall.rsc verbose=yes dry-run   # check syntax and execution, change nothing
```

Export does not contain user passwords, installed certificates, SSH keys, or the Dude and User Manager databases. Import on the RouterOS version that made the export. Files named `*.auto.rsc` run automatically when uploaded by FTP or SFTP.

## RouterOS 6 versus 7

- v7 merged most packages, added WireGuard, containers, REST API, Let's Encrypt, CAKE and FQ-CoDel queues, IPv6 NAT, VXLAN and a new kernel. LCD and KVM packages were dropped; do not run v7 on less than 64 MB RAM.
- Routing was redesigned: `/routing/bgp/connection`, `template`, `session`; OSPFv2 and v3 in one `/routing/ospf` with no default instance or area; routing filters are script-like `if ... then` rules; PIM-SM is `/routing/pimsm`. See `routeros-routing`, `routeros-bgp`, `routeros-ospf`.
- Wireless has two command trees: `/interface/wifi` (Wi-Fi 6 and 7 devices, and 802.11ac ARM devices with the `wifi-qcom-ac` package) and the legacy `/interface/wireless` (package `wireless`, the only choice for MIPS devices and 802.11 a/b/g/n). Their properties differ; do not mix them. See `routeros-wireless`.
- The routing-protocol configuration upgrade from v6 runs only once; the details are in `routeros-install-upgrade`.

## Where to look

| Need | Open |
| --- | --- |
| Which skill covers a menu or topic | `references/skill-map.md` |
| What a type such as `ipPrefix` or `super` means | `references/guides/cli-reference.md` |
| Console keys, safe mode, hot-lock, login options | `references/guides/management-tools/console.md` |
| Every file in this skill | `references/INDEX.md` |
| Single commands such as `/import`, `/password`, `/undo`, `/safe-mode` | `references/cli/` |

## Skills by topic

| Topic | Skills |
| --- | --- |
| Start | `routeros-initial-setup`, `routeros-install-upgrade`, `routeros-troubleshooting` |
| Security and access | `routeros-firewall`, `routeros-users-aaa`, `routeros-certificates`, `routeros-management-tools`, `routeros-api` |
| Interfaces and IP services | `routeros-ethernet`, `routeros-bridging-switching`, `routeros-switch-chip`, `routeros-ip-addressing`, `routeros-dhcp`, `routeros-dns`, `routeros-queues`, `routeros-network-services` |
| Routing, tunnels, redundancy | `routeros-routing`, `routeros-ospf`, `routeros-bgp`, `routeros-mpls`, `routeros-vpn`, `routeros-ipsec`, `routeros-high-availability` |
| Wireless and access networks | `routeros-wireless`, `routeros-mobile-networking`, `routeros-hotspot`, `routeros-user-manager` |
| Operations and automation | `routeros-system-utilities`, `routeros-diagnostics-monitoring`, `routeros-scripting` |
| Hardware, storage, apps | `routeros-hardware`, `routeros-storage`, `routeros-containers`, `routeros-iot` |

Related skills: `routeros-initial-setup` (first configuration, backup, reset), `routeros-scripting` (the scripting language), `routeros-firewall`, `routeros-ip-addressing`, `routeros-api` (REST and API access).
