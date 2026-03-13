---
name: epic-verifier
description: Use when all implementation tasks in an epic are closed, before calling finishing-a-development-branch
---

# Epic Verifier

Dedicated verification agent for epic completion. Runs after all implementation tasks close, before finishing-a-development-branch. Builders build, verifiers verify -- separation prevents self-certification.

**REQUIRED BACKGROUND:** Read `superpowers-bd:verification-before-completion`, `superpowers-bd:rule-of-five-code`, and `superpowers-bd:rule-of-five-tests` SKILL.md files.

**Trigger:** All implementation tasks in epic show `status: closed`

**Do NOT use:** mid-epic (tasks still open), for single-task (use verification-before-completion), as substitute for per-task code review.

## Quick Reference

| Check | Question | Evidence Required |
|-------|----------|-------------------|
| **YAGNI** | Built only what requested? | List code not in plan |
| **Drift** | Matches spec? | Deviations with file:line |
| **Test Coverage** | Paths tested? | Untested functions |
| **Regressions** | All tests pass? | Test suite output |
| **Documentation** | Docs updated? | Outdated locations |
| **Security** | No vulnerabilities? | Concerns or "none" |
| **Rule-of-Five** | >50 line files reviewed? | Per-file 5-pass results |

## Dispatch

Use template at `./verifier-prompt.md`:

```
Task tool:
  subagent_type: "general-purpose"
  model: "sonnet"  # or "opus" for max-20x
  description: "Epic verification: {epic_id}"
  prompt: [use template]
```

Required context: `{epic_id}` (verifier self-reads from beads), base SHA, head SHA, test command.

## Model Selection

| Tier | Model | Rationale |
|------|-------|-----------|
| max-20x | opus | Catches subtle issues |
| max-5x | sonnet | Good quality/cost balance |
| pro/api | sonnet | Verification quality matters |

## Integration

Mandatory gate: all impl tasks closed -> dispatch epic-verifier -> PASS -> finishing-a-development-branch / FAIL -> fix and re-verify.

## Red Flags - Verification Theater

| Claim Without Evidence | Reject Because |
|------------------------|----------------|
| "YAGNI passed" | Must list what was compared |
| "Tests pass" | Must show test output |
| "No security issues" | Must list what was checked |
| "Rule-of-five done" | Must show per-file findings |

**Evidence missing = reject verification.**

## Reference Files

- `references/edge-cases.md`: Unusual epic shapes (no artifacts, no tests, review-only)
- `references/common-failures.md`: Verification being skipped or rubber-stamped
- `references/example-output.md`: Output format reference for verification report
- `references/why-separation-matters.md`: Pushback on why dedicated verifier is needed

<!-- compressed: 2026-02-11, original: 519 words, compressed: 327 words -->
