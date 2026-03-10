---
name: nexus
description: Use this skill when working on Nexus context workflows, CDD specifications, or deriving reusable skills from repository code.
---

# Nexus Skill Hub

This is the top-level Nexus skill. Use it to choose the correct Nexus sub-skill for the task, then read that sub-skill directly.

## Sub-skills

- `context-driven-development`: Defines the canonical CDD format and workflow for context planning, creation, updates, reviews, search, and sync.
  - `context-driven-development/SKILL.md`
- `skill-from-codebase`: Defines how to derive or update a reusable skill from existing code and repository behavior.
  - `skill-from-codebase/SKILL.md`

## Selection Guide

- Use `context-driven-development` for `.nexus/context/` work, context quality/compliance, Next Actions, and dependency semantics.
- Use `skill-from-codebase` when the goal is creating or refreshing a skill from implemented code patterns.
- If both apply, start with `context-driven-development` for scope and constraints, then use `skill-from-codebase` for extraction.
