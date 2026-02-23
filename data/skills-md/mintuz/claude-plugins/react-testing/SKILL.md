---
name: react-testing
description: WHEN testing React components/hooks/context with React Testing Library; NOT e2e; covers renderHook, providers, forms, and anti-patterns.
---

# React Testing Library

This skill focuses on React-specific testing patterns. For general DOM testing patterns (queries, userEvent, async, accessibility), load the `frontend-testing` skill. For TDD workflow, load the `tdd` skill.

## Core Principles

**React components are functions** - Test them like functions: inputs (props) → output (rendered DOM).

**Test behavior, not implementation:**

- ✅ Test what users see and do
- ✅ Test through public APIs (props, rendered output)
- ❌ Don't test component state
- ❌ Don't test component methods
- ❌ Don't use shallow rendering

**Modern RTL handles cleanup automatically:**

- No manual `act()` for render, userEvent, or async queries
- No manual `cleanup()` - it's automatic
- Use factory functions instead of `beforeEach`

## Quick Reference

| Topic                                                | Guide                                           |
| ---------------------------------------------------- | ----------------------------------------------- |
| Testing components, props, and conditional rendering | [components.md](references/components.md)       |
| Testing custom hooks with renderHook                 | [hooks.md](references/hooks.md)                 |
| Testing context providers and consumers              | [context.md](references/context.md)             |
| Testing form inputs, submissions, and validation     | [forms.md](references/forms.md)                 |
| Common React testing mistakes to avoid               | [anti-patterns.md](references/anti-patterns.md) |
| Loading states, error boundaries, portals, Suspense  | [advanced.md](references/advanced.md)           |

## When to Use Each Guide

### Components

Use [components.md](references/components.md) when you need:

- Basic component testing patterns
- Testing how props affect rendered output
- Testing conditional rendering
- Examples of correct vs incorrect component tests

### Hooks

Use [hooks.md](references/hooks.md) when you need:

- Testing custom hooks with `renderHook`
- Using `result.current`, `act()`, and `rerender()`
- Testing hooks with props

### Context

Use [context.md](references/context.md) when you need:

- Using the `wrapper` option with providers
- Setting up multiple providers
- Creating custom render functions for context
- Testing components that consume context

### Forms

Use [forms.md](references/forms.md) when you need:

- Testing controlled inputs
- Testing form submissions
- Testing form validation
- User interaction patterns with forms

### Anti-Patterns

Use [anti-patterns.md](references/anti-patterns.md) when you need:

- When to avoid manual `act()` wrapping
- Why manual `cleanup()` is unnecessary
- Avoiding `beforeEach` render patterns
- Why to avoid testing component internals
- Why shallow rendering is problematic

### Advanced

Use [advanced.md](references/advanced.md) when you need:

- Testing loading states
- Testing error boundaries
- Testing portals
- Testing React Suspense

## Summary Checklist

React-specific checks:

- [ ] Using `render()` from @testing-library/react (not enzyme's shallow/mount)
- [ ] Using `renderHook()` for custom hooks
- [ ] Using `wrapper` option for context providers
- [ ] No manual `act()` calls (RTL handles it)
- [ ] No manual `cleanup()` calls (automatic)
- [ ] Testing component output, not internal state
- [ ] Using factory functions, not `beforeEach` render
- [ ] Following TDD workflow (see `tdd` skill)
- [ ] Using general DOM testing patterns (see `frontend-testing` skill)
