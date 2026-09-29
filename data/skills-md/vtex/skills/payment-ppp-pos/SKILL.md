---
name: payment-ppp-pos
description: "Apply when implementing a VTEX Payment Provider Protocol connector for Point of Sale (POS) payments on VTEX Sales App. Covers Venda Direta Credito and Venda Direta Debito manifest methods, the two-phase Payment App challenge (terminal connector then wait-for-confirmation), null card data on Create Payment, asynchronous undefined status, timeout pairing of secondsWaiting and delayToCancel, and callback payloads with cardBrand, firstDigits, and lastDigits. Use for building or debugging PPP + POS integrations that charge a physical card on a payment terminal."
---

# PPP Applied to POS (VTEX Sales App)

## When this skill applies

Use this skill when the task is to **create, extend, or debug a payment connector that charges a physical card on a POS terminal** from VTEX Sales App.

- The user mentions PPP + POS, POS connector, in-store payments, Sales App card payments, payment terminal, or `Venda Direta Credito` / `Venda Direta Debito`
- The source of truth is [Payment Provider Protocol for Point of Sale (POS)](https://developers.vtex.com/docs/guides/payments-integration-ppp-applied-to-pos)
- The goal is to remove the "implement from scratch" barrier: clone the official PPF example from [Payment Provider Framework](https://developers.vtex.com/docs/guides/payments-integration-payment-provider-framework) Getting started, or overlay POS on existing PPP — not generate a generic ecommerce connector

Load companions when the step needs them. Do not dump all three into the first reply.

| Companion | Load when |
|---|---|
| [generation.md](references/generation.md) | The user asked to **create** a POS connector. Ask the four questions, then implement in the listed order. |
| [ppf-scaffold.md](references/ppf-scaffold.md) | Hosting is **VTEX IO / PPF**. Copy overlay files onto the official PPF example app. |
| [examples.md](references/examples.md) | You need expected JSON, the state machine table, or IO retry vs standalone notification. |

The hard constraints below override ecommerce PPP and PCI habits. If a generated file violates one, STOP and fix it before writing more files.

Do not use this skill as the default choice for:

- Ecommerce PPP endpoints, manifests, and homologation shapes with no POS methods — use [`payment-provider-protocol`](../payment-provider-protocol/SKILL.md)
- IO connector wiring (`PaymentProvider`, `configuration.json`, `this.retry`) — use [`payment-provider-framework`](../payment-provider-framework/SKILL.md) together with this skill
- Pix, Boleto, or browser-redirect async methods — use [`payment-async-flow`](../payment-async-flow/SKILL.md)
- Ecommerce card data and Secure Proxy — use [`payment-pci-security`](../payment-pci-security/SKILL.md)
- Sales App cart, PDP, or menu UI extensions — use [`sales-app-extensibility`](../../../sales-app/skills/sales-app-extensibility/SKILL.md)

## Decision rules

- Prefer **VTEX IO / PPF** unless the partner already hosts PPP middleware. Clone the official example app from the Payment Provider Framework guide and overlay POS; do not start from an empty Express app.
- POS payments are still PPP. Implement the six payment-flow endpoints, then overlay the POS rules in this skill.
- `authorize()` is a state machine. It never waits on the POS. It only returns the current phase. The connector **answers** Create Payment; it does not push the Gateway between phases. After the terminal app closes, **VTEX Sales App** triggers a Gateway callback that issues Create Payment ([POS guide](https://developers.vtex.com/docs/guides/payments-integration-ppp-applied-to-pos) step 8). **Wait for confirmation** then polls the Gateway, which issues more Create Payment (step 9). Do not POST `callbackUrl` until the processor reports a final status — retry-on-pending is unnecessary and adds about 1 second per authorize.

| Stored phase | Who drives the next Create Payment | Create Payment returns |
|---|---|---|
| *(none yet)* | Sales App checkout → Gateway (step 3) | Persist `identify-terminal`; `undefined` + `vtex.terminal-connector-app` |
| `identify-terminal` (no serial) | Gateway / Sales App | Same terminal app until `submitUrl` stores a serial |
| `identify-terminal` (serial stored) | Sales App after the terminal app closes (step 8) | Start the processor charge **once**; `undefined` + `vtex.challenge-wait-for-confirmation` |
| `await-pos` | Wait for confirmation polling (step 9) | Same wait app; no second charge; no retry POST |
| `approved` / `denied` | Wait app / Sales App after IO retry | Final status + `cardBrand` + `firstDigits` + `lastDigits` |
- `Venda Direta Credito` and `Venda Direta Debito` are **asynchronous card-present** methods. Return `status: "undefined"` and resolve later via `callbackUrl`. Do not treat them as sync Visa/Mastercard authorizations.
- Branch on `paymentMethod`. On PPF, use `isDirectSaleAuthorization` from `@vtex/payment-provider` (canonical `DirectSale` names, and the narrowed type has no `card` / `secureProxyUrl`). On standalone HTTP, compare to those same ASCII strings. A connector may support ecommerce and POS.
- The Gateway does **not** receive the shopper's card for POS. All `card` fields arrive as `null`. Do not call Secure Proxy on this path.
- Use VTEX's ready-made Payment Apps unless the partner has a documented reason to build a custom one:
  - Identify the terminal: `vtex.terminal-connector-app`
  - Wait for the POS result: `vtex.challenge-wait-for-confirmation`
- Do not use `vtex.challenge-terminal-connector-app`. That name appears as a flow-diagram example in the POS guide; the implementation contract and the published app are `vtex.terminal-connector-app`.
- `paymentAppData.payload` is a **serialized JSON string**, not a nested object. On PPF, build pending responses with `Authorizations.pending` so that is a compile error. Do not close those objects with `as AuthorizationResponse` — that cast hides the mistake. `cardBrand`, `firstDigits`, and `lastDigits` are required by the POS guide but are not on the SDK response types (checked on `@vtex/payment-provider` 1.4.0 and 1.8.0); the **final** approved/denied response is the one place a cast is justified.
- Communication between the payment processor and the physical POS is outside VTEX. The connector only identifies the terminal, starts the processor transaction, and reports `approved` or `denied` to the Gateway.
- Without VTEX IO, `callbackUrl` is a notification endpoint: POST the final status (include POS card fields). With VTEX IO, `callbackUrl` is a retry endpoint: persist state, then POST it with an **empty body**. Inside a `PaymentProvider` method use `this.retry(request)`. From a `service.json` extra route use `new Payments(ctx.vtex).retry(callbackUrl)` — same client as `this.retry` (gateway-retry metric, IO tracing, configured timeout). Do not POST `status` / `cardBrand` on IO. Return the final status plus POS card fields on the next Create Payment / `authorize()`.
- POS serial collection and the processor webhook are **extra public routes**, not PPP inbound-request. The official example's `this.callback(req, resp)` is Test Suite only.
- `delayToCancel` must be greater than or equal to `secondsWaiting`.
- Every connector endpoint must respond in under 20 seconds in production (under 5 seconds during the Payment Provider Test Suite).
- This skill can generate connector code and a test checklist. It cannot replace a real POS, a Sales App device, a configured test account, or homologation.

## Hard constraints

Code samples use example identifiers (`PartnerPos`, `partnername`, `connector-partnerpos`, `provider.example.com`) and example numbers (`SECONDS_WAITING = 600`, `firstDigits` / `lastDigits` such as `411111` / `1111`). Replace them with the partner's connector name, public hosts, timeouts, and processor card fragments. `600` is not a VTEX-required default; the rule is `delayToCancel >= secondsWaiting`. Example BIN/last-four values are truncated fragments, not a PAN.

### Constraint: Manifest must declare the POS payment methods by exact API name

GET `/manifest` (and PPF `paymentProvider/configuration.json` `paymentMethods`) MUST include `Venda Direta Credito` and/or `Venda Direta Debito` with the exact ASCII names from the POS guide. Admin labels with accents (`Venda Direta Crédito`, `Venda Direta Débito`) are display names only.

**Why this matters**
The Gateway and Sales App payment conditions bind to these method names. If the manifest only lists `Visa` / `Mastercard`, merchants cannot configure POS. If the connector invents a name such as `"POS Credit"`, Admin and Sales App will not attach the in-store flow.

**Detection**
If the task is POS and `paymentMethods` lacks `Venda Direta Credito` or `Venda Direta Debito`, STOP and add them before generating other code.

**Correct**

```json
{
  "paymentMethods": [
    { "name": "Venda Direta Debito", "allowsSplit": "onCapture" },
    { "name": "Venda Direta Credito", "allowsSplit": "onCapture" }
  ]
}
```

**Wrong**

```json
{
  "paymentMethods": [
    { "name": "Visa", "allowsSplit": "onCapture" },
    { "name": "Mastercard", "allowsSplit": "onCapture" },
    { "name": "POS Credit", "allowsSplit": "onCapture" }
  ]
}
```

### Constraint: Detect POS from `paymentMethod` and never read card PAN from the Gateway

For `Venda Direta Credito` and `Venda Direta Debito`, Create Payment sends `card.holder`, `card.number`, `card.csc`, `card.expiration`, `card.document`, and `card.token` as `null`. The connector MUST NOT require those fields, MUST NOT call Secure Proxy, and MUST NOT decline the payment because card data is missing.

On PPF, branch with `isDirectSaleAuthorization` from `@vtex/payment-provider`. That guard uses the SDK `DirectSale` names (exact ASCII), and `DirectSaleAuthorization` has no `card` and no `secureProxyUrl` — so `authorization.card` is a compile error after the narrow. Do not hand-roll `POS_METHODS` or `(authorization as any).paymentMethod`. On standalone HTTP, compare `paymentMethod` to those same two strings. `callbackUrl` and `value` are already on `Authorization`; do not cast them.

**Why this matters**
The shopper pays on the physical terminal. Treating POS as an ecommerce card authorization fails the charge, or worse, invents Secure Proxy calls with empty tokens. A hand-rolled accented string fails at the Gateway instead of at compile time.

**Detection**
If POS authorize logic reads `card.number` / `secureProxyUrl` or returns `denied` when `card` is null, STOP and split POS from ecommerce. If PPF code uses `as any` to read `paymentMethod`, `callbackUrl`, or `value`, STOP and use the typed fields / guard.

**Correct**

```typescript
import {
  isDirectSaleAuthorization,
  AuthorizationRequest,
} from "@vtex/payment-provider";

async function authorize(request: AuthorizationRequest) {
  if (isDirectSaleAuthorization(request)) {
    return authorizePos(request);
  }

  return authorizeEcommerce(request);
}
```

**Wrong**

```typescript
async function authorize(request: CreatePaymentRequest) {
  if (!request.card?.number) {
    return { status: "denied", message: "Missing card number" };
  }

  return secureProxy.charge(request.card, request.secureProxyUrl);
}
```

### Constraint: First Create Payment response must open the terminal Payment App

When the connector has **not** yet received the POS serial number for this `paymentId`, Create Payment MUST return `status: "undefined"` and `paymentAppData` for `vtex.terminal-connector-app`. `payload` MUST be a JSON string with `submitUrl`, the HTTPS endpoint that receives `{"serialNumber": "12345"}`.

Replace the host in examples with the partner's real public URL. Persist `callbackUrl` and `paymentId` before responding.

On PPF, return `Authorizations.pending(authorization, { delayToCancel, paymentAppData })`. `AppData.payload` is `Maybe<string>`, so an object payload is a compile error. Do not wrap that object in `as AuthorizationResponse`.

**Why this matters**
Without this response, Sales App never opens the camera/barcode challenge, so the processor never learns which terminal to use. A nested `payload` object is not injected into the Payment App. A whole-response cast turns that compile error off.

**Detection**
If the first POS response is `approved`/`denied`, omits `paymentAppData`, uses `vtex.challenge-terminal-connector-app`, sets `payload` as an object, or uses `as AuthorizationResponse` on a pending body, STOP and fix.

**Correct**

```typescript
import { Authorizations } from "@vtex/payment-provider";

const SECONDS_WAITING = 600;

async function authorizePos(request: CreatePaymentRequest) {
  const existing = await store.get(request.paymentId);

  if (!existing) {
    await store.save(request.paymentId, {
      phase: "identify-terminal",
      status: "undefined",
      callbackUrl: request.callbackUrl,
      paymentMethod: request.paymentMethod,
      value: request.value,
    });

    return Authorizations.pending(request, {
      acquirer: "PartnerPos",
      code: "POS_IDENTIFY_TERMINAL",
      message: "Identify the POS terminal",
      delayToAutoSettle: 21600,
      delayToAutoSettleAfterAntifraud: 1800,
      delayToCancel: SECONDS_WAITING,
      paymentAppData: {
        appName: "vtex.terminal-connector-app",
        payload: JSON.stringify({
          submitUrl: `https://provider.example.com/pos/serial/${request.paymentId}`,
        }),
      },
    });
  }

  return continuePos(request, existing);
}
```

**Wrong**

```typescript
return {
  paymentId: request.paymentId,
  status: "approved",
  paymentAppData: {
    appName: "vtex.challenge-terminal-connector-app",
    payload: {
      submitUrl: "https://provider.example.com/pos/serial",
    },
  },
};
```

### Constraint: After the serial number, wait with `vtex.challenge-wait-for-confirmation`

When `submitUrl` receives `{"serialNumber": "..."}`, the connector MUST associate that serial with `paymentId` (POS guide step 7). Do **not** start the POS charge in that handler.

The **next** Create Payment — driven by Sales App after the terminal app closes (step 8) — MUST start the processor charge **once**, then return `status: "undefined"` plus `vtex.challenge-wait-for-confirmation` with payload `{"secondsWaiting": <int>}` (steps 8.b–8.d). Later polls (step 9) MUST NOT start another charge and MUST NOT POST `callbackUrl`.

Do not start the POS charge before the serial number exists, and do not start it from the first `authorize()` (no serial yet).

`secondsWaiting` is how long the Wait for confirmation app polls. `delayToCancel` (seconds, Create Payment response) is how long the Gateway keeps the payment `undefined` before calling Cancel. Set `delayToCancel >= secondsWaiting`.

**Why this matters**
Starting the terminal before it is identified charges the wrong device or none. Starting the charge in `submitUrl` diverges from the published sequence (8.b starts the payment, 8.c confirms it started, 8.d returns the wait app). If `delayToCancel` is shorter than `secondsWaiting`, the Gateway cancels while Sales App is still waiting. If Create Payment starts a new processor charge on every poll, the shopper is charged twice.

**Detection**
If Wait for confirmation is returned before a serial is stored, if `startPosCharge` runs in the serial handler or on every poll, if `secondsWaiting` is missing, or if `delayToCancel < secondsWaiting`, STOP.

**Correct**

```typescript
async function onSerialNumber(paymentId: string, serialNumber: string) {
  const payment = await store.get(paymentId);
  if (!payment || payment.phase !== "identify-terminal") {
    return;
  }

  await store.save(paymentId, {
    ...payment,
    serialNumber,
  });
}

function waitingResponse(request: CreatePaymentRequest) {
  return Authorizations.pending(request, {
    acquirer: "PartnerPos",
    code: "POS_WAITING",
    message: "Waiting for POS confirmation",
    delayToAutoSettle: 21600,
    delayToAutoSettleAfterAntifraud: 1800,
    delayToCancel: SECONDS_WAITING,
    paymentAppData: {
      appName: "vtex.challenge-wait-for-confirmation",
      payload: JSON.stringify({ secondsWaiting: SECONDS_WAITING }),
    },
  });
}
```

**Wrong**

```typescript
async function authorizePos(request: CreatePaymentRequest) {
  await processor.startPosCharge({ paymentId: request.paymentId });

  return {
    paymentId: request.paymentId,
    status: "undefined",
    delayToCancel: 30,
    paymentAppData: {
      appName: "vtex.challenge-wait-for-confirmation",
      payload: JSON.stringify({ secondsWaiting: 600 }),
    },
  };
}
```

### Constraint: Approve or deny only through the mandatory callback, including POS card fields

The processor, not VTEX, reads the physical card. When it reports a final result, the connector MUST notify the Gateway. POS cannot be approved or denied without this callback. Include:

- `status`: `"approved"` or `"denied"`
- `cardBrand`
- `firstDigits` (first six digits / BIN)
- `lastDigits` (last four digits)

Those three card fields are required for merchant reconciliation. They come from the processor after the terminal reads the card — not from the original Create Payment `card` object.

Do not log or store the full PAN. `firstDigits` + `lastDigits` are the allowed fragments.

**Why this matters**
Without notifying the Gateway, Sales App stays on Wait for confirmation until timeout, then cancels. Missing BIN/last-four breaks financial reports even when the charge succeeded on the terminal. On IO, posting a standalone notification body to `callbackUrl` does not complete the flow — the Gateway expects a **bodiless** retry POST, then a new `authorize()`.

**Detection**
If POS code returns `approved` on the first Create Payment, STOP. If PPF code `fetch`es `callbackUrl` with `status` / `cardBrand` in the body, STOP and use `Payments.retry` / `this.retry`. If a Service route calls `this.retry` (there is no `this`), STOP and use `new Payments(ctx.vtex).retry(stored.callbackUrl)`. If pending `authorize()` POSTs `callbackUrl` to "nudge" the Gateway, STOP. If standalone code omits the three card fields on the notification POST, STOP.

**Correct (PPF extra route — typical processor webhook)**

```typescript
import { Payments } from "@vtex/payment-provider";

await vbase.saveJSON("pos", paymentId, {
  status: "approved",
  cardBrand: event.cardBrand,
  firstDigits: event.firstDigits,
  lastDigits: event.lastDigits,
  authorizationId: event.authorizationId,
  nsu: event.nsu,
  tid: event.tid,
});

await new Payments(ctx.vtex).retry(callbackUrl);
```

**Correct (inside a `PaymentProvider` method only)**

```typescript
return this.retry(authorization);
```

The next `authorize()` MUST return `status`, `cardBrand`, `firstDigits`, and `lastDigits` from the persisted record. See [examples.md](references/examples.md) for the standalone notification payload.

**Wrong**

```typescript
async function authorizePos(request: CreatePaymentRequest) {
  return {
    paymentId: request.paymentId,
    status: "approved",
    message: "Assume the terminal will succeed",
  };
}

// Also wrong on VTEX IO: notification payload to callbackUrl
await fetch(authorization.callbackUrl, {
  method: "POST",
  body: JSON.stringify({
    paymentId: request.paymentId,
    status: "approved",
    cardBrand: "Visa",
    firstDigits: "411111",
    lastDigits: "1111",
  }),
});
```

### Constraint: Keep Create Payment idempotent and answers under 20 seconds

Create Payment for a given `paymentId` MUST return the **current** stored phase and status. It MUST NOT create a second processor transaction. Polling from Wait for confirmation will call Create Payment many times while status is still `undefined`. Those calls **can overlap** (different `requestId`, same `paymentId`) — a sequential get-then-save can create two records or drop a phase update.

On PPF, persist with `getRawJSON` (capture `etag`) then `saveJSON(..., ifMatch)`. On 412, re-read and continue from the stored document. Pair with [`payment-idempotency`](../payment-idempotency/SKILL.md). Do not put unique per-request fields (random `tid`, `requestId`) on the first identify-terminal write.

VBase composes the metadata bucket as `{vendor}.{appName}.{bucket}` and rejects names longer than 50 characters (`400 Metadata bucket name too large`). Use a short bucket such as `pos`. The skill placeholders (`partnername.connector-partnerpos`) fit `pos-payments`; a longer real `vendor.appName` does not.

Do not wait for the shopper to finish on the POS inside the HTTP handler. Compare-and-set `identify-terminal` → `await-pos`, start the processor charge only as the winner of that write, and return. Password retries and insufficient-funds handling stay between the processor and the POS.

**Why this matters**
The Gateway treats a >20s response as failure. Duplicate POS charges happen when each poll hits the acquirer again. Overlapping first writes for one `paymentId` return inconsistent `tid`s and break PPP idempotency. A long VBase bucket fails on the first Create Payment with an opaque 400.

**Detection**
If the handler `await`s the terminal result, calls `processor.startPosCharge` when `phase` is already `await-pos` or final, uses `getJSON` + `saveJSON` with no `etag`, or uses a VBase bucket that makes `{vendor}.{appName}.{bucket}` longer than 50 characters, STOP.

**Correct**

```typescript
const POS_BUCKET = "pos";

async function savePos(vbase: VBase, paymentId: string, record: PosRecord, etag?: string) {
  try {
    await vbase.saveJSON(POS_BUCKET, paymentId, record, undefined, etag);
    return true;
  } catch (err) {
    const status = (err as any).response && (err as any).response.status;
    if (status === 412) {
      return false;
    }
    throw err;
  }
}

async function continuePos(
  vbase: VBase,
  request: CreatePaymentRequest,
  existing: PosRecord,
  etag?: string
) {
  if (existing.status === "denied") {
    return {
      ...Authorizations.deny(request, {
        acquirer: "PartnerPos",
        code: existing.code,
        message: existing.message,
        tid: existing.tid,
        delayToCancel: SECONDS_WAITING,
      }),
      cardBrand: existing.cardBrand,
      firstDigits: existing.firstDigits,
      lastDigits: existing.lastDigits,
    } as AuthorizationResponse;
  }

  if (existing.status === "approved") {
    return {
      ...Authorizations.approve(request, {
        authorizationId: existing.authorizationId as string,
        nsu: existing.nsu,
        tid: existing.tid as string,
        acquirer: "PartnerPos",
        code: existing.code,
        message: existing.message,
      }),
      delayToCancel: SECONDS_WAITING,
      cardBrand: existing.cardBrand,
      firstDigits: existing.firstDigits,
      lastDigits: existing.lastDigits,
    } as AuthorizationResponse;
  }

  if (existing.phase === "await-pos") {
    return waitingResponse(request);
  }

  if (existing.serialNumber && existing.phase === "identify-terminal") {
    const won = await savePos(
      vbase,
      request.paymentId,
      { ...existing, phase: "await-pos" },
      etag
    );
    if (won) {
      await processor.startPosCharge({
        paymentId: request.paymentId,
        serialNumber: existing.serialNumber,
        amount: existing.value,
      });
    }
    return waitingResponse(request);
  }

  return Authorizations.pending(request, {
    acquirer: "PartnerPos",
    code: "POS_IDENTIFY_TERMINAL",
    message: "Identify the POS terminal",
    delayToCancel: SECONDS_WAITING,
    paymentAppData: {
      appName: "vtex.terminal-connector-app",
      payload: JSON.stringify({
        submitUrl: `https://provider.example.com/pos/serial/${request.paymentId}`,
      }),
    },
  });
}
```

**Wrong**

```typescript
async function authorizePos(request: CreatePaymentRequest) {
  const result = await processor.startPosCharge(request);
  await processor.waitUntilCardFinished(result, { timeoutMs: 120000 });
  return { paymentId: request.paymentId, status: result.status };
}
```

### Constraint: Collect the POS serial on a public custom route, not inbound-request

`vtex.terminal-connector-app` POSTs `{"serialNumber":"..."}` to `submitUrl`. That URL MUST be a public HTTPS endpoint the Payment App can call. On PPF, declare it in `service.json` `routes` and pass it into `PaymentProviderService`. Do **not** use `POST /payments/{paymentId}/inbound-request/{action}` for this step.

**Why this matters**
Inbound-request is Gateway-initiated. The terminal app posts from the Sales App device. If `submitUrl` is an inbound path, the serial never arrives and the POS charge never starts.

**Detection**
If `submitUrl` contains `/inbound`, STOP. If PPF has no extra `service.json` route for serial collection, STOP.

**Correct**

```json
{
  "routes": {
    "posSerial": {
      "path": "/_v/partnerpos/pos/serial/:paymentId",
      "public": true
    }
  }
}
```

**Wrong**

```json
{
  "submitUrl": "https://account.myvtex.com/_v/api/my-connector/payments/PAY1/inbound/serial"
}
```

## Preferred pattern

Follow [generation.md](references/generation.md) in order. For PPF, overlay POS on the official example app from the [Payment Provider Framework](https://developers.vtex.com/docs/guides/payments-integration-payment-provider-framework) guide using [ppf-scaffold.md](references/ppf-scaffold.md). Compare IO vs standalone payloads in [examples.md](references/examples.md).

```text
Sales App checkout
  → Gateway POST /payments (Venda Direta Credito|Debito, card = null)
  → authorize(): undefined + vtex.terminal-connector-app (submitUrl)
  → POST submitUrl {"serialNumber":"..."}   (public custom route; store serial only)
  → Sales App closes the terminal app and calls the Gateway (connector does not retry)
  → authorize(): start processor charge once, then undefined + vtex.challenge-wait-for-confirmation
  → Wait for confirmation polls authorize() (still undefined; no second charge; no retry POST)
  → Processor webhook
       PPF: persist + Payments.retry(callbackUrl) / this.retry inside PaymentProvider
       Standalone: POST notification payload (status + card fragments)
  → authorize() returns approved|denied + cardBrand/firstDigits/lastDigits
  → Sales App places the order
```

## Common failure modes

- Generating an ecommerce PPP connector (Visa/Mastercard + Secure Proxy) when the user asked for PPP + POS.
- Omitting `Venda Direta Credito` / `Venda Direta Debito` from the manifest, or using accented Admin labels as API names.
- Returning `approved` before the terminal finishes, or waiting inside Create Payment for the card to be inserted.
- Using `vtex.challenge-terminal-connector-app` instead of `vtex.terminal-connector-app`.
- Sending `paymentAppData.payload` as an object instead of `JSON.stringify(...)`, or hiding that with `as AuthorizationResponse` on a pending body.
- Setting `delayToCancel` below `secondsWaiting`, so the Gateway cancels a payment the Wait app is still polling.
- Starting the POS charge in the `submitUrl` handler (POS guide step 8.b starts it on the following Create Payment).
- Starting a new POS charge on every Create Payment poll (broken idempotency).
- POSTing `callbackUrl` on pending responses to "nudge" the Gateway. Sales App and Wait for confirmation already drive Create Payment.
- Using `getJSON` + `saveJSON` with no `etag` while Create Payment calls overlap for one `paymentId`.
- Using a VBase bucket that makes `{vendor}.{appName}.{bucket}` longer than 50 characters (default to `pos`).
- Skipping the Gateway callback, or omitting `cardBrand`, `firstDigits`, and `lastDigits`.
- **On VTEX IO:** POSTing a standalone notification payload (`status` + card fields) to `callbackUrl` instead of a bodiless `Payments.retry` / `this.retry`.
- Copying the example's Test Suite `this.callback(req, resp)` as the POS processor webhook.
- Calling `this.retry` from a `service.json` extra route (no `PaymentProvider` `this`). Use `new Payments(ctx.vtex).retry(callbackUrl)` there.
- Putting `submitUrl` on PPP inbound-request instead of a public custom route.
- Applying [`payment-pci-security`](../payment-pci-security/SKILL.md) Secure Proxy to POS authorize because "it is a card payment".
- Building a Sales App cart/PDP extension instead of a payment connector.
- Starting from an empty Express app when the partner can use PPF / the official example app.

## Review checklist

- [ ] For PPF, was the app overlaid on the official PPF example (or an existing PPF connector), not an empty HTTP server?
- [ ] Does `/manifest` (and IO `configuration.json`) declare `Venda Direta Credito` and/or `Venda Direta Debito` with those exact names?
- [ ] Does authorize branch with `isDirectSaleAuthorization` (PPF) or the exact ASCII method names (standalone), and skip Gateway card PAN / Secure Proxy for POS?
- [ ] Is the first POS response `Authorizations.pending` + `vtex.terminal-connector-app` with string `payload.submitUrl` (no whole-response cast)?
- [ ] Is `submitUrl` a public custom route (`service.json`) that accepts `{"serialNumber": "..."}` and is not inbound-request?
- [ ] Does `submitUrl` only persist the serial (step 7), and does the **next** Create Payment start the processor charge once (step 8.b)?
- [ ] Is the waiting response `undefined` + `vtex.challenge-wait-for-confirmation` with `secondsWaiting`?
- [ ] Is `delayToCancel >= secondsWaiting`, and does every endpoint respond in under 20 seconds?
- [ ] Are overlapping Create Payment calls for the same `paymentId` safe (`getRawJSON` + `ifMatch`, no second POS charge, no retry-on-pending)?
- [ ] Is the PPF VBase bucket short enough that `{vendor}.{appName}.{bucket}` is ≤ 50 characters (use `pos`)?
- [ ] **PPF:** processor webhook persists card fragments then `Payments.retry(callbackUrl)` (or `this.retry` inside `PaymentProvider`)? Next `authorize()` returns the card fragments (cast only that final response)?
- [ ] **Standalone:** notification POST includes `status`, `cardBrand`, `firstDigits`, `lastDigits`?
- [ ] Is Cancel implemented so Gateway timeout can abort an `undefined` POS payment?
- [ ] Has the partner been told they still need a Sales App device, POS terminal, test account, payment conditions, and homologation?

### Testing prerequisites (cannot be automated by the skill)

VTEX often provides a preconfigured store for connector testing. To configure a store manually:

1. Install the connector (PPF: follow the Payment Provider Framework install steps).
2. Register a Gateway affiliation for the connector.
3. Create payment conditions **Venda Direta Crédito** and/or **Venda Direta Débito** on that affiliation.
4. Show those methods on Sales App (`checkout-instore-custom.js`). Standard condition IDs are `44` (debit) and `45` (credit); confirm on the Admin Payment Conditions page.
5. Install VTEX Sales App on a device and complete a purchase on a real or certified test POS.
6. Run the Payment Provider Test Suite, including async approved/denied cases, then open a homologation ticket when required.

## Related skills

Companions for this skill:

- [generation.md](references/generation.md) — Questions to ask, clone-the-example workflow, implementation order
- [ppf-scaffold.md](references/ppf-scaffold.md) — Overlay files for the official PPF example app
- [examples.md](references/examples.md) — Partner prompts and IO vs standalone payloads

Other payment / Sales App skills:

- [`payment-provider-protocol`](../payment-provider-protocol/SKILL.md) — Mandatory PPP endpoints and response shapes; use together with this skill
- [`payment-provider-framework`](../payment-provider-framework/SKILL.md) — Use when the POS connector is a VTEX IO app
- [`payment-async-flow`](../payment-async-flow/SKILL.md) — Generic `undefined` + `callbackUrl` rules; POS adds Payment Apps and card-fragment callbacks on top
- [`payment-idempotency`](../payment-idempotency/SKILL.md) — `paymentId` must not create a second POS charge; Create Payment for one id can overlap (etag / `ifMatch`)
- [`payment-pci-security`](../payment-pci-security/SKILL.md) — Ecommerce card-not-present only; do not apply Secure Proxy to POS authorize
- [`sales-app-extensibility`](../../../sales-app/skills/sales-app-extensibility/SKILL.md) — Sales App UI extensions; not the POS payment connector

## Reference

- [Payment Provider Protocol for Point of Sale (POS) - VTEX Sales App](https://developers.vtex.com/docs/guides/payments-integration-ppp-applied-to-pos) — Manifest methods, two-phase Payment Apps, timeouts, callback card fields, testing
- [Payment App](https://developers.vtex.com/docs/guides/payments-integration-payment-app) — `paymentAppData.appName` and `payload` contract
- [Payment Provider Framework](https://developers.vtex.com/docs/guides/payments-integration-payment-provider-framework) — Clone the official example app (Getting started), IO connector implementation, `this.retry`, extra routes
- [Payment Provider Protocol (Help Center)](https://help.vtex.com/en/docs/tutorials/payment-provider-protocol) — Callback URL, notification payload including `cardBrand` / `firstDigits` / `lastDigits`
- [Define payment methods displayed on VTEX Sales App](https://developers.vtex.com/docs/guides/define-payment-methods-displayed-on-vtex-sales-app) — Sales App payment condition filters (`44` debit, `45` credit)
- [Payment provider homologation](https://developers.vtex.com/docs/guides/payments-integration-payment-provider-homologation) — Test Suite and publishing
- [Registering gateway affiliations](https://help.vtex.com/en/tutorial/registering-gateway-affiliations--tutorials_444) — Affiliation setup for tests
- [Configuring payment conditions](https://help.vtex.com/en/tutorial/how-to-configure-payment-conditions--tutorials_455) — Admin conditions for Venda Direta
