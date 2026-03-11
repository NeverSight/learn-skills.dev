---
name: massgen-log-analyzer
description: Run MassGen experiments and analyze logs using automation mode, logfire tracing, and SQL queries. Use this skill for performance analysis, debugging agent behavior, evaluating coordination patterns, and improving the logging structure, or whenever an ANALYSIS_REPORT.md is needed in a log directory.
---

# MassGen Log Analyzer

This skill provides a structured workflow for running MassGen experiments and analyzing the resulting traces and logs using Logfire.

## Purpose

The log-analyzer skill helps you:
- Run MassGen experiments with proper instrumentation
- Query and analyze traces hierarchically
- Debug agent behavior and coordination patterns
- Measure performance and identify bottlenecks
- Improve the logging structure itself
- **Generate markdown analysis reports** saved to the log directory

## CLI Quick Reference

The `massgen logs` CLI provides quick access to log analysis:

### List Logs with Analysis Status
```bash
uv run massgen logs list                    # Show all recent logs with analysis status
uv run massgen logs list --analyzed         # Only logs with ANALYSIS_REPORT.md
uv run massgen logs list --unanalyzed       # Only logs needing analysis
uv run massgen logs list --limit 20         # Show more logs
```

### Generate Analysis Prompt
```bash
# Run from within your coding CLI (e.g., Claude Code) so it sees output
uv run massgen logs analyze                 # Analyze latest turn of latest log
uv run massgen logs analyze --log-dir PATH  # Analyze specific log
uv run massgen logs analyze --turn 1        # Analyze specific turn
```

The prompt output tells your coding CLI to use this skill on the specified log directory.

### Multi-Agent Self-Analysis
```bash
uv run massgen logs analyze --mode self                 # Run 3-agent analysis team (prompts if report exists)
uv run massgen logs analyze --mode self --force         # Overwrite existing report without prompting
uv run massgen logs analyze --mode self --turn 2        # Analyze specific turn
uv run massgen logs analyze --mode self --config PATH   # Use custom config
```

Self-analysis mode runs MassGen with multiple agents to analyze logs from different perspectives (correctness, efficiency, behavior) and produces a combined ANALYSIS_REPORT.md.

### Multi-Turn Sessions

MassGen log directories support multiple turns (coordination sessions). Each turn has its own `turn_N/` directory with attempts inside:

```text
log_YYYYMMDD_HHMMSS/
├── turn_1/                    # First coordination session
│   ├── ANALYSIS_REPORT.md     # Report for turn 1
│   ├── attempt_1/             # First attempt
│   └── attempt_2/             # Retry if orchestration restarted
├── turn_2/                    # Second coordination session (if multi-turn)
│   ├── ANALYSIS_REPORT.md     # Report for turn 2
│   └── attempt_1/
```

When analyzing, the `--turn` flag specifies which turn to analyze. Without it, the latest turn is analyzed.

## When to Use Logfire vs Local Logs

**Use Local Log Files When:**
- Analyzing command patterns and repetition (commands are in `streaming_debug.log`)
- Checking detailed tool arguments and outputs (in `coordination_events.json`)
- Reading vote reasoning and agent decisions (in `agent_*/*/vote.json`)
- Viewing the coordination flow table (in `coordination_table.txt`)
- Getting cost/token summaries (in `metrics_summary.json`)

**Use Logfire When:**
- You need precise timing data with millisecond accuracy
- Analyzing span hierarchy and parent-child relationships
- Finding exceptions and error stack traces
- Creating shareable trace links for collaboration
- Querying across multiple sessions (e.g., "find all sessions with errors")
- Real-time monitoring of running experiments

**Rate Limiting:** If Logfire returns a rate limit error, **wait up to 60 seconds and retry** rather than falling back to local logs. The rate limit resets quickly and Logfire data is worth waiting for when timing/hierarchy analysis is needed.

**Key Local Log Files:**

| File | Contains |
|------|----------|
| `status.json` | Real-time status with **agent reliability metrics** (enforcement events, buffer loss) |
| `metrics_summary.json` | Cost, tokens, tool stats, round history |
| `coordination_events.json` | Full event timeline with tool calls |
| `coordination_table.txt` | Human-readable coordination flow |
| `streaming_debug.log` | Raw streaming data including command strings |
| `agent_*/*/vote.json` | Vote reasoning and context |
| `agent_*/*/execution_trace.md` | **Full tool calls, arguments, results, and reasoning** - invaluable for debugging |
| `execution_metadata.yaml` | Config and session metadata |

**Execution Traces (`execution_trace.md`):**
These are the most detailed debug artifacts. Each agent snapshot includes an execution trace with:
- Complete tool calls with full arguments (not truncated)
- Full tool results (not truncated)
- Reasoning/thinking blocks from the model
- Timestamps and round markers

Use execution traces when you need to understand exactly what an agent did and why - they capture everything the agent saw and produced during that answer/vote iteration.

**Enforcement Reliability (`status.json`):**
The `status.json` file includes per-agent reliability metrics that track workflow enforcement events:

```json
{
  "agents": {
    "agent_a": {
      "reliability": {
        "enforcement_attempts": [
          {
            "round": 0,
            "attempt": 1,
            "max_attempts": 3,
            "reason": "no_workflow_tool",
            "tool_calls": ["search", "read_file"],
            "error_message": "Must use workflow tools",
            "buffer_preview": "First 500 chars of lost content...",
            "buffer_chars": 1500,
            "timestamp": 1736683468.123
          }
        ],
        "by_round": {"0": {"count": 2, "reasons": ["no_workflow_tool", "invalid_vote_id"]}},
        "unknown_tools": ["execute_command"],
        "workflow_errors": ["invalid_vote_id"],
        "total_enforcement_retries": 2,
        "total_buffer_chars_lost": 3000,
        "outcome": "ok"
      }
    }
  }
}
```

**Enforcement Reason Codes:**
| Reason | Description |
|--------|-------------|
| `no_workflow_tool` | Agent called tools but none were `vote` or `new_answer` |
| `no_tool_calls` | Agent provided text-only response, no tools called |
| `invalid_vote_id` | Agent voted for non-existent agent ID |
| `vote_no_answers` | Agent tried to vote when no answers exist |
| `vote_and_answer` | Agent used both `vote` and `new_answer` in same response |
| `answer_limit` | Agent hit max answer count limit |
| `answer_novelty` | Answer too similar to existing answers |
| `answer_duplicate` | Exact duplicate of existing answer |
| `api_error` | API/streaming error (e.g., "peer closed connection") |
| `connection_recovery` | API stream ended early, recovered with preserved context |
| `mcp_disconnected` | MCP server disconnected mid-session (e.g., "Server 'X' not connected") |

This data is invaluable for understanding **why agents needed retries** and **how much content was lost** due to enforcement restarts.

## Logfire Setup

Before using this skill, you need to set up Logfire for observability.

### Step 1: Install MassGen with Observability Support

```bash
pip install "massgen[observability]"

# Or with uv
uv pip install "massgen[observability]"
```

### Step 2: Create a Logfire Account

Go to <https://logfire.pydantic.dev/> and create a free account.

### Step 3: Authenticate with Logfire

```bash
# This creates ~/.logfire/credentials.json
uv run logfire auth

# Or set the token directly as an environment variable
export LOGFIRE_TOKEN=your_token_here
```

### Step 4: Get Your Read Token for the MCP Server

1. Go to <https://logfire.pydantic.dev/> and log in
2. Navigate to your project settings
3. Create a **Read Token** (this is different from the write token used for authentication)
4. Copy the token for use in Step 5

### Step 5: Add the Logfire MCP Server

```bash
claude mcp add logfire -e LOGFIRE_READ_TOKEN="your-read-token-here" -- uvx logfire-mcp@latest
```

Then restart Claude Code and re-invoke this skill.

## Prerequisites

**Logfire MCP Server (Optional but Recommended):**
The Logfire MCP server provides enhanced analysis with precise timing data and cross-session queries. If `LOGFIRE_READ_TOKEN` is not set, self-analysis mode will automatically disable the Logfire MCP and fall back to local log files only.

When configured, the MCP server provides these tools:
- `mcp__logfire__arbitrary_query` - Run SQL queries against logfire data
- `mcp__logfire__schema_reference` - Get the database schema
- `mcp__logfire__find_exceptions_in_file` - Find exceptions in a file
- `mcp__logfire__logfire_link` - Create links to traces in the UI

**Required Flags:**
- `--automation` - Clean output for programmatic parsing -- see `massgen-develops-massgen` skill for more info on this flag
- `--logfire` - Enable Logfire tracing (optional, but required to populate Logfire data)

## Part 1: Running MassGen Experiments

### Basic Command Format

```bash
uv run massgen --automation --logfire --config [config_file] "[question]"
```

### Running in Background (Recommended)

Use `run_in_background: true` (or however you run tasks in the background) to run experiments asynchronously so you can monitor progress and end early if needed.

**Expected Output (first lines):**
```
LOG_DIR: .massgen/massgen_logs/log_YYYYMMDD_HHMMSS_ffffff
STATUS: .massgen/massgen_logs/log_YYYYMMDD_HHMMSS_ffffff/turn_1/attempt_1/status.json
QUESTION: Your task here
[Coordination in progress - monitor status.json for real-time updates]
```

**Parse the LOG_DIR** - you'll need this for file-based analysis!

### Monitoring Progress

`status.json` updates every 2 seconds; use that to track progress.

```bash
cat [log_dir]/turn_1/attempt_1/status.json
```

**Key fields to monitor:**
- `coordination.completion_percentage` (0-100)
- `coordination.phase` - "initial_answer", "enforcement", "presentation"
- `results.winner` - null while running, agent_id when complete
- `agents[].status` - "waiting", "streaming", "answered", "voted", "error"
- `agents[].error` - null if ok, error details if failed

### Reading Final Results

After completion (exit code 0):

```bash
# Read the final answer
cat [log_dir]/turn_1/attempt_1/final/[winner]/answer.txt
```

**Other useful files:**
- `execution_metadata.yaml` - Full config and execution details
- `coordination_events.json` - Complete event log
- `coordination_table.txt` - Human-readable coordination summary

## Part 2: Querying Logfire

### Database Schema

The main table is `records` with these key columns:

| Column | Description |
|--------|-------------|
| `span_name` | Name of the span (e.g., "agent.agent_a.round_0") |
| `span_id` | Unique identifier for this span |
| `parent_span_id` | ID of the parent span (null for root) |
| `trace_id` | Groups all spans in a single trace |
| `duration` | Time in seconds |
| `start_timestamp` | When the span started |
| `end_timestamp` | When the span ended |
| `attributes` | JSON blob with custom attributes |
| `message` | Log message |
| `is_exception` | Boolean for errors |
| `exception_type` | Type of exception if any |
| `exception_message` | Exception message |

### MassGen Span Hierarchy

MassGen creates hierarchical spans:

```
coordination.session (root)
├── Coordination event: coordination_started
├── agent.agent_a.round_0
│   ├── llm.openrouter.stream
│   ├── mcp.filesystem.write_file
│   └── Tool execution: mcp__filesystem__write_file
├── agent.agent_b.round_0
├── Agent answer: agent1.1
├── agent.agent_a.round_1 (voting round)
├── Agent vote: agent_a -> agent1.1
├── Coordination event: winner_selected
└── agent.agent_a.presentation
    ├── Winner selected: agent1.1
    ├── llm.openrouter.stream
    └── Final answer from agent_a
```

### Custom Attributes

MassGen spans include these custom attributes (access via `attributes->'key'`):

| Attribute | Description |
|-----------|-------------|
| `massgen.agent_id` | Agent identifier (agent_a, agent_b) |
| `massgen.iteration` | Current iteration number |
| `massgen.round` | Round number for this agent |
| `massgen.round_type` | "initial_answer", "voting", or "presentation" |
| `massgen.backend` | Backend provider name |
| `massgen.num_context_answers` | Number of answers in context |
| `massgen.is_winner` | True for presentation spans |
| `massgen.outcome` | "vote", "answer", or "error" (set after round completes) |
| `massgen.voted_for` | Agent ID voted for (only set for votes) |
| `massgen.voted_for_label` | Answer label voted for (e.g., "agent1.1", only set for votes) |
| `massgen.answer_label` | Answer label assigned (e.g., "agent1.1", only set for answers) |
| `massgen.error_message` | Error message (only set when outcome is "error") |
| `massgen.usage.input` | Input token count |
| `massgen.usage.output` | Output token count |
| `massgen.usage.reasoning` | Reasoning token count |
| `massgen.usage.cached_input` | Cached input token count |
| `massgen.usage.cost` | Estimated cost in USD |

## Part 3: Common Analysis Queries

### 1. View Trace Hierarchy

```sql
SELECT span_name, span_id, parent_span_id, duration, start_timestamp
FROM records
WHERE trace_id = '[YOUR_TRACE_ID]'
ORDER BY start_timestamp
LIMIT 50
```

### 2. Find Recent Sessions

```sql
SELECT span_name, trace_id, duration, start_timestamp
FROM records
WHERE span_name = 'coordination.session'
ORDER BY start_timestamp DESC
LIMIT 10
```

### 3. Agent Round Performance

```sql
SELECT
  span_name,
  duration,
  attributes->>'massgen.agent_id' as agent_id,
  attributes->>'massgen.round' as round,
  attributes->>'massgen.round_type' as round_type
FROM records
WHERE span_name LIKE 'agent.%'
ORDER BY start_timestamp DESC
LIMIT 20
```

### 4. Tool Call Analysis

```sql
SELECT
  span_name,
  duration,
  parent_span_id,
  start_timestamp
FROM records
WHERE span_name LIKE 'mcp.%' OR span_name LIKE 'Tool execution:%'
ORDER BY start_timestamp DESC
LIMIT 30
```

### 5. Find Errors

```sql
SELECT
  span_name,
  exception_type,
  exception_message,
  trace_id,
  start_timestamp
FROM records
WHERE is_exception = true
ORDER BY start_timestamp DESC
LIMIT 20
```

### 6. LLM Call Performance

```sql
SELECT
  span_name,
  duration,
  attributes->>'gen_ai.request.model' as model,
  start_timestamp
FROM records
WHERE span_name LIKE 'llm.%'
ORDER BY start_timestamp DESC
LIMIT 30
```

### 7. Full Trace with Hierarchy (Nested View)

```sql
SELECT
  CASE
    WHEN parent_span_id IS NULL THEN span_name
    ELSE '  └─ ' || span_name
  END as hierarchy,
  duration,
  span_id,
  parent_span_id
FROM records
WHERE trace_id = '[YOUR_TRACE_ID]'
ORDER BY start_timestamp
```

### 8. Coordination Events Timeline

```sql
SELECT span_name, message, duration, start_timestamp
FROM records
WHERE span_name LIKE 'Coordination event:%'
   OR span_name LIKE 'Agent answer:%'
   OR span_name LIKE 'Agent vote:%'
   OR span_name LIKE 'Winner selected:%'
ORDER BY start_timestamp DESC
LIMIT 30
```

## Part 4: Analysis Workflow

### Step 1: Run Experiment

```bash
uv run massgen --automation --logfire --config [config] "[prompt]" 2>&1
```

### Step 2: Find the Trace

Query for recent sessions:
```sql
SELECT trace_id, duration, start_timestamp
FROM records
WHERE span_name = 'coordination.session'
ORDER BY start_timestamp DESC
LIMIT 5
```

### Step 3: Analyze Hierarchy

Get full trace structure:
```sql
SELECT span_name, span_id, parent_span_id, duration
FROM records
WHERE trace_id = '[trace_id_from_step_2]'
ORDER BY start_timestamp
```

### Step 4: Investigate Specific Issues

**Slow tool calls:**
```sql
SELECT span_name, duration, parent_span_id
FROM records
WHERE trace_id = '[trace_id]' AND span_name LIKE 'mcp.%'
ORDER BY duration DESC
```

**Agent comparison:**
```sql
SELECT
  attributes->>'massgen.agent_id' as agent,
  COUNT(*) as rounds,
  SUM(duration) as total_time,
  AVG(duration) as avg_round_time
FROM records
WHERE trace_id = '[trace_id]' AND span_name LIKE 'agent.%'
GROUP BY attributes->>'massgen.agent_id'
```

### Step 5: Create Trace Link

Use the MCP tool to create a viewable link:
```
mcp__logfire__logfire_link(trace_id="[your_trace_id]")
```

## Part 5: Improving the Logging Structure

### Current Span Types

| Span Pattern | Source | Description |
|--------------|--------|-------------|
| `coordination.session` | coordination_tracker.py | Root session span |
| `agent.{id}.round_{n}` | orchestrator.py | Agent execution round |
| `agent.{id}.presentation` | orchestrator.py | Winner's final presentation |
| `mcp.{server}.{tool}` | mcp_tools/client.py | MCP tool execution |
| `llm.{provider}.stream` | backends | LLM streaming call |
| `Tool execution: {name}` | base_with_custom_tool.py | Tool wrapper |
| `Coordination event: *` | coordination_tracker.py | Coordination events |
| `Agent answer: {label}` | coordination_tracker.py | Answer submission |
| `Agent vote: {from} -> {to}` | coordination_tracker.py | Vote cast |

### Adding New Spans

Use the tracer from structured_logging:

```python
from massgen.structured_logging import get_tracer

tracer = get_tracer()
with tracer.span("my_operation", attributes={
    "massgen.custom_key": "value",
}):
    do_work()
```

### Context Propagation Notes

**Known limitation:** When multiple agents run concurrently via `asyncio.create_task`, child spans may not nest correctly under agent round spans. This is an OpenTelemetry context propagation issue with concurrent async code. The presentation phase works correctly because only one agent runs.

**Workaround:** For accurate nesting in concurrent scenarios, explicit context passing with `contextvars.copy_context()` would be needed.

## Logfire Documentation Reference

**Main Documentation:** <https://logfire.pydantic.dev/docs/>

### Key Pages to Know

| Topic | URL | Description |
|-------|-----|-------------|
| **Getting Started** | `/docs/` | Overview, setup, and core concepts |
| **Manual Tracing** | `/docs/guides/onboarding-checklist/add-manual-tracing/` | Creating spans, adding attributes |
| **SQL Explorer** | `/docs/guides/web-ui/explore/` | Writing SQL queries in the UI |
| **Live View** | `/docs/guides/web-ui/live/` | Real-time trace monitoring |
| **Query API** | `/docs/how-to-guides/query-api/` | Programmatic access to data |
| **OpenAI Integration** | `/docs/integrations/llms/openai/` | LLM call instrumentation |

### Logfire Concepts

**Spans vs Logs:**
- **Spans** represent operations with measurable duration (use `with logfire.span():`)
- **Logs** capture point-in-time events (use `logfire.info()`, `logfire.error()`, etc.)
- Spans and logs inside a span block become children of that span

**Span Names vs Messages:**
- `span_name` = the first argument (used for filtering, keep low-cardinality)
- `message` = formatted result with attribute values interpolated
- Example: `logfire.info('Hello {name}', name='Alice')` → span_name="Hello {name}", message="Hello Alice"

**Attributes:**
- Keyword arguments become structured JSON attributes
- Access in SQL via `attributes->>'key'` or `attributes->'key'`
- Cast when needed: `(attributes->'cost')::float`

### Live View Features

The Logfire Live View UI (<https://logfire.pydantic.dev/>) provides:
- **Real-time streaming** of traces as they arrive
- **SQL search pane** (press `/` to open) with auto-complete
- **Natural language to SQL** - describe what you want and get a query
- **Timeline histogram** showing span counts over time
- **Trace details panel** with attributes, exceptions, and OpenTelemetry data
- **Cross-linking** between SQL results and trace view via trace_id/span_id

### SQL Explorer Tips

The Explore page uses Apache DataFusion SQL syntax (similar to Postgres):

```sql
-- Subqueries and CTEs work
WITH recent AS (
  SELECT * FROM records
  WHERE start_timestamp > now() - interval '1 hour'
)
SELECT * FROM recent WHERE is_exception;

-- Access nested JSON
SELECT attributes->>'massgen.agent_id' as agent FROM records;

-- Cast JSON values
SELECT (attributes->'token_count')::int as tokens FROM records;

-- Time filtering is efficient
WHERE start_timestamp > now() - interval '30 minutes'
```

### LLM Instrumentation

Logfire auto-instruments OpenAI calls when configured:
- Captures conversation display, token usage, response metadata
- Creates separate spans for streaming requests vs responses
- Works with both sync and async clients

MassGen's backends use this for `llm.{provider}.stream` spans.

## Reference Documentation

**Logfire:**
- Main docs: <https://logfire.pydantic.dev/docs/>
- Live View: <https://logfire.pydantic.dev/docs/guides/web-ui/live/>
- SQL Explorer: <https://logfire.pydantic.dev/docs/guides/web-ui/explore/>
- Query API: <https://logfire.pydantic.dev/docs/how-to-guides/query-api/>
- Manual tracing: <https://logfire.pydantic.dev/docs/guides/onboarding-checklist/add-manual-tracing/>
- OpenAI integration: <https://logfire.pydantic.dev/docs/integrations/llms/openai/>
- Schema reference: Use `mcp__logfire__schema_reference` tool

**MassGen:**
- Automation mode: `AI_USAGE.md`
- Status file reference: `docs/source/reference/status_file.rst`
- Structured logging: `massgen/structured_logging.py`

## Tips for Effective Analysis

1. **Always use both flags:** `--automation --logfire` together
2. **Run in background** for long tasks to monitor progress
3. **Query by trace_id** to isolate specific sessions
4. **Check parent_span_id** to understand hierarchy
5. **Use duration** to identify bottlenecks
6. **Look at attributes** for MassGen-specific context
7. **Create trace links** to share findings with team

Note that you may get an error like so:
```bash
Error: Error executing tool arbitrary_query: b'{"detail":"Rate limit exceeded for organization xxx: per minute
     limit reached."}'
```

In this case, please sleep (for up to a minute) and try again.

## Part 6: Comprehensive Log Analysis Report

When asked to analyze a MassGen log run, generate a **markdown report** saved to `[log_dir]/turn_N/ANALYSIS_REPORT.md` where N is the turn being analyzed. Each turn (coordination session) gets its own analysis report as a sibling to the attempt directories. The report must cover the **Standard Analysis Questions** below.

### Important: Ground Truth and Correctness

**CRITICAL**: Do not assume any agent's answer is "correct" unless the user explicitly provides ground truth.

- Report what each agent claimed/produced without asserting correctness
- Note when agents agree or disagree, but don't claim agreement = correctness
- If agents produce different answers, present both neutrally
- Only mark answers as correct/incorrect if user provides the actual answer
- Phrases to avoid: "correctly identified", "got the right answer", "solved correctly"
- Phrases to use: "claimed", "produced", "submitted", "arrived at"

### Standard Analysis Questions

Every analysis report MUST answer these questions:

#### 1. Correctness
- Did coordination complete successfully?
- Did all agents submit answers?
- Did voting occur correctly?
- Was a winner selected and did they provide a final answer?

#### 2. Efficiency & Bottlenecks
- What was the total duration and breakdown by phase?
- What were the slowest operations?
- Which tools took the most time?
- Build a **per-round timing table sorted by agent** with:
  - Round start/end timestamps
  - Total round time
  - Tool wall time
  - Non-tool time (model/streaming/waiting)
- Split each checklist-containing round into:
  - **Evaluation** = round start -> first `submit_checklist` start
  - **Checklist->Propose** = first `submit_checklist` end -> first `propose_improvements` start
  - **Implementation** = first `propose_improvements` end -> round end
  - **Post-checklist (no propose)** = first `submit_checklist` end -> round end (if no propose happened)
- Report percentages for **evaluation vs implementation**:
  - Across all checklist-containing segments
  - Across only segments that actually include `propose_improvements`

#### 3. Command Pattern Analysis
- **Were there frequently repeated commands that could be avoided?** (e.g., `openskills read`, `npm install`, `ls -R`)
- **What commands produced unnecessarily long output?** (e.g., skill docs, directory listings)
- **What were the slowest `execute_command` patterns?** (e.g., web scraping, package installs)

#### 4. Work Duplication Analysis
- **Was expensive work (like image generation) unnecessarily redone?**
- **Did both agents generate similar/identical assets?**
- **Were assets regenerated after restarts instead of being reused?**
- **Could caching or sharing have saved time/cost?**

#### 5. Agent Behavior & Decision Making
- **How did agents evaluate previous answers?** What reasoning did they provide?
- **How did agents decide between voting vs providing a new answer?**
- **Did agents genuinely build upon each other's work or work in isolation?**
- **Were there timeouts or incomplete rounds?**

#### 6. Cost & Token Analysis
- Total cost and breakdown by agent
- Token usage (input, output, reasoning, cached)
- Cache hit rate

#### 7. Errors & Issues
- Any exceptions or failures?
- Any timeouts?
- Any agent errors?

#### 8. Agent Reasoning & Behavior Analysis (CRITICAL)

**This is the most important section.** Analyzing how agents think and act reveals root causes of successes and failures.

**Data Sources:**
- `agent_outputs/agent_*.txt` - Full output including reasoning (if available)
- `agent_*/*/execution_trace.md` - Complete tool calls with arguments and results
- `streaming_debug.log` - Raw streaming chunks

**Note:** Some models don't emit explicit reasoning traces. For these, analyze **tool call patterns and content** instead - the sequence of actions still reveals decision-making.

**For EACH agent, analyze:**

1. **Strategy** - What approach did they take? (from reasoning OR tool sequence)
2. **Tool Responses** - How did they handle successes/failures/inconsistencies?
3. **Error Recovery** - Did they detect problems? Implement workarounds?
4. **Decision Quality** - Logical errors? Over/under-verification? Analysis paralysis?
5. **Cross-Agent Comparison** - Which had best reasoning? What patterns led to success?

**Key Patterns:**

| Pattern | Good Sign | Bad Sign |
|---------|-----------|----------|
| Failure detection | Pivots after 2-3 failures | Repeats broken approach 6+ times |
| Result validation | Cross-validates outputs | Accepts first result blindly |
| Inconsistency handling | Investigates conflicts | Ignores contradictions |
| Workarounds | Creative alternatives when stuck | Gives up or loops |
| Time management | Commits when confident | Endless verification, no answer |

**Extract Key Evidence:** For each agent, include 2-3 quotes (if reasoning available) OR describe key tool sequences that illustrate their decision quality.

#### 9. Tool Reliability Analysis

Analyze tool behavior patterns beyond simple error listing:

1. **Consistency** - Same input, same output? Document variance.
2. **False Positives/Negatives** - Tools reporting wrong success/failure status?
3. **Root Cause Hypotheses** - For each failure pattern, propose likely causes (path issues, rate limits, model limitations, etc.)

#### 10. Enforcement & Workflow Reliability Analysis

**Data Source:** `status.json` → `agents[].reliability`

Check if agents needed retries due to workflow violations. Key metrics:
- `total_enforcement_retries` - How many times agent was forced to retry
- `total_buffer_chars_lost` - Content discarded due to restarts
- `unknown_tools` - Hallucinated tool names
- `by_round` - Which rounds had issues

**Red Flags:** >=2 retries per round, >5000 chars lost, populated `unknown_tools` list.

See "Enforcement Reliability" in the Key Local Log Files section for the full schema and reason codes.

#### 11. Answer Quality Progression

**Data Sources:** `agent_outputs/agent_*.txt`, `agent_*/*/execution_trace.md`, `agent_*/*/vote.json`

For each agent, trace how answer quality evolved across rounds:
- What specifically changed between answer N and answer N+1?
- Were changes **substantive** (new approach, novel feature, structural improvement) or **cosmetic** (minor wording, small style tweak)?
- Did any agents regress — produce a worse answer after seeing others?
- Which evaluation criteria improved per round, and which stagnated?

**Score each round-over-round transition:**
- 🟢 Substantive improvement — meaningfully better on at least one important dimension
- 🟡 Marginal improvement — polished but no new capability or insight
- 🔴 No improvement / regression — same or worse despite the cost

#### 12. Improvement Proposal Quality

**Data Sources:** `agent_outputs/agent_*.txt` (look for gap analysis, diagnostic sections, improvement plans), `agent_*/*/vote.json`

Before each new answer, agents (or the coordination system) propose improvements. Analyze each:
- **Specificity**: Did the proposal identify *why* something fails, or just that it fails? ("Animation timing misaligned with 5-second viewing window" vs "improve animation")
- **Actionability**: Could a downstream agent implement the proposal without additional reasoning?
- **Accuracy**: Did the proposal correctly diagnose the root problem, or address symptoms?
- **Completeness**: Did it cover all the key gaps, or miss the decisive differentiator?

**Rate each proposal:**

| Proposal | Specific? | Actionable? | Accurate? | Was it the right call? |
|----------|-----------|-------------|-----------|------------------------|
| [proposal summary] | Yes/No | Yes/No | Yes/No | Yes/No — [why] |

Also note: were improvements proposed by the agent itself (self-reflection), by peer evaluation, or inferred from evaluation criteria gaps?

#### 13. Round ROI ("Was It Worth It?")

**Data Sources:** `metrics_summary.json`, `coordination_events.json`, agent outputs

For each round, evaluate return on investment:
- **Cost**: tokens × model rate for this round
- **Time**: wall-clock seconds for this round
- **Quality delta**: what materially changed vs the prior best answer
- **Verdict**: Was the round worth its cost and time?

| Round | Agent | Cost | Time | Quality Delta | Verdict |
|-------|-------|------|------|---------------|---------|
| R0 | agent_a | $X | Xs | Baseline | — |
| R1 | agent_a | $X | Xs | [what changed] | 🟢/🟡/🔴 |

**Diminishing returns detection**: At what round did additional iterations stop producing meaningful improvement? Was there a clear stopping point the system missed?

Also flag: did any agent spend expensive rounds just verifying/validating rather than improving?

#### 14. Delegation & Model Allocation Analysis

**Data Sources:** `agent_outputs/agent_*.txt`, `execution_trace.md`, `metrics_summary.json`

Analyze what fraction of each agent's work was mechanical vs required genuine intelligence, and whether the right model tier was used.

**Classify each agent's work per round:**

- **Mechanical** (predictable, templated, a weaker model could do it — AND consumes enough context to be worth delegating):
  - Structural validation (element counts, dimension checks, format compliance) — especially when it generates lots of shell output
  - Boilerplate generation (loops, coordinate math, template filling) — large repetitive code blocks
  - Binary checklist scoring (E1–E4 style: does feature X exist?) — when it involves many tool calls or long output
  - Evidence collection (running shell commands, parsing output, pixel diffs) — high token cost for low reasoning content

  *Note: protocol steps like task status updates and workflow tool calls are not worth delegating — they're low-context and the main model handles them cheaply inline. The question is whether delegating saves meaningful tokens, not just whether a weaker model could theoretically do it.*

- **Quality / Intelligence** (requires genuine reasoning, synthesis, or creativity):
  - Root cause diagnosis (connecting symptom to underlying design flaw)
  - Cross-agent synthesis (identifying best elements from N answers and planning a hybrid)
  - Novel approach invention (feature or design not present in any prior answer)
  - Pedagogical or domain reasoning (e.g., "this animation timing misses the 5s attention window")
  - Tradeoff analysis (why one design choice beats another for a specific goal)

**For each agent/round, estimate:**
- % mechanical vs % quality reasoning
- Which specific activities were mechanical vs intelligence-requiring
- Quote passages: mechanical template-filling vs genuine diagnostic insight

**Overall assessment:**
- What fraction of total context (tokens) across the run was mechanical?
- Could a cheaper model (e.g., Haiku) have handled the mechanical fraction without degrading output quality?
- Were any quality-critical moments handled by a weaker subagent (or should they have been escalated)?
- Estimated cost savings if mechanical work had been routed to a cheaper model tier

### Data Sources for Each Question

| Question | Primary Source | Secondary Source |
|----------|----------------|------------------|
| Correctness | `coordination_events.json`, `coordination_table.txt` | Logfire coordination events |
| Efficiency | `metrics_summary.json` | Logfire duration queries |
| Command patterns | `streaming_debug.log` (grep for `"command":`) | - |
| Work duplication | `streaming_debug.log` (grep for tool prompts/args) | `metrics_summary.json` tool counts |
| Agent decisions | `agent_*/*/vote.json`, `coordination_events.json` | Logfire vote spans |
| Eval vs implementation timing | `status.json`, `metrics_events.json` | `events.jsonl`, Logfire span durations |
| Cost/tokens | `metrics_summary.json` | Logfire usage attributes |
| Errors | `coordination_events.json`, `metrics_summary.json` | Logfire `is_exception=true` |
| Enforcement | `status.json` → `agents[].reliability` | - |

### Analysis Commands

**Find repeated commands:**
```bash
grep -o '"command": "[^"]*"' streaming_debug.log | sed 's/"command": "//;s/"$//' | sort | uniq -c | sort -rn | head -30
```

**Find generate_media prompts (to check for duplication):**
```bash
grep -o '"prompts": \[.*\]' streaming_debug.log
```

**Check vote reasoning:**
```bash
cat agent_*/*/vote.json | jq '.reason'
```

**Find timeout events:**
```bash
cat coordination_events.json | jq '.events[] | select(.event_type == "agent_timeout")'
```

**Compute per-round evaluation vs implementation timing (sorted by agent):**
```bash
python - <<'PY'
import json
from collections import defaultdict
from pathlib import Path

base = Path(".")
status = json.loads((base / "status.json").read_text())
metrics = json.loads((base / "metrics_events.json").read_text())

def m(seconds):
    return seconds / 60.0

def union(intervals):
    if not intervals:
        return 0.0
    intervals = sorted(intervals)
    cs, ce = intervals[0]
    total = 0.0
    for s, e in intervals[1:]:
        if s <= ce:
            ce = max(ce, e)
        else:
            total += ce - cs
            cs, ce = s, e
    total += ce - cs
    return total

segments = []
for agent_id, agent_data in status["agents"].items():
    rounds = sorted(agent_data.get("round_history", []), key=lambda r: r["start_time"])
    for idx, r in enumerate(rounds, 1):
        segments.append({
            "agent": agent_id,
            "seg_idx": idx,
            "round_number": r["round_number"],
            "round_type": r["round_type"],
            "outcome": r["outcome"],
            "start": float(r["start_time"]),
            "end": float(r["end_time"]),
            "duration": float(r["duration_ms"]) / 1000.0,
        })

by_segment = defaultdict(list)
for t in metrics["tool_executions"]:
    ts = float(t["start_time"])
    te = float(t["end_time"])
    candidates = [
        s for s in segments
        if s["agent"] == t["agent_id"] and not (te < s["start"] or ts > s["end"])
    ]
    if not candidates:
        continue
    best = max(
        candidates,
        key=lambda s: max(0.0, min(te, s["end"]) - max(ts, s["start"])),
    )
    by_segment[(best["agent"], best["seg_idx"])].append(t)

rows = []
for s in sorted(segments, key=lambda x: (x["agent"], x["start"])):
    calls = sorted(by_segment.get((s["agent"], s["seg_idx"]), []), key=lambda t: t["start_time"])
    submit = [t for t in calls if t["tool_name"] == "mcp__massgen_checklist__submit_checklist"]
    propose = [t for t in calls if t["tool_name"] == "mcp__massgen_checklist__propose_improvements"]

    # round-level tool wall time
    ints = []
    for t in calls:
        ts, te = float(t["start_time"]), float(t["end_time"])
        ov = max(0.0, min(te, s["end"]) - max(ts, s["start"]))
        if ov > 0:
            ints.append((max(ts, s["start"]), min(te, s["end"])))
    tool_wall = union(ints)
    non_tool = max(0.0, s["duration"] - tool_wall)

    eval_pre = mid = impl_post = post_no_propose = 0.0
    first_submit = submit[0] if submit else None
    first_propose = propose[0] if propose else None

    if first_submit:
        eval_pre = max(0.0, min(s["end"], float(first_submit["start_time"])) - s["start"])
    elif first_propose:
        eval_pre = max(0.0, min(s["end"], float(first_propose["start_time"])) - s["start"])

    if first_submit and first_propose:
        mid = max(0.0, min(s["end"], float(first_propose["start_time"])) - float(first_submit["end_time"]))
        impl_post = max(0.0, s["end"] - float(first_propose["end_time"]))
    elif first_submit and not first_propose:
        post_no_propose = max(0.0, s["end"] - float(first_submit["end_time"]))
    elif first_propose and not first_submit:
        impl_post = max(0.0, s["end"] - float(first_propose["end_time"]))

    rows.append({
        **s,
        "tool_wall": tool_wall,
        "non_tool": non_tool,
        "submit_count": len(submit),
        "propose_count": len(propose),
        "eval_pre": eval_pre,
        "mid": mid,
        "impl_post": impl_post,
        "post_no_propose": post_no_propose,
    })

print("| Agent | Segment | Round | Type | Outcome | Total (min) | Tool wall (min) | Non-tool (min) | Eval pre (min) | Checklist->Propose (min) | Improve post-propose (min) | Post-checklist no-propose (min) |")
print("|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|")
for r in rows:
    print(
        f"| {r['agent']} | {r['seg_idx']} | {r['round_number']} | {r['round_type']} | {r['outcome']} | "
        f"{m(r['duration']):.2f} | {m(r['tool_wall']):.2f} | {m(r['non_tool']):.2f} | "
        f"{m(r['eval_pre']):.2f} | {m(r['mid']):.2f} | {m(r['impl_post']):.2f} | {m(r['post_no_propose']):.2f} |"
    )
PY
```

### Report Template

Save this report to `[log_dir]/turn_N/ANALYSIS_REPORT.md` (where N is the turn number being analyzed):

```markdown
# MassGen Log Analysis Report

**Session:** [log_dir name]
**Trace ID:** [trace_id if available]
**Generated:** [timestamp]
**Logfire Link:** [link if available]

## Executive Summary

[2-3 sentence summary of the run: what was the task, did it succeed, key findings]

## Session Overview

| Metric | Value |
|--------|-------|
| Duration | X minutes |
| Agents | [list] |
| Winner | [agent_id] |
| Total Cost | $X.XX |
| Total Answers | X |
| Total Votes | X |
| Total Restarts | X |

## 1. Correctness Analysis

### Coordination Flow
[Timeline of key events]

### Status
- [ ] All phases completed
- [ ] All agents submitted answers
- [ ] Voting completed correctly
- [ ] Winner selected
- [ ] Final answer delivered

### Issues Found
[List any correctness issues]

## 2. Efficiency Analysis

### Phase Duration Breakdown
| Phase | Count | Avg (s) | Max (s) | Total (s) | % of Total |
|-------|-------|---------|---------|-----------|------------|
| initial_answer | | | | | |
| voting | | | | | |
| presentation | | | | | |

### Per-Round Timing (Sorted by Agent)
| Agent | Segment | Round | Type | Outcome | Start-End | Total (min) | Tool wall (min) | Non-tool (min) |
|-------|---------|-------|------|---------|-----------|-------------|-----------------|----------------|
| agent_a | 1 | r0 | initial_answer | answer | HH:MM:SS-HH:MM:SS | | | |
| ... | | | | | | | | |

### Evaluation vs Implementation Timing (Checklist-Gated Phases)

**Phase definitions used in this report:**
- Evaluation = round start -> first `submit_checklist` start
- Checklist->Propose = first `submit_checklist` end -> first `propose_improvements` start
- Implementation = first `propose_improvements` end -> round end
- Post-checklist (no propose) = first `submit_checklist` end -> round end (if no propose happened)

| Scope | Evaluation (min / %) | Checklist->Propose (min / %) | Implementation (min / %) | Post-checklist no-propose (min / %) |
|-------|-----------------------|-------------------------------|---------------------------|--------------------------------------|
| All checklist-containing segments | | | | |
| Only segments with propose_improvements | | | | |

### Per-Round Evaluation vs Improvement Table
| Agent | Segment | Round | Total (min) | Eval pre-checklist (min) | Checklist->Propose (min) | Improve post-propose (min) | Post-checklist no-propose (min) | Eval vs Improve verdict |
|-------|---------|-------|-------------|----------------------------|---------------------------|-----------------------------|----------------------------------|-------------------------|
| agent_c | 2 | r1 | | | | | | [which side dominates and why] |
| ... | | | | | | | | |

### Top Bottlenecks
1. [Operation] - X seconds (X% of total)
2. [Operation] - X seconds
3. [Operation] - X seconds

## 3. Command Pattern Analysis

### Frequently Repeated Commands
| Command | Times Run | Issue | Recommendation |
|---------|-----------|-------|----------------|
| `openskills read pptx` | X | Long output (~5KB) re-read after restarts | Cache skill docs |
| `npm install ...` | X | Reinstalled after each restart | Persist node_modules |
| ... | | | |

### Commands with Excessive Output
| Command | Output Size | Issue |
|---------|-------------|-------|
| | | |

### Slowest Command Patterns
| Pattern | Max Time | Avg Time | Notes |
|---------|----------|----------|-------|
| Web scraping (crawl4ai) | Xs | Xs | |
| npm install | Xs | Xs | |
| PPTX pipeline | Xs | Xs | |

## 4. Work Duplication Analysis

### Duplicated Work Found
| Work Type | Times Repeated | Wasted Time | Wasted Cost |
|-----------|----------------|-------------|-------------|
| Image generation | X | X min | $X.XX |
| Research/scraping | X | X min | - |
| Package installs | X | X min | - |

### Specific Examples
[List specific examples of duplicated work with prompts/commands]

### Recommendations
1. [Specific recommendation to avoid duplication]
2. [Specific recommendation]

## 5. Agent Behavior Analysis

### Answer Progression
| Label | Agent | Time | Summary |
|-------|-------|------|---------|
| agent1.1 | agent_a | HH:MM | [brief description] |
| agent2.1 | agent_b | HH:MM | [brief description] |
| ... | | | |

### Voting Analysis
| Voter | Voted For | Reasoning Summary |
|-------|-----------|-------------------|
| agent_b | agent1.1 | "[key quote from reasoning]" |

### Vote vs New Answer Decisions
[Explain how agents decided whether to vote or provide new answers]

### Agent Collaboration Quality
- Did agents read each other's answers? [Yes/No with evidence]
- Did agents build upon previous work? [Yes/No with evidence]
- Did agents provide genuine evaluation? [Yes/No with evidence]

### Timeouts/Incomplete Rounds
[List any timeouts with context]

## 6. Cost & Token Analysis

### Cost Breakdown
| Agent | Input Tokens | Output Tokens | Reasoning | Cost |
|-------|--------------|---------------|-----------|------|
| agent_a | | | | $X.XX |
| agent_b | | | | $X.XX |
| **Total** | | | | **$X.XX** |

### Cache Efficiency
- Cached input tokens: X (X% cache hit rate)

### Tool Cost Impact
| Tool | Calls | Est. Time Cost | Notes |
|------|-------|----------------|-------|
| generate_media | X | X min | |
| command_line | X | X min | |

## 7. Errors & Issues

### Exceptions
[List any exceptions with type and message]

### Failed Tool Calls
[List any failed tools]

### Agent Errors
[List any agent-level errors]

### Timeouts
[List any timeouts with duration and context]

## 8. Recommendations

### High Priority
1. **[Issue]**: [Specific actionable recommendation]
2. **[Issue]**: [Specific actionable recommendation]

### Medium Priority
1. **[Issue]**: [Recommendation]

### Low Priority / Future Improvements
1. **[Issue]**: [Recommendation]

## 9. Suggested Linear Issues

Based on the analysis, the following issues are suggested for tracking. If you have access to the Linear project and the session is interactive, **present these to the user for approval before creating.** Regardless of access, you should write them in a section as below, as we want to learn from the logs to propose and later solve concrete issues:

| Priority | Title | Description | Labels |
|----------|-------|-------------|--------|
| High | [Short title] | [1-2 sentence description] | log-analysis, [area] |
| Medium | [Short title] | [Description] | log-analysis, [area] |

**After user approval**, create issues in Linear with:
- Project: MassGen
- Label: `log-analysis` (to identify issues from log analysis)
- Additional labels as appropriate (e.g., `performance`, `agent-behavior`, `tooling`)

## Appendix

### Configuration Used
[Key config settings from execution_metadata.yaml]

### Files Generated
[List of output files in the workspace]
```

### Workflow for Generating Report

1. **Read local files first** (metrics_summary.json, coordination_table.txt, coordination_events.json, status.json, metrics_events.json)
2. **Build per-round timing table sorted by agent**, including total/tool/non-tool time
3. **Compute checklist phase windows** (`pre_checklist`, `checklist_to_propose`, `post_propose`, `post_checklist_no_propose`) and evaluation vs implementation percentages
4. **For large logs, parallelize workflow analysis**: assign one subagent per agent/workflow lane and merge their timing tables
5. **Query Logfire** for trace_id and timing data (if available; wait and retry on rate limits)
6. **Analyze streaming_debug.log** for command patterns
7. **Check vote.json files** for agent reasoning
8. **Generate the report** using the template
9. **Save to** `[log_dir]/turn_N/ANALYSIS_REPORT.md` (N = turn number being analyzed)
10. **Print summary** to the user
11. **Suggest Linear issues** based on findings - present to user for approval, if session is interactive
12. **Create approved issues** in Linear with `log-analysis` label

## Part 7: Quick Reference - SQL Queries

### Correctness Queries

```sql
-- Check coordination flow
SELECT span_name, start_timestamp, duration
FROM records
WHERE trace_id = '[TRACE_ID]'
  AND (span_name LIKE 'Coordination event:%'
       OR span_name LIKE 'Agent answer:%'
       OR span_name LIKE 'Agent vote:%'
       OR span_name LIKE 'Winner selected:%'
       OR span_name LIKE 'Final answer%')
ORDER BY start_timestamp
```

### Efficiency Queries

```sql
-- Phase duration breakdown
SELECT
  CASE
    WHEN span_name LIKE 'agent.%.round_0' THEN 'initial_answer'
    WHEN span_name LIKE 'agent.%.round_%' THEN 'voting'
    WHEN span_name LIKE 'agent.%.presentation' THEN 'presentation'
    ELSE 'other'
  END as phase,
  COUNT(*) as count,
  ROUND(AVG(duration)::numeric, 2) as avg_duration_sec,
  ROUND(MAX(duration)::numeric, 2) as max_duration_sec,
  ROUND(SUM(duration)::numeric, 2) as total_duration_sec
FROM records
WHERE trace_id = '[TRACE_ID]'
  AND span_name LIKE 'agent.%'
GROUP BY 1
ORDER BY total_duration_sec DESC
```

### Error Queries

```sql
-- Find all exceptions
SELECT span_name, exception_type, exception_message, start_timestamp
FROM records
WHERE trace_id = '[TRACE_ID]' AND is_exception = true
ORDER BY start_timestamp
```

### Cost Queries

```sql
-- Token usage by agent
SELECT
  attributes->>'massgen.agent_id' as agent,
  SUM((attributes->'massgen.usage.input')::int) as total_input_tokens,
  SUM((attributes->'massgen.usage.output')::int) as total_output_tokens,
  SUM((attributes->'massgen.usage.cost')::float) as total_cost_usd
FROM records
WHERE trace_id = '[TRACE_ID]'
  AND span_name LIKE 'agent.%'
  AND attributes->>'massgen.usage.input' IS NOT NULL
GROUP BY attributes->>'massgen.agent_id'
```
