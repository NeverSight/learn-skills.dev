---
name: principle-prove-it-works
description: "Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'"
---

# Prove It Works

Verify every task output by checking the real thing directly. Do not infer from proxies, self-reports, or "it compiles."

**Why:** Unverified work has unknown correctness. Indirect verification (file mtimes, output freshness, agent self-reports, cached screenshots) feels cheaper than direct observation. Acting on a wrong inference costs far more than checking the source.

Check the real thing, not a proxy:
- Check process liveness directly, not indirectly through derived state
- Read the actual value, not a cached or derived representation
- When verification fails, suspect the observation method before suspecting the system

## Account for the accepted scope

Check against the original accepted requirements. A plan, summary, or delegation cannot silently narrow them. Link each requirement to evidence or an explicit gap in the existing task record. An unmet requirement prevents a full completion claim. Preserve any `backstop` or `judgment` tags and record authorized scope changes separately. Reuse a runner's record when one exists.

When the work includes a threat model or security review, reconcile every declared threat with mitigation evidence at the threatened boundary. A claim of mitigation is not evidence. Record accepted risk with its authorized owner, transferred responsibility with its owner and evidence, or an open gap. Unresolved threats stay visible in the completion verdict.

## Tie proof to the result

Record the artifact each check exercised, its revision when applicable, and the relevant environment. After combining changes, rerun checks for the affected paths on the integrated result. Separate passing branches do not prove their combination.

Run a named acceptance helper when the task or project requires it. If it cannot run, report the gap. Justify any replacement against the same acceptance criteria before treating it as equivalent.

## Script the check when you can

The strongest proof is a deterministic script that re-runs the same comparison, not a one-time eyeball. Write the script, run it, and keep its output as an artifact a reviewer can re-run instead of trusting your word.

Keep the artifact visible for the human. Commit it only for large or complex work where the trail has to be auditable later, like a big port or migration (the **show-me-your-work** skill).
