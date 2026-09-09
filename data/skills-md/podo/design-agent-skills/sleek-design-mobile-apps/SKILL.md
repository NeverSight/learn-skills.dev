---
name: sleek-design-mobile-apps
description: |
  AI-powered mobile app design integrated with the Sleek platform — design
  screens, create projects, and manage assets via natural language. Requires
  a Sleek Pro account and API key.
triggers:
  - "Sleek design"
  - "sleekdotdesign"
  - "sleek-design-mobile-apps"
  - "Sleek Pro"
  - "Sleek platform"
das:
  type: platform
  category: visual-components
  upstream: "https://github.com/sleekdotdesign/agent-skills"
  version: latest
  install: false
---

# sleek-design-mobile-apps

> Catalogue stub — full platform skill: [sleekdotdesign/agent-skills](https://github.com/sleekdotdesign/agent-skills)

## Decision tree

1. **Is the skill already installed?** Check `~/.design-agent-skills/skills/sleek-design-mobile-apps/` for skill content.
   - Yes → invoke and proceed
   - No → go to step 2

2. **Do you have a Sleek Pro account and API key?**
   - No → this skill requires a Sleek Pro account. Visit [sleek.design](https://sleek.design) to sign up.
   - Yes → install below

## Install command

```bash
npx skills add sleekdotdesign/agent-skills -s sleek-design-mobile-apps
```

> Note: A Sleek Pro account and configured API key are required. See the [GitHub README](https://github.com/sleekdotdesign/agent-skills) for API key setup.

## Invoke after install

- Skill name: `sleek-design-mobile-apps`
- Triggers: "Sleek design", "sleekdotdesign", "Sleek Pro"

## What it does

Natural-language interface to the Sleek design platform for mobile app design. Design screens, create and manage Sleek projects, and handle design assets through conversation. Integrates directly with your Sleek Pro workspace.

## When NOT to use

- Without a Sleek Pro account — use `mobile-app-design` or `mobile-app-ui-design` instead
- General mobile design guidance not requiring the Sleek platform
- Figma-based workflows — use `work-with-design-systems` or `claude2figma`
