---
name: db-schema-design
description: Use this skill when creating, reviewing, or migrating relational database schemas. It applies across projects and ORMs/frameworks such as Symfony Doctrine, Prisma, Drizzle, Rails ActiveRecord, Laravel Eloquent, raw SQL, or any other relational database layer.
---

# DB Schema Design Skill

## Purpose

Create and update database schemas that are maintainable, queryable, performant, understandable by Product Owners, and aligned with the real application domain.

Use this skill before:

- Creating new tables, columns, relationships, indexes, keys, uniqueness rules, enums, JSON fields, arrays, or migrations.
- Updating an existing data model.
- Reviewing a proposed database schema.
- Accepting a user-requested database change that may harm maintainability, data quality, privacy, queryability, or performance.
- Translating a product requirement into persistent data.

The agent acts as an expert database design consultant, not as a passive code generator.

---

## Controversial Recommendations Policy

- Normal database structure is allowed: primary keys, foreign keys, unique constraints, simple `CHECK` constraints, non-null required columns, and selective indexes.
- Simple database validation constraints are allowed for stable data integrity rules, especially in new projects, new modules, or schemas that already use DB-level validation. Be more cautious about introducing the first `CHECK` constraint in an established project.
- Avoid triggers, stored procedures, generated database functions, and database-side business rules for workflow or application process logic.
- Do not recommend composite indexes unless explicitly doing measured query tuning.
- When recommending lookup tables, look at the current usage of those values and consider how likely they are to change in the future. If you do not know, ask the user.
- Do not recommend soft delete, audit expansion, partitioning, materialized views, or type-purity migrations unless driven by a concrete product or operational problem.

---

## Core Principles

## 1. Understand the domain before modelling

Do not jump directly to tables.

Before proposing a schema, understand:

- What real-world/application concepts exist.
- Who owns what.
- What users call those concepts.
- How the data will be created, changed, searched, filtered, displayed, reported, and deleted.
- Whether the requested change is the real need or only one proposed implementation.

Ask a small number of high-value Product Owner questions when needed.

Do not ask a 20-question form.

Good questions are specific, easy to answer, and explain the trade-off.

Bad:

> Should this be normalized?

Good:

> Is a “Sampling Window” a real concept users may edit, report on, or add fields to later? If yes, it should probably be its own table. If it is only display text, a simpler column may be enough.

---

## 2. Model the application domain, not the ORM convenience

Prefer models that match how users and Product Owners think about the application.

If the user thinks there is a concept called `X`, and `X` has properties, lifecycle, permissions, reports, or future fields, strongly consider modelling `X` as its own table.

Adding tables is acceptable. Avoid lazy “one table solves everything” designs.

A good schema should make ordinary future product changes easier, such as:

- Adding a field to an object.
- Adding a new dashboard graph.
- Changing one object into many.
- Reporting by status, type, owner, date, or category.
- Auditing who changed something, if the project needs that.
- Applying permissions to a concept.

---

## 3. Simplicity matters, but not laziness

Prefer the simplest model that still represents the domain honestly.

Do not confuse “fewer tables” with “simpler design”.

Sometimes 3 clear tables are simpler than 1 overloaded table with nullable columns, JSON, arrays, magic types, or XOR relationships.

When there are several reasonable models, compare them using:

- Domain fit.
- Query simplicity.
- Migration risk.
- Future extensibility.
- Application/repository validation clarity.
- Product Owner understandability.
- Performance and indexing.
- Data quality.
- Privacy exposure.

If two models are both valid, explain the trade-off briefly and ask the Product Owner to decide.

If the user delegates the decision to the agent, prefer:

1. Maintainability.
2. Domain clarity.
3. Queryability.
4. Clear application/repository validation rules.
5. Simplicity.
6. Performance.

---

## 3a. Name schema-qualified tables clearly

Schema names may group related tables and reduce repetition, but the table name must still be understandable if moved out of that schema.

Use schema names as context, not as the only source of meaning.

When naming tables:

- Preserve previous developer naming where it is already reasonably explicit.
- Avoid making table names generic or misleading just because the schema provides context.
- Join, assignment, membership, allocation, and link tables should name their role instead of masquerading as entity tables.
- Avoid generic names like `base`, `items`, `slots`, or `actors` when the table is not that entity.

Examples:

- Prefer `experiments.experiments` over `experiments.base`.
- Prefer `experiments.experiment_participants` over `experiments.participants` for experiment-participant assignments.
- Prefer `experiments.experiment_time_slots` over `experiments.time_slots` when the table links experiments to time slots.

---

## 4. Avoid JSON and arrays by default

JSON, JSONB, unstructured blobs, and arrays are forbidden by default for domain data.

They may only be used after explicit justification.

Before accepting JSON or arrays, ask:

> Will we need to filter, search, report, validate, join, audit, permission, migrate, or add fields to this data later?

If yes, use relational tables and columns.

JSON/arrays are acceptable only for cases such as:

- External provider payload snapshots where the application does not query inside them.
- Rare metadata that is genuinely schemaless and not part of core business logic.
- Temporary import/debug fields with a clear lifecycle.
- Append-only technical logs where the DB is not the main analysis layer.
- Database-specific advanced use cases explicitly justified by the team.

If JSON or arrays are used, document:

- Why a relational model was rejected.
- Whether the field is queried.
- Validation rules.
- Migration strategy if the data becomes first-class later.
- Indexing strategy, if any.

---

## 5. Prefer lookup tables over enums for business concepts

Prefer small reference/lookup tables over hardcoded database or ORM enums when:

- Values may be renamed.
- Values may be hidden/deprecated.
- Values need translations.
- Values need ordering.
- Values need permissions.
- Values need third-party mappings.
- Product Owners may add/change them.
- Different projects/customers may have different lists.

Enums are acceptable for stable technical states that rarely change and are not user-managed.

Examples:

- Good enum candidate: migration job status: `pending`, `running`, `failed`, `completed`.
- Better lookup table candidate: experiment phase, metric category, survey item type, cancellation reason.

---

## 6. Keep workflow logic out of the database, but keep integrity in the database

Do not recommend database-level workflow or business-process logic such as triggers, stored procedures, custom database functions, or other database-side logic that tries to run application behavior.

Keep workflow validation and business process rules in the backend/service/repository layer where they are easier to test, version, profile, and reason about with product requirements.

This rule does not ban normal relational integrity constraints:

- Primary keys.
- Foreign keys.
- Simple `CHECK` constraints for stable validity rules.
- Unique constraints.
- Non-null columns where the field is required.
- Indexes selected for real access patterns.

When a domain rule needs validation, prefer:

- Request/schema validation at the application boundary.
- Service-level lifecycle checks.
- Repository-level duplicate checks when needed before writes.
- Unit/integration tests covering invalid inputs and race-sensitive paths.

These integrity constraints are valid because they protect data shape and relational correctness, not because they encode business workflows.

Simple `CHECK` constraints are acceptable when they enforce stable rules that must always hold, especially in new projects, new modules, or schemas that already use DB-level validation. They are also reasonable when expected data volume is moderate and valid data is more important than a small performance cost.

For existing projects, first inspect the schema style before recommending new `CHECK` constraints. If the project already uses similar checks, follow that convention.

If an established project, especially one that is already 2-3 years old, has no prior `CHECK` constraints, explicitly say that adding one would introduce a new database-level validation pattern. Present that as a trade-off, not as an obvious default, and ask for or highlight confirmation unless the user has already approved that direction.

Avoid proposing triggers, stored procedures, generated database functions, or other database-side workflow logic as the safer alternative. If the user explicitly asks for database-side logic, warn about the trade-off and ask for confirmation before implementation.

Examples:

- New project or new module: `CHECK (percentage >= 0 AND percentage <= 100)` is a reasonable recommendation when that range is a stable invariant.
- Established 2-3 year old project with no prior checks: say explicitly that adding `CHECK (credits >= 0)` would introduce the first DB-level validation constraint pattern in this schema, explain the integrity benefit vs convention change, and confirm that direction before treating it as preferred.

---

## 7. Index conservatively for real access patterns

Indexes must be driven by backend API queries, searches, filters, joins, uniqueness rules, reporting needs, and realistic data volumes. Do not recommend an index just because a query has a matching `WHERE` clause.

For every new or changed table, identify:

- Primary key.
- Foreign keys.
- Unique constraints.
- Common `WHERE` filters.
- Common joins.
- Search fields.
- Sorting/pagination fields.
- Dashboard/reporting filters.

Create indexes for:

- Foreign keys by default unless clearly unnecessary.
- High-volume or selective columns frequently used in `WHERE`, after considering expected row counts.
- Search fields such as email, external IDs, slugs, codes, or names where appropriate.
- Unique business identifiers.

Do not index blindly. Each non-unique index has write/storage cost.

Do not recommend composite indexes as schema-review suggestions to the user. In normal schema reviews, bug triage, feature design, or migration advice, the output should never include "add a composite index" as a recommended action.

The only acceptable mentions of multi-column indexes are:

- Composite unique constraints that enforce a business rule, such as one membership per `(project_id, member_id)`.
- Existing composite indexes that are being explained, not recommended.
- Index-specific performance work where the user explicitly asks for query tuning, execution-plan analysis, or index design.

Even in explicit performance work, do not suggest a composite index without measured evidence, expected high cardinality, and an explanation of why existing primary keys, unique constraints, and single-column indexes are insufficient.

Never recommend composite indexes for small bounded child sets, such as users in one workspace, members in one project, rows under one parent, or tables expected to contain only hundreds or low thousands of rows per parent. In those cases, one sensible single-column index, or no extra index beyond existing keys/uniqueness, is usually enough.

When unsure, ask:

> Is this query expected to scan enough rows that the current primary key, unique constraints, or simple single-column indexes will not be enough? If not, avoid adding an index.

---

## 8. Partitioning is not the default performance solution

Never introduce partitioning on your own.

Only consider partitioning when the user explicitly asks for it or when the project already uses it.

Before partitioning, first consider:

- Better indexes.
- Better targeted single-column indexes first; do not propose composite indexes unless the user explicitly requested index tuning.
- Query rewrites.
- Archiving.
- Materialized views/read models.
- Data retention rules.

Partitioning is mainly acceptable when it improves human operation and maintenance, such as:

- Easier archiving.
- Easier deletion by period/tenant.
- Easier backup/restore.
- Very large operational tables with clear lifecycle boundaries.

Do not partition just because a table may become “large”.

If partitioning is required, prefer partition keys that align with maintenance operations and avoid low-cardinality partitioning. Be careful with tenant/status partitions unless there is a clear operational reason.

---

## Optional Recommendation: Store Only What the Application Needs

This is a useful recommendation, not an absolute rule.

Consider avoiding standard personal fields by default, especially when they are not clearly needed:

- first name
- last name
- date of birth
- gender
- phone
- address
- email
- profile image

Ask purpose-based questions instead.

Bad:

> Do we need date of birth?

Good:

> Do we need the user’s birthday because the app sends age-based content, birthday messages, legal eligibility checks, or something else?

Bad:

> Should we store first name and last name?

Good:

> How does the app need to address this person in emails and UI? A single `display_name` may be enough.

This recommendation can conflict with simplicity and maintainability. For example, a standard `email` column may be simpler and more maintainable if the whole project expects users to have emails.

Use judgement. Do not over-engineer privacy-driven modelling if it makes the model confusing or inconsistent with the rest of the app.

---

## Basics Every Schema Must Follow

## Keys and relational integrity

Every table must have:

- A real primary key.
- Non-null key columns.
- Foreign keys for real relationships unless the project has an explicit reason not to enforce them.
- Unique constraints for business rules that must be true.

For new tables, do not treat a unique index as a substitute for table identity. A table should have a primary key, and business uniqueness should be enforced separately with non-null unique constraints.

Default to surrogate primary keys unless the project already has a strong, intentional convention that justifies something else.

Simple database validation constraints are allowed for core data integrity rules that must always hold. Use `CHECK` constraints when the rule is stable and the project/module conventions support it.

In existing projects, inspect whether similar `CHECK` constraints already exist before recommending one. If this would be the first `CHECK` constraint in an established schema, call that out explicitly as a new database-level validation pattern and explain the trade-off.

Do not recommend triggers, stored procedures, or database functions for application/business workflow logic. Put those rules in backend validation and service/repository code instead.

Avoid nullable columns in keys. A nullable value in a key usually weakens the meaning of the key and can behave unexpectedly across databases.

Be cautious about using natural/business columns as primary keys. They can work, but they often make future migrations, deduplication, data cleaning, renaming, imports, and external integrations harder. In most cases, keep them as `UNIQUE NOT NULL` business constraints instead of table identity.

Usually, a project should choose either:

- Bigint-like generated IDs.
- UUID-like generated IDs.
- A clear project-standard ID strategy.

Follow the project convention unless there is a strong reason to challenge it.

## Bigint vs int for normal numeric columns

Do not make `bigint` the default for normal numeric columns in PostgreSQL-like systems.

Use `bigint` when growth estimates justify it, especially for audit, event, log, counter, or other high-volume tables where values may realistically exceed `int` over the system lifetime.

For ordinary bounded application numbers, prefer the smaller appropriate type. Use appropriate types for genuinely small bounded values, such as ratings from 1 to 5 or display order values with clear limits.

## Bigint vs UUID for identifiers

Do not claim that UUIDs are “secure” and bigint IDs are “unsafe”.

Security does not come from whether the URL contains a bigint or a UUID. Security comes from route authorization, role checks, permission checks, tenancy checks, and access control.

Bad reasoning:

> We should use UUIDs because `/profile/user/123` is unsafe but `/profile/user/uuid` is safe.

Correct reasoning:

> Both routes need proper authorization. The ID type does not replace permission checks.

Prefer bigint-like identifiers when:

- Humans need to copy, type, read, or mention the identifier.
- The ID is used in tickets, support, operations, customer service, or communication.
- Short readable references matter, such as task IDs in Taiga/Trello-like apps.

Prefer UUID-like identifiers when:

- IDs are mostly used inside generated links.
- Humans rarely type them manually.
- Distributed generation is useful.
- The project already uses UUIDs consistently.

When asked which UUID version to use, research the current best option for the project’s database, ORM, language, runtime, and indexing behaviour. Do not assume one UUID version is universally best.

## Audit columns

Do not automatically add audit columns.

First inspect the project convention.

If existing tables consistently use audit columns, copy the existing pattern.

If the project has existing tables and does not use audit columns, do not introduce them unless the user agrees.

If this is the first table or there is no clear convention, ask the user which audit fields they want.

Usually prefer a small audit set, often 2–3 fields, not a large default list.

Example compact question:

> Existing tables do not show a clear audit convention. Do you want this new table to track creation/update timestamps, or keep it minimal?

Do not add `created_by`, `updated_by`, soft-delete columns, or lifecycle flags unless the project convention or product need supports them.

## Naming

Use names that fit what users and Product Owners say about the objects.

Prefer domain names over technical names.

Good:

- `experiment_protocol`
- `sampling_window`
- `metric_definition`
- `catalog_category`

Avoid vague names:

- `data`
- `metadata`
- `config`
- `details`
- `payload`
- `item`
- `record`
- `object`
- `mapping`

For many-to-many tables, be explicit about the tables/concepts being linked.

Good:

- `author_publication`
- `user_role`
- `experiment_metric`
- `catalog_item_tag`

Bad:

- `links`
- `relations`
- `mapping`
- `entity_join`

If a new concept exists but the user has not named it, propose one domain-fitting name and briefly explain it.

Example:

> I would call this `sampling_window` because it represents the scheduled day/time instances for data collection, not just a display field on the experiment.

## Ownership tree

Before creating relationships, define the ownership tree.

Ask:

- What is the parent object?
- Can this child exist without the parent?
- Is this relationship one-to-one, one-to-many, or many-to-many?
- Can ownership change?
- Is the relationship historical or current-only?

Prefer one clear path between concepts.

Avoid relationship cycles where the model allows going from object X to object Y through multiple competing routes. Cycles increase ambiguity, bugs, authorization mistakes, and deletion complexity.

## Column types

Use simple, precise types:

- Booleans for real yes/no states.
- Dates for calendar dates.
- Timestamps for moments in time.
- Numeric types for calculations.
- Text for human-entered variable-length content.
- Lookup table foreign keys for business categories.
- Avoid custom exotic types unless project-standard.

## Nullability

Nullable columns are allowed only when absence is meaningful.

For each nullable column, know what `NULL` means:

- Unknown?
- Not applicable?
- Not collected yet?
- Removed/hidden?
- System-created?
- Optional user input?

If several nullable columns express different object types or modes, consider separate tables or a clearer relationship.

## Deletion and hiding

Decide deletion semantics early:

- Hard delete.
- Soft delete.
- Hide from UI.
- Archive.
- Preserve for audit/history.

Do not add `is_hidden`, `is_deleted`, or `deleted_at` casually. They affect uniqueness, indexes, queries, permissions, and reporting.

If hidden rows should not participate in ordering or uniqueness, use explicit partial unique indexes where supported, or model visible/hidden lifecycle clearly.

---

## Handling Controversial Models

A model is controversial when two or more schemas could reasonably solve the problem, or when the proposed design includes:

- JSON/arrays for business data.
- Nullable XOR relationships.
- Polymorphic associations.
- Duplicated columns.
- Multiple paths between the same objects.
- New enum/business states.
- Soft deletion affecting uniqueness.
- Complex display ordering.
- Denormalized read data.
- Partitioning.
- Large migrations.
- Sensitive personal data.
- Missing keys, uniqueness, or relational integrity.
- Tables that do not match Product Owner concepts.

When this happens, do not silently choose.

Return a compact decision note:

```md
## Decision needed: <topic>

I see two reasonable models:

A) <model A>
- Benefit: <main benefit>
- Cost: <main cost>

B) <model B>
- Benefit: <main benefit>
- Cost: <main cost>

Key question:
<one Product Owner question that decides most of the issue>

My recommendation:
<short recommendation and why>
````

Always include this future-change question when it is relevant:

> If the client asks for normal additions later — a new form question, one extra dashboard graph, one object becoming two objects, or a new field on this concept — which model adapts more easily?

---

## When Reviewing an Existing Model

When reviewing an existing schema, be pragmatic.

Do not assume the user wants to migrate the entire database model.

Pick battles.

Focus on the 2–3 highest-impact changes that are worth the migration cost.

Prioritize changes that:

- Avoid serious future modelling pain.
- Fix data correctness problems.
- Remove JSON/array business-data traps.
- Fix missing primary keys, foreign keys, or uniqueness rules that allow duplicate or orphaned data.
- Fix missing indexes that affect real API/query performance.
- Simplify a confusing model that developers already struggle with.
- Prevent privacy/compliance risk from unnecessary data.
- Align the model with the Product Owner’s domain concepts.

Avoid recommending large rewrites for theoretical purity.

When giving feedback, separate:

```md
## High-impact changes worth considering

1. <change>
Why it matters:
Migration cost:
Recommendation:

## Minor issues I would not migrate only for this

- <issue>
```

---

## When the User Requests a Bad Design

If the user asks for something that goes against this skill, warn them once before implementing.

Be concise. Users are busy and may be annoyed.

Use this structure:

```md
This goes against the DB schema skill recommendation.

Main risk:
- <risk 1>
- <risk 2>
- <risk 3>

Safer alternative:
<alternative>

Please confirm if you still want the original approach.
```

Do not lecture. Do not produce long theory. Focus on the one issue that matters most.

If the user confirms, proceed, but document the risk in the migration/schema decision note.

---

## Migration-Specific Rules

Before changing an existing schema, understand why the change is needed.

Never treat a migration as a local isolated patch if it affects the domain model.

Ask:

- What user/product problem caused this migration?
- Is this fixing data quality, adding a feature, improving performance, or working around an old bad model?
- Is the current schema wrong, incomplete, or only inconvenient?
- Will old data need backfill, cleanup, deduplication, or validation?
- Does the change preserve existing app behavior?
- What happens to historical data?

Be suspicious of incremental migrations that:

- Add nullable columns to avoid understanding ownership.
- Add JSON to avoid designing child tables.
- Add arrays to avoid many-to-many tables.
- Add duplicate fields without defining the source of truth.
- Add status columns without lifecycle rules.
- Add indexes without matching real queries.
- Add personal data because it is “standard”.

For each migration, produce:

- Schema change summary.
- Data migration/backfill plan.
- Risk and rollback notes.
- Index/key/uniqueness changes.
- Whether any new `CHECK` constraint follows existing schema style or introduces a new DB-level validation pattern.
- Required Product Owner confirmation, if any.

---

## Data Quality Checklist

Evaluate the design using these data quality attributes:

## Attributes

- Accuracy: Does the data represent the real-world fact correctly?
- Completeness: Can required facts be missing?
- Conformance: Does the data follow expected formats and domain rules?
- Consistency: Can two places disagree about the same fact?
- Timeliness: Is the data updated at the right time?
- Uniqueness: Can duplicate records appear?
- Validity: Are impossible values prevented?

## Actions

Consider data quality across:

- Acquisition/Entry: How does data enter the system?
- Cleaning: How are mistakes corrected?
- Storage: How are keys, uniqueness, and indexes represented?
- Analysis: How will reports, dashboards, and exports use it?

If a schema makes cleaning, deduplication, or reporting hard, flag it.

---

## Required Workflow

## Step 1: Inspect project conventions

Before proposing code:

- Read existing schema/migrations/models.
- Identify naming style.
- Identify ID strategy.
- Identify audit-column convention, if any.
- Identify soft-delete/hide patterns.
- Identify enum vs lookup-table conventions.
- Identify existing index style.
- Identify whether `CHECK` constraints or similar DB-level validation constraints are already part of the schema style.
- Identify ORM/framework limitations.
- Identify database engine and version if available.

Do not assume Symfony, Prisma, Drizzle, or any specific ORM. The design is framework-independent first, implementation-specific second.

## Step 2: Restate the domain problem

Briefly summarize:

- The application concept.
- The user action.
- The data that must persist.
- The expected queries/reports.
- The lifecycle of the data.

If this cannot be summarized confidently, ask Product Owner questions.

## Step 3: Ask minimal Product Owner questions

Ask only questions that change the model.

Prioritize:

1. Ownership/lifecycle.
2. Cardinality.
3. Search/reporting needs.
4. Future changes.
5. Keys and uniqueness.
6. Deletion/history.
7. Privacy/data minimization, only when relevant.

Use at most 3 questions initially unless the task is clearly large.

## Step 4: Propose schema options if needed

If there is one clearly good model, propose it.

If multiple models are reasonable, show options and recommendation.

Do not hide controversial trade-offs.

## Step 5: Design the relational model

For each table include:

- Purpose.
- Columns.
- Primary key.
- Foreign keys.
- `CHECK` constraints for stable integrity rules, when appropriate for the project/module style.
- Required/nullable fields.
- Unique constraints for business uniqueness.
- Application/repository validation rules for business invariants.
- Indexes.
- Audit fields only if project convention or user decision supports them.
- Deletion/hiding behavior.
- Expected queries supported.

## Step 6: Validate against anti-patterns

Before writing final code/migration, explicitly check:

- Is any JSON/array used for business data?
- Is any enum better as a lookup table?
- Are nullable columns hiding multiple concepts?
- Is there an XOR relationship?
- Are there relationship cycles?
- Are keys non-null?
- If a `CHECK` constraint is proposed, does it enforce stable integrity rather than workflow logic?
- If this is an existing project, does the proposed `CHECK` follow existing schema convention, or is it the first one that must be called out as a new pattern?
- Does each table have a real primary key, with business uniqueness represented separately by normal unique constraints?
- Are high-volume or genuinely selective filters indexed without over-indexing small bounded sets?
- Is personal data reasonable for the app?
- Is the schema understandable to the Product Owner?
- Does it match existing project conventions?

## Step 7: Produce implementation

Only after the design is clear, produce implementation for the target project:

- SQL migration.
- Doctrine entities/migrations.
- Prisma schema/migration.
- Drizzle schema/migration.
- Tests.
- Backfill script.
- Query/index verification.

Implementation must follow the chosen project framework, but the design reasoning must remain framework-independent.

## Step 8: Produce final concise report

End with:

```md
## Schema decision summary

Chosen model:
<short>

Why:
<short>

Main trade-off:
<short>

Indexes/keys/uniqueness:
<short>

Questions still open:
<only if any>

Skill deviations:
<none, or list confirmed deviations>
```

---

## Output Style

Be concise.

Assume users are busy.

Do not produce long lectures unless asked.

For Product Owner questions:

- Use plain language.
- Explain why the answer matters.
- Keep the question answerable.
- Avoid database jargon where possible.

For developers:

- Be specific about keys, uniqueness, indexes, migrations, and application/repository validation code.
- Separate “domain decision” from “implementation detail”.
- Do not bury warnings.
