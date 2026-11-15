---
name: kicad-view
description: "Shows a KiCad 10 schematic or PCB with view.py (this skill's folder): KiCad's own plots cropped to named parts, each pin's net from KiCad's netlist, resistance between nets, checks of stated connections and decoupling, a 3D render, and a comparison of two git revisions. Use whenever a design needs looking at, before and after any edit, to check a connection, to see what a commit changed, or when the user asks to see or screenshot a board or schematic."
---

# Look at a KiCad design

`view.py` (this skill's folder) runs `kicad-cli` and poppler's `pdftoppm`/`pdfinfo` (`brew install poppler` or
`apt install poppler-utils`) with plain `python3`. Write its output to `<scratch>`,
never into the project, and open the PNGs to look at them.

```bash
V=<skill dir>/view.py
python3 $V sch board.kicad_sch -o <scratch>/sheet.png                    # whole sheet
python3 $V sch board.kicad_sch -o <scratch>/u2.png --around U2,C3       # zoomed to these symbols
python3 $V sch board.kicad_sch -o <scratch>/a.png --zoom 120,30,80,60   # window x,y,w,h (sheet mm); --page N
python3 $V pcb board.kicad_pcb -o <scratch>/top.png                     # whole board, F.Cu + silk + outline
python3 $V pcb board.kicad_pcb -o <scratch>/u2.png --around U2 --layers F.Cu,F.SilkS,F.CrtYd,Edge.Cuts
python3 $V pcb board.kicad_pcb -o <scratch>/bot.png --back              # bottom, seen from below (mirrored)
python3 $V pins board.kicad_sch U2 R3                                    # each pin's net (no refs: every part)
python3 $V net board.kicad_sch /I2C_SDA                                  # every pin on a net
python3 $V ohms board.kicad_sch +3V3 [GND]                               # resistance between nets, resistors only
python3 $V expect board.kicad_sch DESIGN.md                              # check stated connections
python3 $V decoupling board.kicad_sch                                    # each IC supply pin and the caps on its rail
```

`--dpi` and `--margin` adjust the crops. `kicad-cli` is found at its usual place on macOS and Windows, or on `PATH`,
or from `$KICAD_CLI`.

- **Connections come from the netlist, not the picture.** A wire that looks connected but isn't shows up as its own net:
  a missing junction, a label one character off, or an end one grid step away. Unnamed nets read `Net-(C2-Pad2)`;
  unconnected pins read `unconnected-(U1-NC-Pad5)`. Names escape `/` as `{slash}`.
- **`ohms`** solves the resistor network between two nets (capacitors open, ICs and diodes ignored), lists the other
  parts across both nets, whose leakage or clamps can change a meter reading, and lists series chains of two-pin parts
  that aren't all resistors (an LED and its resistor): give those both meter polarities. Values read like KiCad's
  (`4k7`, `10k`, `1M`, `100R`; `m` is milli).
- **`expect`** reads every line shaped like `` `U2.4 = +3V3` `` (pin on a net) or `` `U2.4 == C3.1` `` (two pins on
  one net) from any file, such as a list in DESIGN.md, and reports each mismatch. Exit code 1 on a mismatch or
  when no line matched.
- **`decoupling`** lists each IC's `power_in` pins by rail with the capacitors from that rail to ground, and flags a
  rail with none. Exit code 1 if any.
- **Pictures are for spotting problems.** Take numbers from the files or from `board.py pads`.
- **Overlap:** judge text overlap only from a zoomed crop. A whole sheet is too small.
- **Layers:** use canonical names (`F.SilkS`, `F.CrtYd`, `In1.Cu`). One copper layer per picture, since a bottom pour
  hides top tracks.

## 3D render

`K` is `kicad-cli`: `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli` on macOS,
`C:/Program Files/KiCad/10.0/bin/kicad-cli.exe` on Windows, `kicad-cli` on Linux.

```bash
"$K" pcb render -o <scratch>/3d.png --side top --quality basic --width 1600 --height 1000 board.kicad_pcb
```

Add `--zoom 4 --pan "X,Y,0"` for a close-up (aim by trial), and `--side bottom`, `--perspective` or `--rotate` for
other views. Parts without a 3D model (some sensors) show only their pads.

## Compare two revisions

```bash
mkdir -p <scratch>/old <scratch>/new
git archive <old-rev> | tar -x -C <scratch>/old       # or use the working tree as "new"
git archive <new-rev> | tar -x -C <scratch>/new
for t in old new; do python3 $V pins <scratch>/$t/board.kicad_sch > <scratch>/$t.tsv; done
diff <scratch>/old.tsv <scratch>/new.tsv
```

- **Changed lines** are pins whose net changed.
- **Auto-named nets** (`Net-(...)`) rename when their namesake part changes. Check them, but they aren't
  necessarily changes.
- **Values and fields:** run `"$K" sch export bom --fields 'Reference,Value,Footprint,${DNP}' -o <scratch>/$t.csv
  <scratch>/$t/board.kicad_sch` for both trees and diff the two files.
- **Pictures:** plot the same area from both trees and compare them side by side.
