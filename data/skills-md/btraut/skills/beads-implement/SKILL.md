---
name: beads-implement
description: Implement Beads work items from a bead id. Use when the user runs $beads-implement <bead-id> or asks to implement a bead/epic; if it is an epic, implement all sub-tasks, committing after each one and only interrupting when blocked or a decision is needed.
---

# Beads Implement

Use this skill to execute work from a bead or epic id with minimal back-and-forth.

## Workflow

1. **Prime bd (always)**
   - Run `bd prime` first. It is the fastest way to get the current "how to start this bead" primer.
   - If `bd prime` is unavailable or confusing, consult the official Beads GitHub repo at `https://github.com/steveyegge/beads` for workflow guidance.

2. **Open the bead**
   - Use `bd show <id>` and read the title, description, acceptance criteria, and dependencies.
   - If required info is missing or a dependency blocks progress, ask a single targeted question and wait.

3. **Start work in Beads**
   - Mark the bead `in_progress` if your bd workflow supports it (check `bd prime` / `bd update --help`).
   - Add a short note on your intended approach if the bead is ambiguous.

4. **Create a brief to-do list**
   - At the start of execution, create a short to-do list of the tasks/sub-tasks you plan to complete and update it as you go.

5. **Decide scope**
   - If the bead is a single task, implement it directly.
   - If the bead is an epic, identify all sub-tasks and implement them in dependency order.

6. **Delegate aggressively (use sub-agents)**
   - If the work splits cleanly, spawn sub-agents instead of serializing everything in your own head.
   - Good sub-agent targets: repo exploration, API/library doc lookup, reproducer creation, test strategy, narrow refactors with a clear file list.
   - Give each sub-agent explicit ownership (files + expected output), and merge their results.

7. **Implement, commit, and write notes (repeat per task/sub-task)**
   - Implement, run relevant checks/tests, then commit.
   - One commit per task/sub-task.
   - Commit message: include the bead id in the subject.
   - Commit body: write real notes (what changed, why, tests run, follow-ups/risk).
   - After the commit, add the same notes to the bead (so the bead survives compaction and future handoffs). Use `bd update <id>` and whatever flag/subcommand your bd version uses for notes (check `bd prime`).

   Minimal commit template:

   ```text
   <BEAD-ID>: <imperative summary>

   Why:
   - ...

   What:
   - ...

   Tests:
   - ...

   Notes/Risks:
   - ...
   ```

8. **Communicate only when needed**
   - Do not interrupt the user while work is progressing.
   - Only pause to ask for help when blocked, when information is missing, or when a meaningful decision is required.

9. **Close out**
   - When complete, close the bead (or mark it done) with a clear reason.
   - After closing, run the session-end sync step recommended by `bd prime` for your installed `bd` version.
   - If `bd prime` is unavailable, verify the session-close command in the official Beads GitHub repo at `https://github.com/steveyegge/beads` before ending the session.

10. **Report progress**
   - Provide a concise summary of completed tasks, commits made, and what remains (if anything).
