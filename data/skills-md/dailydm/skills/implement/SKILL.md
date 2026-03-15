---
name: implement
description: "Implement: execute a task from a Breakdown"
disable-model-invocation: true
---

# Implement: execute a task from a Breakdown

When the user types `/implement` and references a task file (e.g., `@projects/<domain-name>/<project-name>/tasks/01-add-feature-flag.md`), do the following:

## 1) Understand the task and its context (required)

- Read the task file end-to-end.
- Identify the **goal**, **acceptance criteria**, **key touch points**, and **risks**.
- Read the parent Plan (`plan.md`) and Breakdown (`tasks/*.md` overview file) for broader context.
- Check **Dependencies** — if a blocking task is incomplete, warn the user before proceeding.
- Search the codebase for the **key touch points** to understand existing patterns and conventions.

## 2) Shape Up principles for implementation

Follow the Shape Up "hill climbing" model:

### Uphill (figuring it out)

- Explore unknowns first — if there are risks or unclear patterns, investigate before writing code.
- Find existing examples in the codebase that match the task's patterns.
- Identify the smallest working vertical slice that proves the approach.

### Downhill (making it happen)

- Implement incrementally — small, reviewable commits.
- Follow TDD when the task specifies it: write failing tests first, then implement to pass.
- Don't gold-plate — implement exactly what's in the acceptance criteria, nothing more.

## 3) Implementation workflow

### Step 1: Pre-flight checks

- [ ] Verify dependencies are complete (warn if not)
- [ ] Identify existing patterns to follow
- [ ] List the files that will be created or modified

### Step 2: Write tests first (if TDD task)

For tasks marked "(TDD)":

1. Create the spec file(s) listed in **Key touch points**
2. Write test cases for each acceptance criterion
3. Run tests — they should fail (red)
4. Show the user the failing tests before implementing

### Step 3: Implement the feature

1. Create/modify files listed in **Key touch points**
2. Follow existing codebase conventions (Sorbet types, module structure, naming)
3. Reference the **Implementation notes** and **Risks** sections for guidance
4. Run tests after each significant change

### Step 4: Verify acceptance criteria

Go through each acceptance criterion checkbox:

- [ ] Criterion 1 — explain how it's satisfied
- [ ] Criterion 2 — explain how it's satisfied
- [ ] ...

### Step 5: Final checks

- [ ] All tests pass
- [ ] Code follows existing patterns
- [ ] No TODOs or placeholders left behind

### Step 6: Post-completion tooling (run as needed)

Run the following tools based on which files were changed:

#### Ruby files (`.rb`)

- [ ] `bundle exec rubocop -a <changed files>` — ensure linting passes
- [ ] `bin/tapioca dsl` — regenerate Sorbet RBI files if models/classes were created/modified

#### TypeScript/React files (`.tsx`, `.ts`)

- [ ] `npm run prettier -- --write <changed files>` — format files
- [ ] `npm run tsc` — ensure TypeScript compilation passes

#### GraphQL changes

- [ ] `rake graphql:schema:dump` — regenerate schema if GraphQL types/resolvers changed
- [ ] `npm run codegen` — regenerate client types if `.graphql` files or schema changed

#### Packwerk changes

- [ ] `bin/packwerk update-todo` — update packwerk todo if package boundaries changed

## 4) Output format

Structure your response as:

```
## Task: [Task title]

### Pre-flight
- Dependencies: [status]
- Patterns identified: [list]
- Files to touch: [list]

### Implementation

[Show code changes with explanations]

### Acceptance criteria verification
- [x] Criterion 1 — [how satisfied]
- [x] Criterion 2 — [how satisfied]
...

### Next steps
- [Any follow-up or blocked tasks now unblocked]
```

## 5) Important rules

- **Don't skip tests** — if the task is marked TDD, write tests first.
- **Don't over-engineer** — implement only what's in the acceptance criteria.
- **Don't break existing functionality** — run existing tests if touching shared code.
- **Ask before major decisions** — if you encounter something not covered by the task, ask the user.
- **Update the task file** — after completion, offer to mark acceptance criteria as checked.

## 6) When blocked

If you cannot complete a task because:

- A dependency task is incomplete → list what's missing and which task provides it
- The codebase doesn't match expectations → describe the discrepancy and ask for guidance
- A decision is needed → present options with tradeoffs

Do not guess or make assumptions on architectural decisions not specified in the task.
