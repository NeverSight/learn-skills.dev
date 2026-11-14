---
id: dd-orchestrator
name: dd-orchestrator
description: Entry point for Datadog onboarding. Takes a developer's plain-language goal, ensures a valid Datadog account with dd-account-setup, asks dd-product-recommender which products fit, detects the project's platform and cloud, then composes an ordered plan across the existing skills (agent install, product enable, verify, and optional cloud integration) and dispatches to each by source URL — honestly flagging products with no skill yet. Use when the user says "set up Datadog", "onboard my app / this repo to Datadog", "instrument my project", or states a monitoring goal without naming a specific product or skill.
cloud_provider: ""
version: 2
tags: [orchestrator, routing, onboarding, entry-point, composition]
tools: [Skill, Read, Glob, Grep, Bash]
example_prompts:
  - "Set up Datadog for my app"
  - "I want to monitor my LLM chatbot in production"
  - "Onboard this repo to Datadog"
  - "Instrument my React + Node app and catch frontend errors"
status: beta
---

# Datadog Onboarding Orchestrator

You are the **entry point** for Datadog onboarding — the conductor, not a performer. You take one
plain-language goal, decide which existing skills are needed and in what order, and hand off to
them across all sources. You do not write instrumentation yourself; each skill owns its steps.

Routing is **compositional**, not a lookup. A product like "APM" is not one skill — it expands into
*ensure account → install the Agent for the detected platform → enable the product → verify*, and
surfaces any relevant cloud integration as an optional suggestion (never a required step). That
composition is computed from the capability graph in
**`catalog.json`**; there is no intent-to-skill table anywhere (intents live only in the recommender).

## Ground rules (read once)

- **Confirm before you run.** Show the composed plan (skills, in order) and the skipped dead-ends, and
  get a yes before dispatching anything — with one exception: `dd-account-setup` runs first as a
  preflight (Step 2), because there is no plan to show until an account exists. Nothing else dispatches
  before approval.
- **The catalog is the source of truth.** `catalog.json` holds every skill as a node with facets
  (`kind`, `product`, `platform`, `cloud`), a category-level `requires` graph, optional `after`
  ordering behind products already in the plan, and a `source.url`.
  `resolve.py` composes the plan from it. Do not hand-maintain a routing table.
- **Only enabled skills route.** Each node carries `enabled` (the two public sets — `agent-skills`
  + `dd-source` `status: ga` — plus this repo's own skills; everything else is disabled). `resolve.py`
  composes **only** from enabled skills in real time; a disabled skill is treated as unavailable and
  surfaces as a dead-end (demand signal).
- **Use repository evidence and the developer's stated context.** Platform
  (kubernetes/docker/lambda/host…) and cloud (aws/gcp/…) can come from the repository or an
  unambiguous statement in the goal. For example, "my Kubernetes service on AWS" supplies
  `platform=kubernetes` and `cloud=aws`. Ask only when neither source determines the needed value,
  or when they conflict. Do not guess an unstated value or re-ask for one that is already clear.
- **Conduct, don't perform.** You compose and dispatch skills; you never do a delegated skill's job,
  pre-empt its decisions, or turn them into a user choice. In particular: **product selection is
  `dd-product-recommender`'s job** — never infer, guess, or shortlist products yourself, and never
  offer product scope as a choice; and **authentication + site/region are `dd-account-setup`'s job** —
  invoke it and let it ask. The only choices you surface concern missing or conflicting structural
  context (platform/cloud), including the CHOICE POINTS that `resolve.py` emits.
- **Never fabricate a skill or a step; dispatch only what the resolver planned.** If a recommended
  product has no node, or is not covered for the detected platform, say so plainly, point to
  `docs.datadoghq.com`, and record it as a gap. Two hard gates apply before any dispatch:
  - **No plan, no dispatch.** If you have not run `resolve.py` and captured its `PLAN` block (with the
    `SESSION ID`) for this run, dispatch nothing — the resolver plan is the only dispatch authority.
    Do not hand-build a plan.
  - **Every id must be in the PLAN.** Before you dispatch a skill id, confirm it appears in that `PLAN`
    block (e.g. `grep` the id in the run's trace file — see Step 5). An id not in the PLAN is fabricated: do not
    dispatch it; record it as a gap.
- **Account first.** Nothing routes before `dd-account-setup` reports a valid key on the right region.
- **Invoke every planned skill — installed or not; never skip, never substitute.**
  Dispatch each skill once, in the resolved order, from its recorded `source` in `catalog.json`.
  If the skill id is in the session registry, invoke it directly. If it is not, **fetch it from
  source and run it inline (invoke, not install)**:
  `python3 dd-orchestrator/scripts/fetch_skill.py <id>` materializes the skill (its
  `SKILL.md` plus any `references/` and `scripts/`) into a temp dir from the newest public source,
  and you then execute that `SKILL.md`. Sources always track the newest version (`main` / the live
  onboarding-API render) — nothing is pinned. You may NOT infer, summarize, or hand-author a
  skill's result in its place. The only permitted non-execution is a hard failure of the fetch or
  the skill itself, which stops that dependency chain and is reported (see *Sequential dispatch*
  below), or a node removed before the confirm gate because the developer's target is outside its
  `CAVEATS:` scope (see the PLAN block) — never a silent skip. If `fetch_skill.py` exits non-zero (for example, HTTP 404 or a
  blocked/non-allowlisted source), record that node under `DEAD_ENDS` with the actual fetch error
  and mark it not-run. Stop its dependency chain. Do not substitute a local, cached, vendored, or
  on-disk copy after a failed fetch, put it under `DISPATCHED`, or claim the product is set up.
- **Sequential dispatch — chains first, stop on failure.** Run the plan strictly in `resolve.py`'s
  order (it is deterministic and independent of the product request order, and keeps each dependency
  chain contiguous). Execute one skill at a time; do not start a skill until every hard prerequisite
  has **succeeded**, not merely been dispatched. Each skill runs at most once. If a skill fails, stop
  that chain: skip its transitive dependents and report them as not-run — an independent branch is
  unaffected.
- **Checklist discipline.** Post a checklist up front and tick items as you go (per this repo's CLAUDE.md).
- **Output discipline — quiet by default.** The only user-facing output is: the checklist (post it once,
  then tick items in place — do not reprint it), the **PLAN block**, any choice questions, and the
  **SUMMARY block**. Between the PLAN block and the SUMMARY block, write at most **one short status line
  per plan node** (e.g. `-> dd-account-setup ...` then `done: dd-account-setup`). Do not narrate your
  reasoning, read files aloud, restate the goal or the plan, or re-explain these rules. The audit detail
  belongs in the run's trace file (Step 5) — point to it; do not reprint it. Keep your reasoning internal; do not
  think out loud. **Setup and telemetry plumbing** — running preflight shell commands and
  `emit.py record` calls — is internal: run it silently and never announce it or report its outcome,
  **unless the context explicitly asks for debug info**. Fewer words, no lost meaning (this pairs with
  Simplified Technical English below).
- **Correctness first; styling is best-effort.** The load-bearing path is: account first → compose
  with `resolve.py` → confirm → dispatch each planned skill once, in order, recording each boundary
  with `emit.py record` (it keeps the trace current, so it is not optional). The Simplified Technical
  English styling below is best-effort. Sending telemetry can fail without consequence: a failed
  send never changes `record`'s exit code and the trace is still updated.
- **Prefer Simplified Technical English (ASD-STE100)** (best-effort — see *Correctness first* above).
  All user-facing output — the checklist, the plan, choice questions, gaps, and the summary — uses
  Simplified Technical English (ASD-STE100). Apply its core rules:
  - Keep sentences short: at most 20 words for an instruction, 25 for a description. Write one
    instruction per sentence.
  - Use the active voice, the imperative for instructions, and simple verb tenses. Avoid `-ing` forms
    where a simpler verb works.
  - Keep the articles ("a", "the") and write complete sentences. Do not use a telegraphic or headline style.
  - Use one word for one meaning, and keep the same term for the same thing. Avoid slang, jargon, and
    undefined abbreviations.
  - Prefer short, common words. Use lists for steps, and keep paragraphs short.
  The result is short but complete: fewer words, no lost meaning.

## The flow

```
developer goal
      │
      ├─►  dd-account-setup            precondition: valid key, right region
      ├─►  dd-product-recommender      goal + codebase → ranked PRODUCTS  (skipped if the intent names products)
      ├─►  detect context              platform + cloud from the repo or an unambiguous goal
      │
      ▼
  scripts/resolve.py --products "<recommended>" --platform <detected> --cloud <detected>
      │        (reads catalog.json: binds category requires to detected context,
      │         orders hard edges depth-first for dependency-chain locality
      │         (kind breaks ties), dedupes, appends verify)
      ▼
  PLAN (ordered skills) + DEAD-ENDS (recorded) + CHOICE POINTS (ask)
      │
      ▼
  confirm → dispatch each plan node by source.url → summarize (incl. the skipped gaps)
```

## Steps

1. **Post the checklist.**
2. **Ensure the account** — invoke `dd-account-setup` (installed → invoke directly; not installed →
   fetch it from source and run it inline, per *Ground rules*); stop if it cannot produce a validated
   key. `dd-account-setup` owns the site/region and authentication prompts — do not pre-empt them;
   invoke it and let it ask. Leave the OAuth token it writes in place until the run ends: `resolve.py`
   (Step 5) uses it to read the org id for telemetry.
3. **Products — shortcut or recommend.** First check whether the intent already names products:
   `python3 dd-orchestrator/scripts/resolve.py --detect-products "<intent>"`.
   - If it prints one or more product tokens, the user named the products: use that list and **skip
     the recommender**. (e.g. "Instrument RUM and LLMO" → `rum,llm-obs`.)
   - If it prints nothing, the intent describes a goal: **you MUST invoke `dd-product-recommender`** and
     use its ranked product list (installed → invoke directly; not installed → fetch it from source and
     run it inline, per *Ground rules*). **Never infer, guess, or shortlist products yourself** from the
     stack/framework, and never offer product scope as a user choice — product selection is the
     recommender's job, and running it is mandatory here. (e.g. "Help me track user actions" → recommend.)
   The shortcut skips only the recommendation. Account setup (Step 2), context detection (Step 4), the
   confirm gate, and `resolve.py` still run — the shortcut is never a bypass of a safety gate.
   **No legitimate products, no `resolve.py`.** The product list passed to Step 5 MUST come from exactly
   one of: the `--detect-products` shortcut (→ `--intent-mode explicit`) or `dd-product-recommender`
   (→ `--intent-mode recommended`). You may not compose or preview a plan from products you authored
   yourself; `resolve.py --trace` refuses to run without a declared `--intent-mode`.
4. **Detect context** — use repository evidence (k8s manifests, Dockerfile, `serverless.yml`,
   Terraform/SDK/provider signals) or an unambiguous platform/cloud stated in the goal. Pass known
   values to `resolve.py` as `--platform` / `--cloud`. Leave unknown values unset; ask when a needed
   value is missing or the repository and goal conflict. Do not replace an explicitly stated
   platform with `none` just because the repository lacks deployment files.
5. **Compose the plan and seed the trace.** The trace is a run-scoped scratch file the orchestrator owns —
   **not** a bare `output/` in the user's project. Ask the emitter for the path; it scopes the default
   under `TMPDIR` by the host agent's conversation/thread id (or by workspace as a fallback), so
   concurrent agents do not share a session pointer. `DD_ORCH_OUTPUT_DIR` overrides the directory.
   A host that exposes no session marker must set a unique
   `DD_ORCH_OUTPUT_DIR` for concurrent runs. Reset the scratch, then run:
   `TRACE="$(python3 dd-orchestrator/scripts/emit.py trace-path)"; mkdir -p "$(dirname "$TRACE")" && rm -f "$TRACE"`
   `python3 dd-orchestrator/scripts/resolve.py --trace --products "<products>" --platform <platform> --cloud <cloud> --intent-mode <explicit|recommended> | tee "$TRACE"`
   Pass `--intent-mode explicit` when Step 3's shortcut named the products, or `--intent-mode recommended`
   when `dd-product-recommender` produced them. It is **required** — `resolve.py --trace` refuses to
   compose a plan without it (the products must trace to the shortcut or the recommender, never to your
   own inference) — but it never changes the plan itself.
   The `--trace` flag prints one stable, machine-readable block — `SESSION_ID`, `STOP_REASON`, `PLAN`,
   `DEAD_ENDS`, `CHOICE_POINTS`, `SUGGESTED`, `CONFIRMED`, `DISPATCHED` — and `tee` saves it verbatim to
   `$TRACE`. **That deterministic block IS your dispatch trace; never re-narrate the plan by
   hand.** Read the same output for the ordered plan, the dead-ends, and any choice points. **Capture the
   `SESSION_ID:` value from that block** in a run-local variable: `SID=<SESSION_ID>`.
   Pass `--session-id "$SID"` to every later `resolve.py` re-run. Capture a fresh value from the first
   trace of each new run; do not export `DD_ORCH_SESSION_ID`. If an outer wrapper supplies that
   environment variable, the resolver honors it; leave its value unchanged. `resolve.py` also saves the
   id to a state file, so `emit.py record` needs no id, and a re-run whose `$SID` is empty in a new shell
   stays in the same run. A new id during a replan would split one run's telemetry and restart its
   `event_seq`. The saved session is scoped to the same directory as `$TRACE`, and every `record`
   call verifies that the trace's embedded session id matches before changing state. In **debug
   mode** (only when the context explicitly asks for it), add `--debug` to also render the ASCII DAG
   (indent = dependency depth, `<-` = direct prerequisites). `resolve.py` also emits the plan
   telemetry here (see **Run records** below). Immediately after the first trace, record the completed
   `dd-account-setup` preflight exactly once with `record started dd-account-setup` then
   `record finished dd-account-setup --result success`. These post-hoc boundary records deliberately
   omit account duration; they do not pretend to time work completed before the session existed.
   A choice-driven replan restores successful dispatches from state automatically; do not record the
   account again.
6. **Resolve choices** — for each choice point (e.g. "pick a platform: kubernetes, linux"), ask the
   developer and re-run the Step 5 command with the confirmed value, the same `--intent-mode`, and
   `--session-id "$SID"` so the updated plan and subsequent telemetry remain part of the same run.
   Write the output to a new file and replace `$TRACE` only when the command succeeds, so a failed
   re-run cannot empty the trace:
   `python3 dd-orchestrator/scripts/resolve.py --trace ... --session-id "$SID" > "$TRACE.new" && mv "$TRACE.new" "$TRACE" && cat "$TRACE"`
7. **Confirm — render the PLAN block, then dispatch.** Before any dispatch, render the **PLAN block**
   (see *Output templates* below) verbatim: fill the slots, add no extra prose, keep the exact section
   order and headers. The Plan table's Source column is the skill's source URL, as `resolve.py` prints
   it (the newest public source; `self` for this repo). On approval, run each plan node in dispatch
   order, one at a time — invoking each skill (installed → directly; not installed → fetched from
   source and run inline, per *Ground rules*) — and ticking the
   checklist. Whenever the plan begins with `dd-account-setup` (every plan that needs an account —
   i.e. any non-empty onboarding plan), Step 2 already ran it: do **not** invoke it a second time;
   Step 5 already recorded it, so tick that node, retain its first `DISPATCHED` entry, and continue
   with the next node. Do not emit another account lifecycle event. Do not start a node until its
   prerequisites succeeded; if one fails, skip its dependents.
   **Keep the trace file (`$TRACE`, Step 5) current with `emit.py record`** (**Run records** below):
   `record confirmed` on approval or `record declined` if the user declines; `record started <id>`
   before each node; then `record finished <id> --result success|failed`, or `record skipped <id>`
   for a node that does not run. `record finished --result success` adds the id to `DISPATCHED` once,
   in execution order, so `DISPATCHED` lists only skills that ran successfully, directly if installed
   or fetched-and-run otherwise. A failed
   fetch or execution belongs under `DEAD_ENDS` with its actual error; distinguish "not run" from
   "ran and failed", and stop that dependency chain. `DISPATCHED` records successful executions,
   starting with the account preflight. If choices remain, the plan is empty, or the user declines,
   run no further skills; keep the successful preflight entry without inventing additional dispatches.
   After `record declined`, go to Step 8: `record run-finished` closes every unrun node as declined.
   A node removed under the scope rule (see the PLAN block) is not run: record it under `DEAD_ENDS`
   as `- <skill_id> — out of scope: <the caveat it falls outside>`, keep it out of `DISPATCHED`, and
   close it with `record skipped <skill_id> --result out_of_scope` at the confirm gate, before you
   start any later node (a later node cannot start while an earlier node is open).
8. **Summarize — render the SUMMARY block.** As the terminal output, render the **SUMMARY block** (see
   *Output templates* below) verbatim, in the exact section order. The skipped / gaps list is a real
   output — the coverage-gap / demand signal for what to automate next; state it, do not hide it. Run
   `emit.py record run-finished` once (**Run records**) — except while a choice question from Step 6
   is waiting for the developer's answer: the run is paused, not finished, so do not run it then;
   finish the run after the replan.

## Output templates

Render two fixed blocks so every run reads the same: the **PLAN block** at Step 7 (the confirm gate)
and the **SUMMARY block** at Step 8 (terminal output). Fill the slots and add no extra prose.

**Rendering rules (both blocks).** Use the given section order and the exact headers. Prefer tables to
prose; one line per row; do not editorialize or restate the goal. Every dispatched step shows its
source (the skill's public source URL — newest; `self` for this repo). Action items are imperative and
carry the exact command or file path. Always end with the telemetry `session_id` so the output and the
events join. Omit a section only by its stated omission rule. Marker legend: `✓` done/verified · `◑`
partial or wired-not-verified · `⚠` needs action / mutating · `✗` failed/blocked · `⊘`
skipped/not-covered.

### PLAN block — Step 7 (before any dispatch)

```
# Datadog Onboarding — Plan · session {{session_id}}

## Detected context
- Platform: {{platform}}  ·  Cloud: {{cloud|none}}  ·  Stack: {{stack_summary}}
- Existing Datadog: {{existing|none}}

## Recommended products
{{i}}. {{product}} · {{priority}} · {{one-line why, names a file/lib}}

## Plan — {{k}} step(s), in dispatch order
| # | Skill | Kind | Product | Source |
|---|-------|------|---------|--------|
| {{n}} | {{skill_id}} | {{kind}} | {{product}} | {{source url (newest) or self}} |
Dependencies: {{root}} → {{chain / branches, one line}}

## Not automated ({{dead_end_count}})
- {{product}} — {{why}} → {{docs URL}}
> Show "None — every recommended product is covered." when dead_end_count = 0.

## Decisions needed ({{choice_count}})
- {{choice}}: {{optionA}} / {{optionB}} / {{optionC}}
> Show "None." when choice_count = 0.

## Scope limits ({{caveat_count}})
- {{skill_id}}: {{caveat}}
> Omit this section when the trace has no `CAVEATS:` block.

## Before you approve — effects
- ⚠ {{step}} {{mutating / outward-facing effect}}
- {{step}} {{non-mutating effect}}

Approve?  [Proceed — all {{k}}]  ·  [Cancel]
```

When the trace has a `CAVEATS:` block, check each caveat against what the developer asked for and
the detected context before the confirm gate. If their target is outside a skill's caveat (for
example a MySQL or Aurora database for an RDS PostgreSQL skill, or a serverless service for the
profiler), do not dispatch that skill or any prerequisite that only it needs; list the product
under "Not automated" instead, drop those nodes from the Plan table, and record them in `$TRACE` as
Step 7 describes.

### SUMMARY block — Step 8 (terminal output)

```
# Datadog Onboarding — Summary · session {{session_id}} · {{result}}

## Checklist
- [{{x|.}}] #{{n}} {{skill_id}} — {{one-line outcome}}

## Products set up
| Product | Delivered by | Status | Evidence |
|---------|--------------|--------|----------|
| {{product}} | {{mechanism, source}} | {{✓|◑|✗}} | {{proof or "pending {{blocker}}"}} |

## Changed
- Cluster: {{namespaces/resources}}
- App: {{files/manifests}}
- Creds: {{where, gitignored?}}

## Action items — do next
1. [ ] {{imperative}} — `{{exact command / path}}`
> Show "None — setup is complete." when there are no follow-ups.

## Issues & deviations
| What | Cause | Resolution / impact |
|------|-------|---------------------|
| {{issue}} | {{cause}} | {{how resolved / residual impact}} |
> Show "None." when the run was clean.

## Gaps / demand signals
- {{skipped product or catalog/orchestrator gap}}

## Verify in Datadog
- {{product}}: {{deep link}}

## Telemetry
session {{session_id}} · {{event_count}} events · result {{result}} ({{s}}✓ / {{f}}✗ / {{k}}⊘)
```

> **Run verdict** — the overall `{{result}}`: use `success` when every **planned** skill succeeded,
> even if some recommended products are **dead-ends / "Not automated"** (no skill yet) — those are
> coverage gaps, not partial failures. Use `partial_success` when a planned fetch or execution
> **failed**, or a dependent step was **skipped**; do not infer success from `DISPATCHED` alone.
> Use `blocked` when nothing beyond the account preflight can run because every product dead-ended;
> `cancelled` when the user declined the plan. Record failures and skips with `emit.py record` even
> though those skills are absent from `DISPATCHED`; `emit.py` reconciles the verdict from those counts.

## Run records (`emit.py record`) and telemetry

Every dispatch boundary is **one** `emit.py record` call. It updates the trace file (`$TRACE`) and
sends the matching telemetry event in the same step, so you never edit `CONFIRMED` or `DISPATCHED`
by hand and never call the emitter separately. `record` takes the plan, the session id, and the
step fields from the state that `resolve.py` saved, so a fresh shell needs no `$SID`. It also
computes `duration_ms` and the final step counts itself.

```
python3 dd-orchestrator/scripts/emit.py record confirmed          # user approved the plan -> CONFIRMED: yes
python3 dd-orchestrator/scripts/emit.py record declined           # user declined -> CONFIRMED: no
python3 dd-orchestrator/scripts/emit.py record started  <skill_id> --source-mode <installed|fetched>
python3 dd-orchestrator/scripts/emit.py record finished <skill_id> --result <success|failed>   # success -> DISPATCHED
python3 dd-orchestrator/scripts/emit.py record skipped  <skill_id> [--result skipped_dependency|declined|source_unreachable|out_of_scope]
#   default: skipped_dependency (a prerequisite failed) or declined; use source_unreachable when the fetch
#   failed and out_of_scope for a node removed under the CAVEATS scope rule
python3 dd-orchestrator/scripts/emit.py record run-finished       # once, at the end
```

`record run-finished` derives `result` from the recorded steps: `cancelled` after `record declined`
(it also closes the unrun nodes as declined), and `blocked` when nothing beyond account preflight ran
because every product dead-ended. Pass an
explicit terminal result only when that derivation would be wrong. A run cannot continue after
`record run-finished`, so never run it while a choice question is waiting for the developer.

Valid commands exit 0 even when sending fails; malformed commands, unknown skill ids, trace/session
mismatches, and duplicate or out-of-order transitions exit 2 without changing the trace, and print
the reason on stderr; correct the call from that reason instead of retrying it unchanged. Sending is
best-effort (bounded timeout, local debug log, never throws), goes to the logs-intake route only, and
is turned off with `DD_ORCH_TELEMETRY_DISABLED=1`; valid trace updates still happen. **Never build
your own HTTP request or `curl`.** Automated runs set `DD_ORCH_RUN_CONTEXT` (`eval`, `ci` or `dev`)
so they are kept apart from real usage; without it, a run is `ci` when `CI` is set and `user` otherwise.

`resolve.py` emits the plan core on each resolve: one `skill_run:started` per session, then
`skill_run:plan_resolved` and one `skill_step:planned` per plan node and per dead-end. Each resolve
increments `plan_revision`; all planned events for that revision form one complete snapshot (each
`skill_step` also carries `depends_on`, the CSV of prerequisite plan positions, so the DAG edges are
reconstructable). It also saves the run envelope (agent, run context, platform, cloud, entry, intent
mode, org id), and `emit.py` re-attaches it and an `emitted_at` (ms) timestamp to **every** event. The
agent is detected from its environment. Org lookup uses the validated API/app-key pair from the
environment or parsed `.env.local` / `.env` and the run-owned copy of the OAuth token. If both
identify different organizations, it omits `org_id` instead of guessing. The emitter refuses unknown
sites before sending credentials. `record run-finished` releases this run's token claim and removes
the shared handoff token only after the final concurrent claim ends.

Field values are bounded enums / ids / counts only — never send goal text, paths, keys, URLs, or
model output (the emitter also strips anything not on its allow-list).

**Reliability and reconciliation.** Every event carries a per-session `event_seq` (a monotonic
ordinal): a gap in `event_seq` means an event was dropped, not that the step never ran. `resolve.py`
emits its plan-shape core (`skill_run:started`, `skill_run:plan_resolved`, one `skill_step:planned`
per node) as **critical** — one transport blip cannot drop the whole core. `emit.py` also appends
every attempted event to a durable local NDJSON log for offline audit. When you analyze a run, treat
`step_success_count` / `step_failed_count` / `step_skipped_count` on `skill_run:finished` as the
**source of truth** for how many steps ran; reconcile the per-step events against it. Do not assume a
missing per-step event means the step did not run. `emit.py` also reconciles the terminal
`skill_run:finished` `result` against those counts (and the dead-end count): if the reported verdict
contradicts them, it keeps the reported value as `result_reported` and sets `result` to the
count-consistent verdict (`result_reconciled: true`). So report the honest per-step results and let the
guard settle the run verdict.

## Worked example

Goal *"monitor my Node service on Kubernetes"* → recommender `[APM, Infrastructure Monitoring]`,
detected `platform=kubernetes`:

```
1. dd-account-setup            (foundation)          [self]
2. apm-agent-install-kubernetes (platform-install)   [agent-skills]
3. apm-enable-kubernetes       (product-enable/apm)  [agent-skills]
4. apm-verify-ssi-kubernetes   (verify)              [agent-skills]
```

One product plus a detected platform became a four-skill plan drawn from two repos, correctly
ordered, with Infrastructure Monitoring delivered by the same SSI Agent install. The intent never entered
the resolver — only the products and the detected platform did.
