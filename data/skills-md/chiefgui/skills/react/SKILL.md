---
name: react
description: React architecture & best practices.
---

# React

- Follow the project's React and framework conventions.
- Keep ownership explicit and data flow predictable.

## Components

- Split components around coherent responsibilities, not line counts.
- Keep related rendering and behavior together.
- Hide substantial behavior behind small APIs that minimize caller coordination.
- Prefer composition over accumulating boolean mode props.
- Keep feature-specific knowledge out of shared UI components.
- Define components outside other components to preserve identity.

## Compound components

- Use compound APIs sparingly, when meaningful UI parts need flexible composition.
- Prefer ordinary props and children when they express the required variation clearly.
- Expose meaningful UI parts, not every internal element.
- Keep coordination inside the component family, including when state is externally controlled.
- Scope internal context to each root instance.
- Avoid inspecting or cloning children to coordinate behavior.

## State

- Keep state close to its consumers; lift it only as far as shared ownership requires.
- Derive values during rendering instead of storing redundant state.
- Avoid copying props into state unless an independent draft is intentional.
- Distinguish local UI state, URL state, and server state; respect each source of truth.
- Use context for a coherent shared scope, not as a catch-all store.
- Group related transitions when independent updates allow invalid states.
- Use stable keys that represent identity; reset state deliberately when identity changes.

## Effects

- Keep rendering pure.
- Use effects to synchronize with external systems; handle user actions in event handlers.
- Avoid effect chains that calculate or coordinate application state.
- Include reactive dependencies; restructure the code instead of suppressing dependency checks.
- Clean up external resources when dependencies change or components unmount.
- Prevent stale asynchronous results from replacing current data.

## Hooks and logic

- Extract hooks around coherent capabilities, not merely to shorten components.
- Keep logic in plain functions when it does not need React.
- Avoid lifecycle wrappers that hide effect dependencies.
- Treat custom hooks as reusable logic; separate calls do not share state unless they access a shared source.

## Data boundaries

- Use the project's existing loading, caching, and mutation mechanisms.
- Keep transport details from spreading through rendering code.
- Represent loading, empty, error, and success states explicitly.
- Keep server-only dependencies outside client boundaries.
