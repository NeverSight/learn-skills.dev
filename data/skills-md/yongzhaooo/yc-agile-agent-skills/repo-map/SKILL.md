---
name: repo-map
description: Locate code ownership and trace affected paths when a task's entry point, dependencies, or change boundary is unclear. Use a broader repository map only for cross-module or architecture questions.
---

# Repo Map

Locate the directly owning files first. Stop when the requested location or change
boundary is clear; a local lookup does not need a repository map.

Read applicable repository instructions first. Repository-local authority, retrieval,
sensitivity, and maintenance rules override this generic policy.

Narrow root, glob, file type, and symbol context before reading broad results. **If a
route produces no new evidence, switch to a materially different route** instead of
repeating a wider version of the same search.

Treat a stale or inconsistent project index as degraded. Exact or full-text evidence may
remain usable with its warnings, but do not claim semantic retrieval is healthy.

When behavior crosses modules or the impact is unclear, trace only the relevant:
- Entry points and user/system triggers.
- Owning files and symbols.
- Call chain or data flow through boundary layers.
- Shared abstractions that amplify blast radius.
- Existing tests and verification commands.
- Unknowns and the fastest check for each unknown.

Return the requested paths or symbols. For a broader map, include only the affected
flow, meaningful risks, write boundary, and verification surface needed by the task.

Stay in mapping mode unless the user has already asked for implementation.
