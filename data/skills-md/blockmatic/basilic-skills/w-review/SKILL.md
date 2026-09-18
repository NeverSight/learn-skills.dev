---
name: w-review
description: Review a change for evidenced defects and risks without editing it.
disable-model-invocation: true
---

Use the specified diff, branch, PR, or working tree and its intended behavior. Remain read-only unless fixes are also requested.

1. Understand the trigger and expected result before judging the implementation. Read tests to learn which claims are actually exercised.
2. Check the in-scope [review dimensions](references/review-dimensions.md), including docs/README when behavior changed. Concentrate on changed behavior, callers, and failure paths. Skip dimensions that are out of scope and say so.
3. Validate suspected defects with a concrete execution path, failing case, or source evidence. Do not invent timings or vulnerabilities from appearances.
4. Challenge verification claims. Order findings by impact with file/line, trigger, consequence, and smallest useful remedy. An inspection is not proof that tests passed and is not approval to merge.
