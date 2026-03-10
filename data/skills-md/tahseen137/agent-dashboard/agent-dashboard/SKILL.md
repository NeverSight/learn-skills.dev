---
name: agent-dashboard
description: >
  Real-time agent dashboard for OpenClaw. Monitor active tasks, cron job health, issues,
  and action items from anywhere. Three setup tiers: (1) Zero-config canvas rendering
  inside OpenClaw, (2) GitHub Pages with 30-second polling — free, 2-minute setup,
  (3) Supabase Realtime + Vercel for instant websocket updates. All data stays on your
  machine. PIN-protected. No external services required for Tier 1. Tier 3 requires
  SUPABASE_URL and SUPABASE_ANON_KEY (no service_role key needed). Only operational
  status data is pushed (task names, cron status, timestamps) — never credentials,
  API keys, or file contents.
---

# Mission Control 🚀

A real-time dashboard showing what your OpenClaw agent is doing, cron job health, issues requiring attention, and recent activity. Check it from anywhere — your phone, your laptop, wherever.

## Quick Start

### Tier 1 — Canvas (Zero Setup) ⚡

No external services. The agent renders the dashboard directly in your OpenClaw session.

**How to use:**
```
Show me the mission control dashboard
```

The agent will:
1. Gather current state (active tasks, crons, etc.)
2. Generate a dashboard using the canvas tool
3. Present it inline in your session

That's it. No deploy, no accounts, nothing to configure.

---

### Tier 2 — GitHub Pages + Polling (Recommended) 🌐

Free hosting with 30-second auto-refresh. Takes 2 minutes to set up.

**Setup:**

1. **Create a repo:**
   ```bash
   gh repo create mission-control --public --clone
   cd mission-control
   ```

2. **Copy the dashboard:**
   ```bash
   mkdir -p data
   # Copy tier2-github.html to index.html
   # Copy assets/templates/dashboard-data.json to data/
   ```

3. **Edit `index.html`:**
   - Change `YOUR_PIN_HERE` to your chosen PIN

4. **Enable GitHub Pages:**
   - Go to repo Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/ (root)`

5. **Deploy:**
   ```bash
   git add -A && git commit -m "Initial deploy" && git push
   ```

Your dashboard is now live at `https://YOUR_USERNAME.github.io/mission-control/`

---

### Tier 3 — Supabase Realtime + Vercel (Premium) ⚡🔥

True websocket realtime — updates appear in under 1 second.

**Prerequisites:**
- Supabase account (free tier works)
- Vercel account (free tier works)

**Step 1: Create Supabase Table**

In your Supabase SQL Editor, run `assets/templates/setup-supabase.sql`.

**Step 2: Get Your Keys**

From Supabase Dashboard → Settings → API:
- Copy `SUPABASE_URL` (Project URL)
- Copy `SUPABASE_ANON_KEY` (anon public key)

That's it — no service_role key needed. The anon key handles both reads (dashboard) and writes (push script) via table-specific RLS.

**Step 3: Edit the Dashboard**

In `tier3-realtime.html`:
1. Replace `YOUR_SUPABASE_URL` with your project URL
2. Replace `YOUR_SUPABASE_ANON_KEY` with your anon key
3. Replace `YOUR_PIN_HERE` with your chosen PIN

**Step 4: Deploy to Vercel**

```bash
mkdir mission-control && cd mission-control
# Copy tier3-realtime.html as index.html
vercel deploy --prod
```

**Step 5: Configure Push Script**

```bash
export SUPABASE_URL="https://YOUR_PROJECT.supabase.co"
export SUPABASE_ANON_KEY="eyJ..."  # Same anon key used by the dashboard
```

---

## 🔄 Keeping It Fresh — Auto-Update Mechanism

**The dashboard updates itself automatically.** Here's how:

### 1. Cron Auto-Update (Every 30 Minutes)

Set up a cron job that collects data from OpenClaw APIs and pushes it:

```
Create a cron job called "Dashboard Update" that runs every 30 minutes.
It should:
1. Run `cron list` to get all cron job statuses, error counts, last run times
2. Run `sessions_list` to find any active sub-agents and their current tasks
3. Build the dashboard JSON from this API data
4. Push to Supabase (or git push for Tier 2)
```

**Data sources:** Only OpenClaw built-in APIs (`cron list`, `sessions_list`). No local files are read. Action items and recent activity are added manually via the "Manual Update" command below.

**Sample cron configuration:**
```yaml
name: Dashboard Update
schedule: "*/30 * * * *"  # Every 30 minutes
model: sonnet             # Fast model for quick updates
prompt: |
  Update the Mission Control dashboard:
  
  1. Run `cron list` to get job names, statuses, error counts, last run times
  2. Run `sessions_list` to find active sub-agents and their tasks
  3. Build JSON matching the dashboard schema from API data only
  4. Push to Supabase or GitHub
  
  Do not read local files. Only use cron list and sessions_list data.
```

### 2. Real-Time Event Pushes

Beyond the periodic cron, the agent pushes updates **immediately** when significant events happen:

- ✅ Task starts or finishes
- ❌ Errors or failures
- 🚀 Deploys complete
- 📧 Important notifications arrive

This means the dashboard reflects changes within seconds, not just every 30 minutes.

**How to enable:** When you start a major task, tell the agent:
```
After this deploy finishes, push an update to Mission Control.
```

### 3. Force Update Button

Every dashboard tier includes a **🔄 Update** button in the header:
- **Tier 2:** Re-fetches `dashboard-data.json` immediately
- **Tier 3:** Re-fetches from Supabase immediately
- Resets the "Updated X ago" timer
- Shows loading spinner while fetching

Use this when you want to confirm the latest state without waiting for auto-refresh.

### The Result

The combination of **periodic cron + real-time pushes + manual refresh** keeps your dashboard accurate at all times. You'll always see what your agent is actually doing.

---

## Dashboard Features

### 🚨 Action Required
Urgent items that need your attention. Highlighted at the top with priority badges (high/medium/low).

### ⚡ Active Now
What the agent is currently working on, with model name and duration.

### 📊 Products
Your product cards with live/testing/down status badges.

### ⏰ Cron Jobs
Table showing all scheduled jobs with status, last run time, and error counts. Click to expand error details.

### 📋 Recent Activity
Timeline of recent events and accomplishments.

### 🔴 Live Indicator (Tier 3 only)
Green pulsing dot shows websocket is connected. Flash animation when data updates.

---

## Requirements by Tier

| Tier | Tools Needed | External Accounts | Env Vars |
|------|-------------|-------------------|----------|
| **Tier 1** | None | None | None |
| **Tier 2** | `git`, `gh` CLI | GitHub (free) | `DASHBOARD_PIN` |
| **Tier 3** | `curl` | Supabase (free), Vercel (free) | See below |

### Environment Variables

| Variable | Required | Tier | Purpose |
|----------|----------|------|---------|
| `DASHBOARD_PIN` | No | All | PIN code for dashboard access (set directly in HTML config) |
| `SUPABASE_URL` | Yes | Tier 3 only | Your Supabase project URL |
| `SUPABASE_ANON_KEY` | Yes | Tier 3 only | Supabase anon key — used for both dashboard reads AND push script writes |

**Tier 1 needs zero env vars.** Tier 2 needs only a GitHub repo. Tier 3 needs only `SUPABASE_URL` and `SUPABASE_ANON_KEY` — no service_role key required.

### Permissions Used by OpenClaw

| Tier | Permissions | Why |
|------|-------------|-----|
| Tier 1 | None | Canvas is built into OpenClaw |
| Tier 2 | `exec` | To run `git push` to YOUR GitHub repo |
| Tier 3 | `exec` | To run `curl` to YOUR Supabase project |

No other permissions are used. No `read` permission needed — this skill does not access local files.

---

## Data Schema

The dashboard expects JSON in this format:

```json
{
  "lastUpdated": "2024-01-15T12:00:00Z",
  "actionRequired": [
    {
      "title": "Review PR #42",
      "url": "https://github.com/you/repo/pull/42",
      "priority": "high"
    }
  ],
  "activeNow": [
    {
      "task": "Deploying new feature",
      "model": "opus",
      "startedAt": "2024-01-15T11:45:00Z"
    }
  ],
  "products": [
    {
      "name": "My App",
      "url": "https://myapp.example.com",
      "status": "live",
      "lastChecked": "2024-01-15T12:00:00Z"
    }
  ],
  "crons": [
    {
      "name": "Daily Report",
      "schedule": "9:00 AM daily",
      "lastRun": "2024-01-15T09:00:00Z",
      "status": "ok",
      "errors": 0,
      "lastError": null
    }
  ],
  "recentActivity": [
    {
      "time": "2024-01-15T11:30:00Z",
      "event": "✅ Deployed v2.1.0 to production"
    }
  ]
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `lastUpdated` | ISO-8601 | When data was last refreshed |
| `actionRequired[].priority` | `high\|medium\|low` | Urgency level |
| `products[].status` | `live\|testing\|down` | Product health |
| `crons[].status` | `ok\|error\|paused` | Job status |

---

## Security & Privacy

**This is an instruction-only skill — no executable code, no install scripts, no third-party dependencies.**

### What This Skill Does and Doesn't Do

| ✅ Does | ❌ Doesn't |
|---------|-----------|
| Render HTML dashboards | Read local files (no HEARTBEAT.md, no memory files, no source code) |
| Push operational status to YOUR services | Send data to third-party services |
| Read OpenClaw APIs only (cron list, sessions_list) | Store, log, or transmit credentials |
| Use YOUR Supabase/GitHub accounts | Require service_role or admin keys |

### Exactly What Data Gets Pushed (Tier 2 & 3)

The dashboard pushes ONLY these fields — nothing else:

| Field | Example | Contains secrets? |
|-------|---------|-------------------|
| `actionRequired[].title` | "Review PR #42" | ❌ No |
| `activeNow[].task` | "Deploying v2.0" | ❌ No |
| `products[].name` | "My App" | ❌ No |
| `products[].url` | "https://myapp.com" | ❌ No (public URLs only) |
| `products[].status` | "live" | ❌ No |
| `crons[].name` | "Daily Report" | ❌ No |
| `crons[].status` | "ok" / "error" | ❌ No |
| `crons[].lastError` | "timeout after 30s" | ❌ No (error messages only) |
| `recentActivity[].event` | "✅ Deployed v2.1" | ❌ No |

**Never pushed:** passwords, API keys, tokens, file contents, database credentials, user data, or PII. The agent builds the JSON from operational status only — task names, timestamps, and status codes.

### What Data the Agent Reads

The auto-update cron uses ONLY OpenClaw built-in APIs:

| Source | What it extracts | Sensitive? |
|--------|-----------------|------------|
| `cron list` (OpenClaw API) | Job names, status, error counts | ❌ No |
| `sessions_list` (OpenClaw API) | Active task labels, models | ❌ No |

**No local files are read.** The cron does not access HEARTBEAT.md, memory files, source code, or any other files on disk. Action items and recent activity are added manually by the user via the "Manual Update" command.

### No Service Role Key Required

**This skill does NOT require a Supabase `service_role` key.** The anon key handles both reads and writes via table-specific RLS:

- The `dashboard_state` table allows anon `SELECT` and `UPDATE` (via RLS policy)
- The anon key can ONLY read/write this single table — it cannot access any other tables
- Worst case if someone gets your anon key: they can overwrite dashboard status data (not sensitive)
- The anon key is the same one already embedded in your client-side Supabase app

### Row Level Security (Tier 3)

The provided SQL (`setup-supabase.sql`) configures table-specific RLS:
- **`SELECT`:** Allowed for anon — dashboard can read status
- **`UPDATE`:** Allowed for anon on `dashboard_state` table only — push script can update status
- **Other tables:** Unaffected — the anon key's existing RLS policies on all other tables remain unchanged
- **No `DELETE`:** Anon cannot delete the dashboard row

### PIN Protection — Limitations

The client-side PIN prevents casual access, NOT determined attackers.

**For stronger protection:**
- **Tier 2:** Make your GitHub Pages repo **private** (GitHub Pro)
- **Tier 3:** Use Vercel's **password protection** (Pro plan) or add Supabase Auth
- **All tiers:** The dashboard only contains operational status — no secrets to steal even if accessed

---

## Files Included

```
agent-dashboard/
├── SKILL.md                      # This file
├── assets/
│   ├── tier1-canvas.html         # Lightweight canvas version
│   ├── tier2-github.html         # GitHub Pages + polling
│   ├── tier3-realtime.html       # Supabase Realtime version
│   └── push-dashboard.sh         # Push script for Tier 3
├── assets/templates/
│   ├── dashboard-data.json       # Sample data structure
│   └── setup-supabase.sql        # Supabase table setup
└── references/
    └── customization.md          # Theme and layout customization
```

---

## Troubleshooting

### Dashboard shows "Disconnected" (Tier 3)
- Check Supabase project is running
- Verify anon key is correct
- Ensure realtime is enabled on the table

### Data not updating (Tier 2)
- Check GitHub Pages is enabled
- Verify `data/dashboard-data.json` was pushed
- Hard refresh the page (Ctrl+Shift+R)
- Click the Force Update button to confirm data is stale

### PIN not working
- PINs are case-sensitive
- Check you're using the same PIN in HTML config

### Cron status not accurate
- Ensure your Dashboard Update cron is running (`cron list`)
- Check for errors in the cron output
- Manually run the update: "Update my Mission Control dashboard now"

---

## Credits

Built for the OpenClaw community. MIT License.
