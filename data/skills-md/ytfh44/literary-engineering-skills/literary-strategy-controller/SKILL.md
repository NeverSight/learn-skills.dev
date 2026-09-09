---
name: literary-strategy-controller
description: Use when a revision plan is being executed over a longer passage and several local fixes are already in play — track the document state, compute marginal utility before each next operation, and avoid turning six individually correct local choices into one house style; decides motif vs. template (repetition must change the work state); use for state-dependent adaptation instead of randomization.
license: Apache-2.0
---

# Literary Strategy Controller

## Use when

More than one or two local fixes are being applied to the same document.
Each fix may be correct in isolation; the sequence is the risk. This skill
keeps the sequence honest by tracking what the document already does.

## Do not use when

Do not use this for a single-sentence question; it is a full-document
controller. Do not use it to randomize ("sometimes do the opposite to mix
it up") — randomness is a stable distribution in disguise. Do not use it to
enforce quotas ("at most three metaphors per page"); quotas are proxies
for state that should be measured, not preset.

## Core test

**A local optimum repeated six times is a house style.**

Every operation in this pack is locally correct under some condition. The
condition includes the document's history: what has already been done, how
densely, and with what neighbors. The controller asks, before each
operation:

> Given what this document already does, is this operation still the
> marginal best move?

## Document state

Maintain a running state list while revising (update it per operation):

- **relation density** — explicit edges per unit text;
- **direct naming density** — how often states/meanings are named outright;
- **eventification density** — how often properties become event
  consequences;
- **explicit emotion density** — direct emotion labels;
- **metaphor function distribution** — what the metaphors are *doing*
  (voice, motif, semantic), not how many there are;
- **narrator intervention level** — scene / near-scene / summary / verdict;
- **attention continuity** — continuous vs. hard-cut vs. withheld-anchor;
- **hard-cut frequency** — deliberate discontinuities per unit;
- **closure mode** — open vs. settled endings;
- **recent operation history** — the last N operations, in order.

The state is descriptive, not a scoreboard. A high value is a fact about
the document, never automatically a defect.

## Marginal utility

Before each operation, estimate:

```text
marginal_gain =
  local_gain
  - saturation            (this technique already used heavily nearby)
  - redundant_neighbor_similarity  (same operation within a small window)
  + contrast_value        (the change breaks a monotone run on purpose)
  + motif_payoff          (the operation feeds a recurring element)
  + long_range_structural_payoff  (the operation sets up a later payoff)
```

Use the formula as a checklist, not arithmetic: name each term explicitly,
and record which term decided the call. If saturation is the only term
that changed between two candidate operations, the decision is
state-driven — exactly what this skill exists to make possible.

## State-dependent adaptation

Example:

> 局部上："他很紧张"确实可以换成具体动作。
>
> 全文上：过去 700 字已经有六次心理状态都通过具体动作表达。
>
> 因此：这一次保留直接命名，反而更有边际价值。

This is not a coin flip. The system knows what it has already done. The
same technique is not punished on the second occurrence — repetition that
changes the work state is motif, and motif has its own payoff term. The
decision rule is:

**Repetition must change the work state.** If the next occurrence adds
force, scale, contrast, or structure, it is a motif and may be chosen
freely. If it merely repeats, saturation applies.

## Workflow

1. Record the document state before starting (baseline).
2. Before each planned operation, name its local_gain and its cost terms
   (saturation, neighbor similarity).
3. Decide by marginal utility, not by the skill's local rule alone.
4. Update the state list after each applied operation.
5. When two operations tie, prefer the one whose contrast_value or
   motif_payoff is higher — never decide by "we haven't done this in a
   while."
6. At the end, report the state deltas and the operations the controller
   vetoed or redirected, with reasons.

## Minimal pair

Passage with six concrete-evidence renderings already in 700 characters:

> 他紧张地搓了搓手。她不安地挪了挪椅子。他焦虑地看了一眼手机。
>
> 他紧张地搓了搓手。她挪了挪椅子。他看了一眼手机。
>
> 他搓了搓手。她挪了挪椅子。他看了一眼手机。他很紧张，但不想让她
> 看出来。

The first run is the local rule applied three times — saturation has
already set in. The third version keeps one direct label because the state
(six eventified emotions) makes it the marginal best move: the label now
carries contrast and changes the work state.

## Counterexamples

- A genuinely repetitive style can be the work's design (litany,
  incantation, a character's monotony); the controller reports the state,
  and the design may choose saturation on purpose.
- A motif can appear many times when each occurrence changes the work
  state; the controller's job is to distinguish motif from template, not
  to count occurrences.
- A short passage (under ~500 characters) usually has no meaningful
  state history; do not run the controller where there is nothing to
  control.

## Rule strength

**Method — state tracking, no quotas.** No preset thresholds, no
"maximum N per passage" rules, no randomization. The reliable operations
are state maintenance, marginal-utility naming, and veto reporting. The
controller never grades prose; it only reports what the document already
does and which move the state favors next.

## Read next

- [state-checklist.md](references/state-checklist.md) for the state fields
  and update rules.
- See `corpus-convergence-audit` for measuring an existing corpus; this
  skill is the forward-looking side of the same discipline.

## Return shape

Return **baseline state -> candidate operation -> marginal terms ->
decision -> state delta**. When vetoing, give the term that decided the
veto (usually saturation or redundant-neighbor similarity). When
redirecting (e.g., direct label instead of another evidence rendering),
state the contrast or motif payoff that justified it.
