---
name: kicad-assembly-export
description: "Makes JLCPCB assembly files (BOM and CPL/pick-and-place) from a KiCad 10 board and checks the order: LCSC numbers on every placed part, BOM and CPL agree, parts clear of the edge, rotations. Use when the user wants JLC to assemble a board, asks for a BOM, CPL, centroid or pick-and-place file, or adds LCSC numbers. For Gerbers, use kicad-fab-export."
---

# Export a board for JLCPCB assembly

`K` is `kicad-cli` (see `kicad-view`). Gerbers come from `kicad-fab-export`.

## What JLC accepts

From JLC's help center, read on 2026-11-05:
- **BOM:** columns `Comment`, `Designator`, `Footprint` and `JLCPCB Part #`.
  - Separate designators with commas, with no ranges and no repeats.
  - Put at most 200 designators in one row.
  - Use csv, xls or xlsx.
- **CPL:** columns `Designator`, `Mid X`, `Mid Y`, `Layer` (`Top`/`Bottom`) and `Rotation`.
  - Positions are in mm. Rotation is in degrees, counter-clockwise positive.
  - Put both sides in one file.
- **Both files:**
  - JLC places a part only if its designator appears in both files, matched exactly, including case.
  - The CPL and the Gerbers share one origin. The jobsets use KiCad's absolute origin, so if you change
    `use_drill_place_file_origin`, change the Gerber job's `use_drill_origin` to match.

## Part numbers

Each part JLC places needs an `LCSC` field (`C` + digits). Add it with `kicad-schematic`, then run `board.py sync`
(`kicad-board-edit`). If the project already uses another field name, change `fields_ordered` in the jobset instead. To
choose parts, use `kicad-part-selection`.

## Setup, once per project

```bash
cp <skill dir>/jlc-assembly.kicad_jobset <project dir>/
```

The jobset writes `fab/assembly/<project>_bom.csv` and `fab/assembly/<project>_cpl-all-pos.csv`. Commit it with the
project.

- **BOM:**
  - leaves out DNP parts and parts excluded from the BOM;
  - groups rows by value, footprint and LCSC number;
  - writes no designator ranges.
- **CPL:**
  - includes both sides, in mm, from the absolute origin;
  - leaves out DNP parts and parts marked "exclude from position files", such as mounting holes and fiducials;
  - keeps through-hole parts. If JLC won't fit them, set `exclude_footprints_with_th: true`.

## Export

JLC cuts the stencil from the paste layers in the Gerber zip: add `F.Paste` (and `B.Paste` for bottom parts) to the
fab jobset's layers (`kicad-fab-export`) before ordering assembly.

Run this after the DRC gate and the Gerbers:

```bash
"$K" jobset run --stop-on-error -f jlc-assembly.kicad_jobset board.kicad_pro
```

Then convert KiCad's position file into JLC's CPL, applying rotation corrections from `jlc-rotations.csv` in the
project (columns `Match,Offset`; `Match` is a designator or a `Package` value, and a designator row wins) and writing
the side as `Top`/`Bottom`:

```bash
python3 <skill dir>/jlc_asm.py cpl fab/assembly/<p>_cpl-all-pos.csv fab/assembly/<p>_cpl.csv jlc-rotations.csv
```

The y values come out negative. That's expected, and they match the Gerbers.

## Check before ordering

1. **BOM against CPL:** `python3 <skill dir>/jlc_asm.py check fab/assembly/<p>_bom.csv fab/assembly/<p>_cpl.csv`
   lists parts in one file only, placed parts without an LCSC number, malformed numbers, and the sides used.

   - **No LCSC number:** JLC won't fit the part. Say whether the user will supply it or hand-solder it later.
   - **Wrong part behind a number:** the check only sees that a number exists. JLC fits whatever the C-number names,
     so look up each number's package, value and variant on lcsc.com and compare them with the row's Footprint and
     Comment. A C-number for an 0603 on an 0402 footprint is built without complaint.
   - **Both sides listed:** the order needs Standard assembly.
2. **Distance from the edge.** JLC wants part bodies at least 2.5 mm from the edge, unless rails are added. First add
   any parts JLC won't place to the exclusion list in a copy of `jlcpcb-assembly.kicad_dru`, then, with KiCad's Python
   (`kicad-board-edit`), run `drc("board.kicad_pcb", rules="<copy>", parity=False)` from `board.py`. It runs on a
   temporary copy; the findings that matter name the rule "JLC assembly: part to board edge".
3. **Economic or Standard:**

   | | Economic | Standard |
   |---|---|---|
   | Sides | one | one or both |
   | Board | 10×10–470×500 mm, 0.8–1.6 mm, 2/4/6 layers | 70×70–460×500 mm |
   | Smallest package | 0402 | 01005 |
   | IC / BGA pitch | 0.4 / 0.5 mm | 0.35 / 0.3 mm |
   | Quantity | 2–50 | 2–80,000 |
   | Rails, fiducials | not needed | needed (JLC adds them) |

   Use nominal (IPC-7351 density level B) land patterns, as KiCad's stock footprints do. Check JLC's assembly page
   before using level A ("Most", the largest pads) or C ("Least", high density).
4. **Rotations.** JLC defines each package's zero angle by its tape orientation, which sometimes differs from KiCad's,
   and JLC doesn't publish its convention.
   - Ask the user to check every polarised part in the placement preview on JLC's order page before paying: ICs,
     diodes, LEDs, electrolytics, transistors and connectors.
   - For each part shown wrong, add a package line to `jlc-rotations.csv`, re-export and check again. Commit the file.
   - Community tables, such as `cpl_rotations_db.csv` in matthewlai/JLCKicadTools, are useful starting guesses. They are
     not JLC's own.
5. **Bottom side.** JLC's convention for the bottom side isn't documented. Check every bottom part in the preview, and
   prefer one-sided assembly.
6. **Origin off-centre.** JLC places parts by their centre, but many connector and through-hole footprints have their
   origin on pin 1. Check these in the preview.

## Rules

- **Hand edits:** never edit the BOM or CPL by hand, except through the CPL step above. Fix the schematic or
  `jlc-rotations.csv`, then re-export.
- **Re-export:** after any change to the board or the part numbers, re-export both files. If the project keeps them,
  commit them with the change.
