---
name: incident-response
description: |
  Investigate, fix, postmortem, prevent.
  Full incident lifecycle from bug report to systemic prevention.
  Use when: production down, critical bug, incident response, post-incident review.
  Composes: /investigate, /fix, /postmortem, /codify-learning.
argument-hint: <bug-report>
effort: max
---

# /incident-response

Fix the fire. Then prevent the next one.

## Role

Incident commander running the response lifecycle.

## Objective

Resolve the incident described in `$ARGUMENTS`. Fix it, verify it, learn from it, prevent recurrence.

## Latitude

- Multi-AI investigation: Codex (stack traces), Gemini (research), Thinktank (validate hypothesis)
- Create branch immediately: `fix/incident-$(date +%Y%m%d-%H%M)`
- Demand observable proof — never trust "should work"

## Workflow

1. **Triage** — Parse Sentry context if available (stack trace, file paths, breadcrumbs, affected users)
2. **Investigate** — `/investigate $ARGUMENTS` (creates INCIDENT.md with timeline, evidence, root cause)
   - If issue body contains Sentry link: query via Sentry MCP for full context
   - `git log --oneline -10` on affected files to identify causal PR/commit
3. **Branch** — `fix/incident-$(date +%Y%m%d-%H%M)` from main
4. **Reproduce** — Write failing test that reproduces the error BEFORE fixing
5. **Fix** — `/fix "Root cause from investigation"` (Codex delegation + verify)
6. **Verify** — Observable proof: log entries, metrics, database state. Mark UNVERIFIED until confirmed.
7. **Auto-revert check** — If fix cannot be verified within 30 min, revert the causal commit:
   ```bash
   git revert <causal-commit> --no-edit
   git push
   ```
8. **Postmortem** — `/postmortem` (blameless: summary, timeline, 5 Whys, follow-ups)
9. **Prevent** — If systemic: create prevention issue, optionally `/autopilot` it
10. **Codify** — `/codify-learning` (regression test, agent update, monitoring rule)

## Sentry Integration

When the issue body contains Sentry context (auto-filed by Sentry-GitHub integration):
- Extract stack trace, file paths, breadcrumbs from issue body
- Use Sentry MCP to query full event details if available
- Cross-reference affected files with `git log` to find causal commit
- Include Sentry issue link in PR description for auto-resolution on deploy

## Auto-Detected Issues

Issues labeled `auto-detected` + `bug` are created by the observability pipeline.
The flywheel coordinator prioritizes these and routes them here.
Treat as P0 unless evidence suggests otherwise.

## Output

Incident resolved, postmortem filed, prevention issue created (if applicable).
PR includes `fixes #<issue>` for Sentry auto-resolution on deploy.
