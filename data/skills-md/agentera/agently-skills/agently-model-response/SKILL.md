---
name: agently-model-response
description: Use when the user wants to reuse one model result, read text/data/meta without re-requesting, or stream partial updates, including `get_response()`, async getters, `delta`, `instant`, and `specific`.
---

# Agently Model Response

Use this skill when the output contract is already chosen and the remaining issue is how the response instance should be consumed or reused.

The user does not need to say `get_response()`. Requests to reuse one result as text, parsed data, metadata, or progressive updates should route here.

## Native-First Rules

- prefer `get_response()` when one request result must be consumed more than once
- prefer async response APIs in async runtimes
- use `delta`, `instant`, `specific`, or `all` instead of custom stream splitting logic

## Anti-Patterns

- do not re-issue the same request to obtain text, data, and metadata separately
- do not build ad hoc field-level stream parsers when `instant` or `streaming_parse` already fits

## Read Next

- `references/overview.md`
