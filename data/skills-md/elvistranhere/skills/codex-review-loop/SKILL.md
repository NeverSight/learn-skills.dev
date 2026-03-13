---
name: codex-review-loop
description: "Automated code review and fix loop using OpenAI Codex CLI as reviewer and Claude Code as fixer. Use when the user says 'codex review', 'review loop', 'auto review and fix', 'review my code', or wants to run iterative code review against a base branch until all issues are resolved. Calls codex exec review to review the diff, Claude Code fixes the findings, then re-reviews until clean or max rounds reached."
allowed-tools: Bash(codex *), Bash(git *), Bash(npx *), Bash(npm *), Bash(pnpm *), Read, Edit, Grep, Glob
---

# Codex Review Loop

Iterative review-fix cycle: Codex reviews the diff, Claude Code fixes, repeat until LGTM.

Works with any language or framework — TypeScript, Python, Go, Rust, etc.

## Prerequisites

- `codex` CLI installed and authenticated
  ```bash
  npm install -g @openai/codex
  codex --version  # verify
  ```
- Inside a git repo with changes on the current branch vs a base branch

## Parameters

| Param | Default | Description |
|-------|---------|-------------|
| `BASE_BRANCH` | `staging` | Branch to diff against (`main`, `master`, `develop`, etc.) |
| `MAX_ROUNDS` | `5` | Safety cap to prevent infinite loops |
| `FOCUS` | _(none)_ | Optional review focus, e.g. "security", "performance", "leftover code" |
| `TYPECHECK_CMD` | _(auto)_ | Command to run after fixes. Auto-detected if not provided. |

## Workflow

### Step 0: Auto-detect Typecheck Command

If `TYPECHECK_CMD` was not provided by the user, detect it before starting:

1. Check `package.json` scripts for `typecheck` or `type-check` → use `npm run typecheck`
2. Else if `tsconfig.json` exists → use `npx tsc --noEmit`
3. Else if `mypy.ini` or `pyproject.toml` exists → use `mypy .`
4. Else if `cargo.toml` exists → use `cargo check`
5. Otherwise → no typecheck, skip the gate

### Step 1: Run Codex Review

```bash
bash ~/.claude/skills/codex-review-loop/scripts/codex-review.sh <BASE_BRANCH> /tmp/codex-review-findings.md "<FOCUS>"
```

Script handles: preflight checks, empty diff detection, timeout, partial output warnings.

Then read `/tmp/codex-review-findings.md`.

### Step 2: Parse Findings

Codex output varies — it may be structured (file:line bullets) or prose. Handle both:

- **Clean**: output contains "LGTM", "no issues", "looks good", or has zero actionable items → go to Step 5
- **Structured findings**: extract `file`, `line` (if present), `severity`, `description`
- **Prose findings**: extract the core issue description and the file mentioned

For each finding, build a **signature**: `file:line:first_30_chars_of_description` (use `unknown:0:` prefix if no file/line).

Write all signatures for this round to `/tmp/codex-review-seen.txt` (append, one per line).

Skip any finding whose signature already exists in `/tmp/codex-review-seen.txt` from a prior round.

### Step 3: Fix Findings

For each new (non-repeat) finding:

1. Read the file at the specified location using the Read tool
2. Understand the issue in full context
3. Apply the fix using the Edit tool
4. **Skip** if: subjective style preference, false positive, or outside scope of the diff
5. Note skipped findings with reason: `repeat | style | false-positive | out-of-scope`

After fixing all actionable findings, go to **Step 4**.

### Step 4: Verify & Loop

If `TYPECHECK_CMD` is set (or was auto-detected):

```bash
<TYPECHECK_CMD>
```

If typecheck fails → fix the type errors before proceeding. Do not re-review with broken types.

Check loop safety:
- If ALL findings this round were repeats → **stop immediately** (infinite loop guard)
- If `round >= MAX_ROUNDS` → go to Step 5
- Otherwise → increment round counter and go back to **Step 1**

Clean up temp files at the start of each round:
```bash
rm -f /tmp/codex-review-findings.md
```

### Step 5: Final Report

Output a summary table:

```
## Codex Review Loop — Complete

| | |
|---|---|
| **Rounds** | <N> |
| **Base branch** | <BASE_BRANCH> |
| **Findings fixed** | <count> |
| **Findings skipped** | <count> (repeat: X, style: Y, false-positive: Z) |
| **Status** | ✅ LGTM / ⚠️ Stopped at max rounds |

### Files changed
- `path/to/file.ts` — <brief description of what was fixed>
- `path/to/other.py` — <brief description>

### Skipped findings
- `file:line` — <reason>
```

Then clean up:
```bash
rm -f /tmp/codex-review-findings.md /tmp/codex-review-seen.txt
```

## Loop Safety

- **MAX_ROUNDS cap**: Never exceed configured max (default 5).
- **Repeat detection**: Signatures are written to `/tmp/codex-review-seen.txt` and persist across rounds. If a finding's signature is already in that file, skip it. If ALL findings in a round are repeats, stop immediately.
- **Type check gate**: Always fix type errors before re-reviewing. Broken types produce noisy findings.
- **Empty diff guard**: Script exits early if there's nothing to review vs the base branch.
- **No commits**: Never commit or push. Leave that to the user.

## Codex CLI Quick Reference

```bash
# Review diff vs base branch
codex exec review --base <branch>

# With focus prompt (focus goes BEFORE flags)
codex exec review "Focus on security vulnerabilities" --base <branch>

# Review only uncommitted changes
codex exec review --uncommitted

# Review a specific commit
codex exec review --commit <sha>

# Shorthand
codex review --base <branch>
```

Timeout: 1–5 min per review depending on diff size.
