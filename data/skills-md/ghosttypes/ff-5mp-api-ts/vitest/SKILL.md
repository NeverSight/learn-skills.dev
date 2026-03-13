---
name: vitest
description: "Comprehensive Vitest testing framework skill for writing, configuring, and running tests in JavaScript/TypeScript projects. Use when Claude needs to: set up Vitest in a new or existing project (Vite or non-Vite), write or modify tests using Vitest APIs, configure Vitest for specific scenarios (coverage, browser testing, mocking, etc.), migrate from Jest or older Vitest versions, debug test failures or configuration issues, implement advanced testing patterns (workspace, browser mode, snapshots, mocking)."
---

# Vitest

## Overview

Vitest is a blazing-fast unit test framework powered by Vite. This skill provides complete Vitest documentation, APIs, configuration options, and migration guides to enable flawless test development in any JavaScript or TypeScript project.

**Key capabilities:**
- Vite-native for instant feedback and HMR
- Jest-compatible API for easy migration
- Works in Vite and non-Vite projects
- Built-in TypeScript, JSX, and ESM support
- Native code coverage (V8 and Istanbul)
- Browser mode for component testing
- Workspace support for monorepos

## Quick Start Decision Tree

**Is this a new project or adding tests to an existing project?**

- **New project**: Start with "Installation & Setup"
- **Existing project**: Check framework type below

**What type of project is it?**

- **Vite/Vue/React/Svelte**: Use Vite integration (see "Vite Project Setup")
- **Non-Vite (Next.js, Angular, vanilla)**: Use standalone mode (see "Standalone Project Setup")
- **Monorepo**: Use workspace configuration (see "Workspace Setup")

**Are you migrating from Jest?**

- **Yes**: See "Migration from Jest" section

## Installation & Setup

### Basic Installation

```bash
# Install Vitest
npm install -D vitest

# Add test script to package.json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui"
  }
}
```

### Vite Project Setup

For projects already using Vite, extend the existing `vite.config.ts`:

```ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    // test options
  },
  // your existing Vite config
})
```

Vitest automatically shares your Vite config, plugins, and transformations.

### Standalone Project Setup

For non-Vite projects, create `vitest.config.ts`:

```ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    include: ['**/*.{test,spec}.{js,ts}'],
    environment: 'node' // or 'jsdom' for browser environment
  }
})
```

**Framework-specific setup guides:**
- **Next.js**: See `references/guide/index.md` for configuration
- **Angular**: Use `environment: 'jsdom'` with appropriate transformers
- **React/Vue/Svelte**: Extend Vite config for best experience

### TypeScript Setup

Vitest supports TypeScript out of the box. Ensure `tsconfig.json` includes test files:

```json
{
  "include": ["src/**/*", "**/*.test.ts"]
}
```

## Writing Tests

### Basic Test Structure

```ts
// math.test.ts
import { describe, it, expect } from 'vitest'
import { add } from './math'

describe('add', () => {
  it('should add two numbers', () => {
    expect(add(1, 2)).toBe(3)
  })

  it('should handle negative numbers', () => {
    expect(add(-1, -2)).toBe(-3)
  })
})
```

### Test Organization

- **Use `describe` blocks** to group related tests
- **Name test files** with `.test.ts` or `.spec.ts` suffix
- **Co-locate tests** with source code or in `__tests__` directories
- **Use test context** for sharing data between tests (see `references/guide/test-context.md`)

### Lifecycle Hooks

```ts
import { beforeAll, beforeEach, afterAll, afterEach } from 'vitest'

describe('database tests', () => {
  beforeAll(async () => {
    // Runs once before all tests
    await connectDatabase()
  })

  beforeEach(async () => {
    // Runs before each test
    await clearDatabase()
  })

  afterEach(async () => {
    // Runs after each test
    await cleanup()
  })

  afterAll(async () => {
    // Runs once after all tests
    await disconnectDatabase()
  })
})
```

For complete lifecycle reference, see `references/api/hooks.md`.

### Running Tests

```bash
# Run all tests once
vitest run

# Watch mode (default)
vitest

# Run matching pattern
vitest --testNamePattern="should add"

# UI mode
vitest --ui

# Coverage
vitest --coverage
```

See `references/guide/cli.md` for complete CLI reference.

## Mocking

Vitest provides comprehensive mocking capabilities through the `vi` utility.

### Function Mocking

```ts
import { vi, describe, it, expect } from 'vitest'

const mockFn = vi.fn()
mockFn('hello')
expect(mockFn).toHaveBeenCalledWith('hello')

// With return value
const mocked = vi.fn().mockReturnValue('test')
expect(mocked()).toBe('test')

// With implementation
const callback = vi.fn((x) => x + 1)
expect(callback(1)).toBe(2)
```

### Module Mocking

```ts
import { vi, expect, it } from 'vitest'
import { fetchData } from './api'

// Mock entire module
vi.mock('./api', () => ({
  fetchData: vi.fn(() => Promise.resolve('mocked data'))
}))

it('uses mocked API', async () => {
  const data = await fetchData()
  expect(data).toBe('mocked data')
})
```

### Timer Mocking

```ts
import { vi, beforeEach, expect, it } from 'vitest'

beforeEach(() => {
  vi.useFakeTimers()
})

it('calls callback after timeout', () => {
  const callback = vi.fn()
  setTimeout(callback, 1000)

  vi.advanceTimersByTime(1000)
  expect(callback).toHaveBeenCalled()
})
```

**Complete mocking reference:**
- **Functions**: `references/guide/mocking/functions.md`
- **Modules**: `references/guide/mocking/modules.md`
- **Timers**: `references/guide/mocking/timers.md`
- **Globals**: `references/guide/mocking/globals.md`
- **Dates**: `references/guide/mocking/dates.md`

## Configuration Patterns

### Common Configuration Scenarios

**1. Browser Environment (React/Vue/Svelte)**

```ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts']
  }
})
```

**2. Code Coverage**

```ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8', // or 'istanbul'
      include: ['src/**/*.{js,ts}'],
      exclude: ['src/**/*.test.{js,ts}', 'src/**/*.config.{js,ts}']
    }
  }
})
```

**3. Monorepo/Workspace**

```ts
export default defineConfig({
  test: {
    workspace: [
      'packages/*',
      'apps/*'
    ]
  }
})
```

**4. Browser Mode (Component Testing)**

```ts
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: 'playwright', // or 'webdriverio'
      headless: true
    }
  }
})
```

See `references/config/INDEX.md` for complete configuration reference.

## Advanced Features

### Snapshot Testing

```ts
import { expect, it } from 'vitest'

it('matches snapshot', () => {
  const data = { foo: 'bar' }
  expect(data).toMatchSnapshot()
})
```

See `references/guide/snapshot.md` for complete snapshot guide.

### In-Source Testing

Write tests directly next to code:

```ts
// src/math.ts
export function add(a: number, b: number) {
  return a + b
}

// @ts-ignore
if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest
  it('adds numbers', () => {
    expect(add(1, 2)).toBe(3)
  })
}
```

See `references/guide/in-source.md` for configuration.

### Test Tags

Organize and filter tests by tags:

```ts
import { test } from 'vitest'

test('slow integration test', { tags: ['@slow', '@integration'] }, () => {
  // test code
})

// Run only fast tests
// vitest --tags @fast
```

See `references/guide/test-tags.md` for usage.

### Browser Testing

Test components in real browser:

```ts
import { expect, test } from 'vitest'
import { render } from '@testing-library/vue'

test('renders button', async () => {
  const { getByText } = render(Button, {
    props: { label: 'Click me' }
  })

  expect(getByText('Click me')).toBeTruthy()
})
```

See `references/guide/browser/` for complete browser testing guide.

## Migration

### From Jest to Vitest

Vitest is largely compatible with Jest. The migration process:

1. **Install Vitest**: `npm install -D vitest`
2. **Update configuration**: Replace `jest.config.js` with `vitest.config.ts`
3. **Update scripts**: Change `test` script to use `vitest`
4. **Update imports**: Replace `@jest/globals` with `vitest`
5. **Verify mocks**: Most Jest mocks work unchanged

**Key differences:**
- **Auto-mocked modules**: Vitest doesn't auto-mock by default
- **Timer mocks**: Use `vi.useFakeTimers()` instead of `jest.useFakeTimers()`
- **Environment variables**: Use `process.env` directly

See `references/guide/comparisons.md` for detailed Jest comparison.

### From Older Vitest Versions

**Migrating to Vitest 4.0:**
- Coverage provider changes: V8 now uses AST-based remapping
- Removed `coverage.all` and `coverage.extensions` - use `coverage.include` instead
- Coverage ignore hints updated - see `references/guide/migration.md`

See migration guides:
- **Vitest 4.0**: `references/guide/migration.md#vitest-4`
- **Vitest 3.0**: `references/vitest-3.md`
- **Vitest 3.2**: `references/vitest-3-2.md`

## Troubleshooting

### Common Issues

**Tests run in wrong environment:**
```ts
// vitest.config.ts
export default defineConfig({
  test: {
    environment: 'jsdom' // for browser tests
    // or 'node' for server tests
  }
})
```

**Modules not transforming:**
- Check `transformMode` configuration
- Ensure dependencies are in `deps.interopDefault`

**Timeouts:**
- Increase timeout: `test({ timeout: 10000 }, () => { ... })`
- Or globally: `test: { timeout: 10000 }`

**Watch mode not detecting changes:**
- Check file inclusion patterns
- Verify `include` and `exclude` in config

See `references/guide/common-errors.md` for more troubleshooting.

## Resources

This skill includes comprehensive Vitest documentation organized for progressive disclosure:

### Documentation Indices

- **[Main INDEX](references/INDEX.md)** - Complete documentation navigation
- **[Guide INDEX](references/guide/INDEX.md)** - Usage guides by topic
- **[API INDEX](references/api/INDEX.md)** - Complete API reference
- **[Config INDEX](references/config/INDEX.md)** - All configuration options

### Key Documentation

**Getting Started:**
- **[Getting Started Guide](references/guide/index.md)** - Installation and first test
- **[Features](references/guide/features.md)** - Vitest capabilities overview
- **[CLI Reference](references/guide/cli.md)** - Command-line options

**Core Concepts:**
- **[Lifecycle](references/guide/lifecycle.md)** - Test hooks and setup/teardown
- **[Test Context](references/guide/test-context.md)** - Sharing data between tests
- **[Filtering](references/guide/filtering.md)** - Running specific tests

**Mocking:**
- **[Mocking Overview](references/guide/mocking.md)** - Mocking guide
- **[vi API](references/api/vi.md)** - Mocking utilities
- **[mock API](references/api/mock.md)** - Mock functions

**API Reference:**
- **[test](references/api/test.md)** - Test definition
- **[expect](references/api/expect.md)** - Assertions and matchers
- **[describe](references/api/describe.md)** - Test suites
- **[hooks](references/api/hooks.md)** - Lifecycle hooks

**Configuration:**
- **[Config Reference](references/config/INDEX.md)** - All options
- **[Coverage](references/config/coverage.md)** - Coverage setup
- **[Browser Mode](references/config/browser/INDEX.md)** - Browser testing config

**Migration:**
- **[Migration Guide](references/guide/migration.md)** - Version migration
- **[Jest Comparison](references/guide/comparisons.md)** - Jest to Vitest
- **[Vitest 4.0](references/vitest-4.md)** - Latest release notes

**Advanced:**
- **[Browser Testing](references/guide/browser/)** - Component testing guide
- **[Workspace](references/guide/projects.md)** - Monorepo setup
- **[Performance](references/guide/improving-performance.md)** - Optimization

When working with Vitest, consult the appropriate reference file based on your task. Start with the guide for conceptual understanding, then refer to API/config references for specific implementation details.
