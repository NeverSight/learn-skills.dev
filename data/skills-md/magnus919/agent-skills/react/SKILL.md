---
name: react
description: >-
  Operate React applications as a named tool: inspect and diagnose React/Vite
  projects, design component boundaries and state flow, implement accessible
  responsive UI, and verify behavior with the project's tests. Use when a task
  explicitly involves React, JSX/TSX, React hooks, React Router, Vite React
  configuration, or React build failures. Do not use for framework-agnostic
  frontend strategy (route to frontend-engineering), browser automation (route
  to playwright), accessibility policy or audits (route to web-accessibility),
  or non-React mobile apps (route to mobile-development).
license: MIT
compatibility: >-
  The bundled diagnostic script uses Python 3.8+ standard library only. Running
  or building an application requires its repository package manager and Node.js.
metadata:
  tags: react, jsx, tsx, vite, hooks, components, router, frontend
  source: https://react.dev/
---

# React Application Engineering

Use this skill for the React-specific implementation layer. Preserve the
project's existing React version, package manager, build scripts, styling
conventions, and routing model unless the user asks for a migration.

## Operating loop

1. **Diagnose before editing.** Run `scripts/react-doctor.py --json [PROJECT]` and
   inspect `package.json`, source entry points, Vite config, TypeScript config,
   routes, and test scripts. The diagnostic is bounded and read-only.
2. **Define the component contract.** Identify the page/feature boundary,
   inputs and outputs, owned state, server state, loading/empty/error/success
   states, and side effects. Keep reusable components independent of route
   globals and avoid passing state through unrelated layers.
3. **Implement with explicit data flow.** Prefer local state for local behavior,
   context only for genuinely cross-cutting concerns, and the existing server
   state/cache solution for remote data. Keep effects for synchronization with
   external systems; derive values during render rather than storing duplicates.
4. **Keep UI resilient.** Render a useful loading, empty, error, and success
   experience. Cancel or ignore stale async work, handle aborts, and avoid
   setting state after an obsolete request. Preserve stable keys and avoid
   mutating props or state.
5. **Build for the browser.** Use semantic HTML, keyboard-operable controls,
   visible focus, responsive layout, and stable accessible names. For detailed
   accessibility requirements, load [web-accessibility](../web-accessibility/SKILL.md).
6. **Verify in layers.** Run the narrowest existing unit/component test, then
   lint/typecheck, then the production build. For browser-level flows use
   [playwright](../playwright/SKILL.md), not ad hoc browser automation. Report
   the exact commands and any environment-dependent checks that were skipped.

## React-specific rules

- Hooks run unconditionally and in the same order on every render; never call
  them in branches, loops, event handlers, or nested functions.
- Effects synchronize with external systems. Do not use an effect to calculate
  a value that can be derived from props/state, or to mirror props into state
  without a clear user-editing requirement.
- Use functional updates when the next state depends on the previous state.
  Give list items stable keys from domain identity, not array indexes when the
  list can reorder, insert, or delete.
- Treat event handlers as user intent and keep them separate from render-time
  computation. Disable or guard duplicate submissions and expose pending state.
- Keep API response validation and transformation at the integration boundary;
  components should consume a typed, predictable view model.
- Do not add a state library or router solely because it is popular. First map
  ownership and use the project's existing choices.
- In Vite, expose only intentionally public variables using the project's
  documented prefix (normally `VITE_`); never put secrets in client bundles.
  Read [references/vite-diagnostics.md](references/vite-diagnostics.md) for
  environment, build, and deployment checks.

## Routing and handoffs

- Component architecture, responsive implementation, performance budgets, and
  general frontend testing: [frontend-engineering](../frontend-engineering/SKILL.md).
- Browser E2E authoring, locator choice, network interception, and Playwright
  runs: [playwright](../playwright/SKILL.md).
- Semantic structure, keyboard/focus behavior, WCAG acceptance evidence, and
  accessibility audits: [web-accessibility](../web-accessibility/SKILL.md).
- React Native, Expo, Android, or iOS implementation: [mobile-development](../mobile-development/SKILL.md).

## Reference routing

| Load when | Reference |
|---|---|
| Choosing component boundaries, state ownership, effects, or async UI behavior | `references/component-and-state.md` |
| Diagnosing Vite env exposure, dependency versions, build output, or deployment paths | `references/vite-diagnostics.md` |

## Included script

`scripts/react-doctor.py` is a read-only, dependency-free diagnostic. Run
`scripts/react-doctor.py --help` for options. It accepts a project directory,
checks common React/Vite signals, and emits human-readable or bounded JSON
output. It does not install packages, execute project scripts, access the
network, or print environment values.

## Completion boundary

Stop when the requested React change is implemented, the project's relevant
checks have run, and remaining failures are reported with their command and
root-cause evidence. Do not broaden a component task into a framework migration
or an accessibility audit without explicit scope.
