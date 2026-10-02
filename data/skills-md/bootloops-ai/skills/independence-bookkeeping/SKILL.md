---
name: independence-bookkeeping
description: Provenance rules that keep checks independent. Use when setting up any comparison, oracle, or reference value — and whenever tempted to certify a result with machinery that helped produce it.
---

# independence-bookkeeping — keeping the second route honest

**THE LAW: independence is an auditable property of records, never an
assumption. Two routes are independent when you can produce the trail showing
what each one depends on — code, inputs, tuning history — and the trails do
not meet at any layer where the feared error could live. If you cannot produce
the trail, you do not have independence; you have a feeling, and correlated
routes agree wrongly with exactly the same warm feeling as independent ones.**

The strongest evidence a computed result can carry is agreement with a second
route that could not have failed the same way. The entire content of that
check is the "could not" — and the "could not" is a fact about records, not
about intentions. Nobody sets out to build a circular check. Independence
decays silently, through ordinary tidy-minded acts: a stale reference gets
"refreshed" with the current code; two evaluators quietly converge on the
same library; an oracle's values leak into the tuning of the thing the oracle
later certifies. None of these announce themselves, and every one of them
leaves the comparison script printing PASS. The only defense is bookkeeping
kept from the start, because independence lost cannot be reconstructed
afterward — once a value has touched a fit, no amount of later diligence
untouches it.

## The one-way contamination rule

**An oracle that fed a fit may never certify the result.** Contamination is
one-way and permanent. The moment a reference value influences any choice —
a fitted parameter, a model form, a tolerance, a stopping decision, even
which of several candidates you kept — that value belongs to the production
side of the ledger forever. Certification draws only from the disjoint set:
values the fitting process never saw and could not have seen.

This is stricter than it first looks. Influence includes the soft channels:
you glanced at the reference while debugging and "fixed" the code until it
agreed; you used it to decide how many terms were enough; you discarded a run
because it disagreed with it. All of these are fits in everything but name.
The test is counterfactual: **if this reference had been different, could
anything about the result have come out different?** If yes, it fed the fit.

## The ledger — what to write down and when

Keep provenance as an append-only record, written at the moment of creation,
not reconstructed at certification time. Memory of provenance is worthless;
the whole point is that six weeks later nobody remembers which script
produced the number.

**1. A birth record for every reference value.** Generator (program plus
version or commit), inputs and settings, working precision, the estimated
accuracy *and where that estimate comes from* (internal convergence, an
error bound, agreement with something else — name it), and the date. A
reference without a recorded accuracy cannot support a digit claim: a
comparison is only as good as the weaker side, and an undocumented reference
has no known strength. Comparisons have stalled at exactly the digit count
of a reference nobody recorded — the agreement was real, and every claimed
digit past it was manufactured.

**2. A contact log for every oracle.** Each time a value enters a fit,
a tuning decision, a model selection, or a debugging session, append the
event. The log is append-only; entries are never removed, because the rule
above is one-way. Certification of claim C requires a reference whose
contact log contains neither C nor anything C was built on.

**3. A lineage audit for any claimed "two independent routes."** Walk each
route's dependency stack down to the libraries, the tabulated inputs, and
the constants. Two programs in different languages that call the same
special-function library share that library's defects; two derivations that
read the same published table share its typos. Shared hardware and compilers
rarely matter; shared mathematics and shared data almost always do. Write
down the *deepest shared layer* and then argue, in writing, that the failure
you are guarding against cannot live there. "Fully disjoint" is often
impossible — that is fine; undocumented sharing is what kills you, not
sharing itself.

**4. One deliberately different engine.** Keep an evaluator around precisely
because it shares nothing with the rest of your stack — different algorithm,
different language, different author if you can get one. It will be slower.
Its value is not speed; its value is that its errors are uncorrelated with
everyone else's, which makes its agreement worth more per digit than any
in-family check.

**5. The comparison itself is code — test it before believing it.** Before
any pass counts as evidence, feed the comparator a deliberately mismatched
pair and watch it fail. A comparator that has never been seen to fail proves
nothing: loose tolerances, a wrong column, a string comparison of truncated
prints — all of these return agreement on everything, forever, and the
output looks identical to a real pass. Also write down, *before* running the
real comparison, what outcome would count as failure. A failure criterion
chosen after seeing the numbers is a fit.

**6. Close the loop in the record.** When a comparison certifies a claim,
the certificate cites the reference's birth record; the reference's contact
log gains the claim. The reference is now burned for anything built on top
of that claim. This is the price of using it, and the ledger is how you know
the price was paid.

## Failure-mode catalogue

The classes this discipline exists to catch. Every one of them prints PASS.

- **The shared-library twins.** Two "independent" implementations both call
  the same underlying expansion; a defect there makes them agree, wrongly,
  to full precision — the check measures the library's self-consistency.
- **The regenerated reference.** A stored reference goes stale or missing
  and someone helpfully re-derives it with the current code; from that day
  the check compares the program with itself and can never fail again.
- **Circular calibration.** Route A is tuned until it matches route B; route
  B is later "validated" by its agreement with route A. Each certificate
  cites the other; nothing external anchors either one.
- **The leaky oracle.** Reference values were used to choose among candidate
  models — keep the form that matches — and then the same references certify
  the chosen model; the certificate measures the selection, not the truth.
- **The undocumented-precision stall.** The comparison "confirms to many
  digits", but the reference was only ever good to fewer, a fact recorded
  nowhere; every digit past the reference's true accuracy is fiction.
- **Contamination one step removed.** The raw values are properly held out,
  but the "independent" check compares residuals computed with the fitted
  parameters — the held-out quantity is a function of the fit.
- **The comparator that cannot fail.** Tolerance too loose, wrong field
  compared, truncated strings matched — the harness agrees with anything,
  and nobody ever planted a known mismatch to find out.
- **The helpful cache.** A shared cache or memoization layer serves route B
  the value route A stored; two routes return the same number because it is
  the same number.
- **The convenient partial audit.** Independence declared after inspecting
  the top layer only; three layers down, both routes read the same input
  table.
- **Post-hoc promotion.** A value computed as a quick internal cross-check
  is promoted months later into the official certificate, its casual birth
  record never upgraded to match its new weight.

## Worked micro-example: certifying a fitted constant

You fit a linear combination of candidate constants to a high-precision
value and the fit closes beautifully. What certifies it?

*Not* agreement with the value you fit to — that is residual arithmetic
restated, evidence of nothing. Certification needs digits the fit never saw:
extend the target value past the precision used in the fit, using an
evaluator that did not produce the fit input, and check the fitted form
against the extension; or evaluate both sides at a different point where an
untouched reference exists. Add the destructive control: refit with one
supposedly essential candidate removed and confirm the fit collapses. A fit
that survives the removal of its key ingredient was never measuring that
ingredient.

A birth record small enough that there is no excuse to skip it:

```
value:     target integral at the check point
accuracy:  60 digits (internal convergence estimate; last 5 digits unconfirmed)
generator: series evaluator v3.2 (commit <hash>), 80-digit working precision
date:      <date written at creation>
contacts:  fed the ansatz fit of <date>  -> may not certify that fit
```

Five lines. The last one is the ledger doing its job: whoever reaches for
this value at certification time is told, by the record and not by memory,
that it is burned.

## Closing checklist

Before calling any agreement a certification:

- [ ] Every reference has a birth record: generator + version, inputs,
      accuracy with its basis, date — written at creation, not recalled.
- [ ] Every oracle has a contact log; every fit, tuning, selection, and
      debugging use is in it.
- [ ] The certifying reference is disjoint from the claim: not in its
      contact history, not produced by the code under test.
- [ ] The counterfactual test passes: had the reference differed, the
      result could not have come out different.
- [ ] For "two independent routes": the deepest shared layer is named in
      writing, with the argument that the feared error cannot live there.
- [ ] The comparator has been shown to FAIL on a planted mismatch.
- [ ] The failure criterion was written down before the comparison ran.
- [ ] Claimed agreement digits do not exceed the recorded accuracy of the
      weaker side.
- [ ] The certificate cites the birth record; the contact log now records
      the certification, burning the reference for anything built on it.

If any box is unchecked, the honest statement is "consistent, pending an
independent check" — and the word *independent* stays out of the writeup
until the ledger can back it.

The empirical basis for distrusting "independent" implementations that share a
layer is Knight and Leveson (IEEE Trans. Softw. Eng. SE-12 (1986) 96); the
one-way contamination rule is the train/test separation of statistical learning
stated for oracles.
