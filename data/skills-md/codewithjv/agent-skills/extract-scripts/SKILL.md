---
name: extract-scripts
description: Review a skill and extract deterministic, mechanical steps into shell scripts. Makes skills more reliable by separating precision work (scripts) from judgment work (AI). Use when asked to extract scripts from a skill, make a skill more deterministic, or split a skill into script + prompt.
---

# Extract Scripts from Skills

Review a skill file and extract the mechanical, deterministic steps into standalone shell scripts. The skill keeps only the judgment calls — summarising, interpreting, choosing, writing.

## When to Use

Activate when the user:
- Asks to extract scripts from a skill
- Wants to make a skill more reliable or deterministic
- Says a skill is inconsistent or keeps getting CLI commands wrong
- Asks to split a skill into script + prompt
- Wants to audit a skill for script extraction candidates

## Process

### Step 1: Read the skill

Read the target skill file. If the user doesn't specify one, ask which skill to review.

### Step 2: Classify each step

Go through every instruction in the skill and classify it:

- **Script** (S) — has one right answer, runs the same every time. Examples:
  - CLI commands with specific flags (`git log --since="1 week ago" --oneline`)
  - File creation with fixed paths or formats (`echo "# Title" > report.md`)
  - Data collection (`npm test 2>&1 | tail -20`)
  - Directory setup, file copying, environment checks
  - Any step where you could write it once and it works forever

- **AI** (A) — needs thinking, interpretation, or creativity. Examples:
  - Summarising collected data
  - Choosing between options
  - Writing prose, recommendations, analysis
  - Interpreting results or making judgment calls
  - Anything where the "right answer" depends on context

Present the classification to the user as a table:

```
| Step | Classification | Reason |
|------|---------------|--------|
| Run git log... | S (Script) | Exact command, one right answer |
| Summarise themes | A (AI) | Needs interpretation |
```

### Step 3: Write the script

Create a shell script that handles all the S-classified steps.

**All scripts MUST be location-independent.** They should work if someone pulls them to a different folder or a different computer. Follow these rules:

- Start with `#!/bin/bash`
- **Resolve the script's own directory first:**
  ```bash
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  ```
  Use `$SCRIPT_DIR` as the base for any relative paths (e.g., `"$SCRIPT_DIR/../data"`).
- **Never hardcode absolute paths.** No `/Users/jv/...`, no `~/specific-project/...`. Use `$SCRIPT_DIR`, `$PWD`, or accept paths as arguments.
- **Use `command -v` to check for required tools** before running them:
  ```bash
  command -v jq >/dev/null 2>&1 || { echo "Error: jq is required but not installed"; exit 1; }
  ```
- **Accept inputs as arguments or environment variables**, not baked-in values:
  ```bash
  INPUT_FILE="${1:?Usage: $0 <input-file>}"
  OUTPUT_DIR="${2:-$SCRIPT_DIR/output}"
  ```
- **Use `mktemp` for temporary files** instead of hardcoded `/tmp/my-thing.txt`:
  ```bash
  TMPFILE=$(mktemp)
  trap 'rm -f "$TMPFILE"' EXIT
  ```
- Add a comment at the top explaining what the script does
- End with a confirmation message (`echo "Done: output written to $OUTFILE"`)
- Make it executable: remind the user to run `chmod +x script.sh`

**Use parameters to make scripts resilient:**

- **Add `set -euo pipefail`** after the shebang. This makes the script fail fast on errors (`-e`), undefined variables (`-u`), and broken pipes (`-o pipefail`) instead of silently continuing with wrong data.
- **Provide sensible defaults for optional parameters** using `${VAR:-default}`:
  ```bash
  SINCE="${1:-7}"  # days to look back, defaults to 7
  FORMAT="${2:-oneline}"  # output format, defaults to oneline
  ```
- **Validate required parameters early** and print usage if missing:
  ```bash
  if [ $# -lt 1 ]; then
    echo "Usage: $0 <input-file> [output-dir]"
    echo "  input-file: path to the skill file to process"
    echo "  output-dir: where to write results (default: ./output)"
    exit 1
  fi
  ```
- **Validate that input files/dirs actually exist** before doing work:
  ```bash
  [ -f "$INPUT_FILE" ] || { echo "Error: $INPUT_FILE not found"; exit 1; }
  [ -d "$OUTPUT_DIR" ] || mkdir -p "$OUTPUT_DIR"
  ```
- **Use named variables instead of positional `$1`, `$2` in the body.** Assign arguments to descriptive names at the top, then use those names throughout. `$INPUT_FILE` is readable, `$1` buried on line 40 is not.
- **Make the script idempotent where possible.** Running it twice should produce the same result, not duplicate data or fail because output already exists. Use `mkdir -p` instead of `mkdir`, overwrite output files instead of appending blindly.

Place the script next to the skill file, or in a `scripts/` directory if there are multiple.

### Step 4: Rewrite the skill

Rewrite the skill to:
1. Call the script first (`Run ./script-name.sh`)
2. Read the script's output
3. Do only the judgment work with that output

The rewritten skill should be noticeably shorter. If it isn't, the original probably didn't have many mechanical steps and might not need this treatment — say so.

### Step 5: Optionally add AI calls to the script

If the workflow benefits from it, show how the script could call AI CLIs directly:

```bash
# Collect data deterministically, then ask AI to analyse
TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT
git log --since="1 week ago" --oneline > "$TMPFILE"
codex exec "Summarise the themes: $(cat "$TMPFILE")"
```

This makes the entire workflow runnable as a single script — deterministic orchestration with AI judgment on demand.

## Output Format

Produce three artifacts:

1. **Classification table** — every step labeled S or A with reasoning
2. **Shell script** — handles all S steps
3. **Rewritten skill** — calls the script, then does only A steps

## Tips

- Don't force it. If a skill is mostly judgment calls with one or two simple commands, it probably doesn't need a script. Say so.
- Scripts should be independently testable. The user should be able to run the script alone to verify the data collection works before involving the AI.
- Keep scripts focused. One script per logical phase. Don't create a mega-script that's as hard to debug as the original skill.
- Variable names should be descriptive. `$OUTFILE` and `$TODAY` are better than `$F` and `$D`.
- Always use `"$VARIABLE"` with quotes to handle spaces in paths.
- **Portability is non-negotiable.** Every script must work when moved to a different directory or cloned to a different machine. No hardcoded paths, no assumptions about home directory layout, no machine-specific values baked in. If the script needs something specific to the environment, it takes it as an argument or reads it from an env var.
