---
name: figcraft-html-import
description: "Import HTML or a web page into Figma using FigCraft's native import_html converter. Use when: html to figma, import html, import webpage, capture static page, convert HTML into editable Figma layers. For pixel-perfect live web capture, use official Figma MCP generate_figma_design as a visual reference when available."
disable-model-invocation: false
---

# HTML Import

Use this skill when the deliverable is editable Figma layers generated from HTML, a local `.html` file, or a simple web URL.

FigCraft's native path converts HTML into a `create_frame` payload so the result stays inside the declarative pipeline: Opinion Engine, design preflight, lint, verification debt, and token/component workflows still apply.

## Skill Boundaries

- Use `import_html` for static HTML, local HTML files, and simple server-rendered pages.
- Local `filePath` imports require `.html`, `.htm`, or `.xhtml`; by default they are limited to the MCP server cwd. Set `FIGCRAFT_HTML_IMPORT_ROOTS` to allow additional roots.
- URL imports are for public `http(s)` pages. Private/loopback URLs such as localhost are blocked by default; set `FIGCRAFT_HTML_IMPORT_ALLOW_PRIVATE_URLS=true` only when intentionally importing a local/private page.
- Use `dryRun:true` first for unfamiliar HTML to inspect the generated `create_frame` payload.
- If the source is a live web app with JavaScript rendering, external CSS, animations, or complex responsive behavior, use the official Figma MCP `generate_figma_design` as a pixel reference when available, then rebuild/refine through FigCraft tools.
- If the task is ordinary from-scratch UI creation without an HTML source, use `figma-create-ui`.
- If the task is mapping code components to Figma components, use `figcraft-code-connect`; Code Connect's `figma.html` is not an HTML import path.

## Workflow

1. Call `get_mode` first. If it fails, stop and ask the user to open Figma -> Plugins -> FigCraft.
2. Load `ui-ux-fundamentals`, plus `design-guardian` when a library is selected or `design-creator` when no library exists.
3. Inspect the source:
   - Inline snippet: pass `html`.
   - Local file: pass absolute `filePath`.
   - Static URL: pass `url`; JavaScript is not executed.
4. For non-trivial HTML, call `import_html({ ..., dryRun:true })` and inspect:
   - root dimensions and name
   - generated `children`
   - unresolved image warnings
   - node count and depth truncation warnings
5. Write with `import_html` only after the payload looks reasonable.
6. Verify the result:
   - `export_image` on the returned root frame
   - `lint_fix_all`
   - `verify_design` if `_qualityScore < 80`, `_qualityWarning` exists, or `_verificationDebt` remains

## Native Converter Contract

`import_html` is conservative by design.

It supports:
- semantic containers: `main`, `section`, `article`, `header`, `footer`, `nav`, `div`, `form`
- text: headings, paragraphs, spans, labels, links, buttons
- controls: `input`, `textarea`, `select`
- media: remote `img` URLs and inline `svg`
- inline CSS basics: color, background color, border, radius, padding, margin, gap, width, height, font size, font weight, line height, text decoration, flex direction

It does not currently support:
- JavaScript execution
- full external CSS cascade
- CSS Grid fidelity
- pseudo-elements
- canvas/video rendering
- local relative images as image bytes
- exact browser layout parity

## Follow-Up Fixes

After import, prefer normal FigCraft edits:

- Use `nodes(method:"update")` for layout, fills, strokes, sizing, and text props.
- Use `text(method:"set_content")` or `text(method:"set_range")` for content changes.
- In library mode, replace hardcoded colors/text styles with `search_design_system` + `variables_ep(method:"batch_bind")` where appropriate.
- For repeated UI pieces discovered in the import, convert stable patterns into components with `create_component_from_node` or rebuild them via `create_component`.

## Examples

Dry-run a local file:

```json
{
  "filePath": "/absolute/path/page.html",
  "name": "Imported / Pricing Page",
  "width": 1440,
  "dryRun": true
}
```

Import an inline snippet:

```json
{
  "html": "<main><h1>Launch faster</h1><p>Design and ship with one system.</p><button>Start</button></main>",
  "name": "Imported / Landing",
  "width": 1200
}
```
