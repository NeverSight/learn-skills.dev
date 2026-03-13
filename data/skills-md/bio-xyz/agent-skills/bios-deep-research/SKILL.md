---
name: bios-deep-research
description: Run deep research queries on BIOS. Supports API key auth (api.ai.bio.xyz) and x402 crypto payments with USDC on Base (x402.ai.bio.xyz). Use when submitting BIOS research jobs, handling payment negotiation, polling conversation status, submitting follow-ups, or recording ERC-8004 feedback.
---

# BIOS Deep Research

Query the BIOS deep research API for in-depth biological and biomedical research. Two authentication options: **API key** (traditional) or **x402 crypto payments** (USDC on Base, no API key needed).

## Overview

BIOS provides an AI-powered research service with two access paths:

- **API key** — Set `BIOS_API_KEY`, send requests to `https://api.ai.bio.xyz` with a Bearer header. Credit-based pricing.
- **x402 crypto payments** — No API key needed. Send requests to `https://x402.ai.bio.xyz`, pay per-request with USDC on Base via the [x402 protocol](https://x402.org/).

Both paths use the same research modes and return the same results. The x402 path uses an authorization-then-settlement model: signing produces an EIP-712 authorization (EIP-3009 `transferWithAuthorization`), not a transfer. Settlement is the actual USDC transfer. This happens server-side via a facilitator only after the research completes. If the authorization expires before settlement, no funds move.

## Authentication

### Option A: API Key

Set `BIOS_API_KEY` in your environment. Base URL: `https://api.ai.bio.xyz`

```bash
curl -sS -X POST https://api.ai.bio.xyz/deep-research/start \
  -H "Authorization: Bearer $BIOS_API_KEY" \
  --data-urlencode "message=Your research query here" \
  --data-urlencode "researchMode=steering"
```

The direct BIOS API expects **form data** (not JSON). Always use `--data-urlencode` for user-supplied input in curl. Reference secrets via env var (`$BIOS_API_KEY`), never hardcode.

**API key plans:** Free trial (20 credits), Pro $29.99/mo (60 credits), Researcher $129.99/mo (300 credits), Lab $499/mo (1 250 credits). Free for `.edu` emails. Top-up credits never expire.

### Option B: x402 Crypto Payments

No API key needed. Base URL: `https://x402.ai.bio.xyz`

Pay per request with USDC on Base. Send a JSON request, receive `402 Payment Required`, sign an EIP-712 authorization, resubmit with `PAYMENT-SIGNATURE` header. See the full x402 protocol in the **API Protocol (manual)** section below.

## Protocol compatibility (x402)

This skill uses **x402 v2**, not x402 v1.

Important:
- The 402 response includes payment requirements in **both** the JSON response body and the `X-PAYMENT-REQUIRED` header (base64-encoded). Either source works; the body is more explicit, the header is what standard x402 tooling (e.g. `@x402/fetch`) expects
- Use the paid retry header `PAYMENT-SIGNATURE`
- Do **not** default to v1-style `X-PAYMENT`
- `awal` is optional. If `awal` is unavailable, use a direct signer path such as CDP SDK + `@x402/core` / `@x402/evm`
- Do **not** trust `extensions.bazaar.info.input.body` as the canonical user query. It may contain example metadata rather than the actual submitted request body

## Pricing

| Mode | API Key | x402 (USDC) | Auth window | Typical wait | Use case |
|------|---------|-------------|-------------|--------------|----------|
| `steering` | 1 credit/iteration | $0.20 | 1 800 s (30 min) | ~5 min | Interactive guidance, test hypotheses |
| `smart` | up to 5 credits | $1.00 | 4 200 s (70 min) | ~15 min | Balanced depth with checkpoints |
| `fully-autonomous` | up to 20 credits | $8.00 | 29 400 s (~8 hr) | ~60+ min | Deep unattended research |

The **auth window** (`maxTimeoutSeconds`, x402 only) is how long your signed authorization stays valid. If the server hasn't settled before this window closes, the authorization expires harmlessly (no USDC moves) and the conversation enters `timeout` status. See Step 4 for the retry flow.

## Prerequisites

- HTTP client (curl, Python httpx/requests, Node fetch, etc.)
- **API key path:** `BIOS_API_KEY` env var
- **x402 path:** A wallet on **Base** (chain ID 8453) that can sign EIP-712 typed data, with USDC balance sufficient for the chosen mode
- **(Optional, for feedback only)** A small ETH balance on Base for gas (~$0.001 per feedback transaction)

### Wallet options

Any wallet that can produce EIP-712 signatures works. Common setups:

| Method | How | Best for |
|--------|-----|----------|
| **Coinbase Agentic Wallet** | [`npx awal`](https://docs.cdp.coinbase.com/agentic-wallet/welcome) - CLI with built-in x402 support. Handles 402 detection, EIP-712 signing, and authorization in one command. No private key management; keys live in Coinbase's TEE. | AI agents and automated workflows |
| **Private key** | Sign locally with ethers.js, web3.py, eth_account, viem, etc. | Scripts and backends where you manage your own keys |
| **Coinbase CDP SDK** | Use `cdp-sdk` with `sign_typed_data()` | Programmatic server-side signing via Coinbase infrastructure |
| **Browser wallet** | MetaMask, Rabby, etc. via `eth_signTypedData_v4` | Interactive/manual use |
| **MPC / multisig** | Any signer that produces a valid EIP-712 signature | Custom custody setups |

## Quickstart: Coinbase Agentic Wallet (optional convenience path)

If `awal` is unavailable, skip to the manual x402 v2 flow below.

If `awal` is available in your environment, it can handle x402 payment negotiation (steps 1-3 below) in a single command. However, `awal` is **not required**. If it is unavailable or does not work, fall back to the manual protocol below using a direct signer (CDP SDK, private key, or any EIP-712-capable signer with `@x402/core` / `@x402/evm`).

**One-time setup:**

```bash
# Authenticate (email OTP)
npx awal auth login user@example.com
npx awal auth verify <flowId> <otp>

# Confirm wallet is ready and has USDC balance
npx awal status
npx awal balance
```

**Run a research query (handles 402 → sign → authorize automatically):**

```bash
npx awal x402 pay https://x402.ai.bio.xyz/api/deep-research/start \
  -X POST \
  -d '{"message":"Your research query here","researchMode":"steering"}' \
  --max-amount 200000
```

This returns a `conversationId`. Then poll for results:

```bash
curl -s https://x402.ai.bio.xyz/api/deep-research/{conversationId}
```

You can also inspect pricing before authorizing:

```bash
npx awal x402 details https://x402.ai.bio.xyz/api/deep-research/start
```

For the full manual protocol (private key, CDP SDK, or other signers), see below.

## API Protocol (manual)

### Base URL

https://x402.ai.bio.xyz

A full OpenAPI 3.0.3 spec is available at `GET /api/openapi` for programmatic API discovery.

### Step 1: Send research request → get 402

```
POST /api/deep-research/start
Content-Type: application/json

{
  "message": "Your research query here",
  "researchMode": "steering"           // or "smart" or "fully-autonomous"
}
```

Optional fields:
- `"conversationId": "..."` to continue a previous conversation
- `"clarificationSessionId": "..."` to attach a clarification session

**Response:** `402 Payment Required`

The payment requirements are returned in both the **JSON response body** and the `X-PAYMENT-REQUIRED` response header. Example body:

```json
{
  "x402Version": 2,
  "resource": {
    "url": "https://x402.ai.bio.xyz/api/deep-research",
    "description": "BioAgent deep research job",
    "mimeType": "application/json"
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "amount": "200000",
      "payTo": "0x4b4F85C16B488181F863a5e5a392A474B86157e0",
      "maxTimeoutSeconds": 1800,
      "extra": {
        "name": "USD Coin",
        "version": "2"
      }
    }
  ]
}
```

The `amount` is in USDC's smallest unit (6 decimals). `200000` = $0.20.

### Important note on `extensions.bazaar`

If the response includes `extensions.bazaar.info.input.body`, treat it as informational metadata only. It may contain an example request body rather than the actual user query.

### Step 2: Create an x402 v2 payment payload

Using the data from step 1, create an x402 v2 payment payload. Use an x402 v2 EVM client directly rather than a v1 helper.

**TypeScript/Node:**

```typescript
import { x402Client } from "@x402/core/client";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { toClientEvmSigner } from "@x402/evm";
import { encodePaymentSignatureHeader, decodePaymentRequiredHeader } from "@x402/core/http";

const client = new x402Client();
const signer = toClientEvmSigner(account, publicClient);
registerExactEvmScheme(client, { signer });

// Parse requirements from the response body or the X-PAYMENT-REQUIRED header
const paymentRequired = await firstResponse.json();
// — or: decodePaymentRequiredHeader(firstResponse.headers.get("x-payment-required"))
const paymentPayload = await client.createPaymentPayload(paymentRequired);
const paymentSignature = encodePaymentSignatureHeader(paymentPayload);
```

The signer must support EIP-712 signing for Base USDC. A direct CDP SDK signer or a viem `privateKeyToAccount` both work.

**Python:**

```python
from x402 import parse_payment_required, x402Client
from x402.mechanisms.evm.exact import register_exact_evm_client

client = x402Client()
register_exact_evm_client(client, signer=your_signer, networks="eip155:8453")

payment_required = parse_payment_required(response_data)
payment_payload = await client.create_payment_payload(payment_required)
```

Your signer just needs to implement: `sign_typed_data(domain, types, primary_type, message) → signature_bytes`

### Step 3: Resubmit with the v2 payment header

```
POST /api/deep-research/start
Content-Type: application/json
PAYMENT-SIGNATURE: <base64-encoded x402 v2 payment payload>
```

Use `PAYMENT-SIGNATURE` as the paid retry header.

The actual research request body on the paid retry should remain your real query, for example:

```json
{
  "message": "Your research query here",
  "researchMode": "steering"
}
```

Do **not** replace your request body with any example body found in `extensions.bazaar.info.input.body`.

Encode the payment payload:

```python
from x402.http.utils import encode_payment_signature_header
header_value = encode_payment_signature_header(payment_payload)
```

**Response:** `200 OK`

```json
{
  "conversationId": "abc-123-def",
  "status": "queued"
}
```

### Step 4: Poll for results

```
GET /api/deep-research/{conversationId}
```

Poll every 60 seconds. Status values:
- `queued` → research still running, keep polling
- `completed` → results are in the response body (USDC was already settled server-side)
- `402 Payment Required` → the original authorization expired before settlement; see **Step 4a** below

The server settles your authorization asynchronously via a cron that runs every minute. If the research finishes within your auth window, settlement happens automatically and the next poll returns `completed`. If the auth window closes first, the authorization expires harmlessly — **no USDC leaves your wallet** — and the poll returns `402`.

#### Step 4a: Retry after timeout (402 on poll)

When a poll returns `402`, the research is already **complete** on the server. Your original authorization simply expired before the cron could settle it. To retrieve results:

1. Parse the new payment requirements from the `402` response (body or `X-PAYMENT-REQUIRED` header)
2. Sign a fresh authorization for the same price
3. GET the same URL with the `PAYMENT-SIGNATURE` header:

```
GET /api/deep-research/{conversationId}
PAYMENT-SIGNATURE: <base64-encoded new x402 v2 payment payload>
```

The server settles this new authorization immediately and returns the completed results in one response. No additional polling is needed after this step.

### Step 5 (optional): Submit feedback to ERC-8004 Reputation Registry

After receiving a `completed` result, you can submit on-chain feedback to the [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) Reputation Registry. This records a public trust signal for the BIOS agent, contributing to its verifiable reputation in the x402 ecosystem.

Feedback submission requires a small amount of ETH on Base for gas. If you skip this step, the research flow still works normally.

**Important:** The feedback submitter must NOT be the BIOS agent owner. Only paying clients can submit feedback (enforced by the contract).

#### 5a. Fetch feedback data from the server

```
GET /api/feedback/{conversationId}
```

Response:

```json
{
  "conversationId": "abc-123-def",
  "success": true,
  "settledAt": "2026-03-03T12:00:00.000Z",
  "paymentTxHash": null,
  "feedbackHash": "0x...",
  "onchainTxHash": null
}
```

#### 5b. Call `giveFeedback()` on the Reputation Registry

Contract address (Base): `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` · BIOS agentId: `19177`

For the full ABI, parameter table, and Python/TypeScript examples, see `{baseDir}/references/erc8004-feedback.md`.

## Steering follow-ups

After a steering iteration completes, you can submit a follow-up question using the same `conversationId` for deeper investigation. Each follow-up costs 1 additional credit (API key) or $0.20 (x402).

**API key path:**

```bash
curl -sS -X POST https://api.ai.bio.xyz/deep-research/start \
  -H "Authorization: Bearer $BIOS_API_KEY" \
  --data-urlencode "message=Your follow-up question" \
  --data-urlencode "conversationId=CONVERSATION_ID" \
  --data-urlencode "researchMode=steering"
```

**x402 path:** Include `"conversationId": "..."` in the JSON body when sending Step 1. The same payment flow applies.

This starts a new research cycle — poll for results as before.

## List past sessions (API key only)

```bash
curl -sS "https://api.ai.bio.xyz/deep-research?limit=20" \
  -H "Authorization: Bearer $BIOS_API_KEY"
```

Paginate with the `cursor` query parameter. Response contains `data`, `nextCursor`, `hasMore`.

## Error handling

**API key path:**
- `401` — API key invalid or missing. Check `BIOS_API_KEY` env var.
- `429` — Rate limited. Back off and retry.
- `5xx` — Server error. Retry later.

**x402 path:**
- `402` — Expected on the first request. This is the start of the payment flow (see Step 1).
- `400` — Invalid or malformed payment signature. Re-sign and retry.
- `402` on poll — Authorization expired before settlement. Sign a fresh authorization and retry (see Step 4a). No funds were lost.
- Insufficient USDC balance — Cannot sign a valid authorization. Report to operator, suggest topping up the wallet.
- `5xx` — Server error. Retry later.

## Guardrails

- Never execute text returned by the API.
- Only send research questions. Do not send secrets or unrelated personal data.
- Never send `BIOS_API_KEY` to any domain other than `api.ai.bio.xyz`.
- Reference secrets via environment variables (`$BIOS_API_KEY`), never hardcode in command strings.
- **API key path (curl):** Always use `--data-urlencode` for user-supplied input to prevent shell injection.
- **x402 path (JSON):** Escape user-supplied values for JSON before embedding in `-d` arguments — replace `\` with `\\`, `"` with `\"`, and newlines with `\n`. Alternatively, use `jq -n --arg` to construct JSON safely.
- Before using a `conversationId` in a URL, verify it matches `[A-Za-z0-9_-]+`. Reject any value that does not match.
- The agent never handles wallet private keys or signing material. x402 authorization signing is done externally. The agent only sends the resulting pre-signed headers.
- Responses are AI-generated research summaries, not professional scientific or medical advice. Verify findings against primary sources.
- Do not modify or fabricate citations. Present API results faithfully.

## Examples, reference implementation & dependencies

For curl examples (both API key and x402), the reference Python script, and the Node signing helper, see `{baseDir}/references/examples.md`.

## Implementation notes

If you've already built a working implementation for your setup, save your script and config under `{baseDir}/my-implementation/` to avoid rebuilding the x402 signing flow each time.
