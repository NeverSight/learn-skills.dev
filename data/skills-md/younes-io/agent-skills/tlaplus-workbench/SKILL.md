---
name: tlaplus-workbench
description: "Write and iteratively refine executable TLA+ specs (.tla) and TLC model configs (.cfg) from natural-language system designs; run TLC model checking; summarize pass/fail and counterexamples with explicit assumptions and bounds. Use when asked to: design/validate a state machine or distributed protocol with TLA+, create/edit .tla or .cfg files, run TLC, or interpret TLC failures/counterexamples."
---

# TLA+ Workbench

## Outputs

- TLA+ spec(s): `*.tla`
- TLC config(s): `*.cfg`
- TLC run artifacts: `.tlaplus-workbench/runs/<run-id>/...` (logs, json trace if any)

## Non-Negotiables (Honesty Rules)

- Never say "proved correct". Say "no counterexample found" and state the bounds/model used.
- Always surface modeling assumptions you introduced to remove ambiguity.
- If liveness is in scope, explicitly state fairness assumptions used in the run (`WF_`/`SF_`), or explicitly say "none (safety-only run)".
- Actively guard against vacuous success before calling a run "pass":
  - Show that at least one non-stuttering transition is reachable.
  - If using `CONSTRAINT` / `ACTION_CONSTRAINT`, list each one and the behavior it excludes.
  - Reject properties that are tautological or trivially weakened.
  - If any vacuity check is inconclusive, report "inconclusive coverage" instead of "pass".

## Workflow (NL -> Spec+CFG -> TLC -> Iterate)

### 1) Pin Down Scope and Bounds (Ask, Don't Guess)

Ask for (and record) answers:
- What are the state variables?
- What are the actions/steps?
- What safety properties must never break? (invariants)
- What liveness properties must eventually happen? (temporal properties)
- If liveness is in scope, what fairness model applies to which actions? (`WF_`/`SF_`)
- What environment/failure model is in-scope? (message loss, crashes, reordering, clock skew, retries)
- What bounds make the model finite? (small sets for nodes, messages, values, time, etc.)

If the user doesn't specify bounds, propose minimal ones (and label them as "proposed"):
- 2-3 nodes, 2-3 values, short message buffers, small time domain.

### 2) Write the Minimal Spec Skeleton (Then Grow It)

Use a consistent structure:
- `CONSTANTS` for bounded sets (e.g., `Nodes`, `Values`).
- `VARIABLES` for state.
- `Vars == <<...>>` as a single canonical variable tuple name. Use the same casing (`Vars`) everywhere.
- `TypeOK` (type invariant) to keep the model honest.
- `Init` and `Next` (with `UNCHANGED` for untouched vars).
- For safety checks: `Spec == Init /\\ [][Next]_Vars`.
- For liveness checks: extend `Spec` with explicit fairness assumptions, e.g. `/\\ WF_Vars(SomeAction)` or `/\\ SF_Vars(SomeAction)`.
- Named invariants as separate operators so they can be listed in the `.cfg`.

Prefer modeling the *design* over implementation details. If the design is fuzzy, model the uncertainty explicitly with nondeterminism and constraints.

### Requirement Ledger (Prevent Hallucinated Coverage)

Maintain a compact checklist that maps each natural-language requirement to one of:
- A named invariant/operator in the spec (and listed in the `.cfg`)
- A temporal property (and listed in the `.cfg`)
- A precondition in one or more actions
- Explicitly "not modeled yet"

When reporting results, include this ledger (or a short version) so it's obvious what passed vs what was never encoded.

### 3) Write the TLC `.cfg` (Make the Model Check Run)

Baseline config (edit as needed):

```tla
SPECIFICATION Spec
\* Or:
\* INIT Init
\* NEXT Next

CONSTANTS
  \* Example:
  \* Nodes = {n1, n2, n3}
  \* Values = {v1, v2}

INVARIANT
  TypeOK
  \* Add safety invariants here

CHECK_DEADLOCK TRUE
```

Deadlock policy:
- Keep `CHECK_DEADLOCK TRUE` by default.
- If terminal states are intentional, define an explicit terminal condition in the spec and report deadlock outcomes as either "expected terminal completion" or "unexpected stall".

If you introduce `CONSTRAINT` / `ACTION_CONSTRAINT`, call it out as a *coverage tradeoff* and report what behavior it removes.

### 4) Run TLC Deterministically (Via Bundled Script)

Prereqs:
- `java` on PATH
- `jq` on PATH
- `tla2tools.jar` available and pointed to by `TLA2TOOLS_JAR` (or pass `--jar`)

Run (from the `tlaplus-workbench` skill directory):

```bash
scripts/tlc_check.sh --spec path/to/Foo.tla --cfg path/to/Foo.cfg
```

This writes a run directory under the spec folder:
- `.tlaplus-workbench/runs/<run-id>/summary.json`
- `.tlaplus-workbench/runs/<run-id>/tlc.stdout`
- `.tlaplus-workbench/runs/<run-id>/tlc.stderr`
- `.tlaplus-workbench/runs/<run-id>/counterexample.json` (only if TLC produced one)

### 5) Iterate (Tight Loop)

If TLC fails:
- Explain the failure using the dumped trace (focus on state deltas and the violated property).
- Patch the spec/config minimally.
- Re-run and compare.

If TLC passes:
- Report: bounds, invariants/properties checked, fairness assumptions used (or "none"), deadlock interpretation, and what's still unmodeled.
  - Confirm vacuity checks passed; otherwise report "inconclusive coverage."
  - Example: "Checked with 3 nodes, 2 values, bounded message buffer of size 2; no counterexample found."

## Resources

### scripts/
- `scripts/tlc_check.sh`: run TLC with `-dumpTrace json`, capture logs, emit `summary.json`
- `scripts/tlc_trace_summary.sh`: summarize a `counterexample.json` into step-by-step diffs (optional helper)

### references/
- `references/spec_skeleton.md`: minimal skeleton patterns and cfg snippets
