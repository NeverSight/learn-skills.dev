---
name: super-skills
description: Decomposes complex user requests into executable subtasks, identifies required capabilities, searches for existing skills, and creates new skills when needed.
version: 1.4.0
author: 10e9928a
tags: [task-decomposition, skill-generation, workflow-automation, orchestration]
trigger: always
---

# Super Skills

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 Core: Understand → Plan → Execute → Iterate             │
│  🚨 Rule: Problem → Analyze → Solve → Continue (NEVER WAIT) │
│  📊 Complexity: 4-8 Direct | 9-14 Staged | 15-20 Iterative  │
└─────────────────────────────────────────────────────────────┘
```

## Core Philosophy

| Principle | Description |
|-----------|-------------|
| **Understand First** | Deeply analyze requirements before acting |
| **Incremental Delivery** | Produce verifiable intermediate results at each step |
| **Expect Failures** | Design recovery mechanisms for every stage |
| **Never Stop** | Solve problems proactively; NEVER pause waiting for user |

## Workflow

```
UNDERSTAND ──→ PLAN ──→ EXECUTE ──→ ITERATE
    │            │          │          │
 Multi-layer  Task       Search &   Feedback
 Analysis     Breakdown  Install    Adjustment
 Complexity   Risk ID    Checkpoint Optimize
```

---

## Phase 1: Understanding

### 1.1 Multi-Layer Analysis

```yaml
understanding:
  surface:    # Literal meaning
    request: "{user's exact words}"
    keywords: [key terms]
    
  intent:     # True intent
    goal: "{what user really wants}"
    success: "{success criteria}"
    
  context:    # Environment
    env: "{OS/language/framework}"
    constraints: "{time/resources/permissions}"
    
  hidden:     # Unstated needs
    assumptions: "{implicit assumptions}"
    edge_cases: "{boundary conditions}"
```

### 1.2 Requirement Handling

| Type | Action |
|------|--------|
| Explicit | Execute directly |
| Implicit | Proactively supplement |
| Ambiguous | State assumptions, choose most likely interpretation |
| Conflicting | Point out conflict, request clarification |
| Out of Scope | Explain why, provide alternatives |

### 1.3 Complexity Score

```
Dimensions (1-5 each):
  technical + scope + uncertainty + dependencies = total

Strategy:
  4-8   → Direct execution
  9-14  → Staged verification
  15-20 → Iterative prototyping
```

### 1.4 Clarification

```
Confidence ≥70%: State assumptions → Continue → Leave adjustment points
Confidence <70%: Provide options for user to choose (NO open-ended questions)
```

---

## Phase 2: Planning

### 2.1 Task Structure

```yaml
task:
  id: 1
  name: "{task name}"
  capability: "{capability type}"
  input: [required inputs]
  output: "{type/format}"
  depends_on: [prerequisite task IDs]
  timeout: "30s"
  retries: 3
  validation: "{success condition}"
  fallback: "{alternative approach}"
```

### 2.2 Dependency Graph

```
[1:Setup] → [2:Auth] → [3:Fetch] ─┐
                                  ↓
[4:Process] ← [5:Transform] ← [6:Parse]
     ↓
[7:Output]

Critical Path: 1→2→3→6→5→4→7
Parallel Opportunities: Independent tasks can run concurrently
```

### 2.3 Capability Map

| Capability | Status | Keywords |
|------------|--------|----------|
| `browser_automation` | ❌ | browser, puppeteer, playwright |
| `api_integration` | ❌ | api, rest, {service} |
| `data_extraction` | ⚠️ | parse, pdf, ocr |
| `message_delivery` | ❌ | slack, discord, email |
| `database_operations` | ❌ | sql, mongodb |
| `deployment` | ❌ | deploy, docker, k8s |
| `data_transformation` | ✅ | — |
| `content_generation` | ✅ | — |
| `code_execution` | ✅ | — |
| `scheduling` | ✅ | — |

✅ Built-in | ⚠️ Complex | ❌ Skill required

---

## Phase 3: Skill Acquisition

```bash
# Search priority
1. npx skills find {service_name}      # Exact match
2. npx skills find {capability} {domain}  # Combined
3. https://skills.sh/                  # Browse

# Install
npx skills add <skill> -g

# On failure: Switch registry → Manual clone → Inline implementation
```

### Evaluation Criteria

| Dimension | Weight |
|-----------|--------|
| Feature match | 40% |
| Documentation quality | 20% |
| Maintenance status | 20% |
| Community validation | 10% |
| Dependency simplicity | 10% |

---

## Phase 4: Risk & Resilience

### 4.1 Risk Matrix

| Risk | Detection | Auto-Resolution |
|------|-----------|-----------------|
| Token expired | 401/403 | Refresh → Re-auth → Degrade |
| Rate limited | 429 | Backoff → Cache → Degrade |
| Timeout | Timeout | Increase → Reduce batch → Chunk |
| Parse error | Parse Error | Switch parser → Regex → Raw text |
| Connection failed | Connection | Retry → Proxy → Offline mode |
| Missing dependency | Import Error | Auto-install → Alternative pkg → Inline |

### 4.2 Resilience Patterns

```yaml
retry:           max=3, backoff=exponential
circuit_breaker: threshold=5, recovery=60s
timeout:         connect=10s, read=30s, total=120s
fallback:        cache | default | skip
```

### 4.3 Checkpoints

```yaml
checkpoint:
  trigger: after_each_task
  content: [task_id, state, data, timestamp]
  recovery: Load checkpoint → Validate → Resume from failure point
```

---

## Phase 5: Execution

### 5.0 🚨 Problem Solving (CRITICAL)

**On problem → Analyze → Solve → Continue. NEVER pause waiting.**

```
Problem → Diagnose type → Analyze cause → Try solutions by priority → Continue
                                          ↓
                            Plan A fails → Plan B → Plan C → Degraded solution
```

#### Auto-Fix Table

| Problem | Auto-Resolution (in order) |
|---------|---------------------------|
| Missing dependency | Install → Alternative pkg → Inline |
| Permission denied | Adjust perms → Alternative path → Minimal perms |
| API failure | Retry (backoff) → Switch endpoint → Cache → Degrade |
| Timeout | Increase timeout → Reduce batch → Chunk → Async |
| Parse error | Switch parser → Regex → Raw text |
| Auth failure | Refresh token → Re-auth → Backup credentials |
| Resource exhausted | Chunk → Clear cache → Stream → Reduce concurrency |
| Network issue | Retry → Switch network → Proxy → Offline |
| File not found | Create → Default value → Skip |

#### Mindset

```yaml
forbidden:
  - "I encountered a problem and need your help"
  - "Execution paused, waiting for instructions"
  
required:
  - "Encountered X issue, trying Y solution"
  - "Plan A failed, switching to Plan B"
  - "Problem resolved, continuing execution"
```

#### Escalation (ONLY when ALL conditions met)

- Tried ≥3 different solutions
- All failed
- Goal completely unachievable
- No acceptable degraded solution available

### 5.1 Execution Modes

| Mode | Use Case |
|------|----------|
| Sequential | Tasks with strong dependencies |
| Parallel | Independent tasks |
| Pipeline | Data stream processing |
| Iterative | Requires feedback loops |

### 5.2 Progress Template

```
══════════════════════════════════════
📊 PROGRESS
══════════════════════════════════════
Phase 1: Setup              [████████░░] 80%
  ✅ Task 1: Initialize     Done (2.3s)
  🔄 Task 2: Fetch          Running...
  ⏳ Task 3: Process        Waiting
──────────────────────────────────────
⏱️ Elapsed: 3m | ETA: ~5m
══════════════════════════════════════
```

---

## Phase 6: Iteration

### Feedback Loop

```
Collect feedback → Analyze issues → Adjust approach → Loop
```

### Adjustment Levels

| Level | Actions |
|-------|---------|
| Minor | Parameter tuning, format adjustment |
| Moderate | Replace skills, add/remove tasks |
| Major | Redesign architecture |

---

## Execution Plan Template

```
════════════════════════════════════════════════════
📋 SUPER SKILLS PLAN
════════════════════════════════════════════════════

🎯 REQUEST: {user's exact words}

📊 UNDERSTANDING
────────────────────────────────────────────────────
Intent:      {true intent}
Success:     {success criteria}
Complexity:  {score} → {strategy}

Assumptions:
  • {assumption 1}
  • {assumption 2}

────────────────────────────────────────────────────
📋 TASKS
────────────────────────────────────────────────────
│ ID │ Task       │ Capability  │ Status │ Risk │
├────┼────────────┼─────────────┼────────┼──────┤
│ 1  │ {task}     │ {capability}│ ✅/📦  │ 🟢/🔴│

Status: ✅ Built-in | 🔧 Found | 📦 Create
Risk:   🟢 Low | 🟡 Medium | 🔴 High

────────────────────────────────────────────────────
🔧 SKILLS
────────────────────────────────────────────────────
npx skills add {skill} -g

────────────────────────────────────────────────────
🛡️ RESILIENCE
────────────────────────────────────────────────────
Checkpoints: □ After Phase 1  □ After Phase 2
Fallbacks:   {task} → {alternative}

────────────────────────────────────────────────────
✅ COMPLETION
────────────────────────────────────────────────────
□ {acceptance criterion 1}
□ {acceptance criterion 2}
════════════════════════════════════════════════════
```

---

## Example: E-commerce Pipeline

```yaml
# "Scrape product data from multiple platforms daily, analyze price trends, send report"

understanding:
  intent: "Automated price monitoring for pricing decisions"
  success: "Daily price trend visualization report received"
  
complexity:
  technical: 4, scope: 4, uncertainty: 3, dependencies: 4
  total: 15 → Iterative prototyping strategy

tasks:
  1. Configure product list  → file_operations ✅
  2. Multi-platform scraping → browser_automation ❌
  3. Data persistence        → database_operations ❌
  4. Data cleaning           → data_transformation ✅
  5. Trend analysis          → code_execution ✅
  6. Generate charts         → content_generation ✅
  7. Generate report         → content_generation ✅
  8. Send email              → message_delivery ❌

resilience:
  checkpoints: [after:2 save:raw_data] [after:5 save:analysis]
  fallbacks:
    task_2: "Skip failed platforms, continue with others"
    task_8: "Save to local file"
```

---

## Error Handling (Every error has auto-resolution)

| Phase | Error | Auto-Resolution |
|-------|-------|-----------------|
| Analysis | Unclear requirements | Choose most likely → State assumptions → Leave adjustment points |
| Analysis | Beyond capability | Search alternatives → Combine capabilities → Partial implementation |
| Planning | Circular dependency | Break weakest link → Merge tasks |
| Search | Skill not found | Expand keywords → Online search → Auto-create |
| Install | Installation failed | Switch registry → Manual clone → Inline implementation |
| Execution | Auth failure | Refresh → Re-auth → Degrade to public data |
| Execution | Rate limited | Backoff → Switch account → Use cache |
| Execution | Timeout | Increase timeout → Reduce batch → Skip and continue |
| Validation | Result mismatch | Retry with adjusted params → Relax validation → Mark for review |

---

## Best Practices

| Phase | Principles |
|-------|------------|
| Understanding | Multi-layer analysis, proactive assumptions, complexity assessment |
| Planning | Architecture first, clear dependencies, upfront risk identification |
| Execution | **NEVER STOP**, try multiple solutions, graceful degradation, incremental verification |
| Iteration | Fast feedback, continuous optimization, knowledge accumulation |

---

## Resources

- CLI: `npx skills --help`
- Browse: https://skills.sh/
- Capabilities: `references/capability_types.md`
- Template: `assets/skill_template.md`
