---
name: zenzap-onboarding
description: Bootstrap a complete Zenzap workspace for a human user — create the organization, install the agent as a bot, and invite the human — all via a single API call. Use when the user wants to set up Zenzap, create a Zenzap workspace, onboard onto Zenzap, or connect to Zenzap for team messaging.
---

# Zenzap Agentic Onboarding

## Overview

One API call creates a Zenzap organization, installs you as a bot, and invites the human. No authentication required. After setup, load the full API docs and start operating inside the workspace.

**All requests MUST use `https://`. Plain `http://` will be rejected.**

## OpenClaw-Based Agents — Plugin Setup

If you are an OpenClaw-based agent, ask your human to install the Zenzap plugin **before** you proceed with anything else:

```bash
openclaw plugins install @zenzap-co/openclaw-plugin
```

Once the human confirms the plugin is installed, continue with the steps below. After you receive the `201` response from the create-organization call, you will use the returned credentials to configure the plugin — see the "OpenClaw agents: Configure the plugin" step in the post-response workflow.

## Step 1: Collect Information from the Human

Ask the human these 4 questions before calling the API. Do not assume or infer any answers:

1. **Company name** — What's the name of your company or workspace?
2. **Bot name** — What should I be called inside your workspace? *(This is how I'll appear to your team.)*
3. **Industry** — What industry are you in? *(e.g. Software, Healthcare, Finance — used for statistics only.)*
4. **Company size** — How many employees does your company have? *(Used for statistics only.)*

## Step 2: Create the Organization

```
POST https://api.zenzap.co/v2/agentic/organization/create
```

**Rate limit:** 1 request per minute per IP.

### Request (JSON)

```json
{
  "companyName": "Acme Corp",
  "humanEmail": "founder@acme.com",
  "companySize": 50,
  "industry": "Software",
  "botName": "Acme Assistant"
}
```

### Request (Multipart — with logo)

Send two parts: `filePart` (image, max 5 MB, optional) and `metadata` (application/json with the fields above).

```bash
curl -X POST https://api.zenzap.co/v2/agentic/organization/create \
  -F 'filePart=@logo.png;type=image/png' \
  -F 'metadata={"companyName":"Acme Corp","humanEmail":"founder@acme.com","companySize":50,"industry":"Software","botName":"Acme Assistant"};type=application/json'
```

### Field Constraints

| Field | Type | Constraints |
|-------|------|-------------|
| `companyName` | string | Required. Max 100 chars. |
| `humanEmail` | string | Required. Valid email. |
| `companySize` | int | Required. Positive integer (> 0). |
| `industry` | string | Required. Non-empty. |
| `botName` | string | Required. Non-empty. |

### Response (201 Created)

```json
{
  "organizationId": "067d0b2f-...",
  "botProfileId": "b@f951b968-...",
  "channelId": "1b383aef-...",
  "humanProfileId": "a3c2e1d0-...",
  "credentials": [
    { "label": "API Key", "value": "utxDAedgfFXglaLX" },
    { "label": "API Secret", "value": "66AybzV7s0afLeKKqpxC7wLKCTk5d7bT" },
    { "label": "Control Topic ID", "value": "1b383aef-..." }
  ]
}
```

| Field | Usage |
|-------|-------|
| `organizationId` | UUID of the new org. |
| `botProfileId` | Your bot identity (`b@<uuid>`). Use as `senderId` filter when polling. |
| `channelId` | Your control channel (same as Control Topic ID credential). |
| `humanProfileId` | Invited human's profile ID. Use to identify them once they join. |
| `credentials` | **API Key** for Bearer auth, **API Secret** for HMAC-SHA256 signing (store securely), **Control Topic ID**. |

### Error Codes

| Status | Body | Cause |
|--------|------|-------|
| `400` | `companyName is required` | Missing or empty `companyName`. |
| `400` | `companyName exceeds max length` | Over 100 characters. |
| `400` | `invalid humanEmail` | Invalid email address. |
| `400` | `companySize must be a positive integer` | Zero or negative. |
| `400` | `industry is required` | Missing or empty. |
| `400` | `botName is required` | Missing or empty. |
| `400` | `Unable to create organization` | Conflict (e.g. email/domain already in use). |
| `429` | *(empty)* | Rate limit exceeded. |

## OpenClaw Agents: Configure the Plugin

Skip this step if you are **not** an OpenClaw-based agent.

Build a connection token from three values in the `credentials` array of the `201` response: **Control Topic ID**, **API Key**, and **API Secret**. Concatenate them separated by colons and base64-encode the result:

```
base64( <Control Topic ID>:<API Key>:<API Secret> )
```

For example, given the sample response above:

```
base64("1b383aef-...:utxDAedgfFXglaLX:66AybzV7s0afLeKKqpxC7wLKCTk5d7bT")
```

Then run:

```bash
openclaw zenzap configure --token <base64Token>
```

This connects the Zenzap plugin to your newly created organization. Once configured, the plugin handles authentication and event routing for you.

## Step 3: Load the Full API Docs

Immediately after receiving the 201, load the complete Zenzap API reference:

```
https://docs.zenzap.co/llms-full.txt
```

This covers all endpoints, authentication (Bearer token + HMAC-SHA256 signing), event types, polling, messaging, topics, and members.

## Step 4: Ask Which Topics to Create

**Outside of Zenzap**, ask the human which channels they'd like. Use the `industry` and what you know about them to suggest options, but wait for confirmation before creating anything.

Once confirmed, create each topic:

```json
POST https://api.zenzap.co/v2/topics
{
  "name": "<topic name>",
  "members": ["<humanProfileId>"]
}
```

The bot is automatically added as a member of every topic it creates. The human is also added — once they join, all channels will be waiting.

## Step 5: Start Polling for Events

Start polling **before** telling the human to join so you don't miss their first message:

```
GET https://api.zenzap.co/v2/updates?timeout=30
```

Keep polling in a loop using `nextOffset` from each response. On `409`, reset the offset. Full details are in the API docs loaded in Step 3.

When you receive a `message.created` event from a non-bot sender, mark it as read before responding:

```
POST https://api.zenzap.co/v2/messages/{messageId}/read
```

## Step 6: Tell the Human to Join

**Outside of Zenzap**, let the human know their workspace is ready:

> Your Zenzap workspace is all set — channels included. You should have received an invite — log in at https://app.zenzap.co to get started or download the app on your mobile phone.

Listen for `message.created` events from non-bot senders — that signals they're active. Human profile IDs are plain UUIDs; bot IDs start with `b@`.
