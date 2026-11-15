---
name: kicad-fab-export
description: "Exports Gerbers, drill files and the JLCPCB fab zip from a KiCad 10 board, after a DRC check, and verifies the files. Also exports STEP and DXF files for enclosures. Use when the user asks for Gerbers, a fab zip, files to order a PCB, or a STEP/DXF, or after a board change in a project that keeps its fab zip. For the BOM and CPL files JLC assembly needs, use kicad-assembly-export."
---

# Export a board for JLCPCB

`K` is `kicad-cli`. The `kicad-view` skill gives its path for each OS.

The template `jlc-fab.kicad_jobset`, in this skill's folder, follows JLC's KiCad guide. It produces one zip,
`fab/<project>_gerber.zip`, containing:
- **Gerbers:** copper, mask and silk on both sides, plus Edge.Cuts. They use Protel extensions, no X2, netlist
  attributes, silk clipped at mask openings, and the 4.6 format. Zones are refilled first.
- **Drill files:** Excellon, in mm, absolute origin. PTH and NPTH come out as separate files, and slots are G85.

## Setup, once per project

```bash
cp <skill dir>/jlc-fab.kicad_jobset <project dir>/
```

Then edit the copy:
- **Zip name:** set it in `output_path`, e.g. `${KIPRJMOD}/fab/Name_gerber.zip`. Keep `${KIPRJMOD}`, because a
  relative path resolves against the shell's directory, not the project's.
- **4+ copper layers:** add `In1.Cu`, `In2.Cu`, … to the Gerber job's `layers`, in stack order.
- **Stencil or assembly:** add `F.Paste` and `B.Paste`.
- **Layer names:** use KiCad's canonical names (`F.SilkS`, not `F.Silkscreen`).
- **Other settings:** the key names come from KiCad's `common/jobs/job_export_pcb_*.cpp`. A job's defaults differ from
  `kicad-cli`'s flags, so state every setting explicitly.

Commit the jobset with the project.

## Export

```bash
"$K" pcb drc --severity-error --exit-code-violations --refill-zones --schematic-parity \
     -o <scratch>/drc.rpt board.kicad_pcb \
  && "$K" jobset run --stop-on-error -f jlc-fab.kicad_jobset board.kicad_pro
```

Keep the DRC gate as a separate command. In KiCad 10.0, a failed DRC job inside the jobset still lets the zip be
written.

If DRC reports errors, fix them (`kicad-check`). Export anyway only if the user says so. This gate stops only on
errors, and only for the project's own rules: run `kicad-check` first, whose warnings (dangling tracks, silk over
copper) and JLC passes it doesn't cover.

## Check the output

1. **File list:** run `unzip -l <zip>`. The zip's root should hold:
   - `-F_Cu.gtl`, `-B_Cu.gbl`, `-F_Mask.gts`, `-B_Mask.gbs`, `-F_Silkscreen.gto`, `-B_Silkscreen.gbo`, `-Edge_Cuts.gm1`;
   - `-In<n>_Cu.g<n>` for each inner layer;
   - `-PTH.drl` and `-NPTH.drl`.

   The number of copper files must match the layer count.
2. **Holes:** `grep -h '^T[0-9]*C' <unzipped>/*.drl` lists the drill diameters in mm. Compare the smallest with the
   fab's minimum.
3. **Render the Gerbers themselves, not KiCad's plot.** Export mistakes only show up in the files. This needs
   `uv` (`brew install uv` or astral.sh/uv), which fetches pygerber on the fly:

   ```bash
   mkdir -p <scratch>/gbr/in <scratch>/gbr/out && unzip -q -o <zip> -d <scratch>/gbr/in && cd <scratch>/gbr
   uv run --no-project --with pygerber pygerber render project -d 20 -o out/top.png \
       in/*-F_Cu.gtl in/*-F_Mask.gts in/*-F_Silkscreen.gto in/*-Edge_Cuts.gm1
   uv run --no-project --with pygerber pygerber render raster -t copper -d 20 -o out/B_Cu.png in/*-B_Cu.gbl
   ```

   - `-d` is dots per mm. 20 is enough for a whole board; use 60 or more for detail.
   - Render the bottom and each inner layer too.
   - Look for shorts, slivers, pours cut in two, missing pads, silk on pads or past the edge, and an outline that
     isn't closed.
   - pygerber 2.4 can't read drill files, so use step 2 for holes.
4. **JLC's order page:** it renders the uploaded files and shows the layer order it read. Ask the user to look before
   paying.
5. **Re-export:** if the board hasn't changed, only the dates differ. Confirm by diffing the unzipped files with
   `grep -v -e CreationDate -e 'date '`.

## Mechanical files

```bash
"$K" pcb export step -f -o <scratch>/board.step board.kicad_pcb
"$K" pcb export dxf --mode-single -l Edge.Cuts --output-units mm -o <scratch>/outline.dxf board.kicad_pcb
```

**STEP**
- A part whose footprint names no 3D model is missing from the STEP. `board.py sync` (`kicad-board-edit`) restores
  models that the API dropped.
- Useful options: `--board-only`, `--no-dnp`, `--drill-origin`, and `--user-origin 0x0mm`.

**DXF**
- The output defaults to inches, so always pass `mm`.
- Add `F.Fab` or `F.CrtYd` to include part outlines.

These files go to the user, not into the fab zip.

## Rules

- In a project that commits its fab zip, re-export after every board change and commit the zip with that change.
- Never edit files inside the zip. If a fab needs different settings, change the project's jobset and give the reason
  in the commit.
- For BOM and CPL files, use `kicad-assembly-export`.
