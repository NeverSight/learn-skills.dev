---
name: expo-skills
description: |
  Official Expo skills for working with Expo projects and Expo Application
  Services (EAS). Fine-tuned for Opus models by the Expo team. Covers the
  Expo SDK, EAS Build, EAS Submit, and Expo Router.
triggers:
  - "Expo"
  - "EAS"
  - "expo-skills"
  - "Expo Router"
  - "Expo SDK"
  - "EAS Build"
  - "EAS Submit"
das:
  type: package
  category: official-suites
  upstream: "https://github.com/expo/skills"
  version: latest
  install: false
---

# expo-skills

> Catalogue stub — full package: [expo/skills](https://github.com/expo/skills)

## Decision tree

1. **Is the skill already installed?** Check `~/.design-agent-skills/skills/` for Expo skill directories.
   - Yes → invoke and proceed
   - No → go to step 2

2. **Shell access?** Yes → install below. No → show user the command (Claude Code: send with `!` as a chat message — add `-g` for global or omit for project-only).

## Install command

```bash
npx skills add expo/skills
```

> Fine-tuned for Opus models. See the [GitHub README](https://github.com/expo/skills) for the full list of included skills.

## Invoke after install

- Skill names: check `ls ~/.design-agent-skills/skills/` for installed skill names after install
- Triggers: "Expo", "EAS", "expo-skills", "Expo Router", "Expo SDK", "EAS Build", "EAS Submit"

## What it does

The official Expo skill suite authored by the Expo team, fine-tuned for Opus models. Covers working within the Expo managed and bare workflows, the full Expo SDK API surface, Expo Router (file-based navigation), EAS Build (cloud build service for iOS and Android), and EAS Submit (automated app store submission). The authoritative source for Expo-specific patterns and APIs.

## When NOT to use

- Bare React Native without Expo — use `callstack-agent-skills` or `software-mansion-skills`
- Animation and gesture-heavy work in an Expo project — combine with `software-mansion-skills`
- Mobile UI design work — use `mobile-app-design` or `mobile-app-ui-design`
