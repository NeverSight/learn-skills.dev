---
name: context
description: Analyze conversation context to classify what is being discussed, detect relevant domains from domain-registry, and determine optimal routing (parallel-workflow vs debate-protocol vs deep-council). Can be invoked directly or called by other skills as a pre-flight step.
location: managed
dependencies:
  - domain-registry
allowed-tools:
  - ToolSearch
  - Read
  - Glob
  - Grep
  - Bash(ls *)
  - Bash(git remote -v)
  - Task
  - Skill
  - Write
  - Bash(mkdir *)
---

# Deep Context: Artifact Classifier and Smart Router

Execute this skill to analyze conversation context, detect relevant domains, and determine the optimal review routing strategy.

## Execution Instructions

When invoked, analyze the current conversation and produce a context report.

---

## Dependency Check

Before executing any step, verify the domain-registry is present:

```
[skills-root]/domain-registry/README.md
```

Where `[skills-root]` is the parent of this skill's directory. Resolve with `ls ../` from this skill's location.

If missing → **stop immediately** and output:

```
⚠ Missing required skill for context:

  domain-registry
    Expected: {skills-root}/domain-registry/README.md

Install:
  git clone https://github.com/mikeng-io/agent-skills /tmp/agent-skills
  cp -r /tmp/agent-skills/skills/domain-registry {skills-root}/
```

Dependency present → proceed to Step 1.

---

## Step 1: Analyze Conversation

Extract from the conversation:

```yaml
conversation_signals:
  files_mentioned: []        # File paths referenced (e.g., "src/auth.go")
  artifacts_mentioned: []    # Other artifacts (Figma files, spreadsheets, docs)
  topics: []                 # Key topics discussed
  concerns: []               # What the user is worried about
  explicit_domains: []       # Domains explicitly named by user
  explicit_routing: ""       # If user said "multi-model", "debate", "thorough", etc.
  intent: ""                 # What the user wants to accomplish
```

---

## Step 2: Classify Artifact Type

Determine the primary artifact type from signals:

```yaml
artifact_type_rules:
  code:
    signals:
      - File extensions: .go, .py, .ts, .js, .rs, .java, .rb, .kt, .swift, .c, .cpp
      - Mentions of: function, class, module, API, endpoint, service, handler
      - Git references or diff mentions

  financial:
    signals:
      - Terms: P&L, revenue, profit, loss, budget, forecast, balance sheet, ROI, EBITDA
      - Spreadsheet files: .xlsx, .csv with financial column names
      - GAAP, IFRS, accounting mentions

  marketing:
    signals:
      - Terms: campaign, audience, conversion, CTR, CPC, funnel, brand, messaging, copywriting
      - Marketing channel names: email, social, PPC, SEO, content marketing

  research:
    signals:
      - Terms: literature, sources, evidence, citations, study, paper, methodology
      - Academic language patterns
      - Bibliography or reference mentions

  creative:
    signals:
      - Design files: .fig, .sketch, .psd, .ai, .xd
      - Terms: design, visual, layout, color, typography, UX, wireframe, mockup, copy

  mixed:
    signals:
      - Signals from 2+ categories above present simultaneously
```

Artifact type selection:
1. If signals from 2+ types → `mixed`
2. If dominant signals clearly point to one type → that type
3. Default → `code` (most common)

---

## Step 2.5: Enrich Context with DeepWiki (Optional)

If the artifact type is `code` or `mixed` and a GitHub repository can be identified, optionally invoke the `deepwiki` skill to get architectural context before domain selection. This enriches domain detection beyond what file names and conversation signals alone can provide.

**When to invoke:**
- Artifact type is `code` or `mixed`
- Minimal conversation context (low-confidence signals from Step 1)
- User asks about architectural intent, not just file contents
- Repository is large or unfamiliar — conversation signals may not surface all relevant domains

**Invocation:**
```
Skill("deepwiki")
```

Pass the question: `"What are the primary technical domains and architectural concerns of this codebase? What systems, components, or subsystems are involved?"`

**Use the returned answer to:**
- Supplement `explicit_domains` before running domain-registry matching
- Confirm or expand `artifact_type` if the codebase is more complex than conversation signals suggested
- Add technical terms from the answer to the conversation signals for better domain trigger matching

If `deepwiki` returns `availability: "unavailable"` → skip and proceed to Step 3 with signals from Step 1 only. Non-blocking.

---

## Step 3: Select Domains from Domain-Registry

Read the domain-registry files to match detected signals:

```bash
# Read all three domain category files
Read: [skills-root]/domain-registry/domains/technical.md
Read: [skills-root]/domain-registry/domains/business.md
Read: [skills-root]/domain-registry/domains/creative.md
```

Where `[skills-root]` is the parent directory of the skill invoking this step. Resolve by navigating up from the current skill's location using `ls` or `Glob` if needed.

For each domain in the registry files:
- Check if any of the domain's `trigger_signals` appear in the conversation
- Match against: file names, topics, concerns, explicit mentions, technical terms
- Select ALL matching domains (minimum 1, no maximum)

If no domains match clearly:
- For `code` artifact type → default to `api` + `testing`
- For `financial` → default to `finance`
- For `marketing` → default to `marketing`
- For `research` → default to `content`
- For `creative` → default to `design` + `ux`

---

## Step 4: Determine Routing

Apply routing decision rules:

```yaml
routing_rules:
  parallel-workflow:
    conditions:
      - domains_count < 3
      - no high-stakes signals (production incident, financial risk, security breach)
      - no explicit "thorough" or "critical" in user request
    description: "Parallel independent sub-agents, no debate needed"

  debate-protocol:
    conditions_any:
      - domains_count >= 3
      - high_stakes_signals: [production, incident, breach, compliance, audit, lawsuit, financial risk]
      - explicit_signals: ["thorough", "critical", "high-stakes", "careful", "deep"]
    intensity_selection:
      thorough: explicit "thorough" or "critical" in request
      standard: default for debate-protocol routing
      quick: explicit "quick" or "fast" in request
    description: "Structured 5-phase adversarial debate across domains"

  deep-council:
    conditions_any:
      - explicit_signals: ["multi-model", "multiple models", "council", "cross-model"]
      - user explicitly requests multiple AI perspectives
      - intensity = thorough → deep-council (recommended — thorough analysis benefits from multi-model perspectives)
    description: "Multi-model review across Claude, Gemini, Codex, OpenCode bridges"
```

Routing priority: `deep-council` > `debate-protocol` > `parallel-workflow`

---

## Step 5: Determine Confidence and Surface Missing Signals

Check each signal explicitly and record what could not be resolved:

```yaml
signal_resolution:
  artifact_identified: true | false   # specific files/paths/topics clearly present?
  intent_clear: true | false          # review? audit? verify? research? explore?
  domains_detectable: true | false    # can domains be matched from domain-registry?
  scope_bounded: true | false         # is scope narrow enough to proceed without clarification?
```

Build the `missing_signals` list from any signal that resolved to `false`:

```yaml
missing_signal_map:
  artifact_identified: false  →  "artifact"
  intent_clear: false         →  "intent"
  domains_detectable: false   →  "domains"
  scope_bounded: false        →  "scope"
```

Derive overall confidence from the resolved signals:

```yaml
confidence_levels:
  high:    all four signals true  →  preflight_needed: false
  medium:  1 signal false         →  preflight_needed: true  (scope or domains)
  low:     2+ signals false       →  preflight_needed: true  (artifact or intent unresolved)
```

---

## Step 6: Produce Context Report

Output the context report:

```yaml
context_report:
  artifact_type: code | financial | marketing | creative | research | mixed
  topics: []                    # Key topics identified
  concerns: []                  # User concerns identified
  domains: []                   # Selected domain names from domain-registry
  domain_experts: []            # Corresponding expert_role values
  routing: parallel-workflow | debate-protocol | deep-council
  debate_intensity: quick | standard | thorough   # Only if routing = debate-protocol
  confidence: high | medium | low
  preflight_needed: true | false   # true if any signal resolved to false in Step 5
  missing_signals: []              # subset of ["artifact", "intent", "domains", "scope"]
                                   # empty when preflight_needed: false
  rationale: ""                    # Brief explanation of routing decision
  signals_detected:
    files: []
    topics: []
    explicit_mentions: []
```

`missing_signals` is the direct handoff to preflight — it tells preflight exactly which questions to ask, so preflight skips questions for signals that context already resolved.

Display this report to the user and/or return it to the calling skill.

---

## Step 7: Save Artifact

Save context report to `.outputs/context/{YYYYMMDD-HHMMSS}-context.md` with YAML frontmatter:

```yaml
---
skill: context
timestamp: {ISO-8601}
artifact_type: {artifact_type}
domains: [{domain1}, {domain2}]
routing: {routing}
confidence: {confidence}
context_summary: "{brief description of what was analyzed}"
session_id: "{unique id}"
---
```

Also save JSON companion: `{YYYYMMDD-HHMMSS}-context.json`

**No symlinks.** To find the latest artifact:
```bash
ls -t .outputs/context/ | head -1
```

**QMD Integration (optional):**
```bash
qmd collection add .outputs/context/ --name "context-reports" --mask "**/*.md" 2>/dev/null || true
qmd update 2>/dev/null || true
```

---

## Notes

- **Pre-flight pattern**: Other skills can call this at the start to determine routing before spawning agents
- **Progressive enhancement**: If domain-registry is not found, fall back to basic artifact type detection
- **Non-blocking**: Always produces a result, even with low confidence
- **Model-agnostic**: Works in any Claude, Gemini, Codex, or OpenCode context
