---
verified: true
lastVerifiedAt: '2026-02-28'
name: omega-gemini-cli
description: Use when the user wants to use Google Gemini for analysis, large files or codebases, sandbox execution, or brainstorming. Uses headless Gemini CLI scripts (no MCP). Triggers on "use Gemini", "analyze with Gemini", "large file", "sandbox", "brainstorm with Gemini".
version: 2.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read]
best_practices:
  - Always run verify-setup.mjs before first invocation to check CLI availability
  - Use stdin prompt delivery (built into ask-gemini.mjs) -- never pass prompt as positional arg directly to gemini CLI
  - For file review, embed file content in prompt text -- no dedicated --file flag exists
  - Use --json flag for machine-parseable output (wraps response in {"response":"..."} envelope)
  - Use --sandbox / -s flag for code execution tasks requiring isolated sandbox
  - Use --model gemini-2.5-flash or gemini-2.5-flash-lite to reduce quota/latency
  - Set user expectations: simple queries ~2 min, large file/codebase review ~5-10 min
error_handling: graceful
streaming: not_supported
---

# Gemini CLI Skill

Headless wrapper for Google Gemini CLI. Sends prompts via stdin to `gemini -p "" --yolo`.
Free tier available — no API key required (Google OAuth only).

## When to Use

- Get a Google Gemini perspective on any question
- Free-tier AI consultation (no API key costs)
- Code review from Gemini's model
- Brainstorming and analysis tasks
- Cross-validation of Claude's own responses
- Large files or codebases that benefit from Gemini's context window
- Sandbox execution (run/test code via Gemini)

## Response Times

Gemini CLI runs as a subprocess and includes model startup time:

- Simple Q&A / news query: ~2 minutes
- Codebase or large-file review: ~5–10 minutes

Set expectations with the user before running long tasks.

## Usage

### Ask a question

```bash
node .claude/skills/omega-gemini-cli/scripts/ask-gemini.mjs "What is the best caching strategy for a Node.js API?"
```

### Specify model (short or long flag)

```bash
node .claude/skills/omega-gemini-cli/scripts/ask-gemini.mjs "Explain async/await" --model gemini-2.5-flash
node .claude/skills/omega-gemini-cli/scripts/ask-gemini.mjs "Explain async/await" -m gemini-2.5-flash
```

### JSON output

```bash
node .claude/skills/omega-gemini-cli/scripts/ask-gemini.mjs "List 5 design patterns" --json
# Returns: {"response":"..."} on success, {"error":"...","raw":"..."} on parse failure
```

### Code sandbox (short or long flag)

```bash
node .claude/skills/omega-gemini-cli/scripts/ask-gemini.mjs "Write and run a fibonacci function" --sandbox
node .claude/skills/omega-gemini-cli/scripts/ask-gemini.mjs "Write and run a fibonacci function" -s
```

### Stdin usage

```bash
echo "Explain recursion" | node .claude/skills/omega-gemini-cli/scripts/ask-gemini.mjs
```

### File review (embed content in prompt)

```bash
node .claude/skills/omega-gemini-cli/scripts/ask-gemini.mjs "Review this code: $(cat src/auth.ts)"
```

## Availability Check

```bash
node .claude/skills/omega-gemini-cli/scripts/verify-setup.mjs
# Exit 0 = available (Node 18+ and Gemini CLI found)
# Exit 1 = not installed or too old
```

## Scripts

| Script              | Purpose                                                   |
| ------------------- | --------------------------------------------------------- |
| `ask-gemini.mjs`    | Core headless wrapper — sends prompt via stdin            |
| `parse-args.mjs`    | Argument parser (--model/-m, --json, --sandbox/-s)        |
| `verify-setup.mjs`  | Availability check (Node 18+, Gemini CLI via PATH or npx) |
| `format-output.mjs` | Output normalization (JSON envelope handling)             |

## Flags

| Flag            | Short | Description                                                 |
| --------------- | ----- | ----------------------------------------------------------- |
| `--model MODEL` | `-m`  | Gemini model (e.g., gemini-2.5-flash, gemini-2.5-pro)       |
| `--json`        |       | Machine-readable JSON output: `{"response":"..."}` envelope |
| `--sandbox`     | `-s`  | Code execution sandbox mode                                 |

## Models (2026)

| Model ID                 | Notes                                 |
| ------------------------ | ------------------------------------- |
| `gemini-3-pro-preview`   | Latest (2026), highest capability     |
| `gemini-3-flash-preview` | Latest (2026), faster                 |
| `gemini-2.5-pro`         | Stable, high capability               |
| `gemini-2.5-flash`       | Recommended: lower quota/latency      |
| `gemini-2.5-flash-lite`  | Lightest, fastest, lowest quota usage |

## Exit Codes

| Code | Meaning                                                         |
| ---- | --------------------------------------------------------------- |
| 0    | Success                                                         |
| 1    | Error (CLI failure, auth issue, JSON parse failure with --json) |
| 9009 | Windows: command not found (falls back to npx automatically)    |

## Slash Commands (when installed in a project with .claude/commands/)

| Command               | Purpose                                                                 |
| --------------------- | ----------------------------------------------------------------------- |
| `/analyze`            | Run headless script with user's prompt (and any @ file refs)            |
| `/sandbox`            | Run with --sandbox; execute or test code                                |
| `/omega-gemini`       | Alias: run headless for analysis, sandbox, or brainstorm as appropriate |
| `/brainstorm`         | Brainstorm mode (build prompt with challenge + optional methodology)    |
| `/omega-gemini-setup` | Verify Node and Gemini CLI; guide user to install and auth. No MCP.     |

## Anti-Patterns & Iron Laws

1. ALWAYS use verify-setup.mjs before first use
2. NEVER pass prompt as positional arg to raw gemini CLI — use ask-gemini.mjs wrapper
3. ALWAYS validate model parameter (wrapper validates via regex `^[a-zA-Z0-9._-]+$` on Windows)
4. NEVER assume gemini is on PATH — wrapper handles npx `@google/gemini-cli` fallback automatically
5. ALWAYS handle exit code 1 and 9009 gracefully
6. ALWAYS set user expectations about response time before running (2–10 minutes typical)

## Integration Notes

- **Auth:** One-time Google OAuth via `gemini` interactive session (run `gemini` once to sign in)
- **Rate limits:** Governed by Gemini API quotas (generous for personal use on free tier)
- **Platform:** Full cross-platform; Windows uses `shell: true` with model validation; non-Windows uses array args (no shell)
- **npx fallback:** On PATH miss, automatically retries with `npx -y @google/gemini-cli`
- **No timeout flag:** Unlike other omega wrappers, gemini wrapper has no --timeout-ms
- **Stdin delivery:** Prompt always sent via stdin to avoid shell argument length limits (8191-char cmd.exe limit on Windows, ARG_MAX on Linux/macOS)
- **JSON envelope:** `--json` wraps output as `{"response":"..."}` on success or `{"error":"...","raw":"..."}` on failure

## Requirements

- **Node.js 18+** to run the scripts
- **Google Gemini CLI** (`npm install -g @google/gemini-cli`) with one-time Google sign-in

## Memory Protocol

Before work: Read `.claude/context/memory/learnings.md`
After work: Append findings to learnings or issues as needed.

_Note: Use `pnpm search:code` to discover references to this skill codebase-wide._
