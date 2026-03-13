---
name: writing-plans
description: This skill should be used when the user has a spec or requirements for a multi-step task before touching code.
license: MIT
---

# Writing Plans

## Purpose

Create executable, low-ambiguity implementation plans that another engineer can run task-by-task with predictable outcomes.

## When to Use

Use this skill when:
- Requirements/specs exist but implementation has not started
- Work is multi-step and requires coordination across files and tests
- A handoff-ready plan is needed for another session or engineer

## Progress Tracking

Display progress at each planning phase:

```
[████░░░░░░░░░░░░░░░░] 25% — Phase 1/4: Gathering Context & Constraints
[████████░░░░░░░░░░░░] 50% — Phase 2/4: Decomposing Into Tasks
[████████████░░░░░░░░] 75% — Phase 3/4: Specifying Files & Commands
[████████████████████] 100% — Phase 4/4: Writing & Saving Plan
```

## Workflow

1. Gather context and constraints
2. Break work into bite-sized, test-first tasks
3. Specify exact files, code snippets, and commands
4. Add validation criteria and expected outputs
5. Save plan and hand off to `executing-plans`

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses superpowers:executing-plans

## Critical Rules

- Always include exact paths and exact commands.
- Always define expected outcomes for test/verification steps.
- Never leave steps abstract (avoid "implement validation" without concrete code intent).

## Example Usage

1. "Use writing-plans to plan migration from REST to GraphQL."
2. "Use writing-plans to break down an auth refactor into TDD tasks."
3. "Use writing-plans to prepare a handoff plan for a new caching layer."
