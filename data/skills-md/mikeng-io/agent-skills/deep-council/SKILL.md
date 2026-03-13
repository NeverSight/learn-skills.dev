---
name: deep-council
description: Multi-model review council. Dispatches review tasks to all available bridge adapters (Claude, Gemini, Codex, OpenCode), each of which runs internal sub-agents. Synthesizes findings across model families using debate-protocol. Usable standalone or as a second-pass from deep-verify. Orchestrator-agnostic — can be invoked by Claude Code, OpenCode, or Codex CLI.
location: managed
dependencies:
  - context
  - preflight
  - bridge-commons
  - bridge-claude
  - bridge-gemini
  - bridge-codex
  - bridge-opencode
  - domain-registry
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - Write
  - Bash(mkdir *)
  - Bash(ls *)
  - Bash(which *)
  - Bash(cat *)
---

# Deep Council: Multi-Model Review Council

Execute this skill to run a multi-model review using all available bridge adapters, synthesizing findings across model families.

## Execution Instructions

When invoked, you will:

0. **Resolve scope and context** — invoke preflight (if sparse) + context skill in parallel
1. Populate council context from working_scope
2. Read and inventory available bridges
3. Dispatch all available bridges in parallel via Task agents
4. Synthesize findings across bridges using debate-protocol logic
5. Produce a consolidated multi-model report

---

## Dependency Check

Before executing any step, verify all required skills are present. Use `Glob` or `ls` to check each:

```
[skills-root]/context/SKILL.md
[skills-root]/preflight/SKILL.md
[skills-root]/bridge-commons/SKILL.md
[skills-root]/bridge-claude/SKILL.md
[skills-root]/bridge-gemini/SKILL.md
[skills-root]/bridge-codex/SKILL.md
[skills-root]/bridge-opencode/SKILL.md
[skills-root]/domain-registry/README.md
```

Where `[skills-root]` is the parent of this skill's directory (e.g., `skills/` or `.claude/skills/`). Resolve with `ls ../` from this skill's location.

If any required file is missing → **stop immediately** and output:

```
⚠ Missing required skills for deep-council:

  {missing-skill}
    Expected: {skills-root}/{missing-skill}/SKILL.md

Install the missing skill(s):
  git clone https://github.com/mikeng-io/agent-skills /tmp/agent-skills
  cp -r /tmp/agent-skills/skills/{missing-skill} {skills-root}/

Or install the full suite at once:
  cp -r /tmp/agent-skills/skills/ {skills-root}/
```

All dependencies present → proceed to Step 0.

---

## Step 0: Scope & Context Resolution

**Context (always required):**

Invoke `Skill("context")` first. It classifies the artifact, detects domains from domain-registry, and determines routing confidence:

```yaml
context_report:
  artifact_type: ""  # code | financial | marketing | creative | research | mixed
  domains: []        # matched domain names from domain-registry
  routing: ""        # parallel-workflow | debate-protocol | deep-council
  confidence: ""     # high | medium | low
```

**Preflight (conditional — triggered by context confidence):**

Invoke `Skill("preflight")` only if `context_report.confidence == "low"` OR one or more of these signals remains unresolved after context runs:
- Artifact is not clearly identified
- Intent is ambiguous (review vs. audit vs. verify vs. research)
- Domains could not be detected
- Scope is too broad to proceed

Preflight asks at most 3 targeted questions (one at a time) to fill exactly the gaps context could not resolve:

```yaml
scope_clarification:
  artifact: ""       # what to analyze
  intent: ""         # review | audit | verify | research | explore
  domains: []        # inferred domains (supplements context_report.domains)
  constraints: []    # any explicit focus areas
  confidence: ""     # high | medium
```

If `context_report.confidence == "high"` → skip preflight entirely.

**Post-preflight validation** (only when preflight ran):

```yaml
if scope_clarification.confidence == "medium":
  # Preflight completed but scope still contains assumptions
  emit_warning: |
    ⚠ Preflight returned confidence: medium — scope may contain unverified assumptions.
    Assumptions made: {scope_clarification.assumptions}
    Proceeding with available context. Findings may be scoped more narrowly than intended.
  # Record warning in synthesis_notes of final report
  # Do NOT block — proceed with the available working_scope
```

If `scope_clarification.confidence == "high"` after preflight → proceed normally.

**Merge into working scope:**
```yaml
working_scope:
  artifact: ""            # from context signals + scope_clarification if preflight ran
  intent: ""              # from context or scope_clarification
  domains: []             # from context_report (authoritative), supplemented by preflight
  constraints: []         # from scope_clarification (empty if preflight skipped)
  context_summary: ""     # combined description for agent prompts
  intensity: ""           # from routing signals and any explicit user request
```

Use `working_scope` throughout this skill. Do not re-extract context from conversation after Step 0.

---

## Step 1: Populate Council Context

Using `working_scope` from Step 0, populate the council context:

```yaml
council_context:
  review_scope: ""        # from working_scope.artifact
  context_summary: ""     # from working_scope.context_summary
  artifact_type: ""       # from working_scope context_report.artifact_type
  domains: []             # from working_scope.domains
  intensity: "standard"   # from working_scope.intensity (quick | standard | thorough)
  review_id: ""           # Generate a unique ID: council-{YYYYMMDD-HHmmss}
  task_type: "review"     # from working_scope.intent — defaults to "review"
```

**Optional: enrich with DeepWiki (if configured)**

If the review involves a GitHub repository and `mcp__devin__*` tools are available, invoke the `deepwiki` skill to supplement `context_summary` with architectural intent before dispatching bridges. Bridges with richer context produce better-targeted findings.

```
Skill("deepwiki")
→ ask_question: "What are the primary architectural concerns and component relationships relevant to: {review_scope}?"
→ Append answer to context_summary before Step 4 bridge dispatch
```

Falls back gracefully if DeepWiki is not configured. Non-blocking.

Read domain-registry to confirm domain selection:
```
Read: [skills-root]/domain-registry/domains/technical.md
Read: [skills-root]/domain-registry/domains/business.md
Read: [skills-root]/domain-registry/domains/creative.md
```

---

## Step 1B: Model Discovery & Settings

Before dispatching bridges, discover what models and providers are configured and confirm with the user. This step runs once per project — results are cached in `.bridge-settings.json`.

### Load or Discover

```bash
# Check for existing settings
cat .bridge-settings.json 2>/dev/null
```

If `.bridge-settings.json` exists and is current → **load settings and proceed to Step 2** (skip user prompt unless user passes `--reconfigure`).

If not found or `--reconfigure` → run discovery:

```bash
# Codex: list available models
codex models list 2>/dev/null

# OpenCode: list authenticated providers
opencode auth list 2>/dev/null

# Gemini: check availability
which gemini 2>/dev/null && echo "available"
```

### Present to User

Show discovered configuration:

```
Available bridges for this review:

  [claude]     ✓ Task tool accessible
  [gemini]     ✓ CLI found           Model: {gemini default}
  [codex]      ✓ MCP configured      Models: {from codex models list}
  [opencode]   ✓ Providers: {list}   Dispatch: {single-model | multi-model (N models)}
                                     Models: {models array from settings, or "default"}

Reasoning level (applies to Codex):  medium / high / xhigh  [medium]

OpenCode multi-model: add/remove models, or press Enter to accept current settings.
  Current: {bridges.opencode.models or "default (single model)"}
  Format:  provider/model  e.g. glm/glm-4-7, kimi/moonshot-v1-8k, qwen/qwen-plus

Enable/disable bridges, select models, or press Enter to accept defaults.
```

Wait for user input. Accept `Enter` to use defaults.

### Save Settings

```json
// .bridge-settings.json — suite-owned config, separate from any CLI tool's own config
{
  "bridges": {
    "claude":    { "enabled": true },
    "gemini":    { "enabled": true },
    "codex":     { "enabled": true, "model": null },
    "opencode":  {
      "enabled": true,
      "model":   null,
      "models":  []
    }
  },
  "reasoning_level": "medium",
  "updated": "{ISO-8601}",
  "ttl_hours": 24
}
```

`opencode.models` — controls multi-model dispatch:
- `[]` or missing → single invocation with OpenCode's default model
- `["glm/glm-4-7", "kimi/moonshot-v1-8k"]` → two parallel invocations, mini-synthesis within bridge
- `["glm/glm-4-7", "kimi/moonshot-v1-8k", "qwen/qwen-plus"]` → three models, bridge-opencode acts as its own mini-council

`model` (singular) is a legacy single-model override — ignored when `models` has entries. See bridge-commons for the full bridge settings schema and the two-layer debate architecture.

On load, if `(current_time - updated) > ttl_hours` → force re-discovery even without `--reconfigure`.

Apply these settings when dispatching bridges in Step 4.

---

## Step 2: Read Bridge Reference Docs

Use the Read tool to load each bridge's reference document:

```
Read: [skills-root]/bridge-claude/SKILL.md
Read: [skills-root]/bridge-gemini/SKILL.md
Read: [skills-root]/bridge-codex/SKILL.md
Read: [skills-root]/bridge-opencode/SKILL.md
```

These files define exactly how each bridge executor should operate. Their instructions will be embedded verbatim into Task agent prompts.

---

## Step 3: Check Bridge Availability

For each bridge, determine availability:

```yaml
bridge_claude:
  status: available_via_task_tool   # Available when Task tool is accessible (default in Claude Code; may be unavailable in other executors)

bridge_gemini:
  check: "which gemini"
  status: available | unavailable

bridge_codex:
  check_mcp: "cat .mcp.json 2>/dev/null | grep -i codex"
  check_cli: "which codex"
  status: available_mcp | available_cli | unavailable

bridge_opencode:
  check_mcp: "cat .mcp.json 2>/dev/null | grep -i opencode"
  check_cli: "which opencode"
  status: available_mcp | available_cli | unavailable
```

Build availability list: `available_bridges = [bridge names that are available]`
Build skipped list: `skipped_bridges = [bridge names that are unavailable]`

At least one bridge must return COMPLETED for synthesis to proceed. If zero bridges complete, emit ABORTED with explanation.

---

## Step 4: Dispatch Bridges in Parallel

For each available bridge, spawn a Task agent. The Task prompt embeds:
1. The full bridge SKILL.md instructions (read in Step 2)
2. The specific bridge_input for this review

### Bridge Input (same for all bridges)

```json
{
  "bridge_input": {
    "session_id": "{review_id}",
    "review_id": "{review_id}",
    "scope": "{review_scope}",
    "review_scope": "{review_scope}",
    "task_type": "{task_type}",
    "task_description": "{context_summary}",
    "domains": {domains},
    "context_summary": "{context_summary}",
    "intensity": "{intensity}"
  }
}
```

`session_id` and `scope` are the bridge-commons canonical field names; `review_id` and `review_scope` are aliases for backward compatibility.

### Task Prompt Template (for each bridge)

```
You are executing the {bridge_name} review bridge.

## Bridge Instructions

{full contents of bridge-{name}/SKILL.md}

## Your Input

{bridge_input JSON}

## Your Task

Follow the bridge instructions exactly. Check availability first (if required),
then execute the review with the provided input. Return the complete bridge
report JSON as your final output.
```

### Parallel Dispatch

Spawn ALL available bridge Task agents simultaneously:
```
Task: bridge-claude executor (if available — Task tool accessible)
Task: bridge-gemini executor (if gemini available)
Task: bridge-codex executor (if codex available)
Task: bridge-opencode executor (if opencode available)
```

Wait for ALL tasks to complete before proceeding.

---

## Step 5: Collect Bridge Reports

Collect all bridge reports. Each should conform to its bridge's output format:
- `bridge_claude_report` — findings, verdict, domains_covered
- `bridge_gemini_report` — findings, verdict, status (may be SKIPPED)
- `bridge_codex_report` — findings, verdict, status (may be SKIPPED)
- `bridge_opencode_report` — findings, verdict, status, models_used

SKIPPED bridges are noted but do not block synthesis.

### HALTED Bridges

If any bridge returns `status: HALTED`:

1. Surface the bridge's `halt_message` to the user
2. Offer: [skip this bridge / retry after setup / abort entire review]
3. **Non-interactive default**: auto-SKIPPED with a warning in the report
   (`"auto_skipped_halted_bridges": [{"bridge": "...", "halt_reason": "..."}]`)
4. Continue council synthesis with remaining COMPLETED bridges

HALTED does not block the council — it is surfaced and handled, then the council proceeds.

---

## Step 6: Cross-Bridge Synthesis

Cross-bridge synthesis runs in two stages: mechanical deduplication first, then adversarial debate.

### Stage A: Mechanical Deduplication

Collect all findings from all bridge reports. Apply these rules:

```yaml
multi_model_confirmed_preliminary:
  condition: "Finding confirmed by 2+ bridge reports (>70% description overlap)"
  action: "Merge into single finding — inherit highest severity, list all contributing bridges"

single_source_preliminary:
  condition: "Finding from exactly 1 bridge"
  action: "Retain with bridge attribution"

disputed_preliminary:
  condition: "Finding present in 1+ bridges but explicitly contradicted by another"
  action: "Flag as disputed with both positions recorded"
```

**Severity escalation rule:** If 2+ bridges independently rate the same issue CRITICAL or HIGH → escalate to the higher rating.

**Stateless CLI path flag:** When two or more stateless CLI bridges (gemini CLI, codex CLI, opencode CLI) both confirm the same finding, add `"shared_cli_path": true` to the merged finding. These confirmations should be weighted as lower-confidence than genuine independent model-family agreement — stateless bridges embed prior-round context verbatim, and if both truncated to the same context window, "agreement" may reflect truncation-survivor correlation rather than independent discovery. The Debate Coordinator (Stage B) MUST apply additional scrutiny to findings marked `shared_cli_path: true`.

After Stage A, you have a `preliminary_findings` list with initial classification. This is NOT the final output — proceed to Stage B.

---

### Stage B: Debate — Adversarial Validation

Spawn a **Debate Coordinator** Task agent to challenge the preliminary findings. Do NOT skip this stage — mechanical deduplication catches overlaps but does not validate them. The debate catches:
- Findings that look confirmed but rest on a shared wrong assumption across bridges
- Severity assessments that are inflated or deflated uniformly
- Cross-bridge integration issues no single bridge found

**Debate Coordinator Task Prompt:**

```
You are a DEBATE COORDINATOR for cross-bridge synthesis. Your job is NOT to summarize findings — it is to challenge them adversarially and surface issues the mechanical deduplication missed.

## Context
{council_context.context_summary}
Scope: {council_context.review_scope}
Intensity: {council_context.intensity}
Domains covered: {council_context.domains}

## Preliminary Findings (from {N} bridges)
{preliminary_findings JSON — include all multi-model-confirmed, single-source, and disputed findings}

## Your Obligations

### Role 1: Devil's Advocate

MUST challenge every multi-model-confirmed CRITICAL or HIGH finding. A finding that "all bridges agree on" is exactly the finding most in need of adversarial review — agreement can reflect shared bias, shared prompting, or shared blindspot.

For each CRITICAL/HIGH preliminary finding, ask:
1. What assumption does every bridge share that could be wrong?
2. What scenario makes this finding not apply? Is that scenario plausible?
3. Is the severity calibrated to impact (actual harm, actual likelihood), or is it inherited from the first bridge's framing?

SHOULD challenge MEDIUM findings when you detect a pattern (e.g., 3 MEDIUM findings all assume X — challenge X itself).

**A valid challenge MUST do one of:**
- (a) Identify a missing assumption that, if corrected, reduces severity
- (b) Propose an alternative explanation that is at least as plausible as the finding's stated cause
- (c) Surface a scenario where the finding demonstrably does not apply, and assess how likely that scenario is

**An invalid challenge** is: "I don't think this is serious", "This might not matter", or any claim without an identified mechanism.

### Role 2: Integration Checker

Review all surviving findings (after DA challenge rounds) for cross-component implications:

- **Interface mismatches**: does finding A in component X assume something about Y that Y doesn't guarantee?
- **Error propagation gaps**: if finding B causes a failure, which callers of that component don't handle it?
- **Shared assumption failures**: if finding C's root cause is true, does it also make finding D worse than either bridge stated?
- **New findings from combination**: two MEDIUM findings that together imply a CRITICAL scenario neither bridge named

Surface integration findings under domain: "integration".

## Debate Rounds

Run 2 rounds (standard intensity) or 3 rounds (thorough intensity):

**Round 1** — DA challenges multi-model-confirmed CRITICALs and HIGHs. For each:
- If challenge succeeds → downgrade or mark DISPUTED with rationale
- If challenge fails (finding holds) → mark CONFIRMED with "DA-challenged" annotation

**Round 2** — Integration Checker reviews all Round 1 survivors. Surfaces integration findings.

**Round 3 (thorough only)** — DA challenges any newly added integration findings.

## Output Format (JSON)

Return:
{
  "debate_rounds": 2,  // or 3 for thorough
  "confirmed_findings": [...],         // survived all challenges (include DA-challenged annotation)
  "downgraded_findings": [...],        // severity reduced by DA (include rationale)
  "disputed_findings": [...],          // challenged but not resolved
  "withdrawn_findings": [...],         // DA challenge revealed finding was invalid
  "integration_findings": [...],       // new findings from Integration Checker
  "challenge_notes": [                 // record of each challenge outcome
    {
      "finding_id": "...",
      "challenge": "...",
      "response": "...",
      "outcome": "confirmed | downgraded | disputed | withdrawn"
    }
  ]
}
```

### Stage B Output → Final Classification

Replace preliminary classification with debate output:

```yaml
multi_model_confirmed:   # Debate-confirmed multi-bridge findings
single_source_findings:  # Surviving single-source findings (debate-unchallenged)
disputed_findings:       # Debate-disputed (from both preliminary + debate rounds)
integration_findings:    # New findings from Integration Checker
withdrawn_findings:      # Findings invalidated by DA challenge
```

### Cross-Bridge Verdict

**Note:** Cross-bridge verdict thresholds deliberately differ from per-bridge bridge-commons thresholds.
Per-bridge: FAIL = any single CRITICAL finding (that bridge's internal debate flagged it).
Cross-bridge: FAIL = multi-model-confirmed CRITICAL (requires multiple model families to agree).
This is intentional — cross-bridge synthesis accounts for depth asymmetry (some bridges run richer
debate than others) by requiring multi-model agreement before escalating to FAIL.

```yaml
FAIL:
  - Any multi-model-confirmed CRITICAL finding
  - Any single-source CRITICAL finding (from a high-depth bridge — claude with Agent Teams or Task Tool)
  - 3+ multi-model-confirmed HIGH findings

CONCERNS:
  - 1-2 multi-model-confirmed HIGH findings
  - Multiple single-source HIGH findings
  - Any disputed CRITICAL/HIGH finding

PASS:
  - No CRITICAL/HIGH confirmed findings
  - Only MEDIUM/LOW/INFO across all bridges
```

---

## Step 7: Produce Output

### Council Report Structure

```json
{
  "type": "deep-council",
  "review_id": "{review_id}",
  "verdict": "PASS | FAIL | CONCERNS",
  "timestamp": "{ISO-8601}",
  "bridges_invoked": ["claude", "gemini", "codex", "opencode"],
  "bridges_available": ["claude", "gemini"],
  "bridges_skipped": ["codex", "opencode"],
  "auto_skipped_halted_bridges": [
    {"bridge": "{bridge}", "halt_reason": "{halt_reason}"}
  ],
  "partial_coverage": false,
  "skip_reasons": {
    "codex": "CLI not found, MCP not configured",
    "opencode": "CLI not found, MCP not configured"
  },
  "domains_covered": ["{domain1}", "{domain2}"],
  "intensity": "standard",
  "multi_model_confirmed": [
    {
      "id": "MMC001",
      "severity": "HIGH",
      "title": "...",
      "description": "...",
      "evidence": "...",
      "remediation": "...",
      "confirmed_by": ["{bridge1}", "{bridge2}"],
      "source_findings": [
        {"bridge": "{bridge1}", "finding_id": "{original-id}"},
        {"bridge": "{bridge2}", "finding_id": "{original-id}"}
      ],
      "domains": ["{domain}"]
    }
  ],
  "single_source_findings": [
    {
      "id": "SS001",
      "severity": "MEDIUM",
      "title": "...",
      "description": "...",
      "source_bridge": "{bridge}",
      "domains": ["{domain}"]
    }
  ],
  "disputed_findings": [
    {
      "id": "D001",
      "title": "...",
      "positions": [
        {"bridge": "claude", "severity": "HIGH", "position": "..."},
        {"bridge": "gemini", "severity": "LOW", "position": "..."}
      ]
    }
  ],
  "synthesis_notes": "Summary of cross-model analysis"
}
```

If zero bridges return COMPLETED, emit the following instead and stop:

```json
{
  "status": "ABORTED",
  "abort_reason": "No bridges returned COMPLETED results",
  "bridges_attempted": ["..."],
  "bridges_skipped": ["..."],
  "bridges_halted": ["..."]
}
```

---

## Step 8: Save Artifact

Save to `.outputs/council/{YYYYMMDD-HHMMSS}-council-{review_id}.md` with YAML frontmatter:

```yaml
---
skill: deep-council
timestamp: {ISO-8601}
artifact_type: council
domains: [{domain1}, {domain2}]
verdict: PASS | FAIL | CONCERNS
bridges_available: [{bridge1}, {bridge2}]
bridges_skipped: [{bridge3}]
review_id: "{unique id}"
context_summary: "{brief description of what was reviewed}"
---
```

Also save JSON companion: `{YYYYMMDD-HHMMSS}-council-{review_id}.json`

**No symlinks.** To find the latest artifact:
```bash
ls -t .outputs/council/ | head -1
```

**QMD Integration (optional):**
```bash
qmd collection add .outputs/council/ --name "council-reports" --mask "**/*.md" 2>/dev/null || true
qmd update 2>/dev/null || true
```

---

## Fallback Mode

If invoked with `--fallback-mode` (e.g., from deep-verify as a second pass):

- Use only bridge-claude (if available — Task tool accessible in current executor)
- Apply debate-protocol logic with single-bridge findings
- Mark report `"fallback": true`
- Merge findings with calling skill's existing report

---

## Notes

- **No Skill-within-Skill**: Bridges are read via Read tool and embedded in Task prompts — NOT called via Skill tool
- **Minimum threshold**: At least one bridge must return COMPLETED; zero completions emits ABORTED
- **SKIPPED/HALTED bridges don't block**: Council proceeds and notes what was skipped or halted
- **Transparent attribution**: Every finding carries its source bridge(s)
- **Intensity propagates**: The intensity setting flows to all bridges and their sub-agents
