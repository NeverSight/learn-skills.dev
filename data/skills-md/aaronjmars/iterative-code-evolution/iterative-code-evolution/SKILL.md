---
name: iterative-code-evolution
description: Systematically improve code through structured analysis-mutation-evaluation loops. Adapted from ALMA (Automated meta-Learning of Memory designs for Agentic systems). Use when iterating on code quality, optimizing implementations, debugging persistent issues, or evolving a design through multiple improvement cycles. Replaces ad-hoc "try and fix" with disciplined reflection, variant tracking, and principled selection of what to change next.
---

# Iterative Code Evolution

A structured methodology for improving code through disciplined reflect → mutate → verify → score cycles, adapted from the ALMA research framework for meta-learning code designs.

## When to Use This Skill

- Iterating on code that isn't working well enough (performance, correctness, design)
- Optimizing an implementation across multiple rounds of changes
- Debugging persistent or recurring issues where simple fixes keep failing
- Evolving a system design through structured experimentation
- Any task where you've already tried 2+ approaches and need discipline about what to try next
- Building or improving prompts, pipelines, agents, or any "program" that benefits from iterative refinement

## When NOT to Use This Skill

- Simple one-shot code generation (just write it)
- Mechanical tasks with clear solutions (refactoring, formatting, migrations)
- When the user has already specified exactly what to change

## Core Concepts

### The Evolution Loop

Every improvement cycle follows this sequence:

```
┌─────────────────────────────────────────────────────┐
│  1. ANALYZE  — structured diagnosis of current code │
│  2. PLAN     — prioritized, concrete changes        │
│  3. MUTATE   — implement the changes                │
│  4. VERIFY   — run it, check for errors             │
│  5. SCORE    — measure improvement vs. baseline     │
│  6. ARCHIVE  — log what was tried and what happened │
│                                                     │
│  Loop back to 1 with new knowledge                  │
└─────────────────────────────────────────────────────┘
```

### The Evolution Log

Track all iterations in `.evolution/log.json` at the project root. This is the memory that makes each cycle smarter than the last.

```json
{
  "baseline": {
    "description": "Initial implementation before evolution began",
    "score": 0.0,
    "timestamp": "2025-01-15T10:00:00Z"
  },
  "variants": {
    "v001": {
      "parent": "baseline",
      "description": "Added input validation and error handling",
      "changes_made": [
        {
          "what": "Added type checks on all public methods",
          "why": "Runtime crashes from malformed input in 3/10 test cases",
          "priority": "High"
        }
      ],
      "score": 0.6,
      "delta": "+0.6 vs parent",
      "timestamp": "2025-01-15T10:30:00Z",
      "learned": "Input validation was the primary failure mode — most other logic was sound"
    },
    "v002": {
      "parent": "v001",
      "description": "Refactored parsing logic to handle edge cases",
      "changes_made": [
        {
          "what": "Rewrote parse_input() to use state machine instead of regex",
          "why": "Regex approach failed on nested structures (seen in test cases 7,8)",
          "priority": "High"
        }
      ],
      "score": 0.85,
      "delta": "+0.25 vs parent",
      "timestamp": "2025-01-15T11:00:00Z",
      "learned": "State machine approach generalizes better than regex for this grammar"
    }
  },
  "principles_learned": [
    "Input validation fixes give the biggest early gains",
    "Regex-based parsing breaks on recursive structures — prefer state machines",
    "Small targeted changes score better than large rewrites"
  ]
}
```

## The Process in Detail

### Phase 1: ANALYZE — Structured Diagnosis

Before changing anything, perform a structured analysis of the current code and its outputs. This is the most important phase — it prevents wasted mutations.

**Step 1 — Learn from past edits** (skip on first iteration)

Review the evolution log. For each previous change:
- Did the score improve or degrade?
- What pattern made it succeed or fail?
- Extract 2-3 principles to adopt and 2-3 pitfalls to avoid

**Step 2 — Component-level assessment**

For each meaningful component (function, class, module, pipeline stage), label it:

| Label | Meaning |
|-------|---------|
| **Working** | Produces correct output, no issues observed |
| **Fragile** | Works on happy path but fails on edge cases or specific inputs |
| **Broken** | Produces wrong output or errors |
| **Redundant** | Duplicates logic found elsewhere, adds complexity without value |
| **Missing** | A needed component that doesn't exist yet |

For each label, write a one-line explanation of *why* — linked to specific test outputs or observed behavior.

**Step 3 — Quality and coherence check**

Look for cross-cutting issues:
- **Data flow**: Do components pass structured data to each other, or rely on implicit state?
- **Error handling**: Are errors caught and handled, or silently swallowed?
- **Duplication**: Is the same logic repeated in multiple places?
- **Hardcoding**: Are there magic numbers, hardcoded paths, or environment-specific assumptions?
- **Generalization**: Which parts would work on new inputs vs. which are overfitted to test cases?

**Step 4 — Produce prioritized suggestions**

Based on Steps 1-3, produce concrete changes. Each suggestion must have:

```
- PRIORITY: High | Medium | Low
- WHAT: Precise description of the change (code-level, not vague)
- WHY: Link to a specific observation from Steps 1-3
- RISK: What could go wrong if this change is made incorrectly
```

**Rule: Every suggestion must link to an observation.** No "this might help" suggestions — only changes grounded in something you actually saw in the code or outputs.

**Rule: Limit to 3 suggestions per cycle.** More than 3 changes at once makes it impossible to attribute improvement or regression to specific changes.

### Phase 2: PLAN — Select What to Change

Pick 1-3 suggestions from the analysis. Selection principles:

- **High priority first** — fix broken things before optimizing working things
- **One theme per cycle** — don't mix unrelated changes (e.g., don't fix parsing AND refactor error handling in the same mutation)
- **Prefer targeted over sweeping** — a surgical change to one function beats a rewrite of three modules
- **If stuck, explore** — if the last 2+ cycles showed diminishing returns on the same component, pick a different component to modify (this is the ALMA "visit penalty" principle — don't keep grinding on the same thing)

### Phase 3: MUTATE — Implement Changes

Write the new code. Key discipline:

- **Change only what the plan says.** Resist the urge to "fix one more thing" while you're in there.
- **Preserve interfaces.** Don't change function signatures or return types unless the plan explicitly calls for it.
- **Comment the rationale.** Add a brief comment near each change referencing the evolution cycle (e.g., `# evo-v003: switched to state machine per edge case failures`)

### Phase 4: VERIFY — Run and Check

Execute the modified code against the same inputs/tests used for scoring.

**If it crashes (up to 3 retries):**

Use the reflection-fix protocol:
1. Read the full error traceback
2. Identify the **root cause** (not the symptom)
3. Fix **only** the root cause — do not make unrelated improvements
4. Re-run

After 3 failed retries, **revert to parent variant** and log the failure:
```json
{
  "attempted": "Description of what was tried",
  "failure_mode": "The error that couldn't be resolved",
  "learned": "Why this approach doesn't work"
}
```

This failure data is valuable — it prevents re-attempting the same broken approach.

**If it runs but produces wrong output:**

Don't immediately retry. Go back to Phase 1 (ANALYZE) with the new outputs. The wrong output is diagnostic data.

### Phase 5: SCORE — Measure Improvement

Compare the new variant's performance against its parent (not just the baseline). Scoring depends on context:

| Context | Score Method |
|---------|-------------|
| Tests exist | Pass rate: tests_passed / total_tests |
| Performance optimization | Metric delta (latency, throughput, memory) |
| Code quality | Weighted checklist (correctness, edge cases, readability) |
| User feedback | Binary: better/worse/same per the user's judgment |
| LLM/prompt output quality | Sample outputs graded against criteria |

**Always compute delta vs. parent.** This is how you learn which changes help vs. hurt.

### Phase 6: ARCHIVE — Log and Learn

Update `.evolution/log.json`:
1. Record the new variant with parent, description, changes, score, delta
2. Write a `learned` field: one sentence about what this cycle taught you
3. If the score improved, add the underlying principle to `principles_learned`
4. If the score degraded, add the failure mode to `principles_learned` as a pitfall

## Variant Management

### When to Branch vs. Modify

- **Modify in place** (same file, new version): When the change is clearly incremental (fixing a bug, adding a check, tuning a parameter)
- **Branch** (copy to a new file): When trying a fundamentally different approach (different algorithm, different architecture, different strategy)

Keep branches in `.evolution/variants/` with descriptive names. The evolution log tracks which is active.

### Selection: Which Variant to Iterate On

If you have multiple variants, pick the next one to improve using:

```
score(variant) = normalized_reward - 0.5 * log(1 + visit_count)
```

Where:
- `normalized_reward` = variant score relative to baseline (0-1 range)
- `visit_count` = how many times this variant has been selected for iteration

This balances **exploitation** (iterating on the best variant) with **exploration** (trying variants that haven't been touched recently). It prevents getting stuck in local optima.

## Quick Reference: Analysis Template

When performing Phase 1, structure your thinking as:

```markdown
## Evolution Cycle [N] — Analysis

### Lessons from Previous Cycles
- Cycle [N-1] changed [X], score went [up/down] by [amount]
- Principle: [what we learned]
- Pitfall: [what to avoid]

### Component Assessment
| Component | Status | Evidence |
|-----------|--------|----------|
| function_a() | Working | All test cases pass |
| function_b() | Fragile | Fails on empty input (test #4) |
| class_C | Broken | Returns None instead of dict |

### Cross-Cutting Issues
- [Issue 1 with specific evidence]
- [Issue 2 with specific evidence]

### Planned Changes (max 3)
1. **[High]** WHAT: ... | WHY: ... | RISK: ...
2. **[Medium]** WHAT: ... | WHY: ... | RISK: ...
```

## Example: Full Evolution Cycle

**Context:** User asks to improve a web scraper that's failing on 40% of target pages.

**Cycle 1 — Analysis:**
- Component assessment: `parse_html()` is Broken (crashes on pages with no `<article>` tag), `fetch_page()` is Working, `extract_links()` is Fragile (misses relative URLs)
- Cross-cutting: No error handling — one bad page kills the entire batch
- Past edits: None (first cycle)
- Plan: [High] Add fallback selectors in `parse_html()` for pages without `<article>`

**Cycle 1 — Mutate:** Add cascading selector logic: try `<article>`, fall back to `<main>`, fall back to `<body>`.

**Cycle 1 — Verify:** Runs without crashes. 

**Cycle 1 — Score:** Pass rate 40% → 72%. Delta: +32%.

**Cycle 1 — Archive:** Learned: "Most failures were selector misses, not logic errors. Fallback chains are high-value."

**Cycle 2 — Analysis:**
- Lessons: Fallback selectors gave +32%. Principle: handle structural variation before fixing logic.
- Component assessment: `parse_html()` now Working. `extract_links()` still Fragile — relative URLs not resolved.
- Plan: [High] Resolve relative URLs using `urljoin` in `extract_links()`

**Cycle 2 — Mutate:** Add base URL resolution.

**Cycle 2 — Score:** 72% → 88%. Delta: +16%.

**Cycle 2 — Archive:** Learned: "URL resolution was second-biggest failure mode. Always normalize URLs at extraction time."

## Key Principles

- **Every change must link to an observation** — no speculative fixes
- **Max 3 changes per cycle** — attribute improvements accurately
- **Log everything** — failed attempts are as valuable as successes
- **Score against parent, not just baseline** — track marginal improvement
- **Explore when stuck** — if 2+ cycles on the same component show diminishing returns, move to a different component
- **Revert on 3 failed retries** — don't spiral; log the failure and try a different approach
- **Principles compound** — the evolution log's `principles_learned` list is the most valuable artifact; it encodes what works for *this specific codebase*
