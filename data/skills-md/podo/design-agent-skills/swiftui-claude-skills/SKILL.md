---
name: swiftui-claude-skills
description: |
  AI-swarm verified SwiftUI skills for iOS 26 Liquid Glass, animations, and UI patterns.
  Verified against WWDC 2025 docs and Xcode 26.3, current through iOS 26.4 RC. Different
  from swiftui-patterns which focuses on general SwiftUI best practices.
triggers:
  - "SwiftUI iOS 26"
  - "swiftui-claude-skills"
  - "WWDC 2025 SwiftUI"
  - "Xcode 26"
  - "199-biotechnologies"
das:
  category: visual-components
  upstream: "https://github.com/199-biotechnologies/swiftui-claude-skills"
  version: latest
  install: false
---

# swiftui-claude-skills

> Catalogue stub — full package: [199-biotechnologies/swiftui-claude-skills](https://github.com/199-biotechnologies/swiftui-claude-skills)

## Decision tree

1. **Is the package already installed?**
   Check: `~/.design-agent-skills/skills/swiftui-claude-skills/SKILL.md` exists.
   - Yes → invoke `swiftui-claude-skills` and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
npx skills add 199-biotechnologies/swiftui-claude-skills
```

## Invoke after install

- Skill name: `swiftui-claude-skills`
- Trigger phrases: "SwiftUI iOS 26", "swiftui-claude-skills", "WWDC 2025 SwiftUI", "Xcode 26", "199-biotechnologies"

## What it does

Provides AI-swarm verified SwiftUI knowledge current through iOS 26.4 RC, verified against WWDC 2025 session documentation and tested in Xcode 26.3. Covers iOS 26 Liquid Glass UI patterns, the updated SwiftUI animation system, new iOS 26 UI components and modifiers, and general best-practice UI patterns. The AI-swarm verification process cross-checks API details against multiple sources to reduce hallucination risk on rapidly-changing Apple APIs.

## When NOT to use

- General SwiftUI without iOS 26 specifics — use swiftui-patterns instead
- Liquid Glass only, without broader SwiftUI — use liquid-glass-skill for a focused scope
- Android or cross-platform mobile — use mobile-app-design instead
