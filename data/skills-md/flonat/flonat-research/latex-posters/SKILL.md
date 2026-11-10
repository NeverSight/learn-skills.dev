---
name: latex-posters
description: "Create a large-format academic poster in LaTeX using beamerposter, tikzposter, or baposter. Use when the requested deliverable is a conference or research poster rather than sequential presentation slides. For slide decks, use $beamer-deck."
allowed-tools: [Read, Write, Edit, Bash]
skill-dependencies: [latex]
---

# LaTeX Research Posters

## Overview

Research posters are a critical medium for scientific communication at conferences, symposia, and academic events. This skill provides comprehensive guidance for creating professional, visually appealing research posters using LaTeX packages.

## When to Use This Skill

- Creating research posters for conferences, symposia, or poster sessions
- Designing academic posters for university events or thesis defenses
- Converting scientific papers into poster format
- Creating template posters for research groups or departments

## Compilation Convention

**Always use `latex` to compile posters.** Its pre-flight installs or verifies the fail-closed canonical `.latexmkrc` beside the poster driver. Build artifacts go to `out/`, and the requested PDF is copied back only after a successful build. Never hand-write a poster-specific rc file.

---

## Core Capabilities

### 1. LaTeX Poster Packages

Three major packages, each with distinct advantages:

- **beamerposter** — Extension of Beamer. Familiar syntax, excellent themes. Best for traditional academic posters and institutional branding.
- **tikzposter** — Modern, flexible with TikZ integration. Built-in color themes. Best for colorful, modern designs.
- **baposter** — Box-based layout with automatic spacing. Best for multi-column layouts.

Package guides: [`references/poster_packages_beamerposter.md`](references/poster_packages_beamerposter.md) (beamerposter & tikzposter) | [`references/poster_packages_baposter.md`](references/poster_packages_baposter.md) (baposter & selection guide)

### 2. Poster Layout and Structure

Common sections: Header/Title, Introduction, Methods, Results, Conclusions, References, Acknowledgments. Layout strategies include column-based grids, block-based arrangements, Z-pattern flow, and visual hierarchy.

Layout guides: [`references/poster_layout_grids.md`](references/poster_layout_grids.md) (column grid systems) | [`references/poster_layout_flow.md`](references/poster_layout_flow.md) (Z/F/Gutenberg patterns) | [`references/poster_layout_spatial.md`](references/poster_layout_spatial.md) (header, content, footer) | [`references/poster_layout_blocks.md`](references/poster_layout_blocks.md) (blocks, patterns & testing)

### 3. Design Principles

- **Typography:** Title 72-120pt, headers 48-72pt, body 24-36pt minimum. Sans-serif fonts (Helvetica, Arial).
- **Color:** High-contrast, color-blind friendly palettes. Institutional colors for branding.
- **Content:** 300-800 words total. Bullet points over paragraphs. 40-50% visual content.

Design guides: [`references/poster_design_typography.md`](references/poster_design_typography.md) (typography & color) | [`references/poster_design_accessibility.md`](references/poster_design_accessibility.md) (accessibility & layout)

### 4. Standard Poster Sizes

| Standard | Size | Notes |
|----------|------|-------|
| A0 | 841 x 1189 mm | Most common European |
| A1 | 594 x 841 mm | Smaller format |
| 36 x 48" | 914 x 1219 mm | Common US conference |
| 48 x 72" | 1219 x 1829 mm | Extra large |

### 5. Templates

Ready-to-use templates in `assets/` directory for beamerposter (classic, modern, colorful), tikzposter (default, rays, wave), and baposter (portrait, landscape, minimal).

### 6. Content Patterns and Presentation Tips

Effective content organization for experimental, computational, and review/survey posters. Physical presentation tips and digital backup strategies.

Content guides: [`references/poster_content_sections.md`](references/poster_content_sections.md) (principles & sections) | [`references/poster_content_writing.md`](references/poster_content_writing.md) (writing style & quality)

## Workflow

1. **Planning** — Determine size, orientation, core messages, key figures (3-6)
2. **Package selection** — beamerposter (familiar), tikzposter (modern), baposter (structured)
3. **Layout** — Column structure, content flow, space allocation (title 10-15%, content 70-80%, footer 5-10%)
4. **Integration** — High-res figures (300 DPI), consistent styling, QR codes for supplementary materials
5. **Review** — Check page size (`pdfinfo`), font embedding (`pdffonts`), reduced-scale print test
6. **Delivery** — Compile with `latex`, verify output, prepare print and digital versions

## TikZ Diagrams

If the poster contains TikZ diagrams (common with tikzposter), run the 6-pass verification from [`../shared/tikz-rules.md`](../shared/tikz-rules.md) — compute Bezier depths, check gaps, verify label fit, check shape boundary clearance.

## Common Pitfalls

- Too much text (>1000 words) or font sizes too small (<24pt body)
- Low-contrast colors or red-green combinations (color blindness)
- Wrong poster dimensions for conference requirements
- Images below 300 DPI at final print size
- Fonts not embedded in PDF

## Package Installation

```bash
tlmgr install beamerposter tikzposter baposter qrcode graphics xcolor tcolorbox subcaption
```

## Cross-References

| Skill | When to use alongside |
|-------|----------------------|
| `latex` | **Default compiler** — used in Workflow step 6 for compilation and error resolution |
| `latex` | For manual compilation config and `.latexmkrc` setup |
| `proofread` | Content quality check on poster text |
| `bib-validate` | Cross-reference citation keys if the poster includes a bibliography |

**Shared resources:**
- [`../shared/palettes.md`](../shared/palettes.md) — colour palette inspiration
- [`../shared/tikz-rules.md`](../shared/tikz-rules.md) — TikZ anti-collision rules (if poster uses TikZ diagrams)
