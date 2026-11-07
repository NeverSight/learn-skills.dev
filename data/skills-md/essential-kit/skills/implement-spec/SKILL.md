---
name: implement-spec
description: "Implement the result of /to-spec and /to-tickets in code."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The spec and tickets are **GitHub issues**. Use the `gh` CLI, which infers the repository from the clone:

- **Read a ticket**: `gh issue view <number> --json number,title,body,labels,comments`
- **Close a ticket**: `gh issue close <number> --comment "<what landed>"`

Before starting, read `GLOSSARY.md` at the repo root (or `GLOSSARY-MAP.md` and the per-context glossaries it points at) and any ADRs under `docs/adr/` or `src/*/docs/adr/` that touch the area. If they don't exist, proceed silently. Use their vocabulary in branches, commits, and PRs, and surface any ADR conflict rather than silently overriding it.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way GitHub closes work: a merged PR with a closing reference, or a direct `gh issue close`.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. Read the spec and tickets to understand the task graph.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch. If the user asks for a PR, or the repo closes work through PRs, open a draft PR after the first merge in step 5 (a branch with no commits ahead of main can't open one). Its body should include `Closes #<spec>` and one `Closes #<ticket>` line per ticket, so merging closes them all.

4. Use **implementer subagents** to implement each ticket, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - calls the Skill tool with `tdd` to build the ticket;
   - merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are complete, call the Skill tool with `code-review` on the integration branch. Fix all issues raised by the code review in a single **implementer subagent**.

8. If a draft PR exists, mark it ready for review. Otherwise, close each ticket with `gh issue close <number> --comment "<what landed>"`, and report the integration branch.

9. Clean up all **implementer subagent** worktrees.
