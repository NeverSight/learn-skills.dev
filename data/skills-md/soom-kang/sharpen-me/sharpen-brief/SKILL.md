---
name: sharpen-brief
license: MIT
description: Restore project context from current evidence after a gap or handoff. Use for changed outcomes, still-open blockers, and pending decisions; do not turn routine progress updates into a full project history or begin implementation.
---

# Sharpen Brief

Give the reader enough current context to act without remembering an earlier session. Report outcomes and evidence rather than the agent's activity.

## Inputs

Required: project or run scope and accessible evidence. Optional: last-known revision, run, date, prior decision, audience, and length. Default to a concise read-only briefing. Without a reliable baseline, provide a current snapshot rather than inventing a history.

## Procedure

1. Inspect relevant repository instructions, status, diffs, commits, run results, and maintained notes. Memory may locate evidence but cannot prove current completion. Respect supplied archives as captured state, not live state.
2. Verify any baseline. Neither mtime nor commit date establishes when the reader understood the project.
3. Use the baseline only to identify new changes. Include currently open blockers, risks, and unresolved decisions even when they predate it. Do not repeat old completed work as new.
4. Separate verified outcomes, pending work, blocked checks, and decisions. Local tests are not deployment or authenticated verification; a passing run proves its recorded checks, not every possible requirement. A recorded blocker need not be the only one.
5. Reconcile contradictory sources or state the conflict. Put uncertainty next to the conclusion it qualifies.
6. Lead with decisions the reader actually needs to make. If none exists, lead with the relevant status rather than manufacturing an ask. Explain unfamiliar terms briefly on first use and give the next action only when supported.

## Output and stopping

Follow the caller's format through the end of the response. If it requires a final JSON object or another machine-readable value, add no prose after it. Otherwise give a short, source-linked briefing: decisions or current status, meaningful changes since the baseline, still-open blockers, and material verification limits. Explain new terminology only where needed. Attach observation dates to status that may go stale. Do not force JSON fields, a glossary, or per-section expansion offers.

Stop once the requested scope is understandable or unavailable evidence prevents a reliable account. State missing sources instead of broadening indefinitely. Do not edit, choose product policy, send messages, or create monitoring jobs.

## Examples

- Since revision B a help text changed, while an earlier recovery blocker is still open: report the change and retain that blocker.
- Recent mtimes but no baseline: report current evidenced state without claiming changes occurred while the reader was away.
