---
name: game-architect
description: READ this skill when designing or planning any game system architecture — including combat, skills, AI, UI, multiplayer, narrative, or scene systems. Contains paradigm selection guides (DDD / Data-Driven / Prototype), system-specific design references, and mixing strategies. Works as a domain knowledge plugin alongside workflow skills (OpenSpec, SpecKit) or plan mode of an agent.
---

# Game Architect Skill

Game architecture domain knowledge reference. Provides paradigm selection, system design references for game project architecture.

> [!NOTE]
> This skill contains **domain knowledge only**, not a workflow. Pair it with a workflow skill (e.g., OpenSpec, SpecKit) or an agent's plan mode for structured design flow.

## Usage Modes

### With Workflow Skill (Recommended)

When used with a workflow skill (e.g., OpenSpec, SpecKit) or in the plan mode of an agent, this skill serves as a domain knowledge plugin:

- **During requirements/spec phases**: Consult the Paradigm Selection Guide and System-Specific References to inform architectural decisions
- **During design/planning phases**: Use the Reference Lookup Guide below to read relevant `references/` documents

### Standalone

A lightweight `workflow-standalone.md` is also available as a self-contained design pipeline if needed.

### Knowledge Mode (Query)

When user requests to query knowledge for game architecture, this skill provides a reference lookup guide to relevant `references/` documents based on the task.

---

## Reference Lookup Guide

When designing game architecture, read the relevant `references/` documents based on the task:

### Architecture References

| When | Read |
|------|------|
| Always (high-level structure) | `references/macro-design.md` |
| Always (core principles) | `references/principles.md` |
| Requirement analysis | `references/requirements.md` |
| Choosing DDD paradigm | `references/domain-driven-design.md` |
| Choosing Data-Driven paradigm | `references/data-driven-design.md` |
| Choosing Prototype paradigm | `references/prototype-design.md` |
| Evolution & extensibility review | `references/evolution.md` |
| Performance optimization needed | `references/performance-optimization.md` |
| Multiplayer support needed | `references/system-multiplayer.md` |

For system-specific design, see the System-Specific References table below.

### System-Specific References

| System Category | Reference |
|----------------|-----------|
| Foundation & Core (Logs, Timers, Modules, Events, Resources, Audio, Input) | `references/system-foundation.md` |
| Time & Logic Flow (Update Loops, Async, FSM, Command Queues, Controllers) | `references/system-time.md` |
| Combat & Scene (Scene Graphs, Spatial Partitioning, ECS/EC, Loading) | `references/system-scene.md` |
| UI & Modules (Modules Management, MVC/MVP/MVVM, UI Management, Data Binding, Reactive) | `references/system-ui.md` |
| Skill System (Attribute, Skill, Buff) | `references/system-skill.md` |
| Action Combat System (HitBox, Damage, Melee, Projectiles) | `references/system-action-combat.md` |
| Narrative System (Dialogue, Cutscenes, Story Flow) | `references/system-narrative.md` |
| Game AI System (Movement, Pathfinding, Decision Making, Tactical) | `references/system-game-ai.md` |
| Multiplayer System (Client-Server, Sync Models, Distributed Server, AOI, Communication) | `references/system-multiplayer.md` |
| Algorithm & Data Structures (Pathfinding, Search, Physics, Generic Solver) | `references/algorithm.md` |

---

## Paradigm Selection Guide

| Paradigm | KeyPoint | Applicability Scope | Examples | Reference |
| :--- | :--- | :--- | :--- | :--- |
| **Domain-Driven Design (DDD)** | OOP & Entity First | High Rule Complexity. <br> Rich Domain Concepts. <br> Many Distinct Entities. | Core Combat Logic, Physics Interactions, Damage/Buff Rules, Complex AI Decision. | `references/domain-driven-design.md` |
| **Data-Driven Design** | Data Layer First | High Content Complexity. <br>  Flow Orchestration. <br> Simple Data Management. | **Content**:  Quests, Level Design.<br>**Flow**: Tutorial Flow, Skill Execution, Narrative.<br>**Mgmt**: Inventory, Shop, Mail, Leaderboard. | `references/data-driven-design.md` |
| **Use-Case Driven Prototype** | Use-Case Implementation First | Rapid Validation | Game Jam, Core Mechanic Testing. | `references/prototype-design.md` |

### Mixing Paradigms

Most projects mix paradigms:
1.  **Macro Consistency**: All modules follow the same Module Management Framework.
2.  **Domain for Core Entities & Rules**: Use DDD for systems with high rule complexity, rich domain concepts, and many distinct entities (e.g., Combat Actors, Damage Formulas, AI Decision).
3.  **Data for Content, Flow & State**: Use Data-Driven for expandable content (Quests, Level Design), flow orchestration (Tutorial, Skill Execution, Narrative), and simple data management (Inventory, Shop).
4.  **Hybrid Paradigms**:
    - 4.1 **Entities as Data**: Domain Entities naturally hold both data (fields) and behavior (methods). Design entities to be serialization-friendly (use IDs, keep state as plain fields) so they serve both roles without a separate data layer.
    - 4.2 **Flow + Domain**: Use data-driven flow to orchestrate the sequence/pipeline, domain logic to handle rules at each step. E.g., Skill System: flow drives cast→channel→apply, domain handles damage calc and buff interactions.
    - 4.3 **Separate Data/Domain Layers**: Only when edit-time and runtime representations truly diverge. Use a Bake/Compile step to bridge them. E.g., visual node-graph editors, compiled assets.
5.  **Paradigm Interchangeability**: Many systems can be validly implemented with either paradigm. E.g., Actor inheritance hierarchy (Domain) ↔ ECS components + systems (Data-Driven); Buff objects with encapsulated rules (Domain) ↔ Tag + Effect data entries resolved by a generic pipeline (Data-Driven). See **Selection Criteria** table above for trade-off signals.
6.  **Integration**: Application Layer bridges different paradigms.

### Selection Criteria

When both DDD and Data-Driven fit, use these signals:

| Signal | Favor DDD | Favor Data-Driven |
|--------|-----------|-------------------|
| Entity interactions | Complex multi-entity rules (attacker × defender × buffs × environment) | Mostly CRUD + display, few cross-entity rules |
| Behavior source | Varies by entity type, hard to express as pure data | Driven by config tables, designer-authored content |
| Change frequency | Rules change with game balance iterations | Content/flow changes far more often than logic |
| Performance profile | Acceptable overhead for rich object graphs | Needs batch processing, cache-friendly layouts |
| Networking | Stateful objects acceptable | Flat state snapshots preferred (sync, rollback) |
| Team workflow | Programmers own the logic | Designers need to iterate without code changes |

---
