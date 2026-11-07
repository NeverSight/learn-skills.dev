---
name: ds-swarm
description: "Fan out N parallel workers on slices of a job or on a race, collect every result, and return one evidence-backed report. Use for wide coverage, audits, races between approaches or exploration, or for /ds-swarm, 'swarm this', 'split this across workers'."
---

# ds-swarm

Split work that is wide but shallow across parallel workers, then merge their proven results into one report.

## Steps

1. State the done condition and the report the swarm must return.
2. Pick the shape. Partition the job into non-overlapping slices, or race N workers on the same brief, or both. For a race, decide up front how you will choose: first pass, rank all, or best one.
3. Write one brief per worker that stands alone: goal, exact slice, how to verify, what to report. When workers test specific commits, name the exact commit hashes and the measurement method.
4. Give every worker that writes files its own output location.
5. Spawn all workers at once. If the harness cannot run subagents, run the briefs one by one in fresh contexts.
6. Each worker reports PASS, ISSUES or BLOCKED with evidence: commands run and their output. ISSUES lists every provable issue, not just the first.
7. Collect results. Reject any result with no evidence or the wrong commit and respawn that worker once. A second miss is a recorded gap, not a pass.
8. Merge into one report: the verdict, each slice or arm with its evidence, gaps, and duplicates merged by root cause.

## Stop when

- Every slice has a result or a recorded gap and the report is written.
- Or a race has a winner under the rule from step 2.
- Never respawn a worker more than once.

## Rules

- Workers do not share writable state.
- A missing slice is never counted as passing.
- Report what workers proved, not what they claimed.
