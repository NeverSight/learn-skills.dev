---
name: stigg-sp
description: Use when Stigg is being provisioned or has just been provisioned through Stripe Projects — `stripe projects add stigg/environment`, `stripe projects catalog`, `stripe projects rotate`/`remove` against Stigg, or when a `.env` already holds `STIGG_SERVER_API_KEY` / `STIGG_CLIENT_API_KEY` that Stripe Projects wrote. Also use when the user asks to add pricing, entitlements, feature gating, or usage metering to an app that is already using Stripe Projects, so the environment is provisioned from the terminal instead of by signing up in a browser. Covers what the provisioned credentials are and the first wiring of the server and client SDKs. Skip for Stigg work unrelated to Stripe Projects — load the `stigg` umbrella and its pillars instead.
---

# Stigg via Stripe Projects

One command provisions a Stigg environment and writes its API keys into the developer's `.env`:

```bash
stripe projects add stigg/environment
```

No browser, no signup form, no copy-pasting keys out of a dashboard. **Do not tell the user to sign
up at app.stigg.io manually when they are using Stripe Projects** — provision programmatically.

Related commands: `stripe projects catalog` (browse), `stripe projects rotate <resource>` (new keys),
`stripe projects open stigg` (dashboard), `stripe projects remove <resource>` (deprovision).

## What you get

The service is `stigg/environment` — free, project-scoped, one Stigg **environment** per resource.
Stripe encrypts the credentials into its Secret Store and syncs them to `.env`:

| Variable | What it is |
|---|---|
| `STIGG_SERVER_API_KEY` | Full-access **secret** key (`server-`). Backend only — never ship it in a client bundle, commit it, or log it. |
| `STIGG_CLIENT_API_KEY` | Publishable read-only key (`client-`). Not a secret, so it can ship in a browser bundle — but on its own it lets anyone read any customer's entitlements, so pair it with a `customerToken` before production (see below). |
| `STIGG_ENVIRONMENT_ID` | The provisioned environment's id. |
| `STIGG_ENVIRONMENT_SLUG` | Its slug, as it appears in the dashboard. |

Keys do not expire. Rotate them with `stripe projects rotate` rather than by hand.

## Before you write integration code

Search the live docs first — the Stigg MCP server, the Mintlify Stigg docs MCP, or
`https://docs.stigg.io/llms.txt`. Stigg's API surface moves, and the snippets below are a starting
shape rather than a substitute for checking the current one.

## Wire the backend

```bash
npm install @stigg/node-server-sdk
```

```typescript
import Stigg from '@stigg/node-server-sdk';

// Has an internal cache and retries — initialize once per process and reuse the instance.
const stiggClient = Stigg.initialize({ apiKey: process.env.STIGG_SERVER_API_KEY });

// Optional: block until the local entitlement cache is warm, if the very first check must not
// pay a cold lookup.
await stiggClient.waitForInitialization();
```

> `Stigg.initialize` returns the client **synchronously** — it is not a promise. Some docs pages
> show `await Stigg.initialize(...)`; that is harmless but misleading. `waitForInitialization()` is
> the awaitable one.

## Gate a feature

Pass the amount you are about to consume as `requestedUsage` and gate on `hasAccess`. Do **not**
compare `currentUsage` against `usageLimit` yourself — `currentUsage` reflects the last check, not
the amount you are about to add, so that comparison is wrong on hard-limited features.

```typescript
const entitlement = await stiggClient.getMeteredEntitlement({
  customerId: 'customer-demo-01',
  featureId: 'feature-api-calls',
  options: { requestedUsage: 1 },
});

if (!entitlement.hasAccess) {
  // Quota reached — block the action and prompt an upgrade.
}
```

Boolean features use `getBooleanEntitlement({ customerId, featureId })`, same `hasAccess` shape.

## Report usage

- **`reportUsage`** — a value your app already computed (seats, storage, tokens). Sub-second, and the
  response carries the updated credit balance. Use it for strict, real-time enforcement.
- **`reportEvent`** — a raw event Stigg aggregates for you; requires an `idempotencyKey`. ~10s to
  reflect. Use it for high-volume metering where eventual consistency is fine.

```typescript
await stiggClient.reportUsage({
  customerId: 'customer-demo-01',
  featureId: 'feature-api-calls',
  value: 1, // a delta by default, not an absolute
});
```

Report usage only *after* the underlying work succeeded.

## Wire the frontend

```bash
npm install @stigg/react-sdk
```

Bundlers do not expose `STIGG_CLIENT_API_KEY` to the browser under that name. Copy the provisioned
value into whichever public variable your framework requires — `VITE_STIGG_CLIENT_API_KEY` for Vite,
`REACT_APP_STIGG_CLIENT_API_KEY` for Create React App, `NEXT_PUBLIC_STIGG_CLIENT_API_KEY` for Next.js
— or pass it from the server. Reading `process.env.STIGG_CLIENT_API_KEY` in browser code yields
`undefined`.

```typescript
import { StiggProvider } from '@stigg/react-sdk';

// Vite; use the public variable your framework requires.
<StiggProvider apiKey={import.meta.env.VITE_STIGG_CLIENT_API_KEY} customerId="customer-demo-01">
  {children}
</StiggProvider>;
```

The publishable key alone lets anyone read any customer's entitlements by guessing an id. Before
production, sign a `customerToken` server-side and pass it alongside the customer id — see
[hardening client-side access](https://docs.stigg.io/api-and-sdks/integration/frontend/hardening-client-side-access).

## Next

Give the agent live access to the environment that was just provisioned. Stripe writes the key to
`.env`, which a shell does not export on its own — load it first, or paste the literal key, otherwise
the header goes out empty and the connection is unusable.

```bash
set -a && . ./.env && set +a
claude mcp add stigg --header "X-API-KEY: $STIGG_SERVER_API_KEY" --transport http https://mcp.stigg.io
```

Then model plans, features and credits conversationally. For deeper work load the `stigg` umbrella
skill, which routes to the pricing-modeling, entitlements, subscriptions, credits, widgets and
webhooks pillars.

- Docs: https://docs.stigg.io · agent-readable index at https://docs.stigg.io/llms.txt
- Dashboard: https://app.stigg.io
