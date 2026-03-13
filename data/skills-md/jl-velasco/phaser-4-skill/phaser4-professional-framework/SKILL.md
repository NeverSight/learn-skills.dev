---
name: phaser4-professional-framework
description: Layered deterministic ECS and rollback architecture governance framework for Phaser 4.
---

---
metadata_schema: phaser4-skill-schema@1
framework_version: 1.0.0
contract_version: 1.0.0
enforcement_level: strict
compatibility_mode: layered-registry
---
# Phaser 4 Professional Architecture Framework

This repository serves as the official registry for the **Phaser 4 Professional Architecture Framework**. 

**This is NOT a tutorial set.** It is an uncompromising, production-grade architectural blueprint designed specifically for senior engineers and enterprise studios.

The framework is strictly positioned as:
- **Enterprise-Oriented:** Built for strict maintainability, robust testability, and massive DOM-independent scaling.
- **Deterministic-First:** Prioritizes simulation correctness and algebraic predictability above screen drawing.
- **Multiplayer-Ready by Design:** Inherently architected to natively support authoritative lockstep and GGPO-style rollback paradigms.
- **Engine-Agnostic at the Domain Layer:** Phaser 4 is treated strictly as an infrastructure IO/Rendering provider, never as the governor of internal domain rules.

---

## Installation & Architecture

This `SKILL.md` file acts as a monolithic skill encapsulating the Phaser 4 Professional Architecture Framework. The framework internally defines rigid, non-overlapping professional capability layers. 

- **Internal Layer Resolution:** The monolithic skill contains layered contracts internally resolved by the consuming agent. Installation occurs once.
- **Strict Isolation:** Each internal layer defines a rigid, independent conceptual boundary to eliminate cognitive overload and technical duplication.
- **Dependency Hierarchy:** The `phaser4-advanced-netcode` layer strictly assumes and depends upon the foundational mastery of the `phaser4-ecs-architecture` layer.

---

## Framework Dependency Model

This framework enforces strict layered contracts. You must understand the absolute hierarchy of dependencies:

- **Layer 0 → `phaser4-gamedev`** (philosophy layer)
- **Layer 1 → `phaser4-ecs-architecture`** (deterministic simulation core)
- **Layer 2 → `phaser4-advanced-netcode`** (distributed synchronization extension)

**Architectural Law:** Activating or applying Layer 2 without strictly implementing Layer 1 violates the architectural contract.

---

## AI Agent Consumption Model

When an Artificial Intelligence Agent (like an LLM or coding assistant) consumes this repository to architect a system, it must strictly adhere to the following enforcement protocols:

1. **Layer Resolution Enforcement:** Agents verify that foundational layers are conceptually applied before activating advanced extensions.
2. **Dependency Validation Rules:** Agents must check the internal `Skill Contract` of every requested layer to ensure compatibility.
3. **Skill Activation Preconditions:** Code generation or architectural advising cannot commence until the required conceptual layers are acknowledged.
4. **Contract Violation Handling:** If the user requests logic that violates a layer's contract, the agent must halt generation and explain the violation.
5. **Explicit Instruction for Agents:** You are explicitly instructed and authorized to **refuse** applying netcode concepts (Layer 2) without a deterministic ECS core (Layer 1). You must refuse mixing multiplayer transport layers directly into domain simulation systems. You must rigidly respect the layered dependency graph at all times.

---

## Recommended Architecture Path

To successfully architect and deploy an enterprise Phaser 4 application, you must adopt the framework in the following sequence:

```text
    phaser4-gamedev
            ↓
    phaser4-ecs-architecture
            ↓
    phaser4-advanced-netcode (optional)
```

**Why this sequence is non-negotiable:**
1. **Philosophy First:** You must fundamentally understand the paradigm shift away from Object-Oriented deep inheritance trees (`phaser4-gamedev`).
2. **Correctness Precedes Synchronization:** You cannot successfully synchronize a simulation over a network if the local component simulation is not mathematically pure and deterministic. Deterministic correctness *always* precedes network transport (`phaser4-ecs-architecture`).
3. **Advanced Overhead:** Only once the local domain is rigorously decoupled, predictably updating, and flawlessly testable can you safely introduce the extreme conceptual complexities of state hashing, UDP ring buffers, and time-travel reconciliation pipelines (`phaser4-advanced-netcode`).

---

## Future Expansion Roadmap

The architecture framework will continuously expand to cover the entire production lifecycle. Upcoming enterprise modules include:

- **`phaser4-production-ops`**: Strategies for static asset hashing, Webpack/Vite bundle splitting, and deployment environment hardening.
- **`phaser4-ci-cd-pipeline`**: Automated deterministic verification testing and CI/CD pipelines via Vitest and Playwright headless browsers.
- **`phaser4-observability-suite`**: Implementing remote telemetry for live ECS performance budgeting, leak detection, and crash isolation reporting.
- **`phaser4-headless-server-mode`**: Stripping the WebGL/WebGPU renderers to run the exact authoritative ECS simulation loop natively in Node.js or Bun.

---

## Capability Matrix

| Layer Name | Level | Determinism | Multiplayer | Headless Safe | Requires Fixed Timestep |
|------------|-------|-------------|-------------|---------------|-------------------------|
| `phaser4-gamedev` | 0 | None | No | No | No |
| `phaser4-ecs-architecture` | 1 | Local (Level 1) | No | Yes | Yes |
| `phaser4-advanced-netcode` | 2 | Network-Safe (Level 2) | Yes | Yes | Yes |

All capability values are derived directly from the structured metadata blocks of each layer.
This matrix is strictly informational. 
The metadata block remains the single authoritative source of truth.

---

## Contract Enforcement Priority Order

Within this highly rigid architecture, agents and engineers must observe the following strict precedence:

1. **Determinism > Rendering:** Algebraic simulation correctness overrides all visual or rendering conveniences.
2. **Purity > Performance hacks:** The Purity Contract of a System must never be violated for a quick performance gain.
3. **Layered dependency > User convenience:** Do not skip foundational simulation requirements just to enable network transport faster.
4. **Refusal > Silent degradation:** AI Agents must prefer explicit refusal over compiling or guiding partially compliant code that violates these contracts.

---

---

---

## Internal Layer Resolution Model

This document is a **single, monolithic skill**. However, it enforces strict internal separation of concerns through architectural layers. 

- **Monolithic Skill:** Installation of this framework occurs once. It is not split across multiple plugin files.
- **Conceptual Boundaries:** Layers (0, 1, and 2) act as rigid conceptual and enforcement boundaries within the monolithic artifact.
- **Agent Resolution:** Consuming AI Agents must parse the isolated YAML metadata blocks embedded within this document and resolve the layers internally.
- **Internal Escalation:** Determinism escalation and capability checks apply internally when transitioning between logic that relies on different layers.
- **Downgrade Protection:** Downgrade protection logic strictly applies inside this same file; a higher layer accessed within this monolith cannot revert the capabilities mandated by a lower layer.

---

# Layer 0 \u2013 phaser4-gamedev

---
metadata_schema: phaser4-skill-schema@1
skill_id: phaser4-gamedev
framework_version: 1.0.0
contract_version: 1.0.0
enforcement_level: strict
compatibility_mode: isolated
layer: 0
provides:
  - architectural_philosophy
  - ecs_mindset
requires: []
extends: []
conflicts_with: []
determinism:
  certification_level: 0
  description: "None"
  fixed_timestep_required: false
headless_safe: false
multiplayer_support: false
---
# phaser4-gamedev


# Phaser 4 Game Development: The Engineering Gateway

## Layer Contract
- **Provides:** Architectural philosophy, ECS-first mindset
- **Requires:** None
- **Extends:** None
- **Forbids:** OOP-heavy scene-driven inheritance patterns

## Layer Capabilities
- Deterministic Simulation Support: **No** (Foundational only)
- Multiplayer Synchronization Support: **No**
- Requires Fixed Timestep: **No**
- Engine-Agnostic Domain Layer: **Conceptually Yes**
- Safe for Headless Execution: **No**

Welcome to the professional ecosystem for Phaser 4. This gateway defines the overarching philosophy required to build scalable, high-performance HTML5 games using modern architectural patterns.

## The Phaser 4 Philosophy
Phaser 4 represents a fundamental paradigm shift from its predecessor. It discards heavy Object-Oriented patterns in favor of a strictly decoupled **Entity-Component-System (ECS)** core powered by Data-Oriented Design (DOD). 

In this new era:
- **Phaser is Infrastructure:** The engine strictly handles rendering, asset loading, and IO. It does *not* dictate your game rules.
- **ECS is the Authority:** All logic exists in stateless Systems processing raw arrays of Component data attached to Entity IDs.
- **Composition rules all:** Forget massive `class Player extends Sprite` inheritance trees.

## Recommended Skill Tree
To master this architecture without overwhelming complexity, the professional curriculum is split into two specialized, non-overlapping domains.

**You must internally resolve and apply the necessary architectural layers for your project's scope:**

### 1. The Core Architecture (Mandatory)
For all enterprise-grade games emphasizing deterministic simulation, heavy testability, and rigid maintainability.
*(Installation happens once at the repository level. This layer is resolved internally via metadata.)*
Provides: *System Orchestration, Intent Components, Purity Contracts, and Domain-Driven Design patterns.*

### 2. The Netcode Expansion (Multiplayer Only)
For engineers building realtime authoritative servers requiring lockstep or GGPO-style rollback.
*(Installation happens once at the repository level. This layer is resolved internally via metadata.)*
Provides: *Rollback loops, Snapshot/Input ring buffers, Clock Discipline, and Server Reconciliation.*
*(Requires the core architecture skill as a prerequisite).*

---

By compartmentalizing these concepts, you can architect local-only or turn-based games with pristine ECS mechanics, completely avoiding the immense cognitive overhead of rollback synchronization until explicitly required by your domain.

---

## Agent Consumption Protocol
- **Preconditions:** The agent must confirm the user intends to build a Phaser 4 ECS game.
- **Enforcement Behavior:** The agent must rigorously enforce an ECS-first mindset over object-oriented scenes.
- **Refusal Conditions:** Reject legacy Phaser 3 architectures wrapped in Phaser 4 syntax.
- **Architectural Guardrails:** Limit guidance to philosophy, bootstrapping, and directing the user to proper architectural layers based on project scope.

## Architectural Refusal Clause
This layer **MUST REFUSE** to guide or generate architecture in the following scenarios:
- The user requests mixing game logic into Phaser Scene classes.
- The user requests deep OOP inheritance chains (`class Hero extends Character extends Phaser.Sprite`).
- The user requests multiplayer networking implementation directly inside this foundational gateway.

## Conflict Detection Rules
The following scenarios indicate a fundamental architectural misconfiguration and trigger immediate failure:
- If OOP classes extend Phaser Base Objects natively within the domain layer → INVALID.
- If game state is directly coupled to Scene instances instead of ECS data structures → INVALID.

## Layer Integrity Guarantee
- The YAML metadata block is contract-authoritative for this layer.
- Contract version upgrades must explicitly bump `contract_version`.
- Any mutation or overriding of `enforcement_level` fields invalidates framework certification.

---

# Layer 1 \u2013 phaser4-ecs-architecture

---
metadata_schema: phaser4-skill-schema@1
skill_id: phaser4-ecs-architecture
framework_version: 1.0.0
contract_version: 1.0.0
enforcement_level: strict
compatibility_mode: isolated
layer: 1
provides:
  - deterministic_simulation
  - fixed_timestep_loop
  - purity_contract
  - system_orchestration
requires:
  - phaser4-gamedev
extends:
  - phaser4-gamedev
conflicts_with: []
determinism:
  certification_level: 1
  description: "Local"
  fixed_timestep_required: true
headless_safe: true
multiplayer_support: false
---
# phaser4-ecs-architecture


# Phaser 4 ECS Architecture: Pro Patterns

## Layer Contract
- **Provides:** Deterministic simulation core, Fixed Timestep loop, Purity Contract, System Orchestration
- **Requires:** `phaser4-gamedev` (conceptual)
- **Extends:** `phaser4-gamedev`
- **Forbids:** Multiplayer transport logic inside core simulation

## Layer Capabilities
- Deterministic Simulation Support: **Yes**
- Multiplayer Synchronization Support: **No**
- Requires Fixed Timestep: **Yes**
- Engine-Agnostic Domain Layer: **Yes**
- Safe for Headless Execution: **Yes**

## Determinism Certification Level
- **Level 0** → No guarantees
- **Level 1** → Local deterministic
- **Level 2** → Network deterministic (rollback safe)

*(This module explicitly provides Level 1 guarantees).*

Learn to build incredibly fast, data-oriented 2D browser games using Phaser 4's new Entity-Component-System (ECS) architecture, TypeScript-first approach, and WebGL/WebGPU rendering.

## Target Audience
This layer is designed for:
- **Senior/Lead Developers** architecting long-term, maintainable browser games.
- **Teams migrating from Phaser 3** who need to unlearn OOP habits and adopt ECS paradigms.
- **Enterprise Studios** demanding strict TypeScript, DDD (Domain-Driven Design), and testable game logic.

## What You Will Build
By the end of this layer, you will be able to:
- Build an ECS-based 2D game architecture from scratch.
- Separate game logic (Systems) from visual representation (Rendering).
- Implement modular input and physics handling.
- Create reusable, data-only entity factories.
- Structure a scalable, enterprise-grade Phaser 4 repository.

## TypeScript Strict Configuration
To get the most out of Phaser 4's typing system, this layer assumes the following `tsconfig.json` compiler options:
- `"strict": true`
- `"noImplicitAny": true`
- `"exactOptionalPropertyTypes": true`
- **No usage of `any`** – Always define explicit interfaces for your components and systems.

### ESLint & Code Quality Enforcement
Professional Phaser 4 projects must enforce consistency and architectural constraints automatically.

Recommended rules:
- No `any`
- Explicit return types on public functions
- No unused exports
- No circular imports
- Max function length (encourage small Systems)
- No direct mutation of external state outside Systems

Example ESLint philosophy:

```json
{
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "import/no-cycle": "error",
    "max-lines-per-function": ["warn", 60]
  }
}
```

Architecture is enforced by tooling, not discipline alone.

## Recommended Architecture Layering
We recommend strictly separating concerns to keep your game testable and scalable:
- **Core:** Game bootstrap, canvas setup, and renderer initialization.
- **Scene Layer:** Purely for lifecycle management (Init, Preload, Start, Stop) and grouping display objects. No game logic goes here.
- **ECS Layer:** Where the magic happens. Components (pure data) and Systems (pure logic).
- **Domain Layer:** Your specific game rules and state management.
- **Infrastructure Layer:** Adapters for external APIs, Audio management, or Asset loading.

### Architectural Rules (Non-Negotiable)
This layer is intentionally opinionated. Follow these rules:
1. **Scenes are orchestration only.**
2. **No gameplay logic inside Sprites or GameObjects.**
3. **Systems process data — they do not create rendering objects.**
4. **Domain must not import Phaser.**
5. **Rendering is an adapter over ECS state.**

### Authoritative World
The ECS store is the sole source of truth for the game domain. External mutation (UI callbacks, input events) must encode intents and enqueue them for the System pipeline. All adapters (Renderer, Audio, UI) strictly derive state from the ECS on a read-only basis.

*If your game breaks when Phaser is removed from your domain folder, your architecture is wrong.*

---

## Migration Mindset (Phaser 3 → Phaser 4)
If you are coming from Phaser 3, you **must** undergo a mental paradigm shift. The framework is no longer a God-object that controls your game design.

### The Phaser 3 Way (Obsolete)
- **God Scenes**: `this.add`, `this.physics`, `this.tweens` all tightly coupled to the Scene instance.
- **Fat GameObjects**: Extending `Phaser.GameObjects.Sprite` to add business logic (`update()` methods inside view classes).
- **Inheritance Traps**: Deep class hierarchies (`class Enemy extends Character extends Sprite`).
- **Implicit State**: State hidden within the Phaser rendering graph.

### The Phaser 4 Way (Modern, Pro)
- **Lightweight Scenes**: Scenes only manage lifecycle events (start, stop) and group display lists.
- **Pure Entities**: Entities are just IDs. Visuals are just rendering components.
- **Composition over Inheritance**: Features are added by attaching pure Data Components.
- **Explicit State**: State is explicitly defined in Components, making testing trivial.

---

## Module 1 – Modern Setup
Phaser 4 games do not rely on a monolithic `new Phaser.Game(config)` object in the same way Phaser 3 did. Instead, you compose the game loop and renderer manually, giving you fine-grained control.

```typescript
// src/main.ts
import { Game } from '@phaserjs/phaser/Game';
import { Scene } from '@phaserjs/phaser/Scene';
import { WebGLRenderer } from '@phaserjs/phaser/renderer/webgl1/WebGLRenderer';

class MainScene extends Scene {
    // Scene implementation...
}

// Initialize the Game
const game = new Game({
    width: 800,
    height: 600,
    renderer: WebGLRenderer,
    parent: 'game-container',
    scenes: [MainScene]
});
```

---

## Module 2 – ECS Mental Model
Phaser 4 represents a major architectural shift. Instead of classic Object-Oriented inheritance (`class Player extends Phaser.GameObjects.Sprite`), Phaser 4 utilizes an **Entity-Component-System (ECS)** core.

*   **Entities:** Just unique IDs representing an object in your game.
*   **Components:** Pure data attached to an entity (e.g., `Position { x, y }`, `Velocity { x, y }`).
*   **Systems:** Functions that iterate over entities possessing specific components. *Systems must be pure when possible*.

*(Note: This guide assumes ergonomic, sparse Map-based component stores typical in JS/TS. However, ultra high-performance engines eventually migrate toward dense, indexed Structure of Arrays (SoA) memory layouts, trading developer ergonomics for raw CPU cache performance.)*

Because of ECS, you shouldn't rely on massive classes with methods for everything (e.g. `sprite.setAlpha(0.5)`). Instead, you use modular functions that mutate the component data of the entity.

### ECS Anti-Patterns
Avoid bringing Phaser 3 mental models into Phaser 4.

**❌ Wrong (OOP inheritance mindset)**
```typescript
class Player extends Sprite {
    attack() {
        this.setVelocityX(100);
    }
}
```

**✅ Correct (Data-Oriented ECS mindset)**
```typescript
// Component
interface Position {
    x: number;
    y: number;
}

interface Velocity {
    x: number;
    y: number;
}

// System
function MovementSystem(entities: Entity[]) {
    // deterministic processing of data
}
```

Entities are not behavior containers. **Behavior lives in Systems.**

### Component Lifecycle
The lifecycle of a component within the ECS goes: **Created → Active → Marked for Removal → Purged**. 
You must *never* dynamically delete a component or entity mid-iteration during a System's hot loop, as this shuffles underlying arrays and corrupts active iterators. Always defer destruction by tagging entities with a `PendingDestroy` component, and purge them safely at the frame boundary via a dedicated cleanup system.

### Entity Identity & Recycling
An entity is mathematically just an integer ID. A controlled ID allocator should manage acquisition and recycling. Never reuse an ID within the exact same frame it was destroyed to avoid stale reference resolution during deferred execution.

---

## Module 3 – Scene Lifecycle
Unlike Phaser 3, where Scenes were heavy managers of systems (`this.add`, `this.physics`), Phaser 4 Scenes are lightweight. They act structurally to group entities and manage lifecycle events. 

**Architectural Principle:** Do not put game logic inside your Scene classes.

```typescript
import { Scene } from '@phaserjs/phaser/Scene';
import { On } from '@phaserjs/phaser/events/On';

export class GameScene extends Scene {
    constructor() {
        super();
        
        // Listen to lifecycle events
        On(this, 'start', () => this.start());
        On(this, 'update', (delta: number, time: number) => this.update(delta, time));
    }

    start() {
        // Initialization and object creation
    }

    update(delta: number, time: number) {
        // Delegate loop logic to ECS Systems here
    }
}
```

---

## Module 4 – Rendering & Display List
In Phaser 4, what you previously knew as a `Sprite` is internally handled as an Entity with various Components (Transform, Texture, etc.).

You construct objects and explicitly add them to the **Display List** of the scene using `AddChild`. This cleanly separates rendering from domain logic.

```typescript
import { Sprite } from '@phaserjs/phaser/gameobjects/sprite/Sprite';
import { Text } from '@phaserjs/phaser/gameobjects/text/Text';
import { AddChild } from '@phaserjs/phaser/display/AddChild';
import { SetPosition } from '@phaserjs/phaser/components/transform/SetPosition';

// 1. Create the Object (Entity instantiation)
const player = new Sprite(100, 100, 'player-texture');
const scoreText = new Text(10, 10, 'Score: 0', { font: '16px Arial', fill: '#FFF' });

// 2. Modify component data via modular functions
SetPosition(scoreText, 20, 20);

// 3. Add to the Scene's Display List for rendering
AddChild(this, player);
AddChild(this, scoreText);
```

---

## Module 5 – Input System
Phaser 4 features a unified input system. `Pointer` events handle both mouse clicks and touch automatically.

```typescript
import { Keyboard } from '@phaserjs/phaser/input/keyboard/Keyboard';
import { SetInteractive } from '@phaserjs/phaser/input/SetInteractive';
import { On } from '@phaserjs/phaser/events/On';

// -- Keyboard --
const keyboard = new Keyboard();
On(keyboard, 'keydown-SPACE', () => console.log('Jump!'));

// -- Pointer (Mouse/Touch) --
// Interactive objects must be explicitly enabled for input.
SetInteractive(player);
On(player, 'pointerdown', (pointer) => {
    console.log(`Player clicked at ${pointer.x}, ${pointer.y}`);
});
```

---

## Module 6 – Physics Integration
Physics bodies are attached to entities as Components, and processed by Physics Systems. Phaser 4 supports two primary physics engines:

1.  **Arcade Physics**: Lightweight, fast, AABB/circular collisions. Best for retro games.
2.  **Matter.js**: Advanced, full-body physics simulations including joints and polygons.

```typescript
// Example concept for adding physics to an entity in a modular way
import { AddArcadeBody } from '@phaserjs/phaser/physics/arcade/AddArcadeBody';

// Assuming 'player' is an entity/sprite
AddArcadeBody(player, { isStatic: false });
```

---

## Module 7 – Asset Loading
Assets are loaded asynchronously within a `preload` method of a Scene or a dedicated "Boot Scene".

```typescript
import { ImageFile } from '@phaserjs/phaser/loader/files/ImageFile';
import { SpriteSheetFile } from '@phaserjs/phaser/loader/files/SpriteSheetFile';
import { AudioFile } from '@phaserjs/phaser/loader/files/AudioFile';

export class PreloadScene extends Scene {
    async preload() {
        // Use Promise.all() for parallel, modular loading
        await Promise.all([
            ImageFile('background', 'assets/bg.png').load(),
            SpriteSheetFile('hero', 'assets/hero.png', { frameWidth: 32, frameHeight: 32 }).load(),
            AudioFile('jumpSound', 'assets/jump.mp3').load()
        ]);
    }
}
```

---

## Module 8 – Project Architecture
For a scalable, enterprise-grade game, use Vite or Webpack and adhere to this strict module structure:

```text
/public
  /assets        <-- All static images, sounds, tilemaps
  index.html     <-- Entry point holding the `<div id="game-container">`
/src
  /core          <-- Bootstrap and configurations
  /components    <-- Custom ECS Components (Interfaces/Data only)
  /systems       <-- Custom ECS Systems (Pure logic/Functions)
  /scenes        <-- Lightweight lifecycle managers
  /entities      <-- Prefabs and Entity instantiators
  /domain        <-- Specific game rules and utilities
  main.ts        <-- Initializes the Game instance
```

---

## Module 9 – Domain-Driven Game Design
Advanced Phaser 4 architecture separates game rules from rendering completely.

Example domain rule:

```typescript
// domain/CombatRules.ts
export function calculateDamage(
    baseDamage: number,
    defense: number
): number {
    return Math.max(baseDamage - defense, 0);
}
```

This file:
- Does not import Phaser
- Is fully testable
- Guarantees deterministic behavior for replays

*Game engines are infrastructure. Rules are domain.*

---

## Module 10 – Testing Strategy
Professional game architecture must be testable.

**What we test:**
- Domain rules (pure functions)
- Systems (with mocked entity data)
- Deterministic behavior

**What we do NOT test:**
- Scene lifecycle wiring
- Renderer internals
- Phaser framework code

Example Vitest test:

```typescript
import { describe, it, expect } from 'vitest'
import { calculateDamage } from '../domain/CombatRules'

describe('CombatRules', () => {
    it('never returns negative damage', () => {
        expect(calculateDamage(5, 10)).toBe(0)
    })
})
```

*If your game logic cannot be unit tested, it is tightly coupled to the engine.*

---

## Module 11 – Deterministic Simulation Basics
ECS architecture enables deterministic simulation. To ensure predictability across simulation ticks:

- Systems must be deterministic.
- State must be structured purely.
- No hidden randomness inside Systems (inject RNG).
- Avoid frame-rate dependent logic.

### Purity Contract
Systems must operate under a strict mathematical purity contract:
- They depend **only** on explicit component inputs and the given deltaTime.
- No reading of hidden globals (e.g., `window.performance.now()`, `Math.random()`).
- The contract guarantees that the same input snapshot plus the same delta time yields the exact identical output snapshot every single time.

### Fixed Timestep Strategy
To decouple render iterations (FPS) from simulation logic, you **must** implement an accumulator pattern with a fixed simulation step (e.g., 16.66ms for 60Hz). 

```typescript
accumulator += deltaTime;
while (accumulator >= fixedStep) {
    simulateGameTick(fixedStep);
    accumulator -= fixedStep;
}
```
This loop guarantees stable simulation windows and prevents physics divergence.

---

## Module 12 – Performance Considerations (Data-Oriented Design)
Phaser 4 is fast because of ECS. To maximize performance, adhere to Data-Oriented Design (DOD):

- **Structure of Arrays (SoA) vs Array of Structures (AoS):** Prefer flat, tightly packed arrays for identical components (SoA) to maximize CPU cache hits and logical memory locality. Avoid scattering data in random object properties (AoS).
- **Predictable Memory Access:** Hot loops inside Systems should iterate over contiguous blocks of memory. Predictable patterns allow the CPU prefetcher to keep the pipeline fed.
- **Minimize GC Pressure:** Avoid raw object allocations (`new` or `{}`) inside hot updating loops. Per-frame heap memory allocations trigger Garbage Collection micro-stutters.
- **Object Pooling:** If you must allocate Entities dynamically (e.g., projectiles), use a pre-allocated pool to recycle IDs and re-initialize Component data.

---

## Module 13 – Production Hardening
Before deploying an enterprise game, enforce specific production constraints:

### System Fault Isolation
Each System invocation should be wrapped in guarded execution (e.g., Error Boundaries). One failing System must not corrupt the authoritative ECS state. Implement strict crash containment so the engine can recover or halt gracefully without dragging down the main simulation loop.

- **Dev/Prod Build Separation:** Use Vite/Webpack environment variables to strip out debug systems, logging, and visual colliders in production.
- **Logging Strategy:** Do not use `console.log`. Abstract logging into an Infrastructure service that sends telemetry to a backend in prod, and writes to console in dev.
- **Error Handling:** Wrap core game loops in Error Boundaries. If a system crashes, the game should gracefully fail or attempt to recover the ECS state snapshot, not blank page.
- **Asset Load Failure:** Handle `Promise.catch` on `ImageFile` loaders. Provide fallback textures ("pink squares") so a missing sub-asset doesn't halt the entire game bootstrap.
- **Versioned Builds:** Hash your asset filenames to bust cache upon new releases, ensuring players never load stale `.js` or `.png` files.

---

## Module 14 – End-to-End Minimal Example
This is how a true professional structures a feature using pure ECS in Phaser 4.

### 1. Components (Pure Data)
```typescript
// ECS/Components.ts
export interface Position {
    x: number;
    y: number;
}
export interface Velocity {
    x: number;
    y: number;
}
```

### 2. System (Pure Logic)
```typescript
// ECS/MovementSystem.ts
import { Position, Velocity } from './Components';

export function MovementSystem(
    positions: Map<number, Position>, 
    velocities: Map<number, Velocity>, 
    deltaMs: number
) {
    const deltaSec = deltaMs / 1000;
    for (const [entityId, pos] of positions) {
        const vel = velocities.get(entityId);
        if (vel) {
            pos.x += vel.x * deltaSec;
            pos.y += vel.y * deltaSec;
        }
    }
}
```

### 3. Unit Test (Deterministic validation)
```typescript
// tests/MovementSystem.test.ts
import { describe, it, expect } from 'vitest';
import { MovementSystem } from '../ECS/MovementSystem';

describe('MovementSystem', () => {
    it('updates position deterministically based on velocity and delta', () => {
        const posMap = new Map([[1, { x: 0, y: 0 }]]);
        const velMap = new Map([[1, { x: 100, y: 0 }]]);
        
        // Advance exactly 0.5 seconds (500ms)
        MovementSystem(posMap, velMap, 500); 
        
        expect(posMap.get(1)?.x).toBe(50); // 100 * 0.5
    });
});
```

### 4. Render Adapter (Infrastructure)
```typescript
// Infrastructure/RenderSyncSystem.ts
import { Sprite } from '@phaserjs/phaser/gameobjects/sprite/Sprite';
import { SetPosition } from '@phaserjs/phaser/components/transform/SetPosition';
import { Position } from '../ECS/Components';

export function RenderSyncSystem(
    positions: Map<number, Position>, 
    sprites: Map<number, Sprite>
) {
    for (const [entityId, pos] of positions) {
        const sprite = sprites.get(entityId);
        if (sprite) {
            SetPosition(sprite, pos.x, pos.y);
        }
    }
}
```

---

## System Orchestration Strategy
To maintain a deterministic execution pipeline, your `update` loop must orchestrate Systems in a strict, top-down order. Predictable system execution order is non-negotiable for simulation correctness and replayability.

**Rule:** Systems must *never* call other Systems directly. Data flows via Components only.

A central `SystemRunner` or orchestrated loop should control execution:
1. **Input Systems:** (Read hardware state, encode to Intent Components)
2. **AI Systems:** (Decide actions, write to Intent Components)
3. **Physics/Movement Systems:** (Process Intents, simulate world, update Spatial Components)
4. **Domain Systems:** (Resolve combat, rules, state machines based on spatial changes)
5. **Render Sync Systems:** (Read Spatial Components, update Sprites/Transforms)

### System Execution Contract
- Systems must not retain hidden mutable state across frames.
- Inter-system communication must occur strictly via Components.
- A System must be replayable solely from component inputs + deltaTime.

### Read vs Write Systems
Systems should be strictly categorized as either **Mutating** (Write) or **Observational** (Read).
- **Write Systems** (e.g., Physics, Domain) mutate authoritative ECS state. They must be executed synchronously in a rigid, deterministic order.
- **Read Systems** (e.g., Render Sync, Audio) never mutate simulation state. They only consume data to update adapters. Because they are pure observers, Read Systems can and should be safely parallelized or run asynchronously.

### Concurrency Boundaries
If you are parallelizing work via Web Workers:
- Read Systems may be safely parallelized, but **only** over immutable snapshots of the ECS state.
- Never allow concurrent reads over mutating component buffers.
- Enforce strict isolation to prevent data races and torn reads during the core simulation tick.

### Intent Components
Input systems should never directly mutate spatial or velocity state. Instead, they write to **Intent Components** (e.g., `MoveIntent`, `FireIntent`). Subsequent Simulation Systems consume these intents, validate them against authoritative domain rules, and finally apply the resulting actions before clearing the intent. This rigidly decouples raw hardware input from simulated logic execution.

---

## Observability & Telemetry
In an enterprise environment, you cannot optimize what you cannot measure. A professional engine architecture requires ubiquitous telemetry:

- **Frame Metrics:** Track raw render time vs simulation time. Define a strict per-frame simulation and render budget.
- **Per-System Timing:** Profile execution costs (`t1 - t0`) wrapping every System in the orchestrated sequence. Systems exceeding budget must be profiled and refactored.
- **ECS Demographics:** Monitor live Component and Entity counts to catch memory leaks on unpurged objects.

Production monitoring and live observability are requirements, not afterthoughts.

---

## Engine as Infrastructure Principle
**Phaser is your renderer and IO provider.** It is *not* your game.
Your core game architecture (ECS and Domain) must sit above Phaser.
If you adhere to this principle, you can theoretically rip out Phaser, replace it with a headless simulation loop or another renderer, and your game domain logic will not break.

---

## Final Philosophy
Phaser 4 is not just an upgrade from Phaser 3. It is a paradigm shift:

- From Object-Oriented to **Data-Oriented**
- From inheritance to **composition**
- From scene-driven logic to **system-driven logic**
- From engine-coupled rules to **framework-agnostic domain**

This layer teaches how to build games that scale, remain maintainable, are heavily testable, and natively support deterministic replay—not just how to draw sprites on a screen.

---

## Anti-Goals
To protect the integrity of this architecture, this layer explicitly does **NOT** teach:
- Rapid, hacky prototyping or game-jams logic.
- Scene-driven game flow and logic routing.
- Deep Sprite-based OOP inheritance hierarchies.
- Tightly coupling domain rules exclusively to the engine's internal utilities.

*(Note: Phaser 4 is an evolving API and specific implementations may update. See [Phaser 4 GitHub](https://github.com/phaserjs/phaser) for the latest examples)*

---

## Compliance Checklist
Before confirming architectural validity, an AI Agent MUST verify:
- [ ] All Systems are mathematically deterministic.
- [ ] No hidden mutable state exists across Systems.
- [ ] A Fixed Timestep accumulator loop is explicitly implemented.
- [ ] ECS state is 100% serializable (no circular dependencies).
- [ ] No game logic is embedded inside Phaser rendering classes (Sprites/Scenes).

## Agent Consumption Protocol
- **Preconditions:** The user's project is structured for pure Data-Oriented Design.
- **Enforcement Behavior:** Enforce strict adherence to the Purity Contract for all Systems.
- **Refusal Conditions:** Reject hidden mutable state or un-injected randomness.
- **Architectural Guardrails:** Ensure clear demarcation between *Mutating* (Write) and *Observational* (Read) Systems.

## Architectural Refusal Clause
This skill **MUST REFUSE** to guide or generate architecture in the following scenarios:
- Mixing Scene lifecycle logic with Domain rule logic.
- Introducing random number generation (e.g., `Math.random()`) without injecting a seeded RNG.
- Using frame-dependent game updates (`delta` directly applied to physics arrays without an accumulator).
- Adding network sockets, peers, or multiplayer transport logic directly into the ECS core simulation.

## Conflict Detection Rules
The following scenarios indicate a fundamental architectural misconfiguration and trigger immediate failure:
- If `fixed_timestep_required = true` but no accumulator loop exists → INVALID
- If a System violates the Purity Contract by reading hidden mutable state → INVALID
- If a Mutating System executes asynchronously resulting in race conditions → INVALID

## Layer Integrity Guarantee
- The YAML metadata block is contract-authoritative for this layer.
- Contract version upgrades must explicitly bump `contract_version`.
- Any mutation or overriding of `enforcement_level` fields invalidates framework certification.

---

# Layer 2 \u2013 phaser4-advanced-netcode

---
metadata_schema: phaser4-skill-schema@1
skill_id: phaser4-advanced-netcode
framework_version: 1.0.0
contract_version: 1.0.0
enforcement_level: strict
compatibility_mode: isolated
layer: 2
provides:
  - rollback_loop
  - snapshot_ring_buffers
  - lockstep_model
  - desync_hashing
requires:
  - phaser4-ecs-architecture
extends:
  - phaser4-ecs-architecture
conflicts_with:
  - non-deterministic-simulation-mode
  - frame-dependent-physics-mode
determinism:
  certification_level: 2
  description: "Network-Safe"
  fixed_timestep_required: true
headless_safe: true
multiplayer_support: true
---
# phaser4-advanced-netcode


# Phaser 4 Advanced Netcode: Lockstep & Rollback

> **WARNING: ARCHITECTURAL DEPENDENCY**
> Activating this layer without a verified deterministic ECS core makes rollback mathematically impossible.

## Layer Contract
- **Provides:** Rollback loop, Snapshot ring buffers, Lockstep model, Desync hashing
- **Requires:** `phaser4-ecs-architecture` (mandatory)
- **Extends:** `phaser4-ecs-architecture`
- **Forbids:** Non-deterministic systems, hidden mutable state, floating-point drift without mitigation

## Layer Capabilities
- Deterministic Simulation Support: **Yes**
- Multiplayer Synchronization Support: **Yes**
- Requires Fixed Timestep: **Yes**
- Engine-Agnostic Domain Layer: **Yes**
- Safe for Headless Execution: **Yes**

## Determinism Certification Level
- **Level 0** → No guarantees
- **Level 1** → Local deterministic
- **Level 2** → Network deterministic (rollback safe)

*(This module explicitly operates at Level 2).*

Building rollback-capable deterministic multiplayer engines inherently requires an uncompromised Entity-Component-System (ECS) foundation. This layer assumes complete mastery of Data-Oriented Design, System Orchestration, and the Purity Contract as outlined in the `phaser4-ecs-architecture` layer.

## Target Audience
This layer is designed for:
- **Multiplayer Engine Architects** building authoritative, high-density realtime combat or IO domains.
- **Netcode Engineers** implementing Rollback (GGPO) or Lockstep synchronization.

---

## Module 1 – The Determinism Boundary
In multiplayer environments, you must explicitly define an absolute deterministic domain boundary. 

Snapshots and network inputs must encompass *only* the authoritative simulation components (`Position`, `Health`, `Velocity`, `Hitbox`) within this boundary. Components existing outside this boundary (e.g., render adapters, visual tweens, audio queues, debug UI states, non-deterministic infrastructure) are strictly excluded from rollback algorithms and server reconciliation pipelines. 

If purely visual state bleeds into the simulation hashing, desync detection becomes impossible.

---

## Module 2 – Snapshot Architecture & Memory Footprint
Because ECS decouples data from logic, your entire game state exists as numerical arrays or maps. This enables full state serialization natively via bit-packed binary structures.

### Snapshot Memory Footprint Estimation Logic
To survive strict UDP MTU budgets (often ~1200 bytes per packet safely), serialization must compress ECS data mathematically:
1. **Identify Authoritative Bytes:** Count the bytes of active components inside the Determinism Boundary.
2. **Bit-Packing:** Compress booleans into bit-masks (1 byte = 8 flags). Compress floats into half-precision (16-bit) if millimeter precision is unnecessary.
3. **Delta Compression:** Send only delta-compressed snapshots (the XOR difference from the last mutually ACKed frame) when transmitting large world states.
4. **Estimation:** `Estimated Footprint = SUM(Packed Component Sizes) * Max Entity Count`. If this exceeds the MTU, you must implement snapshot chunking across sequence-numbered packets.

---

## Module 3 – Lockstep vs. Rollback CPU Trade-offs
When architecting your netcode on Phaser 4, you must choose a synchronization model:

### Deterministic Lockstep
- **Mechanism:** All peers execute Simulation Tick `N` at exactly the same time.
- **Constraint:** Requires fixed-point math (to avoid cross-CPU floating-point drift) to prevent butterfly effects.
- **Trade-off:** Minimal CPU overhead (simulating exactly 1 step per frame). High latency = immediate simulation stuttering, as Player 1 must wait for Player 2's packet to proceed.

### Rollback (GGPO Style)
- **Mechanism:** Peers predict inputs locally and simulate ahead of network confirmation.
- **Constraint:** Extremely demanding CPU requirements.
- **Trade-off:** Hides latency entirely from the local player. However, if a late network input contradicts local prediction, the engine must roll back, apply the true input, and re-simulate the delta. You might need to execute 8+ heavy simulation frames within a single 16ms render window during a deep rollback event.

---

## Module 4 – Authoritative Tick Source & Clock Discipline
In a networked simulation, the local clock is irrelevant. The engine must adhere to an **Authoritative Tick Source**.
- The Server (or host) dictates the absolute `TickId`.
- Clients implement **Clock Discipline**: they must continuously adjust their local tick execution rate (speeding up or slowing down by fractions of a millisecond per frame) to remain a specific number of ticks *ahead* of the server (prediction window) and gracefully absorb network jitter.
- Time must never run backwards on a client UI, even if the underlying tick simulation rewinds.

---

## Module 5 – Formal Rollback Algorithm
A production-grade rollback engine requires three distinct state management pillars:

### 1. Frame Numbering Strategy
Every simulation tick operates on a universally synchronized monotonically increasing integer (`TickId`).

### 2. Snapshot Buffer Structure
A ring-buffer of full state snapshots representing your rollback window (e.g., the last 60 frames). This structure guarantees instant, allocation-free state snapping.

### 3. Input History Buffer Structure
A deterministic record of local inputs, predicted remote inputs, and confirmed remote inputs, indexed strictly by `TickId`.

### Rollback Trigger Detection & Re-Simulation Loop
When an authoritative input packet arrives from the server/peer:
1. Decode the packet's `TickId` and remote inputs.
2. Compare the decoded inputs against the previously predicted inputs in the Input History Buffer for that `TickId`.
3. If identical, do nothing (prediction succeeded).
4. If divergent, trigger the **Rollback Loop**.

### Pseudocode: Rollback Handling Loop
```typescript
function triggerRollback(syncTickId: number, authoritativeInputs: Input[]) {
    const currentTickId = Engine.getCurrentTick();
    
    // 1. State Rehydration Timing Guarantee
    // Restore the ECS state to precisely the syncTickId snapshot from the ring buffer.
    ECS.rehydrateSnapshot(SnapshotBuffer.get(syncTickId));
    
    // 2. Overwrite history with authoritative truth
    InputHistoryBuffer.insertConfirmedInputs(syncTickId, authoritativeInputs);
    
    // 3. Fast-forward re-simulation loop up to the current frame
    for (let tick = syncTickId; tick < currentTickId; tick++) {
        // Fetch inputs (confirmed ones for past ticks, re-predicting for uncertain future ticks)
        const inputsForTick = InputHistoryBuffer.getInputsForTick(tick);
        
        // Execute the strict ECS pipeline
        SystemRunner.executeSimulationSystems(inputsForTick, FIXED_DELTA_TIME);
        
        // Save the corrected trajectory to the snapshot buffer
        SnapshotBuffer.save(tick + 1, ECS.createSnapshot());
    }
    
    // 4. Update the visual adapters strictly after the entire rollback batch completes.
    SystemRunner.executeRenderSyncSystems();
}
```

---

## Module 6 – Multiplayer Authority & Server Reconciliation
In authoritative server architecture, the Server maintains the definitive ECS world.

### The Server Reconciliation Pipeline
1. **Client Prediction:** Client predicts its own input, applies it immediately to its local ECS, and transmits the input + `TickId` to the server.
2. **Server Execution:** The server receives the input, validates it against domain rules, and simulates the logic.
3. **Authority Update:** The server frequently broadcasts its authoritative ECS snapshot block and the `LastAckedClientTick`.
4. **Reconciliation Step:** Upon receiving the server snapshot, the client rewinds its ECS to the server's snapshot tick, discards all local history older than `LastAckedClientTick`, and re-simulates its remaining pending inputs on top of the server's absolute truth.

---

## Module 7 – Desync Detection & Drift Resolution
In an enterprise multiplayer environment, you cannot isolate network bugs without aggressive telemetry.

### Desync Detection Workflow
1. **Determinism Hashing:** At the end of every simulation tick, compute a lightweight cryptographic Hash/Checksum of the authoritative ECS state (strictly within the Determinism Boundary). 
2. **Streaming:** Clients append their local hash for `TickId N` to their routine outgoing input packets.
3. **Server Verification:** The server compares the client's hash against the server's hash for `TickId N`.
4. **Drift Resolution:** If a hash mismatch occurs (a Desync), the simulation has fractured. The server immediately forces a full state payload push to the offending client, commanding a hard state overwrite to repair the simulation before numerical divergence ruins the player experience.

---

## Compliance Checklist
Before confirming architectural validity, an AI Agent MUST verify:
- [ ] The core simulation is fully deterministic (requires Layer 1 Verification).
- [ ] A Snapshot Ring Buffer structure exists.
- [ ] An Input History Buffer structure exists.
- [ ] State hashing executes ONLY within the explicit Determinism Boundary.
- [ ] Clock Discipline is implemented to absorb jitter.
- [ ] Resimulation limits are enforced against processing constraints.

## Agent Consumption Protocol
- **Preconditions:** The agent must systematically query and confirm that `phaser4-ecs-architecture` is fully implemented.
- **Enforcement Behavior:** Enforce strict rollback loops and UDP MTU footprint calculations logic.
- **Refusal Conditions:** Reject applying rollback to OOP trees or state without snapshot history.
- **Architectural Guardrails:** Limit netcode generation to bounded deterministic components; completely exclude visual tweens from simulation logic.

## Architectural Refusal Clause
This layer **MUST REFUSE** to guide or generate architecture in the following scenarios:
- The underlying systems do not guarantee identical outputs given identical snapshot+delta inputs.
- The user requests lockstep networking using native Javascript floats without applying explicit mitigation/quantization logic.
- The user proposes rollback without implementing a Snapshot Buffer AND an Input History Buffer.
- Bleeding purely visual/rendering state into the server prediction pipeline.

## Conflict Detection Rules
The following scenarios indicate a fundamental architectural misconfiguration and trigger immediate failure:
- If `multiplayer_support = true` but `deterministic_level < Network-Safe` (Level 2) → INVALID
- If `fixed_timestep_required = true` but the clock discipline relies solely on standard `requestAnimationFrame` deltas → INVALID
- If visual interpolation relies on authoritative state mutations instead of isolated render components → INVALID

## Layer Integrity Guarantee
- The YAML metadata block is contract-authoritative for this layer.
- Contract version upgrades must explicitly bump `contract_version`.
- Any mutation or overriding of `enforcement_level` fields invalidates framework certification.

---

# Global Governance Rules

## Agent Validation Protocol

When an Artificial Intelligence Agent attempts to implement or query this framework, it is architecturally obligated to execute the following validation layer before commencing any code generation:

1. **Parse Metadata Blocks:** Radically ingest the YAML `metadata_schema` rules.
2. **Validate Dependency Graph:** Validate `requires`, `extends`, and prevent missing layers.
3. **Validate Determinism Hierarchy:** Read the structured `determinism` object and verify certification bounds.
4. **Reject Incompatible Combinations:** Immediately halt if `conflicts_with` rules flag a violation.
5. **Abort on Strict Violation:** Immediately abort the task entirely upon any `enforcement_level: strict` infraction.

---

## Global Conflict Resolution Policy

- If two internally applied layers declare `conflicts_with` each other → HARD FAIL.
- If determinism certification decreases across layers → HARD FAIL.
- If `enforcement_level` is `strict` → no partial execution allowed.
- Agents must request explicit user override to proceed.

---

## Contract Evolution Rules

- Any modification to metadata structure requires `metadata_schema` version bump.
- Any behavioral guarantee change requires `contract_version` bump.
- Any capability expansion requires `framework_version` bump.

---

## Registry Authority Model

- Registry-level policies override individual layer metadata if conflict arises.
- Individual layers may extend but not weaken global enforcement rules.
- `enforcement_level` declared in registry is minimum allowed level.

---

## Determinism Escalation Rule

- Determinism certification may increase across layers.
- It may never decrease.
- Activating a lower certification layer on top of a higher applied layer results in a HARD FAIL.
- Agents must verify certification monotonicity.

---

## Explicit Downgrade Protection

- `fixed_timestep_required` cannot change from true to false in higher layers.
- `headless_safe` cannot downgrade from true to false once introduced.
- `multiplayer_support` cannot be enabled without certification_level 2.

---

## Canonical Metadata Field Definitions

To maintain absolute rigour during automated certification and agent ingestion, the framework strictly enforces the following schema fields:

- **`metadata_schema`** (String): Defines the version of the parser schema the file adheres to. (Monotonic: restricted to version bumps)
- **`framework_version`** (String): Represents the overarching architecture framework version. (Monotonic: increasing-only)
- **`contract_version`** (String): Designates the strict API behavioral guarantee level. (Monotonic: increasing-only)
- **`enforcement_level`** (Enum): The severity of parsing strictness (e.g., `strict`). (Monotonic: immutable, forbidden to override downwards from registry)
- **`compatibility_mode`** (Enum): Defines how the skill interconnects (e.g., `isolated`, `layered-registry`). (Monotonic: restricted by layer rules)
- **`layer`** (Integer): The hierarchical dependency level of the layer. (Monotonic: increasing-only, overridden per layer)
- **`provides`** (List): The architectural capabilities the layer introduces. (Monotonic: unrestricted additions)
- **`requires`** (List): The foundational layers necessary to operate. (Monotonic: unrestricted)
- **`extends`** (List): The layers from which conceptual guarantees are inherited. (Monotonic: unrestricted)
- **`conflicts_with`** (List): Explicit declarations of architectural incompatibilities. (Monotonic: unrestricted expansions)
- **`determinism.certification_level`** (Integer): 0, 1, or 2 denoting simulation correctness. (Monotonic: increasing-only, forbidden to downgrade across layers)
- **`determinism.fixed_timestep_required`** (Boolean): Whether the accumulator loop is mandated. (Monotonic: increasing-only, forbidden to override from true to false)
- **`headless_safe`** (Boolean): Whether the codebase logic can execute without DOM/Renderers. (Monotonic: increasing-only, forbidden to override from true to false)
- **`multiplayer_support`** (Boolean): Whether the logic is safe for network synchronization. (Monotonic: strictly tied to certification level 2)

---

## Layer Resolution Semantics

When an AI Agent resolves the capabilities of multiple requested internal layers, the semantic contract operates as follows:

- **`requires`** → Hard dependency: The agent must verify the specified layer is applied. It cannot apply the current layer without it.
- **`extends`** → Semantic extension: Inherits the conceptual and behavioral guarantees of the specified layer without redefining them.
- **`provides`** → Additive capability only: The layer grants new operational scope, but does not mutate or weaken the guarantees of lower layers.
- **`conflicts_with`** → Hard fail: If the agent detects an applied layer or user intent matching this list, it must immediately abort.
- **`compatibility_mode`** → Defines the parsing expectation. Registry modes dictate global policies, whereas isolated modes dictate self-contained validations.

**Important Registry Rules:**
- The `enforcement_level` declared in the central registry is the absolute **minimum allowed level** for the entire project.
- No individual layer may weaken or bypass registry constraints.
