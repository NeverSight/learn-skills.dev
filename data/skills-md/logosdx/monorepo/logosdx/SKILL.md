---
name: logosdx
description: Implements LogosDX patterns for DOM manipulation, HTTP clients, lifecycle hooks, events, state machines, storage adapters, and React context hooks. Use when tasks involve @logosdx libraries or HookEngine/FetchEngine/ObserverEngine/StateMachine/StorageAdapter code.
metadata:
  references: dom, fetch, hooks, observer, state-machine, storage, react, utils
---

# LogosDX Skill

Use this skill for LogosDX setup and integration. Read only the reference file(s) needed for the task.

## Quick Start

1. Identify package scope (`dom`, `fetch`, `hooks`, `observer`, `state-machine`, `storage`, `react`, `utils`).
2. Open the matching file from `references/`.
3. Implement with strict typing and lifecycle cleanup.
4. Run project checks (typecheck/tests) before finishing.

## Critical Rules

- Define type shapes first (`headers`, `params`, `state`, `events`, storage schema).
- Prefer package-native error flows (`attempt`, `attemptSync`, `isFetchError`).
- Always clean up resources (`cleanup()`, `off()`, `destroy()`).
- Keep React hook methods at component top level only.

## Reference Map

- DOM manipulation, CSS, attributes, events, behaviors, viewport: `references/dom.md`
- Lifecycle hooks, middleware, plugins, priority chains: `references/hooks.md`
- HTTP client, retry/cache/dedupe/rate-limit, lifecycle events: `references/fetch.md`
- Typed events, async generators, queues, observation: `references/observer.md`
- Finite state machines, guards, invoke, StateHub coordination: `references/state-machine.md`
- Storage CRUD, key wrappers, events, custom adapters: `references/storage.md`
- React factories, hooks, provider composition: `references/react.md`
- Error tuples, flow control, memoization, typed helpers: `references/utils.md`
- Cross-file index and routing: `references/REFERENCE.md`

## Task Routing

- DOM manipulation, CSS, events, behaviors, viewport tasks -> `references/dom.md`
- Hook/middleware/plugin tasks -> `references/hooks.md`
- API tasks -> `references/fetch.md`
- Event/queue tasks -> `references/observer.md`
- State machine/FSM tasks -> `references/state-machine.md`
- Persistence tasks -> `references/storage.md`
- React integration tasks -> `references/react.md`
- Error handling and shared utility patterns -> `references/utils.md`
- Cross-package design -> `references/REFERENCE.md` then package-specific files
