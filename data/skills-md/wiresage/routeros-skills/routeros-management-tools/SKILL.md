---
name: routeros-management-tools
description: Ways to reach and manage MikroTik RouterOS devices. Covers WinBox (v4 and legacy v3), WebFig and its HTTPS certificate, the SSH server and client (host keys, key login, ssh-exec in scripts, known hosts), the serial console, MAC Telnet and the MAC server, RoMON overlay management, Quick Set, the MikroTik mobile app, TR-069, CMR fleet management, The Dude, FlashFig and the branding package. Use when choosing or securing a management path, recovering access to a router with a broken IP configuration, running commands on another device from a script, managing a fleet, or enabling HTTPS for the web interface.
---

# RouterOS management tools

Every management path is also an attack surface. Enable the ones you use, restrict them in `/ip/service` and the firewall (`routeros-initial-setup`,
`routeros-system-utilities`), and prefer keys and VPNs over exposing ports.

| Tool | Reaches the router by | Notes |
| --- | --- | --- |
| **WinBox** v4 (Windows, Linux, macOS) | IP (TCP 8291) or MAC | Signed binary; ECSRP authentication; the GUI mirrors the CLI and has a terminal. v3 is the legacy Wine/Windows build |
| **WebFig** | IP, HTTP/HTTPS | Same layout as WinBox in a browser. Use HTTPS (`www-ssl` with a certificate) |
| **SSH** | IP, TCP 22 | Server on by default; client `/system/ssh`, scripts use `/system/ssh-exec` |
| **Serial console** | RS232 cable | For first setup and recovery; null-modem cable and a terminal program, port settings (`/port/set serial0 baud-rate=... data-bits=8 parity=none stop-bits=1`) must match the device |
| **MAC Telnet / MAC WinBox / MAC ping** | MAC on the same L2 segment | Needs no IP configuration; allowed on the `LAN` interface list by default |
| **RoMON** | MAC-layer overlay between routers | Independent of L2 and L3 configuration; unencrypted, so use SSH or WinBox on top |
| **API, REST API** | IP | `routeros-api` |
| **CMR** | Fleet server and clients | Monitoring, upgrades, alerts, scripts on many devices |
| **TR-069 client** | ACS over HTTP(S) | `/tr069-client` (`acs-url`, `username`, `password`, `periodic-inform-interval`, `client-certificate`) |

## SSH

```ros
/ip/ssh/print                                   # host-key-fingerprint, strong-crypto, password-authentication
/ip/ssh/set strong-crypto=yes
/user/ssh-keys/import public-key-file=id_ed25519.pub user=ops     # then password login is off for that user
/ip/ssh/regenerate-host-key                     # after a leak; clients that pinned the key will complain
/system/ssh 192.168.88.3 user=noc               # router as client
```

- Host key type defaults to Ed25519 on new installs (upgraded routers keep RSA). Moving a router: `export-host-key` and `import-host-key`.
- Scripted use needs `ssh-exec`. It never prompts, so the server's key must be pinned beforehand, or it fails with `host key not trusted`:
  `/ip/ssh/known-hosts/add host=192.168.88.3 key="ssh-ed25519 AAAA..."`. `known-hosts-ignore=yes` on a single command skips validation;
  `known-hosts-trusted-subnets` skips it for whole subnets. Both remove protection against impersonation: use them knowingly.
- `ssh-exec ... as-value` returns `exit-code` and `output`. Never put a password on the command line (it lands in scripts and history); use key
  authentication on both sides.

## WebFig HTTPS

For LAN access use a self-signed certificate made on the router and distribute its CA to browsers; for a public name use Let's Encrypt
(`routeros-certificates`). Then assign it: `/ip/service/set www-ssl certificate=<name> disabled=no` and disable plain `www`.

## Recover access

1. Wrong IP configuration, router unreachable: WinBox "Neighbors" tab or `/tool/mac-telnet <MAC>` from a device on the same segment, then fix the
   address. If MAC access was disabled for hardening, use the serial console or the reset button (`routeros-initial-setup`).
2. Serial console: a null-modem cable and a terminal program with the port settings of the device (see your model's quick guide or manual);
   `/system/serial-terminal` lets one RouterOS device manage serial devices (modems, switches).
3. RoMON when only some routers still have IP: `/tool/romon/set enabled=yes`, choose ports in `/tool/romon/port`, then `/tool/romon/ssh` from a peer.
   Hardware-offloaded bridges flood the multicast frames; on some switch chips (RB5009's 88E6393X with tagged-only ports) the frames never reach the CPU.

## Fleet and legacy tools

- **CMR** (package `cmr`, arm, arm64, x86; every device can be a client except smips and powerpc): inventory, rule-based upgrades, alerts, scripts on many devices,
  WiFi and VLAN provisioning. It does not configure IP, DHCP, routing, firewall or users; use `run-script` for one-off changes. A script sent through CMR
  runs without a user session, with only the `read`, `write`, `test` and `reboot` policies. Guide: `references/guides/management-tools/cmr.md`.
- **The Dude** is discontinued legacy software provided as is (package `dude`, its own database that backups do not contain).
- **Quick Set** is for first setup of a router with default configuration; it can overwrite settings made elsewhere. **FlashFig** is a Windows
  tool for bulk configuration of RouterBOARDs; **Branding** customizes names and logos; the mobile app covers basic setup.

## Where to look

| Need | Open |
| --- | --- |
| WinBox v4 and v3 | `references/guides/management-tools/winbox.md`, `winbox-legacy.md` |
| WebFig and HTTPS | `references/guides/management-tools/webfig.md` |
| SSH server, client, keys, ssh-exec | `references/guides/management-tools/ssh.md` |
| MAC server, RoMON, serial console | `mac-server.md`, `romon.md`, `serial-console.md` in the same folder |
| CMR, TR-069, Dude, Quick Set, FlashFig, branding | the matching file in the same folder |
| Properties | `references/cli/cmr/`, `references/cli/dude/`, `references/cli/tool/romon/`, `references/cli/ip/ssh.md`, `references/cli/system/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-fundamentals` (console), `routeros-initial-setup`, `routeros-users-aaa` (accounts, keys), `routeros-certificates`,
`routeros-api`, `routeros-system-utilities` (services, device mode), `routeros-diagnostics-monitoring`.
