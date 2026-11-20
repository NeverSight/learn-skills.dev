---
name: root-cause-fix
description: "Apply when something fails: a bug, a red check, a flaky test, or an agent that goes in circles."
disable-model-invocation: true
license: MIT
compatibility: "No tools needed."
---

# Root-cause-fix

Fix the first wrong decision, not the place where the failure showed.

- Reproduce it, on the real surface when you can. Read the actual state. Do not guess from the code.
- Ask what changed. Compare with the last version that worked. Check whether the base is already broken before you blame the change.
- Ask "why" until the answer is a wrong decision in the code or in the design. A guard, a retry, a fallback value, a swallowed error or a poll at the place of the symptom hides the fault, unless the state that it handles is legitimate.
- Fix the pattern. Find every place with the same fault.
- When two fixes that share one assumption fail, the assumption is wrong. Test it directly, or give the problem to a fresh reader with no context.
- Say the cause in one sentence. If you cannot, you have not found it.
