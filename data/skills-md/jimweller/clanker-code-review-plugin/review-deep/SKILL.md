---
name: review-deep
description: Whole-codebase deep audit. Partitions the repo into 25-file components, runs 9 perspectives by 3 models (OpenAI, Gemini, Claude) on every component via opencode run with Serena navigation, sweeps for gaps, and runs one ocr scan coverage pass. Then collates and deduplicates the findings and verifies every Critical and High issue against a clean export of the reviewed commit with isolated claude -p judges. The run directory feeds the review-tickets skill.
context: fork
disable-model-invocation: true
---

<!-- markdownlint-disable-file MD041 -->

STARTER_CHARACTER = 🕵️‍♂️

# Code Review Command

Review a codebase from 9 perspectives against 3 models. The repo is cut into components of at most 25 files, and each of the 27 perspective and model pairs reviews every component, so every file gets all 27 reviews. Each arm is its own `opencode run` process that works in its own copy of the reviewed commit, navigates it with Serena, and writes its own findings. A sweep per pair then looks for defects the component boundaries hid.

Nothing is packed. There is no orchestrator process and no `task` fan-out. A reviewer reads the files of the reviewed commit, so a citation points at a real line in a real file. No reviewer reads the live repository.

One `ocr scan` runs alongside them. It reviews every reviewable file in its own conversation with a generic checklist, which makes it an independent fourth source.

## Arguments

If the user provided a path with the invocation, treat it as the target directory relative to the repo root. Otherwise review the whole repo. That is the deliberate default, already accepted by whoever invoked this skill, not a decision to re-confirm.

This skill runs `context: fork`, dispatched as a subagent with no user present to answer a prompt. Never pause before Step 2 to confirm scope, cost, or model spend. Proceed straight through Step 1 into dispatch. If cost matters, that call was made before invocation, by passing a narrower path.

## Models

| Label  | Model ID                     | Variant |
| ------ | ---------------------------- | ------- |
| openai | openai/gpt-6-sol             |         |
| gemini | google/gemini-3.8-flash      |         |
| claude | az-anthropic/claude-opus-5-5 | xhigh   |

The ocr coverage pass uses the provider and model in `~/.opencodereview/config.json`.

Every ID must exist in `~/.config/opencode/opencode.json` under the matching provider and in that provider's `whitelist`. An ID missing from either fails that arm with `Model not found`, which surfaces only as an `error` event in the NDJSON.

```bash
jq -r '.provider | to_entries[] | .key as $p | .value.models | keys[] | "\($p)/\(.)"' ~/.config/opencode/opencode.json
```

The gemini arm runs a Flash model on purpose. Google publishes no pro above `gemini-3.1-pro-preview`, so the newest Google model available is `gemini-3.8-flash`, seven minor versions ahead of the newest pro. Measured on one security review of a 1070-file repo, flash returned 11 findings against pro's 6 on the same agent and prompt, at roughly twice the tokens. That is a single comparison, not a benchmark.

## The rule that cost two days to learn

Redirect stdin from `/dev/null` on every `opencode run`. Without it the process blocks before creating a session, writes zero bytes, logs nothing past `message=init`, and exits only when something kills it. `opencode run` reads stdin to EOF before it does anything else, so any launcher that leaves stdin open hangs it, and a background job, a CI step, and an agent harness all do. This is anomalyco/opencode issue #38723, open against 1.18.25 and reproduced here on 1.18.20.

The hang looks intermittent and is not. Whether the launcher closes stdin decides it. Three reporters measured it deterministically across macOS arm64, Linux aarch64, and Windows, 5 of 5 hangs without the redirect against 5 to 10 of 10 successes with it.

An earlier version of this file banned wrapping `opencode run` in `timeout` and blamed a 44 percent failure rate on the wrapper. That was wrong. The stall reproduces with no `timeout` anywhere, and upstream's own reproduction script uses `timeout 120`. Removing every bound is what turned a one-line stdin bug into a multi-day investigation, so Step 2b now checks each reviewer for a session row.

Impose no token cap and no turn cap on a reviewer. A review of a large repo takes as long as it takes.

Serena is the only MCP server the arms get. Step 1's `opencode_env.py` starts it with `--project-from-cwd`, and `--dir` points at the target so Serena's walk finds the project. Serena reads its settings from `SERENA_HOME`, `~/.serena-reviewer` by default, which holds its `serena_config.yml` and downloaded language servers.

### Why researcher is disabled

The arms never load the operator's MCP servers, so `researcher` cannot reach them. It is worth knowing why it once broke them: Google rejects its schemas.

`researcher` declares optional arrays as the union type `["null","array"]`, which is valid JSON Schema. Anthropic and OpenAI accept it. Google converts JSON Schema into its own OpenAPI-subset proto, turns the union into `any_of`, drops `items` from the array branch, then rejects its own output with `any_of[0].items: missing field`. The gemini arm fails in 5 seconds with one `error` event and 5712 bytes of NDJSON.

Any MCP server using that pattern breaks a Google arm the same way. If a gemini arm starts failing with `field predicate failed: $type == Type.ARRAY`, find the server owning the named properties and disable it.

## Procedure

### Step 1: Resolve Target and Prepare

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

S="${CLAUDE_SKILL_DIR}/scripts"   # replace ${CLAUDE_SKILL_DIR} with this SKILL.md's own directory on a non-Claude harness
[ -f "$S/init_run.py" ] || { echo "scripts not found at $S"; exit 1; }
python3 "$S/preflight.py" --tier deep || exit 1

STATE_DIR="$PROJECT_ROOT/.llmtmp/review-deep"
mkdir -p "$STATE_DIR"
find "$STATE_DIR" -mindepth 1 -delete
mkdir -p "$STATE_DIR/components" "$STATE_DIR/coverage" "$STATE_DIR/parts"

INIT=$(python3 "$S/init_run.py" "$PROJECT_ROOT" "$TARGET_PATH" "$STATE_DIR") || exit 1
echo "$INIT"
RUN_DIR=$(printf '%s\n' "$INIT" | sed -n 's/^RUN_DIR=//p')
EXPORT=$(python3 "$S/export.py" "$RUN_DIR" | sed -n 's/^EXPORT=//p')
[ -d "$EXPORT" ] || { echo "export.py made no export"; exit 1; }

SCOPE=""
[ "$TARGET_PATH" != "$PROJECT_ROOT" ] && SCOPE="--path ${TARGET_PATH#"$PROJECT_ROOT"/}"
ocr scan --preview --format json --repo "$EXPORT" $SCOPE 2>/dev/null > "$STATE_DIR/ocr-preview.json"
jq -r '.files[] | select(.will_review) | .path' "$STATE_DIR/ocr-preview.json" > "$STATE_DIR/ledger.txt"
jq -r '.files[] | select(.will_review | not) | "\(.path)\t\(.exclude_reason)"' "$STATE_DIR/ocr-preview.json" > "$STATE_DIR/skipped.txt"

python3 "$S/partition.py" "$STATE_DIR"
python3 "$S/opencode_env.py" "$STATE_DIR" || exit 1

echo "PROJECT_ROOT=$PROJECT_ROOT"
echo "TARGET_PATH=$TARGET_PATH"
echo "TARGET_NAME=$TARGET_NAME"
echo "STATE_DIR=$STATE_DIR"
echo "EXPORT=$EXPORT"
echo "LEDGER=$(wc -l < "$STATE_DIR/ledger.txt" | tr -d ' ') reviewable, $(wc -l < "$STATE_DIR/skipped.txt" | tr -d ' ') skipped"
```

`preflight.py --tier deep` checks every tool, config file, model whitelist entry, and provider key this skill needs before anything is wiped, and fails loudly by name rather than partway through a run. The `$S` guard catches a partial or corrupted plugin install the same way.

`init_run.py` records the reviewed commit, HEAD at this moment, and creates the run directory at `${XDG_CACHE_HOME:-~/.cache}/review-deep/<repo>-<commit12>`, outside the repository. It prints `RUN_DIR`, and Step 5 uses it. It warns when the working tree has uncommitted changes, because every reviewer and judge reads the commit, so uncommitted changes go unreviewed. Commit first when the warning lists source files. `run.json` in the run directory holds the models, the concurrency, the files a judge must not see, and the commit sentence tickets carry. Edit it before Step 5 to change any of them.

`export.py` exports the reviewed commit with `git archive` into a new temporary directory, deletes every name in `run.json` `judge_exclude` at any depth, such as `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.opencode/`, and `.llmdocs/`, and commits the result as a one-commit repository of its own, so opencode, Serena, and ocr find their project root there. Every arm reviews its own `cp -R` copy of it, and the ocr scan reviews another. The live repository is never read by a model and never modified. Measured on a 1179-file repository, the export took 0.6 s and 12 MB, so 27 concurrent copies hold about 324 MB.

`ocr scan --preview` runs on the export and lists every file without calling a model, so the ledger matches exactly what the arms can see. `ledger.txt` holds the reviewable ones. `skipped.txt` holds the rest with ocr's reason, such as `binary` or `unsupported_ext`, and Step 5 reports it as the skipped ledger.

`partition.py` cuts the ledger into components of at most 25 files along directory lines, the size Anthropic's Claude Security scanner uses. A reviewer given the whole repo stops after 40 to 50 files by its own choice. Given a component, it reviews every file. A 41-file repo yields 1 component and a 414-file repo yields 22.

`opencode_env.py` writes the only opencode config the arms read, `$STATE_DIR/opencode-config/opencode/opencode.json`. It copies `provider` and `enabled_providers` from `~/.config/opencode/opencode.json` and adds Serena as the one MCP server, with this plugin's reviewer context and manual under `opencode/serena/`. It also adds nine primary agents whose prompts are the bodies of the plugin's `agents/reviewer-<area>.md`, the same text review-full and review-diff give their Claude reviewers. Each agent may read, search, use Serena's read tools, and write only under `$STATE_DIR/parts` and `$STATE_DIR/coverage`. No skill, subagent, shell, or web tool.

`find -delete` rather than `rm -f`. A `safe-rm` shim on `PATH` moves paths to Trash and exits non-zero on a missing path even under `-f`, which breaks the wipe on a first run.

### Step 2: Dispatch Component Reviewers and the Coverage Pass

Each of the 27 area and model pairs reviews every component, so a run has 27 arms per component. A worker pool runs them `CONCURRENCY` at a time, beside one ocr scan. Substitute the values Step 1 printed.

Run this block as one background Bash call, as written. The call stays open until the pool and the ocr scan exit, and its completion notification is the signal that Step 2 has finished. Never launch the block with `nohup`, a trailing `&`, or a wrapper script started in the background, because the call then returns at once and no notification ever comes. Never watch a log for the `done,` line. On a quartermaster run the agent detached the block and waited with `tail -f | grep -m1 '^done,'`. `grep` exited on the match, but `tail` exits only when it next writes, and `done,` is the last line the log gets. The call sat idle until its 60-minute `timeout` killed `tail`.

```bash
export PROJECT_ROOT TARGET_PATH STATE_DIR EXPORT
AREAS="security architecture solid correctness testing ops performance quality data"
MODELS="openai:openai/gpt-6-sol gemini:google/gemini-3.8-flash claude:az-anthropic/claude-opus-5-5"
CONCURRENCY=27

cat > "$STATE_DIR/arm.sh" <<'ARM'
#!/bin/bash
label=$1 model=$2 area=$3 comp=$4
if [ ! -d "$STATE_DIR/parts" ] || [ ! -d "$TARGET_PATH" ] || [ ! -d "$PROJECT_ROOT" ] || [ ! -d "$EXPORT" ]; then
  echo "arm.sh: STATE_DIR='$STATE_DIR' TARGET_PATH='$TARGET_PATH' PROJECT_ROOT='$PROJECT_ROOT' EXPORT='$EXPORT'. Export all four with the values Step 1 printed." >&2
  exit 255
fi
VARIANT=""
[ "$label" = claude ] && VARIANT="--variant xhigh"
base="$label-$area-$comp"
arm_dir=$(mktemp -d "${TMPDIR:-/tmp}/review-deep-arm.XXXXXX")
trap 'rm -rf "$arm_dir"' EXIT
copy="$(cd -P "$arm_dir" && pwd -P)/repo"
cp -R "$EXPORT" "$copy"
work="$copy/.review-arm"
mkdir -p "$work" "$STATE_DIR/arms"
echo "$copy" > "$STATE_DIR/arms/$base.root"
target="$copy${TARGET_PATH#"$PROJECT_ROOT"}"
if [ "$comp" = sweep ]; then
  cp "$STATE_DIR/ledger.txt" "$work/ledger.txt"
  cp "$STATE_DIR/$label-$area.md" "$work/listed-findings.md"
  scope="LEDGER_PATH: $work/ledger.txt
FINDINGS_PATH: $work/listed-findings.md

LEDGER_PATH lists every reviewable source file. A component-by-component
review already covered them, and its findings are in FINDINGS_PATH. Look only
for defects that are not already listed there, especially defects that span
components. Do not repeat a listed finding."
else
  cp "$STATE_DIR/components/$comp.txt" "$work/ledger.txt"
  scope="LEDGER_PATH: $work/ledger.txt
COVERAGE_PATH: $work/coverage.txt

LEDGER_PATH lists the source files assigned to you, one path per line,
relative to $copy. Read it first and review every file it lists. The rest of
the repository is context: follow calls into it, and report defects in the
listed files.

For every path in LEDGER_PATH, write one line to COVERAGE_PATH: the path, then
reviewed or skipped, then a short reason. Every listed path must appear
exactly once before you finish."
fi
prompt="Review the source files under $target that your ledger assigns.

Navigate with serena symbolic tools: get_symbols_overview to map a file,
find_symbol to read a definition, find_referencing_symbols to find callers,
find_declaration and find_implementations to resolve a usage. Read a whole
file only when symbolic navigation cannot answer the question. Everything
you need is under $copy.

Cite path:line with the path relative to $copy, and name the enclosing
function, method, or type. A line you saw counts as verified, and find_symbol
returns a symbol's line range. When you cannot verify the exact line, cite the
nearest line you saw and end the finding with \`line unconfirmed\`. Never drop
a real defect because its line number is uncertain.

$scope

OUTPUT_PATH: $work/findings.md

Write your findings to OUTPUT_PATH. Writing that file is mandatory and is
how your work is delivered. Do not return findings as your response."
raw="$STATE_DIR/parts/raw-$base.ndjson"
wrote_findings() {
  [ -s "$work/findings.md" ] ||
    jq -r 'select(.type=="text") | .part.text' "$raw" 2>/dev/null | grep -q '^## '
}
mkdir -p "$STATE_DIR/opencode-db" "$STATE_DIR/parts/attempts"
attempt=1
max_attempts=3
while :; do
  XDG_CONFIG_HOME="$STATE_DIR/opencode-config" \
  OPENCODE_PURE=1 \
  OPENCODE_DISABLE_EXTERNAL_SKILLS=1 \
  OPENCODE_DISABLE_CLAUDE_CODE=1 \
  OPENCODE_DISABLE_PROJECT_CONFIG=1 \
  OPENCODE_DISABLE_AUTOUPDATE=1 \
  OPENCODE_DB="$STATE_DIR/opencode-db/$base.db" \
  opencode run \
    --agent "reviewer-$area" \
    -m "$model" $VARIANT \
    --format json \
    --dir "$target" \
    --title "Review $label $area $comp" \
    "$prompt" \
    < /dev/null \
    > "$raw" 2> "$STATE_DIR/parts/$base.log"

  if wrote_findings && ! grep -q '"Failed to execute statement"' "$raw" 2>/dev/null; then break; fi
  [ "$attempt" -ge "$max_attempts" ] && break
  mv "$raw" "$STATE_DIR/parts/attempts/raw-$base.attempt$attempt.ndjson"
  sleep $((5 + RANDOM % 15))
  attempt=$((attempt + 1))
done
[ -s "$work/findings.md" ] && sed "s|$copy/||g" "$work/findings.md" > "$STATE_DIR/parts/$base.md"
[ -s "$work/coverage.txt" ] && sed "s|$copy/||g" "$work/coverage.txt" > "$STATE_DIR/coverage/$base.txt"
wrote_findings || { echo "arm.sh: $base wrote no findings in $attempt attempts" >&2; exit 1; }
ARM

: > "$STATE_DIR/tasks.txt"
for comp in $(ls "$STATE_DIR/components" | sed 's/\.txt$//'); do
  for entry in $MODELS; do
    for area in $AREAS; do
      echo "${entry%%:*} ${entry#*:} $area $comp" >> "$STATE_DIR/tasks.txt"
    done
  done
done

SCOPE=""
[ "$TARGET_PATH" != "$PROJECT_ROOT" ] && SCOPE="--path ${TARGET_PATH#"$PROJECT_ROOT"/}"
OCR_COPY="$(mktemp -d "${TMPDIR:-/tmp}/review-deep-ocr.XXXXXX")/repo"
cp -R "$EXPORT" "$OCR_COPY"
ocr scan --audience agent --repo "$OCR_COPY" $SCOPE --max-tokens 1000000 \
  --format json --output "$STATE_DIR/ocr-scan.json" \
  < /dev/null > /dev/null 2> "$STATE_DIR/ocr-scan.log" &
echo $! > "$STATE_DIR/ocr.pid"

echo "dispatching $(wc -l < "$STATE_DIR/tasks.txt" | tr -d ' ') arms, $CONCURRENCY at a time, plus 1 ocr scan"
xargs -P "$CONCURRENCY" -L 1 bash "$STATE_DIR/arm.sh" < "$STATE_DIR/tasks.txt"
wait
rm -rf "$(dirname "$OCR_COPY")"
echo "done, $(ls "$STATE_DIR"/parts/*.md 2>/dev/null | wc -l | tr -d ' ') part files written"
```

`xargs -P` is a rolling pool over the flat task list in `tasks.txt`, not a lockstep batch per component: as soon as any of the 27 slots frees, the next task in the list starts, whatever component it belongs to. Arms from c03 commonly start while c01 arms are still running. Do not report a wave count or a component-by-component ETA; measure actual throughput instead, from `parts/*.md` written per minute of elapsed time, and project the remainder from that rate.

`CONCURRENCY=27` holds 27 `opencode` processes at once, which a 48 GB machine carried without trouble. Each held 370 to 800 MB.

Reviewers run as an appliance. `XDG_CONFIG_HOME` points opencode at the config Step 1 generated, so none of the operator's opencode agents, skills, rules, plugins, or MCP servers load. Credentials still resolve, because opencode keeps `auth.json` under `XDG_DATA_HOME` and providers read keys from environment variables. `OPENCODE_PURE=1` skips external plugins, `OPENCODE_DISABLE_EXTERNAL_SKILLS=1` skips the skill scans under `~/.claude` and `~/.agents`, `OPENCODE_DISABLE_CLAUDE_CODE=1` skips `~/.claude/CLAUDE.md` and `.claude/skills`, and `OPENCODE_DISABLE_PROJECT_CONFIG=1` skips the reviewed repo's `opencode.json`, `.opencode/`, and `AGENTS.md`. Each was measured against opencode 1.18.20 with `opencode debug config`, `opencode debug skill`, and a planted instruction the model was asked to find.

Each arm runs in a copy of the export under `$TMPDIR/review-deep-arm.*`, with `--dir` inside it. `arm.sh` puts the arm's ledger, and for a sweep that area's merged findings, in the copy's `.review-arm/`. The arm writes its findings and coverage record there with `write`, or `apply_patch` on an OpenAI model. `arm.sh` copies them to `parts/` and `coverage/`, strips the copy's path from citations, and deletes the copy on exit. The generated agents deny every tool and then allow `read`, `grep`, `glob`, the write tools, and Serena minus its four write families. One shared `external_directory` rule denies every path outside the arm's own copy, and an `edit` rule allows writes only under `.review-arm/`. Measured on opencode 1.18.20: `grep` given an absolute path outside the copy, `glob`, and `read` were refused, and `grep` inside the copy worked.

Serena runs as its own process, so opencode's rules do not reach it. Measured on Serena 1.7.0: it refused a relative path that leaves the copy and an absolute directory path, but `find_symbol`, `get_symbols_overview`, and `get_diagnostics_for_file` answered for an absolute file path outside the copy. An arm that knows or guesses a file path elsewhere on the machine can still read that file's symbols through Serena. It resolved a `go.work` module inside the copy, across the module boundary. They run as `mode: primary`, because opencode ignores a subagent's `tools` block when the agent is selected with `--agent`.

A reviewer must not call `task`. Two of 27 reviewers on a 1070-file repo spawned a subagent that never returned, and `TaskTool` runs a foreground subagent with a blocking `yield`, so the parent hung and Step 2's `wait` hung with it. The agents set `tools.task: false` and `permission.task: {"*": deny}`. After the fix both reviewers completed with zero `task` calls.

Nothing guards against two runs at once. Step 1 wipes `STATE_DIR` and every arm writes to fixed paths, so a second invocation against the same repo destroys the first. Check for an in-flight run before dispatching.

Provider limits are not the constraint. OpenAI reports 40,000,000 tokens per minute and Azure Foundry 15,000,000.

opencode's own session store can die under write pressure at `CONCURRENCY=27`. Measured on a 1217-file repo: 26 arms failed in one four-second burst with `error="Failed to execute statement"` against opencode's shared SQLite store (visible in `~/.local/share/opencode/log/opencode.log`, not in the arm's own stderr, which stays empty). 25 of the 26 wrote no output at all. Confirmed upstream (anomalyco/opencode#48416, #47566, #38849, #33320, #21215): opencode's SQLite connection runs `busy_timeout=0`, so a writer that loses the race for the write lock fails immediately instead of waiting, and `Effect.orDie` on the SQL adapter turns that into a fatal message failure instead of a warning. The failing write fires from a `child_process` exit handler right after any concurrent process's tool call returns, so it tracks how many opencode processes are alive and busy at that moment, not which ones just launched.

`arm.sh` gives each arm its own database instead of racing on the shared one: `OPENCODE_DB="$STATE_DIR/opencode-db/$base.db"` (confirmed by reading opencode's own source: `OPENCODE_DB` is checked directly and, given an absolute path, used as the SQLite file with no further resolution against the shared data dir). This is the actual fix, not a workaround; a run this size no longer touches `~/.local/share/opencode/opencode.db` at all, and the write-contention failure has nothing left to contend over. `auth.json`, the provider credentials, and the downloaded tool cache under `bin/` are untouched, since only the DB path changes.

The retry loop re-runs the same `opencode run` invocation up to twice more in two cases. The first is a `grep` match for `"Failed to execute statement"` in the arm's NDJSON, kept as defense in depth for whatever the per-arm database leaves uncovered. The second is an arm that ends with no findings, meaning `OUTPUT_PATH` is empty and no text event carries a `## ` heading. Measured on a 718-file repo, 20 of 351 gemini arms read files, made no write call, and ended on a `stop` step with 0 output tokens. None of the 331 gemini arms that wrote findings ended that way. Attempts are separated by 5 to 19 seconds of jittered sleep so retries don't restack into the same contention window. A superseded attempt's NDJSON moves to `parts/attempts/raw-$base.attemptN.ndjson` and is never deleted. That directory sits outside the `parts/raw-*.ndjson` glob Step 3 extracts from. An arm with no findings after 3 attempts exits 1 with its name on stderr and surfaces as an ordinary `MISSING` entry in Step 3.

`arm.sh` exits 255 when `STATE_DIR`, `TARGET_PATH`, `PROJECT_ROOT`, or `EXPORT` is unset or names a missing directory. `xargs` stops launching arms after an exit of 255, so a batch dispatched from a shell that never exported them fails on its first arms instead of reporting success. Shell variables do not carry between Bash calls, so every call that runs `arm.sh` exports all four. One retry batch ran all 20 of its arms with an empty `STATE_DIR`. Each arm failed on `mkdir: /opencode-db: Read-only file system`, and the batch still exited 0.

### Step 2b: Confirm Arms Start

Run this as a separate foreground call while Step 2 is still waiting. An arm that never created a session wrote nothing and never will, and it holds a pool slot.

```bash
find "$STATE_DIR/parts" -maxdepth 1 -name 'raw-*.ndjson' -size 0 -mmin +1 | sed 's|.*/raw-||; s|\.ndjson$||; s/^/NO SESSION /'
```

A healthy arm writes NDJSON within seconds of launch. Kill any arm named here. Step 3 re-dispatches it.

Check the ocr scan the same way, using the PID Step 2 saved. It runs as `node`, not `ocr`, so `pgrep -x ocr` or an `ocr scan` name match never finds it; a process check with no result was misreported once as "the ocr scan has exited" when it was still running.

```bash
OCR_PID=$(cat "$STATE_DIR/ocr.pid" 2>/dev/null)
if [ -n "$OCR_PID" ] && kill -0 "$OCR_PID" 2>/dev/null; then
  echo "ocr scan running, pid $OCR_PID, log last wrote $(stat -f '%Sm' "$STATE_DIR/ocr-scan.log" 2>/dev/null)"
else
  echo "ocr scan not running and $STATE_DIR/ocr-scan.json is $([ -s "$STATE_DIR/ocr-scan.json" ] && echo present || echo MISSING)"
fi
```

A stale log with no growing output for several minutes is not proof of a hang; the tool only logs warnings and failed tool calls, so silence during successful work is normal. Measured on a 1217-file repo: the log went quiet for roughly 40 minutes, then wrote nothing further and exited clean about 80 minutes after launch, with `ocr-scan.json` present and `status=success` (719 files reviewed, 2586 findings). Tens of minutes of silence on a repo that size is the expected shape of a healthy run, not a symptom. Absence from `ps` (`kill -0` fails) together with a missing `ocr-scan.json` is proof it is dead. Re-launch only in that case, with the same command from Step 2, against the same `$STATE_DIR/ocr-scan.json` path.

### Step 3: Collect and Verify

An arm sometimes returns its findings as its response instead of writing OUTPUT_PATH. `gpt-6-sol` does this. The findings are in the NDJSON, so copy them out first. An arm with nothing to copy is left with no part file, so a `MISSING` check and a file count agree. Then merge each area and model's parts into one file.

The merge rebuilds each merged file from scratch out of the component parts and, once Step 4 has run, that area's sweep part. Running it again at any point gives the same result, so a re-dispatch after the sweep keeps the sweep's findings.

```bash
for f in "$STATE_DIR"/parts/raw-*.ndjson; do
  b=$(basename "$f" .ndjson); out="$STATE_DIR/parts/${b#raw-}.md"
  [ -s "$out" ] && continue
  jq -r 'select(.type=="text") | .part.text' "$f" | awk '/^## /{p=1} p' | sed -E 's#[^ `]*/review-deep-arm\.[^/ ]+/repo/##g' > "$out"
  [ -s "$out" ] || rm -f "$out"
done

for label in openai gemini claude; do
  for area in security architecture solid correctness testing ops performance quality data; do
    out="$STATE_DIR/$label-$area.md"
    parts=$(ls "$STATE_DIR"/parts/"$label-$area"-c*.md "$STATE_DIR"/parts/"$label-$area"-sweep.md 2>/dev/null)
    [ -z "$parts" ] && continue
    { grep -h -m1 '^## ' $parts | head -1; echo; grep -h '^- \*\*' $parts; } > "$out"
    grep -q '^- \*\*' "$out" || echo "No findings." >> "$out"
    for c in "$STATE_DIR"/components/*.txt; do
      comp=$(basename "$c" .txt)
      [ -s "$STATE_DIR/parts/$label-$area-$comp.md" ] || echo "MISSING $label $area $comp"
    done
  done
done
```

```bash
for label in openai gemini claude; do
  echo "== $label =="
  for area in security architecture solid correctness testing ops performance quality data; do
    f="$STATE_DIR/$label-$area.md"
    if [ ! -s "$f" ]; then
      echo "  $area MISSING"
    else
      n=$(grep -c '^- \*\*' "$f")
      cited=$(grep -oE '^- \*\*(Critical|High|Medium|Low)\*\* `[^`]+`' "$f" | grep -c ':[0-9]')
      unconf=$(grep -c 'line unconfirmed' "$f")
      echo "  $area ok findings=$n cited=$cited unconfirmed=$unconf"
    fi
  done
done
```

Then check coverage. Each arm's coverage record says which of its files it reviewed. The opened-files count checks the records against what arms actually read.

```bash
total=$(wc -l < "$STATE_DIR/ledger.txt" | tr -d ' ')
while read -r label model area comp; do
  f="$STATE_DIR/coverage/$label-$area-$comp.txt"
  want=$(wc -l < "$STATE_DIR/components/$comp.txt" | tr -d ' ')
  got=$(awk '$2 ~ /^reviewed/' "$f" 2>/dev/null | wc -l | tr -d ' ')
  [ "$got" -lt "$want" ] && echo "SHORT $label $area $comp reviewed=$got of $want"
done < "$STATE_DIR/tasks.txt"
cat "$STATE_DIR"/coverage/*.txt 2>/dev/null | awk '$2 ~ /^reviewed/ {print $1}' | sort -u > "$STATE_DIR/reviewed.txt"
echo "ledger files reviewed by at least one arm=$(comm -12 <(sort "$STATE_DIR/ledger.txt") "$STATE_DIR/reviewed.txt" | wc -l | tr -d ' ') of $total"
comm -23 <(sort "$STATE_DIR/ledger.txt") "$STATE_DIR/reviewed.txt" | sed 's/^/  never reviewed: /'
jq -r 'select(.type=="tool_use") | .part.state.input | (.filePath // .relative_path // .path // empty)' \
  "$STATE_DIR"/parts/raw-*.ndjson 2>/dev/null | sed -E 's#^.*/review-deep-arm\.[^/]+/repo/##' | sort -u > "$STATE_DIR/opened.txt"
echo "ledger files opened=$(comm -12 <(sort "$STATE_DIR/ledger.txt") "$STATE_DIR/opened.txt" | wc -l | tr -d ' ') of $total"
if [ -s "$STATE_DIR/ocr-scan.json" ]; then
  jq -r '"ocr status=\(.status) files=\(.summary.files_reviewed) findings=\(.comments|length)"' "$STATE_DIR/ocr-scan.json"
else
  echo "ocr-scan.json MISSING, run the Step 2b ocr liveness check before treating this as a dead scan"
fi
```

A `SHORT` line is an arm that marked some of its component `skipped` or wrote no coverage record. Read its reasons in the coverage record. A skip because the file belongs to another area is fine. A skip for lack of depth is a gap.

Re-dispatch a `MISSING` arm from a shell that exports the values Step 1 printed, then rerun the extract-and-merge block above. `arm.sh` already retried the arm twice, so re-dispatch it once.

```bash
export PROJECT_ROOT=<PROJECT_ROOT> TARGET_PATH=<TARGET_PATH> STATE_DIR=<STATE_DIR> EXPORT=<EXPORT>
bash "$STATE_DIR/arm.sh" <label> <model> <area> <comp>
```

Treat an area as unreviewed when its merged file is missing, or has neither a finding line nor exactly `No findings.` Never record either as `No findings.` Report every arm still missing after one retry to the operator as not reviewed, naming the model, area, and component.

Compare `cited` against `findings`. A finding whose first backticked field carries no `:line` is unusable, because nobody can confirm it without re-reading the whole file. `cited` counts a finding carrying a `path:line` whether or not it ends with `line unconfirmed`, so subtract `unconfirmed` for the count the reviewer stands behind. Read uncited findings before re-dispatching, and re-dispatch only when they carry no symbol either.

### Step 4: Sweep

One sweep arm per area and model gets the whole ledger and that area's merged findings, and looks only for defects not already listed. It catches what a component boundary hid.

```bash
: > "$STATE_DIR/sweeps.txt"
for entry in $MODELS; do
  for area in $AREAS; do
    [ -s "$STATE_DIR/${entry%%:*}-$area.md" ] && echo "${entry%%:*} ${entry#*:} $area sweep" >> "$STATE_DIR/sweeps.txt"
  done
done
xargs -P "$CONCURRENCY" -L 1 bash "$STATE_DIR/arm.sh" < "$STATE_DIR/sweeps.txt"
```

Run this block as one background Bash call, the same way as Step 2. Its completion notification is the signal to continue.

Then rerun the Step 3 extract-and-merge block. It extracts each sweep's findings and rebuilds that area's merged file with them. Check each sweep afterward.

```bash
while read -r label model area comp; do
  s="$STATE_DIR/parts/$label-$area-sweep.md"
  if [ -s "$s" ]; then echo "$label-$area sweep added=$(grep -c '^- \*\*' "$s")"; else echo "MISSING $label $area sweep"; fi
done < "$STATE_DIR/sweeps.txt"
```

Re-dispatch a `MISSING` sweep the same way as a `MISSING` arm in Step 3.

Re-export `STATE_DIR`, `TARGET_PATH`, `PROJECT_ROOT`, and `EXPORT`, and reset `AREAS`, `MODELS`, and `CONCURRENCY`, when a block runs as a separate call from Step 2.

After the last sweep and the last re-dispatch, delete the export. Step 5 makes its own checkout for the judges.

```bash
rm -rf "$EXPORT"
```

### Step 5: Collate, Verify, and Report

Run the scripted stages. Run each model stage as a background Bash call. Its pool returns when every call has finished, and the completion notification is the signal to continue. Never poll a running stage with `sleep`. Run the stage command itself as the background call. Never detach it with `nohup` or a trailing `&`, and never wait on a log line with `tail -f | grep -m1`, for the reasons Step 2 gives.

```bash
S="${CLAUDE_SKILL_DIR}/scripts"   # replace ${CLAUDE_SKILL_DIR} with this SKILL.md's own directory on a non-Claude harness
[ -f "$S/init_run.py" ] || { echo "scripts not found at $S"; exit 1; }
RUN=<RUN_DIR printed by Step 1>
python3 "$S/checkout.py" "$RUN"
python3 "$S/normalize.py" "$RUN"
python3 "$S/collate.py" "$RUN"         # one model call per component, background
uv run --with scikit-learn --with scipy --with numpy python "$S/windows.py" "$RUN"
python3 "$S/merge.py" "$RUN"           # one model call per similarity window, background
python3 "$S/rank.py" "$RUN"
python3 "$S/verify.py" "$RUN"          # one model call per Critical or High issue, background
python3 "$S/report.py" "$RUN"
```

| Stage | Output | What it does |
| ----- | ------ | ------------ |
| `checkout.py` | `checkout/` | Exports the reviewed commit with `git archive` and deletes `judge_exclude` paths, such as `CLAUDE.md`, `.claude/`, and review state. Every model stage reads only this tree. |
| `normalize.py` | `findings.jsonl` | Parses every merged findings file and ocr's comments into findings with stable IDs. Exits 1 on any bullet it cannot parse. |
| `collate.py` | `issues-by-component.jsonl` | Groups each component's findings into issues, where one issue is one code change. Every finding ID must land in exactly one issue or in the dropped list. |
| `windows.py` | `windows.json` | Orders all issues by text similarity and cuts overlapping windows of 150, so one window can see a defect reported in two components. |
| `merge.py` | `global_merges.json` | Merges issues that describe the same defect, where one change fixes all. The same pattern in independent places stays apart. |
| `rank.py` | `issues.jsonl`, `issues.md` | Applies the merges and ranks by severity, source count, and finding count. |
| `verify.py` | `verify/results.jsonl`, `verify/second.jsonl` | Opus at high tries to refute each Critical and High issue and returns a verdict, quoted evidence, the locations and members that do not hold, and its own severity. Fable at high rechecks, blind, every issue the verifier confirms as Critical. |
| `report.py` | `report.md` | Counts, every confirmed issue at the lower of its two ratings, the refuted ones with the reason, and coverage gaps. |

Every model call runs as its own `claude -p --bare` process with `--tools Bash,Read` under `--permission-mode dontAsk`, a 5-minute prompt cache, and the prompt on stdin. The pool checks that each process started with exactly those tools, checks every answer's content, and retries a rejected answer up to three times with the reasons appended. A verdict whose evidence quote is not the code at the reviewed commit is rejected. The review-tickets skill documents the measurements behind each of these settings.

The merge rule is narrower than it was. An earlier rule also merged the same kind of defect with the same kind of fix. It built one issue of 77 findings across 24 files, and tickets built from it cited locations that did not support the claim.

Report the counts from `report.md`, the confirmed Critical issues, and the coverage gaps to the operator. The run directory is the input to the review-tickets skill.

## Expected Output Files

`.llmtmp/review-deep/` holds the whole run and is wiped at the start of the next one:

- `<label>-<area>.md`, 27 merged findings files, component parts plus sweep
- `ocr-scan.json`, `ocr-scan.log`, and `ocr.pid`, the coverage pass
- `ledger.txt` and `skipped.txt`, the reviewable files and the excluded ones with ocr's reason
- `components/cNN.txt`, the partition
- `coverage/<label>-<area>-<comp>.txt`, each arm's reviewed or skipped record
- `reviewed.txt` and `opened.txt`, the files arms marked reviewed and the files they opened
- `parts/<label>-<area>-<comp>.md`, `parts/raw-*.ndjson`, `parts/*.log`, each arm's findings, event stream, and stderr
- `parts/attempts/raw-*.attemptN.ndjson`, a superseded attempt's event stream, kept when arm.sh retries past a SQLite write-contention failure or an arm that wrote no findings
- `opencode-db/<label>-<area>-<comp>.db`, each arm's isolated opencode session database
- `opencode-config/`, the generated opencode config every arm runs under, and its per-area prompt files
- `arms/<label>-<area>-<comp>.root`, the path of the copy each arm ran in, the one root its tool calls may touch
- `arm.sh`, `tasks.txt`, `sweeps.txt`, the runner and its work lists

The run directory, `${XDG_CACHE_HOME:-~/.cache}/review-deep/<repo>-<commit12>/`, holds Step 5's output and survives the next review of a different commit:

- `run.json`, the repository, commit, models, concurrency, judge exclusions, and commit sentence
- `checkout/`, the export every judge reads, and `checkout_excluded.json`
- `findings.jsonl`, `issues-by-component.jsonl`, `dropped.jsonl`, `unassigned.jsonl`, `windows.json`, `global_merges.json`
- `issues.jsonl` and `issues.md`, every issue with its member findings inlined
- `verify/results.jsonl` and `verify/second.jsonl`, the verdicts
- `report.md`
- `collate/`, `merge/`, `verify/first/`, `verify/second/`, each with `pool.log` and every model process's event stream under `calls/`

## NDJSON Reference

One JSON object per line. Skip lines that fail to parse.

| Type | Meaning | Key fields |
| ---- | ------- | ---------- |
| `step_start` | An LLM turn begins | |
| `text` | Model emitted text | `part.text` |
| `tool_use` | Model called a tool | `part.tool`, `part.state.status`, `part.state.input` |
| `step_finish` | A turn completed | `part.reason`, `part.cost`, `part.tokens` |
| `error` | Session-level error | `error.data.message` |

A `step_finish` reason of `stop` means done and `tool-calls` means continuing.

```bash
jq -s '[.[] | select(.type=="step_finish") | .part.cost] | add' "$NDJSON"
tac "$NDJSON" | jq -s 'first(.[] | select(.type=="step_finish")) | .part.tokens.total'
jq -r 'select(.type=="tool_use") | .part.tool' "$NDJSON" | sort | uniq -c | sort -rn
jq -r 'select(.type=="error") | .error.data.message' "$NDJSON"
```

Serena carried 119 of 181 tool calls on a TypeScript repo and 2 of 28 on a repo of HTML, CSS, and a Dockerfile. Symbolic navigation is worth little where no language server backs the files.

## Tests

Tests and evals for review-deep and review-tickets, plus the guard tests and preflight tests that cover all four skills, live in `evals/` at the root of this plugin's repository, outside the installed skill.

| Check | Command, from `evals/` | Cost |
| ----- | ------ | ---- |
| Unit tests, one directory per skill, plus preflight and guard | `uv run --with pytest pytest -q unit/review_deep`, `unit/review_tickets`, `unit/preflight`, and `unit/guard` | none |
| End-to-end replay on the harbor fixture, all three kinds | `uv run --with pytest pytest -q test_end_to_end.py` | none |
| Live quality eval against `fixture/truth.json` | `python3 live_eval.py WORK_DIR --run` | about $3 at list price |

`unit/review_deep` imports `windows.py`, which imports scikit-learn, scipy, and numpy, so run it as `uv run --with pytest --with numpy --with scipy --with scikit-learn pytest -q unit/review_deep`. The other directories need no extra packages.

Run the unit tests and the replay after any change to `scripts/`. The replay stops with "prompt changed" when a prompt changes. Record again with `python3 pipeline.py WORK_DIR --mode record`, check the run with `live_eval.py`, and save it with `python3 golden.py save RUN_DIR`. Run the live eval on demand after changing a model, an effort level, or a prompt.

## Rules

- The invoking agent is a launcher. It performs no review analysis of its own. The Step 5 scripts and their model calls do all of it.
- NEVER let a Step 5 model call read the live working tree. They run in the run directory's `checkout/`.
- NEVER poll a background stage with `sleep`, a wait loop, or a log watcher such as `tail -f | grep -m1`. Wait for its completion notification.
- Keep prompts in `prompts/` as `.txt`. A markdown formatter rewrote a `.md` prompt and changed its meaning.
- ALWAYS redirect stdin from `/dev/null` on `opencode run`. Omitting it hangs the process before session creation with no output and no error, which is anomalyco/opencode issue #38723.
- Impose no token cap and no turn cap on a reviewer. Let it finish.
- Run Step 2b a minute or so after dispatch, and again during long runs. An arm with an empty NDJSON is dead and holds a pool slot, and wall time cannot tell that apart from a slow review.
- Run the Step 2 and Step 4 dispatch blocks as background Bash calls, never detached with `nohup` or `&`. The pool blocks until every arm exits, and backgrounding keeps that out of the main session. The call's completion notification is the only signal that the pool has finished.
- ALWAYS export `STATE_DIR`, `TARGET_PATH`, and `PROJECT_ROOT` in every Bash call that runs `arm.sh`, including a single re-dispatch. Shell variables do not carry between calls, and `arm.sh` exits 255 without them.
- Launch every arm through the pool and the ocr scan in one bash block. They are independent processes.
- Use plain message invocation, not `--command`. The `--command` flag has a known issue with the context7 MCP server.
- Do NOT clean up per-area files, NDJSON, or logs during a run. Step 1 wipes them at the start of the next one.
- If an arm fails, still wait for and report the others.
- The opencode arms need only the operator's providers in `~/.config/opencode/opencode.json` and a Serena home at `~/.serena-reviewer`. Their agents, Serena context, and Serena manual come from this plugin through `opencode_env.py`. `preflight.py --tier deep` checks the providers and the Serena home by name before Step 1 wipes anything.
