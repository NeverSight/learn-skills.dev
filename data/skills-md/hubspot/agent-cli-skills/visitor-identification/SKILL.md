---
name: visitor-identification
description: Generate a HubSpot Conversations visitor identification token for a known website visitor by email, with guidance on required scopes, account tier requirements, and how the frontend must use the token with the HubSpot Conversations SDK.
triggers:
  - "visitor identification"
  - "visitor id token"
  - "visitor token"
  - "identify visitor"
  - "conversations sdk token"
  - "chat widget identification"
  - "identify website visitor"
  - "visitor-identification"
  - "create visitor token"
---

Requires the `conversations` command group from hub-cli PR #251. `hubspot conversations visitor-identification --help` is authoritative.

## What visitor identification is

When a known contact (someone whose email you have) visits your website, the HubSpot Conversations chat widget can identify them — linking the live chat session to their CRM record. To do this, your server generates a short-lived signed token and passes it to the HubSpot Conversations JavaScript SDK. The SDK sends the token to HubSpot, which verifies it and associates the chat session with the contact.

The token is **NOT** a general authentication credential. It identifies one visitor for one chat session and is useless outside the Conversations SDK.

## Requirements

| Requirement | Detail |
|---|---|
| Account tier | Professional or Enterprise |
| Required scope | `conversations.visitor_identification.tokens.create` |
| Token lifetime | 12 hours; cache across page loads and refresh at least every 12 hours |
| Generation side | **Server-side only** — never generate in browser JavaScript; your private app token must remain secret |

## Generate a token

```bash
# Minimal — email only
hubspot conversations visitor-identification create-token \
  --email visitor@example.com

# With name (populates the contact preview in the widget)
hubspot conversations visitor-identification create-token \
  --email visitor@example.com \
  --first-name Jane \
  --last-name Doe
```

Output:
```json
{"ok":true,"data":{"token":"eyJhbGciOiJIUzI1NiJ9..."}}
```

If the private app token is missing the required scope the CLI returns a 403 with a scope hint:
```json
{"ok":false,"error":{"status":403,"message":"Missing scope: conversations.visitor_identification.tokens.create"}}
```

## Setting up the private app token

The `conversations.visitor_identification.tokens.create` scope must be granted on the HubSpot private app whose token is in `HUBSPOT_ACCESS_TOKEN`. To add the scope:

1. In HubSpot: **Settings → Integrations → Private Apps → [your app] → Scopes**
2. Under "CRM", enable `conversations.visitor_identification.tokens.create`
3. Rotate the token if required after scope change

## What the frontend must do with the token

After generating the token server-side, set `loadImmediately: false` before the widget loads. Then set the identification properties and load the widget:

```javascript
const { token } = await fetch('/api/hs-visitor-token').then(r => r.json());

window.hsConversationsSettings = {
  loadImmediately: false,
  identificationEmail: 'visitor@example.com',
  identificationToken: token,
};

window.HubSpotConversations.widget.load();
```

Key rules:
- Generate the token server-side for authenticated users; cache it across page loads only if it is refreshed at least every 12 hours.
- Do **not** expose your `HUBSPOT_ACCESS_TOKEN` (private app token) to the frontend.
- `identificationEmail` must match the email used to generate the token.

See HubSpot's public documentation for the full Conversations SDK reference.

## Known constraints

- Requires Professional or Enterprise HubSpot subscription. On Starter or Free the API returns a 403.
- One token per email address per call. Bulk generation is not supported.
- The token payload is opaque — do not attempt to decode or store it beyond passing it to the SDK.
