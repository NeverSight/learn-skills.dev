---
name: numerical-verification
description: Verify numerical and scientific code against independent oracles — closed-form solutions, slow reference implementations, invariants and symmetries, limiting cases, convergence order, and property tests — instead of hand-written expected values. Use this whenever writing, testing, refactoring, or optimizing simulation, solver, linear algebra, Monte Carlo, or analysis code; whenever a test needs an expected value that isn't obvious; whenever someone asks how to test code whose right answer is unknown; and before trusting any number a research script produces. This replaces ordinary TDD for scientific code.
---

# Numerical verification

Model-invoked.

Standard TDD assumes you know the expected output. In scientific computing you usually
don't — the whole point of the code is to produce a number nobody has. So the discipline
shifts: **a test asserts a property you can compute two independent ways.** Your job is to
find the cheapest independent second way.

The cardinal sin is writing an assertion whose expected value you obtained by running the
code under test. That is a snapshot. Snapshots detect change; they never detect error.
Label them as such and never let one stand in for a correctness claim.

## The oracle ladder

Work down this list and use the strongest oracle that applies. Record which one each test
uses, in the test's own docstring — a reader must be able to see what the test would catch.

**1. Closed form.** An exact solution: a free or non-interacting limit, a two-level or
two-body problem, a Gaussian integral, a case with a known eigenspectrum. Strongest
possible check. Usually available only at small size or special parameter values, which is
fine — bugs are rarely size-dependent.

**2. Independent implementation (the slow twin).** A dense, brute-force, obviously-correct
version of the same computation, agreeing with the fast path to machine precision on
randomized inputs at small size. This is the single highest-value piece of test
infrastructure in a research repo. If the project has no slow twin, building one comes
before anything else.

**3. Invariants and symmetries.** Cheap, and they run at production size where the
stronger oracles can't. Check the ones that apply: conservation of energy, particle
number, probability, momentum, charge; trace preservation and normalization; hermiticity;
positive semi-definiteness; unitarity; idempotence of projectors; gauge or basis
invariance; permutation and translation symmetry; time-reversal; detailed balance; sum
rules; reciprocity. Invariants are the only oracle you can afford to assert inside a
production run — do that.

**4. Limiting cases.** Turn a coupling to zero and recover the known simpler physics. Take
the high-temperature, weak-field, non-interacting, or continuum limit. Each limit is a
separate test, and each one wires a different part of the code.

**5. Convergence order.** Refine the discretization and assert the *rate*, not just that
the error is small. Error falling is weak evidence; error falling as h² when the scheme is
second-order is strong evidence. Use Richardson extrapolation to estimate the rate, and
the method of manufactured solutions when no analytic solution exists: pick the answer,
substitute it into the equations to derive the source term that produces it, then verify
the solver recovers it at the design order. MMS is underused and catches an enormous class
of bugs.

**6. Randomized property tests.** Sample the parameter space and assert the properties
above at each point. Catches the bug that only appears near a degeneracy, at zero
temperature, or when two eigenvalues cross — which hand-picked test points never do.

**7. Snapshot / golden regression.** Stored outputs at fixed small configurations. No
correctness claim whatsoever; detects unintended change. Useful, but name these tests so
nobody mistakes them for verification.

## The loop

1. **Find the smallest instance where an oracle applies.** Usually a handful of degrees of
   freedom. Resist the urge to test at production size — you lose the oracle and gain
   nothing.

2. **Write the assertion first, and prove it can fail.** After it passes, perturb the
   implementation — flip a sign, change a constant by 1%, transpose an index — and confirm
   the test goes red. An assertion nobody has seen fail is testing nothing, and this is the
   most common defect in scientific test suites. Tolerance that's too loose, an invariant
   that holds trivially, a comparison against a quantity derived from the same code path:
   all of these pass forever and catch nothing. Do the sabotage check.

3. **Implement the obvious, slow, unoptimized version.** Make it pass.

4. **Only then write the fast path**, and test it against the slow twin over randomized
   inputs.

5. **Keep the slow twin forever.** If you ever have to choose which implementation to
   delete, delete the fast one. You can rewrite an optimization; you cannot rewrite the
   thing that told you the optimization was right.

## Tolerances

Every tolerance needs a justification, written next to it. Pick from:

- Floating point: roughly (machine epsilon) × (condition number) × (operation count).
  If you don't know the condition number, estimate it — that estimate is itself useful.
- Discretization: the method's order times the step size, which you should have measured
  in the convergence test rather than assumed.
- Stochastic: k standard errors, with the standard error computed accounting for
  autocorrelation, not from naive sample variance.

Use relative tolerance for quantities that span magnitudes, absolute tolerance near zero,
and both when comparing arrays with mixed scales — a default `allclose` on an array whose
entries span ten orders of magnitude is testing only the largest entry.

**A tolerance loosened to make a test pass is a bug report.** Sometimes the correct
resolution really is a looser tolerance, but that conclusion needs a reason recorded in
the commit message, not a silent edit.

## Where to point the tests

The bugs are near the edges of validity, so test there deliberately: degeneracies and
level crossings, near-singular and ill-conditioned inputs, zero and infinite limits of
each parameter, stiff regimes, the boundary of the physical domain, the smallest and
largest sizes the code claims to support, and every branch the production configuration
takes that the smoke configuration does not.

## Anti-patterns

- Comparing against a value you got from this code last Tuesday
- Global RNG seeding, so test outcomes depend on test order
- Testing only in the regime where the physics is boring
- Asserting a result is "reasonable" rather than equal to something
- A single test that runs the whole pipeline and checks the final plot's mean — when it
  fails you learn nothing
- Ignoring solver convergence flags, eigensolver return codes, or NaN propagation, then
  asserting on the output anyway
