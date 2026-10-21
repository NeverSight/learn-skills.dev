---
name: weknora
description: Work with a WeKnora knowledge base through its REST API — list and inspect knowledge bases, search one or many of them, import files, URLs, or Markdown, confirm an import finished parsing, read and edit chunks, and ask questions with a streamed answer. Use when the task targets a user's own WeKnora instance and its stored documents; use web or research instead for public sources.
compatibility: Requires a filesystem-based host with shell/network access and a reachable WeKnora instance. Supply WEKNORA_BASE_URL and WEKNORA_API_KEY for independent use; optionally use arks with a managed connection for supported retrieval operations. arks and the SSE consumer require Node.js 20+. Intended for Claude Code and Codex CLI on macOS, Linux, and Windows.
---

# WeKnora

Operate a user's WeKnora knowledge base. Choose the independent environment path or optional managed `arks` path; WeKnora is a connection, not a Web search Provider.

## Readiness and execution path

Check whether each environment variable is supplied without printing its value:

1. **Both `WEKNORA_BASE_URL` and `WEKNORA_API_KEY` supplied:** use the independent REST/script path; `arks` is not required. Empty or invalid values are a configuration error. The URL is already the `/api/v1` root, for example `https://weknora.example.com/api/v1`; preserve deployment prefixes and legitimate private HTTP, and never append `/api/v1` again.
2. **Neither supplied:** for connection verification, knowledge-base list/detail, or single-base search, read [managed execution](references/managed.md). Use `arks` only when it is available and the connection is configured. For other operations, explain that independent environment credentials are needed; a stored key is not exported to complete them.
3. **Only one supplied:** stop and ask the human to complete the pair in their own terminal. Never fill the missing half from managed storage or switch paths after a request fails.

Never request a key in chat, pass its literal value as a command argument, or write ad-hoc key files/shell profiles. Managed storage is allowed only through human-controlled `arks setup weknora`. The Skill never reads private ArkSpace configuration or credential files. Missing CLI does not authorize installation; offer manual environment configuration instead.

Obtain consent before probing the independent key once with `GET /auth/me`. A `403` may mean capability/scope denial or a route with no API-key policy; it is not proof that the key is missing or invalid. Follow [errors](references/errors.md), with no automatic connection fallback.

Independent requests refer to the key only as an environment expansion, never as a literal:

```bash
curl -sS "$WEKNORA_BASE_URL/knowledge-bases?page=1&page_size=20" \
  -H "X-API-Key: $WEKNORA_API_KEY"
```

## Preflight

Two checks are mandatory. Skipping them is the usual cause of a confidently wrong answer.

**Before any retrieval**, read the knowledge base and its computed capability flags:

```text
GET /knowledge-bases/:id  →  capabilities: { vector, keyword, wiki, graph, faq }
```

A knowledge base with its retrieval indexes off searches empty **without erroring**. Report that the knowledge base has no usable index rather than reporting "no results". `faq` is true only for a FAQ-type knowledge base.

**Before treating any entry as searchable**, read it and require both fields:

```text
GET /knowledge/:id  →  parse_status == "completed"  AND  enable_status == "enabled"
```

`draft`, `pending`, `processing`, and `finalizing` are not searchable yet. An entry created without `status: "publish"` stays `draft` forever — see [Pitfalls](references/pitfalls.md).

Search and list payloads may carry `data: null` as well as `data: []`. Both mean empty. Do not treat `null` as malformed or retry it.

## Route

Load exactly the reference matching the requested outcome:

- Importing files, URLs, or Markdown; assigning tags or metadata; writing a short summary: [Ingest](references/ingest.md)
- Supported retrieval using an optional managed connection: [Managed execution](references/managed.md)
- Independent REST endpoints or their required capability: [Endpoints](references/endpoints.md)
- A question over a knowledge base that returns a streamed answer: [SSE chat](references/sse.md)
- A non-2xx response, an unexpected `data` shape, or `403`: [Errors and pagination](references/errors.md)
- An import that never becomes searchable, or a surprising field name: [Pitfalls](references/pitfalls.md)

Do not guess a route from a REST convention. Chunks live at `/chunks/:knowledge_id`, **not** under `/knowledge/:id`. Every route outside [Endpoints](references/endpoints.md) is out of scope for this Skill.

## Workflows

### Import a document — return after writing by default

1. Identify and confirm the target knowledge base. Read [Ingest](references/ingest.md) before constructing requests.
2. Read existing tags; reuse 1–3 clearly relevant tags, or automatically create 1–3 content-backed topic tags if none fit. Import consent covers this limited creation; follow Ingest without a separate approval prompt. Prepare source-backed custom metadata and a short summary when the source text is available.
3. Choose the route by source: for Markdown content (including a document drafted in the conversation or a supplied `.md` file), prefer creating a manual document with `POST /knowledge-bases/:id/knowledge/manual`; use the file endpoint for other local file formats, and the URL endpoint for web sources. Honor an explicit request to preserve/upload the original Markdown file. Read [Ingest](references/ingest.md) for request shapes.
4. Apply `tag_ids` using the selected route; for manual Markdown send `status: "publish"`. Preserve Wiki, graph, and other processing settings. A `409` returns an existing entry: report it without re-uploading or modifying it automatically.
5. Using the new entry ID, save metadata and, when supported and prepared, the short summary. These writes do **not** require parsing to finish. Read the entry once to verify selected tag IDs and other saved fields, and capture current status; missing tags mean decoration incomplete, not a fully tagged import.

6. Return the ID, knowledge base, saved tags/metadata, summary strategy, and observed `parse_status`. Report background processing as pending, not searchable. Do not poll or wait for Wiki, graph, or parsing on an ordinary import; partial decoration failures do not justify re-uploading.

For an explicit verification request or import-and-answer task, poll `GET /knowledge/:id` within an agreed time budget, requiring `parse_status == "completed"` and `enable_status == "enabled"`. On `failed`, report the failure. On deadline or cancellation, return the ID and last observed status; leave processing running unless cancellation was requested. `finalizing` can include long-running enhancement tasks and is not by itself a stall.

### Answer a question over a knowledge base

1. Run both preflight checks. If either fails, report that and stop.
2. Create a session with `POST /sessions`, then stream with `POST /knowledge-chat/:session_id` or `POST /agent-chat/:session_id`.
3. Assemble the answer from `answer` deltas and terminate on `complete` or `error`. Read [SSE chat](references/sse.md) before writing this consumer; the protocol has non-obvious rules.
4. Prefer `scripts/consume-sse.mjs` over hand-rolled parsing:

   ```bash
   node scripts/consume-sse.mjs --session <session_id> --query "…"
   ```

5. Attribute the answer to the documents in `knowledge_references`. A stream that ends without reaching `complete` is an incomplete result, not an answer.

### Search and read

With a managed connection, use the operations in [managed execution](references/managed.md); search performs knowledge-base capability preflight. Document/chunk reads and multi-base search still use the independent environment path. With an independent connection:

- One knowledge base: `POST /knowledge-bases/:id/hybrid-search` (POST is the documented form; `GET` exists only for backwards compatibility).
- Several knowledge bases: `POST /knowledge-search`.
- Read one document: `GET /knowledge/:id`. List documents: `GET /knowledge-bases/:id/knowledge`. Read its chunks: `GET /chunks/:knowledge_id`.

### Inspect or fix parsing

1. Read chunks with `GET /chunks/:knowledge_id` to see what was actually indexed, and with `GET /chunks/by-id/:id` for one chunk.
2. Use `PUT /chunks/:knowledge_id/:id` to correct a chunk; revisions are available at `GET /chunks/:knowledge_id/:id/revisions` and `POST /chunks/:knowledge_id/:id/revert`.
3. Re-run parsing with `POST /knowledge/:id/reparse` after changing process configuration. `POST /knowledge/:id/cancel-parse` stops a parse in flight.

### Validate chunking without writing

`POST /chunker/preview` returns the split a document would produce and writes nothing. Use it when the user wants to tune chunking, or when you need to check a document's shape. Prefer it over creating a throwaway knowledge base or entry.

## Safety

- **Never create a knowledge base or a knowledge entry for testing.** Validation goes through `POST /chunker/preview`. Creating content in a user's instance changes their data.
- **Confirm before every irreversible or billable call.** These include all `DELETE` routes, `POST /knowledge/batch-delete`, `POST /knowledge/batch-reparse`, `POST /knowledge/move`, chunk delete and revert, `DELETE /knowledge/:id` (which removes chunks), and session deletes. Name the exact resource and state that it cannot be undone, then wait for confirmation.
- **Tell the user that content leaves their environment.** Uploaded files, submitted URLs, and chat queries are sent to the WeKnora instance and may reach a configured model Provider. Say so before the first call that sends content.
- **Respect the key's scope.** A scoped key is limited to a capability set and often to a knowledge-base allow-list; a call outside it returns `403`. A batch operation touching one out-of-list knowledge base is rejected as a whole, with no partial application. On `403`, report the likely scope mismatch and ask the user to inspect the key; never retry in a loop or broaden the request to work around it.
- **A knowledge-base-scoped key cannot use `?resource_urls=public`** and cannot use the `/files` proxy. Such a key stays in the default `handle` mode; resolve `resource://` handles through the knowledge-base-scoped route instead.
- Never write to, edit, or remove this Skill's own files, or the user's agent configuration, without permission.

## Result handling

- Read the single JSON body. Treat `success: false` as failure and branch on the HTTP status and the numeric `error.code`; see [Errors and pagination](references/errors.md) for the two error shapes.
- Never paste a raw envelope, a session dump, or an entire chunk listing into the conversation. Answer the question, cite the documents, or write the requested artifact.
- Quote a citation as the source document plus knowledge base. WeKnora's `knowledge_references` identify documents, not passage offsets — do not imply passage-level grounding the API did not return.
- On an ingest, distinguish **written**, **decoration incomplete**, and **searchable**. Report the observed `parse_status`, not an invented terminal status. A successful write does not prove searchable content.
