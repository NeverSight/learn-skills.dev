---
name: design
description: Claude-grade visual design outside Claude Code — distinctive web/UI design direction, poster and canvas art philosophy, and a 10-theme styling library, portable to any agent that reads SKILL.md. Use when building or restyling a UI, landing page, poster, slide deck, static art piece, or any artifact that must not look AI-generated.
when_to_use: Any visual output task — new UI, redesign, poster, deck, report, landing page — where the result should read as deliberately designed rather than templated. NOT for backend code, copywriting alone, or image generation via diffusion models.
version: 1.0.0
license: Apache-2.0 (derived from anthropics/skills; see LICENSE.txt)
metadata:
  agentskills:
    tags: [design, frontend, ui, typography, art, themes]
---

# Design

Distinctive visual design guidance distilled from Anthropic's design skills
(frontend-design, canvas-design, theme-factory), consolidated so any agent — not
just Claude Code — can produce work with a deliberate point of view. The
references below carry Anthropic's original guidance verbatim; they are the
skill, not background reading.

## Route by output type (MANDATORY: read the matched reference before designing)

| Task | Read |
|---|---|
| Web UI, landing page, app screen, component redesign | [references/web-interfaces.md](references/web-interfaces.md) |
| Poster, album art, static PNG/PDF art piece, visual identity | [references/canvas-art.md](references/canvas-art.md) |
| Styling an existing artifact (slides, docs, reports) with a coherent theme | [references/themes.md](references/themes.md) |

Generative/algorithmic art (p5.js, flow fields, particles) is its own skill:
`skills/algorithmic-art`.

## Core discipline (orientation only — never a substitute for the reference)

1. **Ground in the subject.** Pin down what the thing is, who it's for, and its
   single job before designing. Distinctive choices come from the subject's own
   world — its materials, instruments, vernacular — not from a style library.
2. **Avoid the AI-default looks.** Current AI design clusters around: cream
   background + high-contrast serif + terracotta accent; near-black + one acid
   accent; broadsheet hairlines + zero border-radius. Also: purple gradients,
   uniform rounded corners, excessive centering, Inter-for-everything. These are
   defaults, not choices — spend freedom elsewhere unless the brief asks for one.
3. **One signature element.** Spend boldness in a single memorable place; keep
   everything around it quiet. Cut decoration that does not serve the brief.
4. **Typography carries personality.** Pair display and body faces deliberately
   with a clear scale. Need font files? `scripts/fetch_fonts.py` downloads a
   curated OFL set (display/body/mono) on demand — run with no args to list.
5. **Plan, critique, then build.** Draft a compact token system (4-6 named hex
   colors, 2+ type roles, layout concept, signature element). Review it against
   the brief: any part you'd produce for *any* similar prompt gets revised.
   Only then write code, deriving every decision from the plan.
6. **Quality floor, unannounced.** Responsive to mobile, visible keyboard focus,
   reduced-motion respected, nothing overlapping or clipped.

## Verify like a designer

Render the real artifact and look at it — screenshot web pages (the
`webapp-testing` skill automates this), open generated PDFs/PNGs. Fix what you
see, re-render. A static code read is not observation. Before shipping, remove
one accessory (Chanel's rule): the last pass deletes, it does not add.
