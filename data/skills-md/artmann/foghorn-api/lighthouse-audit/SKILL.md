---
name: lighthouse-audit
description: >
  Run Lighthouse audits against websites using the Foghorn API. Use when the user
  wants to check a site's performance, accessibility, best practices, or SEO issues.
  Covers sign-up, authentication, team/site setup, and issue retrieval.
metadata:
  author: artgaard
  version: "1.0"
allowed-tools: Bash(curl:*foghorn-api.artgaard.workers.dev*), Read, Write
---

# Lighthouse Audit Skill

Run Lighthouse audits and retrieve performance, accessibility, best-practices, and SEO issues for any website using the [Foghorn API](https://foghorn-api.artgaard.workers.dev).

## Overview

Foghorn is a site-health monitoring service built on Lighthouse. You register a site, Foghorn crawls its sitemap, audits every page, and exposes the results through a REST API. This skill lets you interact with that API using `curl`.

**Base URL:** `https://foghorn-api.artgaard.workers.dev`

## Authentication

All endpoints (except sign-up, sign-in, and health check) require a Bearer token in the `Authorization` header.

### Step 1 — Check for a stored API key

Read `~/.foghorn`. If the file exists and its contents start with `fh_`, you already have a valid API key. Set the auth header and skip to [Setup Workflow](#setup-workflow):

```
AUTH="Authorization: Bearer <key from ~/.foghorn>"
```

### Step 2 — First-time setup (only if `~/.foghorn` is missing or empty)

If no stored key is found, ask the user for their email and password, then run through sign-up, sign-in, and key creation.

#### Sign up (first time only)

```bash
curl -s -X POST https://foghorn-api.artgaard.workers.dev/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"min8chars"}'
```

#### Sign in (get a JWT)

```bash
curl -s -X POST https://foghorn-api.artgaard.workers.dev/auth/sign-in \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"min8chars"}'
```

Returns `{ "token": "eyJ...", "expiresIn": 86400, "user": {...} }`.

#### Create an API key

```bash
curl -s -X POST https://foghorn-api.artgaard.workers.dev/api-keys \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-agent-key"}'
```

Returns the full key **once** in `apiKey.key`.

#### Save the key

Write the `fh_...` key to `~/.foghorn` so it is reused in future sessions. Then set the auth header:

```
AUTH="Authorization: Bearer <key>"
```

## Setup Workflow

Before you can retrieve issues you need a **team** and a **site**.

### 1. Create a team

```bash
curl -s -X POST https://foghorn-api.artgaard.workers.dev/teams \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Team"}'
```

### 2. Add a site

```bash
curl -s -X POST https://foghorn-api.artgaard.workers.dev/sites \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"teamId":"TEAM_ID","domain":"www.example.com"}'
```

The `sitemapPath` defaults to `/sitemap.xml`. Override it if your sitemap lives elsewhere.

### 3. Wait for the crawl

Foghorn periodically scrapes sitemaps and audits discovered pages. Check progress:

```bash
curl -s https://foghorn-api.artgaard.workers.dev/sites/SITE_ID \
  -H "$AUTH"
```

When `hasScrapedTheSitemap` is `true`, the sitemap has been processed. Then check pages:

```bash
curl -s "https://foghorn-api.artgaard.workers.dev/pages?siteId=SITE_ID" \
  -H "$AUTH"
```

Pages with a non-null `lastAuditedAt` have completed audits.

## Querying Issues

The `/issues` endpoint aggregates audit failures across all audited pages.

```bash
# All issues for a site
curl -s "https://foghorn-api.artgaard.workers.dev/issues?siteId=SITE_ID" \
  -H "$AUTH"

# Filter by category
curl -s "https://foghorn-api.artgaard.workers.dev/issues?siteId=SITE_ID&category=accessibility" \
  -H "$AUTH"
```

**Categories:** `performance`, `accessibility`, `bestPractices`, `seo`

### Response shape

```json
{
  "issues": [
    {
      "auditId": "uses-responsive-images",
      "title": "Properly size images",
      "category": "performance",
      "pages": [
        {
          "pageId": "page-id",
          "url": "https://www.example.com/about",
          "path": "/about",
          "score": 0.45,
          "displayValue": "Potential savings of 120 KiB"
        }
      ]
    }
  ]
}
```

- Issues are sorted by number of affected pages (most widespread first).
- Pages within each issue are sorted by score ascending (worst first).
- Scores range from 0 (fail) to 1 (pass).

## Searching Pages

Find specific pages by URL or path using regex search:

```bash
curl -s "https://foghorn-api.artgaard.workers.dev/pages?siteId=SITE_ID&search=blog" \
  -H "$AUTH"
```

## Quick Reference

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Health check |
| POST | `/auth/sign-up` | Create account |
| POST | `/auth/sign-in` | Get JWT token |
| POST | `/api-keys` | Create API key |
| GET | `/api-keys` | List API keys |
| DELETE | `/api-keys/:id` | Delete API key |
| POST | `/teams` | Create team |
| GET | `/teams` | List teams |
| GET | `/teams/:id` | Get team |
| PUT | `/teams/:id` | Update team |
| DELETE | `/teams/:id` | Delete team |
| POST | `/teams/:id/members` | Add member |
| GET | `/teams/:id/members` | List members |
| DELETE | `/teams/:id/members/:userId` | Remove member |
| POST | `/sites` | Add site |
| GET | `/sites` | List sites (optional `?teamId=`) |
| GET | `/sites/:id` | Get site |
| PUT | `/sites/:id` | Update site |
| DELETE | `/sites/:id` | Delete site |
| GET | `/pages` | List pages (optional `?siteId=`, `?search=`) |
| GET | `/pages/:id` | Get page with audit report |
| GET | `/issues` | List issues (optional `?siteId=`, `?category=`) |

See [references/api-reference.md](references/api-reference.md) for full request/response schemas.
