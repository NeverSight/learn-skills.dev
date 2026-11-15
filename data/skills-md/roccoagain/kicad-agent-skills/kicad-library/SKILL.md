---
name: kicad-library
description: "Creates or fixes KiCad 10 symbols and footprints for parts that aren't in KiCad's libraries: land patterns from the datasheet or IPC-7351, pin 1, courtyard and silk, 3D models, pin stacks, and symbol pins matched to footprint pads. Also sets up project library tables. Use when a part needs a new symbol or footprint, or a footprint might be wrong. To place an existing symbol, use kicad-schematic."
---

# Symbols and footprints

`K` is `kicad-cli` (see `kicad-view`). Footprint mistakes (a mirrored pinout, the wrong pitch, pin 1 in the wrong
corner) are the most common reason a first board fails, so check every footprint against the datasheet by the numbers.

## Where things live

- **Stock libraries:** `/Applications/KiCad/KiCad.app/Contents/SharedSupport/{symbols,footprints,3dmodels}` on macOS,
  or `/usr/share/kicad/...` on Linux. Search there first, for example
  `ls <footprints>/Package_SO.pretty | grep -i tssop`.
- **Project libraries:** `<project>.pretty/` and `<project>.kicad_sym`, listed in `fp-lib-table` and `sym-lib-table`
  with `${KIPRJMOD}` paths.
  - KiCad reads the project's tables only if the folder has a `.kicad_pro`.
  - Never edit the stock libraries. Copy the part into the project library instead.

## Footprints

Take pad sizes from the datasheet's **recommended land pattern**, not from the package drawing.

### No land pattern in the datasheet

`ipc_land.py` in this skill's folder computes IPC-7351B nominal pads the same way KiCad's generator does, from the
package's min/max dimensions:

```bash
python3 -I <this skill>/ipc_land.py gw 5.80 6.20 0.40 1.27 0.31 0.51   # SOIC-8: span L, lead length T, lead width W
# Z=6.90 G=3.00 X=0.60 -> pad 1.950 x 0.600 mm, pad centres at +/-2.4750 mm from the part's centre
```

- **Families:** `gw` for gull wing with pitch above 0.625 mm, `gw-fine` for 0.625 mm or less, and `qfn` for QFN/DFN.
  For `qfn`, L is the body size.
- **Accuracy:** the result matches KiCad's SOIC-8 exactly, and QFN, TSSOP and MSOP to within 0.1 mm.
- **Cross-check:** compare the result with a stock footprint of the same family and pitch. Recheck your inputs if any
  pad differs by more than 0.1 mm.
- **Exposed pad:** keep signal pads at least 0.2 mm from it.
- **Report:** show the numbers you entered, with the datasheet page they came from.

### File format and conventions (KLC)

A footprint file looks like this: `(footprint "Name" (version 20260206) (generator "pcbnew") (layer "F.Cu") (descr ...)
(tags ...) (property "Reference" "REF**" ...) (property "Value" "Name" ...) (attr smd|through_hole) ... (model ...))`.

**Origin and pads**
- **Origin:** the part's centre for SMD, and pin 1 for most through-hole parts. Pick-and-place uses this origin.
- **SMD pads:** `(pad "1" smd roundrect (at x y) (size w h) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25))`.
- **Through-hole pads:** `thru_hole` with `(drill d)` and `(layers "*.Cu" "*.Mask")`.
- **Mounting holes:** `np_thru_hole` with an empty pad number.
- **Pad numbers:** exactly the datasheet's pin numbers, including BGA ball names such as `A1`.
- **Exposed pad:**
  - Number it as the datasheet does.
  - Split the paste into a grid covering 50–70 % of the pad.
  - Add thermal vias if the datasheet asks for them. Vias in a pad wick solder unless tented or plugged (JLC plugs
    for a fee); note the choice for the order.

**Layers**
- **F.Fab:** the body at its real size, drawn with 0.1 mm lines, plus a pin-1 mark and `${REFERENCE}`.
- **F.SilkS:**
  - the outline, kept 0.2 mm from the pads;
  - a pin-1 mark that stays visible once the part is placed;
  - 0.12 mm lines, as KiCad uses (JLC prefers 0.15 mm).
- **F.CrtYd:**
  - a closed outline 0.25 mm outside the body and pads (0.15 mm for parts smaller than 0603, 0.5 mm for connectors,
    1.0 mm for BGAs);
  - points on a 0.01 mm grid;
  - 0.05 mm lines.

**3D model**
- Reference it like this: `(model "${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/SOIC-8_3.9x4.9mm_P1.27mm.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))`.
- Keep project models in `${KIPRJMOD}/3dmodels/`.
- Check the model's alignment in a render.

## Symbols

```
(symbol "LDO_TEST"
	(exclude_from_sim no) (in_bom yes) (on_board yes)
	(property "Reference" "U" (at -5.08 6.35 0) (effects (font (size 1.27 1.27)) (justify left)))
	(property "Value" "LDO_TEST" (at 0 6.35 0) (effects (font (size 1.27 1.27)) (justify left)))
	(property "Footprint" "Package_TO_SOT_SMD:SOT-23-5" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
	(property "Datasheet" "https://..." (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
	(property "Description" "..." (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))
	(symbol "LDO_TEST_0_1"
		(rectangle (start -5.08 5.08) (end 5.08 -5.08) (stroke (width 0.254) (type default)) (fill (type background))))
	(symbol "LDO_TEST_1_1"
		(pin power_in line (at -7.62 2.54 0) (length 2.54) (name "VIN" (effects (font (size 1.27 1.27))))
			(number "1" (effects (font (size 1.27 1.27)))))
		...)
	(embedded_fonts no))
```

**Units**
- `Name_0_1` holds graphics shared by all units.
- `Name_1_1`, `Name_2_1`, and so on hold each unit's pins.

**Pins**
- **Position:** library y points up. A pin's `(at x y angle)` is its connection end, and `angle` points into the body.
  Put pin ends on the 2.54 mm grid, with a length of 2.54 mm.
- **Types:** these drive ERC.
  - `power_in` for supply pins;
  - `power_out` for regulator outputs;
  - `input`, `output` and `bidirectional` for signals;
  - `passive` for resistors and connectors;
  - `no_connect` for NC pins.

  Types that are too loose hide real errors, and types that are too strict raise false ones.
- **Layout:** follow the project library's existing symbols, else KiCad's library conventions (KLC).
- **Repeated pins:** make one pin numbered `"[2,5,8,11]"` or `"[1-4]"`, which is a KiCad 10 native stack. Don't stack
  hidden pins on top of each other; KiCad flags that as a legacy stack.
- **Alternate functions:** give the pin its main name, then add the others as `(alternate "USART1_TX" bidirectional line)`
  entries. Don't join the names with slashes.
- **Name formatting:** `~{RESET}` draws an overbar, `_{x}` a subscript, and `^{x}` a superscript.
- **Pin table:** the datasheet's pin table is the source of truth. If the table in the PDF is an image, have the user
  confirm your reading of it.

## Check every new or changed part

1. **Parse.** Write the output to scratch: an in-place upgrade re-sorts the whole library.

   ```bash
   mkdir -p <scratch>/chk && "$K" fp upgrade --force -o <scratch>/chk <lib>.pretty
   "$K" sym upgrade --force -o <scratch>/chk/x.kicad_sym <lib>.kicad_sym
   ```

   Exit code 2 with "Unable to load library" means a syntax error.
2. **Render.**

   ```bash
   "$K" fp export svg --fp <Name> -o <scratch>/svg <lib>.pretty
   "$K" sym export svg -o <scratch>/svg <lib>.kicad_sym
   ```

   The output folder must already exist. Convert each SVG to PNG with `rsvg-convert -w 1000 -b white x.svg -o x.png`
   (librsvg: `brew install librsvg` or `apt install librsvg2-bin`).
   Check pin 1, the pad shapes and the outline.
3. **Numbers.** Make a short table comparing the file with the datasheet:
   - pitch;
   - row spacing (pad centre to pad centre);
   - pad size;
   - pin-1 position;
   - exposed pad.
4. **Pins against pads:** `python3 <this skill>/pinpad.py <lib>.kicad_sym <Symbol> <lib>.pretty/<Footprint>.kicad_mod`
   lists pins without a pad and pads without a pin (native stacks expanded).
   - Both lists must be empty, unless a pad is deliberately unconnected. If so, say which.
   - Then check each pin's function against the pinout for this exact package. Other packages of the same part often
     number their pins differently.
5. **On the board.** After `board.py sync` (`kicad-board-edit`), DRC reports any courtyard overlaps, clearance
   problems, and `lib_footprint_mismatch`.

## Changing a part that's already in use

- **Schematics:** each schematic keeps its own copy of the symbol. `lib_symbol_mismatch` catches moved pins, but not
  renamed ones. Re-copy the symbol into every schematic that uses it with
  `s.refresh_symbol("Lib:Name")` (`kicad-schematic`), then check the netlist.
- **Boards:** each board keeps its own copy of the footprint, so DRC reports `lib_footprint_mismatch`. To update it,
  delete the part, re-add it with `board.py sync`, and re-route its pads.
