---
name: review-fix-loop
description: Use when a code analysis tool reports findings and you want an automated fix-verify loop — runs the analysis command, dispatches parallel subagents to fix all findings, verifies with project lint and tests, and loops until zero findings remain.
---

# review-fix-loop

Autonomous review-and-fix loop. Runs any code analysis tool, dispatches parallel subagents to fix all findings, verifies with the project's own lint and test commands, and loops until zero findings remain.

## Examples

CodeRabbit review of all changes:

```
/review-fix-loop coderabbit review --plain -t all
```

DeepSource issues as JSON:

```
/review-fix-loop deepsource issues --output json
```

Auto-detect tool from project config:

```
/review-fix-loop
```

---

## Step 1 — Determine the analysis command

Everything the user types after `/review-fix-loop` is available as `$ARGUMENTS`.

If the user provided a command (from `$ARGUMENTS`), use it as-is.

If no command was provided, auto-detect by checking for config files in the project root:

| Config file | Tool | Command | Auth check |
|---|---|---|---|
| `.coderabbit.yaml` | CodeRabbit | `coderabbit review --plain -t all` | `coderabbit auth status` |
| `.deepsource.toml` | DeepSource | `deepsource issues --output json` | `deepsource auth status` |
| `.eslintrc*` or `eslint.config.*` | ESLint | `eslint . --format json` | — |
| `ruff.toml` or `[tool.ruff]` in `pyproject.toml` | Ruff | `ruff check --output-format json` | — |

If multiple config files exist, list them and ask the user which tool to run.

If no config file is found, ask the user to provide the analysis command.

---

## Step 2 — Prerequisite check

Extract the tool name (first word of the analysis command) and verify it is available:

```bash
command -v <tool-name> >/dev/null 2>&1
```

If not found, tell the user the tool is not installed and suggest installation. **Halt** — do not proceed until the tool is available.

If the tool has an auth check listed in the Step 1 table, run it. For user-provided commands not in the table, skip the auth check. If unauthenticated, tell the user how to authenticate. **Halt** until resolved.

---

## Step 3 — Run analysis

Execute the analysis command and capture full stdout and stderr:

```bash
<analysis-command> 2>&1
```

If the command exits with a non-zero status and produces no parseable findings, report the error to the user and **halt**.

Store the complete output for parsing.

---

## Step 4 — Parse findings

From the captured output, extract all findings. Each finding has:

- **File path** (relative to project root)
- **Line number** (if present in the output)
- **Issue description** — title, category, severity, or equivalent
- **Fix instructions** — the tool's suggested fix, remediation text, or "Prompt for AI Agent" block if present. If none, use the issue description.

Build a list: `findings = [{file, line, description, fix_instructions}, ...]`

Display a count:

```
Findings: <total> across <file_count> files
```

---

## Step 5 — Zero findings check

If `findings` is empty:
- Print: `Zero findings. Codebase is clean.`
- **Exit loop** — skip to Step 10.

---

## Step 6 — Group by file

Group findings by file path. All findings in the same file go to one subagent to avoid conflicting edits.

---

## Step 7 — Fix with subagents (parallel)

For each file group, dispatch one subagent in parallel with this prompt:

```
Fix the following findings in `<file_path>`.

Current file content:
<content of the file>

Findings to fix:
<for each finding in the group>
- Line <line>: <description>
  Fix instructions: <fix_instructions>
</for each>

Requirements:
- Edit only what is needed to fix the listed findings.
- Do not refactor unrelated code.
- Preserve all existing tests.
- After editing, confirm what was changed.
```

### Claude Code

Use the `Agent` tool with `subagent_type: "general-purpose"` for each file group. Launch all agents in a single message to run them in parallel. Wait for all to complete before proceeding.

### Gemini CLI

Use the `generalist_agent` tool for each file group. Dispatch all calls to run in parallel. Wait for all to complete before proceeding.

### Other agents

If parallel subagent dispatch is not available, fix each file group sequentially — read the file, apply the fixes directly, then move to the next file group.

---

## Step 8 — Verify

Discover and run the project's lint and test commands.

### Discovery order

Check these sources in order. Use the first lint command and first test command found:

**1. Project files:**

| File | Lint command | Test command |
|---|---|---|
| `package.json` | `scripts.lint` (run via `npm run lint`) | `scripts.test` (run via `npm test`) |
| `pyproject.toml` | Look for `[tool.ruff]` → `ruff check .` | Look for `[tool.pytest]` → `pytest --tb=short -q` |
| `Makefile` | `make lint` (if target exists) | `make test` (if target exists) |
| `Justfile` | `just lint` (if recipe exists) | `just test` (if recipe exists) |

**2. CLAUDE.md or project docs:**

Look for a "Commands" section listing lint/test commands.

**3. Ask the user:**

If no lint or test commands can be detected, ask: "What commands do you use to lint and test this project?"

### Run verification

Run the lint command first, then the test command:

```bash
<lint-command>
<test-command>
```

If either fails:
- Read the error output.
- Fix the regressions directly (do not spawn subagents for verification fixes).
- Re-run the failing command until it passes before continuing.

---

## Step 9 — Loop

Go back to Step 3.

**Maximum iterations**: if the loop has completed 5 iterations, exit regardless of findings and proceed to Step 10.

**Stuck detection**: track the set of findings each iteration by (file + description). If the same findings appear unchanged for 2 consecutive loops:
- Print: `Stuck after <n> iterations. The following findings require manual review:`
- List each stuck finding with file, line, and description.
- **Exit loop**.

---

## Step 10 — Report

After the loop exits (clean or stuck), print a summary:

```
+----------------------------------+
|  Review Fix Loop — Summary       |
+----------------+-----------------+
| Iterations     | <n>             |
| Fixed          | <count>         |
| Remaining      | <count>         |
+----------------+-----------------+
```

If remaining > 0, list each stuck finding below the table with its file path, line number, and description.
