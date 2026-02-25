---
name: cogames-variant-debug
description: "Debug CoGames mission or variant regressions by comparing branch vs main. Use when behavior changes or a `cogames play` command regresses."
---

# CoGames Variant Debug

## Workflow
- Reproduce with the provided `uv run cogames play` command.
- Locate variant definitions, map setup, and reward/assembler logic.
- Diff against origin/main to isolate the regression.
- Propose a minimal fix and a verification command.
