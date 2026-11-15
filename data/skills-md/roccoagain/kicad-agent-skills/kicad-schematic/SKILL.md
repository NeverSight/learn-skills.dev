---
name: kicad-schematic
description: "Edits or draws a KiCad 10 schematic with sch.py, a small Python library in this skill's folder: adds symbols (including multi-unit parts), wires, labels, power symbols and no-connects by pin, changes values and fields, then checks with ERC and carries the change to the board. Use when making any schematic change, such as adding a part, connecting nets or changing a value, and when drawing a new schematic. To create a symbol, use kicad-library."
---

# Change a schematic

Make every change with `sch.py` (this skill's folder) from a short script in `<scratch>`. It needs only `python3`.
It handles the parts that go wrong by hand:
- copying and flattening library symbols;
- pin positions under rotation and mirroring;
- instances, references, UUIDs and string escaping;
- junctions;
- running ERC after every save.

It inserts new items and leaves the rest of the file byte for byte, so the diff shows only the change.

```python
import sys; sys.path.insert(0, "<skill dir>")              # this SKILL.md's folder
from sch import Schematic

s = Schematic("board.kicad_sch")                           # refuses if KiCad has the sheet open
s.add("Device:C_Small", "C?", (120.65, 50.8), value="100nF",            # "C?" = next free C; on the 1.27 mm grid
      footprint="Capacitor_SMD:C_0603_1608Metric", fields={"LCSC": "C14663", "Voltage": "50V"})
s.add("MCU_ST_STM32G0:STM32G030F6Px", "U2", (170.18, 82.55), footprint="Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm")
s.power("C1", "1", "+3V3"); s.power("C1", "2", "GND")     # on the pin, pointing away from the part
s.power("U2", "4", "+3V3", stub=2.54)                      # after a 2.54 mm wire
s.label("U2", "9", "UART_TX")                              # stub + label, text reading away from the part
s.connect(("U2", "4"), ("C1", "1"))                        # wire with at most one bend (first="v" to go vertical first)
s.wire(("D1", "2"), (150, 124.46), ("R3", "1"))            # explicit corners; legs horizontal or vertical
s.nc("U2", "7")
s.set_field("R3", "Value", "1k")                           # existing or new symbol, every unit; new fields hidden
s.add("Amplifier_Operational:LM358", "U3", (127, 88.9), unit=2)         # another unit of U3: fields copied
s.refresh_symbol("MyLib:LDO")                              # re-copy a symbol changed in its library
s.remove("J2")                                             # a part plus its stubs, labels and no-connects
s.add("Connector:Conn_ARM_SWD_TagConnect_TC2030-NL", "J2", (196.85, 121.92),
      in_bom=False, in_pos=False)                          # footprint-only part: no BOM line, not placed
s.box(125, 25, 215, 140, "MCU")                            # dashed block outline with a bold title
s.text("Place C1 at U2 pin 4", 135, 50)                    # notes; "\n" for line breaks
s.save()                                                   # writes, adds junctions, prints lint and ERC
```

To plan a placement:
- `python3 sch.py symbol Lib:Name` lists a library symbol's pins: number, name, type and offset.
- `python3 sch.py pins board.kicad_sch U2 [R3 ...]` lists where placed symbols' pins land, and which way each
  points.
- `s.pin(ref, n)` returns `(x, y, out_dx, out_dy)` inside a script; `s.units(ref)` lists a part's placed units.
  A pin on a unit that isn't placed yet raises an error naming the unit to add.
- `python3 sch.py lint board.kicad_sch` reports text overlapping text, wires, pins or parts, wires running through a
  part, and points off the grid. It measures text from KiCad's own plot, and `save()` runs it.

Coordinates are sheet mm, with y pointing down; `add()` refuses a position off the 1.27 mm grid. Rotation is
counter-clockwise, and `mirror="x"|"y"` is applied after rotating.

## Before

- **Editor closed.** If the sheet is open in KiCad (`~<name>.kicad_sch.lck`), its next save overwrites your edit.
  `Schematic()` refuses to open it, so ask the user to close it.
- **Clean git tree,** and one session per sheet: `.kicad_sch` files merge badly.
- **Pin lists:** save `view.py pins` (`kicad-view`) for the parts you'll touch, to diff afterwards.

## Drawing

Follow the sheet's existing conventions: symbols, block layout, label style, power-symbol direction, value units.
On a new sheet, KiCad's defaults. Lint must show no new problems (run `sch.py lint` before the edit to know what was
already there); then look at the area you changed (`view.py sch --around U2,C3`).

Facts that trip the drawing up:
- `R_Small`/`C_Small` pin 1 is the **top** pin at rotation 0.
- `Device:LED` and `Device:D` pin 1 is the cathode (K), and so is pad 1 of KiCad's LED and diode footprints.
- A rail fed only by a connector or a regulator output needs one `PWR_FLAG` on its wire
  (`s.power_at(x, y, "PWR_FLAG")`), or ERC reports "input power pin not driven".
- Field positions come from the library symbol and turn with the part, as in KiCad. Pass `ref_at=(x, y)` or
  `value_at=(x, y)` (sheet mm) to `add()` to move them; a moved field reads horizontally.
- KiCad's pair router finds differential pairs by a `+`/`-` or `P`/`N` name ending.
- Compare each block with its datasheet's reference circuit, and report every departure and open choice you made.

## Limits of sch.py

- **Multi-sheet designs:** it edits one sheet file at a time. New symbols on a sub-sheet get the right instance path,
  found through the sheet symbols that use the file, and `"R?"` numbers stay unique across the hierarchy. It can't
  add sheet symbols, and a sheet used more than once gets one reference for all its uses: annotate in KiCad.
- **Library changes:** a sheet keeps its own copy of each symbol. After changing a symbol in its library, call
  `s.refresh_symbol("Lib:Name")` so the sheet uses the new version; `remove()` and `add()` alone keep the old copy.
- **Moving or replacing a part:** use `remove(ref)`, then `add()` it again with its connections. `remove()` takes
  the stub wires, labels, power symbols and no-connects that hang off the part's pins. It stops at branches and at
  other parts' pins, so shared nets survive.
- **Not handled:** editing existing wires, labels and text. Make those as small text edits to the file, and
  confirm with ERC and the netlist.
- **Regenerating:** don't regenerate a whole sheet once a board exists. New symbol UUIDs break the board's links to
  its symbols (parity fails). Edit in place instead.

## After

1. **ERC and lint** print on every save: no new errors or problems (`kicad-check` for the full run).
2. **Netlist:** check every touched pin is on the intended net and nothing else changed (`view.py pins`, diff with
   before).
3. **Update the board:** run `"$KPY" -I board.py sync` (`kicad-board-edit`). It adds parts, copies values and
   fields, and moves unrouted pads to new nets. A footprint change, or a routed pad on a changed net, needs
   re-routing.
4. **Update the documents:** design notes, the test plan (`kicad-bringup`) if a reading changed, and the BOM/order if a
   part number changed.
