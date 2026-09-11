---
name: setup-routines
disable-model-invocation: true
description: "Configure Claude Code routines for PR review, codebase health, issue triage, and docs drift."
---

Configure [Claude Code routines](https://claude.ai/code/routines): cloud sessions triggered by schedule, GitHub event, or API. **Enforcement model:** hooks and CLAUDE.md own standards; the prompt owns the task. Add `/agent-watchdog` for outputs; `/visual-recap` only when requested.

## Templates

| Template | Trigger | Result |
|---|---|---|
| [pr-review](routines/pr-review.md) | `pull_request.opened` | Review and inline comments |
| [pr-feedback-resolve](routines/pr-feedback-resolve.md) | `pull_request.review_submitted` | Fix/reply/resolve threads |
| [issue-triage](routines/issue-triage.md) | `issues.opened` | Classify, label, investigate |
| [weekly-health](routines/weekly-health.md) | weekly | Health report issue |
| [docs-drift](routines/docs-drift.md) | weekly | Stale-doc PR/issue |

## Setup

1. **Prerequisites:** Claude Code web access, GitHub connected through `/web-setup`, and eligible plan.
2. **Pick:** hooks -> pr-review; feedback skill -> pr-feedback-resolve; triage -> issue-triage; quality gates -> weekly-health; reference docs -> docs-drift.
3. **Web:** at [routines](https://claude.ai/code/routines), create; name; paste `routines/*.md` and fill `OWNER`/`REPO`; select repo/environment; choose event/schedule/API trigger; remove unused connectors; save.
4. **CLI schedule only:** `/schedule daily codebase health check at 9am`. GitHub/API triggers use web.
5. **Customize:** project checks, labels, scope, and connector actions. Keep stable prompts; repository rules evolve. See [REFERENCE.md](REFERENCE.md) for examples/API setup.
6. **Test once manually:** Web **Run now** or `/schedule run`; watch the returned session, inspect output, and tighten drift. See the reference for enforcement, triggers, and troubleshooting.

Routines must survive a closed laptop and pass the same PostToolUse/Stop gates as interactive work.
