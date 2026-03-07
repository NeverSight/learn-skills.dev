---
name: ask-questions-if-underspecified
description: Ask the minimum clarifying questions before implementation when requirements are ambiguous or missing crucial details
version: 1.2.0
category: 'Planning & Architecture'
agents: [planner, developer, architect]
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash]
tags: [clarification, requirements, underspecified, questions, scope, ambiguity]
verified: true
lastVerifiedAt: 2026-03-01T00:00:00.000Z
best_practices:
  - Follow existing project patterns
  - Document all outputs clearly
  - Handle errors gracefully
error_handling: graceful
streaming: supported
---

# Ask Questions If Underspecified

<identity>
Ask Questions If Underspecified Skill - Ask the minimum clarifying questions before implementation when requirements are ambiguous or missing crucial details
</identity>

<capabilities>
- Identify ambiguous or missing requirements that would block correct implementation
- Generate minimum viable clarifying questions with concrete best-guess defaults
- Distinguish scope/constraint questions (ask) from implementation detail decisions (decide yourself)
- Unblock parallel work by proceeding with stated defaults while awaiting answers
</capabilities>

<instructions>
<execution_process>

### Step 1: Assess Underspecification

Identify which aspects are unclear or missing:

- **Scope**: What exactly should be included/excluded?
- **Constraints**: Performance targets, platform requirements, security rules?
- **Acceptance criteria**: How will the user judge success?
- **Priority**: Which conflicting options should win?

Do NOT ask about things you can determine by reading existing code and conventions.

### Step 2: Triage Questions

Categorize each candidate question:

| Type                                              | Ask or Decide?                                      |
| ------------------------------------------------- | --------------------------------------------------- |
| Scope boundary (what to include)                  | **Ask**                                             |
| Non-functional requirement (perf/security target) | **Ask**                                             |
| Acceptance criteria                               | **Ask**                                             |
| Implementation approach                           | **Decide yourself**                                 |
| Code style / naming                               | **Decide yourself** (follow existing patterns)      |
| Nice-to-have polish                               | **Decide yourself** (proceed with sensible default) |

### Step 3: Ask Concisely (Max 3 Questions)

For each blocking question:

1. State what you assume (best-guess default)
2. Ask the specific question in one sentence
3. Offer 2–3 concrete options when applicable

Format:

```
I'll [proceed with X default assumption]. Quick questions before I start:
1. [Specific question]? (default: [assumption])
2. [Specific question]? (default: [assumption])
```

</execution_process>

<best_practices>

1. **Provide defaults with every question**: Always state your best-guess assumption so the user can simply confirm rather than answer from scratch
2. **Ask about outcomes, not implementation**: "Should this support offline use?" not "Should I use IndexedDB or localStorage?"
3. **Read the codebase first**: Many apparent ambiguities are resolved by existing patterns — check before asking
4. **Batch all questions in one message**: Never ask one question, wait for answer, then ask another

</best_practices>
</instructions>

<examples>
<usage_example>
**Example — Underspecified feature request:**

User: "Add a search feature to the dashboard"

Good response:

```
I'll implement client-side search with debouncing and case-insensitive matching. Quick questions before I start:
1. Should search cover all columns or just the name/title column? (default: name/title only)
2. Should results filter in place or open in a new panel? (default: filter in place)
```

Bad response:

```
Before I start, I need to know:
1. What search algorithm should I use?
2. Should it be case sensitive?
3. What debounce delay?
4. Should I use a library?
5. How many results to show?
```

</usage_example>
</examples>

## Iron Laws

1. **NEVER ask more than 3 questions at once** — more than 3 questions causes decision paralysis; triage ruthlessly and decide the rest yourself.
2. **ALWAYS provide a best-guess default alongside every question** — a question without a default forces the user to think from scratch; a question with a default lets them confirm in one word.
3. **NEVER ask about implementation details you can decide yourself** — algorithm choice, code structure, naming conventions, and library selection are your decisions, not the user's.
4. **NEVER block on nice-to-have requirements** — identify what is truly blocking vs. what can be decided with a sensible default; proceed with the default and note your assumption.
5. **ALWAYS read existing code before asking** — check existing patterns, conventions, and related code first; most apparent ambiguities are resolved by looking at what already exists.

## Anti-Patterns

| Anti-Pattern                           | Why It Fails                                       | Correct Approach                                     |
| -------------------------------------- | -------------------------------------------------- | ---------------------------------------------------- |
| Asking 5+ questions before starting    | Paralyzes user; feels like interrogation           | Triage to max 3 blocking questions; decide the rest  |
| Asking about implementation approach   | That is the agent's job, not the user's            | Ask about scope/constraints/acceptance criteria only |
| Questions without defaults             | User must think from scratch; slower feedback loop | Always state: "default: X — correct?"                |
| Sequential questioning (one at a time) | Creates a slow back-and-forth waterfall            | Batch all questions into one message                 |
| Asking things visible in the codebase  | Shows insufficient research effort                 | Read existing conventions before asking              |

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
