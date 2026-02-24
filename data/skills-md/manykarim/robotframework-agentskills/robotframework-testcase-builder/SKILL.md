---
name: robotframework-testcase-builder
description: Generate Robot Framework test cases from structured requirements or scenarios. Use when asked to create test cases, apply tags/setup/teardown/templates, or produce keyword-driven tests.
---

# Robot Framework Test Case Builder

Create test cases in Robot Framework syntax from structured input. Output JSON only.

## Input (JSON)

Provide input via `--input` or stdin. Example:

```json
{
  "style": "keyword-driven",
  "tests": [
    {
      "name": "User can create account",
      "documentation": "Happy path account creation.",
      "tags": ["smoke"],
      "setup": {"keyword": "Open Browser", "args": ["${URL}", "chromium"]},
      "teardown": {"keyword": "Close Browser"},
      "steps": [
        {"keyword": "Go To Sign Up"},
        {"keyword": "Create User", "args": ["${username}", "${role}"]},
        {"keyword": "User Should Be Logged In"}
      ]
    }
  ]
}
```

Template-driven test:

```json
{
  "style": "template",
  "tests": [
    {
      "name": "Login works",
      "template": "Login Should Succeed",
      "data_rows": [
        ["alice", "pass"],
        ["bob", "pass"]
      ]
    }
  ]
}
```

## Command

```bash
python scripts/testcase_builder.py --input tests.json
```

## Flags

- `--allow-control` -- Suppress warnings when control structures (`FOR`, `IF`,
  `WHILE`, `TRY`, etc.) appear in test steps. Without this flag the builder
  emits a warning for each control keyword found, encouraging you to move
  control logic into user keywords.
- `--input FILE` -- Path to the JSON input file (alternative to stdin).

## Timeout support

Add `"timeout"` to a test object to render a `[Timeout]` setting:

```json
{
  "name": "Slow Operation",
  "timeout": "30s",
  "steps": [{"keyword": "Long Running Task"}]
}
```

## Output (JSON)
- `artifact`: test case block(s)
- `warnings` and `suggestions`
