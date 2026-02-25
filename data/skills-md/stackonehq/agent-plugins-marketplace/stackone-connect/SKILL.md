---
name: stackone-connect
description: Implement account linking using StackOne Connect Sessions and the Hub React component. Use when user asks to "connect a provider", "embed the integration picker", "add BambooHR to my app", "create a connect session", "set up auth links", or "handle account webhooks". Covers the full flow from session creation to webhook handling. Do NOT use for making API calls after linking (use stackone-platform) or building AI agents (use stackone-agents).
license: MIT
compatibility: Requires network access to fetch live documentation from docs.stackone.com
metadata:
  author: stackone
  version: "2.0"
---

# StackOne Connect — Account Linking

## Important

Before writing code, fetch the latest documentation:
1. Fetch `https://docs.stackone.com/guides/connect-tools-overview` for the current connection flow
2. Fetch `https://www.npmjs.com/package/@stackone/hub` for the latest Hub component API

The Hub component is in active beta — props and peer dependencies change between versions.

## Instructions

### Step 1: Choose a connection method

| Method | When to use |
|--------|-------------|
| **Embedded Hub** | In-app integration picker — users stay in your app |
| **Auth Link** | Email onboarding or external flows — standalone URL, valid 5 days |
| **Dashboard** | Internal testing only — never for production |

If unsure, recommend the Embedded Hub. It provides the best user experience.

### Step 2: Create a Connect Session (backend)

Your backend creates a session token that the frontend uses to initialize the Hub:

```bash
curl -X POST https://api.stackone.com/connect_sessions \
  -H "Authorization: Basic $(echo -n 'YOUR_API_KEY:' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "origin_owner_id": "customer-123",
    "origin_owner_name": "Acme Inc"
  }'
```

The response includes a `token` field. Pass this to the frontend.

To filter which providers appear in the Hub:
```json
{
  "origin_owner_id": "customer-123",
  "origin_owner_name": "Acme Inc",
  "provider": "bamboohr",
  "categories": ["hris"]
}
```

Fetch `https://docs.stackone.com/platform/api-reference/connect-sessions/create-connect-session` for the full request/response schema.

### Step 3: Initialize the Hub (frontend)

```bash
npm install @stackone/hub
```

```tsx
import { StackOneHub } from "@stackone/hub";

function ConnectorPage() {
  const [token, setToken] = useState<string>();

  useEffect(() => {
    fetchConnectSessionToken().then(setToken);
  }, []);

  if (!token) return <div>Loading...</div>;

  return (
    <StackOneHub
      token={token}
      onSuccess={(account) => {
        // Store account.id — you'll need it for all subsequent API calls
        console.log("Connected:", account.id, account.provider);
      }}
      onCancel={() => console.log("User cancelled")}
      onClose={() => console.log("Hub closed")}
    />
  );
}
```

For the full props API and theming options, consult `references/hub-reference.md`.

### Step 4: Set up webhook listeners

Webhooks are required for Auth Links (no frontend callbacks) and recommended for the Embedded Hub:

| Event | When it fires |
|-------|---------------|
| `account.created` | New account linked |
| `account.updated` | Credentials refreshed |
| `account.deleted` | Account disconnected |

Fetch `https://docs.stackone.com/guides/webhooks` for the webhook payload format and setup instructions.

### Step 5: Verify the connection

After receiving `onSuccess` or the `account.created` webhook, make a test API call:

```bash
curl https://api.stackone.com/accounts/{account_id} \
  -H "Authorization: Basic $(echo -n 'YOUR_API_KEY:' | base64)"
```

A `200` response with `status: "active"` confirms the connection is working.

## Examples

### Example 1: User wants to add an integration picker to a React app

User says: "I want to let my customers connect their BambooHR account"

Actions:
1. Create a backend endpoint that calls `POST /connect_sessions` with `provider: "bamboohr"`
2. Return the session token to the frontend
3. Install `@stackone/hub` and render `<StackOneHub token={token} />`
4. Handle `onSuccess` to store the account ID
5. Set up a webhook endpoint for `account.created` as a backup

Result: Working integration picker that filters to BambooHR only.

### Example 2: User wants to send connection links via email

User says: "I need to onboard customers by email, not in-app"

Actions:
1. Create a Connect Session with `origin_owner_id` set to the customer
2. Generate an auth link from the session (fetch auth link docs)
3. Set up webhook listeners — auth links have no frontend callbacks
4. Send the link via email (valid for 5 days)

Result: Customer clicks link, authenticates, webhook fires with account details.

## Troubleshooting

### Hub component doesn't render
**Cause**: Missing peer dependencies.
- `@stackone/hub` requires: `react`, `react-dom`, `react-hook-form`, `@hookform/resolvers`, `zod`
- Check that versions match — fetch the NPM page for exact version constraints
- Verify the session token is valid and not expired

### Connect Session token expired
**Cause**: Tokens are short-lived.
- Generate a new token for each Hub initialization
- Do not cache tokens across sessions

### onSuccess fires but account status is "error"
**Cause**: Provider-side authentication succeeded but StackOne couldn't sync data.
- Check the account details in the dashboard for the specific error
- Common cause: insufficient permissions on the provider side
- The provider may require additional OAuth scopes

### Webhooks not arriving
**Cause**: Webhook endpoint configuration issue.
- Verify the endpoint URL is publicly accessible (not localhost)
- Check the webhook signing secret matches
- Fetch `https://docs.stackone.com/guides/webhooks` for the verification process
