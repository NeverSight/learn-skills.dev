---
name: w-debug-browser
description: Reproduce and resolve an authorized browser issue using runtime evidence.
disable-model-invocation: true
---

Use the affected URL, expected interaction, and available browser tools. Inspect the app's README and browser-testing conventions first.

1. Reproduce the interaction and collect relevant DOM, network, and console evidence before adding instrumentation.
2. Trace the failure to its owning client or server boundary. Use the repository logger for necessary temporary traces; avoid secrets in captured output.
3. Apply the smallest authorized fix, then replay the same interaction and relevant failure or empty states.
4. Run affected automated checks and remove temporary traces introduced here. Distinguish runtime evidence from automated results. If tools or credentials block reproduction, report the exact limitation rather than looping without new evidence.
5. Docs: `/w-docs` if behavior or commands changed.
