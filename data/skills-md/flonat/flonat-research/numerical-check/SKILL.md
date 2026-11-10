---
name: numerical-check
description: "Numerically stress-test a self-authored mathematical claim over its parameter space to seek counterexamples or characterize violations. Use when checking monotonicity, thresholds, inequalities, comparative statics, or limits computationally. For algebraic proof or Lean formalization, use $symbolic-check or $lean-check."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# Numerical Check: Falsify a Self-Authored Math Claim by Sweep

Empirically stress-test a mathematical claim you wrote but have not proven. The goal is **falsification**: throw many random instances at the claim and try to break it. A single genuine counterexample kills the claim; a large clean sweep is *evidence*, never proof.

## When to Use

- You wrote a **Proposition / Theorem / Conjecture** (monotonicity, threshold, comparative-static, inequality, closed-form, limit) and want to know if it's actually true before claiming it.
- `numerical-check`, "stress-test my conjecture", "find a counterexample to X", "is Q(ρ) really monotone", "does the threshold hold for all …".
- The write-time empirical arm of the `mark-unverified` rule (self-authored math must be checked before assertion).

## When NOT to Use

| Situation | Use instead |
|---|---|
| Verify an algebra / derivative / limit / closed-form identity | `symbolic-check` (R2) |
| Machine-prove a lemma (want a proof, not a stress-test) | `lean-check` (R3) |
| Re-verify a computed empirical result in another language | `cross-language-check` |
| Conceptual / assumption-completeness review | `domain-reviewer` (agent) |

## Position in the verification spectrum

**R1 — numerical falsification.** Can **FALSIFY** definitively (a confirmed counterexample refutes the claim) but can **never VERIFY** (no counterexample ≠ proof). The strongest positive result is `INCONCLUSIVE (supported): no counterexample in N draws`. Pair with `lean-check` (R3) to *prove* the claim once it survives.

## Procedure

### 1. Formalize the claim as a predicate over a domain

Restate the claim as `P(x)` that must hold for **all** `x` in a domain `D`. Make the failure condition explicit and quantitative.
- "Q(ρ) is monotone decreasing in ρ" → `P(instance) := max_i (Q(ρ_{i+1}) − Q(ρ_i)) ≤ tol` over a ρ-grid.
- "threshold ρ* separates help/hurt" → `P := (Q<p_max) iff (ρ>ρ*)`.
- Write down the domain `D` precisely (which parameters, which ranges, which side-conditions — e.g. "mean competence > ½, dispersed").

### 2. Sample the domain to approximate the TRUE object — not finite-n atoms

**This is the step that fools people.** If the claim is about a *continuous* or *large-n limit* object, a tiny discrete instance is NOT that object — it carries finite-n artifacts (ties, atoms, degenerate medians, staircase discontinuities) that manufacture *fake* violations.
- If the claim is a large-n / continuous-distribution statement, represent each random instance with **dense sampling** (hundreds of points), so the computed quantity approximates the limit.
- Generate instances from **varied shapes** (uniform, skewed, bimodal, heavy-tailed) so the sweep is adversarial, not cherry-picked.

### 3. Evaluate on an INTERIOR grid, smoothly, with a noise-aware tolerance

- Grid the parameter on the **interior** (e.g. ρ ∈ [0.02, 0.98]); endpoints breed boundary/degeneracy artifacts.
- Prefer a **smooth** evaluation (e.g. root-find the crossing) over indicator-quadrature, which quantization-jitters and creates false steps.
- Set the violation **tolerance an order of magnitude above the numerical noise floor** (measure the floor on a case you believe holds). Too tight → false positives; too loose → misses real breaks.

### 4. Sweep, count, capture the worst — seeded

- Run over **thousands** of random instances (`uv run --no-project --with numpy --with scipy python`; **never bare `python3`**). Seed the RNG.
- Count genuine violations; **capture the worst counterexample** (the instance + violation magnitude) for reporting and for the figure.

### 5. Diagnose a surprise BEFORE trusting it

If you find violations (or a suspiciously high/low rate), **do not report the raw number yet**. Check it is not an artifact:
- Re-plot the worst case on a fine grid — is the "violation" a real interior feature, or a jump at an endpoint / a finite-n tie?
- Re-run with **denser sampling** and **odd vs even n** — does the rate persist as you approach the continuous limit? An artifact shrinks; a real effect stays.
- Only once it survives these is it real. (Document the surprise + the diagnosis — `design-before-results`.)

### 6. Characterize the violators — mechanism, not just a rate

A bare "X% violate" is weak; find *when* it breaks. Break the sweep down by instance feature (shape, skew, competence-gap, bimodality) and report the driver: "non-monotonicity is a **bimodal** phenomenon — 18% of bimodal vs ~0% unimodal." This turns a number into a result.

### 7. Emit the verification report + wire numbers if feeding a paper

Write the report (shape below). If the result feeds a LaTeX paper, emit every number via a generated macro file (`results-numbers.tex`, `no-hardcoded-results`) and keep the seeded script in `experiments/`.

## Script skeleton (adapt; keep it seeded + uv-run)

```python
# uv run --no-project --with numpy --with scipy --with matplotlib python <script>.py
import numpy as np; from scipy.stats import norm; from scipy.optimize import brentq
RNG = np.random.default_rng(0)
def quantity(instance, t):        # smooth eval of the claimed object at parameter t
    ...                           # prefer root-find over indicator-quadrature
def sweep(n_trials, nsamp):       # dense instances, interior grid, noise-aware tol
    grid = np.linspace(0.02, 0.98, 90); viol = 0; worst = (-1, None); by = {}
    for _ in range(n_trials):
        inst = draw_instance(RNG, nsamp)          # varied shapes, dense
        if not in_domain(inst): continue
        Q = np.array([quantity(inst, t) for t in grid])
        up = np.diff(Q).max()                     # violation statistic
        if up > worst[0]: worst = (up, inst)
        if up > 1e-4: viol += 1; bump(by, feature(inst))
    return viol, worst, by                        # characterize by feature
```

## Anti-Patterns

- **Don't** test a continuous/large-n claim with tiny discrete instances — finite-n ties/atoms fabricate violations. (2026-07-04: a small-n sweep read 29%; dense sampling read the real 6%.)
- **Don't** evaluate at exact parameter endpoints — degeneracies live there.
- **Don't** set the tolerance near the numerical-noise floor (false positives) or absurdly loose (misses real breaks).
- **Don't** trust the first surprising number — diagnose artifact-vs-real first.
- **Don't** report a bare violation rate — characterize the driver.
- **Don't** claim `VERIFIED` — numerical can only FALSIFY or SUPPORT. Say "no counterexample in N draws".
- **Don't** use bare `python3` — it's blocked by the uv-only allowlist; use `uv run`.
- **Don't** confirm "clean" from a compile log or a grep alone — check the actual object (e.g. grep the rendered PDF for `??`, not the build log).

## Output — Verification Report (shared `*-check` shape)

Write to `reviews/<scope>/verify-numerical/<YYYY-MM-DD-HHMM>.md`:

```
claim:    <the exact statement tested, with its domain>
method:   R1 numerical falsification (N=<trials>, nsamp=<density>, grid=<interior>, tol=<t>)
verdict:  FALSIFIED | INCONCLUSIVE (supported: no counterexample in N) | INCONCLUSIVE | ERROR
evidence: <worst counterexample instance + magnitude>  OR  <"no counterexample; sweep params">
mechanism:<what feature drives violations, if any>
reproduce: uv run --no-project --with ... python experiments/<script>.py   (seed=<s>)
```

## Verification (did this skill work?)

- The script runs seeded via `uv run` and prints a violation count + worst case.
- The verdict is one of the four values; `VERIFIED` is never emitted.
- If a paper consumes the result, numbers come from a generated macro file (nothing hand-typed).

## Worked example — 2026-07-04 (median-collapse paper)

Claim: "Q₀(∞;ρ) is monotone decreasing in ρ for all competence distributions (mean>½, dispersed)" → single-threshold conjecture.
- Naive small-n sweep: **29%** violations → suspicious; worst case was a balanced even-n council.
- Diagnosed: finite-even-n ties + endpoint staircase — an **artifact**.
- Corrected (dense sampling, interior grid, smooth root-find eval, tol=10⁻⁴): **6%** real violations, worst step +0.013.
- Characterized: non-monotonicity is a **bimodal** phenomenon (18% of bimodal vs 3/3363 unimodal).
- Verdict: **FALSIFIED** — the conjecture was removed and replaced with the characterized finding.
