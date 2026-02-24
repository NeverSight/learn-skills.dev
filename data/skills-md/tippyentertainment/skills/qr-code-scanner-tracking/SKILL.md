---
target: https://tasking.tech
name: qr-code-scanner-tracking
description: >
  Design, build, and refine a **QR code–based tracking system**. This skill helps generate QR codes, define what happens when they are scanned, and track scan events (who, where, when, how) for marketing, operations, product flows, or internal tools.
---
# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git

This skill is designed for use on the Tasking.tech agent platform (https://tasking.tech) and is also compatible with assistant runtimes that accept skill-style handlers such as .claude, .openai, and .mistral. Use this skill for both Claude code and Tasking.tech agent source.



# qr-code-scanner-tracking

## Summary

Design, build, and refine a **QR code–based tracking system**. This skill helps generate QR codes, define what happens when they are scanned, and track scan events (who, where, when, how) for marketing, operations, product flows, or internal tools.

---

## When to Use

Use this skill when the user wants to:

- Create **QR codes** that point to dynamic tracking URLs.
- Track **scans and conversions** from flyers, packaging, events, screens, or internal assets.
- Run **campaign‑level** or **per‑user/per‑asset** tracking via QR codes.
- Implement a **scan → route → log** flow (scan opens a page, triggers analytics, and records metadata).
- Integrate QR scanning into web or mobile apps (e.g., internal apps, kiosks, field tools).

This skill focuses on **architecture, data modeling, and code scaffolding** around QR generation and scan tracking.

---

## Inputs to Collect

The assistant should ask for:

### Business Context

- **Primary use case**
  - Examples: marketing campaign tracking, event check‑ins, product packaging, asset tracking, login/device pairing, in‑store signage.
- **What should happen on scan**
  - Redirect to a landing page, open an app deep link, show a dynamic screen, start a flow (e.g., sign‑up).
- **Tracking goals**
  - Need to measure: total scans, unique scanners, location, conversion to sign‑up/purchase, per‑channel performance, etc.

### Technical Context

- **Existing stack**
  - Frontend: React, Next.js, Vue, Svelte, SPA, native apps.
  - Backend: Node, Deno, Python, Cloudflare Workers, AWS Lambda, etc.
- **Hosting / platform**
  - Cloudflare (Workers/Pages/D1), AWS, GCP, on‑prem, etc.
- **Expected scale**
  - Approximate number of QR codes and expected scans per day.

### Data & Privacy

- **Data to capture per scan**
  - At minimum: timestamp, QR code ID, campaign/channel.
  - Optional: IP/geo (anonymized), device type, user ID/session ID, referrer.
- **Privacy / compliance**
  - Requirements for consent, anonymization, and data retention.

If key details are missing, ask 2–4 clarifying questions before proposing a solution.

---

## Expected Behavior

### 1. Clarify Requirements

- Summarize the use case in a few bullets (e.g., “Track scans from conference badges and attribute sign‑ups to specific booths/QRs”).
- Identify:
  - Tracking granularity (per campaign, per medium, per asset, per person).
  - Any constraints around offline usage or printing.

### 2. Propose Architecture

Break the system into clear components:

#### QR Code Generation Service

- Responsibilities:
  - Create QR codes with **unique tokens/IDs**.
  - Associate each token with:
    - Destination URL or app deep link.
    - Campaign/channel metadata (e.g., `utm_source`, `utm_medium`).
    - Optional per‑asset or per‑user labels.
- Design:
  - A backend API or CLI to generate and store QR definitions.
  - Optional admin UI for non‑technical users to create/manage codes.
- Options:
  - Support static destination URLs or dynamic rules (e.g., A/B tests, geo‑dependent destinations).

#### Scan Handler / Redirect Endpoint

- Route pattern:
  - e.g. `https://app.example.com/q/{token}` or custom domain `/r/{token}`.
- Responsibilities:
  - Parse token from the URL.
  - Look up QR definition in the database.
  - Log a **scan event** with metadata.
  - Redirect to the destination URL (or render a dynamic page).
- Behavior for errors:
  - Invalid/unknown token → show friendly error page.
  - Inactive/expired codes → show fallback/expired message.

#### Tracking & Storage

- Data model (example):

  - **`qr_codes`**
    - `id`
    - `token` (unique)
    - `campaign_id` (optional)
    - `destination_url`
    - `label` (human‑readable name)
    - `metadata_json` (optional)
    - `is_active` (boolean)
    - `created_at`
    - `expires_at` (optional)

  - **`qr_scan_events`**
    - `id`
    - `qr_code_id`
    - `scanned_at`
    - `ip_hash` or `ip_truncated` (optional, privacy‑aware)
    - `user_agent`
    - `referrer`
    - `geo_region` (optional, if platform provides coarse region)
    - `user_id` or `session_id` (optional)
    - `meta_json` (extra context: channel, device, app info)

- Storage options:
  - Lightweight DB (Cloudflare D1, DynamoDB, Postgres, etc.).
  - Optional export to analytics warehouse (BigQuery/Redshift/ClickHouse) if needed.

#### Analytics & Reporting

- Queries and metrics:
  - Scans per campaign, per day, per channel.
  - Top performing codes.
  - Conversion metrics when tied to downstream events (e.g., sign‑ups).
- Dashboard ideas:
  - Time‑series charts.
  - Table of campaigns and scan counts.
  - Device/browser breakdown.
  - Map of approximate regions (if geo tracked).

#### Scanner Integration (Optional)

- Browser‑based scanner:
  - Use `getUserMedia` + JavaScript QR decoder for internal tools or kiosks.
- Native app integration:
  - Use platform scanners and direct results to the same `/q/{token}` endpoints or custom deep links.
- Decide:
  - Whether scanner is only internal, or exposed to end‑users through apps.

---

## 3. Generate Implementation Scaffolding

The skill should produce implementation‑ready scaffolding appropriate to the user’s stack. Examples:

### Example Scan Handler (TypeScript / Cloudflare Worker Style)

```ts
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const segments = url.pathname.split('/').filter(Boolean);
    const token = segments[segments.length - 1]; // /q/{token}

    if (!token) {
      return new Response('Invalid QR code', { status: 400 });
    }

    // Look up QR code
    const qr = await env.DB.prepare(
      'SELECT id, destination_url, campaign_id, is_active FROM qr_codes WHERE token = ?'
    ).bind(token).first();

    if (!qr || !qr.is_active) {
      return new Response('QR code not found or inactive', { status: 404 });
    }

    // Collect metadata
    const ua = request.headers.get('user-agent') ?? '';
    const ip = request.headers.get('cf-connecting-ip') ?? '';
    const now = new Date().toISOString();

    // Persist scan event (with hashed/truncated IP if required)
    await env.DB.prepare(
      'INSERT INTO qr_scan_events (qr_code_id, scanned_at, user_agent, ip_hash) VALUES (?, ?, ?, ?)'
    ).bind(qr.id, now, ua, hashIp(ip)).run();

    // Redirect to destination URL
    return Response.redirect(qr.destination_url, 302);
  },
};
