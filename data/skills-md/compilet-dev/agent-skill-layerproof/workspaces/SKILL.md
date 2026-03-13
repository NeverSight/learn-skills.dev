---
name: workspaces
description: Public API workspace management (X-API-KEY). Create, list, get, update, delete workspaces. Types follow PublicApiWorkspaceController (/api/v2/workspaces).
---

# Skill: Workspace Management

## Description

Manage workspaces. This skill documents the **public API** at `/api/v2/workspaces` (PublicApiWorkspaceController). Authenticate with `X-API-KEY` header. List supports pagination with `page` and `page_size` (default 20, max 100).

---

## TypeScript types (request / response)

Mirrors `PublicApiWorkspaceController` data classes.

```typescript
// --- Create (POST) — 201 ---
type PublicApiCreateWorkspaceRequest = {
  name: string;           // required, 1–255 chars
  description?: string | null;
  default_theme_id?: string | null;  // optional theme UUID
};
type PublicApiWorkspaceResponse = {
  id: string;
  user_id: string;
  name: string;
  description: string | null;
  default_theme_id: string | null;
  shared_working_dir_live_object_id: string;
  project_count: number;
  created_at: string;     // ISO 8601
  updated_at: string;    // ISO 8601
  thumbnail_url?: string | null;
};

// --- List (GET) ---
// Query: page (default 20), page_size (default 20, max 100)
type PublicApiWorkspaceListResponse = {
  data: PublicApiWorkspaceResponse[];
  total: number;
  page: number;
  page_size: number;
};

// --- Update (PUT) ---
type PublicApiUpdateWorkspaceRequest = {
  name?: string | null;   // max 255 if provided
  description?: string | null;
  default_theme_id?: string | null;  // optional theme UUID
};
```

---

## Create Workspace

Request body: `PublicApiCreateWorkspaceRequest`. Response (201): `PublicApiWorkspaceResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/workspaces" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"name":"<workspace_name>","description":"<description>"}'
```

---

## List Workspaces

Query: `page` (default 20), `page_size` (default 20, max 100). Response: `PublicApiWorkspaceListResponse`.

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/workspaces?page=0&page_size=20" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Get Workspace

Response: `PublicApiWorkspaceResponse`.

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/workspaces/<workspace_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Update Workspace

Request body: `PublicApiUpdateWorkspaceRequest`. Response: `PublicApiWorkspaceResponse`.

```bash
curl -X PUT "$LAYERPROOF_BASE_URL/api/v2/workspaces/<workspace_id>" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"name":"New name","description":"New description"}'
```

---

## Delete Workspace

Response: 204 No Content.

```bash
curl -X DELETE "$LAYERPROOF_BASE_URL/api/v2/workspaces/<workspace_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Agent behavior

When the user asks to manage workspaces (create, list, get, update, delete), do the following.

### 1. Choose the right endpoint

| User intent | Endpoint | Method |
|-------------|----------|--------|
| Create workspace | `/api/v2/workspaces` | POST |
| List workspaces | `/api/v2/workspaces?page=0&page_size=20` | GET |
| Get workspace by ID | `/api/v2/workspaces/{workspaceId}` | GET |
| Update workspace | `/api/v2/workspaces/{workspaceId}` | PUT |
| Delete workspace | `/api/v2/workspaces/{workspaceId}` | DELETE |

### 2. Build and run

- **Auth**: Include `X-API-KEY: $LAYERPROOF_API_KEY`. Read `LAYERPROOF_BASE_URL` and `LAYERPROOF_API_KEY` from the environment; if missing, tell the user to set them.
- **GET**: Build path and query params (`page`, `page_size` for list). Run curl and show result.
- **POST/PUT**: Build JSON body (name, description for create; name/description optional for update). Run curl and show result.
- **DELETE**: Build path; run curl. Response is 204 with no body.

### 3. Response handling

- Always show the **raw JSON response** in a JSON code block.
- For 204 delete, indicate success and no body.
- On error, show response body and status code.

### 4. Example workflows

**Workflow A — User**: "Create workspace Marketing."

1. Choose POST /api/v2/workspaces.
2. Body: `{"name":"Marketing"}` (or with description).
3. Run curl; show JSON. Returned `id` is the workspace ID for get/update/delete.

**Workflow B — User**: "Set up a workspace for Q2, create it if it doesn’t exist, then list my workspaces and show the one I’ll use for new projects."

1. GET `/api/v2/workspaces` with `page`, `page_size`; inspect list for a workspace named "Q2" or similar.
2. If not found: POST `/api/v2/workspaces` with `{"name":"Q2","description":"Q2 campaigns and decks"}`; capture `id` as `workspace_id`.
3. If found: use that workspace’s `id`. Optionally GET `/api/v2/workspaces/{id}` to show full details.
4. Tell user: "Use workspace_id <id> when creating projects (e.g. POST /api/v2/projects with workspace_id in body)."

**Workflow C — User**: "Rename workspace X to 'Marketing 2025' and add a description."

1. Resolve workspace ID (from list or user). PUT `/api/v2/workspaces/{workspaceId}` with `{"name":"Marketing 2025","description":"..."}`.
2. Run curl; show JSON. Optionally GET the workspace again to confirm name and description.

---

## Response format (required)

- (if response contains url to show image) please show image and show json response instead of table
- Always show the **raw JSON response** (verbatim) in a JSON code block.
- If the response contains a URL for an image, **render/show the image** and also show the **JSON response** (do not convert to a table).
