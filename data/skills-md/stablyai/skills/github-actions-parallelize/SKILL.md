---
name: github-actions-parallelize
description: Reference for concurrent steps within a GitHub Actions job and the background, wait, wait-all, cancel, and parallel keywords.
---

# GitHub Actions parallel steps

Steps can run concurrently within one job, with separate logs and execution:

- `background: true`: starts a step asynchronously; execution proceeds immediately.
- `wait`: blocks until specific named background steps finish.
- `wait-all`: blocks until all earlier background steps finish.
- `cancel`: gracefully stops a background step, including a long-running service.
- `parallel`: groups concurrent steps and waits for the group to finish; shorthand for background steps followed by a wait.

Reference: [workflow syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions).
