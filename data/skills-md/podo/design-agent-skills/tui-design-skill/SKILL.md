---
name: tui-design-skill
description: |
  Designs clean, professional terminal UIs and CLIs across four ecosystems: Go (Bubble Tea/
  Lipgloss), Rust (Ratatui), Python (Textual), and TypeScript (Ink). Covers layout patterns,
  color systems, keybinding conventions, and framework-specific design patterns.
triggers:
  - "TUI design"
  - "terminal UI"
  - "Bubble Tea"
  - "Ratatui"
  - "Textual Python"
  - "Ink TypeScript"
  - "tui-design-skill"
das:
  category: tui-terminal
  upstream: "https://github.com/gfargo/tui-design-skill"
  version: latest
  install: false
---

# tui-design-skill

> Catalogue stub — full package: [gfargo/tui-design-skill](https://github.com/gfargo/tui-design-skill)

## Decision tree

1. **Is the package already installed?**
   Check: `~/.design-agent-skills/skills/tui-design-skill/SKILL.md` exists.
   - Yes → invoke `tui-design-skill` and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
/plugin marketplace add gfargo/tui-design-skill
```

## Invoke after install

- Skill name: `tui-design-skill`
- Trigger phrases: "TUI design", "terminal UI", "Bubble Tea", "Ratatui", "Textual Python", "Ink TypeScript"

## What it does

Provides design knowledge for building professional terminal user interfaces across four major ecosystems: Go with Bubble Tea and Lipgloss for component-based TUIs, Rust with Ratatui for high-performance terminal apps, Python with Textual for rich TUI applications, and TypeScript/Node.js with Ink for React-style terminal rendering. Covers terminal color systems (true color, 256-color, ANSI), layout composition patterns, keybinding conventions, focus management, and framework-specific component design.

## When NOT to use

- Web UI design — use a frontend-design skill instead
- When you need a specific framework without TUI layout conventions (the skill adds opinionated design patterns)
- Simple CLI argument parsing without interactive UI
