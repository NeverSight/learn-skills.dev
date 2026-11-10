---
name: symbolic-check
description: "Use SymPy to prove or refute a self-authored algebraic identity, derivative, limit, comparative-static sign, or closed form. Use when exact symbolic manipulation can settle the claim. For parameter sweeps or full theorem proving, use $numerical-check or $lean-check."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# Symbolic Check: Prove/Refute a Self-Authored Algebra Step with a CAS

Verify a symbolic manipulation you wrote — an identity, a derivative, a limit, a comparative-static sign, a closed form — using sympy. Unlike numerical falsification, this can **positively verify** the step: a CAS-confirmed identity *is* correct.

## When to Use

- You wrote `A = B`, `∂f/∂x = g`, `lim = L`, `sign(∂f/∂x) = −`, or "the closed form is …" and want it *proven* before it ships.
- `symbolic-check`, "verify this algebra / derivative / limit", "check the comparative-static sign", "does this closed form equal the original".
- Companion to `mark-unverified` for self-authored algebra (the derivative-sign / closed-form family the rule explicitly names).

## When NOT to Use

| Situation | Use instead |
|---|---|
| A full theorem/lemma you want machine-proven end-to-end | `lean-check` (R3) |
| A distributional / probabilistic claim over a parameter space | `numerical-check` (R1) |
| Re-verify a computed empirical result | `cross-language-check` |
| Conceptual / assumption review | `domain-reviewer` |

## Position in the verification spectrum

**R2 — symbolic / CAS.** Can **VERIFY** (prove) or **FALSIFY** a symbolic step; between numerical falsification (R1) and formal proof (R3) in strength. It proves *algebra*, not arbitrary theorems — reasoning beyond symbolic manipulation (measure theory, limits sympy can't evaluate) escalates to `lean-check` or `domain-reviewer`.

## Procedure

### 1. Transcribe the claim precisely, with declared symbol domains

- Restate the exact claim: identity `A == B`, derivative `diff(f,x) == g`, limit `limit(f,x,a) == L`, sign `sign(diff(f,x))` over a domain, or closed form `expr == cf`.
- **Declare assumptions on the symbols** — `symbols('x', positive=True, real=True)` etc. Comparative-static signs and simplifications are *wrong without the right domain*. State them explicitly (they are part of the claim).

### 2. Prove the core with `.equals()`, not `simplify(...)==0`

sympy's `simplify` is heuristic — a **non-zero** result does **not** mean the claim is false, only that simplify gave up. Use `(A - B).equals(0)`, which combines symbolic + random-point numerical testing and returns:
- `True`  → **VERIFIED** (identity holds)
- `False` → **FALSIFIED** (a witness point disproves it)
- `None`  → **INCONCLUSIVE** (undecided) — go to step 3.

For derivatives: `diff(f, x).equals(g)`. For limits: `limit(f, x, a)` and compare to `L`. For a closed form: `expr.equals(cf)`.

### 3. On `None`, escalate — do NOT guess

- Try stronger simplifiers targeted at the form: `factor`, `radsimp`, `trigsimp`, `powsimp`, `together`, `rewrite(...)`, `assuming(...)` with the domain.
- **Numerically substitute** several random in-domain points into `A - B` — if all ≈ 0, report `INCONCLUSIVE (numerically consistent, symbolically undecided)`; if any is far from 0, that's a **FALSIFIED** witness.
- Never upgrade `None` to `VERIFIED`. Undecided is undecided.

### 4. Comparative-static / monotonicity signs

- Compute `d = diff(f, x)`. Ask whether `d` has a definite sign *under the assumptions*.
- Try `refine(d > 0, Q.positive(...))` / `ask(Q.negative(d), assumptions)`; if sympy can't decide, sample the domain numerically to conjecture the sign, then report `INCONCLUSIVE (sign consistent on N points)` — a sign you can't prove symbolically is a candidate for `numerical-check` (falsify) or `lean-check` (prove).

### 5. Belt-and-suspenders

Even on a `.equals() == True`, do a **quick numerical substitution** at one random point as a sanity check against a symbol/transcription bug. A transcription error is the most common real failure.

### 6. Emit the verification report

## Script skeleton (adapt)

```python
# uv run --no-project --with sympy python <script>.py
import sympy as sp
mu, mumax, rho = sp.symbols('mu mumax rho', positive=True)   # DECLARE the domain
# --- identity / closed-form ---
A = mu / sp.sqrt(rho); B = mumax                              # claim: threshold solves A == B
rho_star = sp.solve(sp.Eq(A, B), rho)                        # -> [mu**2/mumax**2]
print("rho* =", rho_star, " expected (mu/mumax)**2:", (mu/mumax)**2)
print("identity holds:", (rho_star[0] - (mu/mumax)**2).equals(0))   # True / False / None
# --- derivative sign (monotonicity) ---
Phi = lambda z: (1 + sp.erf(z/sp.sqrt(2)))/2                 # standard normal CDF
Q = Phi(mu/sp.sqrt(rho)); d = sp.diff(Q, rho)
print("dQ/drho =", sp.simplify(d), " sign<0 on domain (mu>0):", sp.ask(sp.Q.negative(d), sp.Q.positive(mu)))
```

## Anti-Patterns

- **Don't** read `simplify(A - B) != 0` as FALSIFIED — that's simplify giving up. Use `.equals()`.
- **Don't** upgrade a `None` (undecided) to VERIFIED. Report INCONCLUSIVE.
- **Don't** verify a sign/closed-form without declaring the symbol assumptions — the domain is part of the claim, and the wrong domain gives the wrong answer.
- **Don't** skip the numerical sanity substitution — it catches transcription bugs a symbolic pass can hide.
- **Don't** use bare `python3` — use `uv run --no-project --with sympy python`.
- **Don't** force a hard theorem through the CAS — if it needs real reasoning (not symbolic manipulation), escalate to `lean-check` (R3) or `domain-reviewer`.

## Output — Verification Report (shared `*-check` shape)

Write to `reviews/<scope>/verify-symbolic/<YYYY-MM-DD-HHMM>.md`:

```
claim:    <exact symbolic statement + declared symbol domains>
method:   R2 symbolic/CAS (sympy .equals() [+ numeric sanity at <k> points])
verdict:  VERIFIED | FALSIFIED | INCONCLUSIVE (numerically consistent, symbolically undecided) | ERROR
evidence: <simplified form / witness point that disproves / the derived closed form>
reproduce: uv run --no-project --with sympy python experiments/<script>.py
```

## Verification (did this skill work?)

- Verdict is one of the four; `VERIFIED` is emitted **only** on `.equals() == True` (or an exact `solve`/`limit` match), never on `None`.
- A numerical sanity substitution accompanies every VERIFIED.
- If feeding a paper, the confirmed closed form / sign is the value that goes in (and any derived constant is emitted via a macro, `no-hardcoded-results`).

## Worked example — 2026-07-04 (median-collapse paper)

- **Closed-form threshold:** claim `ρ* = (μ_med/μ_max)²` solves `Φ(μ_med/√ρ) = Φ(μ_max)`. `solve(μ_med/√ρ = μ_max, ρ)` → `μ_med²/μ_max²`; `.equals()` → **VERIFIED**.
- **Homogeneous monotonicity (Prop 3.1):** `d/dρ Φ(μ/√ρ) = φ(μ/√ρ)·μ·(−½ρ^{-3/2})`, negative for `μ>0` → sign **VERIFIED** under `Q.positive(mu)` (numeric-confirmed on the domain where sympy hesitates).
- These are the algebra rungs beneath the theorems `numerical-check` stress-tested and `lean-check` could formalize.
