---
name: solana-simd
description: "Solana Improvement Documents reference — accounts model, PDAs, CPIs, Token Extensions (Token-2022), priority fees (SIMD-0096), address lookup tables, versioned transactions, rent mechanics, and key SIMD proposals (0033 fee markets, 0047 syscall, 0096 priority fees, 0172 staking)."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: solana
  category: Infrastructure
tags:
  - solana
  - simd
  - improvement-proposals
  - pda
  - cpi
  - token-extensions
  - priority-fees
  - anchor
---

# Solana Improvement Documents (SIMD) Reference

Solana Improvement Documents (SIMDs) are the formal mechanism for proposing changes to the Solana protocol. They cover everything from fee market restructuring to new syscalls, staking changes, and token standards. This skill covers the SIMDs that matter most for developers, along with the core Solana primitives (accounts, PDAs, CPIs, rent) that every program depends on.

## What You Probably Got Wrong

> AI models trained on Ethereum or outdated Solana docs produce broken code. Fix these assumptions first.

- **Solana programs are stateless — state lives in accounts, not contracts** — There is no contract storage. Programs are executable code only. All mutable state is stored in separate data accounts that programs read and write via instruction inputs. If you write Solana code like Solidity (expecting `self.balances[user]`), it will not compile.

- **PDA bumps MUST be canonical** — `Pubkey::find_program_address` returns the canonical bump (highest valid bump 255..0). Always store and reuse this bump. Never call `create_program_address` with an arbitrary bump — it may produce a valid pubkey on the ed25519 curve, meaning it has a private key and is not a PDA. Anchor's `seeds` constraint handles this automatically.

- **`invoke_signed` is NOT the same as `invoke`** — `invoke` passes through existing signers from the transaction. `invoke_signed` lets a PDA sign by providing the seeds + bump. Use `invoke` when a human wallet signs. Use `invoke_signed` when your program's PDA needs to authorize a CPI call.

- **Rent exemption is not optional in practice** — Accounts below the rent-exempt minimum are garbage collected. Since SIMD-0084 (epoch-based rent collection removal), all new accounts must be rent-exempt at creation. The minimum is ~0.00089088 SOL per byte. Always calculate: `Rent::get()?.minimum_balance(data_len)`.

- **Token-2022 is NOT a drop-in replacement for SPL Token** — Programs that hardcode the SPL Token program ID (`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`) will reject Token-2022 tokens (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`). You must check both program IDs or use the `spl_token_2022::check_spl_token_program_account` helper.

- **Priority fees are per compute unit, not per transaction** — `ComputeBudgetProgram.setComputeUnitPrice({ microLamports })` sets the price PER compute unit. Total priority fee = `microLamports * compute_units_consumed / 1_000_000`. Overpaying happens when you set high `microLamports` without reducing the compute unit limit.

- **Account data size is fixed at creation** — You cannot resize an account after creation (unless you use `realloc`). Plan your data layout carefully. `realloc` has constraints: max 10KB increase per instruction, and the account must be owned by the calling program.

- **CPI depth limit is 4, not unlimited** — Program A calls B calls C calls D — that is depth 4, the maximum. Design your program architecture accordingly. Each CPI level also reduces available compute units.

## How to Look Up Any SIMD

When a user asks about ANY SIMD — even ones not covered in this skill — fetch the full spec on demand.

### Step 1: Find the filename

SIMD filenames include a slug (e.g., `0096-reward-collected-priority-fee-in-entirety.md`), so you can't construct the URL from just the number. First, list the proposals directory and find the matching file:

```
WebFetch: https://api.github.com/repos/solana-foundation/solana-improvement-documents/contents/proposals
Prompt: "Find the filename that starts with {NNNN} (zero-padded to 4 digits)"
```

Examples: SIMD-96 → look for `0096-*`, SIMD-33 → look for `0033-*`

### Step 2: Fetch the raw spec

Once you have the full filename:

```
WebFetch: https://raw.githubusercontent.com/solana-foundation/solana-improvement-documents/main/proposals/{full-filename}
```

Examples:
- SIMD-0096 → `https://raw.githubusercontent.com/solana-foundation/solana-improvement-documents/main/proposals/0096-reward-collected-priority-fee-in-entirety.md`
- SIMD-0033 → `https://raw.githubusercontent.com/solana-foundation/solana-improvement-documents/main/proposals/0033-timely-vote-credits.md`

### Step 3: Parse and summarize

The fetched markdown has YAML frontmatter (`simd`, `title`, `authors`, `category`, `type`, `status`, `created`) followed by sections: Summary, Motivation, New Terminology, Detailed Design, Impact, Security Considerations.

Extract and present: title, status, what it changes, implementation details, and impact on validators/developers.

### Alternative methods

```bash
# GitHub CLI — list all proposals and grep for the number
gh api repos/solana-foundation/solana-improvement-documents/contents/proposals --jq '.[].name' | grep "^{NNNN}"

# Then fetch the matched file
gh api repos/solana-foundation/solana-improvement-documents/contents/proposals/{matched-filename} --jq '.content' | base64 -d
```

### Sources

| Source | URL | Best for |
|--------|-----|----------|
| GitHub repo | https://github.com/solana-foundation/solana-improvement-documents | Raw specs, PR discussions, git blame |
| Solana Forum | https://forum.solana.com/c/simd/5 | Community discussion, context, rationale |

- Raw specs: `https://raw.githubusercontent.com/solana-foundation/solana-improvement-documents/main/proposals/{filename}`
- All proposals: https://github.com/solana-foundation/solana-improvement-documents/tree/main/proposals
- Forum discussions: https://forum.solana.com/c/simd/5

## SIMD Status Lifecycle

```
Draft -> Review -> Accepted -> Implemented -> Activated
                            -> Rejected
                            -> Withdrawn
```

- **Draft**: Initial proposal, open for feedback
- **Review**: Under formal review by core contributors
- **Accepted**: Approved for implementation
- **Implemented**: Code merged, awaiting feature gate activation
- **Activated**: Live on mainnet-beta
- **Rejected/Withdrawn**: Not proceeding

## Core Solana Concepts

### Accounts Model

Everything on Solana is an account. Programs, token mints, user wallets, PDAs — all accounts with different configurations.

| Field | Type | Description |
|-------|------|-------------|
| `lamports` | `u64` | Balance in lamports (1 SOL = 1e9 lamports) |
| `data` | `Vec<u8>` | Arbitrary byte array, max 10 MB |
| `owner` | `Pubkey` | Program that owns this account (can write to `data`) |
| `executable` | `bool` | Whether this account is a program |
| `rent_epoch` | `u64` | Deprecated since SIMD-0084 |

Key rules:
- Only the **owner program** can modify an account's `data` and debit `lamports`
- Any program can **credit** lamports to any account
- Account data size is set at creation and requires `realloc` to change
- The System Program owns all wallet accounts (no data, just lamports)

### Programs

Programs are stateless executable accounts. They process instructions that reference other accounts.

```rust
use anchor_lang::prelude::*;

declare_id!("YourProgramID11111111111111111111111111111");

#[program]
pub mod my_program {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, data: u64) -> Result<()> {
        let account = &mut ctx.accounts.my_account;
        account.data = data;
        account.authority = ctx.accounts.authority.key();
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + MyAccount::INIT_SPACE
    )]
    pub my_account: Account<'info, MyAccount>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
#[derive(InitSpace)]
pub struct MyAccount {
    pub data: u64,
    pub authority: Pubkey,
}
```

### PDAs (Program Derived Addresses)

PDAs are deterministic addresses derived from seeds and a program ID. They are NOT on the ed25519 curve, so no private key exists — only the deriving program can sign for them.

#### Derivation

```rust
// On-chain: find canonical PDA
let (pda, bump) = Pubkey::find_program_address(
    &[b"vault", user.key().as_ref()],
    ctx.program_id,
);

// Verify PDA matches expected account
require_keys_eq!(pda, ctx.accounts.vault.key());
```

```typescript
// Client-side: derive the same PDA
import { PublicKey } from "@solana/web3.js";

const [pda, bump] = PublicKey.findProgramAddressSync(
  [Buffer.from("vault"), userPublicKey.toBuffer()],
  programId
);
```

#### Anchor PDA Constraints

```rust
#[derive(Accounts)]
pub struct WithdrawFromVault<'info> {
    #[account(
        mut,
        seeds = [b"vault", authority.key().as_ref()],
        bump,
        // Anchor derives the PDA, verifies it matches, stores the bump
    )]
    pub vault: Account<'info, Vault>,
    pub authority: Signer<'info>,
}
```

#### Canonical Bump Rule

```rust
// CORRECT: Use find_program_address (tries bumps 255 down to 0)
let (pda, bump) = Pubkey::find_program_address(&seeds, &program_id);

// WRONG: Never use create_program_address with a guess
// This may produce a valid ed25519 pubkey (has private key = NOT a PDA)
let pda = Pubkey::create_program_address(&[&seeds, &[arbitrary_bump]], &program_id);
```

### CPIs (Cross-Program Invocations)

#### `invoke` — Pass-Through Signing

```rust
use anchor_lang::prelude::*;
use anchor_spl::token::{self, Transfer, Token, TokenAccount};

pub fn transfer_tokens(ctx: Context<TransferTokens>, amount: u64) -> Result<()> {
    let cpi_accounts = Transfer {
        from: ctx.accounts.source.to_account_info(),
        to: ctx.accounts.destination.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };
    let cpi_program = ctx.accounts.token_program.to_account_info();
    let cpi_ctx = CpiContext::new(cpi_program, cpi_accounts);
    token::transfer(cpi_ctx, amount)?;
    Ok(())
}
```

#### `invoke_signed` — PDA Signing

```rust
pub fn transfer_from_vault(ctx: Context<VaultTransfer>, amount: u64) -> Result<()> {
    let seeds = &[
        b"vault",
        ctx.accounts.authority.key.as_ref(),
        &[ctx.accounts.vault.bump],
    ];
    let signer_seeds = &[&seeds[..]];

    let cpi_accounts = Transfer {
        from: ctx.accounts.vault_token.to_account_info(),
        to: ctx.accounts.destination.to_account_info(),
        authority: ctx.accounts.vault.to_account_info(),
    };
    let cpi_ctx = CpiContext::new_with_signer(
        ctx.accounts.token_program.to_account_info(),
        cpi_accounts,
        signer_seeds,
    );
    token::transfer(cpi_ctx, amount)?;
    Ok(())
}
```

### Rent

Since SIMD-0084, all accounts must be rent-exempt at creation. The minimum balance is proportional to the account's data size.

```rust
// Calculate rent-exempt minimum
let rent = Rent::get()?;
let lamports = rent.minimum_balance(data_len);
```

| Data Size | Rent-Exempt Minimum |
|-----------|-------------------|
| 0 bytes (wallet) | 0.00089088 SOL |
| 165 bytes (token account) | 0.00203928 SOL |
| 82 bytes (mint) | 0.00144768 SOL |
| 200 bytes | 0.00227616 SOL |
| 1,000 bytes | 0.00795168 SOL |
| 10,000 bytes | 0.07228128 SOL |

Reclaiming rent: close the account and transfer lamports back.

```rust
// Anchor: close an account and reclaim rent
#[derive(Accounts)]
pub struct CloseVault<'info> {
    #[account(
        mut,
        close = authority,
        seeds = [b"vault", authority.key().as_ref()],
        bump,
    )]
    pub vault: Account<'info, Vault>,
    #[account(mut)]
    pub authority: Signer<'info>,
}
```

## Key SIMDs Deep-Dive

### SIMD-0033 — Timely Vote Credits

**Status**: Activated

Validators earn more vote credits for voting quickly. A vote landing within 2 slots of the voted-on slot earns more credits than one landing 32 slots later. This incentivizes low-latency validator infrastructure and faster consensus convergence.

**Developer impact**: None directly. Validators with better infrastructure earn more staking rewards, affecting APY calculations for staking protocols.

### SIMD-0046 — Versioned Transactions

**Status**: Activated

Introduced `VersionedTransaction` and Address Lookup Tables (ALTs). Legacy transactions are limited to 35 accounts (1232-byte size limit). V0 transactions reference ALTs to compress account lists, supporting 256+ accounts per transaction.

```typescript
import {
  Connection,
  VersionedTransaction,
  TransactionMessage,
  AddressLookupTableProgram,
  PublicKey,
} from "@solana/web3.js";

// Fetch an existing lookup table
const lookupTableAddress = new PublicKey("...");
const lookupTableAccount = await connection
  .getAddressLookupTable(lookupTableAddress)
  .then((res) => res.value);

if (!lookupTableAccount) throw new Error("Lookup table not found");

// Build a V0 transaction using the lookup table
const messageV0 = new TransactionMessage({
  payerKey: payer.publicKey,
  recentBlockhash: (await connection.getLatestBlockhash()).blockhash,
  instructions,
}).compileToV0Message([lookupTableAccount]);

const tx = new VersionedTransaction(messageV0);
tx.sign([payer]);
const sig = await connection.sendTransaction(tx);
```

### SIMD-0047 — Syscall Probing

**Status**: Accepted

Allows programs to query whether a syscall is available before calling it. Enables forward-compatible programs that can use new features when available and fall back gracefully when they are not. Important for programs deployed across multiple clusters at different feature activation stages.

### SIMD-0096 — Reward Full Priority Fee to Validator

**Status**: Activated

100% of priority fees go to the block-producing validator (previously 50% was burned). This aligns validator incentives and reduces off-protocol fee arrangements. Developers still set priority fees the same way, but the economic distribution changed.

```typescript
import { ComputeBudgetProgram } from "@solana/web3.js";

// Set compute unit limit (reduces wasted compute budget)
const setLimitIx = ComputeBudgetProgram.setComputeUnitLimit({
  units: 200_000,
});

// Set priority fee in micro-lamports per compute unit
const setPriceIx = ComputeBudgetProgram.setComputeUnitPrice({
  microLamports: 50_000, // 50,000 micro-lamports per CU
});

// Total priority fee = 200,000 CU * 50,000 microLamports / 1,000,000 = 10,000 lamports
// = 0.00001 SOL
```

### SIMD-0172 — Staking Rewards Distribution

**Status**: Accepted

Changes how staking rewards are distributed. Instead of bulk reward distribution at epoch boundaries (which causes slot-level congestion and delayed reward visibility), rewards are distributed incrementally within epochs. This smooths validator economics and reduces epoch-boundary performance impact.

## Token Extensions (Token-2022)

Token-2022 (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`) extends SPL Token with built-in features that previously required custom programs.

### Key Extensions

| Extension | Description | Use Case |
|-----------|-------------|----------|
| Transfer Fees | Percentage fee on every transfer | Protocol revenue, tax tokens |
| Confidential Transfers | Encrypted balances and amounts | Privacy-preserving payments |
| Interest-Bearing | Accumulating display balance | Yield-bearing stablecoins |
| Permanent Delegate | Authority that can transfer/burn any holder's tokens | Regulated assets, compliance |
| Non-Transferable | Soulbound tokens | Credentials, reputation |
| Transfer Hook | Custom program invoked on every transfer | Royalties, compliance checks |
| Metadata Pointer | On-chain metadata directly in mint | Eliminates Metaplex dependency |
| Group/Member | Hierarchical token relationships | Collections, token sets |

### Creating a Token-2022 Mint with Transfer Fees

```typescript
import {
  Connection,
  Keypair,
  SystemProgram,
  Transaction,
} from "@solana/web3.js";
import {
  TOKEN_2022_PROGRAM_ID,
  createInitializeMintInstruction,
  createInitializeTransferFeeConfigInstruction,
  getMintLen,
  ExtensionType,
} from "@solana/spl-token";

async function createMintWithTransferFee(
  connection: Connection,
  payer: Keypair,
  mintAuthority: Keypair,
  feeBasisPoints: number,   // e.g., 100 = 1%
  maxFee: bigint             // max fee in token base units
): Promise<Keypair> {
  const mintKeypair = Keypair.generate();

  const extensions = [ExtensionType.TransferFeeConfig];
  const mintLen = getMintLen(extensions);
  const lamports = await connection.getMinimumBalanceForRentExemption(mintLen);

  const tx = new Transaction().add(
    SystemProgram.createAccount({
      fromPubkey: payer.publicKey,
      newAccountPubkey: mintKeypair.publicKey,
      space: mintLen,
      lamports,
      programId: TOKEN_2022_PROGRAM_ID,
    }),
    createInitializeTransferFeeConfigInstruction(
      mintKeypair.publicKey,
      mintAuthority.publicKey,  // transferFeeConfigAuthority
      mintAuthority.publicKey,  // withdrawWithheldAuthority
      feeBasisPoints,
      maxFee,
      TOKEN_2022_PROGRAM_ID
    ),
    createInitializeMintInstruction(
      mintKeypair.publicKey,
      9,                         // decimals
      mintAuthority.publicKey,
      null,                      // freezeAuthority
      TOKEN_2022_PROGRAM_ID
    )
  );

  await connection.sendTransaction(tx, [payer, mintKeypair]);
  return mintKeypair;
}
```

### Checking Token Program Compatibility

```rust
use anchor_lang::prelude::*;

// Accept both SPL Token and Token-2022
pub fn check_token_program(token_program: &AccountInfo) -> Result<()> {
    let key = token_program.key();
    require!(
        key == spl_token::id() || key == spl_token_2022::id(),
        ErrorCode::InvalidTokenProgram
    );
    Ok(())
}
```

## Versioned Transactions and Address Lookup Tables

### Creating an Address Lookup Table

```typescript
import {
  Connection,
  Keypair,
  AddressLookupTableProgram,
  PublicKey,
} from "@solana/web3.js";

async function createLookupTable(
  connection: Connection,
  payer: Keypair,
  addresses: PublicKey[]
): Promise<PublicKey> {
  const slot = await connection.getSlot();

  // Step 1: Create the lookup table
  const [createIx, lookupTableAddress] =
    AddressLookupTableProgram.createLookupTable({
      authority: payer.publicKey,
      payer: payer.publicKey,
      recentSlot: slot,
    });

  // Step 2: Extend with addresses (max 30 per instruction)
  const extendIx = AddressLookupTableProgram.extendLookupTable({
    payer: payer.publicKey,
    authority: payer.publicKey,
    lookupTable: lookupTableAddress,
    addresses,
  });

  // Send both in one transaction
  const tx = new Transaction().add(createIx, extendIx);
  await connection.sendTransaction(tx, [payer]);

  return lookupTableAddress;
}
```

### When to Use ALTs

- Transactions referencing more than ~20 unique accounts
- DeFi aggregators routing through multiple pools
- Batch operations touching many token accounts
- Any transaction hitting the 1232-byte size limit

## Priority Fees in Practice

### Estimating Priority Fees

```typescript
import { Connection } from "@solana/web3.js";

async function estimatePriorityFee(
  connection: Connection,
  accountKeys: string[]
): Promise<number> {
  const fees = await connection.getRecentPrioritizationFees({
    lockedWritableAccounts: accountKeys.map(
      (key) => new PublicKey(key)
    ),
  });

  if (fees.length === 0) return 0;

  // Sort by fee, take the median for a balanced estimate
  const sorted = fees
    .map((f) => f.prioritizationFee)
    .sort((a, b) => a - b);
  const median = sorted[Math.floor(sorted.length / 2)];

  return median;
}
```

### Setting Priority Fees on a Transaction

```typescript
import {
  Connection,
  Transaction,
  ComputeBudgetProgram,
} from "@solana/web3.js";

function addPriorityFee(
  tx: Transaction,
  computeUnits: number,
  microLamportsPerCU: number
): Transaction {
  // Always set BOTH compute unit limit and price
  tx.add(
    ComputeBudgetProgram.setComputeUnitLimit({ units: computeUnits }),
    ComputeBudgetProgram.setComputeUnitPrice({ microLamports: microLamportsPerCU })
  );
  return tx;
}

// Cost calculation:
// priority_fee_lamports = computeUnits * microLamportsPerCU / 1_000_000
// Example: 200,000 CU * 50,000 microLamports = 10,000 lamports = 0.00001 SOL
```

### Priority Fee Tiers (March 2026 Estimates)

| Tier | microLamports/CU | Use Case |
|------|------------------|----------|
| Low | 1,000 - 10,000 | Non-urgent transfers |
| Medium | 10,000 - 100,000 | Normal DeFi operations |
| High | 100,000 - 1,000,000 | Time-sensitive swaps |
| Urgent | 1,000,000+ | NFT mints, liquidations |

These vary significantly by network congestion. Always use `getRecentPrioritizationFees` for real-time estimates.

## Key Constants

| Parameter | Value |
|-----------|-------|
| Slot time | ~400ms |
| Epoch length | ~2 days (~432,000 slots) |
| Max transaction size | 1,232 bytes |
| Max accounts per tx (legacy) | ~35 |
| Max accounts per tx (v0 + ALT) | 256+ |
| Max CPI depth | 4 |
| Compute unit limit (default) | 200,000 per instruction |
| Compute unit limit (max) | 1,400,000 per transaction |
| Min rent per byte | ~0.00089 SOL |
| Max account data | 10 MB |
| Max `realloc` increase per ix | 10,240 bytes (10 KB) |
| Lamports per SOL | 1,000,000,000 |

## Network Endpoints

| Network | RPC | WebSocket |
|---------|-----|-----------|
| Mainnet | `https://api.mainnet-beta.solana.com` | `wss://api.mainnet-beta.solana.com` |
| Devnet | `https://api.devnet.solana.com` | `wss://api.devnet.solana.com` |
| Testnet | `https://api.testnet.solana.com` | `wss://api.testnet.solana.com` |

Public endpoints are rate-limited. Use Helius, QuickNode, Triton, or Alchemy for production.

## Quick SIMD Lookup

| SIMD | Title | Status |
|------|-------|--------|
| 0002 | Fee-payer signed first | Activated |
| 0033 | Timely Vote Credits | Activated |
| 0046 | Versioned Transactions | Activated |
| 0047 | Syscall Probing | Accepted |
| 0048 | Native Program Upgrades | Activated |
| 0072 | Priority Fee Market | Activated |
| 0083 | Token Extensions (Token-2022) | Activated |
| 0084 | Remove Rent Collection | Activated |
| 0096 | Reward Full Priority Fee to Validator | Activated |
| 0105 | QUIC Protocol for TPU | Activated |
| 0118 | Partitioned Epoch Rewards | Activated |
| 0133 | Increase Account Data Limit | Review |
| 0148 | Token Metadata in Token-2022 | Activated |
| 0159 | Reduce Rent Cost | Draft |
| 0163 | Multiple Delegations per Account | Review |
| 0172 | Staking Rewards Distribution | Accepted |
| 0175 | Confidential Transfers v2 | Review |
| 0185 | Vote Account Size Reduction | Draft |
| 0186 | Precompile for Secp256r1 | Activated |
| 0193 | ZK Token Proof Program | Review |

Full list: https://github.com/solana-foundation/solana-improvement-documents/tree/main/proposals

## Related Skills

- **solana-agent-kit** — Solana Agent Kit for building AI agents that interact with Solana
- **jupiter** — Jupiter aggregator for token swaps and DCA
- **drift** — Drift Protocol for perpetuals and margin trading

## References

- SIMD Repository: https://github.com/solana-foundation/solana-improvement-documents
- Solana Docs: https://docs.solana.com
- Anchor Framework: https://www.anchor-lang.com
- SPL Token Docs: https://spl.solana.com/token
- Token-2022 Docs: https://spl.solana.com/token-2022
- Solana Cookbook: https://solanacookbook.com
- Compute Budget: https://docs.solana.com/developing/programming-model/runtime#compute-budget
- Address Lookup Tables: https://docs.solana.com/developing/lookup-tables

Last verified: 2026-03-01
