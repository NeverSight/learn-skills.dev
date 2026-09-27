---
name: write-adr
description: Use when the user wants to write ADRs (Architecture Decision Records), document technical decisions about system design, data models, API contracts, diagrams, or testing strategy, or plan implementation architecture from a PRD or feature brief.
---

This skill creates one or more ADR documents that — together with the PRD — give an AI development agent everything it needs to implement the feature or application without ambiguity. All technical decisions, reasoning, diagrams, data structures, and test plans are defined here so the implementing agent does not have to make architectural guesses.

Technical implementation details and testing strategy intentionally excluded from PRD belong here.

---

## Process

### Step 1 — Read the PRD (if it exists)
Check for `docs/PRD.md`. If found, read it fully before proceeding. If not found, ask the user to provide a description of the feature or application: what it does, who uses it, what the main flows are.

### Step 2 — Ask clarifying questions (REQUIRED — minimum 5)
Ask the user at least five focused clarifying questions before writing any ADR. Do not start writing until you have answers. If the PRD, user, or codebase already answers a topic, ask a deeper question about another decision instead of repeating it. Relevant topics include:

- Which frameworks, languages, and runtime environments are being used or preferred?
- Are there specific libraries or tools already decided? If their Context7 IDs are known, record them for Step 3.
- What are the deployment constraints — local dev only, Docker, cloud, serverless?
- What is the persistence strategy — which database/storage, why?
- Are there external APIs or services being integrated? What are their constraints?
- What are the performance or scale expectations for this PoC/MVP?
- Are there security requirements (auth, secrets management, data privacy)?
- Any testing requirements — unit only, integration, e2e? TDD approach expected?
- Are there any existing architectural patterns in the codebase that must be followed?

Resolve decisions that affect the architecture before writing. Record any remaining assumptions or open questions instead of inventing answers.

### Step 3 — Check current technology documentation
For libraries, frameworks, and SDKs that affect a decision, prefer the Context7 CLI (`ctx7` or `npx ctx7@latest`). Use a verified Context7 ID already supplied in the PRD or brief directly with `docs <libraryId> "<question>"`; otherwise resolve it with `library <name> "<question>"` first. If the CLI is unavailable, use configured Context7 MCP; if neither is available, use official documentation. Follow an installed Context7 skill for setup details.

Store every verified Context7 ID used in the ADR's **Technology Documentation References** table so implementing agents can fetch current docs directly without resolving the library again. Where no Context7 ID is available, record the official documentation link instead. Do not invent IDs.

### Step 4 — Determine ADR structure
Choose based on complexity:

**Simple** (use a single file):
- Single technical layer, or straightforward feature addition
- Fewer than 3 distinct integrated components
- Save as: `docs/ADR/000-[short-description].md`

**Complex** (use a folder with multiple files):
- Multiple distinct technical layers (e.g., frontend + backend + database + AI/LLM)
- Multiple integration points or external services
- Large scope requiring per-area ownership
- Save as:
  - `docs/ADR/000-main-architecture.md` — overall system, component map, main decisions
  - `docs/ADR/001-[area].md`, `002-[area].md`, etc. — one file per technical area

File naming: use zero-padded numbers + short kebab-case description. Do NOT include "ADR" in the filename — the folder provides that context.
Examples: `000-main-architecture.md`, `001-backend-api.md`, `002-frontend.md`, `003-database.md`

### Step 5 — Write the ADR(s)
Use the templates below. Save to `docs/ADR/`.

---

## Rules

- **Language**: Always write the ADR in English, regardless of the language of the brief or conversation.
- **No code snippets**: Do not include implementation code. The implementing agent can get exact API usage from current documentation. Describe what, not how.
- **No vague statements**: Every constraint, decision, or requirement must be concrete and verifiable — same standard as Acceptance Criteria in the PRD.
- **Diagrams are mandatory**: Include architecture diagrams, data flow diagrams, and sequence diagrams for all flows where applicable. Only skip a diagram type if it genuinely cannot be expressed that way. More detail is better.
- **Testing is mandatory**: Every ADR must include a testing strategy. TDD is the primary self-validation tool for implementing agents.
- **Documentation references**: Record Context7 IDs when available; otherwise record official documentation links. Do not invent IDs.
- **Purpose**: This document, together with the PRD, must give a developer agent a clear picture of the system. Resolve decisions that affect implementation with the user; record lesser open questions explicitly.
- **Do NOT implement the code**: Focus on describing Architecture Decisions (ADRs) to provide all technical details for the agent that will implement the code.

---

## ADR-000 Template — Main Architecture (or Single ADR)

````markdown
# ADR: [Product / Feature Name] — Main Architecture

**Date:** [today]
**Status:** Accepted
**PRD:** [link to docs/PRD.md if exists]

---

## 1. Overview

What is being built. What problem it solves. How this ADR relates to the PRD.

---

## 2. Technology Documentation References

Libraries, frameworks, and SDKs relevant to the decisions below. Record each verified Context7 ID so implementing agents can fetch current docs directly without searching again; use an official documentation link when no ID is available.

| Library | Context7 ID or official docs | Used for |
|---|---|---|
| [Library name] | `/org/repo` | [purpose] |

---

## 3. System Architecture

### Architecture pattern
[e.g., monolith, monorepo, microservices, SPA + REST API, etc.]

### Repository structure
Describe the repo layout: folders, modules, build artifacts, how frontend and backend relate.

### Technology stack
List each layer with the chosen technology and one-sentence justification.

| Layer | Technology | Reason |
|---|---|---|
| Backend | | |
| Frontend | | |
| Database | | |
| AI/LLM | | |
| ... | | |

---

## 4. Module Structure & Dependencies

List all modules/packages/services. For each:
- What it is responsible for
- What it depends on
- What depends on it

Describe the dependency direction explicitly. No circular dependencies.

---

## 5. Data Models

Describe each entity/model conceptually:
- Name and purpose
- Key fields and their types (conceptual, not schema code)
- Relationships to other models
- Persistence (where it is stored, how long)

---

## 6. API / Interface Contracts

For each endpoint or interface boundary:
- Name / path
- Input (fields, types, constraints)
- Output (fields, types)
- Error cases
- Notes (auth required, rate limit, streaming, etc.)

No code. Conceptual contracts only.

---

## 7. Environment Variables

All required environment variables the application needs to run.

| Variable | Purpose | Required | Example value |
|---|---|---|---|
| | | Yes/No | |

---

## 8. Technical Decisions

One record per significant decision. Use the format below.

### [short title]
**Status:** Accepted | Proposed | Superseded
**Date:** [today]
**Context:** Why this decision was needed. What problem or constraint triggered it. (2-3 sentences)
**Decision:** What was decided. Brief reasoning — why this option over others.
**Rejected alternatives:**
- [Alternative A]: [1-2 sentences why rejected]
- [Alternative B]: [1-2 sentences why rejected]
**Consequences:**
- (+) [positive consequence]
- (-) [negative consequence or trade-off]
**Review trigger:** [Specific condition that would require revisiting this decision. E.g., "If concurrent sessions exceed 100/day", "If we add authentication", "If we move to production"]

---

## 9. Diagrams

### 9.1 Architecture / Component Diagram
[Mermaid diagram showing components and their relationships]

```mermaid
...
```

### 9.2 Data Flow Diagram
[Mermaid diagram showing how data moves through the system]

```mermaid
...
```

### 9.3 Sequence Diagrams
One diagram per main flow. Cover: happy path, error path, and any async/streaming flows.

#### [Flow name — e.g., Form submission and AI analysis]
```mermaid
sequenceDiagram
...
```

#### [Flow name — e.g., Session resume]
```mermaid
sequenceDiagram
...
```

---

## 10. Testing Strategy

### Philosophy
Describe the testing approach. TDD is recommended — tests should be written before or alongside implementation and serve as the agent's primary self-validation mechanism.

### Test layers

| Layer | Type | Scope | Tools |
|---|---|---|---|
| Unit | | | |
| Integration | | | |
| E2E | | | |

### Key test scenarios

List the most important scenarios to cover. For each:
- Scenario name
- What is being tested
- Input conditions
- Expected output / behavior
- Edge cases to cover

Include both happy path and failure/edge cases.

### Technical acceptance criteria

Measurable, verifiable criteria that confirm the implementation is correct from a technical standpoint (complement the business ACs in the PRD).

- TAC-01: [concrete, testable statement]
- TAC-02: ...
````

---

## Granular ADR Template (ADR-001+)

Use this for each focused technical area in a complex project.

````markdown
# ADR-[NNN]: [Technical Area Name]

**Date:** [today]
**Status:** Accepted
**Relates to:** `docs/ADR/000-main-architecture.md`

---

## 1. Scope

What technical area this ADR covers. What it does NOT cover (leave to other ADRs).

---

## 2. Technology Documentation References

Libraries specific to this area, with verified Context7 IDs or official documentation links.

| Library | Context7 ID or official docs | Used for |
|---|---|---|

---

## 3. Component Design

Describe the internal design of this area:
- Layers / classes / services and their responsibilities
- Key interfaces and contracts between them
- State management (if any)

---

## 4. Data Structures

Models, DTOs, request/response shapes specific to this area. Conceptual descriptions, no code.

---

## 5. Interface Contracts

Endpoints, events, or method signatures this area exposes or consumes. Input/output/error for each.

---

## 6. Technical Decisions

[Same ADR record format as in the main architecture template]

---

## 7. Diagrams

### Component / Class Diagram
```mermaid
...
```

### Sequence Diagrams
```mermaid
sequenceDiagram
...
```

---

## 8. Testing Strategy

### Test scenarios for this area

| Scenario | Type | Input | Expected output | Edge cases |
|---|---|---|---|---|

### Technical acceptance criteria

- TAC-[NNN]-01: [concrete, testable statement]
````
