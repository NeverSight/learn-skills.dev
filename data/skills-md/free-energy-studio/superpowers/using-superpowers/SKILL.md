---
name: using-superpowers
description: Use when choosing which Free Energy Superpowers guidance applies to a development task, or when explicitly asked about the skill workflow.
---

# Using Free Energy Superpowers

Skills are task-specific guidance, not a sequence every request must traverse.
Answer simple questions directly. Do not load a workflow because a keyword happens
to match, re-load unchanged instructions for every follow-up, or announce each skill.

For software work, use `applying-development-principles` as the engineering
standard. Its principles govern the choice and depth of the workflows below;
they are not a separate layer applied afterward. Load other skills when they
help with the actual task:

- Unresolved product or design choices: `brainstorming`.
- A bug whose cause is unknown: `systematic-debugging`.
- Work needing sequencing or handoff: `writing-plans`, then `executing-plans`.
- Testable behavior changes: `test-driven-development`.
- Completion claims: `verification-before-completion`.
- Material changes needing independent scrutiny: `requesting-code-review`.
- Feedback to evaluate: `receiving-code-review`.
- Workspace isolation or delivery decisions: `using-git-worktrees` or
  `finishing-a-development-branch`.
- Useful, permitted delegation: `dispatching-parallel-agents` or
  `subagent-driven-development`.
- Authoring instructions: `writing-skills`.

For Linear issue work or an issue-linked branch, read
[the Linear workflow](../applying-development-principles/references/linear.md).
Do not load ticket policy for unrelated development or ordinary questions.

Load an explicitly requested skill. Read applicable instructions before relying on
them, using the host's native skill loader or file reader. Read supporting material
only when the main skill calls for it in this task. A subagent with a bounded brief
does not need to repeat the controller's planning workflow.

Host/system rules take precedence. Within those boundaries, follow explicit user
intent and repository rules over generic skill defaults. Skills grant no additional
permission to mutate data, contact people, publish, merge, or delete work.

When tool names differ, trust the tools actually available. The platform references
in `references/` are lookup aids, not prerequisites for ordinary work.
Available mappings: `references/codex-tools.md`, `references/pi-tools.md`,
`references/antigravity-tools.md`, `references/hermes-tools.md`, and
`references/gemini-tools.md`.
