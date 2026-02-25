---
name: git-worktree-runner
description: >
  Guide for using gtr (git-worktree-runner), a CLI tool for managing git worktrees
  with editor and AI tool integration. Use this skill when the user asks about:
  (1) creating, managing, or removing git worktrees,
  (2) setting up gtr / git-gtr for a project,
  (3) configuring editors (Cursor, VS Code, Zed) or AI tools (Claude Code, Aider, Codex, Gemini) with worktrees,
  (4) running parallel development workflows across multiple branches,
  (5) copying config/env files to new worktrees,
  (6) setting up hooks for worktree creation/removal,
  (7) troubleshooting git worktree issues,
  (8) any mention of "gtr", "git gtr", "git worktree runner", or "worktree" in context of parallel dev.
  Triggers on keywords: gtr, git-gtr, worktree, parallel branches, multi-branch workflow.
---

# git-worktree-runner (gtr)

A portable CLI for managing git worktrees with editor and AI tool integration. Wraps `git worktree` with quality-of-life features for modern parallel development.

## Installation

```bash
git clone https://github.com/coderabbitai/git-worktree-runner.git
cd git-worktree-runner
sudo ln -s "$(pwd)/bin/git-gtr" /usr/local/bin/git-gtr
```

Requires Git 2.5+ and Bash 3.2+. Shell completions available for Bash, Zsh, and Fish.

## Core Workflow

```bash
cd ~/your-repo
git gtr config set gtr.editor.default cursor    # one-time
git gtr config set gtr.ai.default claude         # one-time

git gtr new my-feature          # create worktree
git gtr editor my-feature       # open in editor
git gtr ai my-feature           # start AI tool
git gtr run my-feature npm test # run commands
git gtr rm my-feature           # clean up
```

Use `1` to reference the main repo (e.g., `git gtr ai 1`).

## Commands Reference

| Command | Purpose |
|---|---|
| `git gtr new <branch> [opts]` | Create worktree. Options: `--from <ref>`, `--from-current`, `--track`, `--no-copy`, `--no-fetch`, `--force` (requires `--name`), `--name <suffix>`, `--yes` |
| `git gtr editor <branch>` | Open in configured editor. Override: `--editor <n>` |
| `git gtr ai <branch> [-- args]` | Start AI tool. Override: `--ai <n>`. Pass args after `--` |
| `git gtr go <branch>` | Print path. Use: `cd "$(git gtr go my-feature)"` |
| `git gtr run <branch> <cmd>` | Execute command in worktree directory |
| `git gtr rm <branch>... [opts]` | Remove worktree(s). Options: `--delete-branch`, `--force`, `--yes` |
| `git gtr list [--porcelain]` | List all worktrees |
| `git gtr config {get\|set\|add\|unset} <key> [val]` | Manage config. Add `--global` for global scope |
| `git gtr doctor` | Health check |
| `git gtr adapter` | List available editor & AI adapters |
| `git gtr clean` | Remove stale worktrees |

## Configuration

All config stored via `git config`. For full configuration details including worktree directory settings, file copying patterns, hooks, and advanced usage, read [references/configuration.md](references/configuration.md).

### Key Config Values

```
gtr.worktrees.dir      # base directory for worktrees (default: <repo>-worktrees)
gtr.worktrees.prefix   # folder prefix (default: "")
gtr.defaultBranch      # default branch (default: auto-detect)
gtr.editor.default     # editor: cursor, vscode, zed, none
gtr.ai.default         # AI tool: claude, aider, codex, continue, cursor, gemini, opencode, none
gtr.copy.include       # glob patterns for files to copy (multi-valued)
gtr.copy.exclude       # glob patterns to exclude (multi-valued)
gtr.copy.includeDirs   # directories to copy (e.g., node_modules)
gtr.copy.excludeDirs   # directory patterns to exclude
gtr.hook.postCreate    # commands to run after creation (multi-valued)
gtr.hook.postRemove    # commands to run after removal (multi-valued)
```

## Common Scenarios

**Parallel AI agents on one feature:**
```bash
git gtr new feature-auth
git gtr new feature-auth --force --name backend
git gtr new feature-auth --force --name frontend
git gtr ai feature-auth-backend -- --message "Implement API"
git gtr ai feature-auth-frontend -- --message "Build UI"
```

**Node.js project setup:**
```bash
git gtr config set gtr.editor.default cursor
git gtr config add gtr.copy.include "**/.env.example"
git gtr config add gtr.hook.postCreate "npm install"
git gtr config add gtr.hook.postCreate "npm run build"
```

**Non-interactive automation (CI/scripts):**
```bash
git gtr new ci-test --yes --no-copy
git gtr rm ci-test --yes --delete-branch
```

## Troubleshooting

- **Worktree creation fails**: Run `git fetch origin` first. Check branch exists with `git branch -a | grep <branch>`. Try `--track remote`.
- **Editor not opening**: Verify command available (`command -v cursor`). Check config: `git gtr config get gtr.editor.default`.
- **File copying issues**: Check patterns: `git gtr config get gtr.copy.include`. Test with `find . -path "<pattern>"`.
- **Health check**: Run `git gtr doctor` to verify git, editors, and AI tools are properly configured.

## Platform Support

- macOS: Full support (Ventura+). GUI: `open`, terminal: iTerm2/Terminal.app
- Linux: Full support. GUI: `xdg-open`, terminal: gnome-terminal/konsole
- Windows: Git Bash or WSL required
