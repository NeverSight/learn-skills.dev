---
name: agent-observability-trace-rca
description: Root cause analysis on production LLM traces. Diagnoses why an LLM application is failing — works from eval judge verdicts, runtime errors, or structural anomalies depending on what signals are present. Walks the span tree from symptom to root cause. Use when user says "what's wrong with my app", "why is my eval failing", "analyze errors", "root cause analysis", "diagnose failures", or wants to understand production failure patterns.
---

## Backend

**Detection** — At the start of every invocation, before taking any action, determine which backend to use:

1. If the user passed `--backend pup` anywhere in their invocation → use **pup mode** immediately, regardless of whether MCP tools are present. Skip steps 2–4.
2. Check whether MCP tools are present in your active tool list. The canonical signal is whether `mcp__datadog-llmo-mcp__list_llmobs_evals` appears in your available tools.
3. If MCP tools are present → use **MCP mode** throughout. Call MCP tools exactly as named in this skill's workflow sections.
4. If MCP tools are absent → check whether `pup` is executable: run `pup --version` via Bash. A JSON response containing `"version"` confirms pup is available.
5. If pup responds → use **pup mode** throughout. Translate every MCP tool call to its pup equivalent using the Tool Reference appendix at the bottom of this file.
6. If neither is available → stop and tell the user:
   > "Neither the Datadog MCP server nor the pup CLI is available. Connect the MCP server (`claude mcp add --scope user --transport http datadog-llmo-mcp 'https://mcp.datadoghq.com/api/unstable/mcp-server/mcp?toolsets=llmobs'`) or install pup."

`--backend pup` is accepted anywhere in the invocation arguments and is stripped before passing remaining args to the skill logic.

**pup invocation rules:**
- Invoke via Bash: `pup llm-obs <subcommand> [flags]`
- pup always outputs JSON. Parse directly — no content-block unwrapping (unlike MCP results, which may wrap JSON in `[{"type": "text", "text": "<json>"}]`).
- If pup returns an auth error, tell the user to run `pup auth login` and stop.
- Parallelization: issue multiple Bash tool calls in a single message (one pup command per call).
- Time flags: pup accepts bare duration strings (`1h`, `7d`, `30m`) and RFC3339 timestamps. Do **not** use `now-`-prefixed strings — strip the prefix when converting from a skill `--timeframe` argument: `now-7d` → `7d`, `now-24h` → `24h`, `now-30d` → `30d`.
- `--summary` on `pup llm-obs spans search` strips payload fields to essential metadata only. Use it in bulk/search phases where content is not needed.

**Invocation ID:** At the very start of each invocation, before any MCP tool call, generate an 8-character hex invocation ID (e.g., `3a9f1c2b`). Keep it constant for the entire invocation.

**Intent tagging:** On every MCP tool call, prefix `telemetry.intent` with `skill:agent-observability-trace-rca[<inv_id>] — ` followed by a description of why the tool is being called. On the **first MCP tool call only**, use `skill:agent-observability-trace-rca:start[<inv_id>] — ` instead (note the `:start` suffix). Example first call: `skill:agent-observability-trace-rca:start[3a9f1c2b] — Phase 0: discover configured evals for task-cruncher to infer analysis mode`

# Agent Observability Trace RCA — Root Cause Analysis from Production LLM Traces

Diagnose **why an LLM application is failing** by searching production traces and walking the span tree from symptom to root cause. The skill automatically selects the best analysis mode based on available signals:

| Mode | Signal | When auto-selected |
|------|--------|--------------------|
| **Eval Signal** | LLM judge verdicts and reasoning (pass/fail rates, scoring) | Evaluators are configured for the app |
| **Error Signal** | Runtime errors (`@status:error`, error types, stack traces) | No evals configured, or user explicitly asks about errors/crashes |
| **Generic** | Structural anomalies (latency, agent loops, retrieval misses) | Explicit `mode=generic` override, or no strong signal found in Phase 1 |

The mode is **announced (never asked)** in the first user-facing output with a one-line override hint.

## Methodology

**Resolve → Search → Observe → Open Coding → Axial Coding → Root Cause Navigation → Recommendations**

## Usage

```
What's wrong with <ml_app> over the last <timeframe>
Why is <ml_app> failing today
Analyze eval failures for <eval_name> on <ml_app>
Look at the errors on <ml_app> over the last <timeframe>
Root-cause low scores on <eval_name>
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `ml_app` | Yes (or `eval_name`) | — | The application to analyze. |
| `eval_name` | No | — | One or more evaluators to focus on. Implies Eval Signal mode. Pass a list for multi-eval analysis. |
| `timeframe` | No | `now-24h` | How far back to look. |
| `mode` | No | inferred | Explicit mode override: `eval`, `errors`, `generic`. Skips inference entirely. |
| `failure_filter` | No | — | Narrowing scope: `"errors"` (routes to Error Signal path), `"high latency"` (post-fetch duration sort), `"low scores on <eval>"` (promotes to `eval_name`), a tool name or span name (`@name:<x>` query). |

If neither `ml_app` nor `eval_name` is provided, ask the user.

## Available Tools

### Eval discovery & overview

| Tool | Purpose |
|------|---------|
| `list_llmobs_evals` | Discover all configured evals for an `ml_app`. Used in Phase 0 mode inference. |
| `get_llmobs_eval_aggregate_stats` | Pass/fail rate or score distribution for an eval over a time window. |
| `get_llmobs_evaluator` | Full evaluator config: prompt template, assessment criteria, span filter, sampling, provider. Use instead of the deprecated `get_llmobs_eval_config`. |

### Trace & span exploration

| Tool | Purpose |
|------|---------|
| `search_llmobs_spans` | Find spans by tags, span kind, status, query syntax. Paginate with cursor. Entry point for Phase 1. |
| `get_llmobs_span_details` | Metadata, evaluations (scores, labels, reasoning), `status`, error fields, duration, and **`content_info`** map showing available fields + sizes. |
| `get_llmobs_span_content` | Actual content for a span field. Supports JSONPath via `path` param for targeted extraction. |
| `get_llmobs_trace` | Full trace hierarchy as span tree with span counts by kind. |
| `find_llmobs_error_spans` | All error spans in a trace with error type, message, stack, and propagation context. |
| `expand_llmobs_spans` | Load children of collapsed trace nodes. |
| `get_llmobs_agent_loop` | Chronological agent execution timeline (LLM calls, tool invocations, decisions). May return empty — see Phase 4b fallback. |

### Key `get_llmobs_span_content` patterns

| Field | Path | What you get |
|-------|------|-------------|
| `messages` | `$.messages[0]` | System prompt (first message, usually `system` role) |
| `messages` | `$.messages[-1]` | Last assistant response |
| `messages` | *(no path)* | Full conversation including tool calls |
| `input` / `output` | — | Span I/O |
| `documents` | — | Retrieved documents (RAG apps) |
| `metadata` | — | Custom metadata (prompt versions, feature flags, user segments) |

### How to use `search_llmobs_spans`

**Always include `@ml_app:"<ml_app>"` in the `query` string — the structured `ml_app` parameter is unreliable and can return spans from other apps.** Do not rely on the structured parameter alone.

Useful query fragments — combine with space (AND):

| Goal | Query |
|------|-------|
| Errors only | `@status:error` |
| Eval is present on the span | `@evaluations.custom.<eval_name>:*` (presence only — pass/fail is read from `get_llmobs_span_details`, not the query) |
| A specific tool by name | `@name:<tool_name>` |

Dedicated params (`span_kind`, `root_spans_only`, `ml_app`) work alongside `query`, but `query` takes precedence over `tags`.

### Parallelization rules

1. **`get_llmobs_span_details`**: Group span_ids by trace_id, chunk each trace's span_ids into batches of at most 20. Issue ALL chunks for a page in a **single message**.
2. **`get_llmobs_span_content`**: Each call is independent — always issue ALL in a single message.
3. **`get_llmobs_trace` / `find_llmobs_error_spans` / `get_llmobs_agent_loop`**: Parallelize across different traces in a single message.
4. **Pipeline parallelism**: Start `get_llmobs_span_details` for page 1 results immediately — don't wait to collect all pages.

---

## Analysis Workflow

**Output discipline**: Phases 0–5 are internal analysis. The only user-facing outputs during these phases are the Phase 1 Signal Summary and the mandatory checkpoints at Phases 2 and 3. Do NOT narrate reasoning, summarize intermediate findings, or output Phase 4 deep-dive results as prose. All detailed findings go exclusively into the Phase 6 report.

---

### Phase 0: Resolve Inputs & Infer Mode

**First: check for classification context.** Scan the conversation for a `# Session Classification Summary` header. If found → enter **Step 0S** below and skip all remaining Phase 0 steps and Phase 1 entirely.

#### Step 0S — Extract Failure Bucket from Classification Output

The canonical handoff format is the **Per-Unit Details table** inside the `# Session Classification Summary` section. Extract one row per unit:

| Field | Source |
|-------|--------|
| `trace_id` | Link URL in the ID column: parse the `trace_id=` or `session_id=` query parameter from the link href |
| `verdict` | Verdict column |
| `failure_mode` | Failure Mode column (`none` for passing rows) |
| `detail` | Reason column — use as the Phase 2 reasoning input (same role as eval judge reasoning or error messages) |
| `app_type` | From the `# Session Classification Summary` header line (e.g. `Root span kind: agent`) — default `LLM` if absent |

**Failure bucket** = all rows where verdict is `no` or `partial`.

- < 5 entries → note low confidence, proceed anyway.
- Empty → report "No failures found in the classification output" and stop.

Present this overview before proceeding:

```
## Classification Overview (from agent-observability-session-classify)

**ml_app**: <from summary header>  |  **Classified**: N  |  **Failures (no+partial)**: F  |  **Pass rate**: X%

| Failure Mode | Count |
|---|---|
...

Proceeding to Phase 2 using F failure traces. Mode inference bypassed — classification verdict is the signal.
```

Then **skip Phase 1 and jump directly to Phase 2**. Carry forward:
- Phase 2 reasoning input: `(trace_id, span_id, detail)` tuples — same structure as eval reasoning or error messages
- Phase 4 navigation: use `app_type` from each trace block to choose the span navigation strategy
- Phases 2–7: run completely unchanged — the failure bucket structure is identical regardless of source

---

**Standard resolution (no classification context):**

1. If neither `ml_app` nor `eval_name` provided → ask the user. If `eval_name` is provided but `ml_app` is not → also ask for `ml_app` (eval names are not globally unique; without it, span searches return results from all apps sharing the eval name).
2. If `timeframe` not provided → default to `now-24h`.
3. **Resolve `failure_filter`** (before mode inference):
   - `"errors"` → force **Error Signal** mode
   - `"low scores on <eval>"` → treat as `eval_name=<eval>`, then continue inference
   - `"high latency"` → note for Phase 1 (sort by duration post-fetch); continue inference
   - Tool/span name → note as `@name:<x>` query fragment for Phase 1; continue inference
4. **Resolve mode** (skip if `mode` was explicitly provided):
   - `eval_name` given → **Eval Signal**
   - User explicitly mentioned errors/exceptions/crashes → **Error Signal**
   - Otherwise → call `list_llmobs_evals_by_ml_app(ml_app)`:
     - Evals returned → **Eval Signal**
     - No evals → **Error Signal** (announce auto-selection in Phase 1)
5. When `eval_name` is multi-valued, note for Phase 1: run parallel per-eval searches and merge+dedup by `(trace_id, span_id)`.

---

### Phase 1: Find Problematic Spans

Three mode-specific paths. All end with a **Signal Summary** that labels the mode and includes a one-line override hint.

**Mode switch handling**: At any checkpoint, if the user says "switch to [error|eval|generic] mode", re-enter Phase 1 with the new mode. Phase 0 inputs do not re-resolve.

**Auto-pivot**: If the selected mode finds no data (0 evals configured, 0 error spans in timeframe), announce the pivot to Generic and proceed — do not stop and ask.

---

#### Eval Signal path

##### Step 1a: Eval overview (parallel)

For each eval, call both in a single parallel batch:
- `get_llmobs_eval_aggregate_stats(eval_name, from, to)`
- `get_llmobs_evaluator(eval_name)`

**Interpret aggregate stats:**
- **`total_count == 0`** → Note "no data." Skip this eval (or pivot to Generic if it's the only one).
- **Boolean `pass_rate == 1.0`** → Note "100% pass." Skip unless it's the only eval.
- **Boolean with failures** → Note counts and pass_rate. Continue.
- **Score with assessment criteria** → Note distribution and pass/fail counts. Continue.
- **Score WITHOUT assessment criteria** → Infer failures: bottom quartile, or below median if bimodal. Label as "inferred failures" in report.
- **Categorical with assessment criteria** → Note top_values and pass/fail. Continue.
- **Categorical WITHOUT assessment criteria** → Infer from context (e.g., "error", "incomplete", "off_topic" are likely failures). Ask user if genuinely ambiguous.

**Interpret eval config:**
- **Config returned** (custom) → Store `prompt_template`, `assessment_criteria`, `parsing_type`, `output_schema`.
- **Config nil** (OOTB) → Note prompt is not inspectable.

**Calibration cross-check**: When two evals share a name prefix but differ in type (e.g. `foo-boolean` and `foo-score`), compare their pass rates on overlapping spans. A discrepancy >20% is an **Evaluator Calibration Discrepancy** — flag it in the report.

##### Step 1b: Collect failure spans

For each eval:
1. `search_llmobs_spans(query="@evaluations.custom.<eval_name>:*", from, limit=50)`. When multi-valued, issue one search per eval in parallel — merge result sets, dedup by `(trace_id, span_id)`.
2. Paginate until ≥15–20 failures OR no more pages. Cap at 200 spans total.
3. `get_llmobs_span_details` per trace_id batch (follow Parallelization Rules).
4. Extract per row: **assessment**, **value**, **reasoning**, **span_id**, **trace_id**, **span_kind**, **content_info**.
5. Separate into pass/fail buckets using thresholds from Step 1a.

**JSON-type eval fallback**: If `@evaluations.custom.<eval_name>:*` returns 0 spans but `get_llmobs_eval_aggregate_stats` confirmed `total_count > 0`, the eval is JSON-type and scores are not indexed on this field. Fall back to: search by the span name or span kind that the eval targets (check `get_llmobs_evaluator` for the span filter), then inspect output payloads for JSON verdict fields via `get_llmobs_span_content(field="output")`.

##### Step 1c: Signal Summary (Eval Signal)

```
## Signal Summary: `{ml_app}` · Eval Signal
(Inferred from {N} configured eval(s). Say `switch to error mode` or `switch to generic mode` to change.)

**Timeframe**: {from} → {to}

| Eval | Type | Total | Pass Rate | Status |
|------|------|------:|:---------:|--------|
| eval_1 | boolean | 4,891 | 37.3% | ⚠ Investigating |
| eval_2 | score | 1,200 | — (inferred threshold) | ⚠ Investigating |
| eval_3 | boolean | 500 | 99.2% | ✓ Healthy |

**Collected**: {pass_count} passing, {fail_count} failing.
```

For a single eval, collapse to a single-line header instead of a table.

---

#### Error Signal path

##### Step 1a: Sample error spans

`search_llmobs_spans(query="@ml_app:\"<ml_app>\" @status:error", from=timeframe, limit=50)`. Paginate until ≥30 error spans or no more pages.

##### Step 1a.5: Soft error scan

MCP tool spans sometimes report `@status:ok` but carry `"isError": true` in their output payload — these are invisible to `@status:error` queries and can outnumber hard errors.

Call `search_llmobs_spans(query="@ml_app:\"<ml_app>\" @status:ok", span_kind="tool", from=timeframe, limit=20)`. For a sample of 5–10 results, call `get_llmobs_span_content(field="output")` in parallel. If any payloads contain `"isError": true`, add **MCP soft errors** as a separate row in the error frequency table with the note: *(status:ok but isError:true in payload — not queryable via @status:error)*.

##### Step 1b: Group by error type

Group spans by `error_type` tag → frequency table. If `error_type` tag is absent on some spans, supplement with the `error.type` field from `get_llmobs_span_details` (fetched in Step 1d).

##### Step 1c: Fetch stack traces (parallel)

For the top 3–4 error types by count, pick 2–3 representative trace IDs each. Call `find_llmobs_error_spans(trace_id)` in parallel across all selected traces. Extract:
- Error message and stack trace
- Origin span kind and name
- Whether errors propagate from children to parents (cascade) or are isolated

##### Step 1d: Fetch span details

`get_llmobs_span_details` on representative spans for each error type (follow Parallelization Rules). Extract `content_info`, `span_kind`, duration.

##### Step 1e: Signal Summary (Error Signal)

```
## Signal Summary: `{ml_app}` · Error Signal
(No evals configured — analyzing runtime errors. Say `switch to eval mode` or `switch to generic mode` to change.)

**Timeframe**: {from} → {to}  |  **Total error spans sampled**: {N}

| Error Type | Spans | Cascade? | Origin Span Kind |
|------------|------:|:--------:|-----------------|
| TimeoutError | 42 | Yes | tool |
| APIError 429 | 18 | No | tool |
| ValueError | 7 | No | llm |
| MCP soft errors (isError:true) | 23 | No | tool |
```

---

#### Generic path

##### Step 1a: Eval health check (when evals are configured)

If `list_llmobs_evals` returned evals in Phase 0, call `get_llmobs_eval_aggregate_stats` for each enabled eval in parallel. Flag any enabled eval with `total_count: 0` as **Broken Eval Configuration** — include in the Signal Summary anomaly table as a High severity row.

##### Step 1b: Broad span search

`search_llmobs_spans(query="@ml_app:\"<ml_app>\"", root_spans_only=true, from=timeframe, limit=50)`. Apply `failure_filter` narrowing if present (tool/span name → `@name:<x>` query; `"high latency"` → sort result set by `duration` after Step 1c). Paginate until ≥30 spans.

##### Step 1c: Fetch span details

`get_llmobs_span_details` per trace_id batch.

##### Step 1d: Rank by structural anomalies

Partition spans using heuristics:
- Top decile by `duration` (latency outliers)
- Agent spans with >N tool/LLM iterations (long-running loops)
- Retrieval spans returning 0 documents (RAG miss)
- Workflow spans whose child set is missing an expected step (compare against median child layout)
- **Token efficiency**: Check if `non_cached_input_tokens ≈ input_tokens` across LLM spans. If the app has stable system prompts (>1k tokens) and cache hit rate is 0%, flag as High severity — enabling `cache_control: ephemeral` on the system prompt would cut input token costs by 60–90%

##### Step 1e: Signal Summary (Generic)

```
## Signal Summary: `{ml_app}` · Generic
(Analyzing structural anomalies. Say `switch to eval mode` or `switch to error mode` to change.)

**Timeframe**: {from} → {to}  |  **Sampled**: {N} root spans

| Anomaly Type | Count |
|---|:---:|
| Latency outliers (>p90) | 12 |
| Long agent loops (>8 iterations) | 5 |
| RAG retrieval misses | 3 |
| Zero prompt cache utilization | All LLM spans |
| Broken eval configurations | 2 |
```

---

### Phase 1.5: Determine App Profile & Where the Root Cause Lives

Inspect `content_info` and `span_kind` across collected spans. Drives Phase 4 strategy.

**App profile** (from content_info):

| Signal | App profile | Phase 4 strategy |
|--------|------------|-----------------|
| `content_info` has `messages` | LLM/chat app | Extract system prompt via `messages[0]`, check conversation flow |
| `content_info` has `documents` | RAG app | Check retrieval quality alongside LLM output |
| Trace contains `agent` span kind | Agent app | Try `get_llmobs_agent_loop` first; if it returns empty use child-span reconstruction (see Phase 4b) |
| `messages.count > 10` | Long conversation | Check for context overflow |
| `content_info` has `metadata` | Has custom metadata | Check for clustering by metadata values (prompt version, feature flags) |

> **LLM Experiments traces**: If root spans have `span_kind: experiment` and carry `input`, `output`, and `expected_output` structured fields, you are looking at a [Datadog LLM Experiments](https://docs.datadoghq.com/llm_observability/experiments/) trace. Each span represents one dataset record run. Read quality signal from the root span's `input`/`output`/`expected_output` fields via `get_llmobs_span_content` — not from LLM sub-span messages, which may contain stub or placeholder content. Evaluations attached to experiment spans are computed by the Experiments framework at run time and may not be registered as online Datadog evaluators (`get_llmobs_evaluator` will return 404 for them).

**Where the root cause likely lives** — by symptom span kind:

| Symptom span kind | Symptom looks like | But root cause is often in... |
|-------------------|-------------------|------------------------------|
| `llm` | Bad LLM response (eval flagged, wrong output) | **Parent** agent (bad instructions), **sibling** retrieval (bad context), **sibling** tool (bad data) |
| `agent` | Bad orchestration | **Child** spans (wrong tool calls, bad routing), full agent loop |
| `tool` | Bad tool result | **Parent** LLM (passed wrong parameters), tool implementation |
| `workflow` | Bad overall output | **Child** sub-spans (which step first deviated?) |
| `retrieval` | Bad retrieval | Query construction (parent), index/embedding config (outside trace) |

**Key insight**: The signal — eval verdict, error message, latency outlier — flags one span in isolation. It's a *symptom report*, not a diagnosis. The root cause often lives in a different span: a parent that gave bad instructions, a sibling that provided bad context, or a child that made a wrong decision. Phase 4 navigates the tree to find it.

---

### Phase 2: Open Coding — Initial Failure Categorization

**Goal**: Read per-row evidence and propose initial, concrete failure categories. Pool all problematic rows together — categories should describe app behaviors, not which signal flagged them.

**Per-row "reasoning input"** by mode:
- **Eval Signal**: judge assessment + reasoning from `get_llmobs_span_details`
- **Error Signal**: error message + stack trace excerpt from `find_llmobs_error_spans`
- **Generic**: one-line description of the structural anomaly that flagged the row

**Shortcuts**:
- **< 15 problematic rows**: Combine Phases 2 and 3 into one pass. Still produce the checkpoint.
- **> 80% share the same reasoning/error/symptom**: Skip to Phase 4 with the dominant pattern. Still output checkpoint.
- **> 50 problematic rows**: Sample ~50, build taxonomy, then spot-check 10–15 more.

1. **Use per-row signal from Phase 1** — do NOT re-fetch. Only call `get_llmobs_span_content(field="input"/"output")` for spans where the reasoning is insufficient (generic, empty, or just a stack trace with no app context).

2. **If eval config is loaded** (Eval Signal), distinguish early:
   - **App failures**: Output genuinely violates the eval's criteria
   - **Eval failures**: Output seems reasonable but eval criteria are too strict/ambiguous

3. **Each pattern must be specific**: "Agent called search instead of calculator for price computation" — NOT "tool issue."

#### MANDATORY CHECKPOINT

```
**Open coding**: {N} problematic rows → {K} initial categories: {Category1} ({count}), {Category2} ({count}), ...
```

---

### Phase 3: Axial Coding — Refine Failure Taxonomy

**Goal**: 3–8 final categories, ranked by impact.

1. **Merge**: Categories with < 3 occurrences → parent category or drop as noise.
2. **Split**: Categories with > 30% of failures → more specific sub-categories. Pull additional span content if needed.
3. **Validate**: 2–3 representative examples per category confirm the label fits.
4. **Rank**: `priority = count × severity` (severity: high / medium / low).

#### MANDATORY CHECKPOINT

```
**Axial coding**: {merges/splits/drops}. Final categories:
1. {Category} ({count}, {pct}%) — {severity}
2. ...
```

---

### Phase 4: Root Cause Analysis — Navigate from Symptom to Root Cause

**Goal**: The signal flagged a span. That's the symptom. Navigate the trace tree to find the actual root cause — it's often in a different span.

For each of the top 3 categories, pick 2–3 representative traces:

#### Step 4a: Trace structure + errors (parallel)

For each representative trace, call in a single message:
- `get_llmobs_trace(trace_id)` — span hierarchy; locate the symptom span and its parent/siblings/children
- `find_llmobs_error_spans(trace_id)` — check for runtime errors anywhere in the trace

**Runtime vs behavioral**: If errors exist on or near the symptom span, the root cause may be a runtime failure rather than a behavioral one. Check this first.

**Distributed trace fallback**: If `get_llmobs_trace` returns "cannot find parent" or an empty span list (common in Ray-based or multi-process execution), reconstruct the trace manually using `get_llmobs_span_details` on the span_ids collected in Phase 1, sorted by `start_ms`.

#### Step 4b: Navigate to the root cause (parallel)

Use the symptom span kind (from Phase 1.5). Issue ALL calls in a single message.

**If symptom is on an `llm` span** (most common):
- `get_llmobs_span_content(field="messages", path="$.messages[0]")` on **symptom span** — system prompt
- `get_llmobs_span_content(field="messages")` on **symptom span** — full context received
- `get_llmobs_span_content(field="documents")` on **sibling retrieval spans** (if any)
- `get_llmobs_span_content(field="input")` on **sibling tool spans** (if any)
- `get_llmobs_span_content(field="messages", path="$.messages[0]")` on **parent agent/workflow span**

**If symptom is on an `agent` span**:
- `get_llmobs_agent_loop(trace_id, span_id)` — full decision timeline *(try first; if it returns 0 iterations, use the fallback below)*
- `get_llmobs_span_details` on **child spans** — sort by `start_ms` to reconstruct the execution timeline
- `get_llmobs_span_content(field="input"/"output")` on **child spans that look wrong**

**Agent loop fallback** (when `get_llmobs_agent_loop` returns 0 iterations): Reconstruct the timeline from `get_llmobs_span_details` results sorted by `start_ms`. Group by `span_kind` to identify LLM → tool → LLM sequences. This fallback is frequently needed — `get_llmobs_agent_loop` returns empty for many apps.

**If symptom is on a `tool` span**:
- `get_llmobs_span_content(field="input")` on **symptom span** — what parameters was it called with?
- `get_llmobs_span_content(field="messages")` on **parent LLM span** — did the LLM construct the call correctly?

**If symptom is on a `workflow` span**:
- `get_llmobs_span_details` on **all child spans** — find which step first deviated
- `get_llmobs_span_content(field="input"/"output")` on the **deviating child**

**Always also fetch**:
- `get_llmobs_span_content(field="metadata")` on the symptom span — clustering signals (prompt version, feature flags)

#### Step 4c: Diagnose — from symptom to root cause

For each category, trace the causal chain:

1. **Symptom** — what the signal flagged (eval reasoning, error message, anomaly note). The signal only saw one span in isolation — its reasoning may be shallow.
2. **Trace context** — what surrounding spans reveal (parent instructions, sibling data, child decisions).
3. **Root cause** — the specific span and decision point where the failure originated. Often NOT the symptom span itself.

**For suspected eval issues** (Eval Signal, if config loaded): Compare eval criteria against evidence. Is the prompt ambiguous? Criteria too strict?

**Root cause categories:**

| Category | Description |
|----------|-------------|
| **System Prompt Deficiency** | Instructions unclear, missing, or contradictory — in symptom span OR its parent |
| **Tool Gap** | Needed tool doesn't exist or parameters too coarse |
| **Tool Misuse** | Wrong tool called or wrong parameters — often visible in agent loop or parent LLM |
| **Routing/Handoff Error** | Wrong sub-agent selected (multi-agent systems) |
| **Retrieval Failure** | RAG returned irrelevant or missing context — check sibling retrieval spans |
| **Context Overflow** | Critical info lost due to context length |
| **Upstream Data Issue** | A sibling or parent span provided bad data that cascaded to the symptom span |
| **Runtime Error** | Tool/API failure, timeout, exception — from `find_llmobs_error_spans` |
| **Evaluator Miscalibration** | Eval criteria produce false positives/negatives (Eval Signal mode only) |

---

### Phase 5: Generate Recommendations

**Goal**: Concrete, actionable recommendations grounded in trace evidence. Actual text/code changes with before/after quotes from the trace — not generic advice.

Recommendation types: **System Prompt Edit** (quote actual prompt, provide before/after), **Tool Gap/Misuse** (reference agent loop steps), **Routing/Handoff Fix**, **Retrieval Fix** (show retrieved vs needed), **Evaluator Prompt Edit** (flag that eval changes need re-validation; Eval Signal only), **Other**.

**When run in Claude Code with codebase access**: Search the codebase for system prompt, tool definitions, or routing logic. Propose specific diffs. Always ask before modifying files.

---

### Phase 6: Compile RCA Report

Write the full report following the Output Format below. **This is the primary deliverable — output it directly in the chat.**

---

### Phase 7: Post-Analysis Actions

**Do NOT take any action automatically.** After presenting the report, ask the user what they'd like to do next:

1. Save the report to `agent-observability-rca-{ml_app}-{date}.md`
2. Apply fixes (if codebase is available)
3. Deeper investigation of remaining categories
4. Export to a Datadog notebook — in pup mode, use `pup notebooks create` to create the notebook and `pup notebooks edit NOTEBOOK_ID --file /tmp/nb_cells.json` to append sections (see Tool Reference)
5. Re-run on an expanded time range (e.g. `now-7d` if current window was `now-24h`)

**If the user chooses option 4**, follow the notebook creation fallback pattern:

1. Call `mcp__datadog-mcp-core__create_datadog_notebook` with:
   - **`name`**: `Agent Observability RCA: {ml_app} ({mode}) — YYYY-MM-DD`
   - **`type`**: `report`
   - **`time_span`**: `1w`
   - **`cells`**: one cell per section (see Notebook Cell Structure below)

2. **If the MCP call fails**, inspect the error before giving up:
   - **Auth / permission error (401, 403)** → stop and tell the user.
   - **Field validation error** (error message names a specific field) → fix that field and retry the MCP call once.
   - **Any other error** (binding, serialization, unexpected response) → fall back to pup:
     - Write the notebook payload to `/tmp/nb_rca_{ml_app}.json` as a full API envelope: `{"data": {"attributes": {"name": "...", "time": {...}, "cells": [...]}, "type": "notebooks"}}`
     - Run `pup notebooks create --file /tmp/nb_rca_{ml_app}.json`
     - If pup is not available either, render the full notebook content as markdown in chat so the user has it.

3. After successful creation by either method, output the URL on its own line:
   `RCA report exported to notebook: <url>`

Print the URL prominently — if `/eval-bootstrap` runs next in the same session, it will detect this URL and offer to append the evaluator suite to the same notebook.

#### Notebook Cell Structure

| Cell | Content |
|------|---------|
| 1 — Overview | Structured header (see Overview cell format below — follow it exactly) |
| 2 — Signal Summary | Mode-specific health table |
| 3 — Failure Taxonomy | Taxonomy table |
| 4…N — Failure Modes | One cell per failure mode |
| N+1 — Action Plan + Limitations | Action plan table + bullet list |

**Notebook formatting rules** (apply to every cell):
- **No triple-backtick code blocks** — use blockquotes (`>`) for prompts/rubrics, inline code (`` ` ``) for short values
- **Evidence as tables** — not bullet lists
- **Tool inputs as tables** — Argument | Wrong value passed | Correct approach
- **Action plan as a table** — Priority | Action | Confidence | Impact

---

## Output Format

---

### Overview cell (notebook Cell 1 / report header)

The Overview cell must follow this exact structure. No prose paragraphs. No inline-numbered findings. App description is one sentence maximum.

```
## `{ml_app}`  ·  {Eval Signal | Error Signal | Generic}  ·  {timeframe}
**Date**: {YYYY-MM-DD}  |  **Profile**: {short app profile}  |  **Model**: `{model(s)}`

{One sentence: what does this app do?}

| Metric | Value |
|--------|-------|
{mode-appropriate rows — see below}

### Findings

- **{Finding 1}** (~{pct}%): one-line root cause description
- **{Finding 2}** (~{pct}%): one-line root cause description
- **{Finding 3}** (if present): one-line root cause description

### Recommendations

- **{Recommendation 1}**: specific next step tied to Finding 1
- **{Recommendation 2}**: specific next step tied to Finding 2

*Sample: {N} spans analyzed. Confidence: High | Medium | Low — {one-line reason if Medium or Low}.*
```

**Mode-appropriate metric rows:**

Eval Signal:
```
| Eval | `{eval_name}` ({type}) |
| Spans evaluated | {total_count} |
| Pass rate | {pass_rate}% ({pass_count} pass / {fail_count} fail) |
| Top failure mode | {name} (~{pct}%) |
| Evals configured | {N} |
```

Error Signal:
```
| Error spans | {N} confirmed |
| Top error type | `{type}` ({pct}%) |
| Affected operation | `{span_name}` |
| Cascade pattern | Isolated / Cascading |
| Evals configured | {N} (none = no quality signal) |
```

Generic:
```
| Spans sampled | {N} root spans |
| Top anomaly | {type}: {count} spans |
| Error spans | {N} (0 = structurally healthy) |
| Evals configured | {N} (none = no quality signal) |
```

---

### Signal Summary Table

**When entering from Step 0S (classification context)**, replace the Signal Summary table with:

```
## Classification Signal Summary

**Source**: agent-observability-session-classify  |  **ml_app**: {app}  |  **Signal**: content-only | content+evals

| Metric | Value |
|--------|-------|
| Traces classified | N |
| Failures in corpus (no+partial) | F |
| Pass rate | X% |
| Failure modes | list |

*Root cause analysis is based on per-trace classification verdicts, not automated eval judge reasoning.*
```

**Otherwise**, mode-specific — pick the appropriate variant:

**Eval Signal** — one row per eval:

| Eval | Type | Total | Pass Rate | Status |
|------|------|------:|:---------:|--------|
| eval_1 | boolean | 4,891 | 37.3% | ⚠ Investigating |

**Error Signal** — one row per error type:

| Error Type | Spans | Cascade? | Origin Span Kind |
|------------|------:|:--------:|-----------------|
| TimeoutError | 42 | Yes | tool |

**Generic** — one row per anomaly type:

| Anomaly Type | Count |
|---|:---:|
| Latency outliers (>p90) | 12 |

---

### Failure Taxonomy

| # | Failure Mode | Traces | % | Severity | Root Cause |
|---|-------------|-------:|:-:|:--------:|-----------|
| 1 | ... | ... | ...% | **High** | Tool Misuse |

---

### Failure Mode Sections (one per top 3–5 modes)

```
## Failure Mode N: [Name]

**Count**: {n} spans, {t} traces  |  **Severity**: High/Medium/Low  |  **Root Cause**: [Category]

[3–5 sentences: what goes wrong, when, what triggers it, causal chain.]

**Evidence**

{Use the mode-appropriate column set:}

Eval Signal — Trace | Judge verdict | What the trace revealed:
| Trace | Judge verdict | What the trace revealed |
|---|---|---|
| [69de86a7...](https://app.datadoghq.com/llm/traces?query=trace_id:{full_id}) | fail | Parent agent has no date format instruction |

Error Signal — Trace | Behavior | Version:
| Trace | Behavior | Version |
|---|---|---|
| [69de86a7...](https://app.datadoghq.com/llm/traces?query=trace_id:{full_id}) | 7 parallel calls, all 400 | v107624932 |

Generic — Trace | Anomaly | Signal:
| Trace | Anomaly | Signal |
|---|---|---|
| [69de86a7...](https://app.datadoghq.com/llm/traces?query=trace_id:{full_id}) | 94s, 12 tool calls | Latency outlier |

{For tool misuse — add a tool inputs table:}
**Tool inputs (100% of sampled calls)**

| Argument | Value passed (wrong) | Correct approach |
|---|---|---|
| `query` | `"monitor_id:123 group_status:alert"` | `"monitor_id:123"` (name/tag only) |

{For Eval Signal — add judge reasoning as a blockquote:}
> "{quoted judge reasoning}"

**Root cause**: [WHY this happens — specific span, parameter, or prompt.]

**Fix**:
  BEFORE: [actual text from trace]
  AFTER:  [proposed replacement]

**Impact**: Eliminates ~{n} spans / {timeframe}.
```

---

### Prioritized Action Plan

| Priority | Action | Confidence | Impact |
|:---:|---|:---:|---|
| 1 | Fix `monitor_groups_search` schema — add `group_states` param | High | Eliminates ~21 spans/7d |

**When mode is Generic and no evals are configured**, always append as the final action plan row:

| N | Configure at least one evaluator | High | Enables Eval Signal mode for future RCAs — app currently has no ongoing quality signal |

---

### Limitations & Follow-ups

Bullet list of what needs more data or follow-up action.

---

## Operating Rules

- **Ground in evidence**: Every claim references span IDs with clickable trace links: `[Trace {first_8}...](https://app.datadoghq.com/llm/traces?query=trace_id:{full_32_char_id})`.
- **Root cause over symptom**: "System prompt doesn't specify date format" not "model gave wrong answer."
- **Show your math**: "47 failures (34%)" not "many failures."
- **Honest about uncertainty**: < 5 examples = tentative. Flag it.
- **Anonymize PII**: No emails or names. User/org IDs are fine.
- **MCP result parsing safety**: Before writing any script that iterates over MCP tool results, inspect the raw structure first — check top-level keys and whether the payload is nested inside a content block (e.g. `[{'type': 'text', 'text': '<json>'}]`). Extract and `json.loads()` the inner payload if needed. Never assume MCP results are bare dicts or lists.

---

## Tool Reference

This appendix applies only in **pup mode**. In MCP mode, use the tool names in the workflow sections directly.

### Spans and traces

| MCP Tool | pup Command |
|---|---|
| `search_llmobs_spans(query, ml_app, from, to, limit, cursor, root_spans_only, span_kind, summary)` | `pup llm-obs spans search --query "@ml_app:A [other_filters]" [--from F] [--to T] [--limit N] [--cursor C] [--root-spans-only] [--span-kind K] [--summary]` — **always use `--query "@ml_app:A"` to filter by ml_app**; the `--ml-app A` flag is unreliable and silently returns spans from other apps. |
| `get_llmobs_span_details(trace_id, span_ids, from, to)` | `pup llm-obs spans get-details --trace-id T --span-ids S1,S2,...` |
| `get_llmobs_span_content(trace_id, span_id, field, path)` | `pup llm-obs spans get-content --trace-id T --span-id S --field F [--path P]` |
| `get_llmobs_trace(trace_id, include_tree)` | `pup llm-obs spans get-trace --trace-id T [--include-tree]` |
| `get_llmobs_agent_loop(trace_id, span_id)` | `pup llm-obs spans get-agent-loop --trace-id T [--span-id S]` |
| `find_llmobs_error_spans(trace_id)` | `pup llm-obs spans find-errors --trace-id T` |
| `expand_llmobs_spans(trace_id, span_ids, max_depth, filter_kind)` | `pup llm-obs spans expand --trace-id T --span-ids S1,S2,... [--max-depth N] [--filter-kind K]` |

### Evaluators

| MCP Tool | pup Command |
|---|---|
| `list_llmobs_evals()` | `pup llm-obs evals list` (filter by `ml_app` client-side) |
| `list_llmobs_evals_by_ml_app(ml_app)` | `pup llm-obs evals list-by-ml-app --ml-app A` |
| `get_llmobs_evaluator(eval_name)` | `pup llm-obs evals get-evaluator EVAL_NAME` |
| `get_llmobs_eval_aggregate_stats(eval_name, ml_app, from, to)` | `pup llm-obs evals get-aggregate-stats EVAL_NAME [--ml-app A] [--from F] [--to T]` |

### Notebooks

| MCP Tool | pup Command |
|---|---|
| `create_datadog_notebook(name, cells, ...)` | `pup notebooks create --title "TITLE" --file /tmp/nb_cells.json` — confirm exact flags with `pup notebooks create --help` |
| `edit_datadog_notebook(id, cells, append_only=true)` | `pup notebooks edit NOTEBOOK_ID --file /tmp/nb_cells.json` (fetches current notebook, appends provided cells, writes back) |

The cells file is a JSON array of cell objects:
```json
[{"attributes": {"definition": {"type": "markdown", "text": "## Section\n\nContent."}}, "type": "notebook_cells"}]
```
