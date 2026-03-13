---
name: slides
description: Public API slide editing (X-API-KEY). Edit slide images with AI, accept/revert edits, object removal, text extraction, save Konva nodes. Types follow PublicApiSlideController (/api/v2/projects/{projectId}/slides).
---

# Skill: Slide Editing

## Description

Modify slides after generation. This skill documents the **public API** at `/api/v2/projects/{projectId}/slides` (PublicApiSlideController). All slide endpoints require `projectId` and `slideId` in the path. Authenticate with `X-API-KEY` header.

---

## TypeScript types (request / response)

Mirrors `PublicApiSlideController` (/api/v2/projects/{projectId}/slides) data classes.

```typescript
// Shared: cropped region for region-based editing. Must lie fully within image bounds.
// Constraints: x >= 0, y >= 0, width > 0, height > 0; x + width <= image width, y + height <= image height.
type CroppedRegion = {
  x: number;
  y: number;
  width: number;
  height: number;
};

// --- Edit Slide Image (POST) — async, poll jobs ---
type SlideImageEditRequest = {
  /** AI instruction for the edit (required, non-blank) */
  instruction: string;
  /** Path to input image in project working dir (required, non-blank) */
  input_image_path: string;
  /** Optional extra reference image paths */
  other_reference_image_paths?: string[];
  /** Optional region to edit; only this region is modified */
  cropped_region?: CroppedRegion;
};

// --- Accept Image Edit (POST) ---
type AcceptImageEditRequest = {
  live_object_id: string;   // UUID from image-edit or object-removal response (required)
  target_node_id?: string;
  override_image_path?: string;  // Optional path to use instead of workflow output
};

// --- Revert Slide (POST) ---
type RevertSlideRequest = {
  history_entry_id: string;  // UUID from slide history (required)
  node_id?: string;
};

// --- Object Removal (POST) — async, poll jobs ---
type ObjectRemovalRequest = {
  input_image_path: string;  // required, non-blank
  mask_path?: string;
  cropped_region?: CroppedRegion;
};

// --- Extract Text (POST) — async, poll jobs ---
type ExtractTextRequest = {
  node_id?: string;
  node_image_path?: string;
};

// --- Save Konva Nodes (PUT) ---
type SaveKonvaNodesRequest = {
  konva_nodes: Record<string, unknown>;  // required
  konva_order: string[];                  // required
  flattened_image_path?: string;
  base_snapshot_id?: string;  // UUID, optional
};

// --- Responses ---
type TriggerWorkflowResponse = {
  activity_id: string;   // UUID – poll GET /api/v2/jobs/{activityId}
  workflow_type: string;
  live_object_id: string; // UUID – pass to accept-image-edit when done
};

type AcceptImageEditResponse = {
  id: string;             // slide UUID
  slide_section_id: string;
  image_path: string | null;
  status: string;
};
```

---

## Edit Slide Image (async)

Request body: `SlideImageEditRequest`. Response: `TriggerWorkflowResponse`.

Triggers AI-powered slide image editing. Upload input image first, then call with `instruction` and `input_image_path`. Poll `GET /api/v2/jobs/{activityId}` for status; when DONE, call accept-image-edit with `live_object_id`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slides/<slide_id>/image-edit" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"instruction":"Make the background blue","input_image_path":"/slides/slide-1.png"}'
```

With optional region and reference images:

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slides/<slide_id>/image-edit" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"instruction":"Replace this area","input_image_path":"/slides/slide-1.png","cropped_region":{"x":0,"y":0,"width":200,"height":100},"other_reference_image_paths":["/ref.png"]}'
```

---

## Accept Image Edit

Request body: `AcceptImageEditRequest`. Response: `AcceptImageEditResponse`.

Call after the image-edit or object-removal workflow completes successfully. Use `live_object_id` from the trigger response.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slides/<slide_id>/accept-image-edit" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"live_object_id":"<live_object_uuid>"}'
```

---

## Revert Slide

Request body: `RevertSlideRequest`. Response: `AcceptImageEditResponse`.

Reverts the slide to a previous version using `history_entry_id` from slide history.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slides/<slide_id>/revert" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"history_entry_id":"<history_entry_uuid>"}'
```

---

## Remove Objects (async)

Request body: `ObjectRemovalRequest`. Response: `TriggerWorkflowResponse`.

Triggers AI-powered object removal. Optional `mask_path` for mask-based removal. Poll jobs; when DONE, call accept-image-edit with `live_object_id`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slides/<slide_id>/object-removal" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"input_image_path":"/slides/slide-1.png"}'
```

With mask:

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slides/<slide_id>/object-removal" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"input_image_path":"/slides/slide-1.png","mask_path":"/masks/mask.png"}'
```

---

## Extract Text (async)

Request body: `ExtractTextRequest` (optional). Response: `TriggerWorkflowResponse`.

Performs OCR, removes text from image via inpainting, creates editable Konva text nodes. Poll `GET /api/v2/jobs/{activityId}` for status.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slides/<slide_id>/extract-text" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{}'
```

With optional node:

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slides/<slide_id>/extract-text" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"node_id":"node-1","node_image_path":"/nodes/node1.png"}'
```

---

## Save Konva Nodes

Request body: `SaveKonvaNodesRequest`. Response: 200, no body.

Persists Konva canvas nodes and order (positions, layer order, flattened image path).

```bash
curl -X PUT "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slides/<slide_id>/konva-nodes" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"konva_nodes":{},"konva_order":[]}'
```

---

## Agent behavior

When the user asks to edit slides (image edit, accept edit, revert, remove objects, extract text, save canvas), do the following.

### 1. Choose the right endpoint

| User intent | Endpoint | Method |
|-------------|----------|--------|
| Edit slide image with AI instruction | `/api/v2/projects/{projectId}/slides/{slideId}/image-edit` | POST |
| Accept edited image after workflow completes | `/api/v2/projects/{projectId}/slides/{slideId}/accept-image-edit` | POST |
| Revert slide to previous version | `/api/v2/projects/{projectId}/slides/{slideId}/revert` | POST |
| Remove objects from slide image (AI) | `/api/v2/projects/{projectId}/slides/{slideId}/object-removal` | POST |
| Extract text from slide (OCR + inpainting) | `/api/v2/projects/{projectId}/slides/{slideId}/extract-text` | POST |
| Save Konva canvas nodes/order | `/api/v2/projects/{projectId}/slides/{slideId}/konva-nodes` | PUT |

All paths require `projectId` and `slideId` (replace placeholders with actual UUIDs).

### 2. Build and run the request

- **Auth**: Every request must include `X-API-KEY: $LAYERPROOF_API_KEY`. Read `LAYERPROOF_BASE_URL` and `LAYERPROOF_API_KEY` from the environment; if missing, tell the user to set them.
- **Path**: Resolve `project_id` and `slide_id` from context (e.g. from project/slide-deck list or user input). If missing, ask the user.
- **POST/PUT**: Build JSON body from the types above. Use `-X POST` or `-X PUT`, `-H "Content-Type: application/json"`, and `-d '...'`. Run the curl and show the result.

### 3. After async endpoints (image-edit, object-removal, extract-text)

- Response includes `activity_id` and `live_object_id`. Tell the user the workflow was started.
- Suggest polling `GET $LAYERPROOF_BASE_URL/api/v2/jobs/<activity_id>` until `status` is `DONE` or `CANCELED`.
- For image-edit and object-removal: when DONE, tell the user to call **accept-image-edit** with `live_object_id` to apply the result.

### 4. Response handling

- Always show the **raw JSON response** in a JSON code block; do not convert to a table.
- If the response contains a URL for an image (e.g. `image_path`), show the image and the JSON.
- On error (4xx/5xx), show the response body and status code; suggest fixing API key, projectId/slideId, or request body.

### 5. Example workflows

**Workflow A — User**: "Edit slide image in project X, slide Y: make the background darker."

1. Choose `POST /api/v2/projects/{projectId}/slides/{slideId}/image-edit`.
2. Resolve projectId and slideId (from user or ask).
3. Build body: `{"instruction":"Make the background darker","input_image_path":"/path/to/slide/image"}` (user may need to provide image path).
4. Run curl; show JSON. Mention polling jobs with `activity_id` and calling accept-image-edit with `live_object_id` when done.

**Workflow B — User**: "Edit two slides: darker background on slide 1, remove the logo from slide 3; then revert slide 1 if I don’t like it."

1. Resolve projectId; get slide ids from slide-deck GET deck (e.g. `slides[0].id`, `slides[2].id`).
2. For slide 1: POST `.../slides/{slideId1}/image-edit` with `{"instruction":"Make the background darker"}`; capture `activity_id_1` and `live_object_id_1`. For slide 3: POST `.../slides/{slideId3}/object-removal` with region/instruction; capture `activity_id_3` and `live_object_id_3`.
3. Poll `GET /api/v2/jobs/{activity_id_1}` and `.../jobs/{activity_id_3}` until both DONE. If either fails, report which slide and reason.
4. POST `.../slides/{slideId1}/accept-image-edit` with `{"live_object_id":"<live_object_id_1>"}`; POST `.../slides/{slideId3}/accept-image-edit` with `{"live_object_id":"<live_object_id_3>"}`. Show updated slide images (GET deck or slide detail).
5. If user says "revert slide 1": GET slide history (if available) for slideId1 to get `history_entry_id`; POST `.../slides/{slideId1}/revert` with `{"history_entry_id":"<id>"}`. Confirm with GET deck.

**Workflow C — User**: "Extract text from slide 2 and replace the old text (OCR + inpainting)."

1. Resolve projectId and slideId for slide 2. POST `.../slides/{slideId}/extract-text` (body per API); capture `activity_id`.
2. Poll `GET /api/v2/jobs/{activity_id}` until DONE. When DONE, `output` may contain extracted text or updated asset reference.
3. If a follow-up accept or apply step is required (e.g. accept-image-edit), use the returned `live_object_id`; otherwise show the result (e.g. updated slide or transcript) from GET deck.

---

## Response format (required)

- (if response contains url to show image) please show image and show json response instead of table
- Always show the **raw JSON response** (verbatim) in a JSON code block.
- If the response contains a URL for an image, **render/show the image** and also show the **JSON response** (do not convert to a table).
