---
name: codex
description: |
  Delegate coding execution to Codex CLI for implementation tasks with clear success criteria.

  **USE THIS SKILL WHEN:**
  - Refactoring, renaming, migrating, upgrading, or converting code
  - Generating tests, adding coverage, writing unit/integration tests
  - Batch edits across repo: "update all", "apply everywhere", "sweep"
  - Implementing features: "wire up", "scaffold", "add support for"
  - Fixing issues: "fix failing tests", "fix type/lint errors", "fix the build", "green CI"
  - API changes: "update usages", "adopt new API", "codemod"
  - Standardization: "make consistent", "deduplicate", "standardize"
  - Code review or investigation WITH concrete artifacts (diff, logs, repro, failing test)

  **USE CLAUDE (NOT CODEX) WHEN:**
  - Strategic decisions: "should we", "compare approaches", "recommend strategy"
  - System design, architecture, requirements design
  - Teaching, explaining concepts, brainstorming, RFC writing
  - Unknown problems without repro/logs/stack traces
  - Ambiguous tasks needing clarification first

  **TWO-STAGE MODEL:** For mixed requests ("assess then implement"), Claude frames first, then Codex executes if the plan is concrete.

  CodeX is cost-effective and strong at execution. Claude handles ambiguity, strategy, and architecture better.
---

# CodeX — Your Codex Coding Partner

Delegate coding execution to Codex CLI. CodeX turns clear plans into working code.

## Critical rules

- ONLY interact with CodeX through the bundled shell script. NEVER call `codex` CLI directly.
- Run the script ONCE per task. If it succeeds (exit code 0), read the output file and proceed. Do NOT re-run or retry.
- Do NOT read or inspect the script source code. Treat it as a black box.
- ALWAYS quote file paths containing brackets, spaces, or special characters when passing to the script (e.g. `--file "src/app/[locale]/page.tsx"`). Unquoted `[...]` triggers zsh glob expansion.
- **Keep the task prompt focused.** Aim for under ~500 words. Describe WHAT to do and key constraints, not step-by-step HOW. CodeX is an autonomous agent with full workspace access — it reads files, explores code, and figures out implementation details on its own.
- **Never paste file contents into the prompt.** Use `--file` to point CodeX to key files — it reads them directly. Duplicating file contents in the prompt wastes tokens and adds no value.
- **Don't reference or describe the SKILL.md itself in the prompt.** CodeX doesn't need to know about this skill's configuration.

## Decision policy

### Use Codex when:

- The user wants code executed with **concrete success criteria**
- The task involves **repetitive, patterned, or multi-file changes**
- **Tests need to be generated** from existing code behavior
- **Bug fixes** meet the Artifact Gate (see below)
- **Reviewing** concrete diffs, plans, or files (with `--read-only`)
- **Fixing CI/build issues** with available logs or error output

### Use Claude when:

- The task requires **choosing an approach** or resolving ambiguity
- **Requirements need clarification** before implementation
- The problem is **unknown or unbounded** (no repro, no logs, unclear scope)
- The request involves **strategic/system-level decisions**
- **Teaching, explaining, brainstorming**, or RFC writing

### Two-stage model (Claude → Codex):

For requests mixing strategy and execution:

1. **Stage 1 (Claude):** Frame the problem, assess feasibility, define scope and success criteria
2. **Stage 2 (Codex):** Execute only if Stage 1 produces a concrete, actionable plan
3. **If decision remains uncertain after Stage 1:** Stay in Claude and ask for clarification rather than partially handing off

### Artifact Gate for debugging/investigation:

Use Codex for `debug`, `investigate`, `analyze` tasks **only when** the prompt includes:

- Reproducible command or steps
- Failing test case
- Logs or stack traces
- Performance profile (heap, CPU)
- Bounded symptom surface (specific files/modules)

**Without these artifacts → Use Claude first** to gather evidence and clarify the problem.

## Mode selection guide

Choose the appropriate flags based on task type:

### Reasoning level (`--reasoning`)

| Level | Use for |
|-------|---------|
| `high` | Code review, root-cause debugging, complex refactoring, migration validation, nontrivial failure analysis |
| `medium` (default) | Routine refactors, renames, codemods, test generation, lint/type sweeps |
| `low` | Simple, mechanical changes with clear patterns |

### Read-only mode (`--read-only`)

Use `--read-only` for **analysis without edits**:
- Review a diff or implementation plan
- Assess migration feasibility or risks
- Inspect logs and explain failure causes
- Analyze a specific file or code pattern

**Combine with `--reasoning high`** for deep investigation/review tasks with concrete artifacts.

**Do NOT use `--read-only`** for generic teaching, brainstorming, RFC writing, or architecture exploration — those stay with Claude.

## How to call the script

The script path is:

```
~/.claude/skills/codex/scripts/ask_codex.sh
```

Minimal invocation:

```bash
~/.claude/skills/codex/scripts/ask_codex.sh "Your request in natural language"
```

With file context:

```bash
~/.claude/skills/codex/scripts/ask_codex.sh "Refactor these components to use the new API" \
  --file src/components/UserList.tsx \
  --file src/components/UserDetail.tsx
```

With high reasoning for complex tasks:

```bash
~/.claude/skills/codex/scripts/ask_codex.sh "Debug this memory leak" \
  --reasoning high \
  --file src/memory-intensive-module.ts
```

Read-only analysis:

```bash
~/.claude/skills/codex/scripts/ask_codex.sh "Review this refactor plan for risks" \
  --read-only \
  --reasoning high \
  --file docs/refactor-plan.md
```

Multi-turn conversation (continue a previous session):

```bash
~/.claude/skills/codex/scripts/ask_codex.sh "Also add retry logic with exponential backoff" \
  --session <session_id from previous run>
```

The script prints on success:

```
session_id=<thread_id>
output_path=<path to markdown file>
```

Read the file at `output_path` to get CodeX's response. Save `session_id` if you plan follow-up calls.

## Workflow

1. **Assess the task** against the Decision Policy and Artifact Gate
2. **Select the appropriate mode** (reasoning level, read-only if needed)
3. **Design the solution** and identify key files involved
4. **Run the script** with a clear, concise task description. Tell CodeX the goal and constraints, not step-by-step implementation details — it figures those out itself
5. **Pass relevant files** with `--file` (2-6 high-signal entry points; CodeX has full workspace access and will discover related files on its own)
6. **Read the output** — CodeX executes changes and reports what it did
7. **Review the changes** in your workspace before presenting to user

For multi-step projects, use `--session <id>` to continue with full conversation history. For independent parallel tasks, use the Task tool with `run_in_background: true`.

## Result review checklist

After Codex completes, verify:

- [ ] Changed files match the intended scope
- [ ] No unintended modifications (check git diff)
- [ ] Tests pass (if applicable)
- [ ] The changes satisfy the original success criteria
- [ ] No obvious security issues introduced
- [ ] Edge cases are reasonably handled

Summarize the deltas and any risks when presenting results to the user.

## Options

- `--workspace <path>` — Target workspace directory (defaults to current directory)
- `--file <path>` — Point CodeX to key entry-point files (repeatable, workspace-relative or absolute). Don't duplicate their contents in the prompt
- `--session <id>` — Resume a previous session for multi-turn conversation
- `--model <name>` — Override model (default: uses Codex config)
- `--reasoning <level>` — Reasoning effort: `low`, `medium`, `high` (default: `medium`)
- `--sandbox <mode>` — Override sandbox policy (default: workspace-write via full-auto)
- `--read-only` — Read-only mode for pure discussion/analysis, no file changes
