---
name: solid
description: When designing module boundaries, interfaces, or class hierarchies for maintainable architecture. Use when the user says "how should I structure this," "too coupled," "hard to test," "dependency injection," "single responsibility," or "interface design." For simpler structural concerns, see separation-of-concerns.
metadata:
  version: 1.0.0
---

# SOLID Principles

## Before Applying

If `.agents/stack-context.md` exists, read it first. Apply this principle using idiomatic patterns for the detected stack. For framework-specific details, use context7 MCP or web search — don't guess.

## Principle

Five design principles that produce modular, testable, and resilient systems. While originally framed for object-oriented design, the underlying ideas apply to any paradigm — functions, modules, services, or components.

## Why This Matters in Production

SOLID code is change-friendly code. Production systems change constantly — new features, bug fixes, integrations, scaling. Systems designed with SOLID principles absorb change locally rather than requiring cascading modifications. This means fewer regressions, faster feature delivery, and smaller blast radius when things go wrong.

---

### S — Single Responsibility Principle

**A module should have one, and only one, reason to change.**

Every module, function, or component should own exactly one piece of functionality. When a change request comes in, you should be able to predict which file needs editing without searching.

**Violations look like:**
- A function that validates input, queries the database, applies business logic, and formats the response
- A "utils" file that grows indefinitely because nothing else has a clear home
- A class that changes every time any feature in the system changes

**Apply it:**
- If a function does two things, split it into two functions
- If a module handles both "what to do" and "how to do it," separate policy from mechanism
- Name modules after their responsibility — if the name is vague ("Manager", "Helper", "Utils"), the responsibility is unclear

---

### O — Open/Closed Principle

**Software should be open for extension but closed for modification.**

You should be able to add new behavior without modifying existing, working code. This doesn't mean you never touch existing code — it means you design so that the common extension points don't require it.

**Violations look like:**
- A growing switch statement that gets a new case every time a feature is added
- A function that checks `if type == "x"` for an ever-expanding list of types
- Every new integration requiring changes to a central dispatch function

**Apply it:**
- Use dispatch tables, registries, or polymorphism instead of branching on type
- Design around contracts (interfaces, protocols, function signatures) that new implementations can fulfill
- Plugin architectures — but only when you have multiple plugins (see YAGNI)

---

### L — Liskov Substitution Principle

**Subtypes must be usable wherever their parent type is expected, without surprises.**

If your code accepts a base type, any implementation of that type should work correctly. No special-casing, no "except when it's type X" guards.

**Violations look like:**
- A subclass that throws "not implemented" for inherited methods
- Type checks (`instanceof`, `typeof`) to determine behavior after accepting a general type
- Consumers that must know which specific implementation they're dealing with

**Apply it:**
- If a subtype can't fulfill the full contract of the parent, it shouldn't be a subtype — use composition instead
- Design interfaces around what consumers need, not what implementations can provide
- Test with substitution: swap implementations and verify the system still behaves correctly

---

### I — Interface Segregation Principle

**No consumer should be forced to depend on methods it doesn't use.**

Keep interfaces small and focused. A consumer that only reads data shouldn't depend on an interface that also includes write, delete, and admin operations.

**Violations look like:**
- A "god interface" with 20+ methods that most implementations only partially fulfill
- Consumers that import a large module but only use one function
- Mock objects in tests that stub out 15 methods when the test only exercises 2

**Apply it:**
- Split large interfaces into role-based ones: `Reader`, `Writer`, `Admin` instead of `Repository`
- In languages without interfaces, apply the principle to module boundaries — export only what consumers need
- If your test mocks are painful to write, your interfaces are too broad

---

### D — Dependency Inversion Principle

**High-level policy should not depend on low-level detail. Both should depend on abstractions.**

Your business logic should not directly import database drivers, HTTP clients, or filesystem operations. It should depend on abstractions that those details implement.

**Violations look like:**
- Business logic that directly instantiates database connections, HTTP clients, or external SDKs
- Inability to test business rules without spinning up real infrastructure
- Changing a database or API provider requires rewriting business logic

**Apply it:**
- Pass dependencies in (dependency injection) rather than constructing them internally
- Define interfaces at the boundary of your business logic — let infrastructure adapt to them
- In functional code: accept functions as parameters instead of hard-coding calls to specific implementations

---

## Boundaries

- **SOLID is a set of heuristics, not laws.** Small scripts, prototypes, and glue code don't need full SOLID treatment. Apply these principles where they reduce the cost of change.
- **Don't over-abstract.** SOLID taken to the extreme produces an explosion of tiny classes and interfaces that are harder to navigate than the original monolith. An abstraction must earn its keep by serving multiple consumers or enabling meaningful testability.
- **Tension with KISS:** Every interface, injection point, and abstraction adds a layer of indirection. Apply SOLID where the system genuinely changes along those axes, not prophylactically.
- **Functional code gets SOLID for free in some areas.** Pure functions naturally satisfy SRP. Higher-order functions naturally satisfy DIP. Focus SOLID effort on the architectural boundaries where it matters most.

## Code Review Checklist

- [ ] Does each module have a clear, single responsibility?
- [ ] Can new behavior be added without modifying existing working code?
- [ ] Are interfaces small enough that consumers don't depend on things they don't use?
- [ ] Are dependencies injected rather than hard-coded?
- [ ] Could you swap an implementation (e.g., database, API client) without touching business logic?

## Related Skills

- **separation-of-concerns**: For layer-level structure (SoC is the "what," SOLID is the "how")
- **law-of-demeter**: For reducing coupling between components
- **yagni**: To avoid over-applying SOLID with premature abstractions
