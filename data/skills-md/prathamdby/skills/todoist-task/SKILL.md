---
name: todoist-task
description: >
  todoist-task to create or preview self-contained tasks with requested metadata.
---

# Todoist task

Preserve meaning, literals, links, and constraints; invent no requirements or
completion criteria. Default Inbox, no parent/date, p4; creation unless preview.
Record `request | title/description | project/parent/date/priority | missing | duplicate | IDs | verified | terminal`.

## 1. Resolve and clarify

Use Todoist connector only. Unavailable/disconnected blocks, not substitution.
Preview uses read-only metadata resolution and never creates a task/project.
Resolve relative dates with user's Todoist timezone/configured week; ordinary
deadline/done-by means due date, dedicated deadline only when explicitly asked
and supported.
Resolve project exactly, create one only if requested. Parent needs URL/ID/
unique title; subtasks have no date unless supplied or inheritance was requested.

Apply future-reader test: identifiable/executable six months later without the
conversation? Projects do not name tools/repos/branches/files/issues.
Ask one question listing missing identifiers, create nothing that turn, then
resume without another confirmation. User-accepted ambiguity is recorded.
Done when metadata and references resolve or uncertainty is explicitly accepted.

## 2. Format

Title: action verb + specific deliverable + necessary qualifier, sentence case,
no period; aim 4–10 words, specificity wins. Preserve exact technical names.
Description: short context/result sentence, bullets for distinct supplied
requirements, supplied test/delivery/follow-up last. Hyperlink links.
Use headings only for distinct areas of a long task; avoid imposed Objective/
Requirements/Done when boilerplate, repeated metadata, and invented work.
Done when title and description stand alone and read naturally.

## 3. Preview or create

Resolve project/parent and search active normalized title + parent;
match → DUPLICATE. Preview shows exact payload and returns PREVIEW without
write calls. Otherwise create each item once; never retry batch successes.
Done when preview is sent or each creation has an ID/identified failure.

## 4. Verify

Read back every created title/description/project/parent/date/priority.
Correct an authorized mismatch once; remaining difference → BLOCKED with ID.
Report verified title, project, parent if present, due date.
Done when every reported success matches the service.

Terminals: CREATED, PREVIEW, NEEDS_CONTEXT, DUPLICATE, BLOCKED.
