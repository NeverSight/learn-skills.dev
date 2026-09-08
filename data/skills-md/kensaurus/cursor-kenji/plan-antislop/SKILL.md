---
name: plan-antislop
description: >
  Plan-only authenticity / AI-slop audit across prose, UI, code, and IA.
  Use when "looks like AI slop", "reads like ChatGPT", or "authenticity
  burndown". One-page UX apply → enhance-web-ux. Visual polish →
  enhance-web-ui.
license: MIT
---

# Anti-Slop Audit + Authenticity Burndown Plan

**Degree of freedom: HIGH** — inventory tells, score, plan. Stay
**plan-only**. No rewrites until each phase is approved.

## This skill vs neighbors

| Skill | Owns |
|---|---|
| **plan-antislop** (this) | Authenticity / slop burndown (plan only) |
| `enhance-web-ui` / `enhance-web-ux` | Apply polish after the plan |
| `plan-uiux-unification` | Design-system + IA unification |

## How to reason (every plan item)

1. **Propose** — direction to remove a tell (not the rewrite)
2. **Risk** — how loudly it reads as machine-made, and who sees it first
3. **Keep-working** — copy/UI/code that already sounds or looks intentional
4. **Phase** — copy → visual → IA → code (do not execute)

## Worked example

> **Propose:** replace the hero dual-clause ("It's not just a tracker, it's a companion") with the concrete benefit already in the docs.
> **Risk:** first-screen cadence is the loudest AI tell; readers bounce.
> **Keep-working:** settings microcopy is already terse and product-specific.
> **Phase:** Phase 1 — copy pass via `docs-writer`.

**Role:** Senior editor + product designer + staff engineer (authenticity lens).

**Task:** Inventory machine-generated tells across prose, visual/UI, code, and structure/IA.
Score each finding by recognizability × effort, cluster into phased burndowns, emit
`plan-antislop.md`. **Audit & plan only — no rewrites until each phase is approved.**

**Find the AI tells. Plan their removal. Change nothing until approved.**

"Slop" is content that is *recognizably* machine-generated: technically fine,
semantically empty, and uniform in a way no human hand would produce. This skill
is the **audit-and-plan** half of de-slopping. It inventories slop across four
surfaces, ranks each finding by *recognizability × effort*, and emits a phased
burndown the user approves before any rewrite happens.

This skill never rewrites. It produces `plan-antislop.md`. Execution is handed to
`enhance-web-ux`, `enhance-web-ui`, `enhance-web-landing`, `design-frontend`,
`audit-i18n`, or `docs-writer` after approval — same contract as every `plan-*`
skill in this repo.

---

## When this fires

Trigger phrases: *"this feels AI-generated"*, *"de-slop this"*, *"reads like
ChatGPT"*, *"make it sound human"*, *"every page looks identical"*, *"it's
generic/templated/soulless"*, *"strip the AI smell before launch"*, *"voice and
authenticity pass"*.

Do **not** fire for: functional bugs (`debug-*`), security/RLS
(`plan-security-audit`), missing tests (`plan-test-coverage`), or designing a new
surface from scratch (`design-frontend`). Slop is about *recognizability*, not
correctness — code can be 100% working and still be 100% slop.

---

## The four slop surfaces  [HIGH freedom]

Audit each surface the codebase actually has. Skip surfaces that don't apply
(a backend-only repo has no visual surface).

### 1 · Prose & copy slop

The most detectable surface. Scan all user-facing strings, marketing copy,
READMEs, microcopy, error messages, and comments for:

- **Cadence tells** — "It's not just X, it's Y." / "In today's fast-paced world…"
  / "Let's dive in." / "The result? …" / "But here's the thing:" / rhetorical
  question → one-line answer.
- **Filler vocabulary** — *delve, tapestry, realm, landscape, leverage,
  seamless, robust, elevate, unlock, empower, navigate, foster, testament,
  bustling, vibrant, game-changer, at the end of the day.*
- **Hedge-and-pad** — "it's important to note that", "it's worth mentioning",
  "in conclusion", triple-adjective stacks, sentences that restate the heading.
- **Punctuation tics** — em-dash overuse, "—and that's the point.", emoji as
  bullet points, Title Case Everywhere, bolded **every** other phrase.
- **Empty symmetry** — three benefits that are the same benefit, "Fast. Simple.
  Powerful." triads, conclusions that summarize a 2-paragraph page.

Output for each: file/line, the tell, *why a human wouldn't write it*, and a
direction for the fix (not the fix itself).

### 2 · Visual & UI slop

The "I've seen this exact app 400 times" surface:

- **Default-palette tell** — untouched shadcn violet/zinc, the default Tailwind
  blue-600 CTA, no brand color anywhere.
- **Card-grid monotony** — every section is a 3-up grid of identical rounded
  cards with an icon, a bold title, and two lines of gray text.
- **Centered-everything** — every section center-aligned, max-w-2xl, same
  vertical rhythm, no asymmetry, no intentional focal point.
- **Iconography slop** — a lucide icon on every feature whether it means
  anything or not; emoji in headings.
- **No hierarchy** — all sections weighted equally; nothing is the hero, nothing
  recedes; uniform spacing top to bottom.
- **Generic motion** — fade-in-on-scroll on everything, or no motion at all.

Cross-check against the project's design tokens if `audit-uiux-design-system`
data or a tokens file exists — slop is often *divergence from* the design system
plus *convergence toward* the framework default.

### 3 · Code slop

Working code that no engineer would have left as-is:

- **Placeholder residue** — `// TODO: implement`, `// your logic here`,
  `foo`/`bar`/`data`/`handleClick` naming, `lorem ipsum`, commented-out
  scaffolding, `console.log('here')`.
- **Comment slop** — comments restating the code (`// increment i by 1`),
  docstrings that paraphrase the function name, banner comments around trivial
  blocks.
- **Over-abstraction** — a factory + interface + strategy for one concrete case;
  `utils/helpers/index.ts` dumping grounds; premature generics.
- **Copy-paste uniformity** — five near-identical components that should be one
  parameterized component; the same try/catch boilerplate everywhere.
- **Defensive theater** — `if (!data) return null` guards that can't trigger;
  empty catch blocks; types widened to `any` to silence the compiler.

This overlaps `audit-code-quality` — here the lens is specifically *"looks
auto-generated"*, not general correctness. Flag, don't fix.

### 4 · Structure & IA slop

The shape of the thing:

- **Listicle-brain** — everything is a bulleted list because the model defaults
  to lists; no prose, no flow, no argument.
- **Symmetrical IA** — every page has identical Hero → Features → Testimonials →
  CTA scaffolding regardless of purpose.
- **README slop** — emoji-headers, a feature table no one asked for, "## Getting
  Started" boilerplate, badges that don't link anywhere, a "Contributing"
  section on a solo throwaway.
- **Empty completeness** — sections that exist because the template had them
  (FAQ with invented questions, "Roadmap" with placeholder quarters).

---

## Procedure  [HIGH freedom]

1. **Scope.** Identify which of the four surfaces exist. State assumptions. If
   the user pointed at a specific route/file, scope to it; otherwise sweep the
   user-facing surface area.
2. **Inventory.** Walk each in-scope surface. Collect concrete findings with
   `path:line` (or route + screenshot region for visual). Quote the *minimum*
   needed to identify the tell — never paste whole files.
3. **Score.** Rate each finding **Recognizability** (how loudly it screams "AI
   wrote this": High / Med / Low) × **Effort** (S / M / L). High-recognizability +
   Small-effort items are the top of the burndown — biggest authenticity gain per
   minute.
4. **Cluster into phases.** Group findings so each phase is independently
   shippable and maps to one execution skill. Suggested default ordering:
   - **Phase 1 — Copy pass** (`docs-writer` / `audit-i18n`): kill cadence tells &
     filler vocab. Highest signal, lowest risk, no visual regression.
   - **Phase 2 — Visual identity** (`enhance-web-ui` / `design-frontend`): break
     the default palette, introduce hierarchy and one intentional focal point per
     view, de-monotonize the card grids.
   - **Phase 3 — UX & flow** (`enhance-web-ux` / `enhance-web-landing`): fix IA,
     replace symmetrical scaffolding with purpose-driven structure.
   - **Phase 4 — Code cleanup** (`audit-code-quality` / `workflow-refactor`):
     placeholder residue, comment slop, over-abstraction.
5. **Emit the report.** Write `plan-antislop.md` (template below). End the turn.
   **Do not start Phase 1.** Wait for explicit approval per phase — the
   `composer-2.5-execution.mdc` handoff contract applies.

---

## Guardrails  [LOW freedom — run exactly]

- **Plan only.** No rewrites, no edits, no "while I'm here" fixes. The deliverable
  is the report.
- **Slop ≠ broken.** Don't flag working code as slop just because it's simple.
  Simple-and-intentional is the *goal*, not a defect. The test is "would a human
  engineer/writer have left this exact thing?" — not "could this be fancier?"
- **Voice is the user's, not yours.** Recommend *directions* ("warm up the CTA
  copy to match the conversational tone of the docs"), never ghost-write the
  replacement in the plan. The whole point is to remove generic voice, so don't
  inject a different generic voice.
- **Don't over-correct into anti-slop slop.** Forced quirkiness, ironic
  lowercase, gratuitous em-dashes-the-other-way, and "edgy" copy are *also* slop.
  Flag the tendency; aim for intentional, not performative.
- **Cite the design system.** When flagging visual slop, reference the project's
  actual tokens/brand if they exist. "Diverges from your defined `--brand-500`"
  is actionable; "use nicer colors" is not.
- **Minimal quoting.** Identify tells by location and short excerpt; never
  reproduce large blocks of the source.

## Self-critique before the burndown  [LOW freedom — do not skip]

1. **evidenced-not-assumed** — `path:line` (or route + region) plus the tell
2. **plan-only** — direction only; no rewrite and no ghost-written replacement
3. **phase justified** — high-recognizability + small-effort leads; copy before code
4. **right-owner** — functional bugs → `debug-*`; new surface from scratch → `design-frontend`
5. **no-false-safety** — simple-and-intentional is not slop; don't invent anti-slop slop

---

## Report template — `plan-antislop.md`

```markdown
# Anti-Slop Burndown — <repo/route>

_Audit-only. Nothing changes until each phase is approved._

## Scope
- Surfaces audited: [ ] Prose  [ ] Visual  [ ] Code  [ ] Structure
- Out of scope / assumptions: …

## Slop score (at a glance)
| Surface    | Findings | High-recognizability | Top quick win |
|------------|----------|----------------------|---------------|
| Prose      | n        | n                    | …             |
| Visual     | n        | n                    | …             |
| Code       | n        | n                    | …             |
| Structure  | n        | n                    | …             |

## Findings
### Prose & copy
| # | Location | Tell | Why it reads as AI | Recog | Effort | Direction |
|---|----------|------|--------------------|-------|--------|-----------|
| P1 | hero/page.tsx:24 | "It's not just a tracker, it's a companion" | dual-clause hype cadence | High | S | state the concrete benefit plainly |

### Visual & UI
| # | Route/region | Tell | Recog | Effort | Direction |
|---|--------------|------|-------|--------|-----------|

### Code
| # | path:line | Tell | Recog | Effort | Direction |
|---|-----------|------|-------|--------|-----------|

### Structure & IA
| # | Location | Tell | Recog | Effort | Direction |
|---|----------|------|-------|--------|-----------|

## Phased burndown
- **Phase 1 — Copy pass** → `docs-writer` / `audit-i18n` — items P1, P3, P7…
- **Phase 2 — Visual identity** → `enhance-web-ui` / `design-frontend` — V1, V2…
- **Phase 3 — UX & flow** → `enhance-web-ux` / `enhance-web-landing` — S1, S4…
- **Phase 4 — Code cleanup** → `audit-code-quality` / `workflow-refactor` — C2…

## Execution handoff
Approve a phase to run it. Suggested order maximizes authenticity-per-effort.
Re-run `plan-antislop` after execution to confirm the burndown closed.
```

---

## Chains with

- **Six-skill plan loop** — slots beside `plan-uiux-unification`; run after it so
  visual-slop findings inherit the design-system burndown.
- **Execution:** `enhance-web-ux`, `enhance-web-ui`, `enhance-web-landing`,
  `design-frontend`, `audit-i18n`, `docs-writer`, `workflow-refactor`.
- **Verify:** after execution, `test-playwright` (does it still work?) and a
  second `plan-antislop` pass (did the slop actually drop?).

> Plan with a strong reasoning model; execute with `composer-2.5-execution.mdc`
> riding along. The plan says *which* slop to remove; the rule constrains *how*.
