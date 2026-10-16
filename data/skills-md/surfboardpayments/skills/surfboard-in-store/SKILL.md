---
name: surfboard-in-store
description: "Build in-store card payments with Surfboard Payments: create an order against a terminal, initiate a CARD/SWISH/KLARNA payment, poll for status, and issue a receipt. Covers SurfTouch, SurfPad, SurfPrint, SurfMini, CheckoutX SoftPOS, inter-app integration, tips, and partial payments. Use for POS, till, kiosk, or any integration driving a physical payment terminal."
---

# In-store payments

Read `surfboard-payments` first. Terminal registration itself is `surfboard-terminals`.

## Check the terminal type before you write anything

```
GET {SURFBOARD_API_URL}/terminals/:terminalId
```

Read `terminalType`. This decides whether the flow below is achievable at all, and it
is not a detail you can defer.

| `terminalType` | Server-initiated payment | What to do |
|---|---|---|
| Networked EMV terminal | Yes | Follow this skill. |
| `checkoutX` (SoftPOS) | **No** | See below before writing code. |

**SoftPOS payments cannot be completed from a server.** A `checkoutX` terminal reports
`ACTIVE`, accepts the create-order call, and returns a real `orderId`, `paymentId`, and
`interAppJWT`. That is step 1 of 2. Step 2 is a native app switch on the same physical
device, launching `checkoutx://com.surfboard.checkoutx/...` with the `interAppJWT` from
a point-of-sale app installed alongside it. There is no server-side substitute.

If the POS is a web application, or runs on a different machine from the terminal, a
SoftPOS terminal **cannot take a payment through it**. What you will observe instead is
a `PAYMENT_FAILED` a few seconds after initiation, with no card ever prompted for and
the generic message "An error occurred during transaction processing." Nothing in that
points at the architecture, so say it plainly to the user now rather than letting them
debug the card, the amount, or the credentials.

Either target a networked terminal, or build the POS as a native app on the device and
follow `references/guides/interapp-integration.md`.

## The flow

```
create order  →  initiate payment  →  poll status  →  receipt
```

Order creation can initiate the payment in the same call, and usually should, for one
round trip instead of two.

## 1. Create an order and initiate payment

```
POST {SURFBOARD_API_URL}/orders
```

```json
{
  "terminal$id": "YOUR_TERMINAL_ID",
  "orderLines": [
    {
      "id": "ITEM-001",
      "name": "Flat white",
      "quantity": 1,
      "amount": {
        "regular": 4500,
        "total": 4500,
        "currency": "752",
        "tax": [{ "amount": 900, "percentage": 25, "type": "VAT" }]
      }
    }
  ],
  "totalOrderAmount": {
    "regular": 4500,
    "total": 4500,
    "currency": "752",
    "tax": [{ "amount": 900, "percentage": 25, "type": "VAT" }]
  },
  "controlFunctions": {
    "initiatePaymentsOptions": { "paymentMethod": "CARD" }
  }
}
```

Response:

```json
{
  "status": "SUCCESS",
  "data": { "orderId": "83a1ba32774149710b", "paymentId": "83a1ba3264bd500106" },
  "message": "Order created successfully"
}
```

**Store both IDs.** `orderId` for refunds and reporting, `paymentId` for status,
captures, and voids.

### Three things about `amount` that examples hide

Every example in the documentation uses `quantity: 1`, so none of these surface until
you build a real cart.

**`total` is the price of one unit, not the line.** It must equal
`regular + shipping - campaign` for a single unit; the order total is
`sum(total * quantity)`. Sending `4500 * 2 = 9000` on a line of quantity 2 is
rejected with `P_0001 ... Invalid item price for item id`.

**`amount.tax` is required on every line**, including zero-VAT lines, where you still
send a `0` percentage entry. Omitting it returns
`P_0001 ... Cannot read properties of undefined (reading 'vatValue')`, which is an
internal null dereference leaking out as a validation message. If you see `vatValue`,
a line is missing its tax array.

**Prices include tax.** `total` equals `regular`; the tax array reports the VAT
contained in that price. Never add tax on top. See `surfboard-payments`.

Also: amounts are integers in minor units (`4500` is 45.00), currency is the numeric
ISO 4217 code as a string (`"752"`, not `"SEK"`), and `terminal$id` needs quoting in
most ORMs and template languages.

Payment methods: `CARD`, `SWISH`, `KLARNA`.

## 2. Wait for the customer

The terminal now prompts for a card. This takes as long as the customer takes, so
never block a request thread on it. Poll the payment, or subscribe to webhooks
(`surfboard-webhooks`). Webhooks are better in production; polling is fine while
building.

Poll with backoff and a hard timeout. A payment that never reaches a terminal state
is a real outcome, not a bug to retry forever.

## 3. Terminal states

`completed`, `failed`, and `canceled` are final. Stop polling. `initiated` and
`processing` mean keep waiting.

Check `status` in the envelope, not the HTTP code.

## 4. Receipt

Digital receipts go out through the Receipts API. `references/guides/receipts.md`
covers the shape, including emailing and the hosted receipt URL.

## Reference implementation

```ts
// server-side only. These credentials never reach a browser.
const h = {
  'Content-Type': 'application/json',
  'API-KEY': process.env.SURFBOARD_API_KEY!,
  'API-SECRET': process.env.SURFBOARD_API_SECRET!,
  'MERCHANT-ID': process.env.SURFBOARD_MERCHANT_ID!,
}
// Orders are not merchant-scoped. The merchant travels in the MERCHANT-ID header.
const base = process.env.SURFBOARD_API_URL

export async function charge(minorUnits: number, terminalId: string) {
  const amount = { regular: minorUnits, total: minorUnits, currency: '752' }

  const res = await fetch(`${base}/orders`, {
    method: 'POST',
    headers: h,
    body: JSON.stringify({
      'terminal$id': terminalId,
      orderLines: [{ id: 'ITEM-001', name: 'Sale', quantity: 1, amount }],
      totalOrderAmount: amount,
      controlFunctions: { initiatePaymentsOptions: { paymentMethod: 'CARD' } },
    }),
  })

  const body = await res.json()
  // Errors come back 2xx, usually 201. Never trust the HTTP code here.
  if (body.status !== 'SUCCESS') throw new Error(body.message)
  return body.data // { orderId, paymentId }
}
```

```python
import os, requests

H = {
    "Content-Type": "application/json",
    "API-KEY": os.environ["SURFBOARD_API_KEY"],
    "API-SECRET": os.environ["SURFBOARD_API_SECRET"],
    "MERCHANT-ID": os.environ["SURFBOARD_MERCHANT_ID"],
}
# Orders are not merchant-scoped. The merchant travels in the MERCHANT-ID header.
BASE = os.environ["SURFBOARD_API_URL"]

def charge(minor_units: int, terminal_id: str):
    amount = {"regular": minor_units, "total": minor_units, "currency": "752"}
    r = requests.post(
        f"{BASE}/orders",
        headers=H,
        json={
            "terminal$id": terminal_id,
            "orderLines": [{"id": "ITEM-001", "name": "Sale", "quantity": 1, "amount": amount}],
            "totalOrderAmount": amount,
            "controlFunctions": {"initiatePaymentsOptions": {"paymentMethod": "CARD"}},
        },
    )
    body = r.json()
    if body["status"] != "SUCCESS":
        raise RuntimeError(body["message"])
    return body["data"]
```

## Variations

| Need | Where |
|---|---|
| Tips on the terminal | `references/guides/tips-configuration.md` |
| Split or partial payment | `references/guides/partial-payments.md` |
| Launch from another Android app | `references/guides/interapp-integration.md` |
| SoftPOS on Surfboard hardware | `references/guides/checkoutx-softpos.md` |
| Identify the customer at card tap | `references/guides/customer-identification.md` |
| Read an NFC tag | `references/guides/nfc-tag-reading.md` |
| Branded screens on the terminal | `references/guides/pos-templates.md` |
| A full EMV terminal integration | `references/guides/emv-terminal-integration.md` |

## When it fails

Order creation has its own error families: `OR_*`, `PS_*`, `GC_*`, `SP_*`. The full
table is in `references/guides/create-order-error-codes.md`. Look the code up rather
than guessing from the message.

## Verify before reporting success

Create a real order in Demo, initiate the payment, and poll until it reaches a terminal
state. Show the user the `orderId` and the final status. Do not report a working
integration on the strength of compiling code.
