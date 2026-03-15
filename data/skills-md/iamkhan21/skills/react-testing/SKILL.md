---
name: react-testing
description: Testing React components, hooks, and interactions with React Testing Library. Use when writing new tests, debugging failing tests, refactoring test code, setting up test infrastructure, mocking APIs in React tests, or when the user mentions Jest/Vitest with React, `render`, `screen`, `userEvent`, `waitFor`, `findBy`, MSW, or testing patterns. Also use when the user asks how to test a specific React component or hook, even if they don't mention "testing library" explicitly.
triggers:
  - file_globs: ["*.test.tsx", "*.test.ts", "*.spec.ts", "*.spec.tsx"]
  - keywords: ["render", "screen", "userEvent", "waitFor", "findBy", "getByRole", "renderHook"]
  - topics: ["Testing Library", "React Testing Library", "component tests", "hook tests", "Jest React", "Vitest React"]
---

# React Testing

## Quick Start

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("submits form with user input", async () => {
  const user = userEvent.setup();
  render(<LoginForm />);

  await user.type(screen.getByLabelText(/email/i), "test@example.com");
  await user.click(screen.getByRole("button", { name: /sign in/i }));

  expect(await screen.findByText(/welcome/i)).toBeInTheDocument();
});
```

## Core Principle

**Test behavior, not implementation.** Tests verify observable behavior through public interfaces (DOM, props, callbacks), not internal state or private helpers. A refactor that preserves behavior should never break tests.

## Framework Note

Examples use Jest syntax. For Vitest projects, the APIs are nearly identical — see [references/vitest-differences.md](references/vitest-differences.md) for the key differences (`vi.fn()` vs `jest.fn()`, module mocking, etc.). `@testing-library/jest-dom` works with both.

## Queries

Prefer queries by user perception: `getByRole` → `getByLabelText` → `getByText` → `getByTestId` (last resort).

See [references/query-cheatsheet.md](references/query-cheatsheet.md).

## User Interactions

Use `userEvent.setup()` for realistic interactions. Prefer over `fireEvent`.

See [references/user-interactions.md](references/user-interactions.md).

## Async Patterns

Use `findBy*` to wait for a single element. Use `waitFor` when you need multiple assertions or conditions. Keep side effects (clicks, typing) outside `waitFor` — only put assertions inside.

See [references/async-patterns.md](references/async-patterns.md).

## Accessibility Matchers

Beyond `toBeInTheDocument()`, use `jest-dom` matchers that verify accessible state: `toBeVisible()`, `toBeEnabled()`, `toHaveAccessibleName()`, `toBeInvalid()`. These catch real usability issues, not just DOM presence.

See [references/accessibility-matchers.md](references/accessibility-matchers.md).

## Test Utilities

Reduce boilerplate with setup functions that return `user` and domain-specific actions. Use `screen` for all DOM queries.

See [references/test-utilities.md](references/test-utilities.md).

## Mocking

Mock only at system boundaries: network, time, randomness, browser APIs. Never mock your own components, hooks, or internal utilities.

See [references/mocking-patterns.md](references/mocking-patterns.md).

## Providers

Use custom render helper for required providers (router, store, theme). Create a fresh QueryClient per test to avoid cache leaks.

See [references/providers.md](references/providers.md).

## Testing Hooks

```typescript
const { result } = renderHook(() => useCounter(0));
act(() => result.current.increment());
expect(result.current.count).toBe(1);
```

See [references/hooks-testing.md](references/hooks-testing.md).

## Suspense & Error Boundaries

Test loading fallbacks by rendering inside `<Suspense>` and asserting the fallback appears, then awaiting the resolved content. Test error boundaries by rendering a component that throws and verifying the fallback UI.

See [references/suspense-error-boundaries.md](references/suspense-error-boundaries.md).

## Anti-Patterns & Code Smells

Common mistakes: testing implementation details, nested describe/beforeEach with shared mutable state, wrong query types. Test struggles are design feedback — if tests are hard to write, the component may need refactoring.

See [references/anti-patterns.md](references/anti-patterns.md).

## Troubleshooting

Covers `act()` warnings, tests that pass alone but fail together, JSDOM limitations, query errors, and async pitfalls.

See [references/troubleshooting.md](references/troubleshooting.md).

## React 18+ Notes

- `@testing-library/react` v14+ handles React 18's `createRoot` automatically — no manual migration needed
- `act()` warnings are more strict in React 18; most are resolved by properly awaiting async operations with `findBy*` or `waitFor`
- `React.startTransition` updates are batched — use `waitFor` to assert on their results
- Concurrent features (useTransition, useDeferredValue) work in tests but don't exhibit concurrent scheduling in JSDOM — test the user-visible behavior, not the scheduling

## Test Design

- One behavior per test
- Test name describes behavior, not implementation
- Prefer integration-style tests over shallow unit tests
- ~70% coverage sufficient

See [references/design-patterns.md](references/design-patterns.md) and [references/workflow.md](references/workflow.md).
