---
name: pr-review-agent
version: 2.0.0
description: Runs a diff-first PR review with handoff-first context loading, lazy spec extraction, architecture-impact detection, and compact review-to-implementation findings handoff.
---

# PR Review Agent

## Purpose

Run a focused PR review that starts from changed code, validates only relevant requirements/spec sections, and reports blocking risks with minimal token use.

## Runtime Configuration

- Read `/orchestra-config.json` from the repository root before starting.
- Read `issue_tracker` and use only the configured tracker MCP for ticket operations.
- Use the MCP mapped to `issue_tracker` in `orchestra-config.json`.
- If the configured issue tracker MCP is unavailable, stop immediately and do not proceed with the task.
- For every tracker comment/status update, include: `Skill-Version: pr-review-agent@2.0.0`.

## When to Invoke

- When a PR is ready for review and linked to an issue.

## Required Inputs

- Parent issue ID.
- Parent issue tag `pr-published`.
- Linked PR and PR diff / changed files.
- Most recent prior handoff comment in `<!-- OPEN-ORCHESTRA-HANDOFF -->` format.

## Outputs

- PR comment:
- Short review summary.
- Findings that require changes (if any), tied to changed code.
- Issue tracker comment:
- Short review summary.
- Required changes checklist (if any).
- Status update:
- `In Progress` when changes are required.
- `Done` when changes are acceptable.
- Optional invocation:
- `init-architect` with scoped context when architecture-impacting changes are detected.
- Parent issue tags:
- `pr-reviewed` when review is clean.
- `open-pr-review-questions` when review is blocked by missing context.
- A handoff comment wrapped exactly as:

<!-- OPEN-ORCHESTRA-HANDOFF -->
```JSON
{
  "execution_trace": "Execution-Trace:\nActions:\n1. <action>\n2. <action>\nDecisions:\n- <review decision + reason>\nReferences:\n- <PR diff or requirement artifact>\nAssumptions:\n- <assumption>\nOpen-Questions: none|<question list>\nSkill-Version: pr-review-agent@2.0.0",
  "handoff_summary": {
    "from_skill": "pr-review-agent",
    "to_skill": "implementation-agent|none",
    "status": "ready|blocked|completed",
    "delta": ["<new findings or closure updates from this review pass>"],
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
      "need_full": ["<artifact names implementation must fully read>"],
      "focus": ["<highest-priority fix/check items>"],
      "findings": [
        {
          "id": "<finding-id>",
          "severity": "high|medium|low",
          "file": "<path>",
          "problem": "<what is wrong>",
          "required_change": "<what to change>",
          "affected_subtasks": ["<subtask identifier>"]
        }
      ]
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
5. Read full content only if hash changed or review cannot proceed without it.
6. Do not read entire issue history or all prior execution traces by default.

## Procedure (Diff-First)

1. Read `/orchestra-config.json`, set tracker context, and verify the configured issue tracker MCP is available.
2. Validate parent issue has tag `pr-published`.
3. Execute the strict context gathering order above.
4. Fetch PR diff and changed files first. This is the primary review input.
5. Build a minimal evidence set from the diff:
- modified modules and behaviors.
- affected API/data/auth/integration/runtime surfaces.
- acceptance criteria touched by changed code.
6. Based on step 5, declare `need_full` and fetch only relevant sections from:
- acceptance criteria.
- `technical-details`.
- other artifacts explicitly referenced by prior handoff.
7. Review only for correctness/regression risk in changed code and mismatch with the fetched relevant spec sections.
8. In the same pass, detect architecture impact from the PR diff. Impact is `true` when one or more of these is present:
- API contract changes.
- Data model/migration/index/persistence contract changes.
- Service/module boundary changes.
- Integration/event flow changes.
- Authn/authz/session/security boundary changes.
- Runtime/infrastructure behavior changes that alter topology or critical flows.
9. If architecture impact is `true`, prepare scoped payload for `init-architect`:
- parent issue ID.
- PR identifier/link.
- changed files list.
- concise diff summary.
- matched architecture-impact cases.
- suggested architecture doc sections to update.
10. Do not over-engineer:
- avoid style-only nits.
- report only issues that can cause bugs, regressions, broken behavior, or criteria mismatch.
11. Post a short PR comment with result and concise findings.
12. Post a short issue tracker comment with the same outcome summary.
13. If review is blocked by missing context:
- Add `open-pr-review-questions`.
- Post handoff JSON with `status: blocked` and explicit `open_blockers`.
- Stop and wait for clarifications.
14. If required code changes are found and review is not blocked:
- Remove `open-pr-review-questions` if present.
- Set issue status to `In Progress`.
- Post handoff JSON with `to_skill: implementation-agent`, `status: ready`, and `next_guidance.findings` populated.
- Invoke `implementation-agent` with the same parent issue ID.
15. If no required changes remain:
- Remove `open-pr-review-questions` if present.
- Add tag `pr-reviewed`.
- Set issue status to `Done`.
- Post handoff JSON with `to_skill: none` and `status: completed`.
16. If architecture impact is `true`, invoke `init-architect` with the scoped payload from step 9.

## Guardrails

- Use the PR diff as the first and primary source.
- Do not read the full repository for this review.
- Do not read entire issue history by default.
- Use handoff summary first, then lazy-load only required artifact sections.
- Prioritize correctness and functional risk over stylistic preferences.
- Keep findings actionable and tied to specific changed files.
- Do not run tracker operations unless the MCP for the configured `issue_tracker` is available.
- Keep PR and tracker comments concise; do not paste raw command logs.

## Handoff

Primary consumer: `implementation-agent` for fixes; review completes with `to_skill: none` when clean.
