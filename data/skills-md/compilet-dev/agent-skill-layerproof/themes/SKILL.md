---
name: themes
description: Public API theme management (X-API-KEY). List, get, generate, and apply themes. Types follow PublicThemeController (/api/v2/themes).
---

# Skill: Theme Management

## Description

Themes define visual styling for slides. This skill documents the **public API** at `/api/v2/themes` (PublicThemeController). Authenticate with `X-API-KEY` header.

---

## TypeScript types (request / response)

Mirrors `PublicThemeController` (/api/v2/themes) data classes.

```typescript
// --- List Themes (GET) ---
// Query: offset (default 0), limit (default 20), search (optional)
type PublicThemeListResponse = {
  data: PublicThemeResponse[];
  total: number;
  offset: number;
  limit: number;
};

// --- Get Theme By ID (GET) ---
type PublicThemeResponse = {
  id: string;
  name: string;
  description: string | null;
  visibility: string;       // "PRIVATE" | "SYSTEM" | "SHARED"
  preview_url: string;
  created_at: string;       // ISO 8601
  updated_at: string;      // ISO 8601
};

// --- Generate Theme (POST) — async ---
type PublicGenerateThemeRequest = {
  prompt: string;           // required, 1–5000 chars
  project_id?: string | null;  // optional THEME project UUID; if omitted, a project is created automatically
};
type PublicGenerateThemeResponse = {
  activity_id: string;      // UUID – poll GET /api/v2/jobs/{activity_id}
  theme_id: string;        // UUID
};

// --- Apply Theme (POST) ---
type PublicApplyThemeRequest = {
  slide_deck_id: string;   // UUID, required
  theme_id: string;        // UUID, required
  regenerate_slides?: boolean;  // default false; if true, triggers batch image regeneration – poll activity_id
};
type PublicApplyThemeResponse = {
  theme_id: string;
  theme_name: string;
  slide_deck_id: string;
  applied: boolean;        // true when applied successfully
  activity_id: string | null;  // set when regenerate_slides is true – poll GET /api/v2/jobs/{activity_id}
};
```

---

## List Themes

Query: `offset` (default 0), `limit` (default 20), `search` (optional). Response: `PublicThemeListResponse`.

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/themes?offset=0&limit=20" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Get Theme By ID

Response: `PublicThemeResponse`.

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/themes/<theme_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Generate Theme

Request body: `PublicGenerateThemeRequest`. Response (202): `PublicGenerateThemeResponse`.

Only `prompt` is required. Optional `project_id` uses an existing THEME project; if omitted, one is created automatically. Poll `GET /api/v2/jobs/{activityId}` for status.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/themes/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"prompt":"Clean, minimal style with SF Pro"}'
```

With optional `project_id`:

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/themes/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"prompt":"Clean, minimal style","project_id":"<theme_project_uuid>"}'
```

---

## Apply Theme

Request body: `PublicApplyThemeRequest`. Response: `PublicApplyThemeResponse`.

Theme and slide deck are specified in the body. When `regenerate_slides` is true, poll `GET /api/v2/jobs/{activityId}` for batch image regeneration status.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/themes/apply" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"slide_deck_id":"<slide_deck_uuid>","theme_id":"<theme_uuid>"}'
```

With slide regeneration:

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/themes/apply" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"slide_deck_id":"<slide_deck_uuid>","theme_id":"<theme_uuid>","regenerate_slides":true}'
```

---

## Agent behavior

When the user asks to work with themes (list, get, generate, apply), do the following.

### 1. Choose the right endpoint

| User intent | Endpoint | Method |
|-------------|----------|--------|
| List/browse themes, search themes | `/api/v2/themes` | GET |
| Get one theme by ID | `/api/v2/themes/<theme_id>` | GET |
| Create a new theme from a prompt | `/api/v2/themes/generate` | POST |
| Apply a theme to a slide deck | `/api/v2/themes/apply` | POST |

### 2. Build and run the request

- **Auth**: Every request must include `X-API-KEY: $LAYERPROOF_API_KEY`. Read `LAYERPROOF_BASE_URL` and `LAYERPROOF_API_KEY` from the environment; if missing, tell the user to set them.
- **GET**: Build `curl` with the chosen path and query params (`offset`, `limit`, `search` for list). Run the curl and show the result.
- **POST**: Build a JSON body from the user's input (prompt, theme ID, slide deck ID, etc.). Use `-X POST`, `-H "Content-Type: application/json"`, and `-d '...'`. Run the curl and show the result.

### 3. After generate or apply (with regeneration)

- **Generate theme**: Response includes `activity_id` and `theme_id`. Tell the user the theme was started and give `theme_id`. Optionally poll `GET $LAYERPROOF_BASE_URL/api/v2/jobs/<activity_id>` until `status` is `DONE` or `CANCELED`, then report outcome.
- **Apply theme with `regenerate_slides: true`**: Response may include `activity_id`. If present, tell the user regeneration was started and optionally poll `GET .../api/v2/jobs/<activity_id>` for status.

### 4. Response handling

- Always show the **raw JSON response** in a JSON code block; do not convert to a table.
- If the response contains a URL for an image (e.g. `preview_url`), show the image and the JSON.
- On error (4xx/5xx), show the response body and status code; suggest fixing missing/invalid API key, IDs, or request body.

### 5. Example workflows

**Workflow A — User**: "Generate a theme with prompt: minimal dark mode."

1. Choose `POST /api/v2/themes/generate`.
2. Build body: `{"prompt":"minimal dark mode"}`.
3. Run: `curl -X POST "$LAYERPROOF_BASE_URL/api/v2/themes/generate" -H "Content-Type: application/json" -H "X-API-KEY: $LAYERPROOF_API_KEY" -d '{"prompt":"minimal dark mode"}'`.
4. Show the JSON response; if it contains `activity_id`, mention they can poll `/api/v2/jobs/{activityId}` for status and use `theme_id` once done.

**Workflow B — User**: "List themes, generate a new 'corporate blue' theme, wait for it to finish, then apply it to my slide deck and regenerate slides."

1. GET `/api/v2/themes` with optional `limit`, `offset`, `search`; show list. User may pick existing or request new.
2. POST `/api/v2/themes/generate` with `{"prompt":"corporate blue"}`; capture `activity_id` and `theme_id`.
3. Poll `GET /api/v2/jobs/{activity_id}` until status is DONE (or CANCELED). If DONE, theme is ready; if failed, report `failure_reason`.
4. Resolve projectId and slideDeckId (projects + slide-deck). POST or PUT the slide-deck theme/settings endpoint with `theme_id` (e.g. PUT `.../slide-deck/.../settings` with `{"theme_id":"<theme_id>"}`).
5. If the API supports "apply theme and regenerate": use that endpoint with `regenerate_slides: true`; capture `activity_id` and poll jobs until DONE. Otherwise: apply theme then use slide-deck batch-generate; poll that job.

**Workflow C — User**: "I have a theme ID; apply it to deck X and only update the look (no slide regeneration)."

1. Resolve slideDeckId from project. PUT `.../settings` with `{"theme_id":"<theme_id>"}` (or apply-theme without regeneration).
2. Confirm with GET deck; `slide_deck.theme` or similar should reflect the new theme. No job polling needed if no regeneration.

---

## Response format (required)

- (if response contains url to show image) please show image and show json response instead of table
- Always show the **raw JSON response** (verbatim) in a JSON code block.
- If the response contains a URL for an image, **render/show the image** and also show the **JSON response** (do not convert to a table).
