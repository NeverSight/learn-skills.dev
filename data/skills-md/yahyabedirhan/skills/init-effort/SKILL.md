---
name: init-effort
description: Start a new effort on its own branch and worktree, or a brand-new project in its own repo.
argument-hint: "The idea, in a sentence or a paragraph"
disable-model-invocation: true
---

# Init Effort

An **effort** is work big enough for its own branch and pull request: a feature, a new app, a refactor, a re-architecture. Do routine upkeep, such as data edits and small fixes, in the current checkout without this skill; the project may list what counts as routine there.

Both the effort's thinking now and its build later happen in the worktree this skill creates. Write only into that worktree and, for a new project, the new repo, so the repository this session was started in stays as it was.

## Parameters

- `<worktree-tool>`: the tool that makes and frees worktrees, e.g. `treehouse`, or plain git worktrees.
- `<session-host>`: where agent sessions run, e.g. `herdr`, Claude Code Desktop, Codex Desktop.
- `<agent>`: the command that starts a new agent session, e.g. `claude` or `codex`, with its flags.

## Flow

1. **Decide where it lives:** an effort in an existing repo, which is the current one or one the idea names, or a new project that has no repo yet.
2. **Name it.** Propose a short kebab-case effort name, and a branch that follows the project's branch naming, or `<area>/<effort>` when the project has none. Confirm both with the maintainer.
   - **For a new project:** first propose a few project names and confirm one.
3. **For a new project only, create it.** Ask which licence it takes, recommending MIT in the maintainer's name. Ask too whether its GitHub repo is public or private. Then read `project-creation.md`, and create and push the repo.
4. **Create the worktree** on the new branch with `<worktree-tool>`, from the remote default branch.
   - When the work builds on unpushed commits on the local default branch, branch from the local one instead.
5. **Write the idea into a handoff** in the worktree, in the project's handoff folder, else at `.handoff/<date>-<effort>.md`. It holds the idea as the maintainer gave it, the effort, the branch and the worktree.
   - **For a new project:** it also holds its repo.
6. **Start the thinking session:** start `<agent>` in the worktree through `<session-host>`, passing the worktree, the effort as the topic, `thinking` as the role, and the starting prompt below.
   - **When it runs in another session:** tell the maintainer where, and stop once `<session-host>` reports it working on the prompt or the maintainer says it started.

The starting prompt is one line, since a prompt of several lines arrives as pasted text and its skills never start:

```text
Think through the effort in <handoff path>: grill me on it with the grilling skill, using the prototype skill when a question needs a runnable answer, then write the spec with to-spec and the tickets with to-tickets, and hand over to an orchestrator with the handover skill.
```

This prompt only includes skills an agent can load.

## References

- [project-creation.md](project-creation.md): creating a new project's repo: the name checks, the setup and the first commit.
