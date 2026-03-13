---
name: paystack-testing
description: >-
  Paystack Testing Guide — comprehensive testing strategies for Paystack integrations
  using test mode keys. Covers test card numbers, bank account test data, webhook
  testing, transaction simulation, transfer testing, and end-to-end test patterns.
  Use this skill whenever writing tests for Paystack payments, simulating transactions
  in test mode, testing webhook handlers, mocking Paystack API responses, validating
  payment flows before going live, or debugging failed test transactions. Also use when
  you see references to sk_test_, pk_test_, test card numbers, or Paystack test mode.
---

# Paystack Testing

Complete guide for testing Paystack integrations in test mode.

> Depends on: **paystack-setup** for the `paystackRequest` helper.

## Test Environment Setup

### Environment Variables

```env
# .env.test (or .env.local for development)
PAYSTACK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NEXT_PUBLIC_PAYSTACK_PUBLIC_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> **Never commit real keys**. Use `sk_test_*` / `pk_test_*` keys from your Paystack Dashboard → Settings → API Keys & Webhooks.

### Test vs Live Mode

| Aspect | Test Mode | Live Mode |
| --- | --- | --- |
| Key prefix | `sk_test_` / `pk_test_` | `sk_live_` / `pk_live_` |
| Real charges | No | Yes |
| Webhooks | Sent to test webhook URL | Sent to live webhook URL |
| Card validation | Simulated | Real bank processing |
| Transfers | Simulated (no real payout) | Real bank transfers |

## Test Card Numbers

Use these with the Paystack Popup or Charge API in test mode:

| Card Number | Expiry | CVV | Behavior |
| --- | --- | --- | --- |
| `4084 0840 8408 4081` | Any future date | `408` | Successful transaction |
| `4084 0840 8408 4081` | Any future date | `408` | PIN auth → use `1234` |
| `5060 6666 6666 6666 666` | Any future date | `123` | Verve card — success |
| `5078 5078 5078 5078 12` | Any future date | `081` | Insufficient funds |
| `4000 0000 0000 0002` | Any future date | Any | Card declined |

### PIN, OTP, and other test values

| Auth | Test Value |
| --- | --- |
| PIN | `1234` |
| OTP | `123456` |
| Phone | `08012345678` |
| Birthday | `1999-12-31` |

## Integration Tests with TypeScript

### Transaction Flow Test

```typescript
import { describe, it, expect, beforeAll } from "vitest";

const BASE_URL = "https://api.paystack.co";
const SECRET_KEY = process.env.PAYSTACK_SECRET_KEY!;

async function paystackRequest<T = any>(
  path: string,
  options: RequestInit = {}
): Promise<{ status: boolean; message: string; data: T }> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${SECRET_KEY}`,
      "Content-Type": "application/json",
      ...options.headers,
    },
  });
  return res.json();
}

describe("Paystack Transaction Flow", () => {
  let authorizationUrl: string;
  let reference: string;

  it("should initialize a transaction", async () => {
    const res = await paystackRequest<{
      authorization_url: string;
      access_code: string;
      reference: string;
    }>("/transaction/initialize", {
      method: "POST",
      body: JSON.stringify({
        email: "test@example.com",
        amount: 50000, // ₦500
        callback_url: "https://example.com/callback",
      }),
    });

    expect(res.status).toBe(true);
    expect(res.data.authorization_url).toContain("paystack.com");
    expect(res.data.reference).toBeTruthy();
    authorizationUrl = res.data.authorization_url;
    reference = res.data.reference;
  });

  it("should verify transaction (pending before payment)", async () => {
    const res = await paystackRequest(`/transaction/verify/${reference}`);
    // In test mode without completing payment, status may be "abandoned"
    expect(res.status).toBe(true);
  });

  it("should list transactions", async () => {
    const res = await paystackRequest("/transaction?perPage=5");
    expect(res.status).toBe(true);
    expect(Array.isArray(res.data)).toBe(true);
  });
});
```

### Customer API Tests

```typescript
describe("Paystack Customers", () => {
  let customerCode: string;

  it("should create a customer", async () => {
    const res = await paystackRequest<{
      customer_code: string;
      email: string;
    }>("/customer", {
      method: "POST",
      body: JSON.stringify({
        email: `test-${Date.now()}@example.com`,
        first_name: "Test",
        last_name: "User",
      }),
    });

    expect(res.status).toBe(true);
    expect(res.data.customer_code).toMatch(/^CUS_/);
    customerCode = res.data.customer_code;
  });

  it("should fetch the customer", async () => {
    const res = await paystackRequest(`/customer/${customerCode}`);
    expect(res.status).toBe(true);
    expect(res.data.customer_code).toBe(customerCode);
  });
});
```

### Plan + Subscription Tests

```typescript
describe("Paystack Plans", () => {
  let planCode: string;

  it("should create a plan", async () => {
    const res = await paystackRequest<{ plan_code: string }>("/plan", {
      method: "POST",
      body: JSON.stringify({
        name: `Test Plan ${Date.now()}`,
        interval: "monthly",
        amount: 100000, // ₦1,000
      }),
    });

    expect(res.status).toBe(true);
    expect(res.data.plan_code).toMatch(/^PLN_/);
    planCode = res.data.plan_code;
  });

  it("should list plans", async () => {
    const res = await paystackRequest("/plan?perPage=5");
    expect(res.status).toBe(true);
  });

  it("should fetch the plan", async () => {
    const res = await paystackRequest(`/plan/${planCode}`);
    expect(res.status).toBe(true);
    expect(res.data.plan_code).toBe(planCode);
  });
});
```

### Transfer Recipient + Transfer Tests

```typescript
describe("Paystack Transfers", () => {
  let recipientCode: string;

  it("should create a transfer recipient", async () => {
    const res = await paystackRequest<{ recipient_code: string }>(
      "/transferrecipient",
      {
        method: "POST",
        body: JSON.stringify({
          type: "nuban",
          name: "Test Recipient",
          account_number: "0000000000",
          bank_code: "058",
          currency: "NGN",
        }),
      }
    );

    expect(res.status).toBe(true);
    expect(res.data.recipient_code).toMatch(/^RCP_/);
    recipientCode = res.data.recipient_code;
  });

  it("should initiate a transfer (test mode)", async () => {
    const res = await paystackRequest("/transfer", {
      method: "POST",
      body: JSON.stringify({
        source: "balance",
        amount: 10000, // ₦100
        recipient: recipientCode,
        reason: "Test transfer",
      }),
    });

    // In test mode, transfers are simulated
    expect(res.status).toBe(true);
  });
});
```

## Webhook Testing

### Unit Test for Webhook Signature Validation

```typescript
import { createHmac } from "crypto";
import { describe, it, expect } from "vitest";

function validateWebhookSignature(
  body: string,
  signature: string,
  secret: string
): boolean {
  const hash = createHmac("sha512", secret).update(body).digest("hex");
  return hash === signature;
}

describe("Webhook Signature Validation", () => {
  const secret = "sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";

  it("should validate a correct signature", () => {
    const body = JSON.stringify({
      event: "charge.success",
      data: { reference: "test_ref_123" },
    });
    const signature = createHmac("sha512", secret).update(body).digest("hex");

    expect(validateWebhookSignature(body, signature, secret)).toBe(true);
  });

  it("should reject an invalid signature", () => {
    const body = JSON.stringify({ event: "charge.success" });
    expect(validateWebhookSignature(body, "invalid_hash", secret)).toBe(false);
  });

  it("should reject a tampered body", () => {
    const body = JSON.stringify({ event: "charge.success" });
    const signature = createHmac("sha512", secret).update(body).digest("hex");
    const tampered = JSON.stringify({ event: "charge.failed" });

    expect(validateWebhookSignature(tampered, signature, secret)).toBe(false);
  });
});
```

### Testing Webhooks Locally

Use Paystack's test mode + a tunnel service:

```bash
# 1. Start your local server
npm run dev

# 2. Expose localhost via tunnel (pick one)
npx localtunnel --port 3000
# or
ngrok http 3000

# 3. Set the tunnel URL as your test webhook URL in Paystack Dashboard
#    Dashboard → Settings → API Keys & Webhooks → Test Webhook URL

# 4. Trigger events by completing test transactions
#    Paystack will send webhooks to your tunnel URL
```

### Mock Webhook Handler Test

```typescript
import { describe, it, expect, vi } from "vitest";
import { createHmac } from "crypto";

// Simulates a POST to your webhook endpoint
async function simulateWebhook(
  handler: (req: Request) => Promise<Response>,
  event: string,
  data: Record<string, unknown>,
  secret: string
) {
  const body = JSON.stringify({ event, data });
  const signature = createHmac("sha512", secret).update(body).digest("hex");

  return handler(
    new Request("http://localhost/api/webhooks/paystack", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-paystack-signature": signature,
      },
      body,
    })
  );
}

describe("Webhook Handler", () => {
  const secret = "sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";

  it("should process charge.success event", async () => {
    const processPayment = vi.fn();

    // Your actual webhook handler
    async function webhookHandler(req: Request): Promise<Response> {
      const body = await req.text();
      const sig = req.headers.get("x-paystack-signature")!;
      const hash = createHmac("sha512", secret).update(body).digest("hex");

      if (hash !== sig) {
        return new Response("Unauthorized", { status: 401 });
      }

      const { event, data } = JSON.parse(body);
      if (event === "charge.success") {
        processPayment(data);
      }
      return new Response("OK", { status: 200 });
    }

    const res = await simulateWebhook(
      webhookHandler,
      "charge.success",
      { reference: "test_123", amount: 50000, currency: "NGN" },
      secret
    );

    expect(res.status).toBe(200);
    expect(processPayment).toHaveBeenCalledWith(
      expect.objectContaining({ reference: "test_123" })
    );
  });
});
```

## Bank Account Resolution Test

```typescript
describe("Bank Verification", () => {
  it("should resolve a bank account", async () => {
    const res = await paystackRequest(
      "/bank/resolve?account_number=0000000000&bank_code=058"
    );
    // Test mode may return mock data
    expect(res.status).toBe(true);
  });

  it("should list banks", async () => {
    const res = await paystackRequest("/bank?country=nigeria&perPage=10");
    expect(res.status).toBe(true);
    expect(res.data.length).toBeGreaterThan(0);
    expect(res.data[0]).toHaveProperty("code");
    expect(res.data[0]).toHaveProperty("name");
  });
});
```

## Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    testTimeout: 30_000, // API calls may take time
    setupFiles: ["./tests/setup.ts"],
  },
});
```

```typescript
// tests/setup.ts
import { config } from "dotenv";
config({ path: ".env.test" });

if (!process.env.PAYSTACK_SECRET_KEY?.startsWith("sk_test_")) {
  throw new Error(
    "Tests must use test mode keys (sk_test_*). Never run tests with live keys."
  );
}
```

## Checklist Before Going Live

- [ ] All tests pass with `sk_test_` keys
- [ ] Webhook signature validation tested (valid + invalid + tampered)
- [ ] Transaction initialize → verify flow tested
- [ ] Error responses handled (invalid amount, missing fields, etc.)
- [ ] Idempotency: duplicate references handled gracefully
- [ ] Switch to `sk_live_` / `pk_live_` keys in production environment
- [ ] Live webhook URL configured in Dashboard
- [ ] IP whitelist verified for webhook source (52.31.139.75, 52.49.173.169, 52.214.14.220)
