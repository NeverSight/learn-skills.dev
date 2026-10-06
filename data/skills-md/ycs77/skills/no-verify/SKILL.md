---
name: no-verify
description: Skip agent-run tests and browser verification after implementation; I will verify the changes myself.
disable-model-invocation: true
---

When invoked for an implementation task, complete the requested changes and hand them off for user verification. You may run linting, typechecks, and formatting. Skip agent-run tests, builds, smoke checks, and browser verification. Do not claim the changes passed checks you did not run.

If a higher-priority instruction requires a check, run that check and report it explicitly; this skill cannot override that requirement.
