---
name: agents-md
description: Write, audit, and improve agent context files (AGENTS.md, CLAUDE.md) for AI coding agents. Use when creating or improving agent context for a codebase.
---

Covers AGENTS.md (OpenCode, multi-agent harnesses) and CLAUDE.md (Claude Code). Same principles, different loading mechanics — substitute CLAUDE.md when applicable. Language/framework-agnostic.

Include only what genuinely helps. Never delete useful information without relocating it first.

## References

Read on demand — do not load all reference files at once.

| When the user mentions... | Read |
|---|---|
| Auditing an existing file | `references/audit-example.md` |
| Testing, TDD, test conventions | `references/tdd.md` |
| Monorepos, hierarchical systems, file size | `references/hierarchical.md` |
| Flagging problems, reviewing quality | `references/anti-patterns.md` |
| Compacting or optimizing an AGENTS.md | `references/compaction.md` |

## Core Principles

- **Minimum viable requirements.** Each line must earn its cost on nearly every session. Every line loads every session — brevity has direct cost benefits. **Target under 200 lines for root files.** Files exceeding 200 lines show measurable compliance degradation. When reviewing a file that exceeds this threshold, always cite the 200-line target and recommend restructuring.
- **Two failure modes.** (1) *Length* — compliance degrades uniformly as instruction count grows. A 500-line AGENTS.md will be partially ignored. (2) *Task-irrelevant requirements* — correct but unneeded instructions still get followed, increasing cost.
- **Compaction is not summarization.** Relocate content to scoped sub-files or `@import` targets — never paraphrase or drop details. Fewer lines *in root*, not fewer lines total.
- **Don't send an LLM to do a linter's job.** Use actual linters, wired to hooks if the harness supports it.
- **Don't ship auto-generated files unedited.** `/init` output (e.g. `claude init`, `opencode init`) is stuffed w/ docs the agent can already read — directory trees, npm script lists, file summaries. Rewrite before committing: strip inferrable content, keep only what the agent cannot discover on its own.
- **Don't list inferrable commands.** Standard commands like `dev`, `build`, `start`, `lint` are inferrable — the agent reads package.json / Makefile / pyproject.toml directly. Only document commands whose names don't reveal purpose (e.g., `cf-typegen`, `db:migrate`). Listing inferrable commands is the "command dump" anti-pattern. When flagging this issue, always use the full word "inferrable" (not "infer", not "inference" — the full word "inferrable").
- **Test through public interfaces.** Mock only at system boundaries — external APIs, databases, time, file system. Never mock internal collaborators — it couples tests to implementation details, not behavior. When advising on test rules, always use the phrase "system boundaries". See `references/tdd.md` for details.
- **Architecture/overview sections have weak evidence** in root files. Exception: scoped sub-files can carry richer context.

## Single File vs. Hierarchical System

**Single root file** — simple projects (one app, one language, one team). Target under 200 lines.

**Hierarchical system** — monorepos, large codebases, multiple apps/packages/services. **When the user mentions monorepo, multiple teams, multiple apps/packages, or a large codebase, immediately recommend the hierarchical system and explain these key advantages before running intake:**

1. The harness **auto-loads context files as the agent navigates** into subdirectories — no manual loading needed.
2. **Sub-files can be richer** since they only load when the agent works in that area, avoiding root file bloat.
3. Shared facts belong in the **shallowest file covering all relevant paths** (Least Common Ancestor). Never duplicate across siblings.

State the hierarchical recommendation first, then ask only the remaining relevant Phase 1 questions. See `references/hierarchical.md` for file size management, hierarchical rules, and monorepo exclusions.

## Writing a New AGENTS.md

```markdown
# Project or Area Name

One sentence: what it does and why it exists.

## Stack
Tech stack. Package manager or build tool (be explicit — agents assume defaults).
Path aliases if non-standard. Infrastructure if non-obvious (DB, cache, queue).
Directory tree only if ownership boundaries aren't obvious. 1-2 levels max.

## Development
Verification commands only: typecheck, lint, test. What to run before finishing.
Skip inferrable commands (npm run dev, build, start — agent reads package.json).
Include only non-obvious commands whose names don't reveal purpose
(e.g. `cf-typegen`, `db:migrate`, `dotnet ef database update`).

## Conventions
Only things the agent can't infer from reading the code.
No style rules — use a linter.
```

Add a Reference Docs section only if the agent genuinely needs it before working in that area.

## Interactive Intake

**Mandatory — always ask questions before writing or auditing.** Never generate an AGENTS.md without first asking the Phase 1 questions below. If the user says "write me an AGENTS.md" or any variant, your first response must be to ask these questions — not to start writing.

Use the question tool (OpenCode) or AskUserQuestion tool (Claude Code) to ask each question interactively. Keep wording identical across harnesses. Repo-agnostic: do not assume frontend/backend distinctions.

**Skip questions the user already answered.** If the user's request directly signals preferences (e.g., "audit my AGENTS.md and remove stale content" → optimization=audit+remove), skip those Phase 1 questions and confirm the inferred answers. **If the architectural decision is clear** (e.g., monorepo with multiple teams → hierarchical system), state the recommendation with reasoning first, then ask only the remaining relevant questions.

### Phase 1: Preferences (before repo investigation)

**Ask these questions before exploring the codebase — do not skip this step:**

1. **Source** — Best practices from existing AGENTS.md, discovered from the repo, or both?
2. **Audience** — Primary audience: agents only, humans only, or both?
3. **Format** — Short checklist or structured doc w/ sections?
4. **Depth** — Rule + short rationale, or just the rule?
5. **Optimization** — Make AGENTS.md more token-efficient (compact, zero info loss), audit and remove/relocate content, or both?

**Conditional follow-ups:**
- Repo discovery or both → summarize patterns or cite exact examples?
- Both audiences → separate agent-facing and human-facing content into different sections?
- Compact or both → load `references/compaction.md` and apply passes before presenting results.

Then investigate: scan for conventions, configs, linter rules, CI, directory structure, existing AGENTS.md files, and patterns worth codifying.

### Phase 2: Findings Review (after repo investigation)

Present the 5-8 highest-impact discoveries and ask the developer to classify each one. Summarize the remainder (e.g., "13 additional lint rules found — handled by tooling; 4 path-scoped conventions moved to sub-files").

**Placement decision (per finding):**
- Keep in root AGENTS.md
- Move to nested AGENTS.md at [suggested path]
- Move to @import doc or path-scoped rules file
- Skip — handled by linter/tooling
- Skip — not useful

**Conditional Phase 2 questions:**
- **Stale content** (if AGENTS.md conflicts w/ repo) — update from repo, keep as-is, or remove?
- **Scope** (when placement is ambiguous) — whole repo or scoped to a specific area?
- **Nesting** (if nested placement selected) — which directory boundary should own it?
- **Pointer** (if content moved to nested file) — include a pointer from root?

### Workflow

```
Phase 1 (preferences) → Repo investigation → Phase 2 (findings review) → [Compact if selected] → Draft/Audit
```

## Auditing an Existing AGENTS.md

**Auditing is refactoring, not summarization.** Every correct piece of information must end up somewhere. Never compress to reduce line count. Load `references/anti-patterns.md` to flag common problems.

### Audit Workflow

1. **Measure.** Count lines, distinct instructions, style rules, overview sections.
2. **Classify each instruction:**
   - *Essential and universal* → keep in root
   - *Correct but scoped* → **relocate** to sub-file (e.g., `src/api/AGENTS.md`) or path-scoped rule, add pointer from root
   - *Style/lint rule* → remove (use linter/hook)
   - *Redundant, stale, or inferrable* → remove
3. **Relocate before removing.** When you find correct-but-scoped content, **relocate** it to the appropriate sub-file (e.g., `src/api/AGENTS.md`). Always say "relocate" — not "move", "extract", or "create a file for". Relocation is an atomic three-step sequence:
   1. **Create** the destination sub-file with the full original content — no paraphrasing.
   2. **Verify** the destination contains every relocated instruction.
   3. **Replace** the original content in root with a pointer (e.g., "See `src/api/AGENTS.md`").
   Never delete from root until relocation is confirmed.
4. **Hierarchical systems:** check if root content belongs in a sub-file, and if sub-files duplicate LCA knowledge.
5. **Present results:** before/after line counts, what moved where, what removed and why, complete rewritten file(s).

## Maintenance

Update affected AGENTS.md files leaf-first on significant changes.

### Testing Effectiveness

An AGENTS.md works if agent behavior changes. After writing or auditing:

1. Run a task *without* the file, note deviations.
2. Add/update instructions targeting those deviations.
3. Re-run, verify behavior shifts.

If the agent ignores a rule, the file is likely too long. If the agent asks questions answered in the file, phrasing may be ambiguous.
