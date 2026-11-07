---
name: jev-fabric
description: Run, supervise and observe native processes with bounded receipts, durable background jobs and live filtered watches, and make explicit typed Jev decisions (choice, noul, score) from structured state. Use when a task needs a long-running or detached command that outlives the shell tool call, bounded log observation instead of tailing everything, or a fast typed judgment over an observation rather than generated text. Also use it when Python, TypeScript or other code should drive processes and Jev calls through one budgeted JSONL session (`serve`).
---

# jev-fabric

`jev-fabric` is a single native executable (written in Bend, no Node or Python at
runtime). It owns child processes in their own process groups, keeps bounded
receipts and event logs, and makes **explicit** typed Jev decisions. No output ever
triggers a model call by itself: you decide when to ask.

Every command here starts with `jev-fabric --`; the leading `--` is optional and
dropped (`jev-fabric exec ...` is the same call). Bend runtime options go between
`+RTS` and `-RTS`, and those words, like `--RTS`, are read by the runtime wherever
they appear on jev-fabric's own command line.

## Check the install

```bash
jev-fabric -- --version        # 0.8.1-native (Bend 2.0.38)
jev-fabric -- capabilities     # {"version":…,"protocol":2,"store":1,"platform":…,"features":[…]}
```

If it is missing, install the release binary (macOS universal, Linux x64/arm64):

```bash
curl -fsSL https://raw.githubusercontent.com/fabric-runtime/jev-fabric/main/install.sh | sh
```

It installs to `~/.local/bin/jev-fabric` and the Bend library to
`~/.local/share/jev-fabric/current/native/`. `jev-fabric -- update` reruns that
installer for the latest release. Ask before installing or updating.

## Run something once

```bash
jev-fabric -- exec /bin/echo hello                       # literal argv, no shell
jev-fabric -- exec --timeout-ms 5000 -- make test        # bounded ceiling
printf 'input\n' | jev-fabric -- exec --stdin /bin/cat   # forward stdin
jev-fabric -- exec /bin/sh -c 'ls | wc -l'               # shells are explicit
jev-fabric -- exec --cwd /abs/project -- make test       # start in another directory
```

The receipt is one JSON line: `state` (`exited`, `failed`, `timed_out`,
`cancelled`), `exitCode`, `timedOut`, bounded `stdout`/`stderr` tails (32 KiB) and
`truncated` flags. `exited` means the process exited, **not** that the task
succeeded: read the output and verify.

## Background jobs that outlive the tool call

```bash
id=$(jev-fabric -- start --label dev /bin/sh -c 'npm run dev' | jq -r .id)
jev-fabric -- status "$id"             # running state or final receipt
jev-fabric -- watch "$id" ready        # lines containing "ready" until exit or 5 s
jev-fabric -- follow "$id"             # live JSONL events until exit or 30 s
jev-fabric -- events "$id"             # bounded JSONL replay (last 64 events)
jev-fabric -- events "$id" 12          # only events after sequence 12
jev-fabric -- wait --timeout-ms 60000 "$id"   # waiting never cancels the job
jev-fabric -- stop "$id"               # idempotent cooperative stop
jev-fabric -- list                     # all jobs here, newest first, with labels
jev-fabric -- read "$id" stdout 0      # raw bytes by offset: {"text":…,"next":N,"omittedBytes":0,…}
```

An interactive job keeps its stdin open and survives your tool call:

```bash
id=$(jev-fabric -- start --input pipe -- python3 -u -i | jq -r .id)
printf 'print(6 * 7)\n' | jev-fabric -- write "$id" --stdin   # include the newline
jev-fabric -- read --wait-ms 5000 "$id" stdout 0              # then read from "next"
jev-fabric -- close-input "$id"
```

Writes are queued (1 MiB at most) and reach the child within 25 ms; for
millisecond round trips from code, use a `serve` session child instead.

- Job IDs are random, not PIDs. Storage is `.jev-fabric-native/` in the current
  directory (created with a `.gitignore`), or `JEV_FABRIC_HOME`. Run controls
  from the same directory/home; any agent or program sharing it sees the same
  jobs, so `list` finds work started earlier or by another harness. `start
  --cwd DIR` runs the job elsewhere without moving that storage.
- A storage home written by a newer jev-fabric is refused with exit code 22
  (`storage home uses store format N`): upgrade rather than work around it.
- `--label TEXT` (1..120 printable characters, one line) names a job; `status`,
  `wait`, `stop` and `list` report it. `start --timeout-ms` may be up to
  86400000 (24 h) for dev servers; the default lifetime stays 1 h.
- `follow <id> [after]` prints each event as it is published, a `follow.loss`
  record if older events were evicted, and one final
  `{"type":"follow.end","reason":"finished"|"timeout","next":N,"receipt":{...}}`.
  Resume with `follow <id> N`. A timeout never stops the job.
- `watch` returns `monitor.batch` lines (≤32 per batch), `monitor.loss` records when
  output was dropped, and a final `monitor.end` summary. A match is an observation,
  not proof of completion.
- Prefer `watch <id> <literal>` over repeatedly dumping `events` when you only need
  a signal such as `listening on`, `error` or `PASS`.

## Timers are ceilings, not delays

Defaults: work 1 h, Jev 30 s, `wait` 30 s, `watch` 5 s. Completion returns
immediately. Override once per call with `--timeout-ms N` placed **before** the
command, or globally with `JEV_FABRIC_TIMEOUT_MS`, `JEV_FABRIC_JEV_TIMEOUT_MS`,
`JEV_FABRIC_WAIT_MS`, `JEV_FABRIC_WATCH_MS`. Everything after the command is passed
through literally. Your own shell tool still has its own limit: use `start` for
anything longer than it.

## Typed Jev decisions

Jev answers structured questions about a state with typed values, not prose:

- `choice`: one key out of 1..255 described options, plus probabilities
- `noul`: a probability that a yes/no statement holds
- `score`: an ordinal position on 2..10 described levels

```bash
jev-fabric -- validate request.json                  # offline, no credentials
jev-fabric -- jev request.json 10000                 # one call, ≤10000 reported tokens
```

Provider and credentials come from the environment and are never printed:

```bash
export JEV_PROVIDER=typesafe          # or openrouter | vercel | subq
export TYPESAFE_API_KEY=...           # (subq: SUBQ_API_KEY) or a literal argv resolver:
export JEV_CREDENTIAL_COMMAND='["pass","show","typesafe"]'
```

Rules:

- **Only call Jev when the user has authorized network model calls.** Each call is
  billed. Never loop Jev calls without a call budget.
- Validate first. Deterministic checks (exit codes, parsers, tests) come before any
  judgment; use Jev for the fuzzy part only.
- An answer is a decision input, not permission: confidence never widens what you
  are allowed to do, and an executed action still needs verification.
- No automatic retries. A failed dispatch still counts as a call.

See [references/jev-requests.md](references/jev-requests.md) for the request
schema, limits and patterns (including choosing among more than 255 options).

## Additive lossless decisions

Legacy `jev` stays strict and unchanged. For multi-provider decisions use
`decision-providers` (offline registered presets, not live availability),
`validate-decision request.json` (offline schema check), then an **authorized**
`decide [--timeout-ms N] request.json [max-tokens]`. This path requires curl
7.82+ and uses private curl, not the pooled legacy connection.

For model changes, use `resolve-decision [--profile NAME | --provider PROVIDER
--model MODEL] request.json` first: full routing/adapter preflight without key
lookup or inference. The same target flags apply to `decide`. Portable profiles
come from explicit `DECISION_PROFILES` JSON or `DECISION_PROFILES_FILE`, never an
auto-discovered repository file. Explicit provider selection does not inherit
another provider's ambient model/endpoint. Client `withDecisionTarget` /
`with_decision_target` views bind immutable targets and share their parent's
connection/budget; these APIs require feature `decision-targets`.

Inspect both transport success and result `status`, per-question refusals,
`provenance` and `budget`. `rawJson` preserves exact provider numeric text;
missing confidence/distributions are never fabricated. `jev` and `decide` share
the session evaluation/token budget; unknown usage or dispatch uncertainty
stops later calls. Generated estimates require `allowGenerated:true`; local
HTTP requires exact loopback and `allowLocal:true`. Neither opt-in grants
permission to make model calls.

With TypeSafe, `decide` also takes images and a `box` question (one bounding
box, Jev 1.14: `jev-preview` or `jev-1.14.0`). Each image needs a `ref`
written into the state or instructions where it belongs;
`providerOptions: {"longContext": true}` lifts the context limit. TypeSafe calls
these experimental, so don't rely on them for production decisions.

See [the decisions reference](https://github.com/fabric-runtime/jev-fabric/blob/main/docs/decisions.md)
for supported image adapters, options, credentials and client examples.

## Sessions from Python, TypeScript or any language

When code (not you, turn by turn) makes many calls, one `serve` session beats
repeated CLI invocations: one Jev client, so the shared `jev`/`decide` call/token
budget spans the session. Legacy Jev caches its credential and keeps TLS warm;
`decide` resolves ephemeral credentials and uses private curl per dispatch.

```bash
jev-fabric -- serve --timeout-ms 600000 20 50000   # 10 min, ≤20 Jev calls, ≤50000 tokens
```

Write one JSON request per line; read one response per line and match it by
`id`: requests run concurrently, so responses can arrive out of order.

```text
← {"ready":{"protocol":2,"version":"0.5.1-native","store":1,"features":[...],...}}
→ {"id":1,"op":"start","argv":["/bin/sh","-c","npm run dev"]}
← {"id":1,"ok":true,"result":{"id":"<job>"}}
→ {"id":2,"op":"watch","job":"<job>","literal":"ready","timeoutMs":30000}
← {"id":2,"ok":true,"result":[{"type":"monitor.batch",...},{"type":"monitor.end",...}]}
→ {"id":3,"op":"jev","request":{"state":...,"questions":{...}}}
← {"id":3,"ok":false,"error":{"code":1,"message":"Jev budget exhausted"}}
```

Ops: `exec` (`argv`, `stdin?`, `cwd?`), `start` (`argv`, `label?`, `cwd?`),
`status`/`stop` (`job`), `events` (`job`, `after?`, `waitMs?` for a long poll),
`wait` (`job`), `watch` (`job`, `literal`), `list` (`scope?`), `capabilities`,
`validate`/`jev` (`request`, `provider?`, `credential?`); plus `validateDecision`
(`request`), `decisionProviders` (no fields), `decide` (`request`, `timeoutMs?`,
`credential?`, with routing inside `request`). Most work ops take `timeoutMs?`.
Unknown fields are rejected. Close stdin to end the session.

For an interactive process driven from code (a REPL, a language server, a game
bridge), `spawn` a **session child**: it ends with the session, its stdin stays
open, and its output is read by byte offset.

```text
→ {"id":1,"op":"spawn","argv":["python3","-u","-i"]}          # → {"id":"s-…",…}
→ {"id":2,"op":"write","job":"s-…","text":"print(6 * 7)\n"}    # → {"written":13,…}
→ {"id":3,"op":"read","job":"s-…","stream":"stdout","offset":0,"waitMs":5000}
← {"id":3,"ok":true,"result":{"offset":0,"bytes":3,"omittedBytes":0,"text":"42\n","next":3,"eof":false,…}}
```

Read from `next` each time; `omittedBytes` above zero means the 1 MiB rolling
window moved past your offset. `closeInput` sends end of input; `stop`, `wait`,
`status` and `events` take the `s-` id too. Ready-made single-file clients live in
`~/.local/share/jev-fabric/current/clients/` (`python/jev_fabric.py`,
`typescript/jev-fabric.ts`). The protocol reference is `docs/serve-protocol.md`
in the repository.

## Composed programs in Bend

For loops that need persistent interactive child sessions, concurrent effects or
shared deadline scopes (a game bot, a crawler, a supervisor), write a Bend
program against the library and run it:

```bash
jev-fabric -- run program.bend arg1 arg2     # compiles (needs `bend` 2.0.38), then runs
```

Legacy Jev HTTPS keeps one pooled TLS connection per process, so a Bend program
or a `serve` session making many Jev calls is much faster than repeated `jev` CLI
invocations. See
[references/bend-api.md](references/bend-api.md).

## Boundaries

- Trusted native execution, **not a sandbox**. Commands run with your privileges.
- Shell syntax only happens when you invoke a shell explicitly.
- Logs are bounded observations: the first 1 MiB per stream is spooled (the
  latest 1 MiB for session children), receipts keep 32 KiB tails, events keep
  the latest 64. Disclosed loss, never silent.
- No restart recovery, exactly-once execution or rollback. A crashed worker is
  reported failed, not resumed.
