---
name: runtime-probes
description: "Apply when explicitly asked to probe, stress, fuzz, or chaos-test a product, feature, or PR for unreported bugs, including preparing a source-grounded handoff when the runtime is unavailable. Do not apply to ordinary static review or investigation of a known defect unless the request also asks for exploratory runtime probing. Two passes: a closed probe taxonomy, then a promotion gate that keeps only caller-reachable findings."
---

# Runtime probes

The twin of the **spec-probes** skill on the other side of the code. That one probes a requirement before anything runs. This one probes a running system or prepares a bounded runtime handoff when the target is not yet reachable.

Two failure modes shape the design. An unbounded probe run burns budget and returns noise. A promoted finding no caller can reach wastes a maintainer's day. Pass 1 bounds the search. Pass 2 bounds what escapes it.

## Before either pass

Name the scope, the surface, and the stop predicate, in that order.

**Scope.** A PR diff, one feature, or a whole product. For a diff, use the **blast-radius** skill for the change map, and probe what it names rather than re-deriving it.

**Surface.** Probes run against the real thing through the project's `verify-<app>` driver, which the **create-verification-skill** skill builds when the project has none. If that driver is absent, report the required verification surface as a blocker instead of inventing another route. A probe that never reached the running surface is `not run`, never a pass.

**Stop predicate.** Bound execution before it starts. Open-ended live exploration needs a task- or project-supplied budget and consequence floor. Report those two limits separately, preserving supplied values and naming either one that is absent. A caller-supplied finite action list is already bounded when its invocation count and termination condition or timeout are explicit. Never treat probes you selected or their count as a task-supplied budget, invocation limit, or finite authorization; a plan cannot supply its own execution limits. If an executable run is not bounded, stop and ask for the missing limit instead of inventing one or substituting different work. A plan for an unavailable runtime may proceed, but it must say which execution limits are still absent. The budget caps the search; the consequence floor defines which effects merit continued investigation and promotion. When a loop-governance suite is installed, hand it the outer loop and keep this skill as the method that loop runs.

Keep one runtime-probes-owned record outside the tree, with one row per probe. Each row names the entry point, category, probe, status, and either its observation and evidence IDs or the reason it did not run. A completed invocation needs its own evidence ID; a count is not evidence. If writes are forbidden, keep the same facts in the reply instead of creating the file. Use the **show-me-your-work** skill separately for its decision log.

## Pass 1: probe

During live execution, inventory the entry points, use their shapes to select relevant categories, and form bounded adversarial hypotheses. Adapt to observed results while staying inside the stated scope and stop predicate. A read-only query is never asked about interrupted sequences. The taxonomy is closed on purpose: eight categories cleared beat forty nobody finishes.

For plan-only or unavailable work, include only probes for which the task or source supplies a concrete condition and a place where the result could be observed. Preserve stated branches, boundaries, and outcomes without inventing order, timing, evidence, or extra categories. Classify from the condition the source actually states: wrong type or encoding is malformed input, abandonment before completion is interruption, and retry after completion is replay. Similar words or outcomes do not license a different category. Use the smallest set that distinguishes the source's behavior partitions. Mark these probes `not run` and state why they were not executed. If a requested probe lacks a condition or observable surface, record the missing fact rather than filling it in.

After a task-supplied finite work unit, disposition only the supplied work. Treat scope as an allow-list: contextual facts do not authorize analyzing, classifying, proposing, or requesting follow-up for adjacent scenarios. Bundled or precomputed adjacent results are context, not effects discovered by the authorized action. If the authorized action itself causes a material unexpected effect, record that effect once and ask before expanding. During live exploration, boundaries are starting points rather than a ceiling; adapt values and types to observed behavior within scope and budget.

| Category | Shapes | Adversarial question |
|---|---|---|
| Malformed input | `input` | What happens on the wrong type, wrong encoding, or a field the caller was never meant to send? |
| Extreme size | `input`, `resource` | What happens at zero, at one, at documented boundaries, and far past the largest realistic value? |
| Interrupted sequence | `sequence`, `state` | What survives when the operation is abandoned halfway by a closed tab, killed process, or dropped connection? |
| Repeat and replay | `sequence`, `state` | What happens on a double submit, back navigation, or retried request? |
| Stale state | `state` | What happens when the client acts on state the server has since changed? |
| Dependency failure | `boundary` | What does the caller see when a dependency errors, returns nothing, or disappears? |
| Dependency slowness | `boundary`, `resource` | What happens when a call takes ten seconds instead of ten milliseconds? |
| Concurrent actors | `concurrency`, `state` | What happens when two actors touch the same record, file, or key at once? |

For an open-ended run, use the **swarm** skill to fan the probes out, partitioned by entry point. That skill resolves its own worker model and effort, so do not restate the choice here. Workers report `PASS`, `ISSUES`, or `BLOCKED` with evidence, which is swarm's own contract. Do not mint a second one.

For caller-supplied finite work, run only the supplied effectful actions and preserve their order and meaning. Read-only inspection of supplied files is allowed, but it is not probe evidence and cannot expand scope, add a replay, or support an adjacent disposition. Unless concurrency is explicit, issue one action, observe its result, then decide whether the next action remains authorized. A literal command is the entire invocation, not a prefix: run it as written, once. If its required execution context is unavailable, report the blocker instead of trying a wrapper, substitute, or retry. Record each invocation separately.

During executed runtime work, an entry point with no matching shape gets one soft "unclassified, probe by hand" row, not silence. Do not add this row to a plan-only or unavailable reply.

## Pass 2: promote

Every finding is a hypothesis. Judge each on your configured `judgment and prose` model and its configured effort. Use the **pstack-harness** skill to resolve them. A finding promotes only when all three hold.

1. **It reproduces.** For live work, the harness replays it from a clean start and it fails again. For a disposition-only task, task-supplied completed observations are the execution evidence the task authorizes; do not demand a replay the task forbids. A finding with neither a clean replay nor supplied completed evidence does not promote.
2. **A real caller can reach it.** Name the caller and the path from a real entry point to the failure. A supplied source statement that maps the executed driver or operation to that caller path is reachability evidence; do not require the probe to invoke the real entry point again or ask the maintainer to reconfirm a mapping the source already states. Strict reachability still means a defect behind a guard no caller gets past does not promote. Escalate when the source leaves the caller mapping or an applicable guard unresolved, not when it states the mapping directly.
3. **A maintainer would take the fix.** The consequence is user-visible, data-affecting, or crosses a security or privacy boundary. Internal untidiness is not a defect.

Triage every finding against the `fix` / `dismiss` / `ask` rubric in `../poteto-mode/references/bugbot-triage.md`, whose three verdicts are tagged on the states below. Record a learned dismissal pattern there in its own format instead of re-deriving it next run.

Each finding ends the run in exactly one state.

- **promoted** (`fix`): it clears all three conditions. It earns a regression test and a row in the issue list.
- **dismissed** (`dismiss`), with a reason. "Unreachable, the one caller validates this field against a bounded enum" is valid. Silence is not.
- **gap**: it reproduces but fails condition 2, and the row names the guard that makes it unreachable. Strict reachability buys a finding list nobody has to re-litigate. It costs you this row. Delete that guard later and the gap goes live, so the guard's name is the whole value of keeping the row. This state is produced by condition 2, not by the rubric, so it carries no rubric tag.
- **escalated** (`ask`): you cannot settle condition 2 or 3 yourself, and the finding touches security, privacy, auth, billing, data retention, or a permission boundary. Ask the user. Never spend an unsure call on a dismissal in those categories, which is that rubric's own standing rule. The run ends here for that finding, not the finding itself. Once the answer comes back it becomes promoted, dismissed, or a gap.

## Residue

After an executed run, the probe harness is the artifact. Commit it when the task authorizes repository changes so a reviewer can rerun it. For plan-only, unavailable, or read-only work, do not create or commit a harness; leave the bounded handoff in `findings.tsv` unless file changes are forbidden.

With explicit authority to add regression coverage, use the **poteto-tdd** skill. Each promoted finding becomes one failing test staged before its fix. With explicit authority to implement the fix, run the Bug fix playbook (`../poteto-mode/playbooks/bug-fix.md`), one finding at a time. Do not stage a test or begin a fix without that authority, and do not batch fixes into one commit.

A promoted test asserts an invariant, not a transcript. "Rejects a quantity below zero" survives a refactor. "Returns this exact error string for this exact byte sequence" does not. Use the **verify-commands** skill on every promoted test before it lands, because a generated test that passes green while measuring nothing is worse than no test at all.

Report the scope, surface, stop condition, work performed or left `not run`, evidence IDs, and final dispositions. When neither executed nor task-supplied completed evidence exists, report the blocker and missing facts without claiming a pass, finding, reproduction, or Pass 2 outcome. Name whether the probe record was written or kept inline.
