---
name: frontend-engineering
description: Build and maintain web frontends — component architecture, state management,
  API integration, responsive layout, client-side performance, and frontend testing
  patterns. Framework agnostic, focused on web frontend implementation. Do not use
  for backend service implementation, data engineering, or platform infrastructure
  work.
license: MIT
metadata:
  tags: frontend, web, ui, components, state-management, performance, javascript,
    typescript, responsive, testing
  source_repo: https://github.com/magnus919/hermes-profiles
---

# Frontend Engineering Methodology

Frontend engineering is the craft of building the user-facing layer of applications — components, state management, API integration, responsive layout, and client-side performance. This methodology bridges UX design (user journeys, wireframes, accessibility standards) and quality validation (qa-methodology).

## The Frontend Engineer's Domain

| You own | You don't own |
|---------|--------------|
| Component implementation — UI component composition, props/state interfaces, rendering patterns, lifecycle | User journeys, wireframes, accessibility standards, interaction design — that's the product-design-and-ux |
| State management — client-side state architecture, data fetching patterns, caching, optimistic updates | API contract design — that's the api-design-and-evolution |
| API integration — frontend-to-backend data flow, auth flows (OAuth, JWT), real-time updates | Test strategy and automation — that's the QA-engineer |
| Responsive design implementation — layout systems, breakpoints, cross-device testing | Visual identity and brand guidelines — that's the brand-designer |
| Client-side performance — bundle optimization, lazy loading, Core Web Vitals, render optimization | Editorial content and copy — owned by the content and marketing team, outside this skill's scope |
| Frontend testing — component tests, integration tests, visual regression, accessibility tests | Code review and quality gates — that's the qa-methodology |
| E2E test scenarios and user-flow coverage for frontend features | Operating the browser test tool (Playwright) — authoring/running specs, selectors, network mocking, scraping — route to [playwright](../playwright/SKILL.md) |
| Mobile app implementation (iOS/Android/Flutter/React Native) | Mobile platform work — scaffolding, builds and code signing, device/emulator testing, store submission, mobile lifecycle — route to [mobile-development](../mobile-development/SKILL.md); this skill owns web frontends |
| Build tooling — bundler config, TypeScript config, linting, formatting, dev environment | CI/CD pipeline infrastructure — that's the platform-engineer |

For React component and hooks work, load [react](../react/SKILL.md); for Vite config, modes, plugins, and builds, load [vite](../vite/SKILL.md). This skill remains the owner of framework-neutral architecture and frontend strategy.

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/component-architecture.md` | Designing component trees — composition patterns, props/state interfaces, lifecycle, accessibility fundamentals |
| `references/state-management.md` | Choosing and implementing state management — client vs server state, data fetching, caching, optimistic updates |
| `references/api-integration.md` | Connecting frontend to backend — API client design, auth token flow, error handling in the UI, real-time subscriptions |
| `references/responsive-layout-testing.md` | Implementing responsive designs (layout system selection — Grid vs Flexbox vs Container Queries, breakpoint strategies, cross-device testing methodology) and testing frontend code (component testing with Testing Library, integration testing with Playwright/Cypress, visual regression, accessibility testing with axe-core and Lighthouse CI, test data management) |
| `references/performance.md` | Optimizing client-side performance — Core Web Vitals, bundle analysis, code splitting, render optimization |

## Templates

| Template | When to Use |
|-----------|-------------|
| `templates/component-state-design-record.md` | Designing a component tree and state ownership for a feature — decomposition, state scoping, data fetching, and error/loading UX |
| `templates/performance-budget.md` | Defining performance targets — bundle byte budgets, Core Web Vitals budgets, measurement setup, and CI enforcement |

## Scripts

| Script | When to Use |
|-----------|-------------|
| `scripts/bundle-budget-checker.py` | Checking a bundle size report against total and per-chunk budgets; fails (exit 1) when a budget is exceeded, so CI can block performance regressions |

## Core Principles

**Components are the unit of composition, not pages** — Design and build components as reusable, composable units. Pages are assembled from components, not built as monoliths. A well-designed component can be reused in contexts its creator never imagined.

**Co-locate state with the components that need it** — Not every piece of state belongs in a global store. Local state stays local. Server state is fetched and cached. Only truly shared application state belongs in a global context.

**Design for every state, not just the happy path** — Every data-dependent component has at least four states: loading, empty, error, and success. Designing for all four is not a nicety — it creates a resilient user experience.

**Accessibility is not a feature, it's a requirement** — Keyboard navigation, screen reader support, color contrast, and focus management are not enhancements. They are part of the implementation contract.

**Performance is a UX concern** — Every millisecond of load time, every layout shift, every janky interaction erodes user trust. Performance budgeting, bundle analysis, and render optimization are part of frontend engineering, not an afterthought.
