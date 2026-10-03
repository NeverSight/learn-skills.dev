---
name: cc-quality-practices
description: "Applies Code Complete's QA process design: selects defect-detection techniques by phase, sizes the test suite, and designs review and inspection processes. For QA planning and process design, not active bug investigation (use cc-debugging)."
user-invocable: false
---

# cc-quality-practices

Improving quality reduces development cost. No single defect-detection technique exceeds ~75% effectiveness, so combine techniques — combining nearly doubles detection rates. Mature suites run about 5 dirty tests (error paths, bad data, edge cases) for every 1 clean test (happy path).

For active bug diagnosis (an actual failing test or repro to chase down), hand off: `Skill(code-foundations:cc-debugging)`. This skill is for QA planning and process design.

Shared CC vocabulary and thresholds (cohesion spectrum, coupling, key metrics): `Read(${CLAUDE_PLUGIN_ROOT}/references/cc-foundations.md)`.

## External vs internal quality

- **External** (users care): correctness, usability, efficiency, reliability, integrity, robustness.
- **Internal** (developers care): maintainability, flexibility, portability, reusability, readability, testability.

Internal quality enables external quality: poor maintainability blocks fixing defects, which degrades reliability.

## Defect-detection techniques (detection rate)

| Technique | Rate | Notes |
|---|---|---|
| Formal inspection | 45–70% | Roles, checklists, preparation. Preparation finds ~90% of the defects; the meeting adds ~10% [Votta 1991]. |
| Pair programming | 40–60% | Real-time review during development. |
| Walk-through | 20–40% | Author-led, less structured. |
| Code reading | 20–35% | Individual review emphasizing preparation. |
| Unit testing | 15–50% | Developer tests of individual components. |

## Modes

### CHECKER

Execute the quality, review, and testing checklists against the code or process. Checklists:

- `Read(${CLAUDE_SKILL_DIR}/checklists/qa-and-testing.md)` — QA plan, inspections, test cases, data-flow.
- `Read(${CLAUDE_SKILL_DIR}/checklists/debugging.md)` — finding, fixing, brute-force, general approach.

Output one row per item: `| Item | Status | Evidence | Location |`, status ∈ VIOLATION (fails item) / WARNING (partial) / PASS.

### APPLIER

Produce test cases, review procedures, and quality plans.

**Test-case generation** (output: test-case list):
1. Identify requirements → one test per requirement.
2. Compute minimum tests: `1 + count(if/while/for/and/or) + case branches` (add 1 if no default case).
3. Add data-flow tests covering all defined-used paths.
4. Add boundary tests: below, at, above each boundary.
5. Add dirty tests at ~5:1 — bad data, wrong size/kind, uninitialized.
6. Add nominal tests: middle-of-road expected values.
7. Run with a coverage monitor — compare actual vs believed coverage.

## Choosing a review method

| Need | Method |
|---|---|
| Highest defect detection (45–70%) | Formal inspection (default) |
| Team geographically dispersed | Code reading (individual prep, async-friendly) |
| Schedule pressure + quality | Pair programming |
| Diverse viewpoints, larger group | Walk-through |

## When advising a human team's review process

Inspection roles and meeting mechanics apply when designing a review process for a human team (not for solo or agent work):

1. PLANNING — moderator distributes materials with line numbers + checklist.
2. PREPARATION — each reviewer works alone using the checklist (where ~90% of defects are found).
3. MEETING — reader paraphrases the code; scribe records defects.
4. REPORT — moderator lists each defect with type and severity.
5. REWORK — author fixes defects.
6. FOLLOW-UP — moderator verifies all fixes complete.

## Chain

| After | Next |
|---|---|
| Defect to fix found | `Skill(code-foundations:cc-refactoring-guidance)` |
| Design issues found | `Skill(code-foundations:cc-routine-and-class-design)` |
| Active bug to diagnose | `Skill(code-foundations:cc-debugging)` |
