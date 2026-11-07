---
name: codebase-map
description: Build a persistent, evidence-based map of a software repository inside docs/codebase-map/ - TL;DR, architecture and dependency diagrams in Mermaid, real data flows traced with an archetype-specific strategy, the most important files ("the spine"), a reading order, potentially AI-assisted code, key concepts, and open questions. Five modes - "codebase-map init" builds the full map, "codebase-map update" refreshes it after changes, "codebase-map explain [topic]" covers one feature or domain, "codebase-map trace [flow]" follows one request path, "codebase-map check" reports drift without writing. Use whenever the user wants to understand, document, or onboard into an unfamiliar or AI-generated codebase - "map this repo", "explain the architecture", "how does this app work", "trace this feature", "which files matter", "update the codebase map".
---

# Codebase Map

## Purpose

Build a persistent, evidence-based mental model of a software repository.

The goal is not merely to document the codebase.

The goal is to help the developer understand:

* how the system is structured
* where important logic lives
* how components depend on each other
* how real user requests move through the system
* which files are worth reading first
* which concepts are central to the application
* where AI-assisted or unfamiliar code may require additional attention
* what is still unknown

The output must remain inside the repository so it can be reused by the developer and future coding agents.

---

# Commands

The skill supports five modes. Accept them as commands, as natural language, or as a mix of both — `codebase-map update`, `/codebase-map update`, and "update the codebase map" all mean the same thing.

Resolve the mode before doing any work. When the mode is ambiguous, apply the default resolution rules below rather than asking, unless the choice would waste significant effort.

| Command | Mode | What it does |
| --- | --- | --- |
| `codebase-map` or `codebase-map init` | INIT | Full workflow. Build the complete map from scratch. |
| `codebase-map update` | UPDATE | Re-inspect the repository, refresh what changed, preserve what is still accurate. |
| `codebase-map explain <topic>` | EXPLAIN | Focused analysis of one feature, domain, or module. |
| `codebase-map trace <flow>` | TRACE | Trace a single user-facing flow end to end. |
| `codebase-map check` | CHECK | Verify the existing map against the repository. Report drift. Change nothing. |

## Default resolution

* No `docs/codebase-map/` directory and no explicit mode → INIT
* `docs/codebase-map/` already exists and no explicit mode → UPDATE
* A named feature, domain, or area in the request → EXPLAIN
* A named user action or request path → TRACE

Always state which mode is running in the first line of the response.

---

## INIT

Run the full workflow: Step 0, Step 0.5, then documents 1 through 9 and the INDEX.

If `docs/codebase-map/` already exists, say that INIT will overwrite it and confirm before proceeding, unless the request explicitly asks to rebuild from scratch.

---

## UPDATE

Do not regenerate everything.

1. Read the existing map, including INDEX.md.
2. Determine what changed. If the repository is a git repo and the map records a commit, diff against it (`git diff --stat <recorded-commit>..HEAD`). Otherwise compare the map's claims against the current file tree.
3. Re-inspect only the affected areas.
4. Update the documents those changes touch.
5. Preserve information that is still accurate, including the developer's own edits to the map.
6. Remove claims the implementation now contradicts.
7. Refresh the INDEX and the recorded commit.

Report in the response: what changed in the repository, which documents were updated, and which were left alone because nothing affecting them changed.

If the map is so far out of date that patching produces something incoherent, say so and recommend INIT rather than silently rebuilding.

---

## EXPLAIN

For a focused request such as `codebase-map explain payments`.

Do not analyze the whole repository.

1. Locate everything belonging to the named area: entry points, routes, services, models, jobs, configuration, tests, external integrations.
2. Trace how it works, using the archetype-appropriate strategy from Step 0.5.
3. Identify its boundaries: what it depends on and what depends on it.
4. Note the evidence labels and anything that could not be determined.

Write to:

```text
docs/codebase-map/04-data-flows/[topic].md
docs/codebase-map/04-data-flows/[topic].mmd
```

If the topic is a cross-cutting concern rather than a flow (authentication model, permissions, configuration), extend `08-key-concepts.md` instead of creating a flow document.

Add the new document to the INDEX. If the finding contradicts something in the existing map, correct it.

If no code matching the topic can be found, say so and list the closest candidates found instead of guessing.

---

## TRACE

For a single flow such as `codebase-map trace checkout`.

Same as EXPLAIN, but narrower: follow one user-facing request from trigger to response and back, producing one flow document and its diagram. Use the tracing strategy for the repository archetype.

Where the trace cannot continue — dynamic dispatch, an external service, a runtime-loaded plugin — say where it stopped and why rather than inventing the remaining steps.

---

## CHECK

Read-only. Write nothing, not even inside `docs/codebase-map/`.

Verify the existing map against the current repository:

* do the referenced paths still exist?
* do the entry points still match?
* do the documented flows still pass through the files they claim?
* have new major domains, services, or dependencies appeared that the map never mentions?
* are there INDEX links pointing at missing documents?

Report drift as a short list, worst first, and recommend UPDATE or INIT.

This mode is cheap on purpose. Use it in CI or before trusting a map you did not generate.

---

# Core principles

## 1. Inspect before explaining

Do not begin by guessing the architecture from filenames.

Inspect the actual implementation.

Follow, where applicable:

* imports
* exports
* function calls
* component relationships
* API routes
* API clients
* services
* database queries
* models
* authentication
* authorization
* external integrations
* background jobs
* queues
* event handlers
* configuration
* environment variables

---

## 2. Evidence over assumptions

Every important architectural statement should be based on repository evidence.

Use these confidence labels when useful:

### CONFIRMED

Directly supported by the implementation.

### INFERRED

Strongly suggested by the implementation but not explicitly established.

### UNKNOWN

The repository does not provide enough evidence to determine the answer.

Never present an inference as a confirmed fact.

Never invent missing architecture.

### File and line references

Cite locations as `path/to/file.ext:start-end`. A line reference may only be written for a file that was read in this session, from the line numbers actually seen. Never recall, estimate, or extrapolate a line number. If a file was not read in full, cite the file without line numbers rather than guess.

Before finishing, spot-check at least one reference per flow document against the file. A wrong line number is worse than none: it teaches the reader to distrust every other number in the map.

---

## 3. Implementation is the source of truth

Prefer:

1. actual implementation
2. configuration
3. tests
4. current documentation
5. comments

over stale documentation.

If documentation conflicts with the implementation, mention the conflict.

---

## 4. Do not modify application code

This skill is an analysis and documentation workflow.

Do not:

* refactor
* fix bugs
* change dependencies
* change configuration
* rename files
* restructure the application
* modify business logic

Only create or update files inside:

```text
docs/codebase-map/
```

If that directory does not exist, create it.

---

## 5. Depth over summary

The map is a reference a developer will navigate, not a summary they will skim. Every document should contain something the reader could not have learned from the file tree and function names alone.

Read files in full. Cite concrete values: thresholds, limits, timeouts, versions. Record failure branches, not only happy paths. Record what is absent, not only what is present.

If context pressure forces a choice between covering more of the repository shallowly and covering the important parts deeply, choose depth and record the gap under "What was not explored".

---

# Output structure

Create the following structure:

```text
docs/
└── codebase-map/
    ├── INDEX.md
    ├── 01-tldr.md
    ├── 02-system-architecture.md
    ├── 02-system-architecture.mmd
    ├── 03-dependency-graph.md
    ├── 03-dependency-graph.mmd
    ├── 04-data-flows/
    │   ├── [feature-name].md
    │   ├── [feature-name].mmd
    │   └── ...
    ├── 05-the-spine.md
    ├── 06-recommended-reading-order.md
    ├── 07-potentially-ai-assisted-code.md
    ├── 08-key-concepts.md
    └── 09-open-questions.md
```

Do not create unnecessary files.

For a small repository, simplify the structure when appropriate while preserving the important information.

---

# Workflow

## Step 0 — Repository reconnaissance

Before creating the final documents, inspect the repository.

Identify:

* application entry points
* major directories
* frontend
* backend
* API layer
* business logic
* database layer
* authentication
* authorization
* external services
* background processing
* configuration
* tests
* generated code
* scripts
* infrastructure

Determine the major architectural domains.

Examples:

```text
Frontend
Backend
API
Database
Authentication
Payments
Notifications
Background Jobs
External Integrations
```

Do not assume these domains exist. Use only domains supported by the repository.

For large repositories, analyze domains/modules first and then build the system-level map from those results.

---

## Step 0.5 — Identify the repository archetype

Before tracing anything, determine what kind of system this is.

The archetype decides *how* to trace, not just *what* to document. Tracing a CLI tool the same way as a React application wastes effort and produces a misleading map.

Use repository evidence: manifests, entry points, framework fingerprints, directory layout, build and deployment configuration.

| Archetype | Tracing strategy | Primary data-flow output |
| --- | --- | --- |
| Frontend application | Start from a visible value or screen and trace backward to its source | Render path: component → state → data source |
| Backend API / service | Trace the request lifecycle from route to response | Request lifecycle trace |
| Full-stack application | Combine both: start at the user action, cross the network boundary, continue to the data store | End-to-end request trace |
| CLI tool | Trace command parsing → command handler → side effects | Command execution trace |
| Library / SDK | Trace the public API surface inward to the core implementation | Abstraction layer map |
| Data / ETL pipeline | Trace one record through every stage and transformation | Data lineage map |
| Background worker / queue consumer | Trace job enqueue → handler → retries → completion | Job lifecycle trace |
| Infrastructure as code | Trace resource dependencies and what changes together | Blast-radius map |
| Monorepo | Identify the archetype of each significant package, then map cross-package dependencies | Per-package flows plus a package dependency map |

A repository may combine archetypes. Record every archetype that applies and say which one drives each data flow.

State the detected archetype(s) in `01-tldr.md`, with the evidence that supports the classification.

If the archetype cannot be determined confidently, label it UNKNOWN, explain what is ambiguous, and fall back to tracing entry points.

---

# 1. TL;DR

Create:

```text
docs/codebase-map/01-tldr.md
```

Explain the application in a way that a developer can understand quickly.

Include:

* what the application does
* main architectural style
* major domains
* main entry points
* primary data stores
* important external services
* important architectural observations
* biggest areas of complexity

End with:

## If you remember only 5 things

List the five most important facts a developer should remember about the system.

Keep this document concise.

---

# 2. System architecture

Create:

```text
docs/codebase-map/02-system-architecture.md
docs/codebase-map/02-system-architecture.mmd
```

Explain the high-level architecture.

Include, when applicable:

* clients
* frontend
* backend
* API
* services
* business logic
* database
* caches
* queues
* background workers
* external APIs
* authentication providers
* storage

The Mermaid diagram should show relationships between major architectural components.

Prefer a high-level diagram over a huge file-by-file diagram.

Example structure:

```text
User
  ↓
Frontend
  ↓
API
  ↓
Application Services
  ↓
Database
```

Add external systems where relevant.

---

# 3. Dependency graph

Create:

```text
docs/codebase-map/03-dependency-graph.md
docs/codebase-map/03-dependency-graph.mmd
```

Map important dependencies between modules/files.

Do not attempt to put every file into one unreadable graph.

Identify:

* major entry points
* core modules
* highly connected modules
* important shared utilities
* important dependency chains
* circular dependencies
* suspicious coupling
* unusual architectural relationships

If the repository is large, create a high-level graph rather than a massive unreadable graph.

The Markdown document should explain the important relationships discovered in the graph.

---

# 4. Data flows

Create 3–5 representative real user flows.

Prioritize flows that teach the developer how the application actually works. Always include the flow that carries the product's core value — the thing the application exists to do.

Good examples include:

* sign up
* login
* create a resource
* update a resource
* checkout
* payment
* file upload
* search
* dashboard loading
* notification
* background job

For every selected flow create:

```text
docs/codebase-map/04-data-flows/[feature-name].md
docs/codebase-map/04-data-flows/[feature-name].mmd
```

Select the flows and the tracing strategy based on the archetype identified in Step 0.5. For a CLI tool, trace commands rather than inventing UI layers. For a pipeline, follow one record through the stages. For a frontend, start from the visible value and trace backward.

Trace the request as far as the repository allows. Read every file on the path in full before writing. Do not summarize a step from its function name.

## Required structure of every flow document

Each flow document uses exactly these sections, in this order. Sections are not optional; if one has nothing to say, write one line explaining why.

```markdown
# Flow N — [Name]

Archetype strategy: [which strategy from Step 0.5 and why]. Diagram: [link to .mmd]

## Trigger
What starts this flow. Every caller of the entry point, including the ones that are not the obvious user action (timers, other flows, lifecycle hooks, crash recovery).

## Path — [CONFIRMED unless labelled]
Numbered steps. Every step names the function and cites `path/to/file.ext:start-end`. Every step that is not directly observed in code is labelled INFERRED or UNKNOWN inline. Include the concrete values that govern behaviour: thresholds, timeouts, limits, batch sizes, retry counts, feature flags.

## Data touched
Table: value | where it is stored | which flow writes it. Include in-memory state that outlives the request, not only the database.

## Failure modes — [CONFIRMED from code, not observed]
Table: failure | what the code does | what the user sees. Cover every external call, every early return, every swallowed exception, every null-returning branch. Say explicitly when a failure is silent.

## What is NOT in this flow
Things a reader would reasonably expect here and will not find: features described in the README or comments but not implemented, code that exists but is never called on this path, stale comments referring to removed behaviour, tables or models that are written but never read.

## Observations — [INFERRED, not verified at runtime]
Race conditions, ordering assumptions, performance characteristics, inconsistencies between constants and documentation. Each observation states what it is based on.

## Where the trace stops
The exact point where repository evidence ends — external service internals, dynamic dispatch, platform behaviour, runtime configuration — and why. If the trace reached the end, say so.
```

The failure-mode table is the most valuable section and the one most often skipped. A happy-path diagram hides every place where work is silently discarded. Write this section from the code's error branches, not from imagination.

Depth is the point. A flow document for a non-trivial feature typically runs 60–150 lines. A flow that fits in fifteen lines has been summarized, not traced.

## Diagram for each flow

The `.mmd` file is a sequence diagram for request-style flows and a flowchart for read-path or fan-out flows. Embed the same diagram in the `.md` file inside a mermaid code block so the document reads standalone.

Label edges with the mechanism where it matters: stream, callback, HTTP method, event name, `await` vs fire-and-forget.

---

# 5. The Spine

Create:

```text
docs/codebase-map/05-the-spine.md
```

Identify approximately 5–15 files or modules that are especially important for understanding the system.

For each include:

* path
* responsibility
* why it matters
* what it connects to
* what a developer should understand before reading it

Think of this as:

> "If I only have one hour to understand this repository, these are the files I should read."

---

# 6. Recommended reading order

Create:

```text
docs/codebase-map/06-recommended-reading-order.md
```

Create a practical reading sequence.

Example:

```text
1. README
2. Application entry point
3. Main routing
4. Authentication
5. Core domain
6. API layer
7. Database layer
8. Important feature flow
9. Background jobs
10. External integrations
```

Use actual repository paths.

For every step explain briefly:

* what to read
* why to read it
* what concept it teaches

The goal is to minimize random file browsing.

---

# 7. Potentially AI-assisted code

Create:

```text
docs/codebase-map/07-potentially-ai-assisted-code.md
```

Identify code that may deserve additional human review.

Possible signals:

* repetitive generated-looking code
* unusually verbose implementations
* inconsistent patterns
* duplicated logic
* comments that explain obvious code excessively
* abstractions inconsistent with surrounding code
* suspiciously generic naming
* TODO-heavy implementations
* code that does not match established project conventions
* complex code with weak or missing tests

Do NOT claim:

> "This code was written by AI."

Instead use language such as:

> "This section has characteristics that may indicate AI assistance or generated code and deserves manual review."

Clearly distinguish evidence from speculation.

---

# 8. Key concepts

Create:

```text
docs/codebase-map/08-key-concepts.md
```

Explain the concepts a developer needs to understand before comfortably modifying the repository.

Include things such as:

* domain concepts
* important entities
* important abstractions
* architectural patterns
* state management
* authentication model
* authorization model
* data model
* event system
* important conventions
* unusual implementation decisions

End with:

## Follow one real request

Choose one representative request and summarize its journey through the system.

Example:

```text
User clicks "Create"
→ CreateForm
→ useCreateProject()
→ POST /api/projects
→ projectController
→ projectService
→ ProjectRepository
→ PostgreSQL
→ response
→ UI state update
```

Use actual repository paths.

---

# 9. Open questions

Create:

```text
docs/codebase-map/09-open-questions.md
```

Record things that cannot confidently be determined.

Examples:

* unclear ownership of a module
* unused-looking code
* undocumented external service
* unclear authentication behavior
* conflicting documentation
* unexplained configuration
* possible dead code
* unclear background job behavior
* uncertain data lifecycle

Separate:

### Confirmed unknowns

The repository clearly does not provide the answer.

### Questions for the developer

Questions that require domain/business knowledge rather than more code inspection.

Do not turn guesses into answers.

## What was not explored

State the boundaries of this map explicitly. A map that silently looks complete is worse than one that admits its edges.

List:

* directories or packages that were not inspected, and why (low centrality, generated code, vendored dependencies, time or size limits)
* areas inspected only at surface level rather than traced
* flows that were not traced
* code paths that could not be followed (dynamic dispatch, reflection, runtime plugin loading, configuration-driven behavior, external services with no local implementation)
* anything blocked by missing access, missing environment variables, or missing credentials

Be specific. Write "`packages/legacy-import/` was not inspected" rather than "some areas were skipped."

If coverage is high, say so plainly and note what remains.

---

# 10. INDEX

Create:

```text
docs/codebase-map/INDEX.md
```

This is the entry point.

Include:

* short description
* links to every generated document
* architecture diagram link
* dependency graph link
* data flow links
* recommended reading order
* the date the map was generated or last updated
* the commit the map was generated from, when the repository is a git repo — record the short hash (`git rev-parse --short HEAD`), since UPDATE and CHECK rely on it to detect drift

Recommended structure:

```text
# Codebase Map

## Start here

- [TL;DR](./01-tldr.md)
- [System Architecture](./02-system-architecture.md)
- [The Spine](./05-the-spine.md)
- [Recommended Reading Order](./06-recommended-reading-order.md)

## Architecture

- [System Architecture Diagram](./02-system-architecture.mmd)
- [Dependency Graph](./03-dependency-graph.md)
- [Dependency Graph Diagram](./03-dependency-graph.mmd)

## Data Flows

- [Feature A](./04-data-flows/feature-a.md)
- [Feature B](./04-data-flows/feature-b.md)

## Understanding

- [Key Concepts](./08-key-concepts.md)
- [Potentially AI-Assisted Code](./07-potentially-ai-assisted-code.md)
- [Open Questions](./09-open-questions.md)
```

Update the INDEX whenever other files are created or renamed.

---

# Diagram rules

Use Mermaid.

Prioritize readability.

Do not create diagrams that are technically complete but impossible to understand.

Prefer:

```text
high-level architecture
        ↓
domain relationships
        ↓
important dependencies
        ↓
specific data flows
```

over one enormous graph.

If a graph becomes too large, split it.

Every diagram should answer a specific question.

## Conventions

Use the same visual language in every diagram so a reader learns it once:

* Code that exists but is never called, or a model that is never used, gets a dashed grey style. Define it once and apply it by class rather than by node label:

```text
classDef unwired stroke-dasharray: 5 5,stroke:#999,color:#999;
class ProgressionService,GridCell unwired;
```

* Dashed edges (`-.->`) mean an indirect or conditional relationship: a stream subscription, a fire-and-forget call, an import that is never invoked. Label the edge with the reason.
* Solid edges mean a direct synchronous call or a hard dependency.
* Data stores use the cylinder shape `[(name)]`. External services and third-party packages use the stadium shape `([name])`.
* Group by deployment boundary in the system architecture diagram, and by directory in the dependency graph. Do not mix the two in one diagram.
* Node labels carry identity, not findings. Put "not wired in" in a style and a note, not in the node text.

---

# Large repository rules

For large repositories:

1. identify major domains
2. understand each domain
3. map important dependencies between domains
4. identify system-level entry points
5. create focused data-flow diagrams
6. avoid analyzing every file equally

Prioritize files based on:

* dependency centrality
* entry-point relevance
* business importance
* architectural importance
* frequency of use
* complexity

Do not spend equal effort on trivial files and core architecture.

---

# Incremental updates

See the UPDATE and EXPLAIN modes in the Commands section.

The principle: never regenerate what has not changed, and never preserve what the implementation now contradicts.

---

# Quality checks

Before finishing, verify:

* the repository archetype is identified and the data flows match it
* all important entry points are represented
* what was not explored is stated explicitly
* architecture matches implementation
* diagrams are readable
* important dependencies are represented
* at least 3 useful data flows exist for a sufficiently large application
* every flow document has all seven required sections, including a failure-mode table
* every file:line reference comes from a file read in this session, and at least one per flow was spot-checked
* paths actually exist
* claims are evidence-based
* inferred information is labeled
* unknown information is not fabricated
* INDEX links are valid
* no application code was modified

---

# Final response

The chat response should be short.

Do not paste the generated documentation into chat.

Report only:

* which mode ran
* what was created or updated
* number of data flows
* major areas mapped
* important unknowns
* any limitations or issues encountered

The persistent files are the primary output.

---

# Behavior summary

When this skill is invoked:

```text
Inspect
  ↓
Identify archetype
  ↓
Understand
  ↓
Map
  ↓
Trace real flows
  ↓
Identify important files
  ↓
Document evidence
  ↓
Generate Mermaid diagrams
  ↓
Write persistent artifacts
  ↓
Validate
```

The objective is not to make the AI sound like it understands the codebase.

The objective is to make the developer actually understand it.
