---
name: w-errors
description: Add error handling that matches existing repo error and logging packages.
disable-model-invocation: true
---

Harden the current code's failure paths. Follow the error-handling page named from `AGENTS.md` and existing error/logger packages. Do not hide the owning failure with retries.

1. Identify failure points on the changed path: validation, I/O, authz, empty/invalid input.
2. Use the repo error type and logger. Return or render existing user-facing error patterns.
3. Retry only when the write is replay-safe. Otherwise keep an explicit no-retry path with a bounded deadline if a retry is already required.
4. Cover the new path with a test or a named manual scenario. Run the smallest existing check.
5. Docs: `/w-docs` if behavior or commands changed.
