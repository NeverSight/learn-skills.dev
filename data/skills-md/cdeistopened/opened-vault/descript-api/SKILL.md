---
name: descript-api
description: Automate Descript project creation and editing via the Descript API (Early Access). Import media, prompt Underlord for edits, and poll job status.
---

# Descript API Skill

Programmatically create projects, import media, and edit via Agent Underlord - all without opening the Descript app.

**API Docs:** https://docs.descriptapi.com/openapi-experimental.html
**OpenAPI Spec (local):** `/Users/charliedeist/Downloads/openapi (1).json`
**Status:** Early Access (limited endpoints, evolving)
**Drive ID:** `e37dd160-e316-48a0-8923-17b71afee0de`

---

## Authentication

**Key:** `DESCRIPT_API_KEY` in `~/.zshrc` (also stored in `~/.descript-cli/config.json`)

**CRITICAL:** Use **lowercase** `authorization` header. Capitalized `Authorization` returns 401.

```bash
curl -s https://descriptapi.com/v1/status \
  -H "authorization: Bearer $DESCRIPT_API_KEY"
```

**CLI:** `descript-api` (npm `@descript/platform-cli`), config at `~/.descript-cli/config.json`

---

## Endpoints

| Method | Path | Status | Purpose |
|--------|------|--------|---------|
| POST | /jobs/import/project_media | Live | Import media, create project, transcribe |
| POST | /jobs/agent | Live | Underlord — AI edit via natural language prompt |
| GET | /jobs/{job_id} | Live | Poll job status |
| DELETE | /jobs/{job_id} | Live | Cancel running job |
| GET | /jobs | WIP | List jobs (not yet functional) |
| GET | /status | Live | Returns drive_id, confirms auth |
| GET | /published_projects/{slug} | Live | Get metadata + subtitles for published project |

---

## 1. Import Media → New Project

`POST https://descriptapi.com/v1/jobs/import/project_media`

Creates a new project, imports media from URLs, auto-transcribes, and optionally creates compositions.

```bash
curl -X POST https://descriptapi.com/v1/jobs/import/project_media \
  -H "authorization: Bearer $DESCRIPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Laura Froyen Episode",
    "add_media": {
      "ela-track.mp4": {
        "url": "https://example.com/ela-track.mp4"
      }
    },
    "add_compositions": [
      {
        "name": "Full Episode",
        "width": 1920,
        "height": 1080,
        "clips": [{ "media": "ela-track.mp4" }]
      }
    ]
  }'
```

**Response:** `{ "job_id": "...", "project_id": "...", "project_url": "https://web.descript.com/..." }`

**Key constraints:**
- Media URLs must be **publicly accessible** and support HTTP Range requests
- Sign URLs for 12-48 hours to avoid expiration during processing
- Importing into **existing projects is NOT yet supported** - always creates new
- FPS and language settings are accepted but ignored (auto-detected)

**Multitrack sequences** (for multicam/multi-speaker):
```json
"add_media": {
  "ela-track.mp4": { "url": "https://..." },
  "laura-track.mp4": { "url": "https://..." },
  "Multicam": {
    "tracks": [
      { "media": "ela-track.mp4", "offset": 0 },
      { "media": "laura-track.mp4", "offset": 0 }
    ]
  }
}
```

---

## 2. Agent Edit (Underlord)

`POST https://descriptapi.com/v1/jobs/agent`

Send a natural language prompt to Underlord for editing. **One-shot only** — no conversation or follow-ups.

```bash
curl -X POST https://descriptapi.com/v1/jobs/agent \
  -H "authorization: Bearer $DESCRIPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "YOUR_PROJECT_ID",
    "prompt": "Create a vertical 9:16 Instagram Reel, under 60 seconds. Extract the section where the guest talks about pilot training. Name the composition \"He got his pilot license before his driver license\". Apply the yellow text title layout. Add classic karaoke-style captions. Apply Studio Sound."
  }'
```

**Response:** `{ "job_id": "...", "drive_id": "...", "project_id": "...", "project_url": "..." }`
**Cost:** ~14-18 AI credits per composition, jobs take 30-90 seconds.

### Model Selection

The `model` parameter selects which AI model Underlord uses. Optional — defaults to Descript's default model.

```json
{
  "project_id": "...",
  "model": "haiku-4.5",
  "prompt": "..."
}
```

**Available models** (validated March 2026):

| Model | Variant |
|-------|---------|
| `haiku-4.5` | `haiku-4.5-underlord` |
| `sonnet-4.5` | `sonnet-4.5-underlord` |
| `sonnet-4.6` | `sonnet-4.6-underlord` |
| `opus-4.6` | `opus-4.6-underlord` |
| `gemini-3.1-pro` | — |
| `gpt-5.4` | — |
| `automatic` | Default (lets Descript choose) |

The `-underlord` variants may be fine-tuned for editing tasks. Invalid model values return 400 with the full allowed list.

**Model benchmarks (March 2026, Bria Bloom cold opens):**
- **haiku-4.5**: 3 credits per composition, follows clip extraction precisely (37 sec when asked for ~40 sec). Best for editing tasks.
- **gpt-5.4**: 16-22 credits per composition, over-interprets extraction prompts (produced 6 min clip when asked for ~40 sec). Grabs entire surrounding conversation instead of specific moments.
- **Recommendation**: Use `haiku-4.5` for clip extraction and cold open assembly. It's 5-7x cheaper and significantly more precise at following duration/extraction constraints.

### Underlord Prompt Engineering

**Structure:** Action + Context + Tone + Format + Constraints

**Rules:**
- Lead with a strong verb: "Create", "Extract", "Change", "Find"
- **Platform context**: "for Instagram Reels", "for TikTok", "for YouTube Shorts"
- **Dimensions**: Say "vertical 9:16 portrait (1080x1920)" for Reels/TikTok
- **Duration**: "under 60 seconds", "45-second clip"
- **Tone**: "humorous", "professional", "conversational", "fast-paced"
- **Audience**: "Gen Z", "hiring managers", "parents"
- Use **positive framing**: "Make sound conversational" NOT "Stop sounding robotic"
- Use **positive inclusion**: "Keep all content marketing mentions" NOT "Don't cut marketing parts"

### Underlord Capabilities

- Rough cuts from raw footage
- B-roll sourcing and insertion
- AI effects: Eye Contact, Studio Sound (can specify %, e.g. "Studio Sound 55%")
- Clip creation with aspect ratio changes
- Captions (classic karaoke style, bold, etc.)
- Title card generation
- Filler word + retake removal
- Audio mixing + background music
- **Layout pack application** (e.g. "yellow text title layout", "Berlin Carrot layout")
- Generated media (AI images/video for B-roll)
- Chapter marking by topic
- Aspect ratio changes on existing compositions

### Layout Packs

Layouts are visual templates that add text overlays, title cards, and styling. Descript's built-in layouts can be referenced by name:

```
"Apply the Berlin Carrot layout"
```

**Custom/workspace layout packs (e.g. "OpenEd Layouts") DO NOT work via API** as of March 2026. Underlord can see the pack exists (ID: `7501f9e0-2755-474e-b51e-2cd5af687abc`) but gets "Invalid layout pack ID" errors when querying individual layouts within it. Jobs that reference custom layouts either fail or fall back to generating ad-hoc visual elements.

**Practical workflow:** Create clips via API (extract, 9:16, captions, Studio Sound), then apply custom layouts (like "yellow text title" from OpenEd Layouts) manually in the Descript app — one click per clip.

**Naming the composition = on-screen text.** When you name a composition (e.g., "He got his pilot license before his driver license"), built-in layouts use that name as the on-screen title. Custom layouts require manual application but the composition name still persists for reference.

**Template system:** Templates are saved prompt workflows, accessible only from the Descript app UI (Home → Browse templates). NOT accessible via API.

### Fixing Dimensions on Existing Clips

If a clip was created in landscape, fix with a follow-up prompt:

```
"Find the composition called 'My Clip Name' and change its aspect ratio to 9:16 vertical portrait (1080x1920). Keep all existing edits, captions, and studio sound."
```

### Social Clip Creation Workflow

**For podcast clips destined for Instagram/TikTok/Shorts:**

1. **Read transcript** — Use `GET /published_projects/{slug}` if project is published, or read local polished transcripts
2. **Identify compelling moments** — Apply podcast-production skill's On-Screen Hook Standards (see `OpenEd Vault/.claude/skills/podcast-production/SKILL.md`)
3. **Craft on-screen hook** — This becomes the composition name. Follow complementarity principle: text should ADD context that makes audio land harder
4. **Send Underlord prompt:**
   ```
   Create a vertical 9:16 Instagram Reel, under 60 seconds.
   Extract the section where [SPEAKER] talks about [TOPIC].
   Name the composition "[ON-SCREEN HOOK TEXT]".
   Apply the [LAYOUT NAME] layout.
   Add classic karaoke-style captions.
   Apply Studio Sound.
   ```
5. **Poll job** until `job_state: "stopped"`
6. **Review in Descript** at `project_url`

**On-screen hook standards** (from podcast-production skill):
- **Complementarity principle:** Text ADDs to audio, doesn't just label it
- **"First 3 words" test:** First 3 words do 80% of the work — front-load the punch
- **Categories:** Polarizing, Counter-Intuitive, Direct Challenge, Curiosity Gap
- **Length variety:** Punchy (2-4 words), Statement (5-8), Narrative (9-15), Full quote (15+)

---

## 3. Poll Job Status

`GET https://descriptapi.com/v1/jobs/{job_id}`

```bash
curl -s "https://descriptapi.com/v1/jobs/$JOB_ID" \
  -H "authorization: Bearer $DESCRIPT_API_KEY"
```

**Job states:**
- `queued` - Waiting to start
- `running` - Processing (may include `progress.label`)
- `stopped` - Finished (check `result.status` for outcome: `success`, `partial`, `error`)
- `cancelled` - User cancelled

**Import job result includes:** `media_status` (per-file), `media_seconds_used`, `created_compositions`
**Agent job result includes:** `agent_response` (summary), `project_changed`, `ai_credits_used`

---

## 4. Cancel Job

`DELETE https://descriptapi.com/v1/jobs/{job_id}`

```bash
curl -X DELETE "https://descriptapi.com/v1/jobs/$JOB_ID" \
  -H "authorization: Bearer $DESCRIPT_API_KEY"
```

---

## 5. Published Projects (Transcript Access)

`GET https://descriptapi.com/v1/published_projects/{slug}`

Returns full WEBVTT subtitles (parseable for transcript text), plus: title, duration, publish_type, privacy, published_by.

**Getting slugs:** Share URLs from `share.descript.com/view/{slug}` — found in `OpenEd Vault/Published Content/Podcasts/*.md`

Useful for reading transcript content before prompting Underlord.

---

## Known Project IDs (OpenEd Podcasts)

| Title | Project ID | Share Slug |
|-------|-----------|------------|
| Matt & Ella | 73eb189c-d8a2-4083-bb6e-6db0d918dbcf | 0ipYl5nj8t7 |
| Matt's Daughter's story | 3d6ab90d-7586-44d8-b7eb-8b032675035b | phZc6KjiVUq |
| Do you homeschool? | 53207ee1-6a1f-4b80-b8df-2b8537c7691a | p5ktrepwirG |
| Jon England - Elijah Edit | c77cfb22-d96c-40ae-89fe-3c10b6030b08 | N2SPiMBMRAJ |
| Micro Schools on the Rise | a897a140-07b9-4990-bf02-3b20e6a48b15 | h0sdFLyjYJO |
| Industry vs. Education | 37b31dbf-37c0-4756-977e-2ce13bb87e03 | dRGNGLIqAuz |
| 2 best options if kid hates school | f2d0c580-345d-4923-9736-f6ccf93c66d9 | TJyXgzGA2Ei |
| Navigating Adoption Curve | 875c9a18-6852-4348-a4c0-728515e48c86 | WCJPJCOai7F |
| 019 - Krystle | d98fa476-a155-4151-8b24-4ecd52c63d69 | RefPSjlKRCD |
| 013 - Joey Mascio | ecb41f6d-100f-4ed5-8736-66edbd92e606 | RgCNPlAndar |
| Kerry McDonald | 55205b27-f63d-49be-a2f5-e8d76bd96b15 | UZYmhPZ9BzD |
| 008 - Mark Hyatt | 129f7165-382e-4872-8f5c-15863cf3958e | qWVa2T5DsAK |
| Matt Barnes | afef2962-b916-460d-bfa8-d32e111f39cd | amcWiaAh7dm |
| 017 - Jamie Lesko | e934e140-fead-4347-9a6a-a795a2c37926 | cZoBhD03G2e |
| 019 - Q&A episode | a6d6fa37-be73-4e32-9e6d-eee94c2fa93f | f5FrL8wMaPv |
| Where'd you get those from? | 9c9a81e4-a842-480e-b662-1950a7f7a457 | uPn3f7iRnFK |
| 005 - Andrea Fife | 972fc085-bd41-4592-a4df-dd0015497e42 | s12svKamJXN |
| Matt Beaudreau | 15e7423d-dd69-4b8d-8c96-b28e6a21d345 | tN5hzzprIDd |
| Dr. Laura Froyen | 5585b4c4-cd37-4202-b27a-d6bb512f7c11 | — |

---

## Known Issues & Lessons Learned

- **Lowercase `authorization` header** — capitalized `Authorization` returns 401
- **Single-quote the auth header when polling jobs** — the API key contains a colon (`dx_bearer_...:dx_secret_...`) which breaks shell variable expansion with double quotes. Use literal single quotes: `-H 'authorization: Bearer dx_bearer_...:dx_secret_...'` instead of `-H "authorization: Bearer $DESCRIPT_API_KEY"`
- API returns 403 when editing a project across drives
- Occasional 502 Bad Gateway during Agent jobs — retry once
- Agent may return success while certain actions are still processing
- Cannot import media into an existing project (new project each time)
- **Dimension control:** Include "vertical 9:16 portrait (1080x1920)" explicitly — otherwise clips may default to landscape. Fix existing clips with a follow-up aspect ratio change prompt.
- **Composition name = on-screen text** when using layout packs (e.g. yellow text title)
- **Generic prompts fail more often** — be specific about topic/speaker/timestamp range
- **Job failures:** If a job fails with "Job failed unexpectedly", retry with a more structured prompt (explicit platform + dimensions + content description)
- **No list-projects endpoint** — get project_ids from share URLs, previous imports, or web app URLs

---

## Rate Limiting

When you get a `429 Too Many Requests`, check headers:
- `Retry-After` - Seconds to wait
- `X-RateLimit-Remaining` - Requests left in window
- `X-RateLimit-Consumed` - Requests used in window

---

## CLI Alternative

```bash
npm install -g @descript/platform-cli@latest
descript-api config set api-key "YOUR_KEY"
descript-api import --name "My Project" --media "https://example.com/file.mp4"
descript-api agent --project-id YOUR_ID --prompt "Remove filler words"
```

Config stored at `~/.descript-cli/config.json`. CLI has built-in polling and interactive flows.

---

## Helper Script Pattern

```python
import requests
import time
import os

BASE = "https://descriptapi.com/v1"
TOKEN = os.environ.get("DESCRIPT_API_KEY") or "YOUR_KEY_HERE"
HEADERS = {"authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def agent_edit(project_id, prompt):
    body = {"project_id": project_id, "prompt": prompt}
    r = requests.post(f"{BASE}/jobs/agent", json=body, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def poll_job(job_id, interval=5, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        r = requests.get(f"{BASE}/jobs/{job_id}", headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        state = data.get("job_state", "unknown")
        if state in ("stopped", "cancelled"):
            return data
        label = data.get("progress", {}).get("label", "processing...")
        print(f"  [{state}] {label}")
        time.sleep(interval)
    raise TimeoutError(f"Job {job_id} timed out after {timeout}s")

def import_media(name, media_dict, compositions=None):
    body = {"project_name": name, "add_media": media_dict}
    if compositions:
        body["add_compositions"] = compositions
    r = requests.post(f"{BASE}/jobs/import/project_media", json=body, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_published_transcript(slug):
    r = requests.get(f"{BASE}/published_projects/{slug}", headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    # Parse WEBVTT subtitles to plain text
    vtt = data.get("subtitles", "")
    lines = [l for l in vtt.split("\n") if l and not l.startswith("WEBVTT") and "-->" not in l and not l.strip().isdigit()]
    return "\n".join(lines)
```

---

## Related Skills

- **On-screen hook writing:** `OpenEd Vault/.claude/skills/podcast-production/SKILL.md` (On-Screen Hook Standards section)
- **Text-on-broll (non-podcast):** `OpenEd Vault/.claude/skills/text-on-broll/SKILL.md`
- **Video caption creation:** `OpenEd Vault/.claude/skills/video-caption-creation/SKILL.md`
