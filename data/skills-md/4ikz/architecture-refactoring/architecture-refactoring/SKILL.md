---
name: architecture-refactoring
license: Apache-2.0
metadata:
  author: 4iKZ
  version: "0.1.1"
  repository: https://github.com/4iKZ/architecture-refactoring
description: >-
  Use when an existing codebase resists change: files that must be edited
  together across unrelated modules, circular or cross-layer dependencies,
  god modules, shared mutable state, persistence models leaking across
  boundaries, shotgun changes, tests that boot unrelated infrastructure,
  or architecture that keeps drifting. Audits the current system with
  concrete evidence, defines ownership and dependency boundaries, and
  migrates incrementally while preserving behavior. Trigger even when the
  user does not say "architecture" or "refactoring", for example "clean this
  up", "untangle this", "where should I start", "we keep breaking things",
  or "make this easier to change". Do not use for greenfield design,
  mechanical renames, formatting, dependency upgrades, or purely stylistic
  cleanup.
---

# Architecture Refactoring

Use this skill to improve the architecture of an **existing** software system. The objective is not pattern compliance or aesthetic cleanliness. The objective is to make likely future changes more local, predictable, and independently testable.

Core rule:

> Things that change together should live together. Things that change for different reasons should be separated. Cross-boundary knowledge should be narrow, explicit, and stable.

## Non-negotiable constraints

1. **Understand before editing.** Trace actual callers, callees, data ownership, runtime flow, tests, configuration, persistence, and external integrations before moving responsibilities.
2. **Preserve behavior by default.** Unless the task explicitly requests behavioral changes, structural refactoring must keep externally observable behavior stable.
3. **Do not equate abstraction with decoupling.** Interfaces, DI containers, events, factories, microservices, or more folders are not automatically improvements.
4. **Prefer incremental migration over rewrites.** Introduce seams, migrate callers in small steps, verify, then remove obsolete paths.
5. **Optimize for change propagation.** A refactor is successful when a likely future change touches fewer unrelated places and requires less cross-module knowledge.
6. **Do not hide uncertainty.** Distinguish verified facts from architectural hypotheses. If a boundary is inferred rather than demonstrated, say so in the working notes.

## Choose the scope

Classify the task before analysis:

- **Local:** one class/package/component, limited callers. Inspect the target plus its immediate dependency neighborhood.
- **Subsystem:** a coherent capability spanning multiple modules. Map its major runtime and data flows.
- **Repository-wide:** architecture modernization or pervasive coupling. Build a repository-level module/dependency view first.

Do not perform a repository-wide audit for a narrowly scoped change unless evidence shows the problem is systemic.

Match effort to scope; enough analysis to support the decision, not exhaustive analysis:

| Scope | Analysis budget | Artifacts | Enough when |
|---|---|---|---|
| Local | target + direct callers/dependencies | short findings, inline in the conversation | one boundary change and its verification are defined |
| Subsystem | 1-3 representative flows, data ownership, tests touching the target | audit + plan, about one page each | target boundary, migration steps, and safe stopping points are clear |
| Repository-wide | module graph, cycles, hotspots, data ownership | audit, plan, and report | the highest-value target is ranked and its first step is verified |

Stop analyzing when the decision is supported by evidence, not when every file has been read.

## Required workflow

### 1. Establish the baseline

Before changing architecture:

- identify build/test/typecheck/lint commands;
- locate architecture documents, ADRs, package boundaries, module manifests, dependency rules, and ownership conventions;
- run the smallest relevant verification suite;
- add characterization tests when important behavior is not otherwise protected;
- record important externally observable behavior that must remain unchanged.

If the baseline is already failing, record the failures and do not attribute them to the refactor.

When you need concrete dependency, cycle, or enforcement tooling for the project's ecosystem, read [references/TOOLING.md](references/TOOLING.md).

### 2. Build an evidence-based architecture map

For the relevant scope, identify:

- entry points and orchestration;
- domain/business policies;
- infrastructure and external adapters;
- persistence and data ownership;
- public module APIs;
- imports/calls/events/queues;
- shared mutable state and caches;
- shared database tables or schemas;
- configuration and initialization dependencies;
- transaction and temporal-order dependencies;
- test seams and test coupling.

Read [references/AUDIT_GUIDE.md](references/AUDIT_GUIDE.md) before mapping a subsystem or the whole repository; for a local change, tracing the immediate neighborhood may be enough.

### 3. Diagnose the real architecture problem

Do not refactor a smell merely because it exists. Identify the mechanism by which it creates cost or risk.

Typical evidence includes:

- circular module dependencies;
- one feature repeatedly requires edits across unrelated modules;
- a module changes for several independent business reasons;
- multiple modules directly mutate the same data;
- internal persistence models leak across boundaries;
- callers depend on initialization order or undocumented side effects;
- tests require booting unrelated infrastructure;
- a shared `utils`, `common`, `core`, or `base` package has become a dependency hub;
- stable policy code directly depends on volatile infrastructure;
- many callers know implementation details that should be private.

For principles and definitions, read [references/PRINCIPLES.md](references/PRINCIPLES.md) when a boundary decision needs justification, not as required reading.

### 4. Define the target boundary before moving code

Every proposed boundary must answer:

- **Responsibility:** what capability does this module own?
- **Invariants:** what rules must remain internally consistent?
- **Data ownership:** what state can this module authoritatively mutate?
- **Public contract:** what may other modules ask it to do or return?
- **Hidden knowledge:** what implementation details should callers stop knowing?
- **Allowed dependencies:** what may this module depend on?
- **Forbidden dependencies:** what dependency directions must not appear?

If these answers are unclear, do not start a large structural migration yet.

### 5. Evaluate alternatives

Consider at least the smallest plausible alternatives, such as:

- move a misplaced responsibility;
- merge artificially separated modules;
- extract one cohesive module;
- introduce a facade around unstable internals;
- introduce an adapter around volatile infrastructure;
- introduce a boundary DTO/contract;
- invert a dependency at a genuine policy/infrastructure seam;
- assign a single owner to shared state;
- break a cycle by fixing ownership rather than relocating imports;
- leave the code unchanged if migration risk exceeds architectural value.

Use [references/REFACTORING_PLAYBOOK.md](references/REFACTORING_PLAYBOOK.md) to choose the smallest operation that addresses the demonstrated problem. For a fully worked end-to-end case — including one where the evidence says leave the code alone — see [references/EXAMPLES.md](references/EXAMPLES.md).

### 6. Rank by architectural value

Prioritize changes roughly by:

`value = change_frequency × blast_radius × defect_or_delivery_cost ÷ migration_risk`

This is a reasoning aid, not a mandatory numeric formula.

Prefer fixing hot, frequently changed coupling over beautifying stable code.

### 7. Write the migration plan

For subsystem or repository-wide work, create a plan using [assets/templates/refactor-plan.md](assets/templates/refactor-plan.md).

The plan must describe:

- current problem and evidence;
- target ownership and dependency direction;
- behavior that must remain unchanged;
- migration sequence;
- verification after each step;
- compatibility strategy if public APIs change;
- rollback or safe stopping points.

A good migration sequence usually looks like:

```text
introduce seam
→ implement new path
→ migrate one caller
→ verify
→ migrate remaining callers
→ verify
→ remove old path
→ enforce new boundary
```

### 8. Execute in small, reversible steps

After each meaningful step:

- keep the repository buildable when practical;
- run the narrowest relevant tests immediately;
- avoid mixing unrelated cleanup into the architecture change;
- preserve compatibility until callers are migrated;
- update imports and ownership deliberately, not via global search-and-replace alone.

Do not perform an undifferentiated repository-wide rewrite.

### 9. Verify behavior and architecture separately

Behavior passing is necessary but not sufficient.

Verify both:

**Behavior**
- tests;
- integration/contract tests;
- build/typecheck/lint;
- critical runtime flows.

**Architecture**
- dependency cycles removed or reduced (re-run the dependency check and include its output; a removal that is only asserted is not verified);
- forbidden dependency directions absent;
- public surface reduced or clarified;
- state ownership clearer;
- internal models no longer leak;
- test isolation improved;
- likely change blast radius reduced.

Read [references/VERIFICATION.md](references/VERIFICATION.md) before executing the first migration step, when you need the structural checks, architecture tests, or the per-step verification record; see [references/TOOLING.md](references/TOOLING.md) for ecosystem-specific enforcement tools.

### 10. Report the trade-off

For substantial changes, produce a concise before/after report using [assets/templates/refactor-report.md](assets/templates/refactor-report.md).

For every major architectural change state:

```text
Before:
After:
Coupling removed:
Coupling introduced:
Why the new coupling is preferable:
Behavior verification:
Architecture verification:
Remaining risks:
```

Never claim “decoupled”, “cleaner”, or “more maintainable” without identifying the concrete dependency or change propagation that improved.

## Decision rules

### Prefer cohesion over arbitrary smallness

A large module with one coherent responsibility can be healthier than several tiny modules that constantly call each other and always change together.

### Prefer explicit coupling over hidden coupling

A direct, typed call can be better than an event or queue when the semantic dependency is inherently synchronous and required. Distributed coupling is still coupling.

### Prefer information hiding over wrapper proliferation

Expose the smallest stable operation that callers need. Do not expose internal database records, SDK objects, mutable collections, or internal workflow steps unless they are intentionally part of the contract.

### Prefer logical boundaries before deployment boundaries

Do not split a monolith into services solely to claim lower coupling. Establish coherent ownership and contracts first. A modular monolith is often safer than a distributed monolith.

### Introduce interfaces only at useful seams

Good reasons include volatile infrastructure, cross-module ownership boundaries, multiple implementations, a testing seam, or a stable policy depending on an implementation detail. “Every class should have an interface” is not a valid reason.

## Red flags — stop and reassess

- New interfaces, factories, or DI containers appear with one implementation and no volatile seam.
- A static cycle was "fixed" by moving imports inside functions, behind a registry, or onto an event bus that still requires the same semantics.
- A cohesive module was split because it was large, and the pieces still change together.
- Callers were migrated before one representative end-to-end flow was verified.
- The change set mixes renames, formatting, dependency upgrades, or other cleanup with the structural migration.
- The report claims "cleaner" or "decoupled" without naming the concrete future change that became local.
- The target is stable, low-churn code with no demonstrated cost.

Read [references/ANTI_PATTERNS.md](references/ANTI_PATTERNS.md) before large changes.

## Gotchas

- File size, method count, or "looks ugly" is a signal, not a finding. Ask which change becomes cheaper.
- A module that passes tests can still be the wrong boundary; what must boot to test it is evidence too.
- Reuse is not ownership: two modules using the same helper does not mean they should share a module.
- Moving an import inside a function, behind a registry, or onto an event bus removes the static symptom, not the semantic dependency.
- If the same future requirement still touches the same set of modules after the migration — now with new names — nothing improved.
- A guarded state transition that a caller bypasses by writing fields directly is a symptom of split ownership, not harmless redundancy.
- Callers that depend on an internal field make it de facto public; shrinking a public surface is a migration, not a delete.

## Stop conditions

Stop and reassess if any of these occur:

- the proposed architecture requires many new abstractions but removes little concrete knowledge;
- a simple change becomes harder to trace after refactoring;
- the number of module hops grows without reducing semantic dependency;
- ownership becomes less clear;
- tests become more integration-heavy rather than more isolated;
- the migration requires changing behavior merely to make the structure fit a pattern;
- an existing stable area has low change frequency and little blast radius, but the refactor is large.

See [references/ANTI_PATTERNS.md](references/ANTI_PATTERNS.md) before large changes.

## Core success criterion

The best architecture lets a developer or coding agent modify one capability without loading the entire system into its working context.

Optimize architecture for the **future shape of change**, not for the current appearance of the directory tree.
