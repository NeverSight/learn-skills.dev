---
name: verify-worktree-plugins
description: "Verify worktree plugin patches are intact after plugin updates. Checks compound-engineering and superpowers skills for Claude Code launch instructions."
---

# Verify Worktree Plugin Patches

After plugin updates, the worktree skills (compound-engineering `git-worktree`, superpowers `using-git-worktrees`) lose custom patches that tell Claude Code to launch new instances in worktree directories.

## What This Checks

| Component | What's Verified |
|---|---|
| compound-engineering SKILL.md | "Claude Code + Worktree Working Directory" section |
| compound-engineering worktree-manager.sh | "Open a NEW Claude Code instance" banner after create |
| superpowers SKILL.md | "Launch Claude Code" in step 5 report |
| PreCompact hook | `getWorktreeContext` function for compaction survival |

Both marketplace and latest cache versions are checked.

## Instructions

### 1. Run the verification script

```bash
bash ~/.claude/scripts/verify-worktree-plugins.sh
```

### 2. If any checks fail, re-apply patches

```bash
bash ~/.claude/scripts/verify-worktree-plugins.sh --patch
```

### 3. If the PreCompact hook is missing worktree detection

The `--patch` flag cannot auto-fix the TypeScript hook. Regenerate it manually:

The hook at `~/.claude/hooks/context-compression-hook.ts` needs a `getWorktreeContext()` function that:
1. Runs `git rev-parse --git-dir` to detect if CWD is a worktree (path contains `/worktrees/`)
2. If yes, outputs branch, worktree path, and main repo path
3. This output gets injected as a `<system-reminder>` during compaction

Regenerate it with this structure:
```typescript
import { execSync } from "node:child_process";

function getWorktreeContext(): string | null {
  // Check git-dir for "/worktrees/" to detect worktree
  // Return formatted context string with branch, path, main repo
  // Return null if not in a worktree
}

// In main(): call getWorktreeContext() and console.log if non-null
```

### 4. Report results to the user

Show the verification output and note any files that needed patching.

## Background

Claude Code's statusline, git context, and system prompt are set at **launch time**. Running `cd` in a Bash tool call does NOT change the process CWD. After auto-compact, Claude reverts to the launch directory's context. Each worktree needs its own Claude Code instance launched from that directory (`cd /path && claude`).

The worktree plugin patches ensure Claude always tells the user to open a new terminal and launch Claude Code from the worktree directory after creation.

## When to Run

- After updating the `compound-engineering` plugin
- After updating the `superpowers` plugin
- If worktree creation stops showing the "launch Claude Code" instructions
- Periodically as a sanity check
