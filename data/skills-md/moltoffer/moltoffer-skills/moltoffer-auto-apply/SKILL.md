---
name: moltoffer-auto-apply
description: "LinkedIn Easy Apply automation. Auto-fill and submit applications using Playwright browser tools. Works with moltoffer-candidate job matches."
emoji: 🚀
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: []
      env: []
    primaryEnv: null
---

# MoltOffer Auto-Apply Skill

Automate LinkedIn Easy Apply submissions using Playwright. Reads pending jobs from the MoltOffer API and auto-fills applications based on persona.md.

## Prerequisites

- **moltoffer-candidate** skill must be set up (persona.md + credentials)
- User must be **logged into LinkedIn** in the browser
- Shared resources from moltoffer-candidate:
  - `../moltoffer-candidate/persona.md` — Personal info for form filling
  - `../moltoffer-candidate/credentials.local.json` — MoltOffer API access

## Commands

```
/moltoffer-auto-apply <action>
```

- `/moltoffer-auto-apply` or `/moltoffer-auto-apply kickoff` - First-time setup (verify LinkedIn login)
- `/moltoffer-auto-apply apply` - Apply to pending jobs (confirm each one)
- `/moltoffer-auto-apply yolo` - Apply to all pending jobs without confirmation (3-5s delay between jobs, stops on critical errors)
- `/moltoffer-auto-apply status` - View application history and statistics

## API Endpoints

Base URL: `https://api.moltoffer.ai/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/pending-apply-jobs` | Fetch jobs confirmed for application |
| `POST` | `/v1/pending-apply-jobs` | Add job to apply queue |
| `PATCH` | `/v1/pending-apply-jobs/:jobId` | Report apply result |

**GET /v1/pending-apply-jobs**

Returns pending jobs with LinkedIn URLs. Only jobs with `status=pending` and a LinkedIn URL.

**POST /v1/pending-apply-jobs**

| Field | Required | Description |
|-------|----------|-------------|
| `jobId` | Yes | Post UUID |

Skips silently if already queued.

**PATCH /v1/pending-apply-jobs/:jobId**

| Field | Required | Description |
|-------|----------|-------------|
| `status` | Yes | `applied` / `skipped` / `needs-human-review` / `error` |
| `reason` | No | Status explanation |
| `appliedAt` | No | Actual apply timestamp (ISO 8601) |

## Execution Flow

### First Time Setup

```
/moltoffer-candidate kickoff   → Set up persona + API key
/moltoffer-auto-apply kickoff  → Verify LinkedIn login
```

### Regular Usage

```
/moltoffer-candidate daily-match  → Find matched jobs
/moltoffer-auto-apply apply       → Apply with confirmation
/moltoffer-auto-apply yolo        → Apply without confirmation
```

### Reference Docs

- [references/onboarding.md](references/onboarding.md) - First-time setup
- [references/workflow.md](references/workflow.md) - Main application workflow
- [references/apply.md](references/apply.md) - Single job application automation

## Core Principles

- **API as source of truth**: Job status tracked via MoltOffer API, no local files
- **Persona-driven**: All form answers inferred from persona.md at application time
- **Rate limiting**: 3-5 second delays between applications
- **Human fallback**: Jobs requiring external application or unclear answers marked as `needs-human-review`
- **Easy Apply only**: Skip jobs that redirect to external sites
- **Login required**: User must log in to LinkedIn manually; never store LinkedIn credentials

## Security Notes

- Never store LinkedIn credentials
- User must log in manually before using this skill
- All automation is client-side via Playwright
