---
name: implement
description: Implement approved project work with tests and final review.
disable-model-invocation: true
---

# Implement

Implement approved work described by the active project's spec or tickets.

Resolve every `.agents/projects/` path from the opened workspace root, including
when the active repository is nested inside it. In a single-repository workspace,
that is the repository root. Keep this artifact root fixed when changing directories;
never use nested repositories or global agent-installation directories for artifacts.

## Process

1. Identify the active project. Read `.agents/projects/<project>/CONTEXT.md`, `LINKS.md`,
   `todo.md`, the approved spec, ticket drafts, tracker tickets, and relevant ADRs.
   Confirm the implementation target and its acceptance criteria before changing code.

   Done when the approved scope, test seams, and current ticket frontier are known.

2. Implement one vertical slice at a time. Use `tdd` at the pre-agreed seams where
   possible. Run typechecking and focused tests regularly; keep the project work list
   current as slices land. Whenever a Jira task completes and its required verification
   passes, invoke `update-ticket` to check the corresponding item in the main ticket.
   This completion update is already authorized; comments and other description
   changes retain their approval gate.

   Done when each accepted slice is implemented, its focused verification passes,
   and its main Jira checklist item is checked or the exact pending update is recorded
   with the tracker-access limitation.

3. Run the full relevant test suite and the repository's coverage tooling. Target
   100% coverage for changed code and require at least 95%, unless the user or the
   repository explicitly opts out. Close meaningful gaps through behavior-focused
   tests, not coverage-only assertions.

   Done when verification passes and coverage meets the threshold, or the explicit
   exception is recorded in `.agents/projects/<project>/todo.md`.

4. Update project artifacts with completed work, material facts, decisions, and ticket
   links. If posting a Jira or GitHub comment, end it with the exact line:

   ```text
   Written by AI Agent
   ```

   Done when the project state accurately reflects the implementation result.

5. Invoke `code-review` against the implementation's fixed point and originating
   local spec or tracker ticket. Address confirmed findings, then rerun affected
   verification.

   Done when the review report is recorded and remaining findings are either fixed or
   explicitly reported to the user.
