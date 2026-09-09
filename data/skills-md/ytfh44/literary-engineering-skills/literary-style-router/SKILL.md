---
name: literary-style-router
description: Use when a fiction-writing or revision request is broad, vague, or described only as “AI-like,” “flat,” “wooden,” “purple,” “not literary,” or “make it better,” and the actual failure mechanism has not yet been identified; routes in two stages — first the carrying layer, then the mechanism within it.
license: Apache-2.0
---

# Literary Style Router

## Use when

The complaint names a symptom, not a mechanism. Diagnose first; then load
the smallest skill set that can act on the cause.

## Do not use when

Skip the router when the user already names a narrow operation: verb roles,
metaphor ablation, a particle swap, dialogue register, clause pressure, or
another domain covered by a dedicated skill.

## Core test

**Route by what the sentence is doing wrong, not by what the user calls the
feeling.**

“AI-like,” “flat,” and “too literary” can each arise from several unrelated
mechanisms. Treat them as search prompts, not diagnoses.

## Two-stage workflow

**Stage 1 — find the layer.** Ask where the failure lives:

| Question | Layer |
| --- | --- |
| Are edges being stated that event order could carry? | relation |
| Are properties being assigned that do no work? | property |
| Is the referent being reclassified by naming? | naming |
| Is a comparison spending words for nothing? | figurative |
| Is a predicate overcommitting or misassigning roles? | verb/event |
| Does a particle/adverb change the stance? | adverb/particle |
| Is the problem in what the reader sees, when, and from where? | discourse |
| Is the problem in who speaks, knows, or wants? | character |

**Stage 2 — find the mechanism within the layer.** Examples:

- “不是A而是B太多” -> relation layer -> concept-link overmarking
  (`relation-scaffolding`)
- “所有东西都用稀有形容词” -> property layer -> affective/discriminative
  overload (`property-and-adjective-engineering`)
- “人物一直叫父亲‘那个男人’” -> naming layer -> relational framing
  (`naming-and-address-engineering`)
- “风追着他为什么成立” -> verb/event layer -> agentive coercion
  (`predicate-licensing-and-personification`)
- “又/才/竟然哪个对” -> adverb/particle layer -> expectation/threshold
  (`adverb-particle-viewpoint-engineering`)

## Workflow

1. **Locate the failure.** Quote the smallest span that creates the
   complaint.
2. **Name the layer** (Stage 1). Prefer a layer diagnosis over an
   adjective.
3. **Name one mechanism** (Stage 2). Event, viewpoint, relation, voice,
   metaphor, motive, or pressure diagnosis — never “it needs more
   imagery.”
4. **Choose one primary skill.** Add at most two secondary skills when they
   answer separate questions.
5. **Order the passes.** Repair structure before ornament. Typical order:
   event/viewpoint -> evidence/voice -> metaphor/rhythm.
6. **Check the document state.** If several local fixes are already in
   play, consult `literary-strategy-controller` before adding another:
   six correct local choices may already be one house style.
7. **Recheck by intervention.** If the user asks for revision or
   validation, use `counterfactual-revision` or `literary-evals` after the
   primary fix.

## Routing map

| Symptom in the text | Primary destination |
| --- | --- |
| staff-report, therapy-summary, retrospective voice | `narrator-intervention-abstraction-control` |
| too many explicit causal/concessive/relationship links | `relation-scaffolding` |
| image says nothing beyond “dark/cold/angry/sad” | `metaphor-audit` |
| wrong agency, weak result, decorative synonym swap | `verb-event-engineering` |
| a noun doing a predicate its class cannot | `predicate-licensing-and-personification` |
| adjectives pile up without a job | `property-and-adjective-engineering` |
| naming shifts carry the frame | `naming-and-address-engineering` |
| a particle/adverb changes the stance | `adverb-particle-viewpoint-engineering` |
| scene is seen in a poor order | `camera-attention-engineering` |
| emotion label replaces evidence | `narrator-intervention-abstraction-control` |
| character suddenly speaks in the author's register | `dialogue-voice` |
| “contradictory traits” feel pasted together | `character-motive` |
| clause length changes but pressure does not | `sentence-pressure` |
| characters act on different knowledge | `knowledge-boundaries` |
| names encode the relationship arc | `social-naming-relation-maps` |
| source-language packaging itself matters | one language-derived engineering skill |

For close collisions, read [routing-matrix.md](references/routing-matrix.md).
For pass order, read [audit-order.md](references/audit-order.md).

## Hard rules

- Do not activate every plausible skill “for completeness.” Context is a
  budget.
- Do not rewrite while the diagnosis is still “it feels off.”
- Do not route “Chinese prose” automatically to
  `chinese-derived-event-geometry`; language is context, not a failure.
- Do not route “make it vivid” automatically to metaphor. The missing
  mechanism may be a verb or camera move.
- Do not route “这段太平了” to metaphor generation. Audit first; the
  verdict may be “no metaphor here” (`metaphor-audit`).
- Do not let the router become a prose critic. Its product is a route.

## Minimal pair

User: “这句很平，帮我修。”

- Weak route: `metaphor-audit` because “flat” sounds like an image problem.
- Strong route: inspect first. If the sentence says “他很紧张,” choose
  `narrator-intervention-abstraction-control`; if it says “他走进房间,”
  but agency/path matter, choose `verb-event-engineering`.

Only the diagnosis changed.

## Counterexamples

- “比较‘杀’和‘毙’怎样改变施受关系。” -> go straight to
  `verb-event-engineering`.
- “把这段法语里的 mouvement 路径和 manière 拆开分析。” -> go straight to
  `french-derived-motion-packaging`.
- “帮我决定又还是才。” -> go straight to
  `adverb-particle-viewpoint-engineering`.

## Rule strength

**Routing protocol.** The router's product is a route, not a verdict: it
activates the smallest skill set and never rewrites prose itself. Its
reliability is measured by trigger accuracy — should-trigger prompts route
to the mechanism, near-misses do not — executed as a trigger battery (see
`literary-evals` and `tests/run_trigger_battery.py`).

## Return shape

When only routing is requested, return:

1. **Layer** — one word (relation/property/naming/figurative/verb-event/
   particle-viewpoint/discourse/character).
2. **Primary mechanism** — one sentence.
3. **Evidence** — the smallest span.
4. **Primary skill** — one name.
5. **Optional secondary skill(s)** — zero to two, each with one reason.

Do not add a full rewrite unless the user asks for one.
