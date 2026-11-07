---
name: clean-commits
description: Rewrite a branch or commit range into a clean, coherent commit history.
disable-model-invocation: true
---

# Clean commits

Rewrite the specified branch or range into commits with one reviewable purpose each. Use the cumulative diff to identify surviving work and the original patches to recover intent.

- Separate independent features, fixes, refactors, formatting, and tooling changes, including mixed hunks within one file.
- Keep tests, documentation, generated files, and lockfile changes with the change they support.
- Drop changes subsequently removed or reverted within the selection, including commits left empty.
- Collapse repeated revisions into their final form wherever possible. Retain intermediate changes only where needed for a coherent sequence.
- Order prerequisites before consumers so each commit leaves a working state. Keep tightly coupled changes together when splitting would break that state.
- Write commit messages describing the resulting change and its rationale.

Review every resulting commit for mixed purposes, broken dependencies, and avoidable churn. Correct these before reporting the cleaned commit list.
