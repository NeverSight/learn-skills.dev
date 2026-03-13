---
name: bridge-codex
description: Reference adapter for Codex multi-agent review. Read by any orchestrating skill via the Read tool. MCP server path (preferred) with auto-setup option, CLI path as fallback, interactive pre-flight advisory when not configured, correct flags embedded. Usable by deep-council, deep-review, deep-audit, or any future skill that needs Codex-based review.
location: managed
context: reference
dependencies:
  - bridge-commons
  - domain-registry
---

# Bridge: Codex Multi-Agent Adapter

This file is a REFERENCE DOCUMENT. Any orchestrating skill reads it via the `Read` tool and embeds its instructions directly into Task agent prompts. It is not invoked as a standalone skill — it is a reusable set of instructions for Codex review dispatch via MCP server or CLI.

**Input schema, output schema, verdict logic, artifact format, and status semantics are defined in `bridge-commons/SKILL.md`. This file covers Codex-specific connection detection, reasoning level, prompt adaptation, and execution.**

## Bridge Identity

```yaml
bridge: codex
model_family: openai/codex
availability: conditional
connection_preference:
  1: native-dispatch # Executor is Codex — use internal multi-agent capability
  2: mcp # Any executor with MCP access — mcp__codex__codex server
  3: cli # Fallback — codex exec
  4: halt # None available — surface advisory, offer setup

native_dispatch:
  detection: "CODEX_SESSION_ID set AND codex features list shows multi_agent enabled"
  reliability: "MEDIUM — env var check + feature verification"
  multi_agent: true # Codex can spawn parallel domain experts internally
```

---

## Step 1: Pre-Flight — Connection Detection

**MUST read `bridge-commons/tool-discovery.md` first** to understand the discovery protocol.

### Step 1.0: Discover Execution Context

Before checking connection paths, discover what dispatch methods are available in the CURRENT execution context.

**Primary detection: Native Codex execution**

```yaml
codex_native:
  signal_1: "CODEX_SESSION_ID environment variable is set"
  signal_2: "codex features list shows multi_agent enabled"
  check: |
    if [ -n "$CODEX_SESSION_ID" ]; then
      codex features list 2>/dev/null | grep -q "multi_agent.*enabled"
    fi
  reliability: MEDIUM (requires both env var AND feature check)

mcp_available:
  signal: "mcp__codex__codex tool is accessible"
  check: "Attempt to list MCP tools or check .mcp.json for codex server"
  reliability: HIGH (actual tool availability)
```

**If running INSIDE Codex with multi-agent enabled**:

```json
{
  "executor_type": "codex",
  "native_dispatch": {
    "available": true,
    "multi_agent": true,
    "session_continuity": true
  },
  "mcp_tools": {
    "available": false
  },
  "recommended_dispatch": "native"
}
```

→ **Use native dispatch** (Step 3N). This allows Codex to spawn parallel domain experts internally.

**If NOT running inside Codex**, proceed to Check A.

---

### Check A: Native Dispatch?

If the executor is Codex CLI with multi-agent support enabled, this is the preferred path — spawn parallel Codex agents rather than routing through MCP or CLI.

```bash
# Check if running inside a Codex execution context
echo ${CODEX_SESSION_ID:+found}

# Check if multi-agent feature is enabled
codex features list 2>/dev/null | grep -q "multi_agent" && echo "enabled"
```

If in a Codex session AND multi-agent is enabled → **use native dispatch** (Step 3N).

This is an experimental feature. If multi-agent is not enabled, or the executor is not Codex → proceed to Check B.

---

### Check B: MCP Server Configured?

Look for a `codex` entry in the active MCP configuration:

```bash
# Check project-level MCP config
cat .mcp.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('found' if 'codex' in d.get('mcpServers',{}) else 'not-found')" 2>/dev/null

# Or check Claude's global MCP settings
cat ~/.claude.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('found' if 'codex' in str(d) else 'not-found')" 2>/dev/null
```

If found → **use MCP path** (Step 3A). No further pre-flight needed — MCP server handles auth internally.

---

### Check C: CLI Available?

```bash
which codex
```

If found → proceed to Check D.

If not found → **no connection available — go to Step 2 (Advisory)**.

---

### Check D: Authenticated? (CLI path only)

```bash
codex login status
```

Exit code 0 → authenticated. Other → **go to Step 2 (Advisory)** with `reason: not_authenticated`.

---

### Check E: Multi-Agent Feature Enabled? (CLI path only — optional)

```bash
codex features list
```

Look for `multi_agent` marked as enabled.

- If enabled → proceed with **parallel multi-agent dispatch** (one sub-agent per domain)
- If not enabled → proceed in **single-agent mode** (one Codex session reviews all domains together)

Multi-agent is a progressive enhancement. Single-agent mode is a valid fallback — do not halt.

Record `multi_agent_enabled: true/false` in output for caller transparency.

→ **Use CLI path** (Step 3B).

---

## Step 2: Advisory — Halt and Present Options

**Do not skip silently.** Surface the appropriate message to the user and wait for a choice.

### Advisory: MCP Server Not Configured + CLI Not Found

```
⚠ Codex is not connected. This bridge requires either the Codex MCP server
  or the Codex CLI.

Options:
  [1] Set up MCP server automatically
      I will add the Codex MCP server to .mcp.json so future sessions
      use it without any CLI installation needed.
      Requires: Node.js 18+ and npx available.

  [2] Install the Codex CLI
      Run: npm install -g @openai/codex
      Then re-run this review.

  [3] Skip Codex bridge
      Continue the review without Codex. Other available bridges will run.

  [4] Abort
      Stop the entire review.

What would you like to do? (1/2/3/4)
```

**If user chooses [1] — Auto-setup MCP server:**

Write (or merge) into `.mcp.json`:

```json
{
  "mcpServers": {
    "codex": {
      "command": "npx",
      "args": ["-y", "codex", "mcp-server"]
    }
  }
}
```

Then verify the server is reachable. If successful → continue with **MCP path (Step 3A)**.
If verification fails → tell the user and offer options [2]/[3]/[4] again.

**If user chooses [2]:** Return `status: HALTED`, `halt_reason: cli_not_installed`. Show install command.

**If user chooses [3]:** Return `status: SKIPPED`, `skip_reason: user_chose_skip`.

**If user chooses [4]:** Return `status: ABORTED`. Calling orchestrator must stop entire review.

---

### Advisory: CLI Found But Not Authenticated

```
⚠ Codex CLI found but not authenticated.

To log in:
  codex login              # Browser OAuth flow (interactive)
  codex login --device-auth   # Device code flow (headless/CI)

After authenticating, re-run this review.

Or:
  [1] Skip Codex bridge and continue
  [2] Abort the entire review
```

Return `status: HALTED`, `halt_reason: not_authenticated`.

---

### Non-Interactive Environments (Automated Pipelines)

If no interactive context is available, return `status: HALTED` with the full advisory text in `halt_message`. Never silently skip in a way that hides a configuration gap.

---

## Reasoning Level Selection

Evaluate the review context and select the Codex reasoning level **before** building the prompt. This applies to both MCP and CLI paths.

### Decision Signals

| Signal                                                                                 | Reasoning Level |
| -------------------------------------------------------------------------------------- | --------------- |
| Security audit, cryptographic review, financial compliance                             | `xhigh`         |
| Multi-component architecture, 3+ CRITICAL findings expected, complex dependency chains | `high`          |
| Standard code review, single-domain analysis, routine audit                            | `medium`        |

**Evaluate in this order:**

1. If request explicitly mentions "critical", "security", "cryptographic", "financial", "compliance" → `xhigh`
2. If scope covers 20+ files OR 3+ domains with HIGH risk signals → `high`
3. Otherwise → `medium`

### Xhigh Alert (MANDATORY)

When `xhigh` is selected, **alert the user before proceeding**:

```
⚠ Reasoning level: XHIGH
Codex will use maximum reasoning depth for this review.
This increases token usage and may take 2–3× longer than standard.

Continue? (y/n)
```

If user declines → fall back to `high`. Return `reasoning_level: "high"` in output.

### Embedding Reasoning Level

**MCP path (Step 3A):** pass as `reasoning` parameter
**CLI path (Step 3B):** pass as `--config reasoning-effort={level}` (config override)

Store selected level in `reasoning_level` output field.

---

## Step 3: Build Domain Prompt

Codex's multi-agent capability means the prompt is addressed to a **coordinator**, not a single domain expert. This differs from the bridge-commons Agent Prompt Template (which addresses one expert per call). Adapt as follows:

```
You are a multi-agent code review coordinator. Spawn one agent per domain
below, run them in parallel using your multi-agent capability, wait for all
to complete, then return a consolidated findings JSON.

Review scope: {review_scope}
Context: {context_summary}
Intensity: {intensity}

Domains to analyze (spawn one agent per domain):
{for each domain:
  "- {domain_name}: focus on {focus_areas from domain-registry}"}

Each agent must return outputs using the schema from bridge-commons:
{
  "domain": "...",
  "outputs": [
    {
      "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO",
      "title": "...",
      "description": "...",
      "evidence": "...",
      "action": "..."
    }
  ]
}

After all agents complete, consolidate all findings and return:
{
  "domains_analyzed": [...],
  "outputs": [...],
  "verdict": "PASS | FAIL | CONCERNS"
}
```

In single-agent mode, drop the coordinator framing and use the bridge-commons Agent Prompt Template directly, covering all domains in one prompt.

---

## Timeout Estimation

Use bridge-commons base timeout table and intensity multiplier. Codex multi-agent adds sub-agent spawn overhead — apply a higher base when multi-agent is enabled:

```yaml
# When multi_agent_enabled: true — increase base by 50%
# e.g., 5-20 files: 180s → 270s to account for agent spawn latency
# When multi_agent_enabled: false — use bridge-commons base times directly
```

No separate bridge multiplier otherwise.

---

## Step 3A: Execute via MCP Server (Preferred)

Use the `codex` MCP tool directly. The MCP server runs `codex mcp-server` and exposes two tools:

### Model Selection — Check Latest at Runtime

Before calling either MCP or CLI, determine the current latest Codex model:

```bash
# Via CLI — lists available models
codex prompt --models 2>/dev/null | head -5

# If unavailable, omit model field to use server default
```

Do NOT hardcode a model name. If model discovery fails, omit the `model` parameter and let the server select its default.

### Tool: `codex` — Start a session

```
Call: mcp__codex__codex
Parameters:
  prompt:          {constructed_prompt}
  approval-policy: "never"                  # No interactive approval prompts
  sandbox:         {resolved from capability_profile}
  model:           {latest from models list, or omit}
  reasoning:       "{medium|high|xhigh}"    # From Reasoning Level Selection
```

Resolve the MCP `sandbox` from bridge-commons:

- `inspect` profile → choose the non-mutating Codex sandbox
- `modify` profile → choose the write-capable Codex sandbox allowed by the executor

The bridge contract is capability-driven. Codex sandbox values are runtime details, not the policy itself.

Capture `structuredContent.threadId` from response for multi-turn use.

### Tool: `codex-reply` — Continue session (if needed)

```
Call: mcp__codex__codex-reply
Parameters:
  prompt:   "Summarize and consolidate all agent findings into the JSON format specified."
  threadId: {threadId from previous call}
```

The `codex-reply` call implements the bridge-commons Post-Analysis Protocol for the MCP path. Use `codex-reply` for each subsequent round — the thread maintains full Round 1 history, so only inject the context packet:

```
Call: mcp__codex__codex-reply
Parameters:
  prompt:   "{role-specific Round N prompt from bridge-commons context packet}"
  threadId: {threadId from Round 1}
```

Run one `codex` + N `codex-reply` calls per role, one role at a time or in parallel sessions.

---

## Step 3B: Execute via CLI (Fallback)

```bash
# Detect latest model first (if CLI supports it)
CODEX_MODEL=$(codex prompt --models 2>/dev/null | awk 'NR==1{print $1}')
MODEL_FLAG=${CODEX_MODEL:+--model $CODEX_MODEL}   # omit flag if empty

timeout {final_timeout} codex exec "{constructed_prompt}" \
  --sandbox {resolved from capability_profile} \
  --ask-for-approval never \
  --json \
  --output-last-message /tmp/codex-bridge-{review_id}.json \
  --ephemeral \
  --skip-git-repo-check \
  $MODEL_FLAG \
  --config reasoning-effort={medium|high|xhigh}
```

For the Post-Analysis Protocol via CLI, use separate `codex exec` calls per round — no session continuity. Embed the full previous-round context in each Round N prompt (same stateless pattern as Gemini CLI).

### CLI Error Handling

| Exit code                | Meaning         | Action                                            |
| ------------------------ | --------------- | ------------------------------------------------- |
| 0                        | Success         | Parse `--output-last-message` file for findings   |
| 124                      | Timeout (shell) | Return SKIPPED, `skip_reason: timeout_after_{n}s` |
| Other                    | CLI error       | Capture stderr, return SKIPPED with error detail  |
| Valid exit, invalid JSON | Parse error     | Attempt partial extraction; else SKIPPED          |

---

## Output

See bridge-commons Output Schema. Bridge-specific fields:

```json
{
  "bridge": "codex",
  "capability_profile": "inspect | modify",
  "model_family": "openai/codex",
  "connection_used": "native-dispatch | mcp | cli",
  "multi_agent_enabled": true,
  "reasoning_level": "medium | high | xhigh"
}
```

Output ID prefix: `X` (e.g., `X001`, `X002`).

---

## Notes

- **MCP server is preferred** — no CLI install needed, auth handled internally, persistent sessions via `codex-reply`
- **Auto-setup option** — orchestrator can write `.mcp.json` to enable MCP server without user installing anything
- **`codex exec` ≠ `codex`** — bare `codex` opens an interactive session; always use `codex exec` for programmatic use
- **Capability resolution is shared** — map `inspect | modify` from bridge-commons onto the appropriate Codex sandbox at runtime
- **HALTED ≠ SKIPPED** — HALTED means the user must make a choice before the review can continue
- **Model**: check latest via `codex prompt --models` at runtime; omit to use server default — never hardcode a model name
- **X-high reasoning requires explicit user confirmation** before proceeding — never activate silently
- **Reasoning level persists in output** (`reasoning_level` field) for caller transparency
- Timeout base increases when multi-agent is enabled (agent spawn overhead)
