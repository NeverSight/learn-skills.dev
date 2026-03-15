---
name: brainstorming-enhanced
description: Clarifies ambiguous feature, product, and design requests before planning or implementation. Use when the user says "let's brainstorm", "help me think through", "what should we build", or "explore approaches", or when a request has unclear requirements, multiple plausible interpretations, or meaningful trade-offs.
license: MIT
metadata:
  author: Skill Atlas
  version: "0.1.0"
  homepage: https://skillatlas.sh/
---

# Brainstorming

Turn rough ideas into a planning-ready brief. Focus on deciding **what** to build and **why**. Do not drift into detailed implementation unless the implementation choice changes the product decision.

## Primary outcome

By the end of this skill, produce:

- a crisp problem statement
- a recommended direction
- 1-2 meaningful alternatives at most
- acceptance criteria or success signals
- constraints, assumptions, and non-goals
- the next step: planning, more refinement, or stop

## When to use this skill

Use this skill when:

- the user explicitly asks to brainstorm, ideate, or explore options
- requirements are vague, incomplete, or contradictory
- multiple product, UX, or scope choices are plausible
- trade-offs need discussion before planning or coding
- the request uses language like "make it better", "something like", "improve", or "not sure"

Use a short version or skip it when:

- the request is already specific enough to plan
- the task is a straightforward bug fix or mechanical change
- the user clearly wants immediate execution and ambiguity is low

If brainstorming is unnecessary, say so and move straight to planning or implementation.

## Workflow

For complex tasks, track progress with this checklist:

```text
Brainstorm progress
- [ ] Decide whether brainstorming is needed
- [ ] Review available context and existing patterns
- [ ] Clarify the problem and success criteria
- [ ] Recommend a direction and explain trade-offs
- [ ] Capture a planning-ready brief and next step
```

### 1) Decide if brainstorming is actually needed

Strong signals to skip or shorten brainstorming:

- clear acceptance criteria
- explicit behavior or scope
- obvious existing pattern to follow
- narrow, low-risk change

Strong signals to use brainstorming:

- unclear user goal
- multiple valid interpretations
- missing success criteria
- unresolved UX or product trade-offs
- uncertainty about scope, users, or non-goals

Do not turn every feature request into a mandatory discovery session.

### 2) Review context before asking questions

When a workspace is available, inspect relevant files, docs, existing flows, and naming conventions first. Avoid asking the user questions the project already answers.

Look for:

- similar features or patterns
- domain language already used in the product
- architectural or UX constraints
- recent decisions worth preserving

### 3) Ask only the questions that change the recommendation

Use the minimum number of questions needed. Momentum matters.

Rules:

- Ask at most one question per turn.
- Prefer multiple-choice when natural.
- Ask about the biggest uncertainty first.
- State assumptions explicitly when you can proceed.
- If the user wants speed, provide a recommendation with labeled assumptions instead of stalling.

Prioritize questions in this order:

1. Problem: What problem are we solving?
2. User/context: Who experiences it and when?
3. Success: How will we know this worked?
4. Constraints: Deadlines, dependencies, compatibility, legal/policy limits, non-goals
5. Edge cases: What must not happen?

Good:

- "Which matters more here: faster completion, fewer mistakes, or higher discoverability?"

Less useful:

- "Tell me everything you want from this feature."

### 4) Use the fast path when the user mostly wants momentum

If the request is only mildly ambiguous, do a micro-brainstorm in one response:

1. State your interpretation of the request.
2. Give a recommended direction.
3. Mention 1 alternative only if it is meaningfully different.
4. Ask one confirmation question only if the answer would change the recommendation.

### 5) Present options with a default

Once the problem is clear enough, lead with one recommendation. Include alternatives only when they are genuinely distinct.

Do not dump a long menu of possibilities. Maximum: one recommendation plus two alternatives.

Use this format:

```md
## Recommendation

### Option A — [short name] (recommended)

[1-3 sentences]

Why this is the default:

- [reason]
- [reason]

Trade-offs:

- [trade-off]
- [trade-off]

### Option B — [short name]

Use when:

- [condition]

Trade-offs:

- [trade-off]

### Option C — [short name]

Only include if genuinely useful.
```

Favor the simplest option that satisfies the stated need. Do not design for hypothetical future requirements unless the user explicitly asks for that flexibility.

### 6) Capture a planning-ready brief

When the direction is stable, summarize it in a concise brief that planning or implementation can consume immediately.

Use this template:

```md
# [Topic]

## Problem

[1-2 sentences]

## Users / context

- [user or scenario]

## Goal

- [desired outcome]

## Recommended approach

[1 short paragraph]

## Acceptance criteria

- [observable behavior]
- [observable behavior]
- [observable behavior]

## Constraints and assumptions

- [constraint or assumption]

## Non-goals

- [explicitly out of scope]

## Open questions

- [only unresolved items that still matter]

## Next step

- planning
- refine one question
- stop here
```

Keep this brief short. It should unblock the next step, not become a long design document.

### 7) Optional persistence

Only create a file if the user wants it or the repo convention supports it.

If persisting notes, prefer:
`docs/brainstorms/YYYY-MM-DD-<topic>.md`

Write the brief only after the core decisions are stable. Do not save pages of unresolved speculation.

## Scope boundaries

During brainstorming:

- focus on **what** and **why**
- mention **how** only when it changes scope, UX, feasibility, or trade-offs
- keep technical deep dives, file-by-file plans, and test implementation details for the planning phase

## Conversation style

Be collaborative, concise, and recommendation-first.

After each meaningful summary, validate lightly:

- "Does this capture the problem?"
- "Is the recommended direction right?"
- "Anything to adjust before I turn this into a brief?"

Do not over-interrogate. Stop asking questions once you can state a confident recommendation and acceptance criteria.

## Anti-patterns

Avoid:

- treating brainstorming as mandatory for every feature
- asking several questions at once
- asking the user what the codebase already reveals
- jumping into architecture or implementation plans too early
- presenting more than 3 options
- writing long design docs before the core decision is settled
- optimizing for hypothetical future needs

## Handoff

When finished, make the next action explicit:

- If the brief is clear, hand off to planning.
- If one unresolved decision blocks progress, surface that single decision.
- If the user only wanted ideation, stop after the brief.

If your environment provides a planning workflow, pass the brief into it and skip redundant rediscovery.
