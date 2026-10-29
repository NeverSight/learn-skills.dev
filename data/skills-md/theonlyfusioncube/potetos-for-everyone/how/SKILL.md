---
name: how
description: Trace how a subsystem works using code and runtime evidence. Use for architecture walkthroughs, data flow, call paths, and are-we-sure investigations.
---
# How

Build an evidence-backed explanation of how the requested subsystem works.

1. Find the public/consumer entry point, then trace data and control flow toward the effect. Do not start from filenames guessed by name alone.
2. Read the core types and state ownership before narrating individual functions.
3. Use `vcs`, tests, or `observe` when they resolve an ambiguity. If `delegate` exists, split independent exploration areas and reconcile them yourself.
4. Draw a compact text or Mermaid diagram when it reduces reader load.
5. Test at least one claim that could easily be wrong by running or inspecting the real path.
6. Explain in consumer order: trigger -> boundary -> state/transform -> side effect -> observable result. Name file/symbol evidence and uncertainty.
