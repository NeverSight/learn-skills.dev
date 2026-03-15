---
name: structure-map
description: Scan project and generate STRUCTURE.md hub + detail files (screens, API routes, DB tables). Works with any tech stack. Also updates instruction files for multi-tool AI support.
---

You are a project structure documentation generator. Your job is to scan the current project and create a comprehensive `STRUCTURE.md` hub file + detail files that help AI coding assistants navigate the codebase without scanning everything.

## Step 0: Diff-aware Update

If `STRUCTURE.md` already exists and the user did NOT say "regenerate":
1. Read the existing `STRUCTURE.md` and detail files
2. List all project files and compare against what's documented
3. Identify changes: **added** files, **deleted** files, **renamed** files
4. Determine which feature domains are affected by the changes
5. Update ONLY the affected domains and their detail file entries
6. Recalculate and update header counts (screens, routes, tables, services)
7. Preserve any manual edits the user made to unaffected sections

If the user says "regenerate", delete existing structure files and recreate everything from scratch.

If `STRUCTURE.md` does not exist, proceed with a full generation (skip to Step 0.5).

## Step 0.5: .gitignore-aware Scanning

Before scanning any files, set up path exclusions:

1. Read `.gitignore` if it exists and parse all ignore patterns
2. Always exclude these directories regardless of `.gitignore`:
   - `node_modules/`, `.dart_tool/`, `__pycache__/`, `.next/`, `.nuxt/`
   - `build/`, `dist/`, `.build/`, `out/`, `.output/`
   - `.cache/`, `coverage/`, `.nyc_output/`
   - `vendor/`, `third_party/`, `deps/`
   - `.git/`, `.svn/`
   - `.claude/`, `.cursor/`, `.agent/`
3. Skip binary files, lock files (`*.lock`, `package-lock.json`), and generated code directories
4. Apply these exclusions to ALL subsequent scanning steps

## Step 1: Detect Tech Stack

Scan the project root to identify:

### Monorepo Detection

First, check if the project is a monorepo:
- Multiple `package.json` / `pubspec.yaml` / `go.mod` / `Cargo.toml` files at different levels
- Workspace config files: `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`
- Common monorepo directories: `apps/`, `packages/`, `services/`, `modules/`, `libs/`

If monorepo detected:
- Identify each sub-project and its root directory
- Detect tech stack per sub-project independently
- Each sub-project becomes its own feature domain (or set of domains)
- In STRUCTURE.md, show each sub-project as a top-level section

### Tech Stack Detection

**Frontend framework** (check in order):
- Flutter — `pubspec.yaml` contains `flutter`
- Next.js — `package.json` contains `next`
- React — `package.json` contains `react` (without next)
- Vue — `package.json` contains `vue`
- Angular — `package.json` contains `@angular/core`
- Svelte — `package.json` contains `svelte`
- None detected

**Backend framework** (check in order):
- Flask — Python files importing `flask`
- Django — `manage.py` exists
- FastAPI — Python files importing `fastapi`
- Express — `package.json` contains `express`
- Rails — `Gemfile` contains `rails`
- Go — `go.mod` exists
- None detected

**Database** (check in order):
- PostgreSQL — `psycopg`, `pg`, `postgres` in config/dependencies
- MySQL — `mysql` in dependencies
- SQLite — `sqlite` in dependencies or `.sqlite` files
- MongoDB — `mongo` in dependencies
- Prisma/Drizzle/other ORM — check schema files
- None detected

**Language**: Infer primary language from file extensions (`.dart`, `.ts`, `.tsx`, `.py`, `.rb`, `.go`, `.java`, `.rs`)

## Step 2: Scan Screens/Pages

Search for UI screen/page files based on detected framework:

| Framework | Search Patterns |
|---|---|
| Flutter | `lib/screens/**/*.dart`, `lib/pages/**/*.dart`, `lib/views/**/*.dart` |
| React/Next | `src/pages/**/*.{tsx,jsx}`, `app/**/*.{tsx,jsx}`, `src/screens/**/*.{tsx,jsx}`, `src/components/**/*.{tsx,jsx}` |
| Vue | `src/views/**/*.vue`, `src/pages/**/*.vue`, `pages/**/*.vue` |
| Angular | `src/app/**/*.component.ts` |
| Svelte | `src/routes/**/*.svelte`, `src/lib/**/*.svelte` |

For each screen/page found, record:
- File path (relative)
- Screen/component name
- Brief purpose (infer from filename, class name, or first widget/component)

## Step 3: Scan API Routes

Search for API route definitions based on detected backend:

| Framework | Pattern to Search |
|---|---|
| Flask | `@app.route`, `@app.get`, `@app.post`, `@app.put`, `@app.delete`, `@bp.route` |
| Django | `path(`, `url(`, `urlpatterns` |
| FastAPI | `@app.get`, `@app.post`, `@router.get`, `@router.post` |
| Express | `router.get`, `router.post`, `app.get`, `app.post` |
| Rails | `resources :`, `get '`, `post '` in `routes.rb` |
| Go | `http.HandleFunc`, `r.GET`, `r.POST`, `e.GET`, `e.POST` |

For each route, record:
- HTTP method + path
- Handler function name
- Source file
- Brief purpose

## Step 4: Scan DB Tables/Models

Search for database schema definitions:

1. **Migration files**: `migrations/`, `db/migrate/`, `alembic/`, `prisma/schema.prisma`, `drizzle/`
2. **ORM models**: `models/`, `models.py`, files with `class.*Model`, `class.*Entity`
3. **Schema files**: `*.schema.json`, `db_schema*.json`, `schema.sql`
4. **Raw SQL**: `CREATE TABLE` statements

For each table/model, record:
- Table/model name
- Key columns (PKs, FKs, important fields)
- Source file (migration or model)

## Step 5: Scan Services & Utilities

Look for service/utility layers:
- `services/`, `utils/`, `helpers/`, `lib/`, `src/lib/`
- Middleware files
- Configuration files

Record each service file with its purpose.

## Step 6: Scan Tests

Look for test files:
- `test/`, `tests/`, `__tests__/`, `spec/`, `*_test.*`, `*.test.*`, `*.spec.*`

Group tests by feature domain.

## Step 7: Build Feature Domains

Group related screens, API routes, tables, and services into logical feature domains. A domain groups things that work together (e.g., "Authentication" domain includes login screen + auth API routes + users table + auth service).

Use naming patterns, import relationships, and file proximity to group items.

### Dependency Graph (Import Analysis)

Parse import/require statements across the codebase to strengthen domain grouping:

1. For each screen file, identify which services it imports
2. For each service file, identify which other services it uses
3. Use import clusters to validate and refine domain groupings — files that import each other heavily likely belong to the same domain
4. Detect **circular dependencies** — if Service A imports Service B and Service B imports Service A, flag this in the output
5. Optionally include a "Key Dependencies" section per domain in STRUCTURE.md showing the most important cross-file relationships:

```
### Key Dependencies
- `frmislemler.dart` → `api_client.dart`, `session_context.dart`
- `islemler_rules.py` → `islemler_normalize.py`
```

## Step 7.5: Extract Navigation Flow

Analyze router/navigator files to extract the app's navigation structure:

| Framework | What to Parse |
|---|---|
| Flutter | `MaterialApp` routes map, `GoRouter` config, `Navigator.push` / `Navigator.pushNamed` calls, `onGenerateRoute` |
| React/Next | `react-router` `<Route>` config, Next.js file-based `app/` or `pages/` directory structure |
| Vue | `vue-router` config (typically `router/index.ts` or `router/index.js`) |
| Angular | `app-routing.module.ts`, lazy-loaded route modules |
| Svelte | SvelteKit file-based `src/routes/` directory structure |

Generate an ASCII tree showing the navigation flow:

```
Login Screen
  └─→ Main Screen (after auth)
        ├─→ Screen A (from menu)
        ├─→ Screen B (from menu)
        │     └─→ Screen B Detail (on row tap)
        └─→ Settings
```

Include this in the "Navigation Flow" section of STRUCTURE.md. If navigation cannot be reliably determined, note it as "Navigation flow could not be auto-detected — add manually."

## Step 8: Generate Output Files

Create `docs/structure/` directory if it doesn't exist.

### 8a: `docs/structure/screens.md`

Only create if screens/pages were found.

```markdown
# Screens / Pages

> Total: {N} screens

## {Domain 1}
| File | Name | Purpose |
|---|---|---|
| `path/to/file.ext` | ScreenName | Brief description |
...

## {Domain 2}
...
```

### 8b: `docs/structure/api-routes.md`

Only create if API routes were found.

```markdown
# API Routes

> Total: {N} routes

## {Domain 1}
| Method | Path | Handler | File | Purpose |
|---|---|---|---|---|
| GET | `/path` | handler_name | `file.ext` | Brief description |
...
```

### 8c: `docs/structure/db-tables.md`

Only create if tables/models were found.

```markdown
# Database Tables / Models

> Total: {N} tables

## {Domain 1}
| Table/Model | Key Columns | Source |
|---|---|---|
| `TableName` | `id`, `name`, `fk_id` | `migration_file.sql` |
...
```

### 8d: `STRUCTURE.md` (Hub File)

```markdown
# {Project Name} Project Structure

> {N} screens | {N} API routes | {N} DB tables | {N} services
> {Tech stack summary, e.g. "Flutter frontend + Flask REST API + PostgreSQL"}

## Quick Lookup

| Feature | Screen/Page | API | Table/Model |
|---|---|---|---|
| {most common feature} | `file` | `/path` | `Table` |
... (top 10-15 most important features)

## Feature Domains

### 1. {Domain Name}
- **Screens**: `file1`, `file2`
- **API**: `/route1`, `/route2`
- **Tables**: `Table1`, `Table2`
- **Services**: `service1`
- **Tests**: `test_file1`, `test_file2`
- **Key Dependencies**: `file1` → `service1` → `Table1`

### 2. {Domain Name}
...

## Navigation Flow

```
Entry Point -> Main Screen
  Action1 -> Screen A
  Action2 -> Screen B
```

## Backend Services

| File | Purpose |
|---|---|
| `service_file` | Description |
...

## Frontend Services

| File | Purpose |
|---|---|
| `service_file` | Description |
...

## Detail Files

- All screens: `docs/structure/screens.md`
- All API routes: `docs/structure/api-routes.md`
- All DB tables: `docs/structure/db-tables.md`

## Maintenance

When screens, routes, or tables are added/removed/renamed:
1. Update this file and the relevant detail file
2. Update header counts
```

## Step 9: Update AI Instruction Files

Check for each instruction file and add a "Project Map" reference if not already present. **Be idempotent** — if the file already contains `STRUCTURE.md`, do NOT add a duplicate reference.

### CLAUDE.md
If `CLAUDE.md` exists at the project root AND does not already mention `STRUCTURE.md`:
Add this section (place it near the top, after any existing "## Project Overview" section):

```markdown
## Project Map (READ FIRST)
Before scanning the codebase, consult `STRUCTURE.md` for a complete map of every screen, API route, and DB table grouped by feature domain.
When user mentions a screen/feature name, look it up in STRUCTURE.md first.
Detail files: `docs/structure/screens.md`, `docs/structure/api-routes.md`, `docs/structure/db-tables.md`.
When adding/removing/renaming screens, routes, or tables, update STRUCTURE.md and the relevant detail file.
```

### AGENTS.md
If `AGENTS.md` exists AND does not already mention `STRUCTURE.md`:
Add this line in an appropriate section:

```markdown
- **Project Map**: See `STRUCTURE.md` for a complete map of screens, API routes, and DB tables. Consult it before scanning the codebase. When adding/removing/renaming screens, routes, or tables, update STRUCTURE.md.
```

### .cursorrules
If `.cursorrules` exists AND does not already mention `STRUCTURE.md`:
Add this section:

```markdown
## Project Map
Before scanning the codebase, consult `STRUCTURE.md` for a complete map of every screen, API route, and DB table grouped by feature domain.
When user mentions a screen/feature name, look it up in STRUCTURE.md first.
```

### .cursor/rules/structure.mdc
If `.cursor/rules/` directory exists AND `structure.mdc` does not already exist:
Create the file:

```markdown
---
description: Project structure map for codebase navigation
globs:
alwaysApply: true
---

Before scanning the codebase, consult `STRUCTURE.md` for a complete map of every screen, API route, and DB table grouped by feature domain.
When user mentions a screen/feature name, look it up in STRUCTURE.md first.
Detail files: `docs/structure/screens.md`, `docs/structure/api-routes.md`, `docs/structure/db-tables.md`.
When adding/removing/renaming screens, routes, or tables, update STRUCTURE.md and the relevant detail file.
```

### .agent/skills/structure-map/SKILL.md (Antigravity)
If `.agent/` directory exists at the project root, create `.agent/skills/structure-map/SKILL.md` with a copy of this skill adapted for Antigravity's format.

## Step 10: Report Summary

After completing all steps, show the user a summary:

```
## Structure Map Generated

**Tech Stack**: {detected stack}
**Counts**: {N} screens | {N} API routes | {N} DB tables | {N} services

### Files Created/Updated:
- STRUCTURE.md (hub)
- docs/structure/screens.md ({N} screens)
- docs/structure/api-routes.md ({N} routes)
- docs/structure/db-tables.md ({N} tables)

### Instruction Files Updated:
- CLAUDE.md — added Project Map reference
- AGENTS.md — added Project Map reference
- .cursorrules — not found, skipped
- .cursor/rules/ — not found, skipped

Run `$structure-map` again anytime to refresh.
```

## Important Rules

1. **Do NOT hallucinate** — only include files, routes, and tables that actually exist in the codebase
2. **Be thorough** — search extensively to find all relevant files
3. **Be idempotent** — running the skill twice should produce the same result, not duplicate content
4. **Adapt to the stack** — the output format should match what the project actually uses (don't show "DB tables" section if there's no database)
5. **Keep it concise** — STRUCTURE.md hub should be under 200 lines; details go in the detail files
6. **Use relative paths** — all file paths in the output should be relative to the project root
7. **Group intelligently** — feature domains should reflect how developers think about the project, not just alphabetical file listings
8. **Respect .gitignore** — never index files or directories that are git-ignored or in the default exclusion list
9. **Incremental by default** — prefer updating only changed sections over full regeneration
10. **Flag issues** — report circular dependencies, orphan files (no imports/not imported), and other structural concerns
