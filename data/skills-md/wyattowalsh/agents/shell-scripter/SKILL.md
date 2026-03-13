---
name: shell-scripter
description: >-
  Shell script generation, review, and dialect conversion. Makefile and justfile
  generation. ShellCheck rules. Use for shell work. NOT for Python
  (python-conventions) or CI/CD (devops-engineer).
argument-hint: "<mode> [script|description]"
license: MIT
model: sonnet
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Shell Scripter

Generate, review, convert, and lint shell scripts. Makefile and justfile generation. References ShellCheck rule IDs with explanations but does NOT run ShellCheck.

**Scope:** Shell scripts (bash, zsh, fish, sh/POSIX), Makefiles, justfiles. NOT for Python scripts (use python-conventions), CI/CD pipelines (use devops-engineer), or running/testing scripts.

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `create <description>` | Generate a shell script from natural language |
| `review <script or path>` | Audit for pitfalls, reference ShellCheck rules |
| `convert <script or path> <target>` | Dialect conversion (bash/zsh/fish) |
| `posix <script or path>` | POSIX compliance check at pattern level |
| `makefile <tasks>` | Generate a Makefile from task descriptions |
| `justfile <tasks>` | Generate a justfile from task descriptions |
| Natural language about shell scripting | Auto-detect mode from intent |
| Empty | Show mode menu with examples |

### Auto-Detection Heuristic

1. Path to `.sh`/`.bash`/`.zsh`/`.fish` file + modification verb (review, check, fix, audit, lint) -> **review**
2. Path to `.sh` file + "to zsh/fish/bash" -> **convert**
3. Path to `.sh` file + "posix" or "portable" -> **posix**
4. "makefile" or "make targets" in input -> **makefile**
5. "justfile" or "just recipes" in input -> **justfile**
6. Describes desired script behavior -> **create**
7. Ambiguous -> ask which mode

## Mode: Create

Generate a shell script from a natural language description.

### Generation Process

1. Determine target dialect (default: bash)
2. Run `uv run python skills/shell-scripter/scripts/dialect-converter.py --list-features <dialect>` to confirm available features
3. Write the script with:
   - Proper shebang (env-based like `env bash`, not hardcoded interpreter paths)
   - `set -euo pipefail` for bash (equivalent for other dialects)
   - Meaningful variable names, quoted expansions
   - Error handling for external commands
   - Usage function if script accepts arguments

### Validation

4. Run `uv run python skills/shell-scripter/scripts/script-analyzer.py --stdin <<< "$SCRIPT"` on the generated script
5. Fix any issues found, present final script

## Mode: Review

Audit a shell script for common pitfalls. Reference ShellCheck rule IDs.

### Analysis

1. Read the target script
2. Run `uv run python skills/shell-scripter/scripts/script-analyzer.py <path>`
3. Parse the JSON output: `{shebang, dialect, issues, posix_compatible, complexity_estimate}`
4. For each issue, load `references/shellcheck-rules.md` to explain the rule ID

### Findings Report

5. Group findings by severity: error > warning > info > style
6. Present findings with:
   - ShellCheck rule ID (e.g., SC2086)
   - Line number and code snippet
   - Explanation of WHY it is a problem
   - Concrete fix
7. If no issues found, state this explicitly

**Severity mapping:**

| Severity | Examples |
|----------|----------|
| error | Unquoted variables in conditionals, syntax errors, command injection |
| warning | Missing error handling, unquoted glob expansions, deprecated syntax |
| info | Suboptimal patterns, unnecessary subshells, redundant commands |
| style | Inconsistent quoting, missing shellcheck directives, naming |

## Mode: Convert

Convert shell syntax between bash, zsh, and fish.

1. Read the source script
2. Identify source dialect (from shebang or `--from` flag)
3. Run `uv run python skills/shell-scripter/scripts/dialect-converter.py <path> --from <source> --to <target>`
4. Parse the JSON output: `{converted_script, changes, warnings}`
5. Present the converted script with a change summary table
6. Flag any constructs that have no direct equivalent in the target dialect

## Mode: POSIX

Check a script for POSIX compliance at the pattern level.

1. Read the target script
2. Run `uv run python skills/shell-scripter/scripts/script-analyzer.py <path> --posix`
3. Identify bash-isms: `[[ ]]`, `(( ))`, arrays, `local`, `source`, process substitution, `{a..z}`, `$'...'`
4. For each bash-ism, suggest the POSIX equivalent from `references/posix-compatibility.md`
5. Report whether the script is POSIX-compatible or list required changes

## Mode: Makefile

Generate a Makefile from task descriptions.

1. Parse task descriptions from `$ARGUMENTS`
2. Determine dependencies between tasks
3. Generate Makefile with:
   - `.PHONY` declarations for non-file targets
   - `.DEFAULT_GOAL`
   - `help` target using self-documenting pattern (`## comments`)
   - Consistent variable naming (`UPPER_SNAKE_CASE`)
   - `.ONESHELL` when multi-line recipes need shared state
4. Follow conventions from `references/makefile-justfile.md`

## Mode: Justfile

Generate a justfile from task descriptions.

1. Parse task descriptions from `$ARGUMENTS`
2. Generate justfile with:
   - Recipe documentation comments
   - Default recipe (first position or `default` alias)
   - Parameter declarations with defaults where sensible
   - `set shell` directive if non-default shell needed
   - `set dotenv-load` if environment variables are referenced
3. Follow conventions from `references/makefile-justfile.md`

## Canonical Vocabulary

Use these terms exactly throughout:

| Term | Definition |
|------|-----------|
| **dialect** | Shell language variant: bash, zsh, fish, sh (POSIX) |
| **bash-ism** | Syntax or feature not in POSIX sh (e.g., arrays, `[[ ]]`) |
| **shebang** | `#!` line specifying the interpreter |
| **SC rule** | A ShellCheck rule ID (e.g., SC2086 = unquoted variable) |
| **recipe** | A justfile target (not "task" or "rule") |
| **target** | A Makefile target (not "task" or "recipe") |
| **portable** | Works across bash/zsh/sh without modification |

## Reference Files

Load ONE reference at a time. Do not preload all references into context.

| File | Content | Read When |
|------|---------|-----------|
| `references/shellcheck-rules.md` | Top 50 ShellCheck rules with severity, explanation, examples, fixes | Review mode, explaining SC rule IDs |
| `references/posix-compatibility.md` | POSIX builtins, bash-isms with POSIX equivalents, portability patterns | POSIX mode, create mode with `--posix` |
| `references/dialect-differences.md` | Syntax differences between bash/zsh/fish with conversion recipes | Convert mode, cross-dialect questions |
| `references/common-pitfalls.md` | Unquoted vars, missing error handling, injection, race conditions, traps | Review mode, create mode best practices |
| `references/makefile-justfile.md` | Makefile best practices, justfile syntax and patterns, migration guide | Makefile mode, justfile mode |

| Script | When to Run |
|--------|-------------|
| `scripts/script-analyzer.py` | Review and POSIX modes -- static analysis of shell scripts |
| `scripts/dialect-converter.py` | Convert mode -- syntax conversion between dialects |

## Critical Rules

1. Never claim to run ShellCheck -- reference SC rule IDs and explain them, but analysis is pattern-based
2. Always use env-based shebangs (e.g., `env bash`), never hardcoded interpreter paths
3. Default to `set -euo pipefail` in generated bash scripts -- omit only with explicit justification
4. Always quote variable expansions unless splitting is intentionally required (SC2086)
5. Never generate scripts that use `eval` unless no alternative exists -- explain the risk
6. Every generated script must include error handling for external commands
7. Generated Makefiles must include a `.PHONY` declaration and a `help` target
8. Generated justfiles must have a default recipe and documentation comments
9. Review findings must include the SC rule ID, line number, and a concrete fix
10. Never modify the script being reviewed -- review is read-only
11. Convert mode must warn about constructs with no direct equivalent in the target dialect
12. POSIX mode must identify every bash-ism and provide a POSIX alternative
