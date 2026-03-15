---
name: audit-claude-md
description: "Audit any project's CLAUDE.md (or AGENTS.md) against best practices and score its effectiveness. Use when reviewing a client's AI development setup, onboarding a new codebase, or improving your own CLAUDE.md. Triggers on requests like \"audit my CLAUDE.md\", \"score my AI setup\", \"review my project context file\", or \"how good is my CLAUDE.md\"."
---

# CLAUDE.md Audit

Analyze and score a project's CLAUDE.md against research-informed best practices (ETH Zurich ICML 2026 + production AI-assisted development workflows). Emphasizes what agents CANNOT discover on their own: behavioral constraints, non-standard tools, and project-specific footguns.

Arguments: $ARGUMENTS

## Instructions

Audit the CLAUDE.md (or AGENTS.md / .cursorrules) in the current project and score it against the rubric in [references/scoring-rubric.md](references/scoring-rubric.md).

**If a path is provided in $ARGUMENTS**, audit that file instead.

## Phase 1: Discover the AI Context Files

Search for all AI context files in the project:

1. Check project root for: `CLAUDE.md`, `AGENTS.md`, `.cursorrules`
2. Check for nested CLAUDE.md files in subdirectories (e.g., `src/CLAUDE.md`, `docs/CLAUDE.md`)
3. Check for linked guide directories: `docs/claude/`, `docs/ai/`, `.claude/`
4. Check for `.claude/learnings/` directory
5. Check for `.claude/skills/`, `.claude/commands/`, `.claude/hooks/`

Report what was found before scoring.

## Phase 2: Read and Analyze

Read the main CLAUDE.md file. If it links to other files (e.g., `docs/claude/tdd.md`), read those too — they contribute to the score.

Count the total line count of the main file. Note whether detail lives in linked files or is crammed into one file.

## Phase 3: Score Against Rubric

Read [references/scoring-rubric.md](references/scoring-rubric.md) and score each category.

**Scoring rules:**
- **Full points**: Item is present, specific, and actionable
- **Partial points** (half, rounded down): Item exists but is vague, incomplete, or generic
- **Zero points**: Item is missing entirely

Be generous with partial credit — a vague section is better than no section.

## Phase 4: Generate Report

Output the report in this format:

```
# CLAUDE.md Audit Report

**Project:** [project name from CLAUDE.md or directory name]
**Files found:** [list of AI context files discovered]
**Main file:** [path] ([line count] lines)
**Linked files:** [count and paths]

## Overall Score: [X]/103 — [Tier Name]

[1-2 sentence summary of the file's strengths and biggest gap]

---

## Foundations — [X]/12

[Table per rubric format]

**Top recommendation:** [...]

## Standards — [X]/14

[Table per rubric format]

**Top recommendation:** [...]

## Behavior Configuration — [X]/29

[Table per rubric format]

**Top recommendation:** [...]

## Architecture — [X]/22

[Table per rubric format]

**Top recommendation:** [...]

## Memory & Learning — [X]/10

[Table per rubric format]

**Top recommendation:** [...]

## Advanced — [X]/16

[Table per rubric format]

**Top recommendation:** [...]

---

## Priority Actions (Top 3)

1. **[Highest impact action]** — [why and what to do] (+[X] points)
2. **[Second action]** — [why and what to do] (+[X] points)
3. **[Third action]** — [why and what to do] (+[X] points)

**Potential score after fixes:** [X]/103 — [New Tier Name]
```

## Phase 5: Offer Next Steps

After presenting the report, offer:

1. **Fix it now** — Implement the top 3 recommendations directly
2. **Generate a template** — Create a CLAUDE.md template pre-filled with the project's detected stack and conventions
3. **Compare to reference** — Show what an elite CLAUDE.md looks like (read [references/elite-example.md](references/elite-example.md))
4. **Save report** — Write the audit report to a file
