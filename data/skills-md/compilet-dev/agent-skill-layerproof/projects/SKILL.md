---
name: projects
description: Public API project management (X-API-KEY). Create, list, get, update, delete, clone, vote projects. Supports cursor pagination. Types follow PublicApiProjectController (/api/v2/projects).
---

# Skill: Projects Management

## Description

Manage Layerproof projects (create, list, get, update, delete, clone, vote). This skill documents the **public API** at `/api/v2/projects` (PublicApiProjectController). Authenticate with `X-API-KEY` header. List uses cursor pagination via `limit` and `cursor` query params.

---

## Requirements

Environment variables:

- `LAYERPROOF_BASE_URL`
- `LAYERPROOF_API_KEY`

All requests must include:

- `X-API-KEY: $LAYERPROOF_API_KEY`

---

## TypeScript types (request / response)

Mirrors `PublicApiProjectController` data classes.

```typescript
// --- Create (POST) — 201 ---
type PublicApiCreateProjectRequest = {
  name: string;                   // required, 1–255 chars
  description?: string | null;    // max 10000 chars
  status?: string | null;         // e.g. "DRAFT"; defaults to DRAFT if omitted
  tags?: string[] | null;
  metadata?: Record<string, any> | null;
  project_kind?: "SLIDE_DECK" | "GENERIC" | "MINDMAP" | "THEME" | "BLOG_POST" | "SOCIAL_CAMPAIGN";  // default: SLIDE_DECK
  workspace_id?: string | null;   // UUID
  theme_id?: string | null;       // UUID; optional theme for slide deck
  aspect_ratio?: string | null;   // e.g. "16:9"
};

// --- Update (PUT) ---
type PublicApiUpdateProjectRequest = {
  name?: string | null;           // 1–255 chars
  description?: string | null;    // max 10000 chars
  status?: string | null;
  tags?: string[] | null;
  metadata?: Record<string, any> | null;
  workspace_id?: string | null;   // UUID
  is_public?: boolean | null;
};

// --- Clone (POST /{projectId}/clone) — 201 ---
type CloneProjectRequest = {
  name?: string | null;           // defaults to "Copy of <source name>"
  workspace_id?: string | null;   // UUID; if null, auto-creates hidden workspace
};

// --- Project response ---
type PublicApiProjectResponse = {
  id: string;
  name: string;
  description: string | null;
  status: string;                 // e.g. "ACTIVE", "DRAFT"
  project_kind: string;           // e.g. "SLIDE_DECK"
  metadata: Record<string, any>;
  slide_deck_id: string | null;
  workspace_id?: string | null;   // UUID
  thumbnail_url?: string | null;  // optional preview image URL
  slide_deck_type?: string | null;  // e.g. "PRESENTATION", "SOCIAL_POST", "WEBPAGE", "VIDEO"
  tags: string[];
  created_at: string;             // ISO 8601
  updated_at: string;             // ISO 8601
  is_public: boolean;
  vote_count: number;
  has_voted?: boolean | null;
};

// --- List response (cursor-paginated) ---
type PublicApiProjectListResponse = {
  data: PublicApiProjectResponse[];
  next_cursor: string | null;     // pass as `cursor` param for next page
  has_more: boolean;
};
```

---

## List Projects

Query params: `limit` (default 20, max 100), `cursor` (from previous `next_cursor`).

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/projects?limit=20" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

Example JSON response:

```json
{"data":[{"id":"2b12d232-eca6-4161-96df-9f954fbbb36f","name":"Exit Strategy Overview","description":"...","status":"ACTIVE","project_kind":"SLIDE_DECK","metadata":{},"slide_deck_id":"ab2c64a5-0b59-45ec-baef-1d5b68dbf5fe","created_at":"2026-03-09T03:15:51.548959Z","updated_at":"2026-03-09T03:16:17.069810Z","is_public":false,"vote_count":0,"has_voted":null}],"next_cursor":null,"has_more":false}
```

---

## Get Project

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

Example JSON response:

```json
{"id":"2b12d232-eca6-4161-96df-9f954fbbb36f","name":"Exit Strategy Overview","description":"...","status":"ACTIVE","project_kind":"SLIDE_DECK","metadata":{"original_prompt":"Create an exit strategy overview"},"slide_deck_id":"ab2c64a5-0b59-45ec-baef-1d5b68dbf5fe","created_at":"2026-03-09T03:15:51.548959Z","updated_at":"2026-03-09T03:16:17.069810Z","is_public":false,"vote_count":0,"has_voted":false}
```

---

## Create Project

Request body: `PublicApiCreateProjectRequest`. Response (201): `PublicApiProjectResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{
    "name": "<project_name>",
    "description": "<description>",
    "project_kind": "SLIDE_DECK"
  }'
```

Example JSON response:

```json
{"id":"68f8270f-f36a-4817-8d0b-2c05efcd1c9a","name":"tmp-skill-project","description":"tmp","status":"DRAFT","project_kind":"SLIDE_DECK","metadata":{},"slide_deck_id":"a877d0c0-9514-40cc-8d27-cee3a1e73934","created_at":"2026-03-10T07:07:46.211172Z","updated_at":"2026-03-10T07:07:46.211176Z","is_public":false,"vote_count":0,"has_voted":null}
```

---

## Update Project

Request body: `PublicApiUpdateProjectRequest`. Only provided fields are updated. Response: `PublicApiProjectResponse`.

```bash
curl -X PUT "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"name":"<new_name>","description":"<new_description>","is_public":true}'
```

---

## Delete Project

Soft-deletes the project and all associated resources. Response: 204 No Content.

```bash
curl -X DELETE "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## List Public Projects

Query params: `limit` (default 20, max 100), `cursor`, `slide_deck_type` (one of `PRESENTATION`, `SOCIAL_POST`, `WEBPAGE`, `VIDEO`; optional).

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/projects/public?limit=20" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Vote for a Project

Records a vote on a public project. Response: 204 No Content.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/vote" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Remove Vote from a Project

Removes a vote from a public project. Response: 204 No Content.

```bash
curl -X DELETE "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/vote" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Clone Project

Clones an owned or public project into a new private project. Request body: `CloneProjectRequest`. Response (201): `PublicApiProjectResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/clone" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"name":"<cloned_project_name>","workspace_id":"<workspace_id>"}'
```

---

## Agent behavior

When the user asks to manage projects, do the following.

### 1. Choose the right endpoint

| User intent | Endpoint | Method |
|-------------|----------|--------|
| List own projects | `/api/v2/projects?limit=20` | GET |
| Get project by ID | `/api/v2/projects/{projectId}` | GET |
| Create project | `/api/v2/projects` | POST |
| Update project | `/api/v2/projects/{projectId}` | PUT |
| Delete project | `/api/v2/projects/{projectId}` | DELETE |
| List public projects | `/api/v2/projects/public?limit=20` | GET |
| Vote for a project | `/api/v2/projects/{projectId}/vote` | POST |
| Remove vote | `/api/v2/projects/{projectId}/vote` | DELETE |
| Clone a project | `/api/v2/projects/{projectId}/clone` | POST |

### 2. Build and run the request

- **Auth**: Include `X-API-KEY: $LAYERPROOF_API_KEY`. Read `LAYERPROOF_BASE_URL` and `LAYERPROOF_API_KEY` from the environment; if missing, tell the user to set them.
- **GET list**: Use `limit` (default 20, max 100) and `cursor` for pagination. Pass `next_cursor` from a previous response as `cursor` to fetch the next page.
- **POST/PUT**: Build JSON body from the appropriate request type. Run curl and show result.
- **DELETE project / vote**: Build path; run curl. Response is 204 with no body.

### 3. Response handling

- Always show the **raw JSON response** in a JSON code block.
- For 204 responses, indicate success and no body.
- On error, show the response body and status code.

### 4. Example workflows

**Workflow A — User**: "Create a project called Q3 Roadmap."

1. Choose POST `/api/v2/projects`.
2. Body: `{"name":"Q3 Roadmap","project_kind":"SLIDE_DECK"}`.
3. Run curl; show JSON. The returned `id` is the project ID; `slide_deck_id` is the associated slide deck.

**Workflow B — User**: "Create a slide deck project in workspace W, then generate an outline for it."

1. Resolve `workspace_id` (e.g. from GET workspaces or user). POST `/api/v2/projects` with `{"name":"...", "project_kind":"SLIDE_DECK", "workspace_id":"<workspace_id>"}`; capture `id` and `slide_deck_id`.
2. Hand off to slide-decks skill: use `projectId = id` and `slideDeckId = slide_deck_id`; POST `.../projects/{projectId}/slide-deck/{slideDeckId}/outline/generate` with prompt and slide_count; poll jobs; get deck or update outline as needed.

**Workflow C — User**: "List my projects, find the one named 'Launch Deck', export it as PPTX, and if there’s a clone or vote option show me how."

1. GET `/api/v2/projects` with `limit` and optional `cursor`; paginate if needed. Locate project where `name` matches "Launch Deck"; capture `id`.
2. Hand off to exports skill: POST `.../projects/{id}/exports/pptx`; poll GET `.../exports/{exportId}` until COMPLETED; show `downloadUrl`.
3. Optionally: POST `.../projects/{id}/clone` to clone, or POST/DELETE `.../projects/{id}/vote` per API; show response and explain usage.

---

## Response format (required)

- (if response contains url to show image) please show image and show json response instead of table
- Always show the **raw JSON response** (verbatim) in a JSON code block.
- If the response contains a URL for an image, **render/show the image** and also show the **JSON response** (do not convert to a table).
