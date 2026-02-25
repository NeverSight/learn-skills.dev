---
name: debugging-patterns
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Grep, Glob, Bash, LSP
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## Quick Five-Step Process (Reference Pattern)

For rapid debugging, use this concise flow:

```
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works
```

**Debugging techniques:**
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- **Add strategic debug logging**
- **Inspect variable states**

**Root Cause Tracing Technique:**
```
1. Observe symptom - Where does error manifest?
2. Find immediate cause - Which code produces the error?
3. Ask "What called this?" - Map call chain upward
4. Keep tracing up - Follow invalid data backward
5. Find original trigger - Where did problem actually start?
```
**Never fix solely where errors appear—trace to the original trigger.**

## LSP-Powered Root Cause Tracing

**Use LSP to trace execution flow systematically:**

| Debugging Need | LSP Tool | Usage |
|----------------|----------|-------|
| "Where is this function defined?" | `lspGotoDefinition` | Jump to source |
| "What calls this function?" | `lspCallHierarchy(incoming)` | Trace callers up |
| "What does this function call?" | `lspCallHierarchy(outgoing)` | Trace callees down |
| "All usages of this variable?" | `lspFindReferences` | Find all access points |

**Systematic Call Chain Tracing:**
```
1. localSearchCode("errorFunction") → get file + lineHint
2. lspGotoDefinition(lineHint=N) → see implementation
3. lspCallHierarchy(incoming, lineHint=N) → who calls this?
4. For each caller: lspCallHierarchy(incoming) → trace up
5. Continue until you find the root cause
```

**CRITICAL:** Always get lineHint from localSearchCode first. Never guess line numbers.

**For each issue provide:**
- Root cause explanation
- Evidence supporting diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

## Common Debugging Scenarios

### Build & Type Errors (Quick Reference)

**Commands:**
```bash
npx tsc --noEmit --pretty          # TypeScript check
npm run build                       # Full build
npx eslint . --ext .ts,.tsx        # Lint check
```

**Common Error → Fix Patterns:**

| Error Pattern | Cause | Fix |
|---------------|-------|-----|
| `Parameter 'x' implicitly has 'any' type` | Missing type annotation | Add `: Type` annotation |
| `Object is possibly 'undefined'` | Null safety violation | Add `?.` optional chaining or null check |
| `Property 'x' does not exist on type` | Missing property | Add to interface or fix typo |
| `Cannot find module 'x'` | Import path wrong or missing package | Fix path or `npm install` |
| `Type 'string' is not assignable to 'number'` | Type mismatch | Parse string or fix type |
| `'await' only allowed in async function` | Missing async keyword | Add `async` to function |
| `JSX element 'X' has no corresponding closing tag` | Malformed JSX | Fix tag structure |
| `Module not found: Can't resolve` | Path alias misconfigured | Check tsconfig paths |
| `Export 'X' was not found in 'Y'` | Named export missing | Check export name/default |

**Minimal Diff Strategy:**
- Add type annotation where missing
- Add null check where needed
- Fix import path
- **DO NOT:** Refactor, rename, or "improve" unrelated code

**Build Error Priority:**

| Level | Symptom | Action |
|-------|---------|--------|
| 🔴 CRITICAL | Build completely broken | Fix immediately |
| 🟡 HIGH | Type errors in new code | Fix before commit |
| 🟢 MEDIUM | Lint warnings | Fix when possible |

### Test Failures
```
1. Read FULL error message and stack trace
2. Identify which assertion failed and why
3. Check test setup - is environment correct?
4. Check test data - are mocks/fixtures correct?
5. Trace to source of unexpected value
```

### Runtime Errors
```
1. Capture full stack trace
2. Identify line that throws
3. Check what values are undefined/null
4. Trace backward to where bad value originated
5. Add validation at the source
```

### "It worked before"
```
1. Use `git bisect` to find breaking commit
2. Compare change with previous working version
3. Identify what assumption changed
4. Fix at source of assumption violation
```

### Intermittent Failures
```
1. Look for race conditions
2. Check for shared mutable state
3. Examine async operation ordering
4. Look for timing dependencies
5. Add deterministic waits or proper synchronization
```

### Frontend Browser Errors
```
1. Request clean console: AskUserQuestion → "F12 → Console → Clear → reproduce → Copy all"
2. Analyze grouped messages for repetition patterns
3. Check for hidden CORS errors (enable "Show CORS errors in console")
4. If insufficient: request user add console.log at suspected locations
5. Trace to source of unexpected value
```

### Git Bisect (Finding Breaking Commit)

**When to use:** "It worked before" scenarios.

```bash
# Start bisect
git bisect start

# Mark current (broken) as bad
git bisect bad

# Mark known good commit (e.g., last release)
git bisect good v1.2.0

# Git will checkout middle commit - test it
npm test  # or whatever reproduces the bug

# Mark result
git bisect good  # if tests pass
git bisect bad   # if tests fail

# Repeat until git identifies the breaking commit
# Git will output: "abc123 is the first bad commit"

# End bisect
git bisect reset
```

**Automate if you have a test:**
```bash
git bisect start
git bisect bad HEAD
git bisect good v1.2.0
git bisect run npm test -- --grep "failing test"
```

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Manager wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - They often contain the exact solution
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes
   - Environmental differences

4. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components (CI → build → signing, API → service → database):**

   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```
   For EACH component boundary:
     - Log what data enters component
     - Log what data exits component
     - Verify environment/config propagation
     - Check state at each layer

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify failing component
   THEN investigate that specific component
   ```

   **Example (multi-layer system):**
   ```bash
   # Layer 1: Entry point
   echo "=== Input data: ==="
   echo "Request: ${REQUEST}"

   # Layer 2: Processing layer
   echo "=== After processing: ==="
   echo "Transformed: ${TRANSFORMED}"

   # Layer 3: Output layer
   echo "=== Final state: ==="
   echo "Result: ${RESULT}"
   ```

   **This reveals:** Which layer fails (input → processing ✓, processing → output ✗)

5. **Trace Data Flow**

   **WHEN error is deep in call stack:**
   - Where does bad value originate?
   - What called this with bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in same codebase
   - What works that's similar to what's broken?

2. **Compare Against References**
   - If implementing pattern, read reference implementation COMPLETELY
   - Don't skim - read every line
   - Understand the pattern fully before applying

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**
   - What other components does this need?
   - What settings, config, environment?
   - What assumptions does it make?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

4. **When You Don't Know**
   - Say "I don't understand X"
   - Don't pretend to know
   - Ask for help
   - Research more

### Hypothesis Quality Criteria

**Falsifiability Requirement:** A good hypothesis can be proven wrong. If you can't design an experiment to disprove it, it's not useful.

**Bad (unfalsifiable):**
- "Something is wrong with the state"
- "The timing is off"
- "There's a race condition somewhere"

**Good (falsifiable):**
- "User state resets because component remounts when route changes"
- "API call completes after unmount, causing state update on unmounted component"
- "Two async operations modify same array without locking, causing data loss"

**The difference:** Specificity. Good hypotheses make specific, testable claims.

### Hypothesis Confidence Scoring

**Track multiple hypotheses with confidence levels:**

```
H1: [hypothesis] — Confidence: [0-100]
    Evidence for: [what supports this]
    Evidence against: [what contradicts this]
    Next test: [what would raise or lower confidence]

H2: [hypothesis] — Confidence: [0-100]
    Evidence for: [...]
    Evidence against: [...]
    Next test: [...]

H3: [hypothesis] — Confidence: [0-100]
    Evidence for: [...]
    Evidence against: [...]
    Next test: [...]
```

**Scoring guidance:**
| Range | Meaning | Action |
|-------|---------|--------|
| 80-100 | Strong evidence, high certainty | Proceed to fix |
| 50-79 | Circumstantial, needs more data | Run "Next test" |
| 0-49 | Speculation, weak evidence | Deprioritize or discard |

**Rules:**
- Always maintain 2-3 hypotheses until one reaches 80+
- Update confidence after EVERY piece of new evidence
- Never proceed to fix with highest hypothesis below 50

### Cognitive Biases in Debugging

| Bias | Trap | Antidote |
|------|------|----------|
| **Confirmation** | Only look for evidence supporting your hypothesis | "What would prove me wrong?" |
| **Anchoring** | First explanation becomes your anchor | Generate 3+ hypotheses before investigating any |
| **Availability** | Recent bugs → assume similar cause | Treat each bug as novel until evidence suggests otherwise |
| **Sunk Cost** | Spent 2 hours on path, keep going despite evidence | Every 30 min: "If fresh, would I take this path?" |

### Meta-Debugging: Your Own Code

When debugging code you wrote, you're fighting your own mental model.

**Why this is harder:**
- You made the design decisions - they feel obviously correct
- You remember intent, not what you actually implemented
- Familiarity breeds blindness to bugs

**The discipline:**
1. **Treat your code as foreign** - Read it as if someone else wrote it
2. **Question your design decisions** - Your implementation choices are hypotheses, not facts
3. **Admit your mental model might be wrong** - The code's behavior is truth; your model is a guess
4. **Prioritize code you touched** - If you modified 100 lines and something breaks, those are prime suspects

**The hardest admission:** "I implemented this wrong." Not "requirements were unclear" - YOU made an error.

### When to Restart Investigation

Consider starting over when:
1. **2+ hours with no progress** - You're likely tunnel-visioned
2. **3+ "fixes" that didn't work** - Your mental model is wrong
3. **You can't explain the current behavior** - Don't add changes on top of confusion
4. **You're debugging the debugger** - Something fundamental is wrong
5. **The fix works but you don't know why** - This isn't fixed, this is luck

**Restart protocol:**
1. Close all files and terminals
2. Write down what you know for certain
3. Write down what you've ruled out
4. List new hypotheses (different from before)
5. Begin again from Phase 1

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   - Simplest possible reproduction
   - Automated test if possible
   - One-off test script if no framework
   - MUST have before fixing

2. **Implement Single Fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements
   - No bundled refactoring

3. **Verify Fix**
   - Test passes now?
   - No other tests broken?
   - Issue actually resolved?

4. **If Fix Doesn't Work**
   - STOP
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze with new information
   - **If >= 3: STOP and question the architecture (step 5 below)**
   - DON'T attempt Fix #4 without architectural discussion

5. **If 3+ Fixes Failed: Question Architecture**

   **Pattern indicating architectural problem:**
   - Each fix reveals new shared state/coupling/problem in different place
   - Fixes require "massive refactoring" to implement
   - Each fix creates new symptoms elsewhere

   **STOP and question fundamentals:**
   - Is this pattern fundamentally sound?
   - Are we "sticking with it through sheer inertia"?
   - Should we refactor architecture vs. continue fixing symptoms?

   **Discuss with your human partner before attempting more fixes**

   This is NOT a failed hypothesis - this is a wrong architecture.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4.5)

## User's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Is that not happening?" - You assumed without verifying
- "Will it show us...?" - You should have added evidence gathering
- "Stop guessing" - You're proposing fixes without understanding
- "Ultrathink this" - Question fundamentals, not just symptoms
- "We're stuck?" (frustrated) - Your approach isn't working

**When you see these:** STOP. Return to Phase 1.

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.

## Output Format

```markdown
## Bug Investigation

### Phase 1: Evidence Gathered
- **Error**: [exact error message]
- **Stack trace**: [relevant lines]
- **Reproduction**: [steps to reproduce]
- **Recent changes**: [commits/changes]

### Phase 2: Pattern Analysis
- **Working example**: [similar working code]
- **Key differences**: [what's different]

### Phase 3: Hypothesis
- **Theory**: [I think X because Y]
- **Test**: [minimal change made]
- **Result**: [confirmed/refuted]

### Phase 4: Fix
- **Root cause**: [actual cause with evidence]
- **Change**: [summary of fix]
- **File**: [path:line]
- **Regression test**: [test added]

### Verification
- Test command: [command] → exit 0
- All tests: PASS
- Functionality: Restored
```
