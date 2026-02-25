---
name: Modellix
description: Use when building applications that generate images or videos from text/images, integrating AI models via API, querying async task results, or handling rate limiting and error scenarios. Reach for this skill when users request image/video generation, need to understand API authentication, or troubleshoot API errors.
metadata:
    mintlify-proj: modellix
    version: "1.0"
---

# Modellix Skill

## Product Summary

Modellix is a Model-as-a-Service (MaaS) platform providing unified API access to 100+ AI models for text-to-image, text-to-video, image-to-image, image-to-video, and video editing tasks. Agents use Modellix to submit async generation tasks and retrieve results via REST API. The primary endpoint is `https://api.modellix.ai/api/v1/`. All requests require Bearer token authentication. Key file paths: API keys are managed in the Modellix console at `https://modellix.ai/console/api-key`. Task results are queried via `GET /api/v1/tasks/{task_id}`. Results expire after 24 hours.

## When to Use

Reach for this skill when:
- A user requests image or video generation from text or images
- You need to integrate AI model APIs into an application
- You're building async task submission and polling workflows
- You encounter API authentication errors (401) or rate limiting (429)
- You need to understand task status transitions (pending → processing → success/failed)
- You're debugging API parameter validation or response parsing
- You need to implement exponential backoff retry logic
- You're managing concurrent task limits or team rate limits

## Quick Reference

### API Endpoint Structure
```
POST https://api.modellix.ai/api/v1/{type}/{provider}/{model_id}/async
GET https://api.modellix.ai/api/v1/tasks/{task_id}
```

### Supported Business Types
| Type | Use Case |
|------|----------|
| `text-to-image` | Generate images from text prompts |
| `text-to-video` | Generate videos from text prompts |
| `image-to-image` | Edit, translate, or transform images |
| `image-to-video` | Animate static images into videos |

### Authentication
All requests require the header:
```
Authorization: Bearer YOUR_API_KEY
```
API keys are created in the Modellix console and displayed only once—save immediately.

### Task Status Values
| Status | Meaning |
|--------|---------|
| `pending` | Task queued, waiting to process |
| `processing` | Task actively running |
| `success` | Task completed, results available in `result` object |
| `failed` | Task failed, check error details |

### Response Structure
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "success",
    "task_id": "task-abc123",
    "model_id": "qwen-image-plus",
    "duration": 3500,
    "result": {
      "resources": [
        {
          "url": "https://cdn.example.com/images/abc123.png",
          "type": "image",
          "width": 1024,
          "height": 1024,
          "format": "png",
          "role": "primary"
        }
      ],
      "metadata": { "image_count": 1 },
      "extensions": { "submit_time": "2024-01-01T10:00:00Z" }
    }
  }
}
```

### Timeout Recommendations
| Task Type | Timeout |
|-----------|---------|
| Text-to-image submission | 30–60 seconds |
| Text-to-video submission | 60–120 seconds |
| Task query | 10–30 seconds |

### Rate Limit Headers
When rate limited (429), check response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704067260
```

## Decision Guidance

### When to Use Async vs Polling
Modellix only offers async endpoints. Always:
1. Submit task with POST to `/async` endpoint
2. Receive `task_id` immediately
3. Poll `GET /tasks/{task_id}` until status is `success` or `failed`

### When to Retry vs Fail
| Error Code | Retryable? | Action |
|-----------|-----------|--------|
| 400 | ❌ No | Fix parameters (missing required fields, invalid format) |
| 401 | ❌ No | Verify API key format and validity |
| 404 | ❌ No | Check task_id exists and hasn't expired (24h limit) |
| 429 | ✅ Yes | Use exponential backoff; check `X-RateLimit-Reset` |
| 500 | ✅ Yes | Retry after 1–4 seconds (max 3 retries) |
| 503 | ✅ Yes | Retry with exponential backoff; service temporarily unavailable |

### When to Use Concurrency Control
- Team concurrent task limit: typically 3 tasks
- If you hit 429 with "Concurrent limit exceeded", wait for running tasks to complete
- Implement semaphore or queue to limit concurrent requests
- Monitor `X-RateLimit-Remaining` and throttle proactively when < 20% quota remains

## Workflow

### 1. Submit a Generation Task
1. Identify the model and business type (e.g., `text-to-image`, `alibaba`, `qwen-image-plus`)
2. Construct the request body with required parameters (e.g., `prompt` for text-to-image)
3. POST to `/api/v1/{type}/{provider}/{model_id}/async` with `Authorization: Bearer {key}`
4. Parse response: extract `task_id` from `data.task_id`
5. Store `task_id` for later polling

### 2. Poll Task Status
1. Wait 1–5 seconds (task processing time varies)
2. GET `/api/v1/tasks/{task_id}` with same API key
3. Check `data.status`:
   - If `pending` or `processing`: wait and retry
   - If `success`: extract results from `data.result.resources`
   - If `failed`: log error and handle failure
4. Repeat until terminal state (success/failed)

### 3. Extract and Use Results
1. Access generated resources in `data.result.resources` array
2. Each resource has `url`, `type` (image/video), `width`, `height`, `format`, `role`
3. Download or use the URL immediately—results expire after 24 hours
4. Store results in your system before expiration

### 4. Handle Errors
1. Check `code` field: 0 = success, non-zero = error
2. Parse `message` field for category and detail (format: `"Category: detail"`)
3. If retryable (429, 500, 503): implement exponential backoff
4. If non-retryable (400, 401, 404): fix the request and resubmit
5. Log full error response for debugging

## Common Gotchas

- **API key displayed only once**: Save immediately after creation. If lost, generate a new key.
- **Results expire after 24 hours**: Download or persist results before expiration. Querying an expired task returns 404.
- **Bearer token format required**: Use `Authorization: Bearer YOUR_KEY`, not `Authorization: YOUR_KEY` or other formats. Missing or malformed headers return 401.
- **Task IDs are unique per API key**: A task submitted with key A cannot be queried with key B. Verify you're using the same key for submission and polling.
- **Async-only API**: There is no synchronous endpoint. Always submit, receive task_id, then poll. Don't expect immediate results.
- **Concurrent task limits are team-wide**: All API keys under the same team share the concurrent quota. If one key hits the limit, other keys in the team are also blocked.
- **Rate limits reset per minute**: `X-RateLimit-Reset` is a Unix timestamp. Calculate wait time as `reset_time - current_time`.
- **Missing required parameters return 400**: Each model has required fields (e.g., `prompt` for text-to-image). Check the model's API reference page for exact parameters.
- **Parameter format errors are strict**: Size must be `"width*height"` (e.g., `"1024*1024"`), not `"1024"` or `"1024x1024"`. Invalid format returns 400.
- **Polling too frequently wastes quota**: Implement exponential backoff (1s, 2s, 4s) rather than polling every 100ms.
- **Task status transitions are one-way**: A task never reverts from `processing` to `pending`. If status seems stuck, check if task_id is correct or if it expired.
- **Provider and model_id are case-sensitive**: Use exact names from the API reference (e.g., `alibaba`, `qwen-image-plus`). Typos return 404.

## Verification Checklist

Before submitting work:
- [ ] API key is valid and saved securely (not in version control)
- [ ] Authorization header uses exact format: `Authorization: Bearer {key}`
- [ ] Request URL matches the pattern: `/api/v1/{type}/{provider}/{model_id}/async`
- [ ] Required parameters are present (check model's API reference page)
- [ ] Parameter formats are correct (e.g., size as `"width*height"`)
- [ ] Task submission returns `code: 0` and includes `task_id`
- [ ] Polling loop handles all task statuses: pending, processing, success, failed
- [ ] Error handling distinguishes retryable (429, 500, 503) from non-retryable (400, 401, 404)
- [ ] Exponential backoff is implemented for retries
- [ ] Results are downloaded/persisted before 24-hour expiration
- [ ] Rate limit headers are monitored; proactive throttling is in place
- [ ] Concurrent task limit is respected (typically 3 per team)
- [ ] Timeout values are set appropriately (30–60s for images, 60–120s for videos)

## Resources

- **Comprehensive navigation**: https://docs.modellix.ai/llms.txt
- **API Usage Guide**: https://docs.modellix.ai/ways-to-use/api
- **Error Handling & Best Practices**: https://docs.modellix.ai/ways-to-use/error-handling
- **Model API Reference**: https://docs.modellix.ai/api-reference/introduction

---

> For additional documentation and navigation, see: https://docs.modellix.ai/llms.txt