---
name: pdd
description: 'Skills for Puzzle Driven Development (PDD). Refer to this skill when a project uses PDD or the operator mentions PDD or puzzle-driven development. Use this skill when: (1) Breaking a large feature into incremental deliverables, (2) Writing @todo stub comments to mark unimplemented code, (3) Picking up an existing @todo puzzle to implement, (4) Deciding whether to wrap up a task with a stub or keep working.'
---

## What is PDD?

Puzzle Driven Development breaks features into small, working increments. Each increment leaves `@todo` puzzle comments marking deferred work. This lets multiple agents (AI or human) work in parallel and progress without being blocked by incomplete pieces.

A good increment:
- **Passes tests** — never leave failing tests as technical debt
- **Has working stubs** — throws an error indicating that the stub is still unimplemented; never silently swallow unimplemented behaviour
- **Documents context** — the `@todo` comment should give the next agent enough to start without reading all the history

## @todo Comment Format

```js
// @todo #1234 Short description of what to implement:
//  - Bullet point of expected behaviour
//  - Reference to related patterns (e.g., "See <file> for ...")
//  - Dependency notes (e.g., "Needs <something> from #1235")
//  - Acceptance criteria
doSomething() {
  throw new Error("doSomething not yet implemented")
}
```

Key rules:
- `@todo` followed by the ticket you are working on. For example, if you are working on issue #1234 say `@todo #1234`. The ticket reference will depend on the issue tracking system used, e.g. `#1234` for GitHub, or `ABC-1234` for Jira/Linear, or `CLAUDE-1` for Claude Code's built-in task list. If it is unclear which ticket is being worked on, ask the operator for this information before continuing.
- No iteration or phase numbers — don't write `@todo Add create action in phase 2`; implementation order can change
- For subsequent lines after the `// @todo`, indent by one space, i.e. add 2 spaces after the line comment, e.g. `//  -`.
- Always pair the comment with a stub so callers fail loudly

## When to Wrap Up With a Stub

If you think you're spending too long on a task:

1. Get tests to pass with a minimal implementation
2. Write a `@todo` comment that explains:
   - The context on what you are working on
   - What you tried and why it didn't work so far
   - What the next agent needs to know to continue the work without repeating your failed attempts
3. Create a task in your task list referring to the todo comment you created.

## Picking Up an Existing Puzzle

When you find a `@todo` to implement:

1. Read the comment fully — it should have context, bullets, and file references
2. Check the ticket numbers in issue tracker for acceptance criteria
3. Study the referenced files/patterns before writing code
4. Remove the `@todo` comment when the implementation is complete
5. Run the relevant tests to confirm nothing breaks
