---
name: e2e-testing
description: 'E2E test architecture and patterns with Playwright. Use when designing test suites, structuring Page Object Models, planning CI sharding strategies, setting up authentication flows, or organizing tests with tags and annotations. Use for test architecture, accessibility auditing with axe-core, network mocking strategies, visual regression workflows, HAR replay, and storageState authentication patterns. For Playwright API details, browser automation, or web scraping, use the playwright skill instead.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# E2E Testing

## Overview

Covers E2E test architecture and patterns using Playwright — how to structure test suites, organize tests, and apply proven patterns for authentication, mocking, visual regression, accessibility auditing, and CI parallelism. Focuses on the WHY and WHEN of test patterns rather than Playwright API specifics.

**When to use:** Designing test suite architecture, structuring Page Object Models, planning CI sharding strategies, setting up authentication flows, organizing tests with tags and annotations, implementing visual regression workflows, mocking network requests, auditing accessibility.

**When NOT to use:** Unit testing (use Vitest/Jest), API-only testing (use integration tests), component testing in isolation (use component test runners). For Playwright API details, browser automation, scraping, or troubleshooting Playwright errors, use the `playwright` skill.

## Quick Reference

| Pattern              | API/Tool                                 | Key Points                                         |
| -------------------- | ---------------------------------------- | -------------------------------------------------- |
| Role-based locators  | `getByRole`, `getByText`, `getByLabel`   | Preferred over CSS/XPath selectors                 |
| Page Object Model    | Classes in `tests/pages/`                | Encapsulate all page-specific locators and actions |
| Authentication       | `storageState` + setup projects          | Authenticate once, reuse across tests              |
| Visual regression    | `expect(page).toHaveScreenshot()`        | Mask dynamic content to prevent flakes             |
| Accessibility audit  | `AxeBuilder` from `@axe-core/playwright` | `.withTags()` + `.analyze()` on key flows          |
| Trace debugging      | `trace: 'on-first-retry'`                | Full DOM snapshots, network logs, and timeline     |
| Network mocking      | `page.route()`                           | Stable tests without third-party dependencies      |
| HAR replay           | `page.routeFromHAR()`                    | High-fidelity mocks from recorded traffic          |
| Image blocking       | `page.route('**/*.{png,jpg}', abort)`    | Speed up tests by skipping images                  |
| CI sharding          | `--shard=1/4`                            | Split suite across parallel CI machines            |
| Blob reports         | `--reporter=blob` + `merge-reports`      | Merge sharded results into a single report         |
| Test tags            | `{ tag: ['@smoke'] }`                    | Filter tests by category with `--grep`             |
| Test steps           | `test.step('name', async () => {})`      | Group actions in trace viewer and reports          |
| Changed tests only   | `--only-changed=$GITHUB_BASE_REF`        | Run only test files changed since base branch      |
| Native a11y checks   | `toHaveAccessibleName`, `toHaveRole`     | Lightweight alternative to full axe-core scans     |
| Git info in reports  | `captureGitInfo` reporter option         | Link test reports to commits for CI debugging      |
| Web-first assertions | `expect(element).toBeVisible()`          | Auto-wait instead of `waitForTimeout`              |

## Common Mistakes

| Mistake                                                  | Correct Pattern                                                               |
| -------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Using `page.waitForTimeout()` for element visibility     | Use web-first assertions like `expect(element).toBeVisible()` which auto-wait |
| Writing raw locators directly in test files              | Encapsulate all selectors in Page Object Model classes                        |
| Testing third-party APIs (Stripe, Auth0) directly        | Mock external services with `page.route()` for stable, fast tests             |
| Debugging CI failures with screenshots instead of traces | Configure `trace: 'on-first-retry'` and use Playwright Trace Viewer           |
| Sharing state between tests via global variables         | Use a fresh `BrowserContext` per test for full isolation                      |
| Running all tests in a single CI job                     | Use Playwright sharding (`--shard=1/N`) across parallel machines              |
| Using CSS/XPath selectors for element location           | Use role-based locators that survive refactors and enforce accessibility      |
| Logging in via UI in every test                          | Use `storageState` with setup projects to authenticate once                   |
| Using `injectAxe`/`checkA11y` from `axe-playwright`      | Use `AxeBuilder` from `@axe-core/playwright` with `.analyze()`                |
| Committing `storageState` JSON files to git              | Add `playwright/.auth/` to `.gitignore`                                       |

## Delegation

- **Discover which user flows lack E2E coverage**: Use `Explore` agent
- **Build a full Page Object Model test suite for an application**: Use `Task` agent
- **Plan a CI sharding strategy for a large test suite**: Use `Plan` agent

> For Playwright API details, browser automation, scraping, stealth mode, screenshots/PDFs, Docker deployment, or troubleshooting Playwright errors, use the `playwright` skill.

## References

- [Role-based locators, auto-waiting, chaining, filtering, and locator strategy](references/locators.md)
- [Page Object Model architecture, fixtures integration, and base page patterns](references/page-objects.md)
- [Authentication with storageState, setup projects, and multi-role testing](references/authentication.md)
- [Network mocking, route interception, HAR replay, and WebSocket mocking](references/mocking.md)
- [Accessibility auditing with AxeBuilder, WCAG tags, and reusable fixtures](references/accessibility.md)
- [Visual regression, snapshot testing, masking, tolerance thresholds, and baseline management](references/visual-testing.md)
- [CI sharding, parallelism, blob reports, and browser caching](references/ci-sharding.md)
- [Test organization with tags, annotations, test.step, and project configuration](references/test-organization.md)
