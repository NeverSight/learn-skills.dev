---
name: flow-simplify
description: "Targeted cleanup of provably dead code and accidental complexity. Use for dead paths, needless indirection or generated slop, not redesign. Hands off to `flow-review` or `flow-refactor`."
metadata:
  stage: build
---

# Simplify

Subtract only where it improves understanding without changing required behavior. Fewer lines
is a possible outcome, not the acceptance criterion.

## Process

1. Bound the cleanup, establish relevant checks and preserve unrelated staged/unstaged work.
   Name the concrete complexity: dead paths, needless indirection, duplicate responsibility,
   stale comments or generated slop.
2. Order reduction passes by semantic risk. For large scopes, authorized read-only reviewers can
   inspect disjoint areas; one writer per file. No arbitrary agent or file-count threshold.
3. Caller-check before deleting a symbol: imports, dynamic lookup, registries, reflection,
   routes, config, templates, tests, generated sources, package exports. Repository search
   cannot see external consumers of a published API.
4. Mark a deletion **CONFIRMED-DEAD** only with usage and runtime evidence; keep uncertain
   exports or negotiate the compatibility change. Keep side-effect imports (registration,
   polyfills) and license, compiler and tool-directive comments.
5. Inspect single-use abstractions instead of auto-inlining. Components, Hooks, closures and
   effects carry identity, state lifetime and evaluation order even with one caller.
6. Remove a defensive guard only when input provenance proves it redundant. Static types do not
   validate network, JSON, storage, DOM or JavaScript consumers.
7. Cut in small steps, run behavior and repository checks, inspect the combined diff. Stop when
   the stated complexity is resolved.

## Anti-patterns

- Net-negative lines as a quality gate, or every single-use component as waste.
- Removing imports, comments or guards on regex or type evidence alone.
- Deleting a public export because internal grep finds no caller.
- Quietly changing error behavior or component state lifetime.

## Done when

- The targeted code is easier to understand with semantics and compatibility preserved.
- Deletions have evidence; uncertain consumers remain explicit.
- Required checks ran on the resulting artifact, not an earlier baseline.

Use `flow-review` for the diff or `flow-refactor` for a separate ownership or structure problem.
