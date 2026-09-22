---
name: exp-campaign
description: Design a staged, prunable research experiment campaign for a researcher's idea, hypothesis, or optimization direction, with ponytail-for-experiments taste. Use when explicitly requested, or when a researcher proposes a direction that needs many experiments, ablation branches, or cross-factor sweeps. Observe existing results, grill the researcher to shared understanding, enumerate the maximal experiment space, then prune it with cheap probe experiments whose outcomes decide which cells never run; deliver a decision-tree plan with observation gates and the final metrics/figure design, and hand execution to exp-batch per stage. For a single bounded experiment branch use exp-batch; for one-off spot checks use exp-probe.
---

# Exp Campaign: observe → grill → enumerate → prune → stage → hand off → review

Ponytail for experiments: **the campaign is as small as the evidence allows, and as complete as the claim requires.** Never open with the full factorial matrix; never silently drop a dimension. Enumerate everything, then earn every deletion with a cheap probe whose outcome justifies it.

## When this skill applies

- A direction that needs multiple branches, ablations, or conditional staging. One bounded branch with known configuration is `exp-batch`; one missing datapoint is `exp-probe`; a still-fuzzy idea is `exp-discuss`.
- The researcher's explicit choice wins; never switch silently. Judge by decision-tree depth and factor count, not by how long the experiments run (if unsure between probe and batch, use batch). Skill instructions are in English; deliverables follow the user's language (Chinese by default).

## 1. Observe before asking

- Read project memory, dashboards, past runs, logs, and previous conclusions. Establish what is already known, which baselines exist, which metrics are canonical, and what the current evidence does NOT cover.
- Restate the researcher's idea in 2-3 sentences: the claim to test, what a convincing final figure looks like, and what is out of scope. Separate explicit requirements from open questions.

## 2. Grill the researcher

Use bounded rounds of frontier questions — only what the settled decisions have already unblocked — each with a recommended answer; facts you can inspect are yours to find, never the researcher's. Recompute the frontier after each round of answers and ask the next round: the round count is not capped, and stopping is decided by whether a further question would still move scope, claim, or acceptance.

Ask about and surface, in frontier order:

- **The claim:** what exactly should the final plot/table show? Which comparison would change the researcher's mind?
- **The axes:** which factors matter (method, model, dataset, precision, seed, lr, …), and which levels per factor.
- **Overlooked details the researcher may have missed:** evaluation split, calibration vs eval data leakage, callback-vs-reload metric consistency, seed variance, degenerate baselines (e.g., all-same-answer collapse), early/late checkpoint selection, and platform/numeric equivalence. Propose these explicitly; researchers under-specify them.
- **Budgets:** device hours, wall-clock deadline, storage; which runs are formal vs exploratory.
- **Acceptance:** what counts as success, tie, and negative result worth keeping.

Stop when execution-critical and acceptance-critical decisions are settled. Do not invent a question quota.

## 3. Enumerate the maximal experiment space

Write the full factor × level matrix as a table. Every cell gets one label:

- **must-run** — the claim directly depends on it;
- **probe-decidable** — a cheap experiment can decide whether this whole row/column/branch is needed;
- **prunable** — already answered by existing evidence, or provably redundant (state the evidence).

The maximal list is the starting point on purpose: pruning must be visible and justified, so reviewers see what was considered.

## 4. Design pruning probes

For each probe-decidable group, design the **smallest experiment whose outcome removes the most cells**:

- Example pattern: two configurations show metric A ≈ metric B (callback vs reload, dtype variants, cache modes) → adopt the cheaper one for the whole remaining matrix; record the equivalence claim, its evidence, and its confidence.
- Each probe specifies: configuration, expected cost, the observation, and the **pruning rule** written as a decision: `if <observed condition> then skip <cells>, else run <cells>`.
- Probes must themselves respect the project’s experiment conventions (preflight, run IDs, output layout). A probe that violates protocol teaches nothing safely.

## 5. Write the staged plan

One Markdown document, tables over prose:

1. **Claim and scope** — including the final deliverable: the metrics table schema (rows = runs, columns = metrics × surfaces × splits) and the figure list (each figure: axes, curve families, reference lines, per-dataset layout). Every planned run must fill at least one cell or curve; a run that changes no figure needs justification.
2. **Current evidence** — what is already measured, with pointers.
3. **Maximal matrix** with per-cell labels from §3.
4. **Stages with observation gates:** Stage 0 probes → decision point (which branches survive) → Stage 1 core runs → Stage 2 confirmatory runs (full epochs, independent reload, formal protocol). For each gate: exact command list, cost estimate, expected observation, the resource/device convention for its runs (chosen from a live read, passed explicitly, never the default device), and the branch table for each outcome. Every run in the plan passes the preflight pass from `exp-batch` before it starts.
5. **Pruning ledger** — assumptions made, probes that justify them, confidence.
6. **Failure handling** — what to do on OOM/NaN/inconclusive/**evicted** (a neighbour's job or the machine taking the card): capture evidence, isolate minimally, do not silently skip. Name these as the expected shapes, not the full space: unforeseen failures are decided on the spot and recorded as deviations, not escalated into a new process.
7. **Deliverables:** the plan file (project working-doc dir; default `docs/experiments/YYYY-MM-DD-<slug>.md`), one self-contained launcher prompt per stage (fenced in the plan AND printed in chat), the gate decisions recorded in the pruning ledger, the mandatory per-stage executor reports (`<slug>.stage<N>.report.md`, written by `exp-batch`), and a results-merge step into the shared dashboard/table.

## 6. Hand off and review

- **Execution happens in separate agent sessions, one per stage or branch.** Like plan-brief: the campaign delivers a self-contained launcher prompt per stage; a fresh session reads the plan, adopts `exp-batch`, and implements + runs that stage. Never execute the campaign inside the planning session.
- Each launcher prompt carries: the cells this stage must fill, exact configs/commands, the metric contract, stop conditions, and the gate observations to report back. The executor follows the plan rather than re-grilling settled decisions; it stops and asks when evidence invalidates the plan.
- **State the waiting arrangement in every launcher prompt.** Either the researcher has already delegated execution — say so explicitly ("you may launch runs and use the `later` tool to wait unattended") — or the executing agent must ask for delegation at stage start. With delegation and a host that provides the `later` tool, the executor runs long jobs in the background, schedules its own wake-up with ~10% margin (prompt written as a complete next-step instruction), and ends the turn; wake-ups chain until the stage's gate observations are collected, re-estimating from observed progress whenever a run overruns rather than trusting the original plan. This keeps multi-hour stages unattended; without it, the executor stops at every long run to wait for a human.
- **Who launches formal runs is the researcher's call**, not the plan's: the executing agent implements code and preflights; the researcher either runs formal commands themselves or grants execution permission explicitly. The plan must state which commands are formal.
- **When a stage's report returns, this session owns the next move** — the researcher is the courier, so do not wait for an automatic ping. Read `<slug>.stage<N>.report.md` (not chat memory), compare predicted vs observed at every gate, write the decision into the pruning ledger (`gate N: observed X → keep / skip cells …`), reopen the cells a failed probe assumption justified and say so loudly, then emit the stage N+1 launcher prompt, replacing the pre-written branch variant it supersedes.
- **Exit:** the campaign closes when every surviving cell has a row in the shared table and each figure in the figure list can be drawn from it. Then record `Status: done (stages: N)` at the top of the plan, state what was pruned and by which evidence, hand the negative results to the researcher, and stop opening branches. If a gate leaves the claim unresolved after the confirmatory stage, hand the open question back instead of adding stages.
- Final review: does the metrics table/figure set answer the original claim? Are negative results and config deviations visible? Publish to the shared dashboard with both callback and reload surfaces where they exist.

## 7. Code organization (planned here, implemented by exp-batch)

The plan decides *where* code lives so every later branch lands consistently:

- **Module placement is a decision, name it:** which existing module each piece belongs in, what stays in the experiment's own directory. No new shared abstraction for a single consumer; but do separate concerns into separate modules when two branches would otherwise edit the same file in different ways.
- **Experiment directory isolation:** each experiment gets its own directory with a predictable layout, so a run can be found by name alone (scripts, configs, outputs mirror each other). Experiments never reach into another experiment's directory.
- **Loose coupling over convenience:** experiments consume stable shared libraries through their existing interfaces; an experiment must not modify shared internals to fit its needs, and shared libraries must not grow experiment-specific branches. If the shared interface genuinely lacks something, that gap is a plan-level decision, not a drive-by edit.
- **Ponytail research code:** the minimum code that runs the experiment correctly. **No defensive programming** — no speculative input validation, no "just in case" branches, no swallowed errors. On error, exit with the real error. Post-mortem decides whether the fix is code or environment (device contention, full disk, stale cache); often the code is already right.

## Hard boundaries

- Never present pruned space as "ran and failed"; pruned means "not run, because probe P showed X".
- Never let the plan claim equivalence of configurations without a measured comparison.
- A campaign plan is not permission to launch formal runs; follow the project's rules on who runs what.
