---
name: fusion-skill-self-report-bug
description: Capture Fusion skill workflow failure context and guide a draft-first bug reporting flow with explicit confirmation before any GitHub mutation.
license: MIT
metadata:
  version: "0.1.0"
  tags:
    - github
    - issue-authoring
    - reliability
    - automation
  mcp:
    required:
      - github
---

# Self-report Fusion Skill Bugs

## When to use

Use this skill when a Fusion skill workflow fails and you need a consistent, triage-ready bug report draft.
Treat this as the default failure handoff for any `fusion-*` skill execution.

Typical triggers:
- "a fusion-* skill failed"
- "this skill run failed"
- "self-report this skill error"
- "create a bug from this workflow failure"
- "capture this automation failure for triage"

## When not to use

Do not use this skill for:
- Feature requests or roadmap planning
- General implementation tasks without observed failure
- Publishing GitHub changes without explicit user confirmation

## Required inputs

Collect before drafting:
- Target repository for the bug report (default: `equinor/fusion-skills`)
- Failing command or workflow step
- Environment context (OS/shell/runtime/tooling versions if available)
- Observed output/error evidence
- Reproduction signal (exact steps or best-effort notes)
- Optional parent issue number for linking

## Instructions

1. Detect or confirm failure intent.
   - If failure context is missing, ask for command used, expected behavior, actual behavior, and key error output.
2. Capture failure context.
   - Normalize context into: command, environment, observed error/output, reproducibility, and impact.
3. Draft locally first.
   - Write `.tmp/BUG-skill-failure-<context>.md` using `assets/issue-templates/skill-workflow-failure-bug.md`.
   - Include reproducible steps and explicit observed/expected behavior.
4. Propose issue metadata.
   - Recommend issue type: `Bug`.
   - Recommend labels for reliability/automation triage (for example `bug`, `automation`, `reliability`), then validate labels against the target repository before mutation.
   - Ask assignee preference (`@me`, specific user, or unassigned).
5. Offer optional relationship linking.
   - If parent issue is provided, prepare to link the new bug as a sub-issue after issue creation.
6. Ask explicit publish confirmation.
   - Do not run any GitHub mutation until the user explicitly confirms publish.
7. Mutate only after confirmation.
   - Create issue via MCP issue mutation.
   - Apply labels/assignee.
   - If parent issue was provided, link as sub-issue.
8. If confirmation is not provided, stop after draft.
   - Return status `No GitHub state changes made`.

## Expected output

Return:
- Draft bug report file path under `.tmp/`
- Captured failure-context summary (command, environment, observed output)
- Proposed title/body and reproduction steps
- Proposed issue type + labels + assignee plan
- Optional parent issue linking plan
- Explicit status: `Awaiting publish confirmation` or `No GitHub state changes made`
- Created issue URL/number only after confirmed mutation

## Safety & constraints

Never:
- Perform GitHub create/edit/comment/close actions without explicit confirmation
- Claim failure evidence that was not provided or observed
- Request or expose secrets/credentials

Always:
- Keep draft-first behavior
- Prefer minimal reproducible detail over long narrative
- Validate label existence in the target repository before applying
