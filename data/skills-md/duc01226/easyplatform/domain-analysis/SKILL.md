---
name: domain-analysis
version: 1.0.0
description: '[Architecture] Analyze business domain: bounded contexts, aggregates, entities, ERD, domain events, and cross-context integration. Generate domain model report with user validation.'
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, TaskCreate, AskUserQuestion
---

**MANDATORY IMPORTANT MUST** use `TaskCreate` to break ALL work into small tasks BEFORE starting.
**MANDATORY IMPORTANT MUST** use `AskUserQuestion` at EVERY decision point — validate every bounded context and entity relationship with user.
**MANDATORY IMPORTANT MUST** produce ERD diagram (Mermaid) and domain model report with confidence %.

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

## Quick Summary

**Goal:** Analyze business domain using DDD principles. Identify bounded contexts, aggregates, entities, value objects, domain events, and cross-context relationships. Generate domain model report with ERD diagram.

**Workflow:**

1. **Load Business Context** — Read idea, business evaluation, refined PBI artifacts + domain-entities-reference.md
2. **Identify Bounded Contexts** — Group related concepts, define context boundaries
3. **Model Entities & Aggregates** — Define aggregates, entities, value objects per context
4. **Map Relationships** — Entity relationships, cross-context integration points
5. **Domain Events** — Identify events that cross context boundaries
6. **Generate ERD** — Mermaid ER diagram with all entities and relationships
7. **User Validation** — Present model, ask 5-8 questions, confirm decisions
8. **Domain Entity Change Assessment** — Compare against domain-entities-reference.md, update if needed

**Key Rules:**

- **MANDATORY IMPORTANT MUST** validate every bounded context boundary with user
- **MANDATORY IMPORTANT MUST** include Mermaid ERD diagram in report
- **MANDATORY IMPORTANT MUST** run user validation interview at end (never skip)
- Every entity must belong to exactly one bounded context
- Cross-context communication via domain events only (no direct references)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Step 0: Locate Active Plan & Domain Reference (MANDATORY)

**MANDATORY IMPORTANT MUST** find and read the current active plan BEFORE starting analysis:

1. **Search for active plan directory** — Glob `plans/*/plan.md` sorted by modification time, or check `TaskList` for plan context
2. **Read `plan.md`** (if exists) — understand project scope, goals, prior decisions
3. **Read all existing research artifacts** — `{plan-dir}/research/*.md` to avoid duplicating work
4. **Read `docs/project-reference/domain-entities-reference.md`** (if exists) — understand current domain entities, their bounded contexts, relationships, and field definitions. This is the project's single source of truth for domain entities.
5. **Set `{plan-dir}` variable** — all outputs write to this directory

If no plan directory exists, create one using the naming convention from session context.

**After completing domain analysis, MUST update `{plan-dir}/plan.md`** with a domain model summary section (bounded contexts, entity count, key relationships, ERD reference).

## Step 1: Load Business Context

Read artifacts from prior workflow steps (search in `plans/` and `team-artifacts/`):

- **Active plan** (`{plan-dir}/plan.md`) — project scope, goals, constraints
- Business evaluation report (value proposition, customer segments)
- Refined PBI (acceptance criteria, user stories, features)
- Discovery interview notes (problem statement, user roles)

Extract and list:

- **Nouns** — Candidate entities (user, order, product, etc.)
- **Verbs** — Candidate domain events (created, approved, assigned, etc.)
- **Roles** — User types with different permissions/views
- **Processes** — Business workflows (application flow, review cycle, etc.)

## Step 2: Identify Bounded Contexts

Group related entities into bounded contexts using DDD principles:

```markdown
### Bounded Context: {Name}

**Purpose:** {What this context owns — one sentence}
**Core domain / Supporting / Generic:** {classification}
**Key Responsibility:** {primary business capability}
**Team ownership:** {suggested team or role}
```

Rules for context boundaries:

- Each context has its own ubiquitous language
- Entities with same name but different meaning = different contexts
- Minimize cross-context dependencies
- Consider team structure (Conway's Law)

**MANDATORY IMPORTANT MUST** present identified contexts to user via `AskUserQuestion`:

- "I identified {N} bounded contexts: {list}. Does this grouping make sense?"
- Options: Agree (Recommended) | Merge {X} and {Y} | Split {Z} | Add missing context

## Step 3: Model Entities & Aggregates

For each bounded context, define:

```markdown
### {Context Name}

**Aggregate Root:** {EntityName}

- **Entities:** {list with descriptions}
- **Value Objects:** {list — immutable, no identity}
- **Invariants:** {business rules this aggregate enforces}

**Other Entities:**

- {Entity} — {purpose, key fields}
```

### Entity Detail Template

| Entity | Type                                   | Key Fields | Relationships | Notes            |
| ------ | -------------------------------------- | ---------- | ------------- | ---------------- |
| {Name} | Aggregate Root / Entity / Value Object | {fields}   | {relations}   | {business rules} |

## Step 4: Map Relationships

### Intra-Context Relationships

```markdown
| From | To        | Type | Cardinality     | Description              |
| ---- | --------- | ---- | --------------- | ------------------------ |
| Job  | Candidate | M:N  | via Application | Candidates apply to jobs |
```

### Cross-Context Integration (Context Map)

```markdown
| Upstream Context | Downstream Context | Pattern | Integration Point          |
| ---------------- | ------------------ | ------- | -------------------------- |
| Recruitment      | Employee           | ACL     | Candidate becomes Employee |
```

Integration patterns to consider:

- **Shared Kernel** — shared model between contexts
- **Customer-Supplier** — upstream publishes, downstream consumes
- **Anti-Corruption Layer (ACL)** — translation between contexts
- **Published Language** — shared API contract
- **Conformist** — downstream conforms to upstream model

## Step 5: Domain Events

Identify events that cross bounded context boundaries:

| Event          | Source Context | Target Context(s)    | Payload            | Trigger        |
| -------------- | -------------- | -------------------- | ------------------ | -------------- |
| CandidateHired | Recruitment    | Employee, Onboarding | candidateId, jobId | Offer accepted |

Rules:

- Events are past-tense (happened already)
- Events carry minimal data (IDs + essential fields)
- Eventual consistency between contexts

## Step 6: Generate ERD

Produce Mermaid ER diagram covering all bounded contexts:

````markdown
```mermaid
erDiagram
    %% Bounded Context: {Name}
    ENTITY_A ||--o{ ENTITY_B : "has many"
    ENTITY_A {
        string id PK
        string name
        datetime createdAt
    }
    ENTITY_B {
        string id PK
        string entityAId FK
        string status
    }
```
````

ERD requirements:

- Group entities by bounded context (use Mermaid comments)
- Show PK/FK fields
- Show cardinality (1:1, 1:N, M:N)
- Include key business fields (not all fields)
- Cross-context references shown as dotted lines or separate diagrams

## Step 7: User Validation Interview

**MANDATORY IMPORTANT MUST** present domain model and ask 5-8 questions via `AskUserQuestion`:

### Required Questions

1. **Context boundaries** — "Are these {N} bounded contexts correct? Any missing or misplaced?"
    - Options: Correct (Recommended) | Need changes | Not sure, explain more
2. **Aggregate roots** — "Is {Entity} the right aggregate root for {Context}?"
3. **Relationship verification** — "The {Entity A} to {Entity B} relationship is {type}. Correct?"
4. **Missing entities** — "Are there business concepts I haven't captured?"
5. **Event verification** — "When {event} happens, should {contexts} be notified?"

### Deep-Dive Questions (pick 2-3 based on complexity)

- "Should {Entity} be a separate aggregate or part of {Aggregate}?"
- "Is {field} really a value object or does it need its own identity?"
- "How does {process} work step-by-step? (verify workflow)"
- "What happens when {edge case}? (verify invariants)"
- "Which entities change most frequently? (performance hints)"

After user confirms, update report with final decisions and mark as `status: confirmed`.

## Step 8: Domain Entity Change Assessment (MANDATORY)

**MANDATORY IMPORTANT MUST** compare domain analysis results against `docs/project-reference/domain-entities-reference.md` (if exists):

1. **Identify new entities** — entities in analysis that don't exist in reference doc
2. **Identify modified entities** — entities with changed fields, relationships, or bounded context assignment
3. **Identify deprecated entities** — entities in reference doc no longer needed by the feature
4. **Present changes to user** via `AskUserQuestion`:
    - "Domain entity changes detected: {N} new, {N} modified, {N} deprecated. Proceed with updating domain-entities-reference.md?"
    - Options: Approve all (Recommended) | Review each change | Skip update

If `docs/project-reference/domain-entities-reference.md` does NOT exist, ask user:

- "No domain-entities-reference.md found. Create it with all entities from this analysis?"
- Options: Yes, create it (Recommended) | No, skip

**After user confirms**, update (or create) `docs/project-reference/domain-entities-reference.md` with the new/modified entities following the existing format in the file. Append new entities to the appropriate bounded context section. Update field lists and relationships for modified entities.

## Step 9: Update Main Plan (MANDATORY)

**MANDATORY IMPORTANT MUST** read `{plan-dir}/plan.md` and append/update a `## Domain Model` section:

```markdown
## Domain Model

- **Bounded Contexts:** {N} — {list names}
- **Total Entities:** {N} ({N} aggregates, {N} entities, {N} value objects)
- **Domain Events:** {N} cross-context events
- **Key Relationships:** {summary of critical relationships}
- **ERD:** See `phase-01-domain-model.md`
- **Full Analysis:** See `research/domain-analysis.md`
```

If `plan.md` already has a Domain Model section, **update it** (use Edit tool). If not, **append it** after the last section.

## Output

```
{plan-dir}/research/domain-analysis.md          # Full domain analysis report
{plan-dir}/phase-01-domain-model.md             # Confirmed domain model with ERD
{plan-dir}/plan.md                              # Updated with domain model summary
docs/project-reference/domain-entities-reference.md  # Updated/created with new/modified entities
```

Report structure:

1. Executive summary (bounded contexts + entity count)
2. Bounded context map with responsibilities
3. Per-context entity/aggregate detail
4. Relationship tables (intra + cross-context)
5. Domain events catalog
6. Mermaid ERD diagram
7. Unresolved questions

Report must be **<=200 lines**. Use tables over prose.

---

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate EVERY bounded context and key relationship with user via `AskUserQuestion`.
**MANDATORY IMPORTANT MUST** include Mermaid ERD and confidence % for all architectural decisions.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/tech-stack-research (Recommended)"** — Research tech stack based on domain model
- **"/plan"** — If tech stack already decided
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
