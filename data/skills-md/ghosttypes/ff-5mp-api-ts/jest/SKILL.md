---
name: jest
description: Comprehensive JavaScript testing with Jest 30.0. Use when writing tests, debugging test failures, setting up Jest in projects, configuring test runners, mocking modules and functions, writing async tests, snapshot testing, framework integration with React or React Native, or any Jest-related task
---

# Jest Testing Framework

## Overview

Jest is a delightful JavaScript testing framework with a focus on simplicity. It works with projects using Babel, TypeScript, Node, React, Angular, Vue, and more.

## Quick Start

**Installation:**
```bash
npm install --save-dev jest
```

**Add to package.json:**
```json
{
  "scripts": {
    "test": "jest"
  }
}
```

**First test (`sum.test.js`):**
```javascript
const sum = require('./sum');

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

**Run tests:**
```bash
npm test
```

## Basic Test Structure

### Test Blocks

- `test(name, fn)` - Single test
- `describe(name, fn)` - Groups related tests
- `only` - Run only this test: `test.only()`, `describe.only()`
- `skip` - Skip this test: `test.skip()`, `describe.skip()`

```javascript
describe('Math operations', () => {
  test('adds 1 + 2 to equal 3', () => {
    expect(sum(1, 2)).toBe(3);
  });

  test('multiplies 3 * 4 to equal 12', () => {
    expect(multiply(3, 4)).toBe(12);
  });
});
```

## Common Matchers

### Exact Equality

```javascript
// Primitive values
expect(2 + 2).toBe(4);

// Objects and arrays (deep equality)
expect({ one: 1, two: 2 }).toEqual({ one: 1, two: 2 });
```

### Truthiness

```javascript
toBeNull()           // matches only null
toBeUndefined()      // matches only undefined
toBeDefined()        // opposite of toBeUndefined
toBeTruthy()        // matches if statement truthy
toBeFalsy()          // matches if statement falsy
```

### Numbers

```javascript
toBeGreaterThan(3)
toBeGreaterThanOrEqual(3.5)
toBeLessThan(5)
toBeLessThanOrEqual(4.5)
toBeCloseTo(0.3)     // floating point
```

### Strings

```javascript
toMatch(/stop/)
```

### Arrays

```javascript
toContain('milk')
```

### Negation

```javascript
expect(2 + 2).not.toBe(5);
```

## Testing Async Code

### Promises

```javascript
// Return the promise
test('the data is peanut butter', () => {
  return fetchData().then(data => {
    expect(data).toBe('peanut butter');
  });
});

// Use .resolves
test('the data is peanut butter', () => {
  return expect(fetchData()).resolves.toBe('peanut butter');
});

// Use .rejects
test('the fetch fails', () => {
  return expect(fetchData()).rejects.toMatch('error');
});
```

### Async/Await

```javascript
test('the data is peanut butter', async () => {
  const data = await fetchData();
  expect(data).toBe('peanut butter');
});

test('the fetch fails', async () => {
  await expect(fetchData()).rejects.toMatch('error');
});
```

### Callbacks

```javascript
test('the data is peanut butter', done => {
  function callback(data) {
    expect(data).toBe('peanut butter');
    done();
  }
  fetchDataCallback(callback);
});
```

## Setup and Teardown

### Repeating Setup (Each Test)

```javascript
beforeEach(() => {
  initializeCityDatabase();
});

afterEach(() => {
  clearCityDatabase();
});
```

### One-Time Setup

```javascript
beforeAll(() => {
  return initializeCityDatabase();
});

afterAll(() => {
  return clearCityDatabase();
});
```

### Scoping

Hooks in `describe` blocks apply only to tests within that block. Outer hooks run before inner hooks.

```javascript
describe('outer', () => {
  beforeAll(() => { /* runs first */ });
  beforeEach(() => { /* runs before each test */ });

  describe('inner', () => {
    beforeAll(() => { /* runs second */ });
    beforeEach(() => { /* runs before each test in inner */ });
  });
});
```

## Mocking

### Mock Functions

```javascript
const mockFn = jest.fn(x => 42 + x);

// Inspect calls
expect(mockFn.mock.calls.length).toBe(2);
expect(mockFn.mock.calls[0][0]).toBe(0);

// Return values
mockFn.mockReturnValueOnce(10).mockReturnValue(true);

// Implementation
mockFn.mockImplementation(() => 'default');
```

### Module Mocking

```javascript
import axios from 'axios';
jest.mock('axios');

// Mock resolved value
axios.get.mockResolvedValue({ data: users });

// Mock implementation
axios.get.mockImplementation(() => Promise.resolve(resp));
```

### Mock Matchers

```javascript
expect(mockFunc).toHaveBeenCalled();
expect(mockFunc).toHaveBeenCalledWith(arg1, arg2);
expect(mockFunc).toHaveBeenLastCalledWith(arg1, arg2);
```

## Snapshot Testing

### Basic Snapshot

```javascript
test('renders correctly', () => {
  const tree = renderer.create(<Link />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

### Update Snapshots

```bash
jest --updateSnapshot
# or
jest -u
```

### Inline Snapshots

```javascript
test('renders correctly', () => {
  const tree = renderer.create(<Link />).toJSON();
  expect(tree).toMatchInlineSnapshot();
});
```

### Property Matchers

```javascript
expect(user).toMatchSnapshot({
  createdAt: expect.any(Date),
  id: expect.any(Number),
});
```

## Configuration

### Generate Config

```bash
npm init jest@latest
```

### Config File (`jest.config.js`)

```javascript
module.exports = {
  // Test environment
  testEnvironment: 'node', // or 'jsdom' for React

  // Test file patterns
  testMatch: [
    '**/__tests__/**/*.[jt]s?(x)',
    '**/?(*.)+(spec|test).[jt]s?(x)'
  ],

  // Coverage
  collectCoverageFrom: ['src/**/*.{js,jsx}'],
  coverageDirectory: 'coverage',

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],

  // Transforms (Babel, TypeScript)
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },

  // Module mocking
  moduleNameMapper: {
    '\\.(css|less)$': 'identity-obj-proxy',
  },
};
```

### TypeScript

```bash
npm install --save-dev ts-jest @types/jest
```

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
};
```

### React

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom jest-environment-jsdom
```

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
};
```

```javascript
// src/setupTests.js
import '@testing-library/jest-dom';
```

## CLI Options

```bash
jest                    # Run all tests
jest --watch            # Watch mode
jest --coverage         # Generate coverage
jest --updateSnapshot   # Update snapshots
jest --verbose          # Detailed output
jest --findRelatedTests # Test changed files
```

## Framework-Specific Testing

### React (see TutorialReact.md)

```javascript
import { render, screen } from '@testing-library/react';

test('renders button', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByText('Click me')).toBeInTheDocument();
});
```

### React Native (see TutorialReactNative.md)

Use `react-test-renderer` for snapshot testing.

### Async Patterns (see TutorialAsync.md)

Comprehensive examples for promises, async/await, callbacks, and timers.

## Best Practices

1. **Descriptive test names** - "should return user when id exists" vs "returns user"
2. **One assertion per test** - Keep tests focused
3. **Arrange-Act-Assert** - Structure tests clearly
4. **Mock external dependencies** - Don't make real API calls
5. **Test behavior, not implementation** - Focus on what, not how
6. **Use setup/teardown** - Avoid code duplication
7. **Keep tests deterministic** - No random data or dates (mock them)

## Resources

### Setup & Configuration
- **GettingStarted.md** - Installation, Babel, TypeScript, ESLint setup
- **Configuration.md** - Complete config options reference
- **CLI.md** - All command-line options
- **EnvironmentVariables.md** - Environment setup
- **TestingFrameworks.md** - Framework-specific setup guides

### Core Testing
- **UsingMatchers.md** - Common matchers (toBe, toEqual, truthiness, numbers, arrays)
- **TestingAsyncCode.md** - Promises, async/await, callbacks, timers
- **SetupAndTeardown.md** - beforeEach, afterEach, beforeAll, afterAll, scoping

### Mocking
- **MockFunctions.md** - Mock functions, .mock property, return values
- **MockFunctionAPI.md** - Complete mock API reference
- **ManualMocks.md** - Manual module mocks
- **Es6ClassMocks.md** - ES6 class mocking
- **BypassingModuleMocks.md** - Bypassing module mocks

### API References
- **ExpectAPI.md** - Complete expect() matcher reference (63k+ bytes)
- **GlobalAPI.md** - describe, test, it, skip, only, etc. (35k+ bytes)
- **JestObjectAPI.md** - Jest object API (36k+ bytes)

### Advanced Features
- **SnapshotTesting.md** - Snapshot testing, inline snapshots, property matchers
- **TimerMocks.md** - Fake timers, timer mocking APIs
- **CodeTransformation.md** - Custom transforms
- **ECMAScriptModules.md** - ESM support
- **WatchPlugins.md** - Custom watch plugins

### Framework Tutorials
- **TutorialReact.md** - React testing with @testing-library/react
- **TutorialReactNative.md** - React Native testing
- **TutorialAsync.md** - Async patterns and examples
- **TutorialjQuery.md** - jQuery testing

### Integration Guides
- **Webpack.md** - Webpack integration
- **Puppeteer.md** - Puppeteer integration
- **DynamoDB.md** - DynamoDB testing
- **MongoDB.md** - MongoDB testing

### Meta & Support
- **Architecture.md** - Jest architecture
- **Troubleshooting.md** - Common issues and solutions
- **MigrationGuide.md** - Upgrading guide
- **JestPlatform.md** - Jest platform packages
- **JestCommunity.md** - Community resources
- **MoreResources.md** - Additional learning resources

### Assets
- **assets/configs/** - Configuration templates (basic, TypeScript, Babel, React, package.json)
- **assets/test-templates/** - Test file templates (basic, async, mock, snapshot, setup, react)
