---
name: xstate-v5
description: Implement, refactor, and review XState v5 state machines (TypeScript and React) using a strict setup().createMachine() ruleset, params-first typing, canonical actor/spawn patterns, and createActorContext() patterns from @xstate/react. Includes guidance for planning/designing statecharts before implementation.
metadata:
  short-description: Strict XState v5 ruleset + design-first planning
---

# xstate-v5 (Strict) Skill

Build, refactor, and review **XState v5** state machines (TypeScript and React) using a strict, strongly-typed ruleset.

**Source of truth:** `references/xstate-v5-rules.md` (this repo, resolved from the skill root). If anything in this skill conflicts with the rules file, follow the rules file.

## Inlined Non-Negotiable Contract (Agent Must Follow)

These requirements are intentionally duplicated here so an agent can comply without first loading external references:

- Design first, code second:
  - Produce planning artifacts before implementation (state inventory, event catalog, transition table, async/actor map, acceptance-test scenarios).
  - Include a boundary/decomposition decision record (what is split vs orchestrated, and why).
- No god-machine architecture:
  - Unrelated domains (auth, toasts, navigation, workflows, transport/retry policy) must not be fully modeled in one machine.
  - A single machine is acceptable only as a thin orchestration root or tightly coupled app-shell parallel regions.
- No state-mirroring context flags:
  - Do not duplicate mode in context booleans (`isLoading`, `isAuthenticated`, etc.) when `state.value` already represents the mode.
  - If a temporary migration flag exists, document rationale and removal plan.
- XState v5 strictness:
  - Use `setup({...}).createMachine({...})`.
  - Implement `actions`/`guards`/`actors` in `setup(...)`.
  - Send event objects only.
  - Avoid forbidden v4 patterns (`interpret`, `Machine`, `cond`, `send`, `pure`, `choose`, etc.).
- Enforce explicit async and actor boundaries:
  - Request/response: `invoke` with `onDone` and `onError`.
  - Long-lived collaborators: `spawnChild`/`stopChild` and explicit routing via `sendTo`.

Fail-closed rule:
- If any detail is ambiguous, load `references/xstate-v5-rules.md` before writing or reviewing machine code.
- If that file is missing/unreadable, stop and report the issue instead of guessing.

## When To Use

Use this skill when the task involves:

- XState v5 machines/actors (`xstate`, `@xstate/react`)
- Refactoring XState code to be more type-safe and idiomatic v5
- Migrating XState v4 patterns (Machine/interpret/cond/send/pure/choose/etc.) to v5 equivalents
- Planning/designing statecharts prior to implementing them as XState v5 machines
- Designing actor boundaries (invoke vs spawnChild) and React integration via `createActorContext`

## Hard Requirements (Enforced)

- Prefer `setup({...}).createMachine({...})` for all machines.
- Implement **all** `actions`, `guards`, and `actors` in the `setup({...})` object.
- Prefer passing event-derived data via typed `params` to actions/guards.
- Never send string events. Always send event objects: `actor.send({ type: '...' })`.
- Forbid XState v4 legacy APIs and patterns listed in `references/xstate-v5-rules.md`.
- Do not model unrelated domains (auth, notifications/toasts, navigation, data lifecycle, etc.) inside one machine, except a thin orchestration machine.
- Do not mirror state in context booleans (`isLoading`, `isAuthenticated`, etc.) when `state.value` already represents that mode.

## Rules Table Of Contents

- Statechart Design: [0 Statechart Design (Before You Code)](references/xstate-v5-rules.md#0-statechart-design-before-you-code)
- Core Principles: [1 Machine Creation Pattern](references/xstate-v5-rules.md#1-machine-creation-pattern), [2 Type Safety First](references/xstate-v5-rules.md#2-type-safety-first)
- Setup Object Rules: [3 Implementation Placement](references/xstate-v5-rules.md#3-implementation-placement), [4 Parameter Typing](references/xstate-v5-rules.md#4-parameter-typing)
- Event Handling Rules: [5 Event Type Safety with assertEvent](references/xstate-v5-rules.md#5-event-type-safety-with-assertevent), [6 Event Object Requirement](references/xstate-v5-rules.md#6-event-object-requirement)
- Deprecated Pattern Prevention: [7 Forbidden v4 Patterns](references/xstate-v5-rules.md#7-forbidden-v4-patterns), [8 Modern v5 Equivalents](references/xstate-v5-rules.md#8-modern-v5-equivalents)
- Context and Input Rules: [9 Context Initialization](references/xstate-v5-rules.md#9-context-initialization), [10 Context Updates](references/xstate-v5-rules.md#10-context-updates)
- Invoke and Actor Rules: [11 Invoke Configuration](references/xstate-v5-rules.md#11-invoke-configuration), [12 Actor Spawning](references/xstate-v5-rules.md#12-actor-spawning)
- Type Helper Rules: [13 Type Helpers](references/xstate-v5-rules.md#13-type-helpers)
- Testing Rules: [14 Type-Safe Testing](references/xstate-v5-rules.md#14-type-safe-testing) ([14.1 Deterministic Actor Tests](references/xstate-v5-rules.md#141-deterministic-actor-tests), [14.2 Model-Based Testing](references/xstate-v5-rules.md#142-model-based-testing-with-xstategraph), [14.3 Graph Utilities](references/xstate-v5-rules.md#143-graph-utilities))
- XState React Rules: [15 Shared State via createActorContext](references/xstate-v5-rules.md#15-shared-state-via-createactorcontext)
- Best Practices Summary: [16 Code Organization](references/xstate-v5-rules.md#16-code-organization), [17 Performance Considerations](references/xstate-v5-rules.md#17-performance-considerations), [18 Error Handling](references/xstate-v5-rules.md#18-error-handling), [19 Documentation](references/xstate-v5-rules.md#19-documentation)
- Enforcement Rules for AI Agents: [20 Mandatory Patterns](references/xstate-v5-rules.md#20-mandatory-patterns), [21 Quality Assurance](references/xstate-v5-rules.md#21-quality-assurance), [22 When Docs Are Ambiguous](references/xstate-v5-rules.md#22-when-docs-are-ambiguous)

## Quick Start

Minimal typed machine skeleton:

```ts
import { setup, assign } from "xstate"

type Ctx = { count: number }

type Ev = { type: "inc" } | { type: "add"; amount: number } | { type: "reset" }

type Input = { initialCount?: number }

export const counterMachine = setup({
  types: {
    context: {} as Ctx,
    events: {} as Ev,
    input: {} as Input,
  },
  actions: {
    inc: assign({ count: ({ context }) => context.count + 1 }),
    add: assign({
      count: ({ context }, params: { amount: number }) => context.count + params.amount,
    }),
    reset: assign({ count: ({ input }) => input.initialCount ?? 0 }),
  },
}).createMachine({
  id: "counter",
  context: ({ input }) => ({ count: input.initialCount ?? 0 }),
  on: {
    inc: { actions: "inc" },
    add: {
      actions: {
        type: "add",
        params: ({ event }) => ({ amount: event.amount }),
      },
    },
    reset: { actions: "reset" },
  },
})
```

React shared state skeleton:

```ts
import { createActorContext, shallowEqual } from "@xstate/react"
import { type SnapshotFrom } from "xstate"
import { counterMachine } from "./counterMachine"

const CounterCtx = createActorContext(counterMachine)

export const CounterProvider = CounterCtx.Provider
export const useCounterSelector = CounterCtx.useSelector
export const useCounterActorRef = CounterCtx.useActorRef

const selectCount = (s: SnapshotFrom<typeof counterMachine>) => s.context.count
export const useCount = () => useCounterSelector(selectCount)

const selectCtx = (s: SnapshotFrom<typeof counterMachine>) => s.context
export const useCounterContext = () => useCounterSelector(selectCtx, shallowEqual)
```

## Workflow (What To Do Each Time)

1. Read `references/xstate-v5-rules.md` first.
2. Identify the target surface area:
   - Plain machine/actor (non-React)
   - React integration (`createActorContext`) or local `useActor`
   - Migration from v4 patterns
3. Design the statechart first:
   - See `references/xstate-v5-rules.md#0-statechart-design-before-you-code`.
   - Write down: state inventory, event catalog (payload + source), transition table, async/actor boundaries, and acceptance-test scenarios.
   - Record a boundary/decomposition decision before type design:
     - Which concerns belong in separate actors/machines (based on lifecycle, owner, and failure mode).
     - Which concerns are intentionally orchestrated at top-level (and why).
     - Any exception note if keeping logic in one machine.
   - Default: do this unless the user explicitly asks to skip planning.
4. Design types first:
   - `types.context`, `types.events`, and `types.input` (and `types.output` if applicable)
   - Use `zod` schemas only if the codebase already uses Zod or the user asks for it.
5. Put implementations in `setup({ actions, guards, actors })`:
   - Actions/guards take typed `params` when they need event-derived data.
   - Only read event-specific fields inside implementations when necessary; use `assertEvent` then.
6. Choose async boundaries:
   - Prefer `invoke` with typed `input` for request/response flows.
   - Use `spawnChild`/`stopChild` for long-lived child actors.
7. Use v5 runtime APIs:
   - `createActor(machine)` (not `interpret`)
   - `raise` / `sendTo` (not `send` action)
   - `enqueueActions` (not `pure`/`choose`)
8. Validate:
   - `tsc` passes; no `any` leaks in params.
   - No string event sends.
   - No v4 forbidden imports or config keys (`cond`, `withContext`, `withConfig`, etc.).
   - Prefer `waitFor` for async actor tests and `xstate/graph` (`createTestModel`, `getShortestPaths`, etc.) for model/graph-driven test generation.

## When A Monolith Is Acceptable

Use a single top-level machine only when it is a thin orchestration root that coordinates child actors or tightly coupled parallel app-shell concerns. Even then, unrelated domain logic should live in separate actors/machines and communicate via explicit events.

## Review Checklist (Use When Auditing PRs)

- All machines are `setup(...).createMachine(...)`.
- Machine has a clear statechart plan (states/events/transition table) or the PR description includes it.
- No domain-smell: one machine has one responsibility or explicit orchestration scope.
- No state-mirroring context flags without documented rationale.
- No implementations inside `types`.
- `actions`/`guards` read event fields only via `params` or `assertEvent`.
- No `interpret`, `Machine`, `withConfig`, `withContext`, `cond`, `send`, `pure`, `choose`.
- `invoke` has `onError` (and `onDone` when appropriate).
- React usage prefers `createActorContext` at module scope; selectors are stable and use `shallowEqual` for objects.

## Common Fixes

- Event payload used inside an action:
  - Prefer: compute payload in `params` and make the action implementation depend on `params`.
  - Otherwise: add `assertEvent(event, 'someType')` inside the implementation.

- v4 `cond`:
  - Rename to `guard` and move guard implementation into `setup({ guards: { ... } })`.

- v4 `interpret`:
  - Replace with `createActor(machine)` and `.start()` where needed.

## Notes

If official docs feel ambiguous, follow the rules file guidance: confirm behavior against XState v5 source, issues/discussions, or a minimal reproduction/type-test rather than guessing.
