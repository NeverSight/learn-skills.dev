---
name: agent-team
description: "Use when work splits into two or more independent parallel sub-agent tracks — exhaustive review or audit, inventorying an unknown-size surface, broad research needing cross-checked claims, codebase mapping, migration or sweep work, adversarial critique of a decision — or when the user asks to fan out, run a team, or cross-check work across independent agents. Near miss: a single bounded sub-agent task, work the main agent can finish in a handful of tool calls, and overlapping mutators without disjoint ownership or isolation."
---

# Agent Team

Run team-shaped work across sub-agents and deliver one synthesized result that states what was covered, what each material claim rests on, whether it was independently verified, and what remains a gap. Delegation is assumed authorized.

Orchestration mechanics — packet wording, parallel dispatch, pacing, how many agents run at once — are the model's own judgment. This skill fixes the bar the result must meet: honest coverage, independent verification of what the answer relies on, candidate-shaped decisions, and isolated mutators.

## Delegation

Delegate genuinely independent, sizeable tracks: wide investigations, noisy exploration where only a compact result matters, or work that benefits from an independent perspective. Keep local anything finishable in a handful of tool calls and any blocking decision the main agent must make now. When one sub-agent can cover a set of named roots, use one.

Before launch, state a short plan: the units, the named roots each covers, who verifies which claims, and the stop rule. Every packet carries the shared context agents would otherwise rediscover — systemic risk, invariants, known not-a-bug items — and asks for evidence with source pointers. Sub-agent reports are evidence, not truth.

## Hard Gate: Coverage

Activation: before launch, for any run whose answer speaks about a surface — audits, inventories, maps, sweeps, research.

Required:

- Evidence roots named before the unit count is set: files, symbols, interfaces, caller trees, sources, sites, or candidates. A pinned list is used as given; a surface of unknown size is inventoried until its roots are listed, or a named sample is recorded as a gap.
- Every packet names its roots and returns, per root, what was inspected and what was found.

Prohibited substitutes: a coarse label (subsystem, folder, epic) standing in for roots when finer roots are listable; roots left for the agent to discover inside a label; a per-root "nothing found" without what was inspected; a unit count taken from a preferred headcount.

Incomplete behavior: a root whose return is empty or evidence-free is re-dispatched once or named a coverage gap. When the inventory cannot be completed, sample with a named cap or return the plan with the missing fact named.

## Hard Gate: Independent Verification

Activation: before synthesis, for every run.

Must-verify claims:

- every claim the answer cites as a reason for its conclusion, decision, or ruling;
- every claim the answer presents as confirmed;
- in a review or audit, every blocker-severity finding;
- in a migration or sweep, each site or batch's verification command and output, plus an independent review of sites the command cannot observe, failed sites, and sites kept for human attention;
- in an open-discovery map or inventory, the completeness of the inventory.

Each must-verify claim passes through an independent lane — an agent other than the one that produced it — and ends `verified`, `refuted`, or `unresolved`. Every other claim enters the answer labeled `unverified`. Reports that conflict go to one targeted verifier; a conflict decidable by one mechanical observation (a file exists, a command prints a value) is settled by the parent citing that observation. A contested claim gets one re-check, and what survives it is `unresolved`.

Verifiers are read-mostly: a verifier that finds a defect returns a fix list, and a fix counts as resolved only after its own check.

Prohibited substitutes: the parent's own reading or lookup standing in for a verification lane; one verification packet that does not target each must-verify claim; a claim the answer cites as a reason, labeled instead of verified; a must-verify claim marked `unverified` in a result presented as complete.

Incomplete behavior: mark the result incomplete and name the unverified must-verify claims, or narrow the answer so they fall out of it.

## Hard Gate: Decision Shape

Activation: when the task is a choice among options — architecture, trade-off, prioritization, recommendation.

Required: one unit per mutually exclusive whole candidate, with a proposer only when a candidate needs construction or strengthening. Each serious candidate is attacked by its own independent critic; conflicting critics go to a judge. When the user asks for adversarial critique, each critique lens runs under its own owner against every candidate. The ruling names why the losing candidates lost.

Prohibited substitutes: units split by analysis angle, facet, or criterion; one shared review spanning candidates; under an adversarial-critique request, one reviewer carrying several lenses.

Incomplete behavior: re-split the work into candidates before launch, or return without a ruling and name what is missing.

## Hard Gate: Mutator Isolation

Activation: before launching any sub-agent that edits.

Required: each mutator owns disjoint paths or works in an isolated copy, with the boundary named in its packet.

Prohibited substitutes: overlapping ownership resolved by "be careful" instructions or by ordering assumptions between concurrent agents.

Incomplete behavior: serialize the overlapping edits or isolate them before launch.

## Synthesis

The final answer, in the user's requested format, contains:

- whether the run is complete or incomplete — incomplete is a valid result;
- the conclusion, decision, or findings;
- the load-bearing claims, each with its evidence and status;
- coverage: the roots, candidates, sources, or sites inspected;
- gaps: skipped scope, samples, caps, failed agents, unresolved claims, and why the team stopped.

A positive absence claim (no issues, safe to proceed, fully covered) requires a closed inspect list; unexamined surface stays in the gaps. The run stops when the requested scope is covered and every must-verify claim has a final status, or when the same blocker recurs without new evidence — then it stops with the remainder named.

Prohibited substitutes: a clean conclusion over unexamined surface; pasted sub-agent reports in place of a synthesis.
