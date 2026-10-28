---
name: hermes-labyrinth-observability
description: Read-only observability dashboard plugin for Hermes Agent — journeys, crossings, guideposts, and reports.
triggers:
  - add hermes labyrinth to my agent setup
  - how do I observe my hermes agent runs
  - install hermes labyrinth plugin
  - view agent journey crossings dashboard
  - export hermes agent report
  - debug autonomous agent with labyrinth
  - set up hermes observability plugin
  - how do I read hermes labyrinth API
---

# Hermes Labyrinth

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Hermes Labyrinth is a **read-only observability dashboard plugin** for [Hermes Agent](https://github.com/NousResearch/hermes-agent). It turns autonomous agent runs into a navigable map of **crossings** (prompts, tool calls, tool results, failures, model switches, subagents, approvals, memory hits, redactions, context compression, cron runs) with exportable evidence. It is not a chat UI — it is a black-box recorder for agents moving through unknown work.

---

## Install

### Plugin Directory Install

```bash
mkdir -p ~/.hermes/plugins
git clone https://github.com/stainlu/hermes-labyrinth.git ~/.hermes/plugins/hermes-labyrinth
```

Start or restart the Hermes dashboard:

```bash
hermes dashboard
```

If the dashboard is already running, rescan plugins without restarting:

```bash
curl http://127.0.0.1:9119/api/dashboard/plugins/rescan
```

Open the dashboard in your browser and select the **Labyrinth** tab.

### Optional Theme

```bash
mkdir -p ~/.hermes/dashboard-themes
cp ~/.hermes/plugins/hermes-labyrinth/theme/hermes-labyrinth.yaml ~/.hermes/dashboard-themes/
```

---

## What Labyrinth Tracks

| View | Contents |
|---|---|
| **Journey index** | Recent CLI, dashboard, gateway, cron, and delegated work |
| **Labyrinth map** | Ordered crossings through a selected agent journey |
| **Inspector** | Input, output, duration, status, evidence, guideposts per crossing |
| **Guideposts** | Generated observations backed by local evidence |
| **Skill atlas** | Bundled, optional, external, and user skill inventory |
| **Cron gate** | Scheduled autonomy, next runs, last failures, workdirs |
| **Model ferry** | Model/provider transitions across sessions |
| **Reports** | Redacted Markdown and JSON exports for one journey |

---

## API Surface

All endpoints are read-only. The plugin API is served by Hermes dashboard at:

```
http://127.0.0.1:9119/api/plugins/hermes-labyrinth/
```

### Endpoints

```
GET /api/plugins/hermes-labyrinth/health
GET /api/plugins/hermes-labyrinth/journeys
GET /api/plugins/hermes-labyrinth/journeys/{journey_id}
GET /api/plugins/hermes-labyrinth/journeys/{journey_id}/crossings
GET /api/plugins/hermes-labyrinth/skills
GET /api/plugins/hermes-labyrinth/cron
GET /api/plugins/hermes-labyrinth/guideposts
GET /api/plugins/hermes-labyrinth/reports/{journey_id}.json
GET /api/plugins/hermes-labyrinth/reports/{journey_id}.md
```

### Example: Fetch All Journeys

```bash
curl http://127.0.0.1:9119/api/plugins/hermes-labyrinth/journeys | jq .
```

### Example: Fetch Crossings for a Journey

```bash
JOURNEY_ID="your-journey-id"
curl "http://127.0.0.1:9119/api/plugins/hermes-labyrinth/journeys/${JOURNEY_ID}/crossings" | jq .
```

### Example: Export a Journey Report as Markdown

```bash
JOURNEY_ID="your-journey-id"
curl "http://127.0.0.1:9119/api/plugins/hermes-labyrinth/reports/${JOURNEY_ID}.md" > report.md
```

### Example: Export a Journey Report as JSON

```bash
JOURNEY_ID="your-journey-id"
curl "http://127.0.0.1:9119/api/plugins/hermes-labyrinth/reports/${JOURNEY_ID}.json" > report.json
```

### Example: Health Check

```bash
curl http://127.0.0.1:9119/api/plugins/hermes-labyrinth/health
```

---

## Python API Client Examples

The plugin backend lives at `dashboard/plugin_api.py`. You can also call the HTTP API from any language. Here are Python examples:

```python
import urllib.request
import json

BASE = "http://127.0.0.1:9119/api/plugins/hermes-labyrinth"

def get_journeys():
    with urllib.request.urlopen(f"{BASE}/journeys") as r:
        return json.loads(r.read())

def get_crossings(journey_id: str):
    with urllib.request.urlopen(f"{BASE}/journeys/{journey_id}/crossings") as r:
        return json.loads(r.read())

def get_report_json(journey_id: str):
    with urllib.request.urlopen(f"{BASE}/reports/{journey_id}.json") as r:
        return json.loads(r.read())

def get_report_md(journey_id: str) -> str:
    with urllib.request.urlopen(f"{BASE}/reports/{journey_id}.md") as r:
        return r.read().decode("utf-8")

# Usage
journeys = get_journeys()
for j in journeys:
    print(j["id"], j.get("status"), j.get("started_at"))
```

### Iterate Crossings and Inspect Tool Calls

```python
import urllib.request
import json

BASE = "http://127.0.0.1:9119/api/plugins/hermes-labyrinth"

def inspect_tool_crossings(journey_id: str):
    with urllib.request.urlopen(f"{BASE}/journeys/{journey_id}/crossings") as r:
        crossings = json.loads(r.read())

    for crossing in crossings:
        if crossing.get("type") == "tool_call":
            print(f"Tool: {crossing['tool']}")
            print(f"  Status:   {crossing.get('status')}")
            print(f"  Duration: {crossing.get('duration_ms')}ms")
            print(f"  Input:    {json.dumps(crossing.get('input', {}))[:200]}")
            print()

inspect_tool_crossings("your-journey-id")
```

### Download and Save All Reports for Recent Journeys

```python
import urllib.request
import json
import pathlib

BASE = "http://127.0.0.1:9119/api/plugins/hermes-labyrinth"
OUT = pathlib.Path("./labyrinth-reports")
OUT.mkdir(exist_ok=True)

with urllib.request.urlopen(f"{BASE}/journeys") as r:
    journeys = json.loads(r.read())

for j in journeys[:10]:  # last 10 journeys
    jid = j["id"]
    try:
        with urllib.request.urlopen(f"{BASE}/reports/{jid}.json") as r:
            (OUT / f"{jid}.json").write_bytes(r.read())
        with urllib.request.urlopen(f"{BASE}/reports/{jid}.md") as r:
            (OUT / f"{jid}.md").write_bytes(r.read())
        print(f"Saved reports for {jid}")
    except Exception as e:
        print(f"Failed {jid}: {e}")
```

---

## JavaScript / Frontend API Examples

The frontend plugin bundle lives in `dashboard/dist/`. If you're extending the UI or writing a custom integration:

```javascript
const BASE = "http://127.0.0.1:9119/api/plugins/hermes-labyrinth";

async function fetchJourneys() {
  const res = await fetch(`${BASE}/journeys`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function fetchCrossings(journeyId) {
  const res = await fetch(`${BASE}/journeys/${journeyId}/crossings`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function fetchReportMarkdown(journeyId) {
  const res = await fetch(`${BASE}/reports/${journeyId}.md`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.text();
}

// Example: log all failed crossings in the most recent journey
async function logFailures() {
  const journeys = await fetchJourneys();
  if (!journeys.length) return;
  const crossings = await fetchCrossings(journeys[0].id);
  const failed = crossings.filter(c => c.status === "failure" || c.status === "error");
  console.table(failed.map(c => ({
    type: c.type,
    tool: c.tool ?? "-",
    duration_ms: c.duration_ms,
    error: c.error?.slice(0, 120),
  })));
}

logFailures();
```

---

## Build & Development

The frontend is built from `src/parts/*.js` + `src/labyrinth.css` into `dashboard/dist/`. The demo `index.html` is generated with content-hash query strings.

```bash
# Build dashboard/dist and index.html
npm run build

# Run reproducibility and parse checks
npm run check

# Run browser smoke tests (headless Chrome)
npm run smoke

# Smoke-test the deployed GitHub Pages demo
npm run smoke:live

# Run all tests (build checks, fixture tests, smoke)
npm test
```

### Full Test Suite

```bash
npm test
```

Runs:
- Reproducible build checks for `dashboard/dist` and `index.html`
- Frontend JavaScript parse checks
- Backend Python parse checks
- API normalization fixture tests (including numeric Hermes timestamps)
- Packed-artifact and dead-control regressions
- Headless Chrome smoke coverage for map modes, route changes, search, dataset switching, and threshold filter

---

## Repository Layout

```
.
├── dashboard/
│   ├── manifest.json        # Hermes dashboard plugin manifest
│   ├── plugin_api.py        # Read-only API over local Hermes state
│   └── dist/                # Generated dashboard plugin bundle
├── docs/
│   ├── CONCEPT.md
│   ├── DESIGN_BRIEF.md
│   └── FUNCTIONAL_SPEC.md
├── scripts/
│   ├── build-plugin.mjs     # Builds dashboard/dist and index.html
│   ├── smoke-demo.mjs       # Browser smoke test for public demo
│   ├── test-plugin-api.py   # Fixture tests for API normalization
│   └── verify.mjs           # Local verification checks
├── src/
│   ├── demo/                # GitHub Pages demo source
│   ├── parts/               # Ordered frontend source chunks
│   └── labyrinth.css        # Frontend CSS source
├── theme/
│   └── hermes-labyrinth.yaml
├── index.html               # Generated GitHub Pages demo
└── package.json
```

---

## Architecture

```
Hermes local state
  ├─ state.db sessions/messages
  ├─ skills directories
  └─ cron config
        ↓
dashboard/plugin_api.py
        ↓
/api/plugins/hermes-labyrinth/*
        ↓
src/parts/*.js + src/labyrinth.css
        ↓ npm run build
dashboard/dist/*
        ↓
Hermes dashboard tab: Labyrinth
```

---

## Data Policy (Important)

- **Read-only by design**: does not start, stop, resume, mutate, or create Hermes sessions.
- **Secret redaction**: applied to previews and reports.
- **Unknown fields**: stay unknown — not silently dropped.
- **Reports**: generated from local Hermes state only.
- **Public demo**: uses sample/mocked data — not live telemetry.

---

## Common Patterns

### Check Plugin Health Before Querying

```python
import urllib.request, json

def is_labyrinth_healthy() -> bool:
    try:
        with urllib.request.urlopen(
            "http://127.0.0.1:9119/api/plugins/hermes-labyrinth/health",
            timeout=3
        ) as r:
            data = json.loads(r.read())
            return data.get("status") == "ok"
    except Exception:
        return False

if not is_labyrinth_healthy():
    print("Labyrinth plugin not reachable — is `hermes dashboard` running?")
```

### Filter Journeys by Type

```python
import urllib.request, json

BASE = "http://127.0.0.1:9119/api/plugins/hermes-labyrinth"

with urllib.request.urlopen(f"{BASE}/journeys") as r:
    journeys = json.loads(r.read())

# Filter to only cron-triggered journeys
cron_journeys = [j for j in journeys if j.get("origin") == "cron"]

# Filter to only failed journeys
failed_journeys = [j for j in journeys if j.get("status") in ("failure", "error")]
```

### Summarize Crossing Types in a Journey

```python
from collections import Counter
import urllib.request, json

BASE = "http://127.0.0.1:9119/api/plugins/hermes-labyrinth"

def summarize_journey(journey_id: str):
    with urllib.request.urlopen(f"{BASE}/journeys/{journey_id}/crossings") as r:
        crossings = json.loads(r.read())
    counts = Counter(c.get("type", "unknown") for c in crossings)
    total_ms = sum(c.get("duration_ms", 0) for c in crossings)
    print(f"Journey {journey_id}: {len(crossings)} crossings, {total_ms}ms total")
    for ctype, n in counts.most_common():
        print(f"  {ctype}: {n}")
```

---

## Troubleshooting

### Plugin tab not appearing in dashboard

1. Confirm clone location: `ls ~/.hermes/plugins/hermes-labyrinth/dashboard/manifest.json`
2. Restart `hermes dashboard` or rescan: `curl http://127.0.0.1:9119/api/dashboard/plugins/rescan`
3. Check `manifest.json` is valid JSON.

### API returns 404

- Verify the plugin loaded: `curl http://127.0.0.1:9119/api/plugins/hermes-labyrinth/health`
- Confirm `hermes dashboard` is running on port `9119`.

### Build artifacts out of date

```bash
npm run build
# Then verify reproducibility
npm run check
```

### Smoke tests fail locally

- Requires headless Chrome/Chromium available in `PATH`.
- Run `npm run smoke` for local, `npm run smoke:live` for the deployed Pages demo.

### Reports contain redacted fields

This is expected. Labyrinth applies secret redaction to all previews and exports by design. Raw values are only accessible inside the Hermes process itself.

### Numeric timestamps in API responses

The API normalization layer handles numeric Hermes timestamps automatically (covered by fixture tests in `scripts/test-plugin-api.py`). If you consume the API directly, expect either ISO 8601 strings or Unix epoch integers in timestamp fields.

---

## Links

- **Live demo**: https://stainlu.github.io/hermes-labyrinth/
- **Hermes Agent**: https://github.com/NousResearch/hermes-agent
- **Release v0.1.0**: https://github.com/stainlu/hermes-labyrinth/releases/tag/v0.1.0
- **License**: MIT
