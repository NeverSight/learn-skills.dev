---
name: agent-observability-replay-trace
description: >-
  Use when a developer wants to iterate on ONE specific Agent Observability / LLM Obs trace whose output
  they didn't like — re-running that trace against their LOCAL code, seeing a concise diff of the old vs
  new output, and looping (change code → replay → diff) until satisfied. Invoked as
  /agent-observability-replay-trace <trace-id> [changes to test]. Signals: "replay this trace"; "iterate on
  a trace"; "this trace's output is wrong, fix it and re-run"; "re-run trace <id> with <change>"; pasting a
  trace id from the Agent Observability UI with a description of what to fix. It fetches the trace via the
  datadog-llmo MCP or the pup CLI, edits code, re-runs the app to emit a NEW trace, and
  diffs the two — no local server, no browser. For agents traced with ddtrace / LLM Obs (Python first-class), with JSON-serializable entry
  input. Do NOT use for: scored Experiments or the browser "Replay" button (that's
  agent-observability-replay-experiment), building an experiment from a dataset/CSV, writing evaluators,
  root-causing failed traces, or RUM/HTTP session replay.
---

# Replay a trace against local code

A fast **iteration loop** on a single production trace: take a trace whose output a developer didn't like,
optionally change the code, **re-run it against their LOCAL code**, and show a concise diff of old vs new
output — repeating until they're happy. Assumes nothing about the project's layout.

Invoked from the developer's coding agent: `/agent-observability-replay-trace <trace-id> [<changes to test>]`.
With no modification, do the replay + diff only (a reproduce/regression check), then offer to enter the loop.

**This file is the workflow spine — terse on purpose. The depth lives in `references/details.md` (trace
backend + pup flags, the runner contract, export mode, polling, the trace-link scoping fix) and
`references/local-setup.md` (making a deployed-only app locally runnable). Read `details.md` before you touch
pup or generate the runner.**

**Writing code — keep comments minimal to none.** Everything you generate or edit (the annotation, the
runner's `ENTRYPOINTS` entries, a local harness, iteration edits) should match the surrounding code and
carry **no unnecessary comments** — don't narrate what the code plainly does; add a comment only for a
genuinely non-obvious *why*.

**Intent tagging:** On every `datadog-llmo` MCP tool call, prefix `telemetry.intent` with `skill:agent-observability-replay-trace[<inv_id>] — ` (a short per-run id, generated once and reused for every call) followed by a description of why the tool is being called. On the **first MCP tool call only**, use `skill:agent-observability-replay-trace:start[<inv_id>] — ` instead (note the `:start` suffix). Example first call: `skill:agent-observability-replay-trace:start[3a9f1c2b] — fetch the original trace's baseline output`. pup-CLI calls carry no `telemetry.intent`, so this applies only on the MCP path.

## Interaction model — selector gates, never a hard stop

This is a live loop. At every decision point present the choices as an **`AskUserQuestion` selector** (the
plan-mode-style menu), not a plain question that ends your turn. Two gates: (a) after you propose code
changes, before replaying; (b) after each diff. The selector's free-text option lets the user type detail
(what to refine) inline — act on it directly, don't ask a follow-up. Keep re-presenting after every replay
until they pick "stop here".

## Scope — check first

- **Traced with `ddtrace` / LLM Obs** (an `ml_app` + a discoverable entrypoint). **Python is first-class**;
  other languages work but you write the runner to the contract in their SDK/build tooling.
- **JSON-serializable entrypoint input**, and a **callable seam** for the root span (see step 3.5 — not a
  binary "is it runnable?"; deployed-only apps often still expose a plain callable).
- **A trace-access backend** — the `datadog-llmo` MCP (used when present) or the `pup` CLI (fallback, and
  the easier install if you have neither) (step 0).
- **Credentials:** `DD_API_KEY` + `DD_SITE` + provider key(s). **Not `DD_APP_KEY`** — plain trace, not an
  Experiment (that's `agent-observability-replay-experiment`).
- **Side effects, irreversible:** replaying re-runs real code (model spend + real writes), and **LLM Obs
  traces cannot be deleted** — a mis-scoped replay (wrong ml_app) *permanently* pollutes the production app's
  dashboards/eval sets. That's why the `<ml_app>-local` isolation (steps 4/6/7) is load-bearing, not tidy.
  Warn before the first replay.

## Workflow

### 0. Ensure a trace-access backend
Pick, in order: (1) the **MCP** if `mcp__datadog-llmo-mcp__*` tools are present — the default (slightly
richer for reads: structured tree + `content_info`); (2) else **`pup`** if installed and `pup auth` targets
the app's org; (3) else the user has neither → guide the **pup install** (it's easier to set up than the
MCP, so recommend pup here):
```
brew tap datadog-labs/pack && brew install datadog-labs/pack/pup
pup auth login
```
(MCP alternative: `claude mcp add --scope user --transport http "datadog-llmo-mcp" "https://mcp.datadoghq.com/api/unstable/mcp-server/mcp?toolsets=llmobs"`; see https://docs.datadoghq.com/bits_ai/mcp_server/setup/.) Don't proceed without a backend.
The backend↔operation mapping and **pup's exact flags/gotchas are in `details.md` — read that section before
using pup.** Two pup musts: (1) results come back at **`data.spans[]`** *or* top-level **`spans[]`**
(varies by version/`--no-agent`) — parse **whichever is present**, or you get zero hits on an ingested
trace (a silent false negative, step 7); (2) check **token expiry** (`pup auth status`), not just that auth
exists — expiry mid-loop looks like "trace not found."

### 1. Parse the command
`<trace-id>` + optional free-text modification (everything after the id); none → diff-only mode. Determine
the `ml_app` from the project (`LLMObs.enable(ml_app=…)` / `DD_LLMOBS_ML_APP`) or the trace; confirm if
ambiguous.

### 2. Fetch the trace + locate the baseline
Fetch via the backend; note `total_duration_ms` (drives step 7), the `trace_url`, and
`metadata.replay_input`/`replay_entrypoint` if present. **Locate the baseline field — it's not always the
root output:** the value the developer dislikes may be a tool-call input or an intermediate output several
levels deep, and the app may post-process it before the span records it. Pick the field the code change can
actually move, or the delta drowns in noise.

### 2.5. Check for fan-out
If the root span **fans out into repeated sibling subtrees** (a batch/map over N parallel sub-runs), the
change under test is usually visible in a **single** branch — replaying the whole root costs ~N× spend and
time for no extra signal. Offer to replay one representative branch; **log what you skipped**. **Pick deliberately: the cheapest
branch that reached the terminal / side-effecting tool** (most branches are no-ops that prove nothing), and
reconstruct its input from the **child** span's input, not the root's. Full root only if the change is
inherently cross-branch.

### 3. Resolve the entrypoint + input
- **Entrypoint:** `metadata.replay_entrypoint` if present; else infer from the root span (name/kind) + code
  and **confirm with the user**.
- **Input:** `metadata.replay_input` if present; else derive a **suggested** input (prefer the code
  signature — the rendered prompt is lossy) and have the user **confirm/edit**.

### 3.5. Ensure a local run path (find the innermost callable seam)
Ask **"what is the innermost callable seam for this root span, and can I call it directly with JSON?"** — not
"is the app runnable?". Already directly callable → **skip, continue**. Buried under a handler/service
(deployed-only, no local `__main__`, live-infra coupling) → follow **`references/local-setup.md`** (detect →
propose → approve → build). The common middle case — a deployed service whose core logic is *already* a plain
callable (ports-and-adapters) — just extract/call that seam; full local-setup is overkill.

### 4. Ensure the two persistent artifacts (one-time setup)
- **a) In-entrypoint annotation** on the app's **real** entrypoint, so all future traces (production too)
  self-describe. Stamp it at **span start, not the success/deferred-finish path** — a failed run must still
  carry `replay_input` (those are the ones you most want to replay):
  ```python
  LLMObs.annotate(span=span, metadata={"replay_entrypoint": "<stable id>", "replay_input": <extractor>})
  ```
  No `replay_output` — the original trace is the baseline. (Non-Python annotate APIs differ — e.g. Go
  `span.Annotate(llmobs.WithAnnotatedMetadata(...))`; see `details.md`.)
- **Isolation pre-flight (before writing the runner):** grep the entrypoint's call path for **per-span/
  per-call ml_app overrides** (Go `llmobs.WithMLApp`; Python `ml_app=` on a decorator or in
  `LLMObs.annotate`). Those **beat** the init-level `-local`, so the app's spans can still land in
  production — tracer-level config is **not** proof of isolation. If any exist, the app's ml_app must
  resolve from env so `-local` wins.
- **b) The runner** — satisfies the **language-independent runner contract in `details.md`** (load env →
  derive `<ml_app>-local` → dispatch one entrypoint on JSON → **flush on every exit path incl. errors** →
  **refuse to start unless ml_app ends in `-local`** → print the `-local` ml_app). **Python:** copy
  `scripts/replay_runner_template.py` and fill `ENTRYPOINTS`. **Other languages:** write to the contract —
  don't assume the Python API carries over (Go APIs + export-mode gotchas in `details.md`), and where the
  language has no in-process dotenv add a **run wrapper (artifact c)** that sources the project env, unsets
  ambient provider vars, and exports the `-local` override. Infer + **confirm the run command**; follow the
  host repo's **build-file conventions** (Bazel/Gazelle → `cmd/<name>/`, run Gazelle, build before replay).

### 5. (If a change was requested) edit, then gate
Make the code changes, show the developer the diff of your changes, then an `AskUserQuestion` selector:
**Replay now** / **Adjust the changes first** / **Cancel**. Only replay on "Replay now".

### 6. Replay
Before the first replay: **warn** (re-running is real — model spend + real writes), and **sanitize the
environment**. The **coding agent's own env** (`ANTHROPIC_API_KEY` / `ANTHROPIC_BASE_URL` set by Claude
Code, and other provider keys) can make the app's SDK **bypass its configured model gateway** — a fidelity
gap **invisible in the diff**. **Unset ambient provider vars by default and report that you did** (don't
just ask); grep the app for its own ambient-key guards. Also **verify the credential's org matches the
trace's org** — a mismatch ships the replay somewhere you can't query (looks like ingest lag).
On confirmation, record `t0` and run — **source the project's env file, never inline secrets** (the marker
tag is fine on the command; `DD_API_KEY=<value>` inline is blocked by the permission classifier and leaks to
history/transcript — use the wrapper/env-file):
```
DD_TAGS=replay_run_id:<unique-id> <run cmd or wrapper> --entrypoint <id> --input-file <path>
```
The runner emits **under `<ml_app>-local`** (idempotent, so replays never pollute production) and prints that
name — poll for the new trace **under it**.

### 7. Wait for the new trace
- **Runner subprocess timeout** = `max(120s, ~3 × total_duration_ms)`.
- **Ingest poll:** after it returns, poll the backend **every ~5s up to ~2 min** for the `replay_run_id` tag
  under `<ml_app>-local` (pup: `--query "replay_run_id:<id>"`, plain `key:value`). **Before ever reporting
  "not found," re-query with no tag filter** (just `<ml_app>-local` + window): if that returns spans, your
  filter/parse/scope is wrong — **not** ingestion. A false "no trace" reads as normal and invites a wasteful
  re-run.
- **Verify isolation on each hit — a tag match is NOT proof.** `--query`/tag matching can return a span
  whose real `ml_app` is a *different* app (the `--ml-app` filter gets ignored). Read `ml_app` off every
  returned span and **assert it ends in `-local`** before reporting a clean replay — otherwise you report
  "clean replay under `-local`" while the trace is actually in production (which you can't undo). This false
  *confidence* is worse than the false negative. Don't hard-fail on timeout; offer to keep waiting.

### 8. Diff (with links to both traces)
Concise summary of how the **new output differs from the old** — meaningful differences only. Note live-world
drift; and because any nondeterministic agent varies run-to-run, **default to two replays** (diff-only mode
too, not just model-facing edits) and use **replay-to-replay comparison** — if the two local runs differ
from each other about as much as from production, the delta is sampling variance, not your change. If the
replay **disables a side-effecting integration** (dry-run), that integration's subtree is absent — **exclude
it from both sides** before comparing span counts, or the structural diff is junk. Lead the diff with both
trace links:
- **Old:** `trace_url` **verbatim** — but **under fan-out** (you replayed one branch) link the **branch
  span**, not the whole-root url.
- **New (replay):** must carry `ml_app=<ml_app>-local` or it opens **empty** — and the `trace_url` is an
  org-switch wrapper (`…/switch_to_user/<id>?next=<encoded /llm/traces …>&flow=org_switch`), so **inject
  `ml_app=<ml_app>-local` into the decoded `next` query and re-encode; do NOT append to the outer URL**
  (mechanics in `details.md`). Browser-unverifiable from here — confirm once it opens non-empty.

### 9. Gate — iterate, or stop on a broken harness
**Harness-failure gate (before the diff):** if a replay reveals the harness is wrong — trace landed under
the wrong ml_app, no trace after the step-7 sanity checks, missing flush, or auth/org misrouted — **do NOT
proceed to a diff on bad data.** Stop and present a selector to fix the harness (re-scope ml_app / add flush
/ fix env) and re-replay.
Otherwise, after the diff, an `AskUserQuestion` selector: **Looks good — stop here** (finish; leave the edits
in the working tree) / **Make more changes** (free-text inline → back to step 5). Re-present after every
replay; end only on "stop here".

## Reference
- `references/details.md` — trace backend + **pup exact flags**, the **runner contract** (+ Go, export mode),
  polling + the false-negative sanity check, the **trace-link scoping fix**, limitations. Read before pup / the runner.
- `references/local-setup.md` — making a deployed-only app locally runnable (step 3.5). Read when that gap shows.
- `scripts/replay_runner_template.py` — the Python runner to copy + fill.
