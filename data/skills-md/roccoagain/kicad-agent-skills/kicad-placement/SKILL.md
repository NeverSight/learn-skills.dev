---
name: kicad-placement
description: "Decides where parts go on a KiCad 10 PCB: pin assignment from the floor plan, datasheet layout constraints, fitting passives at fine-pitch pins, assembly clearances, and comparing candidate placements with board.py score. Use when planning a new placement or redoing one. Moves are made with kicad-board-edit; to judge a finished layout, use kicad-layout-review."
---

# Where parts go

The layout is yours to design. This skill holds the facts and checks that are easy to miss.

## Before placing

- **Datasheet layout sections are requirements.** Where a datasheet leaves a choice open, make it and say it's your
  inference. If its reference design has a part the schematic lacks, report it rather than adding it.
- **Fixed parts first:** the outline, holes, connectors and whatever the enclosure fixes. Ask what fixes them.
- **Assign pins from the floor plan, before the schematic is final.** On an MCU with alternate functions, and on any
  connector or header whose order is free, choose pins from where the other end sits, so buses leave on the side
  they're going and signals don't have to cross. A pin change after placement means a schematic edit, `board.py
  sync`, and re-routing.
- **Bottom side:** ask before placing parts there.

## Passives at fine-pitch pins

Two passives centred on neighbouring pins fit only if the sum of their courtyard widths is no more than twice the
pitch. KiCad's stock courtyard widths:

| Size | Courtyard width |
|---|---|
| 0201 | 0.70 mm |
| 0402 | 0.92 mm (C), 0.94 mm (R) |
| 0603 | 1.46 mm |

So two 0402s fit at 1.27 mm pitch, but not at 0.65 or 0.5 mm. Each pad also needs room in front of it for its
track to escape.

## Assembly

- **Courtyards** must not overlap.
- **Edge clearance** for machine assembly: JLC wants parts 2.5 mm from the edge, or rails (`kicad-assembly-export`).
- **Hand soldering** needs room for the iron: about 1 mm between pads of neighbouring parts, and thermal reliefs on
  pads in pours.

## Doing it

1. **One placement script** (`board.py`, `kicad-board-edit`) holding every part's `place(ref, x, y, rot)`, ending
   with `auto_labels()` and `save()`. Rerun it whenever placement changes. Adding parts to a finished board instead:
   place only those, and pass them to `auto_labels([...])` so the other references stay put.
2. **Positions from numbers:** take pad coordinates from `board.py pads`, not from a picture. Placing by eye is often
   0.3 mm off.
3. **Compare candidates by number:** `b.score()` after the `place()` calls, without saving, prints airwire length,
   crossings, courtyard overlaps, edge distances and decoupling distances. Fewer crossings mean fewer vias; the
   parts with the most airwire are the ones to move. Decoupling caps belong within about 2 mm of their IC's supply
   pin (or the distance the datasheet gives); the list includes every cap to ground, so skip bulk and filter caps.
4. **Look** at the result (`view.py pcb`, `kicad-view`), and record in the design notes any placement a later change
   must respect.
5. **Next:** route (`kicad-routing`).
