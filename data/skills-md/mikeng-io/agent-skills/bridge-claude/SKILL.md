---
name: bridge-claude
description: Reference adapter for Claude (Anthropic) dispatch. Read by any orchestrating skill via the Read tool. Defines how to invoke Claude sub-agents or the Anthropic API, with availability checks. Usable by any AI orchestrator — Claude Code, OpenCode, Codex, Gemini, or custom agents.
location: managed
context: reference
dependencies:
  - bridge-commons
  - domain-registry
  - debate-protocol
---

# Bridge: Claude (Anthropic) Adapter

This file is a REFERENCE DOCUMENT. Any orchestrating skill reads it via the `Read` tool and embeds its instructions directly into Task agent prompts. It is not invoked as a standalone skill — it is a reusable set of instructions for Anthropic model dispatch.

**Input schema, agent prompt template, output schema, verdict logic, timeout formula, artifact format, and status semantics are defined in `bridge-commons/SKILL.md`. This file covers only Claude-specific connection detection and execution paths.**

## Bridge Identity

```yaml
bridge: claude
model_family: anthropic/claude
availability: conditional # Depends on executor — not always available
connection_preference:
  1: native-dispatch # Executor is Claude Code — Task tool / Agent Teams
  2: cli # Any other executor — invoke `claude -p` CLI
  3: api # Last resort — Anthropic HTTP API via ANTHROPIC_API_KEY
  4: skip # None available — return SKIPPED (non-blocking)

native_dispatch:
  detection: "Task tool is accessible with subagent_type parameter"
  reliability: "HIGH — actual capability check, not env var"
  subagent_types: ["explore", "librarian", "oracle", "metis", "momus"]
```

---

## Step 1: Pre-Flight — Connection Detection

**MUST read `bridge-commons/tool-discovery.md` first** to understand the discovery protocol.

### Step 1.0: Discover Execution Context

Before checking connection paths, discover what dispatch methods are available in the CURRENT execution context. This bridge runs inside multiple executors (Claude Code, OpenCode, Codex CLI, Gemini CLI, others).

**Primary detection: Tool availability** (most reliable)

```yaml
# Check if running INSIDE Claude Code (native dispatch)
claude_native:
  signal: "Task tool (uppercase) is accessible with subagent_type parameter"
  check: "Can invoke Task() with subagent_type='explore' or 'oracle'"
  reliability: HIGH

# Environment variables (backup signals, less reliable)
claude_env:
  signal: "CLAUDE_CODE_SESSION is set"
  check: "echo ${CLAUDE_CODE_SESSION:-}"
  reliability: LOW (may not be set in all contexts)
```

**Discovery logic:**

```yaml
# Step 1: Check if Task tool is accessible
# If you're reading this from inside a Claude Code session, you have access to Task tool
# The key signal is: can you invoke Task with subagent_type parameter?

# Step 2: Determine native dispatch type
native_dispatch_type:
  agent_teams:
    condition: "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 AND (domains >= 3 OR intensity = thorough)"
    description: "Teammates share a task list and communicate directly"

  task_tool:
    condition: "Default — always available as fallback"
    description: "Sub-agents report results to parent only"
```

**If Claude native dispatch is available**:

```json
{
  "executor_type": "claude-code",
  "native_dispatch": {
    "available": true,
    "tool_name": "Task",
    "subagent_types": ["explore", "librarian", "oracle", "metis", "momus"],
    "session_continuity": true
  },
  "recommended_dispatch": "native"
}
```

→ **Use native-dispatch path** (Steps 3A + 3B). This is the preferred path.

**If NOT running inside Claude Code**, proceed to Check A.

---

### Check A: Claude Code CLI Installed?

```bash
which claude
```

If found → **use CLI path** (Step 3C). Any external executor (OpenCode, Codex, Gemini, custom agents) can invoke `claude -p` to get Claude's analysis without API keys.

If not found → proceed to Check B.

---

### Check B: Anthropic API Accessible?

```bash
echo ${ANTHROPIC_API_KEY:+found}
```

If `ANTHROPIC_API_KEY` is set → **use API path** (Step 3D).

---

### Neither available → SKIPPED

```json
{
  "bridge": "claude",
  "status": "SKIPPED",
  "skip_reason": "No Anthropic access — Task tool unavailable, claude CLI not found, ANTHROPIC_API_KEY not set",
  "outputs": []
}
```

Claude bridge is non-blocking when unavailable. SKIPPED is a valid outcome.

---

## Step 2: Select Dispatch Mode

Claude bridge has two native-dispatch modes. Select based on task complexity and environment:

```yaml
dispatch_mode:
  agent_teams:
    condition: "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 AND (domains >= 3 OR intensity = thorough)"
    description: "Teammates share a task list and communicate directly — best for complex multi-domain work"
    preferred: true
    caveat:
      "Env var is necessary but not sufficient — TeamCreate may still fail if this bridge
      is executing as a nested sub-agent (Task → Task). Always guard with a fallback."

  task_tool:
    condition: "Default — always available as fallback"
    description: "Sub-agents report results to parent — best for focused, independent tasks"
    preferred: false
```

**Agent Teams vs Task Tool:**

|               | Task Tool                        | Agent Teams                                      |
| ------------- | -------------------------------- | ------------------------------------------------ |
| Communication | Sub-agents report to parent only | Teammates message each other directly            |
| Coordination  | Parent manages all               | Shared task list, self-coordinating              |
| Best for      | Quick focused tasks              | Multi-domain debate, complex analysis            |
| Availability  | Always                           | Requires env var AND top-level execution context |

**Depth note:** Claude sub-agents can spawn their own Task sub-agents (Task → Task works). Agent Teams (`TeamCreate`) in a nested sub-agent is not guaranteed — the experimental feature may not be available at depth 2+. If this bridge is already running inside a Task agent dispatched by deep-council or another orchestrator, attempt Agent Teams but be prepared to fall back.

---

## Step 3A: Execute via Agent Teams (preferred for complex tasks)

When `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set and task complexity warrants it (3+ domains or thorough intensity), attempt Agent Teams. Teammates share a task list and can message each other directly — enabling real-time debate between domain experts.

### Failure guard — attempt before committing

Before executing the full flow, attempt `TeamCreate`. If it fails for any reason (not available in this execution context, naming collision, experimental feature restricted at current depth) → **immediately fall back to Step 3B**. Do not retry Agent Teams.

```
0. ATTEMPT TeamCreate → "bridge-claude-{session_id}"
   IF TeamCreate fails → go to Step 3B (Task Tool fallback)

1. TeamCreate succeeded → continue
2. Spawn teammates:
   - One per domain from bridge_input.domains
   - Devil's Advocate (always)
   - Integration Checker (always)
3. Create tasks in shared task list — one per teammate
4. Teammates self-coordinate: domain experts complete their analysis,
   Devil's Advocate challenges findings via direct messages,
   Integration Checker surfaces cross-component issues
5. Wait for all tasks complete
6. Synthesize via TaskList
7. TeamDelete → clean up
   IF any step 2–6 fails → call TeamDelete before returning SKIPPED
```

Teammates communicate findings and challenges directly without routing through the parent. This replaces the bridge-commons consolidation pass — debate-protocol provides a richer version.

### Teammate prompts

**Domain expert:**

```
You are a {expert_role}. Your task: {task_description}
Scope: {scope} | Context: {context_summary} | Intensity: {intensity}
Focus: {focus_areas from domain-registry}
Return your output as the JSON structure defined in bridge-commons Agent Prompt Template.
```

**Devil's Advocate:**

```
You are a Devil's Advocate for this analysis session.
Scope: {scope} | Context: {context_summary} | Intensity: {intensity}

Your obligations (read debate-protocol/experts/devils-advocate.md for full protocol):
- MUST challenge every CRITICAL and HIGH finding not originated by you, via direct teammate messages
- SHOULD challenge MEDIUM findings when you detect a pattern across multiple findings
- Cross-domain synthesis: actively look for findings whose combination implies a new, higher-severity issue not caught by any single domain expert
- Pre-mortem focus: for each component in scope, ask "what would cause this to fail in production?"

Challenge quality standard: a valid challenge must either (a) identify a missing assumption, (b) propose an alternative explanation that lowers severity, or (c) surface a scenario where the finding does not apply.

Message domain expert teammates directly to challenge their findings. Do not wait for them to send to you first.

Return outputs JSON with domain: "cross-domain". Include both challenge outcomes (findings you successfully challenged/withdrew) and new findings you discovered.
```

**Integration Checker:**

```
You are an Integration Checker for this analysis session.
Scope: {scope} | Context: {context_summary} | Intensity: {intensity}

Focus areas (read debate-protocol/experts/integration-checker.md for full protocol):
- Interface mismatches: where does component A assume something about component B that isn't guaranteed?
- Undocumented contracts: implicit dependencies that work by accident, not by design
- Error propagation gaps: errors that one component produces but callers don't handle
- Timing and ordering dependencies: race conditions, initialization ordering, cascading failures
- Cross-cutting assumptions: things that must be true globally but are only enforced locally

For each finding from domain experts: does it have cross-component implications beyond its stated scope?
If yes, surface those as integration findings even if the original finding is withdrawn.

Return outputs JSON with domain: "integration".
```

---

## Step 3B: Execute via Task Tool (fallback)

When Agent Teams is not available, spawn parallel Task sub-agents — one per domain + Devil's Advocate + Integration Checker. Sub-agents report results to parent only (no direct inter-agent communication). Build prompts using the Agent Prompt Template from bridge-commons.

```
Task 1: {domain_1} expert — focus: {focus_areas}, scope: {scope}
Task 2: {domain_2} expert — focus: {focus_areas}, scope: {scope}
...
Task N:   Devil's Advocate — challenge assumptions, find failure modes (domain: "cross-domain")
Task N+1: Integration Checker — cross-component impacts, implicit contracts (domain: "integration")
```

All tasks run in parallel. After all complete, run the bridge-commons Post-Analysis Protocol. For subsequent rounds, spawn new Task sub-agents with the context packet embedded in their prompts — the parent agent holds all state between rounds and manages the orchestrator synthesis step.

---

## Step 3C: Execute via CLI (external executors)

When any non-Claude-Code executor can call the `claude` CLI:

```bash
CAPABILITY_FLAGS={resolved from bridge-commons capability_profile}

timeout {final_timeout} claude -p "{constructed_prompt}" \
  --output-format json \
  $CAPABILITY_FLAGS
```

**Key flags:**

| Flag                          | Purpose                                              |
| ----------------------------- | ---------------------------------------------------- |
| `-p "prompt"`                 | Prompt string — non-interactive mode                 |
| `--output-format json`        | Structured JSON output for parsing                   |
| `--output-format stream-json` | Streaming JSON for real-time processing              |
| `CAPABILITY_FLAGS`            | Resolved runtime controls for `inspect` or `modify`  |
| `--continue`                  | Resume the most recent session                       |

Resolve `CAPABILITY_FLAGS` from bridge-commons:

- `inspect` profile → constrain Claude to non-mutating tools only
- `modify` profile → enable non-interactive writes so implementation tasks do not block on approvals

The bridge policy is the shared `capability_profile`, not a fixed Claude flag set. Claude-specific permission flags are only the runtime-level translation of that profile.

---

## Step 3D: Execute via Anthropic API (last resort)

```bash
# Discover latest model first — do not hardcode
CLAUDE_MODEL=$(curl -s -H "x-api-key: $ANTHROPIC_API_KEY" \
  https://api.anthropic.com/v1/models | python3 -c \
  "import sys,json; models=json.load(sys.stdin)['data']; print(models[0]['id'])")

curl -s -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$CLAUDE_MODEL\",
    \"max_tokens\": 8096,
    \"messages\": [{\"role\": \"user\", \"content\": \"{constructed_prompt}\"}]
  }"
```

Single API call covers all domains in one prompt. Less parallelism than native-dispatch paths.

---

## Output

See bridge-commons Output Schema. Bridge-specific fields:

```json
{
  "bridge": "claude",
  "capability_profile": "inspect | modify",
  "model_family": "anthropic/claude",
  "connection_used": "native-dispatch | cli | api",
  "agents_spawned": 4
}
```

Output ID prefix: `C` (e.g., `C001`, `C002`).

---

## Notes

- **Not always available** — check Task tool access or `ANTHROPIC_API_KEY` before using
- **SKIPPED is non-blocking** — if unavailable, other bridges continue
- **native-dispatch is preferred** — richer parallel dispatch when running in Claude Code
- **Agent Teams replaces consolidation pass** — when available, debate-protocol runs instead
- **Agent Teams guard is mandatory** — `TeamCreate` can fail even when the env var is set (nested sub-agent context, depth limit, naming collision); always fall back to Task Tool on failure
- **Sub-agent recursion depth** — Task → Task works reliably; Agent Teams inside a Task agent (Task → TeamCreate) is experimental and context-dependent; do not assume it's available at depth 2+
- **TeamDelete on failure** — if any step between TeamCreate and synthesis fails, call TeamDelete before returning SKIPPED to avoid orphaned teams
- **API path works from any executor** — fallback for non-Claude orchestrators
- **Task type drives framing** — the same bridge handles review, planning, research, etc.
