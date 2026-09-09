---
name: design-sprint
description: |
  Deeply researches a codebase, designs a feature through iterative brainstorming
  and annotation cycles, then decomposes it into an implementable issue hierarchy
  (parent + sub-issues with dependencies) on GitHub or GitLab. Hard gates between
  phases ensure research happens before design, and design is complete before
  implementation. Each sub-issue is scoped to require zero creative decisions.
triggers:
  - "design sprint"
  - "feature design sprint"
  - "design and decompose"
  - "design-sprint"
  - "design to issues"
  - "feature breakdown issues"
das:
  type: package
  category: product-pm
  upstream: "https://github.com/aoshimash/skills"
  version: latest
---

# design-sprint

> Catalogue stub — full skill: [aoshimash/skills](https://github.com/aoshimash/skills)

## Install the full skill

Install via Claude Code plugin:

```bash
/plugin install aoshimash/skills
```

Or clone directly:

```bash
# Global
git clone https://github.com/aoshimash/skills /tmp/aoshimash-skills
cp -r /tmp/aoshimash-skills/plugins/aoshimash-skills/skills/design-sprint \
  ~/.agents/skills/design-sprint

# Project
cp -r /tmp/aoshimash-skills/plugins/aoshimash-skills/skills/design-sprint \
  .agents/skills/design-sprint
```

## What it does

A structured 4-phase workflow that bridges design and implementation:

| Phase | Output |
|---|---|
| **0 — Setup** | Detect issue tracker (GitHub/GitLab), confirm scope |
| **1 — Research** | Deep codebase reading → written research artifact (not verbal summary) |
| **2 — Design** | Brainstorm feature → local markdown plan → annotation cycles with user |
| **3 — Decompose** | Plan → parent issue + sub-issues, each implementable with zero creative decisions |
| **4 — Create** | Push issue hierarchy to tracker with dependencies |

Core principles:
- Research before design — never design without a written research artifact
- Plan as shared mutable state — user annotates inline in the markdown file
- Implementation must be boring — if a sub-issue requires design judgment, decompose further
- Hard gates — no phase proceeds without explicit user approval

## When NOT to use

- Design sprint workshop facilitation (Crazy 8s, HMW, voting) → use `pm-skills` (Design Sprint section)
- PM discovery without code → use `deanpeters-pm-skills` or `pm-skills`
- Feature planning without issue creation → use `plan-design-review`
