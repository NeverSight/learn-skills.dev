---
name: w-test
description: Run the repository test scripts and fix failures until they pass.
disable-model-invocation: true
---

Run the documented test scripts from package.json (filtered to the change when the repo supports it). Fix owning causes. Do not publish.

1. Identify the test command for the affected packages (`pnpm test`, Turbo filters, or the app E2E script). Prefer the narrowest suite that covers the change; use the full suite when the failure is unknown or the user asked for it.
2. Run the command. Capture failing tests, not a paraphrase.
3. Fix one owning cause at a time. Re-run the failed command. Do not weaken assertions or skip tests to obtain a pass. Stop when the suite is green or remaining failures need a human (secrets, env, flaky infra).
4. Docs: `/w-docs` if behavior or commands changed.
