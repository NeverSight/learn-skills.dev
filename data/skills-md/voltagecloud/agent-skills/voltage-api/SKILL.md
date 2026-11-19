---
name: voltage-api
description: Build integrations and operate the Voltage API, including wallets, Lightning and on-chain payments, USD quotes, webhooks, balances, and hosted checkout. Use for Voltage product questions, CLI installation and usage, API code, curl requests, and payment debugging. Does not cover the separate Infrastructure API or direct LND administration.
---

# Voltage API

Use **Voltage API** in developer contexts and **Voltage** for the product. Older
sources and dashboard labels may say “Payments”; keep exact API identifiers and
UI labels when needed to locate something.

## Choose the interface

- For supported account operations, prefer the installed `voltage` CLI. Read the
  [CLI guide](references/cli.md) for installation, authentication, commands, and
  output handling. If absent, offer installation when useful; direct API requests
  remain supported. Honor an explicit interface choice.
- For application integrations, use the API contract and server-side examples;
  do not replace API integration code with CLI subprocess calls.
- CLI questions use the official release documentation and installed command help.
  API payloads and business rules use the contract below. Load only the references
  needed for the chosen path.

## Establish the contract

1. Use the bundled [OpenAPI contract](references/openapi.json), including its
   embedded guides, as the authority. Its provenance is in
   [sources.json](references/sources.json).
2. Use [Voltage docs](https://docs.voltageapi.com/) for product/setup context only
   where consistent with the contract. Consult
   [known discrepancies](references/known-discrepancies.md) before adapting examples.
3. Do not use older Voltage APIs, third-party snippets, or model memory to invent
   missing endpoints or behavior. When asked for current information, verify the
   live [contract](https://voltageapi.com/v1/openapi/docs.json) and affected docs;
   disclose unavailable verification. Do not silently rewrite the installed snapshot.
4. If the contract itself documents a gap, expose the limitation. In particular,
   do not fabricate a canonical Taproot Asset send request.

## Read only what the task needs

| Task | Reference |
|---|---|
| Install, configure, operate, or troubleshoot the Voltage CLI | [CLI guide](references/cli.md) |
| Understand terminology, funding models, setup, or applicability | [Product model](references/product-model.md) |
| Obtain IDs, configure credentials, execute curl, or switch environment | [Configuration and execution](references/configuration.md) |
| Find any endpoint, auth requirement, payload, filter, or response | [API index](references/api-index.md), then inspect the exact operation |
| Send, receive, poll, handle errors, inspect balances | [Payment lifecycle](references/payment-lifecycle.md) |
| USD conversion, processing fees, treasury, swaps | [Specialized flows](references/specialized-flows.md) |
| Verify callbacks, manage deliveries, reconcile payments | [Webhooks](references/webhooks.md) |
| Integrate hosted checkout or browser session/stream APIs | [Checkout](references/checkout.md) |

Resolve scripts and references relative to **this installed skill directory**, not
the user's project. In the commands below, `<skill-dir>` means that directory:

```sh
python3 <skill-dir>/scripts/inspect-operation.py create_payment --part request
python3 <skill-dir>/scripts/inspect-operation.py get_payment --part response
python3 <skill-dir>/scripts/inspect-operation.py --schema Amount
python3 <skill-dir>/scripts/inspect-operation.py --guide Payments --section 'Workflow: pay a known BTC invoice from a USD wallet'
```

The inspector includes referenced schema definitions and operation-specific
security schemes. Read both constraints and descriptions: runtime prerequisites
are not all expressible in JSON Schema. The unmodified source guides may contain
upstream relative links; those are not local skill files.

## Integrate or execute

- Establish organization, environment, wallet, network, currency, and the intended
  action. Reuse configured values and prior user authorization. Ask only for missing
  details that affect correctness or authorization. Do not pick a wallet arbitrarily.
- For direct API account access use an environment key in `x-api-key`; the CLI
  also supports browser login. Check each operation's security contract; checkout
  browser tokens are different credentials.
- Generate and persist UUIDv4 IDs before submitting payments; CLI friendly payment
  commands can generate and journal these for you. Raw payment and treasury JSON
  must include an explicit `id`. Empty `202` means accepted, not paid. Use bounded reads to wait for the needed state; reconcile
  ambiguous writes by the existing ID rather than blindly retrying or creating a new ID.
- API payloads use integer base units: BTC millisatoshis, USD cents, assets their
  base units. CLI friendly amount flags accept explicit units and convert exactly.
  For generated JavaScript, reject values outside the safe-integer range or use a
  lossless JSON strategy; the API's int64 range exceeds JavaScript's safe integers.
- Direct requests are supported through the [curl helper](scripts/request.py).
  Read configuration guidance first. It performs one request with no automatic retry,
  and supports the environment-API-key operations, not checkout browser transport.
- A balance check authorizes reads; an invoice request authorizes that receive;
  a send requires an authorized destination, amount, wallet, and understood fees.
  Resolve consequential ambiguity before execution. Do not require repeat approval
  for actions already authorized. A connectivity check alone does not authorize spending.
- Before test payments, verify the wallet's network and environment. A label such
  as “staging” does not prove test funds. Do not silently fall back to mainnet.
- Keep secrets server-side and out of chat, logs, version control, and browser code.
  Webhook creation/rotation returns a one-time secret: arrange secure output before
  executing it. Preserve customer defaults when using one-off configuration overrides.

For application code, adapt [voltage-client.ts](assets/voltage-client.ts) for
bounded payment polling and [verify-webhook.ts](assets/verify-webhook.ts) for raw-body
signature verification. These are focused examples, not a full SDK. Inspect the
operation and response schemas when extending them.

Report the HTTP outcome separately from the business outcome, include relevant
non-secret resource IDs, and state whether a payment completed, failed, is still
pending, or has an uncertain submission outcome. Never label an invoice as paid
because it was generated or a webhook delivery succeeded.
