---
name: x402-agentic-creation
description: Monetize your agent's API or tools using the x402 protocol and USDC micropayments. Enables provisioning, earnings tracking, and withdrawals.
---

# x402-creation

**The monetization layer for the Agentic Web.**

Enable your agent to autonomously earn USDC on Base or Solana by monetizing its own API endpoints or services. This skill handles provisioning, earnings tracking, and automated withdrawals via the x402 protocol.

[Official Website](https://gatex402.dev) | [LLM Documentation](https://gatex402.dev/llms-full.txt)

## Platform Data

- **Protocol**: x402 (HTTP 402 Payment Required)
- **Currency**: USDC (Stablecoin)
- **Networks**: Base Mainnet (Ethereum L2), Solana Mainnet
- **Fees**: 1% platform fee (99% provider revenue)
- **Payouts**: Daily automated withdrawals
- **Min Price**: $0.001 per request

## x402 Protocol Flow

1. **Challenge**: Gateway returns HTTP 402 with payment headers.
2. **Transfer**: Agent submits USDC transfer to specified address.
3. **Verification**: Facilitator confirms transaction on-chain.
4. **Dispatch**: Gateway forwards the authorized request to the provider.

## Activation

Add this skill to your agent to allow it to:

- **Provision**: Register a new API gateway instance on GateX402.
- **Monetize**: Set USDC pricing per request for its tools/endpoints.
- **Withdraw**: Transfer USDC earnings to its wallet.

## Tools

### `provision_api`

Use this tool to register a new API on the GateX402 gateway.

- **Required Inputs**:
  - `api_name` — Human-readable name for the API.
  - `network` — CAIP-2 network ID (e.g. `eip155:8453` for Base Mainnet, `solana:5eykt4UsFv8P8NJdTREpY1vzqAQZSSfL` for Solana Mainnet).
  - `origin_url` — **Your API’s base URL** (the backend you are monetizing), e.g. `https://your-api.example.com`. Do not use the gateway URL (`api.gatex402.dev`).
  - `routes` — Array of `{ path_pattern, method, price_usdc }` (e.g. `path_pattern: "/v1/chat"`, `method: "POST"`, `price_usdc: 0.01`).
- **Outcome**: Returns only `api_slug`, `provider_id`, and a short message in a boundary-wrapped response. The management token is stored by the runtime via `storeManagementToken` and is never returned to the agent.

### `get_earnings`

Retrieve real-time balance of earned USDC split by network.

- **Inputs**: None (uses management token from host).
- **Outcome**: Sanitized balance data wrapped in `<!-- GATEX402_API_RESPONSE -->` boundaries.

### `withdraw_funds`

Trigger a payout to your registered wallet.

- **Required Inputs**: `network` (e.g. `eip155:8453` for Base Mainnet, `solana:5eykt4UsFv8P8NJdTREpY1vzqAQZSSfL` for Solana Mainnet).
- **Outcome**: Sanitized status/tx data wrapped in response boundaries.

## Guardrails

- **Management Token**: The runtime stores the `gx4_mgmt_...` token via `storeManagementToken`; it is never returned to the agent.
- **Credentials**: Wallet private key and management token are injected by the host via `createTools` only; they must never appear in tool parameters.

## Resources

- **Backend**: https://api.gatex402.dev (all provisioning, balance, and withdrawal requests)
- **OpenAPI spec**: https://api.gatex402.dev/openapi.json
- **Homepage**: https://gatex402.dev
- **Bazaar Discovery**: https://gatex402.dev/discover
- **AI Plugin**: https://api.gatex402.dev/.well-known/ai-plugin.json
