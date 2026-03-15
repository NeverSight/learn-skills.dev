---
name: multi-review-aggregation
description: Use when dispatching code reviews for tiers with N greater than 1 (max-20x, max-5x) in subagent-driven development, or manually for critical changes over 200 lines or security-sensitive code
---

# Multi-Review Aggregation

Dispatch N independent code reviews and aggregate findings. Each reviewer catches different bugs -- union preserves the long tail that single-shot misses.

**Research basis:** SWR-Bench (arXiv 2509.01494) -- N independent reviews: 43.67% F1 improvement, 118.83% recall improvement. Diminishing returns past N=5; N=3 captures most improvement.

**Core principle:** Independence via separate Task dispatches -- same base prompt, no shared context.

## N Selection by Tier

| Tier | N Reviews | Rationale |
|------|-----------|-----------|
| max-20x | 3 | Quality priority -- full aggregation |
| max-5x | 3 | Balanced -- same recall benefit |
| pro/api | 1 | Budget priority -- single review |

When N=1, skip this skill -- use standard single code review.

## Parallel Dispatch Pattern

After spec review passes, dispatch N independent reviews (`run_in_background=True`, each gets "Reviewer i of N"). Always aggregate when 2+ reviewers succeed — even unanimous approval may contain different Minor findings, Suggestions, or Not Checked items. Dispatch aggregator (haiku model).

Full dispatch code: see `references/dispatch-code.md`. Aggregator prompt: see `./aggregator-prompt.md`.

## Aggregation Algorithm

### Severity Voting

| Condition | Result |
|-----------|--------|
| All reviewers agree on severity | Keep that severity |
| Reviewers disagree | Use highest severity |
| **Lone finding** Critical or Important | **Keep original severity** (no downgrade) |
| **Lone finding** Minor | Downgrade to Suggestion |
| Lone finding BUT security or data-loss | **Keep original severity** (no downgrade) |

Severity levels: Critical > Important > Minor > Suggestion

### Verdict

- "Ready to merge: Yes" -- zero Critical AND zero Important AND majority approved
- "Ready to merge: With fixes" -- only Minor/Suggestion after aggregation
- "Ready to merge: No" -- any Critical or Important remain

Full deduplication/merging rules: see `references/aggregation-details.md`.

## Output Format

```
## Strengths
- [strength] [Reviewers: 1, 2, 3]

## Issues
### Critical / Important / Minor / Suggestion
- [issue] [Reviewers: N, N] -- file:line
  (note downgrade/security provenance as applicable)

## Uncovered Paths
- [path/scenario] [Reviewers: X, Y]

## Not Checked
- [area] [Reviewers: X, Y]

## Assessment
Ready to merge: [Yes/With fixes/No]
Reviewers: X/N approved, Y requested changes
```

Full format spec: see `references/output-provenance.md`.

## Red Flags

**Never:**
- Share context between reviewers (defeats independence)
- Use N>1 for pro/api tier (budget constraint)
- Skip aggregation when reviewers disagree
- Downgrade security findings even as lone findings

**Always:**
- Dispatch all N reviews in parallel
- Include reviewer number in each dispatch prompt
- Use haiku for aggregation
- Record per-reviewer metrics separately

## Reference Files

- `references/dispatch-code.md`: Full dispatch flow with on_spec_review_pass handler
- `references/aggregation-details.md`: Deduplication, strengths merging, malformed output, timeout recovery
- `references/output-provenance.md`: Provenance annotation rules and full output format spec
- `references/metrics-and-cost.md`: Per-reviewer metric keys, cost impact, per-tier breakdown
- `aggregator-prompt.md`: Aggregator Task dispatch prompt template

<!-- compressed: 2026-02-11, original: 673 words, compressed: 434 words -->
