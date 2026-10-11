---
name: maintain-environment
description: Change what agents run with - a permission rule, a global or project instruction, or a skill (create, install, update, move, fork, publish, remove, audit, with `npx skills`) - and carry the change to every harness, machine and install. Use when the user wants a rule or instruction added or changed, asks where one belongs, wants a skill created or changed, asks which skills they use or which name a default tool, or wants a workstation repo for their personal setup.
---

# Maintain the environment

The environment is what agents run with: permissions, global instructions, project instructions, and skills. Use this skill to change it; to set up a machine or a project, use `/set-up-machine` or `/set-up-project` instead. Write each change once, at its source, and carry it from there to every harness, machine and install it applies to. Keep harness memory features off, because a memory is invisible to every other harness and lives outside any repository; write what it would hold into one of the layers instead. The skills repo and most projects are public, so write personal detail only in the user's workstation repo, or the shared global instructions file on a machine without one: names, accounts, paths on the user's machine, other projects. In a skill or a public `AGENTS.md`, generalise it or make it a parameter.

## Parameters

- `<skills-repo>`: the user's own skills repo on GitHub, as `owner/repo`.
- `<path-to-skills-repo>`: where that repo is cloned.
- `<workstation-repo>`: the user's own repo for their personal agent setup, usually private, as `owner/repo`.
- `<path-to-workstation-repo>`: where that repo is cloned, e.g. `~/code/agent-setup`.

## Environment layers

Write each instruction, rule or piece of know-how in one place only, so changing it later is a one-place edit. Two questions choose the place. Who needs it: only this user, anyone working on one project, or any agent doing a task? And must it be enforced, or is it guidance? The table runs from enforced to guidance; go down it and use the first row that fits. Elsewhere, point at it only where a reader wouldn't otherwise find it.

| Layer | Holds | Where to write it |
|---|---|---|
| **Permission** | A hard rule: deny, ask, allow-and-report or, for a personal permission only, allow. | A rule for anybody is a row in `/set-up-machine`'s rule table, which `/set-up-machine` turns into each harness's native entries and the hook uses for rejection guidance. A personal permission, such as allowing a tool the user added, goes in the user's workstation repo. A project may only add allows. |
| **Global instruction** | The user's working agreement, glossaries, environment defaults and personal workflow, concise permission-rejection guidance and a secrets guardrail. | The user's workstation repo, from which `/set-up-machine` writes the shared global instructions file every harness on the machine reads. The compact rules block comes from `/set-up-machine`'s `references/global-instructions.md`. |
| **Project `AGENTS.md`** | Anything a teammate needs to work on the project: its tracker, its commands, its conventions, its worktree tool. | The project's `AGENTS.md`, with a `CLAUDE.md` holding `@AGENTS.md` so Claude Code reads the same text. |
| **Skill** | How to do a task, written for any team's tools and tracker: a value that differs between setups becomes a parameter. | A `SKILL.md` in the skills repo, or a local skill in one project. |
| **Skill reference** | Detail only some runs need, such as one branch of the flow or one tool's specifics; anything every run needs stays in `SKILL.md`. | A file beside the `SKILL.md`. The skill's body says when to read it, and its closing `## References` section says in one line what each file covers; scripts get a `## Scripts` section the same way. |

### The "team test"

Before settling a change, picture a teammate or contributor with a different setup: another harness, a different session host, and a machine set up with `/set-up-machine` but none of the user's personal workflow. After the change they must still be able to work on any of the user's projects using only that project's instructions, the skills and the roles `/set-up-machine` writes.

A change passes when:

- nothing a teammate needs sits in the global instructions;
- the global instructions hold only the user's working agreement, glossaries, environment defaults and personal workflow, permission-rejection guidance and a secrets guardrail;
- no skill depends on the user's default tool. The user's choice of tool sits in their environment defaults, and how to use a tool sits in that tool's own skill.

Flag every place a change fails the test, and move the failing part to the row of the table that fits it.

The test also decides between the skills repo and the workstation repo. What anybody could use, such as a safety rule or how to do a task, goes in a skill or the rule table. What holds only for this user, such as which tool fills a role, a personal workflow line or a personal permission, goes in their workstation repo.

### Skill parameters

A skill that needs a value from the environment (a tool, a command, a repo) declares it as a **parameter**:

- **One `## Parameters` section, in `SKILL.md`,** added only to a skill that needs such a value, with one short line per parameter: the `<kebab-case>` placeholder named after its role, what it is, and a few examples after "e.g.". For instance: "`<session-host>`: where agent sessions run, e.g. `herdr`, Claude Code Desktop, Codex Desktop."
- **Write what to do when a role has no tool once,** in `/set-up-machine`'s roles table, which `/set-up-machine` copies into the environment defaults on every machine. Never repeat it in a skill, since a copy drifts from the table.
- **Say when to use a tool in the tool's own skill,** in its description ("Use when the project's worktree tool is `treehouse`"), along with anything specific to that tool. No other skill routes to it.
- **In the body, use the placeholder as a noun** ("make the worktree with `<worktree-tool>`"). Anywhere else, use plain words ("the session host").
- **Name another skill by its slash command,** such as `/to-tickets`, not in bold. A starting prompt is the exception: it names skills in words, so it works in every harness.

Before any skill uses a new role, add it to `/set-up-machine`'s roles table, with what it is and what to do when it has no tool.

## Steps

1. Choose the layer the change belongs to, and check it against the team test.
   - **When the user asks to improve their workflow or environment:** read `AGENTS.md` in `<path-to-workstation-repo>`, and the documents it names for whoever maintains the setup, such as the user's principles. Name each principle the change conflicts with before you make it. A routine change, such as installing a skill, needs only the team test.
2. Make the change at that layer's source, writing every instruction and skill with `/writing-for-agents`. For any operation on a skill, read `skill-operations.md`.
   - **For an installed skill:** that is its source repo, never an installed copy, which the next `npx skills update` overwrites.
   - **For a local skill:** that is the project.
   - **For a personal change** (a personal preference, an environment default or a personal permission): that is `<workstation-repo>`, in its clone at `<path-to-workstation-repo>`. Read `references/workstation.md` for which file each kind goes in.
   - **When the user has no workstation repo:** write a personal instruction in the shared file itself, which is its source on such a machine. A personal permission has no home there, so offer to start a workstation repo. Start one, when the user asks or accepts, as `references/workstation.md` says.
   - **When the user has one but this machine has no pointer** (`~/.config/agents/source.md`): run `/set-up-machine` first, which writes it, then make the change in the clone.
3. When the change touches the global instructions, show the user the whole shared file as it will read after the change, with each changed line marked. Wait for their approval before the change is committed or shipped: global instructions shape every agent, so the user wants to know every line of them.
4. After any skill change, run the team-test audit: grep the skills for the name of each tool in the user's environment defaults, and for "environment defaults". Skip each tool's own skill, and `/set-up-machine`, `/set-up-project` and this skill, which manage the instruction files. Judge each hit:
   - **When it is a default,** the skill picks the tool itself: make it a parameter, and move the tool's commands into the tool's own skill.
   - **When it is a mention,** an example such as a parameter's "e.g.", or data: keep it.
   - **When it names the environment defaults:** remove the mention. An agent that has them loaded already sees them, and one that doesn't is pointed at nothing.
5. Ship a change to the skills repo on a branch, through a pull request opened with `/to-pr`, and stop once it is open. The user merges it or asks you to.
6. Carry the change everywhere it applies, as the table below says. `npx skills` installs from the default branch, so the installs and updates run after the merge, in the session told the pull request merged.
7. Report each step this session can't carry: which set-up skill or `npx skills update` still has to run, and whether it runs on this machine, on each other machine or in each project.

| Change | How it reaches everywhere |
|---|---|
| A permission for anybody | Ship the `/set-up-machine` rule-table row; after the merge, update the installed skills and rerun `/set-up-machine` on each machine. |
| A personal change | Have the user commit and push it in their workstation repo, then pull it into the clone and rerun `/set-up-machine` on each machine. |
| A global instruction with no workstation repo | Rerun `/set-up-machine` on each machine; every harness reads the one shared file. |
| A project instruction or project permission | Commit it in the project. For a standard every project shares, change `/set-up-project` instead and rerun it in each project. |
| A skill in a source repo | Ship it; after the merge, `npx skills update <name>` in every scope that installs it, on every machine. A machine whose workstation repo lists the skill in `agents/installs.json` also gets the update from a `/set-up-machine` run. |
| A local skill | Commit it with the project. |
| A set-up skill itself | Treat it as a skill change first, then rerun that set-up skill wherever it applies. |

When the user asks what a skill costs to run, or how to make it cheaper, follow `efficiency-analysis.md`.

## References

- [skill-operations.md](skill-operations.md): the kinds of skill, and creating, installing, updating, moving, removing, forking, upgrading a fork, shipping, auditing and publishing them.
- [efficiency-analysis.md](efficiency-analysis.md): measuring what one run of a skill costs, and making the next run cheaper.
- [references/workstation.md](references/workstation.md): what the user's workstation repo is for, its starting layout, starting one, and which file each personal change goes in.

## Scripts

- [scripts/session-usage.py](scripts/session-usage.py): token and time use of a session transcript, split at given moments, for the efficiency analysis.
