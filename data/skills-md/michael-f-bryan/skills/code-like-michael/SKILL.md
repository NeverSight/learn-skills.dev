---
name: code-like-michael
description: "Write, refactor, review, and shape repositories in Michael's style. Use when the user wants code or repo structure that feels like Michael wrote it: explicit boundaries, typed contracts, pragmatic framework at hard edges, late abstraction, early codegen, drift-aware verification."
---

# Code Like Michael

Treat this skill as binding unless the repository already has stronger local conventions.

The goal is not "clean code" in the abstract. The goal is to produce code and repo shape that make ownership, execution order, contracts, and operational behaviour obvious.

## Non-Negotiables

Always prefer:
- visible composition roots
- responsibility-shaped modules, crates, or packages
- typed contracts at important boundaries
- local wrappers only where semantics begin
- handwritten abstraction only after the seam is stable
- generation and drift checks for mechanical repetition
- realistic seam tests over mock theatre

Do not optimise for:
- abstract symmetry
- service/repository scaffolding by default
- purity facades over real platform boundaries
- deduplication before semantic sameness is proven
- hiding unfinished work behind generic abstractions

## Agent Default

If you are unsure what Michael would do, choose the option that (in order):

1. keeps the top-level flow easier to read
2. makes the boundary contract more explicit
3. avoids introducing a new abstraction layer
4. tests the real seam that can fail
5. makes docs, schemas, diagnostics, or generated output harder to drift

When trading off reduction of duplication vs clearer flow vs stronger data model vs fewer layers vs quicker delivery: prefer clearer flow and stronger data model over deduplication; prefer fewer layers over new abstractions; prefer real seams and drift checks over mock coverage.

## Repo-Shaping Rules

Use these defaults when creating or restructuring a repository:

- Prefer a modular monolith: one delivery unit with clear internal boundaries. Split into separate services or repos only when execution mode, ownership, lifecycle, or operational boundary makes it necessary.
- Start compact, but split early when there are distinct execution modes, ownership boundaries, or tooling surfaces.
- Keep one obvious composition root per executable surface: `main`, `run`, `serve`, CLI command, worker bootstrap, or router setup.
- Separate reusable core from shells early.
- Add a dedicated repo-tooling surface once generation, release, docs, or compatibility workflows exist. In Rust this often means `xtask`; in app repos it may mean `tools/`, `scripts/`, or a dedicated package.
- Keep apps, libs, infra, generated contracts, and docs legible as separate concerns inside one repo when they belong to one delivery unit.

Avoid:
- one giant package mixing runtime, release, codegen, tests, and infra concerns
- microservice-style fragmentation before there are real responsibility boundaries
- repo shapes named after patterns instead of responsibilities

For repo-level guidance, read [references/repo-shaping.md](references/repo-shaping.md).

## Boundary Rule

Choose strictness by boundary type, not by slogan.

- Fail early at integrity boundaries: config, auth, IDs, request shape, transport status, schema input, unsafe defaults.
- Continue with structure when downstream diagnostics are the product: parsers, compilers, analysis pipelines, validation/reporting flows.

Any tolerance should be explicit in types, policy, or API shape. Do not rely on silent best effort.

## Code-Shaping Rules

Prefer:
- thin orchestration at the top
- medium-sized flow functions when they make execution order obvious
- smaller helpers for detailed rules
- stage-shaped or boundary-shaped modules
- explicit structs, enums, and named boundary types
- stable, contextual, lowercase errors; wrap with context at meaningful boundaries only, not every line; reserve panics/assertions for actual invariants

Avoid:
- deep constructor chains that hide startup order
- generic `utils`, `common`, `manager`, or `processor` modules
- reflection-heavy or magical conversion code
- framework or protocol types leaking inward once local semantics begin

## Data Modelling

Domain modelling and interaction design are central to this style. The agent should have strong opinions here: the shape of the code should help people do the right thing by default.

**Core idea**

The model should make the system easier to *discover* (types carry meaning; better autocomplete, docs, and signatures) and harder to *misuse* (invalid states excluded where practical; operations only when preconditions hold). This is not "types for types' sake"—it is about APIs and domain models that are legible under tooling and resistant to accidental misuse. Types are executable documentation, not just for the compiler.

**Key principles**

- **Correctness through construction:** Prefer construction paths that return a *fully usable* value or fail immediately. Avoid `NewX()` then `Initialize()` / `Connect()` / `Start()` on otherwise incomplete objects—that leaves invalid intermediate states and hidden lifecycle rules. RAII-style: if a value exists, it has already satisfied the invariants that define it.
- **Make invalid states unrepresentable:** Use distinct types for IDs, enums/tagged unions for closed sets, lifecycle-specific types, private representation, validated inputs at boundaries. Downstream code then does not have to defend against already-ruled-out cases.
- **State-specific behaviour:** Encapsulate state; expose only the operations that are valid in the current state; require an explicit transition to a new state with a different API. Avoid "god objects" with methods that are only valid in certain phases. Each lifecycle phase gets its own type or narrow interface (e.g. unvalidated config vs validated runtime config; disconnected vs authenticated client; draft vs submitted command).
- **Encapsulation:** Keep representation private so callers cannot reassemble invalid combinations. Prefer constructors, factories, and methods that preserve invariants over public mutable fields.
- **Practical, not dogmatic:** Use the type system where it buys real leverage (discovery, fewer invalid states, clearer lifecycles, simpler downstream code). No maximalist type-level programming. A good modelling choice should pay for itself in editor guidance, clearer signatures, fewer runtime checks, or fewer impossible branches—if it does not, it may be too clever.

**Rules of thumb**

- Prefer named domain types over raw primitives when the value has real semantics.
- Prefer enums, tagged unions, and explicit variants over stringly-typed mode fields.
- Prefer constructors and factory functions that return fully usable objects or fail immediately.
- Avoid `initialize()`, `connect()`, `load()`, or `start()` on otherwise incomplete objects unless the lifecycle is genuinely external and cannot be made safer.
- Prefer lifecycle-specific types or objects when different phases allow different operations.
- Keep internal representation private when exposing it would let callers bypass invariants.
- Use the type system to improve autocomplete, editor guidance, and generated docs, not just correctness.
- Do not collapse multiple distinct workflows into one "options bag" API just to save a few type definitions.
- Do not introduce wrapper types mechanically; introduce them when they remove ambiguity, encode validation, or make downstream code materially clearer.
- In dynamic languages, apply the same principles with validation, frozen data structures, factory functions, and narrower public APIs.

**Prefer:** domain types over primitive strings/ints where semantics matter; making invalid states unrepresentable where practical; explicit enums/unions for closed sets; boundary DTOs separate from core domain types when policies differ; narrow interfaces owned by the consuming domain.

**Avoid:** `map[string]any` / `dict[str, Any]` / `serde_json::Value` as long-lived internal shapes; passing transport-shaped structs deep into the core; generic "metadata" or "options" bags when the shape is already known.

For the full narrative and write-this-not-that code examples, see [references/data-modelling.md](references/data-modelling.md).

## Abstraction Threshold

Do not introduce a handwritten abstraction until one of these is true:

- the repeated shape is semantically identical
- the concern is globally cross-cutting
- the boundary genuinely varies
- lifecycle or concurrency ownership needs a seam

Do introduce generation early when repetition is mechanical:

- grammar-driven syntax trees
- schema-driven models
- generated diagnostics or code tables
- API contracts and clients

Default rule:
- tolerate the first duplication
- inspect the second
- abstract on the third only if the behaviour is truly the same

Introduce abstraction decisively once lifecycle ownership, policy reuse, or stable semantic sameness is clear—not before, but not never.

## Framework, Dependencies, And DI

Michael is not anti-framework. He is anti-fake-boundary.

Use frameworks, code generators, and managed platforms directly when they are the honest outer boundary:
- routers
- GraphQL
- SQL/query generation
- OpenAPI
- Temporal/workflow engines
- Terraform
- managed auth/storage platforms

Wrap them only where local policy or semantics begin.

Prefer:
- explicit parameter passing
- builders
- tiny interfaces at IO seams
- focused dependencies with a clear job

Avoid:
- DI containers
- deep trait graphs
- repository/service layers with no real second implementation
- dependency sprawl that adds complexity without leverage

## Contracts, Docs, And CI

Treat these as product surfaces:
- generated code
- schemas
- diagnostics catalogues
- user-facing docs
- release metadata
- DB policies and migrations

Default moves:
- commit important contract artefacts when the repo expects them
- add drift checks for anything humans would otherwise forget to regenerate
- keep README concise and practical
- add architecture/ADR/spec docs when decisions are durable or externally significant
- build CI around fast feedback: build, tests, lint/format, and regeneration/drift checks first
- add docs publishing, release automation, or deploy steps when the repo has real consumers or a live service

## Testing Rule

Bias toward strong verification, not ritualised TDD.

Prefer:
- request-path tests
- fixture tests
- parser or snapshot tests
- DB/container/integration tests
- corpus tests
- generated-artefact drift checks

Use mocks or tiny fakes only when the seam is already real and the full boundary is too expensive.

Do not invent an interface just so a unit test can exist.

## Operational Concerns

Treat observability, migrations, and rollout as first-class.

Prefer:
- explicit metrics, traces, and logs at important boundaries and lifecycle edges—not buried in magic middleware
- additive DB migrations
- visible lifecycle ownership
- deterministic failure modes in orchestration and workflow code

## Review Hygiene

Prefer:
- small, reviewable diffs
- refactors separated from behavioural changes in distinct commits or PRs
- generated artefacts committed when reproducibility depends on them
- TODOs that make incompleteness visible instead of hiding it behind abstraction

## Defaults By Language

- **Go:** constructors/builders; sentinel errors by default, typed errors when callers need to branch; tiny interfaces at IO seams.
- **Rust:** newtypes/enums for domain meaning; explicit ownership; generation for mechanical repetition.
- **Python:** typed boundary models; small modules; avoid magical metaprogramming unless it buys clear leverage.
- **TypeScript:** explicit schema/type boundaries; generated API types where possible; avoid helper soup and over-generic hooks; keep frontend state and data-fetching seams clear.

## Review Triggers

The result is off-style if:

- the repo shape hides clear ownership boundaries or over-splits before real boundaries exist
- the main flow is hard to recover without tracing multiple abstractions
- a boundary contract is implicit when it should be typed, schematised, generated, or policy-backed
- the data model allows invalid states or uses loose bags of primitives where domain types would clarify
- validation is buried deep in domain logic
- a shared helper deduplicates code that is still semantically different
- a framework facade exists only for stylistic purity
- generated or documented output can drift silently
- tests mostly prove mocked choreography instead of real behaviour
- refactors are mixed with behaviour changes in one large diff
- observability is absent at important boundaries or assumed to be "in the framework"

## Delivery Checklist

Before returning code, check:

- [ ] Is the repo or module shape aligned to real responsibilities (modular monolith unless split is justified)?
- [ ] Is execution order obvious from one composition root per executable surface?
- [ ] Are important boundaries expressed in types, schemas, generated artefacts, or policy?
- [ ] Does the data model use domain types and avoid invalid states where practical?
- [ ] Is validation happening at the correct edge for this boundary type?
- [ ] If bad input is tolerated, is that because richer downstream diagnostics are the product?
- [ ] Did I avoid introducing a new abstraction layer unless the seam is stable?
- [ ] Did I keep frameworks visible at the edge and stop them from defining the core?
- [ ] Do the tests exercise a real seam, corpus, fixture, or drift surface?
- [ ] Can docs, diagnostics, schemas, or generated code drift without a failing check?
- [ ] Are refactors separate from behaviour changes? Is the diff reviewable?
- [ ] Are observability touchpoints explicit at important boundaries where needed?

## Additional Resources

- For data modelling philosophy, construction, state-specific APIs, and write-this-not-that examples, read [references/data-modelling.md](references/data-modelling.md)
- For concrete "write this instead of that" examples (repo shape, composition, naming, boundaries, validation, abstraction, DI, errors, tests), read [references/write-this-not-that.md](references/write-this-not-that.md)
- For boundary and abstraction choices, read [references/boundary-playbook.md](references/boundary-playbook.md)
- For repo topology, docs, CI, dependencies, and rollout defaults, read [references/repo-shaping.md](references/repo-shaping.md)
