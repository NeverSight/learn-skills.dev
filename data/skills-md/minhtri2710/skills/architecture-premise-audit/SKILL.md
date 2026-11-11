---
name: architecture-premise-audit
description: Audit a whole project for a possibly wrong system archetype by deriving expected product capabilities before trusting repository vocabulary. Use only for an explicitly requested broad premise audit, not ordinary architecture review or one named design concern.
---

# Architecture Premise Audit

Determine whether the project is built around the right system archetype, not
merely whether its current modules are internally consistent. Audit read-only
unless the user separately requests changes.

## Boundaries

- Work at the whole-project or named broad-system boundary requested by the user.
- Derive the expected product model before treating repository terminology,
  architecture docs, tests, or benchmarks as authoritative.
- Treat passing proof as evidence about an implementation, not proof that the
  mechanism should exist.
- Complexity is a finding only when it lacks a required product need, owner,
  lifecycle, consumer, scaling contract, or failure contract.
- Do not turn a broad audit into implementation, issue creation, or a second
  review workflow.
- Ask only when one missing fact would reverse the verdict and cannot be bounded
  with an explicit assumption.

For realtime multiplayer, MMO, or another system with a suspected structural
misfit, read
[references/structural-antipatterns.md](references/structural-antipatterns.md)
before constructing the expected capability map. Use its patterns as search
lenses, not as a checklist that every design must satisfy.

## Audit Slice

Judge work by product responsibility rather than repository module. Each audit
slice should identify:

- job to be done and production consumer;
- authoritative owner, state, and lifecycle;
- inputs, outputs, and trust boundaries;
- scaling or adversarial variable;
- failure, overload, and backpressure behavior;
- reusable-platform versus application responsibility.

A slice may cross modules, and one module may contain several slices.

## Procedure

1. **Set the claim.** State the product category, requested boundary, expected
   outcome, material assumptions, and completion rule.
2. **Build the expected atlas.** From product needs and established domain
   mechanisms, list the responsibilities that should exist, likely owners,
   scaling variables, and work that must be bounded or isolated.
3. **Build the observed map, and record it as the coverage ledger.** Trace
   production entry points, authoritative state, durable effects, expensive
   operations, queues, schedulers, external outputs, deployment boundaries, and
   cited proof. Record one ledger row for each item as you discover it: the item,
   which of those nine categories it belongs to, and where it is represented.
   Record a category you traced and found empty as a row stating that derived
   absence. This ledger is the artifact step 6 stops on and output item 2
   reports. A later step that discovers an item this trace missed returns here to
   record it and re-runs the steps after; no step appends a row while checking
   coverage. Do not copy the repository's decomposition without testing it.
4. **Form the slices, then compare every one of them.** Group the ledger rows
   step 3 recorded into audit slices by product responsibility, so that each
   slice identifies everything the Audit Slice section lists and every row
   belongs to at least one slice; a row that fits no slice is a slice of its own
   until a comparison shows otherwise. Then ask of each slice what demonstrated
   requirement forces each mechanism, whether cost follows useful work, whether
   normal and exceptional paths are reversed, and whether removing or relocating
   the mechanism loses an established requirement. A comparison becomes a serious
   candidate when it names a mechanism whose forcing requirement you could not
   find in production, or whose cost does not follow useful work; record which of
   the two promoted it. A comparison you cannot settle either way is a candidate,
   not a dismissal.
5. **Deep-check serious candidates.** For each one, trace real callers and
   consumers, name the hidden premise the mechanism would have to be true for and
   the ongoing tax the product pays for it, name the exact amplification route,
   construct the cleaner counterfactual, identify machinery that disappears, give
   the strongest counterargument, and state evidence that would falsify the
   finding.
6. **Check coverage.** Stop only when every row step 3 recorded in the coverage
   ledger — in all nine of its categories, not a subset — has been carried into a
   comparison at step 4 or 5, or carries a stated exclusion with the rule that
   excludes it. Judge each row by the category step 3 gave it. An empty ledger
   does not satisfy this gate: it means step 3 traced nothing, and the audit
   returns there rather than terminating.
7. **Classify and decide.** Once the coverage gate passes, classify every
   candidate step 4 promoted as exactly one of these six literals, and no other
   label: `ARCHITECTURE_DEFECT`, `OWNER_DEFECT`, `IMPLEMENTATION_DRIFT`,
   `JUSTIFIED_DIVERGENCE`, `QUARANTINED_SCAFFOLD`, `INSUFFICIENT_EVIDENCE`. Then
   rank the findings by the cost of leaving each in place, rank the decisions they
   force, most costly to reverse first, and for each slice write the fitness
   scenario its scaling or adversarial variable makes realistic: what that variable
   does next, and which classified findings decide whether the current architecture
   holds under it. Do not report generic improvements.

## Verdict And Output

Lead with one verdict, composed from the step 7 classifications by the first
condition below that holds, read top to bottom. The step 6 coverage gate is the
precondition: if it never passed, the verdict is `INSUFFICIENT_EVIDENCE` and no
other, whatever was classified.

- `STOP_AND_REDIRECT` — at least one `ARCHITECTURE_DEFECT` whose step 5
  counterfactual removes or relocates the authoritative owner or state of a slice.
- `REDIRECT_RECOMMENDED` — at least one `ARCHITECTURE_DEFECT`, and every such
  counterfactual leaves each slice's authoritative owner and state in place.
- `REPAIR_FIRST` — no `ARCHITECTURE_DEFECT`, and at least one `OWNER_DEFECT` or
  `IMPLEMENTATION_DRIFT`.
- `INSUFFICIENT_EVIDENCE` — none of the above, and at least one candidate
  classified `INSUFFICIENT_EVIDENCE`. An unsettled candidate outranks a sound
  foundation: the audit never reports one while holding the other.
- `KEEP_FOUNDATION` — none of the above, so step 4 promoted no candidate, or every
  promoted candidate is `JUSTIFIED_DIVERGENCE` or `QUARANTINED_SCAFFOLD`.

`INSUFFICIENT_EVIDENCE` is the one literal in both vocabularies, and the two roles
are distinguished by position, not by name: as a step 7 classification it says one
candidate could not be settled, as a verdict it says the audit as a whole could not
be. The fourth condition above is the whole relationship between them.

Then provide only the material sections needed to support it:

1. expected-versus-observed map;
2. the coverage ledger built at step 3, compact, with its exclusions;
3. ranked findings with production evidence, hidden premise, tax, and
   amplification route;
4. counterfactual architecture and machinery removed or relocated;
5. counterargument and falsifier for each finding step 5 deep-checked;
6. the candidates step 7 classified `JUSTIFIED_DIVERGENCE` or
   `QUARANTINED_SCAFFOLD`, with the reason each is not a defect;
7. the prioritized decisions and the per-slice fitness scenarios from step 7.

Make the best evidence-supported judgment available. Expose assumptions, but do
not end with an unranked option menu or an interview questionnaire.
