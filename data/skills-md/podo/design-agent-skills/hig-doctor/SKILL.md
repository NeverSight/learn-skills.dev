---
name: hig-doctor
description: |
  Diagnose Apple HIG compliance issues with targeted guidance and fixes.
  14 specialized skills covering HIG component categories — identifies
  non-compliant patterns and provides specific remediation steps.
triggers:
  - "HIG doctor"
  - "HIG compliance"
  - "Apple HIG audit"
  - "HIG diagnosis"
  - "fix Apple HIG"
das:
  category: visual-components
  upstream: "https://github.com/raintree-technology/hig-doctor"
  version: latest
  install: false
---

# hig-doctor

> Catalogue stub — full package: [raintree-technology/hig-doctor](https://github.com/raintree-technology/hig-doctor)

## Decision tree

Run this to diagnose and fix Apple HIG violations:

1. **Is the HIG Doctor skill already installed?**
   Check: `~/.design-agent-skills/skills/hig-foundations/SKILL.md` exists.
   - Yes → invoke the relevant hig-doctor skill and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
npx skills add raintree-technology/hig-doctor
```

Website: [apple.raintree.technology](https://apple.raintree.technology/)

## Invoke after install

Skills diagnose by component category — invoke the one matching your problem area:
- `hig-components-controls` — button, toggle, slider violations
- `hig-components-layout` — navigation bar, tab bar violations
- `hig-components-menus` — context menu, picker violations
- `hig-components-dialogs` — alert, sheet violations
- `hig-inputs` — text field, form violations
- `hig-foundations` — color, typography, spacing violations

Trigger phrases: "HIG compliance", "Apple HIG audit", "diagnose HIG"

## What it does

HIG Doctor is a multi-skill diagnostic tool for Apple HIG compliance. Each skill covers a category of HIG components, identifies violations in your UI code or design, explains the specific guideline being broken, and provides targeted fixes. Companion to apple-hig-skills (which teaches guidelines) — this diagnoses and repairs.
