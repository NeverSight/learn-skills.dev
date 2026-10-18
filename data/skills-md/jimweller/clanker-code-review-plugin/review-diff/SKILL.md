---
name: review-diff
description: "Review every change on this branch against main across 9 perspectives, then review-deep's scripted collate, verify, and report chain over the same findings. Covers committed, staged, unstaged, and untracked work."
context: fork
disable-model-invocation: true
---

<!-- markdownlint-disable-file MD041 -->

STARTER_CHARACTER = ⚡

# Diff Review

Review everything that differs from `main` across 9 perspectives, each by one subagent. The nine areas' findings then run through the same scripted collate, merge, rank, and isolated-judge verification chain review-deep uses. No arguments.

Available on Claude Code (through this plugin) and Codex. Fails preflight by name on OpenCode and Hermes Agent, neither of which can dispatch a subagent to a named reviewer type.

This skill runs `context: fork`, dispatched as a subagent with no user present to answer a prompt. Never pause before dispatch to confirm scope, cost, or model spend; the diff is whatever it is.

## Step 1: Preflight

Determine your harness. In Claude Code, `HARNESS=claude` and `PLUGIN_ROOT` is this plugin's root, two directories up from this SKILL.md. In Codex, `HARNESS=codex`; `PLUGIN_ROOT` does not apply there, since the nine Codex reviewer agents live at a fixed path, not inside a plugin.

```bash
S="${CLAUDE_SKILL_DIR}/../review-deep/scripts"   # replace ${CLAUDE_SKILL_DIR} with this SKILL.md's own directory on a non-Claude harness
[ -f "$S/init_run.py" ] || { echo "scripts not found at $S"; exit 1; }
HARNESS=claude
PLUGIN_ROOT="$(cd "${CLAUDE_SKILL_DIR}/../.." && pwd)"

OUT=$(python3 "$S/preflight.py" --tier diff --harness "$HARNESS" --plugin-root "$PLUGIN_ROOT")
STATUS=$?
echo "$OUT"
[ "$STATUS" -eq 0 ] || exit 1
LABEL=$(echo "$OUT" | sed -n 's/^LABEL=//p')
AGENT_PREFIX=$(echo "$OUT" | sed -n 's/^AGENT_PREFIX=//p')
```

`preflight.py` checks every tool, agent file, and ref this skill needs (including that `origin/main` or `main` resolves), prints one `PASS` or `FAIL` line per check, and exits 1 on any `FAIL`. On success it also prints `LABEL` (the reviewer source name behind `$LABEL-<area>.md`) and `AGENT_PREFIX` (the namespace prefix for the nine subagent types; `clanker-code-review:` in Claude Code, empty in Codex). The `$S` guard catches a partial or corrupted plugin or skill install.

## Step 2: Resolve the Base

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel)

BASE_REF=$(git rev-parse --verify --quiet origin/main || git rev-parse --verify --quiet main)
if [ -z "$BASE_REF" ]; then
  echo "No main branch found (tried origin/main and main)"
  exit 1
fi

BASE=$(git merge-base HEAD "$BASE_REF")

# On main itself the merge base is HEAD, which would hide committed work.
# Fall back to the previous commit so the branch tip is still under review.
if [ "$BASE" = "$(git rev-parse HEAD)" ]; then
  BASE=$(git rev-parse --verify --quiet HEAD~1 || echo "$BASE")
fi

echo "BASE=$BASE"
```

## Step 3: Collect the Delta

```bash
git log --oneline "${BASE}"..HEAD
git diff "${BASE}" --find-renames --stat
git diff "${BASE}" --find-renames
git status --porcelain
git ls-files --others --exclude-standard
```

`git diff "$BASE"` carries no `..HEAD`, so it spans the merge base through the working tree. Committed, staged, and unstaged changes all land in one diff. `--find-renames` surfaces renames as `R<score>` entries with both paths so a pure rename does not collapse into an empty diff. `git status --porcelain` is the authoritative list of every modified, added, deleted, renamed, copied, and untracked entry. `ls-files --others` surfaces untracked files, which have no diff representation. Files matching `.gitignore` are excluded.

Stop when all five signals are empty (the commit log, the diffstat, the diff, the status, and the untracked list). Report `No changes against main` and stop.

## Step 4: Start the Run

```bash
python3 "$S/init_run.py" --kind diff --base "$BASE" "$PROJECT_ROOT" "$PROJECT_ROOT" "$PROJECT_ROOT/.llmtmp/review-diff"
```

Prints `RUN_DIR` and `COMMIT`. `RUN_DIR` is `${XDG_CACHE_HOME:-~/.cache}/review-diff/<repo>-<commit12>`, outside the repository. On a clean working tree `COMMIT` is HEAD. On a dirty one, `init_run.py` snapshots the working tree into an unreferenced commit over HEAD, so the reviewers, the `git diff` below, and the scripted chain's judges all see the exact same uncommitted edits. `run.json` carries `kind: diff`, `base: $BASE`, and `ticket_label: review-diff`.

## Step 5: Materialize the Input

Write the whole change set to one file. Reviewers hold `Read` but no `Bash`, so they cannot run git themselves. Passing the diff through nine prompts costs nine copies of it in orchestrator output; writing it once and having each reviewer read it costs one.

```bash
STATE_DIR="$PROJECT_ROOT/.llmtmp/review-diff"
mkdir -p "$STATE_DIR"
find "$STATE_DIR" -mindepth 1 -delete
INPUT="$STATE_DIR/input.md"

{
  echo "# Change set vs merge-base ${BASE}, reviewed at commit ${COMMIT}"
  echo; echo "## Commits"; git log --oneline "${BASE}"..HEAD
  echo; echo "## Status"; git status --porcelain
  echo; echo "## Diffstat"; git diff "${BASE}" "${COMMIT}" --find-renames --stat
  echo; echo "## Diff"; git diff "${BASE}" "${COMMIT}" --find-renames
} > "$INPUT"

for f in $(git ls-files --others --exclude-standard); do
  { echo; echo "## Untracked file: $f"; cat -n "$f"; } >> "$INPUT"
done

wc -c "$INPUT"
```

`git diff "$BASE" "$COMMIT"` replaces the old `git diff "$BASE"` against the working tree: reviewers must see exactly what the scripted chain's judges will later check out and verify, and `$COMMIT` (a snapshot when the tree is dirty, HEAD otherwise) is that same, fixed point. Untracked files carry no diff representation, so their full contents are appended with line numbers.

`mkdir -p` then `find -delete` rather than `rm -rf`. A `safe-rm` shim on `PATH` (as in some dotfiles setups) moves paths to Trash and exits non-zero on a missing path even under `-f`, which breaks the wipe on a first run.

## Step 6: Build the Ledger

```bash
python3 "$S/ledger.py" "$STATE_DIR" --diff "$PROJECT_ROOT" "$BASE" "$COMMIT"
python3 "$S/partition.py" "$STATE_DIR"
```

`ledger.py --diff` runs `git diff --name-only --no-renames --diff-filter=d` between `$BASE` and `$COMMIT`, so a rename gives its new path once and a deletion is dropped. The reviewers work from `$INPUT` directly, not from `partition.py`'s components; `report.py`'s coverage section is what actually reads them.

## Step 7: Dispatch 9 Reviewers in Parallel

Issue all 9 Agent calls **in a single tool block** with `run_in_background: false`.

Subagents default to running in the background. A backgrounded fan-out delivers its results in later turns, so Step 8 would find nothing to consolidate. Synchronous dispatch in one block is what makes the fleet parallel and the report possible in this turn.

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

Dispatch all 9 every run. Do not skip a perspective based on which files changed.

Every prompt is identical apart from nothing. Send this, with `<INPUT>` and `<PROJECT_ROOT>` substituted:

```text
Read <INPUT>. It holds the commit log, porcelain status, diffstat, full diff
against the merge-base with main, and the full contents of every untracked
file. That is the complete change set under review.

The project root is <PROJECT_ROOT>. Every path in the diff is relative to it.
Open any file you need in that tree to confirm a finding and to confirm the
line number you cite.

Audit this change set. Apply the Ownership table in your instructions: report
only defect classes you own, and stay silent on the rest.

Write your findings to <STATE_DIR>/<LABEL>-<area>.md. Use an H2 header
followed by findings or exactly "No findings."
```

The brief stays short on purpose. Severity, citation format, output shape, and lane discipline all live in the agent definitions, so one edit there changes every caller.

Do not pack repomix. The input file holds everything.

## Step 8: Check and Re-dispatch

```bash
python3 "$S/check_reviews.py" "$RUN_DIR" "$LABEL"
```

Prints one `PASS` or `FAIL` line per area and exits 1 when any fails: the file is missing, has no H2, has no finding and is not exactly `No findings.`, or holds a bullet that parses as neither `normalize.FULL` nor `normalize.BARE`. Two causes are common here: the agent died on a transient API error and wrote nothing, or a hook blocked its read of `$INPUT` and it wrote a refusal instead. Re-dispatch each failing area's agent once, using the same prompt as Step 7, then run `check_reviews.py` again. A second failure is reported as not reviewed in Step 9, not retried further.

Editing an agent definition does not affect a session already running. Claude Code detects agent files being added or removed, but a session keeps the body it loaded at startup, and a definition reached through a symlink (as dotbot installs them) is not re-read on edit. Restart the session after changing a reviewer.

## Step 9: Run the Scripted Chain and Report

Run each model stage as a background Bash call; its pool returns when every call has finished, and the completion notification is the signal to continue. Never poll a running stage with `sleep`. Run the stage command itself as the background call. Never detach it with `nohup` or a trailing `&`, and never wait on a log line with `tail -f | grep -m1`. `tail` exits only when it next writes, so the call hangs until its timeout once the log gets its last line.

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

A diff's scope is usually small enough to afford verifying Medium-severity issues too: pass `--floor Medium` to `verify.py` (`python3 "$S/verify.py" "$RUN_DIR" --floor Medium`) to widen it past the Critical/High default.

Report the counts from `report.md`, the confirmed issues, and `RUN_DIR` to the operator. The run directory is valid input to the review-tickets skill, with ticket label `review-diff`.

## Tests

See review-deep's Tests section. The same `evals/` at the root of this plugin's repository covers every skill here, including `unit/preflight` for this skill's preflight tier.
