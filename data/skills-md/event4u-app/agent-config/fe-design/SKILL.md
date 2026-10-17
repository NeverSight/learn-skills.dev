---
model_tier: medium
name: fe-design
description: "Frontend design heuristics and the loop applying them: existing-ui-audit, brief, inventory, build, review. Use when building or changing any UI, not only when planning one."
personas:
  - frontend-engineer
domain: engineering
workspaces:
  - engineering
packs:
  - engineering-base
---

# Frontend Design Skill

## Ad-hoc mode — outside the engine, YOU run this loop now

One question decides which mode you are in: **is a `/implement-ticket` run
dispatching this?**

| Situation | Who owns the UI write | This skill is |
|---|---|---|
| A ticketed run — the UI directive set is dispatching | `directives/ui/*` | a reference it cites |
| Anything else — "build me the page", "improve this form", "implement the approved design" | **you, in this turn** | the executor |
| A renderer axis is in play — WebGL / Three.js / canvas / scroll-scrubbed video | **still you** — the renderer is a grounding question, not a second executor | the executor, grounded via `search_stack` |

The third row is an **axis**, not an owner. Renderer selection resolves through
machinery that already exists: `search_stack` in
[`corpus-grounding`](../corpus-grounding/SKILL.md)
(`scripts/decision_engine.ts`), whose stack corpus carries `threejs.csv` among
its stacks, read beside the register in
`design-intelligence`
§ Register. No second frontend executor is declared, and none is needed: a
renderer changes what you ground against, never who writes the UI.

Outside the engine, nothing else owns the design quality of a UI write. Reading
this skill and then writing the UI from priors is the failure it exists to
prevent — the loop below is not optional context, it is the work.

**Skip only when the change is `ui-trivial`, decidable off the diff:** ≤ 1 file,
≤ 5 changed lines, no new component, no new state, no new dependency. Anything
else runs the loop.

### The loop

1. **Audit first** — run [`existing-ui-audit`](../existing-ui-audit/SKILL.md).
   What already exists (components, tokens, layout conventions) outranks every
   heuristic below. Reinventing an existing component is the #1 failure mode.
2. **Brief** — seven keys before any code. Five are the ones the engine gates
   (`REQUIRED_BRIEF_KEYS`): `layout`, `components`, `states`, `microcopy`,
   `a11y`. `states` means all five of `empty`, `loading`, `error`, `success`,
   `disabled` — a brief missing one is unfinished, not concise.

   Two more are **declared, not gated**: `frequency` and `initiation`. The
   engine does not halt on them, and that is stated rather than left to be
   discovered — adding a required key would halt every brief already written
   against the five.

   | Key | Values | Why it is declared and never inferred |
   |---|---|---|
   | `frequency` | `one-time` · `low` · `medium` · `high` (100+ per day) | How often a surface is used decides whether motion on it reads as polish or as a toll. Nothing in a diff reveals it. |
   | `initiation` | `keyboard` · `pointer` · `system` | A keyboard-initiated surface is reached by someone who already knows where they are going; an animation there is pure latency. |

   Both are prefilled from the surface's role and overridden only on evidence.
   There is no resolver and no inference from handlers: a `mousemove` listener
   is not proof of pointer initiation, and a keyboard shortcut in the code is
   not proof anyone uses it.

   | Surface role | `frequency` | `initiation` |
   |---|---|---|
   | Command palette | `high` | `keyboard` |
   | Tooltip | `high` | `pointer` |
   | Modal / sheet | `medium` | `pointer` |
   | Onboarding flow | `one-time` | `pointer` |
   | Toast / notification | `medium` | `system` |
   | Table row action | `high` | `pointer` |

   The default for a role not listed is `medium` / `pointer`, stated in the
   brief as a default rather than left blank.
3. **Inventory — only when an artifact was provided, and before you build.**
   List the artifact's **interactions, keyframes, and script includes** from its
   source (`design-fidelity-mechanics` § Data-basis ladder — read it, do not
   look at a picture of it). Then place **every** listed item in exactly one
   bucket, using the engine's own names (`apply.ts`, `COVERAGE_BUCKETS`) so the
   two surfaces read the same. **Nothing enforces that they stay the same** —
   this is a copied vocabulary, not a shared constant, and no test pins it;
   renaming a bucket in the engine leaves this list stale and silent:

   | Bucket | Meaning |
   |---|---|
   | `honoured` | carried over as-is |
   | `translated` | carried over in a different shape (a handler became a framework binding) |
   | `flagged` | **not** carried over — with the reason, in the output |

   Dropping a handler stays allowed; hiding one does not. An item in no bucket
   is the failure this step exists to catch — "missing JavaScript" is what it
   looks like from the user's side. Inside the engine this is enforced
   (`apply.ts`, `COVERAGE_BUCKETS`, an unaccounted item is a halt); out here it
   is a duty you carry, and nothing checks it for you. (fixture:
   `daf-adhoc-port-coverage`.)
4. **Build** — against the audit's primitives, in the project's stack. Where the
   artifact's own markup/CSS/JS is stack-compatible, adapt **that code**;
   re-deriving it from scratch is a deviation needing confirmation
   (`design-fidelity-mechanics` § Adopt the code).
5. **Review, then re-enter** — run [`design-review`](../design-review/SKILL.md)
   before calling it done, and scope the verdict honestly: render-scoped when
   you can render it, otherwise explicitly static-scoped, naming which checks
   actually ran. "Looks good" with neither scope named is a verdict without
   evidence. Findings → fix them and **re-enter step 5**, at most **2 rounds**,
   and **stop early on a null**: a round that produces **no new finding** ends
   the loop, and a round that produces only findings the provided artifact
   already covers produces no new finding. At the 2-round ceiling with findings
   still open, stop and hand the remaining list back — ship-as-is or abort is
   the user's call, never another silent pass. Judgement alone never buys a
   third round.

   The ceiling is **2**, the same number the engine enforces
   (`directives/ui/polish.ts`, `POLISH_CEILING`), so the ad-hoc path and the
   ticketed path bound the loop identically rather than by two conventions that
   can drift. Fixtures: `daf-adhoc-converges` (round 2 is a null, loop ends) and
   `daf-adhoc-ceiling` (findings remain at the ceiling, loop hands back).

### The floors — pulled immediately before the write

```
PULL references/craft-floor.md IMMEDIATELY BEFORE THE WRITE, NOT AT SKILL LOAD.
```

Twelve universal floors that do not vary by mode, register, intent or stack.
They were inline here until the delivery point moved: a floor read at skill-load
time can be a compaction away from the write it governs (`ADR-227`).

One precedence rule stays here because it is authority, not craft: **the audit
outranks every heuristic.** Say `[audit override]` when it does.

## Positioning — reference inside the engine, executor outside it

Inside a `/implement-ticket` run, `fe-design` is a **universal reference
skill**: it carries stack-agnostic heuristics the UI directive set cites, and
it does not own the flow. The ownership table below applies **to that mode**.
Outside the engine the table has no dispatcher behind it — the ad-hoc loop
above is the owner instead.

| Concern | Owner (engine-mediated runs) |
|---|---|
| Layout / states / microcopy lock | [`directives/ui/design.ts`](../../templates/scripts/work_engine/directives/ui/design.ts) |
| Stack-dispatched implementation | [`directives/ui/apply.ts`](../../templates/scripts/work_engine/directives/ui/apply.ts) → `blade-ui` / `livewire` / `flux` / `react-shadcn-ui` |
| Existing-component inventory + tokens | [`existing-ui-audit`](../existing-ui-audit/SKILL.md) (mandatory pre-step) |
| Grounded selection (style, color tokens, typography, pattern, anti-patterns) | [`design-intelligence`](../design-intelligence/SKILL.md) — corpus-grounded; this skill stays the heuristic layer and *invokes* it |
| Design-review polish loop | [`directives/ui/review.ts`](../../templates/scripts/work_engine/directives/ui/review.ts) + [`directives/ui/polish.ts`](../../templates/scripts/work_engine/directives/ui/polish.ts) |

## When to use

Cite this skill when:

- Planning a new page or feature UI before implementing
- Choosing between component patterns (modal vs. inline, table vs. cards)
- Designing forms with complex validation or multi-step flows
- Making responsive design decisions
- Reviewing UI for accessibility and usability

**Inside a ticketed run**, do NOT use this skill to:

- Implement components — that is the apply-step's stack-dispatched skill
- Audit an existing UI — that is `existing-ui-audit`
- Drive the full UI flow — that is the `directives/ui/` orchestrator

Outside a ticketed run, the first and third lines invert: no dispatcher is
running, so implementation quality and the flow are yours. The second holds in
both modes — the audit is always `existing-ui-audit`; you invoke it, you do not
replace it.

> **Resource-first, before taste.** Any request to recreate / redesign / mock /
> prototype / improve an existing UI runs the
> [resource-first context gate](../existing-ui-audit/SKILL.md#resource-first-context-gate-design-fidelity)
> FIRST — search the project's tokens/design-system/assets, hard-stop and ask
> when a referenced source is inaccessible (never invent from memory), and
> prefer code over screenshots for exact values. Planning here starts from that
> inventory, not from generic aesthetic memory (design-artifact lifecycle,
> Inspect stage).

## How the directive set cites this skill

`directives/ui/design.ts` produces the design brief (layout, components,
states, microcopy, a11y). Selection decisions (style, semantic color
tokens, typography pairing, layout pattern, anti-patterns) come **grounded**
from [`design-intelligence`](../design-intelligence/SKILL.md) — run its
corpus query first; fall back to the heuristics in this reference only
where the corpus reports an evidence gap or the audit already pins a
project pattern. Stack-specific choices come from the dispatched
implementation skill, not from here.

> **When the corpus is not installed.** `design-intelligence` ships in the
> `frontend-design` pack; this skill ships in `engineering-base`. A consumer
> who installed only `laravel` or only `react` therefore has this skill and
> **not** the corpus. Fall back to the heuristics here and say so in the
> result — "selected from heuristics; `frontend-design` not installed, so no
> corpus grounding". The evidence-gap fallback above is about a corpus that
> answered "nothing here"; this is about a corpus that is absent. Never
> present an ungrounded pick as grounded, and never record a missing pack as
> an evidence gap.

## Section index — load on demand

Load the reference file whose sections the task needs — never all of them by default:

- [`references/design-patterns.md`](references/design-patterns.md) — Component Architecture · Form Design · Table Design · Responsive Strategy · Accessibility (a11y) · Motion — decision-tree and rationale · UX Principles · Craft details — typography & imagery · Presenting variants
- [`references/design-read-and-memory.md`](references/design-read-and-memory.md) — Cross-task design memory — read DESIGN.md / PRODUCT.md first · Register — brand vs product · Design Read — articulate intent before generating · Aesthetic direction

## Procedure

When `directives/ui/design.ts` (or any caller) cites this skill:

1. **Inspect `state.ui_audit` first** — review the audit produced by [`existing-ui-audit`](../existing-ui-audit/SKILL.md); it is mandatory. Stop and request the audit if missing.
2. **Pick the smallest matching section** — Component Architecture, Form Design, Table Design, Responsive Strategy, Accessibility, or UX Principles. Cite by H2/H3 heading, never paste the whole skill.
3. **Defer to audit findings** — when the audit pins a project pattern (token, primitive, layout convention), use it. The heuristics here are fallbacks for gaps, not overrides.
4. **Defer to the stack apply skill** — Blade vs. Livewire vs. Flux vs. React-shadcn choices come from the dispatched implementation skill, never from this reference.
5. **Surface conflicts** — if a heuristic here contradicts an audit finding or stack convention, name both and let the caller decide; do not silently pick.

## Output format

When this skill's content is folded into a design brief or review:

1. Quote the cited heuristic verbatim, with the H2/H3 heading and a one-line "why this applies" tie-back to the request.
2. Map each heuristic to a concrete artifact in the brief (component, form section, table column, breakpoint rule, a11y check, UX state).
3. Keep stack-agnostic — never name Blade/Livewire/Flux/React primitives in the cited prose; the apply step adds those.
4. Mark anything overridden by audit findings as `[audit override]` and link to the audit entry.

## Related

- **Orchestrator:** [`directives/ui/`](../../templates/scripts/work_engine/directives/ui/) — owns the UI flow
- **Pre-step (mandatory):** [`existing-ui-audit`](../existing-ui-audit/SKILL.md) — inventory before design
- **Stack apply skills (dispatched, not standalone):**
  - [`blade-ui`](../blade-ui/SKILL.md) — Blade template implementation
  - [`livewire`](../livewire/SKILL.md) — Livewire component implementation
  - [`flux`](../flux/SKILL.md) — Flux component library usage
  - [`react-shadcn-ui`](../react-shadcn-ui/SKILL.md) — React + shadcn primitives
- **Adjacent reference:** [`dashboard-design`](../dashboard-design/SKILL.md) — monitoring dashboard design (different domain)

## Gotcha

- Don't design components without running `existing-ui-audit` first — the audit's component/token inventory is the canonical source for "what already exists in this project". Reinventing is the #1 failure mode.
- Heuristics in this reference apply across stacks; do not promote them to project rules without checking the audit.
- Mobile-first is not optional — every layout must work on 320px width.

## Read the authority object — never re-infer it

Read the resolved `ui_authority`
([contract](../../../docs/contracts/ui-authority.md)) before the loop:
`surface_mode`, `register`, `change_intent`, `reference_maturity`,
`constraints`. This skill is a **declared consumer** — a second decision table
beside the object is a drift surface, so do not re-derive any field.

`surface_mode` sets density, hierarchy and expressiveness only, per
[`design-modes`](../../../docs/guidelines/design-modes.md) § The second axis.

```
QUALITY FLOORS DO NOT VARY BY SURFACE MODE.
A FLOOR THAT MOVES WITH THE MODE IS A PREFERENCE WEARING A FLOOR'S NAME.
```

### The source-led path

`reference_maturity: runnable-artifact` → the artifact's own markup, CSS and JS
is the data basis; adapting it is the **default** and a from-scratch
re-derivation is a deviation. Sort every mechanic into `honoured` / `translated`
/ `flagged`; one present, absent and unflagged is a **silent drop**, target zero.
Procedure and the vanishing-mechanic classes:
[`references/source-led-port.md`](references/source-led-port.md).

Maturity is not decided here — it arrives on the authority object, and per-value
provenance belongs to `road-to-frontend-fidelity-calibration` Phases 0 and 2.

## Anti-slop discipline

Before proposing a direction, scan the Visual (V1–V8) and Layout (L1–L10)
sections of [`design-antipatterns`](../../../docs/guidelines/design-antipatterns.md),
plus Motion (M1–M8) for the interaction layer.
On a match, choose differently or invoke the entry's own override condition in
the brief — every entry has one. Two of them, T7 and T8, are additionally
*register-scoped*: the brand and product registers admit different answers, and
neither admits an undeclared pick. The Q* floors are
in [`references/craft-floor.md`](references/craft-floor.md) instead of here, so
they arrive at the write rather than at skill load.

## Do NOT

- Do NOT skip mobile viewport testing.
- Do NOT use fixed pixel widths for responsive layouts.
- Do NOT ignore accessibility requirements.
- Do NOT use this skill as an executor INSIDE a ticketed run — there the executor is `directives/ui/design.ts` and this is the reference it cites. Outside one, the ad-hoc loop at the top of this file IS the executor; do NOT read the reference and then write the UI from priors.
