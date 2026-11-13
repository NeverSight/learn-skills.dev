---
name: pm-idea-to-plan
description: Orchestrated, idea-to-plan PM workflow. Establishes context once, then composes the PM generative ladder in order — problem → discovery → users → riskiest-assumption test → prioritization → spec → metrics — gating each step, enforcing evidence before the spec, and handing the result to product-review. Trigger when the user wants to go from a raw idea to a build-ready plan ("take me from problem to plan", "I have an app idea, where do I start", "turn this idea into a product plan", "plan a new product end to end") — but NOT when they ask for one specific PM artifact (let that skill trigger directly), and NOT for the strategy/launch arc (vision, competitive analysis, roadmap, GTM — offer those next).
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Idea → Plan (PM Creation Orchestrator) Skill

## How this skill behaves (read first)

This is the **front door for taking a raw idea to a build-ready plan**, and the PM twin of
`ux-design-from-scratch`. Where `pm-product-review` orchestrates the *validation* direction
(generative → audit), this skill orchestrates the *compositional* direction
(generative → generative): it sequences the PM scope ladder —
**problem → discovery → users → riskiest-assumption test → prioritization → spec → metrics** —
pulling in each skill as the work needs it, then hands the result to `pm-product-review` for
validation.

It is the executable form of the **compositional orchestration** section (§9) of
`docs/orchestration-policy.md`, applied to PM. Its whole job is to avoid the failure this skill
was created to fix: **a plan that is overdeveloped as a PRD and underdeveloped as a de-risked
product bet** — a polished spec resting on an unexamined market and an untested
willingness-to-pay. The spec is the *last* rung, not the first, and it never runs before the
evidence rungs beneath it.

> **The one rule that makes this skill earn its place: evidence before spec.** Claude's default,
> asked to "take me from idea to plan," rushes to a plausible-looking PRD — requirements,
> stories, metrics — built on an unvalidated problem and zero adoption evidence. That document
> *looks* complete, which is exactly why it's dangerous: teams build from it. This orchestrator
> forces the problem, the discovery evidence, and the riskiest-assumption test to come *first*,
> and keeps the spec proportionate instead of letting it swallow the plan.

**When NOT to use this skill:**

- **One named artifact** — "write me a PRD", "frame this problem", "build a prioritization
  matrix". Let that skill trigger directly. Explicit scope overrides orchestration.
- **The strategy / launch arc** — vision & strategy, competitive analysis, roadmap, GTM, launch
  experiments. That is a *different* compositional arc (`pm-vision-strategy`,
  `pm-competitive-analysis`, `pm-roadmap`, `pm-gtm-plan`, `pm-experimentation-ab`,
  `pm-analytics`). This skill stops at a validated, build-ready **plan**; offer to continue into
  the strategy arc rather than producing it here.

---

## Step 0 — Establish the context profile (once)

Infer from what the user gave you; ask only the one or two questions that materially change what
runs. State the assumptions you're proceeding with, then build in order. Persist this for the
rest of the session — don't re-ask.

- **The idea, in one line** — what's being proposed, for whom. Restating this back is also the
  first integrity check (if it can only be stated as a solution, the problem isn't framed yet).
- **Stakes & reversibility of the build decision** — a cheap, reversible experiment needs far
  less evidence than an expensive, hard-to-undo bet. This sets how much discovery and testing
  rigor is warranted (over-testing a reversible call is as wrong as under-testing a big one).
- **Stage** — is the *problem* still unproven (does anyone care?), is the *solution* the open
  question (can they use it / will they switch?), or is it *viability/scale* (will they pay,
  does it hold up)? This points each rung at the right depth.
- **Market maturity** — **is this a crowded category?** If yes, the riskiest assumption is almost
  never "can we build it" — it's **switching cost and adoption** (why leave the incumbent?).
  Flag this early; it changes which assumption gets tested first and makes
  `pm-competitive-analysis` a live offer.
- **Evidence already in hand** — existing research, data, or customer contact. Don't re-run
  discovery the user has already done; build on it.

---

## Step 1 — Compose the ladder, gating at each rung

Walk the ladder in order. At each rung classify the skill as **core (apply now) / offer (name,
don't auto-build) / skip (owned elsewhere or already done)** — don't apply every skill at full
depth by default (that's the creation-side bandwagon).

> Child skills are named by their installable skill `name`. Compose one only if it's installed;
> if a named skill isn't present, apply that rung's intent inline with its core best practice and
> note the gap rather than blocking.

### Rung 1 — Frame the problem  ·  `pm-problem-statement` *(core, first)*
Pin the problem as a **gap with evidence**, separated from symptom and solution
(problem + consequence + goal). Nothing downstream is trustworthy until this holds. If the user
can't supply evidence, proceed but **mark the problem as an unvalidated assumption** to be
retired in Rung 3 — don't paper over it.

### Rung 2 — De-risk with discovery  ·  `pm-discovery` *(core — do NOT skip to the spec)*
This is the rung the PRD-rushing default drops, and dropping it is exactly what produces a strong
spec on a weak bet. Discovery establishes **who actually adopts, how it fits their current
workflow, whether they'd switch, and whether they'd pay** — the evidence the plan stands on. Keep
it proportionate to the Step 0 stakes (lightweight continuous contact for a reversible call; a
deeper study for a big irreversible one), but **always run it before the spec**. In a crowded
market, this is where switching-cost evidence comes from.

### Rung 3 — Define the users  ·  `pm-personas-jtbd` *(core)*
Ground the target users in the discovery evidence — jobs-to-be-done and real frustrations, every
detail earning a decision. No demographic fiction. This rung *consumes* Rung 2's output; if
discovery was skipped, personas are guesses and should be labelled as such.

### Rung 4 — Test the riskiest assumption  ·  `pm-assumption-testing` *(core — and foreground it)*
Surface the **leap-of-faith belief** — the one that, if false, sinks the idea — phrase it
falsifiably, and design the **cheapest test that answers it, with pre-set success criteria**.
**Foreground the viability/desirability test, do not bury it under the spec.** In most idea→plan
cases the riskiest belief is *"the people we're targeting will actually adopt this and pay/switch"*
— so a **painted-door, concierge, or pre-sell test that checks real behavior before a line of
code** usually belongs here as an explicit build/no-build gate. A plan that frames this test as a
buried sub-section of the PRD has failed this rung.

### Rung 5 — Prioritize what to build first  ·  `pm-prioritization` *(core)*
Decide the first slice with a method that **traces to the strategy/outcome and exposes
trade-offs**, not fake-precise scores. Prioritization comes *after* the riskiest assumption is
named — you prioritize against validated risk, not against a wish list.

### Rung 6 — Write the plan  ·  `pm-product-spec` *(core, last — and proportionate)*
Only now write the spec/PRD, and keep it proportionate to the evidence beneath it. Every
requirement testable, full flows (not happy paths), explicit scope-out, a
dependencies/constraints/assumptions section, and **each assumption traced back to whether it's
been tested (Rung 4) or is still open**. The spec's job is to *carry forward* the evidence and the
open risks, not to paper over them with polished requirements. `pm-user-story` is owned by this
rung (defer to it).

### Rung 7 — Define success  ·  `pm-okrs-kpis` *(offer → core if metrics carry weight)*
`pm-product-spec` already contains a success-metrics section; pull in `pm-okrs-kpis` when the plan
needs first-class outcome metrics — **outcomes with baseline/target + guardrails**, not vanity
counts. Offer it; make it core when the user asked for success metrics or when the spec's metrics
need real rigor.

> **Consistency rule:** decisions propagate *up* the ladder. The problem framed in Rung 1, the
> evidence from Rung 2, and the validated/open assumptions from Rung 4 are reused by every rung
> above — don't re-litigate them inside the spec. This is the whole point of building idea-up.

---

## Step 2 — Validate via product-review

When the plan exists, hand it to **`pm-product-review`** (if installed), which applies the audit
policy: it **auto-runs `pm-assumption-rigor-audit`** (the always-relevant lens — was the *riskiest*
assumption targeted, falsifiable, matched to a right-fidelity method with pre-set criteria?), and
routes by artifact type — spec → `pm-spec-quality-audit`, metrics → `pm-okr-metric-validity-audit`,
prioritization → `pm-prioritization-rigor-audit`, with `pm-decision-quality-audit` offered for the
build/no-build call. It returns **one** prioritized, de-duplicated report — not one per audit.
Resolve any findings back toward the Step 0 decision. If `pm-product-review` isn't installed, run
whichever audit skills *are* present directly, or self-review against the policy.

---

## Step 3 — Offer the strategy / launch arc (don't auto-run it)

A validated plan is the handoff point, not the finish line. Once the plan passes review, **offer**
to continue into the strategy arc rather than producing it unprompted: product vision & strategy
(`pm-vision-strategy`), competitive analysis (`pm-competitive-analysis` — make this a *strong*
offer in a crowded market, since switching cost is a strategic question this arc owns), roadmap
(`pm-roadmap`), go-to-market (`pm-gtm-plan`), and launch experiments + analytics
(`pm-experimentation-ab`, `pm-analytics`). Naming the next arc is the service; auto-generating it
is the bandwagon.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Jump straight to a PRD when handed an idea | Frame the problem, then de-risk with discovery, *before* the spec |
| Skip discovery because the idea "obviously" has a market | Run discovery proportionate to stakes — adoption, workflow fit, switching cost, willingness to pay |
| Bury the validation test as a PRD sub-section | Foreground the riskiest-assumption test (often a concierge/pre-sell) as an explicit build gate |
| Let the spec become the whole plan | Keep the spec the *last*, proportionate rung; it carries the evidence forward |
| Treat "will they pay/switch" as a detail | In a crowded market, make switching cost the riskiest assumption and test it first |
| Prioritize a feature wish list | Prioritize against validated risk, traced to strategy, with trade-offs exposed |
| Run this orchestrator for a single named artifact | Let that skill trigger directly (explicit scope wins) |
| Auto-produce vision/competitive/roadmap/GTM | Stop at a validated plan; *offer* the strategy arc next |
| Declare done after generating | Hand to `pm-product-review` for one merged, severity-rated report |

---

## Relationship to the policy

This skill *is* the compositional-orchestration section (§9) of `docs/orchestration-policy.md` in
executable form for PM work. Its validation twin is `pm-product-review`; its UX counterpart is
`ux-design-from-scratch`. If this skill and the policy ever diverge, the policy governs — update
this skill to match it.

## Source lessons (Uxcel)

This is an orchestrator — most of its substance lives in the skills it composes (see the source
lessons in `pm-problem-statement`, `pm-discovery`, `pm-personas-jtbd`, `pm-assumption-testing`,
`pm-prioritization`, `pm-product-spec`, `pm-okrs-kpis`). The staging itself — idea → plan, with
evidence and definition before build — is grounded in:

- [Product Development Lifecycle](https://uxcel.com/lessons/product-development-lifecycle-657)
- [Product Development Stages](https://uxcel.com/lessons/product-development-stages-413)
- [Product Definition](https://uxcel.com/lessons/product-definition-570)
