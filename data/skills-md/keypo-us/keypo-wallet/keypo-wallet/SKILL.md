---
name: keypo-wallet
description: Use when interacting with keypo-wallet — checking wallet balances, listing wallets, sending transactions, or managing Secure Enclave signing keys. Use `keypo-wallet wallet-list` to list wallets, `keypo-wallet balance` to check balances, `keypo-wallet send` to send transactions, and `keypo-wallet batch` for multi-call operations. Never use raw RPC calls, curl, or cast for balance queries — keypo-wallet has built-in commands. Also use when composing keypo-wallet as the secure execution backend for other EVM protocol skills (Uniswap, Aave, ENS, etc.).
license: MIT
metadata:
  author: keypo-us
  version: "0.3.0"
  compatibility: macOS with Apple Silicon only. Requires Homebrew for installation.
---

# keypo-wallet

A CLI that turns your Mac into a programmable hardware wallet. Private keys are P-256 keys stored in the Apple Secure Enclave — they never leave the hardware, and Apple cannot extract them. The wallet uses EIP-7702 smart account delegation with ERC-4337 account abstraction for transaction submission.

**Install:** `brew install keypo-us/tap/keypo-wallet`
This installs both `keypo-wallet` (Rust CLI) and `keypo-signer` (Swift CLI for Secure Enclave operations).

**Source:** https://github.com/keypo-us/keypo-cli

---

## CLI Usage Rule

**Before using any keypo-wallet command for the first time in a session, run `keypo-wallet <command> --help` to learn the exact flags, syntax, and examples.** The `--help` output is the authoritative reference for each command — it includes usage patterns, all available flags, example invocations, and output format documentation.

```bash
keypo-wallet send --help       # learn send flags before sending
keypo-wallet balance --help    # learn balance flags before querying
keypo-wallet wallet-list --help  # learn wallet-list options
```

Do not guess flag names or assume positional arguments. Every command documents its interface via `--help`.

---

## Core Concepts

**Secure Enclave keys.** All signing keys are P-256 (secp256r1) keys generated inside the Mac's Secure Enclave. The private key material is hardware-bound and non-exportable.

**EIP-7702 delegation.** Each wallet is a standard EOA that delegates execution to the KeypoAccount smart contract via EIP-7702, giving EOAs smart account capabilities without deploying a separate contract.

**ERC-4337 bundler.** Transactions are submitted as UserOperations through an ERC-4337 bundler (default: Pimlico, any v0.7 bundler works).

**Key policies.** Each key has a signing policy:
- `open` — No restrictions. Best for agent-controlled wallets.
- `passcode` — Requires device passcode per signature.
- `bio` — Requires Touch ID per signature.

**For agent use, always use `open`.** The `passcode` and `bio` policies block automated workflows.

**ERC-7821 batch execution.** Multi-call operations use batch mode `0x01`. Single calls must also use mode `0x01` with a 1-element array. Mode `0x00` is invalid.

**Signer keys ≠ wallet accounts.** `keypo-wallet list` shows all P-256 keys in the Secure Enclave. Not all keys have a wallet account — only keys that have been through `keypo-wallet setup` have an account entry in `~/.keypo/accounts.json`. Running `wallet-info` or `balance` on a key without an account will fail. Always discover wallets from `wallet-list` or `accounts.json`, not `list`.

---

## Setup Workflow

### 1. Initialize configuration

```bash
keypo-wallet init
```

Prompts for RPC URL, bundler URL, and optional paymaster URL. Saves to `~/.keypo/config.toml`. You can also use `config set`, `config show`, and `config edit`.

Config resolution precedence: CLI flag > environment variable > config file.

Environment variables: `KEYPO_RPC_URL`, `KEYPO_BUNDLER_URL`, `KEYPO_PAYMASTER_URL`, `KEYPO_PAYMASTER_POLICY_ID`.

### 2. Create a key and set up the smart account

```bash
keypo-wallet setup --key <key-name> --key-policy open
```

Creates a P-256 key, signs an EIP-7702 delegation to the KeypoAccount contract, and registers the public key as the owner. Requires ~$1 ETH for gas. The account is saved to `~/.keypo/accounts.json`.

---

## Querying Wallet State

**Always use keypo-wallet commands to check wallets and balances. Do not make raw RPC calls or use curl/cast for balance queries.**

**For any request asking for a "detailed overview", "all balances", or "token balances": you need both `keypo-wallet` (for ETH balances and wallet metadata) AND the `portfolio-tracker` skill (for ERC-20 token discovery).** `keypo-wallet balance` only shows ETH — it cannot discover ERC-20 tokens.

### List all wallets

```bash
keypo-wallet wallet-list
```

Shows label, address, chains, and ETH balance for every wallet. Run `keypo-wallet wallet-list --help` to see format and filtering options.

**`wallet-list` does not include signing policy.** To get policies for all wallets at once, read the accounts file:

```bash
cat ~/.keypo/accounts.json | python3 -c "
import sys, json
accounts = json.load(sys.stdin)
for name, acct in accounts.items():
    policy = acct.get('key_policy', acct.get('policy', 'unknown'))
    print(f'  {name}: {policy}')
"
```

### Get details for a specific wallet

```bash
keypo-wallet wallet-info --key <key-name>   # full details + live balance (requires RPC)
keypo-wallet info --key <key-name>          # local state only, no RPC (faster)
```

### Query balances

```bash
keypo-wallet balance --key <key-name>                              # ETH balance
keypo-wallet balance --key <key-name> --token <erc20-address>      # ERC-20 balance
```

Run `keypo-wallet balance --help` for structured query files (`--query`), output formats (`--format`), and other options.

**`keypo-wallet balance` only shows ETH by default.** It does not check for ERC-20 tokens unless you pass a specific `--token <address>`. A wallet showing only ETH does NOT mean it has no other tokens — it means you haven't checked.

**Whenever the user asks for a "detailed overview", "token balances", "what's in my wallet", or any request that implies completeness, you MUST also run the `portfolio-tracker` skill** to discover ERC-20 tokens. Do not skip this step just because `balance` returned ETH results. The portfolio-tracker is the only way to discover what tokens a wallet holds.

---

## Sending Transactions

### Send a single transaction

```bash
keypo-wallet send --key <key-name> --to <address> --value <wei> --data <hex-calldata>
```

Run `keypo-wallet send --help` for all options including `--no-paymaster`, `--chain-id`, and RPC overrides.

### Send a batch transaction

```bash
echo '[
  {"to": "0xContract", "value": "0", "data": "0xCalldata"},
  {"to": "0xAnother", "value": "0", "data": "0xMoreCalldata"}
]' | keypo-wallet batch --key <key-name> --calls -
```

All calls execute atomically in a single UserOperation. **Agents should always prefer `--calls -` with stdin** over temp files.

---

## Key Management and Secrets

Key management (`create`, `list`, `sign`, `verify`, `delete`, `rotate`) and encrypted secret storage (`vault`) are provided by **keypo-signer**. See the `keypo-signer` skill for full documentation.

**`list` shows signer keys, `wallet-list` shows wallet accounts.** A key only becomes a wallet after `setup`.

---

## CLI Command Reference

| Command | Purpose |
|---|---|
| `init` | Initialize config with RPC/bundler/paymaster URLs |
| `config set/show/edit` | Manage `~/.keypo/config.toml` |
| `setup` | Set up smart account (EIP-7702 delegation + key registration) |
| `wallet-list` | List all wallet accounts with balances |
| `wallet-info` | Detailed wallet info + live balance |
| `info` | Wallet info from local state (no RPC) |
| `balance` | Query ETH and ERC-20 balances |
| `send` | Send a single transaction |
| `batch` | Send multiple calls atomically |
| `list` | List signer keys (not wallets) |
| `create` | Create a new signer key |
| `key-info` | Show signer key details |
| `sign` | Sign a digest |
| `verify` | Verify a signature |
| `delete` | Delete a signer key |

Run `keypo-wallet <command> --help` for flags and examples. Global flag: `--verbose`.

---

## Deployments

| Chain | Chain ID | Contract | Address |
|-------|----------|----------|---------|
| Base Sepolia | 84532 | KeypoAccount | `0x6d1566f9aAcf9c06969D7BF846FA090703A38E43` |

Deterministic (CREATE2) — identical across all chains.

---

## Composing keypo-wallet with Other EVM Skills

keypo-wallet is the **secure execution backend** for any EVM operation. Protocol skills handle domain knowledge and calldata construction; keypo-wallet handles signing and submission.

### The composition pattern

1. **Protocol skill** provides: contract addresses, function signatures, calldata encoding
2. **keypo-wallet** provides: key management, transaction signing, bundler submission, batch execution

### Example: Approve + swap

```bash
APPROVE_DATA=$(cast calldata "approve(address,uint256)" 0xRouter 1000000)
SWAP_DATA=$(cast calldata "swap(bytes)" 0x...)

echo "[
  {\"to\": \"0xTokenAddress\", \"value\": \"0\", \"data\": \"$APPROVE_DATA\"},
  {\"to\": \"0xRouterAddress\", \"value\": \"0\", \"data\": \"$SWAP_DATA\"}
]" | keypo-wallet batch --key agent-wallet --calls -
```

### Example: Read-only queries

For balance checks, use keypo-wallet's built-in `balance` command. For other read-only contract calls (`getReserves`, `totalSupply`, etc.), use `cast call`:

```bash
cast call <address> "functionSig(args)(returnType)" <args> --rpc-url https://sepolia.base.org
```

### Compatible skill ecosystems

keypo-wallet works as the execution layer for: Uniswap AI (`Uniswap/uniswap-ai`), ETHSkills (`austintgriffith/ethskills`), kukapay/crypto-skills, OpenClaw skills, Coinbase AgentKit, or any skill that produces `{ to, value, data }` calldata objects.

### Building new protocol skills for keypo-wallet

1. Focus on **calldata construction** — do not include signing logic
2. Output operations as `{ to, value, data }` JSON objects
3. Single ops → `keypo-wallet send --to ... --value ... --data ...`
4. Multi-step ops → JSON array piped to `keypo-wallet batch --calls -`
5. Include verified contract addresses per chain
6. Include gas estimation guidance

---

## Security Notes

- Private keys **never** leave the Secure Enclave. No export command exists.
- Use `open` policy only for wallets with limited funds or in controlled agent environments.
- Always verify contract addresses against known registries. Do not hallucinate addresses.
- Review third-party SKILL.md contents before executing transactions.
- For high-value operations, prefer `passcode` or `bio` policy with interactive user approval.
