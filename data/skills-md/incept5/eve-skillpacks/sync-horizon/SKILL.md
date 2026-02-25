---
name: sync-horizon
description: Sync eve-skillpacks with latest eve-horizon changes. Reads git log, identifies affected skills, updates reference docs and skills, tracks sync point.
---

# Sync Horizon

Synchronize eve-skillpacks with the latest state of the eve-horizon repository.

## Prerequisites

- The eve-horizon repo must be at `../eve-horizon` (sibling directory)
- `.sync-state.json` must exist in the repo root (create from template if missing)
- `.sync-map.json` must exist in the repo root

## Architecture: Orchestrator + Parallel Workers

This sync follows an orchestrator pattern. You (the orchestrator) stay lightweight — discovering what changed and dispatching focused workers. Each worker handles one update in isolation with its own context budget.

**Why:** Previous runs exhausted the context window by reading every diff and every doc in the orchestrator. The fix is strict separation: the orchestrator sees only file names and summaries; workers see only their specific diffs and target files.

## Output Standards (State Today + Progressive Access)

- Distill only shipped platform behavior from eve-horizon source docs.
- Do not carry roadmap content into skillpacks. Remove or ignore sections such as `Planned (Not Implemented)`, `What's next`, roadmap/future notes, and "current vs planned" framing.
- Keep `eve-work/eve-read-eve-docs/SKILL.md` task-first: route by intent, then load only the minimal reference files needed.
- Keep reference docs scoped and actionable; avoid broad copy-paste from system docs.

## Workflow

### Phase 1: Discover Changes (orchestrator — stay lightweight)

1. Read `.sync-state.json` to get `last_synced_commit`
2. If `last_synced_commit` is null, use the first eve-horizon commit (full baseline sync)
3. Get the commit log:
   ```bash
   cd ../eve-horizon && git log --oneline <last_synced_commit>..HEAD
   ```
4. Get the diff stat of watched paths (file names and line counts only):
   ```bash
   cd ../eve-horizon && git diff --stat <last_synced_commit>..HEAD -- docs/system/ docs/ideas/agent-native-design.md docs/ideas/platform-primitives-for-agentic-apps.md packages/cli/src/commands/ AGENTS.md
   ```

**STOP.** Do NOT read individual file diffs. You only need the `--stat` output to know which files changed. Reading diffs is the workers' job.

### Phase 2: Plan Work Items (orchestrator)

Read `.sync-map.json` and cross-reference the changed files against the `reference_docs` and `skill_triggers` mappings.

For each affected target, create a tracked work item:
- **Title**: `Update <target-file> with <brief change summary>`
- **Description** — include everything a worker needs to operate independently:
  - The eve-horizon repo path (`../eve-horizon`)
  - The commit range: `<last_synced_commit>..HEAD`
  - Which source files changed (from `--stat`)
  - The target file path to update
  - Whether this is a reference doc update, skill update, or new skill creation
  - The update rules (see "Worker Instructions" below)

Add a final work item: `Update sync state and produce report` — blocked until all updates finish.

If the user gave additional instructions (e.g., "analyze storage gaps"), add that as a separate work item too, also blocked until updates finish.

If any work item touches `eve-work/eve-read-eve-docs`, also add:
- `Run state-today compliance scan for eve-read-eve-docs`
- `Validate progressive-access routing in eve-read-eve-docs/SKILL.md`
- `Run CLI module progression check for cli task file coverage`

### Phase 3: Dispatch Workers (parallel)

Spawn one background worker per work item. Launch them all at once so they run in parallel.

**Each worker prompt must be self-contained.** The worker has no access to the orchestrator's conversation. Include:

1. The exact git command to get the diff:
   ```
   cd ../eve-horizon && git diff <last_synced_commit>..HEAD -- <source-file-1> <source-file-2>
   ```
2. The target file to read and modify
3. If diffs are large, the full source doc path to read from eve-horizon as reference
4. The appropriate update rules from below

#### Worker Instructions: Reference Docs

> Read the git diff for your assigned source files. Read the current reference doc.
> Distill only implemented behavior into the reference doc; these are curated summaries for agents, not copies of the source.
> Exclude roadmap content: remove or ignore `Planned (Not Implemented)`, `What's next`, roadmap/future sections, and "current vs planned" wording.
> Keep progressive access intact: preserve concise structure and include only task-relevant detail.
> Preserve the existing structure, voice, and formatting.
> Edit the existing file; do not rewrite from scratch.

#### Worker Instructions: Skills

> Read the git diff for your assigned source files. Read the current SKILL.md.
> Update with new commands, changed workflows, or new capabilities.
> Keep the skill state-today only: remove speculative or planned sections.
> Ensure progressive disclosure: SKILL.md should route and instruct; deep detail belongs in `references/`.
> Maintain imperative voice and conciseness. Skills teach agents how to think, not just what to type.
> Edit the existing file; do not rewrite from scratch.

#### Worker Instructions: New Skills

> Create a new directory under the appropriate pack with a SKILL.md file.
> Add a `references/` subdirectory if the skill needs detailed reference material.
> Keep all content state-today only; avoid planned/roadmap sections.
> Follow the conventions of existing skills in the same pack.

#### Example Worker Prompt

```
You are updating a reference doc in the eve-skillpacks repository.

## Your Task
Update the file: eve-work/eve-read-eve-docs/references/secrets-auth.md

## Context
The eve-horizon repo is at ../eve-horizon. Changes since commit abc1234:
- docs/system/auth.md changed (access groups, scoped bindings)
- docs/system/secrets.md changed (credential check improvements)

## Steps
1. Run: cd ../eve-horizon && git diff abc1234..HEAD -- docs/system/auth.md docs/system/secrets.md
2. Read: eve-work/eve-read-eve-docs/references/secrets-auth.md
3. If the diff is large, also read the full source files from ../eve-horizon/docs/system/
4. Distill only shipped behavior into the reference doc and exclude planned/roadmap content
5. Edit the existing file (do not rewrite it from scratch)

These are curated distillations for agents, not verbatim copies. Keep them concise and actionable.
```

### Phase 4: Collect Results and Update Tracking (orchestrator)

Wait for all workers to complete. As each finishes, mark its work item done.

Once all update work items are complete:

1. Get current HEAD:
   ```bash
   cd ../eve-horizon && git rev-parse HEAD
   ```
2. Run state-today and progressive-access checks (must return no matches/failures):
   ```bash
   ./private-skills/sync-horizon/scripts/check-state-today.sh
   ```
3. Optional: keep legacy scan references for audit:
   ```bash
   rg -n "Planned \\(Not Implemented\\)|## Planned|What's next|current vs planned|Planned vs Current" eve-work/eve-read-eve-docs -g '*.md'
   rg -n "^## Planned|Planned \\(Not Implemented\\)" eve-work eve-se eve-design -g 'SKILL.md'
   rg -n "^## Task Router \\(Progressive Access\\)" eve-work/eve-read-eve-docs/SKILL.md
   ```
4. Update `.sync-state.json`:
   - Set `last_synced_commit` to the HEAD hash
   - Set `last_synced_at` to current ISO timestamp
   - Append to `sync_log` (keep last 10 entries)
5. Update ARCHITECTURE.md if the pack structure changed (new skills added or removed)

### Phase 5: Report (orchestrator)

Output a sync report summarizing all work:

```
## Sync Report: <old_commit_short>..<new_commit_short>

### Commits
- <count> commits synced

### Platform Changes
- <list of eve-horizon changes that affected skillpacks>

### Updated Reference Docs
- <file>: <what changed>

### Updated Skills
- <skill>: <what changed>

### New Skills
- <skill>: <why created>

### State-Today Compliance
- <pass/fail + scan results>

### Progressive Access Updates
- <routing or reference-structure improvements made>

### Optional Automated Guard
- `private-skills/sync-horizon/scripts/check-state-today.sh` run status

### Next Steps
- <any manual follow-up needed>
```

## Key Constraints

- **Orchestrator context budget**: The orchestrator must never read full diffs or source docs directly. It only sees: sync state JSON, sync map JSON, `--stat` output, commit log, and worker result summaries.
- **Worker independence**: Each worker prompt must be fully self-contained — commit range, source paths, target path, and update rules all included. Workers cannot reference the orchestrator's conversation.
- **Parallelism**: All workers launch simultaneously. No worker depends on another worker's output.
- **Edit, don't rewrite**: Workers modify existing files incrementally. Full rewrites lose carefully curated structure.
- **State-today fidelity**: Output docs and skills must represent current, shipped behavior only.
- **Progressive access**: Preserve task-first routing in entry skills and keep deep detail in references.
