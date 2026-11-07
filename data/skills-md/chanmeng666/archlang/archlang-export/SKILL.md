---
name: archlang-export
description: Use when the user wants an ArchLang .arch floor plan delivered as files, e.g. "export this plan as PDF", "give me a DXF for CAD", "a PNG I can paste into a document", "one sheet per floor", "print it at 1:50 on A3". Covers SVG, PNG, PDF and DXF output, paper size and scale, multi-storey plans and batches, all through the archlang CLI. Not for writing or changing the plan itself.
license: MIT
compatibility: Needs a shell with Node 18+ and the archlang CLI (npx -y @chanmeng666/archlang, or npm i -g @chanmeng666/archlang for a global archlang). PNG and PDF need optional packages that the CLI can install with --install.
---

# Export a plan

Produce drawing files from a `.arch` plan.
If `archlang` is not on the path, write `npx -y @chanmeng666/archlang` in its place.
Never run a bare `arch`: on Linux, macOS and Git Bash that name is the coreutils command.

This skill is a workflow, not a language reference. `archlang compile --help` lists every format and
flag; `archlang spec` describes the `paper` and `scale` statements.

## Steps

1. **Check the plan compiles.** `archlang compile plan.arch --json` writes nothing and reports `ok`
   and the diagnostics. Do not export a plan with errors; fix it first.
2. **Make sure it is a sheet.** A plan with no `paper` statement has no physical size.
   `archlang finish plan.arch --only sheet --dry-run --json` shows the sheet statements the plan lacks
   (paper, scale, dimensions, title block, room schedule, legend). `archlang finish plan.arch --only sheet`
   adds them on the smallest sheet the drawing fits.
3. **If the user names a paper size or a scale,** edit the plan's `paper` and `scale` statements
   to those values and compile again. If the drawing does not fit the sheet the plan declares,
   `archlang finish plan.arch --reissue -o issued.arch` writes a copy in which only `paper` and `scale`
   are replaced by ones that fit. Tell the user when the sheet they asked for cannot hold the
   drawing at that scale.
4. **Export.** Pick the format by what the file is for:
   - SVG, for the web or further editing: `archlang compile plan.arch -o plan.svg --json`
   - PDF, for print at true size: `archlang compile plan.arch -f pdf -o plan.pdf --install --json`
   - PNG, for a document or a chat: `archlang compile plan.arch -f png -o plan.png --install --json`
     (`-s 2` doubles the raster scale)
   - DXF, for CAD: `archlang compile plan.arch -f dxf -o plan.dxf --json`
5. **Multi-storey plans.** A plan written with `level` blocks compiles to one file per storey,
   named `<stem>.L<level>.<ext>`, and the JSON result lists them in `outputs[]`. To write one
   storey to one named file, add `--level <n>`.
6. **Many plans at once.** Create the output directory first; `batch` does not create it. Then
   `archlang batch a.arch b.arch -f pdf -o out/ --json` renders each input into it and returns one
   result row per input.
7. **Confirm what was written.** Read `output` (or `outputs[]` for a multi-storey plan) and
   `bytes` in the JSON result and list the files for the user. For a PNG you can look at it; for the other formats report the
   path, the sheet size and the scale.

## Report to the user

- Each file written, with its format.
- The paper size and scale of the sheet, and whether you or `finish` chose them.
- Any storey or input that failed, with its diagnostic.

## When something goes wrong

- A missing optional package for PNG or PDF: repeat the command with `--install`.
- Exit code `2` is a fault in the plan source, not in the export: read the diagnostic.
  `3` is a wrong flag: run `archlang compile --help`.
- Text or dimensions too small on the sheet: the scale is too small for the paper. Choose a
  larger sheet or a larger scale in the plan, or let `archlang finish plan.arch --reissue` choose.
