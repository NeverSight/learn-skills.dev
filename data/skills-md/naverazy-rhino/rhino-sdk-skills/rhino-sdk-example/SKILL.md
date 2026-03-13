---
name: rhino-sdk-example
description: "This skill should be used when the user asks for a working example of Rhino Health Python SDK code, says 'show me an example', 'how is X done in practice', 'sample code for', or wants to see real SDK usage patterns for a specific use case."
metadata:
  author: rhino-health
  version: "0.1.0"
---

# Rhino Health SDK — Example Finder

Find and present relevant working examples from the official Rhino Health SDK repository, with inline annotations explaining key patterns.

## Context Loading

1. **Always load first** — `../../context/examples/INDEX.md`
   Maps use cases to example files with key methods, difficulty levels, and recommended context sections.

2. **On match** — read the matched example file from `../../context/examples/<filename>`

3. **On no match** — read `../../context/patterns_and_gotchas.md` as the basis for composing a new example.

## Matching Logic

Read INDEX.md and match the user's request against:
- The **Use Case** column (primary match)
- The **Key SDK Methods** column (secondary match — user mentions a specific method or class)

Pick the single closest match. If multiple examples are relevant, present the best match first and mention the others as "See also".

## On Match: Presenting an Example

Read the full example file. Present it as:

### 1. Overview

Brief description (2-3 sentences) of what the example does, which SDK features it demonstrates, and its difficulty level from the INDEX.

### 2. Full Code

Show the complete example code. Add inline annotations for non-obvious SDK patterns:
- Deep import paths
- `get_*_by_name()` returning `None`
- Triply nested `output_dataset_uids`
- `List[str]` UID requirements for `aggregate_dataset_metric`
- Double-nested `input_dataset_uids` for code object runs
- Filter and group-by dict structures

### 3. Key Takeaways

Bullet list of the patterns demonstrated, cross-referenced to the "Read First" context section from INDEX.md. Example:

- **Authentication**: uses `getpass()` pattern (see patterns_and_gotchas.md §1)
- **Metric execution**: uses `aggregate_dataset_metric` with stringified UIDs (see patterns_and_gotchas.md §4)

## On No Match: Composing an Example

When no existing example matches the user's request:

1. State clearly: "No existing verified example covers this exact use case. Here is a composed example based on documented SDK patterns."
2. Follow the code template from the `write` skill: imports, auth, constants, resource lookup with None checks, core logic, result handling.
3. Use patterns from `patterns_and_gotchas.md` and method signatures from `sdk_reference.md`.
4. Mark placeholder values clearly (e.g., `"<your-project-name>"`).

## Response Format

1. **Example file name + description** (or "Composed example" if no match)
2. **Full annotated code**
3. **Key takeaways** — patterns demonstrated and which context sections to read for deeper understanding
