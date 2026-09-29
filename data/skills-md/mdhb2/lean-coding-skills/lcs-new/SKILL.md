---
name: lcs-new
description: >
  Register a blank work item without creating explore, PRD, SRS, task, code, or documentation artifacts.
  Use when the user asks to create a new work item, register a work item, start a new task,
  buat work item baru, or daftarkan pekerjaan baru before any exploration or planning.
  Do NOT trigger when the user is asking to brainstorm, create a PRD, debug, execute tasks,
  review code, or do any other workflow action directly.
---

# lcs-new — Blank Work Item Registration

Register a new blank work item in the LCS state registry. No artifacts are created inside the work-item directory.

## Chain of Truth Level

Level: Standard

## When to Use

Trigger on explicit intents such as:

- `lcs-new`
- "create new work item"
- "buat work item baru"
- "register a work item"
- "daftarkan pekerjaan baru"

Do not trigger when the user is asking to brainstorm, create a PRD, debug, execute tasks, or review code directly.

## Input

A concise work-item name/title.

If no usable title is supplied, ask only for the work-item name.

## Steps

1. Read `.lcs/state.md` if it exists.
2. If state does not exist, create it from the canonical state template at `skills/lcs-shared/templates/state.template.md`. Ensure `work_items: {}` is present.
3. Ensure `.lcs/work-items/` exists.
4. Generate:
   - work ID: `{YYYYMMDD-HHmmss}-{kebab-slug}` (use current timestamp)
   - path: `.lcs/work-items/{work-id}`
5. Create the work-item directory. Do NOT create any file inside it — no `.gitkeep`, no placeholder.
6. Add one registry entry to state:

```yaml
work_items:
  "{work-id}":
    title: "{user title}"
    path: ".lcs/work-items/{work-id}"
    phase: new
    status: open
    created_at: "{ISO timestamp}"
    updated_at: "{ISO timestamp}"
```

7. Select the new work item:

```yaml
current_work: "{work-id}"
current_phase: new
```

8. Update state `timestamp` and `last_session_note`.
9. Stop. Do not generate `explore.md`, PRD, task files, code, docs, `.gitkeep`, or session artifacts.

## Rollback

If the state write fails after creating the empty directory, delete the directory only if it is still empty, then report failure. Do not leave a silently orphaned blank work item.

## What This Skill Does NOT Do

- Does not create `explore.md`, `prd.md`, `srs.md`, `tests.md`, `task-coverage.md`, or any task files
- Does not create `code-review.md` or `doc.md`
- Does not create `.gitkeep` or any placeholder file
- Does not invoke `lcs-explore`, `lcs-toprd`, or any other skill automatically
- Does not switch to a different work item if one is already selected (only registers a new one)

## Chain of Truth Report
### Level
Standard

### Sources Checked
- `.lcs/state.md`
- `skills/lcs-shared/templates/state.template.md`
- <additional files read>

### Assumptions
- <label each [verified] or [unverified]>

### Plan
1. <Step one>
2. <Step two>

### Actions Taken
<Per-step record of what was done: state read/init, ID/path generated, directory created, registry entry added, item selected>

### Verification
<State read-back result confirming the new entry, selection, and that no artifact files were created>

### Report
<Structured summary with confidence rating>

## Handoff

```markdown
## Handoff

Next recommended skill:
Next file to read:
Current phase: new
Current confidence:
Blocking questions:
Risks to carry forward:
Source of Truth Bundle:
Must Preserve IDs:
Unresolved IDs:
Suggested next command:
```

End with a concise handoff recommending either `lcs-explore` or `lcs-toprd` depending on user intent, but do not invoke them automatically.
