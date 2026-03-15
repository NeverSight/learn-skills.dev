---
name: bridge-commons
description: Shared contract for all bridge adapters — pre-flight SOP, standardized input/output schemas, artifact format, and status semantics. Read by any bridge or orchestrating skill. Not invocable standalone.
location: managed
context: reference
---

# Bridge Commons: Shared Contract

This document defines the shared contract that all bridge adapters implement. Every bridge reads this document and conforms to the schemas, status semantics, artifact format, and pre-flight ordering defined here.

## What Bridges Are

Bridges are reference adapters — they define how to dispatch tasks to specific AI runtimes (Claude Code sub-agents, Gemini CLI, Codex CLI, OpenCode). Each bridge:

- Is a **reference document**, not a runnable skill
- Is **read by orchestrating skills** (e.g., deep-council) via the `Read` tool
- Has its **instructions embedded** into Task agent prompts — not invoked separately
- Returns a **structured report** conforming to this contract
- Is **non-blocking** — unavailability produces `SKIPPED`, not a failure

---

## Pre-Flight SOP

Every bridge executes these checks in order before dispatching. Deviate only where a bridge's specific connection chain differs.

### Check ordering

1. **Primary connection** — preferred execution path (Task tool, HTTP server, MCP)
2. **Secondary connection** — CLI fallback
3. **Tertiary connection** — API fallback (if applicable to this bridge)
4. **Authentication** — verify credentials for the selected path
5. **Multi-agent capability** — detect and record; degrade gracefully if absent
6. **Timeout estimation** — calculate from scope + intensity

If none of steps 1–3 succeed → return `status: SKIPPED` immediately. Never block the calling orchestrator.

### HALTED vs SKIPPED

| Status | Cause | Orchestrator action |
|--------|-------|---------------------|
| `SKIPPED` | Non-fatal unavailability — CLI missing, timeout, parse failure | Non-blocking — continue with other bridges |
| `HALTED` | Requires user decision — no provider configured, explicit user abort | **Interactive:** Surface `halt_message` and wait for user input before proceeding. **Non-interactive / auto-mode:** Orchestrator converts to SKIPPED — record `{"bridge": "...", "halt_reason": "..."}` in the council report's `auto_skipped_halted_bridges` array and set `partial_coverage: true`. Never drop silently — the conversion must always be recorded. |
| `ABORTED` | User chose to stop the entire operation | Stop the orchestrator |
| `COMPLETED` | Task ran and outputs are available | Include in synthesis |

**HALTED→SKIPPED conversion is an orchestrator responsibility.** Bridges return `HALTED` when user input is required; the orchestrator decides whether to wait (interactive) or convert to SKIPPED (non-interactive). This conversion policy must appear in the orchestrator's output — `auto_skipped_halted_bridges` is a required field on any council report that auto-converts HALTED bridges.

---

## Timeout Estimation

Calculate per request from scope and intensity. Never hardcode.

| Scope | Base timeout |
|-------|-------------|
| < 5 files or < 500 LOC | 60 s |
| 5–20 files or < 2,000 LOC | 180 s |
| 20–50 files or < 10,000 LOC | 300 s |
| 50+ files or 10,000+ LOC | 600 s |

| Intensity | Multiplier |
|-----------|-----------|
| `quick` | 0.5 |
| `standard` | 1.0 |
| `thorough` | 1.5 |

Apply any bridge-specific multiplier on top (e.g., OpenCode applies 1.5× for provider routing overhead).

```
final_timeout = base_timeout × intensity_multiplier × bridge_multiplier
```

Wrap every CLI invocation with `timeout {final_timeout}` or equivalent.

---

## Input Schema

All bridges accept this standard input:

```json
{
  "bridge_input": {
    "session_id": "unique identifier for this session",
    "scope": "files, topics, or description of what to work on",
    "task_description": "what the agent should do",
    "task_type": "review | planning | implementation | analysis | research | audit",
    "domains": ["domain1", "domain2"],
    "context_summary": "brief description of context",
    "intensity": "quick | standard | thorough"
  }
}
```

`task_type` drives how agent prompts are framed:

| task_type | Output items use | Framing |
|-----------|-----------------|---------|
| `review` | `finding`, `recommendation` | "What is wrong or could be improved?" |
| `analysis` | `finding`, `observation` | "What does this tell us?" |
| `planning` | `plan-item` | "What should be done and in what order?" |
| `implementation` | `implementation-note` | "What is needed to build this correctly?" |
| `research` | `observation`, `recommendation` | "What do we know? What are the options?" |
| `audit` | `finding`, `compliance-gap` | "Does this meet the stated requirement?" — Compliance-calibrated: unmet MUST → HIGH; unmet SHOULD → MEDIUM; met requirements → INFO. |

### Execution Capability Profile

Dispatch capability is derived from `task_type`. Orchestrators pass `task_type`; bridges resolve the capability profile locally and then translate it into runtime-specific flags, agents, or sandbox values.

| task_type | capability_profile | Intent |
|-----------|--------------------|--------|
| `review` | `inspect` | Analyze without changing project state |
| `analysis` | `inspect` | Analyze without changing project state |
| `research` | `inspect` | Gather evidence without changing project state |
| `audit` | `inspect` | Verify compliance without changing project state |
| `planning` | `inspect` | Produce plans without changing project state |
| `implementation` | `modify` | Permit edits and other state-changing work |

Bridges MUST follow this process:

1. Derive `capability_profile` from `task_type`
2. Resolve bridge-specific invocation settings from that profile
3. Inject the resolved settings into the final command or tool call
4. Record the resolved profile in the bridge output

Bridges MUST NOT treat runtime-specific controls as global policy. Values such as CLI permission flags, sandbox modes, agent names, or tool allowlists are implementation details of the selected bridge and must be chosen through this shared profile rather than hardcoded as the only execution mode.

---

## Agent Prompt Template

Construct one prompt per domain in `bridge_input.domains`. Resolve `{expert_role}`, `{focus_areas}`, and `{standards}` from domain-registry using the **Lookup Protocol** in `domain-registry/README.md`. If no registry entry substantially covers the domain concern, synthesize a session-based virtual expert rather than falling back to a mismatched role. Adapt framing based on `task_type`:

```
You are a {expert_role}.

SCOPE: {scope}
TASK: {task_description}
CONTEXT: {context_summary}
INTENSITY: {intensity}
DOMAIN: {domain}

Focus areas: {focus_areas}
Standards:   {standards}

Return your output as JSON:
{
  "agent": "{expert_role}",
  "domain": "{domain}",
  "outputs": [
    {
      "id": "",
      "type": "finding | recommendation | plan-item | implementation-note | observation",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO | null",
      "title": "Short title",
      "description": "Detailed description",
      "evidence": "Specific reference",
      "action": "Recommended action"
    }
  ],
  "cross_domain_signals": [
    {
      "domain": "name of another domain that should examine this finding",
      "reason": "why this domain needs to weigh in"
    }
  ],
  "summary": "Brief summary",
  "confidence": "high | medium | low"
}

`cross_domain_signals` is optional. Use it when your findings have implications that fall outside your domain and require a different domain expert's perspective. Leave empty (`[]`) if no cross-domain expansion is needed.
```

---

## Output Item Types

| `type` | Severity applies? | Use when |
|--------|-------------------|---------|
| `finding` | Yes | Identifying a problem or risk |
| `recommendation` | Yes | Suggesting an improvement |
| `plan-item` | No (use `null`) | A step or action to execute |
| `implementation-note` | No (use `null`) | A detail needed during implementation |
| `observation` | Optional | A neutral insight or data point |

---

## Severity Scale

| Severity | Meaning |
|----------|---------|
| `CRITICAL` | Must be addressed immediately; blocks progress |
| `HIGH` | Significant risk or quality issue |
| `MEDIUM` | Moderate concern; should be addressed |
| `LOW` | Minor issue; worthwhile to fix |
| `INFO` | Informational only |
| `null` | Not applicable (plan items, observations) |

---

## Verdict Logic

Apply only when `task_type` is `review`, `analysis`, or `audit`. Set `null` for all other task types.

**For `review` and `analysis`:**

| Verdict | Condition |
|---------|-----------|
| `FAIL` | Any `CRITICAL` output |
| `CONCERNS` | One or more `HIGH` outputs, or three or more `MEDIUM` outputs |
| `PASS` | No `CRITICAL` or `HIGH`; only `MEDIUM`, `LOW`, or `INFO` |

**For `audit`** (compliance-calibrated — unmet requirements warrant stricter verdicts):

| Verdict | Condition |
|---------|-----------|
| `FAIL` | Any `CRITICAL` output, or two or more `HIGH` compliance-gaps |
| `CONCERNS` | One `HIGH` compliance-gap, or three or more `MEDIUM` compliance-gaps |
| `PASS` | No `CRITICAL` or `HIGH`; all requirements met or only `LOW`/`INFO` gaps |

---

## Output Schema

```json
{
  "bridge": "claude | gemini | codex | opencode",
  "model_family": "anthropic/claude | google/gemini | openai/codex | multi-provider",
  "connection_used": "native-dispatch | cli | api | http-api | mcp",
  "session_id": "...",
  "task_type": "review | planning | implementation | analysis | research",
  "capability_profile": "inspect | modify",
  "status": "COMPLETED | SKIPPED | HALTED | ABORTED",
  "skip_reason": "...",
  "halt_reason": "...",
  "halt_message": "Advisory text to surface to the user",
  "domains_covered": ["domain1", "domain2"],
  "debate_rounds": 2,
  "outputs": [
    {
      "id": "X001",
      "type": "finding | recommendation | plan-item | implementation-note | observation",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO | null",
      "status": "confirmed | revised | withdrawn | disputed | discovered",
      "title": "Short title",
      "description": "Detailed description",
      "evidence": "Specific reference — file, line, quote",
      "action": "Recommended action or next step",
      "domain": "Which domain this belongs to",
      "agent": "Which agent or reviewer produced this"
    }
  ],
  "withdrawn_outputs": [...],
  "disputed_outputs": [
    {
      "output": {...},
      "unresolved_challenge": "Challenge text that was not resolved"
    }
  ],
  "verdict": "PASS | FAIL | CONCERNS | null",
  "confidence": "high | medium | low",
  "prompt_size_chars_r1": null,
  "prompt_size_chars_r2": null,
  "model_validation_warnings": []
}
```

**Output ID prefixes:** `C` (claude), `G` (gemini), `X` (codex), `O` (opencode).

Status placement rules:
- confirmed: appears in `outputs` array
- revised: appears in `outputs` array (updated finding, supersedes earlier version)
- discovered: appears in `outputs` array (emerged during challenge rounds)
- withdrawn: appears in `withdrawn_outputs` array (not in `outputs`)
- disputed: appears in `disputed_outputs` array (also retained in `outputs` with disputed status)

`debate_rounds`: number of rounds completed (0 for quick/consolidation-only, 1+ for debate mode). `null` when status is not COMPLETED.

---

## Output Deduplication

When multiple agents within a bridge produce similar outputs:

1. Assign unique IDs to all outputs first
2. Identify near-identical outputs (same `domain`, similar `title` and `description`)
3. Keep the highest-severity version; discard the duplicate
4. Record the merge in the JSONL event log

---

## Post-Analysis Protocol

After the initial parallel analysis, every bridge runs a post-analysis protocol before returning results. Two approaches are available — select based on intensity:

**Note:** These round counts apply to the bridge-commons Post-Analysis Protocol — the iterative
debate used within individual bridges (Gemini, Codex, OpenCode). They are distinct from the
debate-protocol skill's round counts, which govern the standalone 5-phase protocol. The two
systems have different purposes and calibrations:
- Bridge Post-Analysis Protocol: lightweight, stateless-compatible, 1–3 rounds
- debate-protocol 5-phase: full adversarial, DA obligations, Phase 3 challenge loop, 3–5 rounds

| Intensity | Approach | Rounds after initial analysis |
|-----------|----------|-------------------------------|
| `quick` | Consolidation pass | 1 (single cross-domain review) |
| `standard` | Two-round debate | 1 challenge + 1 response round |
| `thorough` | Continuous debate | Up to N rounds until convergence or max |

For Claude with Agent Teams, this entire section is superseded by the full `debate-protocol` skill, which provides the same structure with async SendMessage between teammates.

---

### Roles

Domain experts are determined by the orchestrating skill (deep-council, deep-review, etc.) before the bridge is called — the bridge receives them via `bridge_input.domains` and executes. Bridges do not perform domain selection.

Spawn these roles in parallel at the start of each round:

| Role | Count | Source | Purpose |
|------|-------|--------|---------|
| **Domain Expert** | One per domain in `bridge_input.domains` | domain-registry — expert role, focus areas, and standards per domain | Subject-matter analysis; defends and revises findings across rounds |
| **Challenger** | 1 (always) | Fixed role — no domain-registry lookup | Cross-domain challenge — Devil's Advocate equivalent; escalates or withdraws challenges each round |
| **Integration Checker** | 1 (always) | Fixed role — no domain-registry lookup | Surfaces cross-component issues; adds new findings as debates reveal interface gaps |

The total number of parallel agents per round = `len(active_domains) + 2` (one expert per domain, plus Challenger and Integration Checker).

The initial domain list is not fixed for the lifetime of a session. During each round, domain experts and the Integration Checker may signal that additional domains need to examine a finding. The orchestrator adds those domains to the active list before the next round, spawning fresh experts for them. See Between Rounds — Orchestrator Synthesis below.

---

### Round 1 — Initial Analysis (always runs, parallel)

All roles run simultaneously with no inter-agent communication. Each produces independent findings using the Agent Prompt Template above.

The orchestrator (bridge dispatcher or deep-council) collects all Round 1 outputs and moves to the between-rounds step.

---

### Between Rounds — Orchestrator Synthesis

The orchestrator reviews all outputs from the previous round and builds a **context packet** for the next round:

1. Collect `cross_domain_signals` from all outputs — identify domains not yet in the active domain list
2. Add any new domains to the active domain list; these experts will be spawned fresh in the next round
3. Identify open challenges from the Challenger that weren't responded to
4. Identify conflicts between Domain Experts (same issue, different conclusions)
5. Identify gaps (cross-cutting concerns not addressed by any active domain)
6. Group challenges by target domain so experts receive only what's directed at them

**Domain expansion rule:** A domain in `cross_domain_signals` that is already active → assign challenges to that existing expert. A domain not yet active → spawn a new expert for it in the next round, providing the relevant finding as their starting context.

**Context packet format:**

```json
{
  "round": 2,
  "active_domains": ["...current domain list including any newly added..."],
  "newly_added_domains": [
    {
      "domain": "name of newly added domain",
      "trigger_finding_id": "X001",
      "reason": "why this domain was added"
    }
  ],
  "previous_findings": ["...all outputs from previous round..."],
  "open_challenges": [
    {
      "challenge_id": "CH001",
      "target_finding_id": "X001",
      "challenge_text": "This finding assumes X but the evidence shows Y instead",
      "directed_at_domain": "domain name"
    }
  ],
  "synthesis": "Round 1: 5 findings. 2 challenged. 1 new domain added. Gap: coverage expanded."
}
```

If no open challenges, no conflicts, and no new domains to add → stop early (convergence). Do not run additional rounds.

---

### Round N — Challenge & Response

Existing domain experts, Challenger, and Integration Checker re-run with the context packet. Newly added domain experts run for the first time with a focused prompt scoped to their trigger finding.

**Existing domain expert prompt addition:**
```
Previous findings from your domain:
{their_previous_round_outputs}

Challenges directed at your findings:
{challenges_targeting_this_domain}

For each challenge:
- If you agree: withdraw or revise the finding (update severity or description)
- If you disagree: provide evidence-backed defense
- Mark each output with status: confirmed | revised | withdrawn
- If you identify additional domains that should examine your findings, include cross_domain_signals
```

**Newly added domain expert prompt (first appearance in Round N):**
```
You are a {expert_role}.

SCOPE: {scope}
CONTEXT: {context_summary}

You have been brought in because a finding in another domain has implications for yours.

Trigger finding:
{the finding that produced the cross_domain_signal for this domain}

Reason you were added:
{cross_domain_signal.reason}

Analyze this finding from your domain's perspective. Produce your own findings.
Include cross_domain_signals if you identify further domain expansion needed.
```

**Challenger prompt addition:**
```
All domain expert findings from previous round:
{all_previous_findings}

Your previous challenges and expert responses:
{challenge_history}

For each challenge:
- If the expert defended convincingly: withdraw your challenge
- If the defense is insufficient: escalate (raise severity, add evidence)
- Challenge findings from any newly added domain experts
- Add new challenges for findings you haven't challenged yet
```

**Integration Checker prompt addition:**
```
All findings and challenges from previous round, including newly added domain experts:
{all_previous_findings_and_challenges}

Add new cross-component findings that emerge from the ongoing debate.
Focus on: interface gaps revealed by challenges, cascading impacts of revised findings,
and cross-cutting issues that span the newly added domains.
```

---

### Termination Conditions

Stop running rounds when **any** of these is true:

| Condition | Description |
|-----------|-------------|
| Max rounds reached | `quick`: 0 rounds after initial; `standard`: 1; `thorough`: 3 |
| Convergence | No new findings or revisions compared to previous round |
| All challenges resolved | Every challenge is either withdrawn or defended (no `disputed` status) |

---

### Finding States

After debate completes, tag each output with a `status` field:

| Status | Meaning |
|--------|---------|
| `confirmed` | Survived at least one challenge round without revision |
| `revised` | Expert updated the finding in response to a challenge |
| `withdrawn` | Expert retracted (challenged and couldn't defend) |
| `disputed` | Unresolved — Challenger maintains challenge, expert maintains finding |
| `discovered` | New finding surfaced during a challenge round (not in Round 1) |

Withdrawn findings are excluded from the final `outputs` array but recorded in `withdrawn_outputs`.

---

### Context Passing Between Rounds

Since non-Claude bridges lack async messaging, context flows **explicitly** — the orchestrator embeds the full context packet in each Round N prompt:

| Bridge | Session continuity | Context injection |
|--------|-------------------|-------------------|
| OpenCode (HTTP API) | Session remembers Round 1 automatically | Send context packet as next message in same session |
| OpenCode (CLI) | No session state | Embed full Round 1 outputs + context packet in Round 2 prompt |
| Codex (MCP) | `threadId` maintains history | `codex-reply` with context packet as prompt |
| Codex (CLI) | No session state | New `codex exec` with embedded context |
| Gemini (subagents) | No cross-call state | New `gemini -p` call with embedded context |
| Claude (Task tool) | Parent agent holds all state | Spawn Round 2 sub-agents with context from parent |
| Claude (Agent Teams) | Teammates use SendMessage | Superseded by debate-protocol |

For bridges with session continuity (OpenCode HTTP, Codex MCP), the Round 2 prompt only needs to include the context packet — the session already has Round 1 history. For stateless bridges, embed the full previous-round findings in the prompt.

### Stateless Context Size Limit

**Maximum embedded context for stateless Round N prompts: 32,000 characters** (combined previous-round findings + context packet).

When previous-round outputs would exceed this limit:

1. Summarize each finding to: `id`, `title`, `severity`, `description` only (drop `evidence`, `action`, `agent`)
2. If still over limit: retain CRITICAL and HIGH findings verbatim; reduce MEDIUM/LOW to one-line summaries (`"id: title (severity)"`)
3. Annotate the Round N prompt with: `"NOTE: Prior round context summarized due to size (>32k chars). Full outputs in .outputs/bridges/ artifact."`
4. Record approximate prompt size per round in the bridge output as `prompt_size_chars_r{n}` (e.g., `prompt_size_chars_r2: 28500`)

**Bridges MUST NOT silently truncate.** Silent truncation produces Round N responses that are indistinguishable from valid full-context responses and corrupts multi-model confirmation reliability.

---

### Consolidation (after final round)

After debate terminates, the orchestrator runs a final consolidation:

1. Collect all `confirmed`, `revised`, and `discovered` outputs — these form the final `outputs` array
2. Collect `withdrawn` outputs into `withdrawn_outputs`
3. Collect `disputed` outputs into `disputed_outputs` with the unresolved challenge noted
4. Apply verdict logic from the Verdict Logic section above
5. Add any remaining cross-domain outputs (`domain: "cross-domain"`, `agent: "consolidation"`)

For `quick` intensity, the consolidation is the entire protocol — skip all debate rounds and go directly here after Round 1.

---

## Artifact Format

Every bridge saves two files per execution for auditability.

### JSONL event log

Path: `.outputs/bridges/{bridge}-{YYYYMMDD-HHMMSS}-{session_id}.jsonl`

Write events as they occur — one JSON object per line:

```jsonl
{"event": "bridge_start", "bridge": "{bridge}", "session_id": "{session_id}", "timestamp": "{ISO-8601}"}
{"event": "preflight", "step": "availability_check", "result": "found", "path": "{path}"}
{"event": "preflight", "step": "timeout_estimate", "value_seconds": "{n}"}
{"event": "dispatch", "mode": "multi-agent", "domains": ["{domain1}", "{domain2}"]}
{"event": "output", "id": "{id}", "severity": "{severity}", "title": "{title}"}
{"event": "bridge_complete", "status": "COMPLETED", "verdict": "{verdict}", "output_count": "{n}", "timestamp": "{ISO-8601}"}
```

### Markdown summary

Path: `.outputs/bridges/{bridge}-{YYYYMMDD-HHMMSS}-{session_id}.md`

YAML frontmatter + human-readable summary:

```yaml
---
bridge: {bridge}
session_id: {session_id}
timestamp: {ISO-8601}
task_type: {task_type}
domains: [{domain1}, {domain2}]
verdict: {verdict}
status: {status}
---
```

### Directory creation

```bash
mkdir -p .outputs/bridges
```

---

## CLI Error Handling

Common patterns across all CLI-based bridges:

| Exit code | Meaning | Action |
|-----------|---------|--------|
| `0` | Success | Parse output |
| `124` | Timeout (from `timeout` wrapper) | Return `SKIPPED`, reason: `timeout_after_{n}s` |
| Other non-zero | CLI error | Capture stderr; return `SKIPPED` with detail |

Invalid or unparseable output → attempt to extract structured content; if unrecoverable, return `SKIPPED`.

---

## Two-Layer Debate Architecture

The full deep-council execution involves two distinct debate layers. Understanding the distinction prevents confusing the intra-bridge analysis with the cross-bridge synthesis.

```
deep-council
│
├── Layer 2: Intra-Bridge Analysis (runs inside each bridge, before returning to council)
│   │
│   ├── bridge-claude
│   │     Full 5-phase debate-protocol (DA + IC + domain experts via Agent Teams or Task tool)
│   │     Richest intra-bridge analysis — async messaging, multi-round adversarial
│   │
│   ├── bridge-gemini
│   │     Post-Analysis Protocol rounds (sequential, stateless prompts)
│   │     Lighter — no async messaging, 1–3 rounds via re-prompting
│   │
│   ├── bridge-codex
│   │     Post-Analysis Protocol rounds (sequential, stateless prompts)
│   │     Same pattern as gemini
│   │
│   └── bridge-opencode
│         Single-model:  Post-Analysis Protocol rounds (same as gemini/codex)
│         Multi-model:   N parallel model invocations → mini-synthesis within bridge
│                        → becomes its own mini-council before reporting to Layer 1
│
└── Layer 1: Cross-Bridge Synthesis Debate (deep-council Step 6 Stage B)
      Debate Coordinator Task agent challenges aggregated findings from ALL bridges
      DA asks: "Did all bridges agree because they're all right, or shared bias/prompting?"
      IC checks cross-bridge integration implications
      2–3 challenge rounds (standard/thorough)
      Output: confirmed / downgraded / disputed / withdrawn / integration findings
```

**Why the asymmetry exists:** bridge-claude has native sub-agent dispatch (Task tool, Agent Teams) — it can run truly parallel, async-communicating agents. CLI bridges (gemini, codex, opencode) are single-process invocations — they can only achieve multi-round analysis through sequential re-prompting, which is the Post-Analysis Protocol.

**Multi-model opencode fills the gap:** With 2+ models configured in `.bridge-settings.json`, bridge-opencode spawns one invocation per model in parallel — each model produces independent findings, and a mini-synthesis deduplicates and elevates multi-model-confirmed findings. This gives bridge-opencode a Layer 2 that is closer in depth to bridge-claude, without requiring native sub-agent dispatch.

**The two layers are complementary, not redundant:**
- Layer 2 (intra-bridge) maximizes what each model family can find on its own
- Layer 1 (cross-bridge) challenges whether different model families genuinely agree or just share the same blind spot

---

## Bridge Settings

Bridges read suite configuration from `.bridge-settings.json` in the project root. This file is owned by the skill suite — it is not OpenCode's config, Gemini's config, or any CLI tool's config.

```json
{
  "bridges": {
    "claude":   { "enabled": true },
    "gemini":   { "enabled": true },
    "codex":    { "enabled": true,  "model": null },
    "opencode": {
      "enabled": true,
      "model":  null,
      "models": []
    }
  },
  "reasoning_level": "medium",
  "updated": "{ISO-8601}",
  "ttl_hours": 24
}
```

**`opencode.models` array** — controls multi-model dispatch for bridge-opencode:

| Value | Behavior |
|-------|---------|
| `[]` (empty) or missing | Single invocation, OpenCode's configured default model |
| `["glm/glm-4-7"]` (one entry) | Single invocation with that specific model |
| `["glm/glm-4-7", "kimi/moonshot-v1-8k", "qwen/qwen-plus"]` | Three parallel invocations, one per model, mini-synthesis within bridge |

Models must use `provider/model` format as required by OpenCode (e.g., `glm/glm-4-7`, not just `glm`).

`model` (singular): legacy single-model override — ignored when `models` array has entries.

**Model identifier validation:** During bridge availability checks, if a model identifier is specified in `.bridge-settings.json`, bridges SHOULD perform a lightweight validation probe (e.g., `codex models list`, `opencode auth list`) to confirm the identifier is resolvable. If a model cannot be resolved:
- Emit a **warning** in the bridge output (not SKIPPED — the bridge itself may still work with the provider's default model)
- Record: `"model_validation_warnings": [{"model": "...", "reason": "not found in provider model list"}]`
- Continue execution with the provider's default model if the specified model is invalid

This prevents silent capability reduction when committed model identifiers become stale.

---

## Notes

- Bridges do not modify source files unless `capability_profile` resolves to `modify` from `task_type = implementation`
- Bridges do not make external network calls beyond what their connected runtime provides
- `SKIPPED` is always non-blocking — orchestrators must handle it gracefully
- `HALTED` requires explicit user input (interactive) or orchestrator conversion to SKIPPED (non-interactive) — never silently dropped
- All fields in the output schema are required; use `null` where not applicable

### Input Field Aliases (Deprecated)

`session_id` and `scope` are the canonical bridge-commons field names. The following aliases exist in deep-council Step 4 for backward compatibility and will be removed in a future version:

| Alias | Canonical name | Removal target |
|-------|---------------|----------------|
| `review_id` | `session_id` | v3.0 |
| `review_scope` | `scope` | v3.0 |

Bridges MUST accept both forms. New orchestrators SHOULD use canonical names only.
