---
name: routeros-ethernet
description: Ethernet, SFP and wired interfaces on MikroTik RouterOS 7. Covers link speed, auto-negotiation and advertised modes, forced mode for DAC cables and optical modules that fail auto-initialization, FEC, flow control, PoE-out switches on ports, combo ports, cable test, interface statistics and monitoring, MTU, L2MTU and jumbo frames, interface lists (LAN, WAN and custom lists), loop protection on ports, and PWR-Line. Use when a link does not come up or runs at the wrong speed, when setting MTU or jumbo frames, when grouping interfaces in lists for firewall or bridge rules, or when reading port counters and optical module data.
---

# RouterOS Ethernet and interface lists

Ethernet ports live in `/interface/ethernet`; the generic list of all interfaces is `/interface`. Per-port settings include `speed`,
`advertise`, `auto-negotiation`, flow control, `poe-out`, `fec-mode`, `arp`, `loop-protect` and the MTU pair. Names like `ether1` and
`sfp-sfpplus1` are the `default-name`; renaming is allowed, so select by `default-name` in scripts:

```ros
/interface/ethernet/print
/interface/ethernet/monitor ether1 once                       # link state, rate, duplex, partner capabilities, SFP/DDM data
/interface/ethernet/print stats where default-name=ether1     # counters; the list differs per driver
/interface/ethernet/set [find default-name=ether1] comment=WAN
```

## Link problems

1. Is the cable good? `/interface/ethernet/cable-test ether2` reports the damaged pair and the distance (also total length when the other
   end is unplugged). Not on combo ports and only on listed models.
2. Speed or duplex wrong on copper: leave `auto-negotiation=yes`; restrict with `advertise=` (since 7.12 link modes such as `1G-baseT-full`,
   `2.5G-baseT`, `10G-baseT` replace the old speed/duplex values). Forcing a speed on one end only produces a duplex mismatch.
3. **SFP, SFP+, QSFP**: there is no capability exchange. Each side brings the link up in the highest mode it supports, so both ends must
   have the same highest advertised mode. Device A advertising 10G and 25G against device B advertising only 10G will not link.
4. Log message `module auto-initialization failed, try forced-mode` (since 7.12): the module or DAC has a bad EEPROM checksum. Force the
   mode, matching what the module really supports:

```ros
/interface/ethernet/set [find default-name=sfp-sfpplus1] auto-negotiation=no speed=10G-baseCR       # DAC
/interface/ethernet/set [find default-name=sfp-sfpplus1] auto-negotiation=no speed=10G-baseSR-LR    # optical module
```

   Such modules show no EEPROM data in monitor, so DDM readings are unavailable.
5. 25G and faster links need the same `fec-mode` on both ends (`off` by default, `fec74` or `fec91`; some modes require `fec91`;
   CCR2004-1G-2XS-PCIe has no `fec91` on SFP28).
6. Combo ports choose copper or SFP with `combo-mode`. PoE-out ports: `poe-out=auto-on|forced-on|off`, `poe-priority`, and power-cycle ping
   settings on supporting models (`routeros-hardware` covers PoE budgets and standards).

## MTU and L2MTU

| Value | Meaning |
| --- | --- |
| `mtu` | Layer 3 payload size, default 1500 |
| `l2mtu` | Largest frame without the MAC header the interface can carry; read-only on many drivers, settable on some |
| `max-l2mtu` | The hardware limit, shown in `/interface/print` |

Rules of thumb from the manual: every hop in a path must carry the frame, including switches; VLAN tags, MPLS labels and tunnels need
extra bytes, so either raise L2MTU or lower the L3 MTU of tunnel and VLAN interfaces; a bridge uses the lowest L2MTU of its ports; changing
`l2mtu` or MTU on a port in a hardware-offloaded bridge can reset the switch chip and briefly drop all ports
(`routeros-bridging-switching`). Jumbo frames only help if every device in the segment supports them. Per-model `max-l2mtu` values are in
`references/guides/hardware/mtu-in-routeros.md`.

## Interface lists

Lists give firewall, bridge, neighbor discovery, internet detection and many other menus a stable group of interfaces.

```ros
/interface/list/add name=WAN
/interface/list/add name=LAN
/interface/list/member/add list=WAN interface=ether1
/interface/list/member/add list=LAN interface=bridge1
/interface/list/add name=ALL-LAN include=LAN,GUEST        # union of other lists; `exclude=` removes
```

- Built-in lists: `all`, `none`, `dynamic`, `static`. Members are applied include first, then exclude, then static members.
- A bridge as member is not the same as its ports, and listing all ports is not the same as listing the bridge. The manual notes this
  matters in particular for neighbor discovery; check which interface your rule or feature actually sees.
- Use `in-interface-list=WAN` / `LAN` in firewall rules instead of interface names; a PPPoE or VPN interface can be added to the list
  when it appears (`routeros-firewall`, `routeros-vpn`).

## Other

- `loop-protect=on` on a port sends probe frames and disables the port when it sees them returning (`routeros-bridging-switching`).
- `arp` modes and `arp-timeout` per interface: `routeros-ip-addressing`.
- PWR-Line adapters (HomePlug AV) are `/interface/pwr-line`, with `bandwidth` limits and ARP mode (`wired-connections/pwr-line.md`).
- `/interface/blink` blinks a port LED to find a cable; `/interface/reset-counters` clears counters.
- Wired interface and SFP module compatibility tables: `references/guides/wired-connections/mikrotik-wired-interface-compatibility.md`.

## Where to look

| Need | Open |
| --- | --- |
| Auto-negotiation, advertise, forced mode, FEC, cable test, stats | `references/guides/wired-connections/ethernet.md` |
| MTU, L2MTU and per-model limits | `references/guides/hardware/mtu-in-routeros.md` |
| Interface lists | `references/help/interface-lists.md` and `references/cli/interface/list.md` |
| SFP and cable compatibility | `references/guides/wired-connections/mikrotik-wired-interface-compatibility.md` |
| Properties | `references/cli/interface/ethernet.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-bridging-switching`, `routeros-hardware`, `routeros-firewall`, `routeros-diagnostics-monitoring`,
`routeros-high-availability` (bonding).
