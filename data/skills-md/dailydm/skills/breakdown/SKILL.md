---
name: breakdown
description: "Breakdown: convert a Plan into executable tasks"
disable-model-invocation: true
---

# Breakdown: convert a Plan into executable tasks

When the user types `/breakdown` and references a Plan doc, do the following:

## 1) Study the Plan and the codebase (required)

- Read the Plan end-to-end.
- Identify the "must ship" scope, milestones, and the critical path.
- Search the repo for the most relevant implementation paths named in the Plan and confirm they exist.
- Prefer tasks that match existing repo patterns (Flipper flags, Sidekiq jobs, Stripe clients, GraphQL view-model discipline, observability conventions).

## 2) Create individual task files

- **Location**: `projects/<domain-name>/<project-name>/tasks/`
- **Domain name**: the product area or team domain (e.g., `payments`, `family-messaging`, `attendance-plus`)
- **Project name**: derive a stable folder slug from the referenced Plan (prefer `projects/<domain-name>/<project-name>/plan.md`).
- **Filename**: `<milestone>-<task>-<short-slug>.md` (e.g., `1-1-spike-payout-composition.md`, `2-1-add-stripe-payout-model.md`, `2-2-add-stripe-payout-item.md`)
- **First line**: `# <milestone>-<task>: <Task title>` (e.g., `# 1-1: Spike payout composition`, `# 2-1: Add Stripe payout model`)
- **Source link**: reference the Plan doc path (and shaping/pitch paths if present in the Plan).

**Numbering convention**:

- Milestone number comes first (1, 2, 3, etc.) — corresponds to milestones in the Plan
- Task number within the milestone comes second (1, 2, 3, etc.)
- Example: Tasks 2-1, 2-2, 2-3 are all part of Milestone 2

## 3) Create breakdown_for_jira.md

After creating the task files, generate a summary file for Jira ticket creation.

- **Location**: `projects/<domain-name>/<project-name>/breakdown_for_jira.md`
- **Purpose**: Provide a structured summary that can be copied into Jira for creating work items

**Contents of the generated file:**

1. **Header**: Link to the full plan on GitHub
2. **Milestones list**: Copy from the plan
3. **Task table**: Summary of all tasks with dependencies and links
4. **Phineas command**: Template for AI-assisted ticket creation

**Template:**

```markdown
## Breakdown for Jira

Reference the full [plan on GitHub](https://github.com/ParentSquare/parent_square/blob/master/projects/<domain>/<project>/plan.md).

### Milestones

- **M1: <name>** — <description>
- **M2: <name>** — <description>
- **M3: <name>** — <description>
- ...

### Tasks

| Task | Milestone | Title        | Blocked By | Link                                                                                                             |
| ---- | --------- | ------------ | ---------- | ---------------------------------------------------------------------------------------------------------------- |
| 1    | M1        | <task title> | —          | [1-1](https://github.com/ParentSquare/parent_square/blob/master/projects/<domain>/<project>/tasks/1-1-<slug>.md) |
| 2    | M1        | <task title> | Task 1     | [1-2](https://github.com/ParentSquare/parent_square/blob/master/projects/<domain>/<project>/tasks/1-2-<slug>.md) |
| 3    | M2        | <task title> | Tasks 1, 2 | [2-1](https://github.com/ParentSquare/parent_square/blob/master/projects/<domain>/<project>/tasks/2-1-<slug>.md) |
| ...  | ...       | ...          | ...        | ...                                                                                                              |

---

### Phineas Command

> Create individual child work items for each task outlined above. Keep them in the epic. For each task:
>
> 1. Use the task title from the "Title" column
> 2. In the description, note which tasks are blockers (from "Blocked By" column)
> 3. In the description, note the milestone this task supports
> 4. In the description, include the GitHub link to the full task breakdown file
```

**Blocked By column guidance:**

- Analyze each task's dependencies based on the Plan and task file headers
- Use "—" for tasks with no blockers (typically Task 1: Add feature flag)
- List blocking tasks as "Task 1", "Tasks 1, 2", etc.
- Consider both explicit dependencies and implicit ones (e.g., GraphQL queries depend on domain queries)

**Link column guidance:**

- Base URL: `https://github.com/ParentSquare/parent_square/blob/master/`
- Append the relative path: `projects/<domain>/<project>/tasks/<filename>.md`
- Link text should be the task number (e.g., `1-1`, `2-1`)

## 4) Populate each task file (no blanks)

Fill every section. If something cannot be inferred, write the smallest explicit note stating what's missing and what decision would unblock it.

### File header (required for each task)

```markdown
# <milestone>-<task>: <Task title>

**Milestone**: <milestone number and name> (e.g., "Milestone 2: Stripe payout sync")
**Dependencies**: <list of previous tasks this depends on, e.g., "1-1, 2-1"> or "None"
**Source**: [Plan](../plan.md)
```

### Task sections

For each task file, include:

- **Goal**: what changes for users/system (1–2 sentences)
- **Acceptance criteria**: 3–6 checkboxes
- **Key touch points**: concrete files/classes/modules likely to change
- **Risks**: the top 1–2 risks and how the task mitigates them
- **Notes**: rollout, data migration/backfill, performance, and failure handling notes as needed

### Migrations: run immediately (required)

**Do not defer migrations.** When a task includes a migration:

1. The migration is part of that task's deliverable — not a separate "run migrations" task
2. Run `bin/rails db:migrate` locally as part of completing the task
3. The task is not complete until the migration has been verified locally
4. Acceptance criteria should include "Migration runs successfully (up and down)"

**Example**: A task titled "Add StripePayout model" includes:
- Creating the migration file
- Creating the model file
- Running `bin/rails db:migrate`
- Verifying rollback with `bin/rails db:rollback`

### Testing: incremental, not a phase (required)

**Do not create a separate "Testing" phase or milestone.** Tests are written with each task:

1. Each task includes its own unit/integration tests as part of the deliverable
2. Acceptance criteria should include "Tests pass (new + existing)"
3. Prefer TDD: write specs first, then implementation
4. A task without tests is incomplete

**Anti-pattern to avoid**:
```
❌ Phase 1: Build features
❌ Phase 2: Write all tests
```

**Correct pattern**:
```
✅ Task 1-1: Add model + migration + model specs
✅ Task 1-2: Add service + service specs
✅ Task 1-3: Add job + job specs
```

### Manual testing (required for each task)

Each task should include concrete manual testing steps. Prioritize in this order:

1. **End-to-end browser testing** (preferred)
   - Exact URL to visit (e.g., `http://localhost:3000/districts/1/reporting`)
   - User actions to perform (clicks, form inputs, etc.)
   - Expected visual/behavioral outcomes
   - Any prerequisite navigation or setup

2. **GraphQL via GraphiQL** (for API-focused tasks)
   - Exact query/mutation to run in GraphiQL (`http://localhost:3000/graphiql`)
   - Sample variables to use
   - Expected response shape
   - How to verify side effects (database changes, jobs enqueued, etc.)

3. **Rails console verification** (for backend services/queries)
   - Exact commands to run in `bin/rails console`
   - How to instantiate and call the service/query
   - Expected return value or state change
   - How to verify database state before/after

4. **Sidekiq job testing** (for background jobs)
   - How to enqueue the job manually
   - How to monitor via Sidekiq web UI (`http://localhost:3000/sidekiq`)
   - Expected job outcome and how to verify

**Test data setup**: For each task, specify:

- **Required data**: What models/records must exist locally (e.g., "District with ID 1, School with ID 1, User with admin role")
- **Seed commands**: If applicable, how to create the data:
  - Factory commands: `FactoryBot.create(:district)` or `FactoryBot.create(:user, :admin, school: school)`
  - Rails console setup: Multi-line scripts to create related records
  - Existing seeds: Reference to `db/seeds.rb` or environment-specific seeds
- **Feature flag setup**: How to enable the flag locally:
  - Rails console: `Flipper.enable(:feature_name)` or `Flipper.enable(:feature_name, District.find(1))`
  - Flipper UI: `http://localhost:3000/admin/flipper`

**Example task with incremental testing**:

````markdown
### Task 2-1: Add StripePayout model and migration

**Title**: Add `StripePayout` model with migration

**Goal**: Store Stripe payout data locally for fast CSV export queries

**Acceptance criteria**:
- [ ] Migration creates `stripe_payouts` table with correct columns
- [ ] Migration runs successfully (up and down)
- [ ] Model has validations and associations
- [ ] Model specs pass
- [ ] Existing tests still pass

**Key touch points**:

- `db/migrate/YYYYMMDDHHMMSS_create_stripe_payouts.rb`
- `app/models/stripe_payout.rb`
- `spec/models/stripe_payout_spec.rb`

**Automated tests** (included in this task):

```ruby
# spec/models/stripe_payout_spec.rb
RSpec.describe StripePayout do
  describe 'validations' do
    it { is_expected.to validate_presence_of(:stripe_payout_id) }
    it { is_expected.to validate_uniqueness_of(:stripe_payout_id) }
  end

  describe 'associations' do
    it { is_expected.to have_many(:payment_intents).dependent(:nullify) }
  end

  describe '#bank_account_display' do
    it 'returns formatted bank info' do
      payout = build(:stripe_payout, bank_name: 'Chase', bank_last4: '1234')
      expect(payout.bank_account_display).to eq('Chase ****1234')
    end
  end
end
```

**Manual testing**:

1. **Run and verify migration**:

   ```bash
   # Run migration
   bin/rails db:migrate

   # Verify table exists
   bin/rails runner "puts StripePayout.table_exists?"
   # Expected: true

   # Verify rollback works
   bin/rails db:rollback
   bin/rails db:migrate
   ```

2. **Rails console verification**:

   ```ruby
   # Create a payout record
   payout = StripePayout.create!(
     stripe_payout_id: 'po_test123',
     arrival_date: Time.current,
     bank_name: 'Chase',
     bank_last4: '1234',
     status: 'paid'
   )

   # Verify display method
   payout.bank_account_display
   # Expected: "Chase ****1234"

   # Verify validation
   StripePayout.create!(stripe_payout_id: 'po_test123') # Should raise uniqueness error
   ```

3. **Run specs**:

   ```bash
   bin/rspec spec/models/stripe_payout_spec.rb
   # Expected: All tests pass
   ```
````

### Cut list (protect the appetite)

List 5–10 explicit cut candidates aligned to the Plan's "out of scope" and "nice-to-haves".

### Dependencies and parallelism

- **Critical path**: 3–6 bullets
- **Can parallelize**: 3–6 bullets

## 5) Ask for confirmation

After writing the task files and breakdown_for_jira.md, ask the user to confirm:

- Ticketing format preference (Jira vs Linear vs GitHub issues) and whether they want an epic + subtasks
- Any exact policy/legal wording required in UI or exports
- Any pilot tenant/role constraints not already locked in the Plan
