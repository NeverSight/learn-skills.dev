---
name: acpx-faq
description: Run coding agents (codex, claude, agy) through the acpx ACP CLI - one-shot dispatch into named sessions you can watch live. Use before launching or prompting a subagent, or when a command fails, a session is missing, or a prompt is lost.
metadata:
  version: "0.11.0"
  categories: "agents, operations"
  topics: "acpx, acp, agent-orchestration, troubleshooting, headless-agents"
  upstream: "acpx@0.21.1, @agentclientprotocol/claude-agent-acp@0.100.0, @agentclientprotocol/codex-acp@2.5.0, agy@1.5.0, agy_acp_server@1.4.5"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/acpx-faq
    emoji: "🔌"
---

# acpx FAQ

Drive coding agents headlessly through [acpx](https://github.com/openclaw/acpx) (>= 0.19.3).

## Syntax authority

Syntax comes from the binary, not this file. `acpx --skill show acpx` is the vendor
reference (~43k chars) and the tiebreaker on command shape - do NOT dump it into the
transcript. Retrieve in this order:

1. `acpx --help` / `acpx <cmd> --help` - the flags you are about to compose.
2. One topic: `acpx --skill show acpx | rg -B2 -A12 '<term>'`, or a section:
   `acpx --skill show acpx | sed -n '/^## Sessions/,/^## /p'`.
3. Authoring something novel (a flow, an embedded runtime): dump ONCE to a scratch
   file and grep that file.

This file repeats nothing the reference covers. It carries only what the reference
lacks: exit codes, failure semantics, traps, and per-agent recipes. If a syntax
question is not answered here, it is answered there - go get it, never guess a flag.
The repo's `docs/` (exit-codes, session-control, session-watch, permissions, config) cover some of what the
shipped reference omits.

## When this lane

acpx is the headless out-of-process executor lane: another agent, vendor or account,
driven from a script or from another agent, in a plain terminal, ssh or cron.
In-session fan-out stays on the harness's own subagent tool.

## Invariants

1. **Global flags precede the agent subcommand** (`--cwd`, `--model`, `--approve-all`,
   `--agent`, `--format`, `--timeout`, `--ttl`, `--mcp-config`). The prompt form accepts
   only `-s`, `--no-wait`, `-f` (and `exec` also `--config-option`); other subcommands
   carry their own (`sessions watch --cursor`, `sessions export|import --cwd`). A global flag
   after the agent exits **1** with `error: unknown option`; a bad flag *before* the
   agent exits **2**.
2. **`-s <name>` never creates a session.** It resolves one, walking from `--cwd` up
   to the nearest `.git` - a directory *or file*, so each worktree and submodule is its
   own boundary; outside git only the exact `--cwd` is checked. No match exits **4**.
   Create first with `sessions ensure --name <n>` in the same directory.
3. **`status` is not a turn signal.** It probes the queue-owner process, never the
   agent, and keeps saying `running` after the turn has ended. Never gate automation
   on it.
4. **Permission flags are not a sandbox.**
   - **claude**: the adapter starts in `permissions.defaultMode` from the Claude
     settings (`acceptEdits` / `auto` approve edits without asking). Only what that
     mode escalates reaches acpx as a permission request - `--deny-all` refuses those
     (exit 5), but an auto-approved edit never asks.
   - **codex**: writes inside its workspace-write sandbox (rooted at `--cwd`, plus temp
     dirs) raise no request, so `--deny-all` still writes; outside fails with
     `Operation not permitted` - including a linked worktree's gitdir, so a sandboxed
     lane in a `git worktree` cannot commit (`index.lock: Operation not permitted`).
     Network is off unless `config.toml` enables `network_access`. `--approve-all`
     does not change the adapter's mode; `INITIAL_AGENT_MODE=read-only|agent|agent-full-access`
     at spawn, or `codex set-mode agent-full-access -s <n>` on a live session, does.
   - `--allowed-tools` / `--max-turns` reach only claude (and qoder); codex and agy
     ignore them. `--allowed-tools` pre-approves and never restricts: `--help`'s
     `"" for no tools` means no approvals, not no tools.

   The real filesystem control is which `--cwd` you hand it.
5. **`[done] end_turn` and exit 0 are not proof of success.** A content-filter kill,
   an MCP load failure, an API error (a 401 during a token refresh, a 400 model
   rejection), or a truncated turn all end that way. Read the stream, or require the
   agent to write a result file you can check. Before a fan-out, one cheap `exec`
   ("Reply OK") per agent and model catches auth and model errors - codex and agy
   reject an unadvertised `--model` before the turn, claude warns and forwards it.
6. **A persistent session holds a resident process stack only while it is busy or
   warm.** Every `-s` prompt elects a queue owner holding `npm exec -> node <adapter>
   -> <agent>` (plus the agent's MCP servers), roughly 550-650 MB before MCP. After
   the idle TTL (default 300s) the owner exits and the session stays resumable; the
   next prompt respawns it. `sessions close` ends the task - chain it into the launch
   line (see Per agent) so teardown never depends on anyone remembering; `--ttl 0`
   removes the self-reap. See Teardown.

## Per agent

**Dispatch one-shot: `sessions ensure && prompt && sessions close`, one chained
call.** One named session per task, one prompt, closed when the result file is read.
The `&&` chain makes teardown mechanical - nothing reaps open records, and orphans
come from unchained closes - while a turn that fails nonzero (timeout 3, permission 5)
skips the close on its own, leaving the session open for recovery (see Talking to a
live session). An externally cancelled turn still exits 0, so the result file, not
the exit code, is the success check (invariant 5). Do not park a session for expected
follow-ups: a blocker's state lives outside the conversation (creds are machine-level,
partials belong in the result file) - answer it with a fresh session fed the brief
plus that file. Rework - a correction, review, or polish of a session's output - also
gets a fresh session: an agent re-reading its own context misses what fresh eyes
catch. Never `--no-wait` into a session whose launch line carries the close: owner
shutdown drops pending prompts silently and cancels the active turn (verified 0.19.4);
a blocking prompt before the close is safe. Use `exec` for a stateless answer with no
record worth keeping (a preflight "Reply OK"). Sessions key on agent command + cwd +
name; give each parallel executor its own name and, when it writes files, its own
directory (ideally one worktree).

Adapters run through `npm exec` unless the adapter binary (`claude-agent-acp`,
`codex-acp`) is on PATH - that copy wins over the package fallback, and upgrading
acpx never updates it. A fresh HOME per job re-downloads them (hundreds of
MB each); share one `npm_config_cache`. On macOS a fresh HOME also hides the login
Keychain: the claude adapter fails `RUNTIME: Unable to validate model: Could not
resolve authentication method` - keep HOME. The npx cache also reuses stale builds -
pin exact adapter versions in `~/.acpx/config.json` (`agents.<name>.argv`). A pin
freezes which model ids work, and changing it re-keys sessions (see Sessions).

Executors inherit the user's global instruction files (claude's `~/.claude/CLAUDE.md`,
codex's global `AGENTS.md`). A rule like "ask before editing" ends a headless turn on
a question with no work done - open every brief with "act now; do not stop to ask or
end on a question". An executor that reads "use an out-of-process executor" there may
launch a nested acpx lane into the same checkout - add "you are the executor; do not
delegate". Delete or rename the old result file before a relaunch (a poller reads the
stale one), and give parallel lanes their own temp paths and ports - separate
worktrees do not isolate `/tmp`.

They also inherit the launcher's environment, and codex's zsh re-reads
`$ZDOTDIR/.zshenv` (default `~/.zshenv`) for every command - unsetting a secret in
the launcher does not keep it out, and whatever the shell prints lands in the rollout
files under `~/.codex/sessions`.

### agy / Antigravity

The built-in `acpx antigravity` (0.17.1+) runs `agy_acp_server.par` **from PATH**,
and the copy Antigravity installs under `~/.local/lib/antigravity-acp/` is not on
PATH - bare `acpx antigravity` exits 1 with `Failed to spawn agent command:
agy_acp_server.par`. Prepend that directory to PATH, set `agents.antigravity.argv`,
or use `--agent <path>`. The built-in `gemini` agent is the *public Gemini CLI* - a
different product. The `.par` comes from the Antigravity install or the official ACP
registry archive; keep it beside its `localharness_external` helper from the same
release (a missing helper only logs `Localharness not found.` and carries on), or
point `ANTIGRAVITY_HARNESS_PATH` at it. Neither acpx nor `agy update` refreshes the
`.par`: compare its `--version` `Build label:` with the
[ACP registry](https://github.com/agentclientprotocol/registry/blob/main/antigravity-acp/agent.json)
and swap both files together (the installed helper is read-only - `rm -f` it before
copying the new one in).

```bash
D=/abs/real/dir                              # must exist: roots resolve through realpath
acpx --agent ~/.local/lib/antigravity-acp/agy_acp_server.par \
     --cwd "$D" --model gemini-3.8-flash --approve-all --timeout 1800 \
     exec "Carry out $D/brief.md. Write your report to $D/report.md."
```

- **`--approve-all` is mandatory.** Without it every write is refused: exit 5 (or a
  stall to exit 3), with `[done] end_turn` still printed and no report.
- **Fixed-choice questions fail the prompt with exit 5 even under `--approve-all`**
  (final line `Antigravity requested a user answer...`) - for `--agent` launches too.
  acpx fails any agent's fixed-choice question this way (`PERMISSION_PROMPT_UNAVAILABLE`);
  agy is where it bites. Write briefs that never need a user choice.
- **Use only ids the ACP session advertises** - a deliberately bad `--model` prints
  `Available models:` without starting a turn (server 1.4.5: `gemini-4-argon`,
  `gemini-3.8-flash`; the effort-in-id `gemini-3.7-flash-{low,medium,high}` ids are
  gone). `agy models` is a different list. Flash suits rubric-driven bulk work and is
  far faster, but misses real findings in review / bug-hunting work; use a stronger
  model there.
- **agy reads sibling files unprompted** - agents sharing a directory reproduce each
  other's output. One directory per agent, and checksum any rerun before believing an
  agreement number.
- **Auth: needs `auth.type` in `<GEMINI_HOME>/antigravity-acp/settings.json`** (one-time):

  ```bash
  mkdir -p ~/.gemini/antigravity-acp
  echo '{"auth":{"type":"oauth-personal"}}' > ~/.gemini/antigravity-acp/settings.json
  ```

  Without it: immediate `[error] RUNTIME: Authentication required` (exit 1). With it
  but never signed in: `session/new` blocks on a browser sign-in until `--timeout`
  (exit 3) - sign in once interactively. The server's credential is separate from the
  `agy` CLI's: the macOS Keychain (service `gemini`, account `antigravity-acp`), or
  `<GEMINI_HOME>/antigravity-acp/acp_token.json` off macOS or with
  `AGY_ACP_FORCE_FILE_STORAGE=1`. `GEMINI_HOME` alone does not isolate the macOS
  credential. An entitlement problem is server-side - do not "fix" it by switching to
  `gemini-api-key` or a GCP project (separate billing, not fixes).
- **Never pass a positional agent with `--agent`** - exit **2**.
- **Verification prompts: demand a bare reply and read the whole log.** agy routes
  answers into brain artifact files, so a `tail` cannot tell "no tools" from
  "answered elsewhere". Add "Do not create any files".
- **agy hides MCP failures inside a successful-looking turn** - exit 0, `[done]
  end_turn`, and the whole reply is `The MCP server '<name>' failed to initialize: ...`.
  Grep for `failed to initialize`.
- **Prefer `exec`.** A server death mid-checkpoint has been reported to break a saved
  conversation for good (`could not find doneCh for checkpoint`); the only reported
  recovery is deleting `~/.gemini/antigravity-acp/conversations/<id>.db`.

#### Linux / NixOS

The built-in agent adds the required `--uid=` itself. NixOS additionally needs a CA
bundle, so point `--agent` (or `agents.antigravity.argv`) at a wrapper
(`~/.local/bin/agy-acp-server`):

```bash
#!/usr/bin/env bash
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
exec ~/.local/lib/antigravity-acp/agy_acp_server.par --uid= "$@"
```

Without `SSL_CERT_FILE` the `.par`'s embedded OpenSSL has no valid CA paths; its local
proxy reports `502 Bad Gateway: Failed to connect to backend API` and the turn still
ends `[done] end_turn` with **exit 0** (invariant 5). The real
`CERTIFICATE_VERIFY_FAILED` appears only under `--alsologtostderr`.

### codex

```bash
D=/abs/dir
acpx --cwd "$D" codex sessions ensure --name work            # idempotent; -s cannot create
acpx --cwd "$D" codex set model gpt-6-astra -s work
acpx --cwd "$D" codex set reasoning_effort high -s work
{ acpx --cwd "$D" --approve-all --timeout 5400 --suppress-reads \
     codex -s work 'Carry out ./brief.md. Write your report to ./report.md.' && \
  acpx --cwd "$D" codex sessions close work; } > run.log 2>&1 &
# a failed turn skips the close - re-prompt -s work to recover, then close yourself
```

One-shot: `--model <id> exec --config-option reasoning_effort=low` sets model and
effort inline.

- The codex adapter (`@agentclientprotocol/codex-acp`) floats on `^1.1.5` - behavior
  can change without an acpx upgrade, but the breaking 2.x is out of range. A stale
  adapter rejects newer model ids: `[error] RUNTIME: Invalid params` at
  `session/set_config_option` (exit 1), or a 400 `model is not supported` that still
  ends `[done] end_turn`, exit 0. Pin a current one:
  `{"agents":{"codex":{"argv":["npx","-y","@agentclientprotocol/codex-acp@2.5.0"]}}}`.
  An exact pin still floats the codex binary inside it (2.5.0 depends on
  `@openai/codex ^0.165.0`). The same symptoms hit a current adapter when the account
  lacks the model: the advertised list differs per account - preflight under the
  lane's own login.
- **OpenAI's content filter kills benign turns** that end clean (`[done] end_turn`,
  exit 0). Vocabulary like race / sweep / exploit / attack in a filename, comment or
  prompt triggers it. Read the transcript tail before believing completion; recover by
  re-prompting the same `-s <name>` (context survives unless the reconnect fails -
  acpx then silently falls back to `session/new`) with the artifact renamed
  neutrally and the remaining steps listed explicitly.
- **Re-prompting the same name queues behind the current turn** - the recovery path
  after a content-filter kill (above), not a dispatch pattern; close once recovered.
- **Handing off to a human TUI**: `sessions close` first, then `codex resume <id>` -
  `agentSessionId` from `sessions show` when it prints one, else `sessionId` (the
  ordinary codex rollout id).
- **MCP servers still starting when codex builds its tool list are dropped** (1s shared
  grace). `mcp_optional_startup_grace_ms = 0` in `config.toml` waits for each server's
  own `startup_timeout_sec` instead.

### claude

```bash
D=/abs/dir
acpx --cwd "$D" --model claude-opus-5 claude sessions ensure --name work
acpx --cwd "$D" claude set effort high -s work                 # optional; after any model change
{ acpx --cwd "$D" --model claude-opus-5 --approve-all --suppress-reads --timeout 2400 \
     claude -s work -f /abs/brief.md && \
  acpx --cwd "$D" claude sessions close work; } >> run.log 2>&1 &
# failed turn (exit 3/5) = close skipped: re-prompt -s work to recover with context,
# then close; anything after a clean close is a fresh session fed the result file
```

- **Effort is `set effort <level>`**; `set reasoning_effort` is the codex name and
  fails `Unknown config option: reasoning_effort (ACP -32602)` on claude. A model switch resets effort - set model first.
- **Pass the model with `--model <exact id>` at session creation.** `set model`
  fuzzy-matches against the adapter's advertised list and can silently land on a
  different entry (e.g. `opus[1m]`); only an id with no match fails
  (`Invalid value for config option model`). An unknown `--model` fails with
  `RUNTIME: Model '<id>' not found`. Quote ids with brackets (`'...[1m]'`) - globs.
- **Fable runs**: `--model claude-fable-5-1`. Ids absent from the advertised list
  (`claude-fable-5-1`, `'claude-fable-5-1[1m]'`, `claude-opus-5-5` on adapter 0.100.0)
  still run: acpx prints `[acpx] warning: requested model ... was not in the Claude
  ACP advertised model list` and forwards them as given.
- **The bundled Claude Code is whatever the adapter pins.** Built-in adapter
  `^0.95.0` (acpx 0.21.1+) = Claude Code 2.1.309; a caret on 0.x locks the minor, so
  upgrading acpx does not reach newer builds. An older pin fails newer models with
  `Claude Code 2.1.2xx does not support this model` - pin a newer adapter:
  `{"agents":{"claude":{"argv":["npx","-y","@agentclientprotocol/claude-agent-acp@0.100.0"]}}}`
  (Claude Code 2.1.316) in `~/.acpx/config.json`. Any command containing
  `claude-agent-acp` keeps acpx's claude handling.
- **`session/new` has its own 60s deadline**, independent of `--timeout`: a slow
  start (a heavy MCP set, a cold npx cache) exits **3** with `Claude ACP session
  creation timed out before session/new completed.` (`detailCode`
  `CLAUDE_ACP_SESSION_CREATE_TIMEOUT`; its hint naming `--timeout` is wrong). Raise
  it with `ACPX_CLAUDE_ACP_SESSION_CREATE_TIMEOUT_MS`.
- **User settings are excluded on purpose** - user skills are missing (`/polish`
  "isn't available"). Fix with `ACPX_CLAUDE_INCLUDE_USER_SETTINGS=1`. acpx reads it
  from its own environment and re-applies settings whenever the session's process
  spawns (create, load, resume); a live owner keeps what it started with, so after
  changing it close the session or let the owner idle out, then prompt again. A
  `--cwd` under `$HOME` still loads `~/.claude/CLAUDE.md` through the ancestor
  CLAUDE.md walk.
- **Second account**: export `CLAUDE_CONFIG_DIR` and `CLAUDE_SECURESTORAGE_CONFIG_DIR`
  before `acpx`; the child inherits them. Set them on **every** call, not only the
  first - whichever call respawns an idle session decides its account. A tiny wrapper
  script that exports them and execs acpx makes that hard to forget.
- **Edits need no `--approve-all` when Claude's own `permissions.defaultMode` is
  `auto` or `acceptEdits`** (invariant 4); pass it on every prompt anyway so
  escalated requests are not denied.
- **The child's harness refuses long foreground sleeps** (`sleep 90` blocked outright),
  so a child cannot own a long wait or poll loop - and a loop it backgrounds dies when
  its owner exits. Long waits belong to the driving side (`sessions watch`, a
  result-file poll).
- **Subagents inside a child work** (verified with the Agent tool), but an executor
  that spawns them in the background can end its turn before they report -
  `[done] end_turn`, exit 0, no report. The brief must say to wait for every subagent
  and write the report before the final message, and never to end a turn with a
  background loop running.
- **Prompt text the driving harness blocks** (a hook or classifier reading a brief
  that mentions gates, secrets or approvals): send every prompt as `-f <file>`.

## Sessions

- Sessions key on **(agent command, absolute cwd, optional name)** - parallel
  executors need their own directories, which also keeps per-session model and effort
  settings from racing.
- **Changing `agents.<name>.argv` (a pin bump) or a `<cwd>/.acpxrc.json` override
  changes the agent command, so existing `-s` sessions stop resolving (exit 4).**
  Close them before re-pinning. A target repo's `.acpxrc.json` can also replace the
  adapter, the MCP set, the default agent, or permission defaults, or set
  `disableExec: true` (every `exec` then fails, exit 1) - `acpx --cwd <dir> config
  show` before pointing acpx at a repo you do not control.
- `sessions close` is the teardown verb: marks the record closed, sends ACP
  `session/close`, takes down the owner and adapter processes (see Teardown). Also
  required before `codex resume` and `sessions export`.
- **A warm owner keeps what it started with**: `--mcp-config`, `--no-fs` /
  `--no-terminal`, `ACPX_MAX_ACP_MESSAGE_BYTES`, `ACPX_TERMINAL_MAX_OUTPUT_BYTES`,
  `ACPX_CLAUDE_INCLUDE_USER_SETTINGS`, credentials and environment take effect only
  when the next owner spawns - close the session (or let it idle out) first.
- A session whose cwd you deleted still closes with `--cwd <old path>`.
- `sessions new|ensure --resume-session <id>` binds a record to a saved ACP session.
  A record `id:` of the same agent command (0.19.4+) retires that record's owner and
  rebinds the same record, context intact; otherwise pass the ACP `sessionId:` from
  `sessions show`. Resume loads a saved session into a new adapter; it never attaches
  to a live process.

## Completion

`status` states (the shipped reference has no state table): `running` (JSON: `alive`
- the owner's socket answers), `idle` (no owner, including one that was killed),
`dead` (an owner lease remains but is unhealthy, or the recorded exit was abnormal),
`no-session`. `running` holds for the whole idle TTL after a turn ends - a loop
waiting for `idle` spins past real completion (invariant 3). What is actually correct:

- `acpx <agent> sessions watch -s <n>`: its `turn_result` event (`completed`,
  `cancelled`, `failed`) is the settlement signal. Without `--cursor` it first replays
  the retained window, earlier turns included - match the `requestId` from
  `[queued] <id>`, and break out yourself (it never exits on an open session).
  `WATCH_OUTCOME_UNKNOWN` means the owner died mid-turn - the prompt may have run;
  check before resubmitting (`requestId` is not an idempotency key: a resubmit runs
  twice). `WATCH_OWNER_UNSUPPORTED` is an older owner - close it;
- the foreground stream's terminating `[done] end_turn`, plus the process exit code;
- `sessions show <n>` (`lastActivity`, `historyEntries`), `sessions history <n>`, and
  `sessions read <n> --tail N` (shows in-flight tool calls);
- best: a **result file** the brief required the agent to write - poll for the file.

`--no-wait` acknowledges enqueueing (`[queued] <id>`; nothing is printed under
`--format quiet`), which is neither delivery nor completion - behind a running turn
the prompt waits for the turn boundary.

From a Claude Code driver, run `sessions watch` under the Monitor tool so each turn
arrives as a notification:

```bash
acpx --format json --cwd "$D" claude sessions watch -s work --cursor "$LAST" \
  | jq --unbuffered -c 'select(.type=="turn_started" or .type=="turn_result")
      | {type, requestId, status: .result.status}'
```

Keep the last `cursor` when re-arming, or the stream replays earlier turns. A cursor
whose history has rotated away fails `WATCH_CURSOR_EXPIRED` (also `_INVALID`,
`_FOREIGN`, `_FUTURE`) - re-arm without it and dedupe by `requestId`.

Serialize dependent lanes by chaining their one-shot lines with `&&`, or by waiting
on the backgrounded line's exit - never a `pgrep -f` loop, which matches other runs
on the same agent or model. `acpx compare` runs its agents serially in one shared
`--cwd` (each sees the others' writes); a per-agent error does not stop the batch,
and SIGINT/SIGTERM/SIGHUP skips the remaining agents with exit 130.

Supervise a backgrounded text-format run by counting tool lines and mtime
(`rg -c '^\[tool\]' run.log`, `stat -f '%Sm' run.log`). `--format quiet` prints only
the final text (plus an `[acpx] tokens:` line on stderr) - no `[tool]`, no `[done]` -
so those counts read 0; supervise quiet runs by exit code, result file, and the one
stderr line `[acpx] error: <CODE> [<DETAIL_CODE>] <message>` on failure. Under
`--format json` a failure is one JSON-RPC error line whose `error.data` carries
`acpxCode` (`TIMEOUT`, `NO_SESSION`, `EXEC_DISABLED`, `RUNTIME`, ...), `detailCode`
(`AUTH_REQUIRED`, `CLAUDE_ACP_SESSION_CREATE_TIMEOUT`, ...) and `retryable` - branch
on those, not on message text. `exec` saves
nothing to watch; for codex, `tail -f` the newest
`~/.codex/sessions/<date>/rollout-*.jsonl` (written even for `exec`).

## Teardown

`sessions close <n>` takes down the whole resident stack (owner -> `npm exec` ->
`node <adapter>` -> agent binary -> its MCP servers) and marks the task finished.
With chained one-shot dispatch the close runs itself; a separate close is owed only
after a failed turn's recovery or a deliberately tended multi-turn session - there
the idle TTL frees only the process stack, and the record stays open until you close
it. A `"ttl": 0` config makes forgotten owners resident for hours; with the default
they exit after 300s idle.

Liveness and leak check - never `pgrep -l` or `ps -o args`: command lines of wrapper
shells can carry secrets, and the bracketed first letter keeps the pattern from
matching the shell that runs it (Linux `pgrep` matches its ancestors):

```bash
PAT='[a]cpx.*__queue-owner|[c]odex-acp|[c]laude-agent-acp|[a]gy_acp_server|[l]ocalharness_external'
pgrep -f "$PAT" | wc -l                                      # 0 once your runs are closed
P=$(pgrep -d, -f "$PAT") && ps -o pid,ppid,etime,rss,comm -p "$P"   # no args column
```

- `close` returns before `npm exec` / `node` exit - poll for ~10s before calling
  anything a straggler. Other people's runs count too; scope with
  `lsof -a -d cwd -Fn -p <pid>` (adapter and agent run in `--cwd`).
- **A straggler gets a plain `kill <owner pid>`**; SIGTERM takes the stack down within
  seconds. Since 0.19 even SIGKILL no longer strands the adapter (it exits on stdin
  EOF), but a mid-turn kill loses the turn: `Queue owner disconnected before prompt
  completion; outcome unknown`.
- **Owners lingering with no `--ttl 0` on the command line**: run
  `acpx --cwd <dir> config show` - a `ttl` key in `~/.acpx/config.json` or the
  project's `.acpxrc.json` sets the default idle TTL, and `"ttl": 0` disables the
  self-reap for every invocation it covers.
- **Close owners started by an older acpx before upgrading** - 0.19 refuses forced
  retirement of legacy owners it cannot verify (`QUEUE_SHARED_RUNTIME_UNSUPPORTED`:
  wait for idle expiry or close).
- `QUEUE_OWNER_IDENTITY_UNVERIFIED` / `QUEUE_OWNER_RETIREMENT_INCOMPLETE`: acpx kept
  a live owner's lease rather than guess - close or wait. A leftover
  `.acpx/queues/<key>.lock.guard` (or its `.reclaim` dir) blocks recovery until you
  stop every acpx process using that home and remove it by hand. Never share one
  queue home across hosts or namespaces.
- Closed records persist indefinitely; `sessions prune --older-than 7
  --include-history` on a cadence (the event streams are the bulk of
  `~/.acpx/sessions`).

## MCP

`--mcp-config <path>` **replaces** the `mcpServers` acpx itself would pass (from
`~/.acpx/config.json` / `.acpxrc.json`) for that invocation. Servers the agent loads
on its own still load on top: codex's `config.toml` `mcp_servers`, and claude's
user-scope servers once `ACPX_CLAUDE_INCLUDE_USER_SETTINGS=1`. The file path resolves against `--cwd` (the last `--cwd` / `--mcp-config` wins); paths
*inside* the file are passed verbatim. The shipped reference does not mention it.

**The file shape is not the standard one.** acpx wants a JSON *array* of named server
objects; the standard object-keyed map fails with
`Invalid mcpServers in <path>: expected array` (exit 1). `env` and `headers` are
arrays of `{name, value}` too; a missing `type` means stdio.

```jsonc
// RIGHT - an array, each entry carrying its own name
{ "mcpServers": [ { "name": "example", "type": "stdio", "command": "example", "args": ["mcp"],
                    "env": [ { "name": "LOG_LEVEL", "value": "info" } ] } ] }
```

**A stdio server that dies only under agy is an MCP era mismatch, not an acpx fault.**
agy probes stdio with `server/discover` (MCP 2026-07-28 retired the `initialize`
handshake); a legacy server that *aborts* on the unexpected request kills the pipe
instead of answering an error, leaving nothing to fall back from. The codex and claude
adapters do not probe, which is the only reason the same config works for them. Fix
the server (answer an error, or move to a current MCP SDK), or reach it over HTTP.
The turn still exits **0** and ends `[done] end_turn` - grep for
`failed to initialize` before trusting any agy run that used MCP.

- **A live queue owner refuses a config change** (it carries the config path plus a
  SHA-256 fingerprint): `sessions close` first.
- **Verify the effective set, not the file** - a one-shot `exec` that asks the agent
  which MCP servers' tools it sees; the answer depends on the adapter's own config too.
- acpx does no `${...}` expansion; whatever the agent expands resolves in the
  environment it inherited from the **launcher**, so a variable like a session id
  resolves to *your* id. Never let an identity flow in through the environment.

## Limits

- **Incoming ACP messages cap at 64 MiB** since 0.15.1 (previously unlimited);
  `ACPX_MAX_ACP_MESSAGE_BYTES` raises it, `0` disables. Overflow fails exit 1 with
  `ACP message exceeded ACPX_MAX_ACP_MESSAGE_BYTES (<n> bytes)`.
- Terminal output retention defaults to 64 KiB per call when the agent sets no limit;
  `ACPX_TERMINAL_MAX_OUTPUT_BYTES` is a host ceiling that can only lower it.
- Long unattended work: `--timeout 5400`, plus a wrapping shell `timeout` with a
  margin for acpx's cleanup. Exit 3 leaves partial,
  uncommitted work in the cwd - a relaunch prompt should say so. Do NOT add
  `--ttl 0` - the 300s default covers any gap within one run, and `--ttl 0` removes
  the only automatic reaper (invariant 6). Reserve it for a human-driven warm session
  you will close by hand.
- `--format quiet` for fleets you judge by exit code and result file;
  `--suppress-reads` on every long run.
- Headless permission requests nobody can answer are denied; a turn where none was
  approved and at least one was denied exits **5**. `--non-interactive-permissions fail` stops at the first
  one instead (`Permission prompt unavailable in non-interactive mode`).
- `--prompt-retries` retries only before the turn produced any session update - one
  thought chunk disqualifies it - so a mid-turn provider failure still needs a
  re-prompt (openclaw/acpx#850).
- Pass long briefs as `-f <path>` or a path in the prompt, never inlined - inlined
  content in a shell command is what a driving harness's classifier blocks on.

## Talking to a live session

For the one live turn of a one-shot dispatch, and for recovery after a failed one.
Verified end to end with acpx 0.19.4 and claude-agent-acp 0.85.1:

- **Queue:** `--no-wait` prompts run in submission order after the running turn.
- **Redirect:** `cancel -s <name>`, then a new prompt. Nothing reaches a running turn
  otherwise (see below).
- **Blockers:** have the brief tell the agent to stop with `BLOCKED: <what, where>` at
  the top of its result file - and dump everything gathered so far below it - then end
  the turn. Close the session and answer with a fresh one fed the brief plus that
  file: the blocking state lives outside the conversation (creds are machine-level,
  results belong in files), and a resumed child's memory is not what you assume (a
  failed reconnect silently starts a new conversation - see Recovery).
- **Mid-turn channel:** when a brief may need an answer mid-turn, tell the agent to
  append `PROGRESS:` / `QUESTION:` lines to a progress file and to poll an answer file
  with short foreground sleeps. Tail the progress file from the driving side (under
  the Monitor tool from Claude Code) and write the answer file. A blocker answered
  this way resolves inside the turn - no session outlives it. (Both adapters ship a
  `_session/steering` extension - claude-agent-acp 0.84.0, codex-acp 2.0.0 - but acpx
  exposes no verb for it yet - openclaw/acpx#836 - so the file poll stays the only
  mid-turn inbound.)
- **Recovery:** a failed or timed-out turn (exit 3, `turn_result: failed`) leaves the
  session intact - prompt the same name again. After the idle owner exits, the next
  prompt respawns and resumes the same conversation. After any respawn check that
  `sessionId` in `sessions show` is unchanged: a failed reconnect silently falls back
  to a new conversation. After recovery the close is yours to run - the chain already
  skipped it.

## What acpx cannot do

Structural, not bugs. Do not design around them.

- **An ACP session does not wake.** An externally injected message lands in the
  transcript but starts no turn; the only inbound channel is acpx itself
  (`-s <name>`, optionally `--no-wait`), plus a file the brief told the agent to poll.
- **`codex queue --thread` does not reach an acpx-driven codex session** (it does wake
  a plain interactive codex).
- **acpx-spawned Claude sessions bind no IPC socket**, so `ListAgents` /
  `SendMessage` cannot see or reach them.
- **acpx cannot attach to a live process it did not start** (`--resume-session` loads
  a saved ACP session into a new adapter; see Sessions).

## Failures

Exit codes (absent from the shipped reference; repo `docs/exit-codes.md` has them):

| code | meaning |
|---|---|
| 0 | success (also `cancel` with nothing to cancel) |
| 1 | agent / protocol / runtime error - the catch-all; also a global flag after the agent |
| 2 | usage error before the agent: bad or conflicting flags, empty or malformed `--agent`, `--timeout 0`, a missing prompt |
| 3 | `--timeout` exceeded |
| 4 | no session found by the directory walk |
| 5 | permission denied in this turn (none approved, one denied/cancelled); `--non-interactive-permissions fail`; a fixed-choice user question acpx cannot answer (agy) |
| 130 | interrupted - racy: a SIGINT the cooperative cancel settles first exits 0 with `[done] cancelled` |

Error catalog - string -> fix:

- `⚠ No acpx session found (searched up to <dir>)` (exit 4) - invariant 2:
  `sessions ensure --name <n>` first; confirm `--cwd` is inside the same repo boundary.
- `No named session "<n>" for cwd <cwd> and agent <agent>` (exit 1) - `sessions
  close|show` with a wrong name or cwd; `sessions list --local`.
- `error: unknown option '--cwd'` (exit 1) - global flag after the subcommand
  (invariant 1).
- `Do not combine positional agent with --agent override` (exit 2) - drop the
  positional `claude`/`codex`.
- `Agent command must not be empty` (exit 2) - an empty `--agent` (unset variable).
- `Invalid --agent command: unterminated quote` / `empty command` (exit 2) - a broken
  quote, or a quoted empty string, in `--agent`.
- `Prompt is required ...` / `Prompt from stdin is empty` (exit 2) - no prompt
  argument, no `-f`, and a terminal or empty stdin.
- `exec subcommand is disabled by configuration (disableExec: true)` (exit 1) - a
  config or `.acpxrc.json` sets `disableExec`; use a named session.
- `Claude ACP session creation timed out before session/new completed.` (exit 3) -
  raise `ACPX_CLAUDE_ACP_SESSION_CREATE_TIMEOUT_MS` (see claude).
- `Failed to spawn agent command: agy_acp_server.par` (exit 1) - built-in
  `antigravity` with the `.par` off PATH; see agy.
- `Invalid mcpServers in <path>: expected array` (exit 1) - see MCP.
- `MCP config file not found: <path>` (exit 1) - a relative `--mcp-config` resolves
  against `--cwd`.
- `Cannot apply --model "<id>": the ACP agent did not advertise that model. Available
  models: ...` (exit 1, any agent) - pick from that list; codex: or pin a newer adapter.
  A claude id rejected against a list of gpt ids means the agent name was omitted and
  acpx fell back to the configured `defaultAgent` (codex unless a config sets it).
- `Agent rejected session/set_config_option for model "<id>": Invalid params: Invalid
  value for config option model: <id> (ACP -32602)` - `set model` with no match in the
  advertised list; use `--model` at session creation (see claude).
- `RUNTIME: Model '<id>' not found` - `--model` typo or an id the harness lacks; a 404
  mid-turn reads `There's an issue with the selected model (<id>)`.
- `Claude Code 2.1.2xx does not support this model` - adapter too old; pin a newer one
  (see claude).
- `Unknown config option: reasoning_effort (ACP -32602)` from `claude set
  reasoning_effort` - claude's knob is `set effort`.
- `Authentication required` (exit 1) - the agent's own login is missing or expired.
  agy: no `auth.type` in the server's `settings.json` (see agy). claude: `OAuth session
  expired` (`QUEUE_RUNTIME_PROMPT_FAILED`) - log in again under the same config dir.
  Parallel codex lanes on one login race on refresh-token rotation - preflight once,
  then stagger launches. Other agents (`grok-build`): log in with the agent's own CLI.
  A failed `ensure && prompt` leaves the record open - close it.
- `Session queue owner failed to start for session <id>` (exit 1) - often several
  sessions launched at the same instant; relaunch serially or stagger the launches.
- `[acpx] error: ...` followed by `hint: the provider appears rate-limited; retry
  later, switch model, or check provider quota/billing.` (exit 1, 0.19.6+) - quota,
  usage-limit and auth failures now carry the provider's own text instead of
  `Internal error`; an overload can still end clean (openclaw/acpx#850).
- `QUEUE_RUNTIME_PROMPT_FAILED You've hit your usage limit ... try again at <date>`
  (exit 1) - an account quota with a reset time, not a transient: do not retry;
  switch account or model.
- agy stalls at `[client] session/new (running)` until timeout (exit 3) - `auth.type`
  set but never signed in; sign in once interactively.
- `502 Bad Gateway: Failed to connect to backend API` (agy, exit 0) - missing CA
  bundle on NixOS; see Linux / NixOS.
- `Antigravity requested a user answer...` (exit 5) - agy asked a fixed-choice
  question; rewrite the brief so it never needs one.
- `The MCP server '<name>' failed to initialize` (agy, exit 0) - see MCP.
- `RUNTIME: This client is no longer supported for Gemini Code Assist`, or `Gemini CLI
  ACP startup timed out before initialize completed` - you used the built-in `gemini`
  agent; use agy.
- `already has an active writer (code -32600)` - `codex resume` while acpx still owns
  the thread; `sessions close <n>` first.
- `Failed to resume ACP session <id>: Internal error` - `--resume-session` got a
  record `id:` from a different agent command, passed through as an ACP id; use that
  record's `sessionId:`.
- `Queue owner disconnected before prompt completion; outcome unknown` (exit 1) - the
  owner died mid-turn, or dropped a slow reader (full output spool) while the prompt
  kept running; check `sessions history` and the cwd before resubmitting.
- `Missing --skill action.` (exit 1) - `--skill` needs
  `show|list|install|export|help`.
- `error: unknown option '--one-shot'` - not a verb (exit 1 after the agent, 2
  before); `exec` is the one-shot form.
- `Timed out after <ms>ms` (exit 3) - the wall clock ran out, not a stuck agent -
  check `sessions show` for `lastActivity`; an adapter-side timeout surfaces as exit 1
  instead.

Silent failures worth an explicit check: content-filter kills and MCP load failures
both end `[done] end_turn` with exit 0; a denied agy write ends `[done] end_turn`
with exit 5; a `--no-wait` prompt that "sent" may still be queued behind a running
turn; `status` reads `running` long after completion; `sessions close` drops pending
`--no-wait` prompts with no error and cancels the active turn, whose submitter exits
0 with `[done] cancelled`; killing a blocking submitter kills the child's turn with
it (SIGTERM: exit 143, nothing reaches the transcript); and a `completed`
`turn_result` does not prove provider success - a codex provider error can end as a
clean `end_turn` (openclaw/acpx#850) - the result file remains the check.
