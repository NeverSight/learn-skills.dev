---
name: writing-unit-tests-typescript
description: Guidelines and patterns for writing unit tests in TypeScript using Vitest.
---
# Skill: Writing TypeScript Unit Tests

## Overview

This skill covers writing unit tests for the frontend using **Vitest**.

## Project Structure

```text
frontend/
├── package.json          # vitest + jsdom devDependencies
├── vite.config.ts        # Vitest config inline
└── src/
    ├── config/
    │   └── __tests__/
    │       └── authConfig.test.ts
    ├── utils/
    │   ├── citationParser.ts
    │   ├── sseParser.ts
    │   ├── fileAttachments.ts
    │   └── __tests__/
    │       ├── citationParser.test.ts
    │       ├── sseParser.test.ts
    │       └── fileAttachments.test.ts
    ├── services/
    │   └── __tests__/
    │       └── chatService.test.ts
    └── reducers/
        ├── appReducer.ts
        └── __tests__/
            └── appReducer.test.ts    # Includes state shape snapshot
```

## Configuration

The Vitest config lives inline in `vite.config.ts`:

```typescript
export default defineConfig({
  // ... existing config
  test: {
    globals: true,
    environment: "jsdom",
    include: ["src/**/*.test.{ts,tsx}"],
  },
});
```

## Test Anatomy

```typescript
import { describe, it, expect } from "vitest";
import { parseCitations, deduplicateAnnotations } from "../citationParser";

describe("citationParser", () => {
  describe("parseCitations", () => {
    it("returns empty array for empty input", () => {
      expect(parseCitations("", [])).toEqual([]);
    });

    it("extracts citation markers from text", () => {
      const text = "Hello [1] world [2]";
      const result = parseCitations(text, annotations);
      expect(result).toHaveLength(2);
    });
  });

  describe("deduplicateAnnotations", () => {
    it("removes duplicate annotations by URL", () => {
      const annotations = [
        { url: "https://example.com", title: "Example" },
        { url: "https://example.com", title: "Example Duplicate" },
      ];
      expect(deduplicateAnnotations(annotations)).toHaveLength(1);
    });
  });
});
```

## Running Tests

```powershell
# Run tests in watch mode (interactive)
cd frontend
npm test

# Run tests once (CI mode)
npm run test:run

# Run with coverage
npm run test:coverage

# Run specific file
npx vitest run src/utils/__tests__/citationParser.test.ts

# Run tests matching pattern
npx vitest run --testNamePattern="parseCitations"
```

## Testable Units in This Project

### Utils (Pure Functions - Easy to Test)

| File | Functions to Test |
|------|-------------------|
| `citationParser.ts` | `parseContentWithCitations` |
| `sseParser.ts` | `parseSseLine`, `splitSseBuffer` |
| `fileAttachments.ts` | `validateFile`, `validateImageFile`, `validateDocumentFile`, `validateFileCount`, `getEffectiveMimeType`, `convertFilesToDataUris` |
| `errorHandler.ts` | `getUserFriendlyMessage`, `createAppError`, `getErrorCodeFromResponse`, `parseErrorFromResponse`, `getErrorCodeFromMessage`, `isTokenExpiredError`, `isNetworkError`, `retryWithBackoff` |

### Reducers (Pure Functions - Easy to Test)

| File | What to Test |
|------|--------------|
| `appReducer.ts` | All action types, state transitions, immutability |

### Components (Require React Testing Library)

For component testing, add `@testing-library/react` only when needed:

```typescript
import { render, screen } from "@testing-library/react";
import { ChatMessage } from "../ChatMessage";

it("renders message content", () => {
  render(<ChatMessage role="user" content="Hello" />);
  expect(screen.getByText("Hello")).toBeInTheDocument();
});
```

## Assertions Reference

Vitest uses Chai-style assertions via `expect`:

```typescript
// Equality
expect(actual).toBe(expected);           // strict equality (===)
expect(actual).toEqual(expected);        // deep equality

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();

// Numbers
expect(num).toBeGreaterThan(5);
expect(num).toBeLessThanOrEqual(10);

// Strings
expect(str).toContain("substring");
expect(str).toMatch(/regex/);

// Arrays
expect(arr).toHaveLength(3);
expect(arr).toContain(item);

// Objects
expect(obj).toHaveProperty("key");
expect(obj).toMatchObject({ partial: "match" });

// Exceptions
expect(() => throwingFn()).toThrow();
expect(() => throwingFn()).toThrowError("message");

// Async
await expect(asyncFn()).resolves.toBe(value);
await expect(asyncFn()).rejects.toThrow();
```

## Test Organization

Use `describe` blocks to group related tests:

```typescript
describe("moduleName", () => {
  describe("functionName", () => {
    it("handles normal case", () => {});
    it("handles edge case", () => {});
    it("throws on invalid input", () => {});
  });
});
```

## State Shape Snapshot Tests

Use state shape snapshots to prevent accidental state changes from going unnoticed. If a new field is added to `AppState` without updating the test, it fails:

```typescript
it('should have expected state shape (update this test when adding new state fields)', () => {
  const shape = JSON.stringify(Object.keys(initialAppState).sort());
  expect(shape).toBe('["auth","chat","conversations","ui"]');
  const convShape = JSON.stringify(Object.keys(initialAppState.conversations).sort());
  expect(convShape).toBe('["hasMore","isLoading","list","sidebarOpen"]');
});
```

This forces anyone adding state fields to also add test coverage — the test file becomes the registry of all state. Apply this pattern to any new top-level state domain.

## When Unit Tests Aren't Enough

Use the `validating-ui-features` skill and Playwright when:
- Testing requires browser interaction (clicking, navigation)
- Testing authentication flows with MSAL
- Testing SSE streaming with real backend
- Visual regression testing

## Quick Reference

| Command | Purpose |
|---------|---------|
| `npm test` | Watch mode |
| `npm run test:run` | Run once |
| `npm run test:coverage` | With coverage |
| `npx vitest --ui` | Interactive UI |
