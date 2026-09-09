---
name: callstack-agent-skills
description: |
  Official Callstack React Native skills covering best practices (profiling,
  FPS, re-renders, Turbo Modules), GitHub PR workflows, GitHub Actions build
  artifacts, React Native upgrading templates, and brownfield migration strategy.
triggers:
  - "Callstack"
  - "callstack-agent-skills"
  - "React Native profiling"
  - "Turbo Modules"
  - "brownfield migration"
  - "React Native upgrade"
  - "React Native FPS"
das:
  type: package
  category: official-suites
  upstream: "https://github.com/callstackincubator/agent-skills"
  version: latest
  install: false
---

# callstack-agent-skills

> Catalogue stub — full package: [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills)

## Decision tree

1. **Is the skill already installed?** Check `~/.design-agent-skills/skills/` for Callstack skill directories.
   - Yes → invoke and proceed
   - No → go to step 2

2. **Shell access?** Yes → install below. No → show user the command (Claude Code: send with `!` as a chat message — add `-g` for global or omit for project-only).

## Install command

```bash
/plugin install react-native-best-practices@callstack-agent-skills
```

> See the [GitHub README](https://github.com/callstackincubator/agent-skills) for alternative install methods and the full skill list.

## Invoke after install

- Skill names: check `ls ~/.design-agent-skills/skills/` for installed skill names after install
- Triggers: "Callstack", "React Native profiling", "Turbo Modules", "brownfield migration", "React Native upgrade"

## What it does

Official Callstack React Native skill suite covering production best practices: performance profiling, FPS optimization, eliminating unnecessary re-renders, and building Turbo Modules. Also covers GitHub PR review workflows, GitHub Actions CI/CD for build artifacts, version upgrade templates and strategies, and brownfield migration (embedding React Native into existing native iOS/Android apps).

## When NOT to use

- Expo projects — use `expo-skills`
- Animation-heavy and gesture-heavy work — use `software-mansion-skills`
- Figma or UI design work — use `mobile-app-design` or `work-with-design-systems`
