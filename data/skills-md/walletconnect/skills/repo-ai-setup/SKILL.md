---
name: repo-ai-setup
description: |
  Sets up AI agent documentation and automated PR reviews. Creates AGENTS.md, CLAUDE.md symlink, and Claude auto-review GitHub Action.

  Triggers: "repo setup", "setup agents", "setup AI agents", "add AGENTS.md", "setup auto review", "setup repo"
---

# Repo AI Setup

Set up AI agent documentation and automated PR review infrastructure for a WalletConnect repository.

**Arguments:** $ARGUMENTS

## Argument Handling

- `$ARGUMENTS` contains "just docs" or "skip workflow" → run Phases 0–2 only
- `$ARGUMENTS` contains "just workflow" or "just auto-review" → run Phases 0 + 3 only
- No arguments → all phases

---

## Phase 0 — State Detection

Detect the current repo state before doing anything:

1. Check if `AGENTS.md` exists in repo root
2. Check if `CLAUDE.md` exists — if so, determine: regular file or symlink? If symlink, where does it point?
3. Check if `.github/workflows/claude-review.yml` or `.github/workflows/claude-auto-review.yml` exists
4. Detect default branch:
   ```bash
   gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null \
     || git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@.*/@@' \
     || echo "main"
   ```
5. Verify this is a git repo (`git rev-parse --git-dir`)

**Report state summary to user.** Example:

```
Repository state:
  AGENTS.md:      missing
  CLAUDE.md:      exists (regular file)
  Auto-review:    missing
  Default branch: main
  Git repo:       yes
```

Skip any phases whose artifacts already exist.

---

## Phase 1 — Create AGENTS.md

Three branches based on detected state:

### Case A: AGENTS.md already exists
Skip. Report: "AGENTS.md already exists — skipping."

### Case B: CLAUDE.md exists as regular file (not symlink)
Convert it to an agent-agnostic AGENTS.md:

1. `cp CLAUDE.md AGENTS.md`
2. Edit AGENTS.md:
   - Replace `# CLAUDE.md` header with `# AGENTS.md` (if present)
   - Replace "This file provides guidance to Claude Code" or similar → "This file provides guidance to AI coding agents"
   - Replace "Claude Code" → "AI coding agent" and "Claude" → "AI agent" in descriptive text
   - **Preserve** all technical instructions, commands, code blocks, and configuration details unchanged
   - **Preserve** any references to `.claude/` paths, `CLAUDE.md` symlinks, or Claude-specific tooling config (these are real paths/tools)
3. Delete the original `CLAUDE.md` (it will be recreated as a symlink in Phase 2)

### Case C: No agent docs exist (neither AGENTS.md nor CLAUDE.md)
Generate agent docs using Claude Code's `/init` command via a subagent:

1. Launch a **Task agent** with `subagent_type: general-purpose`:
   - Instruct it to run Claude Code's `/init` command as a CLI subprocess:
     ```bash
     claude -p "/init" --allowedTools "Bash,Read,Write,Edit,Glob,Grep"
     ```
   - This generates `CLAUDE.md` in the repo root with real codebase analysis
   - If `claude` CLI is not available, the subagent should fall back to **manual codebase analysis**: scan the repo for build files, test configs, CI workflows, source structure, READMEs, etc., and write a comprehensive `AGENTS.md` directly (use the format guide in [REFERENCE.md](./REFERENCE.md))

2. After the subagent completes:
   - If `CLAUDE.md` was generated, rename it: `mv CLAUDE.md AGENTS.md`
   - Apply the same agent-agnostic edits as Case B step 2
   - If the subagent wrote `AGENTS.md` directly (fallback path), verify it exists

---

## Phase 2 — Create CLAUDE.md Symlink

Ensure `CLAUDE.md` is a symlink pointing to `AGENTS.md`:

1. If `CLAUDE.md` is already a symlink to `AGENTS.md` → skip
2. If `CLAUDE.md` is a symlink to something **other** than `AGENTS.md` → **warn the user** and ask how to proceed (do not overwrite)
3. If `CLAUDE.md` exists as a regular file at this point → warn (shouldn't happen after Phase 1), ask user
4. Otherwise, create the symlink:
   ```bash
   ln -s AGENTS.md CLAUDE.md
   ```
5. Verify:
   ```bash
   readlink CLAUDE.md  # should output "AGENTS.md"
   ```

---

## Phase 3 — Setup Claude Auto-Review Workflow

Set up the GitHub Action for automated Claude PR reviews.

1. If `.github/workflows/claude-review.yml` already exists → skip
2. Also check for `.github/workflows/claude-auto-review.yml` → if exists, skip (alternate naming)
3. Create `.github/workflows/` directory if it doesn't exist:
   ```bash
   mkdir -p .github/workflows
   ```
4. Read the workflow template from [REFERENCE.md](./REFERENCE.md) (Section: Claude Auto-Review Workflow Template)
5. Replace `{DEFAULT_BRANCH}` with the actual default branch detected in Phase 0
6. Write the file to `.github/workflows/claude-review.yml`
7. **Remind the user:** they need to add `ANTHROPIC_API_KEY` as a repository secret:
   - Go to Settings → Secrets and variables → Actions → New repository secret
   - Name: `ANTHROPIC_API_KEY`
   - Value: their Anthropic API key
8. **Ask the user** if they want to add a `project_context` input to the workflow for project-specific review guidance. If yes, ask them for the context string and add it to the workflow per the REFERENCE.md example.

### Not a git repo?
If Phase 0 detected this is not a git repo, skip Phase 3 entirely. Still create AGENTS.md + symlink.

---

## Phase 4 — Summary

Report what was created, modified, and skipped:

```
Setup complete:
  ✓ Created AGENTS.md (from /init analysis)
  ✓ Created CLAUDE.md → AGENTS.md symlink
  ✓ Created .github/workflows/claude-review.yml
  ⚠ Remember to add ANTHROPIC_API_KEY repo secret

Suggested commit message:
  feat: add AI agent documentation and auto-review workflow
```

**Do NOT auto-commit.** Let the user review and commit.

---

## Edge Cases

| Scenario | Handling |
|----------|----------|
| CLAUDE.md symlinks to non-AGENTS.md target | Warn user, ask before changing |
| Not a git repo | Skip Phase 3, still create docs + symlink |
| `gh` CLI not available | Fall back to git commands for branch detection |
| `claude` CLI not available in subagent | Subagent does manual codebase analysis |
| AGENTS.md + CLAUDE.md both exist as regular files | Warn about duplication, ask user which to keep |
| `.github/workflows/` has a differently-named Claude review workflow | Check for both `claude-review.yml` and `claude-auto-review.yml` |
