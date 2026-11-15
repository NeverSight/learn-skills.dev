---
name: kicad-routing
description: "Routes a KiCad 10 board by hand with board.py: net classes and rules, track width for current, clearance for voltage, ground pours and return paths, differential pairs and impedance, then DRC until nothing is unrouted. Use when routing or re-routing, choosing track widths or net classes, or adding pours. Edits are made with kicad-board-edit; to judge a finished layout, use kicad-layout-review."
---

# Route a board

Route by hand, net by net, after placement (`kicad-placement`), with `board.py` (`kicad-board-edit`): `connect`,
`track`, `via`, `gnd_via` and `zone`. Run DRC (printed on every save) until nothing is unconnected.

## Rules and net classes

These live in the `.kicad_pro` JSON; edit it only while the PCB editor is closed.

- **Setting them:** `board.py rules` writes the fab's minimums, the Default class and a Power class;
  `set_rules(pro, classes={...})` adds others. `connect` and `track` take their width from the net's class.
- **Classes:** `net_settings.classes`, each with `name`, `track_width`, `clearance`, `via_diameter`, `via_drill`
  and `priority` (lower wins).
- **Assigning nets:** `net_settings.netclass_patterns` entries such as `{"netclass": "Power", "pattern": "+5V"}`.
  Patterns match the board's net names exactly (`/VBUS`) and accept wildcards (`/USB_D*`).
- **Minimums:** `board.design_settings.rules` (`min_clearance`, `min_track_width`, …), at or above the fab's limits.

DRC enforces a class's clearance but not its track width. Where width matters, add a rule to `<board>.kicad_dru`
(comments on their own lines):

```
(version 1)
(rule "Power track width"
	(condition "A.NetClass == 'Power'")
	(constraint track_width (min 0.5mm)))
```

## Width for current

Outer layers at a 10 °C rise, from IPC-2221 (`I = 0.048 · ΔT^0.44 · A^0.725`, A in mil²):

| Current | 1 oz | 2 oz |
|---|---|---|
| 0.5 A | 0.15 mm | 0.1 mm |
| 1 A | 0.3 mm | 0.15 mm |
| 2 A | 0.8 mm | 0.4 mm |
| 3 A | 1.4 mm | 0.7 mm |
| 5 A | 2.8 mm | 1.4 mm |

- **20 °C rise:** about ⅔ of these widths.
- **Inner layers:** about 2.6× the width at the same copper weight. JLC's inner copper is 0.5 oz, so take about 5×
  the 1 oz column.
- **Voltage drop:** 1 oz copper is about 0.5 mΩ per square (0.3 × 30 mm ≈ 50 mΩ).
- **Vias:** a 0.3 mm drill with standard (about 20 µm) plating carries about 1 A.

## Clearance for voltage

Below 30 V the fab minimum is enough. Above it, IPC-2221 B2 (external, uncoated). The voltages are DC or AC peak:
230 VAC is 325 V peak, the 2.5 mm row.

| Voltage | Clearance |
|---|---|
| 31–150 V | 0.6 mm |
| 151–300 V | 1.25 mm |
| 301–500 V | 2.5 mm |

IPC-2221 is functional spacing only. For mains or anything a user can touch, the safety standard that applies (such as
IEC 62368-1) sets creepage and clearance, usually much larger: ask which. Put those nets in their own class so DRC
enforces the clearance.

## Pours

- **Pad connections:** keep thermal reliefs (the default). A solid connection on one pad of an 0402/0201 tombstones
  it in reflow, and through-hole pads tied solid to a pour are hard to hand-solder, which is how JLC fits through-hole
  parts. `zone(..., pads="solid")` suits a pour that only meets exposed or power pads. A "starved thermal" error on
  a pad boxed in by tracks: connect it with a track or a via.
- **Boxed-in pads:** a pour only reaches a pad through a gap at least its minimum width; a ground pad hemmed in by
  tracks stays unconnected even when poured solid (DRC lists it). Give each SMD ground pad its own `gnd_via()` to
  the other layer's pour as you route, rather than relying on the top pour.
- **Dead copper:** keep island removal on (`island_removal_mode 0`).
- **After filling,** look at each copper layer (`view.py pcb --layers B.Cu`): a route can pass DRC and still cut a
  pour into islands or leave a fast signal without ground under it.

## Differential pairs and impedance

- **Width and gap:** from the fab's impedance calculator for the stackup you will order (JLC has one).
- **2-layer 1.6 mm boards:** with the reference plane about 1.5 mm below, a 90 Ω microstrip pair is impractically
  wide; route it as coplanar waveguide with ground (CPWG) instead. USB full-speed only needs short and matched; short
  USB 2.0 high-speed runs work as CPWG; longer or faster links want 4 layers.
- **Length:** compare a pair by summing `t.GetLength()` (mm via `pcbnew.ToMM`) over each net's tracks, in KiCad's
  Python. Via barrels aren't included.
- **Nearby pour** lowers impedance: keep it at least twice the dielectric height away (about 3 mm on a 1.6 mm 2-layer
  board), or design the line as CPWG with that pour as part of it.
- **Reference copper:** no fast signal may cross a gap or slot in the ground under it. DRC can't see this; look at the
  other layer with `view.py` along each fast net.

## Pin swaps

If two nets cross only because of their pin assignment, swap interchangeable pins (op-amp or gate inputs, identical
units, same-function GPIOs, order-free connector pins). Confirm in the datasheet, change the schematic first, then
`board.py sync`, and report each swap.

## Doing it with board.py

1. **Plan from numbers.** `board.py pads` gives every pad's centre, size and net. Centreline to the edge of other
   copper: the clearance plus half the track width. Centreline to centreline of two tracks: the clearance plus half
   of each width.
2. **One routing script**, in a fresh process after placement: `connect` pad to pad (adding waypoints where the path
   must turn), `track` where every corner matters, vias where a net changes layer, `zone(...)` last.
3. **Iterate on the script, not the board:** start it with `remove_tracks(nets=["*"]); remove_zones()`, so a rerun
   replaces the whole route, and end it with `save(dry_run=True)` until DRC is clean, then `save()`. To route only
   new parts on a finished board, start with `remove_tracks(refs=[...])` for those parts instead, so a rerun
   doesn't duplicate vias or wipe the rest. Moving a part
   a few tenths of a mm often beats contorting a track: change the placement script and rerun both.
4. **Record** in the design notes any constraint a later change must respect.

Done when DRC reports no errors, no unconnected items and no parity issues.
