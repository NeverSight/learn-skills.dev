---
name: fluentci-dag-caching
description: "Optimize CI/CD build and test pipelines with FluentCI native DAG execution, content-addressed caching, task dependencies, parallel jobs, dry-run previews, and Git-aware affected detection. Use for FluentCI task plans, cache misses, or incremental CI scheduling."
license: MIT
---

# FluentCI native execution

## Choose the right layer

A module function, an ordered workspace workflow, and a native task graph are
separate layers. Native plans declare the whole DAG so the engine can schedule
independent tasks. SDK builders construct values; terminal `run`/`run!` calls
execute them. Matrix labels describe cases, not installed runtimes.

Inspect the plan producer, matching SDK/engine capabilities, and the installed
`fluentci execute --help` when permitted. Do not substitute an engine-only command
from another repository into the top-level FluentCI CLI.

## Preview selection before running

For an existing native plan:

```sh
fluentci execute plan.json --dry-run
fluentci execute plan.json --affected --base origin/main --dry-run
```

These preview native task selection and reasons as JSON. They do not run tasks or
publish outputs. Producing `plan.json` may itself execute an SDK build or custom
script; inspect that producer separately. `--dry-run` is not a global safety flag
for `fluentci run`, arbitrary module code, or publishing.

Read [plan structure](references/native-plans.md) when constructing a DAG or
choosing task environment, resources, services, and failure handling. Read
[cache and affected contracts](references/cache-and-affected.md) when configuring
reusable outputs or diagnosing selections/misses.

## Execute and inspect

```sh
fluentci execute plan.json --run-dir /tmp/project-ci-run --progress plain
```

The run directory must be fresh; choose a new path per invocation rather than
deleting an existing journal. `--progress json` exposes machine-readable events;
`plain` is useful in CI/pipes. Commands run on the host with the declared
working directory/environment, not inside Wasm.

Respect task failure and cancellation. Read the terminal report, task errors, and
stdout/stderr paths before retrying. Do not mask failed prerequisites by changing
conditions to `always`, setting allowed failure, removing dependencies, or clearing
the cache unless those semantics are actually requested.

The engine owns scheduling and process cancellation. Describe independent tasks
once, set an appropriate jobs limit, and avoid layering unbounded guest-side
parallel execution on top. Preserve explicit inputs/outputs and resource limits.

[Native plans](https://docs.fluentci.io/guides/native-plans/)
[CLI](https://docs.fluentci.io/reference/cli/)
