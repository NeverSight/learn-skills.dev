---
name: kicad-layout-review
description: "Reviews a finished KiCad 10 PCB layout against its datasheets and its circuit: datasheet layout sections, decoupling distances, regulator and crystal loops, return paths under fast signals, differential pairs, track widths for current, thermal copper, ground pours, ESD parts at connectors, connectors and mounting against the enclosure, silkscreen polarity marks, assembly and test access. Reports findings worst first with board locations and proposed fixes; makes no edits. Use when a layout is finished or changed, before ordering, or when the user asks whether a board's layout is good. For the schematic's electrical design, use kicad-schematic-review; for DRC and manufacturing limits, kicad-check."
---

# Review a board layout

DRC passing means the copper obeys the rules. This skill asks whether the layout serves the circuit, which no rule
checks. The output is a findings table for the user; it changes nothing. Fixes are made afterwards with
`kicad-placement`, `kicad-routing` and `kicad-board-edit`, once the user has chosen them.

## Before

- **Rules first:** run `kicad-check` and leave its findings to it.
- **Design notes:** read DESIGN.md (or CLAUDE.md, AGENTS.md). A finding the user already accepted there is reported
  as "expected", not as new.
- **Layout sections:** collect the layout guidance from the datasheet of every regulator, crystal or oscillator,
  interface IC and connector that has one. Those are the main requirements of this review.
- **Fast nets:** list them from the schematic: clocks, crystal pins, SPI/SWD, USB and other differential pairs,
  switch nodes, and anything the datasheets call sensitive.

## Measuring

With KiCad's Python (`KPY`, see `kicad-board-edit`):
- `board.py pads board.kicad_pcb [REF ...]`: pad centres, sizes and nets.
- `board.py tracks board.kicad_pcb [NET ...]`: every track's ends, layer and width, and every via.
- `board.py nets board.kicad_pcb`: each net's routed length, narrowest and widest track, layers, vias, and for each
  signal via the distance to the nearest ground via.
- `board.py score board.kicad_pcb`: courtyard overlaps, edge distances, and each capacitor's distance from its rail
  pad to the nearest IC pad on that rail.

With `view.py` (`kicad-view`): one copper layer per picture (`--layers B.Cu,Edge.Cuts`), crops around each part
(`--around U2`), the silkscreen layers on their own, and a 3D render for connectors and tall parts. Take numbers from
the measurements and use pictures to see shapes: pours, loops, gaps.

## Checks

| Check | Pass when |
|---|---|
| Datasheet layout sections | Each stated requirement is met (distances, keep-outs, thermal vias, track lengths, copper areas). List every requirement with its result |
| Decoupling | Each IC supply pin's capacitor is within about 2 mm of the pin (or the datasheet's distance), on the same side, between the supply's arrival and the pin, and its ground pad reaches ground through a via or the pour within about 1 mm. A cap whose ground returns through a long track does little |
| Switching regulator | Input cap, switch and their ground form the smallest loop, on one layer. The switch node's copper is no larger than its pads need. The feedback divider sits at the FB pin, its track away from the inductor and switch node. No sensitive tracks under the inductor |
| Crystal or oscillator | Crystal and load caps within a few mm of the pins, the load caps' ground short, no other tracks between them or under them on the next layer |
| Return paths | Each fast track has unbroken ground on the next layer along its whole length: look along it on that layer. Each fast signal via has a ground via within about 1.5 mm (`board.py nets`). No fast track crosses a pour split or slot |
| Differential pairs | Both tracks run together with the same width, gap, layer changes and via count; their lengths (`board.py nets`) match to the interface's tolerance |
| Ground pours | No islands, and no necks narrower than a few track widths carrying return current. On two or more layers, stitching vias join the pours along the edges and near each IC's ground pins |
| Current | The narrowest track on each power net (`board.py nets`) carries its worst-case current by `kicad-routing`'s table; layer changes on power nets have enough vias (about 1 A per 0.3 mm drill) |
| Voltage clearance | Nets above 30 V keep `kicad-routing`'s spacing from everything else, through their own net class |
| Thermal | Exposed pads have the datasheet's thermal vias and copper area. Parts dissipating the power `kicad-schematic-review` computed have that copper. Hot parts sit away from temperature-sensitive ones (sensors, crystals, electrolytics, batteries) |
| ESD and protection | Each protection part is at its connector, and the protected track reaches its pad before anything else, with a short, wide path to ground |
| Analog and high impedance | High-impedance and analog nodes are short, and kept away from switch nodes, clocks and digital edges |
| Connectors and mechanics | Connectors sit flush with or overhang the edge as the enclosure needs, with pin 1 matching the mating cable. The circle under each screw head is clear of other nets' copper (`kicad-new-project`). Part heights clear the enclosure (STEP from `kicad-fab-export`) |
| Silkscreen | Every polarised part (diode, LED, electrolytic, battery, IC and connector pin 1) has a mark that stays visible once the part is fitted. References are readable, beside their part, not under a body. The board name and revision are on the silkscreen |
| Assembly | Small chip parts have matching copper on both pads (both thermal-relieved, or both on similar tracks), or they tombstone. Fine-pitch parts leave room for rework. JLC assembly: part bodies 2.5 mm from the edge, or rails (`kicad-assembly-export`) |
| Test access | The programming or debug connector is reachable with the board in place. Each rail and signal that TEST_PLAN.md (`kicad-bringup`) measures has a pad or test point to probe |

## Report

- **Findings, worst first.** For each: the location (board mm and the parts), what goes wrong physically, the
  measured number against its requirement and the source of that requirement, and a proposed fix with the skill
  that makes it. Group repeats ("4 × signal via over 3 mm from a ground via, all on /CANL").
- **Passed checks**, closest to their limits first, so the user sees the margins.
- **Couldn't check:** anything that needs the ordered stackup, a measurement, the enclosure or a missing datasheet.
- **Design notes:** record only findings the user accepts, with the reason, and only with their agreement.
