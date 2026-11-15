---
name: contributing-to-superpowers
description: Use when editing skills/, agents/, rules/ or .github/ in the superpowers-antigravity repository
---

# Contributing to superpowers-antigravity

This repository is a native Antigravity port of upstream superpowers. Three rules govern every edit under `skills/`, `agents/`, `rules/` and `.github/`.

**The purity law.** Skill, agent and rule text names only Antigravity's own tools and features: no other agent product, no other product's tool names, no tool-mapping file. `.github/` names no other agent product either. The banned vocabulary is `tests/antigravity/purity-patterns.txt`; the tool names skill text may use are the baseline class in `tests/antigravity/known-tools.txt`.

**R3: verbatim port or recorded divergence.** Text ported from upstream stays word for word. Any change to it is a divergence, recorded in the spec and the release notes of the change that makes it.

**R6: shell neutrality.** Skill text works under any shell Antigravity's command tool runs: prefer native tools, give commands that behave the same in every shell, and invoke a bundled script through its interpreter, never by its bare path.

Before you report an edit done, run `bash tests/run-tests.sh` from the repository root (Git Bash on Windows) and fix every FAIL. A SKIP is not a pass.
