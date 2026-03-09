---
name: phaser-design-patterns
description: Design pattern implementation in Phaser 3 with JavaScript, focused on scene architecture, entities, input, physics, and performance. Use when asked to apply, refactor, review, or teach design patterns (creational, structural, or behavioral) in Phaser games.
---

# Phaser Design Patterns

Implement design patterns with a focus on real gameplay, not abstract examples.

## When to use

Use this skill when the user needs to apply, refactor, review, or explain design patterns in Phaser 3 (JavaScript), especially for scene architecture, entities, input systems, physics interactions, and performance-sensitive gameplay code.

## Workflow

1. Identify a real game problem (entity creation, system coordination, behavior variation, etc).
2. Choose a pattern that reduces coupling and does not add unnecessary complexity.
3. Map the pattern to Phaser primitives (Scene, GameObject, Group, Events, Physics, Time, Input).
4. Implement in JavaScript using game-domain naming.
5. Validate at runtime (scene loads, input responds, collisions work, no event leaks).

## Quick Pattern Selection

- Variable entity creation -> Factory Method / Abstract Factory.
- Step-by-step level or UI construction -> Builder.
- Shared state for thousands of instances -> Flyweight + pooling.
- Rules by AI mode/behavior -> State / Strategy.
- Decoupled events between gameplay and UI -> Observer / Mediator.
- Re-runnable actions (input, replay, undo) -> Command.

## Implementation Rules

- Prioritize composition over deep inheritance.
- Keep scenes small and with clear responsibilities.
- Avoid mutable singletons for gameplay logic; reserve them for global services (audio, config).
- Use `delta` in `update(time, delta)` when the pattern affects movement or timers.
- Unsubscribe events in `shutdown`/`destroy` to avoid memory leaks.
- For massive objects (bullets, particles), combine the pattern with pooling (`setActive(false)`, `setVisible(false)`).

## Expected Deliverables

- Explain in 2-4 lines why the pattern solves the problem.
- Show a JavaScript/Phaser snippet with real game context.
- Include relevant risks and anti-patterns.
- Propose minimum validation (manual test or simple test).

## References

- See `references/patterns-map.md` for a complete pattern -> Phaser usage map.
- See `references/phaser-snippets.md` for ready-to-copy and adapt templates.
- See `references/state-machine-pattern-phaser.md` for a full State + StateMachine implementation (Idle/Move/Action) adapted to Phaser.
