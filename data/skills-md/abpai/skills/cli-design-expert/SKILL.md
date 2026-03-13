---
name: cli-design-expert
description: "Design or review command-line interfaces for usability and automation: help text, args/flags, stdout vs stderr, exit codes, TTY behavior, config precedence, and safe handling of secrets and destructive actions."
license: CC-BY-SA-4.0
compatibility: Works with any CLI language/framework. Best with an args parser library and POSIX conventions (stdout/stderr, exit codes, signals). See references/CLI_GUIDELINES.md.
metadata:
  version: "1.1.0"
  author: "cli-guidelines-community"
  upstream_guidelines: "https://clig.dev"
  reference_file: "references/CLI_GUIDELINES.md"
---

# CLI Design Expert

Use this skill to design, refactor, or audit CLIs that are:

- Human-friendly for interactive use
- Predictable in scripts and CI
- Safe for destructive operations
- Clear in output, errors, and exit semantics

Primary reference: `references/CLI_GUIDELINES.md`.

## Working stance

Be direct and engineering-first. If a design is fragile, ambiguous, or hostile to automation, call it out and propose concrete fixes.

## Non-negotiable checks (fast fail)

Treat any failure below as P0.

1. Non-interactive path is required

- Never make an interactive prompt the only input path.
- Every prompt needs a non-interactive alternative (flag/arg/file/stdin).
- If `stdin` is not a TTY, do not prompt. Fail with actionable guidance and required flags.
- Provide `--no-input` (or equivalent) to disable prompts.

1. Secrets safety

- Never accept secrets via flags (leaks via `ps` and shell history).
- Prefer stdin, `--secret-file`, OS keychain, or a TTY-only prompt with a non-interactive alternative.

1. Scriptability and CI behavior

- Detect TTY and adapt output and interactivity.
- Disable spinners/animations when stdout is not a TTY.
- Disable color when stdout/stderr are not TTY, when `NO_COLOR` is set, when `TERM=dumb`, or when `--no-color` is passed.
- Keep stdout clean for data; send status/progress/logging to stderr.

1. Output streams and exit codes

- Primary pipeable output goes to stdout.
- Logs, warnings, progress, and errors go to stderr.
- Exit 0 on success; non-zero on failure. Map non-zero codes to meaningful failure categories.

1. Risk-scaled safeguards

- For destructive actions, use confirmations that scale with risk.
- Support a scriptable bypass (e.g., `--force` or `--yes`), and consider `--confirm="resource-name"` for severe actions.
- Offer `--dry-run` for risky or complex state changes when possible.

1. Signals and cancellation

- Ctrl-C (SIGINT) should exit quickly with immediate feedback.
- Timebox cleanup and allow a second Ctrl-C to force exit if cleanup is slow.

## Quick triage questions

- Who is the user: interactive human, script/CI, or both?
- What is the job-to-be-done: query/list state, or change state?
- What are the core objects and verbs?
- What must stay stable for automation (output format, exit codes, flags)?

## Procedure: Design a new CLI (or add a command)

### Step 1: Propose a command model

- Keep the initial surface area small.
- Choose one model and stay consistent:
- Single command + flags for simple tools.
- Subcommands (often noun-verb or verb-noun) for multi-task tools.

Deliverable:

- List of commands with one-line purposes.

### Step 2: Decide positional args vs flags

Heuristic:

- Use positional args only for obvious primary object(s) where order is standard and unambiguous.
- If two positionals can be confused (similar shape/meaning) or order is not obvious, use flags instead.
- Prefer long flags. Use short flags only for the most common options, and keep them consistent across commands.

Deliverable:

- Usage line + args/flags tables per command.

### Step 3: Define output contract (human + machine)

- Define exactly what goes to stdout vs stderr.
- Provide at least one machine-readable mode when helpful (commonly `--json`).
- Keep human-readable output scannable and useful.

Deliverable:

- `stdout` content
- `stderr` content
- Exit-code map
- High-level `--json` schema (if supported)

### Step 4: Write help text and examples

- `-h/--help` must work even when other args are wrong.
- If run incorrectly, show a short error + the relevant usage + "use --help".
- Lead help with examples (common first). Provide a docs/support path in top-level help.

Deliverable:

- Draft help text for top-level and relevant subcommands.

### Step 5: Define errors and safety

- Errors must be actionable: what failed, why, and how to fix it.
- Do not hide important failures behind generic codes or stack traces unless `--debug` is enabled.
- For state changes, give explicit feedback about what happened (or what would happen in `--dry-run`).

Deliverable:

- Error-message patterns + safety/confirmation design.

### Step 6: Specify interactivity and TTY rules

- Only prompt when stdin is a TTY.
- If piped input is supported, read it. If not, fail quickly with guidance.
- Provide clear quiet and verbose modes if logs exist.

Deliverable:

- TTY behavior table (TTY vs non-TTY).

### Step 7: Add config and env vars (only if needed)

Use explicit precedence to avoid hidden config behavior:

1. Flags
2. Environment variables
3. Project-level config
4. User-level config (XDG, e.g. `~/.config/<tool>/config`)
5. System-wide config

Deliverable:

- Config keys + precedence + storage locations.

## Procedure: Review an existing CLI

Produce two outputs.

### A) Scorecard (0-2 each)

- Command structure and naming
- Args/flags clarity
- Help discoverability (examples first)
- stdout/stderr correctness
- Exit-code discipline
- Scriptability (non-TTY behavior)
- Machine-output mode (when appropriate)
- Safety (`--dry-run`, confirmations)
- Secrets handling
- Signal handling (Ctrl-C)
- Config precedence (if applicable)
- Future-proofing (avoid time bombs)

### B) Prioritized fixes

- P0: correctness, safety, and scriptability failures
- P1: usability and discoverability issues
- P2: polish and consistency

## Templates

### Help skeleton

NAME
<tool> - <one line value prop>

USAGE
<tool> <command> [options] <args>

EXAMPLES
<tool> <command> ...
<tool> <command> ... --json | jq .

OPTIONS
-h, --help Show help
--json Output machine-readable JSON (if supported)
--no-color Disable color
--no-input Disable prompts
-q, --quiet Reduce non-essential output (if supported)
-v, --verbose Increase logging (if supported)
-n, --dry-run Describe changes without applying them (if supported)

SUPPORT
<docs / issues link>

### Error skeleton

Error: <what failed in plain language>.
Cause: <most likely reason>.
Fix: <exact next step / command / flag>.

## References

- Full guideline text: `references/CLI_GUIDELINES.md`
