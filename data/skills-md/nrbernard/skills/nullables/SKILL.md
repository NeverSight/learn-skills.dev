---
name: nullables
description: James Shore's Nullables pattern for testing without mocks. Use when writing or changing tests, adding code that touches the outside world (database, files, network, clock, environment, framework hooks), or replacing mocks.
---

# Nullables

Tests are **sociable** and **state-based**: they run real production code end to end within a unit, and the outside world is switched off by **Nullables**, production classes with a `createNull()` factory. Source: [Testing Without Mocks](https://www.jamesshore.com/v2/projects/nullables/testing-without-mocks).

## 1. Classify each class

Every class is exactly one of:

- **Logic**: pure computation, no outside world. Prefer pure functions and immutable values; expose any mutable state through getters. Test by input → output. Needs no Nullable.
- **Infrastructure Wrapper**: one class per external system (Postgres, file system, clock, environment, HTTP). It owns the third-party library and exposes an interface shaped by what the app needs, in domain terms.
- **Application**: a **Logic Sandwich**: read from wrappers, process with Logic, write to wrappers. For pushed events it is a **Traffic Cop**: listen, then run a Logic Sandwich per event.

Logic and Infrastructure never depend on each other; Values carry data between them. When a class mixes two kinds, split it before testing it.

## 2. Make it Nullable

Every Wrapper and Application class:

- Has a `static create()` that wires real dependencies, taking each as an optional named override (`create({ store = ImportStore.create() } = {})`), and a `static createNull(options = {})` that returns the same class with the outside world off. `createNull()` is production code in the same file; everything except the external call runs for real.
- Does no work in its constructor. Connecting, starting, and listening happen in `connect()` / `start()`.
- Nulls itself one of two ways:
  - **Embedded Stub** (low-level wrapper): `createNull()` injects a minimal stub of the *third-party* library, defined in the same file. Stub only what the wrapper calls.
  - **Fake It Once You Make It** (everything above that): `createNull()` builds Nulled dependencies and translates its own options into theirs. No new stub.
- Takes **Configurable Responses** in `createNull()` options, named in this class's domain terms (`{ accounts: [...] }`, not `{ rows: [...] }`). A single value repeats forever; an array is consumed in order and throws when exhausted.
- Offers **Output Tracking** for every meaningful write: `trackXxx()` returns an `OutputTracker` recording the write in domain terms. Works on real and Nulled instances alike.
- Offers **Behavior Simulation** for every event the outside world pushes: `simulateXxx()` calls the same private handler the real listener calls.

Code shapes and helper implementations (`ConfigurableResponses`, `OutputTracker`): [PATTERNS.md](PATTERNS.md).

## 3. Write the tests

- **Logic**: plain arrange-act-assert on return values.
- **Wrapper**: **Narrow Integration Tests** against a local, dedicated system: the Compose Postgres, a temp directory, or, for a third-party web service, a localhost HTTP server the test starts, which records each request and answers as the test sets. Cover failure paths too (errors, timeouts, malformed responses): **paranoic telemetry**, every failure logged or thrown. Then test the Nulled instance, which proves the Embedded Stub matches the driver it replaces. A third-party service's own behaviour lives in Configurable Responses, each commented with where it was seen; changes on its side surface through paranoic telemetry in production.
- Test each behaviour once, at the class that owns it: "don't test all phases of the moon in your describeMoonPhase() tests, but do test them in your Moon tests." A dependent's tests cover only what the dependent adds.
- **Application**: build the **subject under test** with its `create()`, passing Nulled dependencies (`Ledger.create({ store: ImportStore.createNull() })`), configure their responses, act, then assert on returned values, resulting state, or tracked output. `create()` is the production path, so the test exercises the wiring production runs, and a dependency missing its Null surfaces as a test reaching the outside world. A class's own `createNull()` serves the classes above it.
- Every dependency in a test is the real class, Nulled at the infrastructure edge. The only stubbed code is third-party code, inside an Embedded Stub. Configurable Responses and Output Tracking do the work of mocking libraries, so modules and collaborators are never mocked or spied on (`jest.mock`, `vi.mock`, `vi.spyOn`).
- **Callback props are output.** A UI component hands its result back through a callback prop, such as a form's `onSubmit` or server action. In a component test, a `vi.fn()` passed as that prop is the component's Output Tracking: assert on what it received (`toHaveBeenCalledWith`), and give it a return value to stand in for the answer.
- **Framework-provided dependencies are Nulled at the framework's own seam.** A hook or injected service that reads from the framework, such as a router, the current request or a theme, has no Wrapper to Null, since the framework hands it in rather than the app calling out. Where the framework provides it through an injection point, such as a React context or a DI container, the test provides an Embedded Stub there, with Output Tracking for what the code asks of it (each navigation, each header set). The real component and the real hook run; only the third-party object beneath them is stubbed. The code stays where the design puts it, at a layer fast tests reach, rather than moving to one only a real framework mounts. When the injection point is one of the framework's internals, a single shared test helper imports it, so a framework upgrade that moves it breaks one line.
- **Signature Shielding**: route repeated setup through a helper taking optional named options with defaults and returning an object, so tests survive signature changes:

  ```ts
  async function importFile({ file = sampleQfx(), now = "2026-01-01" } = {}) {
    const store = ImportStore.createNull();
    const saves = store.trackSaves();
    const ledger = Ledger.create({ store, clock: Clock.createNull({ now }) });
    const summary = await ledger.importFile(file);
    return { summary, saves: saves.data };
  }
  ```

- Keep one or two **Smoke Tests** that boot the real app and run its most common workflow. Everything else is narrow.

Converting existing code that uses mocks or has no seams: [LEGACY.md](LEGACY.md).

## Done when

- Every class is classified, and none mixes Logic with Infrastructure.
- Every Wrapper and Application class has `create()` and `createNull()`, and each behaviour its Nulled instance offers is exercised by a test.
- Every Wrapper has Narrow Integration Tests against a local, dedicated system, failure paths included.
- Every Application test builds its subject under test with `create()` and Nulled dependencies.
- Every write a test cares about is visible through Output Tracking; every pushed event through Behavior Simulation.
- Every assertion checks a value, a state, or tracked output.
