---
name: codebase-design
description: Design small, type-safe interfaces that hide complexity and give domain logic a clear home.
---

# Codebase Design

Put related rules and behavior in modules that callers can use without understanding their internals. Judge a design by what callers must know, how many places must change when a rule changes, and how easily its behavior can be tested.

## Terms

Use the project's existing names. These distinctions help explain a design; they are not a reason to rename code or domain concepts.

- **Module:** a function, class, package, or other unit with an interface and an implementation.
- **Interface:** everything a caller must know to use a module correctly, including types, required call order, errors, configuration, and performance constraints. This means more than a TypeScript `interface` declaration.
- **Implementation:** the code behind that interface.
- **Adapter:** an implementation that connects an interface to a particular dependency, such as a database or external service. The term describes its role, not its size.
- **Seam:** a place where behavior or a dependency can be substituted, including for a test. State whether it is internal to a module or exposed to application callers when that distinction matters.

A **deep module** hides decisions that callers would otherwise have to make themselves. A **shallow wrapper** adds an interface without reducing that work. Code size, method count, and the ratio of interface to implementation lines do not establish either one.

## Design from callers

Sketch representative call sites before types or methods. Derive the interface from what those callers need. Keep processing stages, storage details, and coordination inside the module unless callers need to control them.

For each proposed interface, ask:

- Can a caller complete its task without learning internal rules or coordinating unrelated operations?
- Does each parameter represent a choice the caller needs to make?
- When a rule changes, can it be updated in its owning module rather than across callers?
- Would removing the module eliminate unnecessary forwarding, or force callers to handle its behavior themselves?

A module can be useful with one caller or one adapter. Keep it when it isolates a protocol, side effects, or rules that change independently. Do not invent another adapter, configuration option, or future use case to justify the module.

## Place behavior with its owner

Group code that maintains the same rules, data, or workflow. Split a module when that gives an independently changing responsibility a clear home. Do not extract a wrapper that merely moves code without reducing what callers must understand.

A module may use smaller internal modules and dependency interfaces. Keep those details internal when application callers do not need them. Tests may use an internal module's interface to check its own behavior without making that interface part of the application's API.

When a requirement causes repeated workarounds, sketch the design that would meet it cleanly, then choose an authorized migration that preserves required compatibility. Existing structure is context, not a requirement to keep every layer. This comparison does not authorize unrelated rewrites.

## Make behavior testable

Accept dependencies through an appropriate interface so tests can control them without replacing the behavior under test. For example, passing a payment gateway to order processing lets a test exercise payment failures without creating a real charge.

Keep calculations separate from side effects when they have distinct responsibilities. Returning a calculated discount makes that rule testable without modifying a cart or invoking storage.

Test behavior through the interface that owns it. Keep internal tests when they catch important failures that other tests would miss. Do not expose private state, add public methods, or make callers learn implementation details just to simplify test setup.

Simplify methods and parameters when they remove choices callers do not need. Fewer methods do not necessarily mean fewer behaviors to test.

## Further guidance

- Read [DEEPENING.md](DEEPENING.md) when combining related modules while preserving dependency handling and useful tests.
- Read [TYPE-DESIGN.md](TYPE-DESIGN.md) when types, external inputs, or casts affect rules the code must enforce.
- Read [DOMAIN-STRUCTURE.md](DOMAIN-STRUCTURE.md) when stateful code repeats decisions, transition rules, or lookups without a clear owner.
- Read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) when several designs remain plausible after checking requirements and repository conventions.
