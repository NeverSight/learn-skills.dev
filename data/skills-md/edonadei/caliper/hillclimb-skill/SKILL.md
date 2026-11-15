---
name: hillclimb-skill
description: Improve a skill against its existing eval without supervision. Edits the SKILL.md one change a round and keeps a change only when held-out tasks improve too. Use when the user wants the agent itself to hillclimb a skill's eval score, or cut its token cost at the same score.
allowed-tools: Bash, Read, Write, Edit
---

# Hillclimb Skill

Improve a skill against its eval one **round** at a time: one change, one run, one verdict. Requires `caliper` (`pipx install caliper-eval` if missing) and `python3`. Commands, files, the cause list and the report: [REFERENCE.md](REFERENCE.md).

Three terms carry the method:

- **Train / held-out**: the tasks are split once. You read train failures; held-out tasks reach you as scores only. A change that lifts train alone has learned the tasks, not the job.
- **Noise floor**: how far a split's score moves between two runs of the same skill. A gain inside it is not a gain.
- **Keep / revert**: every round ends in one of the two, decided by the verdict table.

The spec and every results JSON are the answer key. Reach them only through `climb.py` and `caliper compare --format json`, and send each `caliper run`'s output to a log file.

## Entry point

`/hillclimb-skill [path]`: optional path to a `SKILL.md`; without one, use the `SKILL.md` in the cwd. Its eval is the `*.eval.yaml` beside it.

- **No eval**: stop and suggest `grill-skill`, which builds one.
- **Fewer than 8 tasks**: stop. There are too few to hold any out; suggest adding tasks with `grill-skill`.
- **A git-sourced skill**: stop. Only a path source can be edited.

## Phase 1 — Frame the climb

Read the `SKILL.md`. Ask one question at a time and wait for each answer:

1. **Objective**: a higher score, or a lower token cost at the same score?
2. **Surface**: the `description` (moves the activation score) or the body (moves the success rate)? One surface per climb, so a score that moves has one cause. Default: the `description` while execution tasks fail activation, the body after.
3. **Smallest gain worth keeping**, in percentage points. Default 10.
4. **Budget**: how many rounds. Default 6. State the cost first: each round is tasks × k agent sessions, and the baseline is two rounds' worth.

Then fix the engine for the whole climb: the same `--model`, `--judge-model` and user-customizations mode on every run. Prefer a judge that is a different model from the one tested.

**Wait for a go-ahead on the framing and the cost before the first run.**

## Phase 2 — Split and baseline

1. Validate the spec, then run the baseline twice at `k=5`.
2. Split from the first baseline with `climb.py split`. The split is fixed for the climb.
3. Score one baseline against the other. Each split's **noise floor** is the larger of that gap and two attempts' worth of the split.

Check the eval before climbing it:

| Signal | What it means | Do |
|---|---|---|
| Exit `2`, or unusable attempts | The environment, not the skill | Fix and re-run the baseline |
| Baseline at 95% or more on the objective's score | No headroom | Offer the cost objective, or stop |
| Noise floor above the smallest gain worth keeping | The eval can't see that gain | Raise `k` or add tasks; say which, and wait |
| A train task fails every attempt in both baselines | Likely the task or its grading | Note it for the reflection round |

A score objective also needs the **control** (`--ablate <skill-name>`, run once at the same `k`): reuse the one `grill-skill` kept, or run it now.

## Phase 3 — Rounds

Each round:

1. **Read** the train failures of the current best run (`climb.py failures`).
2. **Name one cause**: the most common one. Fix it at its root: rewrite the section that causes it, or add the rule that is missing. Write the rule in the skill's own terms, general enough for a request you have not seen. Wording from a task's prompt, `expect:`, assert or transcript stays out of the skill.
3. **Snapshot** the files you will edit, make the one change, run the whole spec, and score it against the current best run.
4. **Verdict**, then one line in the log: the cause, the change, both scores, kept or reverted.

Train must gain more than its noise floor. On held-out, *up* is any rise, *flat* is no change or a fall inside its noise floor, *down* is a fall beyond it.

| Train | Held-out | Verdict |
|---|---|---|
| Gains | Up | **Keep**: this run is the new best |
| Gains | Flat, already at 100% | **Keep** only if the change is a general rule: held-out has nothing left to show |
| Gains | Flat or down | **Revert**: the change learned the train tasks |
| No gain, or down | Any | **Revert** |

With a **cost objective**, keep a change when tokens per attempt fall by 5% or more and neither split falls beyond its noise floor from the *baseline*, so small losses can't add up. Look for cost in sections no train task exercises, repeated meaning, and reference that belongs in a sibling file.

**Two reverts in a row** make the next round a **reflection round**: no edit. Sort every remaining train failure by cause ([REFERENCE.md → Causes](REFERENCE.md#causes)). Only failures caused by the skill go into further rounds. If no single cause could gain more than the noise floor, stop.

A flawed task or grader is the user's to fix: show it with the fix you would make. A spec edit ends the climb, since the baseline, the control and the split are stale.

## Phase 4 — Finish

Stop when the budget is spent, the objective is met, no skill-caused train failure is left, or a reflection round says stop.

1. Restore the version with the best held-out score; on a tie, the one with fewer tokens per attempt.
2. Score it against the baseline, and `caliper compare` it against the control.
3. Report ([REFERENCE.md → Report](REFERENCE.md#report)): held-out is the result; train is shown beside it, labeled optimistic.
4. A held-out gain inside its noise floor is not a result. Say so, recommend against keeping the edits, and offer to restore the original.

Leave the edits uncommitted for the user to review.
