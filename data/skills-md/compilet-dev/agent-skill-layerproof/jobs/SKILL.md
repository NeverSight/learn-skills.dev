---
name: jobs
description: Public API job status polling (X-API-KEY). Poll async operations (outline, slides, exports, etc.) by activityId. Types follow PublicApiJobController (/api/v2/jobs/{activityId}).
---

# Skill: Job Monitoring

## Description

Poll the status of asynchronous operations. This skill documents the **public API** at `/api/v2/jobs/{activityId}` (PublicApiJobController). The `activityId` is returned when you start async operations (e.g. outline/generate, batch-generate, export PNG/PPTX). Authenticate with `X-API-KEY` header.

---

## TypeScript types (request / response)

Mirrors `PublicApiJobController` response.

```typescript
// --- Get Job Status (GET) ---
type JobStatusResponse = {
  activity_id: string;
  status: 'SCHEDULED' | 'RUNNING' | 'PENDING' | 'DONE' | 'CANCELED';
  message: string;
  created_at?: string | null;   // ISO 8601
  updated_at?: string | null;   // ISO 8601
  output?: string | null;       // JSON string when DONE
  failure_reason?: string | null;
};
```

---

## Get Job Status

Response: `JobStatusResponse`.

Poll until `status` is `DONE` or `CANCELED`. When DONE, use `output` (JSON string) for results; when failed, use `failure_reason`.

```bash
curl "$LAYERPROOF_BASE_URL/api/v2/jobs/<activity_id>" \
  -H "X-API-KEY: $LAYERPROOF_API_KEY"
```

---

## Agent behavior

When the user asks to check job status or poll an async operation, do the following.

### 1. Endpoint

| User intent | Endpoint | Method |
|-------------|----------|--------|
| Check/poll job status | `/api/v2/jobs/{activityId}` | GET |

### 2. Build and run

- **Auth**: Include `X-API-KEY: $LAYERPROOF_API_KEY`. Read env vars; if missing, tell the user.
- **Path**: Use the `activity_id` returned from a previous async call (outline generate, batch generate, export, etc.). Run curl and show the result.

### 3. After response

- If status is SCHEDULED/RUNNING/PENDING, suggest polling again after a few seconds.
- If DONE, parse `output` if present and summarize the result.
- If CANCELED or DONE with `failure_reason`, report the outcome.

### 4. Response handling

- Always show the **raw JSON response** in a JSON code block.
- On 404, job not found or user does not own the associated project.

### 5. Example workflows

**Workflow A — User**: "Check status of job [activity_id]."

1. GET `/api/v2/jobs/{activityId}`; show JSON. If SCHEDULED/RUNNING/PENDING, suggest re-polling in a few seconds. If DONE, show `output` (and summarize). If CANCELED or failure_reason, report and stop.

**Workflow B — User**: "I started an outline generate and a batch generate; poll both and tell me when they’re done or if either failed."

1. User provides two activity IDs (or they are in context from prior slide-deck calls). Poll GET `/api/v2/jobs/{activityId1}` and GET `/api/v2/jobs/{activityId2}`.
2. For each: if DONE, report success and optionally parse `output`; if CANCELED or DONE with `failure_reason`, report which job failed and the reason.
3. If both still in progress, suggest polling again; if one is DONE and the other not, report current state and continue polling the other until terminal.

**Workflow C — User**: "Wait for this job and then get the slide deck / campaign / export result."

1. Poll GET `/api/v2/jobs/{activityId}` until status is DONE or CANCELED. If failed, report and stop.
2. When DONE: depending on workflow type (from initial trigger), hand off to the right skill — e.g. slide-decks GET deck, social-campaigns GET campaign, exports GET export status — using IDs from context or from `output` (e.g. project_id, slide_deck_id, campaign_id, export_id) and show the resulting resource or download URL.

---

## Response format (required)

- (if response contains url to show image) please show image and show json response instead of table
- Always show the **raw JSON response** (verbatim) in a JSON code block.
- If the response contains a URL for an image, **render/show the image** and also show the **JSON response** (do not convert to a table).
