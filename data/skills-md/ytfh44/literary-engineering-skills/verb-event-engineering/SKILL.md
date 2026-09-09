---
name: verb-event-engineering
description: Use when a fiction sentence has weak, decorative, over-rare, morally overcommitted, or role-confusing verbs; when changing a predicate may alter agency, responsibility, causation, control, intention, duration, path, result, or the noun's role in the event; use when an event needs decomposition before any verb is replaced.
license: Apache-2.0
---

# Verb Event Engineering

## Use when

The verb is not merely naming an action; it is deciding what kind of event
the nouns inhabit. Before any replacement, decompose what the current
predicate commits to.

## Do not use when

Do not search for a "stronger verb" when the real failure is viewpoint
order, metaphor, or dialogue register. Do not replace a common exact verb
with a rare near-synonym for texture. Do not run verb upgrades as a batch
operation across a passage.

## Core test

**Before replacing a verb, ask what the replacement judges each noun to
be.**

A predicate can turn a noun into actor, patient, cause, experiencer,
instrument, path, or result without changing the nouns themselves.

## The "strong verb" danger

```text
走 -> 踱
看 -> 凝视
说 -> 低吼
```

is not a natural upgrade path. Each step imports commitments — manner,
duration, attitude, emotion, control — that may not be facts of the scene.
If the scene has not established that the walk is deliberate, the stare is
sustained, or the speech is animal, the "stronger" verb adds event promises
the story must now pay. Replace only when the commitment is wanted, and
prefer the least-committing verb that carries the needed distinction.

## Workflow

1. Write the event in plain terms: participants, change, result.
2. Mark what the current verb commits to: agency, intention, control, path,
   duration, result, responsibility.
3. Identify the missing distinction.
4. Test one replacement that changes that distinction and nothing else.
5. Reject replacements whose only gain is rarity, intensity, or "literary"
   color.
6. Read the noun roles again. If responsibility or empathy moved, decide
   whether that move is wanted.

## Working vocabulary

Use standard terms when useful: **valency**, **semantic role**,
**causation**, **result state**, **coercion**. A local term such as "半格合"
may be used only as a working metaphor for how Chinese predicates softly
assign event roles; do not present it as an established grammatical
category.

## Minimal pair

> 逸马杀犬。
>
> 奔马毙犬。

`杀` first asks for a killer and a victim. `毙` foregrounds the death
result. The lexical swap shifts moral/event framing even before any
adjective appears.

Upgrade trap:

> 他说："不行。"
>
> 他低吼："不行。"

The second is not better unless the scene has established the voice quality.
If it has not, the replacement imported an attitude the narrative must now
justify.

## Counterexamples

- `走` -> `踱` is not automatically better. If gait does not matter, `走`
  may be exact and cheaper.
- `看` can be stronger than `凝视` when the scene needs an unmarked
  perception event rather than prolonged attention.
- A genuinely animal growl is `低吼`; the commitment is the scene's fact.

## Rule strength

**Event decomposition.** No universal preference for short or rare verbs,
no "verb energy" metric, no upgrade lists. The reliable operation is
decomposition: enumerate commitments, compare role assignments, choose the
least false / most useful commitment. Replacement tests are one-variable
interventions (see `counterfactual-revision`).

## Read next

- [valency-and-roles.md](references/valency-and-roles.md) for participant
  structure.
- [coercion-and-result.md](references/coercion-and-result.md) for productive
  category crossing and result states.
- [responsibility-and-agency.md](references/responsibility-and-agency.md)
  when verb choice changes blame, intention, or control.
- [verb-ablation.md](references/verb-ablation.md) for controlled replacement
  tests.

## Return shape

Give **current event commitment -> proposed change -> role shift -> reason**.
When revising, offer no more than three verbs unless the user asks for a
lexical search.
