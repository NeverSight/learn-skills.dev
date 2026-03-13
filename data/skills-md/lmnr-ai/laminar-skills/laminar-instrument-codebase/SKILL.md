---
name: laminar-instrument-codebase
description: "Instrument an existing codebase with Laminar tracing: choose which functions to observe, initialize Laminar correctly, add tags/metadata/session IDs, and verify traces. Use when a user asks to add Laminar tracing, instrument functions, or integrate Laminar with a TS/JS or Python codebase."
---

# Laminar Instrument Codebase

## Workflow

1. Identify runtime and entrypoints; map critical flows and select functions to instrument.
2. Initialize Laminar once, early in the app, and configure auto-instrumentation for the libraries in use.
3. Add manual spans with `observe` around selected functions; attach tags, metadata, session/user IDs; suppress sensitive inputs/outputs.
4. Run a representative flow, validate traces in the UI, and tune span granularity and tags.

## References

- `references/function-selection.md` for heuristics on what to instrument.
- `references/ts-instrumentation.md` for TypeScript/JavaScript patterns and snippets.
- `references/python-instrumentation.md` for Python patterns and snippets.
