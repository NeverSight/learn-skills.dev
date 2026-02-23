---
name: factory-review
description: >-
  Structures the human review experience for factory-mode builds. Audit trail
  summaries, PR digests, retrospective synthesis, quality trend tracking, and
  autonomy tuning interface. Activate during Phase 3 human review.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: [pipeline]
  context: [ci-results, git-history, task-state]
  phase: ship
  standalone: false
---

# Factory Review

**Value:** Communication -- factory mode concentrates the human's attention on
decisions that matter. This skill ensures the review interface is clear,
concise, and actionable so the human can provide meaningful oversight without
re-reading every line of code.

## Purpose

Structures the human review experience during Phase 3 of factory-mode builds.
Produces audit trail summaries, PR digests, retrospective synthesis, quality
trend reports, and an autonomy tuning interface. The goal is high-signal review
in minimal time.

## Practices

### Audit Trail Summary

Read from `.factory/audit-trail/` and present a concise build summary:

- **Slices completed:** Count and list (by slice ID and title)
- **Rework rate:** Percentage of slices that required rework cycles
- **Gate failure distribution:** Count of failures by gate type (tdd, review,
  ci, mutation)
- **Escalations pending:** Count and brief description of each unresolved
  escalation

Format as a dashboard-style summary. Lead with the numbers, follow with
details only if the human asks.

### PR Digest

For each merged PR in the build, produce a one-paragraph summary:

1. **What changed:** Feature or fix description in plain language
2. **Which slice:** The vertical slice ID this PR implements
3. **Which pair:** The two engineers who built it
4. **Gate results:** Pass/fail for each quality gate (tdd, review, ci,
   mutation)
5. **Rework count:** Number of rework cycles before all gates passed

Keep each digest to 3-5 sentences. The human should be able to scan all
PR digests in under a minute for a typical build session.

### Retrospective Synthesis

Aggregate findings from team retrospectives (stored in
`.factory/audit-trail/retrospectives/`) and surface patterns:

- **Recurring rework causes:** What kinds of issues triggered the most rework?
- **Pair effectiveness:** Which pairings produced the fewest rework cycles?
- **Domain hotspots:** Which areas of the domain model generated the most
  discussion or revision?
- **Process friction:** Any team-identified impediments or improvement
  suggestions

Present as bullet points grouped by theme. Do not editorialize -- report
what the team said.

### Quality Trend Tracking

Read from `.factory/audit-trail/metrics/` and present trends:

| Metric | Current | Previous | Trend |
|--------|---------|----------|-------|
| Mutation score | % | % | up/down/stable |
| Rework rate | % | % | up/down/stable |
| Cycle time per slice | duration | duration | up/down/stable |
| Gate failure rate by type | counts | counts | up/down/stable |

"Previous" means the last completed build session. If no previous session
exists, omit the comparison column.

### Tuning Interface

Accept adjustments to `.factory/config.yaml` during review. For each proposed
change:

1. **Validate:** Check that the change is consistent (e.g., cannot enable
   auto-merge at `conservative` autonomy level; cannot disable a gate that
   another setting depends on)
2. **Explain implications:** What will change in behavior if this setting is
   modified? Be specific.
3. **Apply or reject:** If valid, apply the change. If invalid, explain why
   and suggest the nearest valid alternative.

Never apply config changes silently. Always confirm with the human before
writing to `.factory/config.yaml`.

### Escalation Review

Present each pending escalation with full context:

1. **Which gate:** The quality gate that triggered the escalation
2. **Rework attempts:** How many rework cycles were attempted
3. **What was tried:** Brief summary of each rework attempt
4. **Current state:** What the code looks like now (diff or description)
5. **Recommendation:** The team's suggested resolution (if any)

The human decides: resolve, override, or send back for more rework.

## Enforcement Note

This skill provides advisory guidance for structuring the review experience.
It reads from audit trail files produced by the pipeline and presents them
in a human-friendly format. It cannot enforce that the human reviews every
item -- it can only make the review efficient and thorough.

## Verification

After completing a factory review session, verify:

- [ ] Audit trail summary was presented with current build metrics
- [ ] Every merged PR has a digest (no PRs skipped)
- [ ] Retrospective synthesis covers all team retrospectives from the session
- [ ] Quality trends include comparison to previous session (if available)
- [ ] All pending escalations were presented with full context
- [ ] Any config changes were validated before being applied
- [ ] Human confirmed or overrode each escalation

If any criterion is not met, revisit the relevant practice.

## Dependencies

This skill requires the `pipeline` skill for factory mode infrastructure.
It integrates with:

- **pipeline:** Reads audit trail files and metrics produced by the pipeline
  orchestrator during Phase 2
- **ensemble-team:** Retrospective synthesis reads team retro output;
  pair effectiveness data comes from pairing history
- **ci-integration:** Gate failure data includes CI_RESULT packets from
  the ci-integration skill

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill pipeline
```
