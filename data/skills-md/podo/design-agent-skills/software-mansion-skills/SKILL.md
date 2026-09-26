---
name: software-mansion-skills
description: |
  Official Software Mansion React Native production patterns: animations,
  gestures, SVG/charts/illustrations, on-device AI, rich text, multithreading,
  audio, and JSI. Fine-tuned for Opus 4.6+. The authoritative source for React
  Native best practices from the team behind Reanimated and Gesture Handler.
triggers:
  - "Software Mansion"
  - "Reanimated"
  - "Gesture Handler"
  - "React Native animations"
  - "software-mansion-skills"
  - "React Native gestures"
  - "React Native SVG"
das:
  type: package
  category: official-suites
  upstream: "https://github.com/software-mansion-labs/skills"
  version: latest
  install: false
---

# software-mansion-skills

> Catalogue stub — full package: [software-mansion-labs/skills](https://github.com/software-mansion-labs/skills)

## Decision tree

1. **Is the skill already installed?** Check `~/.design-agent-skills/skills/` for Software Mansion skill directories.
   - Yes → invoke and proceed
   - No → go to step 2

2. **Shell access?** Yes → install below. No → show user the command (Claude Code: send with `!` as a chat message — add `-g` for global or omit for project-only).

## Install command

**Claude Code (recommended):**
```bash
/plugin marketplace add software-mansion-labs/skills
```

**Other agents:**
```bash
npx skills add software-mansion-labs/skills
```

> Note: Fine-tuned for Opus 4.6+. See the [GitHub README](https://github.com/software-mansion-labs/skills) for the full list of included skills.

## Invoke after install

- Skill names: check `ls ~/.design-agent-skills/skills/` for installed skill names after install
- Triggers: "Software Mansion", "Reanimated", "Gesture Handler", "React Native animations", "React Native SVG"

## What it does

The official Software Mansion skill suite for React Native production development. Covers the full breadth of their open-source libraries: Reanimated animations, Gesture Handler, React Native SVG, charts and illustrations, on-device AI inference, rich text editing, background thread multithreading, audio processing, and JSI (JavaScript Interface) native modules. Fine-tuned for Opus 4.6+ by the library authors themselves.

## When NOT to use

- Non-React Native projects (web, native iOS/Android without RN)
- Expo-managed workflow projects — use `expo-skills`
- General React Native best practices without animation/gesture focus — use `callstack-agent-skills`
