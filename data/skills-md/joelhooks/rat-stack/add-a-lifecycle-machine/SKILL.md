---
name: add-a-lifecycle-machine
description: Learn how XState owns a lifecycle while Effect owns its work, errors, and services.
plain: "XState owns the named states of a lifecycle, while declared Effect actors do its work and keep errors typed."
diagram: |-
  reading
    │ fromEffect actor
    │ runs the work
    ├ ok   → inspected
    └ fail → unreadable
             FileStatsError
  started by
  createEffectActor
---

# Add a lifecycle machine

A lifecycle machine defines named states and the events that permit movement between them. Effect describes work with typed failures and required dependencies. A service is a named interface for one job. Schema defines accepted values and their runtime checks.

Copy `packages/core/src/inspect-machine.ts` when the work has states that matter. Keep a direct Effect when it does not.

Before changing Effect or XState code, read `node_modules/effect/AGENTS.md`. Then read the pinned XState and `@xstate/effect` source listed in `AGENTS.md`.

## 1. Write the states first

List the states and final results before writing the machine.

For file inspection, the states are `reading`, `inspected`, and `unreadable`. The final result is either `Inspected` with file stats or `Unreadable` with a `FileStatsError`.

Use an explicit result union when a known error should move the machine into a final state.

## 2. Put side effects in actors

Define each side effect with `fromEffect` outside the machine:

```ts
const performWork = fromEffect({
  effect: ({ input }) => ThingService.use((service) => service.run(input.id)),
  schemas: { input: Schema.Struct({ id: Schema.String }) },
});
```

An actor is a running unit that processes events or performs work for a machine. These actors carry typed errors and service dependencies. Declare them through `setupEffect`. Do not return an Effect from an inline XState callback.

## 3. Build the machine

Pass the actors and schemas to `setupEffect`, then call `createMachine`:

```ts
type ThingOutcome =
  | { readonly _tag: "Succeeded"; readonly value: ThingResult }
  | { readonly _tag: "Failed"; readonly error: ThingError };
interface ThingContext {
  readonly id: string;
  readonly outcome: ThingOutcome | undefined;
}

export const thingMachine = setupEffect({
  actors: { performWork },
  schemas: {
    context: types<ThingContext>(),
    input: Schema.Struct({ id: Schema.String }),
  },
}).createMachine({
  context: ({ input }) => ({ id: input.id, outcome: undefined }),
  initial: "working",
  output: ({ context }) => context.outcome,
  states: {
    working: {
      invoke: {
        src: "performWork",
        input: ({ context }) => ({ id: context.id }),
        onDone: {
          target: "succeeded",
          context: ({ context, event }) => ({
            ...context,
            outcome: { _tag: "Succeeded", value: event.output },
          }),
        },
        onError: {
          target: "failed",
          context: ({ context, event }) => ({
            ...context,
            outcome: { _tag: "Failed", error: event.error },
          }),
        },
      },
    },
    succeeded: { type: "final" },
    failed: { type: "final" },
  },
});
```

XState owns states and moves between them. Effect owns side effects, errors, services, and cleanup.

## 4. Run it inside Effect

Start the machine with `createEffectActor`. Do not use XState's `createActor`. Hand the actor to `watchActor` from `@rat-stack/capability/actor-watch`, then wait for it with `join` inside `Effect.scoped`:

```ts
export const runThingMachine = Effect.fn("runThingMachine")(function* (
  id: string
) {
  const actor = yield* createEffectActor(thingMachine, { input: { id } });
  yield* watchActor("thingMachine", actor);
  // @effect-diagnostics-next-line anyUnknownInErrorContext:off -- join exposes unknown machine failures; unexpected failures become defects with orDie.
  const outcome = yield* join(actor).pipe(Effect.orDie);
  if (outcome === undefined) {
    return yield* Effect.die(new Error("machine completed without an outcome"));
  }
  if (outcome._tag === "Failed") {
    return yield* outcome.error;
  }
  return outcome.value;
}, Effect.scoped);
```

`watchActor` does nothing until devtools runs the capability. Then `rat_list_actors`, `rat_list_transitions`, and `rat_get_actor` show every state and event. `rat-stack-patterns/watch-effect-actors` fails lint when a runtime module starts an actor without it.

A missing result or machine-level error is a bug in this design. A known product error belongs in the final result. `join` has an `unknown` machine-error channel, so the example uses one narrow diagnostic override before `Effect.orDie`.

Call the runner from the capability handler, the server-side implementation of one named action. Provide its service Layer in `apps/cli/src/cli.ts`. A Layer builds services and supplies their construction dependencies.

## 5. Generate inputs and command histories

Add a property and a model test with each lifecycle. Use `effect/Arbitrary` and `@effect/vitest`. Do not add a separate generator dependency.

Copy the complete test template at `skills/add-a-lifecycle-machine/templates/lifecycle.model.test.md` into `packages/core/test/<name>.model.test.ts`. It runs unchanged for `inspectMachine`. Replace its schemas, service, outcomes, and commands for your lifecycle. The executable reference is `packages/core/test/inspect-machine.model.test.ts`.

- Derive generated inputs, outputs, and failures from the domain schemas.
- Keep the model independent: pending until work settles, then one immutable terminal outcome.
- Use `getShortestPaths` from `xstate/graph` to cover both endings for each generated input and actor result. This export shares the XState pin; do not install `@xstate/graph` for XState 6.
- Use `getPathsFromEvents` to explore generated histories. Check the lifecycle rules after every step. Stop pure traversal at the first terminal event. Only the actor interpreter rejects later delivery.
- Run the same generated commands against `createEffectActor`. Control real child completion through a `Deferred` service fake. Do not inject completion events to settle a running actor.
- Check input forwarding, result preservation, typed failures, and the runner's Effect error channel. Probe after completion and check that neither output nor work changes.
- Keep integration examples with `it.layer`; they do not replace generated tests.

`it.effect.prop` supplies virtual time. For delayed work, add a wait command and use `TestClock.adjust` from `effect/testing`:

```ts
if (command.kind === "wait") {
  yield * TestClock.adjust(command.millis);
}
assertAgainstModel(actor.getSnapshot(), model);
```

Model the deadline independently. Check before, at, and after it. Never use wall-clock sleeps to wait for retries or deadlines.

Before trusting the property, temporarily break a lifecycle rule in the machine. Run the new tests and record the failing shrunk input and replay token. Restore the machine, then prove the tests pass. Keep mutation evidence in the packet or review report. Keep it out of production code.

The `xstate-effect/no-inline-effect` rule blocks inline Effect logic. Fix the code instead of disabling the rule.

## 6. Finish

```sh
pnpm turbo run check test build
```
