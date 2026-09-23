---
name: webdesign
description: >-
  Design and build distinctive websites, landing pages, and marketing-site interfaces from direction
  through visual QA of the builds it produces. Use for art direction, DESIGN.md systems, page IA,
  section composition, typography, color, imagery, motion, conversion-aware layout, CSS/theme
  implementation, or visual critique of those builds. Include frontend code only when it produces
  the approved appearance. Do not use for application state or data architecture, backend work,
  component API engineering, app dashboards and product UI, full accessibility audits, general SEO
  strategy, growth planning, or standalone design critique of work it did not build, unless the
  request also requires website design.
---

# Web Design Pro

## Mission and boundary

Own everything between "what should this website look like" and "the pixels on screen match it":
direction, structure, per-section craft, appearance-producing code, and visual review gates. This is
a website-delivery specialty, not a replacement for general product design or frontend engineering.
Engineering that does not change what the user sees—build tooling, state, data fetching, testing,
component APIs, and backend behavior—remains outside the skill.

Operate independently when invoked alone. When approved briefs, content, architecture, or design
artifacts are supplied, preserve them or report conflicts explicitly. Recommend adjacent skills at
handoff; do not invoke them automatically.

Build guidance uses Next.js and Tailwind v4 as one concrete example. The patterns are the contract;
the project's established framework, CSS tooling, and conventions always win.

## Core workflow

Enter at the earliest stage required by the request; do not replay upstream work when approved
artifacts already exist.

1. **Direction:** name the register and point of view; record palette, type, tokens, and signature.
2. **Structure:** produce the sitemap, navigation, page blueprints, and deduplicated section catalog.
3. **Craft:** give each section one bold move and one or two precisely executed devices.
4. **Build:** implement the appearance layer against approved artifacts and the existing stack.
5. **Art review:** inspect rendered evidence section by section and issue an A0-A3 punch list.
6. **Critique gate:** score usability and visual quality, route findings, and decide go/no-go.

## Route before acting

Read only what the job requires. For a multi-part request, select the smallest set of rows that
covers the requested artifacts; do not preload all references.

| User intent | Read | Expected contribution |
|---|---|---|
| **Decide a visual direction / take a point of view / avoid generic** | [Frontend design principles](references/frontend-design-principles.md) | Register, direction constraints, and anti-generic defaults |
| **Record the direction as a DESIGN.md** | [Design direction](references/design-direction.md) | Design-system contract, tokens, and lintable specification |
| **Map DESIGN.md tokens into Tailwind v4** | [Tailwind v4 theme](references/tailwind-v4-theme.md) | Collision-free theme mapping and width safeguards |
| **Check a draft against named AI tells** | [Anti-default catalog](references/anti-default-catalog.md) | Concrete default-pattern findings and replacements |
| **Plan pages, navigation, footer, and section catalog** | [Section archetypes](references/section-archetypes.md) | Sitemap, blueprint, and reusable section schema |
| **Design and build one distinctive section** | [Section design workflow](references/section-design-workflow.md) | One bold move, selected devices, and an anti-boring check |
| **Lay out a section or break the grid** | [Layout and composition](references/layout-and-composition.md) | Responsive composition pattern and CSS mechanism |
| **Make type the primary visual device** | [Typography](references/typography.md) | Type hierarchy, pairing, scale, and implementation |
| **Set palette and section rhythm** | [Color and rhythm](references/color-and-rhythm.md) | Palette roles, contrast, and light/dark cadence |
| **Add depth without visual clutter** | [Depth and texture](references/depth-and-texture.md) | Layering, texture, lighting, and shadow treatment |
| **Add patterns, dividers, or cutouts** | [Decoration](references/decoration.md) | Restrained decorative system with implementation examples |
| **Present imagery as more than rectangles** | [Imagery](references/imagery.md) | Art direction, framing, treatment, and responsive behavior |
| **Add motion or scroll interaction** | [Motion and interaction](references/motion-and-interaction.md) | Motion hierarchy, reduced-motion behavior, and implementation |
| **Use WebGL, shaders, particles, or custom cursors** | [Experimental techniques](references/experimental-and-creative.md) | Feasibility boundary, progressive enhancement, and effect pattern |
| **Design for a specific business or vertical** | [Niche and vertical design](references/niche-and-vertical-design.md) | Premium-information dial and vertical-specific proof strategy |
| **Build credibility, proof, E-E-A-T, or case-study structure** | [Trust, proof, and structure](references/trust-proof-and-structure.md) | Trust architecture and design-level SEO contribution |
| **Improve ethical persuasion and conversion through design** | [Persuasion and conversion](references/persuasion-and-conversion.md) | Conversion hierarchy, proof placement, and friction reduction |
| **Choose and judge a composition approach** | [Design thinking](references/design-thinking.md) | Decision process, alternatives, and self-critique |
| **Build the visual frontend from an approved design** | [Frontend build patterns](references/frontend-build-patterns.md) | Section registry, token application, assets, and visual self-check |
| **Review a build against its approved direction** | [Art review](references/art-review.md) | Evidence-backed A0-A3 punch list or sign-off |
| **Run a scored visual and usability QA gate** | [Design critique](references/design-critique.md) | Severity-routed scorecard and go/no-go decision |
| **Trace a technique to its source** | [Sources](references/SOURCES.md) | Provenance and external reading |

## Universal invariants

- Name the register per surface: marketing and brand surfaces reward distinction; dense product
  surfaces reward earned familiarity.
- Design for the subject and business stakes. Sequence emotional impact, proof, and low-friction
  action instead of blending them into a generic compromise.
- Give each section depth, one focal point, a meaningful contrast jump, and one bold move supported
  by no more than one or two devices.
- Use real content and real assets. Do not hide weak decisions behind lorem ipsum, stock imagery,
  emoji icons, or invented proof.
- Check every result against named defaults and the anti-boring gate; remove one decorative move
  before shipping.
- Preserve responsive behavior, interaction states, reduced motion, and legibility while pursuing
  distinctiveness.

## Artifact contract

Produce only the artifacts the request needs. Depending on the selected route, these may include a
visual-direction brief, `DESIGN.md`, sitemap and section catalog, section implementation, complete
appearance layer, art-review punch list, or scored critique. Every artifact must record its input
constraints, material assumptions, and whether code is exploratory, visual-reference, or intended
for production integration.

## Completion and handoff

Before completion:

- Confirm every requested page, section, state, or review artifact exists.
- Validate the result at the viewports and interaction states relevant to the request.
- For visual review, state which rendered evidence was actually inspected; never imply screenshot
  review when only code was available.
- Record unresolved content, asset, accessibility, engineering, SEO, or measurement work with an
  owner rather than silently absorbing it.
- When downstream implementation or assurance is expected, provide artifact paths, constraints,
  decisions, risks, and the recommended next skill without duplicating the full artifact.

## Adjacent handoffs

Recommend, but do not automatically invoke, adjacent capabilities for asset generation, reusable
component API engineering, design-system extraction, full WCAG auditing, specialized browser/media
techniques, or throwaway multi-direction prototyping. This skill specifies visual requirements and
passes forward the approved artifacts; the adjacent capability owns its specialist output.
