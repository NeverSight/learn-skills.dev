---
name: rstest-debugging
description: Debug Rstest startup, build, runtime, logging, and memory problems systematically. Use when Rstest is slower than Jest/Vitest or a previous baseline; when runner/build/tests/CLI wall disagree; when setup/collect or Node module loading dominates; when mocked modules still enter bundles; when experimental bundle coverage or asset utilization needs inspection; or when dependency bundling, assets, pools, isolation, logs, or memory need evidence-based tuning.
---

# Rstest Debugging

Diagnose the measured lifecycle stage before changing configuration. Keep behavior and the test manifest fixed, change one variable at a time, and remove experiments that do not produce a repeatable benefit.

## Workflow

1. Establish comparable single-file and full-scope baselines with `references/performance-measurement.md`.
2. Run `rstest --trace` when supported and classify the cost as host build/startup, runtime load/setup/collect, test bodies/hooks, or CLI/report/teardown overhead.
3. Use `DEBUG=rstest` for resolved config and build output. For Rstest 0.11.7+ experimental per-test bundle coverage, follow `references/performance-measurement.md`. Use Rsdoctor only after evidence points to the compiler. Use verbose reporting or a profiler only after narrowing to runtime files/cases.
4. If dependency loading or compilation is implicated, read `references/dependency-bundling.md`. Compare the environment default, `bundleDependencies: false`, and `bundleDependencies: true`; neither bundling nor externalization is universally faster.
5. If a fully mocked heavy module still reaches the build graph, read `references/mocked-module-build-graph.md` before testing an exact external.
6. If assets, console output, pools, isolation, or memory dominate, read `references/runtime-output-memory.md`.
7. Rerun the representative file and full scope. Keep a change only when behavior, discovery, snapshots, and coverage remain valid and the benefit survives repeated measurement. Remove traces, profiles, and `.rstest` debug artifacts created by the diagnosis before handing off.

## Guardrails

- Use the project's installed Rstest for final claims. Label local checkout or unreleased diagnostic results separately.
- Keep Node version, test files, coverage, cache state, environment, workers, and command shape fixed while comparing.
- Do not add worker durations that overlap or subtract runner/build/tests values without verifying their lifecycle boundaries.
- Do not treat aggregate process-tree RSS as physical memory; it can double-count shared pages.
- Do not disable isolation, reduce coverage, silence failures, or change production/test semantics for a benchmark win.
- Do not stack speculative aliases, externals, compiler hooks, pool settings, or caches. Preserve only the measured minimum.

## Handoff from migration

When invoked from `migrate-to-rstest`, first confirm that the Jest/Vitest and Rstest manifests match. If the migration intentionally adds tests, report same-scope performance separately from final expanded-scope performance.
