---
name: bmad-idea
description: Creative Intelligence Suite for AI-driven ideation, design thinking, innovation strategy, problem-solving, and storytelling. 5 named specialist agents with distinct methodologies — no setup required, all workflows available immediately.
allowed-tools: Read Write Bash Grep Glob
metadata:
  tags: bmad, cis, creative, ideation, brainstorming, design-thinking, innovation, problem-solving, storytelling, multi-agent
  platforms: Claude, Gemini, Codex, OpenCode
  keyword: bmad-idea
  version: 1.0.0
  source: user-installed skill
---


# bmad-idea - BMAD Creative Intelligence Suite

## When to use this skill

- Brainstorming ideas using structured creative techniques (36 methods across 7 categories)
- Running a human-centered design thinking process
- Identifying market disruption opportunities or designing new business models
- Diagnosing complex problems using systematic root cause analysis
- Crafting compelling narratives, product stories, or pitches
- Any creative front-end work before structured development begins

---

## Installation

```bash
npx skills add https://github.com/supercent-io/skills-template --skill bmad-idea
```

---

## Creative Workflows

All workflows are available immediately — no sequential phases required.

| Command | Code | Description |
|---------|------|-------------|
| `bmad-cis-brainstorming` | BS | Facilitate a brainstorming session using 36 proven techniques across 7 categories |
| `bmad-cis-design-thinking` | DT | Guide human-centered design through empathy, ideation, and prototyping (5-phase) |
| `bmad-cis-innovation-strategy` | IS | Identify disruption opportunities and design business model innovation |
| `bmad-cis-problem-solving` | PS | Systematic problem diagnosis: root cause analysis and solution planning |
| `bmad-cis-storytelling` | ST | Craft compelling narratives using 25 proven story frameworks |

---

## Slash Commands

| Command | Agent | Shorthand |
|---------|-------|-----------|
| `/cis-brainstorm` | Carson — Brainstorming Coach | `BS` |
| `/cis-design-thinking` | Maya — Design Thinking Coach | `DT` |
| `/cis-innovation-strategy` | Victor — Innovation Strategist | `IS` |
| `/cis-problem-solving` | Dr. Quinn — Creative Problem Solver | `PS` |
| `/cis-storytelling` | Sophia — Storyteller | `ST` |

---

## Specialized Agents

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Carson** 🧠 | Brainstorming Coach | "Yes, and!" energy — 36 ideation techniques, psychological safety |
| **Maya** 🎨 | Design Thinking Coach | Jazz improviser style — empathy mapping, 5-phase facilitation |
| **Victor** ⚡ | Innovation Strategist | Chess grandmaster mindset — JTBD, Blue Ocean Strategy, Disruptive Innovation, BMC |
| **Dr. Quinn** 🔬 | Creative Problem Solver | Sherlock meets scientist — TRIZ, Theory of Constraints, Five Whys, Systems Thinking |
| **Sophia** 📖 | Storyteller *(sidecar memory)* | Master bard style — 25 story frameworks, emotional arc crafting |
| **Caravaggio** 🎨 | Presentation Master | *(in development)* — slide decks, pitch decks, visual hierarchy |

---

## Load an Agent Directly

Start a conversation with a specific agent without triggering a full workflow:

| Command | Agent |
|---------|-------|
| `/cis-agent-brainstorming-coach` | Carson |
| `/cis-agent-design-thinking-coach` | Maya |
| `/cis-agent-innovation-strategist` | Victor |
| `/cis-agent-creative-problem-solver` | Dr. Quinn |
| `/cis-agent-storyteller` | Sophia |
| `/cis-agent-presentation-master` | Caravaggio |

---

## Creative Squad (Team Mode)

Run a full cross-functional creative session with all agents:

```text
creative squad
```

Combines all CIS agents for comprehensive creative development: ideation → design → innovation → problem-solving → narrative.

---

## Visual Tools

Configure image generation preferences on setup:

| Tool | Description |
|------|-------------|
| **Mermaid** | Diagrams in markdown-standard format |
| **Excalidraw** | Editable diagrams and flowcharts |
| **Gemini Nano** | AI image generation via Google Nano |

---

## Quick Reference

| Goal | Command |
|------|---------|
| Generate ideas | `bmad-cis-brainstorming` or `/cis-brainstorm` |
| Design for users | `bmad-cis-design-thinking` or `/cis-design-thinking` |
| Find market gaps | `bmad-cis-innovation-strategy` or `/cis-innovation-strategy` |
| Solve a hard problem | `bmad-cis-problem-solving` or `/cis-problem-solving` |
| Tell a compelling story | `bmad-cis-storytelling` or `/cis-storytelling` |
| Full creative session | `creative squad` |
