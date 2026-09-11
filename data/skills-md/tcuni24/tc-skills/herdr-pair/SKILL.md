---
name: herdr-pair
description: Use when the user asks to run a task with two Herdr agents splitting planning/review from execution — “你负责规划和审核，让 X 执行”, “协同两个 agent”, “把活派给 herdr 里的 X，你把关”, “让它把结论返回给你”, “你拆一下任务再派给 X”. Roles are agent-type agnostic — either side may be claude, opencode, codex, droid, cursor, hermes, omp, kimi, pi, grok or anything else on the roster. Covers role contracts, cutting the work into verifiable rounds, self-contained handoff prompts, the 131,071-byte prompt limit and “argument list too long” recovery, artifact-based verification with and without git, auditing an executor’s explanations and not just its numbers, the concurrent-writer hazard, and the quality kill-switch. Not for one-shot relays — use herdr-handoff for those.
---

# Herdr Pair: Planner + Executor (+ optional Verifier)

At minimum two live Herdr agents share one task. **Planner** owns scope, sequencing, acceptance and
the final report to the user. **Executor** owns edits and command runs. An optional **Verifier**
performs independent read-only checks against a frozen artifact state. The user sees one deliverable.

**Roles are positions, not agent types.** Either seat can be held by any agent on the roster —
claude, opencode, codex, droid, cursor, hermes, omp, kimi, pi, grok, and whatever gets installed
next. Nothing in this skill depends on who is which. Settle your seat first (next section), then
follow that seat's sections.

This is not `herdr-handoff`. That skill relays a message and stops. This one keeps a loop
running and makes whoever plans accountable for work they did not type.

## Which seat are you in

| You are… | when | you follow |
|---|---|---|
| **Planner** | the user is talking to you about the task, and asks you to farm out the doing | §0–§8 |
| **Executor** | another agent sent you a scoped task and expects a report back | “If you are the executor” |
| **Verifier** | the Planner explicitly asks for an independent read-only check of a completed round | “Stable review epochs” + §5 |

If the user's phrasing leaves it open, you are the Planner — the agent holding the user's thread
owns the deliverable. Never assume the seat from agent type; a `hermes` can plan for a `claude`
just as easily as the reverse.

The seats may be filled by the same agent type. Two `claude` panes, or two `opencode` panes, pair
fine — resolution is by `pane_id` (§1), which is unique regardless of type.

A Verifier is optional and does not turn one round into parallel writing. It may inspect only after
the Executor has stopped writing and the Planner has frozen a review epoch. If the Executor writes
again, the Verifier's unfinished or completed conclusion is stale and must be discarded.

## The one rule that matters

> **The Planner is accountable for every line the Executor writes. If the Planner cannot vouch
> for it, it does not ship.**

Everything below exists to make that possible.

## When NOT to pair

Pairing costs a full round-trip per step plus your review time. Skip it and just do the work when:

- the task is mostly **judgment or authoring** (specs, decisions, reviews) — the executor
  becomes a slow typist for your own reasoning;
- the task is **short** (under ~15 minutes solo);
- the task is **deciding** something — what the metric means, which design wins, how a normative
  sentence should read. Delegate a decision and you get a fluent paraphrase of a choice nobody made;
- **you have already delegated this once and got nothing back.** Do not re-delegate a failed
  handoff. Take it back into your own pane.

Pair when the work is **wide and mechanical**: many files, repetitive edits, long test/lint
cycles, pipeline babysitting, migrations.

**Precision work is pairable — paraphrase is the enemy, not precision.** Implementing against a
frozen spec (exact metric definitions, gate IDs, invariants) pairs fine *provided* you fence the
spec file as untouchable and require quoting over restating: "照抄 §5.2 的措辞", "不许改动
coverage 那句", "拿不准就停下来问我，不要自己换个说法". What breaks these tasks is an executor
rewording a definition in good faith — not the difficulty of the definition.

## 0. Preflight

```bash
test "${HERDR_ENV:-}" = 1
herdr --skill
herdr agent prompt --help
```

Not inside Herdr → say so and stop. The installed binary is authoritative over this file.

### pairctl is the dispatch path

This skill ships [`scripts/pairctl.py`](scripts/pairctl.py) as a support script. Agent-skill
layouts may include a `scripts/` directory; that is the supported way to carry this helper.
**Do not enable a global Factory or Cursor hook** to run it, and do not edit
`~/.factory/hooks.json` / `~/.factory/settings.json` for pairing. Invoke the script from this
skill at each dispatch. The one hook this skill does own is the Claude Code `SessionStart`
hook in `~/.claude/settings.json` that runs
[`scripts/claude_session_start_hook.py`](scripts/claude_session_start_hook.py) after
`/compact` or `/clear`; it only calls pairctl (see "Context hygiene is automated" below).

Every Herdr handoff in a pairing session goes through `pairctl`, not a raw `herdr agent prompt`
typed in a shell. pairctl reads the handoff file, assigns `round_id`, and replaces only a
strict `[轮次] round_id=...` header line (other `round_id=` examples in the body stay). It
execs `herdr` with a subprocess argv list (no shell, so backticks are not executed).

`send-round` is two-phase: it first records an uncertain `pending_dispatch` without increasing
`phase_round_count`, then calls herdr. On `type: agent_prompted` it becomes active and counts
the round. Failure paths:

- A: only a definitive pre-delivery failure (`agent_not_found` or failure to start herdr) clears
  pending without counting the round. `agent_prompt_stalled`, timeout, malformed output, process
  death, and other unknown outcomes retain pending because delivery is uncertain. Every later
  command fail-closes and pairctl never resends that dispatch. Inspect the target pane, then use
  `resolve-pending --outcome delivered|not-delivered`; never edit `state.json` by hand.
- B: only a full line matching `[轮次] round_id=...` is rewritten; other `round_id=` strings stay.
- C: `init` has no `--reset` and will not empty an existing state that already has rounds or jobs.
- D: a missing or stale `jobs.tsv` is rebuilt from `state.json`; extra TSV-only rows are dropped.
- E: `rollover --new-session-id` (default `--reason new`) rejects empty values, placeholders
  such as `<id>`, and a repeat of the current session id, and leaves phase/session state
  unchanged. `--reason compact` accepts the same id (in-place compaction keeps it) and bumps
  `compaction_epoch` instead.
- F: `send-round` clears the executor's context first (`--fresh`, the default) and fails closed
  with `fresh_failed` if the pane is not idle or the screen does not confirm a fresh session.
  Nothing is sent and no round is consumed in that case.

```bash
PAIRCTL=/home/tcuni-claw/.agents/skills/herdr-pair/scripts/pairctl.py
python3 "$PAIRCTL" init --planner-pane "$HERDR_PANE_ID"
python3 "$PAIRCTL" send-round --target <executor_pane_id> --file /abs/path/to/handoff.md \
  --executor <executor_pane_id> --scope '<fence>' --acceptance '<command>'
python3 "$PAIRCTL" resolve-pending --outcome delivered  # or not-delivered, after pane inspection
python3 "$PAIRCTL" job-add --round-id <id> --queue <queue> --job-id <id> --label <label> \
  --submitter <pane> --command '<exact command>' --log <log> \
  --expected-artifacts '<paths>' --completion-assertion '<test>' --owner <pane>
python3 "$PAIRCTL" job-update --queue <queue> --job-id <id> --state running
python3 "$PAIRCTL" finish-round --round-id <id> --status accepted
python3 "$PAIRCTL" status
python3 "$PAIRCTL" compact-self [--mode compact|clear]   # queue your own pane's compaction now
python3 "$PAIRCTL" rollover --reason compact --new-session-id <id>   # non-Claude planners, after compaction
```

State defaults to `$XDG_STATE_HOME/herdr-pair/<cwd-hash>` (`~/.local/state/...` when unset).
`state.json` is the source of truth; each state file is written with a lock and atomic replace
(mode `0600`). `jobs.tsv` is a derived view rewritten from `state.json` whenever state loads
successfully under the lock. Do not treat the two files as one cross-file atomic commit.
`init` never wipes rounds or jobs.

### Context hygiene is automated

Slash commands go through `herdr agent prompt` like any other text, and the receiving TUI
executes them. Measured on this box, herdr 0.8.0, 2026-09-07: pi `/new` → "New session
started", kimi `/clear` → "Started a new session", Claude Code `/clear` and `/compact` → run.
Cursor's in-place compact analogue is `/summarize` (user-stated 2026-09-07; `finish-round`
previously failed closed with `no compact command known for agent kind 'cursor'`). A command
sent to a Claude pane that is still working is **queued and runs when that turn
ends**, without cutting the turn short. pairctl uses this in two places:

- **Executor, every round.** `send-round` first runs `herdr agent get` on the target, refuses
  unless it is `idle`/`done`, sends the kind's fresh-session command (pi `/new`; claude, kimi,
  droid `/clear`; codex, opencode `/new`), then polls `herdr agent read --source visible` until
  the screen shows the kind's marker. Only then does the handoff go out, and the round record
  carries `fresh: {kind, command, verified}`. `agent_prompted` on the slash command is *not*
  taken as proof; the screen is. This is why every handoff must be self-contained (§3): the
  executor keeps nothing from the previous round, by design. For a kind pairctl does not know,
  pass `--fresh-command '/…'` plus `--fresh-marker '<screen text>'`; `--no-fresh` sends into the
  existing context deliberately (say why in the round notes).
- **Planner, at the phase boundary.** The `finish-round` that completes round 5 writes the
  checkpoint and then sends your own pane the kind's compact command (claude/pi get
  `/compact <focus instructions naming the checkpoint>`; cursor `/summarize`; droid
  `/compress`; kimi/codex/opencode `/compact`). Because it is
  queued behind your current turn, finish what you were going to say to the user first; the
  compaction happens after. `exit 20` on any later `send-round`/`start-round` re-reports the
  queued command instead of re-sending it. Disable with `init --no-auto-compact` or
  `PAIRCTL_AUTO_COMPACT=0`; trigger by hand with `compact-self` (`--mode clear` sends the
  fresh-session command instead).

After the compaction the phase must be recorded. A **Claude Code planner** gets this for free:
the `SessionStart` hook (`matcher: compact|clear`) runs `pairctl status`, records
`rollover --reason compact|new`, and injects `CHECKPOINT.md` into the fresh context as
`additionalContext`; on `startup`/`resume` it does the same only when a rollover is pending and
the state was touched within 12 hours. Any **other planner** runs
`python3 "$PAIRCTL" rollover --reason compact --new-session-id <id>` itself after its
compaction (the compact-command instruction text says so). A message queued *behind* the compact
command was observed to run before the summary existed, so pairctl never queues a follow-up
through herdr. Instead it spawns `watch-compact-continue`: a detached waiter that polls until
the planner pane has been idle (default 8s, and at least 20s after compact was queued), then
`herdr agent prompt`s the planner to rollover and keep pairing. The user does not have to send
a resume message. Disable with `PAIRCTL_CONTINUE_AFTER_COMPACT=0`.

**exit 20** still means `SESSION_ROLLOVER_REQUIRED`: after five completed rounds the next
`send-round` is hard-blocked and a checkpoint is written. The payload's `planner_compact` field
says whether the compaction was queued (`queued: true`, or the reason it was not). pairctl never
switches sessions, never starts a Droid session, never calls the Factory Sessions API, and never
reads or prints credentials. Nonterminal job rows from `state.json` are copied into the
checkpoint and kept across rollover.

## 1. Resolve the executor

```bash
printf '%s\n' "$HERDR_WORKSPACE_ID" "$HERDR_TAB_ID" "$HERDR_PANE_ID"
herdr agent list
```

`agent list` returns JSON: `agent`, `agent_status`, `cwd`, `foreground_cwd`, `pane_id`,
`tab_id`, `workspace_id`, `terminal_title`. Exclude your own `$HERDR_PANE_ID`.

**Write down your own `$HERDR_PANE_ID` now — it is the return address.** The executor has no way
to find you: nothing in its context names the pane that prompted it, and `herdr agent prompt`
carries no reply channel. Omit it and the executor finishes, reports into its own pane, and you
wait forever on a task that is already done. Every handoff you send must carry it (§3).

**Every agent type in the list is eligible.** Filter on `agent` only when the user named a type
("让 opencode 执行"). When they did not, select on *position and availability* — `cwd`, then
`agent_status` — and never on brand preference. You do not get to decide another agent type is
unworthy; only its track record on this task does (§7).

Prefer, in order: same tab → same workspace + same `cwd` → same `cwd` anywhere. Use a level only
when it yields **exactly one** match; never fall through past an ambiguous level. Always address
the resolved `pane_id`, never the agent name — names repeat across panes, `pane_id` does not.

If the user named a type and several panes match, ask once, listing each candidate's `pane_id`,
`tab_id`, `cwd` and `terminal_title`. If the named type is not live anywhere, say so and offer the
candidates that are — do not silently substitute.

Resolve how broadly the user's executor choice applies:

- “让 Pi 执行这一轮/这个修改” names the writer for that round only.
- “整个任务只能由 Pi 修改” makes Pi the exclusive writer until the user changes it.
- “按任务难度派给不同执行者” authorizes the Planner to choose a different writer per round.

Do not treat a round-level choice as a project-wide lock, and do not treat general delegation as
permission to replace an explicitly exclusive writer. Record the chosen writer in each `round_id`.
A specialist may diagnose or verify read-only without taking the writer seat.

**Hard rule — one active writer per working directory.** Before sending, list all live agents whose
`cwd` is your working directory. Pick one writer and park every other agent that has or may still
have a write-capable prompt (§6). A read-only Verifier may share the directory only during a frozen
review epoch, never while the writer is active. `idle` is not proof that an old prompt cannot resume.

## 2. Cut the work into rounds

One handoff = one round = one diff you can read end-to-end and sign. Do this split before
writing any prompt; it decides how many prompts there are.

A round is correctly sized when all of these hold:

- **one fence** — the files it may touch fit on one line (§3), and no later round reopens them;
- **one acceptance command**, one literal expected result;
- **standalone verifiable** — you can sign its diff without knowing what round N+1 does;
- **no carried-forward values** — every input is in the prompt or already in the repo. If round
  N+1 needs a number round N produced, *you* verify it (§5) and *you* put it in the next prompt.
  A value that travels between rounds unread is how a fabricated number gets laundered past §5.

Splitting is **sequential, not fan-out.** One executor per working directory (§1) — never cut the
work into parallel rounds and fire them at several panes sharing a cwd. If the work is genuinely
parallel, give each executor its own worktree, and still drive them one at a time: you have to
read every diff yourself, and that is the real serial resource.

Cut along **files or mechanical units**, not along phases of thought. "Rewrite the header block in
these 12 docs" is a round. "Define the metric, then apply it" is not two rounds — the first half is
judgment work that should not be delegated at all (§When NOT to pair).

One round means you do not need this loop — send, verify, close out.

### Round and session budget

Do not let a pair silently become a day-long orchestration. `pairctl.py` enforces this:

- Give every handoff a unique `round_id` via `send-round` and record its Executor, scope and
  acceptance command.
- After 3 rounds, pairctl writes a short checkpoint with accepted artifacts, open blockers and
  active background jobs.
- At 5 rounds, stop. The `finish-round` of round 5 exits 20 with `SESSION_ROLLOVER_REQUIRED`,
  writes the checkpoint, and queues your own pane's compact command (§0, "Context hygiene is
  automated"). Finish your report to the user in that turn; the compaction runs after it. Either
  close the phase, take the work back, or tell the user why another phase is worth pairing. Do
  not simply send round 6 by hand.
- The checkpoint, not chat history, is the new source of context after the boundary. In Claude
  Code the `SessionStart` hook records the rollover and injects the checkpoint; in any other
  planner run `pairctl.py rollover --reason compact --new-session-id <id>` first thing after
  the compaction. If the compaction was not queued (`planner_compact.queued: false`), run
  `pairctl.py compact-self` or ask the user to run that kind's compact command (cursor `/summarize`).
- The executor's context is cleared before every round by `send-round`. Never rely on it
  remembering round N when you write round N+1; the handoff carries everything (§3).
- Do not busy-poll. Ask for an ETA once, check once after that ETA, send one stop/report request if
  overdue, then take the work back. Repeated `agent get`/`agent read` loops are not progress.

### Audit the governing spec — it is yours, not the executor's

The spec is fenced **read-only** for the executor (§3), but that fence is not an excuse to leave it
unread. Cutting rounds means reading it end-to-end, and **specs contain defects**: an acceptance
item that is literally unsatisfiable, a prohibition whose object drifted between sections, a
cross-reference to a file that already exists. If the executor hits one of these, it will do the
worst possible thing — quietly satisfy the letter, and break the behavior the same spec requires.

When you find a defect:

- **do not have the executor fix it**, and do not fix it silently yourself mid-round;
- name it to the user as a *spec* defect, not an implementation one, with the conflicting passages
  quoted and the section that carries scope authority identified;
- get the correction authorized, land it as its own dated annotation, and keep the acceptance item
  **mechanically checkable** after the rewrite. A back-check you have to interpret is not a
  back-check.

> **Observed, this repo, 2026-08-24:** a spec's §11 back-check demanded a file not exist. The same
> prohibition appeared twice earlier qualified as "no **weight constants** in that file" — §11 had
> dropped the qualifier, flipping the object from the constants to the file. The file had been
> introduced a week before the spec and held the truncation bound that spec's own §5.4 depended on.
> Read literally, passing the check would have broken the deliverable.

> **Observed, pi-grok-theme, 2026-08-25:** a frozen measurement formula — `rate = output_tokens ÷
> (end.timestamp − start.timestamp)` from event payloads — was literally unsatisfiable: every
> provider sets the message timestamp once at stream creation and both events carry the same
> object, so the duration was identically zero and the spec's own `≥ 0.5s` display threshold could
> never fire. All twelve unit tests passed because they injected synthetic timestamps. Type
> definitions proved the field *existed*; nothing proved it *carried the quantity*. Before freezing
> any measurement formula into a spec, walk the real data path and confirm the quantity exists and
> varies there — a green suite built on injected fixtures launders an unsatisfiable formula all
> the way to release.

## 3. Write a self-contained handoff

**The executor does not inherit your context.** It may not read the repo's `AGENTS.md`, and
delegated subagents routinely skip global rules files. Anything that matters must be *in the prompt*.

Because the seat is type-agnostic, you must assume **zero inherited rules**. Each agent type reads
its global rules from a different hook, and some read none at all in this position:

- the hooks differ per type (`~/.claude/CLAUDE.md`, `~/.config/opencode/AGENTS.md`,
  `~/.codex/AGENTS.md`, `~/.factory/AGENTS.md`, `~/.omp/agent/RULES.md`, `~/.hermes/SOUL.md`, …);
- **`cursor` cli scans the workspace only** — with no `AGENTS.md` in the project root it starts with
  no global rules whatsoever;
- a worktree is not the project root, so a root-level symlink may not be on its path either.

Do not probe which hook your executor honors, and do not shorten the prompt because you believe its
type "already knows". Restate the rules every time. A redundant reminder costs a few lines; a missed
one costs a wrong-place write or an unqueued heavy job.

Always include, verbatim:

- **round identity** — a unique `round_id`; reports and artifacts must repeat it;
- **working directory** (absolute) and, in a worktree, "run everything here, do not `cd` to the repo root";
- **environment rules** — the `slot` queue for anything >1 min / >2 G RAM / heavy NFS IO, the
  `slot audit` + `slot status` preflight, and the ban on writing under `/tmp`;
- **scope fence, in three parts** — the files it may **edit**, the files/dirs it may **create**,
  and an explicit list of what it must not touch (`src/`, untracked scratch dirs, unrelated docs).
  Keep edit and create separate: a fence that only lists editable files silently forbids the new
  test file the task requires, and an executor that needs one will either stop or widen the fence
  on its own. Say where new files go, or say plainly that none are expected;
- **stop conditions** — "do not commit", "do not push", "do not open a PR", "do not merge",
  whichever apply;
- **acceptance** — the literal command and the expected result (`make ci` exit 0, coverage ≥ 84%);
- **background-job contract**, when applicable — queue, label, command, log, expected artifacts,
  completion test, and who may cancel or retry it;
- **the return address** — your `$HERDR_PANE_ID` (§1), plus the literal command to reach you;
- **report contract** — what to send back (below).

Template:

```text
[轮次] round_id=<unique-id>
[目标] 一句话说清要达成什么，不要说怎么做。
[工作目录] /abs/path —— 所有命令都在这里跑，不要 cd 到仓库根。
[可以改] docs/a.md, docs/b.md
[可以新建] tests/contracts/test_x.py；其他新文件一律先问我
[不许动] src/, tests/, .ot-scratch/, 任何未跟踪文件
[环境] 超 1 分钟 / 超 2G 内存 / 重读写 NFS 的命令走 slot；开跑前先 slot audit + slot status；
       中间文件不许放 /tmp，放当前目录下的临时子目录。
[停在哪] 改完就停。不要 commit / push / 开 PR。
[验收] <literal command>，期望 <literal expected output>
[后台作业] 无；或写明 queue/label/command/log/expected artifacts/completion/cancel owner。
[回报] 用 `herdr agent prompt <你的 pane_id> '<短回报或报告路径>'` 发回给我，内容见下方回报契约。
       完成时和被卡住时都要主动发 —— 不要只在自己的窗口里写结论。
       正文控制在几 KB 以内：prompt 是单个 argv 参数，超 131,071 字节（≈43,600 汉字）
       会被 shell 直接拒掉、什么都发不出去。长报告/全表/全日志落盘，回报里给路径 + 3–6 行摘要。
```

### The prompt is one argv argument — 131,071 bytes, hard

`herdr agent prompt <TARGET> <TEXT>` passes `TEXT` as a **single** command-line argument. Linux caps
one argument at `MAX_ARG_STRLEN` = 128 KiB **including the NUL**, so the largest prompt that execs is
**131,071 bytes**. Measured on this box, 2026-08-25: 131,071 delivered, 131,072 failed.

Three things about that limit that will bite you:

- **`ARG_MAX` is a red herring.** `getconf ARG_MAX` reports 2,097,152 here. It bounds the *whole*
  argv+env block, not one argument. Do not size a prompt against it. The per-argument cap is not
  raisable — no `ulimit`, no flag.
- **It counts bytes, not characters.** Chinese is 3 bytes/char in UTF-8, so the ceiling is roughly
  **43,600 汉字**. A report that "looks like 40k characters" can be over.
- **The shell rejects it, so `herdr` never runs.** You get `argument list too long: herdr` from
  zsh/bash — no JSON, no `agent_prompted`, nothing delivered, no partial send. Failure is clean, but
  it is invisible to anything that only greps the output for an error *code* (§4).

`herdr agent prompt` has **no `--file` and no stdin mode** — check `--help` on your build before
assuming otherwise. So the fix is not a bigger prompt, it is a smaller one:

> **Land the payload as a file; send a pointer.** Write the artifact into the working directory
> (`.handoff/<topic>-<date>.md` is a good convention — it survives the session and is greppable
> later), then send a prompt that gives the **absolute or repo-relative path, the instruction to
> read it in full, and a 3–6 line executive summary** so the recipient can tell whether it is urgent
> before opening it.

Pointer prompts beat inline payloads well below the kernel limit anyway. A 100 KB prompt is legal and
still a bad idea: it lands in the executor's context in one undigested block, competing with the work.
**Keep handoff prompts to a few KB.** If yours is heading past ~8 KB, that is the signal to split it
into a file plus a pointer, not the signal to check whether it still fits.

The same rule binds the **executor's report** back to you (below) — a long report is a file plus a
pointer, never a wall of text that may not exec.

> **Observed, this repo, 2026-08-25:** an executor finished a four-section completion report and tried
> to push the full text back through `herdr agent prompt`. 367 KB — nearly 3× the cap. The send died
> in the shell. It recovered correctly (wrote `logs/09DR12_completion_report.md`, sent a short summary
> naming the path), but the round-trip was lost. Nothing in this skill had warned it.

### Report contract

Demand **evidence, not adjectives**. Require:

1. the exact `round_id`, start state and end state;
2. `git status --short` and `git rev-parse HEAD` (paste raw output);
3. `git diff --stat` for what it changed;
4. the acceptance command's **actual** output tail and exit code;
5. **everything it did not do** — not just hard failures, but **every deferral, every assertion it
   weakened or skipped, every fallback it took**. Ask for it in those words. "Anything you could
   not do" reads to an executor as "did anything crash", and a test quietly relaxed from an exact
   match to a `>= 0` is not a crash. Spell it out: "没做到的事，**含所有推迟项、绕过的断言、
   降级的做法**";
6. **assumptions it made** — every judgment call on something you did not state;
7. **a measurement record for every number it reports** (below);
8. every background job's queue, job ID, label, command, log, current state, expected artifacts,
   completion test, and whether it was cancelled or retried.

Explicitly: "不要报告『已完成』；贴出上面各项的原始输出。"

**Not every working directory is a git repo.** Items 1–2 assume one; plenty of pipeline, panel-design
and data directories are not versioned at all, and there the whole of §5's SHA-and-diff machinery is
unavailable. Say which regime you are in *when you write the prompt*, and in the unversioned case
demand a before/after inventory of the exact scope fence. For small scopes this is
`ls -la --time-style=full-iso`; for large data directories, write a machine-readable inventory with
relative path, type, size and nanosecond mtime, plus SHA-256 for control files and final artifacts.
Diff the inventories and reject paths outside the allowlist. Also require `wc -l` for tables and the
exit code of every command. Fix acceptance artifact paths in the prompt so you can verify them
yourself. Without version control you cannot recover from a bad overwrite, so **require `cp -p`
backups for pre-existing files that may be overwritten**, named in the report.

### Background jobs need a ledger

Submitting a job is not completing a round. For every `slot`, scheduler, detached or long-running
job, record this ledger before handing control back:

```text
round_id | queue | job_id | label | submitter | exact command | log |
expected artifacts | completion assertion | state | cancel/retry owner
```

The Executor may submit only the job explicitly authorized in the handoff. A successful submission
response proves only that the scheduler accepted it. The Planner verifies the job ID and log path
and records the row with `pairctl.py job-add` / `job-update`. `state.json` is the source of
truth; `jobs.tsv` is rewritten from it on every successful load and must not be treated as a
second source of truth.
On session rollover, pairctl copies all nonterminal ledger rows into the checkpoint and keeps them
in `jobs.tsv`. A new agent may inspect them, but must not cancel, retry or replace a job unless
the user or named owner authorized that action.

**Cap the report at a few KB and point at files for the rest** (§3, 131,071-byte limit). Put it in the
prompt in those words: "回报正文控制在几 KB 以内；长表格、完整日志、完成报告一律落盘，回报里给路径 +
3–6 行摘要，不要把全文塞进 prompt。"

### Numbers need a measurement record

Any value the executor supplies that will end up in a commit, a doc, or your report to the user —
a hash, a count, a distribution, a coverage figure — must arrive with **the script and the exact
command that produced it**, not just the value. Then **recompute it yourself**: your own script,
your own baseline (`git worktree add <dir> <base-sha>` when the number is a base-vs-HEAD
comparison). Do not re-run the executor's script — a shared fixture is a shared error.

Two numbers that disagree is a *fixture* question before it is an *honesty* question (§7).

## 4. Send

Canonical path — every pairing dispatch:

```bash
python3 /home/tcuni-claw/.agents/skills/herdr-pair/scripts/pairctl.py send-round \
  --target <pane_id> --file /abs/path/to/handoff.md
```

`send-round` is the only supported way to consume a pairing round. It fail-closes: pending
until `agent_prompted`, then one active row. Only a definitive pre-delivery failure clears
pending automatically. A stalled, timed-out, malformed, interrupted, or otherwise ambiguous
dispatch is never resent; inspect the target pane and use `resolve-pending` explicitly.
Exit 20 is the rollover gate described in §0. Do not wrap the handoff in shell double quotes;
pairctl passes the file contents as one argv element.

Before the handoff leaves, `send-round` clears the executor (§0, "Context hygiene is
automated"): `agent get` must say `idle`/`done`, the kind's `/new` or `/clear` is sent, and the
screen must show the fresh-session marker. A `fresh_failed` result means nothing was sent and no
round was consumed; read its `error` (pane still working, unknown agent kind, marker not seen),
fix that, and rerun. Do not reach for `--no-fresh` to get past it unless you want the executor
to keep its previous context on purpose.

Underlying CLI (pairctl invokes this; do not type it for a counted round):

```bash
herdr agent prompt <pane_id> '<message>'
```

`--wait` only when you need the result inside this turn. Read the help text carefully:

> `--wait` **does not track turns.** If the agent is already `working`, that *previous* turn's
> completion can satisfy the wait. A non-working start with no state change in 5000 ms returns
> `agent_prompt_stalled`.

So: `--wait` returning `idle` is **not** evidence your task ran. It is evidence *some* turn ended.
Never treat it as completion.

For asynchronous work, prefer the report contract over polling. Record the ETA from the Executor,
check once after it passes, and if no report arrived send one concise stop/report request. After a
second miss, take the task back instead of continuing to poll.

Confirm delivery only on a successful `type: agent_prompted` response. If the command fails, say
it failed — do not claim it was sent.

**`agent_prompted` proves the pane received it, not that the pane is who you meant.** The response
echoes the target's `pane_id` and `tab_id` — read them and check they are the ones you intended.
Panes get recycled: the agent occupying a pane can change type between two `agent list` calls, and
a pane mid-swap is **absent from the listing entirely**. If the executor you expect is missing,
that is a pane in transition, not a vanished agent — re-list before concluding anything. Never
substitute a same-type agent from a different tab to fill the gap: "the only X in this project" is
a guess about identity, and the user asked for a seat, not a type.

> **Observed, 2026-08-28:** the user said 派给本 tab 的 agy. A listing taken while that pane was
> swapping showed no agy in the tab, so the send went to the only agy sharing the project cwd —
> in a different tab. Delivery succeeded, the response said `tab_id: w2:t1F`, and that mismatch
> was visible in the output at the time. The wrong executor did the work correctly; the cost was
> a concurrent-writer risk on a file the intended executor was about to be handed.

**Do not pipe the send through `tail`/`head` and glance at it.** Two different failures look nothing
alike: a bad target returns JSON (`{"error":{"code":"agent_not_found",…}}`) from a `herdr` that ran,
while an oversized prompt (§3) returns `argument list too long: herdr` from the *shell*, because
`herdr` never execed. Both mean nothing was delivered. Check for the positive `agent_prompted`
response, not for the absence of a string you happened to think of.

### Quote with `'…'`, never `"…"` — backticks get executed

Wrapping the message in double quotes hands it to the shell for expansion first. Handoffs are
written in Markdown, and Markdown paths are written in backticks — so `` `docs/runbook.md` ``
becomes a **command substitution**. The shell runs it, the command fails, and the *empty result*
is spliced into your message. `$VAR` and `$(…)` go the same way.

This failure is worse than the size limit, because it **succeeds**. You get a clean
`type: agent_prompted` back. The only trace is a few lines on stderr:

```
(eval):1: no such file or directory: docs/cnv_probe_runbook.md:2349-2350
(eval):1: permission denied: docs/9dr12_patch_proposal.md
{"id":"cli:agent:prompt","result":{…,"type":"agent_prompted"}}
```

The executor receives a work order **with the file paths hollowed out** and starts on it. A send
that fails you re-send; a send that is silently gutted you do not.

So: wrap the message in **single quotes** (keep ASCII `'` out of the body — use 「」 for Chinese
quoting), or put the order in a file and send only a pointer, which is what §3 already tells you
to do for anything substantial. **Files are immune to all of this** — that is the second reason
the file-plus-pointer pattern is the default, not just a size workaround.

And read the stderr, not only the JSON. `no such file or directory` next to an `agent_prompted`
means the message was corrupted in flight: supersede it immediately with an explicit
「上一条作废，以本条为准；若已动手先回滚」 rather than letting the executor act on fragments.

### Stable review epochs

An independent review is valid only against a frozen artifact state:

1. Park the writer and confirm its report names the `round_id`.
2. Capture `HEAD` plus `git status --short` in Git, or the scoped inventory digest in a non-Git
   directory. Call this `review_epoch`.
3. Send the Verifier the `round_id`, `review_epoch`, read-only fence and acceptance ledger.
4. The Verifier checks the epoch before and after review. Any drift means `STALE_REVIEW`, not pass
   or fail.
5. If the writer changes anything, invalidate all earlier review conclusions and create a new epoch.

Never ask a Verifier to “keep reviewing” while the Executor fixes files. Pause it first, then restart
from the new epoch. A conclusion against an unknown mixture of versions does not count.

## 5. Verify by artifact, never by status

This is the step that gets skipped, and skipping it is how a pairing session produces nothing while
reporting success.

Check the **repository**, not the agent:

```bash
git status --short
git rev-parse HEAD          # did the SHA actually move?
git diff --stat <base>...HEAD
git diff --check
```

Then **read the diff line by line.** Not skim — read. You are about to sign it.

Reject and re-drive when the diff contains:

- **any number, threshold, weight or ID you did not supply** — executors invent plausible values;
- **identifiers that do not exist** — `rg` every file path, symbol and gate ID it introduced;
- claims that contradict your spec (swapped gate IDs, wrong module landing, wrong formula);
- files outside the scope fence;
- a commit, push, or PR you did not authorize.

> **Observed, this repo, 2026-08-24:** an executor reported success while `HEAD` had not moved from
> `311b093` — zero files changed, zero commits. A later round wrote confidently wrong content into
> two docs: the authoritative module was named as `alignment/off_target_metrics.py` when the spec
> said `alignment/off_target.py`, and two gate IDs (G6/G7) were swapped. Both read fluently. Both
> would have shipped without a line-by-line read.

### No git? Verify the artifacts directly

The header says *artifact*, not *commit*, on purpose. In an unversioned directory the principle is
unchanged and only the commands move:

```bash
ls -la --time-style=full-iso <every file the fence allowed>   # mtime + size is your diff
sha256sum <output artifacts>                                  # compare to the reported digests
wc -l <tables>                                                # row counts you predicted
diff <(…) <(…)                                                # against the .bak the round was told to keep
```

Read the **content** of what changed, not just that it changed — the same line-by-line duty as a diff.
And be sharper about scope than you would be with git: there is no `git status` to reveal a stray write
outside the fence, so diff the before/after inventory and inspect anything whose path or metadata
changed. For large generated datasets, hash final artifacts and control files rather than blindly
hashing every multi-gigabyte intermediate.

### An explanation is a claim — check its precondition

The §5 list catches invented *values*. It does not catch an invented *reason*, which is the more
durable failure: a wrong number gets disputed, a wrong explanation gets adopted and quoted onward.

Executors reach for the nearest legitimating clause in the code or spec — a documented escape hatch,
a "known limitation", a tolerance. The clause usually is real. What goes unchecked is whether its
**precondition holds on this data**. So check that separately, against the artifact:

- Quote the clause's condition verbatim from the source, then evaluate it yourself over **every**
  affected record — not a sample, not the three the executor listed.
- **Bulk-parse the enumerated lines and let them outvote the summary line.** A report that lists N
  anomalies individually is self-checking: the detail rows are evidence, the one-line roll-up on top
  is narration. When they disagree, the rows win.
- **Cross-check the executor's numbers against *each other*, not only against your own recomputation.**
  Internal contradiction is the cheapest defect to find — it needs no fixture, no rerun, no baseline —
  and it is conclusive: at least one number is wrong no matter who produced it. Look hardest at pairs
  where one is a *residual* (deficit, unsatisfied count, remaining budget, leftover) and the other is
  an independent recount of the same thing. A residual of **0** sitting next to a recount reporting a
  shortfall is the canonical shape, and it means the accounting is broken, not that one view is
  "stricter".
- If the clause's condition is a threshold ("fewer than K available"), compute the distribution of the
  quantity. "Zero of 1,164 records meet the condition" is a one-command refutation.

> **Observed, this repo, 2026-08-25:** a set-cover step reported 1,164 events short of their K=4 quota
> and explained them as "随机实现" — the script's own docstring does say events with **fewer than 4
> surviving candidates** are random realizations, not defects. Parsing all 1,164 detail lines showed
> **1,164 of 1,164 had ≥ need survivors**, so the clause covered none of them; 409 had ≥4 available and
> selected **zero**. The same run also printed `unsat_slots = 0` — the solver's own deficit counter,
> which can only reach zero if every event was served in full — beside a recount of 3,140 unfilled
> slots, and the recount used the *looser* of the two criteria, so it should have found fewer shortfalls,
> never more. That pair alone was conclusive before any hypothesis about the cause. The docstring had
> also required these events be "单独列出供裁定，不自动处置"; they had been auto-disposed. Nothing here
> required rerunning anything — only reading the artifact against the clause it invoked.

**When you find this, freeze the affected section rather than fixing it.** Downstream numbers computed
from a broken accounting are neither pass nor fail — they are **UNKNOWN**, and saying so is the whole
value. Send the executor the refutation, the ruled-out hypotheses (so it does not re-walk them), and at
most one *labelled-unproven* lead; then let it locate the defect before anyone decides whether to
re-run. An executor handed a lead as if it were a conclusion will confirm it.

### Check the failure you warned about first

The hazard you spelled out in the work order is the one most likely to come back in the receipt —
an instruction is not a guarantee, and a receipt that reads "done" is written by the same agent
that missed it. So verify **your own warning** before anything else, and expect the evidence to be
sitting in the receipt already.

> **Observed, this repo, 2026-08-26:** the order said to anchor a cross-reference by section
> heading, "**不要写死行号**（追加内容本身会让行号漂移）". The executor wrote `L3006` — and its own
> receipt quoted the hunk `2350a2351,2353`, three inserted lines, which had moved the target to
> L3009. L3006 now named a *different* backlog entry. The proof of the defect was inside the
> report claiming success.

Generalize it in the handoff rather than re-warning per task: **cross-references use headings or
anchor text, never line numbers** — any line number read before an edit is stale after it, and the
edit that invalidates it is often the same one being written.

## 6. Concurrent writers

Symptom: your own edit tool warns the file changed on disk, or `git status` shows files you never
touched.

```bash
herdr agent list        # who else has this cwd?
git status --short
git diff                # read the foreign content before doing anything
```

Response, in order:

1. **Park the other agents first** — `herdr agent prompt <pane> '停下，不要再修改 <dir> 下的任何文件，
   等我的下一条指令。'` A pane can still be executing a *stale* prompt from an earlier round; idle now
   does not mean it will stay idle.
2. **Do not discard.** `git checkout -- <file>` throws away work you have not read, and will likely be
   refused as irreversible local destruction anyway. Prefer in-place edits: correct each wrong line so
   the end state is one you can vouch for, non-destructively.
3. **Take ownership of the whole diff** before committing. Any line you cannot defend gets rewritten
   or removed.

**Never** use bare `git stash` / `git stash pop` — the stash stack is shared across worktrees and
sessions, and you will pop someone else's work. If you must stash: `git stash push -u -m "<unique-tag>"`,
capture the SHA from `git stash list --format='%H %gs'`, restore with `git stash apply <sha>`, drop by
re-finding the tag.

**Worktree note:** `.git` is a *file*, so `.git/info/exclude` does not exist. Use
`$(git rev-parse --git-common-dir)/info/exclude`.

## 7. Quality gate — the kill-switch

Track quality across rounds. **Stop and tell the user** — do not silently absorb the work — when any
of these fires:

| Signal | Meaning |
|---|---|
| Reported done, `HEAD` unmoved / no diff | The executor is not actually executing |
| Fabricated numbers or non-existent identifiers | It is filling gaps with invention |
| Same instruction missed twice | It is not reading the prompt |
| Scope fence crossed after being told | Instructions are not binding on it |
| Explanations dissolve on inspection, twice | It is narrating over unread data, not analysing it |
| You are rewriting most of its output | Pairing now costs more than solo |

Report to the user as: what was asked, what came back, which signal fired, and the concrete
evidence (SHA, diff, quoted output). Then recommend either a stronger model/agent or taking the
task back into your own pane. **Do not keep re-prompting a failing executor** — that burns the
user's time and yours.

Finishing the work yourself is always a legitimate outcome. Say that you did.

### Irreproducible is not the same as fabricated

The fabrication row is the one you will misfire on. When a number the executor reported does not
reproduce on your machine, you have **two** hypotheses, and invention is the second one to test:

1. **different fixture** — you measured something else. Fixtures with defaulted, non-exposed
   parameters are the usual culprit: a helper that hardcodes a field and only lets the caller vary
   the row count will happily produce two honest, different hashes;
2. **invention** — the number never came from a run at all.

Distinguish them by **asking for provenance before judging**: the script, the command, the raw
output. Word the ask so that "作废" is a cheap answer — "若你也复不出来，就说这个数作废，不要
补一个解释". An executor that produces a runnable script whose output you can reproduce has given
you a fixture mismatch, not a fabrication; both numbers are real and neither belongs in the commit
until you have recomputed the right one (§3, measurement record).

The row fires when the number **cannot be traced to any run** — no script, shifting explanations,
or a value that entered code or docs unmeasured. It does not fire on a mismatch you have not yet
investigated, and it does not fire on a number that was measured, disputed, and withdrawn.

## 8. Close out

You own the ending. Before reporting to the user:

- run the acceptance command **yourself** — do not trust a pasted result;
- `git diff --check`; back-check every reference the diff introduces;
- stage only the task's files; write the commit message yourself in the repo's style;
- hold irreversible steps (push, merge, delete) for explicit user authorization — a completed
  background job is a system notification, not approval;
- reconcile the background-job ledger: every row must be terminal or explicitly carried into the
  phase checkpoint with its owner and next completion check;
- **walk the spec's acceptance list item by item and mark each one pass / fail / not-run.**

That last one is not optional and not a summary. Enumerate *every* acceptance item the governing
spec names, including the ones no test covers — a real-data run, a figure someone has to eyeball,
a number product has to sign off. An item that cannot be run yet is **not-run**, and not-run is a
perfectly good outcome to report; **silently omitting it is not.** A close-out that lists eight
greens and never mentions the ninth item reads as complete, and that is exactly how an unmet gate
gets merged. Carry the not-run items into the PR description too, under a heading a reviewer
cannot miss, and say what still has to happen before the gate closes.

Final report to the user: **commit SHA, file list, verification results, the acceptance ledger,
open items.** Attribute honestly — say which parts the executor produced and which you wrote or
rewrote.

## If you are the executor

Same skill, other seat. Whatever your type, when another agent hands you a scoped task:

1. **Work the fence, not the goal.** Touch only the files listed. If the task cannot be done inside
   the fence, stop and say why — do not widen it and do not "fix things while you are in there".
2. **Do not invent.** No thresholds, weights, IDs, file paths or symbols the Planner did not supply.
   If a value is missing, that is a blocker to report, not a gap to fill. Fabrication is the single
   fastest way to get the pairing killed (§7).
3. **Obey the stop conditions literally.** "Do not commit" means do not commit, even when the work
   looks finished and committing feels helpful.
4. **Report evidence, not adjectives.** Paste the raw output of `git status --short`,
   `git rev-parse HEAD`, `git diff --stat`, and the acceptance command with its exit code. Never
   answer "已完成" alone — the Planner is going to check the repository anyway, and a claim that the
   diff contradicts costs you the seat.
5. **Send the report back, do not just write it.** Finishing your turn does not notify anyone.
   Use `herdr agent prompt <planner_pane_id> '<短报告或报告路径>'` — the prompt should name the pane; if it
   does not, ask for it before you start. Send when you are blocked, too, not only when you are
   done. A report that only exists in your own pane is a report nobody received.
   **Keep it under a few KB.** The prompt is one argv argument and dies above **131,071 bytes**
   (≈43,600 汉字) with `argument list too long` — from the shell, so nothing is delivered and you get
   no JSON telling you so. Long reports, full tables and logs go to a file in the working directory;
   send the path plus a 3–6 line summary. Do not discover the limit by hitting it.
6. **List what you did not do.** Every deferral, every assertion you weakened or skipped, every
   fallback you took — not only the things that failed outright. A test you relaxed to keep the
   suite green is the single most important line in your report.
7. **Surface every assumption you made.** This is the item that saves the deliverable.
8. **Every number you report needs a runnable command behind it.** If the Planner cannot reproduce
   it, it does not ship. If you cannot reproduce your own number, say it is withdrawn — do not
   supply an explanation for it.
9. **Do not explain an anomaly with a clause you have not evaluated.** Citing a docstring's escape
   hatch, a "known limitation" or a tolerance is a *measurement*, not a quotation: state the clause's
   condition, then report how many affected records actually meet it. If the answer is "I did not
   check", say the anomaly is unexplained — that is a useful report. A confident wrong reason costs
   the Planner more than an honest open question, because it gets believed and quoted onward.
10. **Sanity-check your numbers against each other before sending.** If a residual counter (deficit,
   unsatisfied, remaining) says zero while another line reports a shortfall of the same thing, do not
   ship either number with a story reconciling them — report the contradiction as the finding.
11. **A reason is a claim too — verify its precondition before you lean on it.** "File X does not
   exist, so I wrote to Y instead" needs a `find` that actually covered X, not one directory you
   guessed. A wrong reason attached to a right outcome is still damage: the reviewer reads it as
   evidence you looked, and stops looking themselves.
12. **Cross-reference by heading or anchor text, never by line number.** Any line number you read
   before an edit is stale after it — and the edit invalidating it is usually the one you are
   writing. This applies to your report as much as to the file.
13. **Environment rules bind you even if your global hook never loaded them.** If the prompt states a
   queue (`slot`), a scratch-directory rule, or a working directory, follow it as written.
14. **Repeat the `round_id` in every report and artifact ledger.** Do not report against a different
    or stale round.
15. **If you are the Verifier, enforce the review epoch.** Work read-only, check the epoch before and
    after, and report `STALE_REVIEW` if anything drifted. Never approve while the writer is active.

If a prompt arrives that is stale — it references a state that no longer holds, or repeats work
already landed — do not execute it. Say so and ask. A stale prompt executed confidently is how two
agents end up overwriting one file.

## Common requests

| User wording | Behavior |
|---|---|
| “你负责规划和审核，让 <任意 agent> 执行” | Full loop: §1–§8, Planner signs the result |
| “任务很大，你拆一下再派” | §2 切轮次，一轮一个 handoff；串行驱动，不要同 cwd 并发派发 |
| “协同两个 agent”, no type named | Planner seat is yours; pick the executor by `cwd` + availability, not by type |
| “按不同难度派给不同执行者” | Choose the best writer per round, record it in `round_id`, and preserve one active writer per cwd |
| “让 A 执行、B 独立验收” | A writes that round; freeze a review epoch before B reads; any later write invalidates B's conclusion |
| “这是长时间 slot/后台任务” | Add a background-job ledger row and carry nonterminal rows through every checkpoint/session |
| Pairing reaches round 5 | `finish-round` exits 20, writes the checkpoint, and queues your own compact command (cursor `/summarize`; claude/pi `/compact …`; droid `/compress`); finish your report, let it run. pairctl then waits for the planner pane to go idle and prompts it to rollover + continue. Claude Code also records rollover from SessionStart. Disable auto-continue with `PAIRCTL_CONTINUE_AFTER_COMPACT=0` |
| “每轮都要我手动去 worker 那边 /clear” | Not any more: `send-round` clears the executor (`/new` / `/clear` per kind) and verifies the screen before sending. `fresh_failed` = nothing sent; read the error |
| “/compact 之后它没接着干” / Cursor `/summarize` / “为什么又停下了” | pairctl now waits for idle after compact and prompts the planner to continue; you should not have to ping it. If it still stops, check `compact-continue.log` next to the pairing state and `PAIRCTL_CONTINUE_AFTER_COMPACT` |
| Named type is not live anywhere | Say so, offer live candidates, do not silently substitute |
| “让它把每次的执行结果的结论返回给你” | Put your `$HERDR_PANE_ID` in the prompt (§1); enforce the §3 report contract; verify per §5 before accepting |
| “它跑完了，为什么没发回给你” | You omitted the return address (§1). The work is likely done — go read the repo, then re-send the report contract with the pane id |
| “这个数对不上” | Ask for the script and command first (§7). Fixture mismatch before fabrication |
| “全文发不出去 / argument list too long” | §3 上限 131,071 字节（单个 argv 参数）。落盘 + 指路，不要想办法把全文塞进 prompt |
| “这个目录不是 git 仓库，怎么验” | §5 无 git 分支：`ls -la --time-style=full-iso` + `sha256sum` + `wc -l`；并在派活时就要求覆盖前留 `.bak` |
| “它给的理由听着挺合理” | §5「解释也是断言」：先把免责条款的**前提条件**在全量数据上验一遍，再看它给的几个数彼此矛不矛盾 |
| 送出去返回了 `agent_prompted`，但对方像是没收到完整内容 | §4：用了 `"…"` 包正文，Markdown 反引号被 shell 命令替换吃掉。看 stderr 有没有 `no such file or directory`；立即「上一条作废」+ 落盘指路重发 |
| “我在工单里明明写了不要 X，它还是 X 了” | §5「先查你警告过的那条」。指令不等于保证，且证据往往就在回执自己贴的 diff 里 |
| “质量太低就停下来告诉我” | §7 kill-switch is armed; report the signal and evidence, do not push through |
| “把这个结论同步给 X” | Wrong skill — use `herdr-handoff` |
| Executor already failed this task once | Do not re-delegate. Do it in your own pane and say so |
