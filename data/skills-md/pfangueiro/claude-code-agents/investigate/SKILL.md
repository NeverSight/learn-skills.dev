---
name: investigate
description: Deep root cause analysis engine. Systematically investigates bugs, crashes, unexpected behavior, and performance issues through an 8-phase diagnostic protocol. Uses structured reasoning (sequential-thinking MCP), multi-pass codebase analysis, git forensics, evidence-based hypothesis testing, and the 5 Whys method. Never jumps to a fix — always proves the root cause first.
disable-model-invocation: true
argument-hint: "<bug description, error message, or symptom>"
---

# Investigate — Root Cause Analysis Engine

Systematic deep investigation protocol. Finds the REAL cause, not the surface symptom.

**Core principle:** Never fix what you don't understand. Every fix must trace to a proven root cause with evidence.

## Protocol

Process every `/investigate` invocation through these 8 phases in strict order. Never skip a phase. Never jump to Phase 7 (FIX) without completing Phases 1-6.

---

### Phase 1: OBSERVE — Gather All Symptoms

Collect every observable fact before forming any theory.

1. Parse `$ARGUMENTS` as the symptom description
2. Ask the user for additional context if the description is vague — use AskUserQuestion:
   - What's the expected behavior vs actual behavior?
   - When did it start? What changed recently?
   - Is it consistent or intermittent?
   - Any error messages, logs, or stack traces?
3. Check memory files for known pitfalls related to this area:
   - Read MEMORY.md and any topic-specific memory files
   - Check CLAUDE.md for documented patterns
4. Gather environmental context:
   - Run `git log --oneline -20` to see recent changes
   - Run `git diff --stat HEAD~5` to see what files changed recently
   - Check for any failing tests with the project's test runner

**Output:** A symptom report listing every observable fact, recent changes, and any relevant memory entries.

**Gate:** Do NOT theorize yet. Only facts.

---

### Phase 2: REPRODUCE — Confirm the Issue

An issue you cannot reproduce is an issue you cannot prove you fixed.

1. Identify the shortest path to trigger the symptom:
   - Run existing tests that cover the affected area
   - If no test exists, attempt manual reproduction via Bash
   - For UI issues, check if a Playwright MCP sequence can reproduce it
2. Document the reproduction steps precisely
3. If the issue is **intermittent**:
   - Flag it as potentially timing-dependent (race condition, async, state)
   - Look for concurrent access, shared mutable state, missing locks/guards
   - Check for dependency on external state (network, filesystem, database)
4. If the issue **cannot be reproduced**:
   - Shift to forensic investigation (logs, git history, code review)
   - Do NOT skip remaining phases — proceed with available evidence

**Output:** Reproduction steps, or explicit documentation of why reproduction failed.

**Gate:** Issue confirmed (or forensic mode declared). Proceed.

---

### Phase 3: TRACE — Follow the Execution Path

Start from the symptom and trace backward to the origin.

1. **Locate the symptom** — find the exact file and line where the error occurs:
   - Use Grep for error messages, exception types, log strings
   - Use Explore agent for broad searches if the location is unclear
2. **Trace the call chain** — read every file in the execution path:
   - From error site → caller → caller's caller → entry point
   - Read each file fully with Read tool — do NOT skim
   - Document the complete flow: input → transform → output
3. **Trace the data flow** — follow the data that caused the error:
   - What value caused the crash? Where did it come from?
   - Trace the value backward: variable → assignment → source → input
4. **Map dependencies** — what else touches this code path:
   - Use Grep to find all callers of the failing function
   - Check for shared state, singletons, global variables
   - Look for recent changes in dependencies with `git log --oneline -- <file>`
5. **Check git forensics** — when was the problem introduced:
   - `git log --oneline -- <affected-files>` — who changed these files and when?
   - `git blame <file>` on the suspicious lines — what commit introduced them?
   - If a clear suspect commit is found, read its full diff

**Output:** Complete execution trace with file paths and line numbers. Data flow map. Git timeline.

**Gate:** The full code path from entry point to symptom is mapped and understood.

---

### Phase 4: HYPOTHESIZE — Deep Reasoning with 5 Whys

**This phase MUST use the sequential-thinking MCP server** for structured multi-step reasoning.

1. Start the sequential-thinking chain with the symptom and all evidence from Phases 1-3
2. Apply the **5 Whys method** — for each answer, ask "but why does THAT happen?":
   ```
   Symptom: App crashes when tapping a document
   Why 1: DocumentDetailView accesses a deleted NSManagedObject
   Why 2: The object was deleted from Core Data while the view held a reference
   Why 3: context.delete() was called from a background operation
   Why 4: The background sync didn't check if the view was still displaying the object
   Why 5: There's no soft-delete pattern — objects are hard-deleted immediately
   ROOT CAUSE: Missing soft-delete guard in the sync pipeline
   ```
3. Generate **at least 2 competing hypotheses** — don't lock on the first theory:
   - Categorize each by type: Code Logic | Data State | Timing/Race | Environment | Dependency | Configuration
   - For each hypothesis, define what evidence would prove or disprove it
4. Use **branching** in sequential-thinking to explore alternative explanations:
   ```
   branchFromThought: 3, branchId: "alternative-cause"
   ```
5. Rank hypotheses by likelihood based on available evidence

**Output:** Ranked list of hypotheses with evidence requirements for each.

**Gate:** At least 2 hypotheses generated. Each has defined proof criteria.

---

### Phase 5: PROVE — Test Each Hypothesis with Evidence

Systematically confirm or eliminate each hypothesis. No guessing.

**For each hypothesis (highest-ranked first):**

1. **Gather confirming evidence:**
   - Read the specific code paths predicted by the hypothesis
   - Check logs/output for patterns the hypothesis predicts
   - Run targeted tests that would pass if the hypothesis is correct
   - Use `git blame` / `git log` to check if timing matches
2. **Gather disconfirming evidence:**
   - Look for code paths that should also fail if the hypothesis is correct but don't
   - Check edge cases that contradict the hypothesis
3. **Check external sources:**
   - Use WebSearch for known issues in the library/framework version
   - Use library-docs skill (context7 MCP) to verify correct API usage
   - Search GitHub issues for the library: `mcp__github__search_issues`
4. **Verdict per hypothesis:**
   - **CONFIRMED** — evidence supports it, no contradictions
   - **ELIMINATED** — evidence contradicts it
   - **INCONCLUSIVE** — need more evidence (define what)

**If all hypotheses are eliminated:** Return to Phase 4 with new evidence. Generate new hypotheses.

**Output:** Evidence log per hypothesis. One confirmed root cause (or request for more data).

**Gate:** Exactly one root cause confirmed with evidence. Or an explicit statement that the cause requires additional data from the user (with specific questions).

---

### Phase 6: ROOT CAUSE — Document the Causal Chain

Write the definitive explanation before touching any code.

1. Document the complete causal chain:
   ```
   ROOT CAUSE: <the deepest systemic issue>
     → causes: <intermediate effect>
       → causes: <intermediate effect>
         → manifests as: <the symptom the user reported>
   ```
2. Explain **why** this is the root cause (not just a proximate cause):
   - If fixed, would it prevent recurrence? (yes = root cause)
   - Is there a deeper cause? (if yes, keep digging)
3. Identify the **blast radius** — what else is affected:
   - Are there similar patterns elsewhere in the codebase?
   - Use Grep to find analogous code that may have the same bug
4. Present the root cause analysis to the user before proceeding to fix

**Output:** Root cause statement, causal chain, blast radius assessment.

**Gate:** User understands and agrees with the diagnosis before any fix is attempted.

---

### Phase 7: FIX — Address the Root Cause

Fix the root cause, not the symptom. Minimal, targeted change.

1. Design the fix:
   - What is the minimum change that eliminates the root cause?
   - Does the fix handle all cases in the blast radius (Phase 6)?
   - Does the fix introduce any new risks?
2. Implement the fix:
   - Read every file before modifying it
   - Make the smallest change possible
   - Add inline comments only where the fix is non-obvious
3. Verify the fix:
   - Run the reproduction steps from Phase 2 — symptom should be gone
   - Run existing tests — no regressions
   - Run code-quality agent on modified files if the change is substantial
4. Check for similar patterns:
   - If the bug was a pattern (e.g., missing null check), search for the same pattern elsewhere
   - Fix all instances, not just the reported one

**Output:** Code changes with explanation of what was changed and why.

---

### Phase 8: PREVENT — Ensure It Never Recurs

The investigation isn't complete until recurrence is prevented.

1. **Add a regression test** that would have caught this bug:
   - The test must fail without the fix and pass with it
   - Use test-automation agent for comprehensive test generation
2. **Update project memory** if a new pitfall was discovered:
   - Add to MEMORY.md under Common Pitfalls
   - Include the pattern, why it's dangerous, and the safe alternative
3. **Suggest structural improvements** (optional, only if the bug reveals a design flaw):
   - Propose architectural changes that make this class of bug impossible
   - Present as a suggestion, not an immediate action
4. **Write the investigation summary:**

```
## Investigation Report

**Symptom:** <what was reported>
**Root Cause:** <the deepest systemic issue>
**Causal Chain:** root cause → ... → symptom
**Fix:** <what was changed, which files>
**Blast Radius:** <other areas checked/fixed>
**Regression Test:** <test added>
**Prevention:** <memory updated, guard added, pattern documented>
**Time:** <phases completed, hypotheses tested>
```

---

## Tool Usage by Phase

| Phase | Primary Tools | When to Use Agents |
|-------|--------------|-------------------|
| 1. OBSERVE | Read, Grep, Bash (git log) | — |
| 2. REPRODUCE | Bash (test runner), Playwright MCP | — |
| 3. TRACE | Read, Grep, Glob, Bash (git blame) | Explore agent for broad searches |
| 4. HYPOTHESIZE | sequential-thinking MCP | deep-analysis skill |
| 5. PROVE | Read, Grep, Bash, WebSearch, context7 MCP | library-docs skill, GitHub MCP |
| 6. ROOT CAUSE | Read, Grep | Explore agent for blast radius |
| 7. FIX | Read, Edit, Write, Bash | code-quality agent for review |
| 8. PREVENT | Write, Edit, Bash | test-automation agent for tests |

## Anti-Patterns — What This Skill Prevents

| Bad Habit | What `/investigate` Does Instead |
|-----------|--------------------------------|
| Jump straight to fixing | Forces Phases 1-6 before any code change |
| Fix the symptom | 5 Whys drills to root cause |
| Single theory tunnel vision | Requires 2+ competing hypotheses |
| "It works now" without understanding | Demands evidence-based proof |
| Fix one instance, miss others | Blast radius analysis in Phase 6 |
| No regression test | Phase 8 mandates a test |
| Knowledge lost | Memory update in Phase 8 |

## When to Use `/investigate` vs Other Tools

| Situation | Use |
|-----------|-----|
| Bug, crash, error, unexpected behavior | `/investigate` |
| Build a new feature | `/execute` |
| Quick "what does this code do?" | Explore agent directly |
| Performance slow but unclear why | `/investigate` (treat slowness as symptom) |
| Known fix, just need to apply it | Direct Edit — no investigation needed |
| Security vulnerability found | `/investigate` + security-scan |

## References

See [references/investigation-frameworks.md](references/investigation-frameworks.md) for detailed methodology guides.
