---
name: pipefy-process-design
description: >
  Use this skill ONLY when the user explicitly asks for help designing
  or architecting a process ("help me design", "what's the best structure",
  "how do I organize this flow?"). For direct execution requests
  ("create a pipe for X", "build a reimbursement process", or any message
  with a detailed spec), skip this skill and execute directly using the
  domain skills (pipes-and-cards, automations, etc.).
tags: [pipefy, process-design, orchestration, pipes, consulting]
---

# Pipefy Process Design

This skill activates when the user wants **consulting help** to design a process — not when they want you to build one. If the user already knows what they want (gave you phases, fields, a spec, or a clear use case), **do not use this skill**. Execute directly.

---

## When to use vs when to execute

| Signal | Response |
|--------|----------|
| "Help me design a process for X" | **Use this skill** — consulting mode. |
| "What's the best structure for Y?" | **Use this skill** — architecture guidance. |
| "Create a pipe for X" | **Skip this skill** — route via `pipefy-building`, then the domain skill. |
| User provides phases, fields, or a spec | **Skip this skill** — the spec IS the plan. Route via `pipefy-building`, then build. |

---

## Prerequisites

- Understand the user's industry and use case before advising structure.
- Always search for existing pipes in the org before recommending a new one (`search_pipes`).

---

## Discovery phase

1. **Research existing org structure:**

   MCP: `search_pipes name=""`  (empty search returns all visible pipes)
   MCP: `get_organization organization_id=<id>`

2. **Understand the process intent:**
   - What triggers a new case? (form submission, email, manual)
   - Who are the actors? (submitter, approver, ops team)
   - What are the key decision points? (approve/reject, escalate, auto-close)
   - What data needs to be tracked? (fields per phase)
   - Are there related processes that should be connected? (use relations)

3. **Identify the right Pipefy components:**

   | Need | Component |
   |------|-----------|
   | Workflow stages | Pipe + Phases |
   | Structured data per stage | Phase fields |
   | Reference/lookup data | Database table |
   | Cross-process linkage | Pipe relation |
   | Automatic actions | Automation rule |
   | AI-driven processing | AI automation or AI agent |

---

## Design principles

- **Start with the outcome.** What does "done" look like for this process?
- **Name phases for states, not actions.** "Under Review" not "Review It".
- **Keep the start form minimal.** Only ask for data the requester can provide on day 1.
- **Use required fields sparingly.** Every required field is a blocker.
- **Design for the exception.** Add a "Blocked" or "On Hold" phase for edge cases.
- **Automate the obvious.** If a transition always happens under the same condition, it should be an automation, not a manual step.

---

## Common patterns

### Linear approval flow
`Submission → Under Review → Approved / Rejected → Done`
- Start form: requester fills details.
- "Under Review" phase: approver field + due date.
- Automation: notify approver on card creation.

### Multi-stage pipeline
`Intake → Triage → In Progress → Testing → Deployed`
- Each phase has role-specific fields.
- Automations advance cards on condition.
- SLA fields track time-in-phase.

### Hub-and-spoke (related processes)
- Central "intake" pipe connected via pipe relation to domain-specific pipes.
- Child cards created automatically via automation when parent moves to "Escalated".

---

## Output format

After the design consultation, produce a concise summary:

```
Process: <Name>
Phases: [list]
Start form fields: [list with types]
Key automations: [list]
Related processes: [list or "none"]
Next step: [execute with pipes-and-cards skill? or more questions?]
```

---

## Success criteria

- User has clarity on phases, fields, and automation triggers before execution starts.
- No duplicate pipes created (checked via `search_pipes`).
- The design is buildable with available MCP tools (no features promised that don't exist).

## See also

- [pipefy-building](../../building/pipefy-building/SKILL.md) — for execution / build asks, read the router then the domain skill (do not expand this consulting skill into a build playbook).
- `skills/pipes-and-cards/` — execute the design once finalized.
- `skills/automations/` — add automation rules to the new pipe.
- `skills/process-intelligence/` — analyze an existing process for improvement (distinct from designing new).
