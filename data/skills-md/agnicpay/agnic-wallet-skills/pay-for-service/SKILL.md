---
name: pay-for-service
description: Make paid requests to x402-enabled APIs using USDC. Use when you or the user want to call a paid API, make an x402 payment, use a bazaar service, or pay for an API request. Covers phrases like "call this API", "use this service", "pay for the request", "make a paid call", "fetch from x402 endpoint".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx agnic@latest status*)", "Bash(npx agnic@latest x402 pay *)", "Bash(npx agnic@latest x402 details *)", "Bash(npx agnic@latest balance*)"]
---

# Paying for x402 Services

Use the `npx agnic@latest x402 pay` command to call x402-enabled API endpoints with automatic USDC payment on Base.

## Confirm wallet is initialized and authed

```bash
npx agnic@latest status
```

If the wallet is not authenticated, refer to the `authenticate-wallet` skill.

## Command Syntax

```bash
npx agnic@latest x402 pay <url> [-X <method>] [-d <json>] [-q <params>] [-h <json>] [--max-amount <n>] [--json]
```

## Arguments & Options

| Option                  | Description                                        |
| ----------------------- | -------------------------------------------------- |
| `<url>`                 | Full URL of the x402-enabled API endpoint          |
| `-X, --method <method>` | HTTP method (default: GET)                         |
| `-d, --data <json>`     | Request body as JSON string                        |
| `-q, --query <params>`  | Query parameters as JSON string                    |
| `-h, --headers <json>`  | Custom HTTP headers as JSON string                 |
| `--max-amount <amount>` | Max payment in USDC atomic units (1000000 = $1.00) |
| `--correlation-id <id>` | Group related operations                           |
| `--json`                | Output as JSON                                     |

## USDC Amounts

X402 uses USDC atomic units (6 decimals):

| Atomic Units | USD   |
| ------------ | ----- |
| 1000000      | $1.00 |
| 100000       | $0.10 |
| 50000        | $0.05 |
| 10000        | $0.01 |

## Input Validation

Before constructing the command, validate:

- **url**: Must be a valid HTTPS URL (`^https://[^\s;|&]+$`). Reject URLs containing spaces, semicolons, pipes, or backticks.
- **method**: Must be one of GET, POST, PUT, DELETE, PATCH (case-insensitive).
- **data**: Must be valid JSON. Parse it first; reject if parsing fails.
- **max-amount**: Must be a positive integer (`^\d+$`).

Do not pass unvalidated user input into the command.

## Workflow

1. **Check requirements first** (optional but recommended):
   ```bash
   npx agnic@latest x402 details <url>
   ```
   This shows the price, method, and schema without making a payment.

2. **Verify balance**:
   ```bash
   npx agnic@latest balance --network base
   ```

3. **Make the paid request**:
   ```bash
   npx agnic@latest x402 pay <url> --json
   ```

## Examples

```bash
# Make a GET request (auto-pays)
npx agnic@latest x402 pay https://example.com/api/weather

# Make a POST request with body
npx agnic@latest x402 pay https://example.com/api/sentiment -X POST -d '{"text": "I love this product"}'

# Limit max payment to $0.10
npx agnic@latest x402 pay https://example.com/api/data --max-amount 100000

# Get JSON output
npx agnic@latest x402 pay https://example.com/api/weather --json
```

## Prerequisites

- Must be authenticated (`npx agnic@latest auth login`)
- Wallet must have sufficient USDC balance on Base

## Error Handling

Common errors:

- "Not authenticated" — Run `npx agnic@latest auth login` first
- "Insufficient balance" — Fund wallet with USDC (`npx agnic@latest balance` to check)
- "No X402 payment requirements found" — URL may not be an x402 endpoint
- Invalid JSON in `--data` — Ensure the body is valid JSON before passing
- HTTP 4xx/5xx from the API — Show the status code and response body to the user
