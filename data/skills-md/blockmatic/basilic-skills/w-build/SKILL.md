---
name: w-build
description: Implement an agreed task incrementally and verify the result.
disable-model-invocation: true
---

Use an existing plan or a sufficiently clear implementation request. Read repository instructions, affected README/scripts, matching rules and skills, and technical docs. Resolve consequential decisions from `PRODUCT.md` and matching docs; ask a human for product scope, secrets, or destructive operations. Do not commit.

1. Inspect the working tree and identify the files owned by this task. State the acceptance conditions; preserve unrelated changes.
2. Implement one complete slice using existing packages and patterns. Change owning schemas and run documented generators instead of editing generated clients or migrations.
3. Run the smallest existing check for this change. A reproducible logic defect should have a regression check; use TDD when requested or required by the repository, not as a ritual for prose edits. Never the full pre-push suite (`/w-ship` owns that).
4. Investigate failed checks before building dependent work. Separate regressions caused here from pre-existing or environmental failures; never weaken checks to obtain a pass.
5. If behavior, commands, or conventions changed, update matching MDX and nearest README (`PRODUCT.md` only if product facts changed); otherwise one line why not.
