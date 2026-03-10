---
name: ckbtc
description: "Accept, send, and manage ckBTC (chain-key Bitcoin). Covers BTC deposit flow via minter, ckBTC transfers, withdrawal to BTC, subaccount derivation, and UTXO management. Use when integrating Bitcoin, ckBTC, BTC deposits, or BTC withdrawals in a canister. Do NOT use for plain token transfers without BTC minting/withdrawal — use icrc-ledger instead."
license: Apache-2.0
compatibility: "icp-cli >= 0.1.0"
metadata:
  title: ckBTC Integration
  category: DeFi
---

# Chain-Key Bitcoin (ckBTC) Integration

## What This Is

ckBTC is a 1:1 BTC-backed token native to the Internet Computer. No bridges, no wrapping, no third-party custodians. The ckBTC minter canister holds real BTC and mints/burns ckBTC tokens. Transfers settle in 1-2 seconds with a 10 satoshi fee (versus minutes and thousands of satoshis on Bitcoin L1).

## Prerequisites

- For Motoko: `mops` package manager, `core = "2.0.0"` in mops.toml
- For Rust: `ic-cdk`, `icrc-ledger-types`, `candid`, `serde`

## Canister IDs

### Bitcoin Mainnet

| Canister | ID |
|---|---|
| ckBTC Ledger | `mxzaz-hqaaa-aaaar-qaada-cai` |
| ckBTC Minter | `mqygn-kiaaa-aaaar-qaadq-cai` |
| ckBTC Index | `n5wcd-faaaa-aaaar-qaaea-cai` |
| ckBTC Checker | `oltsj-fqaaa-aaaar-qal5q-cai` |

### Bitcoin Testnet4

| Canister | ID |
|---|---|
| ckBTC Ledger | `mc6ru-gyaaa-aaaar-qaaaq-cai` |
| ckBTC Minter | `ml52i-qqaaa-aaaar-qaaba-cai` |
| ckBTC Index | `mm444-5iaaa-aaaar-qaabq-cai` |

## How It Works

### Deposit Flow (BTC -> ckBTC)

1. Call `get_btc_address` on the minter with the user's principal + subaccount. This returns a unique Bitcoin address controlled by the minter.
2. User sends BTC to that address using any Bitcoin wallet.
3. Wait for Bitcoin confirmations (the minter requires confirmations before minting).
4. Call `update_balance` on the minter with the same principal + subaccount. The minter checks for new UTXOs and mints equivalent ckBTC to the user's ICRC-1 account.

### Transfer Flow (ckBTC -> ckBTC)

Call `icrc1_transfer` on the ckBTC ledger. Fee is 10 satoshis. Settles in 1-2 seconds.

### Withdrawal Flow (ckBTC -> BTC)

1. Call `icrc2_approve` on the ckBTC ledger to grant the minter canister an allowance to spend from your account.
2. Call `retrieve_btc_with_approval` on the minter with `{ address, amount, from_subaccount: null }`.
3. The minter uses the approval to burn the ckBTC and submits a Bitcoin transaction.
4. The BTC arrives at the destination address after Bitcoin confirmations.

### Subaccount Generation

Each user gets a unique deposit address derived from their principal + an optional 32-byte subaccount. To give each user a distinct deposit address within your canister, derive subaccounts from a user-specific identifier (their principal or a sequential ID).

## Mistakes That Break Your Build

1. **Using the wrong minter canister ID.** The minter ID is `mqygn-kiaaa-aaaar-qaadq-cai`. Do not confuse it with the ledger (`mxzaz-...`) or index (`n5wcd-...`).

2. **Forgetting the 10 satoshi transfer fee.** Every `icrc1_transfer` deducts 10 satoshis beyond the amount. If the user has exactly 1000 satoshis and you transfer 1000, it fails with `InsufficientFunds`. Transfer `balance - 10` instead.

3. **Not calling `update_balance` after a BTC deposit.** Sending BTC to the deposit address does nothing until you call `update_balance`. The minter does not auto-detect deposits. Your app must call this.

4. **Using Account Identifier instead of ICRC-1 Account.** ckBTC uses the ICRC-1 standard: `{ owner: Principal, subaccount: ?Blob }`. Do NOT use the legacy `AccountIdentifier` (hex string) from the ICP ledger.

5. **Subaccount must be exactly 32 bytes or null.** Passing a subaccount shorter or longer than 32 bytes causes a trap. Pad with leading zeros if deriving from a shorter value.

6. **Calling `retrieve_btc` with amount below the minimum.** The minter has a minimum withdrawal amount (currently 50,000 satoshis / 0.0005 BTC). Below this, you get `AmountTooLow`.

7. **Not checking the `retrieve_btc` response for errors.** The response is a variant: `Ok` contains `{ block_index }`, `Err` contains specific errors like `MalformedAddress`, `InsufficientFunds`, `TemporarilyUnavailable`. Always match both arms.

8. **Forgetting `owner` in `get_btc_address` args.** If you omit `owner`, Candid sub-typing assigns null, and the minter returns the deposit address of the caller (the canister) instead of the user.

## Implementation

### Motoko

#### mops.toml

```toml
[package]
name = "ckbtc-app"
version = "0.1.0"

[dependencies]
core = "2.0.0"
icrc2-types = "1.1.0"
```

#### icp.yaml

Your backend canister calls the ckBTC ledger and minter by principal directly — no local ckBTC canister deployment needed.

```yaml
canisters:
  - name: backend
    recipe:
      type: "@dfinity/motoko@v4.1.0"
      configuration:
        main: src/backend/main.mo
```

#### src/backend/main.mo

```motoko
import Principal "mo:core/Principal";
import Blob "mo:core/Blob";
import Nat "mo:core/Nat";
import Nat8 "mo:core/Nat8";
import Nat64 "mo:core/Nat64";
import Array "mo:core/Array";
import Result "mo:core/Result";
import Error "mo:core/Error";
import Runtime "mo:core/Runtime";

persistent actor Self {

  // -- Types --

  type Account = {
    owner : Principal;
    subaccount : ?Blob;
  };

  type TransferArgs = {
    from_subaccount : ?Blob;
    to : Account;
    amount : Nat;
    fee : ?Nat;
    memo : ?Blob;
    created_at_time : ?Nat64;
  };

  type TransferResult = {
    #Ok : Nat; // block index
    #Err : TransferError;
  };

  type TransferError = {
    #BadFee : { expected_fee : Nat };
    #BadBurn : { min_burn_amount : Nat };
    #InsufficientFunds : { balance : Nat };
    #TooOld;
    #CreatedInFuture : { ledger_time : Nat64 };
    #Duplicate : { duplicate_of : Nat };
    #TemporarilyUnavailable;
    #GenericError : { error_code : Nat; message : Text };
  };

  type UpdateBalanceResult = {
    #Ok : [UtxoStatus];
    #Err : UpdateBalanceError;
  };

  type UtxoStatus = {
    #ValueTooSmall : Utxo;
    #Tainted : Utxo;
    #Checked : Utxo;
    #Minted : { block_index : Nat64; minted_amount : Nat64; utxo : Utxo };
  };

  type Utxo = {
    outpoint : { txid : Blob; vout : Nat32 };
    value : Nat64;
    height : Nat32;
  };

  type UpdateBalanceError = {
    #NoNewUtxos : {
      required_confirmations : Nat32;
      pending_utxos : ?[PendingUtxo];
      current_confirmations : ?Nat32;
    };
    #AlreadyProcessing;
    #TemporarilyUnavailable : Text;
    #GenericError : { error_code : Nat64; error_message : Text };
  };

  type PendingUtxo = {
    outpoint : { txid : Blob; vout : Nat32 };
    value : Nat64;
    confirmations : Nat32;
  };

  type ApproveArgs = {
    from_subaccount : ?Blob;
    spender : Account;
    amount : Nat;
    expected_allowance : ?Nat;
    expires_at : ?Nat64;
    fee : ?Nat;
    memo : ?Blob;
    created_at_time : ?Nat64;
  };

  type ApproveError = {
    #BadFee : { expected_fee : Nat };
    #InsufficientFunds : { balance : Nat };
    #AllowanceChanged : { current_allowance : Nat };
    #Expired : { ledger_time : Nat64 };
    #TooOld;
    #CreatedInFuture : { ledger_time : Nat64 };
    #Duplicate : { duplicate_of : Nat };
    #TemporarilyUnavailable;
    #GenericError : { error_code : Nat; message : Text };
  };

  type RetrieveBtcWithApprovalArgs = {
    address : Text;
    amount : Nat64;
    from_subaccount : ?Blob;
  };

  type RetrieveBtcResult = {
    #Ok : { block_index : Nat64 };
    #Err : RetrieveBtcError;
  };

  type RetrieveBtcError = {
    #MalformedAddress : Text;
    #AlreadyProcessing;
    #AmountTooLow : Nat64;
    #InsufficientFunds : { balance : Nat64 };
    #InsufficientAllowance : { allowance : Nat64 };
    #TemporarilyUnavailable : Text;
    #GenericError : { error_code : Nat64; error_message : Text };
  };

  // -- Remote canister references (mainnet) --

  transient let ckbtcLedger : actor {
    icrc1_transfer : shared (TransferArgs) -> async TransferResult;
    icrc1_balance_of : shared query (Account) -> async Nat;
    icrc1_fee : shared query () -> async Nat;
    icrc2_approve : shared (ApproveArgs) -> async { #Ok : Nat; #Err : ApproveError };
  } = actor "mxzaz-hqaaa-aaaar-qaada-cai";

  transient let ckbtcMinter : actor {
    get_btc_address : shared ({
      owner : ?Principal;
      subaccount : ?Blob;
    }) -> async Text;
    update_balance : shared ({
      owner : ?Principal;
      subaccount : ?Blob;
    }) -> async UpdateBalanceResult;
    retrieve_btc_with_approval : shared (RetrieveBtcWithApprovalArgs) -> async RetrieveBtcResult;
  } = actor "mqygn-kiaaa-aaaar-qaadq-cai";

  // -- Subaccount derivation --
  // Derive a 32-byte subaccount from a principal for per-user deposit addresses.

  func principalToSubaccount(p : Principal) : Blob {
    let bytes = Blob.toArray(Principal.toBlob(p));
    let size = bytes.size();
    // First byte is length, remaining padded to 32 bytes
    let sub = Array.tabulate<Nat8>(32, func(i : Nat) : Nat8 {
      if (i == 0) { Nat8.fromNat(size) }
      else if (i <= size) { bytes[i - 1] }
      else { 0 }
    });
    Blob.fromArray(sub)
  };

  // -- Deposit: Get user's BTC deposit address --

  public shared ({ caller }) func getDepositAddress() : async Text {
    if (Principal.isAnonymous(caller)) { Runtime.trap("Authentication required") };
    let subaccount = principalToSubaccount(caller);
    await ckbtcMinter.get_btc_address({
      owner = ?Principal.fromActor(Self);
      subaccount = ?subaccount;
    })
  };

  // -- Deposit: Check for new BTC and mint ckBTC --

  public shared ({ caller }) func updateBalance() : async UpdateBalanceResult {
    if (Principal.isAnonymous(caller)) { Runtime.trap("Authentication required") };
    let subaccount = principalToSubaccount(caller);
    await ckbtcMinter.update_balance({
      owner = ?Principal.fromActor(Self);
      subaccount = ?subaccount;
    })
  };

  // -- Check user's ckBTC balance --

  public shared ({ caller }) func getBalance() : async Nat {
    if (Principal.isAnonymous(caller)) { Runtime.trap("Authentication required") };
    let subaccount = principalToSubaccount(caller);
    await ckbtcLedger.icrc1_balance_of({
      owner = Principal.fromActor(Self);
      subaccount = ?subaccount;
    })
  };

  // -- Transfer ckBTC to another user --

  public shared ({ caller }) func transfer(to : Principal, amount : Nat) : async TransferResult {
    if (Principal.isAnonymous(caller)) { Runtime.trap("Authentication required") };
    let fromSubaccount = principalToSubaccount(caller);
    await ckbtcLedger.icrc1_transfer({
      from_subaccount = ?fromSubaccount;
      to = { owner = to; subaccount = null };
      amount = amount;
      fee = ?10; // 10 satoshis
      memo = null;
      created_at_time = null;
    })
  };

  // -- Withdraw: Convert ckBTC back to BTC --

  public shared ({ caller }) func withdraw(btcAddress : Text, amount : Nat64) : async RetrieveBtcResult {
    if (Principal.isAnonymous(caller)) { Runtime.trap("Authentication required") };

    // Step 1: Approve the minter to spend ckBTC from the user's subaccount
    let fromSubaccount = principalToSubaccount(caller);
    let approveResult = await ckbtcLedger.icrc2_approve({
      from_subaccount = ?fromSubaccount;
      spender = {
        owner = Principal.fromText("mqygn-kiaaa-aaaar-qaadq-cai");
        subaccount = null;
      };
      amount = Nat64.toNat(amount) + 10; // amount + fee for the minter's burn
      expected_allowance = null;
      expires_at = null;
      fee = ?10;
      memo = null;
      created_at_time = null;
    });

    switch (approveResult) {
      case (#Err(e)) { return #Err(#GenericError({ error_code = 0; error_message = "Approve for minter failed" })) };
      case (#Ok(_)) {};
    };

    // Step 2: Call retrieve_btc_with_approval on the minter
    await ckbtcMinter.retrieve_btc_with_approval({
      address = btcAddress;
      amount = amount;
      from_subaccount = ?fromSubaccount;
    })
  };
};
```

### Rust

#### Cargo.toml

```toml
[package]
name = "ckbtc_backend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
ic-cdk = "0.19"
ic-cdk-timers = "1.0"
candid = "0.10"
serde = { version = "1", features = ["derive"] }
serde_bytes = "0.11"
icrc-ledger-types = "0.1"
```

#### src/lib.rs

```rust
use candid::{CandidType, Deserialize, Nat, Principal};
use ic_cdk::update;
use ic_cdk::call::Call;
use icrc_ledger_types::icrc1::account::Account;
use icrc_ledger_types::icrc1::transfer::{TransferArg, TransferError};
use icrc_ledger_types::icrc2::approve::{ApproveArgs, ApproveError};

// -- Canister IDs --
const CKBTC_LEDGER: &str = "mxzaz-hqaaa-aaaar-qaada-cai";
const CKBTC_MINTER: &str = "mqygn-kiaaa-aaaar-qaadq-cai";

// -- Minter types --

#[derive(CandidType, Deserialize, Debug)]
struct GetBtcAddressArgs {
    owner: Option<Principal>,
    subaccount: Option<Vec<u8>>,
}

#[derive(CandidType, Deserialize, Debug)]
struct UpdateBalanceArgs {
    owner: Option<Principal>,
    subaccount: Option<Vec<u8>>,
}

#[derive(CandidType, Deserialize, Debug)]
struct RetrieveBtcWithApprovalArgs {
    address: String,
    amount: u64,
    from_subaccount: Option<Vec<u8>>,
}

#[derive(CandidType, Deserialize, Debug)]
struct RetrieveBtcOk {
    block_index: u64,
}

#[derive(CandidType, Deserialize, Debug)]
enum RetrieveBtcError {
    MalformedAddress(String),
    AlreadyProcessing,
    AmountTooLow(u64),
    InsufficientFunds { balance: u64 },
    InsufficientAllowance { allowance: u64 },
    TemporarilyUnavailable(String),
    GenericError { error_code: u64, error_message: String },
}

#[derive(CandidType, Deserialize, Debug)]
struct Utxo {
    outpoint: OutPoint,
    value: u64,
    height: u32,
}

#[derive(CandidType, Deserialize, Debug)]
struct OutPoint {
    txid: Vec<u8>,
    vout: u32,
}

#[derive(CandidType, Deserialize, Debug)]
struct PendingUtxo {
    outpoint: OutPoint,
    value: u64,
    confirmations: u32,
}

#[derive(CandidType, Deserialize, Debug)]
enum UtxoStatus {
    ValueTooSmall(Utxo),
    Tainted(Utxo),
    Checked(Utxo),
    Minted {
        block_index: u64,
        minted_amount: u64,
        utxo: Utxo,
    },
}

#[derive(CandidType, Deserialize, Debug)]
enum UpdateBalanceError {
    NoNewUtxos {
        required_confirmations: u32,
        pending_utxos: Option<Vec<PendingUtxo>>,
        current_confirmations: Option<u32>,
    },
    AlreadyProcessing,
    TemporarilyUnavailable(String),
    GenericError { error_code: u64, error_message: String },
}

type UpdateBalanceResult = Result<Vec<UtxoStatus>, UpdateBalanceError>;
type RetrieveBtcResult = Result<RetrieveBtcOk, RetrieveBtcError>;

// -- Subaccount derivation --
// Derive a 32-byte subaccount from a principal for per-user deposit addresses.

fn principal_to_subaccount(principal: &Principal) -> [u8; 32] {
    let mut subaccount = [0u8; 32];
    let principal_bytes = principal.as_slice();
    subaccount[0] = principal_bytes.len() as u8;
    subaccount[1..1 + principal_bytes.len()].copy_from_slice(principal_bytes);
    subaccount
}

fn ledger_id() -> Principal {
    Principal::from_text(CKBTC_LEDGER).unwrap()
}

fn minter_id() -> Principal {
    Principal::from_text(CKBTC_MINTER).unwrap()
}

// -- Deposit: Get user's BTC deposit address --

#[update]
async fn get_deposit_address() -> String {
    let caller = ic_cdk::api::msg_caller();
    assert_ne!(caller, Principal::anonymous(), "Authentication required");

    let subaccount = principal_to_subaccount(&caller);
    let args = GetBtcAddressArgs {
        owner: Some(ic_cdk::api::canister_self()),
        subaccount: Some(subaccount.to_vec()),
    };

    let (address,): (String,) = Call::unbounded_wait(minter_id(), "get_btc_address")
        .with_arg(args)
        .await
        .expect("Failed to get BTC address")
        .candid_tuple()
        .expect("Failed to decode response");

    address
}

// -- Deposit: Check for new BTC and mint ckBTC --

#[update]
async fn update_balance() -> UpdateBalanceResult {
    let caller = ic_cdk::api::msg_caller();
    assert_ne!(caller, Principal::anonymous(), "Authentication required");

    let subaccount = principal_to_subaccount(&caller);
    let args = UpdateBalanceArgs {
        owner: Some(ic_cdk::api::canister_self()),
        subaccount: Some(subaccount.to_vec()),
    };

    let (result,): (UpdateBalanceResult,) = Call::unbounded_wait(minter_id(), "update_balance")
        .with_arg(args)
        .await
        .expect("Failed to call update_balance")
        .candid_tuple()
        .expect("Failed to decode response");

    result
}

// -- Check user's ckBTC balance --

#[update]
async fn get_balance() -> Nat {
    let caller = ic_cdk::api::msg_caller();
    assert_ne!(caller, Principal::anonymous(), "Authentication required");

    let subaccount = principal_to_subaccount(&caller);
    let account = Account {
        owner: ic_cdk::api::canister_self(),
        subaccount: Some(subaccount),
    };

    let (balance,): (Nat,) = Call::unbounded_wait(ledger_id(), "icrc1_balance_of")
        .with_arg(account)
        .await
        .expect("Failed to get balance")
        .candid_tuple()
        .expect("Failed to decode response");

    balance
}

// -- Transfer ckBTC to another user --

#[update]
async fn transfer(to: Principal, amount: Nat) -> Result<Nat, TransferError> {
    let caller = ic_cdk::api::msg_caller();
    assert_ne!(caller, Principal::anonymous(), "Authentication required");

    let from_subaccount = principal_to_subaccount(&caller);
    let args = TransferArg {
        from_subaccount: Some(from_subaccount),
        to: Account {
            owner: to,
            subaccount: None,
        },
        amount,
        fee: Some(Nat::from(10u64)), // 10 satoshis
        memo: None,
        created_at_time: None,
    };

    let (result,): (Result<Nat, TransferError>,) = Call::unbounded_wait(ledger_id(), "icrc1_transfer")
            .with_arg(args)
            .await
            .expect("Failed to call icrc1_transfer")
            .candid_tuple()
            .expect("Failed to decode response");

    result
}

// -- Withdraw: Convert ckBTC back to BTC --

#[update]
async fn withdraw(btc_address: String, amount: u64) -> RetrieveBtcResult {
    let caller = ic_cdk::api::msg_caller();
    assert_ne!(caller, Principal::anonymous(), "Authentication required");

    // Step 1: Approve the minter to spend ckBTC from the user's subaccount
    let from_subaccount = principal_to_subaccount(&caller);
    let approve_args = ApproveArgs {
        from_subaccount: Some(from_subaccount),
        spender: Account {
            owner: minter_id(),
            subaccount: None,
        },
        amount: Nat::from(amount) + Nat::from(10u64), // amount + fee for the minter's burn
        expected_allowance: None,
        expires_at: None,
        fee: Some(Nat::from(10u64)),
        memo: None,
        created_at_time: None,
    };

    let (approve_result,): (Result<Nat, ApproveError>,) = Call::unbounded_wait(ledger_id(), "icrc2_approve")
            .with_arg(approve_args)
            .await
            .expect("Failed to call icrc2_approve")
            .candid_tuple()
            .expect("Failed to decode response");

    if let Err(e) = approve_result {
        return Err(RetrieveBtcError::GenericError {
            error_code: 0,
            error_message: format!("Approve for minter failed: {:?}", e),
        });
    }

    // Step 2: Call retrieve_btc_with_approval on the minter
    let args = RetrieveBtcWithApprovalArgs {
        address: btc_address,
        amount,
        from_subaccount: Some(from_subaccount.to_vec()),
    };

    let (result,): (RetrieveBtcResult,) = Call::unbounded_wait(minter_id(), "retrieve_btc_with_approval")
            .with_arg(args)
            .await
            .expect("Failed to call retrieve_btc_with_approval")
            .candid_tuple()
            .expect("Failed to decode response");

    result
}

// -- Export Candid interface --
ic_cdk::export_candid!();
```

## Deploy & Test

### Local Development

There is no local ckBTC minter. For local testing, mock the minter interface or test against mainnet/testnet.

### Deploy to Mainnet

```bash
# Deploy your backend canister
icp deploy backend -e ic

# Your canister calls the mainnet ckBTC canisters directly by principal
```

### Using icp to Interact with ckBTC Directly

```bash
# Check ckBTC balance for an account
icp canister call mxzaz-hqaaa-aaaar-qaada-cai icrc1_balance_of \
  '(record { owner = principal "YOUR-PRINCIPAL"; subaccount = null })' \
  -e ic

# Get deposit address
icp canister call mqygn-kiaaa-aaaar-qaadq-cai get_btc_address \
  '(record { owner = opt principal "YOUR-PRINCIPAL"; subaccount = null })' \
  -e ic

# Check for new deposits and mint ckBTC
icp canister call mqygn-kiaaa-aaaar-qaadq-cai update_balance \
  '(record { owner = opt principal "YOUR-PRINCIPAL"; subaccount = null })' \
  -e ic

# Transfer ckBTC (amount in e8s — 1 ckBTC = 100_000_000)
icp canister call mxzaz-hqaaa-aaaar-qaada-cai icrc1_transfer \
  '(record {
    to = record { owner = principal "RECIPIENT-PRINCIPAL"; subaccount = null };
    amount = 100_000;
    fee = opt 10;
    memo = null;
    from_subaccount = null;
    created_at_time = null;
  })' -e ic

# Withdraw ckBTC to a BTC address (amount in satoshis, minimum 50_000)
# Note: In production, use icrc2_approve + retrieve_btc_with_approval (see withdraw function above)
icp canister call mqygn-kiaaa-aaaar-qaadq-cai retrieve_btc_with_approval \
  '(record { address = "bc1q...your-btc-address"; amount = 50_000; from_subaccount = null })' \
  -e ic

# Check transfer fee
icp canister call mxzaz-hqaaa-aaaar-qaada-cai icrc1_fee '()' -e ic
```

## Verify It Works

### Check Balance

```bash
icp canister call mxzaz-hqaaa-aaaar-qaada-cai icrc1_balance_of \
  '(record { owner = principal "YOUR-PRINCIPAL"; subaccount = null })' \
  -e ic
# Expected: (AMOUNT : nat) — balance in satoshis (e8s)
```

### Verify Transfer

```bash
# Transfer 1000 satoshis
icp canister call mxzaz-hqaaa-aaaar-qaada-cai icrc1_transfer \
  '(record {
    to = record { owner = principal "RECIPIENT"; subaccount = null };
    amount = 1_000;
    fee = opt 10;
    memo = null;
    from_subaccount = null;
    created_at_time = null;
  })' -e ic
# Expected: (variant { Ok = BLOCK_INDEX : nat })

# Verify recipient received it
icp canister call mxzaz-hqaaa-aaaar-qaada-cai icrc1_balance_of \
  '(record { owner = principal "RECIPIENT"; subaccount = null })' \
  -e ic
# Expected: balance increased by 1000
```

### Verify Deposit Flow

```bash
# 1. Get deposit address
icp canister call YOUR-CANISTER getDepositAddress -e ic
# Expected: "bc1q..." or "3..." — a valid Bitcoin address

# 2. Send BTC to that address (external wallet)

# 3. Check for new deposits
icp canister call YOUR-CANISTER updateBalance -e ic
# Expected: (variant { Ok = vec { variant { Minted = record { ... } } } })

# 4. Check ckBTC balance
icp canister call YOUR-CANISTER getBalance -e ic
# Expected: balance reflects minted ckBTC
```

### Verify Withdrawal

```bash
icp canister call YOUR-CANISTER withdraw '("bc1q...destination", 50_000 : nat64)' -e ic
# Expected: (variant { Ok = record { block_index = BLOCK_INDEX : nat64 } })
# The BTC will arrive at the destination address after Bitcoin confirmations
```
