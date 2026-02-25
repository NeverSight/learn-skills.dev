---
name: tinkering
description: >
  Safe experimentation framework for AI agents. Creates isolated sandbox
  environments for trying new features, testing approaches, and exploring
  solutions without polluting the main codebase.

  USE WHEN: Agent needs to try something uncertain, explore multiple approaches,
  test a new library, prototype a feature, or run a technical spike before
  committing to implementation.

  PRIMARY TRIGGERS:
  "experiment with" = Setup sandbox + run experiment
  "try this approach" = Quick experiment in sandbox
  "spike" / "POC" / "prototype" = Time-boxed technical investigation
  "tinker" / "tinkering mode" = Enter experimentation workflow
  "explore options" = Multi-approach comparison in sandbox

  NOT FOR: Debugging (use debugger), testing (use test runner),
  or committed feature work (use git branches).

  DIFFERENTIATOR: Unlike git branches (for committed direction), tinkering is
  for "I don't know if this will work" exploration. Try 5 things in sandbox
  before committing to a branch. Faster feedback, zero codebase pollution.
---

# Tinkering

## Overview

Structured experimentation framework. When uncertain about an approach, don't
hack at production code - create an isolated sandbox, try freely, then graduate
successful experiments or discard failed ones cleanly.

**Core principle:** The output of tinkering is **knowledge**, not production code.
A successful experiment teaches you how to solve the problem. The actual
implementation happens after, informed by what you learned.

## When to Use

| Situation | Tinkering? | Why |
|-----------|-----------|-----|
| "Will this library work for our use case?" | Yes | Unknown outcome, need to explore |
| "Which of these 3 approaches is fastest?" | Yes | Comparing multiple options |
| "How do I integrate this API?" | Yes | Technical spike, learning-focused |
| "Add a login button to the header" | No | Clear requirement, use git branch |
| "Fix the null pointer on line 42" | No | Debugging, not experimenting |
| "Refactor auth module to use JWT" | Maybe | If approach uncertain, spike first |

---

## Workflow

### Phase 1: Setup Sandbox

Create isolated experiment environment:

```bash
# 1. Create experiment directory
mkdir -p _experiments/{experiment-name}

# 2. Add to .gitignore (if not already present)
grep -qxF '_experiments/' .gitignore 2>/dev/null || echo '_experiments/' >> .gitignore

# 3. Create manifest (first time only)
# See MANIFEST.md template below
```

**MANIFEST.md template** (create at `_experiments/MANIFEST.md`):
```markdown
# Experiment Log

## Active

### {experiment-name}
- **Date**: YYYY-MM-DD
- **Hypothesis**: What we're trying to learn
- **Status**: active
- **Result**: (pending)

## Completed
<!-- Move finished experiments here -->
```

**Rules:**
- NEVER modify production files during tinkering
- ALL experiment code goes inside `_experiments/{name}/`
- Copy source files into sandbox if you need to modify them

---

### Phase 2: Hypothesize

Before writing any code, state clearly:

```
Question : What specific question are we answering?
Success  : How will we know it works?
Time box : Maximum time to spend (default: 30 min)
Scope    : Which files/areas are involved?
```

Write this in `_experiments/{name}/HYPOTHESIS.md` or as a top comment.

**Example:**
```
Question : Can we replace moment.js with date-fns and reduce bundle size?
Success  : Bundle decreases >20%, all date formatting still works
Time box : 20 minutes
Scope    : src/utils/date.ts, package.json
```

---

### Phase 3: Experiment

Build freely in the sandbox.

**Modifying existing code:**
```bash
# Copy the file(s) you need to change
cp src/utils/date.ts _experiments/date-fns-migration/date.ts
# Edit the copy freely - zero risk to production
```

**New feature exploration:**
```bash
# Create new files directly in sandbox
touch _experiments/websocket-poc/server.ts
touch _experiments/websocket-poc/client.ts
```

**Library evaluation:**
```bash
# Minimal test script in sandbox
touch _experiments/redis-eval/test_redis.py
# Use isolated dependencies (venv, local node_modules)
```

**Multi-approach comparison:**
```
_experiments/caching-spike/
  approach-a-redis/
  approach-b-memory/
  approach-c-sqlite/
  COMPARISON.md       # Side-by-side evaluation
```

**Rules during experimentation:**
- Stay in sandbox - never touch production files
- Quick and dirty is fine - this is throwaway code
- Document learnings as you go
- Stop at time box, even if incomplete - partial answers are still answers

---

### Phase 4: Evaluate

Assess results against the hypothesis.

**Checklist:**
- Did the experiment answer the original question?
- Does it meet the success criteria from Phase 2?
- Any unexpected side effects or constraints discovered?
- Is the approach feasible for production implementation?
- What's the estimated effort to implement properly?

**Update MANIFEST.md:**
```markdown
- **Result**: SUCCESS - date-fns reduced bundle by 34%, all tests pass
- **Status**: graduated
- **Notes**: Need to handle timezone edge case in formatRelative()
```

**Decision:**
- Positive result -> Phase 5, Path A (Graduate)
- Negative result -> Phase 5, Path B (Discard)
- Inconclusive -> Extend time box OR try different approach

---

### Phase 5: Graduate or Discard

#### Path A: Graduate (success)

**Load reference:** `references/graduation-checklist.md`

Quick summary:
1. Do NOT copy-paste experiment code directly into production
2. Re-implement properly using what you learned
3. Write proper tests for the production implementation
4. Apply code standards (experiment was quick & dirty, production shouldn't be)
5. Reference experiment in commit message for context

#### Path B: Discard (failed)

Failed experiments are valuable - they tell you what NOT to do.

1. Update MANIFEST.md with failure reason and learnings
2. Delete experiment files: `rm -rf _experiments/{name}/`
3. Or keep briefly if learnings are worth referencing

---

### Phase 6: Cleanup

```bash
# Remove completed experiment
rm -rf _experiments/{experiment-name}/

# Update MANIFEST.md - move entry to "Completed" section
```

**MANIFEST.md after cleanup:**
```markdown
## Completed

### date-fns-migration (2025-01-15)
- GRADUATED - Implemented in commit abc123
- Learnings: date-fns 3x smaller, timezone handling needs explicit config

### graphql-evaluation (2025-01-10)
- DISCARDED - Too much overhead for our simple REST API
- Learnings: REST + OpenAPI better fit for <20 endpoints
```

---

## Quick Reference

```
Setup      ->  mkdir _experiments/{name}, add to .gitignore
Hypothesize ->  Question + success criteria + time box
Experiment  ->  Build in sandbox (never touch production)
Evaluate    ->  Check against success criteria
Graduate    ->  Re-implement properly in production
Cleanup     ->  Remove files, update manifest
```

## Edge Cases

**Needs database changes:** Use separate test DB or schema prefix. Document in hypothesis.

**Needs running server:** Run from sandbox, use different port to avoid conflicts.

**Multiple concurrent experiments:** Each gets own subdirectory. MANIFEST tracks all.

**Experiment grows into real feature:** Graduate it. Don't let experiments become shadow production code.

**Team member needs to see experiment:** Push to feature branch (temporarily track `_experiments/`) or share via patch.
