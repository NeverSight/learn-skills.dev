---
name: jaan-issue-solve
description: Post supportive comments on closed issues referenced in release changelog
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion
---

# jaan-issue-solve

> Answer closed GitHub issues with warm, supportive comments that explain how the release solved their problem.

## Context Files

Read these before execution:
- `.claude/skills/jaan-issue-solve/LEARN.md` - Past lessons
- `.claude/skills/jaan-issue-solve/template.md` - Comment template
- `CHANGELOG.md` - Release changelog

## Input

**Arguments**: $ARGUMENTS

Parse from arguments:
1. **Version** — Tag to process (e.g., `v6.1.0`). Default: latest git tag.
2. **--dry-run** — Preview comments without posting.

If no arguments provided, detect the latest tag: `git tag --sort=-v:refname | head -1`

---

## Pre-Execution: Apply Past Lessons

**MANDATORY FIRST ACTION** — Read `.claude/skills/jaan-issue-solve/LEARN.md`

If the file exists, apply its lessons throughout execution.

---

# PHASE 1: Analysis (Read-Only)

## Step 1: Verify GitHub CLI

```bash
gh auth status
```

If not authenticated, stop: "GitHub CLI is not authenticated. Run `gh auth login` first."

## Step 2: Determine Target Version

- If version provided in arguments, use it
- Otherwise: `git tag --sort=-v:refname | head -1`
- Confirm: "Targeting release **vX.Y.Z**"

## Step 3: Read Changelog from Main Branch

```bash
git show main:CHANGELOG.md
```

Extract the section for the target version — content between `## [X.Y.Z]` and the next `## [` header.

## Step 4: Extract Issue References

Parse all `#XX` references from the version's changelog section. Collect unique issue numbers.

If no issue references found, report: "No issue references found in changelog for vX.Y.Z" and stop.

## Step 5: Query Each Issue

For each issue reference `#XX`:

```bash
gh issue view XX --json number,title,state,body,comments
```

Build an issue table with columns: Number, Title, State, Already Commented, Eligible.

**Skip rules:**
- **Open issues** — skip (only comment on closed issues)
- **Already commented** — check if any existing comment contains the version string (e.g., "v6.1.0"). If yes, skip (idempotent).

## Step 6: Draft Comments

For each eligible closed issue, read the `.claude/skills/jaan-issue-solve/template.md` and draft a comment:

1. **Opening** — `**Resolved in [vX.Y.Z](https://github.com/{owner}/{repo}/releases/tag/vX.Y.Z)** (\`commit_ref\`)`
2. **Resolution details** — Match the issue to specific changelog entries that reference it. Explain what changed and how it addresses the user's problem. Be specific — don't just say "this was fixed", explain the actual mechanism.
3. **Closing note** — Warm, thankful: "Thank you for reporting this." or "We appreciate you raising this issue."

**Tone rules:**
- Warm and supportive, never robotic or formulaic
- Reference the specific fix, not just the version
- Thank the reporter
- Include commit refs where the changelog provides them
- Link to full changelog at the end

## Step 7: HARD STOP — Preview

Present all drafted comments in a table:

```
ISSUE COMMENT PREVIEW
=====================
Issues found: {total}
Eligible (closed, no prior comment): {eligible}
Skipped (open): {open_count}
Skipped (already commented): {already_count}

---
#{XX} — {title}
[Full comment preview]
---
#{YY} — {title}
[Full comment preview]
---
```

If `--dry-run` flag is set:
> "Dry run complete. No comments posted. Remove --dry-run to post."
> STOP here.

Otherwise, ask user:
> "Post these {N} comments? [y/n/edit]"

**Do NOT proceed without explicit approval.**

---

# PHASE 2: Post Comments

## Step 8: Post Comments

For each approved comment:

```bash
gh issue comment XX --body "..."
```

Report each: "Posted comment on #XX — {title}"

## Step 9: Summary

```
RESULTS
=======
Posted: {count}
Skipped (open): {open_count}
Skipped (already commented): {already_count}
Failed: {fail_count}

Issues commented:
- #{XX} — {title}
- #{YY} — {title}
```

## Step 10: Capture Feedback

> "Any feedback on the comments or this workflow? [y/n]"

If yes, append to `.claude/skills/jaan-issue-solve/LEARN.md` under the appropriate section.

---

## Definition of Done

- [ ] Target version identified
- [ ] Changelog parsed for issue references
- [ ] All closed issues received warm, specific comments
- [ ] No open issues were commented on
- [ ] No duplicate comments posted (idempotent)
- [ ] User approved all comments before posting
