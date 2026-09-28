---
name: service-blueprint
description: |
  Generate professional service blueprints (NN/g, GDS, Practical Service Design): the five
  swim lanes, lines of interaction/visibility/internal-interaction, plus a JSON schema and render pipeline.
triggers:
  - "service blueprint"
  - "service design blueprint"
  - "frontstage backstage"
  - "service delivery map"
das:
  type: package
  category: design-review
  upstream: "https://github.com/j-clegg/service-blueprint-skill"
  version: latest
---

# service-blueprint

> Catalogue stub — full package: [j-clegg/service-blueprint-skill](https://github.com/j-clegg/service-blueprint-skill)

## Install the full skill

Via skills CLI:

```bash
npx skills add j-clegg/service-blueprint-skill -g -y    # global — all projects
npx skills add j-clegg/service-blueprint-skill -y       # project — this project only
```
> **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.

## What it does

A ~28.7KB service-blueprint package: sourced methodology (METHODOLOGY.md), a machine-readable blueprint SCHEMA.md, and a RENDERING.md HTML/Mermaid output pipeline. Maps user actions, frontstage, backstage, and support processes across the lines of interaction/visibility/internal-interaction, with timed facilitation and moments-of-truth analysis. Web research picked this over Owl’s (good but lighter) service-blueprint skill.

## When NOT to use

- Single-user emotional journey only → use a journey-map skill
- High-level UX strategy → use `design-consultation`
