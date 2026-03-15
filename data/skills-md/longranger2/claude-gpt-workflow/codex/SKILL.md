---
name: codex
description: Delegate coding tasks to Codex CLI for execution, or discuss implementation approaches with it. CodeX is a cost-effective, strong coder — great for batch refactoring, code generation, multi-file changes, test writing, and multi-turn implementation tasks. Use when the plan is clear and needs hands-on coding. Claude handles architecture, strategy, copywriting, and ambiguous problems better.
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

## Decision policy

Call CodeX when at least one of these is true:

- The implementation plan is clear and needs coding execution.
- The task involves batch refactoring, code generation, or repetitive changes.
- Multiple files need coordinated modifications following a defined pattern.
- You want a practitioner's perspective on whether a plan is feasible.
- The task is cost-sensitive and doesn't require deep architectural reasoning.
- Writing or updating tests based on existing code.
- Simple-to-moderate bug fixes where the root cause is identified.

## Workflow

1. Design the solution and identify the key files involved.
2. Run the script with a clear, concise task description. Tell CodeX the goal and constraints, not step-by-step implementation details — it figures those out itself. For discussion, use a question-oriented task with `--read-only`.
3. Pass relevant files with `--file` (2-6 high-signal entry points; CodeX has full workspace access and will discover related files on its own).
4. Read the output — CodeX executes changes and reports what it did.
5. Review the changes in your workspace.

For multi-step projects, use `--session <id>` to continue with full conversation history. For independent parallel tasks, use the Task tool with `run_in_background: true`.

## Options

- `--workspace <path>` — Target workspace directory (defaults to current directory).
- `--file <path>` — Point CodeX to key entry-point files (repeatable, workspace-relative or absolute). Don't duplicate their contents in the prompt.
- `--session <id>` — Resume a previous session for multi-turn conversation.
- `--model <name>` — Override model (default: uses Codex config).
- `--reasoning <level>` — Reasoning effort: `low`, `medium`, `high` (default: `medium`). Use `high` for code review, debugging, complex refactoring, or root cause analysis.
- `--sandbox <mode>` — Override sandbox policy (default: workspace-write via full-auto).
- `--read-only` — Read-only mode for pure discussion/analysis, no file changes.
