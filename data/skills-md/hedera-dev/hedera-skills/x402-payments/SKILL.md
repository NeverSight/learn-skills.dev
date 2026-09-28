---
name: x402-payments
description: >
  x402 pay-per-use payments on Hedera. Use when gating HTTP resources behind native HBAR
  payments, wiring a self-hosted Hedera facilitator (verify/settle), building
  x402ResourceServer / ExactHederaScheme flows, or integrating WalletConnect payment
  retries (PAYMENT-REQUIRED → PAYMENT-SIGNATURE).
---

# x402 Payments (Hedera)

**Pay-per-use pattern:** store protected bytes off-chain, record access terms separately (on-chain or config), gate HTTP resources with **HTTP 402** + a **self-hosted Hedera facilitator** that verifies and settles native HBAR transfers.

```text
Buyer → GET protected resource
          ├─ free / public → resource
          └─ paid → 402 PAYMENT-REQUIRED
                → client signs HBAR transfer
                → retry with PAYMENT-SIGNATURE
                → resource server verify + settle via facilitator
                → PAYMENT-RESPONSE + resource
```

The resource server **never holds facilitator keys**. Settlement uses a funded **ECDSA** fee-payer account on the facilitator process.

## Quick Reference

| Piece | Role |
| ----- | ---- |
| Payment asset | `"0.0.0"` — native HBAR; amounts in **tinybars** (1 HBAR = 1e8) |
| Resource server | `@x402/core` + `ExactHederaScheme` → talks to facilitator over HTTP |
| Facilitator | `GET /supported`, `POST /verify`, `POST /settle`, `GET /health` |
| Client | Request → read 402 → sign → retry with `PAYMENT-SIGNATURE` (legacy `X-PAYMENT` also accepted) |
| Wallet | ECDSA Hedera account (e.g. HashPack via WalletConnect / UniversalProvider) |

See [references/examples.md](references/examples.md) for server/client snippets. See [references/facilitator.md](references/facilitator.md) for env vars and settle semantics.

## Critical: Facilitator Fee Payer

Hedera x402 settles with native `TransferTransaction`s. The buyer **partially signs** (authorize buyer → seller). The facilitator must:

1. Verify the signed payload against payment requirements
2. Co-sign as the advertised **fee payer** (`/supported`)
3. Pay network fees and submit until `SUCCESS`

Requires `FACILITATOR_ACCOUNT_ID` + `FACILITATOR_PRIVATE_KEY` on a funded **ECDSA** account — separate from deployer/seller keys. Do not put that key in the resource-server process.

## Critical: Prices Are Tinybars

Payment requirements use tinybars. Convert in UIs with 8-decimal helpers; never float.

```ts
const TINYBAR_PER_HBAR = 100_000_000n;
// hbar "1.5" → 150_000_000n tinybars
```

## Resource Server Flow (paid resource)

1. Load access terms for the resource — if missing → 404
2. If free/public → return the resource
3. Else build payment requirements: `payTo` = seller Hedera account id, `amount` in tinybars, asset `0.0.0`, network (e.g. `hedera:testnet`)
4. No payment header → **402** with `PAYMENT-REQUIRED` header + JSON body
5. With payment header → `verifyPayment` then `settlePayment`; only on success return resource + `PAYMENT-RESPONSE`

```ts
const facilitator = new HTTPFacilitatorClient({ url: FACILITATOR_URL });
const server = new x402ResourceServer(facilitator)
  .register(X402_NETWORK, new ExactHederaScheme());
await server.initialize(); // pulls fee-payer from /supported
```

## Client Flow

```ts
const first = await fetch(resourceUrl);
if (first.status === 402) {
  const paymentRequired = httpClient.getPaymentRequiredResponse(...);
  const payload = await httpClient.createPaymentPayload(paymentRequired);
  const headers = httpClient.encodePaymentSignatureHeader(payload);
  const paid = await fetch(resourceUrl, { headers });
  // processResponse → resource + settle receipt
}
```

Machine-to-machine clients use a key-based signer instead of a browser wallet.

## Checklist

- [ ] Resource server has no facilitator private key
- [ ] Client and server share the same `X402_NETWORK` (e.g. `hedera:testnet`)
- [ ] Amounts are tinybars; asset id is `0.0.0`
- [ ] 402 challenge → signed retry → verify → settle → resource only after success
- [ ] Fee-payer account is ECDSA and funded for network fees
- [ ] Facilitator `/health` OK before testing paid requests
- [ ] `payTo` is a Hedera account id string (e.g. `0.0.1234`), not an EVM address

## References

- [references/examples.md](references/examples.md) — resource server wiring, client retry loop, tinybar helpers
- [references/facilitator.md](references/facilitator.md) — endpoints, env vars, fee-payer role
- [x402 docs](https://docs.x402.org)
- [`@x402/hedera`](https://www.npmjs.com/package/@x402/hedera)
