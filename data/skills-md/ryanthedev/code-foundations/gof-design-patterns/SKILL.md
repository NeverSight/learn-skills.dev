---
name: gof-design-patterns
description: "Maps code symptoms — exploding subclass combinations, switch-on-type dispatch, tangled object construction, incompatible interfaces, one-to-many update cascades — to the matching Gang of Four pattern, then loads that pattern's structural recipe from its 23 reference files. For selecting and implementing a design pattern; not for system-level boundaries (use ca-architecture-boundaries) or module interface depth (use aposd-designing-deep-modules)."
user-invocable: false
---

# Skill: gof-design-patterns

23 Gang of Four patterns as a decision guide. Identify the symptom or goal, pick the pattern, then read its reference file for the structural recipe.

---

## Pick by Symptom

| Code Smell | Pattern(s) |
|---|---|
| if/else or switch on object **type** | Strategy, Visitor |
| if/else or switch on object **state** | State |
| Telescoping constructors | Builder |
| Subclass explosion for feature combinations | Decorator, Strategy, Bridge |
| `new ConcreteClass()` scattered throughout codebase | Factory Method, Abstract Factory |
| Hard-coded class names | Factory Method, Prototype |
| Subsystem complexity leaking into client code | Facade |
| Complex many-to-many object communication | Mediator |
| Manual state propagation to multiple dependents | Observer |
| Duplicated algorithm structure across subclasses | Template Method |
| Large conditional routing requests to handlers | Chain of Responsibility |
| High memory cost from many fine-grained objects | Flyweight |

---

## Pick by Goal

| What you want | Pattern |
|---|---|
| Hide how objects are created | Factory Method, Abstract Factory, Builder, Prototype |
| Ensure exactly one instance globally | Singleton |
| Make incompatible interfaces work together | Adapter |
| Decouple abstraction from implementation | Bridge |
| Treat individual objects and groups uniformly | Composite |
| Add behavior dynamically without subclassing | Decorator |
| Simplify a complex subsystem API | Facade |
| Lazy-load, cache, or control access to an object | Proxy |
| Make requests undoable, queueable, or loggable | Command (+ Memento for undo state) |
| Traverse a collection without exposing internals | Iterator |
| Encapsulate an interchangeable algorithm | Strategy |
| Change behavior when internal state changes | State |
| Notify dependents automatically on state change | Observer |
| Add operations to a stable object structure | Visitor |

---

## Choosing Between Similar Patterns

| Choosing between | Key distinction |
|---|---|
| Strategy vs Template Method | Composition (delegate whole algorithm) vs inheritance (override steps) |
| State vs Strategy | State transitions itself; Strategy is chosen by the client |
| Adapter vs Facade | Adapting a single class vs simplifying an entire subsystem |
| Decorator vs Proxy | Adding behavior vs controlling access |
| Factory Method vs Abstract Factory | Single product type vs product families |
| Command vs Chain of Responsibility | Encapsulate and invoke an action vs route a request to a handler |

---

## Pattern Categories

**Creational (5)** — control *what* gets created and *how*

Abstract Factory · Builder · Factory Method · Prototype · Singleton

**Structural (7)** — compose classes and objects into larger structures

Adapter · Bridge · Composite · Decorator · Facade · Flyweight · Proxy

**Behavioral (11)** — define communication and responsibility between objects

Chain of Responsibility · Command · Interpreter · Iterator · Mediator · Memento · Observer · State · Strategy · Template Method · Visitor

---

## When NOT to Apply a Pattern

Every pattern adds indirection. Apply one only when:

1. The problem is genuinely recurring — not a one-off edge case
2. The flexibility the pattern provides outweighs the extra classes and interfaces
3. Your team can maintain the added indirection

> "If a straightforward solution works, use it." — GoF

---

## Reference Files

Each pattern has a full file in `${CLAUDE_SKILL_DIR}/references/`:

- `foundations.md` — GoF principles (program to interface, favor composition, encapsulate what varies)
- `techniques.md` — master table, pattern relationships, alternative-pattern decision guide
- `gof-<pattern-name>.md` — structure, participants, when to use, consequences, example

Read the relevant pattern file when implementing. This SKILL.md is for selection; the reference files are for execution.
