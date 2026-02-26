---
name: pocketbase
description: >-
  Skill for operating PocketBase backend via REST API and Go package mode.
  Provides collection CRUD, record CRUD, superuser/user authentication,
  backup & restore, migration file generation (JS and Go), Go hooks,
  custom routes, and design guidance for API rules, relations, and security
  patterns. Use for requests related to PocketBase, pb_migrations,
  collection management, record operations, Go framework embedding, and
  backend design.
license: MIT
metadata:
  version: "1.0.0"
allowed-tools: Read Write Edit Bash Grep Glob
---

# PocketBase Skill

Skill for operating a PocketBase v0.23+ backend via REST API and as a Go package. Uses Python scripts (standard library only) to perform authentication, collection CRUD, record CRUD, backup, migration file generation, and includes design guidance for API rules, relations, and security patterns. Supports Go package mode with Go migrations, hooks, custom routes, and middleware.

## Skill Resources

All resources for this skill are bundled in the skill directory at ``:

- **Scripts**: `scripts/` — Python scripts for API operations
- **References**: `references/` — Detailed docs loaded on demand
- **Assets**: `assets/` — Templates and static files

When you need to look up PocketBase details or find skill-related files, check this directory first — everything you need is already here. There is no need to search the user's home directory or other projects.

## Mode Detection

Determine the project mode:

1. `go.mod` exists and contains `github.com/pocketbase/pocketbase` → **Go package mode**
2. Otherwise → **Standalone mode** (existing workflow)

Go package mode additional references:
- Setup & structure → `Read references/go-framework.md`
- Migrations → `Read references/go-migrations.md`
- Hooks & custom routes → `Read references/go-hooks-routes.md`

Go package mode still uses the same REST API. Python scripts (`pb_collections.py`, etc.) and E2E tests work as-is.

## 0. Design Workflow & Decision Making

**Read `references/gotchas.md` FIRST** before writing any PocketBase code.
Your training data contains outdated v0.22 patterns that will fail on v0.23+.
Check field JSON: ensure properties are **flat** (no `options` wrapper) and collection key is `fields` (not `schema`).

### ⚠️ v0.22 Anti-Patterns — DO NOT USE

**Field properties must be FLAT — `options` wrapper was removed in v0.23+:**

```json
// WRONG (v0.22) — "options" wrapper does not exist in v0.23+
{"name": "status", "type": "select", "options": {"values": ["draft", "published"], "maxSelect": 1}}
{"name": "avatar", "type": "file", "options": {"maxSelect": 1, "maxSize": 5242880}}
{"name": "author", "type": "relation", "options": {"collectionId": "...", "maxSelect": 1}}

// CORRECT (v0.23+) — all properties are top-level (flat)
{"name": "status", "type": "select", "values": ["draft", "published"], "maxSelect": 1}
{"name": "avatar", "type": "file", "maxSelect": 1, "maxSize": 5242880}
{"name": "author", "type": "relation", "collectionId": "...", "maxSelect": 1}
```

Applies to ALL field types: `select` (values, maxSelect), `file` (maxSelect, maxSize, mimeTypes, thumbs), `relation` (collectionId, maxSelect), `text` (min, max, pattern).

**This flat-property rule applies everywhere** — inline JSON in `pb_collections.py create`, `collections.json` files used with `pb_collections.py import`, and Go migration code. If you see `"options": {` in any PocketBase field definition, it is WRONG.

**Collection JSON: use `fields` key, not `schema`:**

```json
// WRONG: {"name": "posts", "type": "base", "schema": [...]}
// CORRECT: {"name": "posts", "type": "base", "fields": [...]}
```

**Migration JS: use typed constructors, not `SchemaField`:**

```js
// WRONG:   collection.schema.addField(new SchemaField({type: "select", options: {values: ["a"]}}))
// CORRECT: collection.fields.add(new SelectField({name: "status", values: ["a"]}))
```

**Pre-Generation Checklist** — verify before writing any PocketBase code:

- [ ] Field properties are **flat** (no `options` wrapper)
- [ ] Collection JSON uses `fields` key (not `schema`)
- [ ] Migrations use typed constructors (`SelectField`, `TextField`, `RelationField`, etc.)
- [ ] Hooks use `e.next()` and `$app.findRecordById()` (not `$app.dao()`)
- [ ] Routes use `{paramName}` syntax (not `:paramName`)
- [ ] `@collection` references in API rules use `?=` (not `=`) — `=` breaks with 2+ rows

**Go package mode additional checks:**
- [ ] Collections created via `pb_collections.py` (not hand-written migration files)
- [ ] Auto-generated migration files in `pb_migrations/` are committed to git
- [ ] `migratecmd.MustRegister()` with `Automigrate: true` (dev) is configured in `main.go`
- [ ] `_ "yourmodule/migrations"` blank import exists in `main.go` (if manual migrations are used)
- [ ] Manual migration files (seed data, data transforms) use `package migrations` + `func init()` + `m.Register()`
- [ ] Rules set with `types.Pointer("rule")` (not direct string assignment — `*string` type)
- [ ] Hooks call `return e.Next()` (omitting causes request hang)

### Bootstrap (First-Time Setup)

When PocketBase is not yet running:

1. **Download** — Get the latest version:
   ```bash
   VERSION=$(curl -s https://api.github.com/repos/pocketbase/pocketbase/releases/latest | python3 -c "import sys,json; print(json.load(sys.stdin)['tag_name'].lstrip('v'))")
   ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
   OS=$(uname -s | tr A-Z a-z)
   curl -sL "https://github.com/pocketbase/pocketbase/releases/download/v${VERSION}/pocketbase_${VERSION}_${OS}_${ARCH}.zip" -o pb.zip && unzip -o pb.zip pocketbase && rm pb.zip
   ```
2. **Create superuser** — `./pocketbase superuser create admin@example.com <password>`
3. **Write `.env`** — Confirm credentials with user, write `.env`, add to `.gitignore`
4. **Start** — `nohup ./pocketbase serve --http=127.0.0.1:8090 > pb.log 2>&1 &`
5. **Verify** — `python scripts/pb_health.py`

### Design Decision Tree

When building a PocketBase application, follow this sequence:

1. **Requirements** — Identify entities, relationships, and access patterns
2. **Collection types** — Choose `base`, `auth`, or `view` for each entity
3. **Fields** — Design fields per collection (`Read references/field-types.md`)
4. **Relations** — Design relations (`Read references/relation-patterns.md`)
5. **API rules** — Set security rules (`Read references/api-rules-guide.md`)
   - **Default to `null` (deny all). Open only what is needed.**
   - `null` = superuser only, `""` = anyone including guests
6. **Create** — Create collections via Python scripts (both modes)
   - Use `pb_collections.py create` or `pb_collections.py import --file collections.json`
   - PocketBase auto-generates migration files (`.js` in standalone, `.go` in Go package mode with `Automigrate: true`)
   - Commit the auto-generated migration files to git
   - **Do NOT hand-write migration files for collection schema creation** — let PocketBase generate them
   - For data transforms, seed data, or raw SQL, see Section 6 (Migrations)
   - Hooks/routes: Standalone uses JSVM (`pb_hooks/*.pb.js`), Go uses Go code — `Read references/go-hooks-routes.md`
7. **Seed data** — Insert sample records for verification
8. **Test** — Use Python E2E tests for all integration testing:
   - Read `references/e2e-testing.md`
   - Use `pb_e2e_helpers` module
   - Test positive AND negative access for each collection's API rules
   - Also use E2E tests for custom routes and hooks (Go or JSVM) — call the HTTP endpoint and verify the response
   - Pure functions (utilities, validation, transformation logic) that do not depend on PocketBase can use standard `go test`
9. **Verify** — Run self-tests (see below)

### Self-Test Verification

After creating or modifying collections:

1. Confirm schema: `pb_collections.py get <name>`
2. CRUD smoke test: create → list → get → update → delete
3. Rule verification: test as non-superuser
   - Use `pb_auth.py --collection users --identity ... --password ...`
   - Verify denied access returns expected behavior
4. **E2E test** — Required when any collection has a non-`null` API rule, or when custom routes/hooks exist:
   - `Read references/e2e-testing.md`
   - Generate a test script (`test_e2e.py`) in the project root using `pb_e2e_helpers` module
   - The test MUST cover:
     - Unauthenticated access is denied (expect 401/403)
     - Authenticated user can perform allowed operations
     - User cannot access another user's resources (cross-user isolation)
     - Spoofing prevention — if `createRule` contains `@request.body.X = @request.auth.id`, verify that setting X to a different user's ID is rejected
     - `cascadeDelete` behavior — deleting a parent removes related child records
     - `null` rule (superuser-only) endpoints return 403 for regular users
     - Custom routes: correct response for valid requests, auth middleware rejects unauthenticated/unauthorized requests
     - Hook side effects: verify the expected DB state or response after the hook fires
   - Run the test and fix any failures before marking the task complete

### Reference Index

| Topic | Reference |
|-------|-----------|
| Gotchas & pitfalls | `Read references/gotchas.md` |
| API rules design | `Read references/api-rules-guide.md` |
| Relation patterns | `Read references/relation-patterns.md` |
| JS SDK (frontend) | `Read references/js-sdk.md` |
| JSVM hooks (server) | `Read references/jsvm-hooks.md` |
| File handling | `Read references/file-handling.md` |
| E2E testing patterns | `Read references/e2e-testing.md` |
| Go framework setup   | `Read references/go-framework.md`    |
| Go migrations        | `Read references/go-migrations.md`   |
| Go hooks & routes    | `Read references/go-hooks-routes.md` |
| Production deployment (Docker, binary, proxy) | `Read references/deployment.md` in the `pb-react-spa` skill |
| React SPA frontend | `pb-react-spa` skill (separate skill) |

## 1. Prerequisites and Configuration

### Getting and Starting PocketBase

If PocketBase is not yet installed, guide the user to download the latest version:

**Check the latest version:**
```bash
curl -s https://api.github.com/repos/pocketbase/pocketbase/releases/latest | python3 -c "import sys,json; print(json.load(sys.stdin)['tag_name'])"
```

**Download URL pattern:**
```
https://github.com/pocketbase/pocketbase/releases/download/v{VERSION}/pocketbase_{VERSION}_{OS}_{ARCH}.zip
```

**Platform asset names:**

| Platform | Asset name |
|----------|------------|
| Linux amd64 | `pocketbase_{VERSION}_linux_amd64.zip` |
| Linux arm64 | `pocketbase_{VERSION}_linux_arm64.zip` |
| macOS amd64 | `pocketbase_{VERSION}_darwin_amd64.zip` |
| macOS arm64 (Apple Silicon) | `pocketbase_{VERSION}_darwin_arm64.zip` |
| Windows amd64 | `pocketbase_{VERSION}_windows_amd64.zip` |

**Download, extract, and start:**
```bash
# Example for Linux amd64 (replace VERSION with the actual version number, e.g. 0.28.0)
VERSION=0.28.0
curl -L -o pocketbase.zip "https://github.com/pocketbase/pocketbase/releases/download/v${VERSION}/pocketbase_${VERSION}_linux_amd64.zip"
unzip pocketbase.zip
./pocketbase serve
```

**Create a superuser:**
```bash
./pocketbase superuser create admin@example.com yourpassword
```

**Starting PocketBase in background (for Claude Code sessions):**

```bash
# Start with nohup (survives shell exit)
nohup ./pocketbase serve --http=127.0.0.1:8090 > pb.log 2>&1 &
echo "PID: $!"

# Check if running
python scripts/pb_health.py

# Stop
kill $(pgrep -f 'pocketbase serve')
```

> **Important:** Do NOT use Bash tool's `&` alone — the process dies when the shell session ends. Always use `nohup`.

> **Agent instruction:** If the user's PocketBase is not running or not installed, always recommend downloading the latest version using the GitHub API one-liner above to determine the current version number.

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PB_URL` | No | `http://127.0.0.1:8090` | PocketBase base URL |
| `PB_SUPERUSER_EMAIL` | Yes* | — | Superuser email address |
| `PB_SUPERUSER_PASSWORD` | Yes* | — | Superuser password |

*Required when performing superuser operations.

If environment variables are not set, the `.env` file will be loaded from the **current working directory**. If not found there, parent directories are searched up to the filesystem root (useful for monorepo setups where scripts may run from a subdirectory).

```env
PB_URL=http://127.0.0.1:8090
PB_SUPERUSER_EMAIL=admin@example.com
PB_SUPERUSER_PASSWORD=your-password
```

**Important:** If environment variables are not set, confirm the values with the user before executing operations. When writing credentials to a `.env` file, ensure that `.env` is included in `.gitignore`.

### `pb_config.py` Exports

All PB scripts share this module. Available exports:

| Export | Type | Description |
|--------|------|-------------|
| `PB_URL` | `str` | PocketBase base URL (from env or default `http://127.0.0.1:8090`) |
| `PB_SUPERUSER_EMAIL` | `str` | Superuser email (from env) |
| `PB_SUPERUSER_PASSWORD` | `str` | Superuser password (from env) |
| `pb_request(method, path, data, token, raw_response)` | function | Low-level HTTP request to PB API |
| `pb_authed_request(method, path, data, raw_response)` | function | Auto-authenticated superuser request (retries on 401) |
| `get_superuser_token(force)` | function | Get cached superuser bearer token |
| `print_result(success, status, data)` | function | Print structured JSON output |
| `PBRequestError` | exception | Raised on HTTP errors (has `.status` and `.data`) |

> **Do not** invent exports that don't exist (e.g., `get_config`). Check this table or read `pb_config.py` directly.

### Connection Check

```bash
python scripts/pb_health.py
```

Runs a health check and (if credentials are available) a superuser authentication test.

## 2. Authentication

### Superuser Authentication

```bash
python scripts/pb_auth.py
```

Authenticates using `PB_SUPERUSER_EMAIL` and `PB_SUPERUSER_PASSWORD` via `POST /api/collections/_superusers/auth-with-password`. Returns a token.

### User Authentication

```bash
python scripts/pb_auth.py --collection users --identity user@example.com --password secret
```

Authenticates against any auth collection.

### Token Usage

Each script internally auto-acquires and caches the superuser token. On a 401 error, it retries authentication once.

**Details:** `Read references/auth-api.md` — OAuth2, impersonate, password reset, etc.

## 3. Collection Management

### List

```bash
python scripts/pb_collections.py list
python scripts/pb_collections.py list --filter "name~'user'" --sort "-created"
```

### Get

```bash
python scripts/pb_collections.py get posts
python scripts/pb_collections.py get pbc_1234567890
```

### Create

```bash
# Inline JSON
python scripts/pb_collections.py create '{"name":"posts","type":"base","fields":[{"name":"title","type":"text","required":true},{"name":"content","type":"editor"}]}'

# From file
python scripts/pb_collections.py create --file schema.json
```

Collection types:
- `base` — Standard data collection
- `auth` — Auth collection (automatically adds email, password, username, etc.)
- `view` — Read-only SQL view (requires `viewQuery`)

> **Warning:** PocketBase ships with a `users` auth collection already created. Do **not** `POST` to create a new `users` collection — it will fail with a name conflict. Instead, use `PATCH /api/collections/users` (or `pb_collections.py update users '{...}'`) to customize the existing collection (add fields, change rules, etc.).

### Batch Creation (Recommended for multi-collection setups)

When creating 3+ collections (especially with relations), use import instead of individual create calls:

1. Write a single JSON file with all collections
2. Use collection **names** (not IDs) in `collectionId` for relation fields — PocketBase resolves them during import
3. Import all at once

```bash
python scripts/pb_collections.py import --file collections.json
```

Example `collections.json`:
```json
{
  "collections": [
    {
      "name": "categories",
      "type": "base",
      "fields": [
        {"name": "name", "type": "text", "required": true}
      ]
    },
    {
      "name": "posts",
      "type": "base",
      "fields": [
        {"name": "title", "type": "text", "required": true},
        {"name": "category", "type": "relation", "collectionId": "categories", "maxSelect": 1}
      ],
      "listRule": "@request.auth.id != ''",
      "viewRule": "@request.auth.id != ''"
    }
  ],
  "deleteMissing": false
}
```

This replaces the Phase 1 (create without relations) → Phase 2 (get IDs) → Phase 3 (update with relations) workflow.

**Import pitfalls:**
- **Self-referencing relations** (e.g., `parent` field pointing to the same collection) fail on import because the collection doesn't exist yet when the relation is resolved. Use a 2-pass strategy: create the collection without the self-referencing field, then PATCH to add it:
  ```bash
  python scripts/pb_collections.py create '{"name":"categories","type":"base","fields":[{"name":"name","type":"text","required":true}]}'
  python scripts/pb_collections.py update categories '{"fields":[{"name":"name","type":"text","required":true},{"name":"parent","type":"relation","collectionId":"categories","maxSelect":1}]}'
  ```
- **Indexes** must be SQL strings (e.g., `"CREATE INDEX idx_name ON posts (title)"`), not objects
- **Collection names** are case-sensitive and must match exactly in `collectionId` references

### Update

```bash
python scripts/pb_collections.py update posts '{"listRule":"@request.auth.id != '\'''\''","fields":[{"name":"title","type":"text","required":true},{"name":"content","type":"editor"},{"name":"status","type":"select","values":["draft","published"]}]}'
```

### Delete

```bash
python scripts/pb_collections.py delete posts
```

### Import

```bash
python scripts/pb_collections.py import --file collections.json
```

`collections.json` is a collections array, or `{"collections": [...], "deleteMissing": false}` format.

**Details:** `Read references/collections-api.md` — API rule syntax, all parameters.

## 4. Record Management

### List

```bash
python scripts/pb_records.py list posts
python scripts/pb_records.py list posts --filter 'status="published"' --sort "-created" --expand "author" --page 1 --perPage 50
```

### Get

```bash
python scripts/pb_records.py get posts abc123def456789
python scripts/pb_records.py get posts abc123def456789 --expand "author,comments"
```

### Create

```bash
python scripts/pb_records.py create posts '{"title":"Hello World","content":"<p>My first post</p>","status":"draft"}'
python scripts/pb_records.py create posts --file record.json
```

### Update

```bash
python scripts/pb_records.py update posts abc123def456789 '{"status":"published"}'
```

### Delete

```bash
python scripts/pb_records.py delete posts abc123def456789
```

### Filter Syntax Quick Reference

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equal | `status = "published"` |
| `!=` | Not equal | `status != "draft"` |
| `>`, `>=`, `<`, `<=` | Comparison | `count > 10` |
| `~` | Contains (LIKE) | `title ~ "hello"` |
| `!~` | Does not contain | `title !~ "test"` |
| `?=`, `?~` etc. | Array/multi-value field | `tags ?= "news"` |

Grouping: `(expr1 && expr2) || expr3`

### Sort

`-created` (DESC), `+title` (ASC), `@random`. Comma-separated for multiple fields.

### Expand (Relation Expansion)

`--expand "author"` — Direct relation.
`--expand "author.profile"` — Nested relation (up to 6 levels).
`--expand "author,category"` — Multiple relations.

**Details:** `Read references/records-api.md` — Batch operations, field selection, all operators.

## 5. Backup & Restore

```bash
# List
python scripts/pb_backups.py list

# Create (omit name for auto-generated timestamp name)
python scripts/pb_backups.py create
python scripts/pb_backups.py create my_backup.zip

# Restore (caution: replaces all data; server restart involved)
python scripts/pb_backups.py restore pb_backup_20240101120000.zip

# Delete
python scripts/pb_backups.py delete pb_backup_20240101120000.zip
```

**Notes:**
- Restore replaces all data (no merge)
- Server becomes temporarily unavailable during restore
- Always create a backup of current data before restoring

**Details:** `Read references/backups-api.md`

## 6. Migrations

### Auto-Migration (Primary Workflow — Both Modes)

PocketBase **automatically generates migration files** whenever you change a collection via the Admin UI or the API (e.g., `pb_collections.py create/update`).

| Mode | Auto-generated file format | Directory | Requirement |
|------|---------------------------|-----------|-------------|
| Standalone | `.js` | `pb_migrations/` | Enabled by default |
| Go package | `.go` | `pb_migrations/` | `migratecmd.MustRegister()` with `Automigrate: true` |

**Do NOT hand-write migration files for collection schema creation** — use `pb_collections.py` and let PocketBase generate them.

**Typical workflow (both modes):**
1. Start PocketBase (standalone: `./pocketbase serve`, Go: `go run . serve`)
2. Create/update collections via `pb_collections.py create`, `pb_collections.py import --file collections.json`, or Admin UI
3. PocketBase writes a timestamped migration file to `pb_migrations/`
4. Commit the generated file to git
5. On deploy, PocketBase runs pending migrations automatically at startup

Manual migration files are only for: **seed data, data transforms, raw SQL, and superuser creation**.

### Manual Migration (for operations not auto-generated)

Use `pb_create_migration.py` to generate an empty template when you need to write migration logic that the Admin UI cannot produce:

- Data transformation (copy/reformat existing field values)
- Raw SQL operations
- Seed data insertion
- Complex multi-step schema changes

```bash
python scripts/pb_create_migration.py "backfill_user_slugs"
python scripts/pb_create_migration.py "seed_categories" --dir ./pb_migrations
```

Generates a file in `{timestamp}_{description}.js` format. Write migration logic in the `// === UP ===` and `// === DOWN ===` sections.

### Common Patterns

| Pattern | UP | DOWN |
|---------|-----|------|
| Create collection | `new Collection({...})` + `app.save()` | `app.findCollectionByNameOrId()` + `app.delete()` |
| Add field | `collection.fields.add(new Field({...}))` | `collection.fields.removeByName()` |
| Remove field | `collection.fields.removeByName()` | `collection.fields.add(new Field({...}))` |
| Change rules | `collection.listRule = "..."` | Revert to original rule |
| Execute SQL | `app.db().newQuery("...").execute()` | Reverse SQL |
| Seed data | `new Record(collection)` + `app.save()` | Delete records |

**Details:** `Read references/migrations.md` — Code examples for all patterns.
**Field types:** `Read references/field-types.md` — All field types and configuration options.

## 7. Error Handling

All scripts output structured JSON:

```json
{
  "success": true,
  "status": 200,
  "data": { ... }
}
```

### Common Error Codes

| HTTP Status | Meaning | Resolution |
|-------------|---------|------------|
| 400 | Bad Request | Check request body. Validation error details in `data` field |
| 401 | Unauthorized | Token expired. Scripts auto-retry |
| 403 | Forbidden | Operation denied by API rules. Check rules |
| 404 | Not Found | Collection or record does not exist |

Validation error example:
```json
{
  "success": false,
  "status": 400,
  "data": {
    "status": 400,
    "message": "Failed to create record.",
    "data": {
      "title": {
        "code": "validation_required",
        "message": "Missing required value."
      }
    }
  }
}
```

## 8. Quick Reference

| Task | Script | Detail Reference |
|------|--------|-----------------|
| Connection check | `python scripts/pb_health.py` | — |
| Superuser auth | `python scripts/pb_auth.py` | `references/auth-api.md` |
| User auth | `python scripts/pb_auth.py --collection <name> --identity <email> --password <pw>` | `references/auth-api.md` |
| List collections | `python scripts/pb_collections.py list` | `references/collections-api.md` |
| Get collection | `python scripts/pb_collections.py get <name>` | `references/collections-api.md` |
| Create collection | `python scripts/pb_collections.py create '<json>'` | `references/collections-api.md`, `references/field-types.md` |
| Update collection | `python scripts/pb_collections.py update <name> '<json>'` | `references/collections-api.md` |
| Delete collection | `python scripts/pb_collections.py delete <name>` | `references/collections-api.md` |
| Import collections | `python scripts/pb_collections.py import --file <file>` | `references/collections-api.md` |
| List records | `python scripts/pb_records.py list <collection>` | `references/records-api.md` |
| Get record | `python scripts/pb_records.py get <collection> <id>` | `references/records-api.md` |
| Create record | `python scripts/pb_records.py create <collection> '<json>'` | `references/records-api.md` |
| Update record | `python scripts/pb_records.py update <collection> <id> '<json>'` | `references/records-api.md` |
| Delete record | `python scripts/pb_records.py delete <collection> <id>` | `references/records-api.md` |
| List backups | `python scripts/pb_backups.py list` | `references/backups-api.md` |
| Create backup | `python scripts/pb_backups.py create [name]` | `references/backups-api.md` |
| Restore backup | `python scripts/pb_backups.py restore <key>` | `references/backups-api.md` |
| Delete backup | `python scripts/pb_backups.py delete <key>` | `references/backups-api.md` |
| Generate migration | `python scripts/pb_create_migration.py "<description>"` | `references/migrations.md` |
| API rules design     | — | `references/api-rules-guide.md`   |
| Common pitfalls      | — | `references/gotchas.md`           |
| Relation patterns    | — | `references/relation-patterns.md` |
| JS SDK reference     | — | `references/js-sdk.md`            |
| JSVM hooks           | — | `references/jsvm-hooks.md`        |
| File handling        | — | `references/file-handling.md`     |
| Run E2E tests        | `python3 test_e2e.py` | `references/e2e-testing.md` |
| E2E test helpers     | Import from `scripts/pb_e2e_helpers.py` | `references/e2e-testing.md` |
| Go: build & run      | `go build -o myapp . && ./myapp serve`                          | `references/go-framework.md`   |
| Go: dev run          | `go run . serve`                                                 | `references/go-framework.md`   |
| Go: create superuser | `go run . superuser create email pw`                             | `references/go-framework.md`   |
| Go: manual migration template (seed data / data transforms only) | `assets/migration-template.go`       | `references/go-migrations.md`  |
