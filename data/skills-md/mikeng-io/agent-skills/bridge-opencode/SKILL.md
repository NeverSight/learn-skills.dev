---
name: bridge-opencode
description: Reference adapter for OpenCode — model-agnostic multi-provider bridge. Read by any orchestrating skill via the Read tool. Covers pre-flight checks with interactive advisory, HTTP API server path (preferred), CLI run path as fallback, correct flags and model format embedded. Usable by deep-council, deep-review, deep-audit, or any future skill that needs multi-model review.
location: managed
context: reference
dependencies:
  - bridge-commons
  - domain-registry
---

# Bridge: OpenCode Multi-Model Adapter

This file is a REFERENCE DOCUMENT. Any orchestrating skill reads it via the `Read` tool and embeds its instructions directly into Task agent prompts. It is not invoked as a standalone skill — it is a reusable set of instructions for OpenCode dispatch.

**Input schema, agent prompt template, output schema, verdict logic, artifact format, and status semantics are defined in `bridge-commons/SKILL.md`. This file covers OpenCode-specific connection detection, timeout multiplier, and execution paths.**

## Bridge Identity

```yaml
bridge: opencode
model_family: multi-provider # Routes to any configured AI provider
availability: conditional
connection_preference:
  1: native-dispatch # Executor is OpenCode — use task tool with subagent_type
  2: http-api # OpenCode server running at localhost:4096
  3: cli # Fallback — opencode run
  4: halt # None available — surface advisory, offer setup

native_dispatch:
  detection: "task tool (lowercase) is accessible with subagent_type parameter"
  reliability: "HIGH — actual capability check, not env var"
  subagent_types:
    ["explore", "general", "librarian", "oracle", "metis", "momus"]
```

## Why OpenCode?

OpenCode is provider-agnostic — it routes to whichever AI providers are configured (Anthropic, OpenAI, Google, GLM, Qwen, etc.). Running it as a bridge lets the calling skill get a second opinion from a different model family than the one currently executing the skill.

**Trade-off:** 1.5× timeout multiplier applies because model calls go through OpenCode's routing layer.

---

## Step 1: Pre-Flight — Connection Detection

**MUST read `bridge-commons/tool-discovery.md` first** to understand the discovery protocol.

### Step 1.0: Discover Execution Context

Before checking connection paths, discover what dispatch methods are available in the CURRENT execution context. This bridge runs inside multiple executors (Claude Code, OpenCode, Codex CLI, Gemini CLI, others).

**Primary detection: Tool availability** (most reliable)

```yaml
# Check if running INSIDE OpenCode (native dispatch)
opencode_native:
  signal: "task tool (lowercase) is accessible with subagent_type parameter"
  check: "Can invoke task() with subagent_type='explore' or 'general'"
  reliability: HIGH

# Environment variables (backup signals, less reliable)
opencode_env:
  signal: "OPENCODE_SESSION_ID or OPENCODE_CLIENT is set"
  check: "echo ${OPENCODE_SESSION_ID:-${OPENCODE_CLIENT:-}}"
  reliability: LOW (may not be set in all contexts)
```

**If OpenCode native dispatch is available**:

```json
{
  "executor_type": "opencode",
  "native_dispatch": {
    "available": true,
    "tool_name": "task",
    "subagent_types": [
      "explore",
      "general",
      "librarian",
      "oracle",
      "metis",
      "momus"
    ],
    "session_continuity": true
  },
  "recommended_dispatch": "native"
}
```

→ **Use native dispatch** (Step 3N). This is the preferred path.

**If NOT running inside OpenCode**, proceed to Check A.

---

### Check A: HTTP API Server Running?

```bash
curl -s --max-time 3 http://localhost:4096 -o /dev/null -w "%{http_code}"
# Also check custom port if OPENCODE_PORT env var is set
```

If responds (any HTTP code) → **use HTTP API path** (Step 3A). Server is already running.

---

### Check C: CLI Installed?

```bash
which opencode
```

If found → proceed to Check D.

If not found → **no connection available — go to Step 2 (Advisory)**.

---

### Check D: Provider Authenticated? (CLI path only)

```bash
opencode auth list
```

If output shows at least one authenticated provider → proceed to CLI path.

If no providers configured → **go to Step 2 (Advisory)** with `reason: no_provider_configured`.

---

## Step 2: Advisory — Halt and Present Options

**Do not skip silently.** Surface the appropriate message and wait for a choice.

### Advisory: Not Installed

```
⚠ OpenCode is not installed or not in PATH.

Options:
  [1] Install OpenCode
      npm install -g opencode-ai
      # or: brew install opencode

  [2] Start the OpenCode server (if already installed elsewhere)
      opencode serve --port 4096
      Then re-run this review.

  [3] Skip OpenCode bridge
      Continue without OpenCode. Other available bridges will run.

  [4] Abort the entire review

What would you like to do? (1/2/3/4)
```

Return `status: HALTED`, `halt_reason: cli_not_found`.

---

### Advisory: No Provider Configured

```
⚠ OpenCode is installed but no AI provider is authenticated.

Configure a provider:
  opencode auth login    # Select and authenticate a provider

Alternatively:
  [1] Skip OpenCode bridge
  [2] Abort the entire review
```

Return `status: HALTED`, `halt_reason: no_provider_configured`.

---

### Non-Interactive Environments

Return `status: HALTED` with the full advisory in `halt_message`. Never silently skip.

---

## Step 3: Read Multi-Model Configuration

Before estimating timeout, check bridge settings for a `models` array. This is a **suite-owned config file** — separate from OpenCode's own `~/.config/opencode/` config — that tells the bridge which models to use for multi-model dispatch.

```bash
cat .bridge-settings.json 2>/dev/null
```

Extract `bridges.opencode.models`:

```yaml
multi_model_dispatch:
  condition: "bridges.opencode.models is present AND has 2+ entries"
  action: "Spawn one execution per model — treat each as an independent participant"
  example_config:
    models: ["glm/glm-4-7", "kimi/moonshot-v1-8k", "qwen/qwen-plus"]

single_model_dispatch:
  condition: "models missing OR empty OR has exactly 1 entry"
  action: "Single execution using configured model or OpenCode's default"
```

**Why multi-model matters:** Each model has different training data, biases, and reasoning patterns. With 3 models configured, bridge-opencode becomes its own mini-council — 3 independent perspectives before findings even reach the cross-bridge synthesis layer.

---

## Timeout Estimation

Use bridge-commons base timeout table and intensity multiplier, then apply the OpenCode-specific multiplier:

```yaml
opencode_multiplier: 1.5   # Always applied — provider routing overhead

# Single-model dispatch:
final_timeout: base_timeout × intensity_multiplier × 1.5

# Multi-model dispatch (models run in parallel, not sequential):
final_timeout: max(per_model_base_timeout) × intensity_multiplier × 1.5
# NOT the sum — all model invocations run simultaneously
```

OpenCode internally dispatches to one or more providers — each provider call adds latency.

---

## Step 3: Dispatch — Single-Model vs Multi-Model

### Multi-Model Dispatch (when `models` has 2+ entries)

Spawn one parallel execution per configured model. All models receive the identical `bridge_input` — independence is the point.

**Via HTTP API (preferred when server running):**

```bash
# For each model in bridge_settings.opencode.models, in parallel:
SESSION_A=$(curl -s -X POST http://localhost:4096/session \
  -H "Content-Type: application/json" \
  -d '{"title": "opencode-{model_slug}-{session_id}"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

curl -s -X POST http://localhost:4096/session/$SESSION_A/message \
  -H "Content-Type: application/json" \
  -d '{
    "content": [{"type": "text", "text": "{constructed_prompt}"}],
    "model": "{model_A}"   # e.g., "glm/glm-4-7"
  }' &

SESSION_B=... # similarly for model B
SESSION_C=... # similarly for model C

wait  # collect all
```

**Via CLI (fallback):**

```bash
# Run in parallel — one per model
timeout {final_timeout} opencode run "{constructed_prompt}" --model {model_A} &
PID_A=$!
timeout {final_timeout} opencode run "{constructed_prompt}" --model {model_B} &
PID_B=$!
timeout {final_timeout} opencode run "{constructed_prompt}" --model {model_C} &
PID_C=$!
wait $PID_A $PID_B $PID_C
```

If any model invocation times out or errors → mark it as `skipped` in `instances_completed` and continue with remaining results. Never block on a single model failure.

**Post-dispatch: Mini-Synthesis within bridge-opencode**

After all model invocations complete, run a mini-synthesis before returning to deep-council:

1. **Deduplication**: Findings with >70% description overlap across models → merge (inherit highest severity, list contributing models as `confirmed_by_models`)
2. **Model-confirmed**: Merged findings are elevated (`intra-bridge_multi_model_confirmed: true`)
3. **Single-model findings**: Retained with model attribution
4. **Verdict**: Apply bridge-commons verdict logic to the merged finding set

This mini-synthesis is the intra-bridge equivalent of deep-council's cross-bridge Stage B — but lighter (no full DA challenge round, just deduplication and model-agreement detection).

---

### Single-Model Dispatch (when `models` is empty/missing or has 1 entry)

Proceed to Step 3A or 3B with the single configured model (or OpenCode's default if none specified).

---

## Step 3N: Execute via Native Dispatch (Preferred)

**Use this path when running INSIDE OpenCode** and the `task` tool is accessible.

This is the preferred dispatch path because:

- No subprocess overhead (direct agent invocation)
- Session continuity maintained automatically
- Can spawn parallel subagents for multi-domain review
- Lower latency than HTTP API or CLI

### Single-Domain Dispatch

For single-domain or single-model review, invoke the appropriate subagent:

```yaml
# For exploration/analysis tasks
invoke: task(
  subagent_type: "explore",
  description: "{review_id}-domain-review",
  prompt: "{constructed_prompt from bridge-commons Agent Prompt Template}"
)

# For general-purpose review
invoke: task(
  subagent_type: "general",
  description: "{review_id}-review",
  prompt: "{constructed_prompt}"
)

# For research-backed review
invoke: task(
  subagent_type: "librarian",
  description: "{review_id}-research-review",
  prompt: "{constructed_prompt} + research context from external sources"
)
```

### Multi-Domain Parallel Dispatch

When `bridge_input.domains` has 2+ domains, spawn one subagent per domain in parallel:

```yaml
# Spawn parallel subagents — one per domain
domain_experts: [
  task(subagent_type: "general", prompt: "{domain_1_prompt}"),
  task(subagent_type: "general", prompt: "{domain_2_prompt}"),
  task(subagent_type: "general", prompt: "{domain_3_prompt}"),
]

# After all complete, aggregate outputs
aggregated_findings: collect all outputs
verdict: apply bridge-commons verdict logic
```

### Multi-Model Parallel Dispatch

When `.bridge-settings.json` has `bridges.opencode.models` with 2+ entries, spawn one subagent per model:

```yaml
# Each subagent uses a different model
model_sessions: [
  task(subagent_type: "general", model: "glm/glm-4-7", prompt: "{prompt}"),
  task(subagent_type: "general", model: "kimi/moonshot-v1-8k", prompt: "{prompt}"),
  task(subagent_type: "general", model: "qwen/qwen-plus", prompt: "{prompt}"),
]

# After all complete, run mini-synthesis
deduplication: merge findings with >70% overlap
intra_bridge_confirmed: findings agreed by 2+ models
```

### Post-Analysis Protocol via Native Dispatch

For `standard` and `thorough` intensity, the post-analysis protocol runs within OpenCode:

**Round 2 (Challenge Round)**:

```yaml
# Spawn Challenger subagent
challenger: task(
  subagent_type: "general",
  prompt: "{Devil's Advocate prompt from bridge-commons Post-Analysis Protocol}"
)

# Spawn Integration Checker subagent
integration_checker: task(
  subagent_type: "general",
  prompt: "{Integration Checker prompt from bridge-commons}"
)
```

**Session continuity**: The calling orchestrator (deep-council or other) maintains state between rounds and injects context packets.

### Output from Native Dispatch

Return the standard bridge-commons output schema with:

```json
{
  "bridge": "opencode",
  "connection_used": "native-dispatch",
  "model_family": "multi-provider",
  "dispatch_mode": "multi-domain | multi-model | single",
  "models_used": ["glm/glm-4-7", ...],
  "native_executor": "opencode"
}
```

---

## Step 3A: Execute via HTTP API (Secondary)

The OpenCode HTTP server exposes a REST API. Use it when the server is already running.

OpenAPI spec available at: `http://localhost:{port}/doc`

### Create a session and send a message

```bash
# Create session
SESSION=$(curl -s -X POST http://localhost:4096/session \
  -H "Content-Type: application/json" \
  -d '{"title": "bridge-review-{review_id}"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Send prompt — use bridge-commons Agent Prompt Template for the constructed_prompt
curl -s -X POST http://localhost:4096/session/$SESSION/message \
  -H "Content-Type: application/json" \
  -d '{
    "content": [{"type": "text", "text": "{constructed_prompt}"}],
    "model": "{provider/model}"
  }'
```

For the bridge-commons Post-Analysis Protocol, use the same session for each round — the HTTP session maintains full conversation history, so Round 2+ only needs the context packet injected. Run each role as a separate message (or separate session per role for parallelism):

```bash
# Round 2 message — session already has Round 1 history
curl -s -X POST http://localhost:4096/session/$SESSION/message \
  -H "Content-Type: application/json" \
  -d '{
    "content": [{"type": "text", "text": "{role-specific Round N prompt from bridge-commons context packet}"}]
  }'
```

For true parallel role execution within a round, create one session per role — embed the previous-round outputs explicitly since sessions don't share state:

```bash
# Parallel round execution — one session per role, context embedded in each
CHALLENGER_SESSION=$(curl -s -X POST http://localhost:4096/session \
  -H "Content-Type: application/json" \
  -d '{"title": "challenger-round-2-{session_id}"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
# ... then send challenger Round 2 prompt with embedded context
```

### Model format

Models must use `provider/model` format:

```yaml
model_format: "provider/model"
examples:
  - "anthropic/claude-sonnet-4-20250514"
  - "openai/gpt-4o"
  - "google/gemini-2.0-flash"
  - "glm/glm-4-flash" # If GLM configured
  - "qwen/qwen-plus" # If Qwen configured

selection_strategy:
  - Use default model if no preference (omit model field)
  - Or pass the model configured in the caller's context
```

### Authentication (if server has password)

```bash
# With auth: -u opencode:$OPENCODE_SERVER_PASSWORD
curl -s -u opencode:$OPENCODE_SERVER_PASSWORD \
  -X POST http://localhost:4096/session/...
```

### Agent selection (optional)

```bash
# Resolve the agent from bridge-commons capability_profile
curl -s -X POST http://localhost:4096/session \
  -H "Content-Type: application/json" \
  -d '{"title": "...", "agent": "{resolved from capability_profile}"}'
```

Built-in agents:

- `plan` — inspect-oriented agent
- `build` — modify-oriented agent

Resolve the agent from bridge-commons:

- `inspect` profile → select the analysis-oriented agent
- `modify` profile → select the write-capable agent

---

## Step 3B: Execute via CLI (Fallback)

Build the prompt using the bridge-commons Agent Prompt Template.

```bash
timeout {final_timeout} opencode run "{constructed_prompt}" \
  --format json \
  --model {provider/model} \
  {resolved runtime capability args}
```

**Important:** `opencode` (bare) opens the interactive TUI. Always use `opencode run "..."` for programmatic use.

For the Post-Analysis Protocol via CLI, use separate `opencode run` calls per round — no session continuity. Embed the full previous-round outputs and context packet in each Round N prompt (stateless context passing, same pattern as Gemini CLI).

### CLI Error Handling

| Exit code | Meaning   | Action                                            |
| --------- | --------- | ------------------------------------------------- |
| 0         | Success   | Parse JSON event stream for final message         |
| 124       | Timeout   | Return SKIPPED, `skip_reason: timeout_after_{n}s` |
| Other     | CLI error | Capture stderr, return SKIPPED with detail        |

---

## Output

See bridge-commons Output Schema. Bridge-specific fields:

```json
{
  "bridge": "opencode",
  "capability_profile": "inspect | modify",
  "model_family": "multi-provider",
  "connection_used": "native-dispatch | http-api | cli",
  "dispatch_mode": "multi-model | single-model",
  "models_configured": ["glm/glm-4-7", "kimi/moonshot-v1-8k", "qwen/qwen-plus"],
  "models_used": ["glm/glm-4-7", "kimi/moonshot-v1-8k"],
  "instances_spawned": 3,
  "instances_completed": 2,
  "intra_bridge_confirmed": 4
}
```

- `models_configured`: full list from `.bridge-settings.json`
- `models_used`: models that successfully completed (subset if any timed out)
- `instances_spawned`: number of parallel executions launched
- `instances_completed`: number that returned results (may be less than spawned)
- `intra_bridge_confirmed`: count of findings confirmed by 2+ models within this bridge (before cross-bridge synthesis)

Output ID prefix: `O` (e.g., `O001`, `O002`). In multi-model mode, prefix per model: `O-glm-001`, `O-kimi-001`, etc. Merged findings use: `O-merged-001`.

---

## Notes

- **HTTP API is preferred** — use it when `opencode serve` is already running (lower overhead, session continuity)
- **`opencode run` ≠ `opencode`** — bare `opencode` opens the interactive TUI; always use `opencode run "..."` for scripted use
- **Model format is `provider/model`** — e.g., `anthropic/claude-sonnet-4-20250514`, not just `claude`
- **Capability resolution is shared** — map `inspect | modify` from bridge-commons onto the appropriate OpenCode agent or CLI args at runtime
- **1.5× timeout multiplier** always applies (provider routing overhead)
- **HALTED ≠ SKIPPED** — HALTED requires user input before the review can proceed
