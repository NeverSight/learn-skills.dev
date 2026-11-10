---
name: update-project-doc
description: "Update a project's own CLAUDE.md, README.md, or docs/ to reflect current state. Use when the user asks to update a project's own CLAUDE.md, README.md, or docs/ to reflect current state."
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(ls*), Bash(git log*), Bash(git diff*), Bash(readlink*), Bash(wc*), Bash(date*), AskUserQuestion
argument-hint: (no arguments)
---

# Update Project Doc — Refresh Stale Documentation

> Scan a project's documentation files and update sections that have drifted from reality: file trees, timestamps, bibliography counts, next steps, skill/hook tallies, and more.

## When to Use

- After significant project work (new files, completed milestones, structural changes)
- During `session-close` when offered
- When the user says "update project docs", "refresh docs", "sync my docs", "update my README"
- Periodically to keep documentation accurate

## What It Does NOT Do

- Never rewrites research content (hypotheses, arguments, literature, design decisions)
- Never deletes sections — only updates factual/structural content within existing sections
- Never creates new documentation files — only updates existing ones

---

## Protocol

### Step 1: Detect Documentation Files

Find all documentation files in the project:

1. Check for `CLAUDE.md` in project root
2. Check for `README.md` in project root
3. Scan `docs/` and `docs/*/` for `.md` files containing file trees or counts
4. Note which files exist — only update what's present

**Special case:** Some projects (e.g., the political information paper) have no `CLAUDE.md` because they use a committed `README.md` as their primary project documentation instead. This is intentional for repos meant to be shared or published. In these cases, treat `README.md` as the main documentation file and apply all the same checks to it.

Read each detected file to understand its current content.

### Step 2: Gather Current State

Collect the actual state of the project:

1. **File tree** — use `ls -R` or `Glob` to build the actual directory structure (respect `.gitignore` patterns, skip `out/`, `__pycache__/`, `.venv/`, `node_modules/`)
2. **Recent git history** — `git log --oneline -20` for recent commits
3. **Session logs** — read the latest 1-2 files in `log/` (if the directory exists)
4. **Bibliography count** — count entries in any `.bib` file(s): `grep -c '@' *.bib`
5. **Symlink targets** — `readlink` on any documented symlinks
6. **Context files** — read `.context/current-focus.md` or `.context/project-recap.md` if present

**Task Management only** (detected by presence of `skills/` directory):
7. **Skill count** — count directories in `skills/` that contain `SKILL.md`
8. **Hook count** — count `.sh` files in `hooks/` (if present)
9. **Skill lengths** — `wc -l skills/*/SKILL.md` to identify bloated skills

**Leanness data** (all projects):
10. **CLAUDE.md line count** — `wc -l CLAUDE.md`
11. **CLAUDE.md section sizes** — count lines per `##` section
12. **README.md line count** — `wc -l README.md`
13. **SKILL.md line counts** — (Task Management only) `wc -l skills/*/SKILL.md`
14. **Duplication scan** — check if CLAUDE.md content duplicates what's already in README.md, docs/, or .context/ files
15. **Agent line counts** — `wc -l .claude/agents/*.md` (if present)
16. **Context file line counts** — `wc -l .context/*.md` (if present)

### Step 3: Run Staleness Checks

Compare gathered state against documented content. Flag any mismatches:

| Check | How to Detect |
|-------|--------------|
| **File tree** | Generate actual tree, compare against any tree/structure block in docs (look for ``` blocks or indented listings with file paths) |
| **Timestamps** | Flag "Last updated", "w/c", or date stamps older than 7 days |
| **Bibliography count** | Compare actual `.bib` entry count vs any documented count (e.g., "42 references") |
| **Next steps / roadmap** | Cross-reference items against recent commits and session logs — flag items that appear completed |
| **Manuscript status** | Flag sections marked "TODO", "incomplete", or "placeholder" that now have content |
| **Symlinks** | Verify documented symlink targets still resolve with `readlink` |
| **Skill/hook counts** | (Task Management only) Compare actual count vs documented numbers in CLAUDE.md, README.md, and `.tex` files |
| **Venue/target info** | If CLAUDE.md documents a target journal, check it matches `.context/projects/_index.md` (if accessible) |

### Step 3b: Leanness Audit

Using the data gathered in Step 2 (items 10-14), check infrastructure file sizes against thresholds. This applies to **all projects**, not just Task Management.

| File | Threshold | What to flag | Fix |
|------|-----------|-------------|-----|
| `CLAUDE.md` or `AGENTS.md` | Exceeds the `lean-guidance-files` budget | Current line and word count | Extract reference sections to `docs/`, replace with pointers |
| `CLAUDE.md` sections | Any `##` section > 15 lines of reference material | Section name + line count | Extract to `docs/` with a one-line summary + link |
| `CLAUDE.md` duplication | Content duplicated from README/docs/.context | Which content is duplicated and where | Keep only the pointer in CLAUDE.md |
| `README.md` | > 300 lines total | Current line count | Extract long sections to `docs/` |
| `SKILL.md` files | > 300 lines each (TM only) | File name + line count | Move templates/examples/report formats to `references/` or `templates/` subdirectory |
| Project agents (`.claude/agents/*.md`) | > 400 lines each | File name + line count | Extract verbose prompt sections to companion files |
| Context files (`.context/*.md`) | > 200 lines each | File name + line count | Archive stale content, keep current |

**What counts as "reference material"** (extractable): assessment guidelines, detailed literature notes, long examples, report templates, checklists, reviewer feedback.

**What does NOT count** (keep in place): safety rules, conventions, folder structure trees, session continuity pointers.

Present leanness findings separately from staleness findings in Step 4.

### Step 4: Propose Changes

Present findings grouped by file:

```
Staleness report for [Project Name]:

CLAUDE.md:
  - File structure tree is outdated (missing: X, Y; removed: Z)
  - Skill count says 23, actual is 26
  - "Last updated" date is 3 weeks old

README.md:
  - Directory structure block needs updating
  - Next steps: "Write introduction" appears completed (commit abc1234)
  - Bibliography count says 38, actual is 42

docs/overview.md:
  - No issues detected

Leanness:
  - CLAUDE.md: 237 lines (threshold: 200) — ## Assessment section is 42 lines of guidelines
  - README.md: OK (189 lines)
```

If nothing is stale, report that and stop.

### Step 5: Ask for Confirmation

#### Step 5a: Staleness Fixes

Use `the available structured-question mechanism` to let the user approve, modify, or skip staleness fixes:

- **Apply all** — update everything proposed
- **Select by file** — choose which files to update
- **Skip** — make no changes

#### Step 5b: Offer Leanness Fixes

If Step 3b found leanness issues, present each as an individually actionable item:

```
Leanness fixes available:

| # | File | Issue | Current | Fix |
|---|------|-------|---------|-----|
| 1 | CLAUDE.md | >200 lines | 237 | Extract ## Assessment section → docs/ |
| 2 | skills/X/SKILL.md | >300 lines | 382 | Move checklists → references/ |
```

Use `the available structured-question mechanism` with `multiSelect: true`:
- **Question:** "Which leanness fixes do you want to apply?"
- One option per fix with current size and proposed outcome
- Include an **"All of them"** option as the first choice

**Do not defer or merely report leanness findings.** Always present them as actionable items alongside staleness fixes.

### Step 6: Apply and Report

For each approved change:

1. Use **targeted `Edit` operations** — never rewrite entire files
2. Preserve all surrounding content
3. When updating file trees, match the existing formatting style (├──, |--, indented, etc.)
4. When updating counts, find the exact number and replace it
5. When marking next-step items as done, use strikethrough (~~item~~) rather than deleting

After all edits, print a summary:

```
Updated project docs:
  CLAUDE.md:  file tree, skill count (23 → 26)
  README.md:  directory structure, bib count (38 → 42), 1 next-step marked complete
  Total: 5 edits across 2 files
```

---

## Key Rules

1. **Targeted edits only** — never rewrite entire files. Use `Edit` with precise `old_string` / `new_string`.
2. **Preserve research content** — hypotheses, questions, literature reviews, design decisions, and arguments are sacred. Only update factual/structural sections.
3. **Always show before applying** — never make silent edits. The proposal step is mandatory.
4. **Match existing style** — if the project uses `├──` trees, don't switch to `|--`. If counts use "X total", don't change to "X skills".
5. **Works in any project** — not just Task Management. Adapt checks to what's present.
6. **Idempotent** — running twice in a row should produce no changes the second time.

## Cross-References

- `session-close` — offers to run this skill at Step 3.5
- `sync-repo private` — Task Management-specific superset: propagates counts across all private TM docs including LaTeX files. Run after this skill when in the TM project.
- `vault sync (edit vault files directly)` — syncs state to the central context library (complementary; run after this)
- `update-focus` — updates `current-focus.md` (different purpose: session state, not doc accuracy)
