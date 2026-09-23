---
name: repository-review
description: Review a repository change for correctness, security, and maintainability.
---

# Repository review

Review the diff in this order:

1. Restate the behavior the change is meant to provide.
2. Trace authority boundaries, validation, persistence, and cleanup paths.
3. Check failure behavior, concurrency, stale state, and partial completion.
4. Check macOS, Linux, Windows, and remote-workspace assumptions.
5. Run focused tests before broader quality gates.
6. Report findings by severity with file and line evidence.

Prefer a small reproducible test over a speculative warning. If no issue remains, state which risks were checked.
