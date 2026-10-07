---
name: monomind-design
description: "Design or improve module boundaries, public test seams, and shared operational capabilities. Use when code is hard to test or navigate, workflows duplicate mechanics, domain policy leaks into integrations, or a module interface is becoming shallow or unstable."
---

# Monomind Design

Shape modules that hide meaningful complexity behind small, stable interfaces and keep product policy separate from reusable mechanics.

## Model the boundary

1. Read the project's domain vocabulary, current callers, data flow, tests, and relevant decisions. Name contradictions between the documented model and the code.
2. Describe the module's users, responsibilities, invariants, owned state, and failure modes before proposing files or abstractions.
3. Identify the public **seam**: the smallest interface through which callers can use and tests can observe the behavior.
4. Judge depth by leverage: a deep module offers substantial behavior through a simple interface. Pass-through wrappers, configuration mirrors, and interfaces that expose every internal decision are shallow.

## Separate policy from mechanics

Keep orchestration or action code responsible for:

- domain rules, authorization, and ownership checks;
- state transitions and product-visible failure classification;
- deciding whether and when a capability is invoked;
- choosing user-facing recovery and retry policy.

Keep a service or capability responsible for:

- provider, protocol, command, or SDK mechanics;
- deterministic transformations and readiness checks;
- mechanical retry/backoff only when the caller explicitly selects that policy;
- structured results and typed failures.

Capability APIs take explicit inputs, return structured outputs, and avoid hidden database or global-state access. Prefer several composable capabilities over one method that owns the whole workflow.

Extract repeated mechanics when at least two callers need the same stable operation, or when a volatile external boundary deserves isolation. Keep one-off domain behavior near its owner; duplication is sometimes cheaper than a premature abstraction.

## Change safely

When implementation is authorized:

1. Characterize current behavior through the public seam.
2. Introduce the new boundary without changing behavior.
3. Move one caller at a time and verify after each move.
4. Remove the old path only after all callers and tests use the new seam.
5. Recount concepts and dependencies. A refactor that merely relocates complexity has not improved the design.

Record an ADR only for a hard-to-reverse, surprising tradeoff. Update the domain glossary when the design resolves terminology, but keep implementation detail out of the glossary.

## Completion criteria

- The owning module, public seam, invariants, and dependency direction are explicit.
- Domain policy remains with its owner; shared capabilities expose mechanics without owning product state.
- Tests observe behavior through public interfaces.
- The proposal removes or contains complexity instead of adding indirection.
- Any migration can proceed incrementally with the system kept valid.
