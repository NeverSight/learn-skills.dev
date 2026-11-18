---
name: codex-implement
description: "Delegates implementation of an already-approved plan (from writing-plans) to a single long-running Codex session that writes code directly (workspace-write sandbox). Codex chooses and drives its own superpowers:subagent-driven-development or superpowers:executing-plans to work the plan end to end, including tests. Never touches git — Codex may not commit, and the skill never offers to. Always runs in the current working directory / current branch — there is no worktree mode and no mode choice. Codex runs in a sandbox that cannot install dependencies, use Docker or reliably run tests, so it hands those steps back to Claude via an IMPLEMENTATION_HANDOFF sentinel; Claude executes them (install, confirm tests are red, confirm green), reports the results into the same Codex session and resumes it — this keeps the plan's TDD order intact. Only when everything is green does Claude run the final review, finish and clean up all service artifacts. Invoke as `/codex-implement <plan-path>`."
---

# Codex Implement

FOR CLAUDE CODE ONLY. Hand a finished, approved implementation plan to Codex and let it write the code, instead of a Claude subagent or Claude itself doing it. A sidecar CLI owns the Codex process lifecycle and checkpoint/resume state; this skill launches the sidecar in the background, branches on the outcome, and — only on a clean completion — runs the one and only verification + review pass. The sidecar never runs git commands that mutate state, and neither does this skill: unlike `doc-review`, there is no optional post-run commit prompt here, under any circumstance.

## Invocation

```
/codex-implement <plan-path>
/codex-implement <plan-path> --profile=local
/codex-implement <plan-path> --status
/codex-implement <plan-path> --reset
```

- **`<plan-path>`** (required): path to the plan's markdown file, produced by `writing-plans` and already approved by the user. If missing, **stop immediately** and ask for it — never guess or default to "newest plan file in cwd."
- Codex always writes directly in the current working directory / current branch. There is no worktree mode and no flag to pick one; never ask the user where to run.
- **`--profile=<name>`** (optional): which model backend runs the implementation — `codex` (stock Codex, the default), `local` (the kit-default profile for your own OpenAI-compatible model server) or any other name from `codex.profiles`. Overrides the project config; see "Profiles" below. Without it, the profile comes from `.claude/dev-conventions.json` (`codex.implement.profile` → `codex.profile` → `codex`); the user is never asked.
- **`--status`**: print sidecar state for this plan and stop — no Codex call.
- **`--reset`**: archive prior state for this plan and start fresh on the next invocation.

## Sidecar CLI

The sidecar lives at `${CLAUDE_PLUGIN_ROOT}/scripts/codex-implement.mjs` — invoke via `node`.

```
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-implement.mjs" status  <plan-path>
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-implement.mjs" start   <plan-path> [--max-checkpoints=N] [--timeout=<minutes>] [--profile=<name>] [--effort=medium] [--model=<name>]
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-implement.mjs" resume  <plan-path> [--result-file=<path>] [--timeout=<minutes>]
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-implement.mjs" finish  <plan-path> --reason=complete|blocked|checkpoint-cap|aborted
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-implement.mjs" reset   <plan-path>
```

**`${CLAUDE_PLUGIN_ROOT}` is often empty in the Bash session** (the template path then resolves to `/scripts/codex-implement.mjs` and fails with `MODULE_NOT_FOUND`). Always call the sidecar by the absolute path of `scripts/codex-implement.mjs` inside this skill's own directory (the "Base directory" shown when the skill loads), in double quotes, without `find` and without `${CLAUDE_PLUGIN_ROOT}`: `node "<skill-base-dir>/scripts/codex-implement.mjs" <subcommand> ...`. An allowlist entry is matched against the command literally, quotes included, so use the same quoted path for every subcommand (`start`/`resume`/`finish`/`reset`/`status`) to avoid extra permission prompts.

`start`/`resume` each print a single JSON line on stdout: `{checkpoint, message_path, state_dir, session_id, done, blocked, blocked_reason, handoff, handoff_reason, handoff_count, needs_resume, at_cap, max_checkpoints}`. Parse it and act on `done`/`blocked`/`handoff`/`needs_resume` — see Step 2.

`--result-file=<path>` (a file inside the working directory, ideally in `state_dir`) is how Claude gives Codex the outcome of a handoff, or sends failed verification back after `done: true`. It is **required** by `resume` when the last checkpoint ended in a handoff, and rejected after a plain timeout. The sidecar embeds the file's content (last 40 000 characters) in the resume prompt.

All state lands in `.codex-implement/<plan-slug>/` **in the working directory the sidecar was invoked from** (normally the repository root). The sidecar never touches `.gitignore` — it doesn't add an entry for this directory. On a clean `finish --reason=complete`, the sidecar deletes the whole `.codex-implement/<slug>/` directory itself (see Step 3); on `blocked`/`checkpoint-cap`/`aborted` it's left on disk for inspection.

## Profiles

A profile picks the model backend; everything else (sandbox, prompts, handoff protocol, verification) is identical. The profile definitions are shared with the `doc-review` skill (same `codex` config block, same resolver `scripts/profiles.mjs` — keep the two copies identical), so a backend such as your own model server is described once. This skill uses the **`implement`** role.

Profile name, highest first: `--profile` → `codex.implement.profile` → `codex.profile` → `codex`. Model/effort/timeout, highest first: CLI flags → `codex.implement.*` (only for the role's own default profile) → profile fields → built-in defaults.

Profiles:
- `codex` (built-in, default) — stock Codex, model `gpt-6.1-sol`, effort `medium`. With no config at all, behaviour is identical to before profiles existed. Its model and effort are configurable like any other profile's.
- `local` (kit default) — your own OpenAI-compatible model server: three parameters, `model`, `provider.baseUrl` and the token. It is not built into the sidecar: `setup.sh` and the `update-ai-dev-kit` skill add it to `.claude/dev-conventions.json` together with an explicit `codex` entry (missing keys only, never overwriting yours). The kit cannot know your server, so it ships placeholders (`model: YOUR-MODEL`, `baseUrl: https://YOUR-HOST/v1`); replace them in the project config. The token is **never** written to a file: `provider.envKey` (default `LOCAL_LLM_API_KEY`) only names the env var, which each developer exports in their own shell. While `YOUR-…` placeholders remain the profile counts as unconfigured: `start` stops with a message saying what to replace. Any other backend is a further entry in `codex.profiles`.
- A profile other than `codex` needs a model (its own, from `codex.<role>.model`, or `--model`) unless a `codexProfile` defines it; otherwise `start` fails with a clear message.

Project config (`<repo>/.claude/dev-conventions.json`, key `codex`; the same file the repo uses for `ticketPrefix`):

```json
{
  "codex": {
    "profile": "codex",
    "profiles": {
      "codex": { "model": "gpt-6.1-terra" },
      "local": {
        "model": "my-model",
        "timeoutMin": 90,
        "provider": {
          "name": "Local",
          "baseUrl": "https://llm.example.com/v1",
          "envKey": "LOCAL_LLM_API_KEY",
          "wireApi": "responses"
        }
      }
    },
    "implement": { "profile": "local", "effort": "medium" },
    "review":    { "profile": "codex" }
  }
}
```

- `profiles.<name>` — fields override the built-in profile of that name, or define a new one. Fields: `model`, `effort`, `timeoutMin`, and the backend selectors:
  - `provider` — inline provider `{ baseUrl, envKey, id?, name?, wireApi?, queryParams? }`, declared on the fly through `-c model_providers.<id>.*` so nothing has to be added to `~/.codex/config.toml`. `envKey` is the **name** of the env var holding the API key; the key itself is never written to config or state, and `start` fails early if that variable is not set. `wireApi` defaults to `responses` — check that the server (or a proxy such as LiteLLM) actually speaks that API.
  - `modelProvider` — id of a provider already declared in `~/.codex/config.toml` (`[model_providers.*]`).
  - `codexProfile` — a `[profiles.<name>]` entry in `~/.codex/config.toml`, for setups that already live in Codex's own config.
- `implement` / `review` — per-role section: which profile that skill uses by default, plus optional `model` / `effort` / `timeoutMin` tuning that applies when that default profile is the one in use (so a `--profile` override never inherits, say, a gpt model name into a run on your own model).
- The profile is resolved once, at `start`, and stored in `state.json`; `resume` reuses it, so editing the config mid-run does not switch the model of a live session. To change it, `reset` and start over.
- The config is read from the working directory. The API key env var must be exported in the shell that launches the sidecar.
- A non-Codex model follows the long handoff/sentinel protocol noticeably worse and may lack reliable tool calling; start with a small plan. Make sure the server's context window fits the project rules plus the plan.
### Checking your server

"OpenAI-compatible" does not guarantee that Codex works: Codex talks to the **Responses API** (`POST <baseUrl>/responses`; the old chat wire API was removed), and many servers implement only `/chat/completions`. Check before the first run (`baseUrl` already includes any `/v1` prefix):

```
curl -sS "$BASE_URL/responses" \
  -H "Authorization: Bearer $LOCAL_LLM_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"<model>","input":"Reply with the single word: ok"}'
```

A JSON body with `"object":"response"` and the model's text means the endpoint exists. A 404/405 or an error about an unknown route means the server has no Responses API: put a translating proxy (for example LiteLLM) in front of it. Passing the check is necessary, not sufficient — Codex also needs streaming events and tool calls in the Responses format — so finish with a tiny plan on this profile before trusting it with a real one.

- Without `--profile` the profile is taken from the project config, with no question to the user (same as the workflow-driven `doc-review` runs). To use another backend for one run, pass `--profile`; to change the default, edit `codex.implement.profile`.
- Mention the active profile (and model) when launching and in the final report.

## Execution contract

### Step 0 — Preconditions

1. **Do not run an ad-hoc precondition command to check `codex`'s install/auth status** (e.g. `codex exec --help`, redirected/piped variants, anything with `echo "exit:$?"`) — an invented one-off compound command doesn't match the fixed Bash allowlist and re-triggers a permission prompt every single run. Rely exclusively on the first sidecar call's own error surfacing (Step 2, sub-step 6): if `start`/`resume` fails with an auth error, its stderr carries a `codex login` hint — surface that to the user and stop. Skip to sub-steps 2–3, then Step 1.
2. Resolve `<plan-path>` from the current directory and confirm it exists and is readable. Fail fast here if it doesn't.
3. **Profile — no question.** The profile comes from `.claude/dev-conventions.json` (`--profile` → `codex.implement.profile` → `codex.profile` → `codex`) and is resolved by the sidecar at `start`; do not ask the user and do not pass `--profile` unless the user gave one. A resumed run keeps the profile stored in its state. If the resolved profile is unconfigured (`YOUR-…` placeholders) or lacks a model, `start` fails with a message saying what to fix: relay it to the user and stop.

### Step 1 — Working directory

Codex runs in the current working directory on the current branch. Use `run_cwd = process.cwd()` and `plan-path` unchanged, then go to Step 2.

### Step 2 — Launch and wait

1. If `.codex-implement/<slug>/state.json` doesn't exist yet for this plan, this is a fresh run: launch the sidecar's `start` command. Otherwise (resuming an interrupted prior run), launch `resume`.
2. Run the sidecar call via `Bash` with `run_in_background: true` — a full implementation pass can run for a long time (up to the per-checkpoint timeout, default 45 min, cap 120 min), and this must not block the conversation turn. Do not add a separate polling loop that re-checks `codex-implement.mjs status` on a timer to *detect completion* — the background task's own completion notification (the sidecar process exiting) *is* the "Codex finished this checkpoint" signal — the sidecar call itself blocks until `codex exec` returns.
3. Tell the user: "Launching Codex (profile=`<name>`, checkpoint `<N>`) in the background — this can take a while, I'll report back when it finishes a checkpoint."
4. When the background task completes, parse its stdout JSON line:
   - `done: true, blocked: false` → the run is cleanly finished. Go to Step 3.
   - `done: true, blocked: true` → Codex reported it's stuck. Go to Step 3b (no verification/review — nothing coherent to check against an admittedly-incomplete implementation).
   - `handoff: true` → Codex needs commands run that its sandbox cannot do. Go to Step 2b, then `resume` with `--result-file`.
   - `done: false, handoff: false` (`needs_resume: true`, no sentinel found — the normal shape of a mid-run timeout) → if `at_cap` is true, go to Step 3c (checkpoint-cap). Otherwise, launch `resume` (back to sub-step 1) and continue looping.
5. If the background task itself errored (non-zero exit, not just "no sentinel yet") — the sidecar's stderr carries a hint (e.g. `codex login`) for auth failures. Surface it, and stop; don't auto-retry blindly on an error that isn't a plain timeout.

### Step 2b — Handoff: Claude does what the sandbox cannot

Why this exists: Codex's sandbox cannot install dependencies, reach Docker/testcontainers, or reliably run tests, and the project works by TDD (tests first, confirmed red, then implementation, confirmed green). The sidecar's prompt tells Codex to triage the plan up front and to return every such step to Claude through `IMPLEMENTATION_HANDOFF`, instead of skipping it or faking a result. The session stays warm — Codex is resumed, not restarted.

When the JSON says `handoff: true`:

1. Read the file at `message_path` — the "## Handoff requests" section lists numbered requests: the exact command, the expected outcome (`must FAIL because …`, `must PASS`, `install only`) and what to report back. Run them yourself in `run_cwd`, in order, with the narrowest commands the requests (or the repo's TDD loop commands in `CLAUDE.md`) give. Never run a project's full suite or e2e unless the request is explicitly that and the repo rules allow it.
2. **Judge each result against its expectation — do not just paste output.**
   - Install: confirm it exited 0; report the new/changed packages, not the whole log.
   - **Red check ("must FAIL")**: a test counts as red only if it fails **for the right reason** — an assertion about missing behavior, a "not a function / cannot find provider" caused by the implementation not existing yet. Failures from syntax errors, bad imports of already-existing modules, broken test config or a missing dependency are **not red**; report them as `WRONG-REASON RED`. A test that **passes** before the implementation exists is `UNEXPECTED GREEN` — report it by name.
   - **Green check ("must PASS")**: report pass counts; on failure give test names plus the first error lines and relevant stack frames, trimmed.
3. Write the report to `<state_dir>/handoff-<handoff_count>-result.md` (it lives in the service directory, so it is cleaned up with it). Format, one block per request: `### Request N — <command>`, `exit code`, `verdict: AS EXPECTED | NOT AS EXPECTED | WRONG-REASON RED | UNEXPECTED GREEN`, then the trimmed evidence. Keep it factual; do not add instructions about how to fix things.
4. Launch `resume <plan-path> --result-file=<that file>` in the background (Step 2, sub-step 2) and loop back to the branching in Step 2, sub-step 4.

Rules:
- Do the requested commands even if you suspect Codex could have run them itself — that is cheaper than a second diagnosis round.
- If a command cannot be run from this session either (Docker is down, no network), do not guess: stop, tell the user what is missing, leave the state as it is (`handoff-pending` survives; rerunning `/codex-implement` picks the handoff up again).
- Never edit Codex's code or tests yourself to make a handoff result come out as expected. The outcome is reported as it is; Codex fixes its own work.
- Handoff round-trips consume checkpoints (default cap 14). Codex is instructed to batch: do everything it can across the whole plan, accumulate all blockers, and hand them off in one go (typically install + red for all tests, then green for everything). If Codex hands off after each small group instead, that is a deviation from its instructions — do the requests anyway, but mention it in the final report. A handoff that repeats the same failing request three times in a row is a stuck loop — stop and report it as such (Step 3c style) instead of resuming again.

### Step 3 — Post-completion: verification, review, cleanup (Claude only)

Only reached on `done: true, blocked: false`. **The sidecar state is not finished yet** — `finish` runs last, only after everything is green, because it deletes the service directory and with it the ability to send work back to Codex.

1. **Independently verify** — actually run the repo's build/lint/test commands yourself, in `run_cwd`. Do not trust Codex's self-report, nor even a green you reported to it earlier in a handoff: this is the final run over the finished tree. Prefer, in order: (a) the exact commands the plan's own "Testing strategy"/verification section names, if present — that's the authoritative source; (b) the target repository's own documented conventions (`package.json` scripts, `CLAUDE.md`, `Makefile`, etc.). Never hardcode one stack's commands — discover them per-repo. The repository's rule against running the full suite/e2e automatically still applies: run what the plan names and the affected specs, not everything.
2. **Anything red → back to Codex, not forward.** Write the failures (command, failing test names, first error lines, trimmed) to `<state_dir>/verification-<n>-result.md` and launch `resume <plan-path> --result-file=<that file>` — Codex fixes it in the same warm session. Then loop through Step 2 again and return here on the next `done: true`. Do not patch Codex's code yourself and do not call `finish` while anything is red. The same stuck-loop rule as in Step 2b applies (the same failure three times in a row → stop and report).
3. **Only when verification is fully green: one final code review** — invoke `superpowers:requesting-code-review` if it's available in this environment, scoped to the diff this run actually produced: `git diff <base_sha>..HEAD` plus any uncommitted working-tree changes, where `base_sha` is the value the sidecar captured in `state.json` before checkpoint 1 (read it with `status` before `finish`). If it isn't available, do a direct read-through of the same diff yourself. There is exactly one review pass — no per-checkpoint or per-task review. If the review finds real defects, route them back through step 2 (a `--result-file` with the findings), then re-verify.
4. **Cleanup, once verification and review are clean.** Call `finish --reason=complete`: the sidecar returns the run summary inline (`summary` field; keep it for the Step 4 report) and deletes the whole `.codex-implement/<slug>/` directory — state, checkpoint prompts/messages, handoff and verification result files. After that no Codex artifacts remain, and the task is done for Codex.
5. **Plan-file cleanup is Claude's job, never Codex's.** Codex is instructed never to delete, rename, or move the plan file, even if the repository says to delete a plan file after implementation. If the target repository documents such a convention (check `CLAUDE.md`/`AGENTS.md`/`.claude/rules/**`), delete the plan file yourself now — it is the last step, after the green verification and clean review above, never while issues are outstanding.
6. Report to the user per the format in Step 4.

### Step 3b — Blocked

Codex signaled `IMPLEMENTATION_BLOCKED: <reason>`. Call `finish --reason=blocked`. Report the reason to the user directly; skip verification and review entirely — there's nothing coherent to check against a run Codex itself says didn't finish. Tell the user they can resolve whatever's blocking it and re-invoke `/codex-implement <plan-path>` — the sidecar detects existing state and resumes automatically rather than starting over.

### Step 3c — Checkpoint cap hit

`max_checkpoints` reached (default 8) with no sentinel ever seen across any checkpoint. Call `finish --reason=checkpoint-cap`. Report this as a likely-stuck or looping session — point the user at `.codex-implement/<slug>/checkpoint-*-message.md` for inspection. Do not attempt verification or review; the implementation is, by definition, in an unknown/incomplete state.

### Step 4 — Final report to the user

On clean completion (Step 3), print a compact report:

```
codex-implement on <plan-path>: complete after N checkpoint(s) (profile <name>/<model>).

Verification:
- build: <pass/fail, one line>
- lint: <pass/fail, one line>
- tests: <pass/fail, one line — counts if available>

TDD gates (via handoff): <N handoff(s); red confirmed for <groups/specs>, green confirmed — or "no handoffs needed">

Code review (superpowers:requesting-code-review): <one-line summary — clean, or N findings by severity>

Changes: <files changed count>, uncommitted.

Service files cleaned up (.codex-implement/<slug>/ removed).
```

**Never propose or perform a commit — this line must be absent from the report entirely, not merely answered "no."** This is a hard difference from `doc-review`, which offers an optional post-loop commit; this skill has no equivalent, ever, in any outcome.

## Important constraints

- **Codex writes files directly** (`-s workspace-write` sandbox) — this is the entire point of the skill, unlike `doc-review` where Codex is read-only and Claude applies every edit. There is no human-in-the-loop edit-approval step per file; the safety net here is the independent verification + review pass in Step 3, done once, after the fact.
- **Never `--dangerously-bypass-approvals-and-sandbox`, never `--ephemeral`.** The sandbox stays at `workspace-write` (not full-access), and session persistence must stay on so `resume` remains possible after a timeout or crash.
- **Codex never deletes the plan file, even if a repository convention says to delete it after implementation.** The initial and resume prompts both carry this as a hard constraint, overriding any such convention Codex reads in the target repo's own `CLAUDE.md`/`AGENTS.md`/rules. Deleting the plan file (if the target repo's conventions call for it) is Claude's own responsibility in Step 3, after verification and review both pass — never something Codex does mid-run or unprompted.
- **Git is off-limits to Codex, absolutely** — the initial prompt states this as a hard constraint that overrides the chosen superpowers skill's own instructions (e.g. `subagent-driven-development`'s implementer template normally says to commit after each task; Codex must skip that step here). Verify this wasn't violated as part of Step 3's review — if a review finds a commit was made anyway, flag it prominently to the user; that's a Codex misbehavior, not something to quietly work around.
- **One Codex call for the whole plan, not one per task-group.** Claude does not split the plan into task groups itself — Codex's own chosen superpowers skill (`subagent-driven-development` or `executing-plans`) handles that internally, invisibly to this skill. Resist the temptation to add task-splitting logic here; it duplicates what Codex already does and reintroduces the review-cadence complexity this design deliberately avoids.
- **No intermediate reviews.** Only the single Step 3 review pass, after Codex signals full completion and verification is green — never after individual checkpoints. Handoffs (Step 2b) are command execution on Codex's behalf, not reviews: Claude runs, judges against the stated expectation and reports; it does not critique the code.
- **Handoffs are batched, not per-group.** Codex works on everything it can first, accumulates all blocked verifications, and only then hands them off in one request list. Once Claude unblocks them, Codex continues with everything now reachable, again until the next real blocker. Claude's side of this: execute the whole request list in one pass and report all results in one result file.
- **The sandbox boundary is a handoff, not a skip.** Dependency installs, Docker-backed suites, red/green confirmations and anything else Codex's sandbox cannot do are executed by Claude (Step 2b) and fed back into the same Codex session. Codex must not write implementation for a unit before its tests were confirmed red for the right reason; Claude must not soften a `WRONG-REASON RED` or `UNEXPECTED GREEN` result into `AS EXPECTED`.
- **`finish` comes last.** It deletes the service directory, so it is called only after the final verification is green and the review is clean (Step 3). Before that, failures go back to Codex with `resume --result-file`.
- **State lives in the CWD, not the skill.** `.codex-implement/<slug>/` is written relative to wherever the sidecar was invoked from (the working directory).
- **`.gitignore` is never touched.** The sidecar does not add a `.codex-implement/` entry anywhere. Instead, the service directory is deleted automatically on a clean `finish --reason=complete` (see below), so there's normally nothing left behind to ignore.
- **Service files are deleted after a clean completion, kept otherwise.** On `finish --reason=complete` the sidecar `rm -rf`s the whole `.codex-implement/<slug>/` directory (state.json, checkpoint prompts/messages/stdout, handoff/verification result files, `.lock`) after folding the summary into its JSON output. On `blocked`/`checkpoint-cap`/`aborted` the directory and `final-summary.md` are left on disk — Step 3b/3c point the user at those files for inspection, and a later `resume` needs `state.json` to still exist.
- If `codex` is not available or returns auth errors, tell the user to run `codex login` or `/codex:setup` and stop.

## Troubleshooting

- **`run is waiting on a handoff: pass --result-file=…`**: the last checkpoint ended in `IMPLEMENTATION_HANDOFF`; perform Step 2b and pass the report file. Re-running `/codex-implement <plan>` after a crash lands here too — read the last `checkpoint-*-message.md` for the pending requests.

- **"state dir locked"**: another `start`/`resume` is running for the same plan. Wait, or inspect `.codex-implement/<slug>/.lock`.
- **Resume after a crash**: just re-run `/codex-implement <same-plan-path>`. The sidecar detects existing non-terminal state and calls `resume` with the stored session id — no fresh session, no re-reading the plan from scratch (Codex's own warm context plus a fresh `git status`/`git diff` orients it).
- **Session id missing after a `start` failure**: rare — if the very first checkpoint crashed before Codex emitted its first JSONL event, there's no session to resume; run `reset` and start over.
