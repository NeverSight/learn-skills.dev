---
name: a2a-wallet
description: >
  Use the a2a-wallet CLI to interact with A2A agents — send messages, stream responses,
  and manage tasks. Also supports x402 payment signing and SIWE authentication required
  by A2A agents. Trigger when the user needs to: send a message to an A2A agent, sign
  an x402 payment, authenticate via SIWE, log in or out of a2a-wallet, check their
  wallet address or balance, or configure the a2a-wallet CLI.
compatibility: >
  Requires a2a-wallet CLI to be installed. macOS (Apple Silicon, Intel),
  Linux (x64, arm64), Windows (x64). See INSTALL.md for setup instructions.
metadata:
  author: planetarium
  repository: https://github.com/planetarium/a2a-x402-wallet
---

# a2a-wallet Skill

If a command fails with a "command not found" error, refer to **[INSTALL.md](./INSTALL.md)** in this directory and guide the user through installation.

## Commands

| Command | Description |
|---------|-------------|
| `a2a` | Interact with A2A agents (`card`, `send`, `stream`, `tasks`, `cancel`) |
| `x402 sign` | Sign x402 PaymentRequirements → PaymentPayload (for paywalled agents) |
| `siwe` | SIWE token operations (`prepare`, `encode`, `decode`, `verify`, `auth`) |
| `auth` | Log in / out (`login`, `device start/poll`, `logout`) |
| `config` | Get or set config values (`token`, `url`) |
| `whoami` | Show authenticated user info |
| `balance` | Show wallet balance |
| `sign` | Sign an arbitrary message with the wallet |
| `faucet` | Request testnet tokens |
| `update` | Update the CLI binary |

## Agent Card Extensions

Before interacting with an A2A agent, inspect its card to check which extensions are declared:

```bash
a2a-wallet a2a card https://my-agent.example.com
```

The `capabilities.extensions` array in the card lists supported (and possibly required) extensions. Two extensions are relevant to this CLI:

---

### x402 Payments Extension

**Extension URI**: `https://github.com/google-agentic-commerce/a2a-x402/blob/main/spec/v0.2`

Agents declaring this extension monetize their services via on-chain cryptocurrency payments. If `required: true`, the client **must** implement the x402 flow.

**How to detect**: The agent card will contain:

```json
{
  "capabilities": {
    "extensions": [
      {
        "uri": "https://github.com/google-agentic-commerce/a2a-x402/blob/main/spec/v0.2",
        "required": true
      }
    ]
  }
}
```

**Payment flow**:
1. Send a message → agent replies with `task.status = input-required` and `metadata["x402.payment.status"] = "payment-required"` plus `metadata["x402.payment.required"]` containing `PaymentRequirements`
2. Sign the requirements with `x402 sign`:
   ```bash
   METADATA=$(a2a-wallet x402 sign \
     --scheme exact \
     --network base \
     --asset <token-address> \
     --pay-to <merchant-address> \
     --amount <amount> \
     --extra-name <eip712-domain-name> \
     --extra-version <eip712-domain-version> \
     --json)
   ```
3. Submit payment by sending back with `--task-id` and `--metadata`:
   ```bash
   a2a-wallet a2a send \
     --task-id <task-id> \
     --metadata "$METADATA" \
     https://my-agent.example.com "Payment submitted"
   ```

---

### SIWE Bearer Auth Extension

**Extension URI**: `https://github.com/planetarium/a2a-x402-wallet/tree/main/docs/siwe-bearer-auth/v0.1`

Agents declaring this extension require a wallet-signed auth token on every request. If `required: true`, messages cannot be sent without one.

**How to detect**: The agent card will contain:

```json
{
  "extensions": [
    {
      "uri": "https://github.com/planetarium/a2a-x402-wallet/tree/main/docs/siwe-bearer-auth/v0.1",
      "required": true
    }
  ]
}
```

**Usage**:
1. Generate a token for the agent's domain:
   ```bash
   TOKEN=$(a2a-wallet siwe auth \
     --domain my-agent.example.com \
     --uri    https://my-agent.example.com \
     --ttl    1h \
     --json | jq -r '.token')
   ```
2. Pass it via `--bearer` when sending messages:
   ```bash
   a2a-wallet a2a send   --bearer "$TOKEN" https://my-agent.example.com "Hello"
   a2a-wallet a2a stream --bearer "$TOKEN" https://my-agent.example.com "Hello"
   ```

**Note**: The token is tied to the agent's domain — a token issued for one agent will be rejected by another.

---

## Agent usage tips

- Use `--json` for machine-readable output
- Errors → stderr, exit `0` = success, `1` = failure
- Override token/URL per-call with `--token` / `--url`, or set `A2A_WALLET_TOKEN` env var
- The CLI detects expired tokens before making network requests and prints guidance
- Always run `a2a card <url>` first to check which extensions are required before sending messages
- Use `a2a-wallet --help` or `a2a-wallet <command> --help` to discover options at any time
