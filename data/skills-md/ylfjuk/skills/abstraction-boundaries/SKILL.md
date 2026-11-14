---
name: abstraction-boundaries
description: Design and review code abstractions without premature generalization, leaky boundaries, or special-case-heavy generic layers. Use when extracting shared code, introducing interfaces or generic parameters, designing reusable APIs or plugin systems, or reviewing an abstraction whose concrete assumptions may be leaking through.
---

# Abstraction Boundaries

An abstraction is a promise that several cases can be treated alike. Make that promise only when real cases show what is stable and what varies.

Prefer a little duplication while the pattern is unclear. The cost of removing honest duplication later is usually lower than the cost of preserving the wrong shared model across many callers. WET code—"write everything twice"—is often useful evidence gathering, not a failure to be DRY.

## First decide whether to abstract

Before extracting shared machinery, identify:

- The concrete cases that exist now. Do not count imagined future callers as evidence.
- The behavior they genuinely share, beyond similar syntax or names.
- The dimensions along which they differ.
- The owner of the shared concept and the dependency direction the boundary should enforce.
- The benefit the abstraction will buy: a stable contract, substitution, isolation, coordinated change, or meaningful reuse.

If those answers are unclear, keep the cases separate and colocated with their owners. Wait for the pattern to emerge. There is no required number of examples: two strong cases may reveal a stable seam, while five superficially similar cases may not.

Do not abstract merely to remove repeated lines, introduce an interface, prepare for hypothetical reuse, or make unlike concepts look uniform. Duplication of code is cheaper than coupling concepts that change for different reasons.

### Similar code is not necessarily one concept

Two implementations can be textually identical today while belonging to different product rules. Ask whether they are expected to change together for the same reason, not whether their current lines happen to match.

For example, a checkout may initially label both physical products and subscriptions with `item.title`. It is tempting to replace both formatters with a generic `getPurchasableLabel`. But the labels are governed by different rules: a physical product may later include size and color, while a subscription may include billing cadence or renewal terms. Their present similarity is incidental and volatile, so merging them would couple independent changes.

Keep the implementations separate until a stable shared policy emerges. If callers need uniform composition, abstract the capability—such as `buildCheckoutLabel`—while allowing each item type to implement its own policy. A shared contract does not require a shared implementation.

This is the key distinction:

- **Same implementation:** the code happens to look alike now.
- **Same responsibility:** the behavior represents one rule and should change together.

Extract shared code for the second. Treat the first only as a signal worth investigating.

## Then choose the boundary

Use the smallest boundary that represents the observed variation. Common forms include a function, data shape, interface, injected capability, callback, adapter, or independently composable block. Generic types and base classes are tools, not evidence that an abstraction exists.

Do not treat any shortlist as exhaustive. Depending on what is stable and what varies, useful choices may include:

- A discriminated union or sum type for a closed set of known variants.
- A strategy or callback when one operation varies inside a stable flow.
- An adapter when two independently owned models need translation.
- A facade when callers need a simpler view of a complex subsystem, without implying substitutable implementations.
- A pipeline when independently meaningful transformations compose in sequence.
- Policy-as-data when the variation is genuinely declarative.
- Inheritance or a template method when subtypes share a real invariant and are substitutable—not merely to reuse implementation.
- Dependency injection when a required capability has varying implementations.
- Building blocks when consumers should own composition.

Patterns address different dimensions and may be combined. A facade can invoke a pipeline whose stages use injected adapters; a closed variant can select a strategy; a building block can accept an injected capability. Choose each pattern for a specific job, and avoid adding machinery just to make the design resemble a named pattern.

### Preserve substitutability

Apply the Liskov substitution principle, named after Barbara Liskov, wherever implementations promise the same contract. A caller using that contract should be able to switch implementations without breaking the behavior the contract guarantees.

An implementation must not require stronger preconditions, provide weaker guarantees, or violate the contract's invariants. Matching method signatures is insufficient. This applies to interface implementations and injected capabilities as well as subclasses.

For example, if `Storage` promises both reading and writing, a read-only implementation that rejects every write does not satisfy that contract. Split out the read capability and make callers request what they need.

Litmus test: does a caller following the contract need to identify the implementation to use it correctly?

### Choose who owns composition

Two models deserve additional attention because they define where composition and concrete knowledge live:

### Inject capabilities

Use dependency injection when core behavior is stable but a capability or implementation varies—for example storage, time, randomness, transport, or a backend.

- Declare the required capability explicitly in the signature or construction boundary.
- Keep policy in the core and concrete integration details in adapters or composition code.
- Depend on the narrow behavior the core needs, not an implementation-shaped interface.
- Avoid service locators, ambient globals, and context objects that conceal the real requirements.

Litmus test: can the core be understood and tested using only the declared contract, without knowing which concrete implementation production selects?

### Expose building blocks

Use composable building blocks when consumers need to assemble or adapt small pieces themselves—for example UI primitives, utilities, parsers, and workflow steps.

- Make each block useful on its own.
- Let consumers own composition when their needs genuinely differ.
- Share conventions and compatible shapes without forcing shared machinery.
- If blocks require one another in a prescribed arrangement, describe the result honestly as a framework or composed API.

Litmus test: can a consumer take one block alone, use it directly, and replace or extend it without understanding unrelated blocks?

These models can coexist: inject a varying capability into a block, or build a composed feature from independently useful pieces. Other boundaries may fit better; do not force either model onto every abstraction.

## Prevent collapsed genericism

Collapsed genericism occurs when a supposedly general layer secretly depends on concrete details. Callers then pay for the mismatch through casts, type checks, magic strings, sprawling configuration, exception flags, or context passed through unrelated layers.

When this happens, find the missing distinction and choose the smallest honest repair:

- Make a real variation an explicit capability, parameter, or type-level distinction.
- Move concrete knowledge outward into an adapter or composition boundary.
- Split cases whose behavior or reasons to change are materially different.
- De-generalize the code when there is only one meaningful case.

Do not preserve a false abstraction merely because callers already depend on it.

## Warning signs

- Generic code branches on concrete types, caller identities, or magic values.
- An interface has one local implementation and one local caller but enforces no useful boundary.
- A base class offers hooks mainly so subclasses can undo its assumptions.
- Options and generic parameters grow with every new consumer.
- Context or configuration travels through layers that neither own nor use it.
- Consumers must understand implementation details to use the public contract safely.
- Changes to one case repeatedly require edits to unrelated cases.
- A shared helper has a vague name because the cases share syntax but not meaning.
- Two cases share an implementation even though separate owners or product decisions can change them independently.

One implementation is not automatically a problem: an interface can still enforce an architectural boundary, enable a test seam, or isolate an external system. Judge the boundary by the job it performs, not an implementation count.

## Review procedure

When designing or reviewing an abstraction:

1. Name the existing concrete cases and the evidence that they are one concept, not merely similar code.
2. State what is stable, what varies, who owns each side of the boundary, and whether the cases should change together.
3. Ask whether leaving the code duplicated for now would be safer.
4. Inspect the generic layer for knowledge of concrete cases.
5. Check whether the public contract is smaller and more stable than its implementations.
6. Check that every implementation preserves the promised behavior without requiring callers to identify it.
7. Prefer the smallest correction: wait, inline, split, narrow, inject, or expose a block.

Explain the tradeoff in concrete terms. Do not recommend abstraction or duplication as a universal virtue; recommend the choice whose likely cost is lowest when the next real case arrives.
