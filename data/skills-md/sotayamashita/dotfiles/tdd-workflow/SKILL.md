---
name: tdd-workflow
description: >-
  Test-driven development with Kent Beck's canonical 5-step workflow: Test List,
  Write Test, Make Pass, Refactor, Repeat. Strict vertical-slice cycles with
  automatic project detection. Use when the user asks to "write tests first",
  "use TDD", "red-green-refactor", "test-driven development", "build a feature
  with TDD", "fix a bug with TDD", wants test-first development for any
  language or framework, or mentions "tracer bullet" or "vertical slice".
---

# Test-Driven Development

## The Essence

TDD is a **design workflow**, not a testing technique.
Writing a test is an **interface design** act — you decide how a behavior should be called.
Making it pass is a **learning** act — you discover the simplest implementation.
Refactoring is an **implementation design** act — you improve internal structure.

Every behavior is born from this cycle:

```
Describe the behavior in a test → Make it real → Clean up
```

A test that errors on import is not a failing test. A cycle that stops at RED is not a cycle.

## Workflow Overview

1. **Detect** project context (test framework, conventions)
2. **Confirm** intent with user (strict TDD vs legacy mode)
3. **Test List** — enumerate behavioral scenarios (alive, evolves during coding)
4. **Cycle** — for each item: Write Test → Make Pass → Refactor → Update List
5. **Verify** test quality and isolation

## Step 0: Detect Project Context

Run `scripts/detect_test_env.sh` from the project root. If the script is unavailable, manually check:

- Test framework (Jest, Vitest, pytest, Go test, cargo test, etc.)
- Test file pattern (`.test.ts`, `.spec.ts`, `_test.go`, `test_*.py`)
- Test execution command (`package.json` scripts, `Makefile`, etc.)
- Existing test directory structure

Adapt all subsequent commands to the detected framework. Never assume `npm test`.

## Step 1: Confirm User Intent

**Strict TDD** (default for new features/bug fixes):
- Write failing test first, then implement

**Legacy mode** (existing code without tests):
- See `references/legacy-mode.md`

**Not applicable** — skip TDD for:
- Configuration files, auto-generated code, declarative CSS, throwaway prototypes

## Step 2: Test List (Dynamic)

Create a list of behaviors this change needs to support. This is behavioral analysis.

```
GOOD (behaviors):              BAD (implementation steps):
- adds two positive numbers    - create Calculator class
- returns 0 for 0 + 0          - implement add() method
- handles negative results     - add validation logic
- rejects non-numeric input    - handle edge cases
```

Rules:
1. Write entries in plain language, not code
2. Each entry describes ONE observable behavior
3. Order from simplest/most central to complex/edge-case
4. Share with user, then start coding — do NOT wait for exhaustive approval
5. **This list is ALIVE** — add, remove, reorder items as you learn from each cycle
6. See `references/test-case-derivation.md` for systematic discovery techniques

## Step 3: TDD Cycles

### One cycle = one behavior. A cycle is NOT complete until GREEN.

Pick one item from the test list. Execute this cycle:

### DO NOT write all tests first, then all implementation.

```
WRONG (horizontal):  test1, test2, test3 → impl1, impl2, impl3
RIGHT (vertical):    test1→impl1 → test2→impl2 → test3→impl3
```

### WRITE THE TEST (Interface Design Happens Here)

Write a test for the chosen behavior. As you write, you are designing the interface:
- Function name, parameters, return type, error format
- The test IS the first client of the API — design for the caller

Use Arrange-Act-Assert. Your assertion must express a CONCRETE expected value.
**Never compute the expected value with the same logic you plan to implement.**

See `references/test-quality.md` for good/bad test patterns.

### MAKE THE TEST RUNNABLE (This Is Not RED Yet)

Before the test can fail meaningfully, it must RUN. Create scaffolding:

```python
# Python: create calculator.py
def add(a, b):
    pass
```

```typescript
// TypeScript: create calculator.ts
export function add(a: number, b: number): number {
  return undefined as any;
}
```

```go
// Go: create calculator.go
func Add(a, b int) int {
    return 0
}
```

These stubs are NOT production code. They are scaffolding so the test runner
can execute your test and reach the assertion.

### RED — Confirm the Test Fails for the Right Reason

Run the test. Classify the result:

**VALID RED** — assertion fails with wrong value:
```
✗ Expected 5 but received 0
✗ Expected "confirmed" but received undefined
✗ Expected function to throw but it did not
```
→ Proceed to GREEN.

**INVALID — infrastructure error** (test never reached the assertion):
```
✗ Cannot find module './calculator'
✗ TypeError: add is not a function
✗ SyntaxError: Unexpected token
```
→ Fix scaffolding (create file, add stub). Re-run. Loop until you get a VALID RED.

**INVALID — test passes immediately:**
→ Test is wrong. It tests existing behavior or has weak assertions. Rewrite.

**The rule: your assertion line must EXECUTE and FAIL.**

### GREEN — Make It Pass with Minimal Code

Write just enough code to make THIS test pass. All previous tests must also pass.

Three strategies (choose based on confidence):

1. **Fake It** (default when unsure) — return a hardcoded value:
   ```
   Test: expect(add(2, 3)).toBe(5)
   Code: return 5;   ← literally this
   ```
   The NEXT test will force generalization.

2. **Triangulation** — when 2+ tests demand different hardcoded values, NOW generalize.
   Not before. This is how TDD drives you from specific to general.

3. **Obvious Implementation** — if the correct general solution is immediately clear
   AND trivially simple, write it. If you hesitate, Fake It instead.

No speculative features (YAGNI). No refactoring yet.

### REFACTOR (Only When Green)

All tests pass. Now improve the code:
- Remove duplication (but duplication is a hint, not a command)
- Improve names, extract helpers, simplify structure
- Run tests after EVERY change — stay GREEN
- **Never add behavior during refactor** (new return value or exception = new behavior = new test first)
- See `references/design-and-refactoring.md`

### UPDATE TEST LIST AND REPEAT

After each cycle:
- Did you discover a new case? Add it to the list.
- Is an item no longer relevant? Remove it.
- Pick the next item and repeat until the list is empty.

## Mocking Rules

Mock ONLY at system boundaries: external APIs, databases (prefer test DB), time, randomness.
Never mock your own classes or internal collaborators.
See `references/mocking-guidelines.md`.

## Per-Cycle Checklist (all must be true before reporting to user)

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Assertion executed and failed with WRONG VALUE (not import/type error)
[ ] Wrote minimal code to make test pass (Fake It / Triangulation / Obvious)
[ ] ALL tests pass (including pre-existing)
[ ] No speculative features added
[ ] Reported result AFTER GREEN, not after RED
```

## Completion Checklist

```
[ ] Every behavior has a test that was seen failing (assertion failure) first
[ ] Edge cases and error paths covered
[ ] All tests pass with clean output
[ ] Tests run independently (no order dependency)
[ ] Test names read as behavior specifications
```

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the API you wish existed. Assert first. Ask user. |
| Test too complicated | Design too coupled. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test passes immediately | Strengthen assertions. Verify it tests NEW behavior. |
| Import error on first run | Create stub file/function first, then re-run. |
| Tempted to skip TDD | See `references/discipline.md` |

## Resources

- `references/test-quality.md` — Good vs bad tests, naming, AAA pattern
- `references/test-case-derivation.md` — Systematic test case discovery
- `references/mocking-guidelines.md` — When/how to mock, test doubles
- `references/design-and-refactoring.md` — Interface design, deep modules, refactoring
- `references/discipline.md` — Common rationalizations, red flags
- `references/legacy-mode.md` — Adding tests to existing code
- `scripts/detect_test_env.sh` — Auto-detect test framework and conventions
