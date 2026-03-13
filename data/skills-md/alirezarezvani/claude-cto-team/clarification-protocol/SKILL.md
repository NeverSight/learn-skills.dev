---
name: clarification-protocol
description: Generate targeted clarifying questions (2-3 max) that challenge vague requirements and extract missing context. Use after request-analyzer identifies clarification needs, before routing to specialist agents. Helps cto-orchestrator avoid delegating unclear requirements.
---

# Clarification Protocol

Generates focused, challenging questions to extract missing context and clarify vague requirements before routing to specialist agents.

## When to Use

- After request-analyzer identifies vague terms or missing context
- When requirements are ambiguous and could lead to wrong solutions
- Before delegating to cto-architect or strategic-cto-mentor
- When buzzwords need to be translated into specific requirements

## Core Principles

### 1. Maximum 2-3 Questions Per Round

Users lose patience with long questionnaires. Prioritize ruthlessly:
- Ask only what's blocking progress
- Combine related questions
- Defer nice-to-have information

### 2. Challenge Mode, Not Interview Mode

Don't just ask—challenge assumptions:
- Bad: "What scale do you need?"
- Good: "You mentioned 'scalable'—are we designing for 10K users or 10M? That changes the architecture significantly."

### 3. Provide Example Answers

Help users understand what you're looking for:
- Bad: "What's your timeline?"
- Good: "What's your timeline? For context, a robust MVP typically takes 8-12 weeks with a team of 4."

## Question Generation Framework

### Step 1: Prioritize Missing Information

Rank by impact on routing and design:

| Priority | Category | Examples |
|----------|----------|----------|
| **P0** | Blocking | Can't proceed without this (e.g., "What problem does AI solve here?") |
| **P1** | High Impact | Significantly changes approach (e.g., "1K or 100K users?") |
| **P2** | Medium Impact | Affects details but not direction (e.g., "Budget range?") |
| **P3** | Nice to Have | Can be discovered later (e.g., "Preferred cloud provider?") |

**Ask P0 first, then P1. Defer P2/P3.**

### Step 2: Select Question Type

| Type | When to Use | Template |
|------|-------------|----------|
| **Scope** | Vague feature description | "When you say [X], do you mean [A] or [B]?" |
| **Scale** | Missing numbers | "What scale are we designing for? [X] users? [Y] requests/second?" |
| **Timeline** | Vague deadlines | "What's the actual deadline? Is there flexibility if scope changes?" |
| **Constraint** | Unknown limitations | "Are there constraints I should know about? Budget, team size, existing systems?" |
| **Success** | Unclear goals | "How will we know this succeeded? What metrics matter?" |

### Step 3: Frame as Challenge

Transform neutral questions into challenging ones:

| Neutral (Weak) | Challenge (Strong) |
|----------------|-------------------|
| "What do you mean by AI-powered?" | "'AI-powered' can mean many things—are you trying to classify data, generate content, or make predictions? What specific problem are you solving?" |
| "What's your budget?" | "Knowing budget helps me avoid over-engineering. Are we optimizing for < $5K/month or is $50K/month acceptable for the right solution?" |
| "How many users?" | "You mentioned 'scale'—I want to avoid designing for problems you don't have. How many users today, and what's realistic in 12 months?" |

## Output Format

```
## Clarification Needed

Before I route this to the appropriate specialist, I need to understand a few things:

### Challenge 1: [Vague Term/Concept]
[Direct challenge statement]

**Question**: [Specific question]

**Why this matters**: [Impact on design/routing]

**Example answers**:
- Option A: [example] → leads to [approach]
- Option B: [example] → leads to [different approach]

### Challenge 2: [Missing Context]
[...]

---

Once you clarify these points, I'll route to [suggested agent] with a clear brief.
```

## Question Templates by Category

See [question-templates.md](question-templates.md) for comprehensive templates.

See [challenge-patterns.md](challenge-patterns.md) for examples of turning neutral questions into challenges.

## Examples

### Example 1: AI Feature Request

**User Request**: "We want to add AI capabilities to improve customer experience"

**Clarification Output**:

```
## Clarification Needed

Before I route this to cto-architect, I need to understand what "AI capabilities" means for your use case:

### Challenge 1: Vague AI Requirement
"AI capabilities" could mean anything from a chatbot to predictive analytics. I don't want to design the wrong solution.

**Question**: What specific customer problem are you trying to solve with AI?

**Why this matters**: A recommendation engine has completely different architecture than a support chatbot.

**Example answers**:
- "Customers can't find products" → Recommendation engine / search improvement
- "Support tickets are overwhelming" → AI-assisted ticket routing or chatbot
- "Churn is high" → Predictive analytics for at-risk customers

### Challenge 2: Missing Scale
**Question**: How many customers are we talking about? And how many interactions per day would this AI feature handle?

**Why this matters**: 1,000 daily interactions vs 1,000,000 changes whether we use a simple API call or need dedicated ML infrastructure.

---

Once you clarify these points, I'll route to cto-architect with a clear brief for the appropriate AI architecture.
```

### Example 2: Scaling Concerns

**User Request**: "Our app needs to scale better"

**Clarification Output**:

```
## Clarification Needed

"Scale better" is a symptom—I need to understand the disease before prescribing treatment.

### Challenge 1: What's Actually Broken?
**Question**: What specific scaling issue are you experiencing? Slow page loads? Database timeouts? High infrastructure costs? All of the above?

**Why this matters**: Scaling a slow database is different from scaling a CPU-bound API.

**Example answers**:
- "Page loads take 5+ seconds at peak" → Likely caching/CDN solution
- "Database queries timing out" → Database scaling or query optimization
- "AWS bill doubled last month" → Cost optimization vs actual scaling

### Challenge 2: Current vs Target Scale
**Question**: What's your current traffic, and what do you need to support? Be specific: requests per second, concurrent users, data volume.

**Why this matters**: "Scale" at 10K users looks very different from "scale" at 10M users. I don't want to over-engineer.

---

Once I understand the specific bottleneck, I'll route to the appropriate specialist.
```

## Anti-Patterns to Avoid

### 1. The Interrogation
**Bad**: Asking 10 questions at once
**Good**: Max 2-3 targeted questions

### 2. The Open-Ended Trap
**Bad**: "Tell me more about your requirements"
**Good**: "Is this for internal users (hundreds) or external customers (thousands+)?"

### 3. The Assumption Question
**Bad**: "What microservices architecture do you want?" (assumes microservices)
**Good**: "What's your current architecture, and what's driving the need to change?"

### 4. The Jargon Barrier
**Bad**: "What's your CAP theorem preference for the distributed system?"
**Good**: "If the system goes offline briefly, should it prioritize consistency (everyone sees the same data) or availability (the system stays up)?"

## References

- [Question Templates](question-templates.md) - Ready-to-use question templates by category
- [Challenge Patterns](challenge-patterns.md) - Examples of effective challenge framing
