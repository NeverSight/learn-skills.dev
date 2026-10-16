---
name: kstack-understand
description: Explain how and why code works, with evidence.
disable-model-invocation: true
---

# kstack understand

Shared rules: read `../kstack/SKILL.md` first.

Read only. Answer the question asked, at the depth asked.

1. Find the entry points, then follow the real path: callers, data shapes, state, side effects, config, tests.
2. For "why", read the history of those lines: `git log -L` or `git blame`, the commits and PRs that shaped them (`gh pr view`), and linked issues.
3. Separate what you saw from what you infer. Name what you could not find.

Output: overview, how it works (the path in order), where things live (`file:line`), gotchas, open questions. Skip sections with nothing to say.
