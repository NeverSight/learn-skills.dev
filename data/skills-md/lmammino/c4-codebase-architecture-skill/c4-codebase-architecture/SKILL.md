---
name: c4-codebase-architecture
description: Helps an agent inspect a repository and produce C4 architecture documentation. Use this when reverse engineering a codebase, documenting system context, containers, components, or clarifying architecture from code and infrastructure.
license: MIT
---

# C4 Model Codebase Documentation Skill

## Purpose

This skill helps an agent inspect a codebase and produce useful C4-style architecture documentation. It should combine evidence from the repository with targeted follow-up questions whenever code inspection alone is not enough to determine system boundaries, responsibilities, runtime topology, or business intent.

The skill should be pragmatic rather than dogmatic. The goal is not to force every repository into a perfect set of four diagrams, but to produce the clearest possible architecture view at the right level of detail.

---

## When to use this skill

Use this skill when the user wants to:

* understand the architecture of an existing codebase
* produce C4 documentation for a repository
* generate a system context, container, or component view
* onboard new engineers with architecture docs
* reverse engineer system structure from code and infrastructure definitions
* compare intended architecture with implemented architecture

This skill works best when the repository includes at least some of the following:

* source code
* infrastructure as code
* deployment descriptors
* README or docs
* API specifications
* CI/CD configuration
* test suites

---

## What this skill should produce

The skill should aim to produce some or all of the following, depending on what the codebase supports:

1. **System Context**

   * the system under study
   * human users or personas
   * external systems, APIs, providers, or dependencies
   * key relationships

2. **Container view**

   * main deployable or runnable units
   * databases, queues, frontends, APIs, workers, serverless functions, data stores
   * protocols and interactions between them

3. **Component view**

   * major internal components within a selected container
   * their responsibilities and relationships

4. **Supporting narrative**

   * assumptions made from code inspection
   * unresolved ambiguities
   * questions for the user
   * notable architectural risks or mismatches

5. **Optional diagram source**

   * Mermaid, PlantUML, Structurizr DSL, or plain text diagram descriptions

Unless explicitly requested, the skill does **not** need to generate a full Code-level diagram. It may mention classes, modules, or packages only when that materially improves understanding.

---

## Default operating principles

### 1. Evidence first

Base architectural claims on observable evidence from the repository where possible. Prefer:

* entrypoints
* routing definitions
* package manifests
* deployment descriptors
* infrastructure code
* environment variable usage
* API clients and SDK usage
* integration tests
* queue/topic usage
* persistence code

Do not present guesses as facts.

### 2. Separate facts from inference

When inferring architecture from code, clearly label it as an inference.

For example:

* **Observed**: The repository contains a React app, an Express API, and Terraform for an RDS instance.
* **Inferred**: The system likely uses a browser-based frontend calling a backend API backed by PostgreSQL.

### 3. Ask only high-value questions

When code inspection is insufficient, ask concise, high-leverage questions in batches. Avoid interrogating the user for details that are probably discoverable in the code.

### 4. Respect system boundaries

A repository is not always the whole system. Be explicit about whether the documented scope is:

* this repository only
* a single service within a larger platform
* a monorepo containing multiple systems
* a partial implementation of a broader architecture

### 5. Default to useful levels of detail

Usually the most useful outputs are:

* a System Context diagram
* a Container diagram
* one or two Component diagrams for key containers

Do not force component breakdowns for trivial services.

---

## Repository analysis workflow

### Phase 1: Establish scope

Start by determining what the repository appears to represent.

Look for:

* repo name
* README summary
* workspace or monorepo structure
* top-level folders
* package manifests
* build files
* infrastructure folders
* deployment folders
* docs folders

Try to answer:

* What system or subsystem is this?
* Is this a full product, a service, a library, or infrastructure?
* What is inside scope and outside scope?

If scope is ambiguous, ask the user.

### Phase 2: Identify runtime building blocks

Find the main executable or deployable units.

Look for:

* web frontends
* backend services
* CLI tools
* serverless functions
* workers or scheduled jobs
* databases
* caches
* queues and streams
* search engines
* storage buckets
* third-party SaaS dependencies

Important note: for C4, a "container" means a deployable or runnable unit, not specifically a Docker container.

### Phase 3: Identify interactions

Map how the runtime building blocks interact.

Look for:

* HTTP clients and servers
* SDK calls
* message publishing or consuming
* database access layers
* authentication middleware
* event handlers
* cron or scheduler configuration
* file or object storage access

Try to capture:

* direction of flow
* transport or protocol where visible
* synchronous vs asynchronous behavior
* trust boundaries

### Phase 4: Infer actors and external systems

Code often reveals external systems but not always end users or business actors.

Look for:

* auth providers
* payment systems
* email providers
* cloud services
* partner APIs
* identity systems
* observability systems

For actors, infer cautiously from:

* UI labels
* route names
* domain language
* role checks
* documentation

If user personas are not obvious, ask the user.

### Phase 5: Break down important containers into components

For the most important or complex containers, identify major internal components.

Look for:

* modules
* packages
* feature folders
* controllers
* services
* repositories
* adapters
* domain layers
* handlers
* middleware

A good component breakdown usually focuses on responsibilities, not file-by-file enumeration.

Avoid producing a component diagram that is just a dump of folder names.

### Phase 6: Produce documentation

Produce the final output with:

* stated scope
* assumptions
* C4 views
* clarifying questions if needed
* diagram source if requested

---

## Questions the skill may ask the user

Ask questions only when they materially improve correctness. Prefer batching 3 to 7 questions together.

### About scope

* Is this repository the whole system, or just one service within a larger platform?
* Do you want the documentation to cover only what is in the repo, or also adjacent systems it depends on?
* Is there a preferred audience for the diagrams, such as new engineers, stakeholders, or operations teams?

### About actors and personas

* Who are the primary users or operators of this system?
* Are there distinct personas or roles, such as customer, admin, support, or partner?
* Is there an internal operations team that should appear in the system context view?

### About deployment/runtime topology

* Are the deployable units in the repo also the real runtime containers in production?
* Are there important external pieces not represented in code here, such as managed databases, external queues, or shared gateways?
* Is this deployed as a monolith, microservices, serverless functions, or something hybrid?

### About system boundaries

* What should be considered outside the system boundary for the context diagram?
* Are shared platform services owned by another team and therefore better shown as external systems?

### About ambiguous dependencies

* Is this external dependency central enough to show explicitly in the diagrams?
* Should infrastructure services like S3, Redis, or EventBridge be shown as containers inside the system or as external managed services?

### About components

* Which container would you like the component diagram to focus on?
* Do you want a domain-oriented breakdown, a technical-layer breakdown, or the structure that most closely matches the code?

### About output format

* Do you want Mermaid, PlantUML, Structurizr DSL, or just textual documentation?
* Would you prefer concise docs or something more explanatory and onboarding-friendly?

---

## Heuristics for common codebase shapes

### Monolith

If the repo contains one main application plus a database, the likely outputs are:

* Context: users, system, external integrations
* Container: web app or API, database, maybe background worker
* Component: controllers, services, repositories, integrations

### Monorepo with frontend and backend

If the repo contains multiple apps or packages:

* identify which are independently deployable
* separate libraries from containers
* show shared libraries only when they help explain architecture

### Serverless system

For serverless architectures:

* group functions into meaningful runtime containers where appropriate
* avoid diagramming every function unless the user explicitly wants that level of detail
* show API Gateway, queues, buckets, event buses, and data stores where relevant
* consider "API", "Async worker", and "Scheduled processor" as possible containers even if implemented as multiple functions

### Microservices

For microservices repos:

* show each independently deployable service as a container
* identify service-to-service communication paths
* be careful not to confuse libraries or packages with services

### Library or SDK

If the repo is primarily a library, full C4 documentation may be inappropriate. In that case:

* explain that the repository is not itself a complete runtime system
* document its role in a larger context if the user provides that context
* optionally create a smaller context and component view for the library itself

---

## Output template

Use the following structure by default.

### 1. Scope

State what is being documented and any important scope boundaries.

Example:

> This documentation covers the architecture implied by the current repository. It appears to represent the backend service and its deployment configuration, but not the full end-user platform.

### 2. Observations from the codebase

Summarize the strongest concrete signals found in the repository.

Example:

* React frontend in `apps/web`
* Node.js API in `apps/api`
* PostgreSQL dependency and migration scripts
* Terraform modules for VPC, ECS, RDS, and SQS
* background worker consuming queue messages

### 3. Assumptions and inferences

List anything that is inferred rather than directly observed.

### 4. System Context

Provide a short explanation and, if requested, a diagram definition.

### 5. Container view

Provide a short explanation and, if requested, a diagram definition.

### 6. Component view

Focus on one or more important containers only.

### 7. Open questions

List unresolved ambiguities that would improve the documentation if clarified.

### 8. Suggested next refinements

Recommend what to clarify or document next.

---

## Diagramming guidance

### General guidance

Every diagram should:

* have a clear title
* define its scope
* use descriptive box labels
* label relationships with short verbs or phrases
* include key technology details only where useful
* avoid visual clutter

### Labeling examples

Prefer:

* `Web Application\nReact SPA used by customers`
* `Orders API\nNode.js service handling checkout and order retrieval`
* `PostgreSQL\nStores users, orders, and payment state`

Over vague labels like:

* `Frontend`
* `Backend`
* `DB`

### Relationship examples

Prefer labels like:

* `Submits order via HTTPS`
* `Reads product catalog`
* `Publishes job messages`
* `Verifies identity token`

Avoid unlabeled arrows.

---

## How to treat infrastructure and managed services

The skill should use judgment when placing cloud resources in C4 diagrams.

### Good candidates for container-level visibility

Show these when they materially affect architecture:

* primary databases
* message queues
* event buses
* object storage used as a core workflow element
* caches
* search engines
* identity providers
* major external APIs

### Usually too low-level unless relevant

These are often implementation details unless central to the design:

* subnets
* security groups
* IAM roles
* autoscaling policies
* log groups
* CI runners

### Boundary judgment

When in doubt:

* if the team owns and reasons about it as part of the application architecture, it may belong inside the system boundary
* if it is a platform dependency provided by another team or vendor, it may be better as an external system

---

## Quality bar for the skill

A good result should be:

* faithful to the codebase
* explicit about uncertainty
* useful to humans
* free from box-and-arrow soup
* focused on important runtime structure

A poor result would:

* confuse packages with deployable units
* invent actors with no evidence
* over-document trivial details
* produce diagrams with many unlabeled arrows
* blur the boundary between facts and guesses

---

## Example interaction pattern

### Example opening

> I inspected the repository and I can already see a frontend app, an API service, a worker, and some infrastructure code for a PostgreSQL database and SQS queue. I can draft a first-pass System Context and Container view from that.
>
> Before I finalize it, I need to clarify a few things that the code does not make fully explicit:
>
> 1. Is this repository the entire system or only one part of a larger platform?
> 2. Who are the main user roles that should appear in the context diagram?
> 3. Should managed AWS services like SQS and S3 appear inside the system boundary, or would you prefer them shown as external supporting services?
> 4. Which container would you like me to break down at the Component level?

### Example follow-up behavior

If the user does not answer every question, continue with a best-effort draft and clearly note the assumptions.

---

## Recommended default deliverables

Unless the user asks otherwise, the skill should try to return:

* one concise System Context view
* one concise Container view
* one Component view for the most central container
* one short narrative explaining assumptions and open questions

If the system is large, propose documenting it incrementally rather than forcing everything into one response.

---

## Optional output formats

When asked, the skill may emit diagrams as:

* Mermaid
* PlantUML with C4 extensions
* Structurizr DSL
* plain Markdown with structured sections

If the user has no preference, default to Markdown narrative plus Mermaid.

---

## Final instruction to the agent

Inspect the codebase carefully, infer architecture conservatively, and use targeted questions to resolve what code cannot tell you. Produce C4 documentation that is precise, readable, and honest about uncertainty.
