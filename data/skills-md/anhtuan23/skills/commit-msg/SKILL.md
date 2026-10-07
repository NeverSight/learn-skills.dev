---
name: commit-msg
description: Suggest a Git commit message for changes the agent has just made using a compact conventional format that fits the typical equity workflow.
---

# Commit Msg

Use this skill when the agent has finished making a logical change and should
suggest one commit message for that change.

## Workflow

1. Summarize the changes the agent has just made.
2. Infer the single best commit type from this set only:
   `feat`, `fix`, `refactor`, `chore`, `docs`, `style`, `test`.
3. Add a scope only when one clear area or module dominates the change.
   Omit the scope when the change spans multiple unrelated areas.
4. Write the subject in this format:

   `type(scope): short subject`

   Or, when no scope is justified:

   `type: short subject`

5. Keep the subject under 60 characters, use imperative mood, and avoid ending
   it with a period.
6. For breaking changes, append `!` before the colon:
   - `feat(api)!: remove deprecated endpoint`
   - `refactor!: drop support for Node 14`
7. If the changes are complex, add a short body with 1–3 bullets:
   - one bullet for what changed
   - one bullet for why
   - (optional) one bullet for impact or scope
8. If the changes are small or obvious, suggest only the subject line.

## Output Format

Return exactly one suggested message in a copy-ready block:

```text
type(scope): short subject

- bullet of what changed
- bullet of why
- (optional) bullet of impact or scope
```

If the change is not complex, return only the subject line in the block.

## Decision Rules

- Choose the type by the main purpose of the change, not just the files
  touched.
- Prefer `refactor` over `fix` when behavior is intended to stay the same.
- Prefer `docs` for comments, READMEs, plans, and other documentation-only
  edits.
- Prefer `style` only for formatting or non-behavioral polish.
- Prefer `chore` for maintenance work that does not fit the other allowed
  types.
- If the change really contains multiple unrelated concerns, note that it would
  be cleaner as multiple commits, then still suggest the best single-message
  fallback.

For the rationale behind these conventions, read
`references/commit-message-conventions.md`.
