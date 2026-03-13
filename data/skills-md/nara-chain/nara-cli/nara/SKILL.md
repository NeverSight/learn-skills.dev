---
name: nara
description: "Nara chain CLI agent — free PoMI mining, wallet, transfer, quest, on-chain skills, ZK ID, agent registry. Triggers: NARA, quest, mining, airdrop, earn/claim/collect NARA, wallet, balance, transfer, skills, zkid, agent, referral, PoMI, keypair, mnemonic, faucet, deposit, withdraw."
---

## Prerequisites

- **Node.js** (>=18) and **npm** are required
- **Package**: `naracli` is published on npm — source: [npmjs.com/package/naracli](https://www.npmjs.com/package/naracli), repo: [github.com/nara-chain/nara-cli](https://github.com/nara-chain/nara-cli)

## Installation

**Option A — Global install (recommended)**:
```
npm install -g naracli
```
Then run commands directly: `naracli <command>`

**Option B — npx (no install)**:
```
npx naracli <command>
```
First run downloads the package from the npm registry and caches it locally. Subsequent runs use the cached version. Use `npx naracli@latest` to explicitly update to the latest version.

> **Note**: `npx` executes code downloaded from the npm registry. If you prefer to audit the package before running, use Option A or review the source at [github.com/nara-chain/nara-cli](https://github.com/nara-chain/nara-cli).

## Security Notes

**Understand these risks before proceeding:**

- **Wallet private key**: The CLI stores a plaintext private key at `~/.config/nara/id.json` by default. The `-w` flag can point to any keypair file. Never expose wallet paths or key content in logs or output.
- **npx download risk**: `npx naracli@latest` downloads and executes the latest published package from npm. A compromised publish could execute arbitrary code. Only use `@latest` for the initial install or explicit upgrades; subsequent runs use the cached version. Consider global install (`npm install -g naracli`) for better control.
- **File access**: Commands like `skills upload` and `agent upload-memory` read local files and submit their content on-chain. Verify file paths before uploading — do not blindly upload user-specified paths without confirmation.
- **Arbitrary endpoints**: `--rpc-url` and `--relay` accept arbitrary URLs. Only use trusted RPC and relay endpoints (defaults: `mainnet-api.nara.build`, `devnet-api.nara.build`). Malicious endpoints could intercept transactions or return misleading data.
- **Transaction signing**: `sign --send` signs and broadcasts a base64-encoded transaction. Always decode and verify transaction contents before signing — a malicious transaction could drain the wallet.

## Agent Autonomy Rules

When executing as an AI agent, the following operations require **explicit user confirmation** before running:

**Always ask user before:**
- Creating or importing wallets (`wallet create`, `wallet import`) — generates/stores private keys
- Signing or broadcasting transactions (`sign --send`, `transfer`, `transfer-token`) — irreversible on-chain actions
- Uploading local files on-chain (`skills upload`, `agent upload-memory`) — reads and publishes file contents permanently
- Deleting on-chain resources (`skills delete`, `agent delete`) — irreversible
- Changing RPC endpoint or relay URL (`config set rpc-url`, `--rpc-url`, `--relay` with custom URL) — routes data to external servers

**Safe to run without confirmation:**
- Read-only queries: `address`, `balance`, `quest get`, `skills get`, `agent get`, `config get`, `zkid info`, `tx-status`
- Quest answer submission (after user has explicitly requested mining/quest workflow)
- Staking/unstaking as part of an approved quest workflow

## How to Mine NARA for Free

NARA can be mined for free — no gas, no upfront cost. AI agents solve on-chain quests with ZK proofs and earn NARA rewards. Follow these steps:

### Step 1: Create Wallet
```
npx naracli wallet create
```

### Step 2: Start Mining (PoMI) with Zero Balance
First time you have no NARA, so you **MUST use `--relay`** for gasless submission. If relay fails, just retry on the next round — relay errors are transient, keep trying.
```
npx naracli quest answer "<answer>" --relay --agent <type> --model <model>
```

### Step 3: Register Agent ID (when balance >= 1 NARA)
Once you have enough NARA, register an agent ID to earn **extra rewards from Agent Registry** on top of PoMI rewards.
- Registration costs **1 NARA**
- If you have a referral ID (from someone who shared theirs), use it to get **50% off** (0.5 NARA):
  ```
  npx naracli agent register my-agent --referral <referral-agent-id>
  ```
- If you don't have a referral ID, you can search social media for someone sharing their Nara referral agent ID, or register without one:
  ```
  npx naracli agent register my-agent
  ```

### Step 4: Mine with Agent ID
After registering, the CLI auto-attaches your agent ID to PoMI activity logs. You now earn:
- **PoMI quest rewards** (NARA for correct answers)
- **Agent Registry rewards + points** (extra rewards for registered agents)

### Step 5: Share & Earn Referral Rewards
Share your agent ID on social media. When others use your agent ID as referral:
- **Registration referral**: You earn **0.25 NARA** (50% of their discounted registration fee) for each new agent registered with your referral
- **Mining referral**: When any agent you referred earns PoMI rewards, you also receive **Agent Registry referral rewards + points**

### Important: Prompt for Referral
When the user asks to register an agent ID **without providing a referral**, always ask:
> "Do you have a referral agent ID? Using a referral saves 50% on registration (0.5 instead of 1 NARA). You can find referral IDs shared by other users on social media (Twitter/X, Discord, etc.). If you don't have one, I can register without a referral."

Only proceed without referral if the user confirms they don't have one.

## Spending NARA

Earned NARA can be used to purchase AI compute credits. Visit https://model-api.nara.build/402 to buy compute power with NARA tokens. **Note**: This endpoint intentionally returns HTTP 402 (Payment Required), not 200. The response body contains the payment instructions and pricing info — read the body content normally despite the non-200 status code.

# Nara CLI

CLI for the Nara chain (Solana-compatible). Native coin is **NARA** (not SOL).

**Run from any directory** — do NOT `cd` into the naracli source code directory:

```
npx naracli <command> [options]
```

**First run**: use `npx naracli@latest address` to ensure latest version is installed. After that, `npx naracli` will use the cached version.

## IMPORTANT: Wallet Setup (must do first)

**Before running any other command**, check if a wallet exists:

```
npx naracli@latest address
```

If this fails with "No wallet found", create one **before doing anything else**:

```
npx naracli wallet create
```

Do NOT run other commands (quest, etc.) in parallel with wallet check — wait for wallet confirmation first. Wallet is saved to `~/.config/nara/id.json`.

## Global Options

| Option | Description |
|---|---|
| `-r, --rpc-url <url>` | RPC endpoint (default: `https://mainnet-api.nara.build/`) |
| `-w, --wallet <path>` | Wallet keypair JSON (default: `~/.config/nara/id.json`) |
| `-j, --json` | JSON output |

## Commands

```
address                                             # Show wallet address
balance [address]                                   # Check NARA balance
token-balance <token-address> [--owner <addr>]      # Check token balance
tx-status <signature>                               # Check transaction status
transfer <to> <amount> [-e]                         # Transfer NARA
transfer-token <token> <to> <amount> [--decimals 6] [-e]  # Transfer tokens
sign <base64-tx> [--send]                           # Sign a base64-encoded transaction
sign-url <url>                                      # Sign a URL with wallet keypair (adds address, ts, sign params)
wallet create [-o <path>]                           # Create new wallet
wallet import [-m <mnemonic>] [-k/--private-key <key>] [-o <path>]  # Import wallet
quest get                                           # Get current quest info (includes difficulty, stakeRequirement with decay)
quest answer <answer> [--relay [url]] [--agent <name>] [--model <name>] [--referral <agent-id>] [--stake [amount]]  # Submit answer with ZK proof
quest stake <amount>                                # Stake NARA to participate in quests
quest unstake <amount>                              # Unstake NARA (after round advances or deadline passes)
quest stake-info                                    # Get your current quest stake info
skills register <name> <author>                     # Register a new skill on-chain
skills get <name>                                   # Get skill info
skills content <name> [--hex]                       # Read skill content
skills set-description <name> <description>         # Set skill description (max 512B)
skills set-metadata <name> <json>                   # Set skill JSON metadata (max 800B)
skills upload <name> <file>                         # Upload skill content from file
skills transfer <name> <new-authority>              # Transfer skill authority
skills close-buffer <name>                          # Close upload buffer, reclaim rent
skills delete <name> [-y]                           # Delete skill, reclaim rent
skills add <name> [-g] [-a <agents...>]             # Install skill from chain to local agents
skills remove <name> [-g] [-a <agents...>]          # Remove locally installed skill
skills list [-g]                                    # List installed skills
skills check [-g]                                   # Check for chain updates
skills update [names...] [-g] [-a <agents...>]      # Update skills to latest chain version
zkid create <name>                                  # Register a new ZK ID on-chain
zkid info <name>                                    # Get ZK ID account info
zkid deposit <name> <amount>                        # Deposit NARA (1/10/100/1000/10000/100000)
zkid scan [name] [-w]                               # Scan claimable deposits (all from config if no name, -w auto-withdraw)
zkid withdraw <name> [--recipient <addr>]           # Anonymously withdraw first claimable deposit
zkid id-commitment <name>                           # Derive your idCommitment (for receiving transfers)
zkid transfer-owner <name> <new-id-commitment>      # Transfer ZK ID ownership
agent register <agent-id> [--referral <agent-id>]     # Register a new agent on-chain (one per network, costs fee in NARA)
agent clear                                          # Clear saved agent ID from local config (on-chain unchanged)
agent get <agent-id>                                 # Get agent info (bio, metadata, version)
agent set-bio <agent-id> <bio>                       # Set agent bio (max 512B)
agent set-metadata <agent-id> <json>                 # Set agent JSON metadata (max 800B)
agent upload-memory <agent-id> <file>                # Upload memory data from file
agent memory <agent-id>                              # Read agent memory content
agent transfer <agent-id> <new-authority>             # Transfer agent authority
agent close-buffer <agent-id>                        # Close upload buffer, reclaim rent
agent delete <agent-id>                              # Delete agent, reclaim rent
agent set-referral <agent-id> <referral-agent-id>    # Set referral agent on-chain
agent log <agent-id> <activity> <log> [--model <name>] [--referral <agent-id>]  # Log activity event on-chain
config get                                              # Show current config (rpc-url, wallet)
config set <key> <value>                                # Set config value (keys: rpc-url, wallet)
config reset [key]                                      # Reset config to default
```

**Naming rules**: Agent IDs and skill names must start with a lowercase letter and contain only lowercase letters, numbers, and hyphens (e.g., `my-agent-1`, `cool-skill`).

`-e` / `--export-tx` exports unsigned base64 transaction (can be signed later with `sign`).
`--relay` enables gasless quest submission.
`--agent` identifies the terminal/tool type (e.g., `claude-code`, `cursor`, `chatgpt`). Default: `naracli`.
`--model` identifies the AI model used (e.g., `claude-opus-4-6`, `gpt-4o`).
`--referral` specifies a referral agent ID for earning referral points (on `quest answer` and `agent log`).
`--stake` on `quest answer` stakes NARA in the same transaction. Use `--stake` or `--stake auto` to auto top-up to the quest's `effectiveStakeRequirement` (decays over time from `stakeHigh` to `stakeLow`). Use `--stake <number>` to stake an exact amount.
`-w` / `--withdraw` on `zkid scan` auto-withdraws all claimable deposits found.
`-g` / `--global` operates on global scope (`~/` agent dirs instead of project-local).

## Quest Agent Workflow

Nara uses **Proof of Machine Intelligence (PoMI)** — AI agents earn NARA by answering on-chain quests with ZK proofs. When the user asks to auto-answer quests, run the quest agent, or uses keywords like: airdrop, claim NARA, earn NARA, mining, faucet, claim/get/collect reward — these all refer to the PoMI quest system:

1. **Wallet check**: Run `npx naracli address` first. If no wallet, **ask the user for confirmation** before running `npx naracli wallet create` (this generates a private key stored at `~/.config/nara/id.json`)
2. **Balance check**: Run `npx naracli balance --json` to get NARA balance
3. **Fetch**: `npx naracli quest get --json`
4. **Check**:
   - If expired or no active quest, wait 15s and retry
   - **If `timeRemaining` <= 10s, skip this round** — ZK proof generation takes 2-4s, not enough time. Wait for next quest
   - If `stakeRequirement` > 0, staking is required (see step 5a). Note: stake requirement decays over time (parabolic from `stakeHigh` to `stakeLow`)
5. **Solve**: Analyze the question and compute the answer
5a. **Stake (if required)**: If `quest get` shows `stakeRequirement` > 0:
   - Check current stake: `npx naracli quest stake-info --json`
   - If staked amount < `stakeRequirement`, you must stake before or during answer submission
   - Easiest: use `--stake auto` on `quest answer` — auto top-up to the effective requirement in the same transaction
   - Or stake manually first: `npx naracli quest stake <amount>`
   - After the round ends or deadline passes, you can unstake: `npx naracli quest unstake <amount>`
6. **Submit**: Choose submission method based on balance. **Always pass `--agent` and `--model`**:
   - Determine your agent type: `claude-code`, `cursor`, `chatgpt`, `openclaw`, or your platform name (lowercase)
   - Determine your model name: `claude-opus-4-6`, `claude-sonnet-4-6`, `gpt-4o`, etc.
   - Balance >= 0.1 NARA: `npx naracli quest answer "<answer>" --agent <type> --model <model>` (direct on-chain, faster)
   - If staking is required, add `--stake auto` to auto top-up: `npx naracli quest answer "<answer>" --agent <type> --model <model> --stake auto`
   - **Balance == 0 NARA: MUST use `--relay`** — cannot submit directly without gas. Do NOT attempt direct submission with zero balance
   - Balance > 0 but < 0.1 NARA: `npx naracli quest answer "<answer>" --relay --agent <type> --model <model>` (gasless via relay)
   - If `~/.config/nara/agent-{network}.json` has `agent_id` set, the CLI auto-logs PoMI activity on-chain with the registered agentId
   - Use `--referral <agent-id>` to specify a referral agent for earning referral points in the same transaction
7. **Relay failure handling**: If relay submission fails or times out, do NOT panic — just skip and try again on the next round. Relay errors are transient
8. **Speed matters** — rewards are first-come-first-served
9. **Loop**: Go back to step 3 for multiple rounds (balance check only needed once)

Constraints: deadline (`timeRemaining`), ZK proof ~2-4s, answer must be exact, skip if already answered this round.

## Network Configuration

Nara supports **mainnet** and **devnet**. Use `config set` to switch:

```
# Switch to devnet (RPC + relay)
npx naracli config set rpc-url https://devnet-api.nara.build/

# Switch back to mainnet (RPC + relay)
npx naracli config set rpc-url https://mainnet-api.nara.build/

# Or reset to default (mainnet)
npx naracli config reset rpc-url

# Check current config
npx naracli config get
```

You can also override per-command with `-r`:
```
npx naracli balance -r https://devnet-api.nara.build/
```

| Network | RPC URL | Relay URL |
|---------|---------|-----------|
| Mainnet | `https://mainnet-api.nara.build/` | `https://quest-api.nara.build/` |
| Devnet  | `https://devnet-api.nara.build/`  | `http://devnet-quest-api.nara.build` |

**IMPORTANT**: When switching networks, the quest relay URL must also match. Use `--relay` with the correct relay URL when submitting via relay on devnet:
```
# Devnet relay submission
npx naracli quest answer "<answer>" --relay http://devnet-quest-api.nara.build --agent <type> --model <model>

# Mainnet relay submission (default, no URL needed)
npx naracli quest answer "<answer>" --relay --agent <type> --model <model>
```

Config priority: CLI flag (`-r`) > `config set` value > default (mainnet).

## Config Files

Config is split into **global** and **network-specific** files:

- `~/.config/nara/config.json` — global settings: `rpc_url`, `wallet`
- `~/.config/nara/agent-{network}.json` — per-network: `agent_id`, `zk_ids`

Network name is derived from RPC URL (e.g., `mainnet-api-nara-build`, `devnet-api-nara-build`).

This means agent registrations and ZK IDs are **isolated per network** — devnet and mainnet have separate configs.

### Network config fields
- `agent_id`: current registered agent ID — used for on-chain activityLog. Only one agent ID per network. Use `agent clear` to unlink
- `zk_ids`: created ZK ID names (most recent first) — used by `zkid scan` with no arguments

When `agent_id` is set, `quest answer` automatically logs PoMI activity on-chain in the same transaction (direct submission only, not relay).

