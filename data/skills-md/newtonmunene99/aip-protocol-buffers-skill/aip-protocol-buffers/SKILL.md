---
name: aip-protocol-buffers
description: Summarizes Google AIPs for designing and working with protocol buffers, RPCs, services, messages, fields, and naming. Use when authoring or reviewing .proto files, designing resource-oriented APIs, aligning with google.aip.dev and the API Linter, or checking naming and request/response patterns for standard methods.
---

# AIP Protocol Buffers & API Design Skill

This skill summarizes **Google API Improvement Proposals (AIPs)** for designing
and working with protocol buffers, RPCs, services, messages, fields, and
naming for APIs that follow [resource-oriented design](https://google.aip.dev/121).

**Scope:** General AIP guidance from the
[google.aip.dev](https://google.aip.dev/) codebase (AIPs in approved state).
Domain-specific AIPs (Cloud, Firebase, Auth, etc.) may add further rules.

## Bundled references

- **[references/full-example.md](references/full-example.md):** Read when implementing a new service or checking request/response shape for standard methods.
- **[references/naming-and-methods.md](references/naming-and-methods.md):** Read when checking naming conventions or RPC/method patterns for standard methods.

---

## 1. Protocol Buffers (Protos)

### 1.1 Package and file structure

- **Package:** Each API **must** live in a single package that **ends in a
  major version** (e.g. `google.library.v1`). Directory layout **must** match
  the package (e.g. `google/library/v1`).
- **Syntax:** Use `proto3` only.
- **File names:** Use `snake_case`. Avoid language keywords (e.g. not
  `import.proto`). **Must not** use the version as the filename (e.g. no
  `v1.proto`).
- **File layout order:** Syntax → package → imports (alphabetical) → file
  options → services (standard methods before custom, grouped by resource) →
  resource messages (parent before child) → request/response messages (matching
  RPC order, request before response) → other messages → top-level enums.

### 1.2 API-specific vs common protos

- **API-specific protos** belong in the versioned package (e.g.
  `google.library.v1`). Do **not** create shared "API-specific common" packages
  across versions; duplicate the proto per version if needed.
- **Cross-API references:** Use **resource names** (strings), not the resource
  message type from another API.
- **Common components:** APIs **may** import:
  - `google.api.*` (not subpackages)
  - `google.longrunning.Operation`
  - `google.protobuf.*` (e.g. `Timestamp`, `Duration`, `Struct`, `FieldMask`,
    `Empty`)
  - `google.rpc.*`
  - `google.type.*` (e.g. `Date`, `Money`, `LatLng`, `PostalAddress`,
    `TimeOfDay`)
  - `google.iam.v1.*` where relevant
- **Organization-specific common packages** must end with `.type` (e.g.
  `google.geo.type`), be published in the googleapis repo, and follow AIP-213;
  do **not** put generic types there.

---

## 2. Services (interfaces)

- **Interface name:** Use an intuitive **noun** in PascalCase (e.g. `Library`,
  `Calendar`, `BlobStore`). Avoid names that clash with common language/runtime
  concepts (e.g. `File`). If needed, add a suffix like `Api` or `Service` to
  disambiguate.
- **Methods:** Prefer **standard methods** (Get, List, Create, Update, Delete)
  over custom methods. Group RPCs by resource; list standard methods before
  custom ones.

---

## 3. Resources and resource names

### 3.1 Resource-oriented design

- Model the API as a **resource hierarchy**: resources (nouns) and collections;
  use a small set of **standard methods** plus **custom methods** when
  necessary.
- Each resource **must** support **Get**. All
  non-[singleton](https://google.aip.dev/156) resources **must** support
  **List**.
- Resource schema (message shape) for a given resource **must** be the same
  across all methods that take or return that resource.
- Relationships must form a **directed acyclic graph**; each resource has **at
  most one canonical parent**. Use `parent` for collection scope and optional
  `filter` for other associations (AIP-124, AIP-160).

### 3.2 Resource names

- **Format:** Path-like, without leading slash:
  `publishers/123/books/les-miserables`. Use `/` only as segment separator;
  **no `/` inside** a segment.
- **Segments:** Alternate **collection identifiers** (plural, camelCase, e.g.
  `publishers`, `books`) and **resource ID** segments. Collection IDs must be
  unique within a single resource name (no `people/xyz/people/abc`).
- **Characters:** Prefer DNS-safe (RFC 1123); avoid uppercase in IDs; avoid
  URL-encoding; if Unicode is needed, use NFC (AIP-210).
- **User-specified IDs:** Document format; prefer lowercase letters, numbers,
  hyphen; first character letter, last letter or number; max 63 chars (RFC 1034
  style). Duplicate name → `ALREADY_EXISTS` (or `PERMISSION_DENIED` if user
  cannot see the duplicate).
- **Full resource name** (cross-API): schemeless URI with service name +
  relative name, e.g.
  `//library.googleapis.com/publishers/123/books/les-miserables`.

### 3.3 Resource types and annotations

- **Resource type:** `{ServiceName}/{Type}` (e.g.
  `library.googleapis.com/Book`). Type must match the message name, singular,
  PascalCase, alphanumeric.
- **Annotation:** Use `google.api.resource` with `type`, `pattern`, `singular`,
  `plural`. Pattern variables: **snake_case**, no `_id` suffix, unique within
  pattern. Pattern variables match singular resource type (e.g. `{topic}` for
  Topic).
- **Nested collections:** Child collection segment may drop redundant prefix
  (e.g. `users/{user}/events/{event}` instead of `userEvents` in path);
  message/type name stays e.g. `UserEvent`; `singular`/`plural` not shortened.

### 3.4 Fields for resource names

- **On the resource message:** First field **should** be `string name` with
  resource name; annotate with `(google.api.field_behavior) = IDENTIFIER` and
  `google.api.resource`.
- **In request messages (acting on one resource):** Use `string name` for the
  resource; annotate with `REQUIRED` and `google.api.resource_reference`
  (`type` or `child_type`). Comment **should** document the pattern (e.g.
  `Format: publishers/{publisher}/books/{book}`).
- **In request messages (collection scope):** Use `string parent` for the
  collection's parent resource; same annotations and pattern comment.
- **Referencing another resource:** Prefer `string` with resource name; field
  name ≈ referenced type in snake_case (e.g. `shelf`); use
  `google.api.resource_reference`. Do **not** embed the other resource's
  message type (except internal/revisions cases in AIP-162). Use `_name` suffix
  only if needed to avoid ambiguity (e.g. `crypto_key_name`).
- **Reserved:** Use `name` only for resource name; use `parent` only for parent
  collection. For other concepts use a different name or adjective (e.g.
  `display_name`).

---

## 4. RPCs (methods)

### 4.1 HTTP and transcoding

- Every RPC **must** have an HTTP mapping via `google.api.http` (except
  bi-directional streaming, which should have a non-streaming alternative if
  possible).
- **Verbs:** Use `get`, `post`, `patch`, or `delete` as prescribed; **should
  not** use `put` or `custom`.
- **URI:** Use `{field=path/*}` for variables; use `*` for one segment (no
  `/`), `**` only if needed for path segments. For Update, use nested field in
  path (e.g. `{book.name=...}`).
- **Body:** No `body` for GET/DELETE. For Create/Update, `body` must point to
  the resource field; must not be nested, a URI param, or repeated. Prefer not
  using `json_name` except for compatibility.
- **Method signatures:** Use `google.api.method_signature` as specified per
  method type below.

### 4.2 Standard methods

See [references/naming-and-methods.md](references/naming-and-methods.md) for the standard-methods table.

- **Get:** Request has `name` (required, resource reference). URI single
  variable for resource; `method_signature = "name"`. Response is the resource
  (fully populated unless partial response per AIP-157).
- **List:** Request has `parent` (required when not top-level), `page_size`
  (int32), `page_token` (string); optional `filter`, `order_by`. Response has
  repeated resource field + `next_page_token`; optional `total_size`.
  Pagination is mandatory from the start (AIP-158).
  `method_signature = "parent"` (or `""` for top-level).
- **Create:** Request has `parent`, `{resource}_id`, and resource field (body).
  Resource `name` ignored on input. `method_signature = "parent,book,book_id"`
  (or without `_id` if optional). Management plane **must** allow
  user-specified ID; data plane **should**.
- **Update:** Request has resource field (with `name`) +
  `google.protobuf.FieldMask update_mask`. URI uses `{resource.name=...}`.
  Support partial update (PATCH). Omitted mask = all populated fields. Support
  `*` for full replacement with documented caveats. State fields **must not**
  be writable in Update (use custom methods). Optional `allow_missing` for
  upsert when using client-assigned names.
- **Delete:** Request has `name`. Optional `force` for cascading delete;
  optional `etag` for conditional delete; optional `allow_missing` for no-op
  when missing. Child resources present without `force` →
  `FAILED_PRECONDITION`.

### 4.3 Custom methods

- Use only when standard methods do not fit; prefer standard methods.
- **Name:** Verb + noun, UpperCamelCase (e.g. `ArchiveBook`). **Must not**
  include prepositions or "Async"; **may** use `LongRunning` suffix. **Should
  not** reuse standard verbs (Get, List, Create, Update, Delete).
- **HTTP:** GET for read-only; POST for side effects. URI must include
  `:customVerb` in camelCase (e.g. `:archive`).
- **Body:** Prefer `body: "*"`.
- **Request/response:** `{RpcName}Request` and `{RpcName}Response` (or return
  the resource when operating on one resource).
- **Resource-based:** Single resource → `name` in path. Collection-based →
  `parent` in path + literal collection segment. Stateless → scope field (e.g.
  `project`) in path; verb after `:` (e.g. `:translateText`).

### 4.4 Long-running operations (LRO)

- For operations that take significant time, return
  `google.longrunning.Operation` with `google.longrunning.operation_info`
  (`response_type`, `metadata_type`). Implement the standard Operations
  service; do not define a custom LRO interface.

---

## 5. Messages

- **Names:** Short, PascalCase; no prepositions (e.g. "With", "For"). Omit
  redundant adjectives if there is no contrasting type.
- **Request/response:** Request = RPC name + `Request`; response = resource for
  Get/Create/Update (and some custom), or `ListXResponse` for List, or
  `XResponse` for custom. Response usually holds the full resource unless
  partial response (AIP-157).
- **Conflict:** A message **should not** have a field with the same name as the
  message (after case normalization).

---

## 6. Fields

### 6.1 Field names (AIP-140)

- **Case:** `lower_snake_case` in proto. No leading/trailing/adjacent
  underscores; no word starting with a number.
- **Language:** Correct American English; same concept = same name across APIs;
  avoid overloaded or overly generic names (e.g. "instance", "info", "service"
  only with clear context).
- **Repeated:** Use plural (`books`); non-repeated use singular (`book`).
  Resource names in field names use singular.
- **Prepositions:** Avoid ("for", "with", "at", "by"); e.g. `error_reason` not
  `reason_for_error`. "Per" is allowed in units (AIP-141).
- **Abbreviations:** Use common ones: `config`, `id`, `info`, `spec`, `stats`;
  for units use common abbreviations (e.g. `_km`, `_px`).
- **Adjective + noun:** Adjective before noun: `collected_items` not
  `items_collected`.
- **Verbs:** Field names **must not** be verbs or intent/action; use nouns
  (current or desired value).
- **Booleans:** Omit `is_` prefix: `disabled` not `is_disabled` (exception:
  reserved words, e.g. `is_new`).
- **URIs:** Prefer `uri`; if only URLs, use `url`. Optional prefix (e.g.
  `image_url`).
- **Display:** Human-readable name → `display_name` (no uniqueness).
  Formal/official name → `title` (no uniqueness).
- **Reserved words:** Avoid names that conflict with common language keywords.

### 6.2 Field behavior (AIP-203)

- **Must** apply `google.api.field_behavior` on every field of messages used in
  requests. Use at least one of: `REQUIRED`, `OPTIONAL`, `OUTPUT_ONLY`. Never
  use `FIELD_BEHAVIOR_UNSPECIFIED`.
- **IDENTIFIER:** Only on the resource's `name` field (identifies resource; not
  input on Create; immutable on Update).
- **REQUIRED / OPTIONAL:** For input fields; required = must be present and
  non-empty where applicable.
- **OUTPUT_ONLY:** Response-only; server clears on input; ignore in
  update_mask.
- **INPUT_ONLY:** Request-only; not in response (rare; e.g. some TTL patterns).
- **IMMUTABLE:** Cannot be changed after creation; ignore if unchanged on
  update, error if change requested.
- **UNORDERED_LIST:** Repeated field order not guaranteed.

### 6.3 Standard and special fields

- **Timestamps:** Use `google.protobuf.Timestamp`; names end in `_time` (e.g.
  `create_time`, `update_time`). Use imperative form: `publish_time` not
  `published_time` (AIP-142).
- **Durations:** Use `google.protobuf.Duration`; e.g. `flight_duration`
  (AIP-142).
- **State:** Use enum `State` (or `XxxState`) nested in the resource; values
  like `ACTIVE`, `SUCCEEDED`, `FAILED`, `CREATING`, `DELETING`. Field
  **should** be output-only; state changes via custom methods, not Update
  (AIP-216).
- **Enums:** Values in `UPPER_SNAKE_CASE`; first value `{Enum}_UNSPECIFIED` (or
  `UNKNOWN` if zero). Nested in message when used only there (AIP-126).
- **Quantities:** Include unit suffix (e.g. `distance_km`, `node_count`); use
  `_count` for counts, not `num_` (AIP-141). No unsigned integers.
- **Etag:** Optional `string etag` for optimistic concurrency; mismatch on
  update/delete → `ABORTED`.
- **Format / FieldInfo:** Use `google.api.field_info` format (e.g. UUID4, IPv4,
  IPv6) only when specified by an AIP; document and compare per spec (AIP-202).

### 6.4 Pagination (List)

- Request: `int32 page_size` (optional; document default and max; coerce over
  max; error on negative), `string page_token`.
- Response: repeated items + `string next_page_token` (set only when there is a
  next page).

---

## 7. Naming summary

See [references/naming-and-methods.md](references/naming-and-methods.md) for the naming summary table.

---

## 8. Errors and documentation

- **Errors:** Return `google.rpc.Status` with `google.rpc.Code`. Include
  `ErrorInfo` in `details` with machine-readable `reason` (UPPER_SNAKE_CASE,
  ≤63 chars). Message: developer-facing, English, brief and actionable; dynamic
  parts in `details`.
- **Comments:** Every message, RPC, and field **should** have a clear comment
  (valid American English). Document resource name patterns (Format: `...`) and
  constraints (e.g. page_size default/max).
- **Precedent violations:** If deviating from AIP guidance, document with
  comment prefixed `aip.dev/not-precedent` and justify per AIP-200.

---

## 9. Best practices (concise)

1. Run the [API Linter](https://github.com/googleapis/api-linter) and fix
   reported issues (or document why a rule is disabled).
2. Keep APIs self-contained: versioned package, resource names for cross-API
   refs, shared types only from approved common packages.
3. Use standard methods and standard request/response shapes; add custom
   methods only when necessary.
4. Annotate all request fields with `field_behavior`; annotate resource and
   reference fields with `google.api.resource` / `resource_reference`.
5. Use consistent vocabulary: same concept → same name; avoid overloaded terms;
   prefer standard fields (`name`, `parent`, `create_time`, `update_time`,
   `display_name`, `etag`, `state`).
6. Design for many clients: CLIs, SDKs, declarative/IaC, UIs; avoid
   special-casing that hurts one client for marginal gain.
7. Preserve backwards compatibility: no breaking changes to field behavior,
   required fields, or resource names within a major version; pagination and
   LRO from day one where applicable.

---

## 10. Example (minimal CRUD resource)

For a full minimal CRUD proto example (service, Book resource, and all request/response messages), see [references/full-example.md](references/full-example.md).

---

## 11. References

- **AIP index:** [google.aip.dev](https://google.aip.dev/)
- **API Linter:**
  [github.com/googleapis/api-linter](https://github.com/googleapis/api-linter)
- **Key AIPs:** 1 (purpose), 8 (style), 121 (resource design), 122 (resource
  names), 123 (resource types), 127 (HTTP transcoding), 131–136 (standard +
  custom methods), 140 (field names), 158 (pagination), 190 (naming), 203
  (field behavior), 213/215 (common/API-specific protos)

When in doubt, open the specific AIP on
[google.aip.dev](https://google.aip.dev/) for full guidance and rationale.
