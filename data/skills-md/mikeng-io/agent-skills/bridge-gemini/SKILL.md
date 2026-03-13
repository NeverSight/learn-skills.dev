---
name: bridge-gemini
description: Reference adapter for Gemini CLI. Read by any orchestrating skill via the Read tool. Defines how to invoke Gemini CLI in non-interactive mode, timeout estimation, and fallback behavior. Usable by deep-council, deep-review, deep-audit, or any future skill that needs Gemini-based review.
location: managed
context: reference
dependencies:
  - bridge-commons
  - domain-registry
---

# Bridge: Gemini CLI Adapter

This file is a REFERENCE DOCUMENT. Any orchestrating skill reads it via the `Read` tool and embeds its instructions directly into Task agent prompts. It is not invoked as a standalone skill — it is a reusable set of instructions for Gemini CLI dispatch.

**Input schema, agent prompt template, output schema, verdict logic, timeout formula, artifact format, and status semantics are defined in `bridge-commons/SKILL.md`. This file covers only Gemini-specific connection detection and execution.**

## Bridge Identity

```yaml
bridge: gemini
model_family: google/gemini
availability: conditional
connection_preference:
  1: native-dispatch # Executor is Gemini CLI — Gemini subagents (enableAgents)
  2: cli # Any other executor — gemini -p
  3: skip # Neither — return SKIPPED (non-blocking)

native_dispatch:
  detection: ".gemini/settings.json has experimental.enableAgents: true AND running inside Gemini CLI"
  reliability: "MEDIUM — requires settings check + context awareness"
  subagent_types: [] # Gemini spawns subagents internally
```

---

## Pre-Flight — Connection Detection

**MUST read `bridge-commons/tool-discovery.md` first** to understand the discovery protocol.

### Step 1.0: Discover Execution Context

Before checking connection paths, discover what dispatch methods are available in the CURRENT execution context. This bridge runs inside multiple executors (Claude Code, OpenCode, Codex CLI, Gemini CLI, others).

**Primary detection: Tool availability + settings check** (most reliable)

```yaml
# Check if running INSIDE Gemini CLI (native dispatch)
gemini_native:
  signal: "running inside Gemini CLI AND enableAgents is true"
  check_1: "Am I running inside a Gemini CLI session?"
  check_2: "Is .gemini/settings.json or ~/.gemini/settings.json present with experimental.enableAgents: true?"
  reliability: MEDIUM (requires both context awareness AND settings)

# Environment signals (backup only, less reliable)
gemini_env:
  signal: "GEMINI_SESSION or similar context marker"
  reliability: LOW (may not exist)
```

**Discovery logic:**

```yaml
# Step 1: Check if running inside Gemini CLI
# Gemini CLI doesn't have a standard env var, so check tool access patterns
# If you're reading this from inside a Gemini subagent, you already have native dispatch

# Step 2: Check subagent enablement
native_dispatch_available:
  condition: "enableAgents: true in settings"
  check_project: "cat .gemini/settings.json 2>/dev/null"
  check_user: "cat ~/.gemini/settings.json 2>/dev/null"
  parse: "extract experimental.enableAgents, default false"
```

**If Gemini native dispatch is available**:

```json
{
  "executor_type": "gemini-cli",
  "native_dispatch": {
    "available": true,
    "tool_name": null,
    "subagent_types": [],
    "session_continuity": true
  },
  "recommended_dispatch": "native"
}
```

→ **Use native dispatch** (Subagent Mode section). This is the preferred path.

**If NOT running inside Gemini CLI or enableAgents is false**, proceed to Check A.

---

### Check A: CLI Installed?

```bash
which gemini
```

If found → proceed to Check B (Auth Probe).

If not found → return immediately:

```json
{
  "bridge": "gemini",
  "status": "SKIPPED",
  "skip_reason": "gemini CLI not available (which gemini returned empty)",
  "outputs": [],
  "verdict": null
}
```

Never fail or block — SKIPPED is a valid bridge outcome.

---

### Check B: Auth / Quota Probe

A gemini CLI that is installed but has an expired token or exhausted quota passes Check A and then fails silently at execution time. Catch this at availability check instead:

```bash
# Lightweight probe — verifies auth without a full execution
gemini --version 2>/dev/null
# Or: a minimal non-interactive list/ping command if available
```

If the probe exits non-zero or returns an auth error → return:

```json
{
  "bridge": "gemini",
  "status": "SKIPPED",
  "skip_reason": "gemini CLI auth probe failed: {stderr}",
  "outputs": [],
  "verdict": null
}
```

If the probe succeeds → **use CLI path** (Execution section).

---

## Execution

Build the prompt using the Agent Prompt Template from bridge-commons, adapting to `task_type`. Calculate timeout using bridge-commons formula (no bridge-specific multiplier for Gemini).

```bash
TIMEOUT={calculated_timeout}
PROMPT="{constructed_prompt}"
APPROVAL_MODE={resolved from capability_profile}

timeout $TIMEOUT gemini -p "$PROMPT" --approval-mode "$APPROVAL_MODE" --output-format json
```

Error handling:

- Exit code 0 with JSON → parse and return findings
- Exit code 124 (timeout) → return SKIPPED with reason `timeout_after_{n}s`
- Other exit codes → return SKIPPED with reason `gemini CLI error: {stderr}`
- Invalid JSON output → attempt to extract structured content, else SKIPPED

After execution, run the bridge-commons Post-Analysis Protocol. Gemini uses **stateless context passing** between rounds — embed the full previous-round outputs and context packet in each subsequent `gemini -p` call. There is no session continuity between separate CLI invocations.

For `standard` and `thorough` intensity, construct the Round 2 prompt as:

```
{Agent Prompt Template for this role}

--- ROUND 2 CONTEXT ---
Previous round findings:
{JSON of all Round 1 outputs}

{context packet: open_challenges directed at this domain, synthesis}
```

**Never block the calling orchestrator** — always return a report (even if SKIPPED).

---

## Subagent Mode

Gemini CLI supports custom subagents for parallel domain dispatch when `experimental.enableAgents` is set in `.gemini/settings.json`.

```bash
# Confirm subagents are enabled
cat .gemini/settings.json 2>/dev/null | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(d.get('experimental',{}).get('enableAgents', False))"
```

- If `true` → spawn one subagent per domain; run consolidation pass after all complete
- If `false` or missing → run standard single Gemini call covering all domains (valid fallback)

Subagent mode is a progressive enhancement. Record `subagent_mode: true/false` in output.

---

## Output

See bridge-commons Output Schema. Bridge-specific fields:

```json
{
  "bridge": "gemini",
  "capability_profile": "inspect | modify",
  "model_family": "google/gemini",
  "connection_used": "native-dispatch | cli",
  "subagent_mode": true
}
```

Output ID prefix: `G` (e.g., `G001`, `G002`).

---

## Notes

- Always check availability first — never assume gemini is installed
- Use non-interactive mode only; always specify `--approval-mode`
- Use `--output-format json` for structured parsing (not `-o json`)
- Timeout is estimated from scope, not hardcoded — see bridge-commons formula
- SKIPPED is a valid, non-error outcome

Resolve `APPROVAL_MODE` from bridge-commons:

- `inspect` profile → use Gemini's non-mutating approval mode
- `modify` profile → use Gemini's write-capable approval mode supported by the current runtime

Gemini approval settings are runtime details. The shared policy is `capability_profile`, derived from `task_type`.
