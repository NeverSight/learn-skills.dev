---
name: composition-patterns
description: React composition patterns that scale. Use when refactoring components with boolean prop proliferation, building flexible component libraries, or designing reusable APIs. Triggers on tasks involving compound components, render props, context providers, or component architecture. Includes React 19 API changes.
---

# React Composition Patterns

Composition patterns for building flexible, maintainable React components. Avoid
boolean prop proliferation by using compound components, lifting state, and
composing internals. These patterns make codebases easier for both humans and AI
agents to work with as they scale.

## When NOT to Use

Skip these patterns when: fewer than 3 props, simple variants, or single-use components.

## When to Apply

Reference these guidelines when:

- Refactoring components with many boolean props
- Building reusable component libraries
- Designing flexible component APIs
- Reviewing component architecture
- Working with compound components or context providers

## Rule Categories by Priority

| Priority | Category                | Impact | Prefix          |
| -------- | ----------------------- | ------ | --------------- |
| 1        | Component Architecture  | HIGH   | `architecture-` |
| 2        | State Management        | MEDIUM | `state-`        |
| 3        | Implementation Patterns | MEDIUM | `patterns-`     |
| 4        | React 19 APIs           | MEDIUM | `react19-`      |

## Quick Reference

### 1. Component Architecture (HIGH)

- **Avoid boolean props** — Don't add boolean props like `isThread`, `isEditing`, `isDMThread` to customize behavior. Each boolean doubles possible states. Use composition instead — see [references/architecture-avoid-boolean-props.md](references/architecture-avoid-boolean-props.md)
- **Compound components** — Structure complex components with shared context so each subcomponent accesses state via context, not props — see [references/architecture-compound-components.md](references/architecture-compound-components.md)

### 2. State Management (MEDIUM)

- **Decouple implementation** — Provider is the only place that knows how state is managed — see [references/state-decouple-implementation.md](references/state-decouple-implementation.md)
- **Context interface** — Define generic interface with `state`, `actions`, `meta` for dependency injection — see [references/state-context-interface.md](references/state-context-interface.md)
- **Lift state** — Move state into provider components for sibling access — see [references/state-lift-state.md](references/state-lift-state.md)

### 3. Implementation Patterns (MEDIUM)

- **Explicit variants** — Create explicit variant components instead of boolean modes — see [references/patterns-explicit-variants.md](references/patterns-explicit-variants.md)
- **Children over render props** — Use `children` for composition instead of `renderX` props — see [references/patterns-children-over-render-props.md](references/patterns-children-over-render-props.md)

### 4. React 19 APIs (MEDIUM)

> **React 19+ only.** Skip this section if using React 18 or earlier.

- **No forwardRef** — Don't use `forwardRef`; pass `ref` as a regular prop. Use `use()` instead of `useContext()` — see [references/react19-no-forwardref.md](references/react19-no-forwardref.md)
