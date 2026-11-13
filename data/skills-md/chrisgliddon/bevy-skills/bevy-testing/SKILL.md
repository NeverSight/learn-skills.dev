---
name: bevy-testing
description: "Use when testing Bevy 0.20 with `App::update`, `TimeUpdateStrategy`, `FixedUpdate`, `MessageCursor`, or `On<E>` observers: deterministic stepping, async-task draining with `poll_once` and no sleeps, headless worlds, and capture-based visual regression."
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "2"
  area: testing
  bevy_version: "0.20"
---

# Bevy 0.20 — deterministic testing

## When to use this skill

- Systems/plugins need a minimal `App` harness and direct world assertions.
- Fixed schedules, timers, messages, or observers need deterministic stepping.
- Async work must complete in tests without arbitrary sleeps.
- Rendered output needs capture-based visual regression.

Build the smallest `App` that owns the behaviour under test, control its clock and
inputs, step it explicitly, then inspect world state or emitted output. Do not call
`App::run()` in an ordinary unit/integration test.

## Canonical pattern

```rust
use bevy::{prelude::*, time::{TimePlugin, TimeUpdateStrategy}};

#[derive(Resource, Default)]
struct TickCount(u32);

fn count_tick(mut count: ResMut<TickCount>) {
    count.0 += 1;
}

#[test]
fn fixed_system_runs_exactly_three_times() {
    let mut app = App::new();
    app.add_plugins(TimePlugin)
        .insert_resource(Time::<Fixed>::from_hz(60.0))
        .insert_resource(TimeUpdateStrategy::FixedTimesteps(1))
        .init_resource::<TickCount>()
        .add_systems(FixedUpdate, count_tick);

    // The first update initializes Bevy's real-time clock; it has zero delta.
    app.update();

    for _ in 0..3 {
        app.update();
    }

    assert_eq!(app.world().resource::<TickCount>().0, 3);
}
```

After the first clock-initialising update, `FixedTimesteps(n)` makes each
`app.update()` advance by the fixed timestep times `n` and run exactly `n` fixed
loops. Use `ManualDuration` when the test must exercise zero-tick frames, accumulated
time, or catch-up. Use `ManualInstant` when exact absolute instants matter and advance
its resource before each update.

## Gotchas

- The first `app.update()` initialises real time with zero delta; warm it up before
  counting `FixedTimesteps` ticks or assert that zero-step frame deliberately.
- Running `FixedUpdate` directly bypasses fixed-main clock/message semantics.
- Deferred `Commands` are invisible until a synchronization point.
- Async completion must use an injected fake or a bounded predicate loop, never sleep.
- `DefaultPlugins` adds platform/render/audio state most world tests do not need.
- **Observers lost the bundle generic (0.20).** Stale output writes
  `On<Add, Health>`; 0.20 is `On<Add<Health>>`, and a plain `On<Hit>` for custom
  events. `IntoObserverSystem` now has three generics, so an "inscrutable" trait error
  usually means one generic too many.
- **`&mut World` is an ordinary `SystemParam` (0.20).** An exclusive test helper no
  longer needs a special signature; `System::is_exclusive` is gone.
- **`iter_many` yields `Result` (0.20).** Assertions over an entity list need
  `query.iter_many(ids).matched()` for the old skip-missing behaviour.
- **`NextState::set_if_neq` is `set_if_different` (0.20).** The old name compiles
  with a deprecation warning.
- **`Name` is `From<&'static str>` only (0.20).** Tag test entities with
  `Name::new(string.to_owned())` when the label is not a literal.
- **Events: `Replace` became `Discard` (0.19)**; `Pointer<Click>` became
  `PointerClick` (0.20). Observer tests on these names must be renamed.
- **`ScheduleBuildSettings::shuffle_seed` (0.20, `debug` feature)** randomises
  unordered systems per seed. Use it in CI to surface missing `.before`/`.after`.

## Test through observable contracts

- Insert resources/components and call `app.update()` for scheduled behaviour.
- Invoke pure helper functions directly for algorithms and state machines.
- Read world state, messages with a test-owned `MessageCursor`, or observer effects.
- Keep deferred-command boundaries visible: a command is not applied until the
  schedule reaches a synchronization point.
- Assert invariants and externally meaningful ordering, not arbitrary query/entity or
  same-event observer order.

## Async without sleeps

Production systems poll `Task<T>` with `block_on(poll_once(&mut task))` (both
re-exported from `bevy::tasks`) or `bevy::tasks::futures::check_ready(&mut task)`.
Tests should inject a deterministic inline/fake executor when possible. Otherwise step
the app until an observable completion predicate with a strict maximum step/deadline
and fail with queue/task state. Never use "sleep 100 ms and hope the task finished."

Dropping a Bevy `Task` cancels it unless it was detached. Keep task ownership explicit
and ensure tests cover completion, cancellation, failure, and stale-result paths.

## Headless versus rendered tests

For ECS/gameplay logic, use `App::new()` plus only required plugins (`TimePlugin`,
`AssetPlugin`, `TaskPoolPlugin`, etc.). Avoid `DefaultPlugins` when no window,
renderer, audio device, or filesystem is part of the contract. For render acceptance,
launch a real render app, capture a `Screenshot`, wait for `ScreenshotCaptured`, and
compare a saved artifact against a versioned baseline with documented tolerance.

## Choose the relevant deep dive

| Problem | Read |
|---|---|
| Minimal apps, manual time, fixed loops, schedule stepping | [App and time](references/app-and-time.md) |
| Messages, observers, deferred effects, tasks and no-sleep draining | [Messages, observers, and async](references/messages-observers-and-async.md) |
| Screenshot capture, deterministic scenes, diff thresholds and artifacts | [Visual regression](references/visual-regression.md) |

## Review checklist

- The test owns time; wall-clock speed cannot change its expected result.
- Each test installs only the plugins/resources the subject requires.
- Inputs and random seeds are explicit, and persistent/global state is isolated.
- Fixed input tests cover zero, one, and multiple fixed ticks per update.
- Message cursors are created before/after writes intentionally.
- Async tests have a deterministic fake or a bounded progress loop with useful failure.
- Visual failures retain actual, expected, and diff images plus run metadata.
- Baselines are updated only through an explicit reviewed operation.

## See also

- [`bevy-input-actions`](../bevy-input-actions/SKILL.md) — frame-to-fixed input invariants.
- [`bevy-physics`](../bevy-physics/SKILL.md) — Rapier headless and determinism boundaries.
- [`bevy-diagnostics-profiling`](../bevy-diagnostics-profiling/SKILL.md) — acceptance replays and performance evidence.
- [`bevy-migration-0-19-to-0-20`](../bevy-migration-0-19-to-0-20/SKILL.md) — observer, `iter_many`, and state renames.
- [Bevy `TimeUpdateStrategy`](https://docs.rs/bevy/0.20.1/bevy/time/enum.TimeUpdateStrategy.html)
- [Bevy `Task`](https://docs.rs/bevy/0.20.1/bevy/tasks/struct.Task.html)
