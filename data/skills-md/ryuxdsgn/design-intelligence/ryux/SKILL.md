---
name: ryux
description: "RYUX - design intelligence for AI agents and designers. Tell it what you are doing and it routes to Analyze (understand an existing interface), Design (create or improve UI and UX in Figma, pen.dev, or mockups), Build (implement in code), Critique (find what to change first, with evidence), or QA (verify a build against the design), reads only the knowledge the task needs (product, UX, UI, interaction, forms, content, accessibility, responsive, design system, frontend, anti-slop), and closes with quality gates. Use for any UI, UX, copy, frontend, design review, or design analysis task."
---

# RYUX

> Design intelligence for AI agents and designers. RYUX 2.6.0, MIT licensed.

RYUX is a design intelligence layer for AI and designers. It helps understand, reason, design,
build, critique, and verify interfaces using design knowledge and evidence. It is not a UI
generator, an anti-slop framework, a design system, or a prompt library.

**Understand before you design. Don't design from imagination when evidence is available.**

```
Analyze → Design → Build → Critique → QA → Anti-Slop (final gate) → done
```

## Start with what you are doing

Tell RYUX what you are doing; RYUX decides what it needs to know. Pick the entry point, read its
file, then read only the knowledge modules the task needs (task table below). Paths are relative
to this skill's folder.

| Entry point | When | Read |
| --- | --- | --- |
| **Analyze** | understand a screen, product, or flow that exists | `capabilities/analyze.md` |
| **Design** | create or improve UI and UX without code: Figma, pen.dev, mockups, copy | `capabilities/design.md` |
| **Build** | implement or change the interface in code | `capabilities/build.md` |
| **Critique** | find what should change first, and why | `capabilities/critique.md` |
| **QA** | verify a build against the intended design | `capabilities/qa.md` |

Knowledge modules (`knowledge/`): product, ux, interaction, forms, edge-cases, content, ui,
design-system, accessibility, responsive, frontend, and anti-slop. Evidence comes from the brief, the
project, product data, standards, and the ryux MCP when connected; none is required. Every entry point ends at the quality gates: the Hard
Gates below and the Delivery Gate, with anti-slop as the last check, never the starting point.

Keep the capabilities apart; do not collapse them into one generic "design" answer:

| Capability | Answers | Example |
| --- | --- | --- |
| Analyze | What exists? | "The screen uses a 24px horizontal container." (observed) |
| Design | What should we do, and why? | "Keep 24px: it matches the existing layout system." |
| Critique | Is this decision right? | "24px leaves the table too sparse at 1440 for daily use." |
| QA | Does the build match the intent? | "The build uses 16px where the design says 24px." |

## How RYUX works

1. **Understand the request**: who, what task, which product and market (RX-PR-01). Read the
   RYUX project context in DESIGN.md first when it exists; do not guess what it leaves blank. Ask
   only when the answer would change a major decision (at most three, usually none), and assume
   the rest visibly. DESIGN.md answers are direction, not evidence of what users need.
2. **Pick the entry point** and read its file.
3. **Select knowledge**: read the modules the task table lists, and no others.
4. **Gather evidence**: reference screens through the ryux MCP when connected; otherwise say so.
5. **Reason**: decide with evidence (RX-PR-09, RX-PR-10); on expressive surfaces, set a point of
   view first (RX-UI-12).
6. **Produce**, then render and inspect what you made.
7. **Run the gates**: Hard Gates and the Delivery Gate, with honest claims.

Skip steps that do not apply, but never go from "generate" straight to "done".

## Principle

Do not optimize for visual novelty. Optimize for clarity, usability, consistency, product fit,
accessibility, and intentional decisions. Understand the context before deciding; separate observed
facts from assumptions; prefer evidence over aesthetic preference; do not invent requirements;
explain meaningful decisions with their trade-off; validate before claiming.

## Evidence model

Say where every claim comes from:

| Source | Meaning | Example |
| --- | --- | --- |
| **Observed** (or Measured) | seen in the design, a capture, or read from its values | "body text is 16/24, from the CSS" |
| **Inferred** | a reasonable guess; say it is one | "probably an 8px scale" |
| **Knowledge** | a known pattern or standard, cited | "WCAG 1.4.3", "observed in 4 screens, scr_..." |

Product evidence (brief, requirements, analytics, research, support data) is Observed when sourced;
reference screens show what products do, not what this product's users need. Four questions, not four
output fields: where it came from (source, above), is it known (known, inferred, or **unknown**, kept
visible), how strong is the basis (Strong, Thin, None), how sure is the choice (High, Medium, Low).
Knowledge is what is generally known, evidence is what this context shows, judgment chooses from both.

Rate the evidence for a decision **Strong** (2+ comparable screens), **Thin** (one, or another
context), or **None** (a judgment call; say so, RX-PR-10). Scope each claim to its evidence: one
screen supports "observed in scr_x", not "apps do X"; name the count ("in 4 observed screens"), and
never generalize to a market or category from Thin evidence (RX-PR-02). Label every visual asset's provenance:
**observed** (from the real product), **sourced** (licensed, with its source), **illustrative**
(made to explain, labeled), **generated** (from a Visual Brief, labeled), or **inferred** (a
stand-in until the real one exists). Never invent numbers, user behavior, business rules, research,
compliance, product or competitor facts, screenshots, or references (RX-PR-02, RX-AS-01).

Record a source as `{ type: observed | inferred | knowledge, origin, reference }`, for example
`{ knowledge, ryux-knowledge, scr_123 }` from the ryux MCP, or `{ observed, screenshot, hero.png }`.
Optional sources (the ryux MCP, Figma, a browser, screenshots, other reference libraries) add
evidence when connected; none is required.

## Levels

- **[Required]**: applies within its stated scope; an exception needs a written reason.
- **[Preferred]**: the default; break it only with a short written reason.
- **[Contextual]**: applies only when its "When" situation is present.
- **[Hard Gate]**: a Required rule with no exceptions. Fix it before declaring the work complete.
- **[Quality Lock]**: consistency that must hold across the product.

## Hard Gates (always apply)

No written exception; fix before delivery.

- **Fake data or fake metrics.** Do not invent "48.000+ users", "4,8★", or "+12%". (RX-AS-01)
- **Fake testimonials or people.** Do not make up testimonials, reviewers, or customer photos. (RX-AS-02)
- **Invented business rules or product requirements.** Do not invent business rules, metrics, user data, permissions, pricing, requirements, or API behavior, or name a tool, command, integration, platform, or page the product does not have. (RX-PR-02, RX-FE-02)
- **Placeholder copy shipped as final.** Do not ship placeholder copy or data disguised as final. (RX-AS-03)
- **Fake urgency or scarcity.** Do not write "only 2 left", "offer ends tonight", or fake countdowns with nothing behind them. (RX-AS-04)
- **Missing critical states.** Do not ship only the filled, happy-path screen. (RX-EC-01)
- **Broken responsive behavior.** Do not design for one width only. (RX-RD-01)
- **Accessibility failures.** Do not put light grey text on white or white text on a pale accent. (RX-A11Y-01, RX-A11Y-02, RX-A11Y-03, RX-A11Y-04)
- **Unclear goal or competing actions.** Do not put two equal-weight calls to action side by side, or leave the screen's goal unclear. (RX-PR-03)
- **Unexplained interaction behavior.** Do not ship an action whose in-progress, result, or failure behavior is undefined. (RX-IX-01, RX-IX-12)
- **Duplicate components.** Do not create a near-duplicate component or pattern for one screen. (RX-DS-01)
- **Unnecessary complexity.** Do not add settings, sections, abstractions, or packages "for later", or features because similar products have them. (RX-AS-06)

## Task table: which knowledge to read

| Task | Read |
| --- | --- |
| UI implementation | `knowledge/product.md`, `knowledge/ux.md`, `knowledge/ui.md`, `knowledge/design-system.md`, `knowledge/frontend.md`, `capabilities/qa.md`, `knowledge/anti-slop.md` |
| Form implementation | `knowledge/product.md`, `knowledge/ux.md`, `knowledge/forms.md`, `knowledge/interaction.md`, `knowledge/accessibility.md`, `knowledge/edge-cases.md`, `knowledge/content.md` |
| Mobile UI | `knowledge/ux.md`, `knowledge/ui.md`, `knowledge/responsive.md`, `knowledge/accessibility.md`, `knowledge/anti-slop.md` |
| Checkout or payment | `knowledge/product.md`, `knowledge/interaction.md`, `knowledge/forms.md`, `knowledge/content.md`, `knowledge/edge-cases.md` |
| Data-heavy view (list, table, dashboard) | `knowledge/ux.md`, `knowledge/edge-cases.md`, `knowledge/responsive.md`, `knowledge/design-system.md`, `knowledge/frontend.md` |
| Frontend logic or utilities (formatting, state, data shown to users) | `knowledge/frontend.md`, `knowledge/content.md`, `knowledge/edge-cases.md` |
| Copy only (UI text, chat, announcements) | `knowledge/content.md`, `knowledge/anti-slop.md` |
| Visual refinement | `knowledge/ui.md`, `knowledge/design-system.md`, `capabilities/qa.md`, `knowledge/anti-slop.md` |
| Review or critique | `capabilities/critique.md` (Design Read + heuristic_eval), plus `capabilities/qa.md` |

## Delivery Gate

End UI, UX, copy, or frontend work with this report:

```
PRODUCT        PASS | FAIL | NOT VERIFIED | N/A  · one-line reason · evidence Strong | Thin | None
UX             PASS | FAIL | NOT VERIFIED | N/A  · one-line reason
UI             PASS | FAIL | NOT VERIFIED | N/A  · one-line reason · point of view: <concept> | task UI
DESIGN SYSTEM  PASS | FAIL | NOT VERIFIED | N/A  · one-line reason
ACCESSIBILITY  PASS | FAIL | NOT VERIFIED | N/A  · one-line reason
RESPONSIVE     PASS | FAIL | NOT VERIFIED | N/A  · one-line reason
EDGE CASES     PASS | FAIL | NOT VERIFIED | N/A  · one-line reason
CODE QUALITY   PASS | FAIL | NOT VERIFIED | N/A  · one-line reason
VISUAL QA      PASS | FAIL | NOT VERIFIED | N/A  · one-line reason
ANTI-SLOP      PASS | FAIL | NOT VERIFIED | N/A  · one-line reason
FINAL          PASS | FAIL | NOT VERIFIED
```

- Each area is PASS, FAIL, NOT VERIFIED (it applies, but the evidence was not available: name what is missing), or N/A (it does not apply: say why).
- An area FAILS when a [Required] rule in its skills fails without a written exception.
- A Hard Gate failure cannot be excepted: fix it before declaring the work complete.
- VISUAL QA without a render is NOT VERIFIED; say which render tool was used.
- CODE QUALITY is NOT VERIFIED while changed logic has no test run; say which checks ran (typecheck, tests).
- FINAL is FAIL if any area fails, NOT VERIFIED if none fails but one is not verified, else PASS. PASS means the checked criteria were met, not that the design is good.

## Honest claims

Report what was checked, how, and what was not available. Do not claim "pixel perfect",
"fully accessible", "production ready", "senior-level", or "UX optimized" without evidence. Say
"Keyboard and focus checked by hand; no automated accessibility test was available" instead.

## Design Decision Record

For consequential choices (RX-PR-09) and deviations, write **Decision**, **Options** compared, **Evidence**,
**Trade-off**, and **Choice**. Evidence is Strong (2+ comparable screen_ids), Thin (one, or another context),
or None (no screen_id: a judgment call). With None on a consequential choice, show options or ask (RX-PR-10).

Reference screens and structured review come from the ryux MCP (`search_screens`,
`heuristic_eval`, `delivery_gate`). The hosted server is not live yet; run it locally and connect:
`claude mcp add --transport http ryux http://localhost:8787/mcp`
