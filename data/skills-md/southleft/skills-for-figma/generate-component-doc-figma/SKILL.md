---
name: generate-component-doc-figma
description: "Generate complete Markdown documentation for a Figma component — anatomy/layer tree, design tokens (colors, spacing, typography), states/variants matrix, accessibility notes, content guidelines, and optional code-parity + YAML frontmatter. Use when the user wants a docs page or handoff spec for a component or component set. Triggers: 'document this component', 'generate component docs/spec', 'create a docs page for the Button', 'write up the anatomy and variants', 'component handoff doc from Figma', 'turn this component into Markdown docs'. Reads the node tree, bound variables/tokens, and designer annotations, then the agent assembles Markdown. Requires the Figma Desktop app (Plugin API)."
disable-model-invocation: false
---

# generate-component-doc-figma — Figma component → Markdown docs

Produce a complete documentation page for one component or component set: overview, anatomy tree,
design tokens, variants/states matrix, typography, accessibility, content guidelines, and (optionally)
design-code parity and YAML frontmatter. This skill **collects** structured data from the file via
`use_figma`, then a **deterministic Node converter** (`scripts/generate-doc.mjs`) emits the Markdown —
the same collected JSON always produces identical Markdown. Do **not** freehand the doc from prose.

## Skill boundaries
- **`use_figma` rules** — load the official **`figma-use`** skill first; it is the full Figma Plugin API reference. Essentials these scripts rely on: plain JS with top-level `await` + `return` (no IIFE, no `figma.closePlugin()`; `console.log` is not returned), inputs inlined as `const` at the top of each script, colors in 0–1 range, load fonts before any text op, `await figma.getNodeByIdAsync(...)`, and **atomic errors** (a failed script applies nothing — read the error, fix, retry).
- **The collect script runs anywhere** (`use_figma`); **the converter is Node and runs in a terminal** (`node scripts/generate-doc.mjs ...`). Same split as `export-tokens-figma`. If you can't run Node, you can't produce the doc — say so rather than freehanding it.
- **Markdown section layout + the `cleanVariantName` rule** → [references/doc-template.md](references/doc-template.md). The converter already implements every rule in that file; treat it as the spec, not a checklist for hand-assembly.
- **Reading/writing annotations as standalone specs** → use the `annotations-figma` skill.
- **Exporting the whole token system** (not just one component's tokens) → use `export-tokens-figma`.

## Workflow

1. **Identify the target.** Get the component or component-set node ID from the current selection or a
   URL/ID the user provides. Component **sets** (with variants) produce the richest docs. Set `NODE_ID`
   in the collect script. Also note the file URL (for the `figma:` link / frontmatter).
2. **Collect data → save JSON.** Run [`scripts/collect-component-data.js`](scripts/collect-component-data.js)
   via `use_figma` (`skillNames: "generate-component-doc-figma"`). It returns the anatomy tree, per-variant
   colors (with bound token id + name), typography (font family, numeric weight + name, size, line height,
   letter spacing), spacing tokens, component property definitions (variants/booleans/text props), the
   description, and annotations (with category names). **Save the returned JSON to a file** (e.g.
   `collected.json`).
3. **Generate the Markdown (deterministic).** Run the Node converter in a terminal:
   ```bash
   node scripts/generate-doc.mjs collected.json [--code-info codeInfo.json] [--out docs/components/Button.md] [--frontmatter] [--file-url <figma-url>]
   ```
   It ports the source generator's section logic exactly: Overview (+ When to / When NOT to Use parsed
   from the description), Component Anatomy, Variants (matrix + icon mapping + configurable props),
   Token Specification (color + spacing tables), Typography, Content Guidelines, Accessibility, Design
   Annotations, and — with `--code-info` — Implementation, Design-Code Parity, and Changelog.
   `cleanVariantName` is applied automatically (`Type=Image, Size=12` → `Image / 12`). Same input →
   identical output.
4. **Optional code parity.** To add Implementation / Parity / `[View Source]` & `[Storybook]` links,
   read the component source and write a `codeInfo.json` (props, importStatement, sourceFiles,
   baseComponent, changelog, …), then pass `--code-info codeInfo.json`.
5. **Optional frontmatter.** Pass `--frontmatter` to prepend YAML frontmatter (title, status, version,
   tags, figma URL, lastUpdated).
6. **Review & deliver.** Read the emitted Markdown, sanity-check it, then write/return it. Report the
   path and a one-line summary (variant count, token count).

## Notes
- **Font loading:** if you add a step that writes text into Figma (e.g. stamping the doc back onto the
  canvas), `await figma.loadFontAsync(...)` first. Pure documentation generation reads only.
- The collect script uses `MAX_DEPTH` to keep payloads small for deep trees — raise it only if the
  anatomy looks truncated.
- Token names come from `boundVariables`; a color/spacing with no bound variable renders as `—` in the
  token tables (a hardcoded value to replace with a token).
- The converter is dependency-free (Node 18+, ESM). It exits non-zero with a clear message if the JSON
  is missing or malformed.
- These collect tools require the **Figma Desktop** app (the Plugin API isn't available in the browser).
