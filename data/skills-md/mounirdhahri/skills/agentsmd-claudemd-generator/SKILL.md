---
name: agentsmd-claudemd-generator
description: Generate AGENTS.md and CLAUDE.md files for a repository. AGENTS.md provides cross-tool agent instructions (supported by Claude Code, Cursor, Windsurf, Zed, Codex, and others). CLAUDE.md adds Claude-specific configuration and references AGENTS.md via @import. Use when a repo needs agent onboarding or when starting a new project.
allowed-tools: Read Write Edit Bash(ls:*) Bash(git:*) Bash(tree:*)
---

# AGENTS.md & CLAUDE.md Generator

## What You'll Do

Generate **two files** for the repository:

1. **`AGENTS.md`** — Cross-tool agent instructions following the open standard (https://agents.md). Supported by Claude Code, Cursor, Windsurf, Zed, GitHub Copilot, OpenAI Codex, Aider, and many others. This is the primary file containing project context, conventions, and workflows.
2. **`CLAUDE.md`** — Claude Code-specific configuration that references AGENTS.md via `@import` and adds any Claude-specific instructions. This avoids duplicating content across two files.

### Why two files?

- **AGENTS.md** is the cross-tool standard — any AI coding tool reads it. Put all project knowledge here.
- **CLAUDE.md** is Claude Code-specific. It should be thin: point to AGENTS.md and only add what's Claude-unique.
- This means you maintain docs in one place (AGENTS.md) and every tool benefits.

---

## Reference Documentation

Always prefer pointing users to these docs rather than reciting their contents:

- **AGENTS.md spec**: https://agents.md
- **CLAUDE.md memory docs**: https://code.claude.com/docs/en/memory
- **CLAUDE.md guide (Builder.io)**: https://www.builder.io/blog/claude-md-guide

---

## Phase 1 · Understand the Repository

1. **Check for existing files**
   - Look for existing `AGENTS.md`, `CLAUDE.md`, `CLAUDE.local.md`, `.claude/CLAUDE.md`, and `.claude/rules/` in the repo.
   - If files exist, plan to update/extend rather than overwrite.

2. **Read core docs**
   - Skim `README.md`, `CONTRIBUTING.md`, and any `docs/` directory.
   - Note project philosophy, setup steps, and workflows.

3. **Survey project layout**
   - Identify primary directories, languages, frameworks, and ownership.
   - Run `tree --gitignore -a -L 3` to get a directory snapshot. Trim to top 2-3 levels.

4. **Identify tooling and commands**
   - Find the project's build, test, lint, format, and deploy commands — whatever tool the project actually uses.
   - Note environment requirements: runtimes, package managers, env vars, `.env.example` files.

5. **Identify existing documentation**
   - Check if project docs already cover code style, conventions, patterns, or best practices (e.g., `docs/best_practices.md`, `CONTRIBUTING.md`, style guides).
   - These docs are the **source of truth** — AGENTS.md should reference them via `@import`, not duplicate their content.
   - For core docs that apply to nearly every code change (style guides, conventions, patterns): use `@import` so they're always loaded into context.
   - For docs only relevant occasionally (deployment, setup): use plain markdown links.
   - **Watch for size**: before recommending `@import`, check the file size. Files over ~300 lines (~1,500 tokens) are worth flagging to the developer — warn them that large `@import`s eat into the context window on every conversation. Suggest they either import only the most critical sections, or keep it as a plain link for on-demand reading.

6. **Resolve ambiguities**
   - Ask the developer to confirm the tech stack — don't assume completeness from code alone (CI tools, infrastructure, and platform-specific details are easy to miss).
   - Ask which commands are the **main ones** developers use daily — don't just list everything from package.json/Makefile.
   - Ask the developer when conventions or ownership are unclear. Do not guess.

> **Outcome:** Structured notes covering layout, tooling, commands, testing, conventions, and open questions.

---

## Phase 2 · Generate AGENTS.md

Place at the repository root. Follow this section order for consistency:

```markdown
# Agent Guidelines

Brief one-line project description.

Detailed docs live in @docs/... — reference them with @imports rather than duplicating here.

## Tech Stack

- **React** - Component framework
- **TypeScript** - Language (strict mode)
- **Relay** - GraphQL data fetching
<!-- List each technology with its role in the project -->

## Common Commands

- `<lint command>` — run on changed files
- `<test command>` — run on changed files
- `<type-check command>` — verify types
- `<build command>` — production build

## Pre-Commit Verification

Before every commit, verify code quality on pending files:

\`\`\`sh
<type-check command>
<test command on changed files>
<lint command on changed files>
\`\`\`

Never commit code that fails these checks.

## Code Style & Common Patterns

<!-- If the project already has docs covering style/conventions/patterns (e.g., best_practices.md, CONTRIBUTING.md),
     use @import so they're always in context. Only inline rules that have NO existing doc. -->

@docs/best_practices.md

<!-- Use @import for docs that agents should ALWAYS have in context (conventions, patterns, style rules).
     Use a plain markdown link [Topic](path) for docs that are only needed occasionally.
     Example of inlining ONLY when no existing doc covers it:
- Specific, actionable rules (not vague "follow best practices")
- **UI**: Use <design system> for UI components
- **Data**: Use <data layer> for data fetching
-->

## File Organization

<!-- Annotated structure showing what goes where -->
\`\`\`
src/
├── Apps/           # Sub-applications
├── Components/     # Shared across apps
└── System/         # Framework code
\`\`\`

## Workflow

- Branching model
- PR / review expectations
- Commit message format

## Gotchas

- Non-obvious project quirks
- Common pitfalls

## Further Documentation

- [Topic](docs/topic.md)
- And more in @docs
```

### Writing guidelines

- **Never duplicate existing docs** — if the project already documents code style, patterns, or conventions (in files like `best_practices.md`, `CONTRIBUTING.md`, style guides), use `@import` to pull them into context instead of restating the content. Use `@import` for docs agents should **always** have (conventions, patterns, style rules). Use plain markdown links for docs only needed occasionally. AGENTS.md should complement existing docs, not copy them.
- **Warn about large imports** — before adding an `@import`, check the file size. If a doc is over ~300 lines, warn the developer that it will consume significant context window space on every conversation and ask whether they want to import it fully, import only key sections, or keep it as a plain link.
- **Ask the developer to confirm** the tech stack and which commands are the main ones. Don't assume completeness from code inspection alone — CI tools, infrastructure, and daily-use commands are easy to miss or over-include.
- Keep it **actionable** — agents should follow instructions verbatim, not interpret vague guidance.
- **"Use X for Y"** — map tools to purposes so agents pick the right library (only when not already covered by existing docs).
- **Exact commands** — include the actual shell commands, not descriptions of what to do. Only list the commands developers use most — don't dump the full scripts section from package.json.
- **Pre-commit checks** — always include a verification block with commands to run before committing.
- **Reference deeper docs** — use `@imports` to link to detailed docs instead of duplicating content.
- **Annotate the file tree** — don't dump raw `tree` output; curate it with inline descriptions.
- Stay **under 300 lines**. Only include sections relevant to the project — skip empty ones.

---

## Phase 3 · Generate CLAUDE.md

Place at the repository root alongside AGENTS.md. This file should be **thin** — its job is to point to AGENTS.md. For most projects, this is all you need:

```markdown
# CLAUDE.md

See @AGENTS.md
```

That's often the entire file, and that's fine. Only add a Claude-specific section if the project actually uses Claude-only features:

- **`.claude/rules/`** — references to modular rule files in the project
- **`.claude/commands/`** — custom slash commands available in the project
- **`.claude/agents/`** — custom subagents available in the project
- **Behavioral preferences tied to Claude capabilities** — e.g., "Use plan mode for non-trivial tasks", "Use subagents for parallel research"
- **Tool permission hints** — e.g., "You have permission to run `npm test` without asking"

If none of these apply, don't add them. An empty Claude-specific section is worse than no section.

### Additional Claude memory features

Point the developer to the docs (https://code.claude.com/docs/en/memory) for advanced features like `CLAUDE.local.md`, `.claude/rules/`, `@imports`, `/init`, and auto memory.

---

## Phase 4 · Validate & Wrap Up

1. **Both files exist** at the repo root.
2. **CLAUDE.md references AGENTS.md** via `See @AGENTS.md`.
3. **No duplication** — project knowledge lives in AGENTS.md only.
4. **Commands are accurate** — all listed commands actually work.
5. **Concise** — both files are scannable and under 300 lines.
6. **Handoff summary** — tell the developer what was added, flag open questions, and point to the official docs for advanced features.
