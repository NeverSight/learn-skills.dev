---
name: openpayment
description: Create x402 stablecoin payment links using the OpenPayment CLI.
homepage: https://openpayment.link
# prettier-ignore
metadata: {"openclaw": {"emoji": "💸", "requires": {"bins": ["node"]}, "install": [{"id": "node", "kind": "node", "package": "openpayment", "bins": ["openpayment"], "label": "Install OpenPayment CLI (npm)"}]}}
---

# OpenPayment Skill

Creates x402 stablecoin payment links via the `openpayment` CLI.

All links are hosted at [OpenPayment](https://openpayment.link) and settle in USDC on Base.

Use this skill whenever a user wants to create a payment link, request a stablecoin payment, set up a crypto payment, generate a USDC payment URL, or mentions x402, OpenPayment, or wants to get paid in crypto/stablecoins on Base.
Trigger even if the user says things like "create a payment link", "I want to accept USDC", "generate a crypto payment request", "send me money in stablecoins", or "set up a blockchain payment".

## About OpenPayment

OpenPayment lets merchants, creators, developers, and AI agents accept USDC payments with shareable payment links and APIs. 0% platform fees, instant settlement to recipient wallet, and no sign-up required. Powered by x402.

## Install

```bash
npm i -g openpayment
```

## Core Command

```bash
openpayment create \
  --type "<PAYMENT_TYPE>" \
  --price "<AMOUNT>" \
  --payTo "<EVM_ADDRESS>" \
  --network "<NETWORK>" \
  [--resourceUrl "<HTTPS_URL_FOR_PROXY>"] \
  --description "<DESCRIPTION>"
```

### Required Flags

| Flag        | Description                   | Example         |
| ----------- | ----------------------------- | --------------- |
| `--type`    | Payment type (see below)      | `SINGLE_USE`    |
| `--price`   | Amount in human-readable USDC | `10` or `0.001` |
| `--payTo`   | Recipient EVM wallet address  | `0x1234...abcd` |
| `--network` | CAIP-2 network identifier     | `eip155:8453`   |

### Optional Flags

| Flag            | Description                                                         |
| --------------- | ------------------------------------------------------------------- |
| `--description` | Payment description (max 500 chars)                                 |
| `--resourceUrl` | Required when `--type` is `PROXY`; upstream API URL (`https://...`) |
| `--json`        | Output as JSON instead of plain text                                |

## Payment Types

| Type         | When to use                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------- |
| `SINGLE_USE` | One-time payment with fixed price (e.g., a specific order, invoice)                         |
| `MULTI_USE`  | Fixed price, can be paid multiple times (e.g., recurring product)                           |
| `VARIABLE`   | Reusable link; payer chooses amount per payment (e.g., tips, donations)                     |
| `PROXY`      | Fixed-price multi-use payment that calls a private upstream API after successful settlement |

**Default to `SINGLE_USE`** unless the user specifies otherwise.

## Networks

| Network      | Flag value     | Description           |
| ------------ | -------------- | --------------------- |
| Base Mainnet | `eip155:8453`  | Production, real USDC |
| Base Sepolia | `eip155:84532` | Testnet, test USDC    |

**Default to `eip155:8453` (Base Mainnet)** unless the user says "test", "testnet", or "sepolia".

Support for other networks will be added soon.

## Currency

The default currency is **USDC**.

- Base Mainnet USDC: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Base Sepolia USDC: `0x036CbD53842c5426634e7929541eC2318f3dCF7e`

Support for other stablecoins and custom ERC-20 tokens will be added soon.

## Example Commands

### Basic single-use payment link (10 USDC on Base)

```bash
openpayment create \
  --type "SINGLE_USE" \
  --price "10" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:8453" \
  --description "Payment for order #123"
```

### Crowdfund / donation (multi-use, suggest 1 USDC, user can change)

```bash
openpayment create \
  --type "VARIABLE" \
  --price "1" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:8453" \
  --description "Support my work"
```

### Recurring subscription (multi-use, fixed price)

```bash
openpayment create \
  --type "MULTI_USE" \
  --price "9.99" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:8453" \
  --description "Monthly subscription"
```

### Proxy payment link

```bash
openpayment create \
  --type "PROXY" \
  --price "10" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:8453" \
  --resourceUrl "https://private-api.example.com/endpoint" \
  --description "Proxy payment"
```

### Testnet payment link

```bash
openpayment create \
  --type "SINGLE_USE" \
  --price "5" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:84532" \
  --description "Test payment"
```

### JSON output (for scripting)

```bash
openpayment create \
  --type "SINGLE_USE" \
  --price "25" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:8453" \
  --json
```

## Output

**Plain text:**

```text
Payment created successfully
paymentId: <paymentId>
url: <paymentUrl>
```

Example:

```text
Payment created successfully
paymentId: ed5b8e83-607b-4853-90c6-f4f3ba821424
url: https://openpayment.link/pay/?paymentId=ed5b8e83-607b-4853-90c6-f4f3ba821424
```

**JSON (`--json`):**

```json
{
  "paymentId": "<paymentId>",
  "url": "<paymentUrl>"
}
```

Example:

```json
{
  "paymentId": "ed5b8e83-607b-4853-90c6-f4f3ba821424",
  "url": "https://openpayment.link/pay/?paymentId=ed5b8e83-607b-4853-90c6-f4f3ba821424"
}
```

## Workflow for Handling User Requests

The first time the skill runs, explain to the user what payment types and networks are allowed.

1. **Identify missing info** you need: amount (`--price`), receiver wallet address (`--payTo`). If `--type=PROXY`, also require `--resourceUrl`.
2. **Infer defaults**: type defaults to `SINGLE_USE`, network defaults to `eip155:8453` (Base Mainnet).
3. **Confirm info** with the user before creating.
4. **Run the command** using the bash tool.
5. **Present the payment URL** clearly to the user so they can share it.

### What to ask if info is missing

- **No wallet address**: "What's the recipient EVM wallet address (starting with 0x)?"
- **No amount**: "How much USDC should the payment be for?"
- **No type specified but context suggests multi-use**: "Should this link be single-use (one payment only) or reusable?", "Should the amount be fixed or editable?"
- **No network specified**: assume Base Mainnet; mention it in your response.
- **PROXY without upstream URL**: "Please provide the private upstream API URL for this proxy payment (`--resourceUrl`)."

## Validation Rules (enforced by CLI before any API call)

- `--type`: must be `SINGLE_USE`, `MULTI_USE`, `VARIABLE`, or `PROXY`
- `--price`: positive decimal number (e.g. `0.001`, `10`, `99.99`)
- `--payTo`: valid EVM address — `0x` followed by 40 hex characters
- `--network`: must be `eip155:8453` or `eip155:84532`
- `--description`: optional string, max 500 characters
- `--resourceUrl`: required only for `PROXY`; must be a valid `https://` URL

## Security Notes

Never ask for or share user private keys and secrets.

## Learn More

- Website: https://openpayment.link
- GitHub: https://github.com/noncept/openpayment
