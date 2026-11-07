---
name: team-question
description: 'Use for decomposing features into tasks and research questions.'
effort: medium
argument-hint: "<ticket id, issue URL, or task description>"
---

Before each dispatch or retry, read [host dispatch](../team/references/15-host-dispatch.md) and supply its resolved installed paths.
Before artifact work, read [artifact schema](../team/references/artifacts.md).
Before handling external values, read [external-data rules](../team/references/external-data.md).

# Team Question

Before finalizing prose you author, read the [writing standards](../team/references/writing.md).

Run the QUESTION phase only, then stop. The phase writes, in `docs/plans/<id>/`:

- `1-task.md` — the human's full intent. **Never** read by `researcher` or
  `file-finder`.
- `2-questions.md` — neutral research questions without intent; the only file
  `researcher` and `file-finder` read.
- `3-prd.md` — **only** under `## Conditional PRD` in
  `skills/team/playbooks/question.md`.
- `4-repos.md` — **only when the topic spans more than one repository**:
  each involved repo's slug, absolute path, and role.

## Execution

1. **Resolve `$ARGUMENTS`** to a description:
   - Empty: **discover, do not demand.** Read recent `git log` activity and
     the repo's `README` / `CLAUDE.md` to propose a likely topic; use
     `AskUserQuestion` with labeled options only for a genuine gap in intent.
     Never bare-stop with a "describe it" demand when context is available.
   - Ticket-only: ask the user for context, or fetch the issue body through a
     configured tracker integration.
   - Issue URL: run `gh issue view <url> --json title,body` (or equivalent)
     and use the title plus body as the description.
   - Free text: use directly.

   A ticket identifier (e.g. `ENG-1234`) is recorded as `ticketId` in
   `1-task.md` frontmatter. The orchestrator calls no ticketing system.
2. **Choose `<kebab-topic>`**: a 2–4 word kebab-case slug derived from the
   description. Resolve `<team-question-skill-dir>` to the absolute directory
   containing this `SKILL.md`. From the repository root, run
   `"<team-question-skill-dir>/scripts/prepare-plan-dir.sh" [--ticket <TICKET>] <kebab-topic>`,
   passing `--ticket` only when a ticket identifier is present. Its `dir=`
   line is `docs/plans/<id>/`.
3. **Handle its exit code.** Exit 2: fix the topic or ticket its stderr
   names and rerun. Exit 1 or 3: stop and report its stderr.
4. **Resume detection** from its `state=` line:
   - `new`: the questioner writes every artifact.
   - `questions-only`: re-read `1-task.md` instead of overwriting it; the
     questioner only writes `2-questions.md`.
   - `complete`: skip dispatch and go to the report.
5. Dispatch the `questioner` agent with the full description and the
   target directory `docs/plans/<id>/`. It writes the artifacts above.
6. **Stop once the rerun reports `state=complete`**: rerun the step 2 command
   with `--date <date>` from its first `date=` line. Do not continue to
   RESEARCH. Any other state means the questioner did not write
   `1-task.md` and `2-questions.md`; report that and stop.

Report:

- Path to `1-task.md` and `2-questions.md` (and `3-prd.md` / `4-repos.md` when
  written)
- Topic slug and `<id>`
- Mode: single-repo, or multi-repo with the involved repo slugs
- Tell the user: **"Next: run `/team-research docs/plans/<id>/`"**
