---
name: justfile
description: Create a justfile to orchestrate project tasks. Use when setting up task running for a project.
---

Create a `justfile` to orchestrate project tasks.

The justfile must include at least these rules:

- `default` — list all rules using `just --list`
- `setup` — do the main work
- `test` — (optional) run tests
- `teardown` — clean up artifacts created by setup

Keep the justfile simple and clear about what to run.

Inline bash is acceptable within the justfile. If a task requires more than ~10 commands, extract it into a separate bash script and have the justfile call that script instead.
