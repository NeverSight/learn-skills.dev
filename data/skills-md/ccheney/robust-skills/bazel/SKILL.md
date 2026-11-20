---
name: bazel
description: Configure and troubleshoot Bazel builds. Use when editing BUILD or MODULE.bazel files, writing Starlark, diagnosing target, cache, or CI failures, or adopting or upgrading Bazel.
metadata:
  version: "9.2.0"
---

# Bazel Monorepos

Make build changes against the actual target graph and pinned Bazel/ruleset versions. Examples cover Bazel 9.2.0; they are not an upgrade instruction. The user's explicit instructions take precedence over this skill's guidelines.

## Establish the relevant context

Use the affected targets, error output, or requested build outcome as input. Check `.bazelversion`, relevant module declarations, BUILD files, and the configuration involved in the task. Read other repository configuration only when it affects that question.

| Question | Tool |
|---|---|
| Target dependencies, reverse dependencies, paths | `bazel query` |
| Selected flags, platforms, toolchains, or `select()` branches | `bazel cquery` with the failing invocation's configuration |
| Actual commands, inputs, outputs, tools | `bazel aquery` |
| External modules, versions, generated repositories | `bazel mod` |
| Cache misses or execution performance | Execution logs, profiles, BEP |

If the failing target or invocation cannot be inferred, ask for it and continue independent inspection. Do not invent repository pins or remote-cache endpoints.

## Preserve the build contract

- Declare direct inputs, dependencies, tools, and runtime data on the owning target. Use runfiles APIs for runtime resources.
- Keep package boundaries and visibility deliberate. Neither one target per file nor one per service is a universal template.
- For Bazel 9, use Bzlmod and explicit external language-rule loads. For older repositories, follow version-matched rules until an upgrade is requested.
- Diagnose missing inputs or configuration differences before using `clean --expunge` or disabling sandboxing; those can hide the cause.
- Validate affected targets and configurations. Reserve graph-wide builds/tests for graph-wide impact or required repository checks.

Deliver the requested patch or diagnosis with relevant target labels, evidence, and unresolved configuration dependencies. Finish checks needed for that outcome without expanding a local fix into a repository migration.

## References

Load only the topic needed; use section headings within longer references.

| Task | Reference |
|---|---|
| Packages, labels, dependencies, visibility, BUILD style | [BUILD-GRAPH.md](references/BUILD-GRAPH.md) |
| Modules, extensions, lockfiles, overrides, WORKSPACE migration | [BZLMOD.md](references/BZLMOD.md) |
| rc files, selects, platforms, toolchains, transitions | [CONFIGURATION.md](references/CONFIGURATION.md) |
| Query syntax and build failure diagnosis | [QUERIES-DEBUGGING.md](references/QUERIES-DEBUGGING.md) |
| Sandboxing, runfiles, caching, remote execution | [HERMETICITY-CACHING.md](references/HERMETICITY-CACHING.md) |
| CI gates, affected targets, profiles, performance | [CI-PERFORMANCE.md](references/CI-PERFORMANCE.md) |
| Macros, rules, providers, aspects, repository rules | [STARLARK.md](references/STARLARK.md) |
| Requested adoption or repository consolidation | [ADOPTION.md](references/ADOPTION.md) |
| Compact command or label lookup | [CHEATSHEET.md](references/CHEATSHEET.md) |

Use version-matched [Bazel docs](https://bazel.build/), ruleset release notes, and the [Bazel Central Registry](https://registry.bazel.build/) when bundled guidance does not establish compatibility.
