---
name: lean-check
description: "Formalize a self-authored lemma or theorem in Lean 4/mathlib and require a clean `lake build` without `sorry`. Use when the mathematical claim can be stated faithfully and machine-checked. For numerical falsification or symbolic algebra, use $numerical-check or $symbolic-check."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# Lean Check: Machine-Prove a Self-Authored Lemma

Formalize a lemma/theorem in Lean 4 + mathlib and let the kernel check it. A `lake build` that succeeds **with no `sorry` and no extra axioms** is a machine-verified proof — the strongest guarantee available.

## When to Use

- A **critical lemma** whose correctness you want beyond doubt (the load-bearing step of a theorem).
- `lean-check`, "formalize this in Lean", "machine-check this lemma", "prove this in Lean 4".
- After `numerical-check` fails to falsify a claim and it's important enough to *prove*.

## When NOT to Use

| Situation | Use instead |
|---|---|
| Stress-test / hunt a counterexample to a distributional claim | `numerical-check` (R1) |
| Verify an algebra / derivative / limit / closed-form step | `symbolic-check` (R2) |
| A statement too rich to faithfully formalize in reasonable time (heavy measure theory, bespoke objects) | `domain-reviewer` — do NOT force a lossy Lean statement |

## Position in the verification spectrum

**R3 — formal machine proof.** The top rung: `lake build` (clean, `sorry`-free) = a kernel-checked theorem. Cost is high (formalization effort + statement fidelity), so reserve it for the claims that matter most; use R1/R2 to triage first.

## Toolchain (pre-seeded — do not re-download)

- **Machine:** Mac Mini (hostname contains `Mac-mini`). Check `hostname`; if on the MacBook, run via `ssh mini`.
- **Project:** `~/lean-verify/mathlib_verify/` — Lean `4.31.0`, mathlib `v4.31.0` (cache-backed, ~7.2 GB `.lake`). Health check: `cd ~/lean-verify/mathlib_verify && lake build MathlibVerify.SmokeTest`.
- Refresh mathlib later: `lake update && lake exe cache get`.

## Procedure

### 1. State the lemma FAITHFULLY (the hard part — get this right or the check is worthless)

- Write the Lean statement so it **provably matches the informal claim**. A too-weak, too-strong, or subtly-different statement that happens to `build` gives *false confidence* — the single worst failure mode.
- Before proving, read the Lean statement back against the paper's exact hypotheses and conclusion. State every hypothesis (domains, `0 < ρ < 1`, `StrictMono`, etc.). When unsure the encoding is faithful, ask the user to confirm the statement.
- If the object cannot be faithfully stated in available mathlib (e.g. a bespoke distributional limit), STOP — report `INCONCLUSIVE (not faithfully formalizable)`; do not ship a lossy proxy.

### 2. Write the module into the mathlib project scratch (NEVER the Overleaf paper)

Write to `~/lean-verify/mathlib_verify/MathlibVerify/<Name>.lean`:
```lean
import Mathlib
theorem <name> (<hyps>) : <conclusion> := by
  <tactic proof>
```

### 3. Prove with mathlib tactics; iterate

- Try: `simp`, `norm_num`, `ring`, `linarith`/`nlinarith`, `positivity`, `gcongr`, `field_simp`, `exact?`, `apply?`, `polyrith`.
- Iterate on the proof, not the statement. **If you find yourself weakening the statement to make it build, STOP** — that's cheating the check.

### 4. Build and read the verdict

```bash
cd ~/lean-verify/mathlib_verify && lake build MathlibVerify.<Name>
```
- **Exit 0 + no `sorry`** → candidate VERIFIED. Confirm no shortcuts:
  - `grep -n 'sorry\|admit' MathlibVerify/<Name>.lean` → must be empty.
  - Add `#print axioms <name>` and rebuild → must show only `propext, Classical.choice, Quot.sound` (mathlib's standard axioms); **`sorryAx` present ⇒ NOT proven**.
- **Statement doesn't typecheck** → formalization error (fix the statement, re-verify fidelity).
- **Builds but proof won't close** after honest effort → `INCONCLUSIVE (unproven; claim may still be true)`. Failing to prove is NOT a disproof.
- **You prove the negation** (`¬ <claim>`) → `FALSIFIED`.

### 5. Emit the verification report + keep the .lean

## Verdict semantics (important)

| Outcome | Verdict |
|---|---|
| Faithful statement, clean build, no `sorry`, standard axioms only | **VERIFIED** |
| Proved the negation | **FALSIFIED** |
| Faithful statement, proof didn't close after real effort | **INCONCLUSIVE (unproven)** |
| Can't faithfully formalize the claim | **INCONCLUSIVE (not formalizable)** |
| Toolchain / build-system failure | **ERROR** |

## Anti-Patterns

- **Don't** trust a green build without checking `sorry`/`admit` and `#print axioms` — a `sorry` builds fine and proves nothing.
- **Don't** weaken/alter the statement to make it build — the statement is the claim; a proof of a different statement is false confidence.
- **Don't** read "proof didn't close" as FALSIFIED — inability to prove ≠ disproof.
- **Don't** force a rich probabilistic/measure-theoretic claim into a lossy Lean proxy — report not-formalizable and escalate to `domain-reviewer`.
- **Don't** write into `paper-{venue}/paper/` or re-scaffold mathlib — use the seeded project scratch.
- **Don't** run bare `python`/toolchain guesses — Lean via `lake` only.

## Output — Verification Report (shared `*-check` shape)

Write to `reviews/<scope>/verify-lean/<YYYY-MM-DD-HHMM>.md`, and copy the `.lean` module beside it (or note its path):

```
claim:    <informal statement> ⟶ <Lean statement (verbatim)>
fidelity: <one line: why the Lean statement faithfully encodes the claim>
method:   R3 Lean 4 (v4.31.0) + mathlib; lake build; sorry-free; axioms = <#print axioms output>
verdict:  VERIFIED | FALSIFIED | INCONCLUSIVE (unproven|not formalizable) | ERROR
reproduce: cd ~/lean-verify/mathlib_verify && lake build MathlibVerify.<Name>   (module attached)
```

## Verification (did this skill work?)

- `lake build MathlibVerify.<Name>` exits 0.
- `grep sorry` is empty AND `#print axioms` shows only the standard three.
- The `## fidelity` line exists — no VERIFIED without an explicit statement-faithfulness argument.

## Worked example (toolchain smoke)

`theorem lc_smoke (a b : ℝ) (h : a ≤ b) : a - 1 < b + 1 := by linarith` → `lake build` exit 0, no `sorry`, standard axioms → **VERIFIED**. (A faithful Lean formalization of the median-collapse *theorem* itself — Φ, medians of distributions, the large-council limit — is a genuine formalization project; `lean-check` is for the tractable load-bearing lemmas, with R1/R2 covering the rest.)
