---
name: backend-to-ui
description: Build, redesign and improve existing frontends in any framework or build UI from real backends, APIs and page props. Use for frontend-only apps, established projects, backend-to-frontend integration, visual UX audits, data-heavy screens and one-shot implementation. Preserve architecture, brand and behavior; verify real user flows, accessibility and rendering performance.
license: MIT
metadata:
  version: "1.3.0"
---

# Backend to UI

Build **product-specific interfaces** for existing frontend apps or backend-only projects. Existing React, Vue, Angular, Svelte, server-rendered, native and unfamiliar frameworks are first-class targets. Preserve what works; do not turn a mature application into a generic remake. When a backend exists, its contracts define what the UI can actually do.

## How to work

One request should run end-to-end when the repository and tools permit, **after the required frontend stack is selected**. Do not stop at a plan or mockup. Keep the existing stack, auth and brand. Ask only about true blockers or high-risk changes **except the mandatory frontend stack decision below**; label reasonable product assumptions instead of inventing facts.

## Mandatory frontend stack gate (before editing UI files)

If implementation or redesign is requested, read [stack decision policy](references/stack-selection.md) **before changing frontend code**.

- If the user explicitly names a frontend stack (including plain/native HTML/CSS/JS), use it unless incompatible with hard repository constraints; explain any conflict.
- If the user explicitly authorizes **reuse of the existing frontend stack** and one is reliably detected, proceed with that stack.
- If no stack is specified or authorized, **ask one direct question**. If the repo uses Vue + Inertia, for example: "I found Vue + Inertia. Should I continue with it, or use another frontend stack?" If no frontend is present: "Which frontend stack should I use?"
- **Do not create or modify frontend implementation files before the answer. Never silently fall back to native HTML/CSS/JavaScript, React, Vue or any other framework.** Backend language, a JSON endpoint, and a package manager alone are not frontend-stack consent.
- A read-only audit may proceed without this question; ask before subsequently implementing changes. Once the stack is confirmed, perform remaining steps autonomously and only ask again for a genuine blocker.

**One-shot** means one request can complete the implementation when the stack decision is already resolved; it does not override this explicit user-choice gate.

1. **Inspect.** Verify the frontend stack gate. Choose the work mode: **existing frontend**, **backend-only**, **integrate frontend and backend**, or **read-only audit**. For existing UIs, inspect entry points, routes, shared components, theme/tokens, styles, state owners, data adapters, existing tests, assets and responsive behavior before editing. Read [existing frontend playbook](references/existing-frontend.md). If there is a backend, inspect routes/handlers, schemas, policies, response shapes, pagination and errors; read [data contracts](references/data.md). Never invent backend actions or metrics.
2. **Understand.** Identify the real user, job, device, environment, emotional expectation and **product mode**: operate, explore, play, create, read or persuade. Separate observed facts from assumptions. Do not infer the information architecture from database table names. Read [design direction](references/design.md).
3. **Map.** Document the user flow and what must **remain working** (navigation, component contracts, state, tests and current data flows). If a backend is available, map actions to authorized handlers, fields, states and recovery. In frontend-only apps, use actual local state, fixtures and documented integrations; do **not** fabricate an API. Preserve SSR, native, Inertia, GraphQL and other patterns already used.
4. **Plan for speed.** Trace the **real pipeline**: backend query → transport → client state → render when applicable, or local state → derived state → render for standalone frontends. Preserve efficient existing patterns; apply pagination, cache scope, request deduplication, cancellation/race safety and bounded rendering when relevant. Read [performance](references/performance.md).
5. **Art direct.** Before writing layout code, briefly consider **two materially different compositions** appropriate to the product; select one and state the rationale in the work. Define the dominant subject or task, visual hierarchy, density, typography, color roles, assets and motion. Be specific to the domain, not a default dashboard skin. See [product examples](references/cases.md). Never use large blank desktop margins to hide a phone-sized UI unless that presentation is explicitly the product.
6. **Build.** For an existing frontend, improve it **incrementally in its own framework**: reuse component APIs, routing, styling conventions, state libraries and accessible patterns. Avoid unnecessary replatforming, new dependencies, design-system replacement or regression of unrelated flows. For backend-only projects, implement the explicitly chosen stack. Complete the main user flow and its real states. Give the primary interaction an appropriate share of screen space and visual prominence. Make controls legible and functional; provide loading, empty, error, retry, validation, permission and mutation states where relevant. Do not add decorative complexity in place of useful content.
7. **Test, critique, fix.** Run available tests and inspect **actual rendered desktop and mobile screenshots** (plus an intermediate width when possible). Apply [visual review gates](references/visual-review.md) and [functional verification](references/verify.md). If a serious gate fails, **change the design and review again**; do not stop at a CSS tweak or report success based only on a passing build. Test real data timing and request races. If render tools are unavailable, report visual QA as unverified rather than asserting it passed.
8. **Deliver.** Describe what the user can do, real contracts used, the chosen design rationale, notable visual correction(s), performance controls, tests actually run and outstanding risks. Documentation proportional to the project; no required paperwork for its own sake.

## Hard gates

- **Stack truth:** explicit choice or explicit reuse authorization is required before frontend implementation; detected stack alone is not permission. Never default to native HTML.
- **Existing frontend truth:** do not silently replace existing frameworks, routes, component contracts, state management, design system, localization, theming or working flows. Preserve and verify regressions.
- **Backend truth:** when a backend exists, do not fabricate data, actions or permission checks. When it does not, do not invent a backend or require one to improve UI.
- **Product truth:** screen hierarchy must express the product's defining action or subject. A playful game, a dense operations queue and a medical record must not receive the same page shell.
- **Composition truth:** do not ship a tiny central app surrounded by unused desktop canvas, uniform card grids, repeated pill badges or layers of chrome unless they genuinely serve the task.
- **Craft truth:** typography, proportion, assets, spacing, color and motion must form one coherent direction. Avoid gradient/glass/neon/rounded-card defaults; these are allowed only when supported by the product's visual world and executed with care.
- **Interaction truth:** all visible affordances work; important events have feedback; motion respects reduced-motion preferences and performance.
- **Evidence truth:** screenshot critique requires a screenshot, performance claims require measurements, live API claims require live requests. One-shot means one user prompt, **not** one unreviewed visual pass.

## References (read when needed)

- [stack-selection.md](references/stack-selection.md) — mandatory stack choice and one-shot behavior
- [existing-frontend.md](references/existing-frontend.md) — safe modernization of any existing frontend
- [data.md](references/data.md) — real contracts, permissions, state handling
- [performance.md](references/performance.md) — efficient data pipeline, rendering, cache and races
- [design.md](references/design.md) — product modes and evidence-based visual direction
- [cases.md](references/cases.md) — contextual examples including arcade, operations and reading
- [visual-review.md](references/visual-review.md) — stop-ship visual gates and screenshot iteration
- [stacks.md](references/stacks.md) — stack-specific integration choices
- [verify.md](references/verify.md) — functional and evidence-based acceptance tests

## Example trigger

> Use backend-to-ui to build or improve this project's frontend. Understand its users and backend first. Create a distinctive interface, keep real data fast, inspect screenshots, fix generic design, and test the working flows.
