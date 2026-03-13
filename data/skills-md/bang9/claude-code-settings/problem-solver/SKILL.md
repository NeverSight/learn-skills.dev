---
name: problem-solver
description: Systematic problem-solving workflow for bug fixes and feature implementations. Use when debugging issues, fixing bugs, implementing features, or when the user describes unexpected behavior, errors, or needs a methodical approach to code changes. Ensures reproducible verification and validates solutions are fundamental fixes rather than workarounds.
---

# Problem Solver

A structured workflow for solving problems through iterative planning, reproduction, implementation, and validation.

## When This Skill Activates

- User describes a bug or unexpected behavior
- User requests a feature implementation
- User mentions "fix", "debug", "implement", "solve", or "issue"
- Complex code changes requiring systematic approach

## Workflow Overview

```
Phase 0: Input Collection (gather info from user)
    ↓
Phase 1: First-Pass Planning & Execution
    Step 1.1 → 1.2 → 1.3 → [1.4 ↔ 1.5 iterate until solved]
    ↓
Phase 2: Solution Validation
    ↓
    ├─→ Fundamental Fix → Complete
    └─→ Workaround → Return to Phase 1 with new approach
```

---

## Phase 0: Input Collection

> **Purpose**: Gather sufficient information from the user before analysis begins.

### Required Information Checklist

Before starting, ensure you have:

- [ ] **Scope**: Files, directories, components involved
- [ ] **Resources**: Available tools, MCP servers, test commands
- [ ] **Expected behavior**: What should happen
- [ ] **Actual behavior**: What is happening instead
- [ ] **Reproduction steps**: How to trigger the issue (if known)

### Clarification Protocol

If any required information is unclear or ambiguous:

1. **Stop and ask** - Do not assume or guess
2. **Be specific** - Ask targeted questions, not open-ended ones
3. **Confirm understanding** - Restate the problem before proceeding

> Use AskUserQuestion tool when clarification is needed.

---

## Phase 1: First-Pass Planning & Execution

> **Planning (Step 1.1-1.3) is the most critical part.** Do not rush to implementation. A well-understood problem with a solid plan leads to a fundamental solution.

### Step 1.1: Requirements Definition

> **Purpose**: Structure and analyze the collected information into actionable requirements.

1. List all requirements as bullet points
2. Identify any ambiguous terms or conditions
3. Ask clarifying questions if needed
4. Get user confirmation before proceeding

### Step 1.2: Information Gathering

1. **Locate relevant code** using Grep, Glob, Read
2. **Trace data flow** from input to output
3. **Identify dependencies** and side effects
4. **Document findings** for reference

### Step 1.3: Reproduction Environment (Critical)

Establish a verifiable reproduction **before** making changes.

Choose appropriate method(s) based on the problem type. Combine as needed:

| Problem Type | Method | Example |
|--------------|--------|---------|
| Logic bugs, calculations | Test code | Unit test that fails with current bug |
| UI rendering, interactions | Mock data + UI | Storybook, dev server with fixture data |
| Timing, state, intermittent | Logging | Console logs at key execution points |

> Methods are not mutually exclusive. For example, UI bugs may benefit from mock data + logging together, or a complex state bug might need all three approaches.

**Verification checkpoint**: Can you reliably trigger the issue?

### Step 1.4: Implementation

> Only proceed to implementation when Step 1.1-1.3 are thoroughly completed. Skipping planning leads to workarounds, not fundamental fixes.

1. Create task list with TodoWrite
2. Implement in small, testable increments
3. Run verification after each change
4. Document any deviations from plan

### Step 1.5: Verification

- [ ] Issue no longer reproduces in test environment (run multiple times for intermittent issues)
- [ ] All existing tests pass
- [ ] Edge cases considered and handled
- [ ] No new warnings or errors introduced

> For intermittent or timing-related issues, a single successful test is not sufficient. Run verification multiple times to ensure the fix is reliable.

---

## Phase 2: Solution Validation

### Analysis Questions

Answer each question honestly:

1. **Root cause addressed?** Does this fix the underlying cause, or mask symptoms?
2. **Recurrence risk?** Could similar inputs cause the same problem?
3. **Side effects?** Are other parts of the system affected?
4. **Code quality?** Is the solution clean and maintainable?

### Decision Matrix

| Indicator | Fundamental Fix | Workaround |
|-----------|-----------------|------------|
| Addresses root cause | Yes | No |
| Similar cases handled | Yes | No |
| Code feels natural | Yes | Feels forced |
| Future-proof | Yes | Fragile |

### If Workaround Detected

1. **Document** why current approach is a workaround
2. **Identify** what a fundamental fix would require
3. **Return to Phase 1** with new approach
4. **Repeat** until fundamental fix achieved

---

## Completion Criteria

All must be true:

- [ ] Problem verified as resolved
- [ ] All tests passing
- [ ] Solution validated as fundamental (not workaround)
- [ ] Changes documented/committed appropriately

---

## Quick Reference

For detailed checklists and examples, see:
- [Analysis Checklist](references/ANALYSIS.md)
- [Reproduction Strategies](references/PATTERNS.md)
