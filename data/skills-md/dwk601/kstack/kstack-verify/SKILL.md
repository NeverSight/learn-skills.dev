---
name: kstack-verify
description: Exercise real behavior and retain revision-bound evidence.
disable-model-invocation: true
---

# kstack verify

Shared rules: read `../kstack/SKILL.md` first.

1. Pin the revision and scenario with a concrete pass condition. Find the run recipe in `.kstack/project.json`, docs, scripts, or CI. Prefer existing e2e tests, APIs, and CLI drivers.
2. Use an isolated checkout and instance with its own port, data, and test account. Wait until usable. Never touch production data or edit source as a verification lane.
3. Drive the scenario as a user would. Capture output, screenshots, responses, and side effects. Judge the stated pass condition, not whether the process started.
4. For base/head comparison, run comparable behavior on both. If base lacks the feature, record that fact and verify the added behavior and end state on head. Do not invent a baseline or a ratio between different workloads.
5. Stop only the processes you started, by PID. Retain the evidence outside disposable worktrees.

Report `base/head SHAs | PASS/FAIL/BLOCKED | commands | observations | evidence paths`. Required behavior that cannot run, the wrong interaction method, or inconclusive evidence is BLOCKED. Use N/A only when a check genuinely does not apply, with a reason.

After a successful standalone run, offer to save a missing project recipe. Swarm lanes report it to the coordinator instead of editing project files.
