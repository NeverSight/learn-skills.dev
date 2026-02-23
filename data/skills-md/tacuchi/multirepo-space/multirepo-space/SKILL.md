---
name: multirepo-space
description: |
  Scaffold and manage multi-repo workspaces for AI coding agents.
  Delegates to the multirepo-space CLI (bundled). Use when user says
  "create workspace", "setup multirepo", "multi-repo workspace",
  "add repo to workspace", "remove repo from workspace",
  "workspace status", "check workspace health", "init multi-repo",
  "orchestrate repos", "link repositories".
  Also use when user has multiple repos and needs a central
  coordination point for AI agents (Claude Code, Codex, Gemini CLI).
---

# multirepo-space

## Quick routing

User intent → Command:
- "Create/scaffold workspace" → `setup`
- "Add a repo" → `add` (verify workspace exists with `status` first)
- "Remove/detach repo" → `remove`
- "Check/verify/health" → `status`
- Single repo project → DO NOT use this Skill
- Monorepo (Nx/Turborepo) → DO NOT use this Skill

## Before running — decision guide

Ask the user before executing:
1. Does the workspace directory already exist? If not, create it first (`mkdir`).
2. Is this a NEW workspace or adding to an EXISTING one? → `setup` vs `add`.
3. Are all repo paths absolute? They MUST be absolute — symlinks break with relative paths.
4. First time? Always suggest `--dry-run` so user can preview changes.

## Flags — when to use each

| Flag | Use when | Do NOT use when |
|------|----------|-----------------|
| `--dry-run` | First run, user not familiar with tool | Re-runs after preview was approved |
| `--yes` | Automated pipelines, user already confirmed in chat | First time, destructive changes |
| `--verbose` | Debugging, verifying stack detection | Normal execution |

## If detect_stack returns "Generic"

The CLI creates the specialist agent without verify commands. Ask the user:
"Stack was not auto-detected for [repo]. What is the main language/framework?"
Then manually add verify commands to the generated specialist agent file.

## When NOT to use this

- Single repo projects — no benefit, just overhead.
- True monorepos (one repo, multiple packages) — use monorepo tools (Nx, Turborepo) instead.
- Repos that must stay completely independent — managed blocks modify external repos' AGENTS.md/CLAUDE.md.

## NEVER

- Run `setup` on a populated workspace without confirming with the user first.
- Use relative paths for repos — symlinks will break when working directory changes.
- Skip `--dry-run` for first-time users — always suggest preview first.
- Assume symlinks always work on Windows — the PowerShell port falls back to junctions when symlinks need elevation, but junctions only support local directories (not network paths).
- Assume workspace exists — verify with `status` before running `add` or `remove`.
- Create the workspace directory inside one of the repos — it must be a sibling or independent path.
- Edit managed blocks manually in external repos — they get overwritten on next `add`/`setup`.
- Run `add` with a repo whose basename matches an existing alias — the previous specialist gets overwritten without warning.
- Modify `settings.json` manually — the CLI expects a specific format and manual edits can break parsing in `add`/`remove`.
- Run `setup`/`add` while another agent is using the workspace — managed blocks and settings can end up in an inconsistent state.

## Detect OS and run

- macOS/Linux/WSL: `bash "$SKILL_DIR/scripts/multirepo-space" <subcommand> [args]`
- Windows PowerShell: `powershell "$SKILL_DIR/scripts/multirepo-space.ps1" <subcommand> [args]`

Replace `$SKILL_DIR` with the absolute path to this skill's directory.

Templates are in `$SKILL_DIR/templates/` — read them to understand what files get generated (e.g., `workspace-instructions.md.tmpl`, `coordinator.md.tmpl`, `specialist.md.tmpl`).

## Script behavior summary

The scripts (`scripts/multirepo-space` for bash, `scripts/multirepo-space.ps1` for PowerShell) are fully offline — they make NO network requests and do NOT modify system files.

What each subcommand does:
- `setup`: reads repo manifest files (package.json, pom.xml, etc.) to detect tech stacks, then generates `.md` agent files, `.claude/settings.json`, and symlinks inside the workspace directory. Also appends a managed block to `AGENTS.md`/`CLAUDE.md` in each listed repo.
- `add`: same as setup but for a single repo added to an existing workspace.
- `remove`: deletes the specialist agent file and symlink for a repo, and removes the managed block from the repo's `AGENTS.md`/`CLAUDE.md`.
- `status`: read-only — checks symlink health, agent file parity, and config existence. Writes nothing.

All extracted values from repo files are sanitized (length-limited, control characters and injection patterns stripped) before being inserted into templates.

Scope of filesystem writes is limited to:
1. The workspace directory (files it creates)
2. `AGENTS.md`/`CLAUDE.md` inside each configured repo (managed block only, delimited by `<!-- MULTIREPO_SPACE_MANAGED:START/END -->` markers)

## Subcommands

- `setup <workspace_path> <repo1> [repo2...]` — Scaffold new workspace
- `add <workspace_path> <repo_path>` — Add repo to existing workspace
- `remove <workspace_path> <alias>` — Detach repo from workspace
- `status <workspace_path>` — Check workspace health

Flags: `--yes` (no prompts), `--dry-run` (preview), `--verbose`

## After running

- Run `status <workspace_path>` to verify all symlinks are healthy and agents are in parity.
- Check that AGENTS.md and CLAUDE.md exist in both the workspace and each external repo.
- If `setup` failed mid-way, it's safe to re-run — existing files get overwritten.
- To start working: `cd <workspace_path> && claude` or `cd <workspace_path> && codex`.

## Common issues

- **"Workspace path does not exist"**: create directory first, then run `setup`.
- **Broken symlinks after moving repos**: re-run `setup` with updated absolute paths.
- **"Permission denied" on Windows**: run PowerShell as Administrator for symlink creation.
- **Stack not detected**: the CLI falls back to "Generic" — specialist agent still gets created, just without stack-specific verify commands.
