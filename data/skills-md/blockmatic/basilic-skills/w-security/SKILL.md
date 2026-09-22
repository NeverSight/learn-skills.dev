---
name: w-security
description: Review the change or tree against repository security docs and existing checks.
disable-model-invocation: true
---

Find security defects relative to repository security docs and existing scanners. Do not invent CORS, encryption, password, or header policy. Stay report-only unless the user asked to fix.

1. Read the repository security docs. If missing, stop and ask; do not invent a bar.
2. Spawn 2–3 read-only explorers on authn/authz, secret/exposure, and input validation for the changed paths. Reconcile trigger and consequence yourself.
3. Validate each suspected issue with a trigger and consequence. Skip invented CVEs and timings.
4. If authorized, run existing security scripts or CI jobs from the docs or package.json. Record passed, failed, or not run.
5. If fixes are authorized, change the owning cause. Policy changes need a human. Docs: `/w-docs` if behavior or commands changed.
