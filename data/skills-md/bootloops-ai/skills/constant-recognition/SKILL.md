---
name: constant-recognition
description: Discipline for integer-relation searches (PSLQ, LLL) that turn high-precision digits into exact constants. Use whenever recognizing a numerical value as a closed form, fitting boundary constants, or reporting that no closed form exists.
---

# constant-recognition — naming numbers without fooling yourself

An integer-relation algorithm is a fitting machine. Hand PSLQ a vector of
reals and enough coefficient freedom and it returns a relation, every time;
that is what lattice reduction does. Whether the relation means anything is
decided entirely by choices made **before** the search — which constants are
allowed, how large the integers may be, how many digits pay for it all. The
same choices made *after* seeing the digits are curve fitting with a number
theorist's vocabulary. Everything in this skill exists to keep the decisions
on the correct side of the search.

The asymmetry to internalize: a hit is cheap — noise plus freedom produces
hits on demand — while a null is informative only against a declared ring.
"PSLQ found nothing" means nothing by itself. "Not a Z-linear combination of
{1, ζ(3), π² log 2, Li₃(1/2)} with coefficients below the declared height at
the declared precision" is an exact, reusable, citable statement. The whole
protocol is arranged so that both outcomes mean something.

## The digit budget

Before anything else, the arithmetic that governs the whole exercise. A
candidate relation among n constants with integer coefficients up to height H
consumes roughly n·log₁₀H digits of precision just to be expressible, and a
search run with only that much precision can always satisfy itself. The
digits left over — working precision minus that cost — are the only evidence.
If the surplus is thin, the search is a coin flip; if the ring and heights
cost more digits than you have, the search is theater, and it will still
return a relation. Budget first: choose the ring, choose the largest
coefficients you would believe, compute the cost, and demand a surplus of
many tens of digits before running at all. When the budget does not close,
the correct moves are to compute more digits or to shrink the ring. Running
anyway is the original sin from which every failure below descends.

## Procedure

1. **Declare the ring, in writing, before the first search.** List the
   constants the answer is allowed to draw on and the reason each one is on
   the list: a weight grading, the arithmetic of the geometry the problem
   lives on, the closed forms of solved neighboring cases. The reason
   matters — "it shows up in related problems" admits everything eventually.
   Date the list and keep it with the run, so the record shows the
   declaration preceded the search.

2. **Fix the height bound and pay for it.** State the maximum coefficient
   size you would accept in a believable answer — informed by the heights
   that appear in solved relatives of the problem — then verify the digit
   budget above. Record both numbers with the declaration.

3. **Plant the controls before the real value goes in.** Two of them, both
   pushed through the identical code path — same script, same precision, same
   ring, same height bound:
   - a **positive control**: a value whose closed form in the declared ring
     is independently known. The search must recover exactly that form.
   - a **negative control**: a value constructed to lie outside the ring —
     the digits of a random real at the same precision serve. The search must
     return null.

   A search whose controls have not run is uncalibrated, and any hit it
   produces is unreviewable.

4. **Run, and record everything.** Precision, ring, height bound, the exact
   input vector, the algorithm and its settings. A relation whose search
   parameters were not recorded cannot be distinguished, later, from one
   found by dredging.

5. **Rerun at genuinely higher precision.** Not a handful of extra digits —
   enough to move the noise floor. A true relation persists with the same
   integers; a spurious one dissolves or reshuffles its coefficients.
   Identical integers at two well-separated precisions is the minimum bar for
   taking a hit seriously. It is not the final bar.

6. **Certify on digits the search never touched.** The digits that suggested
   the relation may not also certify it — that is testing a fit on its
   training data. Evaluate the value and the proposed closed form by an
   independent route — a different method or a different implementation — at
   precision beyond everything the search consumed, and demand many digits of
   agreement past the fit. These held-out digits are the acceptance gate;
   nothing moves forward without them.

7. **Report one of two things.** Either the closed form with its full
   certification record (ring, heights, precisions, control outcomes,
   held-out agreement), or the null with its parameters plus the value
   itself: a convergent series or integral representation with an
   arbitrary-precision evaluator, so the number is usable without a name.

## Failure modes

These are the classes the discipline exists to catch. Each one produces
output that looks like success.

**Ring enlargement after seeing the digits.** The declared search fails; a
plausible extra constant goes in "because it appears in related problems";
the enlarged search fails; another constant goes in; the third search closes,
with large coefficients. The closure was manufactured by the enlargement
process — each added constant is added freedom, and enough freedom always
closes. An enlargement is a new experiment: it needs a justification that
does not mention the failed search, and the digit budget must be paid again
for the bigger ring. Repeated ring changes against the same digits are
dredging, whatever the log calls them.

**Height creep.** The same failure on the other axis. The search at the
declared bound returns nothing; the bound is raised "just to see"; a hit
appears. Each raise hands the algorithm more of your digits to spend on
modeling noise, and a relation that appears only after the bound moves is a
statement about the bound. Decide the height you would believe before
searching; a hit above it is grounds for suspicion, never a result.

**The single-precision hit.** A relation found once, at one precision, and
reported. Rerun higher and the integers shuffle — the reduction was returning
the best available fit to that particular noise floor, which is its job. One
precision is zero evidence.

**Stable but correlated: the "recognized" constant that is a fit.** The
subtle one. The relation is stable at two precisions — but both evaluations
came from the same truncated series with a slowly decaying error term, so the
"noise" is the same systematic error twice, and the relation fits that error
as faithfully as it would fit the truth. Two-precision stability tests
against random noise only. The cure is certification from a genuinely
independent evaluation — different representation, different method,
different code — at points never used in the fit.

**Controls bolted on afterward.** The positive control is run after the
discovery, with settings adjusted until it passes, and reported as
calibration. Controls prove the code path only when they run through the
frozen path before the real search; a control tuned after the fact proves
that tuning works.

**The lookup-table shortcut.** Inverse symbolic calculators and large
constant tables are ring enlargement performed by someone else at industrial
scale: they search every constant anyone has cataloged. They are excellent
hypothesis generators and are never results by themselves. A table hit
re-enters this protocol at step 1 — where the declared ring must now answer
the awkward question of why that constant belongs in it.

**Naming under pressure.** Nothing closes and the report is due, so the
"nearest" closed form gets written down, hedged just enough to survive
review. A wrong name is worse than no name: the value works fine as a
number, but a false closed form propagates into later work that trusts it
exactly, and it fails there silently. When nothing closes, refuse. The
refusal deliverable is genuinely useful — the value, the evaluator, the exact
null statement — and a boundary constant with no classical name is sometimes
the interesting discovery. A fabricated name is a corruption of the record.

## A worked shape

What the record of a defensible recognition looks like. The numbers are a
template, not data:

> **Declared** (before search): ring of four weight-graded constants, chosen
> because the solved neighboring cases close at this weight in these
> constants; height bound fixed; digit budget computed from n·log₁₀H; surplus
> large.
> **Controls:** positive (a solved neighbor's value, run blind) recovered
> exactly; negative (random real at working precision) returned null. Same
> script, same settings, before the real value.
> **Search:** hit, with coefficients well under the declared bound.
> **Stability:** identical integers at the working precision and at a second,
> well-separated precision.
> **Certification:** both sides evaluated by an independent method at higher
> precision still; agreement extending far past every digit the search
> consumed.

And the defensible null:

> No relation in the declared ring at the declared height and precision,
> controls passing. Value delivered as a series/integral with an
> arbitrary-precision evaluator; null recorded with its parameters.

Both are results. Only the second is available when the mathematics does not
cooperate, and it has to remain an honorable outcome — otherwise the pressure
to fabricate wins by default.

## Checklist

Before reporting any recognized constant, or any null:

- [ ] Ring declared in writing, dated, before the first search, with a
      stated reason per constant.
- [ ] Height bound fixed in advance; digit budget computed; surplus generous.
- [ ] Positive and negative controls run through the identical code path,
      before the real search, both passing.
- [ ] Search parameters recorded in full.
- [ ] Hit stable — identical integers — under a genuine precision increase.
- [ ] Certification digits independent of every digit the search consumed,
      from an independent evaluation.
- [ ] Any ring enlargement or height raise documented as a new experiment,
      with its own justification and a re-paid budget.
- [ ] If nothing closed: the null stated with its parameters, and the value
      delivered with an evaluator — no invented name.

**Sources and acknowledgments.** PSLQ is the integer-relation algorithm of
Ferguson and Bailey, analyzed and simplified by Ferguson, Bailey and Arno
(Math. Comp. 68 (1999) 351); LLL is the lattice reduction of Lenstra, Lenstra
and Lovász (Math. Ann. 261 (1982) 515). The precision-budget rule, the
two-precision confirmation and the insistence on stating nulls with their
parameters follow the experimental-mathematics practice developed by David H.
Bailey and Jonathan M. Borwein, and by Bailey and Broadhurst for constants
arising in quantum field theory (Math. Comp. 70 (2001) 1719). Most readers will
run these through mpmath (Fredrik Johansson and contributors), PARI/GP or
Mathematica; we are grateful to their maintainers.
