---
name: bmad-gds
description: AI-driven Game Development Studio using BMAD methodology. Routes game projects through Pre-production, Design, Architecture, Production, and Game Testing phases with 6 specialized agents. Supports Unity, Unreal Engine, Godot, and custom engines.
allowed-tools: Read Write Bash Grep Glob
metadata:
  tags: bmad, gds, game-development, game-design, gdd, unity, unreal, godot, multi-agent, workflow
  platforms: Claude, Gemini, Codex, OpenCode
  keyword: bmad-gds
  version: 0.1.4
  source: user-installed skill
---


# bmad-gds - BMAD Game Development Studio

## When to use this skill

- Starting a new game project and need a structured concept → production workflow
- Creating a Game Design Document (GDD), narrative design, or technical architecture
- Managing sprints and dev stories for a game team
- Setting up test frameworks for Unity, Unreal Engine, or Godot projects
- Quick prototyping or rapid feature work without full planning overhead
- Reviewing code or running retrospectives after development epics

---

## Installation

```bash
npx skills add https://github.com/supercent-io/skills-template --skill bmad-gds
```

---

## Supported Engines

Unity · Unreal Engine · Godot · Custom/Other

---

## BMAD-GDS Workflow Commands

### Phase 1 — Pre-production

| Command | Description |
|---------|-------------|
| `bmad-gds-brainstorm-game` | Facilitate a game brainstorming session with game-specific ideation techniques |
| `bmad-gds-game-brief` | Create an interactive game brief defining concept and core mechanics |

### Phase 2 — Design

| Command | Description |
|---------|-------------|
| `bmad-gds-gdd` | Generate a Game Design Document: mechanics, systems, progression, implementation guidance |
| `bmad-gds-narrative` | Create narrative documentation: story structure, character arcs, world-building |

### Phase 3 — Technical

| Command | Description |
|---------|-------------|
| `bmad-gds-project-context` | Generate project-context.md for consistent AI agent coordination |
| `bmad-gds-game-architecture` | Produce scale-adaptive game architecture: engine, systems, networking, technical design |
| `bmad-gds-test-framework` | Initialize test framework architecture for Unity, Unreal, or Godot |
| `bmad-gds-test-design` | Create comprehensive test scenarios covering gameplay, progression, and quality |

### Phase 4 — Production

| Command | Description |
|---------|-------------|
| `bmad-gds-sprint-planning` | Generate or update sprint-status.yaml from epic files |
| `bmad-gds-sprint-status` | View sprint progress, surface risks, get next action recommendation |
| `bmad-gds-create-story` | Create a dev-ready implementation story |
| `bmad-gds-dev-story` | Execute a dev story: implement tasks and tests |
| `bmad-gds-code-review` | QA code review for stories flagged Ready for Review |
| `bmad-gds-correct-course` | Navigate major in-sprint course corrections |
| `bmad-gds-retrospective` | Facilitate retrospective after epic completion |

### Game Testing

| Command | Description |
|---------|-------------|
| `bmad-gds-test-automate` | Generate automated game tests for gameplay systems |
| `bmad-gds-e2e-scaffold` | Scaffold end-to-end testing infrastructure |
| `bmad-gds-playtest-plan` | Create a structured playtesting plan for user testing sessions |
| `bmad-gds-performance-test` | Design a performance testing strategy for profiling and optimization |
| `bmad-gds-test-review` | Review test quality and coverage gaps |

### Quick / Anytime

| Command | Description |
|---------|-------------|
| `bmad-gds-quick-prototype` | Rapid prototyping to validate mechanics without full planning overhead |
| `bmad-gds-quick-spec` | Quick tech spec for simple, well-defined features or tasks |
| `bmad-gds-quick-dev` | Flexible rapid implementation for game features |
| `bmad-gds-document-project` | Analyze and document an existing game project |

---

## Specialized Agents

| Agent | Role |
|-------|------|
| `game-designer` | Game concept, mechanics, GDD, narrative design, brainstorming |
| `game-architect` | Technical architecture, system design, project context |
| `game-dev` | Implementation, dev stories, code review |
| `game-scrum-master` | Sprint planning, story management, course corrections, retrospectives |
| `game-qa` | Test framework, test design, automation, E2E, playtest, performance |
| `game-solo-dev` | Full-scope solo mode: quick prototype, quick spec, quick dev |

---

## Typical Workflow

1. Run `bmad-gds-brainstorm-game` → ideate game concept
2. Run `bmad-gds-game-brief` → lock in concept and core mechanics
3. Run `bmad-gds-gdd` → produce full Game Design Document
4. Run `bmad-gds-game-architecture` → define technical architecture
5. Run `bmad-gds-sprint-planning` → break work into sprints and stories
6. Run `bmad-gds-dev-story` per story → implement features
7. Run `bmad-gds-code-review` → quality gate before merge
8. Run `bmad-gds-retrospective` → continuous improvement after each epic

---

## Quick Reference

| Action | Command |
|--------|---------|
| Brainstorm game concept | `bmad-gds-brainstorm-game` |
| Create game brief | `bmad-gds-game-brief` |
| Generate GDD | `bmad-gds-gdd` |
| Define architecture | `bmad-gds-game-architecture` |
| Plan sprint | `bmad-gds-sprint-planning` |
| Check sprint status | `bmad-gds-sprint-status` |
| Create story | `bmad-gds-create-story` |
| Develop story | `bmad-gds-dev-story` |
| Quick prototype | `bmad-gds-quick-prototype` |
