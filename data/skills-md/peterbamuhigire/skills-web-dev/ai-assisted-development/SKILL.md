---
name: ai-assisted-development
description: Orchestrate AI agents (Claude Code, sub-agents, etc.) for software development workflows. Use when coordinating multiple AI assistants or planning AI-driven development processes.
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# AI-Assisted Development Orchestration

## Overview

Learn to **orchestrate multiple AI agents** (like Claude Code, custom sub-agents, or specialized AI tools) to work together effectively in software development.

This skill bridges **prompting patterns** + **orchestration** + **sub-agent coordination** for real-world AI-assisted development.

**What you'll learn:**
- The 5 orchestration strategies for AI development
- AI-specific coordination patterns (Agent Handoff, Fan-Out/Fan-In, Human-in-the-Loop)
- Real-world examples (MADUUKA, BRIGHTSOMA apps)

**Documentation Structure (Tier 2 Deep Dives):**
- 📖 **[orchestration-strategies.md](references/orchestration-strategies.md)** - The 5 core strategies with detailed examples
- 📖 **[ai-patterns.md](references/ai-patterns.md)** - AI-specific orchestration patterns
- 📖 **[practical-examples.md](references/practical-examples.md)** - Real MADUUKA and BRIGHTSOMA projects

---

## When to Use This Skill

✅ **USE when:**
- Coordinating multiple AI agents on a single project
- Planning complex features with AI assistance
- Creating workflows that involve AI + human collaboration
- Setting up multi-agent development pipelines
- Optimizing AI-assisted development processes

❌ **DON'T USE when:**
- Single simple task with one AI agent (just use that agent directly)
- Manual development without AI assistance
- Basic prompting (use `prompting-patterns-reference.md` instead)

---

## Core Concepts (Quick Reference)

### 1. AI Agent (Definition)
An **AI agent** is a specialized AI assistant that handles ONE category of work.

**Examples:**
- **Planning Agent:** Analyzes requirements, creates specs
- **Coding Agent:** Writes implementation code
- **Testing Agent:** Creates test cases
- **Review Agent:** Reviews code quality
- **Documentation Agent:** Writes documentation

**Each agent has focused expertise and context.**

### 2. Orchestration (for AI Development)
**Orchestration** = Coordinating multiple AI agents to work on a project together.

**Example workflow:**
```
Planning Agent: Create feature spec
    ↓ (spec output)
Coding Agent: Implement feature (uses spec as input)
    ↓ (code output)
Testing Agent: Create tests (uses code as input)
    ↓ (tests output)
Review Agent: Review everything (uses spec + code + tests)
    ↓
Human: Approve and deploy
```

### 3. Execution Strategies
- **Sequential:** One agent after another (most common)
- **Parallel:** Multiple agents working simultaneously (50-70% faster)
- **Conditional:** Different agents based on project type
- **Looping:** Iterate until quality threshold met
- **Retry:** Re-run agent if output unsatisfactory

---

## The 5 Orchestration Strategies (Summary)

**📖 See [orchestration-strategies.md](references/orchestration-strategies.md) for complete details with code examples.**

### Strategy 1: Sequential AI Workflow

**Use when:** Each AI agent needs previous agent's output

**Pattern:**
```
Agent 1 (Planning) → Spec
    ↓
Agent 2 (Coding) → Code
    ↓
Agent 3 (Testing) → Tests
    ↓
Agent 4 (Review) → Feedback
```

**Example:** Feature development pipeline (planning → coding → testing → review)

**Time:** 60 minutes (15 + 25 + 15 + 5)

---

### Strategy 2: Parallel AI Execution

**Use when:** AI agents work on independent components

**Pattern:**
```
                ┌─→ Agent 2a: Backend ──┐
Agent 1 (Spec) ─┼─→ Agent 2b: Frontend ─┼─→ Agent 3 (Integration)
                └─→ Agent 2c: Docs ─────┘
```

**Example:** Full-stack feature (backend + frontend + docs simultaneously)

**Time:** 20 minutes parallel (vs 60 sequential) = **67% faster**

---

### Strategy 3: Conditional AI Routing

**Use when:** Different AI agents handle different project types

**Pattern:**
```
Analyze Project
  │
  ├─ IF (legacy) → Refactoring Agent
  ├─ ELIF (greenfield) → Architecture Agent
  ├─ ELIF (API) → Integration Agent
  └─ ELSE → Ask human
```

**Example:** Documentation generation based on project type

---

### Strategy 4: Looping AI Iteration

**Use when:** AI agent needs to refine output until quality threshold met

**Pattern:**
```
┌──────────────────┐
│ Agent generates  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Quality >= 80%?  │◄──┐
│ YES → Done       │   │
│ NO → Refine      │───┘
└──────────────────┘
(max 3 iterations)
```

**Example:** Code generation with quality loop (syntax → style → tests)

---

### Strategy 5: Retry with Fallback

**Use when:** AI agent might fail due to external dependencies

**Pattern:**
```
Attempt 1 → Success? YES → Done
            ↓ FAIL (wait 5s)
Attempt 2 → Success? YES → Done
            ↓ FAIL (wait 10s)
Attempt 3 → Success? YES → Done
            ↓ FAIL
Fallback → Degraded mode
```

**Example:** External API integration (fetch schema, retry on timeout, use cache if all fail)

---

## The 3 AI Orchestration Patterns (Summary)

**📖 See [ai-patterns.md](references/ai-patterns.md) for complete details with code examples.**

### Pattern 1: Agent Handoff (Pipeline)

**Use case:** One AI agent completes work, passes output to next AI agent

**Flow:**
```
Agent A → Output → Agent B → Output → Agent C → Done
```

**Example:** Requirements Agent → Specification Agent → Implementation Agent

**Key principle:** Each agent's output is next agent's input

---

### Pattern 2: Fan-Out/Fan-In (Parallel + Combine)

**Use case:** Split work across multiple AI agents, then combine results

**Flow:**
```
                ┌─→ Agent A ──┐
Input (split) ──┼─→ Agent B ──┼─→ Combine → Output
                └─→ Agent C ──┘
```

**Example:** Multi-component documentation (database + API + UI docs in parallel, then combine)

**Speedup:** 50-70% faster than sequential

---

### Pattern 3: Human-in-the-Loop (Gated Approval)

**Use case:** AI agents generate work, human approves before continuing

**Flow:**
```
Agent 1 → Output → [HUMAN REVIEW] → Approved? YES → Agent 2
                                                 ↓ NO
                                              Revise
```

**Example:** Spec → [Review] → Code → [Review] → Tests → [Review] → Deploy

**Benefits:** Safety, quality control, compliance, learning

---

## Quick Reference: When to Use Which

| Strategy/Pattern      | Use When                                    | Benefit                     |
|-----------------------|---------------------------------------------|-----------------------------|
| Sequential            | Each agent needs previous output            | Simple, predictable         |
| Parallel              | Independent components                      | 50-70% faster               |
| Conditional           | Different project types                     | Right agent for the job     |
| Looping               | Quality threshold must be met               | High-quality output         |
| Retry                 | External dependencies might fail            | Graceful error handling     |
| Agent Handoff         | Pipeline of transformations                 | Clear traceability          |
| Fan-Out/Fan-In        | Parallel work + combine                     | Maximum speed               |
| Human-in-the-Loop     | High-risk or critical features              | Safety + quality control    |

---

## Real-World Examples (Summary)

**📖 See [practical-examples.md](references/practical-examples.md) for complete detailed walkthroughs.**

### Example 1: MADUUKA - Franchise Inventory Sync

**Project:** Multi-tenant franchise inventory management

**Orchestration used:**
- Sequential (Requirements → Implementation → Testing → Review)
- Parallel (Database + API + Tests simultaneously)
- Human-in-the-Loop (3 approval gates)

**Agents:**
1. Requirements Agent: Create spec (15 min)
2. Database Agent: Schema + models (20 min) ─┐
3. API Agent: Endpoints + validation (20 min) ├─→ Parallel
4. Testing Agent: Tests (20 min) ─────────────┘
5. Integration Agent: Run tests (10 min)
6. Review Agent: Quality check (15 min)

**Result:** **75 minutes** (vs 115 sequential) = **35% faster**

---

### Example 2: BRIGHTSOMA - AI Exam Generation

**Project:** AI-powered exam question generator

**Orchestration used:**
- Looping (Generate questions until quality >= 80%)
- Retry (Handle AI API failures)
- Sequential (Generator → Rubrics → PDF)

**Agents:**
1. Question Generator: 17 questions with quality loops (30 min)
2. Validator: Check quality (embedded in loop)
3. Rubric Generator: Grading rubrics (10 min)
4. PDF Generator: Formatted exam + answer key (5 min)

**Result:** **45 minutes** (vs 180 manual) = **75% faster** + higher quality

---

## Practical Workflow: How to Apply This Skill

### Step 1: Analyze Your Task

**Questions to ask:**
- How many components does this feature have?
- Can any work be done in parallel?
- Are there external dependencies (APIs, databases)?
- Is this high-risk (needs human approval)?
- What's the quality threshold?

### Step 2: Choose Orchestration Strategies

**Based on analysis:**
- **Sequential dependencies?** → Use Sequential strategy
- **Independent components?** → Use Parallel strategy
- **Different project types?** → Use Conditional strategy
- **Quality threshold?** → Use Looping strategy
- **External APIs?** → Use Retry strategy

**Combine multiple strategies for complex projects.**

### Step 3: Design Agent Workflow

**Define agents:**
- What does each agent do? (ONE job each)
- What input does each need?
- What output does each produce?
- What's the execution order?

**Example:**
```markdown
Agent 1: Planning Agent
  Input: User requirements
  Output: docs/specs/feature-spec.md
  Execution: Sequential (first)

Agent 2a: Backend Agent
  Input: docs/specs/feature-spec.md
  Output: Backend code
  Execution: Parallel with 2b and 2c

Agent 2b: Frontend Agent
  Input: docs/specs/feature-spec.md
  Output: Frontend code
  Execution: Parallel with 2a and 2c

Agent 2c: Testing Agent
  Input: docs/specs/feature-spec.md
  Output: Test files
  Execution: Parallel with 2a and 2b

Agent 3: Integration Agent
  Input: Backend + Frontend + Tests
  Output: Integrated feature
  Execution: Sequential (after 2a, 2b, 2c)
```

### Step 4: Write Clear Prompts

**Use prompting patterns** (see `prompting-patterns-reference.md`):

```markdown
"[TASK]

FILE TO READ: [input file from previous agent]

CONTEXT: [Why this is needed, what it builds on]

ORCHESTRATION: [Sequential/Parallel/Conditional/Looping/Retry]
[Dependencies or parallel info]

CONSTRAINTS:
- [Technical constraint 1]
- [Limit 2]
- [Standard 3]

OUTPUT: [Expected output files/format]"
```

### Step 5: Add Human Gates (if needed)

**For high-risk work:**
```
Agent → Output → [HUMAN REVIEW] → Approved? → Next agent
```

**What to check:**
- Security implications
- Business logic correctness
- Compliance requirements
- Performance concerns

### Step 6: Execute and Monitor

**Track:**
- Which agent is running
- What output was produced
- Quality metrics (if looping)
- Time spent per agent
- Any failures or retries

**Log everything** for debugging and optimization.

---

## Best Practices

### DO:
✅ **Break work into focused agents** - Each agent does ONE job well
✅ **Parallelize when possible** - 50-70% faster execution
✅ **Add quality loops** - Don't accept poor output
✅ **Include human gates** - High-risk work needs approval
✅ **Handle failures gracefully** - Retry with backoff, have fallbacks
✅ **Provide clear context** - Each agent gets spec, input files, orchestration info
✅ **Log everything** - Agent interactions, decisions, outputs
✅ **Combine strategies** - Use multiple for complex projects

### DON'T:
❌ **Don't over-orchestrate simple tasks** - Sometimes 1 agent is enough
❌ **Don't parallelize dependent work** - Causes race conditions
❌ **Don't skip quality validation** - AI output needs verification
❌ **Don't forget exit conditions** - Loops must end
❌ **Don't assume AI is perfect** - Plan for failures
❌ **Don't skip human review** - Critical features need oversight

---

## Integration with Other Skills

- **feature-planning:** Use AI agents to execute implementation plans
- **prompting-patterns-reference:** Better prompts = better agent output
- **orchestration-patterns-reference:** General orchestration concepts
- **custom-sub-agents:** Create specialized AI agents

---

## Summary

**AI-assisted development orchestration delivers:**
- **30-75% faster** development (parallelization + automation)
- **Higher quality** output (validation loops, human gates)
- **Better consistency** (AI follows patterns reliably)
- **Reduced errors** (validation catches issues early)

**Key concepts:**
- Break work into focused agents (ONE job each)
- Use 5 orchestration strategies (Sequential, Parallel, Conditional, Looping, Retry)
- Apply 3 AI patterns (Agent Handoff, Fan-Out/Fan-In, Human-in-the-Loop)
- Combine strategies for complex projects
- Always include quality validation and human oversight

**Next steps:**
1. 📖 Read [orchestration-strategies.md](references/orchestration-strategies.md) for detailed strategy examples
2. 📖 Read [ai-patterns.md](references/ai-patterns.md) for AI-specific patterns
3. 📖 Read [practical-examples.md](references/practical-examples.md) for real MADUUKA and BRIGHTSOMA walkthroughs
4. Apply to your own projects!

---

**Related Skills:**
- `feature-planning/` - Create implementation plans that AI agents can execute
- `prompting-patterns-reference.md` - Better prompts for better AI output
- `orchestration-patterns-reference.md` - General orchestration concepts
- `custom-sub-agents/` - Create specialized AI agents

**Last Updated:** 2026-02-07
**Line Count:** ~490 lines (compliant with doc-standards.md)
