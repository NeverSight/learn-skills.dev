---
name: acceptance-gate
description: The standard a computed result must meet before it may be called done. Use whenever an agent claims an integral is solved, a fit has closed, a formula is identified, or any quantitative answer is ready — the claim is not done until it passes this gate.
---

# acceptance-gate — what "done" means

**A result is done when it has survived a check that could have failed, run by
a route that could not have known the answer. It is never done merely because
the computation that produced it finished.**

Why the gate exists: computation produces confident wrong answers at every
stage, and none of them announce themselves. A fit converges to the wrong
basin and reports small residuals. An integer-relation search "recognizes"
numerical noise as a famous constant, because search enough constants and
something always matches a short prefix. Two evaluators built on the same
series expansion agree to great depth on the same wrong value. The agent that
produced the answer — human or model — is the least qualified judge of it,
because everything that produced the answer also produces reasons to believe
it. So "done" is defined externally: agreement with an independent route, at
points that entered no fit, to more digits than the fit could enforce,
deepening when precision is raised, measured by machinery that has
demonstrably failed on a wrong answer. Each clause of that sentence is there
because its absence has, at some point, let a wrong result through.

The bar used for the BootLoops loop-integral results (bootloops.ai): at least
thirty genuine held-back digits, two-precision stable, against an oracle that never fed the fit. Adopt
a bar of that order for anything new. Scale the digit count to the problem;
never scale away the structure.

## The procedure

Run the steps in order. The order is itself part of the discipline: the check
is designed before the answer exists, because a check designed after the
answer exists is chosen — consciously or not — to pass.

**0. Declare the gate before fitting.** Before any fit, search, or model
choice, write down: which evaluation points are reserved, what the
independent route will be, what digit count will count as passing, and what
the controls are. A gate written after the candidate exists inherits the
candidate's blind spots.

**1. Reserve never-fit points.** Choose evaluation points, record them, and
exclude them from every fit, every tuning decision, and every basis
selection — not only the final fit but every exploratory run that shaped the
method. Agreement at fitted points measures interpolation: a fit with enough
parameters reproduces its own inputs exactly, and agreement there means
nothing.

**2. Audit the independent route.** The check values must come from a route
that shares no code, no series representation, and no fitted input with the
derivation. Numerically integrating the original definition, when the
candidate came from a fitted ansatz, is independent; a second wrapper around
the same expansion is not. An oracle whose values entered the fit — even
once, even only to pick a tolerance — is disqualified from certifying (see
independence-bookkeeping). Where full disjointness is impossible, record
exactly what is shared and treat the check as weakened by that much.

**3. Count digits; do not describe them.** Evaluate both sides at the
reserved points and count the digits that genuinely agree. The count must
exceed, by a wide margin, anything the fit's free parameters could have
absorbed. The unit of evidence is a number — "34 digits at each of three
reserved points" — never "excellent agreement".

**4. Rerun at raised precision.** Double the working precision and repeat. A
true identity deepens: the count of agreeing digits grows with the precision.
Agreement pinned at the same depth regardless of working precision is a
truncated intermediate shared by both sides, a coincidence at the resolution
of the search, or a bug. It is never a confirmation.

**5. Run the controls, positive and negative.** Positive: run the identical
gate on a case where the answer is independently known, and confirm it
passes. Negative: perturb the candidate — flip the sign of one term, alter
the last fitted coefficient in its final digit — and confirm the gate fails,
loudly, at the digit where it should. A gate that has never failed anything
certifies nothing: every clause of it might be broken and you would see only
passes.

**6. Leave-one-out, where a fit determined the answer.** For each anchor
point that entered the fit: refit without it, evaluate the refit at the
excluded point, and demand agreement at full depth. An identity survives
every exclusion; an interpolation collapses at exactly the excluded point.
This is the cheapest way to distinguish "found the formula" from "drew a
curve through the data".

**7. Package a standalone evaluator.** The claim ships with a script that
rebuilds the result from the exact data included with it and re-measures this
gate at arbitrary requested precision — no hidden grids, no finite-precision
constants baked in, no state that lived only in the session that produced the
claim. If a stranger cannot rerun the gate, the gate ran once and its
evidence is already decaying.

**8. Report the true verdict.** CLOSED means every part above passed and the
counts are written down. Anything less is OPEN, reported with what was
established and what remains. An honest OPEN is a result; a false CLOSED is
damage, because later work builds on it and the cost of the unwinding grows
with every week it stands.

## Failure modes the gate exists to catch

Each of these is a class observed repeatedly in practice, from agents and
from people. The vignette states the mechanism; learn the shape, not the
example.

- **Satisficing.** The first plausible answer is declared final: a handful of
  digits of numerical noise matches a known constant at the resolution of the
  search, and the search stops. The match was guaranteed by the size of the
  ring searched. The digit bar plus two-precision stability is the cure — a
  coincidence does not deepen.

- **Certifying at fitted points.** The check runs at points the fit saw,
  agreement is perfect, and the perfection is reported as confirmation. It
  confirms only that the fit can reproduce its inputs. Reserved points, set
  aside before fitting, no exceptions.

- **Oracle contamination.** Reference values get used casually during
  development — to pick a tolerance, choose a basis, decide when to stop —
  and are later reused to certify. The gate then verifies that the method
  remembers what it was shown. Track which values touched anything; certify
  only from the disjoint set.

- **False independence through a shared representation.** Two separately
  written evaluators, both resting on the same series expansion or the same
  underlying library, agree to any depth you like — including on a wrong value,
  when the shared layer carries the bug. Their agreement measures the bug's
  consistency. Audit lineage; prefer a route different in kind, not merely in
  authorship.

- **Precision-pinned agreement.** The digit count refuses to grow when
  working precision is raised: both sides share a truncated constant, a fixed
  grid, or a low-precision intermediate. This is the single most diagnostic
  symptom the gate produces. A pinned count is a failure, never "close
  enough".

- **The gate that cannot fail.** The comparison harness itself is broken
  open: a tolerance wide enough to pass anything, a value compared against
  itself through an aliased variable, formatted output string-compared so
  both sides truncate identically, an assertion inside a branch that never
  executes. Every pass from such a gate is vacuous. The negative control is
  the only way to know a gate can fire: you have watched it fire.

- **Threshold drift.** The tolerance is widened, once per awkward case, until
  the candidate passes. The finished gate is then a description of the
  candidate rather than a test of it, and a real error of the same size sails
  through. Thresholds are fixed at step 0 and never touched after the
  candidate exists; a candidate that needs the threshold moved has failed.

- **Adjectives in place of counts.** "Essentially exact", "matches
  beautifully", "agrees to high precision". Every one of these has been used
  to describe agreement that fell apart under an actual digit count. Demand
  the number, the precision it was measured at, and whether the point was
  reserved.

- **Self-graded confidence.** The producing agent's stated confidence offered
  as evidence. Confidence is an output of the same process being audited; it
  tracks fluency, not correctness. The gate is the evidence; there is no
  other kind.

- **Partials rounded up to done.** "Verified" covering nine of ten cases with
  the tenth pending; "closed modulo one term"; a comparison run at lower
  precision than the claim states. The verdict vocabulary is the cure: CLOSED
  has a definition, and the definition is the full gate.

- **The unconditional success line.** A driver prints its PASS banner outside
  the conditional that runs the comparison, or after a caught exception, so a
  run that compared nothing reports success. The verdict line must be printed
  by the comparison itself, from the measured counts — and the negative
  control catches this class too, because a broken driver passes the
  perturbed candidate.

## Two micro-examples

*A fitted closed form.* A candidate formula was fit from evaluations at a
dozen points. The gate: three further points reserved before fitting; the
original definition integrated numerically at those points by a method
sharing nothing with the ansatz; both sides evaluated at two working
precisions and the agreement counted, with the deepening confirmed; one sign
in the candidate flipped and the gate watched to fail at the first affected
digit; each of the twelve anchors dropped in turn and the refit checked at
the dropped point. Only after all of that is the formula an identity rather
than a fit.

*A recognized constant.* A computed number is matched against a declared ring
of constants. The gate: the match must hold to far more digits than the
search consumed; the digit count must grow when the value is recomputed at
higher precision; and the same search, run on noise of the same length, must
come back empty. A search that also identifies noise identifies nothing.

## Checklist before saying "done"

- [ ] Gate declared — reserved points, route, digit bar, controls — before the fit ran.
- [ ] Check route shares no code, no representation, no fitted input with the derivation; any shared remainder is written down.
- [ ] Digit count at reserved points measured and recorded, not adjectivized.
- [ ] Rerun at raised precision; the count deepened.
- [ ] Positive control passed; negative control failed, visibly, at the expected digit.
- [ ] Leave-one-out survived, if a fit determined the answer.
- [ ] Standalone evaluator included: exact data, arbitrary precision, re-measures the gate.
- [ ] Verdict is CLOSED only if every box above is checked; otherwise OPEN, with what remains stated.

**Sources and acknowledgments.** None of the ideas here is new; what is ours is
their assembly into one gate for agent-produced numbers. Declaring the check
before seeing the answer is blind analysis as particle physics practices it
(Klein and Roodman, Annu. Rev. Nucl. Part. Sci. 55 (2005) 141; MacCoun and
Perlmutter, Nature 526 (2015) 187) and preregistration as Nosek, Ebersole,
DeHaven and Mellor argue for it (PNAS 115 (2018) 2600); reserved points and
leave-one-out are Stone's cross-validatory assessment (J. R. Stat. Soc. B 36
(1974) 111); the warning that separately written routes fail together restates
Knight and Leveson's multiversion experiment (IEEE Trans. Softw. Eng. SE-12
(1986) 96).
