---
name: tiktok-farm
description: |
  REST API client for the Farm TikTok app (slug: video-farm) on OfficeX. Discovers winning TikTok content via keyword or channel search, AI-filters with Gemini, schedules deduplicated reposts to volunteer publishers, and tracks proof-of-publication. Also supports manual mode (BYO content) where users skip discovery and inject their own videos/content directly into the scheduling pipeline. Use when: (1) Creating content discovery jobs by keyword or channel scrape, (2) Reviewing, approving, or rejecting discovered video results, (3) Scheduling approved videos with AI-generated captions/instructions for volunteers, (4) Viewing or managing a content calendar, (5) Submitting or checking proof-of-post from volunteers, (6) Checking NocoDB spreadsheet views, (7) Any TikTok theme page growth or content farming workflow, (8) Injecting your own videos into the scheduling/calendar pipeline (manual mode). Triggers: farm tiktok, daily tiktok, tiktok farm, tiktok content, theme page, tiktok repost, tiktok schedule, content farming, tiktok growth, volunteer post, tiktok calendar, tiktok proof, manual content, byo video.
---

# Farm TikTok — API Skill

Batch TikTok content curation engine on OfficeX. Discovers proven viral content via keyword or channel search, AI-filters it, schedules deduplicated reposts to volunteers via magic links, and tracks proof-of-publication. Also supports manual mode where you bring your own content and use the scheduling/calendar/webhook pipeline directly. Grows niche theme pages to 30k+ followers by reseeding winning content.

> **Get started on OfficeX:** Create a free account at [officex.app](https://officex.app) and install this app from the store: [officex.app/store/en/app/video-farm](https://officex.app/store/en/app/video-farm)

## Prerequisites

After installing the app on OfficeX, you'll receive credentials via the install webhook. Set these in your `.env`:

```bash
# Required — from OfficeX app install (agent_context)
OFFICEX_INSTALL_ID="your_install_id"        # Provided on install
OFFICEX_INSTALL_SECRET="your_install_secret" # Provided on install

# Optional — override the default API URL
FARM_TIKTOK_API_URL="https://video-farm-api.cloud.zoomgtm.com"
```

The `OFFICEX_INSTALL_ID` and `OFFICEX_INSTALL_SECRET` are provided automatically when you install the app on OfficeX. They are used to generate the Bearer token for API authentication:

```bash
# Bearer token = Base64(install_id:install_secret)
TOKEN=$(echo -n "${OFFICEX_INSTALL_ID}:${OFFICEX_INSTALL_SECRET}" | base64)
```

## Pipeline

### Search/Channel Mode (AI-powered discovery)
```
CREATE JOB → DISCOVER → AI ANALYZE → APPROVE → SCHEDULE → NOTIFY → PROOF
POST /jobs   TokInsight  Gemini 2.5    PATCH      POST       Email +   POST
             search or   match_score   /results   /results   webhook   /volunteer
             channel     tweet_text    approve    /:id/      at time   /:id/proof
             scrape      caption       schedule
```

### Manual Mode (BYO content)
```
CREATE JOB  →  ADD RESULTS  →  SCHEDULE  →  NOTIFY  →  PROOF
POST /jobs     POST /jobs/     POST         Email +    POST
mode=manual    :id/results     /results/    webhook    /volunteer/
                               :id/schedule at time    :id/proof
```

## Base URL

Use the `base_url` from your `agent_context`. Fallback:

| Stage      | URL                                                  |
| ---------- | ---------------------------------------------------- |
| Staging    | `https://video-farm-api-staging.cloud.zoomgtm.com` |
| Production | `https://video-farm-api.cloud.zoomgtm.com`         |

## Authentication

Bearer token = Base64 of `install_id:install_secret` (from `agent_context` or OfficeX install).

```typescript
const token = btoa(`${installId}:${installSecret}`);
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};
```

Volunteer endpoints (`/volunteer/*`) require no auth.

## TypeScript Types

```typescript
// === Enums ===
type JobStatus = 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
type PublishMode = 'MANUAL_REVIEW' | 'AI_REVIEW' | 'AUTO_APPROVED';
type JobMode = 'search' | 'channel' | 'manual';

// === Entities ===
interface Job {
  job_id: string;
  user_id: string;
  status: JobStatus;
  title?: string;
  job_mode?: JobMode;
  content_prompt?: string;
  channel_username?: string;
  output_quantity: number;
  filter_prompt?: string;
  instruction_prompt?: string;
  caption_prompt?: string;
  publish_mode: PublishMode;
  publish_prompt?: string;
  schedule_prompt?: string;
  on_job_finish_webhook?: string;
  on_job_finish_email?: string;
  on_schedule_webhook_default?: string;
  on_schedule_email_default?: string;
  on_proof_webhook_default?: string;
  on_proof_email_default?: string;
  destination_url?: string;
  tracer?: string;
  inbox_tracer?: string;
  results_created: number;
  results_approved: number;
  credits_spent: number;
  credits_reserved?: number;
  reservation_id?: string;
  notes?: string;
  bookmarked?: boolean;
  created_at: string;
  updated_at: string;
}

interface Result {
  result_id: string;
  job_id: string;
  user_id: string;
  tweet_text: string;
  original_video_url?: string;
  deduplicated_video_url?: string;
  tiktok_video_id?: string;
  tiktok_author?: string;
  tiktok_view_count?: number;
  tiktok_like_count?: number;
  tiktok_comment_count?: number;
  tiktok_caption?: string;
  match_score: number;             // 0-100
  ai_analysis: string;
  approval_decision?: string;
  approved: boolean;
  rejected: boolean;
  user_notes?: string;
  caption?: string;
  pin_comment?: string;
  instructions?: string;
  scheduled_datetime?: string;
  scheduled: boolean;
  on_schedule_email?: string;
  on_schedule_webhook?: string;
  on_proof_webhook?: string;
  on_proof_email?: string;
  destination_url?: string;
  password_protected?: string;
  tracer?: string;
  inbox_tracer?: string;
  bookmarked?: boolean;
}

interface Scheduled {
  scheduled_id: string;
  result_id: string;
  job_id: string;
  user_id: string;
  tweet_text: string;
  status?: 'pending' | 'completed';
  credits_consumed?: number;
  volunteer_magic_link?: string;
  original_video_url?: string;
  deduplicated_video_url?: string;
  dedup_status?: 'pending' | 'completed' | 'failed';
  caption?: string;
  pin_comment?: string;
  instructions?: string;
  instruction_prompt?: string;
  scheduled_datetime: string;
  on_schedule_email?: string;
  on_schedule_webhook?: string;
  on_proof_webhook?: string;
  on_proof_email?: string;
  destination_url?: string;
  password_protected?: string;
  fired: boolean;
  fired_at?: string;
  proof_url?: string;
  proof_timestamp?: string;
  reported_by?: string;
  tracer?: string;
  inbox_tracer?: string;
}

// === Request Types ===
interface CreateJobRequest {
  job_mode?: JobMode;                    // default: 'search'. Use 'manual' for BYO content
  content_prompt?: string;               // keywords (search) or description (channel). Optional for manual
  channel_username?: string;            // required if job_mode='channel'
  output_quantity?: number;             // default: 5
  filter_prompt?: string;
  caption_prompt?: string;
  instruction_prompt?: string;
  publish_mode?: PublishMode;           // default: 'MANUAL_REVIEW'
  publish_prompt?: string;
  schedule_prompt?: string;
  on_job_finish_webhook?: string;
  on_job_finish_email?: string;
  on_schedule_webhook_default?: string;
  on_schedule_email_default?: string;
  on_proof_webhook_default?: string;
  on_proof_email_default?: string;
  destination_url?: string;
  tracer?: string;
  inbox_tracer?: string;
  notes?: string;
  bookmarked?: boolean;
}

interface UpdateResultRequest {
  approved?: boolean;
  rejected?: boolean;
  user_notes?: string;
  caption?: string;
  pin_comment?: string;
  instructions?: string;
  scheduled_datetime?: string;
  on_schedule_email?: string;
  on_schedule_webhook?: string;
  on_proof_webhook?: string;
  on_proof_email?: string;
  destination_url?: string;
  password_protected?: string;
}

interface CreateManualResultRequest {
  post_text?: string;
  original_video_url?: string;
  caption?: string;
  pin_comment?: string;
  instructions?: string;
  scheduled_datetime?: string;
  on_schedule_email?: string;
  on_schedule_webhook?: string;
  on_proof_webhook?: string;
  on_proof_email?: string;
  destination_url?: string;
  password_protected?: string;
  approved?: boolean;                  // default: true
  match_score?: number;                // default: 100
  ai_analysis?: string;               // default: 'Manually created result'
  tiktok_video_id?: string;
  tiktok_author?: string;
  tiktok_view_count?: number;
  tiktok_like_count?: number;
  tiktok_comment_count?: number;
  tiktok_caption?: string;
  user_notes?: string;
  tracer?: string;
  inbox_tracer?: string;
}

interface UpdateScheduledRequest {
  tweet_text?: string;
  scheduled_datetime?: string;
  on_schedule_email?: string;
  on_schedule_webhook?: string;
  on_proof_webhook?: string;
  on_proof_email?: string;
  destination_url?: string;
  instruction_prompt?: string;
}

interface SubmitProofRequest {
  proof_url: string;
  reported_by?: string;
}

// === Response Envelope ===
interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: { code: string; message: string };
}

interface PaginatedResponse<T> {
  items: T[];
  next_cursor?: string;
  total?: number;
}

// === Webhook Events (outbound from app) ===
interface WebhookEvent<T = unknown> {
  id: string;
  action: 'SCHEDULE_FIRED' | 'PROOF_SUBMITTED';
  payload: T;
  timestamp: string;
}

interface ScheduleFiredPayload {
  scheduled_id: string;
  result_id: string;
  job_id: string;
  user_id: string;
  original_video_url: string;
  deduplicated_video_url: string;
  caption: string;
  pin_comment: string;
  instructions?: string;
  volunteer_magic_link: string;
  submit_proof_endpoint: string;
  tracer?: string;
  inbox_tracer?: string;
}

interface ProofSubmittedPayload {
  scheduled_id: string;
  result_id: string;
  job_id: string;
  user_id: string;
  proof_url: string;
  proof_timestamp: string;
  tweet_text: string;
  tracer?: string;
  inbox_tracer?: string;
}
```

## REST API Reference

All endpoints return `ApiResponse<T>`. Authenticated routes require `Authorization: Bearer <token>`.

### Health

```
GET /health → { status: 'healthy', stage, timestamp }
```

### Auth

```
POST /auth/login
Body: { officex_customer_id, officex_install_id, officex_install_secret }
→ { user, token }

GET /auth/me → User
```

### Jobs

```
GET    /jobs?limit=50&cursor=<token>         → PaginatedResponse<Job>
POST   /jobs                                 → 201 { job_id, status:'PENDING', estimated_cost }
GET    /jobs/:job_id                         → Job
PATCH  /jobs/:job_id { notes?, bookmarked? } → Job
DELETE /jobs/:job_id                         → { deleted: true }
POST   /jobs/:job_id/resync-nocodb           → { job_synced: true, results_synced: number }
```

`POST /jobs` reserves OfficeX credits and invokes async processing. Job status progresses: `PENDING → PROCESSING → COMPLETED|FAILED`. For `job_mode='manual'`, the job is created in `COMPLETED` status immediately with no credit reservation — results are added via `POST /jobs/:job_id/results`.

### Results

```
GET   /jobs/:job_id/results?limit=50&cursor=<token>      → PaginatedResponse<Result>
POST  /jobs/:job_id/results CreateManualResultRequest     → 201 Result (manual jobs only)
GET   /results/:result_id                                 → Result
PATCH /results/:result_id UpdateResultRequest             → Result
POST  /results/:result_id/schedule                        → 201 Scheduled
```

`POST /jobs/:job_id/results` creates a result directly on a manual job. Only works when `job_mode='manual'`. Results default to `approved=true`. Use this to inject your own content (videos you created externally, curated links, etc.) into the scheduling/calendar/webhook pipeline.

Scheduling requires `approved === true` and `scheduled === false`. If no `scheduled_datetime`, the AI uses `schedule_prompt` or defaults to +24h. Triggers async video deduplication.

### Scheduled

```
GET    /scheduled?limit=100&cursor=<token>&start_date=ISO&end_date=ISO → PaginatedResponse<Scheduled>
GET    /scheduled/:scheduled_id                                        → Scheduled
PATCH  /scheduled/:scheduled_id UpdateScheduledRequest                 → Scheduled
DELETE /scheduled/:scheduled_id                                        → { message: 'Scheduled entry deleted' }
POST   /scheduled/:scheduled_id/fire-now                               → { message, scheduled_id }
```

Changing `scheduled_datetime` via PATCH deletes and recreates the item (sort key contains datetime). Fails with `ALREADY_FIRED` if the post has already fired.

`POST /scheduled/:scheduled_id/fire-now` immediately invokes the notifier (email + webhook) without waiting for the scheduled time. Fails if already fired.

### Calendar

```
GET /calendar/month/:year/:month → { year, month, days: Record<string, Scheduled[]>, total }
GET /calendar/week/:year/:week   → { year, week, days: Record<string, Scheduled[]>, total }
```

### Volunteer (No Auth)

```
GET /volunteer/:scheduled_id
→ { scheduled_id, tweet_text, scheduled_datetime, destination_url, fired, proof_url,
    proof_timestamp, inbox_tracer, instruction_prompt,
    batch?: { total, completed, current_index, next_task_id } }

POST /volunteer/:scheduled_id/proof
Body: { proof_url, reported_by? }
→ { proof_url, proof_timestamp, has_next_task, next_task_link? }
```

### NocoDB Views

```
GET /nocodb/views                     → { jobs_view_url?, results_view_url?, scheduled_view_url? }
GET /nocodb/jobs/:job_id/results-view → { results_view_url?, view_url? }
```

### Webhooks (OfficeX → App)

```
POST /webhooks/officex
Body: { event: 'INSTALL'|'UNINSTALL'|'RATE_LIMIT_CHANGE', payload, uuid }
INSTALL → { agent_context: { api_url, auth_token, install_id } }
```

## Outbound Webhook Events

| Event             | When                  | Key Fields                                                                                    |
| ----------------- | --------------------- | --------------------------------------------------------------------------------------------- |
| `SCHEDULE_FIRED`  | At scheduled_datetime | scheduled_id, deduplicated_video_url, caption, pin_comment, volunteer_magic_link, submit_proof_endpoint |
| `PROOF_SUBMITTED` | Volunteer submits proof | scheduled_id, proof_url, proof_timestamp, tweet_text, tracer, inbox_tracer                  |

## Error Codes

| Code                    | HTTP | Meaning                             |
| ----------------------- | ---- | ----------------------------------- |
| `INVALID_REQUEST`       | 400  | Missing/invalid fields              |
| `UNAUTHORIZED`          | 401  | Missing or invalid auth             |
| `INVALID_CREDENTIALS`   | 401  | Install credentials mismatch        |
| `MISSING_CREDENTIALS`   | 400  | Missing install_id or install_secret|
| `NOT_APPROVED`          | 400  | Must approve before scheduling      |
| `ALREADY_SCHEDULED`     | 400  | Result already scheduled            |
| `ALREADY_FIRED`         | 400  | Cannot modify a fired post          |
| `MISSING_PROOF_URL`     | 400  | proof_url is required               |
| `JOB_IN_PROGRESS`       | 400  | Cannot delete a processing job      |
| `INVALID_DATE`          | 400  | Invalid year/month/week             |
| `RESERVATION_FAILED`    | 402  | Insufficient credits                |
| `JOB_NOT_FOUND`         | 404  | Job not found                       |
| `RESULT_NOT_FOUND`      | 404  | Result not found                    |
| `SCHEDULED_NOT_FOUND`   | 404  | Scheduled post not found            |
| `USER_NOT_FOUND`        | 404  | User not found                      |

## fetch Examples

### Setup

```typescript
const API = 'https://video-farm-api.cloud.zoomgtm.com'; // or from agent_context.api_url
const token = btoa(`${installId}:${installSecret}`);
const auth = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
```

### Create a keyword search job

```typescript
const res = await fetch(`${API}/jobs`, {
  method: 'POST',
  headers: auth,
  body: JSON.stringify({
    job_mode: 'search',
    content_prompt: 'viral fitness transformation clips',
    output_quantity: 10,
    filter_prompt: 'Only videos with 50k+ views showing real transformations',
    publish_mode: 'AI_REVIEW',
    caption_prompt: 'Motivational tone. Include #fitness #transformation #gymtok',
    schedule_prompt: 'Schedule 2 per day, 9am and 6pm EST',
    on_schedule_email_default: 'volunteer@example.com',
    inbox_tracer: 'fitness-batch-001'
  })
});
const { data } = await res.json();
// { job_id: 'uuid', status: 'PENDING', estimated_cost: 42.22 }
```

### Create a channel scrape job

```typescript
const res = await fetch(`${API}/jobs`, {
  method: 'POST',
  headers: auth,
  body: JSON.stringify({
    job_mode: 'channel',
    channel_username: 'alexhormozi',
    output_quantity: 5,
    publish_mode: 'MANUAL_REVIEW',
    caption_prompt: 'Rewrite in first person. Add #entrepreneurship #business',
    instruction_prompt: 'Post to @our_brand. Add 3 relevant hashtags in comments.'
  })
});
```

### Create a manual job (BYO content, skip discovery)

```typescript
const res = await fetch(`${API}/jobs`, {
  method: 'POST',
  headers: auth,
  body: JSON.stringify({
    job_mode: 'manual',
    schedule_prompt: 'Schedule 3 per day, 8am 12pm 6pm EST',
    on_schedule_email_default: 'volunteer@example.com',
    on_proof_webhook_default: 'https://hooks.example.com/proof',
    inbox_tracer: 'my-batch-001',
    notes: 'Q1 content campaign'
  })
});
const { data } = await res.json();
// { job_id: 'uuid', status: 'COMPLETED', estimated_cost: 0 }
```

### Add results to a manual job

```typescript
// Add your own video as a result
await fetch(`${API}/jobs/${jobId}/results`, {
  method: 'POST',
  headers: auth,
  body: JSON.stringify({
    post_text: 'Check out this amazing transformation! #fitness',
    original_video_url: 'https://example.com/my-video.mp4',
    caption: 'Day 30 of my fitness journey #gymtok',
    instructions: 'Post to @fitness_page with hashtags in first comment',
    scheduled_datetime: '2026-03-15T09:00:00Z'
  })
});
// Result is created with approved=true, ready to schedule
```

### Poll job until complete

```typescript
const poll = async (jobId: string): Promise<Job> => {
  while (true) {
    const { data } = await fetch(`${API}/jobs/${jobId}`, { headers: auth }).then(r => r.json());
    if (data.status === 'COMPLETED' || data.status === 'FAILED') return data;
    await new Promise(r => setTimeout(r, 5000));
  }
};
```

### List and approve results

```typescript
const { data } = await fetch(`${API}/jobs/${jobId}/results`, { headers: auth }).then(r => r.json());

for (const result of data.items.filter((r: Result) => r.match_score >= 80 && !r.approved)) {
  await fetch(`${API}/results/${result.result_id}`, {
    method: 'PATCH',
    headers: auth,
    body: JSON.stringify({
      approved: true,
      caption: 'My custom caption #fyp #viral',
      scheduled_datetime: '2026-02-10T15:00:00Z',
      on_schedule_email: 'volunteer@example.com'
    })
  });
}
```

### Schedule an approved result

```typescript
const { data } = await fetch(`${API}/results/${resultId}/schedule`, {
  method: 'POST',
  headers: auth
}).then(r => r.json());
// data.volunteer_magic_link — send to your volunteer
// data.dedup_status === 'pending' — video processing in background
```

### Get calendar month view

```typescript
const { data } = await fetch(`${API}/calendar/month/2026/2`, {
  headers: auth
}).then(r => r.json());
// data.days = { '2026-02-10': [Scheduled, ...], '2026-02-11': [...] }
```

### Fire a scheduled post immediately

```typescript
await fetch(`${API}/scheduled/${scheduledId}/fire-now`, {
  method: 'POST',
  headers: auth
});
```

### Reschedule a post

```typescript
await fetch(`${API}/scheduled/${scheduledId}`, {
  method: 'PATCH',
  headers: auth,
  body: JSON.stringify({ scheduled_datetime: '2026-02-12T10:00:00Z' })
});
```

### Submit proof (volunteer, no auth)

```typescript
const { data } = await fetch(`${API}/volunteer/${scheduledId}/proof`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    proof_url: 'https://www.tiktok.com/@our_brand/video/1234567890',
    reported_by: 'volunteer@example.com'
  })
}).then(r => r.json());
// { proof_url, proof_timestamp, has_next_task, next_task_link }
```

## Key Concepts

- **Job Modes:** `search` (keyword query via TokInsight), `channel` (scrape @username's videos), or `manual` (BYO content — skip discovery, add results directly via `POST /jobs/:job_id/results`).
- **Publish Modes:** `MANUAL_REVIEW` (you approve each), `AI_REVIEW` (Gemini decides), `AUTO_APPROVED` (auto-approve if match_score >= 70).
- **Video Deduplication:** After scheduling, the video is slightly randomized (zoom, tilt, saturation, speed) to avoid TikTok duplicate detection. Track via `dedup_status`.
- **Tracers:** `tracer` = unique ID per job. `inbox_tracer` = batch grouping key for volunteers so they can navigate between tasks.
- **Volunteer Magic Links:** No-auth links sent to volunteers. Format: `{frontend}/volunteer/{scheduled_id}?inbox_tracer={tracer}`.
- **Scheduling:** An hourly cron finds posts in the next 60min and creates EventBridge rules. At `scheduled_datetime`, the Notifier fires emails + webhooks. Use `POST /scheduled/:id/fire-now` to bypass the schedule and fire immediately.
- **Rescheduling:** Changing `scheduled_datetime` via PATCH is a delete+recreate operation. Fails if already fired.
- **Credit Cost:** ~4.2 credits per video (includes TokInsight search, Gemini analysis, video dedup, email notification). A 5-video job costs ~21 credits. Jobs with `schedule_prompt` or `instruction_prompt` add ~0.04 credits per video per prompt. Manual mode jobs have no upfront cost — credits are only consumed when results are scheduled (dedup + email).
