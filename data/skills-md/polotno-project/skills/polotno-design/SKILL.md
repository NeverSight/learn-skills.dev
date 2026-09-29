---
name: polotno-design
description: >-
  Create, transform, render, and bulk-produce editable Polotno designs.
  Use for posters, flyers, social posts, ads, invitations, menus, and
  marketing images. Also use for Polotno JSON, PNG or PDF export, print
  output, PDF or PSD import, localization, resizing, brand application,
  and data-driven variants. Select the best available Polotno runtime.
  This can be a live desktop app, a local browser editor, or headless scripts.
---

# Polotno design production

Produce an editable Polotno JSON document and the requested output files.

Talk about the design and its files. Keep runtime details and internal checks
out of the user response unless they affect the result.

## Completion contract

The following conditions define a complete design task:

- The JSON passes schema validation and preflight.
- All required assets are present.
- You viewed a current render.
- The render passes `reference/proof-checks.md`.
- Each requested output file exists.

If you cannot view the render, state that the design has no visual proof.
Do not describe its appearance as verified.

## Select a runtime

Use the first available runtime. Read only its file in `reference/runtimes/`.
An explicit user choice takes priority.

1. **Desktop app through MCP.** If `create_design`, `render_page`, and
   `lint_design` exist, use this runtime. Read `reference/runtimes/local-app.md`.
2. **Desktop app through HTTP.** If its discovery file and health URL are
   available, use this runtime. Read `reference/runtimes/local-app.md`.
3. **Local browser editor.** If `scripts/serve.js` and Node.js exist, use this
   runtime. The user browser must have access to this machine. Read
   `reference/runtimes/local-server.md`.
4. **Studio bridge.** This runtime is reserved and not available.
5. **Headless scripts.** If no live editor exists, use this runtime. Also use
   this runtime for unattended work. Read `reference/runtimes/headless.md`.
6. **No terminal.** Author the JSON and give Studio import instructions.
   State that no visual proof was possible.

## Use one command vocabulary

Use these verbs from `reference/commands.md` for all runtimes:

- Documents: `create_design`, `list_designs`, `get_design_json`,
  `patch_design_json`, and `save`.
- Elements: `add_element`, `update_element`, `remove_element`, `move_element`,
  and `set_page`.
- Output and size: `set_design_size`, `render`, `export`, and `lint`.

The selected runtime file maps each verb to a tool, endpoint, or script.
Do not invent a verb or transport.

## Read only the needed references

- New design: read `reference/archetypes.md` and `reference/design-format.md`.
- Final visual proof: read `reference/proof-checks.md`.
- Resize, localization, brand, or bulk work: read `reference/transformations.md`.
- Print or PDF output: read `reference/print-pdf.md`.
- PDF, PSD, or SVG import: read `reference/import.md`.

## Create a new design

### 1. Define the delivery contract

Record the message, content, output use, canvas size, required brand assets,
and asset restrictions.

If a missing fact can make the output incorrect or unusable, ask immediately.
Do not use a fixed question count.

Select unspecified visual details from the brief. Record these selections in
the final delivery note. If several directions have different tradeoffs, make
small first-page proofs before the full build.

For unattended work, use only supplied values and documented defaults. Report
each important default in the delivery note.

### 2. Plan the composition

Select one layout recipe from `reference/archetypes.md`. Apply the visual quality
bar in that file. Define concrete color, type, spacing, margin, and media tokens.

### 3. Compose the JSON

Write the smallest Polotno JSON that expresses the planned composition. Fill
every layout zone with final content or an asset placeholder.

Run schema validation. The validator reads the source without changing it.
If a consumer needs canonical JSON, use explicit normalization.

### 4. Resolve assets

Search for each placeholder. View each candidate before selection. Automatic
selection is permitted only for unattended work.

### 5. Run preflight

Run `lint` after asset resolution. Fix each error. Review each warning and
record the reason for any warning that remains.

### 6. Make a visual proof

Render the current design and view the pixels. Apply
`reference/proof-checks.md` to the render and JSON.

Repair blocking defects first. After each content or geometry repair, run
preflight again and make a new proof. If no blocking defect remains, stop.

### 7. Package the result

Export the requested files. Report the editable design, exported files,
remaining warnings, and important visual selections.

## Transform an existing design

Read `reference/transformations.md` before a resize, localization, brand update,
content update, or bulk run.

Capture the source JSON and a source render. Declare the allowed changes and
protected properties. Derive each result from the source design.

Run preflight on every result. Compare its proof with the source proof. Report
each deliberate change to a protected property.

## Produce bulk variants

Use a design that already passed the completion contract.

1. Add `custom: { slot: "<name>" }` to each variable element.
2. Map every input field to a slot or exclude it explicitly.
3. Derive each variant from the same source template.
4. Run schema validation and preflight on every variant.
5. View the first row, the longest-text row, and the row with most asset changes.
6. Report failures by a stable row key.

## Scope

This skill produces designs and design outputs. Use the `polotno-sdk` skill for
editor development, React integration, Store APIs, or SDK questions.
