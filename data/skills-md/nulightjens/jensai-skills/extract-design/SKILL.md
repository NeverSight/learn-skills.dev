---
name: extract-design
description: Reverse-engineer a DESIGN.md file (per the google-labs-code/design.md spec) from an existing source — HTML page, screenshot, live URL, or design exports. Produces YAML token frontmatter (colors, typography, rounded, spacing, components) plus prose sections (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts) so the visual identity becomes portable across coding agents. Use when the user says "extract design," "make a DESIGN.md from this page," "/extract-design," "turn this into design.md," "reverse engineer the design system from this site/HTML/screenshot," or asks to capture an existing visual identity in a structured, AI-readable format.
---

# extract-design

Turn an existing visual identity into a `DESIGN.md` file that conforms to the [google-labs-code/design.md](https://github.com/google-labs-code/design.md) spec — YAML token frontmatter plus markdown rationale.

## When to use

User asks to:
- Extract a design system from one or more HTML files
- Turn a live URL or screenshot into a DESIGN.md
- Reverse-engineer tokens from a Figma export, Webflow export, or static site
- Generate `DESIGN.md` so other agents can rebuild the same visual identity

## What you produce

For each source the user provides, output **one** `DESIGN.md` file. If the user gives multiple sources representing distinct designs, produce one DESIGN.md per source and name them descriptively (`DESIGN-<source-slug>.md`). Default output location: same directory as the source, unless the user specifies otherwise.

Each DESIGN.md must contain:

1. **YAML frontmatter** — `name`, optional `description`, then `colors`, `typography`, `rounded`, `spacing`, `components` (in that order). All values must follow the spec types (Color = `#hex`, Dimension = `<num>px|em|rem`, Typography = object).
2. **Markdown body** — `## Overview`, `## Colors`, `## Typography`, `## Layout`, `## Elevation & Depth`, `## Shapes`, `## Components`, `## Do's and Don'ts`, in that order. Skip a section only if the source provides no signal for it.

Read [references/spec.md](references/spec.md) for the full normative spec. Read [references/example-atmospheric-glass.md](references/example-atmospheric-glass.md), [references/example-paws-and-paths.md](references/example-paws-and-paths.md), or [references/example-totality-festival.md](references/example-totality-festival.md) when you need a calibration example for the prose voice.

## Workflow

### 1. Identify the source(s)

Sources may be:
- Local HTML file(s) — most common
- Local CSS file(s)
- Live URL — fetch with WebFetch or Playwright MCP
- Screenshot — Read the image, then describe tokens visually
- Multiple files representing one design — merge before extracting
- Multiple files representing different designs — extract separately

### 2. Run the primitive extractor (HTML/CSS sources only)

Use [scripts/extract_primitives.py](scripts/extract_primitives.py) to harvest raw values from the source. The script returns a JSON object with frequency-ranked candidates for colors, font-families, font-sizes, font-weights, border-radii, spacing values, and shadows.

```bash
python3 scripts/extract_primitives.py <path-to-html-or-css> [more-paths...]
```

Run this from the skill's own directory, or prefix the script with the install path (for example `<path-to-skill>/scripts/extract_primitives.py`).

The script is the data-gathering step, not the answer. Its output is a denormalized inventory; you must normalize it into a token system. **Do not paste the raw output into the DESIGN.md.**

For non-HTML sources (screenshots, live URLs you cannot scrape), skip the script and observe directly.

### 3. Normalize into a token system

Apply the heuristics in [references/extraction-heuristics.md](references/extraction-heuristics.md) to convert the raw inventory into a coherent token system:

- Pick a `name` that captures the brand personality (e.g., "Atmospheric Glass," "Heritage," "Boston Newsroom").
- Reduce the color inventory to a small palette (`primary`, `secondary`, `tertiary`, `neutral`, plus surface/on-surface roles). Do not export every observed color — pick the ones that carry semantic weight, then express variants as references.
- Build a typography scale of 6–12 levels using the most-used font families and sizes. Name them semantically (`display-lg`, `headline-lg`, `body-md`, `label-sm`).
- Build a spacing scale (4 / 8 / 16 / 24 / 32 / 64 are common bases). Quantize raw values to the nearest scale step.
- Build a `rounded` scale from the observed border-radii (typically `none`, `sm`, `md`, `lg`, `full`).
- Pick 4–10 components that anchor the system: `button-primary`, `button-secondary`, `button-ghost`, `card`, `input-field`, plus any obvious patterns (testimonial-card, hero-cta, pricing-card, etc.). Each component must reference tokens (`{colors.primary}`), not literal values where a token exists.

### 4. Write prose sections

Voice: confident, specific, present tense. Match the cadence in the calibration examples — short paragraphs, descriptive color names ("Boston Clay," "Limestone"), explicit *why* behind every choice.

- **Overview** — 2–4 sentences naming the personality, target feel, and emotional register.
- **Colors** — bullet each named color with hex + role + usage rule.
- **Typography** — explain font choice rationale, then describe each tier.
- **Layout** — grid model, base unit, container behavior.
- **Elevation & Depth** — how depth is conveyed (shadows, borders, blur, tonal layers).
- **Shapes** — corner radius philosophy + how it varies by component type.
- **Components** — describe the patterns referenced by component tokens.
- **Do's and Don'ts** — 4–8 actionable rules. These are guardrails, not platitudes.

### 5. Validate

After writing, audit the file against the spec:

- Section order matches: Overview → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts
- Every token reference (`{colors.foo}`) resolves to a defined token
- All component `backgroundColor`/`textColor` pairs hit WCAG AA (4.5:1) — flag any that do not
- Every color token is referenced by at least one component or is a documented role color
- `name` field is set; it is the first signal an agent reads

If the user has `npx` available, validate with the official linter:

```bash
npx @google/design.md lint <output-path>
```

This is optional — your manual audit catches most issues. Only suggest the linter if the user asks for verification or the file is going into production.

## Key principles

- **Extract, don't invent.** Every token must trace back to evidence in the source. If the source lacks a `tertiary` color, do not invent one.
- **Tokens over literals.** Inside `components`, prefer `{colors.primary}` over `#1A1C1E`. Literal values in components are a smell.
- **Compress, don't enumerate.** A page with 47 distinct grays still needs only 5–7 surface tokens. Pick the load-bearing ones.
- **Name like a designer.** `boston-clay` beats `red-1`. The prose should make the names feel inevitable.
- **Prose explains *why*.** Token values are the *what*; sections like Overview and Do's and Don'ts justify them.
- **One DESIGN.md per visual identity.** If sources differ, produce separate files. Do not merge incompatible systems.

## Output format

Write the file to disk. Confirm the path back to the user with one sentence on what was extracted. Do not paste the full DESIGN.md back unless the user asked to see it inline.
