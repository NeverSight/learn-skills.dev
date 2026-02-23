---
name: done
description: Captures key decisions, questions, follow-ups, and learnings at end of a coding session. Writes a single markdown file per session. Use when done with a session, wrapping up work, running /done, creating a session summary, saving session context, or ending a coding session.
---

# Done

Distill the current session into a single markdown file capturing decisions, questions, next steps, and context for future sessions.

Manual, end-of-session action. Not every session needs it — skip when the session was trivial or exploratory with no decisions worth preserving.

## Workflow

Copy this checklist to track progress:

```
Done progress:
- [ ] Step 1: Gather context
- [ ] Step 2: Assess significance
- [ ] Step 3: Write session file
- [ ] Step 4: Confirm
```

### Step 1: Gather context

Collect automatically — do not ask the user:

**Git context:**
- Current branch: `git branch --show-current`
- Files changed: `git diff --name-only` and `git diff --cached --name-only`
- Recent commits: `git log --oneline -10`

**Session context:**
- Claude session ID
- Key decisions made and their reasoning
- Questions raised (answered and unanswered)
- Blockers encountered
- Patterns or learnings discovered

If not in a git repo, use `no-repo` as branch and skip files-changed.

### Step 2: Assess significance

- **Write a file** when: decisions were made, architecture was discussed, non-obvious approaches were chosen, there are open questions, or meaningful code was written.
- **Skip** when: quick fix with no decisions, pure exploration with no conclusions, or the user says it is not needed.

If skipping, tell the user why and stop.

### Step 3: Write session file

**Location:**

Default: `.claude/done/` in the repo root.

If the folder does not exist, create it:

```bash
mkdir -p .claude/done
```

The user can override this path in their CLAUDE.md or CLAUDE.local.md:

```markdown
Session files go in /path/to/my/folder
```

If the custom path does not exist, create it with `mkdir -p` before writing.

Common alternatives: an Obsidian vault folder, `docs/sessions/`, or any custom path.

**Filename:** `YYYY-MM-DD-<branch>-<short-session-id>.md`
- Branch: `/` replaced with `-`, truncated at 40 chars
- Session ID: first 8 chars
- Example: `2026-02-19-feat-auth-a1b2c3d4.md`

**Template:**

```markdown
# Session: YYYY-MM-DD <branch>

**Session ID:** <id>
**Branch:** <branch>
**Date:** <date>

## Summary

1-2 sentences of what was accomplished.

## Decisions

- **Decision title**: What was decided. Why this approach was chosen.

## Questions

- [ ] Open question
- [x] Resolved question — answer

## Next Steps

- [ ] Specific actionable task

## Files Changed

- `path/to/file` — what changed and why

## Learnings

- Non-obvious gotcha or pattern discovered

## Context for Next Session

Where to pick up. What state is the code in. What needs attention first.
```

**Writing rules:**
- Omit any section with no content
- Bullets, not paragraphs
- Decisions must include the "why"
- Next steps must be actionable without re-reading the session
- If 20+ files changed, summarize by directory
- Never overwrite existing session files

### Step 4: Confirm

Report the file path and a one-line summary:

```
Session captured: .claude/done/2026-02-19-feat-auth-a1b2c3d4.md

Sections: decisions (3), questions (1 open), next steps (4), files changed (7)
```

## Anti-patterns

- Do not create a file for trivial sessions (quick typo fix, one-liner)
- Do not include full code snippets — reference file paths and line numbers instead
- Do not ask the user to fill in sections — extract everything from session context
- Do not overwrite existing session files — each session gets a unique file
- Do not create rolling/append files (like PROJECT-STATUS.md) — one file per session
- Do not modify any project files other than the session file itself
