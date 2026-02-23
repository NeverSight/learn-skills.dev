---
name: vitest-testing
description: |
  Vitest testing framework for unit, component, and integration tests. Covers test structure (describe/it/test.each), assertions with expect, lifecycle hooks, mocking (vi.fn/vi.mock/vi.spyOn), React Testing Library patterns, hook testing with renderHook, user-event interactions, async utilities, configuration, workspace setup, coverage, and advanced patterns like in-source testing and concurrent execution. Also covers CLI commands, test filtering, tags, sharding, fixtures with test.extend, and fixture scoping.

  Use when writing unit tests, component tests, integration tests, or testing React hooks. Use for test configuration, mocking modules, testing async behavior, snapshot testing, or setting up test coverage.
license: MIT
metadata:
  author: oakoss
  version: '1.2'
  source: 'https://vitest.dev/'
---

# Vitest Testing

## Overview

Vitest is a Vite-native unit testing framework that shares the same configuration and plugin ecosystem. Built for speed with native ESM support, hot module replacement for tests, and parallel execution.

**When to use:** Unit tests, component tests, integration tests, hook tests, in-source tests. Testing React components with React Testing Library. Testing TanStack Query/Router/Form patterns.

**When NOT to use:** End-to-end testing (use Playwright), visual regression testing (use Percy/Chromatic), load testing (use k6).

## Quick Reference

| Pattern             | API                                             | Key Points                          |
| ------------------- | ----------------------------------------------- | ----------------------------------- |
| Test structure      | `describe('suite', () => {})`                   | Organize related tests              |
| Single test         | `test('behavior', () => {})` or `it()`          | Both are aliases                    |
| Parameterized tests | `test.each([...])('name', (arg) => {})`         | Run same test with different inputs |
| Concurrent tests    | `test.concurrent('name', async () => {})`       | Run tests in parallel               |
| Skip test           | `test.skip('name', () => {})` or `skipIf(cond)` | Conditionally skip tests            |
| Only test           | `test.only('name', () => {})`                   | Run specific test for debugging     |
| Assertions          | `expect(value).toBe(expected)`                  | Compare primitive values            |
| Deep equality       | `expect(obj).toEqual(expected)`                 | Compare objects/arrays              |
| Async assertions    | `await expect(promise).resolves.toBe(value)`    | Test promise resolution             |
| Before each test    | `beforeEach(() => {})`                          | Setup before each test              |
| After each test     | `afterEach(() => {})`                           | Cleanup after each test             |
| Mock function       | `vi.fn()`                                       | Create spy function                 |
| Mock module         | `vi.mock('./module')`                           | Replace entire module               |
| Spy on method       | `vi.spyOn(obj, 'method')`                       | Track calls to existing method      |
| Clear mocks         | `vi.clearAllMocks()`                            | Clear call history                  |
| Fake timers         | `vi.useFakeTimers()`                            | Control setTimeout/setInterval      |
| Render component    | `render(<Component />)`                         | Mount React component for testing   |
| Query by role       | `screen.getByRole('button')`                    | Find elements by accessibility role |
| User interaction    | `await user.click(element)`                     | Simulate user events                |
| Wait for change     | `await waitFor(() => expect(...))`              | Wait for async changes              |
| Find async element  | `await screen.findByText('text')`               | Query + wait combined               |
| Render hook         | `renderHook(() => useHook())`                   | Test custom hooks                   |
| Update hook props   | `rerender(newProps)`                            | Re-render hook with new props       |
| Snapshot            | `expect(value).toMatchSnapshot()`               | Compare against saved snapshot      |
| Inline snapshot     | `expect(value).toMatchInlineSnapshot()`         | Snapshot stored in test file        |
| CLI run once        | `vitest run`                                    | Single run, no watch                |
| Run changed tests   | `vitest --changed`                              | Tests affected by git changes       |
| Filter by name      | `vitest -t "pattern"`                           | Grep test names                     |
| Soft assertions     | `expect.soft(value).toBe(x)`                    | Continue on failure, collect all    |
| Poll assertions     | `await expect.poll(() => val).toBe(x)`          | Retry until passing                 |
| Test fixtures       | `const test = base.extend<F>({...})`            | Reusable setup via test.extend      |
| Hoisted mocks       | `vi.hoisted(() => ({ fn: vi.fn() }))`           | Variables for vi.mock factory       |
| Shard tests         | `vitest --shard 1/3`                            | Split across CI workers             |
| Tags                | `test('name', { tags: ['slow'] }, ...)`         | Filter with --tags                  |
| Stub globals        | `vi.stubGlobal('fetch', vi.fn())`               | Replace global objects cleanly      |

## Common Mistakes

| Mistake                                | Correct Pattern                                     |
| -------------------------------------- | --------------------------------------------------- |
| Using `getBy` for async content        | Use `findBy` or `waitFor` for async                 |
| Testing implementation details         | Test behavior and public API                        |
| Using `getByTestId` as first choice    | Prefer `getByRole`, `getByLabelText`, `getByText`   |
| Missing `userEvent.setup()`            | Always call `const user = userEvent.setup()` first  |
| Shared state between tests             | Use `beforeEach` to reset or create fresh instances |
| Not cleaning up mocks                  | Use `vi.clearAllMocks()` in `afterEach`             |
| Mocking too much                       | Only mock external dependencies and APIs            |
| Not disabling retries in tests         | Set `retry: false` for TanStack Query tests         |
| Immediate assertions on async          | Use `await waitFor()` or `findBy` queries           |
| Creating QueryClient in render         | Create once in wrapper or use `useState`            |
| Testing library code                   | Trust the library, test your usage                  |
| Not awaiting user events               | All `user.*` methods return promises                |
| Using `act` manually                   | `userEvent` and Testing Library handle this         |
| Inline select without memoization      | Extract to stable function for TanStack Query       |
| Variables in vi.mock factory           | Use `vi.hoisted()` to declare mock variables        |
| Single `expect` for multiple checks    | Use `expect.soft()` to collect all failures         |
| `setTimeout` in tests for async waits  | Use `expect.poll()` or `vi.waitFor()`               |
| Manual `beforeEach` for reusable setup | Use `test.extend` fixtures for composable setup     |

## Delegation

- **Test discovery**: For finding untested code paths, use `Explore` agent
- **Coverage analysis**: For comprehensive coverage review, use `Task` agent
- **E2E testing**: If `playwright` skill is available, delegate E2E testing to it
- **Code review**: After writing tests, delegate to `code-reviewer` agent

## References

- [Test fundamentals: structure, assertions, lifecycle hooks](references/test-fundamentals.md)
- [Mocking: vi.fn, vi.mock, vi.spyOn, module mocking](references/mocking.md)
- [Component testing: React Testing Library, queries, user-event](references/component-testing.md)
- [Hook testing: renderHook, async hooks, TanStack patterns](references/hook-testing.md)
- [Test setup: jest-dom matchers, cleanup, custom render, MSW, polyfills](references/test-setup.md)
- [Configuration: vitest.config.ts, workspace, coverage, reporters](references/configuration.md)
- [Advanced patterns: snapshots, concurrent tests, in-source, type testing](references/advanced-patterns.md)
- [CLI and filtering: commands, watch mode, tags, sharding](references/cli-and-filtering.md)
- [Fixtures and context: test.extend, scoping, auto fixtures, injection](references/fixtures-and-context.md)
