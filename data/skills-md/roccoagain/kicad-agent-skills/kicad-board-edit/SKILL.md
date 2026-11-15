---
name: kicad-board-edit
description: "Edits a KiCad 10 PCB with board.py, a small library in this skill's folder run with KiCad's bundled Python: creates the board and outline, brings parts in from the schematic (sync), places and rotates parts, adds tracks, vias, pours and holes by pad, changes pad nets, places silkscreen references, then refills and runs DRC on save, or a dry run on a copy. Use when editing a .kicad_pcb in any way, or after a schematic change. For deciding where parts go or how to route, see kicad-placement and kicad-routing."
---

# Edit a board

Make every change with `board.py` (this skill's folder), from a short script in `<scratch>`. Run it with KiCad's
bundled Python (`KPY`):

| OS | `KPY` |
|---|---|
| macOS | `/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3` |
| Linux | the system `python3` that can `import pcbnew` |
| Windows | `C:/Program Files/KiCad/10.0/bin/python.exe` |

Run scripts as `"$KPY" -I script.py`. Ignore the "create wxApp" assertion and the swig "memory leak" lines; they're
harmless.

```python
import sys; sys.path.insert(0, "<skill dir>")
from board import Board

b = Board("board.kicad_pcb")                      # refuses if the board is open in KiCad
b.place("C3", 119.6, 115.35, rot=270)             # mm; degrees CCW; side="B" flips. Keeps 3D models
b.score()                                         # placement metrics after the moves above (no save needed)
b.connect(("C3", "1"), ("U2", "4"))               # net, class width and layer from the pads; one 45° bend per leg
b.connect(("U2", "9"), (115.7, 105.6), ("J1", "2"), first="diagonal")   # through a waypoint; "x"/"y": 90° elbow
b.track("/SDA", [("U2", "11"), (119.0, 112.6), (128.9, 112.6)], layer="B.Cu")   # every corner explicit
P = b.pad                                         # P("U2", "4") -> (x, y), after the moves above
b.via(119.0, 112.6, "/SDA")                       # 0.6 / 0.3 mm
b.gnd_via("C3", "2", dx=0, dy=1.2)                # via plus a stub from the pad
b.zone("GND", ["F.Cu", "B.Cu"])                   # pour over the outline; thermal reliefs (pads="solid": see routing)
b.set_pad_net("J2", "2", "/NRST")                 # only after the same change in the schematic
b.remove_tracks(nets=["/SDA"], region=(115, 110, 135, 120))   # or nets=["*"]; b.remove_zones()
b.remove_tracks(refs=["R3", "D1"])                # the copper hanging off these parts, up to the next pad/branch
b.label("C3", 119.6, 113.2)                       # silkscreen reference, upright
b.auto_labels(["R3", "D1"])                       # beside each courtyard; no argument moves every reference
b.text("SNIFFER rev 2", 121, 103.5, layer="B.SilkS")   # free text; mirrored on the back
b.outline(36, 19, 100, 100, r=1.0); b.add_footprint("H1", "MountingHole:MountingHole_2.2mm_M2", 102.5, 102.5)
b.remove_footprint("J1"); b.remove_outline(); b.remove_texts()   # removals, for replacing or rerunning
b.save()                                          # writes, refills zones, prints DRC with parity
b.save(dry_run=True)                              # or: DRC on a temporary copy; the board file is untouched
```

Command line, with `KPY`:
- `board.py pads board.kicad_pcb [REF ...]`: each part's position, and every pad's centre, size and net. Plan from
  this.
- `board.py tracks board.kicad_pcb [NET ...]`: every track's ends, layer and width, and every via. To join a net that
  already has copper, end the new track exactly on one of these points (or put a via there).
- `board.py nets board.kicad_pcb`: each net's routed length, narrowest and widest track, layers and vias, and each
  signal via's distance to the nearest ground via.
- `board.py score board.kicad_pcb [--skip GND]`: airwire length per net and per part, airwire crossings, courtyard
  overlaps, parts near or past the edge, how much of the board the parts cover, and each capacitor's distance from
  its rail pad to the nearest IC pad on that rail. Poured nets are skipped in the airwires; routed connections still
  count, so on a routed board compare scores before and after rather than reading them alone.
- `board.py sync board.kicad_pcb`: "Update PCB from Schematic". It adds missing parts below the board, copies
  values, fields and DNP/BOM flags, moves unrouted pads to new nets, and restores lost 3D models. It reports
  footprint changes, routed pads on changed nets, and parts the schematic lacks.
- `board.py new board.kicad_pcb W H --holes M3`: a new board with a rounded W × H outline at (100, 100) and four
  mounting holes 4 mm in from the corners.
- `board.py rules board.kicad_pro --power +5V,+3V3,GND --power-width 0.5`: JLC-safe minimums, a 0.2/0.25 mm Default
  class and a Power class, written to the `.kicad_pro` (`set_rules()` for other classes; see `kicad-routing`).

In a script, `drc("board.kicad_pcb", rules="other.kicad_dru", parity=False)` (from `board`) runs DRC on a temporary
copy against another rule file, such as `kicad-assembly-export`'s edge-clearance rule.

Lengths are mm in board coordinates (y down). Points are `(x, y)` or a pad `(ref, num)`. `connect()` and `track()`
draw the geometry they're given and don't steer around other copper: the DRC from `save(dry_run=True)` shows what
they hit. Track widths default to
the net's class in the `.kicad_pro`. A two-pad part at 0° has pad 1 on the left; at 90°, pad 1 is below;
at 270°, above. `gnd_via()` draws its stub on F.Cu unless you pass `layer="B.Cu"` for a bottom-side pad.

## Rules

- **One save per process.** In KiCad 10's bindings, objects read after anything is added or removed come back
  broken. So `board.py` queues tracks, vias, zones and removals until `save()`. Read every pad position before
  saving, and start a new process for the next edit. Keep placement and routing in separate scripts.
- **Try before writing.** While iterating on a route, end the script with `save(dry_run=True)`: the same DRC report,
  from a temporary copy of the project. Switch to `save()` once it's clean.
- **Editor closed.** The editor's next save overwrites the file, so ask the user to save and close the board first.
- **Schematic first.** Anything the schematic owns changes there first, then `board.py sync`: parts, footprints,
  values, fields and pin swaps. Nets come only from the schematic; `board.py` can't invent one.
- **Clean git tree** before each edit, so it's one diff. A project outside git: copy its files to `<scratch>`
  first, or ask the user to `git init`. Every save refills the pours, so the diff also rewrites their
  `filled_polygon` blocks; read the other changes.
- **Scripts live in `<scratch>`.** A one-off edit script replayed later undoes newer work, so it's never committed.
  For a layout job, keep one placement script and one routing script, each starting with the removals that undo its
  own output (`remove_outline()`, `remove_texts()` and holes; `remove_tracks(nets=["*"])` and `remove_zones()`).
  Each fix is then an edit to the script and a rerun. Commit these only if the user wants them kept.
- **Changing a finished board that has no layout scripts** (adding a part, rerouting one): one script that places
  only the new or moved parts, calls `auto_labels([those refs])`, starts with `remove_tracks(refs=[those refs])`,
  routes them, and saves. Existing pours refill on save by themselves; touch them only to change them. It can then
  be rerun without touching the rest.
- **Footprint changes:** after changing a part's footprint in the schematic, `remove_footprint()` the old part in
  one process, then `board.py sync` adds the new one with its nets.
- **Plan from numbers.** Take positions from `pads`, not from a picture. Keep tracks at 0°/45°/90°, leaving one
  clearance plus half a track width from other copper.

## After each edit

1. Read the DRC summary `save()` prints. While placing, unconnected items are expected; nothing else is.
2. Look at the change: `view.py pcb board.kicad_pcb --around U2` (`kicad-view`).
3. Run the full check before committing (`kicad-check`): ERC, DRC, and JLC's limits.
4. Update the design notes if they describe placement or routing.

If the user wants to watch edits live in an open editor, KiCad's IPC API (`kicad-python`) can make them instead, but
`board.py` doesn't use it. Save and close in the editor, edit with `board.py`, then reopen.
