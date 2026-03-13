---
name: slide-decks
description: Public API slide deck operations (X-API-KEY). Generate outlines, update outline, get deck, batch generate slides, generate transcript/image/content, cancel, theme, transcript, duplicate section. Types follow PublicApiSlideDeckController (/api/v2/projects/{projectId}/slide-deck/{slideDeckId}).
---

# Skill: Slide Deck Generation

## Description

Manage AI-generated slide decks and outlines. This skill documents the **public API** at `/api/v2/projects/{projectId}/slide-deck/{slideDeckId}` (PublicApiSlideDeckController). All endpoints require `projectId` and `slideDeckId` in the path. Authenticate with `X-API-KEY` header. Poll async operations via `GET /api/v2/jobs/{activityId}`.

---

## TypeScript types (request / response)

Mirrors `PublicApiSlideDeckController` data classes.

```typescript
// --- Outline section (used in UpdateOutlineRequest and responses) ---
type PublicApiSlideIconAsset = { query: string; slot?: string | null };
type PublicApiSlideImageAsset = { prompt: string; slot?: string | null };
type PublicApiOutlineSection = {
  id: string;
  section_title: string;   // 1–500 chars
  content?: string | null;  // max 5000
  key_points?: string[] | null;
  visual_suggestion?: string | null;  // max 500
  speaker_notes?: string | null;       // max 2000
  layout?: string | null;
  icon_assets?: PublicApiSlideIconAsset[];
  image_assets?: PublicApiSlideImageAsset[];
};

// --- Generate Outline (POST) — async ---
type GenerateOutlineRequest = {
  prompt: string;               // 3–2000 chars, required
  slide_count?: number;         // default 5, min 1
  language?: string;            // 2–10 chars, e.g. "en"
  file_s3_keys?: string[];      // from POST /api/v2/files/prepare
  web_search_enabled?: boolean;
  text_detail_level?: string | null;
  tone?: string | null;
  outline_type?: string | null;
};
type GenerateOutlineResponse = {
  activity_id: string;
  status: string;
  message: string;
  estimated_completion_seconds?: number;
};

// --- Update Outline (PUT) ---
type UpdateOutlineRequest = {
  title: string;                // 1–500 chars
  sections: PublicApiOutlineSection[];  // at least one required
};
type PublicApiOutline = {
  id: string;
  title: string;
  sections: PublicApiOutlineSection[];
  total_sections: number;
  updated_at?: string;
};
type UpdateOutlineResponse = { outline: PublicApiOutline };

// --- Get Deck (GET) ---
type PublicApiSlideDeck = {
  id: string;
  project_id: string;
  title: string;
  description?: string | null;
  deck_type?: string | null;
  slide_numbers?: number | null;
  aspect_ratio: string;
  theme?: string | null;
  outline_generation_live_object_id?: string | null;
  created_at: string;
  updated_at: string;
};
type PublicApiSlide = {
  id: string;
  index: number;
  section_id: string;
  section_title: string;
  content?: string | null;
  key_points?: string[] | null;
  visual_suggestion?: string | null;
  speaker_notes?: string | null;
  transcript?: string | null;
  image_url?: string | null;
  image_expires_at?: string | null;
  generation_status: string;
  error_message?: string | null;
  created_at: string;
  updated_at: string;
};
type PublicApiDeckMetadata = {
  total_slides: number;
  completed_slides: number;
  pending_slides: number;
  overall_progress: number;
};
type GetDeckResponse = {
  slide_deck: PublicApiSlideDeck;
  outline: PublicApiOutline;
  slides: PublicApiSlide[];
  metadata: PublicApiDeckMetadata;
};

// --- Batch Generate Slides (POST) — async ---
type BatchGenerateSlidesRequest = {
  generation_type?: string;          // default "BOTH"
  speaking_style?: string | null;
  target_duration_minutes?: number | null;  // min 1
  transcript_tone?: string | null;
  aspect_ratio?: string | null;
  output_language?: string | null;   // 2–10 chars
  text_detail_level?: string | null;
  tone?: string | null;
};
type BatchGenerateSlidesResponse = {
  activity_id: string;
  total_slides: number;
  status: string;
  message: string;
  estimated_completion_seconds: number;
};

// --- Generate Slide Content / Transcript / Image (POST) — async ---
type GenerateSlideContentRequest = {
  slide_section_id: string;
  speaking_style?: string | null;
  target_duration_minutes?: number | null;  // min 1
  transcript_tone?: string | null;
  generation_type?: string | null;   // default "TRANSCRIPT_AND_IMAGE"
};
type GenerateSlideContentResponse = {
  activity_id: string;
  slide_section_id: string;
  transcript_gen_live_object_id?: string | null;
  image_gen_live_object_id?: string | null;
  status: string;
  message: string;
};

type GenerateSlideTranscriptRequest = {
  slide_section_id: string;
  speaking_style?: string | null;
  target_duration_minutes?: number | null;  // min 1
  transcript_tone?: string | null;
};
type GenerateSlideTranscriptResponse = {
  activity_id: string;
  slide_section_id: string;
  transcript_gen_live_object_id: string;
  status: string;
  message: string;
  estimated_completion_seconds?: number;
};

type GenerateSlideImageRequest = {
  slide_section_id: string;
  aspect_ratio?: string;  // "16:9" | "4:3" | "1:1", default "16:9"
};
type GenerateSlideImageResponse = {
  activity_id: string;
  slide_section_id: string;
  image_gen_live_object_id: string;
  status: string;
  message: string;
  estimated_completion_seconds?: number;
};

// --- Cancel Generation (POST) ---
type CancelGenerationRequest = { live_object_ids?: string[] | null };
type CancelGenerationResponse = {
  cancelled_live_objects: string[];
  failed_to_cancel_live_objects: string[];
  total_activities_cancelled: number;
  message: string;
};

// --- Generate Theme (POST) — async ---
type GenerateThemeRequest = {
  prompt: string;                      // 10–2000 chars
  reference_image_paths?: string[] | null;
};
type GenerateThemeResponse = {
  activity_id: string;
  status: string;
  message: string;
  estimated_completion_seconds: number;
};

// --- Update Transcript (PUT) ---
type UpdateTranscriptRequest = { transcript: string };
type UpdateTranscriptResponse = {
  slide_section_id: string;
  version_id: string;
  version_number: number;
  transcript_gen_live_object_id: string;
  transcript: string;
  updated_at: string;
};

// --- Duplicate Section (POST) ---
type DuplicateSectionRequest = {
  copy_content?: boolean;
  insert_after?: boolean;
};
type DuplicateSectionResponse = {
  new_section_id: string;
  new_section: PublicApiOutlineSection;
  transcript_gen_live_object_id?: string | null;
  image_gen_live_object_id?: string | null;
  message: string;
};
```

---

## Generate Outline (async)

Request body: `GenerateOutlineRequest`. Response (202): `GenerateOutlineResponse`.

Starts outline generation from a prompt. Use `file_s3_keys` from files uploaded via `/api/v2/files/prepare` and confirm. Poll `GET /api/v2/jobs/{activityId}` for status.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/outline/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"prompt":"Create a product launch deck","slide_count":6}'
```

With reference files and language:

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/outline/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"prompt":"Q4 strategy","slide_count":5,"language":"en","file_s3_keys":["public-api/.../file.pdf"],"web_search_enabled":true}'
```

---

## Update Outline

Request body: `UpdateOutlineRequest`. Response: `UpdateOutlineResponse`.

Updates outline title and sections (add, remove, reorder). At least one section required.

```bash
curl -X PUT "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/outline" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"title":"My Deck","sections":[{"id":"section-uuid","section_title":"Intro","content":"...","speaker_notes":"..."}]}'
```

---

## Get Full Slide Deck

Query: `include_images` (default true), `image_expiry_seconds` (default 3600). Response: `GetDeckResponse`.

Returns deck, outline, slides with presigned image URLs, and metadata.

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/?include_images=true&image_expiry_seconds=3600" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Batch Generate Slides (async)

Request body: `BatchGenerateSlidesRequest`. Response (202): `BatchGenerateSlidesResponse`.

Generate transcript and/or images for all outline sections. Requires an outline first. Poll jobs with `activity_id`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/slides/batch-generate" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"generation_type":"BOTH"}'
```

---

## Generate Slide Content (async)

Request body: `GenerateSlideContentRequest`. Response (202): `GenerateSlideContentResponse`.

Generate transcript and image for one section. Poll `GET /api/v2/jobs/{activityId}`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/slides/generate-content" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"slide_section_id":"<section_uuid>"}'
```

---

## Generate Slide Transcript (async)

Request body: `GenerateSlideTranscriptRequest`. Response (202): `GenerateSlideTranscriptResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/slides/generate-transcript" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"slide_section_id":"<section_uuid>"}'
```

---

## Generate Slide Image (async)

Request body: `GenerateSlideImageRequest`. Response (202): `GenerateSlideImageResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/slides/generate-image" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"slide_section_id":"<section_uuid>","aspect_ratio":"16:9"}'
```

---

## Cancel Generation

Request body: `CancelGenerationRequest`. Response: `CancelGenerationResponse`.

Provide `live_object_ids` from active generation responses to cancel.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/cancel" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"live_object_ids":["<live_object_uuid>"]}'
```

---

## Generate Deck Theme (async)

Request body: `GenerateThemeRequest`. Response (202): `GenerateThemeResponse`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/theme/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"prompt":"Minimal corporate blue"}'
```

---

## Update Slide Transcript

Request body: `UpdateTranscriptRequest`. Response: `UpdateTranscriptResponse`.

Path includes `slideSectionId`: `PUT .../slides/{slideSectionId}/transcript`.

```bash
curl -X PUT "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/slides/<slide_section_id>/transcript" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"transcript":"Updated speaker notes."}'
```

---

## Duplicate Slide Section

Request body: `DuplicateSectionRequest`. Response: `DuplicateSectionResponse`.

Path includes `slideSectionId`: `POST .../slides/{slideSectionId}/duplicate`.

```bash
curl -X POST "$LAYERPROOF_BASE_URL/api/v2/projects/<project_id>/slide-deck/<slide_deck_id>/slides/<slide_section_id>/duplicate" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY" \
  -d '{"copy_content":true,"insert_after":true}'
```

---

## Agent behavior

When the user asks to work with slide decks (outline, deck, slides, theme, transcript), do the following.

### 1. Choose the right endpoint

Base path: `/api/v2/projects/{projectId}/slide-deck/{slideDeckId}`. All require `projectId` and `slideDeckId`.

| User intent | Endpoint | Method |
|-------------|----------|--------|
| Generate outline from prompt | `.../outline/generate` | POST |
| Update outline structure | `.../outline` | PUT |
| Get full deck (outline + slides + URLs) | `.../` (with optional query) | GET |
| Batch generate all slides | `.../slides/batch-generate` | POST |
| Generate one slide content | `.../slides/generate-content` | POST |
| Generate one slide transcript | `.../slides/generate-transcript` | POST |
| Generate one slide image | `.../slides/generate-image` | POST |
| Cancel generations | `.../cancel` | POST |
| Generate deck theme | `.../theme/generate` | POST |
| Update slide transcript | `.../slides/{slideSectionId}/transcript` | PUT |
| Duplicate section | `.../slides/{slideSectionId}/duplicate` | POST |

Other endpoints (improve section, generate-manual, visual style, transcript versions, restore version, mark read, TTS, audio download URL, update settings, import prepare/pptx, tone settings, batch layout): use same base path and request/response shapes from controller.

### 2. Build and run the request

- **Auth**: Every request must include `X-API-KEY: $LAYERPROOF_API_KEY`. Read `LAYERPROOF_BASE_URL` and `LAYERPROOF_API_KEY` from the environment; if missing, tell the user to set them.
- **Path**: Resolve `projectId` and `slideDeckId` (and `slideSectionId` where needed) from context or user input. If missing, ask.
- **GET**: Build curl with path and query params (`include_images`, `image_expiry_seconds` for get deck). Run and show result.
- **POST/PUT**: Build JSON body from the types above. Use `-X POST` or `-X PUT`, `-H "Content-Type: application/json"`, and `-d '...'`. Run and show result.

### 3. After async endpoints

- Responses include `activity_id`. Tell the user the job was started and suggest polling `GET $LAYERPROOF_BASE_URL/api/v2/jobs/{activityId}` until `status` is `DONE` or `CANCELED`.
- Typical flow: generate outline → poll until DONE → get deck or update outline → batch generate slides or generate single slide content/transcript/image → poll jobs.

### 4. Response handling

- Always show the **raw JSON response** in a JSON code block; do not convert to a table.
- If the response contains image URLs (e.g. in get deck `slides[].image_url`), show images and the JSON.
- On error (4xx/5xx), show the response body and status code; suggest fixing API key, projectId/slideDeckId/sectionId, or request body.

### 5. Example workflows

**Workflow A — User**: "Generate an outline for a product launch deck in project X."

1. Resolve projectId and slideDeckId (e.g. from GET projects, then `project.slide_deck_id`).
2. Choose `POST .../outline/generate`.
3. Build body: `{"prompt":"Product launch deck","slide_count":5}`.
4. Run curl; show JSON. Tell user to poll `GET /api/v2/jobs/{activityId}` and then call get deck or update outline as needed.

**Workflow B — User**: "Full deck: outline from a prompt and reference PDF, then tweak the outline, apply a theme, batch generate slides, and fix one slide’s image."

1. Resolve projectId and slideDeckId. Get `file_s3_keys` from public-files (prepare → upload → confirm) or project-files if the API accepts them for outline.
2. POST `.../outline/generate` with `{"prompt":"Product launch with pricing","slide_count":6,"file_s3_keys":["<s3_key>"],"language":"en"}`; capture `activity_id`.
3. Poll `GET /api/v2/jobs/{activity_id}` until DONE. On failure, report and stop.
4. GET deck; from `outline.sections` identify a section to change. PUT `.../outline` with `title` and updated `sections` (e.g. edit `section_title`, `key_points`, `visual_suggestion` for one section).
5. If user wants a theme: use themes skill to resolve `theme_id`; PUT `.../settings` with `{"theme_id":"<theme_id>"}` (or apply-theme endpoint per API).
6. POST `.../batch-generate` with optional `generation_type`, `aspect_ratio`, `speaking_style`; capture `activity_id`.
7. Poll `GET /api/v2/jobs/{activity_id}` until DONE.
8. GET deck; check `metadata.completed_slides` and `slides[].generation_status`. If one slide’s image is wrong, POST `.../slides/{sectionId}/generate-image` (or generate-content) with section id; poll that job until DONE; GET deck again to show result.

**Workflow C — User**: "Duplicate a section in the outline and regenerate slides for the new section only."

1. GET deck; from `outline.sections` get section ids and order. Determine source section to duplicate.
2. POST `.../sections/duplicate` with `section_id` (or equivalent); capture new `section_id` from response or GET deck again.
3. PUT `.../outline` to include the new section in `sections` with correct order and titles.
4. POST `.../slides/{newSectionId}/generate-transcript` and/or `generate-image` (or batch-generate if it supports partial); poll job(s); GET deck to confirm.

---

## Response format (required)

- (if response contains url to show image) please show image and show json response instead of table
- Always show the **raw JSON response** (verbatim) in a JSON code block.
- If the response contains a URL for an image, **render/show the image** and also show the **JSON response** (do not convert to a table).
