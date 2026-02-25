---
name: triage-agent
version: 1.0.0
description: Performs lightweight workflow triage on a parent issue, classifies execution track as trivial|standard|complex, sets skip_steps guidance, and emits a compact handoff summary for downstream agents without reading full issue history.
---

# Triage Agent

## Purpose

Classify incoming work into `trivial`, `standard`, or `complex` track and define `skip_steps` guidance so downstream skills can run with minimal context and token cost.

## Runtime Configuration

- Read `/orchestra-config.json` from the repository root before starting.
- Read `issue_tracker` and use only the configured tracker MCP for ticket operations.
- Use the MCP mapped to `issue_tracker` in `orchestra-config.json`.
- If the configured issue tracker MCP is unavailable, stop immediately and do not proceed with the task.
- For every task/comment/status update written to the tracker, include: `Skill-Version: triage-agent@1.0.0`.

## When to Invoke

- After a parent issue already exists in the tracker (created manually, by intake automation, or by `requirements-ticket-agent`).
- At workflow start for an existing parent issue that has not yet been triaged.
- When scope changes materially and track classification needs refresh.

## Required Inputs

- Parent issue ID
- Parent issue with at least baseline context (title + description or equivalent requirements artifact)
- Current workflow tags/labels on parent issue
- Latest previous handoff comment (if present)

## Outputs

- A compact handoff comment for the next stage, wrapped exactly as:

<!-- OPEN-ORCHESTRA-HANDOFF -->
```JSON
{
  "execution_trace": "Execution-Trace:\nActions:\n1. <action>\n2. <action>\nDecisions:\n- <decision + reason>\nReferences:\n- <source>\nAssumptions:\n- <assumption>\nOpen-Questions: none|<question list>\nSkill-Version: triage-agent@1.0.0",
  "handoff_summary": {
    "from_skill": "triage-agent",
    "to_skill": "requirements-ticket-agent|architect-agent|planning-agent",
    "status": "ready|blocked",
    "delta": ["<what changed since prior handoff>"],
    "key_decisions": [{"decision": "<decision>", "reason": "<why>"}],
    "relevant_artifacts": [
      {
        "artifact": "<name>",
        "hash": "sha256:<hash>",
        "last_modified": "<ISO-8601>",
        "summary": "<why this artifact matters>"
      }
    ],
    "open_blockers": [{"blocker": "<text>", "owner": "<owner>", "next_action": "<action>"}],
    "next_guidance": {
      "track": "trivial|standard|complex",
      "skip_steps": ["<skill-name>"],
      "need_full": ["<artifact names to fully read next>"]
    }
  }
}
```

- `handoff_summary` must be <= 600 tokens.
- Existing workflow tags/labels remain the trigger mechanism; do not replace tag-based routing.

## Context Gathering Order (Strict)

1. Locate the most recent comment containing `<!-- OPEN-ORCHESTRA-HANDOFF -->` from the previous skill.
2. Parse the JSON inside it. This is your primary context.
3. Look at its `relevant_artifacts` list and hashes.
4. Declare exactly which artifacts you need via `need_full`.
5. Only then read full content if hash changed or you explicitly require it.
6. Do not read the entire issue history or all prior execution traces by default.

## Procedure

1. Read `/orchestra-config.json`, set tracker context, and verify the configured issue tracker MCP is available.
2. Execute the strict context gathering order above.
3. Determine readiness route from tags/context:
- Route to `requirements-ticket-agent` when requirements are missing/ambiguous or `open-requirements-questions` is present.
- Route to `architect-agent` when requirements are complete (`requirements-done`) and architecture/qa/planning are not yet complete.
- Route to `planning-agent` only when requirements and architecture context are already sufficient for decomposition (for example, architecture work already done and no open architecture/qa blockers).
4. Classify track:
- `trivial`: isolated change, low regression risk, no cross-module impact.
- `standard`: moderate scope, known patterns, normal implementation/review flow.
- `complex`: cross-module/API/data contract/security/runtime impact or high ambiguity.
5. Build `skip_steps` guidance (empty when full standard flow is required). Only skip a stage when required artifacts already exist and no corresponding `open-*-questions` tag is present.
6. Keep tags unchanged except normal stage tags already defined by workflow policy.
7. Post the handoff comment in the exact wrapper format above.
8. Route to the next skill using existing tag/label triggers and the `next_guidance` payload.

## Decision Heuristics

- Complexity signals:
  - `trivial`: single-component/single-file intent, no API/schema/permission/runtime contract changes, clear acceptance criteria.
  - `standard`: bounded multi-file change with known pattern reuse, moderate regression surface, no critical contract shifts.
  - `complex`: cross-service/module coupling, API/schema/contract changes, security/privacy implications, migration/rollout concerns, or unresolved ambiguity.
- Routing signals:
  - Prefer `requirements-ticket-agent` if intent is not testable as written.
  - Prefer `architect-agent` if requirements are testable but implementation design/constraints are not yet captured.
  - Prefer `planning-agent` only when requirements + technical design artifacts are already stable.
- Confidence rule:
  - If confidence is low, mark `status: blocked`, list blockers in `open_blockers`, and avoid aggressive `skip_steps`.

## Guardrails

- Do not read full issue history by default.
- Do not read all artifacts by default.
- Do not modify existing workflow tag contracts.
- Do not emit handoff payloads over 600 tokens.

## Handoff

Primary consumer: next stage skill selected by existing tags/labels, with `next_guidance.track` and `next_guidance.skip_steps` as routing hints.
