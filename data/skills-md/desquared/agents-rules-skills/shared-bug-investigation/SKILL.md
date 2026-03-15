---
name: shared-bug-investigation
description: Scientific method expert for systematic bug investigation and root cause analysis. Use when users report bugs, crashes, unexpected behavior, or debugging requests. Applies hypothesis-driven investigation, controlled experiments, and rigorous validation across any programming language or platform.
---

# Bug Investigation - Scientific Method

Apply scientific methodology to investigate and resolve software bugs systematically.

## Scientific Method Process

1. **Observe** - Gather data about the problem
2. **Hypothesize** - Form testable explanations (ranked by likelihood)
3. **Experiment** - Test hypotheses with controlled changes
4. **Analyze** - Interpret results objectively
5. **Conclude** - Identify root cause and validate fix

## Core Principles

- **Context first** - Understand the project before investigating
- **Hypothesis-driven** - Never jump to solutions without forming testable hypotheses
- **Isolate variables** - Change one thing at a time
- **Reproduce reliably** - Can't fix what you can't reproduce
- **Root causes over symptoms** - Dig deeper than surface fixes
- **Validate rigorously** - Confirm fix resolves issue without regressions

## Investigation Workflow

### Phase 1: Project Context (2-5 min)

**Discover before investigating:**
- Language & version (Python 3.11, Java 17, Go 1.21, etc.)
- Build system (Gradle, npm, Cargo, Make, etc.)
- Key dependencies & frameworks
- Architecture pattern (MVC, microservices, etc.)
- Testing setup

**Quick discovery:**
```bash
# Find package managers
view package.json / requirements.txt / Cargo.toml / pom.xml

# Check config files  
view .env / config.yml / settings.py

# Identify entry points
view main.* / index.* / app.*
```

**Output: One-line context**
```
Python 3.11, Flask API, PostgreSQL, pytest, Docker
```

### Phase 2: Problem Definition

**Gather:**
- Error messages (full text, codes)
- Stack traces / logs
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, version, config)
- Reproducibility (always/sometimes/rare)

**Document:**
```
Bug: [Short description]
Reproduces: [Always/Sometimes/Unable]
Error: [Key error message]
Steps:
1. [Action 1]
2. [Action 2]
3. [Failure occurs]
Expected: [What should happen]
Actual: [What happens]
```

### Phase 3: Hypotheses (Ranked)

### Phase 3: Hypotheses (Ranked)

Form 2-4 testable hypotheses, ranked by likelihood.

**H1: [Most likely cause]**
- Evidence for: [Why this is likely]
- Test: [How to prove/disprove]
- If true: [Expected result]
- If false: [Expected result]

**H2: [Alternative cause]**
- Evidence for: [Supporting observations]
- Test: [Falsifiable experiment]

**Common categories:**
- Logic errors (off-by-one, wrong operator, incorrect condition)
- State issues (race condition, uninitialized, stale data)
- Type/data (null/nil, type mismatch, parsing error)
- Concurrency (data race, deadlock, thread safety)
- Integration (API mismatch, version incompatibility)
- Environment (config, platform-specific, resource limits)

### Phase 4: Experiment

**For each hypothesis:**

**Test H1: [Hypothesis name]**
- Change: [One variable to modify]
- Measure: [What to observe]
- Method: [Specific steps]
- Result: [Actual outcome]
- Conclusion: [Validated/Invalidated]

**Techniques:**
- Add logging at key points
- Use debugger breakpoints
- Binary search (remove half the code)
- Minimal reproduction (strip to essentials)
- Diff working vs broken states
- Isolate components

### Phase 5: Root Cause

**Identified:**
[Clear statement of actual cause]

**Evidence:**
[Chain from observation → hypothesis → validation]

**Why it occurred:**
- Immediate: [Technical reason]
- Contributing: [What enabled this]
- Systemic: [Deeper issue if any]

### Phase 6: Solution & Validation

**Fix:**
[Specific changes to make]

**Why this works:**
[Explain causal connection]

**Validation:**
1. Reproduce bug (confirm failure)
2. Apply fix
3. Retest (confirm success)
4. Test edge cases
5. Run test suite (no regressions)
6. Add test for this bug

**Prevention:**
- [Test to add]
- [Assertion to include]
- [Pattern to avoid]

## Investigation Techniques

**Binary Search:** Remove half the code, test if bug persists. Repeat on failing half until isolated.

**Minimal Reproduction:** Strip to <50 lines that reproduce issue. Removes noise.

**Differential Testing:** Compare working vs broken (commits, versions, configs).

**Strategic Logging:** Add prints at key decision points to trace execution flow.

**Rubber Duck:** Explain code line-by-line aloud. Often reveals logic errors.

## Common Bug Patterns (Language-Agnostic)

**Logic Errors:**
- Off-by-one: `i < n` vs `i <= n`
- Wrong operator: `&&` vs `||`, `==` vs `=`
- Negation errors: `!condition` logic flipped

**State Issues:**
- Race conditions: concurrent access without synchronization
- Uninitialized: using variable before setting value
- Stale state: using outdated cached data

**Type/Data:**
- Null/nil dereference
- Type coercion errors
- Integer overflow
- Floating-point precision

**Concurrency:**
- Deadlock: mutual waiting for locks
- Data race: unsynchronized shared access
- Thread safety: non-thread-safe code on multiple threads

**Integration:**
- API contract mismatch
- Version incompatibility
- Missing dependencies
- Incorrect configuration

## Output Format

```
# Bug Investigation: [Name]

## Context
[One-line: Language, framework, architecture]

## Problem
Error: [Message]
Reproduces: [Always/Sometimes]
Steps: [1,2,3]

## Hypotheses
H1: [Most likely] - Test by [method]
H2: [Alternative] - Test by [method]

## Investigation
Tested H1: [Result - validated/invalidated]
[If needed] Tested H2: [Result]

## Root Cause
[One sentence explanation]
Evidence: [What confirmed it]

## Solution
Fix: [Specific change]
Why it works: [Explanation]
Validated: [Tested successfully]

## Prevention
- Test added: [Description]
- Warning signs: [What to watch for]
```

## Quick Decision Tree

**Symptom → Likely Category:**
- Intermittent failure → Concurrency/state
- Always fails same way → Logic error
- Null/nil crash → Type/data
- Specific environment only → Configuration
- Performance degradation → Resource/algorithm
- After dependency update → Integration

## Critical Reminders

- Start with context discovery
- Form hypotheses before coding
- Change ONE variable at a time
- Reproduce before fixing
- Validate fix rigorously
- Add regression test
- Document root cause
