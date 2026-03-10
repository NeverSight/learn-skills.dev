---
name: behavioral-testing
description: >
  Behavioral testing methodology — test what users experience, not how code is structured.
  Use when writing tests, reviewing test quality, planning test strategy for new features,
  or when existing tests are brittle/verbose/coupled to implementation details.
  Triggers: writing tests, TDD, test review, "tests keep breaking", "too many mocks",
  "tests are verbose", test coverage planning, behavior-driven development.
---

# Behavioral Testing

Test observable behavior. Keep tests terse. Never test implementation details.

## Core Laws

```
1. Test what the user sees, not how the code works
2. If a refactor breaks a test, the test was wrong
3. Mocks isolate — they are never the thing being tested
4. Every assertion must trace to a user-observable outcome
5. Terse tests > thorough ceremony
```

## Writing Tests

### The Pattern

```
Arrange: Set up the minimum preconditions
Act:     Do the thing the user would do
Assert:  Check what the user would see
```

That's it. No red-green-red ritual. No verbose setup. If test setup is longer than the assertion, something is wrong.

### What to Test

Test **behavior at boundaries**, not every line of code:

| Always test | Skip |
|-------------|------|
| What happens with empty/null/whitespace input | Internal method call order |
| Error messages users see | Which helper function was called |
| State transitions (loading → success → error) | Implementation details of state management |
| API failure recovery | Mock call counts (unless it IS the behavior) |
| Edge cases users will hit | Happy-path-only coverage |

### Test Naming

Name tests after the behavior, not the function:

```
✅ "shows error when email is empty"
✅ "redirects to login after session expires"
✅ "prevents duplicate submission on double-click"

❌ "test validateEmail"
❌ "test handleSubmit calls api"
❌ "test useAuth hook returns null"
```

### Keep Tests Terse

```typescript
// ✅ Terse — tests one behavior, reads in 3 seconds
test('shows error when email is empty', () => {
  render(<LoginForm />);
  click(submitButton());
  expect(screen.getByText('Email is required')).toBeVisible();
});

// ❌ Verbose — ceremony obscures intent
test('should display an error message when the user submits the form without entering an email address', () => {
  const mockOnSubmit = vi.fn();
  const mockOnError = vi.fn();
  const { container } = render(
    <LoginForm onSubmit={mockOnSubmit} onError={mockOnError} />
  );
  const form = container.querySelector('form');
  const button = screen.getByRole('button', { name: /submit/i });
  await userEvent.click(button);
  expect(mockOnSubmit).not.toHaveBeenCalled();
  expect(mockOnError).toHaveBeenCalledWith(expect.objectContaining({ field: 'email' }));
  expect(screen.getByText('Email is required')).toBeVisible();
});
```

The terse test catches the same bug. The verbose test also asserts on mock internals — those assertions break when you refactor, even if behavior is unchanged.

## Stop Checks

Before writing or reviewing any test, run these checks:

```
□ Am I asserting on a mock instead of real output?
  → If yes: delete the assertion or unmock it

□ Would a refactor break this test even though behavior hasn't changed?
  → If yes: the test is coupled to implementation — rewrite it

□ Is mock setup > 50% of the test?
  → If yes: use an integration test with real components instead

□ Does this test name describe a user-visible behavior?
  → If no: rename it or question whether it needs to exist

□ Did I write this test after the implementation?
  → If yes: verify it actually fails when behavior is broken, not just when code changes
```

## When to Mock

**Mock external boundaries only.** Network calls, third-party services, timers — things outside your control.

**Never mock** internal modules, components you own, or "just to be safe."

If you need to mock a thing to test it, the design has a coupling problem — fix the design, not the test.

## Detailed References

Load these only when needed:

- **[references/anti-patterns.md](references/anti-patterns.md)** — Common testing mistakes with examples: testing mock behavior, test-only production methods, incomplete mocks, over-mocking
- **[references/test-templates.md](references/test-templates.md)** — Copy-paste test patterns for unit, integration, and E2E tests. Factories, helpers, and terse assertion patterns
- **[references/branch-coverage.md](references/branch-coverage.md)** — Branch matrix methodology for systematic coverage: how to map conditions, prioritize, and verify completeness without testing every permutation
