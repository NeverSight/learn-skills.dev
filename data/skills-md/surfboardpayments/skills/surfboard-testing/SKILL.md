---
name: surfboard-testing
description: "Test and verify a Surfboard Payments integration in the Demo environment: test cards, the payment lifecycle and its terminal states, capture, cancel, void, refund and partial refund, error codes, and proving an integration actually works before reporting success. Use when verifying an integration, debugging a failed payment, or implementing post-payment operations."
---

# Testing and verification

Read `surfboard-payments` first. **This skill is what separates a working integration
from one that compiles.**

## The Demo environment

Demo credentials come from the Developer Portal on signup, with no approval step.
<https://developers.surfboardpayments.com/console/api-keys>

| | Demo |
|---|---|
| Cards | Test cards |
| A real card, used by accident | Voided automatically after 30 minutes. Never captured, never settled. |
| Online terminals | PaymentPage and MerchantInitiated, pre-provisioned on an online store |
| Physical and SoftPOS terminals | Can be registered and driven. They report real states and accept payment initiation. |

Demo covers more than payment page mode: a registered terminal reports `ACTIVE`,
accepts payment initiation, and returns real terminal states. This is worth knowing,
because Demo is where the whole class of order-shape errors below actually surfaces,
and stopping short of it is how they reach production.

What Demo will not do is complete a SoftPOS payment without the device-side app
switch. See `surfboard-in-store`.

Demo covers orders, payments, status, webhooks, refunds, captures, and voids. It does
not cover physical terminal hardware beyond payment page mode.

## What "verified" means

Not "the code compiles". Not "the request was accepted". An integration is verified
when you have:

1. Created an order and received an `orderId` and `paymentId`
2. Initiated a payment
3. Polled or received a webhook until the payment reached a **terminal state**
4. Shown the user the IDs and the final status

If you have not done all four, say what you did and what remains. Do not imply a
working integration you have not observed.

## Terminal states

`completed`, `failed`, `canceled` are final. Stop polling.
`initiated` and `processing` mean keep waiting.

Poll with backoff and a hard timeout. A payment that never reaches a terminal state is
an outcome to surface, not a condition to retry forever.

Check `status` in the envelope. **Errors arrive with a 2xx, and on order creation it
is usually 201.** A client that special-cases 200 and otherwise trusts the HTTP code
will read a 201 as success and then push that 201 into its own error path. Read the
envelope first; map any 2xx-carrying-an-error onto a server-side failure of your own.

## Post-payment operations

| Operation | When | Guide |
|---|---|---|
| **Capture** | Authorised, now take the money | `references/guides/capture-a-payment.md` |
| **Cancel** | Before completion | `references/guides/cancel-a-payment.md` |
| **Void** | Authorised, not yet settled | `references/guides/void-a-payment.md` |
| **Refund** | Settled, give it back | `references/guides/refund-an-order.md` |
| **Partial refund** | Give some of it back | `references/guides/partial-refund.md` |

Void and refund are not interchangeable: voiding an unsettled authorisation and
refunding a settled payment have different windows, different fees, and different
statement lines for the cardholder. Pick by settlement state, not by which endpoint
you already wrote.

Refunds use **negative quantities in order lines**.

## Errors

Order creation has its own families: `OR_*`, `PS_*`, `GC_*`, `SP_*`. Look the code up
in `references/guides/create-order-error-codes.md` rather than inferring from
`message`, because the wording is not a contract.

**`P_*` is the exception, and in practice it is what you will hit most.** Validation
failures come back as `P_0001: Input data validation failed.` followed by a free-text
reason, and the prefix is not in the reference. For `P_0001` the message *is* the only
discriminator, so read it. The common ones are in the table above.

| HTTP | Meaning |
|---|---|
| 400 | Malformed body or a missing required field |
| 401 | Credentials wrong, missing, or from the other environment |
| 403 | Authenticated but not permitted; check `MERCHANT-ID` against the path |
| 404 | An identifier in the path does not resolve |
| 500 | Retry with backoff; if it persists, contact support |

## Failures that look like something else

| Symptom | Actual cause |
|---|---|
| Amounts a hundredth of what they should be | Decimal amount instead of minor units |
| Order rejected on currency | `"SEK"` instead of `"752"` |
| ORM or template error on order creation | `terminal$id`, where the `$` needs quoting |
| Reports missing rows | Pagination loop terminated on a short page |
| Everything 401 after it worked yesterday | Base URL and credentials from different environments |
| 404 on order creation, merchant ID looks right | Path is merchant-scoped. Orders are not: `POST /orders`, merchant in the header |
| `P_0001 ... Invalid item price for item id` | `amount.total` is per unit, not per line |
| `P_0001 ... Invalid total order price` | Tax added on top. `totalOrderAmount.total` must equal `regular` |
| `P_0001 ... reading 'vatValue'` | A line is missing its required `amount.tax` array |
| Payment fails within seconds, no card prompt ever appeared | SoftPOS terminal driven from a server, with no device-side app switch |
| Duplicate fulfilment | Webhook handler not idempotent |
| Registration fails on a terminal that exists | `PaymentPage`/`MerchantInitiated` are pre-provisioned |

## Bundled guides

`references/guides/` holds: payment lifecycle, create order error codes, capture, cancel,
void, refund, partial refund.
