---
name: test-behaviour
description: Pick the test shape that proves a behaviour. Use when you ask "how do I test this?", add a test, test a domain rule, a lifecycle, a retry, a session, a UI interaction, a timer, or a race, or review a test that might be tautological.
plain: "Name what the test proves, pick the shape for it, then plant a bug and watch the test fail."
diagram: |-
  what does it prove?
  ├ domain rule  → it.prop
  ├ history      → model test
  ├ UI behaviour → Scene
  └ one seam     → example
      │
  plant a bug → test fails
  restore     → test passes
---

# Test a behaviour

A test proves one behaviour. Name that behaviour before you write the test. Then pick the shape below that fits it.

Each shape returns a fixed, independent answer. A test that reruns the code under test cannot catch its mistakes. Read [tests that earn their place](/lore/tests-that-earn-their-place) first.

## 1. A domain rule: a property

A rule that holds for many inputs is an `it.prop` over Effect `Arbitrary` inputs. Use `it.effect.prop` when the check returns an Effect.

The events suite generates a sensitive key and requires its removal. The assertion does not call the filter to decide the answer:

```ts repo=rat-stack path=packages/events/test/request-facts.test.ts at=1d4d3252326a216909ccec05e93312d1ab0eaf84 lines=25-39

```

Read [property-based testing](/lore/property-based-testing).

## 2. Anything with history: a model

Sessions, retries, and lifecycles depend on earlier steps. Generate command sequences and check the real system against a small model after each step.

The inspection lifecycle replays generated histories against the real actor:

```ts repo=rat-stack path=packages/core/test/inspect-machine.model.test.ts at=1d4d3252326a216909ccec05e93312d1ab0eaf84 lines=214-219

```

Copy `skills/add-a-lifecycle-machine/templates/lifecycle.model.test.md` for a new machine. Read [model-based testing](/lore/model-based-testing).

## 3. UI behaviour: a Foldkit Scene

A Scene runs `update`, the view, and subscriptions together. Input and time are data:

- Input is a step: `pointerDown`, `click`, `type`, or `Subscription.emit`.
- Time is a Command. Resolve it with `Command.resolve(WaitX, CompletedWaitX(...))`.
- Do not use fake timers, a clock, or a DOM.

A race is a plain assertion. Resolve a stale timer after the state has moved on, then assert that nothing broke.

Assert on what the view shows: roles, text, and data attributes. Do not assert on Model fields.

The reader's copy button resolves the copy and then its reset wait:

```ts repo=rat-stack path=apps/web/test/reader.scene.test.ts at=1d4d3252326a216909ccec05e93312d1ab0eaf84 lines=51-69

```

Read [UI behaviour is a scene](/lore/ui-behaviour-is-a-scene) for the Foldkit UI Toast race.

## 4. A seam: one example

An example test fits one interface between parts, such as a service over the real filesystem. Keep one, and supply services through a Layer:

```ts repo=rat-stack path=packages/core/test/file-inspector.test.ts at=1d4d3252326a216909ccec05e93312d1ab0eaf84 lines=24-34

```

## 5. Always: plant a bug

1. Break the behaviour the test protects.
2. Run the test. It must fail.
3. Restore the code. The test must pass.

Reject these tests:

- A tautological test computes its expected answer with the code under test.
- A change-detector test fails on any edit and proves no rule.
- A regression test for a bug the suite already covers adds nothing.

Do not rewrite an expected result to match broken code.
