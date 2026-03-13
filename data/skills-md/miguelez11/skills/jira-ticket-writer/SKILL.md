---
name: jira-ticket-writer
description: Write well-structured Jira tickets or improve existing ones. Enforces a consistent template with clear context, problem/request definition, acceptance criteria, and definition of done. Use when user asks to write, create, draft, or improve a Jira ticket, story, bug report, or task — or when a ticket lacks structure or clarity.
---

# Jira Ticket Writer

## Quick start

1. Identify ticket type (Bug, Story, Task, Spike)
2. Ask what the user knows — summary, context, problem or goal
3. Fill the template by asking targeted questions for any missing fields
4. Present the full draft — iterate until approved
5. Optionally create or update via `jira` (see jira-cli skill)

## Workflow

- [ ] Confirm ticket type
- [ ] Gather context: what, why, who is affected, what is the expected outcome
- [ ] Fill type-specific sections (see [TEMPLATES.md](TEMPLATES.md))
- [ ] Ensure each acceptance criterion is independently testable
- [ ] Include a clear definition of done
- [ ] Present full draft and iterate on feedback
- [ ] Offer to submit via jira cli (jira cli does not work in sandbox mode) 

## Key principles

**Summary line**: `<Verb> <object> <context>` — 80 chars max.
- Good: `Fix login redirect loop on expired sessions`
- Bad: `Login problem`

**Context**: Answer "why does this matter?" — business impact, affected users, frequency.

**Acceptance criteria**: Each item must be independently verifiable. Prefer:
- Checkbox lists for features
- Given / When / Then for behaviour

**Definition of done**: What makes this closeable? (e.g. code reviewed, unit tests passing, deployed to staging, product sign-off)

**Priority guide**:
- Critical — system down, data loss, security breach
- High — major flow broken, significant user impact
- Medium — degraded experience, workaround exists
- Low — minor polish, rare edge case

See [TEMPLATES.md](TEMPLATES.md) for full templates by ticket type.
