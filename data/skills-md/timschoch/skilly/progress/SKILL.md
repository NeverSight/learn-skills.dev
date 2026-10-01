---
name: progress
description: Print where a long-running task stands. Needs you, blocked, now, next, done, as one short list. Use when the user returns to a long task and runs /progress.
disable-model-invocation: true
---

# Progress

Read-only. Edit no file, run no write command, start no work. Print the report, then stop.

## 1. Collect

Check real state. The conversation alone goes stale after compaction.

| Source         | How                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------- |
| Conversation   | goal, open questions and decisions, stop points the user named                                    |
| Task list      | todo items and their state                                                                        |
| Working tree   | `git status --short`, `git log --oneline <default-branch>..HEAD`                                  |
| PR and CI      | `gh pr view --json number,url,state,mergeStateStatus,statusCheckRollup`, only if a PR exists     |
| Background work | running subagents, background shells, monitors                                                   |

Skip a source that does not apply. Cross-check: a todo marked done without its commit, push or green check is not done.

## 2. Sort

- **Needs you**: only the user can move it. A decision, a question, an approval, a secret, a manual step.
- **Blocked**: waits on something outside. CI, a review, a rate limit, another agent. Name what unblocks it.
- **Now**: the one item in progress.
- **Next**: open items, in order.
- **Done**: finished items. Mark steps that must not run twice: `(pushed)`, `(migration ran)`, `(PR opened)`.

## 3. Print

Use this shape. Omit an empty section, never print "none". Keep each section to about ten items: merge small steps, drop trivia and abandoned attempts.

```markdown
**Needs you**
7. Short summary of the problem.
   7.1 **recommended** option, the one reason that decides it
   7.2 option, its tradeoff
9. Question in one line?

**Blocked**
- CI red on #42 `lint`, waits on the fix in Now

**Now**
- item, link

**Next**
- [ ] item

**Done**
- [x] item, link (pushed)
```

- A decision keeps the number it first got in the conversation. A new item takes the next free number. Numbering follows `.claude/rules/workflow-dialog.md`.
- One sub-item per option. Mark exactly one **recommended**, at the start of its sub-item.
- Link, never restate: PR, issue, commit, file path.
- No recap, no timeline, no narrative, no status colors.
- State unknown? Write "unknown" and the command that checks it. Never guess.
