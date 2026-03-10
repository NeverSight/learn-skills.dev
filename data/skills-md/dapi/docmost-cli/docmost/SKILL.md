---
name: docmost
description: >
  Use when user wants to manage Docmost documentation via docmost-cli: pages, spaces, workspace,
  members, groups, invites, comments, shares, files, search, and export/import.
  Trigger on requests about wiki/docs pages, knowledge base, page history/trash,
  page organization, access control, public sharing, file attachments,
  and workspace administration from terminal.
---

# docmost

Docmost CLI skill for AI agents.

## Install

Install this skill from GitHub:

```bash
npx skills add dapi/docmost-cli --skill docmost --agent '*' -g -y
```

Install CLI:

```bash
npm install -g github:dapi/docmost-cli
```

Set environment variables (recommended):

```bash
export DOCMOST_API_URL=https://docs.example.com/api
export DOCMOST_TOKEN=<token>
# or login with email/password:
export DOCMOST_EMAIL=<email>
export DOCMOST_PASSWORD=<password>
```

Quick check:

```bash
docmost workspace-public --format json
```

## Execution Rules

- No pre-flight checks. Run the needed command directly. If `docmost` is not found, install it (`npm install -g github:dapi/docmost-cli`) and retry.
- All `--format json` output wrapped in envelope: `{ "ok": true, "data": ... }` for success, `{ "ok": false, "error": ... }` for errors.
- Prefer `--format json` for agent workflows.
- Use `--format table` when user explicitly wants human-readable tabular output.
- `--format text` is supported only by:
  - `page-info` (returns markdown content)
  - `page-history-detail` (returns markdown content)
  - `invite-link` (returns raw link)
- Prefer environment variables for credentials; avoid `--password` in command history/process list.
- Auth precedence: `--token` > `DOCMOST_TOKEN` > `--email/--password` > `DOCMOST_EMAIL/DOCMOST_PASSWORD`.
- Use global pagination controls for list/history commands:
  - `--limit <n>` (1..100, default 100)
  - `--max-items <n>` (stop after N total records)
- For markdown/prose content (`page-update`, `comment-create`, `comment-update`), use:
  - literal string, `@path/to/file.md`, or `-` (stdin)
- Binary export/download commands write bytes to stdout unless `--output` is provided:
  - `page-export`, `space-export`, `file-download`
- Use `--quiet` when only exit status matters.

## Output Format

All `--format json` responses use a predictable envelope:

### Success (single object)
```json
{ "ok": true, "data": { "id": "abc", "title": "Runbook" } }
```

### Success (list)
```json
{ "ok": true, "data": [{ "id": "abc" }], "meta": { "count": 2, "hasMore": false } }
```

### Error (stderr)
```json
{ "ok": false, "error": { "code": "NOT_FOUND", "message": "Page not found", "details": null } }
```

### Parsing rules for agents
- Always check `ok` field first
- For lists: items in `data` array, check `meta.hasMore` for pagination
- For mutations: created/updated object returned in `data`
- Errors include typed `code`: AUTH_ERROR, NOT_FOUND, VALIDATION_ERROR, NETWORK_ERROR, INTERNAL_ERROR
- Exit codes: 0=success, 1=internal, 2=auth, 3=not_found, 4=validation, 5=network
- Use `docmost commands` to discover all available commands and their options

## Core Command Patterns

### Discovery

```bash
docmost commands                          # list all commands with options as JSON
```

### Workspace + Members

```bash
docmost workspace-info --format json
docmost workspace-public --format json
docmost workspace-update --name "Docs" --description "Team docs" --format json
docmost workspace-update --enforce-sso true --enforce-mfa true --format json

docmost member-list --format table
docmost member-role --user-id <userId> --role admin --format json
docmost member-remove --user-id <userId> --format json
```

### Users

```bash
docmost user-me --format json
docmost user-update --name "Alice" --locale en --page-edit-mode edit --full-page-width true --format json
```

### Spaces

```bash
docmost space-list --format table
docmost space-info --space-id <spaceId> --format json

docmost space-create --name "Engineering" --slug engineering --description "Tech docs" --format json
docmost space-update --space-id <spaceId> --name "Platform" --format json
docmost space-delete --space-id <spaceId> --format json

docmost space-member-list --space-id <spaceId> --format table
docmost space-member-add --space-id <spaceId> --role writer --user-ids "u1,u2" --format json
docmost space-member-add --space-id <spaceId> --role reader --group-ids "g1,g2" --format json
docmost space-member-remove --space-id <spaceId> --user-id <userId> --format json
docmost space-member-role --space-id <spaceId> --group-id <groupId> --role admin --format json

docmost space-export --space-id <spaceId> --export-format markdown --output ./space.zip --format json
docmost space-export --space-id <spaceId> --export-format html --include-attachments > ./space.zip
```

### Pages

```bash
docmost page-list --format table
docmost page-list --space-id <spaceId> --format table

docmost page-info --page-id <pageId> --format json
docmost page-info --page-id <pageId> --format text

docmost page-create --space-id <spaceId> --title "Runbook" --icon "book" --format json
docmost page-create --space-id <spaceId> --title "Child" --parent-page-id <parentId> --format json

docmost page-update --page-id <pageId> --title "Runbook v2" --format json
docmost page-update --page-id <pageId> --content @./content.md --format json
echo "# Updated" | docmost page-update --page-id <pageId> --content - --format json

docmost page-move --page-id <pageId> --parent-page-id <parentId> --position a00000 --format json
docmost page-move --page-id <pageId> --root --format json
docmost page-move-to-space --page-id <pageId> --space-id <targetSpaceId> --format json

docmost page-delete --page-id <pageId> --format json
docmost page-delete --page-id <pageId> --permanently-delete --format json
docmost page-delete-bulk --page-ids "id1,id2,id3" --format json

docmost page-restore --page-id <pageId> --format json
docmost page-trash --space-id <spaceId> --format table
docmost page-duplicate --page-id <pageId> --format json
docmost page-duplicate --page-id <pageId> --space-id <targetSpaceId> --format json

docmost page-breadcrumbs --page-id <pageId> --format table
docmost page-tree --space-id <spaceId> --format json
docmost page-tree --page-id <pageId> --format json

docmost page-history --page-id <pageId> --limit 50 --max-items 200 --format table
docmost page-history-detail --history-id <historyId> --format json
docmost page-history-detail --history-id <historyId> --format text
```

### Page Import/Export

```bash
docmost page-export --page-id <pageId> --export-format markdown --output ./page.zip
docmost page-export --page-id <pageId> --export-format html --include-children --include-attachments > ./page.zip

docmost page-import --file ./page.md --space-id <spaceId> --format json
docmost page-import-zip --file ./notion.zip --space-id <spaceId> --source notion --format json
```

`page-import-zip --source` supports: `generic`, `notion`, `confluence`.

### Search

```bash
docmost search --query "onboarding" --format table
docmost search --query "oauth" --space-id <spaceId> --creator-id <userId> --format json

docmost search-suggest --query "auth" --format json
docmost search-suggest --query "auth" --space-id <spaceId> --include-pages --include-groups --max-results 20 --format json
```

### Invites

```bash
docmost invite-list --format table
docmost invite-info --invitation-id <inviteId> --format json

docmost invite-create --emails "a@x.com,b@y.com" --role member --format json
docmost invite-create --emails "team@x.com" --role admin --group-ids "g1,g2" --format json

docmost invite-revoke --invitation-id <inviteId> --format json
docmost invite-resend --invitation-id <inviteId> --format json
docmost invite-link --invitation-id <inviteId> --format text
```

### Groups

```bash
docmost group-list --format table
docmost group-info --group-id <groupId> --format json

docmost group-create --name "Tech Writers" --description "Docs team" --format json
docmost group-create --name "Maintainers" --user-ids "u1,u2" --format json

docmost group-update --group-id <groupId> --name "Platform Writers" --format json
docmost group-delete --group-id <groupId> --format json

docmost group-member-list --group-id <groupId> --format table
docmost group-member-add --group-id <groupId> --user-ids "u1,u2" --format json
docmost group-member-remove --group-id <groupId> --user-id <userId> --format json
```

### Comments

```bash
docmost comment-list --page-id <pageId> --format table
docmost comment-info --comment-id <commentId> --format json

docmost comment-create --page-id <pageId> --content @./comment.md --format json
docmost comment-create --page-id <pageId> --content "Please clarify" --selection "Auth flow" --format json
docmost comment-create --page-id <pageId> --content "Reply text" --parent-comment-id <commentId> --format json

docmost comment-update --comment-id <commentId> --content "Updated comment" --format json
docmost comment-delete --comment-id <commentId> --format json
```

### Shares

```bash
docmost share-list --format table
docmost share-info --share-id <shareId> --format json
docmost share-for-page --page-id <pageId> --format json

docmost share-create --page-id <pageId> --include-subpages true --search-indexing false --format json
docmost share-update --share-id <shareId> --include-subpages false --format json
docmost share-delete --share-id <shareId> --format json
```

### Files

```bash
docmost file-upload --file ./diagram.png --page-id <pageId> --format json
docmost file-upload --file ./diagram-v2.png --page-id <pageId> --attachment-id <attachmentId> --format json

docmost file-download --file-id <fileId> --file-name diagram.png --output ./diagram.png
docmost file-download --file-id <fileId> --file-name report.pdf > ./report.pdf
```

## Agent Workflows

### Page CRUD (recommended default)

For requests like "create/update/move/delete doc page":

1. Resolve workspace and target space:
   - `docmost workspace-info --format json` → check `.ok`, use `.data`
   - `docmost space-list --format json` → iterate `.data[]`, check `.meta.hasMore`
2. Inspect existing pages:
   - `docmost page-list --space-id <spaceId> --format json` → iterate `.data[]`
3. Read source page when modifying:
   - `docmost page-info --page-id <pageId> --format text`
4. Apply mutation:
   - `page-create` / `page-update` / `page-move` / `page-delete` → check `.ok`, get `.data.id`
5. Verify:
   - `docmost page-info --page-id <pageId> --format json` → check `.ok`

### Search + History Investigation

For requests like "find where this was documented" or "who changed this":

1. `docmost search --query "..." --format table`
2. `docmost page-info --page-id <pageId> --format text`
3. `docmost page-history --page-id <pageId> --format table`
4. `docmost page-history-detail --history-id <historyId> --format text`

### Access Control

For requests like "add/remove access":

1. Workspace level:
   - `member-list`, `member-role`, `member-remove`, `invite-*`
2. Space level:
   - `space-member-list`, `space-member-add`, `space-member-remove`, `space-member-role`
3. Public page sharing:
   - `share-for-page`, `share-create`, `share-update`, `share-delete`

### Export/Import and Attachments

1. Export content: `page-export` / `space-export`
2. Import content: `page-import` / `page-import-zip`
3. Attach files: `file-upload`
4. Download files: `file-download`

## Request Semantics

- "мой workspace / моё пространство" -> `docmost workspace-info`
- "spaces / разделы" -> `docmost space-list`
- "pages / страницы" -> `docmost page-list`
- "найди / search" -> `docmost search --query "..."`
- "история изменений" -> `docmost page-history`
- "удалённые страницы / корзина" -> `docmost page-trash`
- "доступ / access" -> `member-*` / `space-member-*` / `share-*`

## Trigger Examples

### Should trigger

- "создай страницу в Docmost"
- "обнови страницу runbook"
- "найди в вики всё про oauth"
- "покажи историю изменений этой страницы"
- "восстанови удалённую страницу"
- "перенеси страницу в другой space"
- "экспортни space в markdown"
- "добавь пользователя в space как reader"
- "создай публичный share для страницы"
- "upload файл на страницу"
- "list all Docmost spaces"
- "invite new users to workspace"
- "change member role to admin"
- "import Notion zip into Docmost"
- "покажи дерево страниц"
- "продублируй страницу"

### Should not trigger

- Editing local markdown files without Docmost API interaction
- Git/GitHub operations
- Slack/Telegram/email messaging tasks
- Non-Docmost web scraping or browser automation
