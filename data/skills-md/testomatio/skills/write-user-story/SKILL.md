---
name: write-user-story
description: Write user stories, and acceptance criteria (which represent requirements) from a feature idea, ticket, notes, or existing behavior. Use when the user asks to write, draft, or rewrite requirements, a spec, BRD, user stories, use cases, or acceptance criteria.
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Write User Story

Turn source material into user stories. Acceptance criteria on each story are the requirements — testable, atomic rules the story must satisfy.

If the source of data is a PR, use `qa-pr-requirements-analyzer` skill.
If the source is a ticket in issue tracking system, ask for MCP connection.

## Rules

Every user story must be (at least, but not limited to):

- **Atomic** — one actor, one capability.
- **Clear** — no vague words (`fast`, `relevant`, `user-friendly`, `should work`, `as needed`).
- **Complete** — actor, trigger, outcome, business rules; empty, error, and permission paths covered in AC.
- **Consistent** — same terms throughout; no contradictions.
- **Testable** — every story has acceptance criteria with a measurable pass/fail.

Follow other best practices for writing user stories.

Also:

- Describe **what**, not how. No UI widgets, API implementation details or frameworks unless the user asked for that.
- Flag assumptions and open questions. Never silently invent missing rules. Do NOT: guess, imagine, assume. Always ask the user for clarification if something is unclear.

## Output

Default: user stories + acceptance criteria. Match the user's format if they specify one (BRD, use cases, Gherkin, ticket AC) — still express each unit as a user story with AC.

- Each user story gets a short unique identifier (e.g. `US-1`). Use local IDs only. Never invent TMS IDs.
- Each story has at least one AC. Mark AC with a short unique id (e.g. `AC-1`).
  (Better to set ids at the end of the line to make it more readable.)

## Next actions

- Review for gaps and testability → `qa-requirement-reviewer`
- Risk scenarios → `qa-thinking`
- Test cases from these user stories → `qa-write-test-cases`
