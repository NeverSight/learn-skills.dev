---
name: initializing-projects
description: Generates a minimal, self-maintaining CLAUDE.md for projects through auto-detection and developer interview. Covers project identity, do/don't rules, hooks, and self-maintenance. Use when starting a new project or adding Claude Code support to an existing one
---

# Initializing Projects

Generate a focused CLAUDE.md that gives Claude the context it actually needs — and nothing more.
Agents are smart enough to figure out most things from the code.
The file should capture what they cannot infer: project identity, business context, and hard-won lessons.

## Reference Files

| File | Read When |
|------|-----------|
| `references/claude-md-patterns.md` | Constructing the CLAUDE.md or reviewing examples of effective minimal configs |

## Philosophy

Keep the CLAUDE.md minimal.
Agents read the code, `package.json`, config files, and directory structure on their own.
Only add what they would get wrong or waste time figuring out.

**Include:**
- What the project is, who it's for, and why it exists (mission/vision)
- Do/don't rules for things that have tripped the agent up or need clarification
- Non-obvious conventions that differ from common patterns
- Key files only if they are novel or not where you'd expect them

**Exclude:**
- Tech stack descriptions the agent can read from config files
- Detailed repo structure (it changes, and the agent can explore)
- Generic programming advice
- Standard framework patterns Claude already understands

The file grows over time as the agent (and you) discover gotchas.
Start small — a 20-line CLAUDE.md is better than a 200-line one full of noise.

## Workflow

### Phase 1: Auto-Detection

Scan the project to understand the landscape.
This informs the interview — skip questions you can answer from config files.

**Detect:**
- Package manager and ecosystem (lock files, `packageManager` field, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, workspace configs like `pnpm-workspace.yaml`, `nx.json`, etc.)
- Framework (dependencies in `package.json`, `pyproject.toml`, config files like `next.config.*`)
- Test runner (jest/vitest/pytest config, `scripts.test`, `tests/` directory)
- Formatter (prettier, biome format, black, ruff format configs)
- Linter (eslint, biome lint, ruff check, pylint, clippy configs) — note separately from formatter, as linters inform hook generation in Phase 4
- `ARCHITECTURE.md` — if present, note it; architecture enforcement is already partially set up
- `docs/` directory — if present, note it and scan for front-matter summaries to include in the detection summary
- Existing CLAUDE.md or AGENTS.md — if found, warn and ask whether to merge or replace. Merge = read existing content, preserve user-written sections, add new sections from the template that don't exist yet. Present the merged result for user approval before writing
- README.md — extract project description

Present findings in a concise summary.
Ask the user to confirm or correct before proceeding.

### Phase 2: Interview

Fill gaps that auto-detection cannot cover.
Go as deep as the project warrants — simple projects need 2-3 questions, complex ones may need a longer conversation.

**Core questions:**
- What does this project do? Who is it for? What's the mission? (skip if README is clear)
- Are there conventions or patterns that differ from what you'd expect? (naming, architecture, data flow)
- What has tripped you (or previous Claude sessions) up? What keeps going wrong?
- Are there rules with exceptions? Things that are "always X... except when Y"? (These cause the most agent errors — e.g., "always use UTC... except the reporting module uses user timezone")
- Any business decisions or constraints that affect how code should be written?
- Are there key files or areas of the codebase that are non-obvious or tricky?

Do not ask questions the code answers.
Do not cap the interview artificially — if the user keeps sharing useful context, keep going.
When the user signals they're done, move on.

### Phase 3: Generate CLAUDE.md

Generate a minimal `CLAUDE.md` at the project root.
Only include sections with real content — omit empty sections entirely.

```markdown
## What This Is
[Project description — what it does, who it's for, why it exists]
[Mission/vision if the user shared one]

## Do / Don't
- Do: [specific convention or pattern the agent should follow]
- Don't: [specific thing that has caused problems or is explicitly wrong]
- Do: [rule with exception] — except [when/where the exception applies]
[Add more as discovered during development]

## Known Issues
<!-- Populated by Claude — remove entries when fixed -->

## Decision Log
<!-- Key business/project decisions only, not obvious code choices -->
```

**Conditional sections** (only add if the user raised them):
- **Key Files** — only for files that are non-obvious or in unexpected locations
- **Gotchas** — specific traps or footguns in the codebase
- **Commands** — only if they differ from standard (`pnpm test`, `pnpm dev`, etc.) or have unusual flags

Do not add:
- A "Project Structure" section listing directories the agent can discover itself
- A "Development" section restating `package.json` scripts verbatim
- A "Coding Conventions" section with generic rules the agent already follows
- Tech stack descriptions ("This project uses Next.js 14 with TypeScript") — the agent reads `package.json`

The self-maintenance rules from the user's global `~/.claude/CLAUDE.md` handle plan updates, known issues, and decision logging.
Do not duplicate those rules in the project CLAUDE.md unless the user's global config is missing them.

### Phase 4: Generate Hooks

Create `.claude/settings.json` with PostToolUse hooks matching `Write|Edit`.

**Formatter hooks** (auto-fix on every edit):

**If Prettier:** `npx prettier --write $CLAUDE_FILE_PATH 2>/dev/null || true`
**If Biome:** `npx @biomejs/biome format --write $CLAUDE_FILE_PATH 2>/dev/null || true`
**If Ruff:** `ruff format $CLAUDE_FILE_PATH 2>/dev/null || true`
**If Black:** `black $CLAUDE_FILE_PATH 2>/dev/null || true`

If no formatter is detected, suggest one appropriate for the stack but do not force it. Defaults: Prettier for JS/TS, Ruff for Python, gofmt for Go, rustfmt for Rust.

**Linter hooks** (catch issues mechanically, not via instructions):

If a linter was detected in Phase 1 but no lint hook exists, suggest a PostToolUse lint hook:
**If ESLint:** `npx eslint --fix $CLAUDE_FILE_PATH 2>/dev/null || true`
**If Biome:** `npx @biomejs/biome check --fix $CLAUDE_FILE_PATH 2>/dev/null || true`
**If Ruff:** `ruff check --fix $CLAUDE_FILE_PATH 2>/dev/null || true`

If no linter is detected and the project has 10+ source files, suggest adding one appropriate for the stack. Don't force it — present it as a recommendation with the benefit (mechanical enforcement catches issues automatically, no agent discipline required).

For complex projects (multiple layers, clear architectural boundaries, or the user described layered architecture during the interview), mention `/enforcing-architecture` as a next step for setting up dependency-direction rules and structural checks.

`.claude/settings.json` should be committed to git so project hooks are shared with the team.
If `.claude/settings.local.json` exists (machine-specific overrides), ensure it's in `.gitignore`.

### Phase 5: Verification

Read back every generated file and confirm:
- CLAUDE.md is concise and contains only non-obvious information
- Hooks point to the correct formatter and linter
- No generic boilerplate was included

Present a summary listing all files created and their purpose.
Flag anything that looks wrong or needs manual adjustment.

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Listing tech stack the agent can detect | Only note what's surprising or non-standard |
| Detailed repo structure that will go stale | Let the agent explore; call out only non-obvious key files |
| Generic advice ("write clean code") | Specific do/don't rules from real experience |
| Overwriting existing CLAUDE.md without asking | Warn and offer to merge |
| Padding with empty sections | Omit sections that have no real content |
| Capping the interview prematurely | Let the user share as much context as they want |
| Duplicating global self-maintenance rules | Check if they exist in `~/.claude/CLAUDE.md` first |
