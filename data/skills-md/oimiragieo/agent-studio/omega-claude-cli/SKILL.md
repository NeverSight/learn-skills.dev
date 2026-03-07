---
verified: true
lastVerifiedAt: '2026-02-28'
name: omega-claude-cli
description: Shell out to Claude Code CLI to invoke a second Claude session headlessly. Useful for cross-validation, second opinions, and isolated analysis without sharing current agent context. Requires Anthropic account.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read]
best_practices:
  - Always run verify-setup.mjs before first invocation
  - Use for second-opinion validation where context isolation matters
  - Use --timeout-ms to prevent indefinite hangs
  - --dangerously-skip-permissions is required for headless mode (already in wrapper)
  - Use format-output.mjs to strip conversational text framing from JSON responses
error_handling: graceful
streaming: not_supported
---

# Claude CLI Skill

Headless wrapper for Claude Code CLI. Invokes a separate Claude session via
`claude -p "PROMPT" --dangerously-skip-permissions`. Provides isolated second
opinions without sharing the current agent's context window.

## When to Use

- Second-opinion validation (isolated Claude session without shared context)
- Cross-validation of current agent's reasoning
- Delegated deep analysis that should not consume current context window
- Multi-LLM consultation workflows (as one of the participating models)
- Chairman synthesis in llm-council workflows

## Usage

### Ask a question

```bash
node .claude/skills/omega-claude-cli/scripts/ask-claude.mjs "What are the security implications of this auth design?"
```

### Specify model

```bash
node .claude/skills/omega-claude-cli/scripts/ask-claude.mjs "Review this code" --model sonnet
```

### JSON output (with text stripping)

```bash
node .claude/skills/omega-claude-cli/scripts/ask-claude.mjs "Analyze dependencies" --json
```

### With timeout

```bash
node .claude/skills/omega-claude-cli/scripts/ask-claude.mjs "Deep security review of auth.ts" --timeout-ms 300000
```

## Availability Check

```bash
node .claude/skills/omega-claude-cli/scripts/verify-setup.mjs
# Exit 0 = available (CLI found)
# Exit 1 = not available
```

## Scripts

| Script              | Purpose                                                    |
| ------------------- | ---------------------------------------------------------- |
| `ask-claude.mjs`    | Core headless wrapper — prompt as positional arg to -p     |
| `parse-args.mjs`    | Argument parser (--model, --json, --sandbox, --timeout-ms) |
| `verify-setup.mjs`  | Availability check with npx fallback                       |
| `format-output.mjs` | Output normalization with extractJsonResponse()            |

## Flags

| Flag             | Description                                                      |
| ---------------- | ---------------------------------------------------------------- |
| `--model MODEL`  | opus (Opus 4.6), sonnet (4.5), haiku (4.5), or full model ID     |
| `--json`         | JSON output (strips conversational text via extractJsonResponse) |
| `--sandbox`      | Code execution sandbox mode                                      |
| `--timeout-ms N` | Timeout in milliseconds (exit code 124 on expiry)                |

## Exit Codes

| Code | Meaning                         |
| ---- | ------------------------------- |
| 0    | Success                         |
| 1    | Error (CLI failure, auth issue) |
| 124  | Timeout (--timeout-ms exceeded) |

## Anti-Patterns & Iron Laws

1. ALWAYS use --dangerously-skip-permissions for headless mode (built into wrapper)
2. NEVER expect to share context between this CLI session and the current agent
3. ALWAYS use format-output.mjs to strip conversational text wrapping from JSON
4. ALWAYS set --timeout-ms for production usage
5. NEVER invoke on security-critical tasks without acknowledging the risk

## Integration Notes

- **Auth:** Claude Code subscription or ANTHROPIC_API_KEY env var
- **Models:** opus, sonnet, haiku, or full model IDs
- **Security:** --dangerously-skip-permissions allows all tool execution; intended for trusted automation only
- **Platform:** Full cross-platform (Windows uses cmd.exe /d /s /c wrapper)

## Memory Protocol

Before work: Read `.claude/context/memory/learnings.md`
After work: Append findings to learnings or issues as needed.

_Note: Use `pnpm search:code` to discover references to this skill codebase-wide._
