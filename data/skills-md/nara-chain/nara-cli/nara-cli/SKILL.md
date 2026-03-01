---
name: nara-cli
description: "Nara chain CLI and SDK agent. Use when the user mentions: Nara, NSO, Nara wallet, balance, transfer NSO, quest, answer quest, or any blockchain transaction on the Nara chain. Also triggers for keywords: airdrop, keypair, mnemonic, quest agent, auto-answer, claim NSO, earn NSO, mining, mine NSO, faucet, claim reward, get reward, collect reward."
---

# Nara CLI

CLI for the Nara chain (Solana-compatible). Native coin is **NSO** (not SOL).

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
balance [address]                                   # Check NSO balance
token-balance <token-address> [--owner <addr>]      # Check token balance
tx-status <signature>                               # Check transaction status
transfer <to> <amount> [-e]                         # Transfer NSO
transfer-token <token> <to> <amount> [--decimals 6] [-e]  # Transfer tokens
sign <base64-tx> [--send]                           # Sign a base64-encoded transaction
wallet create                                       # Create new wallet
wallet import [-m <mnemonic>] [-k <key>]            # Import wallet
quest get                                           # Get current quest info
quest answer <answer> [--relay [url]]               # Submit answer with ZK proof
```

`-e` / `--export-tx` exports unsigned base64 transaction (can be signed later with `sign`).
`--relay` enables gasless quest submission.

## Quest Agent Workflow

Nara uses **Proof of Machine Intelligence (PoMI)** — AI agents earn NSO by answering on-chain quests with ZK proofs. When the user asks to auto-answer quests, run the quest agent, or uses keywords like: airdrop, claim NSO, earn NSO, mining, faucet, claim/get/collect reward — these all refer to the PoMI quest system:

1. **Wallet check**: Run `npx naracli address` first. If no wallet, run `npx naracli wallet create` and wait for it to complete
2. **Balance check**: Run `npx naracli balance --json` to get NSO balance
3. **Fetch**: `npx naracli quest get --json`
4. **Check**: If expired or no active quest, wait 15s and retry
5. **Solve**: Analyze the question and compute the answer. See [references/quest-questions.md](references/quest-questions.md) for question types
6. **Submit**: Choose submission method based on balance:
   - Balance >= 0.1 NSO: `npx naracli quest answer "<answer>"` (direct on-chain, faster)
   - Balance < 0.1 NSO: `npx naracli quest answer "<answer>" --relay` (gasless via relay)
7. **Speed matters** — rewards are first-come-first-served
8. **Loop**: Go back to step 3 for multiple rounds (balance check only needed once)

Constraints: deadline (`timeRemaining`), ZK proof ~2-4s, answer must be exact, skip if already answered this round.
