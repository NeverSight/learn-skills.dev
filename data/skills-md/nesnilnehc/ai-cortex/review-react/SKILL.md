---
name: review-react
description: Review React code for component design, hooks correctness, state management, rendering performance, and accessibility. Framework-only atomic skill; output is a findings list.
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code, review-typescript]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review react]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review React

## Purpose

Review **React** code for **framework conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on functional component design, hooks correctness, state management (local and external), rendering performance, side effects and data fetching, routing and code splitting, and accessibility.

---

## Core Objective

**Primary Goal**: Produce a React framework findings list covering component design, hooks correctness, state management, rendering performance, side effects, routing/code splitting, and accessibility for the given code scope.

**Success Criteria** (ALL must be met):

1. ✅ **React framework-only scope**: Only React framework conventions are reviewed; no scope selection, security, or architecture analysis performed
2. ✅ **All seven React dimensions covered**: Component design, hooks correctness, state management, rendering performance, side effects/data fetching, routing/code splitting, and accessibility are assessed where relevant
3. ✅ **Findings format compliant**: Each finding includes Location, Category (`framework-react`), Severity, Title, Description, and optional Suggestion
4. ✅ **Component/file references**: All findings reference specific file:line or component name
5. ✅ **Non-React code excluded**: Non-React files are not analyzed for React-specific rules unless explicitly in scope

**Acceptance Test**: Does the output contain a React-focused findings list with component/file references covering all relevant framework dimensions without performing security, architecture, or scope analysis?

---

## Scope Boundaries

**This skill handles**:

- Functional component design (single responsibility, composition patterns, prop types/defaults, children patterns)
- Hooks correctness (dependency arrays, stale closures, custom hooks extraction, rules of hooks, cleanup in useEffect)
- State management (local vs global state, context usage, reducer patterns, external stores like Zustand/Redux, server state with TanStack Query/SWR)
- Rendering performance (memo/useMemo/useCallback usage, key stability in lists, avoiding unnecessary re-renders, virtualization for large lists)
- Side effects and data fetching (useEffect patterns, race conditions, abort controllers, loading/error states, data fetching libraries)
- Routing and code splitting (React.lazy, Suspense boundaries, route-based splitting, error boundaries)
- Accessibility (ARIA attributes, semantic HTML, keyboard navigation, focus management, screen reader support)

**This skill does NOT handle**:

- Scope selection — scope is provided by the caller
- Security analysis (XSS, injection risks) — use `review-security`
- Architecture analysis — use `review-architecture`
- Language/runtime (JavaScript/TypeScript) conventions — use `review-typescript` or general JS/TS analysis
- Full orchestrated review — use `review-code`

**Handoff point**: When all React findings are emitted, hand off to `review-code` for aggregation. For XSS risks (dangerouslySetInnerHTML misuse, unsanitized content), note them and suggest `review-security`.

---

## Use Cases

- **Orchestrated review**: Used as the framework step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive for React projects.
- **React-only review**: When the user wants only React/frontend framework conventions checked.
- **Pre-PR React checklist**: Ensure hooks usage, component design, and state management patterns are correct.

**When to use**: When the code under review is React and the task includes framework quality. Scope is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: React framework conventions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, security review, or architecture review; do not review non-React files for React rules unless in scope (e.g. mixed repo).

### Review checklist (React framework only)

1. **Component design**: Prefer functional components; single responsibility per component; composition over deep nesting; explicit prop types (TypeScript interfaces or PropTypes) with sensible defaults; use children and render props appropriately.
2. **Hooks correctness**: Correct dependency arrays in useEffect/useMemo/useCallback; avoid stale closures; extract reusable logic into custom hooks; follow rules of hooks (top-level only, React functions only); cleanup functions in useEffect for subscriptions and timers.
3. **State management**: Choose local state (useState) vs global state appropriately; use Context for cross-cutting concerns without overuse; prefer useReducer for complex state transitions; integrate external stores (Zustand, Redux Toolkit) correctly; separate server state (TanStack Query, SWR) from client state.
4. **Rendering performance**: Apply React.memo, useMemo, useCallback where measurably beneficial; stable keys in lists (no index-as-key for dynamic lists); avoid creating objects/functions inline in JSX when it causes re-renders; use virtualization (react-window, react-virtuoso) for large lists.
5. **Side effects and data fetching**: Correct useEffect patterns (single-purpose effects, proper cleanup); handle race conditions with abort controllers or flags; represent loading/error/success states explicitly; prefer data fetching libraries (TanStack Query, SWR) over raw useEffect + fetch.
6. **Routing and code splitting**: Use React.lazy with Suspense for route-based code splitting; define error boundaries for lazy-loaded routes; keep route definitions declarative; avoid loading full modules eagerly when lazy loading is appropriate.
7. **Accessibility**: Use semantic HTML elements; apply ARIA attributes correctly (roles, labels, live regions); ensure keyboard navigation and focus management; support screen readers; test interactive components for accessibility compliance.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line or component name). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) containing React code (.tsx, .jsx, .ts, .js with React APIs). Provided by the user or scope skill.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **framework-react**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, security, or architecture review. Stay within React framework conventions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** review non-React code for React-specific rules unless explicitly in scope.

### Skill Boundaries

**Do NOT do these** (other skills handle them):

- Do NOT select or define the code scope — scope is determined by the caller or `review-code`
- Do NOT perform security analysis (XSS, injection) — use `review-security`
- Do NOT perform architecture analysis — use `review-architecture`

**When to stop and hand off**:

- When all React findings are emitted, hand off to `review-code` for aggregation
- When XSS risks are found (e.g. unsafe `dangerouslySetInnerHTML` usage), note them and suggest `review-security`
- When the user needs a full review (scope + language + cognitive), redirect to `review-code`

---

## Self-Check

### Core Success Criteria

- [ ] **React framework-only scope**: Only React framework conventions are reviewed; no scope selection, security, or architecture analysis performed
- [ ] **All seven React dimensions covered**: Component design, hooks correctness, state management, rendering performance, side effects/data fetching, routing/code splitting, and accessibility are assessed where relevant
- [ ] **Findings format compliant**: Each finding includes Location, Category (`framework-react`), Severity, Title, Description, and optional Suggestion
- [ ] **Component/file references**: All findings reference specific file:line or component name
- [ ] **Non-React code excluded**: Non-React files are not analyzed for React-specific rules unless explicitly in scope

### Process Quality Checks

- [ ] Was only the React framework dimension reviewed (no scope/security/architecture)?
- [ ] Are component design, hooks, state, performance, side effects, routing, and accessibility covered where relevant?
- [ ] Is each finding emitted with Location, Category=framework-react, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line or component?

### Acceptance Test

Does the output contain a React-focused findings list with component/file references covering all relevant framework dimensions without performing security, architecture, or scope analysis?

---

## Examples

### Example 1: Missing cleanup in useEffect

- **Input**: Component that sets up a WebSocket connection in useEffect without a cleanup function.
- **Expected**: Emit a finding (major) for missing cleanup; suggest returning a cleanup function that closes the connection. Category = framework-react.

### Example 2: Index as key in dynamic list

- **Input**: Component rendering a sortable/filterable list using array index as key.
- **Expected**: Emit finding for key instability and potential state bugs; suggest using a stable unique identifier as key. Category = framework-react.

### Edge case: Class component in modern codebase

- **Input**: Legacy class component in a codebase that otherwise uses functional components and hooks.
- **Expected**: Emit a suggestion to migrate to functional component with hooks where feasible; review the class component for lifecycle correctness (componentDidMount, componentWillUnmount cleanup). Note that migration is recommended but not always required for stable, well-tested components.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/Component.tsx` or `.jsx` (optional line or range). |
| **Category** | `framework-react`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `src/components/UserList.tsx:42`
- **Category**: framework-react
- **Severity**: major
- **Title**: useEffect missing cleanup for subscription
- **Description**: The WebSocket subscription in useEffect is never closed, causing memory leaks when the component unmounts.
- **Suggestion**: Return a cleanup function from useEffect that calls `socket.close()`.
```
