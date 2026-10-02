---
name: master-loop
description: "Run a mixed AI harness Herdr pane loop as master: labelled panes named master, planner, coder and verifier execute a multi-unit campaign, one unit at a time. Use when this pane is master or the orchestrator of such a loop, when asked to start or resume the loop, dispatch or brief a unit, or check on the planner/coder/verifier. Requires HERDR_ENV=1."
---

# Master loop

Four Herdr panes, one campaign, one unit in flight at a time.

| Role | Does | Never |
|---|---|---|
| **master** | Owns the plan. Drives **planner only**. Defines units, reports to the owner, asks about commits. Owns architecture-gate and CI edits under §4. | Builds, beyond the environment probe before unit 1 (§3). Edits production code or ordinary tests. Verifies its own gate or CI edit. Talks to coder or verifier. |
| **planner** | Owns the unit-local coder/verifier loop and reports its terminal outcome. | Builds while coder or verifier works. |
| **coder** | Builds the unit. Owns the build tool for its job, for the build and its step's focused tests only. | Verifies its own work: runs revert proofs, full suites, publishes, stress or live runs (§5). Touches the gate. Commits. |
| **verifier** | Reads the diff, runs the suites, executes revert proofs. Owns the build tool for its job. | Fixes what it finds — it reports; planner re-dispatches coder. |

**One agent runs the build/test tool at a time, campaign-wide** — planner and master included stay off
it for that job's lifetime; anyone who must run concurrently is write-files-only. Breakage here is
silent: shared build output, stale test binaries, a green that means nothing.

## 1. Resolve panes and agent hosts every turn

The role is the **pane label** on this tab. Labels are stable; IDs are not in role order; agent *names*
die on reset. Never hardcode an ID or reuse a remembered layout. Verify the Herdr environment in
the current shell and stop on failure; printing a warning and continuing is not a guard.

POSIX shell:

```bash
if [ "${HERDR_ENV:-}" != 1 ]; then
  echo "not inside Herdr - stop" >&2
  exit 1
fi
herdr pane list --workspace "$HERDR_WORKSPACE_ID" | python3 -c '
import json, os, sys
tab = os.environ["HERDR_TAB_ID"]
for pane in json.load(sys.stdin)["result"]["panes"]:
    if pane.get("tab_id") == tab:
        print((pane.get("label") or "(unlabelled)") + "\t" + pane["pane_id"])
'
herdr agent list
```

PowerShell:

```powershell
if ($env:HERDR_ENV -ne '1') {
    throw 'not inside Herdr - stop'
}
(herdr pane list --workspace $env:HERDR_WORKSPACE_ID | ConvertFrom-Json).result.panes |
    Where-Object { $_.tab_id -eq $env:HERDR_TAB_ID } |
    Select-Object @{n = 'label'; e = { $_.label ?? '(unlabelled)' } }, pane_id
herdr agent list
```

Parse Herdr JSON as JSON. A line-oriented `awk` or `sed` parse resolves unlabelled panes to the wrong
ID without erroring, and **any positional field — a dollar sign followed by a digit — is replaced by
the skill's own arguments before you read this file**, fenced code included. Check `command -v jq
python3` before depending on either; a watcher built on a missing `jq` emits nothing rather than
failing.

Join `agent list` to the labelled panes by `pane_id`. Each of `master`, `planner`, `coder` and
`verifier` must occur exactly once on `$HERDR_TAB_ID`; on a missing or duplicate role, say which and
stop, never guess from position. Address panes by the resolved ID and re-resolve after any close,
split, swap or rename. Fix a label with `herdr pane rename <pane-id> <label>`. If a labelled pane has
no agent, use `herdr agent start <name> --kind <claude|codex> --pane <pane-id>`.

The `agent` field identifies `claude` or `codex`; do not infer the host from the pane label, title or
remembered occupant. The host determines skill syntax and which repo instruction files apply.

## 2. Campaign state lives outside the tracked worktree

Use one campaign directory that survives reset, stays out of `git status`, and is writable by every
pane under its active sandbox. A sibling directory such as `C:\dev\<area>\<ticket>\` on Windows or
`/work/<area>/<ticket>/` on Linux is usual, not guaranteed. Verify access before unit 1. If no shared
writable directory exists, ask the owner to designate or authorize one; do not silently move campaign
state into tracked files.

`PLAN.md` (master: unit table with status, locked owner decisions, what is out of scope) is the record,
not your context. Beside it, with `brief-` for an instruction and `report-` for a result so that `ls`
answers "is this round finished?": `brief-planner-u<unit>.md` (master→planner),
`report-planner-u<unit>.md` (planner: terminal outcome), `brief-coder-u<unit>.md` (planner→coder),
`report-coder-u<unit>.md` (coder: files written, revert table, open questions),
`brief-verifier-u<unit>.md` (planner→verifier),
`report-verifier-u<unit>.md` (verifier: verdict, real counts, which proofs it ran),
`baseline-u<unit>/` (pre-unit status, staged and unstaged binary diffs, and hashes or copies of
pre-existing untracked files), and `mutation-u<unit>.md` (revert-proof crash journal, one row per
mutation).

**Every agent writes a file and replies with only the path**, a verdict line and the numbers. Agent
TUIs may use alternate-screen rendering or truncate scrollback, so spoken output is not the record.

**Every report opens with a summary of at most 8 lines**: verdict, counts, files touched, and the proof
run. Put it before any detail. Its reader opens the body only on FAIL, a surprise in the summary, or
the unit-end review. A coordinator reading every report in full fills its context by the fifth step.

## 3. Starting cold

1. Resolve the panes. If the campaign is running, read `PLAN.md` and the latest report first — they, not
   your memory, say where it stands.
2. Build the **constraint block** from every repo instruction file applicable to the target path,
   including `AGENTS.md`, `CLAUDE.md` and `CLAUDE.local.md`. Resolve scope and precedence per host:
   Codex follows `AGENTS.md`; Claude Code follows its Claude instruction files. Put shared constraints
   in the common block and conflicts in labelled host addenda. Give the planner both addenda; give each
   coder or verifier only its matching one. Include exact build/test commands and how they serialize;
   exact format/lint commands, including any that look right but are wrong here; line endings, final newline,
   encoding for new files; commit policy (assume never auto-commit); files no agent may edit
   (architecture gates, CI config — **master's** to own); model families banned for subagents.
   Re-resolve the applicable files before every unit so an instruction changed during the campaign
   cannot leave later briefs stale.
3. Before unit 1, while no agent holds the build tool, probe the environment (runtime usable, image
   cached, tool works offline) and record the findings in `PLAN.md`. For campaigns using `cslq`,
   include `cslq ready` through the actual host execution route and a narrow semantic query from a
   later tool call. Record any sandbox restriction and the working invocation for the host addenda.
   A cold cslq load runs MSBuild's design-time build, so coordinate startup or reload with the build
   owner under the same serialization rule.
4. Size units in `PLAN.md` by behaviour, not job count: **one unit is one reachable behaviour**,
   committed on its own. List a unit's behaviours before briefing; more than one means more than one
   unit. The planner splits the unit into coder steps, **each one slice of that behaviour: one or two
   named tests, the production lines that make them pass, about three files**, statable in one sentence
   or split again. Size for verifiability, not capability: a narrow step fails visibly and its proofs
   stay checkable, whatever the model; slower is fine. Give the planner the limit, never a step list —
   a suggested list gets relayed to the coder as one multi-concern job. Read the unit's first coder
   brief when it lands and stop the planner if it breaks the limit.
5. Put open questions to the owner **before** the unit that depends on them, with a recommendation, not
   a survey. Never open a unit with a question still open inside it.

## 4. The unit cycle

master does steps 1, 2, the gate/CI exception in step 4, and step 6 only.

1. **Open the unit.** Re-resolve its applicable instruction files. Before any agent edits, capture
   `baseline-u<unit>/`: porcelain status, staged and unstaged binary diffs, and hashes or copies of
   pre-existing untracked files. This is the verifier's base when earlier units remain uncommitted.
   Check for a `PENDING` row in any mutation journal first and recover it under §6 before interpreting
   the tree.
   Then write the unit brief into the campaign dir (§5).
2. **Clear and re-brief planner** — at every unit start and after every planner return. Never append
   to a returned planner session; at high context it compacts mid-job. Before any re-dispatch, rename
   the superseded planner report so the watcher does not fire on it. After an owner decision, a block or
   a gate/CI return, record the outcome in `PLAN.md` and dispatch a self-contained resume brief: the
   unit brief, latest planner report, decision and remaining work. Use the syntax for the current
   shell. `<reset>` is `/clear` for Claude, `/new` for Codex.

   POSIX shell (Linux or macOS):

   ```bash
   herdr agent send-keys <planner> ctrl+u
   sleep 1   # sent too fast, the reset no-ops silently
   herdr agent prompt <planner> "<reset>"
   # confirm a fresh session before continuing
   herdr agent send-keys <planner> ctrl+u
   # background this call - it blocks for the whole job
   herdr agent prompt <planner> "$(cat <brief-file>)" --wait --timeout 3600000
   ```

   On Git Bash for Windows, use the POSIX recipe but prefix both `herdr agent prompt` commands with
   `MSYS_NO_PATHCONV=1`.

   PowerShell:

   ```powershell
   herdr agent send-keys $planner 'ctrl+u'
   Start-Sleep -Seconds 1   # sent too fast, the reset no-ops silently
   herdr agent prompt $planner '<reset>'
   # confirm a fresh session before continuing
   $brief = Get-Content -Raw -LiteralPath $briefFile
   herdr agent send-keys $planner 'ctrl+u'
   # background this call - it blocks for the whole job
   herdr agent prompt $planner $brief --wait --timeout 3600000
   ```

   Where Herdr reports an `agent_session`, compare it before and after `<reset>`; otherwise read the
   pane and confirm the previous transcript is gone. Do not send the brief until reset is confirmed.
3. planner resolves coder's current host, clears coder with its host's reset protocol, then briefs
   **coder** using that host's skill syntax. It judges the report against the brief. A report that
   misses the charge goes back to coder, not on to verifier.
4. If the coder reports that an architecture gate or CI file must change, planner returns to master
   with the exact requested change before briefing verifier. As the sole code-edit exception, master
   may edit only that gate or CI file and does not build or test it; master then returns control to
   planner. planner resolves verifier's current host, clears verifier, then briefs **verifier** with
   the unit-local delta from `baseline-u<unit>/`, the coder report, the revert table, and any
   master-authored gate or CI diff. Verdict is PASS or FAIL with real suite counts.
5. planner owns the unit-local loop: FAIL goes back to coder with a fix brief, then to verifier again;
   PASS closes the unit. It may run small, bounded repair rounds without returning to master. Return
   only on PASS, a master-owned gate/CI change, a required owner decision or scope change, or repeated
   failure that needs replanning. **Verify per step, gate per unit:** each step's verifier reviews the
   step diff, runs only that step's focused tests, and runs at least one revert proof itself. Once, at
   unit end, one verifier job runs the full suites, the build and format gates over the whole delta from
   `baseline-u<unit>/`, and records the SHA256 of every delta file. Full suites per step cost minutes
   and catch little the unit-end run misses.
6. **master updates `PLAN.md`**, reports to the owner in a few lines, asks whether to commit. Before
   accepting a PASS, confirm the report says verifier executed the proofs itself — a body disclosing
   proofs it declined to run overrides its own verdict line, and the unit stays open. Then compare the
   SHA256 of every file in the delta with the verifier's final report. A file that changed after the
   verifier's run was never verified. Then read the planner's final report and the delta file list
   against the unit's charge in `PLAN.md`, without building: every step can pass while the unit still
   misses its behaviour. The owner may pre-authorize **chaining**: master commits each verified unit
   and opens the next without asking. It still stops for an owner decision, a gate/CI change, a
   mis-sized unit, or physical/hardware work. Record the authorization and its end point in `PLAN.md`.

For a job dispatch, use `herdr agent prompt ... --wait --timeout <ms>` from a confirmed non-working
state. Herdr first requires observed `working` or `blocked`, then waits for `idle`, `done` or
`blocked`; do not add `--until`. A standalone `agent wait` checks the current state immediately, so
calling it after a non-waiting prompt can accept the pre-dispatch `idle`. Use standalone wait only
after `working` was independently observed.

**A `--wait` dispatch outlives any foreground shell budget and must be backgrounded.** A job timeout
is measured in tens of minutes, while the dispatching harness caps a foreground call far lower —
Claude Code's Bash tool allows at most 10 minutes and defaults to 2. A foreground `--wait` is killed
mid-job and the pane then looks stalled while it is still working. Dispatch it with the host's
background mechanism (`run_in_background` in Claude Code) and collect the result afterwards.

**Completion is the watcher, not the dispatch.** `--wait` returns when the dispatched pane settles,
which a planner does while its coder is still working, and a planner job routinely outlives its
timeout: a three-step unit can take two hours. Neither `done` nor `timeout` proves anything, and
neither is a reason to resend. Run one light background watcher per unit — idle master time is the
costliest loss — polling every 60 s and exiting on the first of:

- `DONE`: `report-planner-u<unit>.md` exists and no role pane is `working`.
- `BLOCKED`: any pane is `blocked`. That needs intervention, not a PASS.
- `STALLED`: no pane `working` for three polls and no report. The planner stopped on a question, or
  its dispatch died.

A pane that started a long background job — a test loop, a publish — goes `idle` while the job runs,
so a watcher keyed on pane state alone reports `STALLED` on a unit that is working. Count a live
build or test process as working too. When that check uses `pgrep -f`, bracket the first character
(`pgrep -f '[t]esthost'`): an unbracketed pattern also matches the watcher's own command line, which
holds the pattern, so the watcher sees itself as activity and never reports `DONE`.

Put waits inside the background loop; Claude Code blocks a foreground `sleep` chained before a check.
If the harness reaps a background task — the dispatch or the watcher — the delivered prompt survives
and the unit keeps running: report the reap, and restart the watcher only when the owner asks. On
`agent_prompt_stalled` or a timeout, never resend blindly; the prompt may still have landed. Inspect
`agent get`, `agent read` and the report path first. `<reset>` is the exception to job dispatch:
send it without `--wait` and confirm the new session as described above before sending the brief.

**Stalls and silent blocks.** A coder on a thinking spinner for 20+ minutes with no file write and no
build process is stalled, though its planner may judge it busy. Master may send the working planner a
short evidence message (Codex queues it into the turn); the planner interrupts the coder, resets it,
and re-dispatches the step from its partial edits. Master still never messages coder or verifier. An
agent that answers a brief with an authentication error ("Login expired") has done nothing: the
planner returns BLOCKED with the exact text instead of retrying, and the owner logs that pane in.

**Waits are silent, at every level.** Every poll's output lands in the waiting agent's context. A
planner that checked its report path, read the other pane's screen and grepped the journal every
minute reached 90% context in one unit. The rule applies to master and planner alike: wait in one
command that loops internally and prints exactly one line when it exits (`DONE`, `BLOCKED`,
`STALLED`, or a timeout). Never poll in a loop of separate tool calls. Never `herdr agent read` or
`pane read` a working pane just to see progress; read a screen only after the wait reports `STALLED`
or `BLOCKED`. A host without background jobs runs the wait in the foreground with a timeout under its
own command budget, then re-issues that same silent wait. The shape, in PowerShell:

```powershell
$deadline = (Get-Date).AddMinutes(25); $idle = 0
while ($true) {
    $state = (herdr agent get $pane | ConvertFrom-Json).result.agent.agent_status
    if ((Test-Path $report) -and $state -ne 'working') { 'DONE'; break }
    if ($state -eq 'blocked') { 'BLOCKED'; break }
    if ($state -ne 'working') { $idle++ } else { $idle = 0 }
    if ($idle -ge 3) { 'STALLED'; break }
    if ((Get-Date) -gt $deadline) { 'WAITING'; break }
    Start-Sleep -Seconds 30
}
```

**The planner holds a context limit.** After each step it appends one line to
`state-u<unit>.md`: step, one-sentence behaviour, verdict, report paths, and the next step. When its
context passes about 50%, it finishes the current dispatch, writes that line, and returns `CONTEXT`
in `report-planner-u<unit>.md`. Master renames that report, resets the planner and re-briefs it from
the unit brief plus the state file (§4.2). Compaction mid-unit loses the step history the planner
judges against. A reset from a state file does not.

### Master-owned gate proof

The coder never edits an architecture gate or CI file. The master may make the required edit only in
the serialized step 4 exception and never validates its own change. The verifier reviews it and runs
the applicable validation. For an architecture rule, verifier first runs the targeted architecture
tests green, then introduces a temporary **compiling** violation in a non-gate source file covered by
the new rule, confirms the targeted test fails for that rule, restores through the mutation journal,
and reruns the targeted test green before the broader required suite. If no faithful compiling
violation exists, verifier reports that the rule is unproved instead of declaring PASS.

For a **CI** file the bite is the same shape where it can be staged: only with explicit owner
approval, push the change on a probe branch, confirm the job fails on the condition the change is
meant to catch, then confirm it green, and cite both runs. Where no faithful failing condition can be
staged, the edit is owner-reviewed rather than verifier-proved and the report says exactly that. A
green run alone is never recorded as proof of a CI change.

As a gate mutation must compile, a CI mutation must be **enactable**: the run must show it reached the
built artifact, not just the source. A condition the build never propagates yields an honest green
carrying no information, so when a probe is green while carrying a mutation, suspect the assertion
before the mutation. A workflow that does not yet
exist on the default branch cannot be proved by pushing a branch (`workflow_dispatch` 404s, `push:`
gates may not fire); only a pull request runs it from its own head, so with owner approval open a
draft PR titled `DO NOT MERGE`, capture both runs, then close it and delete the branch. Since no agent
pushes, master authors and pushes the probe commit — the verifier still judges the two runs.

### The slash trap

**Git Bash rewrites leading `/` arguments into Windows paths before `herdr` runs.** For example,
`"/clear"` arrives as `C:/Program Files/Git/clear`, so the old transcript survives silently. Set
`MSYS_NO_PATHCONV=1` on **every** `herdr agent prompt`; choosing per call invites omissions.

Skill syntax is host-specific and must appear in the brief; plain `lean-work` invokes nothing:

| Host | Put in the brief |
|---|---|
| Claude Code | `/lean-work` on the first line |
| Codex | `$lean-work` in the request; do not send `/lean-work` |

Codex's `/skills` is interactive, not an unattended dispatch mechanism. After dispatch, confirm the
turn started and no unknown-command error remains; a Claude `Skill(<name>)` marker is useful when
present but is not a cross-host requirement. Clear composer text with `ctrl+u` first because automatic
suggestions concatenate with the command. They are UI state, not owner instructions.

The path-conversion workaround is Git Bash on Windows only. Native POSIX shells and PowerShell need no
prefix. Detect the dispatching pane's shell at each hop; master and planner need not use the same shell.

## 5. What every brief carries

Repo/worktree path spelled exactly, plus any checkout that is off-limits · campaign dir, `PLAN.md` and
`baseline-u<unit>/` pointers · which unit, and the charge in one paragraph including what is out of
scope · who the agent is and who owns the build tool for this job · the target host and its correct
skill invocation · the common constraint block plus only the target's matching host addendum · the
output path, and "reply with only that path, the verdict and the counts" · the source of truth to work
from and the existing file whose idiom to follow ("follow the idiom in `<file>`" beats describing it)
· for coder, the revert table (§6) and: files written, anything the gate needs, tests that could not
be written faithfully with the reason, questions the sources could not answer · for coder, its exact
gate commands — the build and its step's focused test filter, nothing more (see below) · the spec sources that
define "right" (plan, research, owner decisions), not only code idioms — code yardsticks alone get
code-quality answers to a domain question.

Put the constraint block in one campaign file that every brief points to by path. But **any fact an
agent needs before it can read that file goes in the brief body, as its first paragraph** — a Codex
pane whose default launcher fails cannot open the file that tells it how to escalate. Keep a coder
brief to about 40 lines.

**A coder runs the build and its step's focused tests, and stops.** The planner never adds full suites,
publishes, stress loops, live runs or revert proofs to a coder brief, and the brief says so in one line:
that is the verifier's job, which repeats every such run anyway. Left unsaid, coders over-deliver: one
campaign's coders mutated their own revert tables, ran AOT publishes, full suites with reruns, and
stress loops of 20+ runs — minutes per step that proved nothing the verifier did not re-prove. Two
exceptions, named in the brief when they apply: a step whose charge *is* reproduction (a flake hunt
runs as many loops as it needs), and a test-first step, which may show its new test red once before
the fix.

**For Windows Codex roles using cslq under a sandbox that denies named pipes**, put this in the
brief body and have planner pass it to each applicable downstream role: run `cslq ready` and
subsequent queries directly through `exec_command` with `sandbox_permissions: "require_escalated"`
and request `prefix_rule: ["cslq"]`, using the exact repo root as `workdir`. Keep the default
background session enabled; no dedicated Herdr pane or extra terminal tab is needed. Each host
must obtain approval through its own mechanism; master approval does not transfer to another
agent. If escalation is unavailable or denied, report BLOCKED with the exact reason rather than
retrying sandboxed modes or routing through another pane. Coordinate cold loads or reloads with
the build owner. Include any known launcher failure and its approved recovery in the first
paragraph too, so the agent can read the referenced files.

**Only master loads this skill**, so a rule reaches another agent only if a brief carries it. Each
brief that dispatches another agent restates: report only when the report file exists and the
dispatched pane has left `working`; reset with the confirmation step above; write the file, reply with
the path.

The master→planner brief is the exception to one addendum per brief: it carries the planner, coder and
verifier host map with each role's invocation syntax, all host addenda, the step-size limit (§3), the
coder run limit and its two exceptions (above), the stall and authentication rules, the silent-wait rule with its snippet, and the context limit with the
state-file path (§4). It also carries the summary-first report rule for the planner to pass to every
coder and verifier brief. The planner re-resolves a downstream pane before dispatch and
updates the map if its occupant changed. Its job is **control, not relay**: it never forwards the
master brief to the coder.

Sequence agents that would touch the same file. Two agents on one file is a lost edit.

When a brief quotes or truncates a source instead of pointing at it, check the evidence survived the
cut: a reviewer answers confidently from what it was given, and an excerpt missing the requirement
reads exactly like a requirement that was never met.

## 6. The one proof rule: the revert table

coder delivers, per test added or changed, **the single production line whose removal or inversion turns
that test red** — reasoned from the code, never executed: a coder mutating the tree to prove its own
table does the verifier's job without the journal, and the verifier must re-run it anyway. verifier executes a sample — mutate, run that test class alone, confirm red, restore —
and states which proofs it ran itself versus accepted from the table. The author never verifies its own
bites; this is what catches a test that pins something other than its name claims, and a test rescued by
its own deadline.

A proof run keeps **one** journal outside the worktree, `mutation-u<unit>.md`, with one row per
mutation, State updated **in place** `PENDING` → `RESTORED` — one table, never a separate closure
table, and the bare word `PENDING` never in prose, so that `grep -c '| PENDING |'` stays the
canonical check. The journal is **append-only across the unit**: each verifier adds rows and edits
only its own row's state, never rewriting, reordering or trimming the file. One verifier's rewrite
once erased fifteen earlier proof rows, leaving them attested only in step reports. Snapshot the worktree once at the head of the run — porcelain status, staged and
unstaged binary diffs, untracked file hashes — not per row. Each row is written **before** the source is touched: status
`PENDING`, file path, pre-mutation hash, the exact reverse content or patch, and the intended
mutation. After the red run, restore by content, confirm the file hash matches the row, mark the row
`RESTORED`. Re-check the run snapshot once at the end of the run. Gate proofs use the same journal.

On start or resume, a `PENDING` row blocks normal work — the hash and reverse patch in that row are
what recovery needs. planner sends verifier a recovery-only brief. If the file still matches the
recorded mutation, verifier restores it and validates against the run snapshot; if it matches neither
the original nor the mutation, stop for an owner decision rather than overwriting unknown work. A
missing verifier report never proves that its mutation was restored.

Mutation traps: it must **compile** (a build failure looks like a red and proves nothing); it must be
real code or a string literal, never a comment (source scans strip comments); and **restore by content,
not by copying a backup** — a copy keeps the old timestamp, the build skips the rebuild, and the run
reports the previous binary, lying in both directions. Touch the write time, or confirm it rebuilt.

A guard on a branch unreachable *because the rest of the unit is correct* has no mutation: ship it with
a comment naming the invariant and say so in the report instead of padding the suite.

## 7. Remaining traps

- `herdr agent read` can snapshot a working agent, but alternate-screen TUIs expose only their current
  viewport; scrolled-away rows never enter Herdr's scrollback and `--lines` cannot recover them. Files,
  not scrollback, remain the durable record.
- **A pane that dies mid-job leaves its edits with no report** — indistinguishable from finished work in
  `git status`. Check for the report file, not the file list. Account or subscription errors kill a pane
  silently.
- A pane whose cwd differs from the target tree may prompt for permission. Compare the exact requested
  path with the brief. Approve only when it is expected and already within owner-authorized scope;
  otherwise report the mismatch and stop.

## 8. master never

Runs the build while an agent holds it, even "just to check" · commits, stages or pushes unasked —
recorded chaining and an owner-approved CI probe, which it does not judge, are the only pre-authorized
commits or pushes · commits a file whose hash
differs from the verifier's final run · edits production code or ordinary tests · lets coder or
verifier edit the architecture gate or CI config · validates its own gate or CI edit · accepts a gate
without verifier's red/green bite proof · records a CI edit as proved on a green run alone · opens a
multi-behaviour unit, or hands the planner a step list · re-briefs a planner without resetting it ·
dispatches a `--wait` job in the foreground, reads its timeout as a failure, or runs a unit without a
watcher · waits by repeated tool calls or reads a working pane's screen for progress instead of one
silent wait · spawns a subagent on a
model family the owner ruled out · works from a remembered pane layout, or writes one down.
