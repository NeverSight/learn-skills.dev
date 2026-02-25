---
name: weekly-analytics
description: >
  Weekly analytics report combining GA4, Google Search Console, and Microsoft Clarity 
  into a premium HTML email. Use for automated Sunday cron jobs that generate weekly 
  product analytics reports. Tracks users, sessions, pageviews, SEO performance (queries, 
  impressions, CTR, position), UX friction (dead clicks, rage clicks, quickbacks), and 
  week-over-week trends. Includes accountability tracking (did we do what we said?), 
  prioritized recommendations with impact/effort ratings, and actionable checklists.
  Persona: $15K/month SEO consultant. Outputs: HTML email + chat summary.
license: MIT
compatibility: Requires Node.js 18+, googleapis npm package
allowed-tools: Read Bash(node:*) Bash(git:*) Bash(curl:*)
metadata:
  author: 0juano
  version: "1.0.0"
  openclaw:
    emoji: "📊"
    requires:
      bins: ["node"]
---

# Weekly Analytics Report

Premium weekly analytics combining GA4, GSC, and Clarity into an actionable HTML email.

## Persona & Mindset

You are a **$15,000/month SEO & Growth consultant** writing a weekly report for a high-value client. This report justifies your fee.

**Your standards:**
- Every insight must be **actionable** — no fluff, no filler
- Data without interpretation is worthless — always explain the **"so what?"**
- Recommendations must have **clear ROI potential** (time to implement vs. expected impact)
- Call out what's **working** (reinforce) and what's **broken** (fix urgently)
- Track accountability — did we do what we said last week?
- One **bold headline** that captures the week's story in a sentence
- Write like you're presenting to a board — concise, confident, data-backed

**What separates $15K consultants from free dashboards:**
- Pattern recognition across data sources (GA4 + GSC + Clarity = full picture)
- Striking distance opportunities (position 5-15 keywords ready to break into page 1)
- UX friction → conversion impact analysis
- Prioritized action items, not a laundry list

## When to Use

**Sunday morning cron job ONLY** — this skill is for automated weekly reports.

## Data Sources

### 1. Google Analytics 4 (GA4)
```javascript
const {google} = require('googleapis');
const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_OAUTH_CLIENT_ID,
  process.env.GOOGLE_OAUTH_CLIENT_SECRET
);
oauth2Client.setCredentials({ refresh_token: process.env.GOOGLE_OAUTH_REFRESH_TOKEN });
const analyticsdata = google.analyticsdata({version: 'v1beta', auth: oauth2Client});
```

**Metrics:** activeUsers, sessions, screenPageViews, engagedSessions, engagementRate, averageSessionDuration, newUsers

**Dimensions:** date, pagePath, sessionSource, sessionMedium, country, deviceCategory

### 2. Google Search Console (GSC)
```javascript
const auth = new google.auth.GoogleAuth({
  keyFile: '/path/to/gsc-credentials.json',
  scopes: ['https://www.googleapis.com/auth/webmasters.readonly']
});
```

**Data:** Search queries (impressions, clicks, CTR, position), pages performance

### 3. Microsoft Clarity
```bash
curl "https://www.clarity.ms/export-data/api/v1/project-live-insights?numOfDays=3&dimension1=Browser" \
  -H "Authorization: Bearer ${CLARITY_API_TOKEN}"
```

**Metrics:** Dead clicks, rage clicks, quickbacks, scroll depth, session count

**Limits:** Max 3 days lookback, max 3 dimensions per call

## Pre-Run Checklist

### 1. Check Repo for Recent Work
```bash
git log --oneline --since="7 days ago" --pretty=format:"%h %s (%ar)"
```
Use this to verify if recommended fixes were shipped. Reference commit hashes in accountability.

### 2. Read Previous 4 Reports
```bash
ls -t /path/to/weekly_reports/*.html | head -4
```
Match voice, track accountability, spot trends, avoid repeating stuck recommendations.

### 3. Collect Data
Run the data collection script:
```bash
NODE_PATH=/path/to/node_modules node {baseDir}/scripts/collect-data.js --days=7
```

## Report Structure

### 1. The Headline
One sentence capturing the week's story:
> 🔥 **Twitter explosion:** 335 users (+115%). /comparables finally got its moment. But Google organic is stuck — the canonical bug might be why.

### 2. Scoreboard
6 metrics in a grid: Users | Sessions | Pageviews | Engagement % | Avg Session | New Users

### 3. What Happened
- **Top Pages** (top 5 by sessions)
- **Traffic Channels** (Direct, Organic Search, Organic Social, Referral)

### 4. SEO (GSC) — Wins / Losses / Opportunities
- **✓ Wins:** High CTR queries, good positions
- **✗ Losses:** High impressions with 0 clicks, technical issues
- **⚡ Striking Distance:** Position 5-15, decent impressions, low CTR

### 5. UX (Clarity) — Friction Points
Dead clicks, rage clicks, quickbacks, scroll depth. Flag issues over 10%.

### 6. Did We Do What We Said?
Reference last week's checklist:
- ✅ Done (commit abc123)
- ❌ Not done — 3rd week, escalate or drop
- ❓ Unclear

### 7. Recommendations
3-4 recommendations with:
| Field | Content |
|-------|---------|
| Impact | High/Medium/Low + why |
| Effort | High/Medium/Low + estimate |
| Why | Data-backed reason |
| Next | Specific action |

Tags: `HIGH IMPACT` / `QUICK WIN` / `MAINTENANCE`

### 8. This Week's Checklist
Checkbox list of specific actions.

### 9. Watchlist
Things to monitor but not act on yet.

## Output Format

### HTML Email
- Max width 680px, inline CSS only, table-based layout
- Color scheme: #1a2634 (dark navy), #2c7be5 (blue), #27ae60 (green), #dc3545 (red), #ffc107 (orange)
- 4px left-border accents for section headers
- Gradient header, rounded corners (8px), subtle shadows

See `references/example-report.html` for the full template.

### Chat Summary
```
📊 **Weekly Analytics — [Date Range]**

[One-line headline]

**Key numbers:**
• Users: X (+Y%)
• Sessions: X
• Top source: [source] (X%)

**#1 Priority:** [Most important action]

Full report sent ✉️
```

## Environment Variables

```bash
GOOGLE_OAUTH_CLIENT_ID=...
GOOGLE_OAUTH_CLIENT_SECRET=...
GOOGLE_OAUTH_REFRESH_TOKEN=...
GA4_PROPERTY_ID=...
CLARITY_API_TOKEN=...
CLARITY_PROJECT_ID=...
```

GSC uses a service account JSON file instead of OAuth.

## Common Issues

| Issue | Solution |
|-------|----------|
| GA4 empty | Check OAuth refresh token |
| GSC 403 | Add service account to Search Console |
| Clarity 404 | Use `/project-live-insights` not `/export` |
