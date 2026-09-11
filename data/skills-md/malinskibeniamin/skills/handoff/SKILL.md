---
name: handoff
description: Compact the current session into a handoff document for another agent or fresh session.
argument-hint: What should the next session focus on?
disable-model-invocation: true
---

For auditing another run use `/agent-watchdog`; for competing plans suggest `/plan-arbiter`. Create only continuation context.

## Procedure

1. `handoff_file=$(mktemp -t handoff-XXXXXX.md)`.
2. Do not duplicate artifacts. Link specs, plans, ADRs, issues, commits, diffs, and docs.
3. Treat arguments as next-session focus.
4. Redact credentials, secrets, personal/customer data; note redaction only when continuation is affected.
5. Suggest useful next skills.
6. Return only path plus 1-2 sentence summary.

If the user explicitly wants a fresh background agent now, do not save a file: check `command -v claude`, then run `claude --bg --name "<descriptive name>" "<handoff summary>"`. On failure/unavailability, never claim it started; return exact command and summary. Include `/agent-watchdog` when its claims need verification.

## Template

```markdown
# Handoff
## Next session focus
<first objective>
## Current state
<branch, cwd, PR/issue, required facts>
## Decisions made
<linked bullets>
## Open questions
<bullets or None>
## Next actions
1. <action>
2. <verification/shipping>
## Relevant artifacts
- <path/URL>: <purpose>
## Suggested skills
- </skill>: <why>
```

## Guardrails

Do not summarize everything. Prefer references over pasted text, redact sensitive data, and label uncertainty. If no useful work happened, write a short starter brief.
