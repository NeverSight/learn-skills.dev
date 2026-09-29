---
name: web-testing
description: Frontend testing with Vitest and Testing Library. Use for unit, component, integration, visual regression, and accessibility tests in web apps. Covers React, Vue, and framework-agnostic patterns including WebGL/Canvas, BVA, mocking with MSW, coverage, and Testcontainers. For Vitest — NOT Playwright or E2E browser automation.
---

## Philosophy

1. **Test behavior, not implementation.** Assert on what the user sees and does — never on internal state or hook return values.
2. **Test at boundaries, not exhaustively.** Apply BVA and Equivalence Partitioning to maximize defect coverage with minimum tests.
3. **Prefer integration tests when the cost is similar.** Follow the Testing Trophy: static analysis, unit, integration, thin E2E.

## Decision Tree

```
What am I testing?
├── Pure function / utility / algorithm  →  Unit test + BVA
├── Custom hook                          →  Hook test with renderHook
├── Single component                     →  Component test (custom render below)
├── Multi-component flow / data fetch    →  Integration test (MSW for APIs)
│     └── Need real backend?             →  Testcontainers (see below)
├── Canvas / WebGL / 3D viewer           →  Contract test + visual regression
│                                            (references/visual-and-canvas.md)
└── Accessibility compliance             →  axe-core test
```

## Quick Start

Install:

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom \
  @testing-library/user-event @vitest/coverage-v8 jsdom
```

### vitest.config.ts

```ts
/// <reference types="vitest" />
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    css: true,
    include: ['src/**/*.{test,spec}.{ts,tsx,js,jsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      include: ['src/**/*.{ts,tsx,js,jsx}'],
      exclude: ['src/**/*.test.*', 'src/**/*.spec.*', 'src/test/**',
        'src/**/*.d.ts', 'src/**/index.ts', 'src/**/*.stories.*'],
      thresholds: { branches: 80, functions: 80, lines: 80, statements: 80 },
    },
  },
});
```

### setup.ts

```ts
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';
import '@testing-library/jest-dom/vitest';

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

// Browser API mocks (not in jsdom)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false, media: query, onchange: null,
    addListener: vi.fn(), removeListener: vi.fn(),
    addEventListener: vi.fn(), removeEventListener: vi.fn(), dispatchEvent: vi.fn(),
  })),
});

class MockIntersectionObserver { observe = vi.fn(); unobserve = vi.fn(); disconnect = vi.fn(); }
Object.defineProperty(window, 'IntersectionObserver', { writable: true, value: MockIntersectionObserver });

class MockResizeObserver { observe = vi.fn(); unobserve = vi.fn(); disconnect = vi.fn(); }
Object.defineProperty(window, 'ResizeObserver', { writable: true, value: MockResizeObserver });

// Optional: import 'vitest-canvas-mock';  — for canvas components
// Optional: MSW server.listen() / resetHandlers() / close() — for API mocking
```

### test-utils.tsx

```tsx
import { type ReactElement, type ReactNode } from 'react';
import { render, type RenderOptions } from '@testing-library/react';

// Add your app providers here (QueryClient, ThemeProvider, Router, Intl, etc.)
function AllProviders({ children }: { children: ReactNode }) {
  return <>{children}</>;
}

function customRender(ui: ReactElement, options?: Omit<RenderOptions, 'wrapper'>) {
  return render(ui, { wrapper: AllProviders, ...options });
}

export * from '@testing-library/react';
export { customRender as render };
```

Run tests:

```bash
npx vitest              # watch mode
npx vitest run          # single run
npx vitest --coverage   # with coverage report
```

## Testing Library Query Priority

| Priority | Query | When |
|----------|-------|------|
| 1 | `getByRole` | Buttons, links, headings, textboxes, checkboxes |
| 2 | `getByLabelText` | Form fields with visible labels |
| 3 | `getByPlaceholderText` | When no label exists (fallback) |
| 4 | `getByText` | Non-interactive text content |
| 5 | `getByDisplayValue` | Inputs showing a current value |
| 6 | `getByAltText` | Images |
| 7 | `getByTitle` | SVGs, tooltips |
| 8 | `getByTestId` | Escape hatch only |

**Variants:** `getBy*` (throws if missing), `queryBy*` (returns null), `findBy*` (async, retries).

## Core Patterns

### Async Code

```tsx
const message = await screen.findByText('Success');          // retries automatically
await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('Saved'));
vi.useFakeTimers();
await act(() => vi.advanceTimersByTimeAsync(1000));
vi.useRealTimers();
```

### User Interactions

Always use `@testing-library/user-event` over `fireEvent`:

```tsx
const user = userEvent.setup();
await user.click(button);
await user.type(input, 'hello');
await user.clear(input);
await user.selectOptions(select, 'option-value');
await user.tab();
await user.keyboard('{Enter}');
```

## Example: Component Test

```tsx
import { render, screen } from '../test-utils';
import userEvent from '@testing-library/user-event';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  const props = { name: 'Alice', role: 'Engineer', onFollow: vi.fn() };

  it('displays name and role', () => {
    render(<UserCard {...props} />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Engineer')).toBeInTheDocument();
  });

  it('calls onFollow when button clicked', async () => {
    const user = userEvent.setup();
    render(<UserCard {...props} />);
    await user.click(screen.getByRole('button', { name: /follow/i }));
    expect(props.onFollow).toHaveBeenCalledTimes(1);
  });

  it('shows skeleton in loading state', () => {
    render(<UserCard {...props} isLoading />);
    expect(screen.queryByText('Alice')).not.toBeInTheDocument();
    expect(screen.getByTestId('user-card-skeleton')).toBeInTheDocument();
  });
});
```

## Example: Hook Test

```tsx
import { renderHook, act } from '@testing-library/react';
import { useDebounce } from './useDebounce';

describe('useDebounce', () => {
  beforeEach(() => { vi.useFakeTimers(); });
  afterEach(() => { vi.useRealTimers(); });

  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('hello', 300));
    expect(result.current).toBe('hello');
  });

  it('updates value after delay', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'hello', delay: 300 } }
    );
    rerender({ value: 'world', delay: 300 });
    act(() => vi.advanceTimersByTime(300));
    expect(result.current).toBe('world');
  });

  it('resets timer on rapid updates', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'a', delay: 300 } }
    );
    rerender({ value: 'ab', delay: 300 });
    act(() => vi.advanceTimersByTime(100));
    rerender({ value: 'abc', delay: 300 });
    act(() => vi.advanceTimersByTime(300));
    expect(result.current).toBe('abc');
  });
});
```

## Example: Integration Test (MSW)

```tsx
import { render, screen } from '../test-utils';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { LoginPage } from './LoginPage';

const server = setupServer(
  http.post('/api/login', async ({ request }) => {
    const body = (await request.json()) as { email: string; password: string };
    if (body.email === 'user@test.com' && body.password === 'correct')
      return HttpResponse.json({ token: 'fake-jwt' });
    return HttpResponse.json({ error: 'Invalid credentials' }, { status: 401 });
  })
);
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Login Flow', () => {
  it('redirects after successful login', async () => {
    const user = userEvent.setup();
    render(<MemoryRouter initialEntries={['/login']}>
      <Routes><Route path="/login" element={<LoginPage />} /></Routes>
    </MemoryRouter>);
    await user.type(screen.getByRole('textbox', { name: /email/i }), 'user@test.com');
    await user.type(screen.getByLabelText(/password/i), 'correct');
    await user.click(screen.getByRole('button', { name: /sign in/i }));
    expect(await screen.findByText(/dashboard/i)).toBeInTheDocument();
  });

  it('shows error for invalid credentials', async () => {
    const user = userEvent.setup();
    render(<MemoryRouter initialEntries={['/login']}>
      <Routes><Route path="/login" element={<LoginPage />} /></Routes>
    </MemoryRouter>);
    await user.type(screen.getByRole('textbox', { name: /email/i }), 'user@test.com');
    await user.type(screen.getByLabelText(/password/i), 'wrong');
    await user.click(screen.getByRole('button', { name: /sign in/i }));
    expect(await screen.findByText('Invalid credentials')).toBeInTheDocument();
  });
});
```

## Boundary Testing

Bugs cluster at the edges. Apply BVA and Equivalence Partitioning to every function with ranges/limits.

| Domain | Test these values |
|--------|------------------|
| Non-negative int | -1, 0, 1 |
| Array index (0..len-1) | -1, 0, 1, len-2, len-1, len |
| Percentage (0-100) | -1, 0, 1, 99, 100, 101 |
| Required string | `""`, `" "`, `"a"` |
| Max length N string | N-1, N, N+1 |
| Array/collection | `[]`, `[x]`, `[x,y]`, at max |
| Special JS values | NaN, Infinity, -0, MAX_SAFE_INTEGER |

### Edge Case Checklist

- **Null/Undefined/Missing:** null input, undefined optional params, missing properties
- **Type coercion:** `"0"` truthy vs `0` falsy, `NaN !== NaN`
- **Concurrent/Async:** rapid clicks, stale closures, race conditions, unmount during async
- **Network:** timeout, 500, 404, 401, malformed JSON, offline
- **Empty states:** no data, no permissions, no results
- **Overflow:** very long strings, large numbers, thousands of items

## Mocking Patterns

### Decision Framework

| Boundary | How |
|----------|-----|
| External APIs | MSW (preferred) or `vi.stubGlobal('fetch', ...)` |
| Browser APIs | Manual mocks in setup.ts (matchMedia, IntersectionObserver) |
| Timers | `vi.useFakeTimers()` / `vi.setSystemTime(new Date(...))` |
| Randomness | `vi.spyOn(Math, 'random').mockReturnValue(0.5)` |
| Third-party SDKs | `vi.mock('module')` at module level |

**Do NOT mock:** your own modules, the library under test, simple utilities.

### Key Primitives

```tsx
// vi.fn() — mock function
const handler = vi.fn();
expect(handler).toHaveBeenCalledWith('arg');

// vi.spyOn() — spy on existing method
vi.spyOn(console, 'error').mockImplementation(() => {});

// vi.mock() — mock entire module
vi.mock('./analytics', () => ({ trackEvent: vi.fn() }));

// vi.hoisted() — hoist variables above vi.mock
const { mockNav } = vi.hoisted(() => ({ mockNav: vi.fn() }));
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal<typeof import('react-router-dom')>();
  return { ...actual, useNavigate: () => mockNav };
});

// Partial mock — keep some exports real
vi.mock('./utils', async (importOriginal) => {
  const actual = await importOriginal<typeof import('./utils')>();
  return { ...actual, sendEmail: vi.fn() };
});
```

## Coverage

| Code category | Branch target | Rationale |
|--------------|--------------|-----------|
| Overall project | 80% | Catches most logic gaps |
| Critical paths (auth, payments) | 95%+ | Outsized bug impact |
| UI-only (no logic) | 70% | Visual tests complement |
| Generated code, types | Exclude | No logic to test |

Intentional exclusions: `/* v8 ignore next */` or `/* v8 ignore start/stop */` — always add a comment explaining why.

CI integration:

```bash
npx vitest run --coverage
```

```yaml
- name: Run tests with coverage
  run: npx vitest run --coverage
- name: Upload coverage
  uses: codecov/codecov-action@v4
  with: { files: coverage/lcov.info, fail_ci_if_error: true }
```

## Accessibility Testing

```bash
npm install -D vitest-axe
```

```tsx
import { axe } from 'vitest-axe';

it('has no accessibility violations', async () => {
  const { container } = render(<LoginForm onSubmit={vi.fn()} />);
  expect(await axe(container)).toHaveNoViolations();
});

// Target specific criteria
const results = await axe(container, { runOnly: ['wcag2a', 'wcag2aa'] });
```

Key checks: form labels via `getByRole`, image alt text, focus management after modal open/close, keyboard navigation (Tab/Enter/Escape), live regions (`role="alert"`).

## Testcontainers

Default to MSW. Use Testcontainers only when backend behavior is too complex to mock (real cursors, DB filtering, auth token refresh).

```tsx
import { GenericContainer, Wait } from 'testcontainers';

let container: StartedTestContainer;
beforeAll(async () => {
  container = await new GenericContainer('your-api:latest')
    .withExposedPorts(3000)
    .withWaitStrategy(Wait.forHttp('/health', 3000))
    .start();
  process.env.VITE_API_URL = `http://${container.getHost()}:${container.getMappedPort(3000)}`;
}, 60_000);
afterAll(async () => { await container.stop(); });
```

Performance: use `globalSetup` to share containers, `.withReuse()` locally, pre-pull images in CI, `--pool=forks`.

## Testing Forms

```tsx
it('validates and submits', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();
  render(<ContactForm onSubmit={onSubmit} />);

  await user.type(screen.getByRole('textbox', { name: /email/i }), 'bad');
  await user.click(screen.getByRole('button', { name: /submit/i }));
  expect(screen.getByRole('alert')).toHaveTextContent('Invalid email');
  expect(onSubmit).not.toHaveBeenCalled();

  await user.clear(screen.getByRole('textbox', { name: /email/i }));
  await user.type(screen.getByRole('textbox', { name: /email/i }), 'user@example.com');
  await user.click(screen.getByRole('button', { name: /submit/i }));
  expect(onSubmit).toHaveBeenCalledWith({ email: 'user@example.com' });
});
```

## Best Practices

**DO:** Test what the user sees; use `screen` for queries; name tests as user stories; use `toBeInTheDocument()` over snapshots; apply BVA; include an `axe` check per component.

**DO NOT:** Test implementation details; snapshot entire components; use `container.querySelector`; mock what you don't own (mock the boundary); use `act()` manually unless necessary; use real timers in tests.

## Snapshot Tests

Use only for stable serializable output (config objects, small SVG icons). Prefer inline snapshots. Never use `toMatchSnapshot()` for UI components.

## Reference Files

| File | Description |
|------|-------------|
| `references/visual-and-canvas.md` | WebGL/Canvas mocking, NGL Viewer testing, pixel matching, headless GL, CI strategies |
