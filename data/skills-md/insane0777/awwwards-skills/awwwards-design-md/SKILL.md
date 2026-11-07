---
name: awwwards-design-md
description: Create an evidence-backed DESIGN.md for any public website URL. Use when asked to extract a site's design system, colors, typography, spacing, radii, shadows, components, or to generate a design.md compatible with Google's design.md format. Composes the awwwards MCP inspection/capture tools; does not invent brand intent, source token names, or unobserved states.
---

# Awwwards DESIGN.md

Build a **DESIGN.md** plus a machine-readable **design-evidence.json** from a
single public page. The document is a cited subset of what was observed, not an
official brand system or the site's original source tokens.

## Before starting

Require:

- an absolute public `http(s)` URL;
- the awwwards MCP available in the current agent;
- Playwright installed for the browser tools.

Supported inputs:

```text
url:      required, absolute public http(s) URL
outDir:   optional, default current directory
viewport: desktop (default) or mobile
```

One URL and one viewport per run. No crawling, login, authenticated pages,
asset downloads, or automatic motion recording.

If `publicOnly` is unavailable on the installed awwwards-mcp version, **stop**.
Do not replace it with an unguarded capture. The skill requires the guarded
capability added for arbitrary public URLs.

## Workflow

Use full-profile tools. For the v2 surface, use the equivalents in
`v2-routing.md`; do not mix profiles.

1. **Guard check** — call `export_design_tokens` with `publicOnly:true`,
   `selector:"body"`, the requested viewport, and `maxNodes:800`.
   A refusal is final: report `BLOCKED_DESTINATION` or `INVALID_URL`.
2. **Structure** — call `analyze_page_structure` with `publicOnly:true`,
   `maxBands:20`, and the same viewport.
3. **Screenshot** — call `capture_live_site` with `publicOnly:true`,
   `inline:false`, and the same viewport. Inspect the saved image yourself
   before writing visual claims.
4. **Components** — choose up to three representative roots from the observed
   structure. Call `capture_component` with `publicOnly:true`,
   `maxNodes:150`, `maxDepth:12`, and `compact:false`. Do not guess selectors
   that the structure capture did not show.
5. **Write** — fill `DESIGN.md` using the template below and
   `design-evidence.json` using the evidence contract.
6. **Validate** — run the bundled validator. Optionally run Google's linter.
7. **Report** — summarize what was captured, what was omitted, and every
   inconclusive or blocked step.

Do not continue after a failed guard, robots block, navigation failure, or
missing required evidence. Report the failure instead.

## Evidence rules

Classify every material statement:

- **observed** — directly present in a tool response, screenshot, or node.
- **inferred** — a grouping or name derived from observed values.
- **proposed** — a recommendation for the user's project.

Never label inferred/proposed values `observed`. Never claim:

- an official brand system;
- recovered original token names;
- complete responsive, hover, focus, or dark-mode coverage;
- accessibility compliance;
- rights to reuse assets;
- pixel-perfect reconstruction.

Every design value in the document needs a claim in the sidecar with:

```json
{
  "id": "color-1",
  "value": "#111111",
  "classification": "observed",
  "artifactId": "tokens",
  "path": "/tokens/colors/0",
  "property": "color",
  "viewport": "desktop",
  "state": "default",
  "method": "computed-style aggregate",
  "sampleCount": 37,
  "limitations": []
}
```

`path` is a JSON pointer into the captured tool response or a node path in a
component pack. It is not a guaranteed reusable CSS selector.

## DESIGN.md template

Use this exact section order. Keep the YAML front matter valid.

```markdown
---
version: alpha
name: <site title or host>
description: <one sentence: what this page appears to be>
colors: {}
typography: {}
rounded: {}
spacing: {}
components: {}
---

## Overview

<What was observed. One paragraph. Cite sources inline as [S1], [S2].>

## Colors

<Observed palette with counts. Distinguish page background, text, accents.>

## Typography

<Families, weights, sizes, line heights, letter spacing. Do not merge
independently aggregated values into a heading style unless a component
capture proves that tuple.>

## Layout

<Section bands, max widths, spacing rhythm, grid/flex evidence.>

## Elevation & Depth

<Shadows, borders, overlays, z-index evidence. Omit with a reason when absent.>

## Shapes

<Radii, borders, icon/button shapes.>

## Components

<Up to three components. For each: observed selector, node path, size,
typography tuple, colors, spacing, border/radius/shadow, states actually seen.>

## Do's and Don'ts

<Only rules grounded in observed evidence or clearly marked proposals.>

## Sources

- [S1] `export_design_tokens` — `<redacted URL>` — `<capturedAt>` — `<artifactId>`
- [S2] `analyze_page_structure` — ...
- [S3] `capture_live_site` — `<saved file>`
- [S4] `capture_component` — `<selector>` — `<node path>`

## Coverage and limitations

<What was not observed; mobile/dark/hover/state gaps; truncation; blocked
resources; robots/auth restrictions.>

## Unresolved details

<Values the evidence cannot establish. Never fill these with guesses.>
```

Keep `DESIGN.md` at or below **24 KiB** UTF-8.

## design-evidence.json

```json
{
  "schemaVersion": "awwwards-design-evidence-v1",
  "requestedUrlHash": "<sha256 of the requested URL>",
  "redactedFinalUrl": "<origin+pathname>",
  "capturedAt": 0,
  "viewport": "desktop",
  "toolVersion": "<installed awwwards-mcp version>",
  "captures": [
    {
      "id": "tokens",
      "tool": "export_design_tokens",
      "artifactId": "tokens",
      "capturedAt": 0,
      "sha256": "<sha256 of the canonical tool JSON>",
      "artifactPath": "tokens.json",
      "coverage": "<complete|partial|unknown>",
      "limitations": []
    }
  ],
  "claims": [],
  "omissions": [],
  "validation": {
    "documentBytes": 0,
    "sidecarBytes": 0,
    "localValidator": "pass",
    "googleLint": "not-run"
  }
}
```

Every capture record must correspond to a real tool response saved next to the
sidecar (`artifactPath`); its SHA-256 must match that file, and every claim
`path` must resolve in the saved response. Keep the sidecar at or below
**256 KiB**. Never embed screenshots as base64 in Markdown; reference the saved
file path.

## Validation

From the installed skill directory:

```bash
node scripts/validate-design-md.mjs DESIGN.md design-evidence.json
```

The validator needs **Node 22+**, **Python 3**, and **PyYAML**
(`pip install pyyaml`), because it parses the front matter with a real YAML
parser instead of guessing. If Python/PyYAML is unavailable, use Google's
linter below as the YAML check and keep the rest of the manual review.

Optional Google-format validation:

```bash
npx --yes --package="@google/design.md" designmd lint DESIGN.md
```

Lint success proves document structure, not extraction accuracy. Manually check
at least ten emitted values against the tool responses and screenshot.

## Stop conditions

Return a short failure report, not a document, for:

- `INVALID_URL` — not absolute public http(s);
- `BLOCKED_DESTINATION` — private/loopback/metadata/reserved host;
- `ROBOTS_DISALLOWED` or `ROBOTS_UNAVAILABLE` — when the MCP reports it;
- `PAGE_BLOCKED` or `TIMEOUT`;
- missing tokens/structure with no usable screenshot;
- a component capture that cannot identify a real root.

## Do not

- Do not call `create_design_brief` as a substitute: it takes Awwwards slugs
  and synthesizes direction, not arbitrary-URL source evidence.
- Do not add a dedicated `get_design_md` tool or claim one exists.
- Do not crawl multiple pages, download assets, or bypass authentication.
- Do not invent CSS variables, source token names, or states.
- Do not write `DESIGN.md` from memory or from the screenshot alone.
