---
name: agentforce-agent-api
description: >
  Integrates Salesforce Agentforce Agent API into web applications using OAuth
  Client Credentials flow. Covers session creation, synchronous messaging, token
  caching, and correct API endpoint/body formats. Use when building chat interfaces
  with Agentforce, setting up Agent API authentication, debugging Agent API errors,
  or connecting external apps to Salesforce agents.
license: MIT
metadata:
  version: "1.0.0"
  author: "Dylan Andersen"
---

# Agentforce Agent API Integration

Build chat interfaces powered by Salesforce Agentforce agents via the Agent API. This skill covers authentication, session management, messaging, and common pitfalls.

## API Endpoints

The Agent API is hosted on `api.salesforce.com`, **NOT** on your My Domain.

```
Base: https://api.salesforce.com/einstein/ai-agent/v1
```

Your My Domain goes in the request body as `instanceConfig.endpoint`.

### Create Session

```
POST https://api.salesforce.com/einstein/ai-agent/v1/agents/{AGENT_ID}/sessions
```

```json
{
  "externalSessionKey": "<random-uuid>",
  "instanceConfig": {
    "endpoint": "https://<MY_DOMAIN>"
  },
  "streamingCapabilities": {
    "chunkTypes": ["Text"]
  },
  "bypassUser": true
}
```

Response returns `sessionId` and `_links` with message/stream/end URLs.

### Send Synchronous Message

```
POST https://api.salesforce.com/einstein/ai-agent/v1/sessions/{SESSION_ID}/messages
```

```json
{
  "message": {
    "type": "Text",
    "text": "Hello",
    "sequenceId": 1
  }
}
```

`sequenceId` goes **inside** the `message` object. Increment per message.

Response text is in `messages[].message` field:

```json
{
  "messages": [
    {
      "type": "Inform",
      "message": "The response text is here",
      "id": "...",
      "feedbackId": "...",
      "isContentSafe": true,
      "citedReferences": []
    }
  ]
}
```

### End Session

```
DELETE https://api.salesforce.com/einstein/ai-agent/v1/sessions/{SESSION_ID}
```

## OAuth Client Credentials Flow

### Connected App Setup

1. Create External Client App in Salesforce Setup
2. Enable OAuth with scopes: `api`, `refresh_token`/`offline_access`, `chatbot_api`, `sfap_api`
3. Enable Client Credentials Flow + JWT-based access tokens
4. Set Run As user (see below)

### Run As User Requirements

The Run As user **must have API login access**. Do NOT use Einstein Agent service users (`serviceagentagentforce...@example.com`) — they have restricted licenses and **cannot authenticate via OAuth**. Every attempt returns `"invalid_grant"` / `"Maximum Logins Exceeded"`.

Use a full Salesforce admin user (dev/testing) or a Salesforce Integration User (production).

### Token Request

```
POST https://{MY_DOMAIN}/services/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id={KEY}&client_secret={SECRET}
```

### Token Caching (Critical)

Salesforce rate limit: **3,600 logins per user per hour** (rolling window).

In Next.js dev mode, HMR resets module-scoped variables on every file save, triggering fresh OAuth requests. Use `globalThis` to persist the token cache:

```typescript
const g = globalThis as typeof globalThis & { __sfToken?: { token: string; expiresAt: number } };
if (!g.__sfToken) g.__sfToken = { token: '', expiresAt: 0 };
```

Additional rules:
- **Never retry on rate limit** — retrying burns more quota
- Dedup concurrent token requests with a shared Promise
- Cache tokens with a 1-minute safety margin before expiry
- Always `.trim()` env vars — hosting platforms can add trailing `\n`

## Environment Variables

```env
SALESFORCE_MY_DOMAIN=your-org.my.salesforce.com
SALESFORCE_CONSUMER_KEY=...
SALESFORCE_CONSUMER_SECRET=...
SALESFORCE_AGENT_ID=0XxHu000000XXXXKXX
```

Always trim: `process.env.SALESFORCE_MY_DOMAIN?.trim()`

Normalize domain for both bare and prefixed formats:
```typescript
const endpoint = myDomain.startsWith('https://') ? myDomain : `https://${myDomain}`;
```

## React Strict Mode

React 18 dev mode double-mounts components. Do NOT use `useRef` guards for session initialization — causes deadlock where neither mount sets state.

Use `AbortController` pattern:

```typescript
useEffect(() => {
  const controller = new AbortController();
  async function init() {
    const res = await fetch('/api/session', { method: 'POST', signal: controller.signal });
    const data = await res.json();
    setSessionId(data.sessionId);
  }
  init().catch(err => {
    if (err instanceof DOMException && err.name === 'AbortError') return;
    // handle real errors
  });
  return () => controller.abort();
}, []);
```

Mount 1's fetch is aborted on cleanup. Mount 2 runs fresh.

## Quick Error Reference

| Error | Cause | Fix |
|---|---|---|
| `Maximum Logins Exceeded` (every attempt) | Einstein Agent service user as Run As | Change to admin/Integration User |
| `login rate exceeded` | Too many OAuth requests | Wait 15-30 min; implement globalThis caching |
| 404 `URL No Longer Exists` | Using My Domain as API host | Use `api.salesforce.com/einstein/ai-agent/v1` |
| `Missing required creator property 'sequenceId'` | sequenceId at top level | Move inside `message` object |
| `Bad force-config endpoint` | Trailing `\n` in env var | `.trim()` all env vars |
| No text in response | Parsing `msg.text` | Use `msg.message` field instead |
| Session stuck on "Connecting..." | useRef guard + Strict Mode | Use AbortController pattern |

## Detailed Guide

For full walkthrough with code examples and step-by-step setup, see [HOW_TO_GET_AGENTFORCE_AGENT_API_WORKING.md](HOW_TO_GET_AGENTFORCE_AGENT_API_WORKING.md) in the project root.
