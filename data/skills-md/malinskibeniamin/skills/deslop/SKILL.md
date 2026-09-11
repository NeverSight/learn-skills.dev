---
name: deslop
description: "Fallback audit for removing unjustified code from an already-bloated diff or repository. Use on explicit deslop, ponytail, lazy mode, YAGNI, or bloat requests; never as a mandatory lifecycle pass."
license: MIT
vendored_from: https://github.com/DietrichGebert/ponytail (write mode)
---

Fallback, not lifecycle. Invoke only when a diff/repo already exceeds its behavior. The bundled `/simplify` is opt-in tactical cleanup; `/deslop` asks whether the surface should exist.

## Advocate for less is more

Optimize **semantic density**, not line counts: negative LOC is not the goal. Use the smallest obvious implementation where each construct carries behavior or clarifies domain. Never trade clarity for characters.

Design for demonstrated scale. No speculative indexes, virtualization, caching, queues, retries, factories, flags, configuration, or extension points. Admit additions only for required behavior, clarifying the domain, or a credible risk.

## Write mode

Explicit `/deslop write`, ponytail, or lazy mode. Understand the full flow first. Fix root cause, not symptoms; grep every caller before shared changes. Then:

1. Delete speculative scope.
2. Reuse the codebase.
3. Use language/standard library.
4. Use native platform.
5. Use installed dependency.
6. Write the smallest clear local expression.
7. Only then own machinery.

Prefer direct code until abstraction removes repeated complexity. Comments explain unavoidable why. Meaningful behavior keeps the smallest public-contract test; do not invent wiring tests or delete useful tests.

Intensity `lite|full|ultra`: name the leaner option, apply the ladder, or challenge every requirement.

Never cut: explicit requirements, trust-boundary validation, security, accessibility, or data-loss error handling.

## Gate mode

Read goal, nearby code, `git diff --stat`, and diff. Tag only proven excess:

- `delete:` dead/speculative.
- `stdlib:` custom replaced by language/library.
- `native:` replaced by platform.
- `yagni:` flexibility without requirement.
- `shrink:` same clear behavior, less surface.

Delete/inline/tighten, then run smallest relevant verification; skill/harness edits need RED -> GREEN eval evidence. Return `NEEDS_CHANGES` only when required behavior is buried in avoidable surface. Report retained/removed rationale. Repository audits rank justified deletions; otherwise end `Lean already. Ship.`

See [REFERENCE.md](REFERENCE.md) for repository audits and the checklist.
