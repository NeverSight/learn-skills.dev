---
name: solution-explorer
description: Exhaustively explore a problem and solution space before implementing a feature or making an architectural decision. Use when asked to implement a feature, design a system, choose between approaches, or any time there are multiple valid ways to solve a problem. Forces systematic exploration of alternatives to find the global optimum instead of settling on the first reasonable idea. Use this skill whenever the user says things like "implement X", "how should we build", "best way to", "design", "architect", "add a feature for", or describes a non-trivial feature they want built. Even if the user doesn't explicitly ask for exploration, use this skill when you recognize that the implementation has multiple viable paradigms worth comparing.
---

# Solution Explorer

## Why This Exists

LLMs satisfice. When asked to implement something, they pattern-match to the most common approach and start building immediately. This is a local maximum — the most obvious solution is rarely the best one across all dimensions that matter. A senior engineer surveys the full landscape of possibilities before committing. This skill forces that discipline.

The underlying dynamic: LLMs are trained on the most frequently written patterns, so they converge on popular approaches. But popular doesn't mean optimal for your specific context, constraints, and goals. The best solution might be an uncommon pattern, a creative combination, or a reframing of the problem entirely.

## Before You Begin: Calibrate the Exploration

Not every decision deserves the same depth of exploration. Before diving in, assess the decision's weight to right-size the process:

**Full exploration (all 5 phases)** — Use when:
- The decision is hard to reverse (architecture, data model, core abstractions)
- Multiple paradigms genuinely exist and the right one isn't clear
- The feature will be lived with for months or years
- Getting it wrong means significant rework

**Abbreviated exploration (Phases 1-3, skip prototyping)** — Use when:
- The problem space is well-understood but there are still 2-3 viable approaches
- Analysis alone can identify a clear winner
- The decision is medium-stakes (meaningful but recoverable)

**Quick exploration (problem framing + rapid paradigm scan)** — Use when:
- The feature is small but you sense there might be a better approach than the obvious one
- Time is tight but you want to at least check you're not missing something
- Write a condensed PROBLEM_BRIEF and SOLUTION_MAP (skip the other artifacts)

When in doubt, start with the full process. You can always abbreviate once you see the landscape — but you can't un-skip exploration you never did.

## The Process

Two phases, mirroring how good engineering actually works:

1. **Diverge** — Map the problem space, then exhaustively explore the solution space
2. **Converge** — Analyze, prototype finalists, select with evidence

All artifacts go in `.claude/explorations/<feature-name>/`.

---

## Phase 1: Frame the Problem

Before exploring solutions, deeply understand what you're actually solving. LLMs often solve the stated problem rather than the real problem, because they match on keywords rather than understanding the underlying need.

### Steps

1. **Restate the problem in your own words.** Not the user's phrasing — your understanding of the underlying need. What capability is missing? What pain point exists? Ask the user to confirm or correct your understanding.

2. **Map the dimensions.** What are the axes along which solutions can vary? Consider:
   - Performance characteristics (latency, throughput, memory footprint)
   - Complexity budget (how much complexity is this problem worth?)
   - Integration surface (what existing systems, APIs, data stores must it work with?)
   - User experience requirements (responsiveness, offline support, error states)
   - Maintenance trajectory (who maintains this? how often will it change?)
   - Scale expectations (current load and realistic future growth)

3. **Define success criteria.** Be specific and rankable:
   - **MUST** — non-negotiable requirements (failing any = approach eliminated)
   - **SHOULD** — important but with room for tradeoffs
   - **NICE** — differentiators between otherwise equivalent approaches

4. **Surface assumptions.** What are you taking for granted? List at least 3 assumptions and verify each with the user. Unexamined assumptions are where "obviously correct" approaches turn out to be wrong. Common hidden assumptions: deployment platform, expected scale, team expertise, security requirements, backward compatibility needs.

### Output: PROBLEM_BRIEF.md

```markdown
# Problem Brief: <feature name>

## Problem statement
<your restatement of the underlying need>

## Dimensions
<axes along which solutions vary, with current understanding of each>

## Success criteria
### Must
### Should
### Nice

## Assumptions
1. <assumption> — status: confirmed / unconfirmed / rejected
2. ...

## Constraints
<hard limits from the codebase, infrastructure, team, or timeline>
```

---

## Phase 2: Explore the Solution Space

This is where most LLMs fail. They generate 2-3 options that are superficial variations of the same theme — different libraries implementing the same strategy. Genuine exploration means thinking across **paradigms**: fundamentally different strategies for solving the problem.

### What's a paradigm?

A paradigm is a high-level strategy that makes qualitatively different tradeoffs. Approaches within the same paradigm share core assumptions; approaches across paradigms don't. Each paradigm represents a different *bet* about what matters most.

Example for "implement collaborative editing":
- **Paradigm: Operational Transform** — bet: correctness through mathematical transforms is worth the complexity
- **Paradigm: CRDTs** — bet: conflict-free data structures eliminate coordination overhead
- **Paradigm: Server-authoritative** — bet: simplicity of a single source of truth outweighs latency costs
- **Paradigm: Turn-based locking** — bet: concurrent editing isn't actually needed if sections are granular enough

These aren't just different libraries — they're fundamentally different bets about what matters most.

### Steps

1. **Identify paradigms.** Brainstorm high-level strategies. Aim for at least 3 distinct paradigms. If you only see 1-2, you haven't looked broadly enough — try these frame-shifts:
   - What if the constraint was opposite? (high scale → low scale, real-time → batch)
   - How do other industries solve analogous problems?
   - What if you had zero dependencies? What if you could use any dependency?
   - What existed before the currently popular approach?

2. **Research each paradigm substantively.** This means more than listing it — for each paradigm, gather enough information to understand its core tradeoffs, not just its existence. Specifically:
   - What libraries, frameworks, or services implement this paradigm?
   - What are the established patterns and best practices?
   - Who has solved this before and what did they learn?
   - What are the known failure modes and scaling cliffs?

   Use web search, documentation lookups, and codebase exploration. Gather real data, not speculation.

   **Parallel research:** If subagents are available, research paradigms concurrently — each paradigm is an independent research task. Spawn one research agent per paradigm with a focused brief: "Research [paradigm name] for [problem]. Find libraries, patterns, failure modes, and real-world usage. Save findings to [path]."

3. **Generate concrete approaches.** Within each paradigm, identify 1-3 specific implementations. Each approach needs:
   - **How it works** — concrete description, not hand-waving
   - **What you gain** — specific advantages in context of the problem dimensions
   - **What you give up** — honest assessment of costs and limitations
   - **Where it shines** — the ideal context for this approach
   - **Known risks** — failure modes, scaling cliffs, maintenance burdens
   - **Complexity** — simple / moderate / complex (relative to this project's standards)

4. **Hunt for the non-obvious.** After your initial exploration, deliberately look for what you might have missed. The best solutions often come from this step:
   - Can the problem be **reframed** to make it trivial? (Sometimes the best "implementation" is realizing you don't need one, or that the real problem is something adjacent.)
   - Is there a **hybrid** that combines strengths of multiple paradigms?
   - What would you recommend under **extreme constraints**? "Ship in 2 hours" vs "must run for 10 years" vs "budget is $0" — each constraint surfaces different solutions.
   - What would someone from a **completely different domain** do? A game developer? A distributed systems researcher? A hardware engineer? A spreadsheet power user?
   - Is there a **managed service** that eliminates the problem entirely? Sometimes the best code is no code.
   - What's the **laziest possible solution** that still meets the MUST criteria? Laziness is an underrated engineering virtue — it often reveals the simplest viable path.

### Output: SOLUTION_MAP.md

```markdown
# Solution Map: <feature name>

## Paradigm 1: <name>
**Core bet:** <what this paradigm assumes matters most>
<brief description of the strategy>

### Approach 1a: <name>
- **How it works:** ...
- **Gains:** ...
- **Gives up:** ...
- **Shines when:** ...
- **Risks:** ...
- **Complexity:** simple | moderate | complex

### Approach 1b: <name>
...

## Paradigm 2: <name>
**Core bet:** <what this paradigm assumes matters most>
...

## Paradigm 3: <name>
**Core bet:** <what this paradigm assumes matters most>
...

## Non-obvious options
<creative, unconventional, or hybrid approaches>

## Eliminated early
<approaches considered but dismissed, with documented reasoning>
```

### Minimum Exploration Gate

Do not proceed to Phase 3 until ALL of the following are true:
- At least **3 distinct paradigms** explored with substantive analysis (each has a documented core bet, at least one concrete approach with tradeoffs, and research-backed information — not just a name and one-sentence description)
- At least **5 total approaches** documented across those paradigms, each with the full gains/gives-up/risks breakdown
- **Research conducted** — real information gathered from web search, docs, or codebase exploration, not just brainstorming from training data
- **Non-obvious section** genuinely attempted with at least one creative reframing or hybrid approach

If you feel like skipping ahead because one approach seems "obviously best" — that's the satisficing instinct this skill exists to counter. Document why it seems obvious, then keep exploring. The goal isn't to waste time; it's to build justified confidence. If the obvious answer is truly best, the exploration will confirm it quickly and you'll have evidence for why.

---

## Phase 3: Analyze and Narrow

Now converge. Evaluate approaches against the success criteria from Phase 1 to identify 2-3 finalists worth prototyping.

### Steps

1. **Build a tradeoff matrix.** Compare **all** approaches (not just your favorites) against each success criterion. Use concrete assessments ("~200ms p95 latency" or "adds ~500 lines of code"), not vague ratings ("good" / "medium"). The matrix should cover every approach that wasn't eliminated early — this forces honest comparison rather than cherry-picking.

2. **Eliminate on dealbreakers.** Which approaches fail a MUST criterion? Remove them, documenting the specific criterion they failed and why. Every elimination should be traceable to evidence.

3. **Rank the survivors.** For SHOULD and NICE criteria, compare how approaches perform. Note where you're genuinely uncertain — these uncertainties are what prototyping should resolve.

4. **Select 2-3 finalists.** Choose approaches that are genuinely different from each other. If your finalists are all from the same paradigm, reconsider whether you explored broadly enough. The point of prototyping is to compare across paradigms, not to A/B test minor variations.

5. **Name the key differentiator.** What single question, if answered, would make the choice clear? This is what prototyping targets. Having a focused question prevents prototypes from turning into full implementations.

### Output: ANALYSIS.md

```markdown
# Analysis: <feature name>

## Tradeoff Matrix

| Criterion | Approach A | Approach B | Approach C | ... |
|-----------|-----------|-----------|-----------|-----|
| MUST: ... | ✅ / ❌    | ...       | ...       |     |
| SHOULD: . | <detail>  | ...       | ...       |     |
| NICE: ... | <detail>  | ...       | ...       |     |

## Eliminated
- <Approach X>: eliminated because <specific MUST failure with evidence>
- ...

## Finalists
1. **<name>** — from Paradigm X. Selected because...
2. **<name>** — from Paradigm Y. Selected because...
3. **<name>** (optional) — from Paradigm Z. Selected because...

## Key differentiator
<the single question that prototyping needs to answer>

## Open risks
<unknowns that could affect the decision>
```

---

## Phase 4: Prototype and Compare

Build minimal prototypes of the finalists. The goal is to answer the key differentiating question, not to build complete implementations.

### What "minimal" means

A prototype should be the smallest amount of code that tests the key differentiator identified in Phase 3. Specifically:
- If the differentiator is **performance**, build just enough to benchmark (a hot loop, a simulated load)
- If it's **developer experience**, build just enough to feel the ergonomics (a typical use case, not exhaustive coverage)
- If it's **complexity**, build just enough to see the wiring (integration points, not full features)
- If it's **feasibility**, build just enough to prove it works (happy path only)

Each prototype should typically be 50-200 lines of code. If you're writing more, you're probably building an implementation, not testing a hypothesis.

### Steps

1. **Define comparison criteria BEFORE writing code.** What will you measure? What will you observe? Write these down first. This prevents post-hoc rationalization — the natural tendency to justify whatever you already built. Be specific: "response time under 100 concurrent requests" not "good performance."

2. **Build minimal prototypes.** Share test harnesses, data fixtures, and scaffolding across prototypes where possible. Put prototypes in `.claude/explorations/<feature-name>/prototypes/`.

3. **Run the comparison.** Execute the comparison plan you defined in step 1. Record results concretely — numbers, observations, code complexity metrics. Not vibes.

4. **Check for surprises.** Did prototyping reveal anything the analysis missed? New tradeoffs? Hidden complexity? An approach that looked simple but has a nasty edge case? Surprises from prototyping are some of the most valuable outputs of this entire process — they represent things you couldn't have known without building.

### Output: COMPARISON.md

```markdown
# Prototype Comparison: <feature name>

## Comparison criteria (defined before prototyping)
1. <what's being measured and how>
2. ...

## Results

### Prototype A: <name>
- Location: `prototypes/a/`
- Criterion 1: <concrete result>
- Criterion 2: <concrete result>
- Surprises: <anything unexpected>

### Prototype B: <name>
- Location: `prototypes/b/`
- ...

## Verdict
<which prototype answered the key differentiating question, and how>

## Updated understanding
<new insights from prototyping that weren't visible during analysis>
```

---

## Phase 5: Decide and Plan

Select the winner based on accumulated evidence and create an implementation plan.

### Steps

1. **Make the decision.** State which approach wins and why. Reference specific evidence: prototype results, research findings, tradeoff analysis. The reasoning should be traceable back through your artifacts — someone reading DECISION.md should be able to follow the chain of evidence through COMPARISON.md → ANALYSIS.md → SOLUTION_MAP.md → PROBLEM_BRIEF.md.

2. **Document what was NOT chosen and why.** This is as important as documenting what was chosen. Future-you will wonder "why didn't we just use X?" — the answer should be in the decision record. Each rejected alternative needs a specific, evidence-based reason, not "it wasn't as good."

3. **Outline implementation steps.** Based on the winning approach, create a concrete plan. If the exploration surfaced risks, include mitigations.

### Output: DECISION.md

```markdown
# Decision: <feature name>

## Selected approach
**<name>** — <one-line description>

## Evidence for this choice
- <evidence from prototyping>
- <evidence from research>
- <evidence from analysis>

## Why not the alternatives
- **<Alternative A>**: <specific reason with evidence — not "it wasn't as good">
- **<Alternative B>**: <specific reason with evidence>

## Implementation plan
1. <step>
2. <step>
...

## Known risks and mitigations
- Risk: <what could go wrong>
  Mitigation: <how to handle it>
```

---

## Session Protocol

Exploration may span multiple sessions, especially for complex features.

### Starting a session

1. Check `.claude/explorations/` for existing exploration artifacts
2. If found, read them in order: PROBLEM_BRIEF → SOLUTION_MAP → ANALYSIS → COMPARISON → DECISION
3. Resume from where the last session left off

### Ending a session mid-exploration

Write HANDOFF.md:

```markdown
# Handoff: <feature name>

## Current phase
<which phase, and where within it>

## Completed
<what's been done, with pointers to artifacts>

## Next steps
<exact actions to resume — not vague, but specific>

## Open questions for the user
<anything blocking that needs user input>
```
