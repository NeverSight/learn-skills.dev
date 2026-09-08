---
name: scientific-illustrator-agent
description: Create editable scientific workflow diagrams in desktop Adobe Illustrator from natural-language ideas or simple reference images, using a bundled Python FigureSpec renderer and Windows COM. Use when the user wants Illustrator vector objects and editable text rather than a raster image.
---

# Scientific Illustrator Agent

This skill bundles the Python engine beside this file. Resolve all relative paths below against this skill directory, not the user's working directory. Windows and locally installed Illustrator are required. Illustrator 2022 was tested; 2020 compatibility is intended but not verified. This is a CLI skill, not an MCP server.

## Prepare

Use an available Windows Python 3.9+ with pywin32, Pydantic and Pillow. If dependencies are missing, create a local virtual environment and install `requirements.txt`; do not replace the user's global Python packages. See `README.md` for installation and COM troubleshooting.

Run `python "<skill-directory>/examples/hello_illustrator.py" --connect-only` to check Illustrator. COM Dispatch can start Illustrator automatically. This does not guarantee the window is foreground. Never terminate Illustrator or repeatedly retry a failed mutation.

## Draw

1. Extract concepts, labels and relationships from the user's idea or reference. Read `docs/input_modes.md`, `src/models/figure_spec.py` and the relevant JSON under `examples/specs/` for the actual supported schema.
2. Write FigureSpec JSON to the user's output directory. For ideas use `mode: create` and horizontal or vertical layout; let the layout engine compute positions. For references use `mode: reconstruct` with normalized positions. Preserve uncertain text as a question or explicit uncertainty rather than inventing scientific content.
3. Keep one conceptual text block in one label, including embedded newlines; do not split words or lines into independent text objects. Use consistent semantic colors, generous whitespace and legible fonts. Prefer short labels and simple arrow topology.
4. Validate: `python "<skill-directory>/examples/render_spec.py" "<spec.json>" --validate-only`.
5. Render: `python "<skill-directory>/examples/render_spec.py" "<spec.json>" --output "<new-output.ai>"`. The renderer creates a new document and refuses existing output files. Preserve other open documents.
6. Inspect the exported PNG, report warnings and confirm editable object/text counts from the renderer. Revise the specification into a fresh output if needed. Deliver the AI and PNG paths.

## Scope and limitations

The CLI supports basic nodes, text and arrows, AI saving and PNG export. It does not call a language or vision model itself: the agent interprets the request and creates the spec. Do not claim pixel-exact reconstruction or original numerical data from a screenshot. Complex branched routing, full visual QC, PDF/SVG export and MCP are not implemented in this CLI.

## Optional progressive construction

Use `examples/progressive_svg.py` for an existing vector SVG, including detailed vector artwork. This is an additional SVG entry point, not automatic bitmap tracing. It starts Illustrator through COM, opens a temporary SVG source, then copies actual graphical groups into a fresh destination document in order. It closes only the temporary source. No selection-dependent operation or raster reveal is used.

Always produce `progressive.ai` and `final.png`. Choose the mode from the user's intent:

- "一步生成", "直接出图": `--mode instant`; no intentional pauses or GIF.
- "逐步生成", "演示过程": `--mode progressive --duration 30 --batch-size 8 --start-delay 10 --live-only` for a roughly 30-second live construction.
- If a replay GIF is requested, omit `--live-only`; output includes `build.gif` and actual exported PNG frames.
- For an explicit per-group speed instead of a target duration, use `--delay-ms 80` or `--speed 快速|正常|慢速`. Never combine `--duration` with `--delay-ms`.

Example (paths are relative to the skill directory unless made absolute):

```powershell
python examples/progressive_svg.py --source-svg examples/specs/progressive_demo.svg --output-dir outputs/demo_new --duration 30 --batch-size 1 --start-delay 10
```

Use absolute paths when invoking from another directory. Select a fresh output directory every time. An element for this command means a top-level SVG graphical group, potentially containing many paths; retain compound paths to preserve holes. A 30-second target excludes source import, final saving and GIF encoding. If copying/redrawing/exporting takes longer, remaining waits are skipped; report the actual construction duration from `process.json`. GIF speed is independent (`--frame-ms`).

The importer accepts a restricted vector/text SVG subset. It rejects images, external resources, scripts, filters and CSS. See `docs/progressive_svg.md` for parameters and requirements. Other SVG features may require a separate conversion step. Private research examples are not part of this skill.
