---
name: checkpoint
description: Save developer context to Goldfish memory — checkpoint proactively and often
allowed-tools: mcp__goldfish__checkpoint
---

# Checkpoint — Save Developer Memory

## The Golden Rule

NEVER ask "should I checkpoint?" — checkpoint at milestones and continuation boundaries, without asking permission.

Every checkpoint you skip is context that future sessions lose forever. `mcp__goldfish__recall` can only return what you've saved. No checkpoints = no memory = starting from scratch every time.

## When to Checkpoint

### MANDATORY milestone moments:
- **Completed a meaningful deliverable** — feature slice, bug fix, or refactor step
- **Made a decision** — architecture/tradeoff that future sessions must follow
- **Captured continuation context** — state needed to resume after crash or context loss
- **Before risky changes** — create a clear save point for reconstruction
- **Before context compaction** — preserve active state and next step
- **User shared requirements/constraints** — preserve what future work must honor
- **Found a blocker or discovery** — capture root cause and path forward

### Good habit moments:
- After successful test runs
- After resolving merge conflicts
- After debugging sessions (even unsuccessful ones — capture what you eliminated)
- When you figure out something non-obvious about the codebase

## How to Write Good Descriptions

Your description becomes the **markdown body** of a `.md` file. Format it with structure — headers, bullet points, bold, code spans. NOT a wall of text.

### The WHAT/WHY/HOW/IMPACT Formula (use markdown)

```
mcp__goldfish__checkpoint({
  description: "## Implemented JWT refresh token rotation\n\nThe existing single-token approach was vulnerable to token theft.\n\n- **Approach:** Rotate tokens on each use, limiting the attack window\n- **Added:** `RefreshTokenStore` with atomic file writes and 7-day expiry\n- **Tests:** All 12 auth tests passing\n- **Impact:** Unblocks the session management PR",
  tags: ["feature", "auth", "security"]
})
```

### Good vs Bad Descriptions

**GOOD (structured markdown):**
```
## Fixed race condition in checkpoint writes

Concurrent saves could corrupt the daily markdown file.

- **Root cause:** Non-atomic write pattern
- **Fix:** Switched to write-tmp-then-rename with file locking
- **Verified:** Reproduced with parallel test, confirmed fix
```

**BAD (wall of text):**
"Fixed race condition in checkpoint file writes where concurrent saves could corrupt the daily markdown file. Root cause was non-atomic write pattern — switched to write-tmp-then-rename. Added file locking with exclusive create flag. Reproduced with parallel test and confirmed fix."

**BAD (no context):**
"Fixed file writing bug"

## How to Choose Tags

Tags are for categorization, not for repeating the description. Keep them short and consistent.

### Useful tag patterns:
- **Type:** `feature`, `bug-fix`, `refactor`, `docs`, `test`, `config`
- **Area:** `auth`, `api`, `ui`, `database`, `build`
- **Status:** `wip`, `blocked`, `discovery`, `decision`
- **Priority:** `critical`, `minor`

### Example:
```
mcp__goldfish__checkpoint({
  description: "## Redesigned plan storage format\n\nSwitched from separate JSON metadata to YAML frontmatter in markdown files.\n\n- **Why:** Aligns plans with checkpoint format, makes everything grep-friendly\n- **Migration:** Script handles existing plans automatically\n- **Breaking:** Plan IDs change from numeric to slug-based",
  tags: ["refactor", "plans", "breaking-change"]
})
```

## What Gets Captured Automatically

You don't need to include these in your description — Goldfish captures them:
- **Git branch** — current branch name
- **Git commit** — current HEAD short hash
- **Changed files** — files modified since last commit
- **Timestamp** — UTC, always

Focus your description on the MEANING, not the mechanics.

## Checkpoint Frequency

Think of checkpoints like git commits — milestone-level, descriptive, and continuation-focused.

- **Too few:** Context gaps that make future recall weak
- **High value:** Milestones, decisions, blockers, and resumability context
- **Best quality:** Each checkpoint should help future-you continue confidently

Checkpoint for continuity quality, not raw quantity.

## Critical Rules

- **NEVER ask permission.** Checkpointing is your job. Just do it.
- **NEVER write lazy descriptions.** "Did stuff" helps nobody. Write for your future self who has zero context.
- **ALWAYS checkpoint before compaction.** If context is about to be lost, save it first.
- **ALWAYS checkpoint after discoveries.** Non-obvious findings are the most valuable things to preserve.
- **Checkpoint FIRST, continue work SECOND.** Save state before moving on.
