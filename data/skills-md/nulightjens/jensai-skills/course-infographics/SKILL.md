---
name: course-infographics
description: >
  Generate infographics (still PNG) and motion graphics (looping GIF, 3-8s) for course
  lessons and classroom content on any course platform (Skool, Kajabi, Teachable, Circle,
  or a self-hosted LMS). All graphics use the Editorial layout (two-column asymmetric).
  Stills showcase topics, vocabulary and definitions. Motion graphics visualize concepts
  with smooth schematic animations. Renders via Remotion on a 60-30-10 dark design system
  driven by one configurable accent color.
  Use when asked to "create infographic", "make course graphic", "generate lesson image",
  "course infographic", "motion graphic for lesson", or "visual for course content".
argument-hint: "[path-to-lesson.md or free text] [--type=still|motion] [--theme=dark|light] [--duration=5s] [--accent=#0d8aff]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Course Infographics Generator

Generate publication-ready infographics and short motion graphics for course lessons and
classroom content, on any platform that accepts images and GIFs.

**IMPORTANT**: Read `references/design-tokens.md` for the color system and the accent
parameter. Read `references/layout-modes.md` for the Editorial layout and its variants.
Read `references/content-routing.md` for content-to-variant mapping. Read
`references/motion-specs.md` for animation timing.

Read the `remotion-best-practices` skill, if it is installed, before writing any Remotion
code. If the host project defines a `DESIGN-RULES.md` at its root, read that too for
project-scoped constraints that override the defaults here.

## Prerequisites

1. A Remotion project to host the compositions. Set `REMOTION_PROJECT` to its path:

   ```bash
   export REMOTION_PROJECT=/path/to/your/remotion-project
   ```

   Run `npm install` inside it if dependencies are not yet installed.
2. Source content available (lesson markdown, module directory, or free text).

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| Accent color | `#0d8aff` | The single 10% accent. Set per project via `--accent`, an `ACCENT_COLOR` env var, or a project design config. Every reference to "accent" in this skill resolves to this value. |
| Theme | `dark` | `dark` or `light` |
| Resolution | `1920x1080` | Canvas size for both tiers |

The accent is a parameter, not a fixed value. Swap it for the course's own color and the
whole system follows, since nothing else in the palette is chromatic.

## Two Tiers

| Tier | Format | Duration | Use |
|------|--------|----------|-----|
| **Still** | PNG 1920x1080 | n/a | Vocab, overviews, definitions, checklists, term lists |
| **Motion** | GIF 1920x1080 | 3-8s loop | Concept visualizations, process flows, comparisons |

**One idea per frame.** Split heavy lessons across multiple graphics rather than cramming
everything into one.

## Workflow

### 1. Analyze Content

Read the input content. Determine:
- What is the key concept or takeaway?
- Is this a still (reference/showcase) or motion (concept visualization)?
- Which right-column variant fits? (See `references/content-routing.md`)

### 2. Select Right-Column Variant

All compositions use the Editorial wrapper. The left column is always: label, serif
headline, accent line, body text. The right column varies:

**Still variants:**

| Variant | Right Column | Use Case |
|---------|-------------|----------|
| Term List | Term + definition rows with hairline dividers | Vocabulary, command references |
| Pull Quote + Stat | Italic serif quote top, big stat number bottom | Concept explainers, takeaways |
| Numbered List | Ordered rows with monospace numbers | Module overviews, sequences |
| Checklist | Completion items with check/dash indicators | Module wrap-ups, summaries |
| Terminal Block | Code block with subtle border, monospace text | Install steps, CLI demos |

**Motion variants:**

| Variant | Right Column | Use Case |
|---------|-------------|----------|
| Schematic Flow | Icons + arrows animating a process | Git push, build pipeline |
| Schematic Comparison | Before/after or this-vs-that with transition | Terminal vs editor |

### 3. Build Props

Construct the props object for the selected composition. Each composition has its own props
type in its file.

### 4. Write Composition (if custom)

If none of the existing templates fit, create a new composition in
`src/infographics/compositions/` following existing patterns. Use the shared tokens, fonts,
layout components, and animation primitives.

### 5. Render

```bash
cd "$REMOTION_PROJECT"

# Still image
npx remotion still src/infographics/Root.tsx <CompositionId> \
  --output=out/<name>.png \
  --props='<json>'

# Motion graphic (GIF)
npx remotion render src/infographics/Root.tsx <CompositionId> \
  --output=out/<name>.gif \
  --props='<json>' \
  --image-format=png
```

Pass props as JSON via the `--props` flag, including the accent color when it differs from
the default.

### 6. Verify

Check rendered output against the rules in `references/design-tokens.md` (and the project's
`DESIGN-RULES.md` if one exists):

- Content fills 80%+ width, 70%+ height
- Nothing below 24px font size
- Accent on ONE meaningful element only, never on individual letters
- No content overflow or cut-off at the bottom
- Two-column editorial layout maintained
- For motion: smooth looping, no jarring cuts

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--type` | `still` | Output type: `still` or `motion` |
| `--theme` | `dark` | Color theme: `dark` or `light` |
| `--duration` | `5s` | Animation duration for motion (3-8s) |
| `--resolution` | `1920x1080` | Output resolution |
| `--accent` | `#0d8aff` | Accent color for the 10% band |
