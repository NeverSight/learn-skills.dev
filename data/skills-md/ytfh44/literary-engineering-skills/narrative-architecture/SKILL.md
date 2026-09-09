---
name: narrative-architecture
description: Use when a literary request asks why a paragraph or scene appears here, how events or scenes depend across a bounded window, whether a reveal is delayed or recontextualized, whether a commitment remains open, or how a local change alters later structural obligations; use for observation over a paragraph, scene, or 3–5 scene window before proposing structural revision.
license: Apache-2.0
---

# Narrative Architecture

## Use when

The question is larger than a sentence or span and smaller than a claim about
the whole novel. The user wants to inspect how a bounded sequence is arranged,
what one event makes possible for another, or what a text has promised without
assuming that every promise must be paid.

Typical requests:

- explain why this paragraph or scene belongs before another;
- distinguish story-time order from presentation order;
- inspect a delayed reveal, flashback, summary, ellipsis, or hard cut;
- trace an event dependency across two or more anchors;
- list commitments, requests, constraints, or debts that remain open in scope;
- compare what a local change does to later structural relations.

## Do not use when

Do not use this for a single-sentence diagnosis, a general plot summary, or a
request to rewrite the whole story. Do not use it to decide what a reader or
character knows; use `knowledge-boundaries`. Do not use it to map the reader's
attention, reveal, occlusion, or scale path inside a scene; use
`camera-attention-engineering`. Do not use it to perform an A/B edit; use
`counterfactual-revision`. Do not use it to choose among skills; use
`literary-style-router`.

Do not infer a global architecture when the user has not supplied a bounded
window. Do not turn a relation into a defect merely because it is unresolved,
nonlinear, ambiguous, or deliberately misleading.

## Core test

**Can I point to at least two textual anchors whose relation is being
observed, and can I separate what the text states from what I infer?**

If either answer is no, report the reading as unknown or out of scope rather
than inventing a structure.

## Scope

Work only over the user's supplied paragraph, scene, or bounded 3–5 scene
window. Name the scope before interpreting it. Preserve the distinction
between:

- story time and discourse time;
- textual evidence and analyst inference;
- an open state and a failed state;
- a deliberate break and a continuity error;
- a causal relation and a merely adjacent event.

The three projections below are report views, not a shared graph engine. Use a
plain anchor-to-anchor list when that is sufficient.

## Three observation projections

### Temporal structure

Record relations that the supplied text supports:

```text
before | after | overlap | repeat | unknown
```

Also record the presentation operation when visible:

```text
scene | summary | ellipsis | pause | analepsis | prolepsis | repeat | cut
```

Do not equate physical continuity with discourse continuity. An omitted action
may be recoverable, and a hard cut may be deliberate.

### Causal structure

Record the weakest relation supported by the evidence:

```text
enables | causes | motivates | prevents | triggers |
consequence_of | correlated_with | unknown
```

Keep agency and uncertainty visible. `unknown` is preferable to a forced clean
chain. If two readings compete, list both and identify the evidence that fails
to decide between them.

### Obligations in scope

Record only elements the text actually establishes as a commitment, request,
debt, constraint, warning, or other forward-facing condition. Use these states:

```text
open | fulfilled | failed | revised | unknown
```

An open state is a description of the supplied window, not a verdict that the
work is incomplete. A transformed, abandoned, delayed, or deliberately
unresolved element may be the intended result.

## Workflow

1. **Bound the window.** Name the paragraph, scene, or scene range and the
   question being tested.
2. **Mark anchors.** Quote or identify the smallest beats that carry the
   relevant event, state, transition, or commitment.
3. **Record explicit relations first.** Separate stated order, dependency, and
   commitment from an interpretation supplied by the reader.
4. **Add inference cautiously.** Every inferred relation receives an
   `inferred`, `contested`, or `unknown` status and a reason.
5. **Check competing readings.** Preserve ambiguity when a red herring,
   unreliable account, dream, montage, parallel thread, or genre convention
   makes more than one structure viable.
6. **Test cross-anchor relevance.** If removing or moving one anchor would not
   change the relation under discussion, the observation is probably local and
   belongs to another skill.
7. **Return observations before actions.** If an intervention is requested,
   state at most one or two falsifiable structural hypotheses. Hand the actual
   one-variable comparison to `counterfactual-revision`.

## Application scenarios

### Scene placement and compression

Ask which intermediate states the reader can reconstruct and which state must
remain on the page. Do not treat every serial action as excessive. A proposed
compression must name the lost or preserved relation.

### Delayed revelation and recontextualization

Describe which anchors are present before and after the reveal, then hand off
reader-knowledge timing to `knowledge-boundaries` and access order to
`camera-attention-engineering`. This skill observes the cross-scene dependency;
it does not decide the reveal's emotional effect.

### Causal ambiguity and agency

List the available causal readings and the evidence for each. Preserve
correlation, coincidence, and unreliable explanation as live possibilities when
the text does not settle them.

### Open commitments and parallel threads

Record which thread or commitment is advanced, complicated, intersected, or
untouched within scope. Do not demand closure, add subplots, or treat a
parallel line as wasted space without a demonstrated structural loss.

### Local change with long-range consequences

Describe the baseline relation and the relation that a proposed boundary move
would test. Do not silently change several scenes or claim a global effect from
one local edit.

## Ownership boundaries

- `knowledge-boundaries` owns facts, beliefs, knowledge timing, and disclosure
  asymmetry.
- `camera-attention-engineering` owns observer access, reveal, occlusion,
  scale, handoff, and deliberate cuts inside a perceptual path.

- `relation-scaffolding` owns sentence-level connectors and relation marking;
  this skill observes dependencies across anchors, not connector frequency.
- `counterfactual-revision` owns the controlled A/B intervention.
- `literary-strategy-controller` owns document history, saturation, marginal
  utility, vetoes, and operation sequencing.
- `literary-style-router` owns selection of the smallest skill set.

Use this skill only for the cross-anchor structural relation that remains after
those owners have been separated. If the distinction cannot be made from the
supplied evidence, preserve the overlap and say so.

## Evidence contract

Each observation must contain:

```text
scope
source_span_or_beat_anchor
projection: temporal | causal | obligation
relation_or_state
epistemic_status: explicit | inferred | contested | unknown
unresolved_questions
```

No anchor means no confident relation. No evidence-backed intervention
command is allowed. The report should make it possible for another skill or a
human to inspect the same anchors without trusting a hidden global model.

## Minimal pair

Baseline: one scene states that a character waits for a reply; the next
scene begins after an unmarked gap.
Candidate: add one sentence explaining the gap.

The comparison asks whether the added sentence changes a temporal, causal, or
obligation relation across the two anchors. It does not assume that explanation
is an improvement. Record the lost ambiguity, preserved uncertainty, or changed
commitment before suggesting any further edit.

## Counterexamples

- An intentional hard cut that creates temporal shock.
- A dream or montage whose order is not literal story time.
- A red herring that is supposed to remain unresolved or be reinterpreted.
- An unreliable narrator whose causal account cannot be confirmed yet.
- A static inventory whose lack of movement is the scene's purpose.
- A promise that decays, transforms, or is deliberately abandoned.
- Parallel threads that are meant to remain separate.
- An open ending that should not be repaired into closure.

## Rule strength

**Observation protocol, not a quality grade.** Prefer explicit evidence, bounded
claims, competing readings, and reversible hypotheses. There are no lexical
bans, universal payoff requirements, or automatic structural rewrites. The
correct output may be a small set of unresolved relations.

## Return shape

Return:

1. **Scope** — the supplied window and the structural question.
2. **Anchors** — quoted beats or stable identifiers.
3. **Temporal observations** — order and presentation operations.
4. **Causal observations** — supported dependencies and unknowns.
5. **Obligation observations** — commitments and in-scope states.
6. **Competing readings** — where evidence does not decide.
7. **Structural hypothesis** — optional, falsifiable, and limited to the next
   controlled experiment.
8. **Handoff** — name `knowledge-boundaries`, `camera-attention-engineering`,
   or `counterfactual-revision` when the question belongs there.

## Read next

- [Knowledge boundaries](../knowledge-boundaries/SKILL.md)
- [Camera and attention](../camera-attention-engineering/SKILL.md)
- [Counterfactual revision](../counterfactual-revision/SKILL.md)
- [Literary style router](../literary-style-router/SKILL.md)
