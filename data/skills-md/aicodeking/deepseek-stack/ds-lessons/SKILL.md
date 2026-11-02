---
name: ds-lessons
description: "Find mistakes agents keep repeating in this repo and turn each into structure that blocks it, preferring types over lint over tests over docs, plus an end-of-session reflection. Use after a user correction, when the same fix comes up twice, at the end of a long session, or for /ds-lessons."
---

# ds-lessons

An instruction an agent can skip is a wish. Make repeated mistakes fail loudly instead.

## Steps

1. Gather mistakes. Read the current session, recent commits, reverts, review comments, agent instruction files and workaround comments. Group them into classes. A class counts once it happened twice.
2. For each class, pick the highest level that works:
   1. Structure: one owner per piece of state, one supported way per task, hidden internals, delete old patterns an agent would copy.
   2. Types: make the bad state impossible to write.
   3. Lint or CI check: the error message names the right file, type or function to use. If the bad pattern is already common, fail only on new additions.
   4. Test: checks behavior, not internals.
   5. Docs or agent rules: only for judgment calls that cannot be checked. Add a short example of the failure.
3. Fix the most frequent classes now, one commit each.
4. Prove each new check. Re-introduce a real past mistake, run the check, and show it fails. Then remove it and show it passes.
5. Keep a table in the agent instruction file: rule, and what enforces it. If a rule already existed but nothing enforced it, treat it as a repeat and enforce it now.
6. End-of-session reflection: list what went wrong, what took extra loops and what the user corrected. Route each item to a check, a skill edit or a rule. Drop one-off issues.

## Stop when

- Each chosen class has an enforcement that you showed failing on a real mistake.
- Or you have handled the top three classes this session. Note the rest.

## Rules

- If the fix is structural, do not also add prose. The prose was the symptom.
- Report each class with evidence, the level chosen, and why a higher level did not work.
