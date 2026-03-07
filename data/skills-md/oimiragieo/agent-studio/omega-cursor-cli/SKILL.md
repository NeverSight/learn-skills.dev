---
name: omega-cursor-cli
description: Shell out to Cursor Agent CLI for headless IDE-aware code tasks. Supports multi-model routing (auto mode routes to Claude, Gemini, GPT). Requires Cursor Pro/Business subscription.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read]
args: '"PROMPT" [--model MODEL] [--json] [--yolo] [--trust] [--timeout-ms N]'
best_practices:
  - Always run verify-setup.mjs before first invocation
  - Cursor subscription is required -- most restrictive availability of all omega tools
  - Use --yolo for non-interactive headless mode (auto-approves all tool calls)
  - Use --trust for workspace trust without prompting
  - Use auto model for Cursor's intelligent model routing
error_handling: graceful
streaming: not_supported
verified: true
lastVerifiedAt: 2026-02-24T04:26:35.324Z
---

# Cursor CLI Skill

<identity>
Headless wrapper for Cursor Agent CLI. Passes prompt as last positional arg
to `cursor-agent --print --output-format text`. Multi-model routing via --model auto.
Requires paid Cursor subscription.
</identity>

<capabilities>
- Headless Cursor Agent CLI invocation with positional prompt
- Multi-model routing (auto, claude-4.6-opus, gemini-3.1-pro, gpt-5.3-codex, etc.)
- JSON output mode
- YOLO mode (auto-approve all tool calls for non-interactive use)
- Trust mode (skip workspace trust prompts)
- MCP approval mode (--approve-mcps)
- Wrapper-level timeout with exit code 124
- Complex Windows PATH resolution (agent, cursor-agent, %LOCALAPPDATA%, npx fallback)
- Availability verification
</capabilities>

## Usage

### Ask a question (auto model selection)

```bash
node .claude/skills/omega-cursor-cli/scripts/ask-cursor.mjs "How should I structure this React component?" --yolo --trust
```

### Specific model

```bash
node .claude/skills/omega-cursor-cli/scripts/ask-cursor.mjs "Review this API design" --model claude-4.6-opus --yolo --trust
```

### With timeout

```bash
node .claude/skills/omega-cursor-cli/scripts/ask-cursor.mjs "Refactor authentication" --yolo --trust --timeout-ms 180000
```

### JSON output

```bash
node .claude/skills/omega-cursor-cli/scripts/ask-cursor.mjs "Generate types" --json --yolo --trust
```

## Availability Check

```bash
node .claude/skills/omega-cursor-cli/scripts/verify-setup.mjs
# Exit 0 = available (CLI found)
# Exit 1 = not available
```

## When to Use

- Multi-model perspective via Cursor's auto routing
- IDE-aware code generation (Cursor has workspace context)
- When a non-Claude, non-OpenAI perspective is desired
- Tasks where Cursor's composer models excel

## Iron Laws

1. ALWAYS use --yolo --trust for headless mode (otherwise blocks on approval prompts)
2. NEVER assume CLI is available -- most restrictive subscription requirement
3. ALWAYS include --timeout-ms for production usage
4. NEVER attempt to detect subscription status programmatically (not possible)
5. ALWAYS handle WSL issues on Windows (some configurations require WSL)

## Anti-Patterns

| Anti-Pattern                     | Why Bad                                | Correct Approach                      |
| -------------------------------- | -------------------------------------- | ------------------------------------- |
| Running without --yolo           | Blocks on tool approval prompts        | Always pass --yolo                    |
| Running without --trust          | Blocks on workspace trust prompt       | Always pass --trust                   |
| Assuming auto model is available | Depends on subscription tier           | Check with cursor-agent --list-models |
| Hardcoding cursor-agent path     | PATH differs across OS/install methods | Wrapper handles resolution            |
| Ignoring WSL requirements        | Some Windows installs are WSL-only     | Document in setup instructions        |

## Scripts

| Script              | Purpose                                                          |
| ------------------- | ---------------------------------------------------------------- |
| `ask-cursor.mjs`    | Core headless wrapper -- prompt as last positional arg           |
| `parse-args.mjs`    | Argument parser (--model, --json, --yolo, --trust, --timeout-ms) |
| `verify-setup.mjs`  | Availability check (multi-path resolution)                       |
| `format-output.mjs` | Output normalization                                             |

## Exit Codes

| Code | Meaning                                 |
| ---- | --------------------------------------- |
| 0    | Success                                 |
| 1    | Error (CLI failure, subscription issue) |
| 124  | Timeout (--timeout-ms exceeded)         |

## Integration Notes

- **Subscription:** Cursor Pro or Business required for agent/headless mode
- **Stdin limit:** `ASK_CURSOR_MAX_STDIN_BYTES` env var (default 50MB)
- **Available models:** claude-4.6-opus, claude-4.6-sonnet, composer-1.5, gemini-3.1-pro, gpt-5.3-codex, auto
- **Platform:** Partial cross-platform (WSL issues on some Windows configurations)
- **PATH resolution order:** agent -> cursor-agent -> %LOCALAPPDATA%\cursor-agent\cursor-agent.cmd -> npx @cursor/agent

## Memory Protocol

Before work: Read `.claude/context/memory/learnings.md`
After work: Append findings to learnings or issues as needed.

_Note: Use `pnpm search:code` to discover references to this skill codebase-wide._
