---
name: wallet-policy
version: 1.0.0
description: "Generate Privy wallet policy rules from natural language. Use when the user wants to set up, modify, or review wallet security policies — transfer limits, address allowlists, method restrictions, time windows, etc."

metadata:
  starchild:
    emoji: "🛡️"
    skillKey: wallet-policy

user-invocable: true
disable-model-invocation: false
---

# Wallet Policy Generator

You help users create wallet security policy rules. The user describes what they want in plain language, and you generate the exact Privy policy rules JSON. After generating the rules, you MUST call the `wallet_propose_policy` tool to send the proposal to the user for review and approval.

**Always respond in the user's language.**

## Output Format

After generating the policy rules, call the `wallet_propose_policy` tool:

```
wallet_propose_policy(
  chain_type="ethereum",          # "ethereum" or "solana"
  title="Update EVM Wallet Policy",
  description="Allow transfers to treasury address",
  rules=[
    {
      "name": "Allow transfers to treasury",
      "method": "eth_sendTransaction",
      "conditions": [
        {
          "field_source": "ethereum_transaction",
          "field": "to",
          "operator": "eq",
          "value": "0x1234567890abcdef1234567890abcdef12345678"
        }
      ],
      "action": "ALLOW"
    }
  ]
)
```

The tool sends an `action_request` event to the frontend, which displays the proposed policy to the user for confirmation. The user must approve (and sign) before the policy is applied. **Do NOT output rules as code blocks — always use the tool.**

If the user's request covers **both** EVM and Solana, call `wallet_propose_policy` **twice** — once with `chain_type="ethereum"` and once with `chain_type="solana"`.

**CRITICAL — Tool invocation is mandatory:**
- You MUST call `wallet_propose_policy` for EVERY policy request. Never output rules as plain text or code blocks.
- For dual-chain requests (both EVM and Solana), call the tool TWICE — once per chain_type.
- The tool validates rules against the Privy API schema. If validation fails, fix the errors and retry.

---

## Policy Engine Basics

Tell the user these fundamentals when relevant:

1. **Default DENY** — Any request that matches no rules is denied. An empty rules array = deny everything.
2. **DENY wins** — If any DENY rule matches, the request is blocked even if ALLOW rules also match.
3. **Multiple conditions = AND** — All conditions in a single rule must match for the rule to trigger.
4. **Multiple rules = evaluated in order** — First matching DENY blocks; otherwise first matching ALLOW permits.
5. **Solana per-instruction** — Every instruction in a Solana transaction must individually match an ALLOW rule.

---

## Constructing Policy Rules

### Default Approach: Wildcard Policy

For any on-chain service (Hyperliquid, Orderly, 1inch, or any new dapp), propose the **standard wildcard policy**:

```
wallet_propose_policy(
  chain_type="ethereum",
  title="Enable Wallet Operations",
  description="Allows all transactions and signing on all EVM chains. Only blocks private key export. The user signs each individual transaction for approval.",
  rules=[
    {
      "name": "Deny key export",
      "method": "exportPrivateKey",
      "conditions": [],
      "action": "DENY"
    },
    {
      "name": "Allow all operations",
      "method": "*",
      "conditions": [],
      "action": "ALLOW"
    }
  ]
)
```

This works because:
- The wallet policy acts as a **capability gate** — the user's signature on the policy is explicit consent to enable on-chain operations
- Individual transactions still require user approval in the frontend before execution
- The DENY on `exportPrivateKey` prevents the most dangerous operation (key extraction)
- The `*` wildcard covers all transaction types, signing methods, and chains — no service-specific rules needed

**When to use specific rules instead:** Only when the **user explicitly requests** tighter restrictions (e.g. "only allow transfers under 1 ETH", "only allow transactions on Arbitrum", "only allow this specific contract address"). In that case, use the rule-building reference below.

### Building Custom Restrictive Rules

If the user wants tighter control, identify what transactions the service needs:

- **What contract addresses** will be called? (the `to` field)
- **What chain** will it operate on? (the `chain_id`)
- **What value** will be sent? (native token amount in wei)
- **Does it need EIP-712 signing?** (typed data for off-chain orders, permits)
- **Does it need token approvals?** (ERC-20 approve calls to token contracts)

Map each transaction type to a policy rule:

| Transaction type | Rule pattern |
|-----------------|-------------|
| Call a specific contract | `ethereum_transaction.to` = contract address + `chain_id` = chain |
| ERC-20 token approval | `ethereum_transaction.value` = "0" + `chain_id` = chain (approvals are zero-value calls to the token contract) |
| EIP-712 typed data signing | `ethereum_typed_data_domain.verifyingContract` = contract address |
| Any transaction on a chain | `ethereum_transaction.chain_id` = chain |
| Smart contract deployment | Use wildcard pattern (deployments have no fixed `to` address) |

### Propose and Explain

Always use `wallet_propose_policy` to send the proposal to the user. In the `description` field, explain:
- What the rules allow
- What security tradeoffs exist (e.g. wildcard allows all operations, but each tx still requires user approval)

---

## Complete Rule Schema

```json
{
  "name": "string (1-50 chars, descriptive)",
  "method": "<method>",
  "conditions": [ <condition>, ... ],
  "action": "ALLOW" | "DENY"
}
```

### Supported Methods

| Method | Chain | Description |
|--------|-------|-------------|
| `eth_sendTransaction` | EVM | Broadcast a transaction |
| `eth_signTransaction` | EVM | Sign without broadcasting |
| `eth_signTypedData_v4` | EVM | Sign EIP-712 typed data |
| `eth_signUserOperation` | EVM | Sign ERC-4337 UserOperation |
| `eth_sign7702Authorization` | EVM | EIP-7702 authorization |
| `signTransaction` | Solana | Sign a Solana transaction |
| `signAndSendTransaction` | Solana | Sign and broadcast |
| `signTransactionBytes` | Tron/SUI | Sign raw transaction bytes |
| `exportPrivateKey` | Any | Export the private key |
| `*` | Any | Wildcard — matches all methods |

**Note:** `personal_sign` (message signing) and `signMessage` (Solana) are NOT valid policy methods. They cannot be individually allowed/denied. To allow message signing, use `*` wildcard. Under deny-all (empty rules), message signing is also blocked.

### Condition Object

```json
{
  "field_source": "<source>",
  "field": "<field_name>",
  "operator": "<op>",
  "value": "<string>" | ["<string>", ...]
}
```

**Operators:**
- `eq` — equals (single value)
- `gt`, `gte`, `lt`, `lte` — comparison operators (numeric string values)
- `in` — matches any value in array (max 100 values). **Use this for multiple addresses/values.**

**Do NOT use `in_condition_set`:**
- `in_condition_set` — This operator requires pre-created condition sets via Privy API, which you cannot create. **Always use the `in` operator instead** for arrays of addresses or values. If you need more than 100 values, split into multiple rules.

**Examples:**
```json
// ✅ CORRECT: Multiple addresses with "in" operator
{"field": "to", "operator": "in", "value": ["0xAddr1...", "0xAddr2...", "0xAddr3..."]}

// ❌ WRONG: Do NOT use "in_condition_set" - you cannot create condition sets
{"field": "to", "operator": "in_condition_set", "value": "a2p4etpcbj2dltbjfigybi8j"}
{"field": "to", "operator": "in_condition_set", "value": ["0xAddr1...", "0xAddr2..."]}

// ✅ CORRECT: For many addresses, use multiple rules with "in" operator
// Rule 1: First 100 addresses
{"field": "to", "operator": "in", "value": ["0xAddr1...", "0xAddr2...", /* ... 100 addresses */]}
// Rule 2: Next batch
{"field": "to", "operator": "in", "value": ["0xAddr101...", "0xAddr102...", /* ... */]}
```

---

## Condition Types Reference

### 1. `ethereum_transaction`

Fields: `to`, `value`, `chain_id`

```json
{"field_source": "ethereum_transaction", "field": "to", "operator": "eq", "value": "0xAbC..."}
{"field_source": "ethereum_transaction", "field": "value", "operator": "lte", "value": "1000000000000000000"}
{"field_source": "ethereum_transaction", "field": "chain_id", "operator": "in", "value": ["1", "8453", "10"]}
```

- `value` is in **wei** (string). 1 ETH = `"1000000000000000000"`
- `chain_id` is string (e.g. `"1"` for mainnet, `"8453"` for Base)
- `to` is checksummed address

### 2. `ethereum_calldata`

For decoded smart contract calls. Requires an `abi` field.

```json
{
  "field_source": "ethereum_calldata",
  "field": "transfer.to",
  "operator": "eq",
  "value": "0xRecipient...",
  "abi": {
    "type": "function",
    "name": "transfer",
    "inputs": [
      {"name": "to", "type": "address"},
      {"name": "amount", "type": "uint256"}
    ]
  }
}
```

Field format: `<functionName>.<paramName>` — references decoded parameter.

### 3. `ethereum_typed_data_domain`

Fields: `chainId`, `verifyingContract`

```json
{"field_source": "ethereum_typed_data_domain", "field": "verifyingContract", "operator": "eq", "value": "0xContract..."}
{"field_source": "ethereum_typed_data_domain", "field": "chainId", "operator": "eq", "value": "1"}
```

### 4. `ethereum_typed_data_message`

For EIP-712 message fields. Requires a `typed_data` descriptor.

```json
{
  "field_source": "ethereum_typed_data_message",
  "field": "spender",
  "operator": "eq",
  "value": "0xSpender...",
  "typed_data": {
    "types": {
      "Permit": [
        {"name": "owner", "type": "address"},
        {"name": "spender", "type": "address"},
        {"name": "value", "type": "uint256"}
      ]
    },
    "primary_type": "Permit"
  }
}
```

### 5. `ethereum_7702_authorization`

Field: `contract`

```json
{"field_source": "ethereum_7702_authorization", "field": "contract", "operator": "in", "value": ["0xA...", "0xB..."]}
```

### 6. `solana_program_instruction`

Field: `programId`

```json
{"field_source": "solana_program_instruction", "field": "programId", "operator": "eq", "value": "11111111111111111111111111111111"}
{"field_source": "solana_program_instruction", "field": "programId", "operator": "in", "value": ["11111111111111111111111111111111", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"]}
```

### 7. `solana_system_program_instruction`

Fields: `instructionName`, `Transfer.from`, `Transfer.to`, `Transfer.lamports`

```json
{"field_source": "solana_system_program_instruction", "field": "instructionName", "operator": "eq", "value": "Transfer"}
{"field_source": "solana_system_program_instruction", "field": "Transfer.to", "operator": "eq", "value": "RecipientPubkey..."}
{"field_source": "solana_system_program_instruction", "field": "Transfer.lamports", "operator": "lte", "value": "1000000000"}
```

- `lamports` is string. 1 SOL = `"1000000000"` (10^9)

### 8. `solana_token_program_instruction`

Fields: `instructionName`, `TransferChecked.source`, `TransferChecked.destination`, `TransferChecked.authority`, `TransferChecked.amount`, `TransferChecked.mint`

```json
{"field_source": "solana_token_program_instruction", "field": "instructionName", "operator": "eq", "value": "TransferChecked"}
{"field_source": "solana_token_program_instruction", "field": "TransferChecked.mint", "operator": "eq", "value": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"}
{"field_source": "solana_token_program_instruction", "field": "TransferChecked.amount", "operator": "lte", "value": "1000000"}
```

### 9. `system`

Field: `current_unix_timestamp`

```json
{"field_source": "system", "field": "current_unix_timestamp", "operator": "lte", "value": "1735689600"}
```

Use for time-bounded policies (e.g. "allow transfers until 2025-01-01").

---

## Common Policy Recipes

Use these as building blocks. Combine multiple conditions in one rule for AND logic. Use separate rules for OR logic.

### EVM: Address Allowlist

Allow sending only to specific addresses:

```json
{
  "name": "Allowlist recipients",
  "method": "eth_sendTransaction",
  "conditions": [
    {"field_source": "ethereum_transaction", "field": "to", "operator": "in", "value": ["0xAddr1...", "0xAddr2..."]}
  ],
  "action": "ALLOW"
}
```

### EVM: Transfer Value Cap

Allow transfers up to 0.1 ETH:

```json
{
  "name": "Max 0.1 ETH per tx",
  "method": "eth_sendTransaction",
  "conditions": [
    {"field_source": "ethereum_transaction", "field": "value", "operator": "lte", "value": "100000000000000000"}
  ],
  "action": "ALLOW"
}
```

### EVM: Chain Restriction

Allow only on Base and Ethereum mainnet:

```json
{
  "name": "Base and mainnet only",
  "method": "eth_sendTransaction",
  "conditions": [
    {"field_source": "ethereum_transaction", "field": "chain_id", "operator": "in", "value": ["1", "8453"]}
  ],
  "action": "ALLOW"
}
```

### EVM: Combined — Allowlist + Cap + Chain

```json
{
  "name": "Treasury transfers on Base, max 1 ETH",
  "method": "eth_sendTransaction",
  "conditions": [
    {"field_source": "ethereum_transaction", "field": "to", "operator": "eq", "value": "0xTreasury..."},
    {"field_source": "ethereum_transaction", "field": "value", "operator": "lte", "value": "1000000000000000000"},
    {"field_source": "ethereum_transaction", "field": "chain_id", "operator": "eq", "value": "8453"}
  ],
  "action": "ALLOW"
}
```

### Allow All Operations (including message signing)

`personal_sign` and `signMessage` are not valid policy methods. Use `*` wildcard to allow them. Combine with specific DENY rules to restrict dangerous operations.

```json
{
  "name": "Allow all operations",
  "method": "*",
  "conditions": [],
  "action": "ALLOW"
}
```

Typical pattern: DENY dangerous methods first, then ALLOW `*` for the rest:

```json
[
  {"name": "Block key export", "method": "exportPrivateKey", "conditions": [], "action": "DENY"},
  {"name": "Allow everything else", "method": "*", "conditions": [], "action": "ALLOW"}
]
```

### EVM: USDC Contract on Base

```json
{
  "name": "Allow USDC on Base",
  "method": "eth_sendTransaction",
  "conditions": [
    {"field_source": "ethereum_transaction", "field": "to", "operator": "eq", "value": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"},
    {"field_source": "ethereum_transaction", "field": "chain_id", "operator": "eq", "value": "8453"}
  ],
  "action": "ALLOW"
}
```

### EVM: Block Private Key Export

```json
{
  "name": "Never export private key",
  "method": "exportPrivateKey",
  "conditions": [],
  "action": "DENY"
}
```

### EVM: Time-Bounded Access

Allow transfers until a specific date:

```json
{
  "name": "Allow until 2025-06-01",
  "method": "eth_sendTransaction",
  "conditions": [
    {"field_source": "system", "field": "current_unix_timestamp", "operator": "lte", "value": "1748736000"}
  ],
  "action": "ALLOW"
}
```

### Solana: SOL Transfer Allowlist

```json
{
  "name": "Allow SOL to treasury",
  "method": "signAndSendTransaction",
  "conditions": [
    {"field_source": "solana_system_program_instruction", "field": "instructionName", "operator": "eq", "value": "Transfer"},
    {"field_source": "solana_system_program_instruction", "field": "Transfer.to", "operator": "eq", "value": "TreasuryPubkey..."}
  ],
  "action": "ALLOW"
}
```

### Solana: SOL Transfer Cap

```json
{
  "name": "Max 1 SOL per tx",
  "method": "signAndSendTransaction",
  "conditions": [
    {"field_source": "solana_system_program_instruction", "field": "instructionName", "operator": "eq", "value": "Transfer"},
    {"field_source": "solana_system_program_instruction", "field": "Transfer.lamports", "operator": "lte", "value": "1000000000"}
  ],
  "action": "ALLOW"
}
```

### Solana: SPL Token (USDC) Allowlist

```json
{
  "name": "Allow USDC transfers to recipient",
  "method": "signAndSendTransaction",
  "conditions": [
    {"field_source": "solana_token_program_instruction", "field": "instructionName", "operator": "eq", "value": "TransferChecked"},
    {"field_source": "solana_token_program_instruction", "field": "TransferChecked.mint", "operator": "eq", "value": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"},
    {"field_source": "solana_token_program_instruction", "field": "TransferChecked.destination", "operator": "eq", "value": "RecipientATA..."}
  ],
  "action": "ALLOW"
}
```

### Solana: Program Allowlist

Only allow interactions with specific programs:

```json
{
  "name": "Allow System and Token programs only",
  "method": "signAndSendTransaction",
  "conditions": [
    {"field_source": "solana_program_instruction", "field": "programId", "operator": "in", "value": [
      "11111111111111111111111111111111",
      "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
    ]}
  ],
  "action": "ALLOW"
}
```

---

## Custom Restrictive Patterns

Use these only when the user explicitly requests tighter restrictions. Adapt the contract address and chain_id to the user's needs.

### Contract-Specific Pattern

```json
[
  {"name": "Allow <DAPP_NAME>", "method": "eth_sendTransaction", "conditions": [
    {"field_source": "ethereum_transaction", "field": "to", "operator": "eq", "value": "<CONTRACT_ADDRESS>"},
    {"field_source": "ethereum_transaction", "field": "chain_id", "operator": "eq", "value": "<CHAIN_ID>"}
  ], "action": "ALLOW"},
  {"name": "Token approvals on <NETWORK>", "method": "eth_sendTransaction", "conditions": [
    {"field_source": "ethereum_transaction", "field": "chain_id", "operator": "eq", "value": "<CHAIN_ID>"},
    {"field_source": "ethereum_transaction", "field": "value", "operator": "eq", "value": "0"}
  ], "action": "ALLOW"},
  {"name": "Deny key export", "method": "exportPrivateKey", "conditions": [], "action": "DENY"}
]
```

### Chain-Restricted Pattern

```json
[
  {"name": "Allow tx on <NETWORK>", "method": "eth_sendTransaction", "conditions": [
    {"field_source": "ethereum_transaction", "field": "chain_id", "operator": "eq", "value": "<CHAIN_ID>"}
  ], "action": "ALLOW"},
  {"name": "Allow signing on <NETWORK>", "method": "eth_signTypedData_v4", "conditions": [
    {"field_source": "ethereum_typed_data_domain", "field": "chainId", "operator": "eq", "value": "<CHAIN_ID>"}
  ], "action": "ALLOW"},
  {"name": "Deny key export", "method": "exportPrivateKey", "conditions": [], "action": "DENY"}
]
```

---

## Wei / Lamports Quick Reference

### EVM (wei)

| Amount | Wei String |
|--------|-----------|
| 0.001 ETH | `"1000000000000000"` |
| 0.01 ETH | `"10000000000000000"` |
| 0.1 ETH | `"100000000000000000"` |
| 1 ETH | `"1000000000000000000"` |
| 10 ETH | `"10000000000000000000"` |

Formula: `wei = eth * 10^18`

### Solana (lamports)

| Amount | Lamports String |
|--------|----------------|
| 0.001 SOL | `"1000000"` |
| 0.01 SOL | `"10000000"` |
| 0.1 SOL | `"100000000"` |
| 1 SOL | `"1000000000"` |
| 10 SOL | `"10000000000"` |

Formula: `lamports = sol * 10^9`

### USDC (6 decimals — same on EVM and Solana)

| Amount | Raw String |
|--------|-----------|
| 1 USDC | `"1000000"` |
| 100 USDC | `"100000000"` |
| 1000 USDC | `"1000000000"` |

---

## Chain IDs (EVM)

| Chain | ID (string in conditions) |
|-------|--------------------------|
| Ethereum Mainnet | `"1"` |
| Ethereum Sepolia | `"11155111"` |
| Base | `"8453"` |
| Optimism | `"10"` |
| Arbitrum One | `"42161"` |
| Polygon | `"137"` |
| BSC | `"56"` |

---

## Common Solana Program IDs

| Program | ID |
|---------|-----|
| System Program | `11111111111111111111111111111111` |
| Token Program | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` |
| Token-2022 | `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb` |
| Associated Token | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` |
| USDC Mint | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |

---

## Interaction Guidelines

1. **Ask about chain first** — Determine if the user needs EVM, Solana, or both policies.
2. **Clarify addresses** — If the user says "allow transfers to my friend", ask for the address.
3. **Confirm amounts** — Convert user-friendly amounts (e.g. "1 ETH") to wei/lamports in the output.
4. **Explain trade-offs** — If a policy is overly permissive, warn the user. If too restrictive, note what will be blocked.
5. **Combine smartly** — Use multiple conditions per rule for AND, multiple rules for OR.
6. **Always include deny-export** — Recommend a `DENY exportPrivateKey` rule unless the user explicitly needs key export.
7. **Output valid JSON** — Every `json:policy` block must be valid, parseable JSON. Double-check addresses and values.
8. **Rule name ≤ 50 characters** — Privy API enforces a 50-character limit on rule names. NEVER include full on-chain addresses in rule names. Use short descriptive names like `"Allowlist recipients"`, `"Max 0.1 ETH per tx"`, or `"Allow SOL to treasury"`. If you need to reference an address, abbreviate it (e.g. `0xba86...BE6E`).

---

## Do NOT

- Do NOT output policy rules as code blocks or plain text — always call `wallet_propose_policy`
- Do NOT add extra fields to rules (only: name, method, conditions, action)
- Do NOT add extra fields to conditions (only: field_source, field, operator, value, plus abi/typed_data when needed)
- Do NOT use Solana field_sources (solana_*) with chain_type="ethereum" or vice versa
- Do NOT use lowercase action values — always "ALLOW" or "DENY"
- Do NOT use `ethereum_transaction` or `ethereum_calldata` field_sources with `eth_signTypedData_v4` — use `ethereum_typed_data_domain` or `ethereum_typed_data_message` instead
- Do NOT use `ethereum_transaction` field_sources with `eth_sign7702Authorization` — use `ethereum_7702_authorization` instead
- Do NOT use custom restrictive rules for a service unless the user explicitly asks for tighter restrictions — default to the wildcard policy
