---
name: gsdl
description: "Get Shit Done (GSD) orchestrator. Runs the full project pipeline from idea to implementation: setup → PRD → task list → implementation. Use when the user wants to build something end-to-end, says \"let's GSD\", \"build this from scratch\", \"get shit done\", or wants to run the full development workflow. Coordinates gsdl-setup-project, gsdl-create-prd, gsdl-create-plan, and gsdl-execute-plan skills. Spawns subagents per parent task during implementation to preserve context. Accepts an optional project name or source URL: /gsdl [project-name] OR /gsdl [linear|notion|slite] [url] OR /gsdl [url]."
disable-model-invocation: true
---

# GSD — Get Shit Done Orchestrator

Coordinates the full project pipeline across four phases. Phases 0–2 run **inline** (interactive, in this context). Phase 3 (implementation) **spawns one subagent per parent task** to keep context fresh.

## Pipeline Overview

```
Phase 0: Setup       → gsdl-setup-project SKILL.md (inline)
Phase 1: PRD         → gsdl-create-prd SKILL.md    (inline, interactive Q&A)
Phase 2: Task List   → gsdl-create-plan SKILL.md   (inline, two-phase with "Go")
Phase 3: Implement   → gsdl-execute-plan SKILL.md  (subagent per parent task)
```

---

## Step 0: Detect Source URL (Pre-flight)

**Before resolving the project name**, check if the user's message contains a URL argument.

Recognized patterns:
- `/gsdl linear https://linear.app/...`
- `/gsdl notion https://notion.so/...`
- `/gsdl slite https://slite.com/...`
- `/gsdl https://linear.app/...` (source auto-detected from URL)
- `/gsdl https://notion.so/...`
- `/gsdl https://notion.site/...`
- `/gsdl https://slite.com/...`

**If a URL is detected:**

1. Read and follow the `gsdl-fetch-source` skill (resolve path per the Skill Path Resolution section below).
2. Pass the URL and optional source-type hint to the skill.
3. The skill returns:
   - A **suggested project name** (kebab-case, derived from the fetched title)
   - **Seed content** (pre-formatted Markdown for `seed.md`)
   - A **source summary** (one-line description of what was fetched)
4. Present the suggested project name to the user and confirm: *"I fetched the content from [source summary]. I'll use `[suggested-name]` as the project name — does that work, or would you like a different name?"*
5. Once confirmed (or adjusted), store both the project name and seed content in context.
6. Proceed to **Step 2: Detect Current Phase** — the seed content will be written to `seed.md` during Phase 0 setup (overriding the normal "describe your idea" prompt).

**If no URL is detected**, skip this step entirely and proceed to Step 1.

---

## Step 1: Resolve Project Name

1. **Check the user's message for a project name argument.** If the user typed `/gsdl my-project`, the project name is `my-project`. Use it directly — do not ask.
2. If a source URL was provided in Step 0, the project name was already resolved there — use it.
3. If no project name was provided and no URL was given, ask: "What's the project name?"
4. Normalize to kebab-case.

---

## Step 2: Detect Current Phase

Read `.planning/[project-name]/progress.md` if it exists — this is the fastest way to resume.

If `progress.md` exists, extract:
- `phase` — last recorded phase (0–3 or "done")
- `prd` — path to the active PRD file
- `tasks` — path to the active task file

Then **verify** the recorded files still exist on disk before trusting them. If a file is missing, fall back to the filesystem scan below.

If `progress.md` does not exist (or a recorded file is missing), scan the filesystem:

| Condition | Start at |
|-----------|----------|
| No `.planning/[project-name]/` folder | Phase 0 |
| `.planning/[project-name]/seed.md` exists, no `tasks/prd-*.md` | Phase 1 |
| `.planning/[project-name]/tasks/prd-*.md` exists, no `tasks/tasks-prd-*.md` | Phase 2 |
| `.planning/[project-name]/tasks/tasks-prd-*.md` exists with unchecked `[ ]` items | Phase 3 |
| All tasks `[x]` | Done |

If multiple PRD or task files exist, use the path recorded in `progress.md` (if available); otherwise ask the user which one to use.

**After determining the active phase and files, write (or update) `progress.md`** — see the Progress File section below.

Announce which phase you're starting from and why before proceeding.

---

## Step 3: Run Each Phase

## Skill Path Resolution

When reading a sub-skill, resolve its path using this priority order:
1. `~/.agents/skills/[skill-name]/SKILL.md` — installed via npx (preferred)
2. `~/.cursor/skills/[skill-name]/SKILL.md` — legacy/manual install

Use whichever path exists. If both exist, prefer `~/.agents/skills/`.

Sub-skills used by this orchestrator:
- `gsdl-fetch-source` — fetches content from Linear, Notion, or Slite (Step 0)
- `gsdl-setup-project` — creates folder structure and seed.md (Phase 0)
- `gsdl-create-prd` — generates the PRD (Phase 1)
- `gsdl-create-plan` — generates the task list (Phase 2)
- `gsdl-execute-plan` — implements sub-tasks (Phase 3)

---

### Phase 0 — Project Setup (Inline)

Read and follow the `gsdl-setup-project` skill (resolve path per above).

Complete the full setup (folder, `tasks/`, `seed.md`):

- **If seed content was pre-fetched in Step 0**: Write the fetched seed content directly to `seed.md` instead of asking the user to describe their idea. Show the user what was written and let them know they can edit `seed.md` before continuing.
- **If no pre-fetched content**: Follow the normal `gsdl-setup-project` flow (prompt the user to describe their idea, populate `seed.md` collaboratively).

Then write the initial `progress.md` (phase 0), show the checkpoint, and wait for user confirmation before continuing to Phase 1.

### Phase 1 — Create PRD (Inline)

Read and follow the `gsdl-create-prd` skill (resolve path per above).

This phase is interactive — ask clarifying questions, iterate on the PRD with the user, then save it to `.planning/[project-name]/tasks/prd-[feature-name].md`.

After saving the PRD, update `progress.md` (phase 1, prd path). Show the checkpoint and wait for confirmation before Phase 2. **Before proceeding to Phase 2, re-read the PRD from disk** at its saved path — the user may have edited the file after reviewing it.

### Phase 2 — Generate Task List (Inline)

Read and follow the `gsdl-create-plan` skill (resolve path per above).

This has two steps: show parent tasks → wait for user "Go" → generate sub-tasks and save to `.planning/[project-name]/tasks/tasks-prd-[name].md`.

After saving the task file, update `progress.md` (phase 2, tasks path). Show the checkpoint and wait for confirmation before Phase 3. **Before proceeding to Phase 3, re-read the task file from disk** at its saved path — the user may have edited the file (reordering, rewording, or adding tasks) after reviewing it.

### Phase 3 — Implementation (Subagent per Parent Task)

Update `progress.md` to phase 3 before starting.

**Re-read the task file from disk** to identify all parent tasks (1.0, 2.0, 3.0, ...). Use the on-disk version as the source of truth, not any prior in-context copy.

For each parent task, in order:

1. Read the task file to get the parent task title and its sub-tasks
2. Spawn a `generalPurpose` subagent using the Task tool with this prompt (fill in all `[placeholders]`):

```
Read and follow the skill at: ~/.agents/skills/gsdl-execute-plan/SKILL.md (if it exists, otherwise ~/.cursor/skills/gsdl-execute-plan/SKILL.md)

You are running in BATCH MODE. Complete ALL sub-tasks under the assigned parent task
without pausing for user approval between sub-tasks. Apply the full completion protocol
after each sub-task (mark [x], update task file, update Relevant Files), but immediately
continue to the next sub-task without waiting.

Project context:
- Project name: [project-name]
- Workspace root: [absolute path to workspace root]
- Task file: [absolute path to .planning/[project-name]/tasks/tasks-prd-*.md]
- Assigned parent task: [N.0] [Parent Task Title]
- Sub-tasks to complete: [N.1] [title], [N.2] [title], ... (list all)

When all sub-tasks under [N.0] are marked [x] and the parent is marked [x]:
- Return a summary: what was built, files created/modified, any issues or blockers
- Do NOT start the next parent task ([N+1].0)
```

3. After the subagent returns, show the user the summary
4. Show the checkpoint and wait for confirmation before spawning the next subagent

---

## Progress File

Maintain `.planning/[project-name]/progress.md` throughout the pipeline. Write it after every phase transition and whenever the active files are first determined.

### Format

```markdown
# [project-name] — GSDL Progress

## State

- Phase: [0 | 1 | 2 | 3 | done]
- Last Updated: [YYYY-MM-DD]

## Active Files

- PRD: [relative path to active prd-*.md, or "none"]
- Tasks: [relative path to active tasks-prd-*.md, or "none"]
```

### When to write/update

| Event | Phase value | PRD | Tasks |
|-------|-------------|-----|-------|
| Phase 0 complete (setup done) | `1` | `none` | `none` |
| PRD saved (Phase 1 complete) | `2` | path to PRD | `none` |
| Task file saved (Phase 2 complete) | `3` | path to PRD | path to tasks |
| All tasks complete | `done` | path to PRD | path to tasks |

---

## Checkpoint Format

Show this between every phase transition and between every parent task in Phase 3:

```
✅ [Phase name / Task N.0 title] complete.

What was done: [1–3 sentence summary]
Files touched: [key files created or modified]

👉 Review the output file before continuing — you can edit it directly and your changes will be picked up automatically.

Ready to continue to [next phase / Task N+1.0]?
Type "yes" / "go" / "next" to continue, or tell me what to review or change first.
```

**Never proceed past a checkpoint without user confirmation. Always re-read the relevant artifact from disk after the user confirms, to pick up any edits they made during the review window.**

---

## Resuming Mid-Pipeline

If GSD is triggered on a project that already has work done:

1. Read `progress.md` (if present) → verify files on disk → fall back to filesystem scan if needed
2. Skip completed phases
3. Announce: "Project '[name]' is at Phase [N]. Resuming from [description]."
4. For Phase 3, check which parent tasks are already `[x]` and skip them

---

## Rules

1. **Always show a checkpoint** between phases and between parent tasks — never chain them automatically
2. **Phases 0–2 are inline** — do not spawn subagents for setup, PRD, or task generation
3. **Each Phase 3 subagent handles exactly one parent task** — never assign two parent tasks to one subagent
4. **Surface blockers immediately** — if a subagent reports an error or missing dependency, pause Phase 3 and resolve with the user before continuing
5. **All files stay within the project folder** — never create files at workspace root
6. **Keep `progress.md` current** — update it at every phase transition so `/gsdl [project-name]` always resumes cleanly
