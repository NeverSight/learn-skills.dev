---
name: writing-lean
description: Lean writing and fluent code. Use when writing or editing code, comments, docs, a pull request, issue, review or commit message.
---

# Writing lean

The code and its specs are the first source of truth: a reader new to the project should learn it
by reading them. Writing is **lean** when it carries only what they cannot say.

- **Code first.** Reach for a clearer name, a smaller function or a sharper spec before a longer
  explanation.
- **One word per idea.** Use the project's term for a concept, from `CONTEXT.md` or the code, every
  time; a synonym reads as a second concept.
- **Say what to do.** State the target ("one-line comments"), not the ban; a prohibition earns its
  place only as a hard guardrail, paired with what to do instead.
- **Once, where it bites.** Each fact has a single source of truth, below; anywhere else, link
  to it.
- **History goes to the story.** What was weighed and what was rejected belong in the issue, pull
  request or commit, where the discussion and the diff sit beside them and `git blame` leads back.

**The deletion test** is the bar for every sentence you write or touch: delete it and ask what a
competent reader loses. If nothing, the code already said it, and it stays deleted.

## Where it goes

| Channel            | Its one job                                                           |
| ------------------ | --------------------------------------------------------------------- |
| Code               | Fluent: concise function and variable names that say what it does     |
| Code comment       | A constraint, trap, citation or non-obvious why, at the line it bites |
| Doc comment        | What the member is for, in one sentence                               |
| README             | The common path: what it is, how to use it, where to go next          |
| Repo docs          | A decision or context the code cannot show                            |
| Issue              | What's wanted and why, in the issue form's fields                     |
| Agent brief        | The contract: behaviour, acceptance criteria, scope                   |
| Pull request       | What changed and why, linked to its issue                             |
| Commit message     | What changed, and why when the diff cannot show it                    |
| Review comment     | One finding and its fix                                               |
| Thread comment     | The new fact or decision, linked to what it answers                   |
| Skill, `AGENTS.md` | How an agent does the work: the steps and the reference behind them   |

## Links from code

Cite an issue in code only when it changes how the code may be modified later: a workaround to
remove when `clhbid/api#123` ships, or a constraint an open decision still holds. Otherwise
`git blame` leads to the pull request and its issue.
