---
name: cksol
description: "Integrate ckSOL (chain-key SOL) into an IC app. Covers converting SOL to ckSOL via per-account Solana deposit addresses (get_deposit_address + deposit_sol with cycles, works from exchanges), withdrawing ckSOL to SOL (icrc2_approve + withdraw_sol), tracking deposit/withdrawal status, deposit-address derivation, fees, minimums, and which calls belong in the frontend vs a backend canister. Use when the user mentions ckSOL, Solana deposits or withdrawals on ICP, or moving SOL to/from the Internet Computer. Do NOT use for plain ICRC-1 ckSOL transfers (use icrc-ledger), SPL tokens, or signing arbitrary Solana transactions from a canister (use the SOL RPC canister / threshold Ed25519 directly)."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2, Node.js >= 22 for frontend code"
metadata:
  title: ckSOL (chain-key SOL)
  category: DeFi
---

# ckSOL Integration

## What This Is

ckSOL is an ICRC-1/ICRC-2 token backed 1:1 by SOL (9 decimals, 1 ckSOL = 1_000_000_000 lamports). The **ckSOL minter** derives one Solana deposit address per ICRC account from its threshold-Ed25519 key. It sweeps deposited SOL to its main address and mints once the sweep is finalized. For withdrawals it burns ckSOL via an ICRC-2 allowance and sends SOL using durable-nonce transactions, which never expire. It talks to Solana through the SOL RPC canister. Only native **SOL** is supported: no SPL tokens.

Source: `github.com/dfinity/cksol`. Minter v0.1.0 has run on mainnet since 2026-10.

## Canister IDs

| | Mainnet (Solana mainnet) | Staging (Solana Devnet, token "ckDevnetSOL") |
|---|---|---|
| Minter | `lh22c-kyaaa-aaaar-qb5nq-cai` | `ljyxk-riaaa-aaaar-qb5mq-cai` |
| Ledger | `ls5lp-lqaaa-aaaar-qb5oa-cai` | `la34w-haaaa-aaaar-qb5na-cai` |
| Index | `2ezyf-hqaaa-aaaar-qb6ga-cai` | `2r6ji-gyaaa-aaaar-qb6fq-cai` |
| Minter main Solana address | `GXVewvv6HehcLFYCmwpqh5CrMjqN9zJ8rqzGq3HEt9Ax` | `Br8eRkeya8hy3sHCYqtWqGeNNZ349aPSUKGVYFWKKer1` |

The ledger fee is 500 lamports. `get_minter_info` (query) on 2026-11-02 returned: `minimum_deposit_amount = 20_000_000` (0.02 SOL), `minimum_withdrawal_amount = 2_000_000` (0.002 SOL), `withdrawal_fee = 1_000_000` (0.001 SOL), `deposit_sol_required_cycles = 1_000_000_000_000`, and `deposit_sol_fee = 45_000_000_000`. **`deposit_sol_fee` is in cycles, not lamports.** Read these values at runtime.

## How the deposit address is computed

The minter uses non-hardened derivation from the IC threshold **Ed25519** key `key_1`, with path `[minter canister id bytes, [0x01], owner principal bytes, 32-byte subaccount (zeros for default)]`. The Solana address is the base58 of the derived 32-byte public key. It is deterministic and stable, one address per `(owner, subaccount)`, and is a plain system account. The minter's main address is the key at the empty path, so it can never collide with a deposit address. You can derive it offline (`deriveDepositAddressOffline` below) or call `get_deposit_address`, an **update** call that anyone may make for any non-anonymous owner.

## Deposit: SOL → ckSOL (deployed "manual" flow)

1. **Address.** `get_deposit_address(record { owner = opt <principal>; subaccount = opt <32 bytes> | null })` returns a base58 address. If `owner` is null, it defaults to the **caller**.
2. **Send SOL** to that address from any wallet or exchange, in one or several transfers (no memo). The **total balance** must reach `minimum_deposit_amount`.
3. **Notify.** `deposit_sol(record { owner = opt <principal>; subaccount })` **with cycles attached** (≥ `deposit_sol_required_cycles`). The minter reads the finalized balance and charges about 2.3B cycles for `getBalance` plus `deposit_sol_fee` (45B), refunding the rest. It then queues `sweepable = balance − 890_880` (the rent-exemption threshold stays on the address, once per address) and returns `Ok(deposit_id : nat64)`. Only canisters can attach cycles, so **a frontend cannot call `deposit_sol` directly**: route it through your backend canister. `owner` may be any principal, so a backend can pay for a user-owned account.
4. **Sweep and mint** happen on minter timers, about a minute each. Up to 10 deposits are swept per Solana transaction, and each deposit pays a 5_000-lamport fee share. ckSOL is minted only after the sweep is **finalized**. The user receives `sweepable − 5_000` lamports.
5. **Track** with `deposit_sol_status(deposit_id)` (query): `Queued { sweepable_amount } → Swept { signature } → Finalized { signature } → Minted { block_index; minted_amount }`. A `Dropped { signature }` status means the sweep failed or expired, nothing was minted, and the funds are still on the address: call `deposit_sol` again. A `Quarantined { signature }` status needs a minter upgrade: use a different subaccount for new deposits.

At most one deposit per account is in flight. Calling `deposit_sol` again while one is queued, swept or finalized returns **the same `deposit_id`** and refunds all cycles, so retries are safe. Example: the first deposit of exactly 1 SOL mints 999_104_120 lamports, the minimum 0.02 SOL mints 19_104_120, and a later deposit to the same address loses only the 5_000 fee share.

**Upcoming automatic flow, not on mainnet as of 2026-11-02.** `watch_deposit_address(record { subaccount })` is free, needs no cycles, and has owner = caller. The minter then scans the address for about 24 h and sweeps automatically, deducting `automatic_deposit_fee` (0.002 SOL). Status is `Watching | Detected { deposit_id }`, and you follow it with `deposit_sol_status`. Before using it, check that the endpoint exists: `icp canister metadata lh22c-kyaaa-aaaar-qb5nq-cai candid:service -n ic`.

## Withdrawal: ckSOL → SOL

1. `icrc2_approve` on the ckSOL ledger, with spender = **minter** and amount ≥ the withdrawal amount. Burns are fee-free, and the approve itself costs 500 lamports.
2. `withdraw_sol(record { address = "<base58>"; amount = <lamports : nat64>; from_subaccount = opt … })` burns from `caller + from_subaccount`. There is no owner argument. It returns `Ok { block_index }`, the burn index, which is also the withdrawal id.
3. The minter batches up to 10 withdrawals per durable-nonce transaction. The destination receives `amount − withdrawal_fee`.
4. Track with `withdraw_sol_status(record { block_index })`, an **update** call: `Pending → TxSent { transaction_id } → TxFinalized (Success | Failure) { transaction_id }`.

Business errors come back as `Err`, not as traps: `ValueTooSmall`, `MalformedAddress`, `InvalidDestination` (Solana reserved/sysvar/program keys, the minter's main address, its nonce accounts), `InsufficientFunds`, `InsufficientAllowance`, `AlreadyProcessing` (one withdrawal per principal at a time), and `TemporarilyUnavailable`.

## Who calls what

| Step | Frontend (user identity) | Backend canister |
|---|---|---|
| `get_deposit_address` | ✅ (owner = user) | ✅ |
| `deposit_sol` (needs cycles) | ❌ | ✅ passes `owner = opt user` |
| `deposit_sol_status` | ✅ query | ✅ |
| `icrc2_approve` + `withdraw_sol` | ✅ (burns from the user's own account) | ✅ only for tokens the canister owns (custodial subaccounts) |
| `withdraw_sol_status` | ✅ | ✅ |

Non-custodial pattern: the frontend shows the address, then calls the backend's `notifySolDeposit`, which calls `deposit_sol` for `owner = caller` with cycles. The frontend then polls `deposit_sol_status`, and the user withdraws directly from the frontend.

## Mistakes That Break Your Build

1. **Calling `deposit_sol` from the browser or without cycles.** It fails with `InsufficientCycles`. It must be called by a canister with `(with cycles = …)` / `.with_cycles(…)`, or via `icp canister call … --proxy <canister> --cycles <n>`.
2. **Omitting `owner` when a canister calls `get_deposit_address` / `deposit_sol`.** It defaults to the caller, which is your canister. The user's SOL is then looked up at, and minted to, the canister's account. Pass `owner = opt user`, and use the **same** `(owner, subaccount)` in both calls.
3. **Using stale API names from older docs.** There is no `process_deposit` and no transaction-signature argument, and the withdrawal endpoint is `withdraw_sol`, not `withdraw`. The minter reads the address **balance**, so the user never needs a transaction signature. Track the result with `deposit_sol_status(deposit_id)`.
4. **Expecting automatic detection on mainnet today.** Without `deposit_sol`, deposited SOL just sits on the deposit address. Nothing is lost, but nothing is minted until someone calls `deposit_sol`, or `watch_deposit_address` once it is deployed.
5. **Depositing below the minimum.** `ValueTooSmall { balance; minimum_deposit_amount }` is checked against the address balance, which includes the 890_880-lamport rent threshold left by earlier sweeps. Top up and call again. Each rejected call still costs your canister about 2.3B cycles.
6. **Sending SPL tokens (USDC on Solana, etc.) or using another chain.** Only native SOL is credited.
7. **Promising 1:1 on the first deposit.** The first sweep of an address keeps 890_880 lamports there, each sweep costs a 5_000-lamport share, and withdrawals cost `withdrawal_fee`. Show users `minted_amount` from `deposit_sol_status`.
8. **Unbounded `deposit_sol` relays.** Each accepted call spends about 47B cycles (about 0.07 USD) of **your** canister. Authenticate, rate-limit per user, and reject anonymous callers (see `canister-security`).
9. **Using `u64` vs `nat` incorrectly.** Minter amounts are `nat64` lamports (`Lamport`), and ledger amounts are `nat`. `deposit_sol_fee` and `deposit_sol_required_cycles` are `nat` cycles.
10. **Concurrent withdrawals from one principal.** `withdraw_sol` returns `AlreadyProcessing` while another withdrawal by the same principal is in progress. A custodial canister must serialize its withdrawals.

## Implementation: frontend (TypeScript)

The `@icp-sdk/canisters` package has no ckSOL module, so generate bindings from the deployed interface:

```bash
npm i @icp-sdk/core@^6 @icp-sdk/canisters@^4 @dfinity/utils@^5 @dfinity/ic-pub-key@^1 bs58@^6
icp canister metadata lh22c-kyaaa-aaaar-qb5nq-cai candid:service -n ic > cksol_minter.did
npx @icp-sdk/bindgen --did-file ./cksol_minter.did --out-dir ./src/bindings
```

```typescript
import { HttpAgent, type Identity } from "@icp-sdk/core/agent";
import { Principal } from "@icp-sdk/core/principal";
import { IcrcLedgerCanister } from "@icp-sdk/canisters/ledger/icrc";
import { createActor } from "./bindings/cksol_minter";
import { schnorr } from "@dfinity/ic-pub-key";
import bs58 from "bs58";

const CKSOL_MINTER = Principal.fromText("lh22c-kyaaa-aaaar-qb5nq-cai");
const CKSOL_LEDGER = Principal.fromText("ls5lp-lqaaa-aaaar-qb5oa-cai");

export async function ckSol(identity: Identity) {
  const agent = await HttpAgent.create({ identity });
  return {
    minter: createActor(CKSOL_MINTER.toText(), { agent }),
    ledger: IcrcLedgerCanister.create({ agent, canisterId: CKSOL_LEDGER }),
  };
}
type Ctx = Awaited<ReturnType<typeof ckSol>>;

// Deposit address: an update call; owner defaults to the caller when omitted.
export async function depositAddress({ minter }: Ctx, owner: Principal, subaccount?: Uint8Array) {
  return minter.get_deposit_address({ owner, subaccount }); // base58 Solana address
}

// Same address computed offline (no IC call): mainnet Ed25519 "key_1",
// path = [minter canister id, [0x01], owner principal bytes, 32-byte subaccount].
export function deriveDepositAddressOffline(owner: Principal, subaccount: Uint8Array = new Uint8Array(32)) {
  const master = schnorr.ed25519.PublicKeyWithChainCode.forMainnetKey("key_1");
  const path = new schnorr.ed25519.DerivationPath([
    CKSOL_MINTER.toUint8Array(), new Uint8Array([1]), owner.toUint8Array(), subaccount,
  ]);
  const hex = master.deriveSubkeyWithChainCode(path).public_key.toHex();
  return bs58.encode(Uint8Array.from(hex.match(/../g)!.map((b) => parseInt(b, 16))));
}

// Track a deposit queued by deposit_sol (called by your backend, which attaches cycles).
export async function depositStatus({ minter }: Ctx, depositId: bigint) {
  return minter.deposit_sol_status(depositId); // NotFound | Queued | Swept | Finalized | Minted | Dropped | Quarantined
}

export async function withdrawSol(ctx: Ctx, address: string, amountLamports: bigint) {
  const info = await ctx.minter.get_minter_info();
  if (amountLamports < info.minimum_withdrawal_amount) throw new Error("below minimum_withdrawal_amount");
  await ctx.ledger.approve({ spender: { owner: CKSOL_MINTER, subaccount: [] }, amount: amountLamports });
  const res = await ctx.minter.withdraw_sol({ address, amount: amountLamports });
  if (res.__kind__ === "Err") throw new Error(res.Err.__kind__);
  // recipient receives amountLamports - info.withdrawal_fee
  return res.Ok.block_index; // poll withdraw_sol_status({ block_index })
}

export async function withdrawStatus({ minter }: Ctx, blockIndex: bigint) {
  return minter.withdraw_sol_status({ block_index: blockIndex }); // NotFound | Pending | TxSent | TxFinalized
}
```

The user sends SOL with their own wallet (Phantom, Solflare, an exchange) to the returned address. No Solana SDK is needed in your app unless you want to build that transfer yourself.

## Implementation: backend relay for `deposit_sol`

### Rust

`Cargo.toml` dependencies: `ic-cdk = "0.19"`, `candid = "0.10"`, `serde = { version = "1", features = ["derive"] }`, `serde_bytes = "0.11"`.

```rust
use candid::{CandidType, Deserialize, Nat, Principal};
use ic_cdk::call::Call;
use ic_cdk::update;

const CKSOL_MINTER: &str = "lh22c-kyaaa-aaaar-qb5nq-cai";
const DEPOSIT_SOL_CYCLES: u128 = 1_000_000_000_000; // >= get_minter_info().deposit_sol_required_cycles; unused part is refunded

#[derive(CandidType, Deserialize)]
struct AccountArgs { owner: Option<Principal>, subaccount: Option<serde_bytes::ByteBuf> }

#[derive(CandidType, Deserialize, Debug)]
struct InsufficientCyclesError { expected: Nat, received: Nat }

#[derive(CandidType, Deserialize, Debug)]
enum DepositSolError {
    InsufficientCycles(InsufficientCyclesError),
    TemporarilyUnavailable(String),
    AlreadyProcessing,
    ValueTooSmall { balance: u64, minimum_deposit_amount: u64 },
    Quarantined { deposit_id: u64 },
}

fn minter() -> Principal { Principal::from_text(CKSOL_MINTER).unwrap() }

fn caller_not_anonymous() -> Principal {
    let caller = ic_cdk::api::msg_caller();
    assert_ne!(caller, Principal::anonymous(), "Authentication required");
    caller
}

/// Solana deposit address of the caller's own ckSOL account (owner = caller, default subaccount).
#[update]
async fn sol_deposit_address() -> Result<String, String> {
    let user = caller_not_anonymous();
    let (address,): (String,) = Call::unbounded_wait(minter(), "get_deposit_address")
        .with_arg(AccountArgs { owner: Some(user), subaccount: None })
        .await
        .map_err(|e| format!("{e:?}"))?
        .candid_tuple()
        .map_err(|e| format!("{e:?}"))?;
    Ok(address)
}

/// After the user sent SOL to the deposit address: pay the cycles and queue the sweep.
/// ckSOL is minted to the USER's account (owner = user), not to this canister.
#[update]
async fn notify_sol_deposit() -> Result<u64, String> {
    let user = caller_not_anonymous();
    // Abuse guard: this call spends ~47B cycles of THIS canister per successful deposit.
    // Add per-user rate limiting / an in-flight set in production (see canister-security skill).
    let (res,): (Result<u64, DepositSolError>,) = Call::unbounded_wait(minter(), "deposit_sol")
        .with_arg(AccountArgs { owner: Some(user), subaccount: None })
        .with_cycles(DEPOSIT_SOL_CYCLES)
        .await
        .map_err(|e| format!("deposit_sol rejected: {e:?}"))?
        .candid_tuple()
        .map_err(|e| format!("{e:?}"))?;
    res.map_err(|e| format!("{e:?}")) // Ok(deposit_id) -> poll deposit_sol_status(deposit_id)
}

ic_cdk::export_candid!();
```

### Motoko

```motoko
import Principal "mo:core/Principal";
import Runtime "mo:core/Runtime";

persistent actor {

  type DepositSolError = {
    #InsufficientCycles : { expected : Nat; received : Nat };
    #TemporarilyUnavailable : Text;
    #AlreadyProcessing;
    #ValueTooSmall : { balance : Nat64; minimum_deposit_amount : Nat64 };
    #Quarantined : { deposit_id : Nat64 };
  };

  transient let minter : actor {
    get_deposit_address : shared { owner : ?Principal; subaccount : ?Blob } -> async Text;
    deposit_sol : shared { owner : ?Principal; subaccount : ?Blob } -> async { #Ok : Nat64; #Err : DepositSolError };
  } = actor "lh22c-kyaaa-aaaar-qb5nq-cai";

  // >= get_minter_info().deposit_sol_required_cycles (1T on 2026-11); the unused part is refunded.
  transient let DEPOSIT_SOL_CYCLES = 1_000_000_000_000;

  // Solana deposit address of the caller's own ckSOL account.
  public shared ({ caller }) func solDepositAddress() : async Text {
    if (caller.isAnonymous()) { Runtime.trap("Authentication required") };
    await minter.get_deposit_address({ owner = ?caller; subaccount = null })
  };

  // After the user sent SOL: pay the cycles and queue the sweep. ckSOL is minted to the CALLER's account.
  // Spends ~47B cycles of this canister per accepted deposit: rate-limit per user in production.
  public shared ({ caller }) func notifySolDeposit() : async { #Ok : Nat64; #Err : DepositSolError } {
    if (caller.isAnonymous()) { Runtime.trap("Authentication required") };
    await (with cycles = DEPOSIT_SOL_CYCLES) minter.deposit_sol({ owner = ?caller; subaccount = null })
  };
};
```

## Verify It Works

```bash
# Fees, minimums, required cycles
icp canister call lh22c-kyaaa-aaaar-qb5nq-cai get_minter_info '()' -n ic --query

# Deposit address for a principal (update call; any caller)
icp canister call lh22c-kyaaa-aaaar-qb5nq-cai get_deposit_address \
  '(record { owner = opt principal "YOUR-PRINCIPAL"; subaccount = null })' -n ic
# Expected: ("7N9yLidkZCEvb1uWUQqRPD53KDUVXoghTF9gxJFBChDS") — a base58 Solana address

# After sending SOL: notify through a cycles-holding proxy canister you control
icp canister call lh22c-kyaaa-aaaar-qb5nq-cai deposit_sol \
  '(record { owner = opt principal "YOUR-PRINCIPAL"; subaccount = null })' \
  -n ic --proxy <PROXY_CANISTER_ID> --cycles 1000000000000
# Expected: (variant { Ok = 42 : nat64 })

icp canister call lh22c-kyaaa-aaaar-qb5nq-cai deposit_sol_status '(42 : nat64)' -n ic --query
# Expected eventually: (variant { Minted = record { block_index = …; minted_amount = … } })

# Withdraw 0.01 SOL
icp canister call ls5lp-lqaaa-aaaar-qb5oa-cai icrc2_approve \
  '(record { spender = record { owner = principal "lh22c-kyaaa-aaaar-qb5nq-cai"; subaccount = null }; amount = 10_000_000 : nat })' -n ic
icp canister call lh22c-kyaaa-aaaar-qb5nq-cai withdraw_sol \
  '(record { address = "<SOLANA_ADDRESS>"; amount = 10_000_000 : nat64; from_subaccount = null })' -n ic
icp canister call lh22c-kyaaa-aaaar-qb5nq-cai withdraw_sol_status '(record { block_index = <BLOCK_INDEX> : nat64 })' -n ic
```
