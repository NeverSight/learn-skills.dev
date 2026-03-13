---
name: game-design-compass
description: Comprehensive game design planning skill that unifies role-based, genre-based, and platform-based design workflows into one system. Use when planning game concepts, writing or refining GDD sections, designing core loops, progression, balance, economy, narrative, level flow, UI/UX, monetization, or adapting design decisions for mobile, PC, console, web/HTML5, and VR/AR. Especially useful when the request needs structured design outputs with checklists, KPIs, risks, and implementation-ready handoff artifacts.
---

# Game Design Compass

## Overview
Use this skill as a single design planning hub that routes requests across three axes:
1. `Role`: who is designing and what ownership the role has.
2. `Genre`: what player expectation and loop structure applies.
3. `Platform`: what constraints and UX assumptions must shape the plan.

Always convert advice into concrete planning artifacts.

## Routing Workflow
1. Identify the request scope.
- If the user asks for responsibility, process, handoff, or design documentation ownership, start with `Role`.
- If the user asks for gameplay identity, retention loops, progression, or expected player behavior, start with `Genre`.
- If the user asks for controls, sessions, compliance, performance, or store/certification concerns, start with `Platform`.
2. Load one primary reference file.
3. Load up to two supporting references from other axes only when needed.
4. Produce a structured output with measurable validation criteria.

## Output Standard
Return these sections in order:
1. `Objective`
2. `Assumptions`
3. `Design Decision`
4. `Tradeoffs`
5. `Validation Metrics`
6. `Deliverables`

## Axis A: Role References
- `references/role/pd-lead.md`
- `references/role/system.md`
- `references/role/balance.md`
- `references/role/uiux.md`
- `references/role/scenario.md`
- `references/role/level.md`
- `references/role/monetization.md`

## Axis B: Genre References
- `references/genre/rpg.md`
- `references/genre/action.md`
- `references/genre/sng.md`
- `references/genre/fps-tps.md`
- `references/genre/strategy.md`
- `references/genre/puzzle-casual.md`
- `references/genre/simulation.md`
- `references/genre/sports-racing.md`
- `references/genre/roguelike.md`
- `references/genre/survival-horror.md`
- `references/genre/moba-br.md`

## Axis C: Platform References
- `references/platform/mobile.md`
- `references/platform/pc.md`
- `references/platform/console.md`
- `references/platform/web-html5.md`
- `references/platform/vr-ar.md`

## Integration Rules
1. Resolve platform constraints before locking core loops.
2. Resolve monetization and economy boundaries before tuning progression speed.
3. Keep narrative, level, and UI decisions consistent with loop pacing.
4. Add one KPI minimum for each major design claim.
5. Add one risk and one mitigation for each major subsystem.

## Quality Gate Checklist
- Is the output actionable by another discipline without extra explanation?
- Are tradeoffs explicit rather than implied?
- Are assumptions testable?
- Is scope control documented?
- Is player value and business value both addressed?

## Source Corpus
Use these repository sources as grounding references:
- `resources/game_design_books/The_Art_of_Game_Design_Lenses_Summary.md`
- `resources/game_design_books/GDD_Template_Markdown.md`
- `resources/game_design_books/Standard_GDD_Template.md`
- `resources/game_design_books/balance_economy/Game_Balance_Economy_Guide.md`
- `resources/game_design_books/combat_system/Combat_System_Design_Guide.md`
- `resources/game_design_books/narrative/Narrative_Design_Guide.md`
- `resources/game_design_books/sound/Audio_Design_Guide.md`
- `resources/game_design_books/ui_ux/Laws_of_UX_Summary.md`

## Cross-Skill Feasibility References
Use implementation-oriented skills only for feasibility checks after planning:
- `[Reference: game-development/game-design]`
- `[Reference: game-development/mobile-games]`
- `[Reference: game-development/pc-games]`
- `[Reference: game-development/web-games]`
- `[Reference: game-development/multiplayer]`
- `[Reference: game-development/vr-ar]`
- `[Reference: game-development/game-art]`
- `[Reference: game-development/game-audio]`
