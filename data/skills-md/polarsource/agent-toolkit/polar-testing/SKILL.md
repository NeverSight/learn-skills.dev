---
name: polar-testing
description: |
  Guide for testing Polar payment integrations using the sandbox environment. Use this skill when: (1) Setting up the Polar sandbox for development; (2) Testing checkout flows without real payments; (3) Using Stripe test cards with Polar; (4) Writing integration tests for payment flows; (5) Testing webhooks locally with the Polar CLI (`polar webhook listen`, `polar webhook trigger`) and generating webhook fixtures; (6) Mocking Polar in unit tests; (7) Setting up CI/CD pipelines with Polar sandbox; (8) Debugging payment issues in sandbox.
---

# Polar Testing Guide

Test Polar integrations safely using the sandbox environment - a fully isolated server where you can experiment without affecting production data or processing real payments.

## Sandbox Environment

### Access

- **Dashboard**: https://sandbox.polar.sh
- **API**: https://sandbox-api.polar.sh/v1

The sandbox is completely isolated from production. You need separate:
- User account
- Organization
- Access tokens
- Webhook endpoints

### Setup Steps

1. Go to https://sandbox.polar.sh/start
2. Create a new account (or use "Go to sandbox" from org switcher)
3. Create a test organization
4. Generate an access token in Settings → Access Tokens, or with `polar auth token` once the CLI is signed in to the sandbox (see "Install and sign in" below)

### SDK Configuration

Set up the client as in `polar-integration` ("Setup") and pass `environment: "sandbox"`:

```typescript
import { createPolar } from "@polar-sh/sdk/2026-10";

const polar = createPolar({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  environment: "sandbox",
});
```

```python
import os

from polar.v2026_10 import Polar

polar = Polar(os.environ["POLAR_ACCESS_TOKEN"], environment="sandbox")
```

### Sandbox Limitations

- No real money is processed, and data is isolated from production
- Customer-facing emails (receipts, renewal reminders) are only delivered to members of your organization; `you+test@example.com` aliases are accepted
- The API allows 100 requests per minute, against 500 in production, which matters for large integration suites

## Test Cards

Polar uses Stripe for payment processing, so any of [Stripe's test cards](https://docs.stripe.com/testing#cards) work. Use a future expiry date and any CVC:

| Card Number | Behavior |
|-------------|----------|
| 4242 4242 4242 4242 | Successful payment |
| 4000 0000 0000 0002 | Generic decline |
| 4000 0000 0000 9995 | Insufficient funds |
| 4000 0027 6000 3184 | Requires 3D Secure authentication |

## Local Webhook Testing

Use the Polar CLI. It forwards your organization's webhook events straight to your local server: no tunnel, no public URL, and no webhook endpoint in the dashboard.

### Install and sign in

```bash
npm install -g @polar-sh/cli

polar auth login --sandbox
```

For other install methods, see the [CLI docs](https://polar.sh/docs/integrate/cli/introduction).

`polar auth login` opens a browser, so ask the user to run it. Check the result with `polar auth whoami --json`: `environments` lists the signed-in environments and `organization` is the active one.

Where no browser is available (CI, remote machines, cloud agents), an organization access token replaces `auth login`:

```bash
export POLAR_ACCESS_TOKEN=polar_oat_...   # scopes: webhooks:read, webhooks:write, organizations:read
export POLAR_ENVIRONMENT=sandbox
```

If `POLAR_ACCESS_TOKEN` is already exported in the shell, for example from the app's `.env`, the CLI uses it instead of the login.

### Forward events to your app

```bash
polar webhook listen 3000/api/polar/webhook
```

`listen` takes a port, a `port/path`, or a full URL. It runs until stopped, so start it in its own terminal or as a background process and keep it running while you test. It forwards every webhook event for the organization, including the ones real sandbox activity produces, such as completing a test checkout. If the account has several organizations, pick one with `--org <id>` or `polar auth org`.

### Set the webhook secret

`listen` signs forwarded events with a local secret, not a dashboard endpoint's secret. Write it to `.env` without printing it:

```bash
secret=$(polar webhook listen --print-secret) && echo "POLAR_WEBHOOK_SECRET=$secret" >> .env
```

If `.env` already has a `POLAR_WEBHOOK_SECRET` line, replace it instead of appending, then restart the dev server. Deployed environments use the secret of their dashboard webhook endpoint.

### Send test events

```bash
polar webhook trigger order.paid
```

`trigger` sends a sample event through the running `listen`. When your handler doesn't accept it (a non-2xx response, a connection error, or a redirect), it prints the handler's response body and exits with status 1. Read that output, fix the handler, and run the same command again until it exits with 0.

A redirect usually means auth middleware is intercepting the webhook route. Exclude the route from it: Polar never follows redirects when delivering webhooks.

```bash
polar webhook trigger --list --json                     # every event you can send
polar webhook trigger order.paid --override data.customer.email=jane@example.com
polar webhook trigger order.paid --seed 7               # the same IDs on every run
```

`--override` takes `path=value` and can be repeated. The API rejects paths that don't exist in the payload.

## Integration Testing

### Test Checkout Flow

Use an organization access token with the `products:write` and `checkouts:write` scopes. Organization tokens already imply the organization, so don't pass `organization_id`.

```typescript
import { describe, it, expect, beforeAll } from "vitest";
import { createPolar } from "@polar-sh/sdk/2026-10";

const polar = createPolar({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  environment: "sandbox",
});

describe("Polar Checkout", () => {
  let testProductId: string;

  beforeAll(async () => {
    const product = await polar.products.create({
      name: "Test Product",
      prices: [{ amount_type: "fixed", price_amount: 1000, price_currency: "usd" }],
    });
    testProductId = product.id;
  });

  it("creates a checkout session", async () => {
    const checkout = await polar.checkouts.create({
      products: [testProductId],
      success_url: "http://localhost:3000/success",
      customer_email: "test@example.com",
    });

    expect(checkout.status).toBe("open");
    expect(checkout.url).toContain("sandbox");
  });

  it("retrieves a checkout", async () => {
    const checkout = await polar.checkouts.create({
      products: [testProductId],
      success_url: "http://localhost:3000/success",
    });

    const retrieved = await polar.checkouts.get(checkout.id);
    expect(retrieved.id).toBe(checkout.id);
  });
});
```

### Test Webhook Handler

Generate fixtures from real payloads instead of writing them by hand. `--dry-run` prints the payload without sending it, so `listen` doesn't need to be running:

```bash
mkdir -p test/fixtures
polar webhook trigger order.paid --dry-run --json --seed 1 > test/fixtures/order.paid.json
polar webhook trigger subscription.created --dry-run --json --seed 1 > test/fixtures/subscription.created.json
```

Sign them the way `polar webhook listen` does ([Standard Webhooks](https://www.standardwebhooks.com/)): an HMAC-SHA256 of `id.timestamp.body`, base64-encoded and keyed with the secret string. This test calls the webhook route from `polar-integration` Recipe 3 directly:

```typescript
import { createHmac } from "node:crypto";
import { readFile } from "node:fs/promises";
import { beforeAll, describe, expect, it, vi } from "vitest";

const secret = "test_webhook_secret";
let POST: (request: Request) => Promise<Response>;

beforeAll(async () => {
  vi.stubEnv("POLAR_WEBHOOK_SECRET", secret);
  ({ POST } = await import("../app/api/polar/webhook/route"));
});

const sign = (id: string, timestamp: number, body: string) =>
  `v1,${createHmac("sha256", secret).update(`${id}.${timestamp}.${body}`).digest("base64")}`;

const webhookRequest = (body: string, signature?: string) => {
  const id = "msg_test";
  const timestamp = Math.floor(Date.now() / 1000);
  return new Request("http://localhost/api/polar/webhook", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "webhook-id": id,
      "webhook-timestamp": String(timestamp),
      "webhook-signature": signature ?? sign(id, timestamp, body),
    },
    body,
  });
};

describe("Polar webhook handler", () => {
  it("accepts a signed order.paid event", async () => {
    const body = await readFile("test/fixtures/order.paid.json", "utf8");
    const response = await POST(webhookRequest(body));
    expect(response.status).toBe(202);
  });

  it("rejects an invalid signature", async () => {
    const body = await readFile("test/fixtures/order.paid.json", "utf8");
    const response = await POST(webhookRequest(body, "v1,invalid"));
    expect(response.status).toBe(403);
  });
});
```

### Test License Key Validation

Validation needs a token with `license_keys:write`. A valid key returns `status: "granted"`; an unknown key throws `ResourceNotFound`:

```typescript
import { describe, it, expect } from "vitest";
import { createPolar, errors } from "@polar-sh/sdk/2026-10";

const polar = createPolar({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  environment: "sandbox",
});
const organization_id = process.env.POLAR_ORG_ID!;

describe("License keys", () => {
  it("validates a granted key", async () => {
    const result = await polar.licenseKeys.validate({ key: process.env.TEST_LICENSE_KEY!, organization_id });
    expect(result.status).toBe("granted");
  });

  it("rejects an unknown key", async () => {
    await expect(
      polar.licenseKeys.validate({ key: "INVALID-KEY", organization_id }),
    ).rejects.toBeInstanceOf(errors.ResourceNotFound);
  });
});
```

## Mocking Polar in Unit Tests

### Mock SDK

Mock `createPolar` and keep the real `webhooks` and `errors` exports. Responses use the same `snake_case` fields as the API:

```typescript
import { vi } from "vitest";

vi.mock("@polar-sh/sdk/2026-10", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@polar-sh/sdk/2026-10")>()),
  createPolar: () => ({
    checkouts: {
      create: vi.fn().mockResolvedValue({
        id: "checkout_mock",
        url: "https://sandbox.polar.sh/checkout/mock",
        status: "open",
      }),
      get: vi.fn().mockResolvedValue({ id: "checkout_mock", status: "succeeded" }),
    },
    customers: {
      getStateExternal: vi.fn().mockResolvedValue({
        active_subscriptions: [{ id: "sub_mock", status: "active", product_id: "prod_mock" }],
        granted_benefits: [],
        active_meters: [],
      }),
    },
    subscriptions: {
      revoke: vi.fn(),
      update: vi.fn(),
    },
  }),
}));
```

### Mock Webhook Payloads

Load the fixtures generated with `polar webhook trigger <event> --dry-run --json` (see Test Webhook Handler). Hand-written payloads drift from the real shape, and `validateEvent` only checks the signature and event type, so the drift goes unnoticed.

```typescript
import orderPaid from "./fixtures/order.paid.json";
import subscriptionCreated from "./fixtures/subscription.created.json";
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Test Polar Integration

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    env:
      POLAR_ACCESS_TOKEN: ${{ secrets.POLAR_SANDBOX_TOKEN }}
      POLAR_ORG_ID: ${{ secrets.POLAR_SANDBOX_ORG_ID }}

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "npm"

      - run: npm ci

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration
```

If CI also runs the Polar CLI, add `POLAR_ENVIRONMENT: sandbox`.

### Environment Setup

Create sandbox credentials specifically for CI:

1. Create a dedicated sandbox organization for CI
2. Create an organization access token for it with only the scopes the tests need (`polar auth token --scope products:write --scope checkouts:write` opens the token page with them preselected)
3. Commit the webhook fixtures; handler tests sign them with a test secret and need no webhook endpoint
4. Store the token and organization ID in GitHub Secrets

## Debugging Tips

### Check Webhook Delivery

Locally, `polar webhook listen` logs every forwarded event with your handler's status, and `polar webhook trigger` prints the handler's response body when it fails.

For a deployed endpoint:

1. Go to sandbox.polar.sh → Settings → Webhooks
2. Click on your endpoint
3. View delivery history and payloads
4. Check response codes and errors

### Common Issues

**Webhook signature mismatch**
- Ensure you're using the sandbox webhook secret
- Locally, use the secret from `polar webhook listen --print-secret` and restart the dev server after changing `.env`
- Check that the raw body is being passed (not parsed JSON)
- Verify timestamp is within tolerance (5 minutes)

**Checkout not completing**
- Use test cards, not real cards
- Check browser console for errors
- Verify `success_url` is correct

**API returns 401**
- Verify you're using a sandbox token with the sandbox API
- Check the token hasn't expired or been revoked

**API returns 403**
- The token is missing a scope the endpoint needs

### Inspect API Errors

The SDK throws typed errors with the HTTP status and response body:

```typescript
import { PolarClientError } from "@polar-sh/sdk";

try {
  await polar.checkouts.create({ products: [productId], success_url: "http://localhost:3000/success" });
} catch (error) {
  if (error instanceof PolarClientError) console.error(error.statusCode, error.error);
  throw error;
}
```

## Test Checklist

Before going to production:

- [ ] Checkout flow completes successfully
- [ ] Webhooks received and processed
- [ ] Subscription lifecycle works (create, cancel, revoke)
- [ ] Benefits granted and revoked correctly
- [ ] License key validation works
- [ ] Error handling for declined payments
- [ ] Customer portal accessible
- [ ] Refund flow tested
