---
name: wallet
version: 1.0.0
description: Multi-chain wallet operations - balance, transfers, signing, and transaction history via Privy Server Wallets (EVM + Solana)
tools:
  - wallet_info
  - wallet_transfer
  - wallet_sign_transaction
  - wallet_sign
  - wallet_sign_typed_data
  - wallet_balance
  - wallet_get_all_balances
  - wallet_transactions
  - wallet_sol_transfer
  - wallet_sol_sign_transaction
  - wallet_sol_sign
  - wallet_sol_balance
  - wallet_sol_transactions
  - wallet_propose_policy

metadata:
  starchild:
    emoji: "💰"
    skillKey: wallet
    requires:
      env: [WALLET_SERVICE_URL]

user-invocable: true
disable-model-invocation: false
---

# Wallet

Interact with this agent's on-chain wallets. Each agent has one wallet per chain (EVM + Solana). Supports balance queries, transfers (policy-gated), message signing, and transaction history.

Authentication is automatic via Fly OIDC token — no API keys or wallet addresses needed. Wallets are bound to this machine at deploy time.

## Available Tools (13)

### Multi-Chain Tools

| Tool | Description |
|------|-------------|
| `wallet_info` | Get all wallet addresses and chain types |
| `wallet_get_all_balances` | **PRIMARY TOOL** - Get complete portfolio across ALL chains (EVM + Solana) with USD values |

### EVM Tools

| Tool | Description |
|------|-------------|
| `wallet_balance` | Get ETH/token balances on a specific chain (requires `chain` parameter) |
| `wallet_transactions` | Get recent EVM transaction history |
| `wallet_transfer` | Sign and broadcast a transaction on-chain (policy-gated). Funds leave the wallet. |
| `wallet_sign_transaction` | Sign a transaction WITHOUT broadcasting (returns RLP-encoded signed tx, nothing sent on-chain) |
| `wallet_sign` | Sign a message (EIP-191 personal_sign) |
| `wallet_sign_typed_data` | Sign EIP-712 structured data (permits, orders, etc.) |

### Solana Tools

| Tool | Description |
|------|-------------|
| `wallet_sol_balance` | Get SOL/SPL token balances with USD values |
| `wallet_sol_transactions` | Get recent Solana transaction history |
| `wallet_sol_transfer` | Sign and broadcast a Solana transaction on-chain (policy-gated). Funds leave the wallet. |
| `wallet_sol_sign_transaction` | Sign a Solana transaction WITHOUT broadcasting (returns base64 signed tx, nothing sent on-chain) |
| `wallet_sol_sign` | Sign a message with the Solana wallet |

---

## Tool Usage Examples

### Check Wallet Info (All Chains)

```
wallet_info()
```

Returns: list of `wallets` with `wallet_address` and `chain_type` for each active wallet.

Use this first to see all available wallets before any operations.

### EVM — Check Balance

**IMPORTANT: Always specify the `chain` parameter! To check all chains at once, use `wallet_get_all_balances` instead.**

```
wallet_balance(chain="ethereum")  # Get ALL tokens on Ethereum
wallet_balance(chain="base", asset="usdc")  # Check specific asset on Base
wallet_balance(chain="polygon", asset="pol")  # Polygon requires explicit asset
```

**chain parameter is REQUIRED.** Valid chains: `ethereum`, `base`, `arbitrum`, `optimism`, `polygon`, `linea`

**Asset naming:**
- For Polygon native token, use `"pol"` NOT `"matic"`
- Use lowercase symbolic names like `"usdc"`, `"weth"`, `"usdt"`
- DO NOT pass contract addresses (e.g., `"0x..."`), use symbols only
- Omit `asset` parameter to discover ALL tokens on the specified chain

**Known Limitation - Polygon:**
The Polygon chain requires explicit asset parameters. Instead of:
```
wallet_balance(chain="polygon")  # ❌ May fail with "eth not supported"
```

Use:
```
wallet_balance(chain="polygon", asset="pol")  # ✅ Check POL balance
wallet_balance(chain="polygon", asset="usdc")  # ✅ Check USDC balance
```

For complete Polygon portfolio, use `wallet_get_all_balances()` which handles this correctly.

For checking balances across ALL chains in one call, use `wallet_get_all_balances()` instead.

### Multi-Chain — Get All Balances

```
wallet_get_all_balances()
```

**This is the PRIMARY tool for comprehensive balance checks.**

Automatically checks ALL supported chains (Ethereum, Base, Arbitrum, Optimism, Polygon, Linea, Solana) and returns complete portfolio with USD values.

Use this instead of calling `wallet_balance()` multiple times for different chains.

### EVM — Query Transaction History

```
wallet_transactions()
wallet_transactions(chain="ethereum", asset="eth", limit=10)
wallet_transactions(limit=50)
```

Defaults: `chain="ethereum"`, `asset="eth"`, `limit=20` (max 100).

Returns: list of transactions with `tx_hash`, `from`, `to`, `amount`, `status`, `timestamp`.

### EVM — Transfer Funds / Contract Calls

```
wallet_transfer(to="0xRecipientAddress", amount="1000000000000000000")
wallet_transfer(to="0xRecipientAddress", amount="1000000000000000000", chain_id=8453)
wallet_transfer(to="0xContractAddress", amount="0", data="0xa9059cbb000000...", chain_id=8453)
```

- `to`: Target wallet or contract address (0x...)
- `amount`: Amount in **wei** (not ETH). `"1000000000000000000"` = 1 ETH. Use `"0"` for contract calls that don't send ETH.
- `chain_id`: Chain ID (default: 1 = Ethereum mainnet, 8453 = Base, 10 = Optimism)
- `data`: Hex-encoded calldata for contract calls (e.g. ERC-20 transfer, swap). Optional — omit for simple ETH transfers.
- `gas_limit`: Gas limit (decimal string). Optional — Privy estimates if omitted.
- `gas_price`: Gas price in wei (decimal string, for legacy transactions). Optional.
- `max_fee_per_gas`: Max fee per gas in wei (decimal string, for EIP-1559 transactions). Optional.
- `max_priority_fee_per_gas`: Max priority fee in wei (decimal string, for EIP-1559 transactions). Optional.
- `nonce`: Transaction nonce (decimal string). Optional — auto-determined if omitted.
- `tx_type`: Transaction type integer. `0`=legacy, `1`=EIP-2930, `2`=EIP-1559, `4`=EIP-7702. Optional.

**Policy enforcement**: Transfers are gated by Privy TEE policy. The target address must be on the whitelist and the amount must be within daily limits. Policy violations return an error.

### EVM — Sign Transaction (without broadcasting)

```
wallet_sign_transaction(to="0xRecipientAddress", amount="1000000000000000000")
wallet_sign_transaction(to="0xRecipientAddress", amount="1000000000000000000", chain_id=8453)
wallet_sign_transaction(to="0xContractAddress", amount="0", data="0xa9059cbb000000...", chain_id=8453, tx_type=2, max_fee_per_gas="30000000000", max_priority_fee_per_gas="2000000000")
```

Same parameters as `wallet_transfer`, plus `max_fee_per_gas` and `max_priority_fee_per_gas` for EIP-1559.

Returns: `signed_transaction` (RLP-encoded hex), `encoding` ("rlp")

Use cases: pre-sign transactions for later submission, multi-step flows, external broadcast.

### EVM — Sign a Message

```
wallet_sign(message="Hello World")
wallet_sign(message="Verify ownership of this wallet")
```

Returns: `signature` (EIP-191 personal_sign format)

Use cases: prove wallet ownership, sign off-chain messages, create verifiable attestations.

### EVM — Sign EIP-712 Typed Data

```
wallet_sign_typed_data(
  domain={"name": "MyDApp", "version": "1", "chainId": 1, "verifyingContract": "0x..."},
  types={"Person": [{"name": "name", "type": "string"}, {"name": "wallet", "type": "address"}]},
  primaryType="Person",
  message={"name": "Alice", "wallet": "0x..."}
)
```

- `domain`: EIP-712 domain separator (name, version, chainId, verifyingContract)
- `types`: Type definitions — mapping of type name to array of `{name, type}` fields
- `primaryType`: The primary type being signed (must exist in `types`)
- `message`: The structured data to sign (must match `primaryType` schema)

Returns: `signature` (hex)

Use cases: EIP-2612 permit approvals, off-chain order signing (Seaport, 0x), gasless approvals, structured attestations.

### Solana — Check Balance

```
wallet_sol_balance()
wallet_sol_balance(chain="solana", asset="sol")
```

All parameters are optional. Returns balances with USD-equivalent values.

### Solana — Query Transaction History

```
wallet_sol_transactions()
wallet_sol_transactions(chain="solana", asset="sol", limit=10)
```

Defaults: `chain="solana"`, `asset="sol"`, `limit=20` (max 100).

### Solana — Sign and Send Transaction

```
wallet_sol_transfer(transaction="<base64-encoded-transaction>")
wallet_sol_transfer(transaction="<base64-encoded-transaction>", caip2="solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1")
```

- `transaction`: Base64-encoded serialized Solana transaction
- `caip2`: CAIP-2 chain identifier (default: `"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"` for mainnet, use `"solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1"` for devnet)

**Policy enforcement**: Same as EVM — transfers are gated by Privy TEE policy.

### Solana — Sign Transaction (without broadcasting)

```
wallet_sol_sign_transaction(transaction="<base64-encoded-transaction>")
```

- `transaction`: Base64-encoded serialized Solana transaction

Returns: `signed_transaction` (base64), `encoding` ("base64")

Use cases: pre-sign transactions for later submission, multi-step flows, external broadcast.

### Solana — Sign a Message

```
wallet_sol_sign(message="<base64-encoded-message>")
```

Returns: `signature` (base64)

---

## Common Workflows

### Pre-Transfer Check (EVM)

1. `wallet_info()` — Confirm wallets are active
2. `wallet_balance(chain="ethereum")` — Check available funds on specific chain (or use `wallet_get_all_balances()`)
3. `wallet_transfer(to="0x...", amount="...")` — Execute transfer
4. `wallet_transactions(limit=1)` — Confirm transaction status

### Pre-Transfer Check (Solana)

1. `wallet_info()` — Confirm wallets are active
2. `wallet_sol_balance()` — Check available SOL funds
3. `wallet_sol_transfer(transaction="...")` — Sign and send transaction
4. `wallet_sol_transactions(limit=1)` — Confirm transaction status

### Monitor All Wallet Activity

1. `wallet_info()` — See all wallets
2. `wallet_get_all_balances()` — Complete portfolio across ALL chains (EVM + Solana)
3. `wallet_transactions(limit=20)` — Recent EVM activity
4. `wallet_sol_transactions(limit=20)` — Recent Solana activity

### Prove Wallet Ownership

1. `wallet_info()` — Get all wallet addresses
2. `wallet_sign(message="I am the owner of this wallet at timestamp 1234567890")` — EVM proof
3. `wallet_sol_sign(message="<base64-encoded-message>")` — Solana proof

---

## Wei Conversion Reference (EVM)

Amounts are always in **wei** (smallest unit). Conversion table:

| Amount | Wei String |
|--------|-----------|
| 0.001 ETH | `"1000000000000000"` |
| 0.01 ETH | `"10000000000000000"` |
| 0.1 ETH | `"100000000000000000"` |
| 1 ETH | `"1000000000000000000"` |
| 10 ETH | `"10000000000000000000"` |

Formula: `wei = eth_amount * 10^18`

## Chain ID Reference (EVM)

| Chain | ID | CAIP-2 | Native Asset |
|-------|----|--------|--------------|
| Ethereum Mainnet | 1 | `eip155:1` | `eth` |
| Ethereum Sepolia | 11155111 | `eip155:11155111` | `eth` |
| Base | 8453 | `eip155:8453` | `eth` |
| Optimism | 10 | `eip155:10` | `eth` |
| Arbitrum One | 42161 | `eip155:42161` | `eth` |
| Polygon | 137 | `eip155:137` | **`pol`** (NOT "matic") |
| Linea | 59144 | `eip155:59144` | `eth` |

## Solana CAIP-2 Reference

| Network | CAIP-2 |
|---------|--------|
| Solana Mainnet | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` |
| Solana Devnet | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` |

---

## Policy & Security

- **Privy TEE enforced**: Even if the agent is compromised, transfers that violate policy are rejected at the Privy TEE layer
- **Per-wallet policy**: Each chain's wallet has its own independent policy
- **Flexible rules**: Policy rules are configured via Privy's rule system (address allowlists, value limits, method restrictions, etc.)
- **Deny-all default**: New wallets have no allowed transfers until policy is configured by the user via the backend
- **Pass-through**: Policy rules are managed directly via Privy (source of truth), no local cache

Policy is managed by the user through the main backend API, not by the agent.

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| "Not running on a Fly Machine" | Wallet requires Fly deployment | Cannot use wallet locally |
| "Policy violation: ..." | Transfer rejected by Privy policy | Check whitelist and daily limits |
| "HTTP 404" | Wallet not found for this machine | Wallet may not be created yet |
| "HTTP 403" | OIDC token invalid or expired | Token will auto-refresh, retry |

