---
name: improve-prompt
description: "Improve a rough prompt into a detailed, actionable one using project context. Returns a well-structured prompt with file paths, patterns, and acceptance criteria."
argument-hint: "<rough prompt to improve>"
metadata:
  version: 1.0.0
---

# Improve Prompt

**Raw prompt from user: `$ARGUMENTS`**

You are a prompt improvement assistant. The user has given you a rough, thin, or vague prompt above. Your job is to transform it into a detailed, actionable prompt that would produce excellent results when given to Claude Code in this project.

## Important

- Do NOT execute the task described in the prompt
- Do NOT write code or make changes
- ONLY output an improved version of the prompt

## How to Improve the Prompt

Analyze the raw prompt and enhance it by adding:

1. **Specific file paths** — Identify which files in the codebase are relevant to the request. Use your knowledge of the project structure to reference exact paths (e.g., `app/home/[account]/feature/_lib/server/...`).

2. **Project patterns** — Reference the correct patterns from the codebase rules:
   - Service pattern (private class + factory function) for data access
   - Server Actions with Zod validation and auth checks
   - Server Components with loaders for data fetching
   - `react-hook-form` + Zod + your component library for forms
   - `import 'server-only'` on all server files
   - RLS policies for new tables

3. **Acceptance criteria** — Define what "done" looks like with specific, testable conditions.

4. **Constraints and context** — Add relevant constraints the user likely forgot:
   - Which part of the app this affects
   - Multi-tenant considerations (account_id scoping)
   - Existing related code to build on or integrate with
   - Testing requirements (unit tests, E2E)

5. **Scope boundaries** — Clarify what's in and out of scope to prevent over-engineering.

6. **Suggested skills and agents** — Recommend which `/skills` and agents to use for the task. Common ones:
   - `/create-plan` — for multi-phase features that need planning
   - `/postgres-expert` — for database schemas, migrations, RLS policies
   - `/service-builder` — for data access / business logic services
   - `/server-action-builder` — for server actions with Zod + auth
   - `/react-form-builder` — for forms with react-hook-form + your component library
   - `/code-review` — for post-implementation review
   - `/playwright-e2e` — for E2E test writing
   - `tdd-guide` agent — for unit tests (Vitest)
   - `security-reviewer` agent — for auth, RLS, secrets auditing

## Output Format

Return the improved prompt in a fenced code block so the user can easily copy it:

~~~
```
<improved prompt here>
```
~~~

After the code block, add a brief "Changes made" summary listing what you added and why (2-4 bullet points).

## Example

**Raw prompt:** "add a notes feature"

**Improved prompt:**
```
Add a Notes feature at app/home/[account]/notes/.

Database:
- Create a `notes` table with: id (uuid PK), account_id (FK to accounts), title (text), content (text), created_by (uuid FK to auth.users), timestamps
- Add RLS policies using your RLS helper function for team access
- Create migration via `npx supabase db diff --schema public -f add_notes_table`

Service layer:
- Create app/home/[account]/notes/_lib/server/notes-service.ts
- Use the service pattern (private class + factory function)
- Methods: createNote, getNotesByAccount, updateNote, deleteNote
- Add `import 'server-only'`

Server actions:
- Create app/home/[account]/notes/_lib/server/server-actions.ts
- Use Server Actions with Zod validation + auth checks for create, update, delete
- Schemas in _lib/schema/notes.schema.ts

UI:
- Server component page.tsx with loader for initial data
- Client component for the notes list and create/edit form
- Use your component library (e.g., shadcn/ui) for Card, Button, Dialog
- Use react-hook-form + Zod for form validation

Testing:
- Unit tests for service and actions in __tests__/notes/
- Use Vitest with happy-dom, thenable mock pattern for Supabase

Acceptance criteria:
- [ ] Notes CRUD works for team members
- [ ] RLS prevents cross-account access
- [ ] npm run verify passes (typecheck + lint + test)

Suggested workflow:
1. /create-plan — to generate phases for this feature
2. /postgres-expert — for the notes table schema, RLS policies, migration
3. /service-builder — for the notes service layer
4. /server-action-builder — for CRUD server actions
5. /react-form-builder — for the create/edit note form
6. /code-review — after implementation to verify compliance
```

**Changes made:**
- Added specific file paths following the route structure pattern
- Referenced project patterns (service, Server Actions with Zod + auth, loaders, RLS)
- Added acceptance criteria with testable conditions
- Included multi-tenant considerations (account_id scoping)
- Added suggested skills workflow for implementation order
