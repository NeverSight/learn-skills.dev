---
name: rlm-tdd
description: 'Use when implementing any code in RLM Phase 3. Enforces strict RED-GREEN-REFACTOR discipline with The Iron Law - no production code without a failing test first. Trigger phrases: "implement this", "add feature", "fix bug", "write a failing test", "TDD".'
---

# RLM TDD Discipline

## Overview

Test-Driven Development is mandatory for all RLM implementation work. This skill ensures test-first discipline is followed rigorously.

**Core Principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**The Iron Law for RLM:**
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

## Trigger examples

- `Implement Phase 3 for run '2026-02-24-add-oauth'`
- `Add a failing regression test first, then fix the bug`
- `I already wrote the code; now add tests` (should trigger TDD reset guidance)
- `Follow RED-GREEN-REFACTOR for this change`

## When to Use

**Always in Phase 3 (Implementation):**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**No Exceptions:**
- Not for "simple" changes
- Not when "under pressure"
- Not because "tests after achieve same goals"

## RED-GREEN-REFACTOR Cycle

```dot
digraph tdd_cycle {
    rankdir=LR;
    red [label="RED\nWrite failing test", shape=box, style=filled, fillcolor="#ffcccc"];
    verify_red [label="Verify fails\ncorrectly", shape=diamond];
    green [label="GREEN\nMinimal code", shape=box, style=filled, fillcolor="#ccffcc"];
    verify_green [label="Verify passes\nAll green", shape=diamond];
    refactor [label="REFACTOR\nClean up", shape=box, style=filled, fillcolor="#ccccff"];
    record [label="Record in\nPhase 3 artifact", shape=box];

    red -> verify_red;
    verify_red -> green [label="yes"];
    verify_red -> red [label="wrong\nfailure"];
    green -> verify_green;
    verify_green -> refactor [label="yes"];
    verify_green -> green [label="no"];
    refactor -> verify_green [label="stay\ngreen"];
    verify_green -> record;
}
```

### RED - Write Failing Test

Write one minimal test showing what should happen.

**Requirements:**
- One behavior per test
- Clear, descriptive name
- Test real code (no mocks unless unavoidable)
- Clear assertion showing expected outcome

<Good>
```typescript
test('rejects empty email with clear error message', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email is required');
});
```
</Good>

<Bad>
```typescript
test('email validation works', async () => {
  const mock = jest.fn().mockResolvedValue({ valid: true });
  const result = await validateEmail(mock);
  expect(mock).toHaveBeenCalled();
});
```
</Bad>

### Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
npm test path/to/test.test.ts
```

**Confirm:**
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**Record in Phase 3 artifact:**
```markdown
### TDD Cycle for R3 (Email Validation)

**RED Phase:**
- Test: `rejects empty email with clear error message`
- Command: `npm test src/forms/email.test.ts`
- Expected failure: "Email is required" not found
- Actual failure: [paste output]
- RED verified: ✅
```

### GREEN - Minimal Code

Write simplest code to pass the test.

**Rules:**
- Just enough to pass
- No additional features
- No "while I'm here" improvements
- No refactoring yet

<Good>
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email is required' };
  }
  // ... rest of form handling
}
```
</Good>

<Bad>
```typescript
function submitForm(
  data: FormData,
  options?: {
    strictMode?: boolean;
    customValidators?: Validator[];
    onValidationError?: (err: Error) => void;
  }
) {
  // YAGNI - over-engineered
}
```
</Bad>

**Record in Phase 3 artifact:**
```markdown
**GREEN Phase:**
- Implementation: Added null check for email field
- Command: `npm test src/forms/email.test.ts`
- Result: PASS
- GREEN verified: ✅
```

### REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers
- Keep tests green

**Never add behavior during refactor.**

**Record in Phase 3 artifact:**
```markdown
**REFACTOR Phase:**
- Extracted `validateRequired(field, name)` helper
- Renamed `submitForm` to `processFormSubmission` for clarity
- All tests still passing: ✅
```

## Common Rationalizations (STOP - You're Rationalizing)

| Excuse | Reality |
|--------|---------|
| "This is just a simple fix, no test needed" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after confirming the fix works" | Tests passing immediately prove nothing. You never saw it catch the bug. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "I already manually tested it" | Ad-hoc ≠ systematic. No record, can't re-run, no regression protection. |
| "Deleting working code is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "TDD is dogmatic, I'm being pragmatic" | TDD IS pragmatic. Finds bugs before commit, enables refactoring. |
| "I'll keep the code as reference" | You'll adapt it. That's testing after. Delete means delete. |
| "Test hard = design unclear" | Listen to the test. Hard to test = hard to use. Simplify design. |
| "I need to explore first" | Fine. Throw away exploration, start TDD fresh. |
| "This is different because..." | It's not. The rules don't have exceptions. |

## Red Flags - STOP and Start Over

If you encounter any of these, DELETE CODE and restart with TDD:

- ❌ Code written before test
- ❌ Test passes immediately (not testing what you think)
- ❌ "I'll add tests later"
- ❌ "This is too simple to test"
- ❌ "I know what I'm doing, I don't need the ritual"
- ❌ Can't explain why test failed (or didn't fail)
- ❌ Test testing mock behavior, not real behavior
- ❌ Multiple behaviors in one test ("and" in test name)

## Integration with RLM Phase 3

### Phase 3 Artifact TDD Section

Every Phase 3 artifact must include:

```markdown
## TDD Compliance Log

### Requirement R1 (Feature X)

**Test:** `test/features/x.test.ts` - "should do Y when Z"
- RED: [timestamp] - Failed as expected: [output]
- GREEN: [timestamp] - Minimal implementation: [description]
- REFACTOR: [timestamp] - Cleanups: [description]
- Final state: ✅ All tests passing

### Requirement R2 (Bug Fix)

**Regression Test:** `test/bugs/issue-123.test.ts` - "reproduces crash on empty input"
- RED: [timestamp] - Confirmed bug: [output]
- GREEN: [timestamp] - Fix applied: [description]
- REFACTOR: [timestamp] - N/A (minimal fix)
- Final state: ✅ Test passes, bug fixed
```

### Phase 3 Coverage Gate Addition

```markdown
## Coverage Gate

- [ ] Every new function has a corresponding test
- [ ] Every bug fix has a regression test that fails before fix
- [ ] All RED phases documented with failure output
- [ ] All GREEN phases documented with minimal implementation
- [ ] All tests passing (no skipped tests)
- [ ] No production code written before failing test

TDD Compliance: PASS / FAIL
```

### Phase 3 Approval Gate Addition

```markdown
## Approval Gate

- [ ] TDD Compliance: PASS
- [ ] Implementation matches Phase 3 plan
- [ ] No code without preceding failing test
- [ ] All tests documented in TDD Compliance Log

Approval: PASS / FAIL
```

## Bug Fix TDD Procedure

1. **Add Regression Test First**
   - Write test that reproduces the bug
   - Run test, confirm it fails with expected error
   - Document failure in Phase 3 artifact

2. **Implement Minimal Fix**
   - Fix only what's needed to make test pass
   - Run test, confirm it passes
   - Document fix in Phase 3 artifact

3. **Verify No Regressions**
   - Run full test suite
   - Confirm nothing else broke
   - Document in Phase 3 artifact

4. **Lock Phase 3**
   - TDD Compliance: PASS
   - Approval: PASS
   - Status: LOCKED

## Example: Complete Phase 3 TDD Section

```markdown
## TDD Compliance Log

### R1: Add email validation

**Test:** `test/forms/validation.test.ts`

RED Phase (2026-02-21T10:15:00Z):
```bash
$ npm test test/forms/validation.test.ts
FAIL: Expected 'Email is required', got undefined
```
RED verified: ✅

GREEN Phase (2026-02-21T10:18:00Z):
- Added null check in `submitForm()` function
- Test passes
GREEN verified: ✅

REFACTOR Phase (2026-02-21T10:22:00Z):
- Extracted `validateRequired()` helper
- All tests still passing
REFACTOR complete: ✅

### R2: Fix crash on empty array

**Regression Test:** `test/utils/array.test.ts`

RED Phase (2026-02-21T10:25:00Z):
```bash
$ npm test test/utils/array.test.ts
FAIL: TypeError: Cannot read property 'map' of undefined
```
RED verified: Bug reproduced ✅

GREEN Phase (2026-02-21T10:27:00Z):
- Added guard clause in `processItems()`
- Test passes
GREEN verified: ✅

REFACTOR: N/A (minimal 2-line fix)

## Verification

Full suite run: `npm test`
Result: 47 passing, 0 failing
```

## References

- **REQUIRED:** Follow this skill for all Phase 3 implementation work
- **SEE ALSO:** `references/rationalizations.md` for extended excuse/reality table
