---
name: tiendanube-shipping-payment-apps
description: "Apply when building a shipping app or a payment app for Tiendanube / Nuvemshop: shipping carriers and carrier options, the rate callback (rates, code, reference, price and price_merchant, delivery dates, pickup points), caching and circuit breaker; payment providers, checkout payment options, the checkout JS file (LoadCheckoutPaymentContext, processPayment), the Process, Cancel and Payment Status APIs, signed requests, transactions and transaction events, refunds; and Business Rules callbacks that filter shipping or payment options, block checkout or prioritize locations. Use when writing or reviewing the backend or checkout script of such an app."
license: MIT
compatibility: "Tiendanube / Nuvemshop Admin API, version 2025-03. Apps and integrations built by partners."
metadata:
  author: commente.me
  version: "0.1.0"
---

# Shipping and payment apps

## When this skill applies

Use this skill when the app itself plugs into the checkout as a shipping carrier, a payment provider or a business rules provider.

- Registering a carrier and its options at install time, and answering the rate callback
- Registering a payment provider with its checkout payment options and hosting the checkout JS file
- Implementing the Process Payment, Cancel Payment and Payment Status endpoints that the platform calls
- Reporting payments and refunds with transactions and transaction events
- Answering Business Rules callbacks (`shipping/before-filter`, `payments/before-filter`, `cart/before-finish`, `location/prioritization`)

Do not use this skill for:

- Querying a store's configured payment and shipping methods by conversation: that is the official Admin MCP
- Updating fulfillment orders, tracking events and labels after the sale (use `tiendanube-orders-fulfillment`)
- Storefront or checkout UI that is not a payment option (use `tiendanube-nube-sdk`)
- The OAuth install flow itself (use `tiendanube-oauth-apps`)

## Decision rules

- Both APIs are gated. Shipping endpoints require a request form for the partner account (the guide says this applies to Brazil-based accounts); Payments APIs and Business Rules must be enabled by partner support.
- Shipping app scopes: `write_shipping`, `write_orders`, `read_customers`. Payment app scopes: `read_payments`, `write_payments`, `read_orders`, `write_orders` (plus `write_scripts` for storefront scripts such as fraud fingerprinting).
- Create exactly one shipping carrier per store (`POST /shipping_carriers` with `name`, HTTPS `callback_url`, `types` of `ship`, `pickup` or both), then one option per service (`POST /shipping_carriers/{id}/options`) with a unique string `code` and `allow_free_shipping: false`.
- In the rate response, return every rate inside a `rates` array; each needs `name`, `code`, `price`, `currency` and `type`, and pickup rates also `address` and `hours`. A `code` that matches no carrier option is not displayed; matching is exact (case and accents).
- Return all your rates without filtering or adding merchant settings. The platform drops inactive options and applies `additional_days` and `additional_cost` itself.
- `ship` rates: one per `code` (repeats keep only the first). `pickup` rates: up to 10 per `code`.
- Free shipping: if every item has `free_shipping: true`, send the full cost in both `price` and `price_merchant`. In a mixed cart, `price_merchant` is the full cost and `price` is the cost after discounting the free-shipping items.
- Product page and cart quotes send only the postal code; checkout sends the full address. Do not reject a quote because the street is missing.
- With multiple locations, expect one quote per origin location for the same cart (`origin.location_id`).
- One store can have several payment providers, each with its own id. Create the provider during installation (`POST /payment_providers`); `PUT` updates only the fields sent and ignores `null`. `enabled: false` deactivates, but the API cannot reactivate it.
- Every `checkout_payment_options[].id` must match the `id` used in the JS file; options without a match are not shown. Use `version: "v2"` on each option to process payments through `Checkout.processPayment`; otherwise the deprecated legacy flow is used.
- An order is paid only when a transaction event with status `success` and type `sale` or `capture` arrives. The Process Payment response does not create or pay the order.
- One transaction per payment method used; a failed attempt and a retry are two transactions. Amounts are strings with two decimals; exclude card interest from the transaction amount.
- Business rules: callbacks must answer within 800 ms or are ignored; several apps' filters are intersected.

## Hard constraints

### Constraint: Answer business errors in the rate callback with 4xx, fast

The rate callback is protected by a circuit breaker: with at least 500 requests in 30 minutes and 50% failures (5xx or a 5-second timeout), calls stop for 5 minutes, then 10 probes decide whether to resume.

**Why this matters**

`4xx` keeps the service healthy in the breaker and lets the merchant's fallback shipping option appear. A `200` with an error message in the body counts as success and hides the fallback, so the shopper sees no shipping option. A `5xx` or slow response pushes the breaker toward opening for every store using the app.

**Detection**

A handler that catches "postal code not served" and returns `200 {"error": ...}`, or that calls the carrier's upstream API synchronously without a timeout.

**Correct**

```js
app.post("/rates", async (req, res) => {
	const quote = req.body;
	if (!coverage.serves(quote.destination.postal_code)) {
		return res.status(422).json({ message: "unsupported_postal_code" });
	}
	const rates = await pricing.quote(quote, { timeoutMs: 3000 });
	res.json({ rates });
});
```

**Wrong**

```js
res.status(200).json({ error: "We do not deliver to this postal code" });
```

Responses are cached for identical carts, origins and destinations: `200` for 15 minutes, `422` for 1 minute; other statuses are not cached.

### Constraint: Send rates with a matching code and a string reference

Each rate's `code` must equal an existing carrier option `code`, as a string. `reference`, when used, must be a string; `null` prevents the rate from being displayed. The reference comes back on the order as `shipping_option_reference`.

**Why this matters**

Rates with an unknown code or a null reference silently disappear from the checkout, and the app cannot recover its own quote id when it later processes the shipment.

**Detection**

`code: 1` (number), codes built from service names that differ in case from the options created at install, or `reference: null`.

**Correct**

```json
{
	"rates": [
		{
			"name": "Acme Express",
			"code": "express",
			"price": 28.15,
			"price_merchant": 28.15,
			"currency": "BRL",
			"type": "ship",
			"min_delivery_date": "2026-11-10T12:00:00-0300",
			"max_delivery_date": "2026-11-12T12:00:00-0300",
			"reference": "q-82731"
		}
	]
}
```

**Wrong**

```json
{ "name": "Acme Express", "code": "Express", "price": 28.15, "currency": "BRL", "type": "ship", "reference": null }
```

### Constraint: Verify signed payment requests and make Cancel idempotent

The platform calls your Process Payment, Cancel Payment and Payment Status endpoints from a published list of IPs, with `X-Timestamp` and `X-Signature` headers. The signature is RSA SHA-256 over `URL|timestamp|SHA-256(payload)`, verified with the published public key. Cancel is sent after a 5xx, a 20-second timeout or malformed JSON from Process, and retried with exponential backoff until `200`.

**Why this matters**

Without verification anyone can trigger charges on your backend. A non-idempotent cancel can reverse a payment twice or fail forever, and a cancel for an attempt you never processed must still return `200`.

**Detection**

A process endpoint that trusts the body without checking `X-Signature`, or a cancel endpoint that returns `404` for an unknown `payment_attempt_id`.

**Correct**

```js
app.post("/cancel", verifySignature, async (req, res) => {
	const attemptId = req.query.payment_attempt_id;
	const attempt = await attempts.find(attemptId);
	if (attempt && !attempt.cancelled) await psp.reverse(attempt.pspId);
	await attempts.markCancelled(attemptId); // repeat calls do nothing
	res.status(200).json({});
});
```

**Wrong**

```js
app.post("/cancel", async (req, res) => {
	const attempt = await attempts.find(req.query.payment_attempt_id);
	if (!attempt) return res.status(404).end();
	await psp.reverse(attempt.pspId);
	res.end();
});
```

### Constraint: Report every money movement as a transaction event

Create the transaction with `POST /orders/{order_id}/transactions` (`payment_provider_id`, `payment_attempt_id` from the process request, `payment_method`, `info.external_id`, `first_event` of type `authorization`, `sale` or `challenge`). Later changes go to `POST /orders/{order_id}/transactions/{id}/events`.

**Why this matters**

There is no endpoint to set an order's payment status; it is computed from transactions. A refund made in the provider's dashboard that is not posted as a `refund` event leaves the order as paid. Partial refunds from the admin only work for orders with a single `paid` or `partially_refunded` transaction created with `info.supports_partial_refund: true` and a `refund_url`.

**Detection**

A webhook handler from the PSP that updates only the app's database, or transactions created without `payment_attempt_id`.

**Correct**

```js
await api.post(`/orders/${orderId}/transactions/${txId}/events`, {
	type: "refund",
	status: "success",
	amount: { value: "40.00", currency: "BRL" },
	happened_at: refund.processedAt
});
```

**Wrong**

```js
await db.payments.update(paymentId, { status: "refunded" }); // the store never learns
```

The `refund_url` receives the platform's refund request; answer `202 Accepted` when accepted, or `422` with `error_code` `insufficient_account_balance`, `refund_rejected` or `transaction_date_too_old`. It must not contain path variables.

## Preferred pattern

Checkout JS file (hosted on a CDN; it and its scripts must load within 30 seconds or the options are hidden):

```js
LoadCheckoutPaymentContext(function (Checkout, PaymentOptions) {
	var card = PaymentOptions.Transparent.CardPayment({
		id: "acme_card", // same id as in checkout_payment_options
		version: "v2",
		onDataChange: Checkout.utils.throttle(function () {
			var total = Checkout.getData("totalPrice");
			Checkout.setInstallments(installmentsFor(total)); // respect min_installment_value
		}, 700),
		onSubmit: function () {
			Checkout.processPayment({ card_token: tokenFromPspSdk() }).catch(function (error) {
				Checkout.showErrorCode(error.response.data.message);
			});
		}
	});
	Checkout.addPaymentOption(card);
});
```

Only essential non-standard data (card tokens, captcha) goes in `extra`; map it in the APIs configuration with markers such as `#extra.card_token`. Success responses for Pix and wire transfer must include the payment data in `response_data.data` so the success page can show instructions.

Business Rules: register with `PUT /{store_id}/business_rules/integrations/{domain}` and `{url, event}`. Domains and scopes: `payments` (`read_payment_options`, `read_payments`), `shipping` (`read_shipping`), `location` (`read_locations`), `cart` (none). Respond with `command` and `detail`: `filter_shipping_options` and `filter_payments_options` keep only the listed options (an empty list removes all), `block_checkout` takes an empty `detail`, `location_prioritization` returns location ids and priorities. On failure or timeout the merchant's default location priority applies.

Checkout SDK customizations (hide payment options, add discount or installment text, hide installments) only work at the payment step and log valid ids with `getPaymentIds`.

## Common failure modes

- Creating several carriers per store, or option codes that change between installs.
- Filtering rates by merchant settings in the app, so the platform applies costs twice or shows nothing.
- Returning a single rate as an object instead of inside `rates`.
- Reporting tracking with `POST /orders/{id}/fulfill` or `/fulfillments` in multi-location stores: only the first fulfillment order is updated.
- Declaring `supported_currencies` that do not match the merchant's PSP account, so the provider is shown or hidden wrongly.
- Treating a `201` from Process Payment as a paid order instead of posting the transaction.
- Forgetting the `challenge` first event for 3D Secure and the follow-up `authorization` or `sale` event.
- Business rules endpoints doing remote lookups that exceed 800 ms.

## Review checklist

- [ ] Carrier and options are created once per store, with stable string codes and `allow_free_shipping: false`
- [ ] Rate callback returns `rates[]` with matching codes, string references, correct `price` and `price_merchant`
- [ ] Business errors return 4xx; upstream calls have timeouts well under 5 seconds
- [ ] Payment provider options use `version: "v2"` and ids that match the JS file
- [ ] Process, Cancel and Status endpoints verify `X-Signature` and the source IPs; Cancel is idempotent
- [ ] Transactions carry `payment_attempt_id`, and every capture, refund and expiration is posted as an event
- [ ] Refund URL answers `202` or `422` with a documented `error_code`
- [ ] Business rules callbacks answer within 800 ms with a valid `command`

## Related skills

- `tiendanube-oauth-apps`: install flow that creates carriers, providers and callbacks
- `tiendanube-orders-fulfillment`: fulfillment orders, tracking events, labels and disputes
- `tiendanube-catalog`: free shipping flags, dimensions and the `additional_days` metafield used in quotes
- `tiendanube-nube-sdk`: checkout UI extensions that are not payment options
- `tiendanube-webhooks`: order events a shipping app listens to

## Reference

- [Shipping Provider guide](https://nuvemshop.dev/en-US/api/guides/shipping-provider.md): app setup and scopes, one carrier per partner, option rules, rate limits per type, code and reference, free shipping in mixed carts, destination data by page, admin links
- [Shipping Carrier](https://nuvemshop.dev/en-US/api/resources/2025-03/shipping-carrier.md): carrier and option endpoints, rate fields, caching and TTL, circuit breaker and fallback, legacy fulfillment events
- [Payment Provider guide](https://nuvemshop.dev/en-US/api/guides/payment-provider.md): scopes, installation, checkout options, Process, Cancel and Status APIs, signature verification, transactions and refunds
- [Payment Provider](https://nuvemshop.dev/en-US/api/resources/2025-03/payment-provider.md): provider fields, currencies, installments, checkout payment options, authentication, PUT semantics
- [Payment Option](https://nuvemshop.dev/en-US/api/resources/2025-03/payment-option.md): listing active options with read_payments
- [Transaction](https://nuvemshop.dev/en-US/api/resources/2025-03/transaction.md): statuses, event types per method, 3D Secure, refund URL contract, discounts on external checkouts
- [Business Rules](https://nuvemshop.dev/en-US/api/resources/2025-03/business-rules.md): domains, events and scopes, callback registration, payload and commands, 800 ms timeout, location prioritization
- [Checkout](https://nuvemshop.dev/en-US/api/resources/2025-03/checkout.md): LoadCheckoutPaymentContext, getData, processPayment and showErrorCode, payment option types, installments, captcha info
- [Checkout SDK](https://nuvemshop.dev/en-US/api/resources/2025-03/checkout_sdk.md): payment step customizations
- [Multi inventory overview](https://nuvemshop.dev/en-US/api/guides/multi-inventory/multi-inventory.md): one quote per location and deprecated fulfillment endpoints
- [Admin MCP](https://nuvemshop.dev/en-US/ai-agents/admin-mcp.md): conversational queries of payment and shipping settings, out of scope for code
