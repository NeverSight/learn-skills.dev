---
name: qa-data-seeder
description: Prepare and seed test data for a feature into a target environment. Analyzes the feature's implementation, proposes data categories covering regular and edge cases, and populates the environment via existing seed mechanisms code access, REST, MCP. Use when the user asks to seed test data, populate a test or staging environment, prepare data for manual/QA testing of a feature, generate a dataset for a feature, or create fixtures in an environment.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# QA Data Seeder

Analyze how a feature is implemented, design a balanced dataset that covers every category QA needs, and populate it into a target environment so the feature can be tested manually or by automation.

## Critical Constraints

- **Never seed production.** Confirm the target environment is a test/dev/staging one before writing any data. If in doubt, stop and ask.
- **Never produce broken data.** Every seeded record must pass the application's own validation. Edge cases are extreme-but-valid values, not corrupt ones. Malformed input belongs in negative tests executed live, never in persisted seed data.
- **Balance the dataset: at least 70% regular (expected) data, at most 30% edge cases.**
- **Do not seed until the user approves the categories and the exact item count** (Step 3 gate).
- Credentials, tokens, and connection strings come from env vars or user input — never hardcode them.
- Prefer the project's existing seeding mechanisms (factories, seed scripts, fixtures, admin console) or REST API or MCP. Write seed script in language of application.
- Generated artifacts (dataset plans, one-off seed scripts) go into the gitignored `.testeiya/seed-data/` — add `.testeiya/` to `.gitignore` if missing.
- Mark every seeded record with one recognizable marker (in a name, note, or tag field the schema allows) so QA can find the data and clean it up later. Use the same marker for the whole run.

## Workflow

### Step 1: Understand the feature

Read the implementation before proposing anything. Collect:

- Entities and models the feature touches, with every field: type, format, length limits, numeric ranges, enums, required vs optional, uniqueness, defaults.
- Validation rules — application-level and DB constraints/migrations.
- Relationships and prerequisites: which records must exist before others can be created.
- Business variations that change behavior: roles, statuses, types, plans/tiers, locales, feature flags, time-dependent logic.
- API endpoints (or UI flows) that create these records, and what they require.

If there is no code access, fall back to the API schema (OpenAPI/Swagger, GraphQL introspection) or ask the user for docs. If MCP available - use it.

### Step 2: Collect environment details

❓ Ask for what the code cannot tell you:

- Platform: web, mobile, or API-only. 
- Base URL if web; API base URL for seeding.
- Environment kind (local, dev, staging) — confirm it is not production.
- Access channel available: existing seed mechanism, REST API, DB/console access.
- How to authenticate: which env vars hold tokens or credentials.
- Which account/tenant/workspace to seed into, or whether to create a fresh one.

Pick the seeding channel in this order: existing seed mechanism → app console/code → new small script -> REST API -> MCP .
For local environments data can be seeded through the backend.


### Step 3: Propose categories and ask for the count

- Derive categories from Step 1: one per business variation, plus edge-case groups (min/max lengths and amounts, unicode, date boundaries, every enum value and reachable state, empty vs full optional fields, collection and relationship extremes).
- Present a table: category, what it lets QA test, regular/edge, planned share.
- Keep regular categories at 70% or more of the total; edge categories at 30% or less.
- ❓ Ask the user for the exact total number of items, then recompute per-category counts and confirm.
- Adjust categories per user feedback before generating anything.

### Step 4: Generate the dataset

- Use realistic values: names, emails, addresses, and amounts that look like production data; unique where the schema requires it.
- Use faker/lorem ipsum generators when available
- Order records so prerequisites come first (parents before children, referenced records before referencing ones).
- Apply the run marker to every record.
- Save the dataset (records or generation rules) to `.testeiya/seed-data/` before seeding, so the run is reviewable and repeatable.

### Step 5: Seed the environment

- Seed through the chosen channel in dependency order; batch where the channel allows.
- Verify each batch as it is written: API response codes, returned IDs, record counts.
- If the application rejects a record, fix the generator to comply — never bypass validation by writing directly to the DB.
- After 3 failed attempts on a category, report the failure with the error output and ask how to proceed.

### Step 6: Verify and hand off

- Re-query the environment per category and compare counts against the approved plan.
- Report a table: category, requested, created, and how to locate the records (the marker).
- Include the environment URL and, for web, a page where QA can see the seeded data.
- Give cleanup instructions: how to find records by the marker and delete them through the same channel.
- Offer follow-ups: `qa-write-test-cases` to write cases against the seeded data, or `qa-thinking` to probe the feature for scenarios the dataset should grow to cover.
