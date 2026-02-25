---
name: typst
description: Syntax guide and ecosystem reference for writing Typst (.typ) files. Use this skill when writing, editing, or debugging Typst documents. Covers core syntax, common errors, packages, and best practices.
license: MIT
---

# Typst Skill

**Current version**: Typst 0.14.2 (Dec 2025)

## Smart Defaults

If you know nothing else, follow these rules:

1. **Always** import `@local/qk:1.0.0` — `#import "@local/qk:1.0.0": *`
2. **Always** use `qk-doc` or `qk-report` preset (unless user specifies custom)
3. **Always** use touying for presentations (not raw page dimensions) — see `references/touying-guide.md`
4. **Always** `#set figure(placement: auto)` — prevents blank half-pages
5. **Always** add `alt:` to images — `image("path.png", alt: "description")`
6. **Always** escape `$` in content — scan for bare `$` before compiling
7. **Default fonts**: Libertinus Serif (body), Inter (headings), New Computer Modern Math (math), Fira Code (code)
8. **Default compile**: `typst compile --root .. Source/<file>.typ`
9. **When in doubt** about template: Study Guide
10. **When in doubt** about visual tool: Typst native first → cetz-plot → matplotlib
11. **Always** scan project for existing `.typ` files and match their style (fonts, colors, qk preset) unless user specifies otherwise

## New Document Decision Tree

```
User request → scan for keywords:
  "resume/CV/job"           → CV / Résumé template
  "slides/presentation"     → Presentation (touying — metropolis default)
  "lecture/class/academic"   → Academic Lecture (touying — university theme)
  "essay/thesis/paper"      → Essay
  "report/brief/client"     → Business Report
  "research/analysis"       → Research Report
  "study guide/revision"    → Study Guide
  "reference/glossary"                      → Annotated Reference
  "cheatsheet/reference card/formula sheet" → Cheatsheet template
  "exam/problem set/homework"              → Exam template
  "flashcard/Q&A/quiz"                     → Flashcard template
  ambiguous?                → ask purpose + audience → pick template
```

**Steps:**
1. Auto-detect template from keywords above
2. Import `@local/qk:1.0.0` at top
3. Use `qk-doc` or `qk-report` preset when applicable
4. Auto-select template. State choice in Phase 3 summary. User can re-invoke with explicit type override if wrong.
5. Build from `references/templates.md`
6. Custom styles are fine — templates are starting points, not constraints

## Visual Tool Routing (compact)

| Need | Tool |
|------|------|
| Tables, boxes, grids | Typst native |
| Flowcharts, trees, ER, state diagrams | `fletcher` |
| Sequence diagrams | `chronos` |
| Gantt charts | `timeliney` |
| Simple charts (< 3 series) | cetz-plot |
| Complex charts (4+ series) | matplotlib |
| Mind maps | `/mindmap` (auto-invoke) |
| Conceptual illustrations | `/nano-banana` (auto-invoke) |
| Real photos, logos | `/image-search` (auto-invoke) |

Detail and examples in `references/tool-routing.md`.

## Proactive Behaviors

### Visual Auto-detection

When writing Typst documents, automatically identify content that benefits from visuals. Do NOT wait for the user to request them. Follow priority: Typst native → cetz-plot → `/image-search` → `/mindmap` → native packages → matplotlib → `/nano-banana`.

| Content pattern | Visual to add | Tool |
|-----------------|---------------|------|
| Comparison grids, attribute tables | Styled table | Typst native |
| Callout boxes, styled layouts | `rect()` / `block()` | Typst native |
| Sequential steps, decision logic | Flowchart / decision tree | `fletcher` |
| Process with inputs/outputs | Workflow diagram | `fletcher` |
| System architecture, ER diagrams | Block / entity diagram | `fletcher` |
| Hierarchy or taxonomy | Tree diagram | `fletcher` or `/mindmap` |
| Topic overview, concept map | Mind map | `/mindmap` |
| Request-response, API flows | Sequence diagram | `chronos` |
| Project schedule, phases | Gantt chart | `timeliney` |
| Historical events, evolution | Timeline | `herodot` or `timeliney` |
| Data trends, distributions (< 3 series) | Line/area/scatter chart | cetz-plot |
| Complex charts (4+ series, annotations) | Publication chart | matplotlib/Python |
| Company logo, brand mark | Logo image | `/image-search --logo` |
| Real-world photograph | Photo | `/image-search` |
| Concept with analogy, metaphor | AI illustration | `/nano-banana` |

See `references/tool-routing.md` for full examples, fallback chains, and auto-invoke rules.

### Content Structure

- Suggest TOC (`#outline()`) at 4+ sections
- Suggest file split at 40+ pages — see `references/common-patterns.md` "Large Documents"
- Convert prose lists to tables when 3+ items with attributes

### Component Library Auto-use

When writing content, automatically convert matching patterns to `@local/qk:1.0.0` components:

| Content pattern | Use instead |
|-----------------|-------------|
| Warning paragraph | `warning[...]` |
| Key point / takeaway | `keypoint[...]` |
| Tip or best practice | `tip[...]` |
| Common mistake / trap | `trap[...]` |
| Step-by-step procedure | `step-box("Title", [...])` |
| KPI or metric highlight | `stat-card("value", "label")` |

### Cross-referencing

Add `<label>` + `@ref` for recurring concepts across sections.

### Accessibility (Typst 0.14+)

- `alt:` on all figures — `image("path.png", alt: "description")`
- Semantic heading hierarchy — don't skip levels
- `table.header()` for repeating headers — improves PDF/UA accessibility

## Fallback Chains

| If this fails... | Try... |
|------------------|--------|
| `/nano-banana` | Placeholder rect with description text |
| `/image-search` | `/nano-banana` with descriptive prompt |
| `/mindmap` | `fletcher` tree diagram |
| matplotlib | Check `.venv` → `uv venv .venv.nosync && ln -s .venv.nosync .venv` |
| `typst compile` | Isolate with `/* ... */`, compile incrementally |

## Reference File Index

| When you need... | Read... |
|------------------|---------|
| Syntax, errors, special chars | `references/quick-ref.md` |
| `@local/qk:1.0.0` API | `references/component-library.md` |
| Visual tool details, examples, fallbacks | `references/tool-routing.md` |
| Document preambles | `references/templates.md` |
| Table patterns, show rules, large docs | `references/common-patterns.md` |
| Page layout, spacing, figures, curves | `references/layout-patterns.md` |
| Math mode traps | `references/math-pitfalls.md` |
| Package imports | `references/packages.md` |
| Touying presentations (themes, slides, speaker notes) | `references/touying-guide.md` |
| Visual verification (PNG rendering, spot-checks) | `references/visual-verification.md` |
| Quality gates, rubrics, dispatch table | `references/quality-gates.md` |
| Data-driven generation (JSON, CSV, batch, variants) | `references/data-driven.md` |
| `sym.*` symbols | `references/symbols.md` |

## Version Notes (0.13–0.14)

| Feature | Ver | Description |
|---------|-----|-------------|
| Tagged PDFs, PDF/UA-1 | 0.14 | Accessible PDFs by default |
| `figure.alt` / `image(alt:)` | 0.14 | Alt text for screen readers |
| `pdf.attach` | 0.14 | Attach files (replaces `pdf.embed`) |
| PDF as image format | 0.14 | `image("file.pdf")` |
| Multiple table headers | 0.14 | Hierarchical headers repeat across pages |
| `curve` function | 0.13 | Bezier drawing (replaces `path`) |

**Deprecated**: `path` → `curve` · `pdf.embed` → `pdf.attach` · `image.decode` → pass bytes directly · polylux:0.3.1 → `polylux:0.4.0` or `touying`

| touying 0.6.1 | 0.6 | Presentation framework — `#show: theme.with(...)` API (NOT the old `register()` pattern) |

## CLI Commands

```bash
typst compile document.typ                     # Compile to PDF
typst compile document.typ --root ..           # Set project root
typst compile document.typ out.pdf --pages 1-5 # Specific pages
typst watch document.typ                       # Watch and recompile
typst fonts                                    # List available fonts
typst query doc.typ "heading.where(level: 1)"  # Query document structure
```

**`--root` flag:** When a `.typ` file uses `#import` or `#image()` with paths outside its directory, set `--root` to the project root.

**Batch compile:** `for f in *.typ; do typst compile "$f"; done`

## Conventions

- Source files in `Source/`, compiled PDFs in `PDFs/`
- Compile with `--root ..` when `.typ` references parent directory assets
- For multi-file projects: `main.typ` + `#include` sections + shared `lib.typ`
- File naming: lowercase-kebab-case (e.g., `portfolio-theory-guide.typ`)

## Fonts

| Font | Style | Notes |
|------|-------|-------|
| New Computer Modern | Academic serif | Default; bundled with Typst |
| Georgia | Readable serif | Safe on macOS |
| Helvetica Neue | Clean sans-serif | macOS only |

**Variable font warning:** Apple system fonts (New York, SF Pro) are variable → "variable fonts are not currently supported." Install static `.otf`/`.ttf` versions or use alternatives.

**CJK fallback:** `#set text(font: ("New Computer Modern", "Songti SC"))`

## Documentation

- [Official Reference](https://typst.app/docs/reference/)
- [Package Registry](https://typst.app/universe/)
- [Tutorial](https://typst.app/docs/tutorial/)
- [Changelog](https://typst.app/docs/changelog/)
