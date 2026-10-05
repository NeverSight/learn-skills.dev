---
name: yandex-tracker
description: Work with Yandex Tracker through the yandex-tracker MCP server (traker-mcp) — search issues with the Tracker query language, create/edit/transition issues with valid field values, manage checklists, comments, worklog, links, bulk changes, queues, boards, dashboards, projects, portfolios and goals. Use when the user mentions Yandex Tracker, Трекер, задачи/очереди/доски/проекты/цели, issue keys like KEY-123, or asks to find/create/update/close/assign issues, check statuses, or plan work in Tracker.
---

# Yandex Tracker via traker-mcp

All interaction goes through MCP tools from the `yandex-tracker` server
(github.com/sdamarketing/tracker_mcp). If the tools are not available, help the
user install the server first:

```bash
curl -fsSL https://raw.githubusercontent.com/sdamarketing/tracker_mcp/main/install.sh | bash
```

## Tool map (185 tools — full v3 API coverage)

| Task | Tools |
|---|---|
| Search / count / suggest | `find_issues` (incl. query2 + scroll >10k), `count_issues`, `get_search_suggest`, `release_search_scroll` |
| Issue lifecycle | `create_issue`, `get_issue`, `edit_issue`, `move_issue`, `get_issue_changelog` |
| Statuses | `get_issue_transitions`, `execute_transition` |
| Links / external apps | `get_issue_links`, `create_issue_link`, `delete_issue_link`, `get_external_applications`, `get_external_links`, `create_external_link`, `delete_external_link` |
| Comments / checklist / time | `add_comment`, `get_issue_comments`, `get_issue_comment`, `edit_comment`, `delete_comment`, `add_comment_reaction`, `get_checklist`, `add_checklist_item`, `edit_checklist_item`, `delete_checklist_item`, `delete_checklist`, `get_issue_worklog`, `add_worklog_record`, `edit_worklog_record`, `delete_worklog_record`, `find_worklog_records` |
| Files | `list_issue_attachments`, `get_issue_attachment`, `download_issue_attachment`, `get_attachment_thumbnail`, `upload_issue_attachment`, `upload_temp_attachment`, `delete_issue_attachment` |
| Reports / filters | `create_issue_report`, `find_issue_reports`, `create_filter`, `get_filter`, `update_filter`, `delete_filter` |
| Bulk | `bulk_update_issues`, `bulk_move_issues`, `bulk_transition_issues`, `get_bulk_operation_info`, `bulk_update_entities` |
| Queues & config | queues CRUD + `set_queue_access`/`get_queue_user_access`/`get_queue_group_access`, local fields CRUD, components CRUD (+ access), versions CRUD, macros CRUD, triggers (CRUD + logs), autoactions (CRUD + logs), workflows (CRUD + action edit) |
| Boards / sprints | boards CRUD + `get_boards_paginate`, columns CRUD, sprints: `get_sprint`/`create_sprint`/`update_sprint`/`start_sprint`/`archive_sprint`/`delete_sprint` |
| Dashboards | `create_dashboard`, `create_cycle_time_widget` |
| Projects / goals | projects CRUD + `get_project_queues`, entities CRUD + comments/checklists/attachments/links/events/access/permissions |
| Catalogs & users | reads + writes for issue types, statuses, resolutions, priorities; fields CRUD + categories; `get_users`, `get_users_relative`, `get_user`, `get_current_user` |
| Absences (gaps) | `create_gaps`, `find_gaps`, `delete_gaps` |
| Migration (import) | `import_issue`, `import_issue_comment`, `import_issue_link`, `import_worklog_record`, `import_issue_attachment` — admin-only, задним числом |

## Core rules

1. **Use keys, not names, for field values**: statuses (`open`, `closed`),
   priorities (`critical`), resolutions (`fixed`), issue types (`task`, `bug`).
   Organizations define custom values — when in doubt or on a 400 error, call
   the catalog tools (`get_priorities`, `get_statuses`, `get_resolutions`,
   `get_issue_types`) and retry with real keys. Never guess priority keys:
   common orgs have `trivial minor normal critical blocker`, some add
   `minimal`/`important` — there is no universal `major`.
2. **Search takes exactly one source**: per `find_issues` call pass one of
   `queue`, `keys`, `filter`, `filterId`, `query`, `query2`. They are not
   combined; priority order is queue > keys > filter > query.
3. **Dates** are `YYYY-MM-DD`; **durations** are ISO 8601 (`PT2H30M`, `P3D`,
   `P1WT4H`). Tracker counts time in 5-day work weeks / 8-hour days, so `P5D`
   shows as 1 week.
4. **Markdown**: issue descriptions, comments and entity descriptions support
   Yandex Flavored Markdown (`**bold**`, lists, ```code```).
5. **Rights mirror the UI**: the token acts as its user. A 403 means the user
   really lacks access — say so instead of retrying.
6. **IAM tokens live ≤ 12 hours**: on 401 with `Bearer` auth, tell the user to
   issue a fresh IAM token and update the client config (`.env` or the MCP
   client's environment block). OAuth tokens (`y0__…`) don't expire like that.

- **Confirm destructive calls.** Every `delete_*`/`bulk_*` tool refuses to run without
  `confirm: true`. First show the user exactly what will be changed or deleted,
  get approval, then retry with `confirm: true`. Never guess.
- **Catalogs are cached.** get_priorities/get_statuses/get_issue_types/get_resolutions/
  get_issue_fields are cached ~10 min; after admin create/update the cache is dropped.

## Recipes

### Find issues

```
find_issues { query: 'Queue: TREK Assignee: me() Resolution: empty()' }
find_issues { filter: { queue: 'TREK', status: 'open' }, order: '+updatedAt', perPage: 50, page: 1 }
count_issues { query: 'Queue: TREK Assignee: me()' }   // cheap pre-count
```

Query-language sort goes inside `query`: `'Queue: TREK "Sort by": Updated DESC'`.
See [references/query-language.md](references/query-language.md) for the full
syntax. For a queue dump prefer `filter` + pagination (`perPage` default 50).

### Create an issue

```
create_issue {
  queue: 'TREK',                      // case-sensitive key, not the name
  summary: 'Fix login page crash',
  description: 'Steps: **1.** open /login …',
  type: 'bug', priority: 'critical',   // keys from get_issue_types/get_priorities
  assignee: 'user-login',
  tags: ['backend'],
}
```

Before creating in an unfamiliar queue, call `get_queue_fields` — it returns
required fields and allowed values, including queue-local custom fields
(ids like `<queue-id>--fieldname`). Pass custom fields through `extraFields`.

Subtasks: pass `parent: 'TREK-12'` at creation, or link afterwards:

```
create_issue_link { issueId: 'TREK-13', relationship: 'is subtask for', issue: 'TREK-12' }
```

Valid relationships: `relates`, `depends on`, `is dependent by`,
`is subtask for`, `is parent task for`, `duplicates`, `is duplicated by`,
`is epic of`, `has epic`.

### Change status (transition)

Never set status directly. List the workflow transitions first, then execute:

```
get_issue_transitions { issueId: 'TREK-1' }
execute_transition {
  issueId: 'TREK-1',
  transitionId: 'close',
  extraFields: { resolution: 'fixed' },   // closing usually REQUIRES a resolution
  comment: 'Fixed in 1.2.3',
}
```

Transitions depend on the queue's workflow (e.g. `start_progress`, `resolve`,
`need_info`, `in_review`, `close`, `wont_fix`). If `execute_transition`
returns 400, the transition screen requires more fields — read the error, it
names every missing field.

### Edit issues and bulk changes

```
edit_issue   { issueId: 'TREK-1', extraFields: { tags: { add: ['urgent'] } } }
bulk_update_issues { issues: ['TREK-1', 'TREK-2'], values: { priority: 'blocker' } }
bulk_transition_issues { issues: ['TREK-1'], transition: 'close', values: { resolution: 'fixed' } }
```

Array fields support `add` / `remove` / `set` / `replace` commands in
`extraFields`/`values`. Bulk `issues` also accepts a query-language string.
Long bulk operations are async — poll `get_bulk_operation_info` with the
returned id.

### Checklist, worklog, comment

```
add_checklist_item { issueId: 'TREK-1', text: 'Repro on staging' }
edit_checklist_item { issueId: 'TREK-1', itemId: '…', checked: true }  // full-list merge is handled by the tool
delete_checklist { issueId: 'TREK-1' }                                // remove whole checklist
add_worklog_record { issueId: 'TREK-1', start: '2026-10-04T12:00:00.000+0000', duration: 'PT45M' }
find_worklog_records { createdBy: 'user1', createdFrom: '2026-10-01T00:00:00.000+0000' }  // search across issues
add_comment { issueId: 'TREK-1', text: 'Deployed' }
get_issue_comment { issueId: 'TREK-1', commentId: '123' }
add_comment_reaction { issueId: 'TREK-1', commentId: '123', reaction: 'HEART' }
```

### Attachments: download and temp upload

```
list_issue_attachments { issueId: 'TREK-1' }
download_issue_attachment { issueId: 'TREK-1', attachmentId: '456' }
// → images come back as image content (rendered in chat), text as text,
//   other binaries as base64 (≤8 МБ). No filename needed — resolved by id.
get_attachment_thumbnail { issueId: 'TREK-1', attachmentId: '456' }   // preview image
upload_temp_attachment { filePath: '/tmp/screenshot.png' }
// → returns a temp id usable ONCE in:
//   create_issue/add_comment attachmentIds, add_entity_attachment, import tools
upload_issue_attachment { issueId: 'TREK-1', filePath: '/tmp/log.txt' }  // direct attach
```

### Search: suggestions and huge sets (>10 000)

```
get_search_suggest { input: 'login crash' }            // user gave imprecise name
find_issues { query: 'Queue: BIG', scrollType: 'sorted', perScroll: 1000 }
// → returns { _scroll: { scrollId, scrollToken, totalCount, hint }, issues }
// continue: find_issues { …, scrollId: '<scrollId>' }
// done early? release_search_scroll { scrollTokens: { '<scrollId>': '<scrollToken>' } }
```

### Saved filters and reports

```
create_filter { name: 'My bugs', query: 'Queue: TREK Type: bug' }   // → id
find_issues { filterId: 42 }                                          // use it
update_filter { filterId: 42, query: '…' }                           // conditions fully replaced
delete_filter { filterId: 42 }                                       // documented /v2 path — tool handles it
create_issue_report { summary: 'Weekly export', format: 'csv', query: 'Queue: TREK', fields: ['key','summary','status'] }
find_issue_reports {}                                                 // list saved reports
```

### Queues, versions, components

```
get_queues {}                          // find the right queue key first
create_queue_version { queueId: 'TREK', name: 'v2.0', dueDate: '2026-12-31' }
create_component { name: 'Billing', queue: 'TREK' }
```

Queue keys are uppercase Latin and case-sensitive everywhere.

### Projects, portfolios, goals (entities)

`entityType` is `project` | `portfolio` | `goal`; all entity fields go in the
`fields` object (the tool wraps them for the API):

```
search_entities { entityType: 'goal', input: 'выручка' }
create_entity { entityType: 'goal', summary: 'Automate Tracker', fields: { end: '2026-12-31' } }
update_entity { entityType: 'project', entityId: '…', fields: { parentEntity: { primary: '<portfolio-id>', secondary: [] } } }
```

Entity statuses: projects/portfolios `draft, in_progress, according_to_plan,
postponed, at_risk, blocked, launched, cancelled`; goals `draft,
according_to_plan, at_risk, blocked, achieved, partially_achieved,
not_achieved, exceeded, cancelled`. `search_entities` returns `id`/`shortId` —
`get_entity`/`update_entity` need the string `id`.

### Boards and dashboards

```
get_statuses {}                       // column statuses must be real keys
create_board { name: 'Dev board', columns: [ { name: 'To Do', statuses: ['open'] },
  { name: 'In Progress', statuses: ['inProgress'] } ] }
update_board { boardId: 4, name: 'Dev board v2', columns: [...] }     // owner not editable
delete_board { boardId: 4 }
get_boards_paginate { perPage: 500 }                                  // >500 boards: pass last id
// Columns (need the board "version" from get_board — If-Match optimistic lock):
create_board_column { boardId: 4, name: 'QA', statuses: ['testing'], version: '1' }
update_board_column { boardId: 4, columnId: 9, statuses: ['tested'], version: '2' }
delete_board_column { boardId: 4, columnId: 9, version: '3' }
create_dashboard { name: 'Team dashboard', layout: 'two-columns' }
create_cycle_time_widget { dashboardId: 7, description: 'Cycle time TREK', query: 'Queue: TREK', fromStatuses: [{ key: 'open' }], toStatuses: [{ key: 'closed' }] }
```

### Sprints (boards with sprintsAvailable)

```
create_sprint { boardId: 4, name: 'Sprint 1', startDate: '2026-10-05', endDate: '2026-10-19' }
start_sprint { sprintId: '53', version: '1' }       // → in_progress
archive_sprint { sprintId: '53', version: '2' }     // → archived
update_sprint { sprintId: '53', name: 'Sprint 1.1', version: '3' }
delete_sprint { sprintId: '53' }
```
Sprint tools need the sprint `version` (from get_sprint / get_board_sprints) —
If-Match optimistic locking, 412 on conflict.

### Queue configuration: rights, fields, automation

```
// Access rights (arrays overwrite, {add:[…]} / {remove:[…]} apply deltas):
set_queue_access { queueId: 'TREK', permissions: { read: { users: { add: ['user1'] } }, write: { groups: [42] } } }
get_queue_user_access { queueId: 'TREK', userId: 'user1' }
// Local fields:
create_queue_local_field { queueId: 'TREK', name: { ru: 'Слой' }, id: 'layer', category: '…', type: 'ru.yandex.startrek.core.fields.StringFieldType' }
// Versions / components:
update_queue_version { versionId: 3, name: 'v2.1', dueDate: '2026-12-31' }
delete_queue_version { versionId: 3 }
get_components {}                                                    // org-wide
update_component { componentId: 5, version: 2, name: 'Billing v2' }  // version from get_component
// Macros:
create_queue_macro { queueId: 'TREK', name: 'Close as dup', body: 'Closed as duplicate', issueUpdate: { resolution: 'duplicate' } }
// Triggers (actions/conditions are typed objects — see docs):
create_queue_trigger { queueId: 'TREK', name: 'Auto-assign', actions: [ { type: 'Update', update: { assignee: 'user1' } } ] }
get_queue_trigger_logs { queueId: 'TREK', triggerId: 7, limit: 50 }
// Workflows:
create_workflow { name: 'Custom flow', initialAction: { name: { ru: 'Открыть' }, target: 'open' }, steps: [ { status: 'open', actions: [] } ] }
get_queue_workflows { queueId: 'TREK' }
update_workflow_action { workflowId: 'W1', statusKey: 'open', actionId: 'close', version: 3, target: 'closed' }
```

### Entities: full lifecycle beyond CRUD

```
// Checklist on a project (same shape as issue checklists):
add_entity_checklist_items { entityType: 'project', entityId: '…', items: [ { text: 'Migrate DB' } ] }
// Links between entities:
create_entity_link { entityType: 'goal', entityId: '…', links: [ { relationship: 'is supported by', entity: '<project-id>' } ] }
get_entity_links { entityType: 'goal', entityId: '…' }
delete_entity_link { entityType: 'goal', entityId: '…', right: '<project-id>' }
// Event history:
get_entity_events { entityType: 'project', entityId: '…', perPage: 50 }
// Bulk (fields + comment + links for every entity at once):
bulk_update_entities { entityType: 'goal', metaEntities: ['id1', 'id2'], fields: { entityStatus: 'at_risk' }, comment: 'Priority raised' }
// Access rights:
get_entity_permissions { entityType: 'project', entityId: '…' }
update_entity_permissions { entityType: 'project', entityId: '…', grant: { READ: { users: ['user1'] } } }
get_entity_access {}        // + inheritance sources
update_entity_access {}     // permissionSources + acl; disable inheritance before acl changes
// Key results of a goal (field via update_entity):
update_entity { entityType: 'goal', entityId: '…', fields: { keyResultItems: [ { type: 'value', text: '1000 MAU', progress: { start: 0, end: 1000, current: 300 } } ] } }
```

### External links and migration

```
get_external_applications {}                          // installed connectors
create_external_link { issueId: 'TREK-1', relationship: 'RELATES', key: 'JIRA-123', origin: '<app-id>' }
// Migration (admin only, custom authors/dates «задним числом»):
import_issue { queue: 'TREK', summary: 'Old issue', createdAt: '2025-01-15T10:00:00.000+0000', createdBy: 'user1' }
import_issue_comment { issueId: 'TREK-1', text: 'From Jira', createdAt: '…', createdBy: 'user1' }
import_issue_attachment { issueId: 'TREK-1', filePath: '/backup/old.png', createdAt: '…', createdBy: 'user1' }
// Absences (admin):
create_gaps { gaps: [ { user: 'user1', workflow: 'vacation', from: '2026-11-01T00:00:00.000+0000', to: '2026-11-15T00:00:00.000+0000', fullDay: true } ] }
find_gaps { users: ['user1'], from: '…', to: '…' }
```

## Pitfalls (verified against the live API)

- `create_queue_version` — the date field is **`dueDate`**, not `releaseDate`.
- Closing transitions without a resolution → 400. Add `resolution` to
  `extraFields`/`values`.
- `find_issues` with two search params silently uses the higher-priority one;
  three or more → 400 «only keys, queue or query».
- **Optimistic locking**: editing fields, components, triggers, workflows,
  board columns and sprints requires the current `version` (query param or
  board/sprint `version` arg); a mismatch returns 412 — re-fetch and retry.
- Entity write endpoints wrap everything in `fields`; the tools do this for
  you — pass `fields: {…}` per the tool schema.
- `delete_filter` is the only v2-documented endpoint — the tool handles it.
- 403 «Organization is not available, not ready or not found» → wrong
  `TRACKER_ORG_ID` or Tracker not enabled for the org — fix credentials,
  don't retry.
- 401 → bad or expired token (IAM ≤12h). Suggest re-running setup:
  `cd ~/.traker-mcp && npm run setup`.
- Comments and issue text use YFM; raw HTML is not rendered.
- Moving an issue to another queue clears components/versions/projects unless
  `moveAllFields: true`, and drops old-queue local fields.
- The API works in UTC: created/updated timestamps come back UTC±00:00.
- `download_issue_attachment` returns images as image content, text files as
  text, binaries as base64 (≤8 МБ). Use `upload_temp_attachment` first to
  attach to entity descriptions/comments.
- Import tools (`import_*`) create records «задним числом» with custom
  authors/dates — only for migration, admin rights required.

## Dialog examples (how requests map to tool calls)

User: «Покажи мои открытые задачи за эту неделю»
→ find_issues({ query: 'Assignee: me() Resolution: empty() "Updated": >= week start' })
  or simpler: find_issues({ filter: { assignee: 'me()', resolution: 'empty()' } })

User: «Закрой TASK-42 как решённую и напиши туда комментарий»
→ 1. execute_transition({ key: 'TASK-42', transition: 'close',
     extraFields: { resolution: 'fixed' } })
  2. add_comment({ key: 'TASK-42', text: '…' })
  If transition fails with 400 → get_issue_transitions to see valid ids, then retry.

User: «Удали закрытые задачи в очереди OPS за прошлый год»
→ 1. find_issues({ query: 'Queue: OPS Status: resolved() "Resolved at": < 2025-01-01' })
     и/или count_issues — показать пользователю список и количество
  2. Спросить подтверждение явно
  3. Удалять по одной: …destructive ops require confirm: true (все delete_*/bulk_* —
     сначала покажите, ЧТО будет затронуто, и только затем повторите с confirm=true)

User: «Что сейчас в спринте?»
→ get_boards → get_sprints({ boardId }) → задачи спринта — это
  find_issues({ filter: { sprint: { id: … } } }) или board issues через фильтры.

User: «Поставь реакцию 👍 на последний комментарий в TASK-7»
→ get_comments({ key: 'TASK-7' }) → взять id последнего →
  add_comment_reaction({ key: 'TASK-7', commentId, reaction: 'LIKE' })

User: «Сколько времени я списал в марте?»
→ search_worklog({ createdBy: 'me()', createdAt: { from: '2025-03-01T00:00:00.000+0300',
  to: '2025-04-01T00:00:00.000+0300' } })

## References

- [query-language.md](references/query-language.md) — full Tracker query
  language and filter recipes.
- [field-catalogs.md](references/field-catalogs.md) — standard catalogs and
  how to discover org-specific values.
