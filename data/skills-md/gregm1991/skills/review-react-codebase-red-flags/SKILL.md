---
name: review-react-codebase-red-flags
description: Reviews React and TypeScript codebases for maintainability red flags from senior frontend practice. Use when auditing React code, reviewing frontend architecture, finding code smells, preparing refactors, or checking whether a React codebase will be painful to maintain.
---

<objective>
Review React codebases for compounding maintainability risks: unnecessary dependencies, inconsistent structure, shallow abstractions, state misuse, TypeScript drift, fragile rendering, missing error handling, and memoization traps.

Use this skill to produce an evidence-backed audit that names concrete red flags, explains why each one will hurt future work, and suggests small corrective moves before problems spread.
</objective>

<quick_start>
Start with a lightweight scan, then inspect representative files before making claims.

Prioritize findings in this order:
1. **Correctness risks**: broken keys, stale effects, empty catches, missing loading/error states, missing error boundaries.
2. **Change-amplifiers**: god components, massive files, scattered conditionals, junk-drawer utilities, global-store overuse.
3. **Performance and bundle risks**: heavyweight dependencies, context re-render storms, broken memoization, un-memoized provider values.
4. **Maintainability hygiene**: folder chaos, no formatter/linter, weak TypeScript, magic values, missing third-party adapters.

For each finding, report: file path, observed evidence, red flag category, why it matters, and the smallest safe next step.
</quick_start>

<workflow>
1. **Map project conventions first**
   - Read package scripts, lint/format config, TypeScript config, routing/app structure, and existing architecture docs.
   - Do not assume one canonical React structure. Judge consistency against the project's apparent conventions.

2. **Scan for red-flag patterns**
   - Dependencies: libraries used for vanilla JS tasks; heavy packages where lighter alternatives exist; direct third-party imports spread through app code.
   - Structure: inconsistent folders, unrelated `utils`/`helpers`, non-colocated feature files, barrel files that re-export broad surfaces.
   - Components: god components, massive files, unreadable conditional rendering, missing early returns, magic values.
   - Props: passing whole objects when only a field is needed; repeated prop plumbing that exposes implementation details.
   - State: derived values in state, `useState` where `useRef` fits, everything in a global store, one massive Context, un-memoized context values.
   - TypeScript: `any`, broad casts, ignored errors, weak domain types, nullable data handled by hope rather than narrowing.
   - Effects and hooks: `eslint-disable` for `react-hooks/exhaustive-deps`, hooks used where plain functions would do, default values that break memoization.
   - Lists and rendering: array index keys, duplicated conditional logic, scattered feature flags or permission checks.
   - Data and failure handling: custom data-fetching layers without strong reason, no error boundaries, empty catch blocks, missing loading/error/empty states.

3. **Inspect before judging**
   - Open the files behind each suspected pattern.
   - Distinguish deliberate local exceptions from systemic problems.
   - Prefer fewer high-confidence findings over a long checklist of weak matches.

4. **Classify severity**
   - **High**: likely correctness bugs, user-visible failures, stale data, broad re-render cascades, or refactors blocked by dangerous coupling.
   - **Medium**: repeated patterns that amplify change cost or testing difficulty.
   - **Low**: hygiene issues that are real but localized or easy to fix opportunistically.

5. **Recommend small refactors**
   - Replace unnecessary dependencies with built-ins when the call site is simple.
   - Wrap third-party libraries behind local adapters at stable seams.
   - Split god components by responsibility, not by arbitrary line count.
   - Move derived values to render-time calculations or `useMemo` only when measurement/identity requires it.
   - Use refs for mutable values that should not trigger rendering.
   - Split contexts by update frequency and consumer groups; memoize provider values.
   - Convert scattered conditionals into named predicates, policy helpers, or dedicated presenter modules.
   - Add explicit loading, error, empty, and boundary behavior where users can hit failure.

6. **Return an audit report**
   - Start with a short executive summary.
   - List findings by severity, not by scan order.
   - Include file paths and concrete evidence.
   - For each finding, provide the smallest safe next step and note when tests should be added before refactoring.
</workflow>

<red_flags>
<category name="dependencies">
- Using libraries for behavior vanilla JavaScript already handles clearly.
- Reaching for heavy dependencies when lighter alternatives or existing project utilities would suffice.
- Importing third-party APIs directly throughout the app instead of isolating them behind adapters.
</category>

<category name="organization">
- No consistent folder structure.
- Junk-drawer `utils` or `helpers` files containing unrelated behavior.
- Related files not colocated, forcing maintainers to chase one feature across the tree.
- Barrel files that re-export everything and hide dependency direction.
</category>

<category name="components_and_rendering">
- God components and massive files nobody wants to touch.
- Passing entire objects when a component only needs one field.
- Unreadable conditional rendering and no early returns.
- Magic values with no name or explanation.
- Array indices used as keys for lists that can reorder, insert, or delete.
</category>

<category name="state_and_context">
- Storing derived values in state.
- Using state for mutable values that should be refs.
- Putting local or feature state into a global store by default.
- One massive Context that re-renders broad parts of the app.
- Context provider values recreated every render without memoization.
</category>

<category name="typescript_hooks_and_errors">
- Poor TypeScript hygiene: `any`, unchecked casts, ignored compiler errors, vague object shapes.
- Disabling `react-hooks/exhaustive-deps` instead of fixing effect design.
- Using a hook when a plain function would do.
- External stores (subscribe/getSnapshot for `useSyncExternalStore`) implemented inside a hook via `useRef` + `useCallback` instead of as a pure factory closure with a thin hook binding. This passes a skim because `useSyncExternalStore` appears correctly at the leaf — check the store's implementation, not just its interface. The tell: every React API in the hook is inert (refs as pure instance storage, `useCallback` only for identity, no `useState`/`useEffect`). Symptoms: the store is plumbed through hook returns and props instead of standing alone, `useCallback` dependency chains exist only to simulate closure stability, and tests need `renderHook` for what could be plain unit tests.
- Rolling a bespoke data-fetching layer without a clear need.
- No error boundaries, empty catch blocks, and missing loading/error states.
- Default object/array/function values that accidentally break memoization.
</category>
</red_flags>

<report_template>
Use this shape for the final audit:

**React red-flags audit**

**Summary**
- Overall risk: High | Medium | Low
- Main theme: <one sentence>
- Best first fix: <one concrete action>

**Findings**

**1. <Severity>: <red flag name>**
- Evidence: `<file:path>` — <specific observed pattern>
- Why it matters: <maintenance, correctness, performance, or testability impact>
- Smallest safe next step: <action>
- Verification: <test, lint, build, or runtime check>

**Notable non-findings**
- <Areas checked that looked healthy, when useful>
</report_template>

<anti_patterns>
- Do not report a red flag from grep alone. Inspect representative code first.
- Do not recommend memoization everywhere. Memoize when identity affects child renders, context values, expensive calculations, or dependency stability.
- Do not split files by line count alone. Split when a named responsibility or seam becomes clearer.
- Do not replace every dependency with handwritten code. Keep libraries that encode hard domain behavior, accessibility, security, dates, localization, data fetching, or complex browser edge cases.
- Do not shame legacy code. Frame findings as risk, evidence, and next safe move.
</anti_patterns>

<success_criteria>
A successful review:
- Identifies React red flags with file-backed evidence.
- Separates systemic problems from isolated exceptions.
- Prioritizes findings by risk and change leverage.
- Recommends incremental fixes that a team can safely execute.
- Calls out verification steps before claiming an issue is fixed.
</success_criteria>

<sources>
Inspired by "29 React Codebase Red Flags from a Senior Frontend Developer" by FrontendJoy, plus common React, TypeScript, and frontend architecture review practice.
</sources>
