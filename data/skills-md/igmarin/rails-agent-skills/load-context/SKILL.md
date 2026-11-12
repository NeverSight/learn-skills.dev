---
name: load-context
type: atomic
license: MIT
description: >
  Use before writing code, specs, or a PRD in an existing Rails app.
  Load schema, routes, and one neighbor per layer. Trigger words: load context,
  before I code, existing patterns.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Load Context


## HARD-GATE

```text
DO NOT propose code, specs, PRDs, or task lists until the Context Summary is posted.
DO NOT silently resolve ambiguity — if requirements conflict or specs and code disagree, post a Confusion Block first.
DO NOT load the entire repo — use targeted reads (schema, routes, one neighbor of each kind).
ALWAYS cite the files you read (path:line where possible) so the user can verify.
ALWAYS re-check context when the user's request changes scope mid-conversation.
```

## Core Process

Load minimum context before any code, spec, or PRD in an existing Rails codebase. A fifteen-second read of `db/schema.rb`, `config/routes.rb`, and one neighbor saves a full retry.

### Automatic Context (Optional)

If `rails-ai-bridge` is running, call the `get_project_context` tool to retrieve unified project context (structure, routes, models, schema, dependencies). When this succeeds, skip manual steps 2 and 3 below and proceed directly to finding neighbor patterns and posting the Context Summary.

### Manual Context Discovery (Fallback)

1. **Scope the change:** In one sentence, name the Rails layer touched (controller, model, service, job, engine, view/Turbo, migration, API, GraphQL).
2. **Load baseline Rails context:** Read at minimum:
   - `db/schema.rb` — tables and columns involved (grep by table name)
   - `config/routes.rb` — routes that border the change
   - `Gemfile.lock` — confirm Rails version + domain gems (sidekiq, pundit, rspec, rails-i18n, graphql, etc.)
   Do not read other files (like `config/application.rb`) as baseline context unless explicitly requested by the task.
3. **Load one neighbor of each kind:** For each Rails layer touched, open the nearest sibling that already solves a similar problem — a comparable controller, service, spec, factory.
   When searching for neighbors, ALWAYS run and cite the exact `grep -r` commands using the pattern: `grep -r "class.*<LayerName>" <directory>`.
   Specifically:
   - Controllers: `grep -r "class.*Controller" app/controllers`
   - Services: `grep -r "class.*Service" app/services`
   - Models: `grep -r "class.*Model" app/models`
   - Jobs: `grep -r "class.*Job" app/jobs`
   Do not use glob patterns or `find` commands to search for classes. Include the exact grep command in the Context Summary.
4. **Detect drift:** If there is an existing spec for the area, compare what it asserts vs what the code currently does. Drift is a red flag — document it.
5. **Post the Context Summary:** Before any proposal, output the template below (see Output Style).
6. **Handle ambiguity:** If steps 2–4 surface a conflict (two patterns used, specs contradict code, missing requirement, unclear boundary), produce a Confusion Block:

```text
### Confusion Block
- Conflict: <what conflicts — e.g., spec asserts X but code does Y>
- Options: <list the options with their tradeoffs>
- Recommendation: <state which option and why, or ask user to choose>
```

Do not pick silently.
7. **Hand off:** With context loaded, proceed to the next skill (`plan-tests`, `apply-stack-conventions`, etc.). The Context Summary travels with the task.

## Output Style

When asked to load project context (or write a plan/recommendation involving context), your output `answer.md` MUST follow the template below exactly. You MUST replicate the template block in its entirety, including the **Resources** section and all three reference links at the end. To avoid ceremony and keep the output concise, weave the motivating principle directly into the introduction rather than using a separate header:

### Context Summary Template

```text
To ensure a rapid setup and avoid retries, we follow the fifteen-second read principle of schema, routes, and one neighbor before proposing any changes.

### Context Summary
**Rails layer:** <controller | model | service | job | engine | view/Turbo | migration | API | GraphQL>
**Files read:**
  - <path>:<line-range> — <one-line finding>
  - <path>:<line-range> — <one-line finding>
  - (repeat for each file)
**Neighbor patterns found:**
  - <layer>: <file path> — <key convention or pattern observed> (found using grep: <exact grep command used>)
  - (repeat per layer)
**Gemfile notes:** Rails <version>; relevant gems: <list>
**Drift detected:** <none | description of spec-vs-code mismatch>
**Ambiguities:** <none | list any unresolved conflicts — triggers a Confusion Block>
**Next step:** <plan-tests | apply-stack-conventions | write migration | etc.>

**Resources:**
Load these files only when their specific content is needed:
  - [EXAMPLES.md](EXAMPLES.md) — Use when you need worked examples showing Context Summary and Confusion Block templates
  - [references/confusion-management.md](references/confusion-management.md) — Use when you encounter ambiguity or conflicting signals between code layers
  - [references/context-sources.md](references/context-sources.md) — Use when you need the comprehensive list of context sources by Rails layer beyond the Quick Reference table
```

## Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Over-grepping | Narrow by directory or class-name prefix. Never read more than one neighbor per layer. |
| Absent schema.rb | Look for `db/structure.sql`. Parse the relevant `CREATE TABLE` block instead. |
| Multiple engines | Scope reads to the specific engine directory; document the boundary in summary. |
| Missing spec | Write "no spec coverage" in summary; treat code as the source of truth. |
| Self-neighbor | Do not use the file being changed; select the nearest independent sibling. |
| Scope changes mid-run | Re-run discovery (steps 1-4) and post an updated Context Summary. |

## Extended Resources (Progressive Disclosure)

Load these files only when their specific content is needed:

- **[EXAMPLES.md](EXAMPLES.md)** — Use when you need worked examples showing Context Summary and Confusion Block templates
- **[references/confusion-management.md](references/confusion-management.md)** — Use when you encounter ambiguity or conflicting signals between code layers
- **[references/context-sources.md](references/context-sources.md)** — Use when you need the comprehensive list of context sources by Rails layer beyond the Quick Reference table
