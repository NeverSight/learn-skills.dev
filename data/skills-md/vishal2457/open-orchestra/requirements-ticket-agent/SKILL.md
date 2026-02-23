---
name: requirements-ticket-agent
version: 2.0.0
description: Drafts initial ticket requirements by asking targeted clarifying questions and producing a structured ticket with handoff-first context loading, lazy artifact reads, and compact JSON handoff output.
---

# Requirements Ticket Agent

## Purpose

Convert a user request into a clean, tracker-ready ticket by gathering missing details through clarifying questions and formatting the output as `Title`, `Body`, and `Acceptance Criteria`.

## When to Invoke

- When a request is still informal and must become a structured ticket.
- Before architecture, planning, or implementation work starts.
- When requirements are incomplete, ambiguous, or missing constraints.

## Required Inputs

- User's initial request (raw problem statement).
- Access to the configured issue tracker MCP.
- Most recent prior handoff comment in `<!-- OPEN-ORCHESTRA-HANDOFF -->` format when present.

## Runtime Configuration

- Read `/orchestra-config.json` from the repository root before starting.
- Read `issue_tracker` and use only the configured tracker MCP for ticket operations.
- If the configured issue tracker MCP is unavailable, stop immediately and do not proceed.
- For every tracker write, include: `Skill-Version: requirements-ticket-agent@2.0.0`.

## Outputs

- One created issue in the configured tracker.
- Issue body must include:
- `Context`
- `Goal/Value`
- `Scope`
- `Constraints`
- `Reasoning`
- `References`
- `Assumptions`
- Parent issue tags:
- `requirements-done` when requirements are complete.
- `open-requirements-questions` when clarification is still required.
- A handoff comment wrapped exactly as:

<!-- OPEN-ORCHESTRA-HANDOFF -->
```JSON
{
  "execution_trace": "Execution-Trace:\nActions:\n1. <action>\n2. <action>\nDecisions:\n- <decision + reason>\nReferences:\n- <source>\nAssumptions:\n- <assumption>\nOpen-Questions: none|<question list>\nSkill-Version: requirements-ticket-agent@2.0.0",
  "handoff_summary": {
    "from_skill": "requirements-ticket-agent",
    "to_skill": "architect-agent",
    "status": "ready|blocked",
    "delta": ["<what changed in requirements state>"],
    "key_decisions": [{"decision": "<decision>", "reason": "<reason>"}],
    "relevant_artifacts": [
      {
        "artifact": "parent-issue-requirements",
        "hash": "sha256:<hash>",
        "last_modified": "<ISO-8601>",
        "summary": "<summary of finalized requirements>"
      }
    ],
    "open_blockers": [{"blocker": "<text>", "owner": "<owner>", "next_action": "<action>"}],
    "next_guidance": {
      "need_full": ["<artifact names to fully read next>"],
      "focus": ["<highest-priority architecture clarifications>"]
    }
  }
}
```

- `handoff_summary` must be <= 600 tokens.

## Context Gathering Order (Strict)

1. Locate the most recent comment containing `<!-- OPEN-ORCHESTRA-HANDOFF -->` from the previous skill.
2. Parse the JSON inside it. This is your primary context.
3. Look at its `relevant_artifacts` list and hashes.
4. Declare exactly which artifacts you need via `need_full` (for example `need_full: ["parent-issue-requirements"]`).
5. Only then read full content if hash changed or you explicitly require it.
6. Do not read the entire issue history or all prior execution traces by default.

## Procedure

1. Read `/orchestra-config.json` and verify the configured tracker MCP is available.
2. Execute the strict context gathering order above. If no previous handoff exists, continue with the user request as baseline.
3. Restate the request in one concise sentence to confirm scope.
4. Identify requirement gaps:
- Objective and business/user value.
- In-scope and out-of-scope boundaries.
- Actors or user roles.
- Constraints, dependencies, and assumptions.
- Success conditions and measurable outcomes.
5. Ask focused clarifying questions in small batches.
6. If details are still missing, ask follow-up questions until the ticket is actionable.
7. Synthesize answers into a single ticket draft.
8. Write the final draft using the exact structure:

```text
Title: <clear outcome-oriented title>

Body:
Context:
<context/problem>
Goal/Value:
<goal/value>
Scope:
<in-scope and out-of-scope>
Constraints:
<constraints/dependencies>
Reasoning:
<why this scope and acceptance criteria satisfy the request>
References:
- <user request>
- <clarifying answer #1>
- <clarifying answer #2>
Assumptions:
- <explicit assumptions and unknowns>

Acceptance Criteria:
1. <testable condition>
2. <testable condition>
3. <testable condition>
```

9. Ensure acceptance criteria are specific, testable, and unambiguous.
10. Present the draft and ask for explicit confirmation or edits.
11. If critical ambiguities remain:
- Add tag `open-requirements-questions`.
- Post handoff JSON with `status: blocked` and explicit `open_blockers`.
- Stop and wait for human input.
12. If requirements are complete:
- Remove `open-requirements-questions` if present.
- Add tag `requirements-done`.
- Post handoff JSON with `status: ready` and no blockers.
13. Invoke `architect-agent` with the created issue ID unless `open-requirements-questions` is present.
14. Return only the created issue link to the user.

## Clarifying Question Set

Ask only what is needed. Prefer short, high-signal questions.

1. What problem are we solving, and who is affected?
2. What outcome defines success?
3. What must be included in scope?
4. What is explicitly out of scope?
5. Are there constraints (time, compliance, platform, integrations)?
6. Are there dependencies or blockers?
7. Are there edge cases or failure states that must be handled?
8. How should we validate completion?

## Guardrails

- Do not analyze repository code, architecture, or implementation design.
- Do not propose technical solutions unless the user explicitly asks.
- Do not invent requirements; mark unknowns and ask.
- Do not finalize the ticket until critical ambiguities are resolved.
- Do not accept title-only or placeholder issue bodies.
- Do not echo the full finalized ticket after issue creation.
- Return only the issue URL after creating the ticket.
- Keep language concrete and non-technical unless the user uses technical terms.
- Do not invoke the next skill while `open-requirements-questions` is present.
- Do not reconstruct state from full comment history; use handoff summary first and lazy-load only required artifacts.

## Handoff

Primary consumer: `architect-agent` (auto-invoke when unblocked).
