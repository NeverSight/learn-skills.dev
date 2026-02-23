---
name: frontend-testing
description: WHEN testing any front-end UI with DOM Testing Library; behavior-first queries, userEvent flows, async patterns.
---

# Front-End Testing with DOM Testing Library

Framework-agnostic DOM Testing Library patterns for behavior-driven testing. For React-specific patterns (renderHook, context, components), load the `react-testing` skill. For TDD workflow (RED-GREEN-REFACTOR), load the `tdd` skill.

## Core Philosophy

**Test behavior users see, not implementation details.**

Testing Library exists to solve a fundamental problem: tests that break when you refactor (false negatives) and tests that pass when bugs exist (false positives).

### Two Types of Users

Your UI components have two users:

1. **End-users**: Interact through the DOM (clicks, typing, reading text)
2. **Developers**: You, refactoring implementation

**Kent C. Dodds principle**: "The more your tests resemble the way your software is used, the more confidence they can give you."

### Why This Matters

**False negatives** (tests break on refactor):

```typescript
// ❌ WRONG - Testing implementation (will break on refactor)
it("should update internal state", () => {
  const component = new CounterComponent();
  component.setState({ count: 5 }); // Coupled to state implementation
  expect(component.state.count).toBe(5);
});
```

**Correct approach** (behavior-driven):

```typescript
// ✅ CORRECT - Testing user-visible behavior
it("should submit form when user clicks submit", async () => {
  const handleSubmit = vi.fn();
  const user = userEvent.setup();

  render(`
    <form id="login-form">
      <label>Email: <input name="email" /></label>
      <button type="submit">Submit</button>
    </form>
  `);

  await user.type(screen.getByLabelText(/email/i), "test@example.com");
  await user.click(screen.getByRole("button", { name: /submit/i }));

  expect(handleSubmit).toHaveBeenCalled();
});
```

## Quick Reference

| Topic                                  | Guide                                                                       |
| -------------------------------------- | --------------------------------------------------------------------------- |
| Query selection priority and details   | [queries.md](queries.md)                                                    |
| userEvent patterns and interactions    | [user-events.md](user-events.md)                                            |
| Async testing (findBy, waitFor)        | [async-testing.md](async-testing.md)                                        |
| MSW for API mocking                    | [msw.md](msw.md)                                                            |
| Common mistakes and fixes              | [anti-patterns.md](anti-patterns.md)                                        |
| Accessibility-first testing principles | [accessibility-first-testing.md](references/accessibility-first-testing.md) |

## When to Use Each Guide

### Queries

Use [queries.md](queries.md) when you need:

- Query priority order (getByRole → getByLabelText → ...)
- Query variant decisions (getBy vs queryBy vs findBy)
- Common query mistakes and fixes

### User Events

Use [user-events.md](user-events.md) when you need:

- userEvent vs fireEvent guidance
- userEvent.setup() pattern
- Common interaction patterns (clicking, typing, keyboard)

### Async Testing

Use [async-testing.md](async-testing.md) when you need:

- findBy queries for async elements
- waitFor for complex conditions
- waitForElementToBeRemoved
- Loading states, API responses, debounced inputs

### MSW

Use [msw.md](msw.md) when you need:

- Network-level API mocking
- setupServer pattern
- Per-test handler overrides

### Anti-Patterns

Use [anti-patterns.md](anti-patterns.md) when you need:

- List of all common mistakes
- Quick reference of what NOT to do
- ESLint plugin setup

### Accessibility-First Testing

Use [accessibility-first-testing.md](references/accessibility-first-testing.md) when you need:

- Why accessible queries improve tests and accessibility
- When to add ARIA attributes vs semantic HTML
- Semantic HTML priority principles

## Summary Checklist

Before merging UI tests, verify:

- [ ] Using `getByRole` as first choice for queries
- [ ] Using `userEvent` with `setup()` (not `fireEvent`)
- [ ] Using `screen` object for all queries (not destructuring from render)
- [ ] Using `findBy*` for async elements (loading, API responses)
- [ ] Using `jest-dom` matchers (`toBeInTheDocument`, `toBeDisabled`, etc.)
- [ ] Testing behavior users see, not implementation details
- [ ] ESLint plugins installed (`eslint-plugin-testing-library`, `eslint-plugin-jest-dom`)
- [ ] No manual `cleanup()` calls (automatic)
- [ ] MSW for API mocking (not fetch/axios mocks)
- [ ] Following TDD workflow (see `tdd` skill)
- [ ] Using test factories for data (see `testing` skill)
- [ ] For framework-specific patterns (React hooks, context, components), see `react-testing` skill
