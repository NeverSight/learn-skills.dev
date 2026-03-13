---
name: exports
description: Public API export (X-API-KEY). Export project as PNG ZIP or PPTX (async), get status, cancel. Types follow PublicApiExportController (/api/v2/projects/{projectId}/exports).
---

# Skill: Export Slides

## Description

Export presentations as PNG ZIP or PPTX. This skill documents the **public API** at `/api/v2/projects/{projectId}/exports` (PublicApiExportController). Exports are async: POST returns exportId (activityId); poll GET .../exports/{exportId} for status; when COMPLETED, use downloadUrl (presigned, ~1 hour). Authenticate with `X-API-KEY` header.

---

## TypeScript types (request / response)

Mirrors `PublicApiExportController` data classes.

```typescript
// --- Export PNG / PPTX (POST) — 202 ---
type PublicExportStartedResponse = {
  exportId: string;  // UUID, use to poll status
  status?: string;   // default "PENDING"
};

// --- Get Export Status (GET) ---
type PublicExportProgress = { current: number; total: number };
type PublicExportStatusData = {
  exportId: string;
  status: string;
  format: string;
  downloadUrl?: string | null;
  expiresAt?: string | null;
  fileSizeBytes?: number | null;
  progress?: PublicExportProgress | null;
  errorMessage?: string | null;
};
type PublicExportStatusResponse = { data: PublicExportStatusData };

// --- Cancel Export (POST) ---
type PublicCancelExportResponse = {
  exportId: string;
  status: string;  // "CANCELLED" or "ALREADY_TERMINAL"
};
```

---

## Export PNG ZIP (async)

Response (202): `PublicExportStartedResponse`. Poll GET .../exports/{exportId} for status.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/exports/png" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Export PPTX (async)

Response (202): `PublicExportStartedResponse`. Poll GET .../exports/{exportId} for status.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/exports/pptx" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Get Export Status

Response: `PublicExportStatusResponse`. When status is COMPLETED, `data.downloadUrl` and `data.expiresAt` are set.

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/exports/<export_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Cancel Export

Response: `PublicCancelExportResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/exports/<export_id>/cancel" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Agent behavior

When the user asks to export a project (PNG ZIP or PPTX) or check/cancel an export, do the following.

### 1. Choose the right endpoint

Base path: `/api/v2/projects/{projectId}/exports`. All require `projectId`.

| User intent | Endpoint | Method |
|-------------|----------|--------|
| Export as PNG ZIP | `.../exports/png` | POST |
| Export as PPTX | `.../exports/pptx` | POST |
| Get export status / download URL | `.../exports/{exportId}` | GET |
| Cancel in-progress export | `.../exports/{exportId}/cancel` | POST |

### 2. Build and run

- **Auth**: Include `X-API-KEY: $LAYERPROOF_API_KEY`. Read env vars; if missing, tell the user.
- **Path**: Resolve projectId from context; exportId from the 202 response of export PNG/PPTX.
- Run curl and show the result.

### 3. After starting export

- Response contains `exportId`. Tell the user to poll GET .../exports/{exportId} until status is COMPLETED (or FAILED). When COMPLETED, use `data.downloadUrl` (valid ~1 hour).

### 4. Response handling

- Always show raw JSON in a code block.
- If downloadUrl is present, show the URL and mention the file can be downloaded.
- On 410, download URL expired; suggest triggering a new export.

### 5. Example workflows

**Workflow A — User**: "Export my project as PPTX and give me the download link."

1. Resolve projectId. POST `.../projects/{projectId}/exports/pptx`; capture `exportId` from 202 response.
2. Poll GET `.../projects/{projectId}/exports/{exportId}` until `data.status` is COMPLETED or FAILED. If FAILED, show `data.errorMessage` and suggest retry or checking project/slides.
3. When COMPLETED, show `data.downloadUrl` and `data.expiresAt`; remind user the URL is temporary (~1 hour).

**Workflow B — User**: "Export the same project as both PNG ZIP and PPTX; if one fails, still get the other."

1. POST `.../exports/png`; get `exportId_png`. POST `.../exports/pptx`; get `exportId_pptx`.
2. Poll both: GET `.../exports/{exportId_png}` and GET `.../exports/{exportId_pptx}` (e.g. in sequence or inform user to poll). For each: when COMPLETED, show downloadUrl; when FAILED, show errorMessage and which format failed.
3. Optionally: if user wants to cancel the slower one, POST `.../exports/{exportId}/cancel` for the relevant exportId.

**Workflow C — User**: "Start a PPTX export; I might cancel it if it takes too long."

1. POST `.../exports/pptx`; get `exportId`. Tell user polling has started.
2. If user says "cancel the export" before COMPLETED: POST `.../exports/{exportId}/cancel`; show response (status CANCELLED or ALREADY_TERMINAL).
3. If not canceled: poll until COMPLETED and show downloadUrl, or FAILED and show errorMessage.

---

## Response format (required)

- (if response contains url to show image) please show image and show json response instead of table
- Always show the **raw JSON response** (verbatim) in a JSON code block.
- If the response contains a URL for an image, **render/show the image** and also show the **JSON response** (do not convert to a table).
