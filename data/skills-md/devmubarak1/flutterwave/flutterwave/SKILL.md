---
name: flutterwave
description: Complete Flutterwave integration skill supporting both v3 Production and v4 Public Beta APIs across checkout, cards, bank transfers, mobile money, transfers, virtual accounts, and webhooks.
---

# flutterwave

The complete, production-ready AI agent skill for integrating the **Flutterwave API**. Natively supports both **v3 (Production Stable)** and **v4 (Next-Gen Public Beta)** so developers and AI agents can choose and switch versions seamlessly without third-party CLI or proxy dependencies.

- **Official Docs (v3):** https://developer.flutterwave.com/docs
- **API Reference (v3):** https://developer.flutterwave.com/reference
- **Official AI Index (v3):** https://developer.flutterwave.com/llms.txt
- **Official Docs & AI Index (v4):** https://developer.flutterwave.com/v4.0.0/llms.txt
- **Markdown Docs Shortcut:** Append `.md` to any Flutterwave documentation URL (e.g. `https://developer.flutterwave.com/docs/getting-started.md`) for clean markdown without HTML noise.

---

## Architecture & Version Comparison

| Feature | v3 (Production Stable) | v4 (Next-Gen Public Beta) |
| --- | --- | --- |
| **Status** | Globally deployed, battle-tested | Public Beta (high performance, microservices) |
| **Base URL** | `https://api.flutterwave.com/v3` | Sandbox: `https://developersandbox-api.flutterwave.com`<br>Live: `https://f4bexperience.flutterwave.com/` |
| **Authentication** | Static Secret Key Bearer (`FLW_SECRET_KEY`) | OAuth 2.0 OpenID Connect Client Credentials (`client_id` + `client_secret`) |
| **Token Endpoint** | N/A | `POST https://idp.flutterwave.com/realms/flutterwave/protocol/openid-connect/token` |
| **Tracing Header** | Optional | `X-Trace-Id` (12–255 char UUID, required) |
| **Idempotency** | Custom `tx_ref` in payload | `X-Idempotency-Key` header + `reference` in payload |
| **Primary Inflow** | `POST /payments` or `POST /charges` | `POST /charges` with `customer_id` and `payment_method_id` |
| **Primary Outflow** | `POST /transfers` with account details | `POST /transfers` with `payment_instruction` & `recipient_id` |

---

## Universal Client Implementation (TypeScript)

Zero external CLI dependencies. Provides full dual-version execution, automatic v4 OAuth 2.0 token caching, and request tracing.

```ts
import crypto from "node:crypto";

export interface FlutterwaveConfig {
  secretKey?: string; // v3 secret key (e.g., FLWSECK_TEST-... or FLWSECK-...)
  encryptionKey?: string; // v3 3DES encryption key for direct card charges
  v4ClientId?: string; // v4 OAuth2 client_id
  v4ClientSecret?: string; // v4 OAuth2 client_secret
  v3BaseUrl?: string; // default: https://api.flutterwave.com/v3
  v4BaseUrl?: string; // sandbox: https://developersandbox-api.flutterwave.com | live: https://f4bexperience.flutterwave.com/
  v4IdpUrl?: string; // default: https://idp.flutterwave.com/realms/flutterwave/protocol/openid-connect/token
}

export interface FlwResponse<T = unknown> {
  status: "success" | "error";
  message: string;
  data: T;
  meta?: Record<string, unknown>;
}

export class FlutterwaveApiError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly payload?: unknown,
  ) {
    super(message);
    this.name = "FlutterwaveApiError";
  }
}

export class Flutterwave {
  private readonly config: FlutterwaveConfig;
  private v4TokenCache: { token: string; expiresAt: number } | null = null;

  constructor(config: FlutterwaveConfig = {}) {
    this.config = {
      secretKey: config.secretKey ?? process.env.FLW_SECRET_KEY,
      encryptionKey: config.encryptionKey ?? process.env.FLW_ENCRYPTION_KEY,
      v4ClientId: config.v4ClientId ?? process.env.FLW_V4_CLIENT_ID,
      v4ClientSecret: config.v4ClientSecret ?? process.env.FLW_V4_CLIENT_SECRET,
      v3BaseUrl: config.v3BaseUrl ?? process.env.FLW_V3_BASE_URL ?? "https://api.flutterwave.com/v3",
      v4BaseUrl: config.v4BaseUrl ?? process.env.FLW_V4_BASE_URL ?? "https://developersandbox-api.flutterwave.com",
      v4IdpUrl: config.v4IdpUrl ?? "https://idp.flutterwave.com/realms/flutterwave/protocol/openid-connect/token",
    };
  }

  /**
   * Retrieves or refreshes OAuth 2.0 access token for v4 requests.
   */
  private async getV4Token(): Promise<string> {
    const now = Date.now();
    if (this.v4TokenCache && this.v4TokenCache.expiresAt > now + 60_000) {
      return this.v4TokenCache.token;
    }

    if (!this.config.v4ClientId || !this.config.v4ClientSecret) {
      throw new Error("Missing v4 credentials: FLW_V4_CLIENT_ID and FLW_V4_CLIENT_SECRET are required for v4 calls.");
    }

    const res = await fetch(this.config.v4IdpUrl!, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "client_credentials",
        client_id: this.config.v4ClientId,
        client_secret: this.config.v4ClientSecret,
      }).toString(),
    });

    if (!res.ok) {
      throw new FlutterwaveApiError(`Failed to fetch v4 OAuth token: ${res.statusText}`, res.status);
    }

    const data = (await res.json()) as { access_token: string; expires_in: number };
    this.v4TokenCache = {
      token: data.access_token,
      expiresAt: now + data.expires_in * 1000,
    };

    return data.access_token;
  }

  /**
   * Executes a typed API request to either v3 or v4.
   */
  async request<T = unknown>(
    version: "v3" | "v4",
    path: string,
    options: RequestInit & { idempotencyKey?: string } = {},
  ): Promise<FlwResponse<T>> {
    const { idempotencyKey, headers: customHeaders, ...init } = options;
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(customHeaders as Record<string, string>),
    };

    let baseUrl: string;
    if (version === "v3") {
      if (!this.config.secretKey) {
        throw new Error("Missing FLW_SECRET_KEY for v3 request");
      }
      baseUrl = this.config.v3BaseUrl!;
      headers["Authorization"] = `Bearer ${this.config.secretKey}`;
    } else {
      baseUrl = this.config.v4BaseUrl!;
      const token = await this.getV4Token();
      headers["Authorization"] = `Bearer ${token}`;
      headers["X-Trace-Id"] = crypto.randomUUID();
      if (idempotencyKey) {
        headers["X-Idempotency-Key"] = idempotencyKey;
      }
    }

    const url = `${baseUrl}${path.startsWith("/") ? path : `/${path}`}`;
    const response = await fetch(url, { ...init, headers });
    const body = (await response.json()) as FlwResponse<T>;

    if (!response.ok || body.status === "error") {
      throw new FlutterwaveApiError(
        body.message || `Flutterwave ${version} request failed with status ${response.status}`,
        response.status,
        body,
      );
    }

    return body;
  }
}
```

---

## Popular Actions & Version Matrix

Any developer or AI agent using this skill can execute any operation in either v3 or v4:

| Action | Method | v3 Route | v4 Beta Route | Key Parameters / Description |
| --- | --- | --- | --- | --- |
| **Standard Hosted Checkout** | `POST` | `/payments` | `/charges` | `tx_ref`, `amount`, `currency`, `redirect_url`, `customer: { email, name }`. Returns checkout URL. |
| **Verify Transaction (by ID)** | `GET` | `/transactions/{id}/verify` | `/charges/{id}` | Confirms final payment status, settled amount, and card token. Mandatory before order fulfillment. |
| **Verify Transaction (by ref)** | `GET` | `/transactions/verify_by_reference?tx_ref=...` | `/charges?reference=...` | Queries payment using the merchant's custom order/transaction reference. |
| **List Transactions** | `GET` | `/transactions` | `/charges` | Filters by `from`, `to`, `status`, `currency`, and pagination `page`. |
| **Direct Card Charge** | `POST` | `/charges?type=card` | `/charges` | v3 uses 3DES encrypted payload; v4 uses `payment_method_id` with `authorization`. |
| **Validate Charge (OTP)** | `POST` | `/validate-charge` | `/charges/{id}/validate` | Submits customer OTP challenge code (`flw_ref`, `otp`). |
| **Bank Transfer Collection** | `POST` | `/charges?type=bank_transfer` | `/virtual-accounts` | Generates dynamic dedicated Nigerian NIP bank account with expiry timer. |
| **Mobile Money (M-Pesa)** | `POST` | `/charges?type=mpesa` | `/charges` | Triggers instant STK push prompt on customer mobile device in Kenya (`KES`). |
| **Mobile Money (Ghana)** | `POST` | `/charges?type=mobile_money_ghana` | `/charges` | Charges MTN, Telecel (Vodafone voucher), or AirtelTigo wallets (`GHS`). |
| **USSD Payment** | `POST` | `/charges?type=ussd` | `/charges` | Returns bank-specific interactive dial code (e.g. `*737*...#` for GTBank) for offline payments. |
| **Tokenized Charge** | `POST` | `/tokenized-charges` | `/charges` (`recurring: true`) | Re-bills stored `card.token` for 1-click checkout and subscriptions without card entry. |
| **Initiate Transfer (Payout)** | `POST` | `/transfers` | `/transfers` | Disburses funds to bank accounts or mobile wallets. v4 uses `payment_instruction` + `action`. |
| **Get Transfer Status** | `GET` | `/transfers/{id}` | `/transfers/{id}` | Inspects payout status (`SUCCESSFUL`, `FAILED`, `PENDING`). |
| **Retry Transfer** | `POST` | `/transfers/{id}/retries` | `/transfers/{id}/retry` | Resubmits failed transfer for reprocessing. |
| **List Beneficiaries** | `GET` | `/beneficiaries` | `/transfer-recipients` | Lists saved bank account and mobile wallet payout contacts. |
| **Create Beneficiary** | `POST` | `/beneficiaries` | `/transfer-recipients` | Saves recipient (`account_number`, `account_bank`, `beneficiary_name`, `currency`). |
| **Create Virtual Account** | `POST` | `/virtual-account-numbers` | `/virtual-accounts` | Provisions permanent or dynamic virtual bank accounts for direct customer wallet funding. |
| **Bulk Virtual Accounts** | `POST` | `/bulk-virtual-account-numbers` | `/virtual-accounts` | Batches creation of dedicated virtual accounts for fintech platforms. |
| **Create Subaccount (Split)** | `POST` | `/subaccounts` | Split configuration | Configures vendor subaccount for marketplace splits (`split_type: "percentage" \| "flat"`). |
| **Create Payment Plan** | `POST` | `/payment-plans` | Subscription plans | Sets automated subscription billing intervals (`daily`, `weekly`, `monthly`, `yearly`). |
| **Create Virtual Card** | `POST` | `/virtual-cards` | Card issuing | Issues digital dollar (`USD`) or local currency debit cards with billing address. |
| **Resolve Bank Account** | `POST` | `/accounts/resolve` | `/accounts/lookup` | Verifies Nigerian bank account number and resolves official registered account holder name. |
| **Validate BVN** | `POST` | `/bvn/match` | KYC validation | Confirms Bank Verification Number matches customer legal identity for compliance. |
| **Issue Refund** | `POST` | `/transactions/{id}/refund` | `/refunds` | Issues full or partial refunds directly to customer's source account. |
| **Manage Chargebacks** | `GET` / `PUT` | `/chargebacks` | `/chargebacks` | Queries open dispute claims and submits defense evidence before the due date. |
| **List Settlements** | `GET` | `/settlements` | `/settlement` | Reconciles bank deposits, gross transactions, and processor fee deductions. |
| **Pay Bills & Airtime** | `POST` | `/bills` | Utility bills | Purchases airtime, mobile data bundles, power tokens, and renews cable TV subscriptions. |

---

## Action Code Recipes

### 1. Create a Standard Checkout Payment Link (v3)

```ts
const flw = new Flutterwave();

const session = await flw.request<{ link: string }>("v3", "/payments", {
  method: "POST",
  body: JSON.stringify({
    tx_ref: `ORD-${Date.now()}`,
    amount: "7500.00",
    currency: "NGN",
    redirect_url: "https://yourdomain.com/checkout/callback",
    customer: {
      email: "buyer@example.com",
      name: "Amina Bello",
      phonenumber: "+2348012345678",
    },
    customizations: {
      title: "Store Checkout",
      description: "Payment for order #1082",
    },
  }),
});

console.log("Customer Payment URL:", session.data.link);
```

### 2. Mandatory Server-Side Transaction Verification (v3 & v4)

```ts
const flw = new Flutterwave();

// v3 verification by Transaction ID
const v3Tx = await flw.request<{
  status: string;
  amount: number;
  currency: string;
  tx_ref: string;
  card?: { token: string };
}>("v3", `/transactions/${transactionId}/verify`, { method: "GET" });

if (v3Tx.data.status === "successful" && v3Tx.data.amount >= orderAmount) {
  // Safe to credit account or ship goods
  const savedCardToken = v3Tx.data.card?.token;
}

// v4 Next-Gen verification by Charge ID
const v4Charge = await flw.request<{
  status: string;
  amount: number;
  currency: string;
  reference: string;
}>("v4", `/charges/${chargeId}`, { method: "GET" });
```

### 3. Initiate Instant Bank Transfer / Payout (v3 & v4)

```ts
const flw = new Flutterwave();

// v3 Payout
const v3Payout = await flw.request("v3", "/transfers", {
  method: "POST",
  body: JSON.stringify({
    account_bank: "058", // GTBank
    account_number: "0123456789",
    amount: 50000,
    currency: "NGN",
    reference: `PAYOUT-${Date.now()}`,
    narration: "Vendor disbursement",
  }),
});

// v4 Next-Gen Transfer Orchestrator
const v4Payout = await flw.request("v4", "/transfers", {
  method: "POST",
  idempotencyKey: `IDEMP-${Date.now()}`,
  body: JSON.stringify({
    action: "instant",
    reference: `V4-PAYOUT-${Date.now()}`,
    narration: "Vendor payment",
    payment_instruction: {
      amount: 50000,
      currency: "NGN",
      recipient_id: "rcb_B9aAgsdzzl",
    },
  }),
});
```

---

## Webhook Ingestion & Security Standard

Flutterwave verifies webhooks using a **secret hash** configured in your Flutterwave Dashboard (**Settings > Webhooks**) and passed in the **`verif-hash`** HTTP header:

```ts
import crypto from "node:crypto";

export function handleFlutterwaveWebhook(req: Request) {
  const incomingHash = req.headers.get("verif-hash");
  const secretHash = process.env.FLW_WEBHOOK_HASH;

  if (!incomingHash || !secretHash) {
    return new Response("Unauthorized", { status: 401 });
  }

  // Timing-safe constant-time comparison to prevent side-channel leaks
  const a = Buffer.from(incomingHash, "utf8");
  const b = Buffer.from(secretHash, "utf8");
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
    return new Response("Forbidden", { status: 403 });
  }

  // Respond HTTP 200 immediately to meet Flutterwave's 60-second SLA
  // Process the event asynchronously in the background
  return new Response(JSON.stringify({ status: "success" }), { status: 200 });
}
```

---

## Test Vectors & Sandbox Testing

| Rail | Test Input | Expected Behavior |
| --- | --- | --- |
| 3DS Mastercard | Card: `5531881111111111`, CVV: `123`, Expiry: `09/32` | Requires OTP -> Enter `12345` -> Successful |
| Verve Card (PIN) | Card: `5060666666666666`, CVV: `111`, Expiry: `05/29` | Requires PIN `1234`, then OTP `12345` -> Successful |
| Decline Simulation | Card: `5531882222222222`, CVV: `123`, Expiry: `09/32` | Direct decline (`Insufficient funds`) |
| Kenya M-Pesa | Phone: `2540700000000` | Auto-approves simulated STK push in sandbox |
| Bank Resolution | Account: `0690000031`, Bank: `044` (Access Bank) | Resolves name: `FLW TEST ACCOUNT` |

---

## Best Practices for Developers and AI Agents

1. **Version Isolation:** Do not mix v3 request fields (e.g. `customer.email` embedded directly) with v4 structures (`payment_instruction`, `customer_id`).
2. **Never Trust Redirect URLs:** Never fulfill an order simply because a customer landed on `redirect_url?status=successful`. Always execute server-side verification.
3. **Deterministic References:** Provide a unique `tx_ref` or `reference` on every payment and payout to avoid collision and guarantee idempotency.
4. **Credential Security:** Store `FLW_SECRET_KEY`, `FLW_V4_CLIENT_ID`, `FLW_V4_CLIENT_SECRET`, and `FLW_WEBHOOK_HASH` in secure environment variables. Never commit credentials to git.
