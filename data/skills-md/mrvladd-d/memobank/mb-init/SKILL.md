---
name: mb-init
description: >
  Create the Memory Bank skeleton and project command proxies in the current repository.
---

# mb-init — Initialize Memory Bank skeleton

- **What it does:** creates the base folders, core docs, and project-native command proxies.
- **Use it when:** you want the skeleton only, without immediately choosing PRD or brownfield mapping.
- **Input:** repository root.
- **Output:** `.memory-bank/`, `.tasks/`, `.protocols/`, `AGENTS.md`, and generated command stubs.

## Goal
Create a consistent baseline so agents can work with **repo-local context** instead of ad-hoc prompts.

## Steps

### 1) Create directories
Create (if missing):
- `.memory-bank/` with subfolders (see `./references/shared-structure-template.md`)
- `.tasks/`
- `.protocols/`

### 2) Create core Memory Bank files
From templates, create:
- `AGENTS.md`
- `CLAUDE.md` → symlink/copy to `AGENTS.md`
- `.memory-bank/index.md`
- `.memory-bank/mbb/index.md`
- `.memory-bank/product.md`
- `.memory-bank/requirements.md`
- `.memory-bank/tasks/backlog.md`
- `.memory-bank/testing/index.md`
- `.memory-bank/skills/index.md`

### 3) Create command stubs
So links from `AGENTS.md` are not broken, create minimal docs under `.memory-bank/commands/`.
Use `./references/shared-commands-*.md`:
- `mb.md`
- `prd.md`
- `prd-to-tasks.md`
- `execute.md`
- `verify.md`
- `autopilot.md`
- `autonomous.md`
- `map-codebase.md`
- `discuss.md`
- `add-tests.md`
- `review.md`
- `find-skill.md`

### 4) Create native skills (proxy commands)
Create thin proxy skills for each command so they work natively across runtimes:
- `.claude/skills/<name>/SKILL.md` → Claude Code + OpenCode
- `.agents/skills/<name>/SKILL.md` → Codex CLI + OpenCode

Each proxy contains: `Read and follow the instructions in .memory-bank/commands/<name>.md`.
This registers commands natively: `/mb` in Claude Code, `$mb` in Codex, `/mb` in OpenCode.

The `init-mb.js` script creates both sets automatically.

### 5) Enforce MBB rules immediately
- Every `.memory-bank/**/*.md` must have frontmatter (`description`, `status`).

## Optional fast path
If Node.js is available, you may run the helper script (safe: doesn’t overwrite existing files):

```bash
# Option A: copy ./scripts/shared-init-mb.js into your repo then run:
node scripts/init-mb.js
```

If you don’t want a script, just create the files manually using the templates.

## Definition of done
- `AGENTS.md` exists and points to `.memory-bank/index.md`.
- `CLAUDE.md` exists and mirrors `AGENTS.md`.
- `.memory-bank/` has the seeded docs.
- `.memory-bank/commands/` has stub command docs.
- `.tasks/` and `.protocols/` exist.
