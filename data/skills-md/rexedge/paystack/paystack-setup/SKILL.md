---
name: paystack-setup
description: >-
  Set up the Paystack API client, environment variables, and TypeScript helpers for
  server-side payment integration. Use this skill whenever starting a new Paystack
  integration, configuring API keys, creating a reusable fetch wrapper for the Paystack
  REST API, or setting up the foundation for any Paystack feature. Also use when you
  see errors related to missing PAYSTACK_SECRET_KEY, authentication failures, or need
  to understand Paystack's base URL, response format, pagination, currencies, or amount
  subunit conversion.
---

# Paystack Setup

Set up the foundational Paystack API client and environment configuration for TypeScript/JavaScript server-side applications.

## API Fundamentals

| Property | Value |
| --- | --- |
| Base URL | `https://api.paystack.co` |
| Auth Header | `Authorization: Bearer SECRET_KEY` |
| Content Type | `application/json` |
| Response Format | `{ status: boolean, message: string, data: object }` |
| Amount Unit | **Subunit** of currency (multiply display amount × 100) |
| Transaction ID | Unsigned 64-bit integer — use `string` in TypeScript |

## Supported Currencies & Subunits

| Currency | Code | Subunit | Multiplier |
| --- | --- | --- | --- |
| Nigerian Naira | NGN | kobo | ×100 |
| US Dollar | USD | cent | ×100 |
| Ghanaian Cedi | GHS | pesewa | ×100 |
| South African Rand | ZAR | cent | ×100 |
| Kenyan Shilling | KES | cent | ×100 |
| West African CFA | XOF | — | ×100 |
| Egyptian Pound | EGP | piaster | ×100 |
| Rwandan Franc | RWF | — | ×100 |

## Environment Variables

Create a `.env` file (or `.env.local` for Next.js):

```env
PAYSTACK_SECRET_KEY=sk_test_xxxxx        # Server-side only, NEVER expose to client
NEXT_PUBLIC_PAYSTACK_PUBLIC_KEY=pk_test_xxxxx  # Safe for client-side (Popup/InlineJS)
```

The secret key (`sk_*`) must NEVER appear in client-side code, browser bundles, or public repositories. The public key (`pk_*`) is safe for front-end use with Paystack Popup/InlineJS only.

Test keys start with `sk_test_` / `pk_test_`. Live keys start with `sk_live_` / `pk_live_`. Get them from the Paystack Dashboard under Settings → API Keys & Webhooks.

## Install Dependencies

```bash
# For client-side Popup/InlineJS checkout
npm install @paystack/inline-js

# Or with pnpm / yarn
pnpm add @paystack/inline-js
yarn add @paystack/inline-js
```

No server-side SDK is needed — use the built-in `fetch` API with the helper below.

## TypeScript API Client Helper

Create a reusable, type-safe Paystack client. Every other Paystack skill depends on this pattern:

```typescript
// lib/paystack.ts
const PAYSTACK_SECRET_KEY = process.env.PAYSTACK_SECRET_KEY;

if (!PAYSTACK_SECRET_KEY) {
  throw new Error("PAYSTACK_SECRET_KEY is not set in environment variables");
}

export interface PaystackResponse<T = unknown> {
  status: boolean;
  message: string;
  data: T;
}

export interface PaystackListResponse<T = unknown> {
  status: boolean;
  message: string;
  data: T[];
  meta: {
    total: number;
    skipped: number;
    perPage: number;
    page: number;
    pageCount: number;
  };
}

export class PaystackError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public response?: unknown
  ) {
    super(message);
    this.name = "PaystackError";
  }
}

export async function paystackRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<PaystackResponse<T>> {
  const url = `https://api.paystack.co${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${PAYSTACK_SECRET_KEY}`,
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new PaystackError(
      data.message || `Paystack API error: ${response.status}`,
      response.status,
      data
    );
  }

  return data as PaystackResponse<T>;
}
```

## Pagination

All list endpoints accept `perPage` (default: 50, max: 100) and `page` (default: 1) as query parameters. The response includes a `meta` object:

```json
{
  "meta": {
    "total": 243,
    "skipped": 0,
    "perPage": 50,
    "page": 1,
    "pageCount": 5
  }
}
```

Build paginated queries like so:

```typescript
const params = new URLSearchParams({
  perPage: "20",
  page: "2",
  from: "2024-01-01T00:00:00.000Z",
  to: "2024-12-31T23:59:59.000Z",
});
const result = await paystackRequest<Transaction[]>(`/transaction?${params}`);
```

## Amount Conversion

Always convert display amounts to subunits before sending to Paystack, and convert back when displaying:

```typescript
// Display → Paystack (multiply by 100)
const amountInKobo = Math.round(amountInNaira * 100);

// Paystack → Display (divide by 100)
const amountInNaira = amountInKobo / 100;
```

Use `Math.round()` to avoid floating-point issues like `19.99 * 100 = 1998.9999999999998`.

## HTTP Methods

| Method | Usage |
| --- | --- |
| POST | Create resources, initiate actions |
| GET | Fetch, list, verify resources |
| PUT | Update resources |
| DELETE | Deactivate or remove resources |

## Error Handling

Wrap Paystack calls in try/catch and handle the `PaystackError` class:

```typescript
import { paystackRequest, PaystackError } from "@/lib/paystack";

try {
  const result = await paystackRequest<Transaction>("/transaction/verify/ref_123");
} catch (error) {
  if (error instanceof PaystackError) {
    console.error(`Paystack error ${error.statusCode}: ${error.message}`);
    // Handle specific status codes
    if (error.statusCode === 400) { /* bad request / validation error */ }
    if (error.statusCode === 401) { /* invalid secret key */ }
    if (error.statusCode === 404) { /* resource not found */ }
  }
  throw error;
}
```

## Security Checklist

- Store `PAYSTACK_SECRET_KEY` in environment variables only, never in code
- Add `.env` and `.env.local` to `.gitignore`
- All Paystack API calls must run server-side (API routes, server actions, backend)
- Use HTTPS for all callback and webhook URLs
- Validate amounts server-side before initializing transactions
- Always verify transaction status server-side after payment, never trust client-side callbacks alone
