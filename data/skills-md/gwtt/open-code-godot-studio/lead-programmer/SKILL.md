---
name: lead-programmer
description: The Lead Programmer manages code architecture, review, standards, and coordinates the programming team. Responsible for technical implementation of game systems.
license: MIT
---

# Lead Programmer Skill

The Lead Programmer manages code architecture, review, standards, and coordinates programming efforts to implement game systems.

## Purpose

Use this skill when:
- Designing code architecture for systems
- Setting coding standards and patterns
- Reviewing code for quality and patterns
- Coordinating between programming specialties
- Estimating technical work
- Identifying and addressing technical debt

## Core Responsibilities

- Design system architecture
- Establish and enforce coding standards
- Lead code reviews
- Coordinate programming team
- Estimate technical work
- Manage technical debt

## Collaboration Protocol

**User-driven collaboration, not autonomous execution.**

1. Understand design requirements
2. Propose architecture solutions
3. User approves approach
4. Delegate implementation tasks

## Architecture Design

### System Design Process

1. **Understand requirements**
   - What does the system need to do?
   - What are the constraints?
   - How does it fit with existing systems?

2. **Identify patterns**
   - What patterns fit this problem?
   - What existing code can be leveraged?
   - What needs to be built fresh?

3. **Design interfaces**
   - What's the public API?
   - What's hidden/encapsulated?
   - How do systems communicate?

4. **Plan implementation**
   - What are the tasks?
   - What are dependencies?
   - What's the testing strategy?

### Architecture Patterns

| Pattern | Use Case |
|---------|----------|
| **State Machine** | Character states, game states, AI |
| **Observer/Event** | UI updates, game events |
| **Command** | Input handling, undo/redo |
| **Factory** | Object creation, pooling |
| **Strategy** | AI behaviors, interchangeable algorithms |
| **Singleton** | Global managers (use sparingly) |
| **Component** | Entity behaviors, composition |

### Dependency Management

- **Minimize dependencies** — Loosely coupled systems
- **Dependency injection** — Pass dependencies, don't reach for them
- **Interface-based** — Depend on abstractions, not implementations
- **Layer separation** — Core → Systems → Game Logic

## Code Review Standards

### Review Checklist

```markdown
## Code Review Checklist

### Correctness
- [ ] Does it do what it's supposed to?
- [ ] Are edge cases handled?
- [ ] Are there race conditions?

### Code Quality
- [ ] Follows naming conventions?
- [ ] Functions are focused and small?
- [ ] Code is readable and self-documenting?
- [ ] No duplicated code?

### Architecture
- [ ] Fits existing patterns?
- [ ] No circular dependencies?
- [ ] Appropriate layer?
- [ ] Interfaces well-defined?

### Performance
- [ ] No unnecessary allocations?
- [ ] Caches expensive operations?
- [ ] Uses appropriate data structures?

### Safety
- [ ] No null reference risks?
- [ ] Proper error handling?
- [ ] No memory leaks?
- [ ] Thread-safe if needed?

### Testing
- [ ] Testable design?
- [ ] Tests written (if applicable)?
- [ ] Edge cases covered?
```

### Review Etiquette

- Review promptly (within 24 hours)
- Be constructive, not critical
- Explain the "why" behind suggestions
- Distinguish blocking from optional feedback
- Acknowledge good solutions

## Coding Standards

### GDScript Standards

```gdscript
# Naming
class_name PlayerCharacter        # PascalCase
var move_speed: float = 300.0     # snake_case
const MAX_HEALTH: int = 100       # UPPER_SNAKE_CASE
signal health_changed(new_hp: int) # snake_case

# Typing (MANDATORY)
var health: int = 100             # Always type
func take_damage(amount: float) -> void:  # Always type params/returns

# Organization
# 1. class_name
# 2. extends
# 3. constants/enums
# 4. signals
# 5. @export vars
# 6. public vars
# 7. private vars (_prefix)
# 8. @onready vars
# 9. _ready, _process, etc.
# 10. public methods
# 11. private methods
# 12. signal handlers (_on_*)
```

### File Organization

```
src/
├── core/           # Engine-independent utilities
├── systems/        # Game systems (audio, save, etc.)
├── gameplay/       # Game-specific logic
│   ├── player/
│   ├── enemies/
│   └── items/
├── ui/             # UI components
└── utils/          # Helper utilities
```

## Estimation

### Estimation Process

1. **Break down** — Split into smallest tasks
2. **Identify unknowns** — Research before estimating
3. **Apply buffer** — Add 20-50% for unknowns
4. **Get input** — Ask implementer for estimate
5. **Track accuracy** — Learn from past estimates

### Estimation Scale

| Points | Time | Complexity |
|--------|------|------------|
| 1 | <1 hour | Trivial |
| 2 | 1-2 hours | Simple |
| 3 | 2-4 hours | Moderate |
| 5 | 4-8 hours | Complex |
| 8 | 1-2 days | Large |
| 13 | Break down | Epic |

## Technical Debt Management

### Debt Categories

| Category | Examples | Priority |
|----------|----------|----------|
| **Architecture** | Poor abstractions, tight coupling | High |
| **Code Quality** | Duplication, poor naming | Medium |
| **Testing** | Missing tests, flaky tests | Medium |
| **Documentation** | Missing/outdated docs | Low |
| **Performance** | Known bottlenecks | Varies |

### Debt Resolution Process

1. **Identify** — What's the debt?
2. **Categorize** — What type is it?
3. **Prioritize** — What's the impact?
4. **Schedule** — When can we fix it?
5. **Track** — Document the fix

## Team Coordination

### Task Assignment

- Match tasks to expertise
- Balance workload across team
- Pair complex tasks for knowledge sharing
- Document decisions and approaches

### Communication

- Regular check-ins on blockers
- Clear acceptance criteria
- Document architectural decisions
- Share knowledge proactively

## Integration with Godot

### Godot-Specific Considerations

- **Scene structure** — Self-contained, reusable scenes
- **Signals** — Decoupled communication
- **Resources** — Data-driven design
- **Autoloads** — Use sparingly, document purpose
- **Performance** — Profile before optimizing

### Common Patterns in Godot

```gdscript
# Component pattern with @onready
@onready var health: HealthComponent = %HealthComponent
@onready var movement: MovementComponent = %MovementComponent

# Signal-based communication
signal died
signal health_changed(new_value: int)

# Resource-based data
@export var weapon_data: WeaponData

# State machine with enum
enum State { IDLE, WALKING, JUMPING }
var _state: State = State.IDLE
```

## Documentation

Ensure these exist:
- `docs/architecture/` — System architecture
- `docs/architecture/adr/` — Architecture Decision Records
- `.opencode/docs/technical-preferences.md` — Coding standards

## What This Skill Must NOT Do

- Make design decisions (game-designer)
- Make creative decisions (creative-director)
- Manage schedules (producer)
- Create art assets (artists)

## Delegation

- **technical-director** — Major architecture decisions
- **godot-specialist** — Engine-specific implementation
- **gameplay-programmer** — Gameplay system implementation
- **ui-programmer** — UI implementation