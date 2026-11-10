---
name: verify-math
description: "Verify a self-authored mathematical result end to end by routing claims across adversarial review, numerical falsification, symbolic or CAS checks, and Lean, then aggregating one report. Use when a theorem, proposition, conjecture, or paper-wide mathematical argument needs the appropriate combination of verification methods. For one known method, use $numerical-check, $symbolic-check, or $lean-check directly."
allowed-tools:
  - Read
  - Grep
  - Bash
  - AskUserQuestion
  - Skill
  - Task
  - Write
  - Edit
agent-dependencies: [domain-reviewer]
---

# Verify Math: Route a Math Claim Through the Verification Spectrum

The front door for verifying self-authored mathematics. Classify each claim, dispatch it to the strongest applicable rung(s), and merge the sub-verdicts into one report. This skill does not verify anything itself — it **routes and aggregates**; the rungs do the work.

## When to Use

- You have a Proposition / Theorem / Conjecture (or a whole paper's worth) and want it verified with the *right* method(s), possibly combined.
- `verify-math`, "verify this theorem", "check all the math in the paper", "is this result correct".
- The operational front end of `mark-unverified`: run this before asserting a self-authored result.

## When NOT to Use

- You already know the single method → call it directly (`numerical-check`, `symbolic-check`, `lean-check`, or `domain-reviewer`).
- Non-mathematical claims (citations, prose) → `proofread`, `bib-validate`, `domain-reviewer`.

## The verification spectrum (the rungs it routes to)

| Rung | Method | Can it… | Tool |
|---|---|---|---|
| R0 | adversarial deductive read | catch conceptual/assumption gaps (no proof) | `domain-reviewer` (agent) |
| R1 | numerical falsification | **falsify** definitively; support (never prove) | `numerical-check` |
| R2 | symbolic / CAS | **prove or falsify** an algebra step | `symbolic-check` |
| R3 | formal Lean proof | **prove** (strongest) | `lean-check` |

## Procedure

### 1. Decompose the result into atomic claims

A theorem is usually several obligations. List each separately: the algebra steps, the distributional/parameter-space claims, the load-bearing lemma, the conceptual assumptions. Verify each with the rung that fits — a single "verdict" on a compound theorem hides which part is shaky.

When the claim lives in LaTeX, extract a self-contained theorem/proof block before dispatch:

```bash
uv run python <skill-dir>/scripts/extract_block.py paper/sections/model.tex "prop:concavity"
```

The helper includes an immediately following proof and any displayed equations referenced by label. Inspect the output and add missing definitions or assumptions before giving it to a reviewer or computational rung.

### 2. Classify each claim → rung

| Claim shape | Rung | Route to |
|---|---|---|
| algebra / derivative / limit / closed-form identity | R2 | `symbolic-check` |
| monotonicity / threshold / comparative-static / inequality over a parameter space (distributional, probabilistic) | R1 | `numerical-check` |
| a critical, faithfully-formalizable lemma | R3 | `lean-check` |
| conceptual correctness, assumption completeness, code-theory alignment | R0 | `domain-reviewer` (Task/agent) |

### 3. Order: falsify cheap → prove expensive

- **Falsify first** with the cheapest applicable rung (usually R1 numerical, or R2 for algebra). A counterexample stops the pipeline — no point proving a false claim.
- **Then prove** the survivors with a proving rung (R2 for algebra, R3 for the key lemma) if the claim is important enough to warrant a positive guarantee.
- **R0 domain-reviewer** runs across the whole result for the conceptual/assumption layer the computational rungs can't see.
- Present the routing plan (claim → rung) and, when it involves R3 (expensive) or ambiguity, confirm with the user before dispatching.

### 4. Dispatch

- Invoke each rung skill via the skill-routing mechanism (`numerical-check`, `symbolic-check`, `lean-check`); dispatch `domain-reviewer` via the Agent tool (fresh context — it reviews math it didn't write, per `agents-vs-skills`).
- Each rung writes its own `reviews/<scope>/verify-<method>/…` report (shared shape).

For a hard proof strategy, existence/uniqueness question, or counterexample search that resists the standard rungs, use an adversarial reasoning pass as **lead generation**, never as a verdict. Make the prompt self-contained: state the exact claim, define every symbol and parameter domain, describe failed approaches, request multiple concrete strategies, and demand explicit algebra or numerical counterexamples. Route every proposed proof step or counterexample back through R1, R2, R3, or the fresh-context R0 reviewer before relying on it.

### 5. Aggregate → one verdict

| Condition | Aggregate verdict |
|---|---|
| **Any** rung returns FALSIFIED | **FALSIFIED** (name which claim + counterexample) |
| A proving rung (R2/R3) VERIFIES the core claim, nothing falsified | **VERIFIED** (note the guarantee level: CAS vs Lean) |
| Only R1 supports (no counterexample), no proving rung | **INCONCLUSIVE (supported: no counterexample in N)** |
| Rungs couldn't decide / not formalizable | **INCONCLUSIVE** |
| Setup/toolchain failure | **ERROR** |

**Numerical alone is never VERIFIED.** Only a proving rung (R2/R3) upgrades a claim from "unfalsified" to "verified".

## Anti-Patterns

- **Don't** collapse a compound theorem into one verdict — decompose; report per-obligation so the shaky step is visible.
- **Don't** report VERIFIED off R1 (numerical) alone — that's INCONCLUSIVE(supported); numerical can't prove.
- **Don't** prove before falsifying — a cheap counterexample saves an expensive Lean effort.
- **Don't** self-review the conceptual layer — dispatch `domain-reviewer` as a fresh-context agent (the session that wrote the math is blind to its own gaps).
- **Don't** skip R0 — the computational rungs verify the *math as stated*; they can't catch a wrong assumption or a statement that doesn't mean what you think.
- **Don't** treat a persuasive exploratory proof or counterexample as verification — it remains a lead until a verification rung checks it.

## Output — Aggregate Verification Report

Write to `reviews/<scope>/verify-math/<YYYY-MM-DD-HHMM>.md`:

```
result:   <the theorem/proposition being verified>
claims:   (one row per atomic obligation)
  - <claim 1> | rung R? | verdict | evidence/report link
  - <claim 2> | rung R? | verdict | ...
verdict:  VERIFIED (Lean|CAS) | FALSIFIED (<which claim>) | INCONCLUSIVE(supported|undecided) | ERROR
guarantee: <the weakest link — the result is only as verified as its least-verified obligation>
next:     <what to escalate — e.g. "obligation 3 unfalsified by R1; Lean-prove it (R3)">
```

## Verification (did this skill work?)

- Each atomic claim has a rung + a sub-verdict + a linked sub-report.
- The aggregate verdict follows the table (FALSIFIED dominates; VERIFIED requires a proving rung).
- The `guarantee` line names the weakest link honestly.

## Worked example — 2026-07-04 (median-collapse paper), how it would route

- Threshold `ρ* = (μ_med/μ_max)²` (closed-form identity) → **R2** `symbolic-check` → VERIFIED.
- Prop 3.1 `d/dρ Φ(μ/√ρ) < 0` (derivative sign) → **R2** → VERIFIED.
- "Q₀(∞;ρ) monotone in ρ for all competence" (distributional monotonicity) → **R1** `numerical-check` → **FALSIFIED** (bimodal counterexample) ⇒ aggregate FALSIFIED for that claim; conjecture removed.
- Median collapse / assumptions (conceptual) → **R0** `domain-reviewer` → substantive check.
- Aggregate: the paper's *symmetric* theorem VERIFIED (CAS); the *general* conjecture FALSIFIED (R1) — exactly the split the paper now reports.
