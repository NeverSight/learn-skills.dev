---
name: init-architect
version: 2.0.0
description: Initializes and maintains architecture artifacts with handoff-first context loading, lazy scoped updates, and compact JSON handoff output for workflow-driven invocations.
---

# Init Architect

## Purpose

Run once after installing skills (and rerun when architecture drifts) to create or refresh architecture-folder artifacts used by `architect-agent`. Also supports scoped updates when invoked from `pr-review-agent` for architecture-impacting PR changes.

## Runtime Configuration

- Read `/orchestra-config.json` from the repository root before starting.
- If `/orchestra-config.json` is missing, create it at repository root with:
- `{ "issue_tracker": "linear" }`
- Read `issue_tracker` and use it for any generated tracker-facing instructions.
- Allowed `issue_tracker` values: `linear`, `jira`.
- For tracker comments in workflow-scoped mode, include: `Skill-Version: init-architect@2.0.0`.

## When to Invoke

- Immediately after skill installation, before running `architect-agent`.
- When architecture artifacts are stale after major system changes.
- When `pr-review-agent` flags architecture-impacting changes and provides scoped PR context.

## Required Inputs

- Repository root path.
- Invocation mode:
- `full` (default): repository analysis and full architecture refresh.
- `scoped`: targeted update using PR-derived scope.
- For `scoped` mode:
- parent issue ID.
- PR identifier/link.
- changed files list.
- concise diff summary.
- matched architecture-impact cases.
- suggested architecture sections.
- Optional existing `/architecture/architecture.md`.
- Optional existing `/architecture/docs/*.md`.
- Optional existing `skills/init-architect/ARCHITECTURE.md` template.
- Most recent prior handoff comment in `<!-- OPEN-ORCHESTRA-HANDOFF -->` format when running in workflow-scoped mode.

## Outputs

- `/orchestra-config.json` in repository root (created only if missing).
- `/architecture/architecture.md` populated as the architecture index.
- `/architecture/docs/*.md` populated for complex domains.
- In `scoped` mode: only impacted sections/documents are updated; unaffected sections remain unchanged.
- Optional targeted updates to `skills/architect-agent/SKILL.md` reference tables so runtime guidance matches generated docs.
- For workflow-scoped mode, a handoff comment wrapped exactly as:

<!-- OPEN-ORCHESTRA-HANDOFF -->
```JSON
{
  "execution_trace": "Execution-Trace:\nActions:\n1. <action>\n2. <action>\nDecisions:\n- <architecture update decision + reason>\nReferences:\n- <changed files or architecture docs>\nAssumptions:\n- <assumption>\nOpen-Questions: none|<question list>\nSkill-Version: init-architect@2.0.0",
  "handoff_summary": {
    "from_skill": "init-architect",
    "to_skill": "architect-agent|pr-review-agent",
    "status": "ready|blocked|completed",
    "delta": ["<what changed in architecture artifacts>"],
    "key_decisions": [{"decision": "<decision>", "reason": "<reason>"}],
    "relevant_artifacts": [
      {
        "artifact": "architecture-index-or-doc",
        "hash": "sha256:<hash>",
        "last_modified": "<ISO-8601>",
        "summary": "<updated sections and rationale>"
      }
    ],
    "open_blockers": [{"blocker": "<text>", "owner": "<owner>", "next_action": "<action>"}],
    "next_guidance": {
      "need_full": ["architecture/architecture.md"],
      "focus": ["<sections downstream agents must re-check>"]
    }
  }
}
```

- `handoff_summary` must be <= 600 tokens.

## Context Gathering Order (Strict)

1. Locate the most recent comment containing `<!-- OPEN-ORCHESTRA-HANDOFF -->` from the previous skill.
2. Parse the JSON inside it. This is your primary context.
3. Look at its `relevant_artifacts` list and hashes.
4. Declare exactly which artifacts you need via `need_full`.
5. Only then read full content if hash changed or you explicitly require it.
6. In non-workflow bootstrap mode with no prior handoff, continue with repository artifacts only.

## Procedure

1. Ensure `/orchestra-config.json` exists and has key `issue_tracker`.
2. Execute the strict context gathering order above when in workflow-scoped mode.
3. Ensure scaffold exists:
- `skills/init-architect/ARCHITECTURE.md`.
4. Ensure generated artifact paths exist:
- `/architecture/architecture.md`.
- `/architecture/docs/`.
5. If architecture content currently lives under `/ARCHITECTURE.md` or `/docs/`, migrate relevant content into `/architecture/` and stop updating legacy root-level copies.
6. Determine mode:
- If scoped payload is present, run `scoped` mode.
- Otherwise run `full` mode.
7. In `full` mode, analyze repository structure (do not read every source file):
- stack, entry points, boundaries, data layer, integrations, auth, sensitive areas, conventions.
8. In `full` mode, write/update `/architecture/architecture.md` as a concise index:
- system overview.
- component map.
- sensitive areas.
- conventions.
- reference docs table.
9. In `full` mode, create/update `/architecture/docs/*.md` only for domains that need detail beyond the index.
10. In `scoped` mode, use provided PR scope first and update only impacted architecture artifacts:
- map changed files and matched cases to existing sections in `/architecture/architecture.md`.
- update only relevant sections in `/architecture/architecture.md`.
- update or create only the necessary `/architecture/docs/*.md` files tied to those sections.
- keep unrelated sections/documents untouched.
11. In `scoped` mode, preserve current architecture structure and terminology unless the PR clearly introduces a new boundary or domain.
12. Keep index shallow; move depth to domain docs.
13. If generated docs change domain/sensitive-area mapping, update relevant sections in `skills/architect-agent/SKILL.md`.
14. In workflow-scoped mode, post handoff JSON with `status: completed` or `status: blocked`.

## Guardrails

- This skill owns architecture artifact generation; `architect-agent` must not regenerate architecture docs.
- Do not overwrite `skills/init-architect/ARCHITECTURE.md` template files.
- Keep generated architecture artifacts under `/architecture/` (`/architecture/architecture.md`, `/architecture/docs/*.md`).
- Prefer clarity over coverage; do not scan the full codebase unnecessarily.
- In `scoped` mode, do not perform a full repository rescan unless scoped context is insufficient.
- In `scoped` mode, prioritize consistency with existing architecture docs and produce minimal diffs.

## Handoff

Primary consumers: `architect-agent`, `pr-review-agent` (scoped invocation).
