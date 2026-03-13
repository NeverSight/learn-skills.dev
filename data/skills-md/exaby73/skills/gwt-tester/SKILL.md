---
name: gwt-tester
description: Write or refactor tests using clear Given/When/Then structure. Use when creating new tests, improving test readability, or standardizing test files with setup hooks, assertion-only Then blocks, and shallow suite nesting.
---

# GWT Tester

Use these instructions to write clean, readable tests with Given/When/Then semantics.

## Terminology Map
Use the agnostic terms below throughout this skill.

| Agnostic term               | JS/TS example | Dart example  |
| --------------------------- | ------------- | ------------- |
| Suite block                 | `describe`    | `group`       |
| Case block                  | `it` / `test` | `test`        |
| Setup once (for a suite)    | `before`      | `setUpAll`    |
| Setup each (per case)       | `beforeEach`  | `setUp`       |
| Teardown once (for a suite) | `after`       | `tearDownAll` |
| Teardown each (per case)    | `afterEach`   | `tearDown`    |

When this skill says:
- "suite block", read `describe` (JS/TS) or `group` (Dart)
- "case block", read `it`/`test` (JS/TS) or `test` (Dart)
- "setup hook", read `before`/`beforeEach` (JS/TS) or `setUpAll`/`setUp` (Dart)
- "teardown hook", read `after`/`afterEach` (JS/TS) or `tearDownAll`/`tearDown` (Dart)

## Rules
1. Keep maximum nesting depth to 3 levels: `suite -> suite -> case`.
   Exception: allow `suite -> suite -> suite -> case` for `When` variant coverage when validating the same behavior across interfaces or variants (for example `via RPC` and `via REST`).
   In this exception, variants are at level 3 and `Then` case blocks are at level 4.
2. Never nest `Given` blocks inside another `Given` block.
3. Keep `Given` setup hooks focused on shared context and test data, not primary behavior under test.
4. Prefer assertion-only case blocks.
5. Move executable behavior into a dedicated `When` block whenever possible. Use setup hooks inside that `When` block to run the action once per case.
   If there is no executable action to perform for a scenario, skip the `When` block and place `Then` cases directly under the `Given` block.
   If that `When` contains variants, place action setup hooks inside each variant block, not in the parent `When` block.
6. Ensure block titles describe behavior that actually happens in that block's scope. Do not title a case `When <action> ...` if `<action>` already ran in another block's setup hook.
7. If a `When` has only one `Then`, use a single case title (`When ... then ...`); in this collapsed form, putting the `When` action inside the case body is acceptable.
8. Remove wrapper suite blocks that do not add scenario context.
9. Write explicit scenario titles: `Given <subject> with <condition>`, optional `When <action>`, and `Then <outcome>`.
10. Place test utilities based on scope:
    - If a utility is specific to one test file, place it at the bottom of that file so test blocks remain the first code in the file.
    - If a utility is reused across test files, move it to shared test utilities following existing codebase conventions.
    - If no shared utility convention exists, create an appropriate `utils` directory and place shared utilities there.
11. Extract a value into a named variable only when that value is used more than once, and place it in the nearest shared scope (for example `Given` or `When`) to make test data updates predictable and centralized.

## Writing Workflow
1. Define scenarios as top-level `Given ...` suite blocks.
2. Add `Given` setup hooks for shared context only.
3. Add nested `When ...` suite blocks for each action path.
   If there is no action to perform, skip `When` and place `Then` cases directly under `Given`.
4. Run the action in setup hooks inside the `When` block when multiple `Then` cases share it.
   If variants exist under that `When`, run setup hooks inside each variant block.
5. Add assertion-only `Then ...` case blocks.
6. If a `When` has only one `Then`, optionally collapse to a single case title: `When ... then ...`.
7. Move logic from `Given` hooks into `When` hooks when that logic is action-specific.
8. If a `When` needs interface/variant coverage, nest variant blocks under that `When` only (for example `via RPC`, `via REST`).
9. Keep nesting shallow and remove redundant wrappers.
10. Run tests and formatter.

## When Variant Coverage
Use one extra nesting level only for variant coverage under the same `When` action.
Keep action setup hooks inside each variant block, not in the parent `When` block.

Example 1 (setup inside variants):

```pseudo
suite("Given an endpoint that returns a user", () => {
  suite("When requesting user 42", () => {
    suite("via RPC", () => {
      setup_each(() => {
        response = requestUserViaRpc(42)
      })

      case("Then status is successful", () => {
        assert(response.status == 200)
      })
    })

    suite("via REST", () => {
      setup_each(() => {
        response = requestUserViaRest(42)
      })

      case("Then status is successful", () => {
        assert(response.status == 200)
      })
    })
  })
})
```

Example 2 (multiple `Then` outcomes per variant):

```pseudo
suite("Given a user endpoint", () => {
  suite("When requesting user 42", () => {
    suite("via RPC", () => {
      setup_each(() => {
        response = requestUserViaRpc(42)
      })

      case("Then status is successful", () => {
        assert(response.status == 200)
      })

      case("Then user payload is present", () => {
        assert(response.body.user != null)
      })
    })

    suite("via REST", () => {
      setup_each(() => {
        response = requestUserViaRest(42)
      })

      case("Then status is successful", () => {
        assert(response.status == 200)
      })

      case("Then user payload is present", () => {
        assert(response.body.user != null)
      })
    })
  })
})
```

## Pseudocode Pattern
```pseudo
suite("Given <subject> with <state>", () => {
  setup_each(() => {
    // arrange shared context
  })

  suite("When <action>", () => {
    setup_each(() => {
      // act
    })

    case("Then <outcome A>", () => {
      // assert only
    })

    case("Then <outcome B>", () => {
      // assert only
    })
  })
})
```

No-action scenario (skip `When`):

```pseudo
suite("Given <subject> with <state>", () => {
  setup_each(() => {
    // arrange shared context only
  })

  case("Then <outcome A>", () => {
    // assert only
  })
})
```

## Title-to-Scope Alignment
Use titles that match where behavior occurs.

Bad example:

```pseudo
suite("Given a counter at zero", () => {
  setup_each(() => {
    // Bad: action belongs in a When block, not Given setup.
    counter.increment()
  })

  case("Then value is one", () => {
    assert(counter.value == 1)
  })
})
```

Good example:

```pseudo
suite("Given a counter at zero", () => {
  setup_each(() => {
    // arrange
  })

  suite("When incremented", () => {
    setup_each(() => {
      counter.increment()
    })

    case("Then value is one", () => {
      assert(counter.value == 1)
    })

    case("Then value is not zero", () => {
      assert(counter.value != 0)
    })
  })
})
```

## Logic Movement for Clean Blocks
Move logic to the narrowest block that owns that behavior.

- Keep data creation and shared fixtures in `Given` setup hooks.
- Move action-specific calls from `Given` setup hooks into the relevant `When` block.
- Keep `Then` case blocks assertion-only.
- Only keep action execution in case bodies for a single `When ... then ...` collapsed case.

## When/Then Collapse
Apply collapse when one action has only one outcome assertion.

Bad example (not collapsed):

```pseudo
suite("Given a counter at zero", () => {
  setup_each(() => {
    // arrange
  })

  suite("When incremented", () => {
    setup_each(() => {
      counter.increment()
    })

    case("Then value is one", () => {
      assert(counter.value == 1)
    })
  })
})
```

Good example (collapsed):

```pseudo
suite("Given a counter at zero", () => {
  setup_each(() => {
    // arrange
  })

  case("When incremented then value is one", () => {
    counter.increment()

    assert(counter.value == 1)
  })
})
```

## Utility Placement
Choose utility location by reuse scope.

- Keep file-specific utilities in the same test file, below all test blocks.
- Move cross-file utilities to shared test utility locations used by the codebase.
- If the repository has no established shared test utility location, create an appropriate `utils` directory for shared test helpers.

## Reused Values
Extract repeated values into named variables near test setup only when the same value is used more than once.

Bad example (no variable extracted):

```pseudo
suite("Given a user lookup", () => {
  suite("When searching by user id", () => {
    case("Then it returns the matching user", () => {
      result = findUser("user-42")
      assert(result.id == "user-42")
    })

    case("Then it records an audit message for that user", () => {
      assert(formatAuditMessage("user-42") == "audit:user-42")
    })
  })
})
```

Bad example (scope too broad):

```pseudo
suite("Given a user lookup", () => {
  userId = "user-42" // Too broad: only shared inside the When block below.

  suite("When searching by user id", () => {
    case("Then it returns the matching user", () => {
      result = findUser(userId)
      assert(result.id == userId)
    })

    case("Then it records an audit message for that user", () => {
      assert(formatAuditMessage(userId) == "audit:" + userId)
    })
  })
})
```

Good example:

```pseudo
suite("Given a user lookup", () => {
  suite("When searching by user id", () => {
    userId = "user-42" // Nearest shared scope.

    case("Then it returns the matching user", () => {
      result = findUser(userId)
      assert(result.id == userId)
    })

    case("Then it records an audit message for that user", () => {
      assert(formatAuditMessage(userId) == "audit:" + userId)
    })
  })
})
```

## Refactoring Guide
When asked to refactor or check existing tests, evaluate against all rules, not only the rule that triggered the edit.

Use this pass order:

1. Map current structure as `Given`, `When`, and `Then` blocks.
2. Move action-specific logic out of `Given` setup hooks into the correct `When` block.
   Keep scenarios with no action directly under `Given` without adding an empty `When`.
3. After each logic move, immediately re-evaluate collapse opportunities:
   - If a `When` block now has only one `Then`, collapse to `When ... then ...`.
   - If additional outcomes still exist, keep `When` + multiple `Then` cases.
4. Re-check title-to-scope alignment after structural edits.
5. Run the full review checklist before finishing.

## Anti-Patterns
- Nesting `Given` inside `Given`.
- Keeping action execution in `Given` setup when it can be moved to a `When` block.
- Calling the SUT inside a case block when it can be executed in `When` setup hooks.
- Mixing setup/action/asserts in a single case block.
- Adding wrapper suite blocks with no new context.
- Adding an empty `When` block when there is no action to perform.
- Collapsing to `When ... then ...` when `When` variants exist, even if there is only one `Then` outcome.
- Depth greater than `suite -> suite -> case`, except `suite -> suite -> suite -> case` for `When` variants.
- A title that claims an action runs in one block when it actually runs in another block.

## Review Checklist
- Are all rules reviewed, not just the rule that prompted the refactor?
- Are there any nested `Given` blocks?
- Does each case block contain assertions only?
- Does `Given` setup contain only shared context?
- Is action logic moved into the relevant `When` block?
- If there is no action to perform, is `When` skipped and are `Then` cases placed directly under `Given`?
- When variants exist, are action setup hooks placed inside each variant block instead of the parent `When` block?
- After each logic move, was `When`/`Then` collapse re-evaluated?
- Do suite and case titles match what actually happens in each block's scope?
- Are single `When` + single `Then` cases collapsed into one case block?
- Are file-specific utilities placed at the bottom of the test file (with tests first)?
- Are shared utilities moved to shared locations that follow existing codebase patterns (or a new appropriate `utils` directory when no pattern exists)?
- Are values extracted into named variables only when reused more than once, and placed in the nearest shared scope (for example `Given` or `When`)?
- Is nesting depth <= 3, or `suite -> suite -> suite -> case` only for `When` variants (level 3) with `Then` case blocks at level 4 (for example `via RPC`/`via REST`)?
