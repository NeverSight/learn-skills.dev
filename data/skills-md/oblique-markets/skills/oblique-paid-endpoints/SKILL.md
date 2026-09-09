---
name: oblique-paid-endpoints
description: Buy pay-per-call API results from oblique.markets (https://api.oblique.markets/api/v1/paid/*) over HTTP 402 — x402 with USDC on Base or Solana, or MPP/Tempo — with no account and no API key. Use when an agent needs x402 Bazaar market data, Base or Solana chain state (gas, block, USDC balance, tx status, priority fees), web extraction, sentiment, sandboxed Python, task routing or LLM inference and can pay a few tenths of a cent per call from its own wallet. Includes a no-wallet quote script, a live catalogue printer and a self-contained buyer that settles a real x402 payment.
license: MIT
metadata:
  author: oblique-markets
  version: "1.1.0"
  homepage: https://oblique.markets
---

# Buying from oblique.markets paid endpoints

Every route under `https://api.oblique.markets/api/v1/paid/*` answers an unpaid request
with **HTTP 402** and a machine-readable quote. You pay the quoted amount, retry the same
request with a payment header, and get JSON. There are no accounts and no API keys; the
payment is the authentication. Two rails are offered on the same 402 (dual-stack):

| Rail | Networks / asset | Retry header | Success header |
|---|---|---|---|
| **x402 v2** | Base `eip155:8453` USDC · Solana `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` USDC | `PAYMENT-SIGNATURE: <base64 payment payload>` | `PAYMENT-RESPONSE` |
| **MPP (Machine Payments Protocol)** | Tempo mainnet chainId `4217`, method `tempo`, intent `charge`, currency `0x20c0000000000000000000000000000000000000` (pathUSD) | `Authorization: Payment <base64url credential>` | `Payment-Receipt` |

Prices are per call, quoted in USD and settled in stablecoin atomic units (6 decimals:
`"2000"` = $0.002). On 2026-09-09 the catalogue advertised 77 paid routes from $0.001079
to $1.00; most cost $0.002–$0.05. Use an SDK for production buying; the bundled
`scripts/buy.py` shows the whole loop in ~150 lines if you want to see exactly what an SDK
signs.

## Discovery surfaces (all free, no auth)

| What | URL |
|---|---|
| x402 catalogue — every route with method, price, scheme, pay-to, MPP terms | `https://oblique.markets/.well-known/x402.json` |
| OpenAPI 3.1 — request bodies, query params, response schemas | `https://oblique.markets/openapi.json` |
| Agent card (A2A) | `https://oblique.markets/.well-known/agent.json` |
| `llms.txt` (prices inline) | `https://api.oblique.markets/llms.txt` |
| Paid MCP server (same routes as tools; listing is free, each call is paid) | `https://api.oblique.markets/mcp` |
| Health (free) | `https://api.oblique.markets/health` |
| Worked clients: TypeScript + Python + MCP configs | `https://github.com/oblique-markets/oblique-examples` |
| Catalogue snapshot with prices (regenerate with `scripts/catalog.py`) | [references/catalog.md](references/catalog.md) |

```bash
scripts/catalog.py                  # today's catalogue as a Markdown table, no wallet
scripts/catalog.py --grep solana    # only matching routes
scripts/catalog.py --json           # machine-readable
```

## Step 1 — read the quote (free)

```bash
curl -si https://api.oblique.markets/api/v1/paid/bazaar-pulse
scripts/quote.sh bazaar-pulse       # same, decoded: x402 accepts, MPP terms, input shape, output example
```

The 402 carries the quote three ways at once:

- **`PAYMENT-REQUIRED` header** — base64 of the x402 v2 `PaymentRequired` JSON.
- **JSON body** — the same object, readable:
  `{"x402Version":2,"accepts":[{"scheme":"exact","network":"eip155:8453","amount":"2000","payTo":"0x9700…D3Ab","asset":"0x8335…2913","maxTimeoutSeconds":60,…},{"network":"solana:5eykt4…","amount":"2000","payTo":"GYyT…ykdS","asset":"EPjF…Dt1v",…}],"extensions":{"bazaar":{"info":{"input":…,"output":{"example":…}}}}}`.
  `extensions.bazaar.info` tells you the input shape and shows an example output **before you
  pay** — read it.
- **`WWW-Authenticate: Payment id="…", realm="api.oblique.markets", method="tempo", intent="charge", request="<base64url>", expires="…"`** — the MPP challenge. `request` decodes to
  `{"amount":"2000","currency":"0x20c0…0000","methodDetails":{"chainId":4217,"supportedModes":["pull"]},"recipient":"0xD96A…3D6d"}`.

`x-payment-amount: $0.002` is also set as a convenience. The challenge is authoritative:
take `amount`, `payTo`, `asset`, `network` from it, never from memory.

## Step 2 — pay and retry

### Quickest: the bundled buyer (Base USDC, no SDK)

`scripts/buy.py` is a complete x402 `exact` buyer in plain Python (`requests` + `eth-account`).
It reads the 402, refuses any quote above your ceiling, signs an EIP-3009
`transferWithAuthorization` for exactly the quoted amount, retries with `PAYMENT-SIGNATURE`,
and prints the result and the decoded settlement receipt (transaction hash included).

```bash
pip install requests==2.32.5 eth-account==0.13.7
printf '%s' '0xYOUR_PRIVATE_KEY' > ./buyer.key       # a dedicated wallet with a little USDC on Base
scripts/buy.py bazaar-pulse --key-file ./buyer.key                       # $0.002
scripts/buy.py 'base-usdc-balance?address=0x970007590aCC5C938cd51345B17AF51B1B40D3Ab' --key-file ./buyer.key
scripts/buy.py web-extract --post '{"url":"https://example.com"}' --max-usd 0.05 --key-file ./buyer.key
scripts/buy.py bazaar-pulse --quote-only                                 # no key: print the quote
```

The key is read from the file named by `--key-file` and nowhere else. `--max-usd` defaults
to 0.01, so a mispriced or unexpected quote exits 3 without signing. Exit 0 is a settled
purchase; 4 means the facilitator rejected the payment; 5 means the route rejected your
input after payment, which settles nothing.

### x402 SDKs (Base or Solana USDC)

The v2 SDKs read the 402, pick a network you configured, sign the USDC authorization, and
retry with `PAYMENT-SIGNATURE`. Working files in `oblique-markets/oblique-examples`:

| Client | File (in the oblique-examples repo) | Buys |
|---|---|---|
| TypeScript, `@x402/fetch` + viem | `oblique-examples/examples/typescript/x402-fetch/index.ts` | `/api/v1/paid/time`, $0.01 |
| TypeScript, Vercel AI SDK `tool()` | `oblique-examples/examples/typescript/vercel-ai-tool/bazaar-pulse-tool.ts` | `bazaar-pulse` |
| Python, `x402[requests,evm]` | `oblique-examples/examples/python/requests/pay_for_time.py` | `time` |
| Python, LangChain `@tool` | `oblique-examples/examples/python/langchain-tool/bazaar_pulse_tool.py` | `bazaar-pulse` |

All four take the private key of a Base wallet holding a little USDC and set an explicit
per-payment ceiling so a mispriced challenge fails instead of spending. Use a dedicated,
thinly funded wallet. Note the SDK generation: x402 **v2** (`@x402/fetch` 2.x, `x402` 2.x on
PyPI, CAIP-2 network ids, `PAYMENT-REQUIRED`/`PAYMENT-RESPONSE` headers). The v1 packages
(`x402-fetch` 1.x, `X-PAYMENT` header) are deprecated and will not match.

Python sketch (`pip install x402[requests,evm]==2.22.0`; mirrors `pay_for_time.py`):

```python
from eth_account import Account
from x402 import SchemeRegistration, prefer_network, x402ClientConfig, x402ClientSync
from x402.http.clients.requests import x402_requests
from x402.mechanisms.evm.exact import ExactEvmScheme
from x402.mechanisms.evm.signers import EthAccountSigner

with open("buyer.key") as f:                                  # dedicated wallet, a little USDC on Base
    signer = EthAccountSigner(Account.from_key(f.read().strip()))
config = x402ClientConfig(
    schemes=[SchemeRegistration(network="eip155:*", client=ExactEvmScheme(signer=signer))],
    spend_controls={"max_amount_per_payment": "$0.05"},   # ceiling: a mispriced quote fails, not spends
    policies=[prefer_network("eip155:8453")],             # Base; register x402.mechanisms.svm.exact for Solana
)
session = x402_requests(x402ClientSync.from_config(config))  # requests.Session: 402 → sign → retry
route = "https://api.oblique.markets/api/v1/paid/base-gas-price"
r = session.get(route, timeout=30)
r.raise_for_status()
print(r.json(), r.headers.get("PAYMENT-RESPONSE"))            # JSON result + base64 settlement receipt
```

### MPP / Tempo

The MPP credential is `Authorization: Payment <base64url JSON>` where the JSON is
`{"challenge":{…echoed WWW-Authenticate params…},"payload":{…tempo-specific signed
transfer…}}` (spec: `https://paymentauth.org/draft-httpauth-payment-00.txt`, §5.2). The
`mppx` client builds it for you (`npm install mppx@0.9.2 viem@2.56.3`):

```ts
import { privateKeyToAccount } from 'viem/accounts'
import { Mppx, tempo } from 'mppx/client'
Mppx.create({ methods: [tempo({ account: privateKeyToAccount(buyerKey) })] })   // buyerKey: read from your key file
// installs a payment-aware fetch: 402 → sign Tempo charge → retry with Authorization: Payment
const route = 'https://api.oblique.markets/api/v1/paid/bazaar-pulse'
const r = await fetch(route)
```

A successful MPP response carries `Payment-Receipt` (base64url JSON). Docs: `https://mpp.dev`
(Tempo charge: `/payment-methods/tempo/charge`).

## Step 3 — read the result

200 with `application/json`. Shapes are in `openapi.json` and in the challenge's
`extensions.bazaar.info.output.example`. Payment failures come back as a fresh 402 (x402 puts
the reason in the body `error`; MPP uses RFC 9457 problem details). A 4xx other than 402 with
a valid payment means the input was rejected (check the schema) — no charge is settled.
`PAYMENT-RESPONSE` decodes to `{"success":true,"transaction":"0x…","network":"eip155:8453","payer":"0x…"}`;
the transaction is the on-chain USDC transfer you can verify yourself.

## When to use which cheap route

Prices from the live catalogue on 2026-09-09. GET routes take query params; POST routes take
JSON bodies. Every one is also a paid MCP tool (`bazaar_pulse`, `base_gas_price`, …).

| Route | Price | Use it when you need… | Input |
|---|---|---|---|
| `GET /api/v1/paid/bazaar-pulse` | $0.002 | the x402 Bazaar's latest daily snapshot: totals, top services by settled calls/payers, networks | none |
| `GET /api/v1/paid/bazaar-price-stats` | $0.002 | how Bazaar listings are priced: min/p25/p50/p75/p90/max, USD bands, per-network medians | `?network=base` or `solana` (optional) |
| `GET /api/v1/paid/base-gas-price` | $0.002 | current Base gas price + EIP-1559 base fee (wei and gwei) with block number | none |
| `GET /api/v1/paid/base-block-number` | $0.002 | current Base mainnet block height from redundant public RPCs | none |
| `GET /api/v1/paid/base-usdc-balance` | $0.003 | a wallet's USDC balance on canonical Base USDC (atomic + formatted) | `?address=0x…` (40 hex) |
| `GET /api/v1/paid/base-tx-status` | $0.003 | success/revert, block, confirmations, gas used, effective gas price of a Base tx | `?hash=0x…` (64 hex) |
| `GET /api/v1/paid/solana-priority-fee` | $0.002 | current Solana slot/block height and a prioritization-fee summary (min/median/p75/max) before sending a tx | `?accounts=…` (optional, up to 5) |
| `GET /api/v1/paid/x402-facilitator-health` | $0.003 | whether the x402 rail is up: live probes of the facilitators with status + latency | none |
| `POST /api/v1/paid/web-extract` | $0.03 | one page as JSON: url, title, meta description, cleaned text, timestamp | `{"url":"https://…"}` |
| `POST /api/v1/paid/run-python` | $0.05 | a short Python program executed in an isolated sandbox, stdout/stderr/exit code returned | `{"code":"…"}` per OpenAPI |
| `POST /api/v1/paid/research-answer` | $0.01 | a concise, cited answer to one research question | `{"question":"…"}` per OpenAPI |
| `POST /api/v1/paid/sentiment` | $0.05 | sentiment of a text block or of current coverage of a topic | `{"query":"…"}` per OpenAPI; the challenge also advertises `{"text":…}` / `{"topic":…}` |
| `POST /api/v1/paid/mpp-route` | $0.01 | a ranked top-3 of catalogued services for a natural-language task, with prices, payment methods and MCP schemas | `{"task":"…","price_cap":0.05,"preferred_chain":"base\|solana\|tempo"}` (`task` required) |

Other frequently useful routes: `time` / `echo` ($0.01, the smallest end-to-end payment
test), `crypto-price` ($0.004), `token-metrics` ($0.003), `x402-endpoint-verify` ($0.02,
lint someone else's 402), `settlement-verify` ($0.01, prove a Base USDC settlement landed),
`inference` (LLM proxy; `$1.00` maximum on Base under the `upto` scheme, `$0.01` fixed on
Solana; models at the free `GET /api/v1/models`). The full list with prices is in
[references/catalog.md](references/catalog.md); `scripts/catalog.py` prints today's.

## Rules of thumb

- Fetch the quote first (free) and compare `amount` against your ceiling before paying.
- Snapshot-based Bazaar routes update once a day; do not re-buy the same day expecting change.
- Prefer Base for `exact` payments (both facilitators cover it); Solana needs the fee-payer the
  challenge names in `extra.feePayer`.
- `scripts/quote.sh <route>` prints the decoded quote for any route without paying;
  `scripts/buy.py <route> --quote-only` does the same from Python.
- The free observatory at `https://remote.observer` (see the `remote-observer` skill) already
  answers the daily Bazaar diff and provider ranking at no cost — pay here for the fuller
  paid variants (`bazaar-trending`, `bazaar-seller-rank`, `bazaar-market-report`, …) or for
  non-market routes.
