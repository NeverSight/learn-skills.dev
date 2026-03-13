---
name: lev-cdo
description: |
  [WHAT] Graph-based thinking playbook (CDO)
  [HOW] Classifies input by complexity, routes to appropriate workflow (Quick/Base/Deep/Epic)
  [WHEN] Use for design, architecture, and complex problem decomposition requiring multi-perspective analysis
  [WHY] Provides a repeatable thinking playbook instead of ad-hoc brainstorming.

  Triggers: "think", "design", "architect", "complexity", "cdo", "graph", "multi-agent", "deep analysis"
skill_type: playbook
category: process-thinking

lifecycle_integration:
  stage: crystallizing
  input_artifact: report.md
  output_artifact: proposal.md

related_skills:
  - skill://lev-research      # Provides recon for CDO workflows
  - skill://lev-find          # Legacy skill name (`lev get` backend for context gathering before CDO execution)
  - skill://planning          # CDO outputs feed into spec authoring
  - skill://work              # Work owns alignment gate during lifecycle routing
  - skill://lev-ultra         # Routes ultra-mode keywords to CDO

protocol_handlers:
  - lev://cdo?complexity={quick|base|deep|epic}
  - lev://debug?mode=rca

plankton: false
---

# lev-cdo - Graph-Based Agentic Thinking

## Lev Concept

**What is this?**
CDO (Complexity-Driven Orchestration) is a graph-based execution system where agents read/write to disk in structured workflows. Problems are classified by complexity, then routed to appropriate patterns (Quick/Base/Deep/Epic).

**Why does it exist?**
Traditional linear thinking fails for interconnected problems. CDO prevents groupthink by ensuring agents never see each other's work during execution - only the final synthesis step reads all artifacts together.

**When to use it:**
- **Design work** - Architecture decisions, system design
- **Complex debugging** - Root cause analysis with multiple hypotheses
- **Strategic analysis** - Multi-perspective evaluation of decisions
- **Assumption exploration** - Socratic questioning of beliefs
- **Research synthesis** - Integrating findings from multiple sources

**When NOT to use it:**
- Simple questions with known answers → Use Quick workflow or just answer
- Single perspective sufficient → Direct execution
- No complexity/interdependencies → Standard task execution

---

## CLI Commands

### Primary Commands

```bash
# Auto-classify and route to appropriate workflow
lev cdo "{query or problem statement}"

# Force specific complexity level
lev cdo --complexity=quick "{query}"
lev cdo --complexity=base "{query}"
lev cdo --complexity=deep "{query}"
lev cdo --complexity=epic --bd-epic=clawd-xxx "{query}"

# Classification only (no execution)
lev cdo classify "{input}"

# Debug mode (RCA workflow)
lev cdo debug "{error description}"
```

### Examples

```bash
# Example 1: Auto-classify (likely: base)
lev cdo "Should we use GraphQL or REST for the API?"

# Example 2: Force deep complexity
lev cdo --complexity=deep "Explore assumptions behind microservices"

# Example 3: Debug workflow
lev cdo debug "Gateway crashes on Telegram messages"

# Example 4: Epic with BD tracking
lev cdo --complexity=epic --bd-epic=clawd-042 "Evaluate voice assistant architecture"
```

---

## Workflows

### Overview: Four Complexity Levels

| Level | Agents | Turns | Pattern | Use When |
|-------|--------|-------|---------|----------|
| **Quick** | 1-2 | 1 | Sequential | Simple question, single perspective |
| **Base** | 2-3 | 2 | Fan-out/merge | Need 2+ perspectives, then synthesis |
| **Deep** | 3-5 | 3-5 | Multi-turn chains | Root cause analysis, assumption drilling |
| **Epic** | 5+ | 5-10 | BD-tracked phases | Strategic analysis, multi-session work |

**Routing logic:**
```
Confidence ≥0.90 → Quick (direct execution)
Confidence ≥0.80 → Base (fan-out perspectives → synthesis)
Confidence ≥0.60 → Deep (multi-turn chains with convergence)
Confidence <0.60 → Epic (BD-tracked, human-in-loop)
```

---

### Workflow 1: Classification & Routing

**Use case:** First step of every CDO invocation

**Handled by:** `skill://lev-cdo/router`

**Process:**
1. Parse input for intent (question, command, idea, research)
2. Assess confidence (0.0-1.0)
3. Determine complexity (quick, base, deep, epic)
4. Validate DoR (Definition of Ready)
5. Route to appropriate workflow

**DoR Gates:**
- Sanity check (problem/solution alignment)
- Prior art check (search for existing implementations)
- Architecture compliance (YAML-first, LLM-first principles)
- Scope validation (user approval for high-effort work)

**See:** `lev-cdo/router/SKILL.md` for full details

---

### Workflow 2: Quick (1-2 agents, 1 turn)

**Example:** "Summarize this document"

**Execution:**
```
Agent: Read 00-input.md → Write FINAL-summary.md
```

**Convergence:** Single output, no iteration

---

### Workflow 3: Base (2-3 agents, 2 turns)

**Example:** "Analyze pros and cons of X"

**Pattern:** Fan-out (parallel perspectives) → Merge (synthesis)

**Execution:**
```
Turn 1 (parallel):
  Agent A: Argue FOR → 01a-pros.md
  Agent B: Argue AGAINST → 01b-cons.md

Turn 2:
  Agent C: Synthesize → FINAL-analysis.md
```

**Convergence:** All perspectives collected + synthesis complete

---

### Workflow 4: Deep (3-5 agents, 3-5 turns)

**Example:** "Explore foundational assumptions behind belief X"

**Pattern:** Multi-turn chains (socratic drilling, debate, synthesis)

**Execution:**
```
Turn 1: Paraphrase belief clearly
Turn 2: Steelman (strengthen before critique)
Turn 3: Dig axioms (3-level socratic drilling)
Turn 4: Map elements (extract components)
Turn 5: Multi-devils debate (FOR/AGAINST/INTEGRATE)
Turn 6: Synthesize findings
Turn 7: Reflection loop (meta-analysis)
```

**Convergence:** All turns complete + confidence ≥0.80

**See:** `lev-cdo/workflows/SKILL.md` for full examples

---

### Workflow 5: Epic (5+ agents, 5-10 turns, BD-tracked)

**Example:** "Should we bet on technology X? Full strategic analysis."

**Pattern:** BD-tracked phases with dependencies

**Execution:**
```
Phase 1: Research (ergodicity, lindy-effect, cynefin)
  → BD: clawd-xxx.1

Phase 2: Analysis (dig-axioms, morphological, TRIZ-40)
  → BD: clawd-xxx.2 (depends on Phase 1)

Phase 3: Synthesis (resonance loop until convergence)
  → BD: clawd-xxx.3 (depends on Phase 2)

Phase 4: Output (synthesize-apply, reflection-loop)
  → BD: clawd-xxx.4 (depends on Phase 3)
```

**Convergence:** All BD milestones closed + final report approved

**See:** `lev-cdo/workflows/SKILL.md` for Epic patterns

---

### Workflow 6: Debug RCA (7-step systematic debugging)

**Triggered by:** "uld", "ultradebug" keywords

**Handled by:** `skill://lev-cdo/debug`

**Steps:**
1. REPRODUCE - Define exact failure
2. ISOLATE - Narrow to minimal case
3. TRACE - Find call path + working code
4. HYPOTHESIZE - Form 2-3 theories
5. VERIFY - Test hypotheses with evidence
6. FIX - Apply minimal fix (NO scope creep)
7. VALIDATE - Adversarial validation (ralph)

**Convergence:** All 7 steps complete + PASS verdict

**See:** `lev-cdo/debug/SKILL.md` for full RCA workflow

---

## Relates (Cross-References)

### Depends On
- `skill://lev-research` - Provides recon before CDO execution
- `skill://lev-find` - Context gathering (legacy skill name for `lev get` backend; prior art, existing patterns)
- `skill://bd` - Epic tracking for multi-session workflows

### Works With
- `skill://planning` - CDO outputs (proposals) feed into spec authoring
- `skill://work` - Alignment and lifecycle gates run in `work`
- `skill://ralph` - Adversarial validation for debug workflows

### Blocks/Enables
- **Blocks:** Execution until DoR validation passes
- **Enables:** Multi-perspective analysis without groupthink

### Lifecycle Position
- **Before:** Raw problem statement or user query
- **After:** FINAL-synthesis.md → proposal.md or report.md
- **Parallel:** Can run multiple CDO workflows simultaneously (different problems)

---

## Sub-Skills Reference

CDO is organized into 4 sub-skills for progressive disclosure:

### 1. router/SKILL.md - Classification & Routing
**Content:**
- Classification logic (intent, confidence, complexity)
- DoR validation gates (4 gates)
- Routing decision table
- Message footer protocol

**Use when:** Understanding how CDO routes work

---

### 2. workflows/SKILL.md - Execution Patterns
**Content:**
- Quick/Base/Deep/Epic workflow examples
- Convergence criteria (critical for avoiding infinite loops)
- Resonance loops
- Agent dispatch patterns
- BD integration for Epic workflows

**Use when:** Building or executing CDO workflows

---

### 3. debug/SKILL.md - RCA Workflow
**Content:**
- 7-step debug template (REPRODUCE → VALIDATE)
- Integration with lev-ultra router
- Minimal fix anti-scope-creep patterns

**Use when:** Debugging complex issues systematically

---

### 4. skill-discovery/SKILL.md - lev-catalog Integration
**Content:**
- Semantic search for skills (axioms, hidden-gems)
- Tag-based browsing
- Discovery-first workflow construction
- 40+ skill catalog reference

**Use when:** Building Deep/Epic workflows from scratch

---

## Quick Start

### Step 1: Classification
```bash
lev cdo classify "Should we migrate to microservices?"
```

**Output:**
```yaml
intent: question
confidence: 0.75
complexity: base
route_to: workflows/base
```

---

### Step 2: Execution
```bash
lev cdo "Should we migrate to microservices?"
```

**Process:**
1. Router classifies (complexity: base)
2. Validates DoR (prior art check, architecture compliance)
3. Dispatches Base workflow:
   - Turn 1: Parallel (argue-for, argue-against)
   - Turn 2: Synthesis
4. Outputs: FINAL-analysis.md

---

### Step 3: Review Output
```bash
cat tmp/microservices-analysis-20260128/FINAL-analysis.md
```

**Contains:**
- Pros (from Turn 1a)
- Cons (from Turn 1b)
- Synthesis with recommendation

---

## Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| Use CDO for simple questions | Direct answer or Quick workflow |
| Skip DoR validation | Always validate before Deep/Epic |
| Let orchestrator synthesize | Dispatch separate synthesis agent |
| Build workflows from scratch | Use skill-discovery to find existing patterns |
| Run Deep without convergence criteria | Define exit conditions upfront |

---

## Related Documentation

**Architecture:**
- BD Issue: lev-001b (lev-core Unified Orchestration)
- Protocol: skill:// (lev-2598), lev:// (lev-pno8)
- Proof of Concept: `~/lev/workshop/poc/skills/tmp/axiom-*/`

**Integration:**
- lev-ultra router: Routes ultra-mode keywords (uld, ult, ulr, ulw)
- BD tracking: Epic workflows create BD structure
- FlowMind: YAML-first compilation (not runtime consumer)

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-cdo, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
