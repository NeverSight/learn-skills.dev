---
verified: true
lastVerifiedAt: '2026-02-28'
name: omega-codex-cli
description: Shell out to OpenAI Codex CLI for headless code generation, analysis, and question-answering. Optimized for code tasks. Requires OPENAI_API_KEY env var.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read]
best_practices:
  - Always run verify-setup.mjs before first invocation
  - Ensure OPENAI_API_KEY env var is set before use
  - Use --json for JSONL event stream output in automation pipelines
  - Use --timeout-ms for long-running tasks to prevent hangs
  - Use --sandbox for isolated workspace-write mode
error_handling: graceful
streaming: supported
---

# Codex CLI Skill

Headless wrapper for OpenAI Codex CLI. Passes prompt as positional arg to `codex exec "PROMPT"`.
Optimized for code generation and analysis. Requires OPENAI_API_KEY.

## When to Use

- Code generation tasks needing OpenAI/GPT model perspective
- Cross-validation of code solutions with a non-Claude model
- Tasks benefiting from Codex's code optimization focus
- Multi-LLM consultation workflows

## Usage

### Ask a question

```bash
node .claude/skills/omega-codex-cli/scripts/ask-codex.mjs "Implement a Redis caching layer for Express"
```

### With timeout

```bash
node .claude/skills/omega-codex-cli/scripts/ask-codex.mjs "Refactor this module" --timeout-ms 120000
```

### JSONL streaming output

```bash
node .claude/skills/omega-codex-cli/scripts/ask-codex.mjs "Generate unit tests" --json
```

### Sandbox mode

```bash
node .claude/skills/omega-codex-cli/scripts/ask-codex.mjs "Write and test a sort algorithm" --sandbox
```

## Availability Check

```bash
node .claude/skills/omega-codex-cli/scripts/verify-setup.mjs
# Exit 0 = available (CLI found + OPENAI_API_KEY set)
# Exit 1 = not available
```

## Scripts

| Script              | Purpose                                                    |
| ------------------- | ---------------------------------------------------------- |
| `ask-codex.mjs`     | Core headless wrapper — prompt as positional arg           |
| `parse-args.mjs`    | Argument parser (--model, --json, --sandbox, --timeout-ms) |
| `verify-setup.mjs`  | Availability check (CLI + OPENAI_API_KEY)                  |
| `format-output.mjs` | JSONL event stream normalization                           |

## Flags

| Flag             | Description                                       |
| ---------------- | ------------------------------------------------- |
| `--model MODEL`  | Codex model to use                                |
| `--json`         | JSONL event stream output                         |
| `--sandbox`      | Workspace-write sandbox mode                      |
| `--timeout-ms N` | Timeout in milliseconds (exit code 124 on expiry) |

## Exit Codes

| Code | Meaning                                    |
| ---- | ------------------------------------------ |
| 0    | Success                                    |
| 1    | Error (CLI failure, auth issue, API error) |
| 124  | Timeout (--timeout-ms exceeded)            |

## Anti-Patterns & Iron Laws

1. ALWAYS verify OPENAI_API_KEY is set before invocation
2. NEVER use stdin for prompt delivery — Codex uses positional arg
3. ALWAYS include --skip-git-repo-check (built into wrapper)
4. ALWAYS set --timeout-ms for production usage
5. NEVER assume --json output is standard JSON — it produces JSONL event stream

## Integration Notes

- **API key:** `OPENAI_API_KEY` env var required
- **Rate limits:** OpenAI API rate limits apply
- **Platform:** Full cross-platform (Windows uses cmd.exe /d /s /c wrapper)

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.

_Note: Use `pnpm search:code` to discover references to this skill codebase-wide._
