---
name: tdd-cycle
description: Execute a complete TDD cycle (RED → GREEN → REFACTOR) for one test. Orchestrates the full workflow from writing a failing test through implementation and refactoring to commit.
---

# Complete TDD Cycle

## Overview

This skill orchestrates a complete Test-Driven Development cycle, guiding through all phases: RED (write failing test), GREEN (make it pass), REFACTOR (improve structure), and proper commits. Use this when you want to complete one full TDD iteration.

## When to Use

Use this skill when:
- Ready to implement next test from PLAN.md
- Want to follow complete TDD workflow
- Need guidance through all TDD phases
- Want structured approach to one iteration
- Following disciplined TDD practice

## Complete Workflow

### Phase 1: RED - Write Failing Test

**Execute tdd-red skill:**
1. Find next unmarked test in PLAN.md
2. Write a failing test with Korean description
3. Run tests to confirm failure
4. Mark test as [ ] in PLAN.md

**Success Criteria:**
- Test fails for the right reason (missing functionality)
- Test name clearly describes behavior
- All other tests still pass
- No compilation errors

**Use:** `/red` command or `tdd-red` skill

---

### Phase 2: GREEN - Make It Pass

**Execute tdd-green skill:**
1. Verify we have a failing test
2. Implement MINIMUM code to make test pass
3. Run ALL tests to confirm they pass
4. Mark test as [x] in PLAN.md

**Success Criteria:**
- New test now passes
- All existing tests still pass
- No compiler warnings
- Used simplest possible implementation

**Use:** `/green` command or `tdd-green` skill

---

### Phase 3: REFACTOR - Improve Structure

**Execute tdd-refactor skill (if needed):**
1. Verify all tests are passing
2. Identify code smells or duplication
3. Make structural improvements one at a time
4. Run tests after each change
5. Keep tests green throughout

**Success Criteria:**
- All tests still passing
- Code quality improved
- Duplication reduced
- Structure is clearer

**When to Skip:**
- Code is already clean
- No obvious improvements needed
- Would be premature optimization

**Use:** `/refactor` command or `tdd-refactor` skill

---

### Phase 4: COMMIT - Save Progress

**Commit Strategy:**

**If Structural Changes Were Made:**
1. First, commit structural changes separately:
   ```
   /commit-tidy
   ```
   - Use "refactor:" or "tidy:" prefix
   - Clearly indicate structural changes only

2. Then, commit behavioral changes:
   ```
   /commit-behavior
   ```
   - Use "feat:", "fix:", or appropriate prefix
   - Describe what functionality was added

**If No Structural Changes:**
- Just commit behavioral changes:
  ```
  /commit-behavior
  ```

**Commit Prerequisites:**
- ALL tests passing
- NO compiler warnings
- NO linter errors
- Clear commit message

---

### Phase 5: REPEAT - Next Test

**Prepare for Next Cycle:**
1. Verify clean state (all tests pass)
2. Review PLAN.md for next test
3. Start new RED phase when ready

---

## Execution Flow

```
START
  ↓
RED: Write failing test
  ↓
Confirm test fails? ──No──> Fix test
  ↓ Yes
GREEN: Implement minimum code
  ↓
All tests pass? ──No──> Debug & fix
  ↓ Yes
Need refactoring? ──Yes──> REFACTOR: Improve structure
  ↓ No                        ↓
  ←───────────────────────────┘
COMMIT: Save changes
  ↓
Next test? ──Yes──> START
  ↓ No
DONE
```

## Key Principles

**RED Phase:**
- Write smallest failing test
- Test one thing only
- Fail for right reason

**GREEN Phase:**
- Simplest implementation
- No premature optimization
- Make it work, not perfect

**REFACTOR Phase:**
- Only when green
- One change at a time
- Keep tests green

**COMMIT Phase:**
- Separate structural from behavioral
- All tests passing
- Clear messages

## Important Reminders

- **NEVER** skip RED - always write test first
- **NEVER** write more code than needed in GREEN
- **NEVER** refactor on red tests
- **ALWAYS** run tests after each phase
- **ALWAYS** keep commits small and focused
- **ONE** test at a time
- **ONE** refactoring at a time

## Useful Commands

Within this cycle, you can use:
- `/red` - Execute RED phase
- `/green` - Execute GREEN phase
- `/refactor` - Execute REFACTOR phase
- `/tidy` - Make structural changes (Tidy First)
- `/commit-tidy` - Commit structural changes
- `/commit-behavior` - Commit behavioral changes
- `/run-tests` - Run all tests
- `/next-test` - View next test in PLAN.md

## Example Complete Cycle

1. **RED:** Write test "should calculate total price with discount"
   - Test fails: `calculateTotalWithDiscount is not defined`

2. **GREEN:** Implement basic calculation
   ```typescript
   function calculateTotalWithDiscount(price, discount) {
     return price - discount;
   }
   ```
   - All tests pass

3. **REFACTOR:** Extract validation logic
   - Add input validation
   - Extract discount calculation
   - All tests still pass

4. **COMMIT:**
   - Commit refactoring: "refactor: extract discount calculation logic"
   - Commit feature: "feat: add total price calculation with discount"

5. **REPEAT:** Move to next test

## Next Steps

After completing one full cycle:
1. Verify clean state
2. Check PLAN.md for next test
3. Start new cycle with RED phase
4. Continue until feature complete
