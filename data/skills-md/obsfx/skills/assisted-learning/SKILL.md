---
name: assisted-learning
description: >
  Assisted learning skill for JavaScript developers exploring new technologies.
  Use when the user wants to learn, understand, or explore a new programming language
  (Elixir, Swift, Go, Rust, Python, etc.), a new tool or platform (Kubernetes, Docker,
  Terraform, Redis, Kafka, etc.), or a new architectural approach or paradigm
  (containerization, microservices, object pooling, distributed systems, event sourcing,
  CQRS, DDD, etc.). Triggers on: "teach me", "explain", "how does X work",
  "X for JavaScript developers", "learn X", "what is X", "compare X to JS",
  "I want to understand X", "show me how X works", "help me learn", "bridge from JS to X",
  "what's the equivalent of X in Y", or any question about unfamiliar technology from a
  JS developer's perspective. Does NOT generate project code — provides explanations,
  comparisons, diagrams, and insights. Stores learning progress in trekker as persistent
  memory across sessions.
---

# Assisted Learning

Teach new technologies to JavaScript developers through side-by-side comparisons, ASCII diagrams, real-world examples, and industry-standard recommendations. Store learning progress in trekker for cross-session continuity.

**Target audience:** JavaScript/TypeScript developers.
**Output:** Explanations, comparisons, diagrams, insights. NOT code generation or scaffolding.

---

## Workflow

```
User asks about a topic
        |
        v
  Classify topic type
        |
        v
    ┌───┴───────────────┐
    |    Type?           |
    └───┬───────┬───────┘
        |       |       |
   Language   Tool   Approach
        |       |       |
        v       v       v
  Load ref   Load ref  Load ref
        |       |       |
        └───┬───┘───────┘
            v
  Research via context7 + web search
            |
            v
    Map to JS mental models
            |
            v
  Build side-by-side comparison
            |
            v
    Create ASCII diagrams
            |
            v
  Identify recommended approach
            |
            v
    Present with insights
            |
            v
     Store in trekker
```

## Topic Classification

Determine which type the user is learning:

| Type | Signal | Reference File |
|------|--------|---------------|
| **Language** | "learn Elixir", "Swift vs JS", "Go syntax" | [language-learning.md](references/language-learning.md) |
| **Tool** | "how does K8s work", "explain Docker", "Redis" | [tool-learning.md](references/tool-learning.md) |
| **Approach** | "what is CQRS", "microservices", "event sourcing" | [approach-learning.md](references/approach-learning.md) |

Load the matching reference file for templates and patterns. If mixed (e.g., "learn Elixir's OTP supervision" = language + approach), load both.

## Core Process

### Step 1: Check Trekker for Prior Learning

Before teaching, check if the user has learned this topic before:

```
trekker search "[topic]" --type epic,task,comment
```

If prior learning exists, resume from where they left off. Do NOT re-explain understood concepts.

### Step 2: Research First

Do NOT rely solely on trained knowledge. Always verify with live sources.

```
context7: resolve-library-id --> context7: query-docs ──┐
                                                        v
WebSearch: current best practices ───────> Synthesize findings
                                                        |
                                                        v
                                              Present with citations
```

- **context7** — `resolve-library-id` then `query-docs` for official documentation, API references, code examples
- **WebSearch** — current best practices, community conventions, recent changes, version-specific info

Refresh knowledge every session. APIs change, conventions evolve, libraries get deprecated.

### Step 3: Map to JS Mental Models

Find the closest JavaScript concept for everything.

**Rules:**
- Every new concept MUST have a JS comparison (or explicit "no JS equivalent — new concept")
- Use the developer's vocabulary: "Think of X as Y but with Z difference"
- Start from what they know, bridge to what they don't
- Acknowledge where the analogy breaks down

### Step 4: Side-by-Side Comparison

Follow the comparison template from the loaded reference file.

**Structure every comparison as:**
1. JS approach (what you know)
2. Target approach (what's new)
3. Key difference (the paradigm shift)
4. Gotcha (common mistake JS devs make)
5. Industry standard (which way passes code review)

### Step 5: ASCII Diagrams

Include at least one ASCII diagram per major concept:

| Context | Diagram Style | Use For |
|---------|--------------|---------|
| Architecture | Box-and-arrow flow | System structure, data flow |
| Lifecycle | Vertical sequence | Request/response, event flow |
| Decision | Diamond branching | When to use X vs Y |
| Comparison | Side-by-side columns | Before/after, JS vs target |
| State | State transition arrows | State machines, lifecycle |

### Step 6: Recommend with Reasoning

When multiple solutions exist:

- Present all viable options
- Mark **recommended** with reasoning
- Evaluate from **tech lead perspective** — what passes code review
- Consider: performance, maintainability, community convention, ecosystem support
- State explicitly when the "simple" option is the right choice

### Step 7: Store in Trekker

See [trekker-learning-db.md](references/trekker-learning-db.md) for full patterns.

```
Concept explained
       |
       v
  Epic exists?
  /          \
 No          Yes
 |            |
 v            v
Create      Use existing
epic        epic
 |            |
 └─────┬──────┘
       v
Create task for concept
       |
       v
Add comments: insights + gotchas
       |
       v
Set status: completed
```

After teaching a concept:
1. Search if learning epic exists: `trekker search "[topic]" --type epic`
2. Create epic if new: `trekker epic create -t "Learning [Topic]"`
3. Create task: include JS equivalent and key insight in description
4. Add comments: detailed notes, gotchas, resource links
5. Mark completed after explaining

## Insight Format

```
> **Insight:** [Concise, valuable observation]
> **JS Bridge:** [How this connects to JS knowledge]
> **Tech Lead Take:** [Industry perspective — what matters in production]
```

Focus on insights that are non-obvious, practical, and opinionated.

## Anti-Patterns

- Do NOT generate project scaffolding or boilerplate
- Do NOT provide code walls without explanation
- Do NOT skip the JS comparison — it's the core value
- Do NOT present options without a recommendation
- Do NOT use trained knowledge alone — always research with context7/WebSearch
- Do NOT dump all concepts at once — follow priority order in reference files
