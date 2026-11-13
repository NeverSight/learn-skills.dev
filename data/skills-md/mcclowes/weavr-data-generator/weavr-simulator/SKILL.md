---
name: weavr-simulator
# prettier-ignore
description: Use when testing Weavr integrations in sandbox - simulate deposits, card transactions, KYC/KYB verification, wire transfers, and 2FA challenges
---

# Weavr Simulator API

API Reference: https://weavr-simulator-api.redoc.ly/

**Sandbox-only** testing tool for simulating financial operations.

## Quick Start

```typescript
// Simulate account deposit - POST /accounts/{account_id}/deposit
// Header: api-key (API_Secret_Key)
{
  "depositAmount": { "currency": "GBP", "amount": 10000 },
  "senderName": "Test Sender",
  "reference": "Test deposit"
}
// Response: { "code": "COMPLETED" }
```

## Core Endpoints

| Category | Endpoint | Purpose |
|----------|----------|---------|
| **Accounts** | `POST /accounts/{id}/deposit` | Simulate incoming wire transfer |
| **Cards** | `POST /cards/{id}/purchase` | Simulate card transaction |
| **Cards** | `POST /cards/{id}/merchant_refund` | Simulate refund |
| **Identity** | `POST /consumers/{id}/verify` | Auto-verify consumer KYC |
| **Identity** | `POST /corporates/{id}/verify` | Auto-verify corporate KYB |
| **Transfers** | `POST /wiretransfers/outgoing/{id}/accept` | Complete OWT |
| **Transfers** | `POST /wiretransfers/outgoing/{id}/reject` | Reject OWT |
| **2FA** | `POST /factors/{cred_id}/challenges/{id}/verify_success` | Pass 2FA |

## Authentication

Header: `api-key` with your API Secret Key (not the regular api-key)

## Reference Files

See [references/endpoints.md](references/endpoints.md) for full endpoint details and request bodies.
