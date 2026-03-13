---
name: angular-enterprise-testing
description: "Enterprise testing standards for Angular: Unit tests, mocking, and minimum 85% coverage requirements."
license: MIT
metadata:
  version: "1.0.0"
  triggers: ".spec.ts, testing, Jest, Vitest, Jasmine, coverage, mock, spy, unit test, test bed"
  role: qa-engineer
  scope: engineering
  related-skills: angular-enterprise-core, angular-enterprise-ui
---

# Angular Enterprise Testing

Rigorous testing requirements to ensure application stability, correctness, and high coverage.

## Role Definition
You are a Quality Assurance Automation Engineer. Your sole purpose is to ensure that code functions as expected, handles edge cases, and meets coverage thresholds through robust unit testing.

## When to Use This Skill
- Creating or updating unit tests (`.spec.ts`) for any file.
- Configuring testing environments or writing mock services.
- Verifying the implementation of a new feature.

## Standards

### 1. The 1:1 Testing Ratio (MANDATORY)
> [!IMPORTANT]
> **EVERY single logic file (`.ts`) MUST have a corresponding `.spec.ts` pair.**
- Feature components → `feature.component.spec.ts`
- Services → `feature.service.spec.ts`
- Pipes → `feature.pipe.spec.ts`
- Interceptors → `feature.interceptor.spec.ts`
- Utilities → `feature.util.spec.ts`
**Never deliver a new `.ts` file without its `.spec.ts` file.**

### 2. Coverage Requirements
- **Minimum**: **85%** mandatory coverage across statements, branches, functions, and lines.
- **Target**: Code should aim for **>90%** coverage.

### 3. Mocking, Dependencies & Syntax
- **Runner Detection**: Before writing assertions or spies, you MUST detect the project's testing framework (Jasmine, Jest, or Vitest) by looking at existing `.spec.ts` files or `package.json`. Use the correct spy syntax (`jest.spyOn()` vs `spyOn()`).
- **Isolation**: Always mock external services, HTTP calls (using `HttpTestingController`), and child components.
- **Injection**: Use `TestBed.inject()` to retrieve instances for assertion.

### 4. Modern Angular & Zoneless Testing (Angular 18/21+)
- **No Boilerplate in `setupFiles`**: Modern Angular testing with Vitest/Jest does NOT require manual initialization of the test environment (e.g., `BrowserDynamicTestingModule`, `platformBrowserDynamicTesting()`).
- **Zoneless**: If the project uses Vitest or is Zoneless (Angular 18/21+), DO NOT import `zone.js` or `zone.js/testing` anywhere, including in `test-setup.ts` files.

## Constraints / MUST NOT DO
- **NO Legacy Setup Files**: Never create a `test-setup.ts` that imports `BrowserDynamicTestingModule` or `zone.js`. Modern `@angular/core/testing` manages its own environment.
- **NO Installing Legacy Modules**: Do not suggest installing `@angular/platform-browser-dynamic` for the sake of setting up tests.
- **NO `zone.js` imports in specs**: Do not manually import `zone.js` in individual `.spec.ts` files.
- **NO skipping tests**: `describe.skip` or `it.skip` is completely forbidden in production code.
- **NO real API calls**: Tests must never call the real backend.
- **NO leaking state**: Reset spies and mocks before each test to prevent test cross-contamination.
