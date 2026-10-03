---
name: clarify
description: "Decomposes underspecified requests by classifying gaps (missing info, ambiguity, false premises) and generating targeted clarifying questions. Produces a confirmed problem statement before any implementation begins. For sharpening a request that already exists; not for open-ended requirement discovery from a vague idea (use the research command)."
user-invocable: false
---

# Skill: clarify

Understand what the user needs before committing to work.

LLMs default to assuming rather than asking — models overwhelmingly proceed without asking even when information is missing (70% of cases in controlled studies). This skill serves as the plan pipeline's clarifier and counteracts that bias by classifying what's unclear and generating targeted clarifying questions.

`adaptive-questioning.md` at `${CLAUDE_PLUGIN_ROOT}/references/adaptive-questioning.md` is a shared reference: the plan pipeline's clarify gates also link to it (Phase 3 planning checkpoints use it for mode-switching).

Your output is a conversation: clarifying questions, differential examples, restatements. Think out loud WITH the user — collaborative exploration, not interrogation.

The fault-type and hypothesis machinery below is *your* analysis for choosing the right question — not something to narrate. The user sees the question itself, and where useful a differential example; never "this is a Parameter fault" or a listed set of interpretations.

---

## Classifying What's Unclear

Not all gaps are the same. Classifying the type determines what kind of question to ask.

### Fault Types

**Intention faults** — The real goal isn't recoverable from the request.
- Indirect intent: "Can you check if this is possible?" (often means "please do this")
- Vague objectives: "Make it better" (better how? for whom?)
- Contextual irrelevance: user introduces an unrelated goal mid-task

**Premise faults** — An assumption in the request is wrong.
- False presupposition: "Fix the race condition in the cache" (no race condition exists)
- Capability mismatch: asking for something the system can't do
- Factual error: assumptions based on code that has since changed

**Parameter faults** — Required details are missing or conflicting.
- Insufficient information: "Build a login page" (OAuth? email/password? SSO?)
- Contradictions: "Keep it simple but handle every edge case"
- Missing priorities: everything seems equally important

**Expression faults** — The language prevents unique interpretation.
- Referential ambiguity: "Update that component" (which one?)
- Lexical ambiguity: "Clean up the API" (refactor? deprecate? document?)
- Scope ambiguity: "Production-ready" means different things to different people

### Ambiguity Direction

Once you've identified a gap, classify which direction it pulls — this shapes your question:

| Direction | Signal | Clarification Action |
|-----------|--------|---------------------|
| **Semantic** | Key terms have multiple valid meanings | Disambiguate: "do you mean A or B?" |
| **Too broad** | Clear intent but scope is huge | Specify: "which part matters most right now?" |
| **Too narrow** | Request is oddly specific for the likely goal | Generalize: "what's the broader outcome you're after?" |

### For Coding Tasks Specifically

Three concrete ways a coding request becomes ambiguous:

- **Missing goal**: the what/why is absent — only the how is stated
- **Missing premises**: constraints are unstated (sort order, error handling, edge cases)
- **Ambiguous terminology**: precise terms replaced with vague ones ("sorted appropriately" vs "ascending by date")

Inconsistencies between requirements are the hardest to detect. Explicitly check whether parts of the request conflict with each other.

---

## Generating Questions

### Think in Hypotheses

Don't start with "what should I ask?" Start with "what are the plausible interpretations?" Then find the question whose answer eliminates the most of them.

1. Generate 2-4 competing interpretations of the request
2. Identify what distinguishes them — the axis of disagreement
3. Ask about that axis

**Example:**
- Request: "Add caching to the API"
- Interpretation A: In-memory cache for latency
- Interpretation B: External cache (Redis) for scaling
- Interpretation C: HTTP cache headers for clients
- Axis: what problem are they solving — speed, load, or bandwidth?
- Question: "What's driving the caching need — slow responses, high server load, or reducing redundant client requests?"

One question targeting the axis of disagreement beats three questions about implementation details.

### Select for Information Gain

Among possible questions, ask the one that maximally reduces uncertainty across your interpretations. If question A would split your hypotheses 50/50 and question B would split them 90/10, ask A — it's more informative regardless of the answer.

Target convergence in 3-5 rounds. Beyond that, returns diminish sharply.

### Concrete Over Abstract

When possible, show the user what different interpretations produce rather than asking abstract questions:

- Weak: "How should error handling work?"
- Strong: "Right now errors silently return null. Option A: throw and let the caller handle it. Option B: return a Result type. They'd look like [snippet A] vs [snippet B]."

Show differential behavioral examples — "If you mean X, here's what happens for input Z. If you mean Y, here's what happens instead." Let the user pick based on observable behavior, not abstract description.

### Five Clarification Strategies

Match your approach to the fault type:

| Strategy | When | Example |
|----------|------|---------|
| **Ask for parameter** | Specific detail is missing | "What should happen when the input is empty?" |
| **Disambiguate** | Multiple valid interpretations exist | "By 'refactor,' do you mean restructure the module or clean up naming?" |
| **Propose alternatives** | Constraints make the request impossible as stated | "That endpoint doesn't support pagination. We could add it, or switch to cursor-based fetching." |
| **Confirm risk** | High-stakes irreversible action | "This would drop the existing table. Proceed, or migrate the data first?" |
| **Report blocker** | Objective barrier exists | "The API rate-limits to 100 req/s. The current design needs 300. How should we handle that?" |

---

## Question Quality

### Attributes

Every question should pass these checks:

| Attribute | Test |
|-----------|------|
| **Focused** | Addresses ONE gap — no compound questions |
| **Answerable** | User can answer from what they already know |
| **Discriminative** | The answer meaningfully narrows interpretations |
| **Non-leading** | Doesn't presuppose the answer |
| **Task-relevant** | Directly advances the work at hand |
| **Constructive** | Builds toward shared understanding, not just gathering data |

### Effort Awareness

Estimate the effort each question requires from the user:

| Effort | Example | Policy |
|--------|---------|--------|
| **Low** | "Should this be async or sync?" | Ask freely — user already knows |
| **Medium** | "What's the expected request volume?" | Ask only if important — user might not know |
| **High** | "What does the upstream service return on timeout?" | Don't ask — investigate yourself |

**The principle: ask about intent, goals, and constraints (the user's knowledge). Figure out implementation details yourself (your job).**

---

## Managing the Conversation

### Track Intent State

Maintain two mental sets as the conversation progresses:

- **Confirmed** (+): interpretations, constraints, and goals the user has validated
- **Ruled out** (-): interpretations the user has rejected or that contradict confirmed information

Score remaining interpretations by alignment with confirmed items and conflict with ruled-out items. This naturally narrows the space with each turn.

### Decouple the Decisions

Three separate questions, in order:

1. **Should I clarify?** — Is there meaningful ambiguity that would change my approach?
2. **What type of clarification?** — Which fault type and strategy apply?
3. **How do I phrase it?** — What specific question, with what framing?

Don't collapse these. Deciding to clarify and blurting out the first question that comes to mind skips the targeting step.

### Short-Circuit Rules

- If all key information is present and you have no competing hypotheses, proceed directly.
- When asking and not-asking would produce equally good outcomes, don't ask. Favor action on ties.
- If the user signals "just do it" or "whatever works," **switch to confirmatory mode** rather than going silent — state your assumptions so the user can object. See [adaptive-questioning.md](${CLAUDE_PLUGIN_ROOT}/references/adaptive-questioning.md) for mode-switching protocol and the genuine-low-stakes exception.

---

## Anti-Patterns

| Pattern | Problem | Instead |
|---------|---------|---------|
| Proceeding without checking | Default execution bias (see intro) | Run detection as a separate pass first |
| Asking implementation details | Shifts investigation to the user | Figure it out from the codebase |
| Rapid-fire question lists | Feels like an interrogation | 1-3 questions max per turn |
| Asking what you could read from code | Wastes their time | Read first, ask about what you can't determine |
| Over-asking on clear requests | Delays work, erodes trust | If it's clear, proceed |
| Abstract questions | Harder for the user to reason about | Show differential examples |
| Leading questions | Biases response, masks intent | Open-ended, or balanced options |
| One round and done | Complex requests need iteration | Continue until hypotheses converge |
| Asking when outcomes are equivalent | Unnecessary friction | Favor direct action on ties |

---

## Chain

| After | Next |
|-------|------|
| Ambiguity resolved, shared understanding reached | Return to calling skill with goal/scope/constraints/approach |
| New ambiguity surfaces during work | Re-enter clarify loop |
