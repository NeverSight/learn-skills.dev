---
name: orchestration-and-backfills
description: Designs scheduling, reruns, and backfills safely for data systems. Use when changing orchestration, retries, dependency timing, historical reprocessing, or publish sequencing.
---

# Orchestration And Backfills

## Overview

Reliable data systems are shaped as much by rerun behavior as by transformation logic. This skill ensures schedules, retries, and backfills are deliberate, safe, and reversible.

## When to Use

- adding or changing a scheduled pipeline
- designing retries or failure handling
- introducing a new dependency chain
- reprocessing historical data
- modifying publish windows or cutover behavior

## Workflow

1. Define execution semantics.
   Specify:
   - schedule or trigger type
   - watermark behavior
   - late-arriving data policy
   - idempotency guarantees
   - retry rules
   - failure notification path

2. Separate normal runs from backfills.
   Historical reprocessing should not silently behave like daily incremental runs unless that has been proven safe.
   For `/backfill` or publish-bound replay, load `safe-backfill-and-replay-orchestration` first and complete `templates/backfill-plan.yaml` before execution.

3. Design the recovery path before rollout.
   Include:
   - restart behavior
   - partial failure handling
   - duplicate prevention
   - publish gating
   - rollback or pause steps

4. Estimate cost and blast radius.
   Backfills can overload warehouses, queues, clusters, or downstream consumers.

5. Prove the run strategy.
   Use a dry run, limited slice, or non-production environment when possible.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "The scheduler will handle retries for us." | Default retries may duplicate writes or hide real data issues. |
| "Backfill is just rerunning the job for older dates." | Historical loads often need different concurrency, checks, and cutover rules. |
| "We can figure out rollback during the incident." | Recovery plans created during outage pressure are usually incomplete. |

## Red Flags

- no idempotency strategy is documented
- backfill and incremental logic are conflated
- downstream consumers are not considered during replay
- recovery steps are absent from the plan

## Verification

- [ ] Execution, retry, and replay rules are documented
- [ ] Backfill behavior is explicitly designed and bounded
- [ ] A recovery path exists for partial or failed runs
- [ ] Rollout risk and cost impact have been considered
