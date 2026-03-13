---
name: best-practices
description: Universal software engineering best practices for any language or project. Use when programming, refactoring code, designing systems, reviewing code, or ensuring production-ready quality. Covers fundamental principles (SOLID, DRY, KISS, YAGNI), architectural patterns (SoC, SSOT, LoD, CQS, DbC), and operational reliability (ETC, PoLP, CoC, Idempotency). Apply when building new features, cleaning up codebases, improving maintainability, or ensuring code follows industry standards.
---

# Universal Best Practices

This skill provides comprehensive guidance on software engineering best practices that apply across all programming languages and project types. Follow these principles to ensure clean, maintainable, production-ready code.

## Core Workflow

When writing or reviewing code:

1. Start with KISS and YAGNI - implement the simplest thing that solves the current need
2. Apply SOLID principles to structure your classes and modules
3. Ensure DRY by eliminating duplication
4. Use SoC to separate concerns into distinct responsibilities
5. Follow LoD to minimize coupling between components
6. Apply remaining principles as relevant to your specific context

## Fundamental Principles

### SOLID

Five core object-oriented design principles that make code maintainable and flexible:

**S - Single Responsibility Principle (SRP)**
- Each class/module should have only ONE reason to change
- One class = one job or responsibility
- Example: Separate `UserRepository` (data access) from `UserValidator` (validation logic)
- Benefit: Changes to one responsibility don't affect unrelated code

**O - Open/Closed Principle (OCP)**
- Open for extension, closed for modification
- Add new functionality without changing existing code
- Use interfaces, abstract classes, or inheritance to extend behavior
- Example: Plugin systems, strategy patterns
- Benefit: Add features without risking existing functionality

**L - Liskov Substitution Principle (LSP)**
- Subtypes must be substitutable for their base types
- Child classes shouldn't break parent class contracts
- Example: If `Bird` has `fly()`, don't create `Penguin extends Bird` - penguins can't fly
- Benefit: Polymorphism works correctly, no surprises

**I - Interface Segregation Principle (ISP)**
- No class should implement methods it doesn't use
- Many specific interfaces > one general interface
- Example: Split `IWorker` into `IWorkable` and `IEatable` instead of forcing robots to implement `eat()`
- Benefit: Lean interfaces, no unnecessary dependencies

**D - Dependency Inversion Principle (DIP)**
- Depend on abstractions, not concrete implementations
- High-level modules shouldn't depend on low-level modules
- Both should depend on abstractions
- Example: `PaymentProcessor` depends on `IPaymentGateway` interface, not concrete `StripeGateway`
- Benefit: Loose coupling, easy to swap implementations

### DRY (Don't Repeat Yourself)

- Every piece of knowledge has ONE authoritative representation
- Avoid duplicating logic, even if written differently
- Example: Extract common tax calculation logic into single function instead of repeating across products
- Benefit: Changes happen in one place, consistency guaranteed

### KISS (Keep It Simple, Stupid)

- Prefer the simplest solution that works
- Avoid unnecessary complexity and cleverness
- Simple code is easier to understand, maintain, and debug
- Example: Use straightforward conditionals over complex nested ternaries
- Benefit: Code is readable and less error-prone

### YAGNI (You Aren't Gonna Need It)

- Don't build features you don't need right now
- No speculative functionality for hypothetical future needs
- Focus on current requirements
- Example: Don't build a recommendation engine if you only need product listing
- Benefit: Less code to maintain, faster delivery

## Architectural Principles

### SoC (Separation of Concerns)

- Divide code into distinct sections, each addressing a separate concern
- Each module focuses on ONE aspect of functionality
- Example: Separate data layer, business logic, and presentation
- Benefit: Changes to one concern don't affect others

### SSOT (Single Source of Truth)

- Every data element is mastered in only ONE place
- All other references point to or derive from this source
- Example: User profile data lives in one database table, not duplicated across systems
- Benefit: No data inconsistency, one place to update

### LoD (Law of Demeter) - Principle of Least Knowledge

- Object should only talk to immediate friends
- Don't access nested objects: `a.getB().getC().doSomething()` violates LoD
- Instead: `a.doSomethingWithC()` where A delegates internally
- **Rule**: Method can only call methods on:
  - Itself (`this`)
  - Its parameters
  - Objects it creates
  - Its direct properties
- Benefit: Reduced coupling, easier refactoring

### CQS (Command Query Separation)

- Methods should either:
  - **Command**: Change state (return void)
  - **Query**: Return data (don't change state)
- Never both in same method
- Example: `getBalance()` reads only, `withdraw()` changes only
- Exception: Sometimes `pop()` or `incrementAndGet()` violates this for practical reasons
- Benefit: Predictable behavior, easier reasoning

### DbC (Design by Contract)

- Define explicit preconditions, postconditions, and invariants
- **Preconditions**: What must be true before method runs
- **Postconditions**: What must be true after method completes
- **Invariants**: What must always be true for the object
- Example: `withdraw(amount)` requires `amount > 0` (precondition) and `balance >= amount` (precondition), ensures `new_balance = old_balance - amount` (postcondition)
- Benefit: Clear contracts, fail-fast validation

## Operational Principles

### ETC (Easier to Change)

- Optimize for change cost, not cleverness
- Ask: "Will this be easy to modify later?"
- Prefer composition over inheritance
- Keep coupling loose, cohesion high
- Benefit: Code adapts to evolving requirements

### PoLP (Principle of Least Privilege)

- Grant minimum permissions needed for the task
- Processes run with minimal privileges
- Functions access only what they need
- Example: Read-only database connection for queries, no write access
- Benefit: Reduced attack surface, limited blast radius

### CoC (Convention over Configuration)

- Use sensible defaults over explicit configuration
- Follow standard conventions to reduce decisions
- Only configure when deviating from convention
- Example: Rails assumes `User` class maps to `users` table - no config needed
- Benefit: Less boilerplate, faster development, easier onboarding

### Idempotency

- Operation produces same result whether executed once or multiple times
- Safe to retry without side effects
- Critical for distributed systems and APIs
- Example: `PUT /users/123` with same data always results in same user state
- Implementation: Use idempotency keys, request IDs, or natural idempotency
- Benefit: Safe retries, fault tolerance, consistency

### POLA (Principle of Least Astonishment)

- System behavior should match user expectations
- Code does what it looks like it does
- No surprises or unexpected behavior
- Example: `delete()` should delete, not archive
- Benefit: Intuitive code, fewer bugs from misunderstanding

## Principle Application Priority

When multiple principles conflict:

1. **Safety first**: PoLP, DbC preconditions
2. **Simplicity**: KISS, YAGNI
3. **Maintainability**: DRY, SoC, SRP
4. **Flexibility**: OCP, DIP, ETC
5. **Consistency**: POLA, CoC

## Common Anti-Patterns to Avoid

- **Premature optimization**: Violates YAGNI and KISS
- **God classes**: Violates SRP and SoC
- **Deep nesting**: Violates LoD
- **Copy-paste code**: Violates DRY
- **Magic numbers/strings**: Violates SSOT and maintainability
- **Mixing commands and queries**: Violates CQS
- **Over-engineering**: Violates KISS and YAGNI

## Quick Reference

For detailed examples and language-specific implementations, see:
- `references/solid-examples.md` - SOLID principle examples
- `references/patterns-reference.md` - Design pattern applications of principles

## When Principles Conflict

**DRY vs KISS**: If abstraction becomes complex, duplicate similar code
**YAGNI vs Future-proofing**: Build for today, refactor when tomorrow arrives
**LoD vs Performance**: Sometimes direct access is needed - document why
**CQS vs Pragmatism**: Database `pop()` operations can violate CQS when needed

Remember: Principles are guidelines, not laws. Apply with judgment based on context.
