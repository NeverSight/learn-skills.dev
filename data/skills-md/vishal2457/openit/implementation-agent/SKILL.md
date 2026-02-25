---
name: implementation-agent
version: 2.1.0
description: Implements tracker subtasks tagged `implement`, publishes/updates the PR, and routes review using handoff-first context loading, lazy artifact reads, and rework_mode support.
---

# Implementation Agent

## Purpose

Implement the parent issue by executing planned implementation subtasks and handling PR publication in the same run with token-efficient context loading and auditable stage handoff.

## Runtime Configuration

- Read `/orchestra-config.json` from the repository root before starting.
- Read `issue_tracker` and use only the configured tracker MCP for ticket operations.
- Use the MCP mapped to `issue_tracker` in `orchestra-config.json`.
- If the configured issue tracker MCP is unavailable, stop immediately and do not proceed with the task.
- For every task/comment/status update written to the tracker, include: `Skill-Version: implementation-agent@2.1.0`.
- Immediately stop if `gh` CLI is unavailable.

## When to Invoke

- After planning is complete on the parent issue.
- After PR review requests implementation rework.

## Required Inputs

- Parent issue ID.
- Parent issue status is `In-progress`.
- Parent issue has tag `planning-done`.
- Child subtasks tagged `implement`.
- Most recent prior handoff comment in `<!-- OPEN-ORCHESTRA-HANDOFF -->` format.

## Outputs

- Code changes implementing all completable `implement` subtasks.
- Git branch created as: `codex/<issue-id>-<short-description>`.
- Each completed subtask marked done in the configured issue tracker.
- Comment on each incomplete subtask explaining why it was not completed.
- Build and lint outcomes recorded in the configured issue tracker as command + pass/fail, with short error excerpts only when failing.
- Branch pushed to remote when work is complete.
- Pull request created (first pass) or updated (rework pass) and linked to the configured tracker issue.
- Parent issue status moved to `In review` after successful publish/update.
- Parent issue tags:
- `implementation-done` when implementation is complete.
- `pr-published` when PR is created or updated and linked.
- `open-implementation-questions` when implementation is blocked.
- A handoff comment wrapped exactly as:

<!-- OPEN-ORCHESTRA-HANDOFF -->
```JSON
{
  "execution_trace": "Execution-Trace:\nActions:\n1. <action>\n2. <action>\nDecisions:\n- <decision + reason>\nReferences:\n- <source artifact or command>\nAssumptions:\n- <assumption>\nOpen-Questions: none|<question list>\nSkill-Version: implementation-agent@2.1.0",
  "handoff_summary": {
    "from_skill": "implementation-agent",
    "to_skill": "pr-review-agent",
    "status": "ready|blocked",
    "delta": ["<what changed in this implementation pass>"],
    "key_decisions": [{"decision": "<decision>", "reason": "<reason>"}],
    "relevant_artifacts": [
      {
        "artifact": "<artifact name>",
        "hash": "sha256:<hash>",
        "last_modified": "<ISO-8601>",
        "summary": "<short relevance summary>"
      }
    ],
    "open_blockers": [{"blocker": "<text>", "owner": "<owner>", "next_action": "<next action>"}],
    "next_guidance": {
      "need_full": ["<artifact names needed by next skill>"],
      "focus": ["<highest-priority checks for next skill>"],
      "findings": [{"id": "<finding-id>", "file": "<path>", "action": "<required fix/check>"}]
    }
  }
}
```

- `handoff_summary` must be <= 600 tokens.

## Context Gathering Order (Strict)

1. Locate the most recent comment containing `<!-- OPEN-ORCHESTRA-HANDOFF -->` from the previous skill.
2. Parse the JSON inside it; treat `handoff_summary` as primary context.
3. Review `relevant_artifacts` and hashes first.
4. Declare exactly which artifacts require full reads with `need_full`.
5. Read full content only if hash changed or the task cannot proceed without it.
6. Do not read entire issue history or all prior execution traces by default.

## Procedure

1. Read `/orchestra-config.json`, set issue tracker context, and verify the configured tracker MCP is available.
2. Execute the strict context gathering order above.
3. Validate prerequisites: parent issue status is `In-progress` and parent has `planning-done`.
4. Determine mode:
- `standard_mode`: previous handoff is from planning/earlier implementation stage.
- `rework_mode`: previous handoff is from `pr-review-agent` and includes `next_guidance.findings`.
5. In `rework_mode`, read only:
- `next_guidance.findings` from the review handoff.
- affected `implement` subtasks referenced by those findings.
- additional artifacts only if explicitly declared in `need_full`.
6. Create a git branch named `codex/<issue-id>-<short-description>` if one is not already active.
7. Implement subtasks in listed order for `standard_mode`, or implement only finding-scoped fixes in `rework_mode`.
8. After finishing work, mark completed subtasks done and add blocker comments for any incomplete subtask.
9. Detect build and lint commands from repository config (for example `package.json`, `Makefile`, or equivalent).
10. Run build and lint commands and record concise results.
11. If implementation is blocked:
- Add `open-implementation-questions`.
- Post handoff JSON with `status: blocked` and concrete `open_blockers`.
- Stop and wait for clarifications.
12. If implementation is complete:
- Remove `open-implementation-questions` if present.
- Add tag `implementation-done`.
- Optionally keep legacy tag `implemented` during migration windows.
- Push branch to origin (`git push -u origin <branch>`).
- If linked PR already exists (typical `rework_mode`), update the existing PR context/comments.
- Otherwise create a PR targeting the base branch and include tracker issue ID/URL.
- Ensure parent issue tag `pr-published` is present.
- Add concise parent issue comment with PR URL and short review request.
- Move parent issue status to `In review`.
- Post handoff JSON with `to_skill: pr-review-agent` and `status: ready`.
13. Invoke `pr-review-agent` with the same parent issue ID unless `open-implementation-questions` is present.

## Guardrails

- Do not start implementation unless parent issue has `planning-done` and status `In-progress`.
- Do not execute subtasks that are not tagged `implement`.
- Do not change scope outside planned subtasks without explicit tracker approval.
- Do not leave incomplete subtasks without a blocker comment.
- Do not run tracker operations unless the MCP for the configured `issue_tracker` is available.
- Do not paste full command output (for example full `pnpm list` or `pnpm build` logs) into tracker or PR comments.
- Do not reconstruct state by reading full comment history; use handoff summary first, then lazy-load only required artifacts.
- Do not create or update a PR if there are no committed changes from this implementation pass.
- Do not move issue status to `In review` until PR creation/update succeeds.
- Ensure the PR references the correct tracker issue ID and URL.

## Handoff

Primary consumer: `pr-review-agent` (auto-invoke when unblocked).
