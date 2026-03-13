---
name: elon-musk
description: Apply First Principles Thinking to break problems into fundamentals and redesign solutions from truth-level constraints. Includes domain research, assumption deconstruction, redesign, and inversion-based execution planning.
---

# Elon Musk Skill

> First Principles Thinking: solve problems by reasoning from fundamentals, not analogy.

---

<when_to_use>

## When to use

| Situation | Example |
|------|------|
| **Only obvious answers appear** | "Need revenue growth -> ads?" |
| **Cost/structure innovation** | "How do we cut infrastructure cost?" |
| **Challenge assumptions** | "We always do it this way" |
| **Strategic decisions** | "A vs B decision" |
| **Market entry design** | "Should we copy competitors?" |

## Invocation

```bash
/elon-musk SaaS pricing is crowded and undifferentiated
/elon-musk infrastructure cost is 40% of revenue
/elon-musk churn is high and retention playbooks are failing
```

## Outputs

- Assumption deconstruction matrix (constraint vs convention vs unverified)
- Comparison table (analogy-based vs first-principles approach)
- Innovative solution options rebuilt from fundamentals
- Execution plan and risk matrix using inversion/pre-mortem

</when_to_use>

---

<argument_validation>

## Required ARGUMENT check

```
If $ARGUMENTS is missing, ask immediately:

"Which problem should we deconstruct using first principles?

Examples:
- Cost innovation: 'SaaS infra cost is 40% of revenue'
- Strategy: 'Only generic market-entry options are visible'
- Assumption challenge: 'We always did it this way, but not sure it is right'
- Technical choice: 'Options look similar; need fundamental differences'"

If $ARGUMENTS exists, continue.
```

</argument_validation>

---

<core_philosophy>

## First Principles Thinking

### Core idea

> Analogy-based thinking copies and slightly modifies existing patterns.
> First-principles thinking decomposes to what is fundamentally true, then rebuilds.

| Dimension | Analogy-based | First principles |
|------|------|------|
| Method | Copy and tweak | Decompose then reconstruct |
| Question | "How do others do this?" | "What is undeniably true?" |
| Outcome | Incremental optimization | Potentially disruptive innovation |
| Effort | Lower cognitive load | Higher cognitive load |
| Best fit | Routine decisions | Breakthrough / blocked situations |

### Typical cases

| Case | Conventional assumption | First-principles decomposition | Result |
|------|------|------|------|
| Space launch | "Rockets are inherently expensive" | Raw material is a small fraction of sell price | Major cost compression |
| EV battery | "Battery packs are fixed-cost expensive" | Component-level material and process decomposition | New cost curve possibilities |

### Supporting methods

| Method | Role | Phase |
|------|------|------|
| Socratic questioning | Assumption deconstruction tool | Phase 2 |
| Inversion | "How do we fail?" reverse risk planning | Phase 4 |
| Pre-mortem | "If we fail in 6 months, why?" | Phase 4 |

</core_philosophy>

---

<workflow>

## Execution flow

| Phase | Task | Tool | Core intent |
|-------|------|------|------|
| **0** | Input + environment check | ToolSearch | detect MCP/tool availability |
| **1** | Domain research (convention + facts + innovation cases) | parallel researcher x3 | collect 3 lenses simultaneously |
| **2** | Assumption deconstruction (Socratic questions + A/B/C) | Sequential Thinking (5-7) | separate constraints from habits |
| **3** | Fundamental redesign | parallel analyst x3 | explore 3-5 alternative paths |
| **4** | Execution + risk | Sequential Thinking (3-5) | inversion and pre-mortem |
| **5** | Save + present | Write | `.hypercore/first-principles/` |

### Complexity profile

| Complexity | Phase 2 depth | Phase 4 depth | Criteria |
|------|------|------|------|
| Simple | 3 thoughts | 2 thoughts | single domain, <=3 assumptions |
| Medium | 5 thoughts | 3 thoughts | multi-domain, 5-7 assumptions |
| Complex | 7+ thoughts | 5 thoughts | industry-level, 10+ assumptions |

</workflow>

---

<sourcing_strategy>

## Search channel strategy

Use Tier-1 MCP channels first, and fallback to built-in web tools when unavailable.

### Phase 0: MCP detection

```
ToolSearch("firecrawl")
ToolSearch("searxng")
ToolSearch("github")

If MCP is available -> pass MCP context into researcher prompts.
If MCP is unavailable -> use WebSearch/WebFetch fallback.
```

</sourcing_strategy>

---

<parallel_agent_execution>

### Priority: Agent Teams for complex parallel work

- If Agent Teams is available: TeamCreate -> spawn workers -> parallel collaboration.
- If not available: parallel Task calls as fallback.

### Phase 1: Parallel domain research (3 directions)

| Agent | Type | Goal | Source requirement |
|------|------|------|------|
| 1-A | researcher | Industry conventions and default approaches | URL + publish date + source type |
| 1-B | researcher | Hard facts/data: cost, benchmarks, constraints | URL + publish date, prefer last 12 months |
| 1-C | researcher | Innovation cases that broke assumptions | URL + publish date |

### Phase 3: Parallel alternative-path analysis

| Agent | Type | Evaluation criteria |
|------|------|------|
| 3-A | analyst | feasibility, impact, resources, risk |
| 3-B | analyst | feasibility, impact, resources, risk |
| 3-C | analyst | feasibility, impact, resources, risk |

### Model routing

| Phase | Agent | Model | Why |
|-------|------|------|------|
| 1 | researcher x3 | sonnet | web-fact collection |
| 2 | Sequential Thinking | main | Socratic decomposition |
| 3 | analyst x3 | sonnet | path feasibility analysis |
| 4 | Sequential Thinking | main | inversion and pre-mortem |

</parallel_agent_execution>

---

<phase_details>

## Phase 2: Assumption deconstruction (core)

### Socratic 6-question set

Apply to each convention collected in Phase 1:

| Question type | Prompt | Purpose |
|------|------|------|
| Clarification | "What exactly does this mean?" | make assumption explicit |
| Assumption probe | "What are we assuming?" | reveal hidden premises |
| Evidence test | "What evidence proves this?" | separate fact from belief |
| Perspective shift | "What other frame exists?" | break fixation |
| Implication test | "If false, what changes?" | evaluate removal impact |
| Meta question | "Why did we accept this as normal?" | expose inertia |

### Required A/B/C classification

| Class | Mark | Definition | Treatment |
|------|------|------|------|
| Physical/technical constraints | A | natural law, hard technical limits | keep as fundamentals |
| Habitual convention | B | "because industry does it" | remove |
| Needs validation | C | testable but not yet confirmed | verify with search/data |

### Phase 2 sequential-thinking template

```
thought 1: extract 5-10 assumptions from Phase 1 material
thought 2: apply Socratic questions and initial A/B/C labels
thought 3: cross-check C items with known facts
thought 4: run extra search for unresolved C items
thought 5: finalize classification and deconstruction matrix
```

---

## Phase 3: Fundamental redesign

### Input

- A items: true constraints
- B items: removed conventions

### Process

```
1. Keep only A constraints; strip B assumptions.
2. Re-ask: "If we design from these truths only, what changes?"
3. Explore 3-5 alternatives in parallel.
4. Build "current vs first-principles" comparison table.
5. Select best path with explicit rationale.
```

---

## Phase 4: Execution and risk

| Method | Question | Process |
|------|------|------|
| Inversion | "How do we fail for sure?" | enumerate 5-7 failure paths and map preventions |
| Pre-mortem | "If we fail in 6 months, why?" | identify top causes and preemptive controls |

</phase_details>

---

<document_storage>

## Result storage

| Item | Rule |
|------|------|
| Path | `.hypercore/first-principles/[number].[problem_summary].md` |
| Numbering | `ls .hypercore/first-principles/ | wc -l` |
| Flow | ensure folder -> Write -> return saved path |

</document_storage>

---

<result_structure>

## Output structure

| Section | Content |
|------|------|
| Header | date, problem statement |
| 1. Domain snapshot | conventions, facts, innovation cases (URLs required) |
| 2. Deconstruction matrix | assumptions + Socratic checks + A/B/C + evidence |
| 3. Fundamental redesign | current vs first-principles comparison and chosen path |
| 4. Execution + risk | action plan, inversion failures, pre-mortem |
| Sources | full URL list |

</result_structure>

---

<examples>

## Core example: cost innovation

```bash
User: /elon-musk infrastructure cost is 40% of SaaS revenue

Phase 0: detect MCP/tools
Phase 1: researcher x3 in parallel
  - conventions: "standard cloud cost structure"
  - facts: compute/network unit economics (recent data)
  - innovation cases: cost-disruptive infra companies

Phase 2: Sequential Thinking
  assumption 1: "Current provider is always optimal" -> B
  assumption 2: "Serverless is always cheaper" -> C -> B after verification
  assumption 3: "Latency constraints are physical" -> A

Phase 3: analyst x3 parallel alternatives
  A: bare metal + automation
  B: hybrid reserved + serverless cold path
  C: edge compute migration

Phase 4: inversion + pre-mortem
  risk: migration downtime -> blue/green rollout
  risk: ops complexity -> automation-first controls

Save: .hypercore/first-principles/00.saas_infra_cost_innovation.md
```

</examples>

---

<validation>

## Validation checklist

| Item | Required |
|------|------|
| ARGUMENT | Ask if missing |
| Phase 0 | MCP/tool availability checked |
| Phase 1 | researcher x3 (convention + facts + cases), source grading |
| Phase 2 | Sequential Thinking 3+ steps, 5+ A/B/C items, 2+ fact cross-checks |
| Phase 3 | analyst x3, comparison table included |
| Phase 4 | inversion 3+ risks, pre-mortem included |
| Save | `.hypercore/first-principles/` |
| Sources | URL + date + source type for factual claims |

| Forbidden |
|------|
| Start without ARGUMENT |
| Deconstruct assumptions without domain research |
| Redesign without A/B/C matrix |
| Execution plan without inversion/pre-mortem |
| Factual claims without sources |
| Pure analogy/copy strategy |
| Exit without saving results |

</validation>
