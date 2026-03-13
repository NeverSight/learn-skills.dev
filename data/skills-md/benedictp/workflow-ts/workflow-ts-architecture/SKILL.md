---
name: workflow-ts-architecture
description: Build and review TypeScript feature logic with workflow-ts (`@workflow-ts/core` and `@workflow-ts/react`) using explicit state machines, typed renderings, workers, composition, and runtime-first tests. Use when requests involve creating or refactoring workflows, wiring React hooks, modeling async worker flows, composing parent/child workflows, adding snapshots/interceptors/devtools, or writing tests for workflow behavior in this repository.
---

# Workflow-ts Architecture

## Goal

Build deterministic application flows in this repository with workflow-ts primitives and documented project conventions.

## Quick start

1. Add `@workflow-ts/core` for workflow runtime logic.
2. Add `@workflow-ts/react` when a React screen should subscribe to rendering.
3. Model `State` and `Rendering` as explicit discriminated unions.
4. Keep actions pure and route side effects through workers.
5. Validate behavior with runtime-level tests before UI tests.

## Canonical references

Read [references/doc-map.md](./references/doc-map.md) first, then load only the specific guide needed for the task.

## How to build a basic workflow

Use this template and customize:

```ts
import { createWorker, type Worker, type Workflow } from '@workflow-ts/core';

interface Props {
  userId: string;
}

type State =
  | { type: 'loading' }
  | { type: 'loaded'; name: string }
  | { type: 'error'; message: string };

type Output = { type: 'closed' };

type Rendering =
  | { type: 'loading'; close: () => void }
  | { type: 'loaded'; name: string; reload: () => void; close: () => void }
  | { type: 'error'; message: string; retry: () => void; close: () => void };

type LoadResult = { ok: true; name: string } | { ok: false; message: string };

interface WorkerProvider {
  loadProfileWorker: () => Worker<LoadResult>;
}

const defaultWorkerProvider: WorkerProvider = {
  loadProfileWorker: () =>
    createWorker<LoadResult>('load-profile', async (signal) => {
      // Cooperate with cancellation via AbortSignal.
      if (signal.aborted) return { ok: false, message: 'Cancelled' };
      return { ok: true as const, name: 'Ada' };
    }),
};

export function createProfileWorkflow(
  workerProvider: WorkerProvider,
): Workflow<Props, State, Output, Rendering> {
  return {
    initialState: () => ({ type: 'loading' }),

    render: (_props, state, ctx) => {
      switch (state.type) {
        case 'loading':
          ctx.runWorker(workerProvider.loadProfileWorker(), 'profile-load', (result) => () => ({
            state: result.ok
              ? { type: 'loaded', name: result.name }
              : { type: 'error', message: result.message },
          }));
          return {
            type: 'loading',
            close: () => ctx.actionSink.send((s) => ({ state: s, output: { type: 'closed' } })),
          };
        case 'loaded':
          return {
            type: 'loaded',
            name: state.name,
            reload: () => ctx.actionSink.send(() => ({ state: { type: 'loading' } })),
            close: () => ctx.actionSink.send((s) => ({ state: s, output: { type: 'closed' } })),
          };
        case 'error':
          return {
            type: 'error',
            message: state.message,
            retry: () => ctx.actionSink.send(() => ({ state: { type: 'loading' } })),
            close: () => ctx.actionSink.send((s) => ({ state: s, output: { type: 'closed' } })),
          };
      }
    },
  };
}

export const profileWorkflow = createProfileWorkflow(defaultWorkerProvider);
```

- `DO` keep state transitions explicit with discriminated unions.
- `DO` model expected business failures as output data from workers.
- `DO` inject workers via a `WorkerProvider` interface for deterministic tests.
- `DO NOT` mutate state; always return new state.
- `DO NOT` rely on thrown worker errors for domain transitions.

## How to integrate with React

Use `useWorkflow` as a single subscription point and map renderings to components:

```tsx
import { useWorkflow } from '@workflow-ts/react';
import type { JSX } from 'react';

export function ProfileScreen({ userId }: { userId: string }): JSX.Element {
  const rendering = useWorkflow(profileWorkflow, { userId });

  switch (rendering.type) {
    case 'loading':
      return <button onClick={rendering.close}>Close</button>;
    case 'loaded':
      return (
        <>
          <h1>{rendering.name}</h1>
          <button onClick={rendering.reload}>Reload</button>
          <button onClick={rendering.close}>Close</button>
        </>
      );
    case 'error':
      return (
        <>
          <p>{rendering.message}</p>
          <button onClick={rendering.retry}>Retry</button>
          <button onClick={rendering.close}>Close</button>
        </>
      );
  }
}
```

- `DO` keep `props` small and immutable.
- `DO` pass only minimal derived inputs to `useWorkflow`.
- `DO NOT` use workflow-ts as a selector-based global store by default.
- `DO NOT` call `updateProps` with identical references to force refreshes.

## How to compose child workflows

Use stable keys and explicit output mapping:

```ts
const childRendering = ctx.renderChild(childWorkflow, childProps, 'child-key', (childOutput) => (state) => ({
  state: handleChildOutput(state, childOutput),
}));
```

- `DO` use stable child keys for long-lived child state.
- `DO` map child output into parent actions/state transitions.
- `DO NOT` change keys unless creating a new child instance intentionally.

## How to run worker-based async flows

Run workers only from `render`, key them by logical effect identity, and inject workers through a provider interface for testability.
Inside `render`, structure logic as:
- optional pre-`switch` worker startup only when it must run regardless of state
- `switch (state.type)` as the main rendering/state-handling structure

```ts
import type { RenderContext, Worker } from '@workflow-ts/core';

interface WorkerProvider {
  loadProfileWorker: () => Worker<LoadResult>;
}

function render(_props: Props, state: State, ctx: RenderContext<State, Output>): Rendering {
  // Pre-switch work is only for workers that must run regardless of state.
  // ctx.runWorker(workerProvider.auditWorker(), 'audit', () => (s) => ({ state: s }));

  switch (state.type) {
    case 'loading':
      ctx.runWorker(workerProvider.loadProfileWorker(), 'profile-load', (result) => () => ({
        state: result.ok
          ? { type: 'loaded', name: result.name }
          : { type: 'error', message: result.message },
      }));
      return {
        type: 'loading',
        close: () => ctx.actionSink.send((s) => ({ state: s, output: { type: 'closed' } })),
      };
    case 'loaded':
      return {
        type: 'loaded',
        name: state.name,
        reload: () => ctx.actionSink.send(() => ({ state: { type: 'loading' } })),
        close: () => ctx.actionSink.send((s) => ({ state: s, output: { type: 'closed' } })),
      };
    case 'error':
      return {
        type: 'error',
        message: state.message,
        retry: () => ctx.actionSink.send(() => ({ state: { type: 'loading' } })),
        close: () => ctx.actionSink.send((s) => ({ state: s, output: { type: 'closed' } })),
      };
  }
}
```

- Same key + running worker keeps the worker alive and updates handlers.
- Missing key in the next render cancels the worker at end of render cycle.
- Disposing runtime cancels all active workers.
- `DO` define worker dependencies behind a `WorkerProvider` interface and inject it into workflow factories.
- `DO` keep `render` primarily as `switch (state.type)` branches for clarity and exhaustiveness.
- `DO NOT` place general branching/return logic before the `switch`; reserve pre-`switch` code for unconditional worker startup only.

## How to write tests first

Prefer runtime-level tests in `@workflow-ts/core` for behavior:

```ts
import { createRuntime } from '@workflow-ts/core';
import { expect, it } from 'vitest';

it('transitions loading -> loaded', () => {
  const runtime = createRuntime(profileWorkflow, { userId: 'u1' });

  expect(runtime.getRendering().type).toBe('loading');
  runtime.send(() => ({ state: { type: 'loaded', name: 'Ada' } }));
  expect(runtime.getRendering().type).toBe('loaded');

  runtime.dispose();
});
```

- Prefer provider-based worker stubs for deterministic retry/failure tests:

```ts
import { createWorker } from '@workflow-ts/core';
import { vi } from 'vitest';

const workerProvider: WorkerProvider = {
  loadProfileWorker: vi
    .fn()
    .mockReturnValueOnce(createWorker('load-profile-fail', async () => ({ ok: false, message: 'TEST' })))
    .mockReturnValueOnce(createWorker('load-profile-ok', async () => ({ ok: true, name: 'Ada' }))),
};
```

- `DO` test initial state/rendering, callbacks, outputs, props updates, and worker behavior.
- `DO` dispose runtime in every test.
- `DO` test worker cancellation and retry paths deterministically.
- `DO` use `WorkerProvider` to stub sequential worker outcomes (for example fail then success on retry).
- `DO NOT` rely on timing sleeps when a deferred completion pattern can be used.

## How to persist and restore snapshots

Define `snapshot` and hydrate via `initialState(props, snapshot)`:

```ts
const runtime = createRuntime(workflow, props, { snapshot: savedSnapshot });
const nextSnapshot = runtime.snapshot();
```

Call `runtime.snapshot()` at lifecycle checkpoints (for example app backgrounding) and restore it on next runtime creation.

## How to add diagnostics

Use runtime interceptors for cross-cutting side effects and DevTools for event timelines:

```ts
const runtime = createRuntime(workflow, props, {
  interceptors: [loggingInterceptor({ prefix: '[workflow]' })],
  devTools: createDevTools(),
});
```

- `DO` keep action functions pure.
- `DO` use interceptors for analytics/logging/metrics.
- `DO` wrap actions with `named(...)` when stable action names are needed.
