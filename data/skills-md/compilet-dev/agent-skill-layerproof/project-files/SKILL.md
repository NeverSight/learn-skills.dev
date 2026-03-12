---
name: project-files
description: Public API project file management (X-API-KEY). Prepare upload/update, confirm, get file, download URL, delete. Types follow PublicApiProjectFileController (/api/v2/projects/{projectId}/...).
---

# Skill: Project Files

## Description

Manage files in project directories. This skill documents the **public API** at `/api/v2/projects/{projectId}` (PublicApiProjectFileController). Upload flow: 1) POST prepare with directoryId; 2) PUT file to `upload_url`; 3) POST confirm with `file_id`. All paths require `projectId`; prepare/prepare-update also need `directoryId`. Authenticate with `X-API-KEY` header.

---

## TypeScript types (request / response)

Mirrors `PublicApiProjectFileController` data classes.

```typescript
// --- Prepare upload (POST) — 201 ---
type PrepareFileUploadRequest = {
  path: string;
  file_name: string;
  mime_type: string;
  size: number;
};
type PrepareFileUploadResponse = {
  upload_url: string;
  file_id: string;
  s3_key: string;
  expires_at: string;
};

// --- Prepare update (POST) ---
type PrepareUpdateFileRequest = {
  path: string;
  mime_type?: string | null;
  size?: number | null;
};
type PrepareUpdateFileResponse = {
  upload_url: string;
  file_id: string;
  s3_key: string;
  expires_at: string;
};

// --- Confirm (POST) ---
type ConfirmFileUploadRequest = { metadata?: Record<string, unknown> | null };
type FileResponse = {
  id: string;
  name: string;
  file_type: string;
  mime_type: string;
  s3_key: string;
  size: number;
  uploaded_at: string;
  uploaded_by: string;
  status: string;
  metadata: Record<string, unknown> | null;
};

// --- Download URL (GET), Get file (GET), Delete (DELETE) ---
type DownloadUrlResponse = {
  download_url: string;
  expires_at: string;
};
```

---

## Prepare Project File Upload

Request body: `PrepareFileUploadRequest`. Response (201): `PrepareFileUploadResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/directories/<directory_id>/files/prepare" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"path":"/","file_name":"doc.pdf","mime_type":"application/pdf","size":2048}'
```

---

## Prepare Project File Update

Request body: `PrepareUpdateFileRequest`. Response: `PrepareUpdateFileResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/directories/<directory_id>/files/prepare-update" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"path":"/doc.pdf","mime_type":"application/pdf","size":2048}'
```

---

## Confirm Project File Upload

Request body: `ConfirmFileUploadRequest`. Response: `FileResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/files/<file_id>/confirm" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"metadata":{}}'
```

---

## Get File Download URL

Response: `DownloadUrlResponse`.

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/files/<file_id>/download-url" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Get File Details

Response: `FileResponse`.

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/files/<file_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Delete Project File

Response: 204 No Content.

```bash
curl -X DELETE "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/files/<file_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Agent behavior

When the user asks to manage project files (upload, update, confirm, download, delete), do the following.

### 1. Choose the right endpoint

Base path: `/api/v2/projects/{projectId}`. Replace `project_id`, `directory_id`, `file_id` as needed.

| User intent | Endpoint | Method |
|-------------|----------|--------|
| Get upload URL for new file | `.../directories/{directoryId}/files/prepare` | POST |
| Get upload URL to update file | `.../directories/{directoryId}/files/prepare-update` | POST |
| Confirm upload after PUT | `.../files/{fileId}/confirm` | POST |
| Get download URL | `.../files/{fileId}/download-url` | GET |
| Get file metadata | `.../files/{fileId}` | GET |
| Delete file | `.../files/{fileId}` | DELETE |

### 2. Build and run the request

- **Auth**: Include `X-API-KEY: $LAYERPROOF_API_KEY`. Read env vars; if missing, tell the user.
- **Path**: Resolve projectId, directoryId, fileId from context or user input.
- **POST**: Build JSON body from types above; run curl and show result.
- **GET/DELETE**: Build path only; run curl and show result.

### 3. Upload flow

Prepare → PUT file to `upload_url` → confirm with `file_id`. Then use `file_id` for get/download/delete.

### 4. Response handling

- Always show raw JSON in a code block; show image + JSON if image URL present.
- On error, show body and status code.

### 5. Example workflows

**Workflow A — User**: "Upload a PDF to project X in the root directory."

1. Resolve projectId and directoryId (e.g. root directory from project or list directories). POST `.../directories/{directoryId}/files/prepare` with `{"path":"/","file_name":"brief.pdf","mime_type":"application/pdf","size":<bytes>}`; get `upload_url`, `file_id`, `s3_key`.
2. Tell user to PUT the file to `upload_url` with `Content-Type: application/pdf`. Then POST `.../files/{file_id}/confirm` with `{}` (or `{"metadata":{}}`).
3. Show JSON; use `file_id` for later get/download/delete.

**Workflow B — User**: "Upload two reference docs to the project, then use them when generating the slide deck outline."

1. For each file: prepare with path (e.g. `/ref1.pdf`, `/ref2.docx`) → user uploads to `upload_url` → confirm. Capture both `file_id` and `s3_key` (if returned) for each.
2. If outline generation accepts project file references: pass the project file identifiers (e.g. s3_keys or file_ids) into the slide-deck outline/generate request (e.g. `file_s3_keys` or equivalent). Otherwise use public-files for outline references and keep project files for project-scoped use only.
3. Hand off to slide-decks: POST outline/generate with the resolved keys; poll job; get deck.

**Workflow C — User**: "Update an existing file in the project (new version) and get a download URL after."

1. Resolve projectId, directoryId, and existing file path. POST `.../directories/{directoryId}/files/prepare-update` with `{"path":"/brief.pdf","mime_type":"application/pdf","size":<new_bytes>}`; get `upload_url`, `file_id`.
2. User PUTs new content to `upload_url`; then POST `.../files/{file_id}/confirm`. GET `.../files/{file_id}/download-url` to show the user a temporary download link.
3. On error (e.g. path not found), show response body and suggest verifying path and project/directory IDs.

---

## Response format (required)

- (if response contains url to show image) please show image and show json response instead of table
- Always show the **raw JSON response** (verbatim) in a JSON code block.
- If the response contains a URL for an image, **render/show the image** and also show the **JSON response** (do not convert to a table).
