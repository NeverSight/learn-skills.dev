---
name: review-full
description: Whole-codebase review by nine specialized reviewer agents against a repomix-packed snapshot, then review-deep's scripted collate, verify, and report chain over the same findings.
context: fork
disable-model-invocation: true
---

<!-- markdownlint-disable-file MD041 -->

STARTER_CHARACTER = 🔎

# Full Review

Review the entire codebase across 9 focus areas, each by one subagent reading a repomix-packed snapshot. The nine areas' findings then run through the same scripted collate, merge, rank, and isolated-judge verification chain review-deep uses, so a full review gets the same deduplication and Critical/High verification, not just a consolidated report.

Available on Claude Code (through this plugin) and Codex. Fails preflight by name on OpenCode and Hermes Agent, neither of which can dispatch a subagent to a named reviewer type.

## Arguments

If the user provided a path with the invocation, treat it as the target directory relative to the repo root. Otherwise pack the whole repo. That is the deliberate default, already accepted by whoever invoked this skill, not a decision to re-confirm.

This skill runs `context: fork`, dispatched as a subagent with no user present to answer a prompt. Never pause before dispatch to confirm scope, cost, or model spend. If cost matters, that call was made before invocation, by passing a narrower path.

## Step 1: Preflight

Determine your harness. In Claude Code, `HARNESS=claude` and `PLUGIN_ROOT` is this plugin's root, two directories up from this SKILL.md. In Codex, `HARNESS=codex`; `PLUGIN_ROOT` does not apply there, since the nine Codex reviewer agents live at a fixed path, not inside a plugin.

```bash
S="${CLAUDE_SKILL_DIR}/../review-deep/scripts"   # replace ${CLAUDE_SKILL_DIR} with this SKILL.md's own directory on a non-Claude harness
[ -f "$S/init_run.py" ] || { echo "scripts not found at $S"; exit 1; }
HARNESS=claude
PLUGIN_ROOT="$(cd "${CLAUDE_SKILL_DIR}/../.." && pwd)"

OUT=$(python3 "$S/preflight.py" --tier full --harness "$HARNESS" --plugin-root "$PLUGIN_ROOT")
STATUS=$?
echo "$OUT"
[ "$STATUS" -eq 0 ] || exit 1
LABEL=$(echo "$OUT" | sed -n 's/^LABEL=//p')
AGENT_PREFIX=$(echo "$OUT" | sed -n 's/^AGENT_PREFIX=//p')
```

`preflight.py` checks every tool, agent file, and MCP server this skill needs, prints one `PASS` or `FAIL` line per check, and exits 1 on any `FAIL`. On success it also prints `LABEL` (the reviewer source name behind `$LABEL-<area>.md`) and `AGENT_PREFIX` (the namespace prefix for the nine subagent types; `clanker-code-review:` in Claude Code, empty in Codex). The `$S` guard catches a partial or corrupted plugin or skill install.

## Step 2: Resolve Target and Prepare

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel)
PROJECT_ROOT=$(cd -P "$PROJECT_ROOT" && pwd -P)
TARGET_PATH="<user-provided path or empty>"
[ -z "$TARGET_PATH" ] && TARGET_PATH="$PROJECT_ROOT"

TARGET_PATH=$(cd -P "$TARGET_PATH" 2>/dev/null && pwd -P) || { echo "TARGET_PATH does not exist"; exit 1; }
case "$TARGET_PATH" in
  "$PROJECT_ROOT"|"$PROJECT_ROOT"/*) ;;
  *) echo "TARGET_PATH escapes PROJECT_ROOT"; exit 1 ;;
esac

TARGET_NAME=$(basename "$TARGET_PATH")
[ "$TARGET_PATH" = "$PROJECT_ROOT" ] && TARGET_NAME="repo"

STATE_DIR="$PROJECT_ROOT/.llmtmp/review-full"
mkdir -p "$STATE_DIR"
find "$STATE_DIR" -mindepth 1 -delete
```

`mkdir -p` then `find -delete` rather than `rm -rf`. A `safe-rm` shim on `PATH` (as in some dotfiles setups) moves paths to Trash and exits non-zero on a missing path even under `-f`, which breaks the wipe on a first run.

## Step 3: Start the Run

```bash
python3 "$S/init_run.py" --kind full "$PROJECT_ROOT" "$TARGET_PATH" "$STATE_DIR"
```

Prints `RUN_DIR` and `COMMIT`. `RUN_DIR` is `${XDG_CACHE_HOME:-~/.cache}/review-full/<repo>-<commit12>`, outside the repository. On a clean working tree `COMMIT` is HEAD. On a dirty one, `init_run.py` snapshots the working tree into an unreferenced commit over HEAD, so Step 7's judges read the same uncommitted edits the nine reviewers see in Step 5. `run.json` carries `kind: full` and `ticket_label: review-full`.

## Step 4: Pack and Build the Ledger

```bash
REPOMIX_FILE="$STATE_DIR/repomix.xml"
INCLUDE=""
[ "$TARGET_PATH" != "$PROJECT_ROOT" ] && INCLUDE="--include ${TARGET_PATH#"$PROJECT_ROOT"/}/**"
npx repomix -o "$REPOMIX_FILE" --quiet --output-show-line-numbers $INCLUDE "$PROJECT_ROOT"

python3 "$S/ledger.py" "$STATE_DIR" --repomix "$REPOMIX_FILE"
python3 "$S/partition.py" "$STATE_DIR"
```

Repomix reads `.repomixignore` from the project root automatically. `--include` is packed from the project root even for a subpath target, so paths in the output stay root-relative; confirm this on the first run against a subpath, since whether `--include` changes that is unverified.

`ledger.py --repomix` reads every `<file path>` entry out of the pack, so the ledger matches exactly what the reviewers can see. The reviewers work from the repomix pack directly, not from `partition.py`'s components; `report.py`'s coverage section is what actually reads them.

## Step 5: Attach and Dispatch

Call `attach_packed_output` with `filePath=REPOMIX_FILE`. Record the returned `outputId`.

Issue all 9 Agent calls **in a single tool block** with `run_in_background: false`. Subagents default to running in the background, and a backgrounded fan-out delivers its results in later turns, so Step 6 would verify files no agent has written yet.

| Agent type | Area |
| --- | --- |
| `${AGENT_PREFIX}reviewer-architecture` | architecture |
| `${AGENT_PREFIX}reviewer-correctness` | correctness |
| `${AGENT_PREFIX}reviewer-data` | data |
| `${AGENT_PREFIX}reviewer-ops` | ops |
| `${AGENT_PREFIX}reviewer-performance` | performance |
| `${AGENT_PREFIX}reviewer-quality` | quality |
| `${AGENT_PREFIX}reviewer-security` | security |
| `${AGENT_PREFIX}reviewer-solid` | solid |
| `${AGENT_PREFIX}reviewer-testing` | testing |

Each prompt contains:

1. The `outputId` from this step.
2. Instruction to use `read_repomix_output` and `grep_repomix_output` for navigation.
3. Instruction: "Read AGENTS.md (or CLAUDE.md) and .llmdocs/architecture.md (if present) via the repomix output for project context."
4. Instruction: "Write findings to `$STATE_DIR/$LABEL-<area>.md`. Use an H2 header followed by findings or exactly `No findings.`"

## Step 6: Check and Re-dispatch

```bash
python3 "$S/check_reviews.py" "$RUN_DIR" "$LABEL"
```

Prints one `PASS` or `FAIL` line per area and exits 1 when any fails: the file is missing, has no H2, has no finding and is not exactly `No findings.`, or holds a bullet that parses as neither `normalize.FULL` nor `normalize.BARE`. Re-dispatch each failing area's agent once, using the same prompt as Step 5, then run `check_reviews.py` again. A second failure is reported as not reviewed in Step 8, not retried further.

## Step 7: Run the Scripted Chain

Run the same chain review-deep's Step 5 does, over this run's `RUN_DIR`. Run each model stage as a background Bash call; its pool returns when every call has finished, and the completion notification is the signal to continue. Never poll a running stage with `sleep`. Run the stage command itself as the background call. Never detach it with `nohup` or a trailing `&`, and never wait on a log line with `tail -f | grep -m1`. `tail` exits only when it next writes, so the call hangs until its timeout once the log gets its last line.

```bash
python3 "$S/checkout.py" "$RUN_DIR"
python3 "$S/normalize.py" "$RUN_DIR"
python3 "$S/collate.py" "$RUN_DIR"         # one model call per component, background
uv run --with scikit-learn --with scipy --with numpy python "$S/windows.py" "$RUN_DIR"
python3 "$S/merge.py" "$RUN_DIR"           # one model call per similarity window, background
python3 "$S/rank.py" "$RUN_DIR"
python3 "$S/verify.py" "$RUN_DIR"          # one model call per Critical or High issue, background
python3 "$S/report.py" "$RUN_DIR"
```

See review-deep's Step 5 for what each stage does and how every model call is run and checked; nothing here differs by kind except `report.py`'s header and coverage section.

## Step 8: Report

Report the counts from `report.md`, the confirmed Critical and High issues, and `RUN_DIR` to the operator. The run directory is valid input to the review-tickets skill, with ticket label `review-full`.

## Tests

See review-deep's Tests section. The same `evals/` at the root of this plugin's repository covers every skill here, including `unit/preflight` for this skill's preflight tier.
