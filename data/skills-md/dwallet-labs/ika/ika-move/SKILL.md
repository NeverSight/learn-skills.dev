---
name: ika-move
description: Guide for integrating Ika dWallet 2PC-MPC protocol into Sui Move contracts. Use when building Move contracts that need cross-chain signing, dWallet creation, presigning, signing, future signing, key importing, or any Ika on-chain integration. Triggers on Move/Sui contract tasks involving dWallets, cross-chain signing, or Ika protocol operations.
---

# Ika Move Integration

Build Sui Move contracts integrating Ika dWallet 2PC-MPC for programmable cross-chain signing.

## References (detailed patterns and complete code)

- `references/protocols-detailed.md` - All coordinator function signatures with full parameter lists
- `references/patterns.md` - Complete integration patterns: treasury, DAO governance, imported key wallet, presign pool, events, enums
- `references/typescript-integration.md` - Full TypeScript SDK flows: DKG prep, signing, key import, polling, IkaTransaction API

## Setup

### Move.toml

```toml
[package]
name = "my_project"
edition = "2024.beta"

[dependencies]
Sui = { git = "https://github.com/MystenLabs/sui.git", subdir = "crates/sui-framework/packages/sui-framework", rev = "framework/testnet" }
ika_dwallet_2pc_mpc = { git = "https://github.com/dwallet-labs/ika.git", subdir = "deployed_contracts/testnet/ika_dwallet_2pc_mpc", rev = "main" }
ika = { git = "https://github.com/dwallet-labs/ika.git", subdir = "deployed_contracts/testnet/ika", rev = "main" }

[addresses]
my_project = "0x0"
```

For mainnet: change `testnet` to `mainnet` in paths.

### TypeScript SDK

```bash
pnpm add @ika.xyz/sdk
```

```typescript
import { getNetworkConfig, IkaClient } from '@ika.xyz/sdk';
import { getJsonRpcFullnodeUrl, SuiJsonRpcClient } from '@mysten/sui/jsonRpc';
const suiClient = new SuiJsonRpcClient({ url: getJsonRpcFullnodeUrl('testnet'), network: 'testnet' });
const ikaClient = new IkaClient({ suiClient, config: getNetworkConfig('testnet'), cache: true });
await ikaClient.initialize();
```

## Crypto Constants

### Curves
- `0` = SECP256K1 (Bitcoin, Ethereum)
- `1` = SECP256R1 (WebAuthn)
- `2` = ED25519 (Solana, Substrate)
- `3` = RISTRETTO (Privacy)

### Signature Algorithms (relative to curve)
- SECP256K1: `0`=ECDSA, `1`=Taproot
- SECP256R1: `0`=ECDSA
- ED25519: `0`=EdDSA
- RISTRETTO: `0`=Schnorrkel

### Hash Schemes (relative to curve+algo)
- SECP256K1+ECDSA: `0`=KECCAK256(Ethereum), `1`=SHA256, `2`=DoubleSHA256(Bitcoin)
- SECP256K1+Taproot: `0`=SHA256
- SECP256R1+ECDSA: `0`=SHA256
- ED25519+EdDSA: `0`=SHA512
- RISTRETTO+Schnorrkel: `0`=Merlin

## Core Imports

```rust
use ika::ika::IKA;
use ika_dwallet_2pc_mpc::{
    coordinator::DWalletCoordinator,
    coordinator_inner::{
        DWalletCap, ImportedKeyDWalletCap,
        UnverifiedPresignCap, VerifiedPresignCap,
        UnverifiedPartialUserSignatureCap, VerifiedPartialUserSignatureCap,
        MessageApproval, ImportedKeyMessageApproval
    },
    sessions_manager::SessionIdentifier
};
use sui::{balance::Balance, coin::Coin, sui::SUI};
```

## Contract Template

```rust
public struct MyContract has key, store {
    id: UID,
    dwallet_cap: DWalletCap,
    presigns: vector<UnverifiedPresignCap>,
    ika_balance: Balance<IKA>,
    sui_balance: Balance<SUI>,
    dwallet_network_encryption_key_id: ID,
}
```

### Required Helpers

```rust
fun random_session(coordinator: &mut DWalletCoordinator, ctx: &mut TxContext): SessionIdentifier {
    coordinator.register_session_identifier(ctx.fresh_object_address().to_bytes(), ctx)
}

fun withdraw_payment_coins(self: &mut MyContract, ctx: &mut TxContext): (Coin<IKA>, Coin<SUI>) {
    let ika = self.ika_balance.withdraw_all().into_coin(ctx);
    let sui = self.sui_balance.withdraw_all().into_coin(ctx);
    (ika, sui)
}

fun return_payment_coins(self: &mut MyContract, ika: Coin<IKA>, sui: Coin<SUI>) {
    self.ika_balance.join(ika.into_balance());
    self.sui_balance.join(sui.into_balance());
}

public fun add_ika_balance(self: &mut MyContract, coin: Coin<IKA>) {
    self.ika_balance.join(coin.into_balance());
}

public fun add_sui_balance(self: &mut MyContract, coin: Coin<SUI>) {
    self.sui_balance.join(coin.into_balance());
}
```

## DWalletCoordinator

Central shared object for all operations. Pass as `&mut DWalletCoordinator` for mutations, `&DWalletCoordinator` for reads.

Get ID in TypeScript: `ikaClient.ikaConfig.objects.ikaDWalletCoordinator.objectID`

## Capabilities

| Capability | Purpose | Created By |
|---|---|---|
| `DWalletCap` | Authorize signing | DKG |
| `ImportedKeyDWalletCap` | Authorize imported key signing | Import verification |
| `UnverifiedPresignCap` | Presign reference (needs verify) | Presign request |
| `VerifiedPresignCap` | Ready for signing | `verify_presign_cap()` |
| `UnverifiedPartialUserSignatureCap` | Partial sig (needs verify) | Future sign |
| `VerifiedPartialUserSignatureCap` | Ready for completion | `verify_partial_user_signature_cap()` |
| `MessageApproval` | Auth to sign specific message | `approve_message()` |
| `ImportedKeyMessageApproval` | Auth for imported keys | `approve_imported_key_message()` |

## SessionIdentifier

Every protocol op needs a unique `SessionIdentifier`. Create via:

```rust
let session = coordinator.register_session_identifier(ctx.fresh_object_address().to_bytes(), ctx);
```

Rules: create just before use, never reuse, one per operation.

## Payment Pattern

All ops require IKA+SUI fees. Pattern: withdraw all -> perform ops (fees auto-deducted from `&mut Coin`) -> return remainder.

## Protocol: DKG (Create dWallet)

### Shared dWallet (recommended for contracts)
Public user share, network signs without user interaction.

```rust
let (dwallet_cap, _) = coordinator.request_dwallet_dkg_with_public_user_secret_key_share(
    dwallet_network_encryption_key_id, curve,
    centralized_public_key_share_and_proof, user_public_output, public_user_secret_key_share,
    option::none(), // sign_during_dkg_request
    session, &mut ika, &mut sui, ctx,
);
```

### Zero-Trust dWallet
Encrypted user share, user must participate in every signature.

```rust
let (dwallet_cap, _) = coordinator.request_dwallet_dkg(
    dwallet_network_encryption_key_id, curve,
    centralized_public_key_share_and_proof, encrypted_centralized_secret_share_and_proof,
    encryption_key_address, user_public_output, signer_public_key,
    option::none(), session, &mut ika, &mut sui, ctx,
);
```

**Important:** After zero-trust DKG (or key import), the dWallet is in `AwaitingKeyHolderSignature` state. The user must call `acceptEncryptedUserShare` to transition the dWallet to `Active` state before it can be used for signing:

```typescript
// Wait for DKG to complete and dWallet to reach AwaitingKeyHolderSignature state
const awaitingDWallet = await ikaClient.getDWalletInParticularState(dwalletId, 'AwaitingKeyHolderSignature');
// The encrypted user secret key share ID comes from the DKG transaction event,
// NOT from the dWallet ID.
const encryptedShare = await ikaClient.getEncryptedUserSecretKeyShare(encryptedUserSecretKeyShareId);

const tx = new Transaction();
const ikaTx = new IkaTransaction({ ikaClient, transaction: tx, userShareEncryptionKeys: keys });
await ikaTx.acceptEncryptedUserShare({
    dWallet: awaitingDWallet,
    encryptedUserSecretKeyShareId: encryptedShare.id,
    userPublicOutput: new Uint8Array(dkgData.userPublicOutput),
});
await suiClient.core.signAndExecuteTransaction({ transaction: tx, signer: keypair });

// dWallet is now Active and ready for signing
const activeDWallet = await ikaClient.getDWalletInParticularState(dwalletId, 'Active');
```

This step is NOT needed for shared dWallets (created with `request_dwallet_dkg_with_public_user_secret_key_share`).

### TypeScript DKG Prep

```typescript
import { prepareDKGAsync, UserShareEncryptionKeys, Curve, createRandomSessionIdentifier } from '@ika.xyz/sdk';
const keys = await UserShareEncryptionKeys.fromRootSeedKey(seed, Curve.SECP256K1);
const bytesToHash = createRandomSessionIdentifier(); // bytes hashed to derive the session identifier
const dkgData = await prepareDKGAsync(ikaClient, Curve.SECP256K1, keys, bytesToHash, signerAddress);
const networkKey = await ikaClient.getLatestNetworkEncryptionKey();
// dkgData has: userDKGMessage, userPublicOutput, encryptedUserShareAndProof, userSecretKeyShare
```

### Sign During DKG (optional)
Pass existing presign to get signature during DKG:

```rust
let sign_req = coordinator.sign_during_dkg_request(verified_presign, hash_scheme, message, msg_sig);
// Pass option::some(sign_req) instead of option::none() in DKG call
```

## Protocol: Presigning

Each signature consumes one presign. Manage a pool.

### Global Presign (most common: Taproot, EdDSA, Schnorr, ECDSA)

```rust
let cap = coordinator.request_global_presign(
    dwallet_network_encryption_key_id, curve, signature_algorithm,
    session, &mut ika, &mut sui, ctx,
);
self.presigns.push_back(cap);
```

### dWallet-Specific Presign (ECDSA with imported keys)

```rust
let cap = coordinator.request_presign(
    dwallet_id, signature_algorithm, session, &mut ika, &mut sui, ctx,
);
```

### Verify Before Use

```rust
let is_ready = coordinator.is_presign_valid(&unverified_cap);
let verified = coordinator.verify_presign_cap(unverified_cap, ctx); // fails if not ready
```

### Pool Management

```rust
// Pop from pool
let unverified = self.presigns.swap_remove(0);

// Auto-replenish after signing
if (self.presigns.length() < MIN_POOL) {
    let s = random_session(coordinator, ctx);
    self.presigns.push_back(coordinator.request_global_presign(
        self.dwallet_network_encryption_key_id, curve, sig_algo, s, &mut ika, &mut sui, ctx,
    ));
};

// Batch add
let mut i = 0;
while (i < count) {
    let s = random_session(coordinator, ctx);
    self.presigns.push_back(coordinator.request_global_presign(..., s, &mut ika, &mut sui, ctx));
    i = i + 1;
};
```

## Protocol: Direct Signing

Single-phase, immediate signature. Use when no governance needed.

```rust
// 1. Verify presign
let verified = coordinator.verify_presign_cap(self.presigns.swap_remove(0), ctx);

// 2. Approve message
let approval = coordinator.approve_message(&self.dwallet_cap, sig_algo, hash_scheme, message);

// 3. Sign
let sign_id = coordinator.request_sign_and_return_id(
    verified, approval, message_centralized_signature, session, &mut ika, &mut sui, ctx,
);
// Also: coordinator.request_sign(...) without return ID
```

### TypeScript: Create User Signature

```typescript
import { createUserSignMessageWithPublicOutput, Curve, SignatureAlgorithm, Hash } from '@ika.xyz/sdk';
const completedPresign = await ikaClient.getPresignInParticularState(presignId, 'Completed');
const protocolPublicParameters = await ikaClient.getProtocolPublicParameters(undefined, Curve.SECP256K1);
const msgSig = await createUserSignMessageWithPublicOutput(
    protocolPublicParameters,
    dWallet.state.Active!.public_output,
    dWallet.public_user_secret_key_share,
    completedPresign.presign,
    message,
    Hash.SHA256,
    SignatureAlgorithm.Taproot,
    Curve.SECP256K1,
);
// Pass msgSig as message_centralized_signature to Move
```

### Retrieve Signature

```typescript
const signSession = await ikaClient.getSignInParticularState(
    signId, Curve.SECP256K1, SignatureAlgorithm.Taproot, 'Completed',
);
const sig = await parseSignatureFromSignOutput(Curve.SECP256K1, SignatureAlgorithm.Taproot, signSession.signature);
```

## Protocol: Future Signing (Two-Phase)

Separates commitment from execution. For governance/multisig/delayed signing.

### Phase 1: Create Partial Signature

```rust
let partial_cap = coordinator.request_future_sign(
    self.dwallet_cap.dwallet_id(), verified_presign, message, hash_scheme,
    message_centralized_signature, session, &mut ika, &mut sui, ctx,
);
// Store partial_cap with request for later
```

### Phase 2: Complete After Approval

```rust
// Verify partial sig
let verified_partial = coordinator.verify_partial_user_signature_cap(partial_cap, ctx);

// Create approval
let approval = coordinator.approve_message(&self.dwallet_cap, sig_algo, hash_scheme, message);

// Complete signature
let sign_id = coordinator.request_sign_with_partial_user_signature_and_return_id(
    verified_partial, approval, session, &mut ika, &mut sui, ctx,
);
```

### Check/Match

```rust
let ready = coordinator.is_partial_user_signature_valid(&unverified_cap);
let matches = coordinator.match_partial_user_signature_with_message_approval(&verified, &approval);
```

## Protocol: Key Importing

Import existing private key into dWallet system. Returns `ImportedKeyDWalletCap`.

```rust
let imported_cap = coordinator.request_imported_key_dwallet_verification(
    dwallet_network_encryption_key_id, curve, centralized_party_message,
    encrypted_centralized_secret_share_and_proof, encryption_key_address,
    user_public_output, signer_public_key, session, &mut ika, &mut sui, ctx,
);
```

### Imported Key Differences
- Use `ImportedKeyDWalletCap` instead of `DWalletCap`
- Use `coordinator.approve_imported_key_message(...)` instead of `approve_message`
- Use `coordinator.request_imported_key_sign_and_return_id(...)` for signing
- Use `coordinator.request_presign(dwallet_id, ...)` for ECDSA presigns (dWallet-specific)
- Future sign completion: `request_imported_key_sign_with_partial_user_signature_and_return_id`

## Protocol: Convert Zero-Trust to Shared

Irreversible. Makes user secret key share public, enabling contract-owned signing.

```rust
coordinator.request_make_dwallet_user_secret_key_shares_public(
    dwallet_id, public_user_secret_key_shares, session, &mut ika, &mut sui, ctx,
);
```

TypeScript: save `dkgData.userSecretKeyShare` during DKG for potential later conversion.

## Complete Example: Bitcoin Taproot Treasury

```rust
module my_protocol::treasury;

use ika::ika::IKA;
use ika_dwallet_2pc_mpc::{
    coordinator::DWalletCoordinator,
    coordinator_inner::{DWalletCap, UnverifiedPresignCap, UnverifiedPartialUserSignatureCap}
};
use sui::{balance::Balance, coin::Coin, sui::SUI, table::{Self, Table}};

const SECP256K1: u32 = 0;
const TAPROOT: u32 = 1;
const SHA256: u32 = 0;
const MIN_PRESIGNS: u64 = 3;

public struct Treasury has key, store {
    id: UID,
    dwallet_cap: DWalletCap,
    presigns: vector<UnverifiedPresignCap>,
    members: vector<address>,
    approval_threshold: u64,
    proposals: Table<u64, Proposal>,
    next_id: u64,
    ika_balance: Balance<IKA>,
    sui_balance: Balance<SUI>,
    dwallet_network_encryption_key_id: ID,
}

public struct Proposal has store {
    message: vector<u8>,
    partial_cap: Option<UnverifiedPartialUserSignatureCap>,
    approvals: u64,
    voters: Table<address, bool>,
    executed: bool,
}

// Create treasury with shared dWallet
public fun create(
    coordinator: &mut DWalletCoordinator,
    mut ika: Coin<IKA>, mut sui: Coin<SUI>,
    enc_key_id: ID,
    dkg_msg: vector<u8>, user_output: vector<u8>, user_share: vector<u8>,
    session_bytes: vector<u8>,
    members: vector<address>, threshold: u64,
    ctx: &mut TxContext,
) {
    let session = coordinator.register_session_identifier(session_bytes, ctx);
    let (dwallet_cap, _) = coordinator.request_dwallet_dkg_with_public_user_secret_key_share(
        enc_key_id, SECP256K1, dkg_msg, user_output, user_share,
        option::none(), session, &mut ika, &mut sui, ctx,
    );

    let treasury = Treasury {
        id: object::new(ctx), dwallet_cap, presigns: vector::empty(),
        members, approval_threshold: threshold,
        proposals: table::new(ctx), next_id: 0,
        ika_balance: ika.into_balance(), sui_balance: sui.into_balance(),
        dwallet_network_encryption_key_id: enc_key_id,
    };
    transfer::public_share_object(treasury);
}

// Create proposal with future sign (Phase 1)
public fun propose(
    self: &mut Treasury, coordinator: &mut DWalletCoordinator,
    message: vector<u8>, msg_sig: vector<u8>, ctx: &mut TxContext,
): u64 {
    assert!(self.members.contains(&ctx.sender()), 0);
    let (mut ika, mut sui) = self.withdraw_payment_coins(ctx);

    let verified = coordinator.verify_presign_cap(self.presigns.swap_remove(0), ctx);
    let session = random_session(coordinator, ctx);
    let partial = coordinator.request_future_sign(
        self.dwallet_cap.dwallet_id(), verified, message, SHA256,
        msg_sig, session, &mut ika, &mut sui, ctx,
    );

    let id = self.next_id;
    self.next_id = id + 1;
    self.proposals.add(id, Proposal {
        message, partial_cap: option::some(partial),
        approvals: 0, voters: table::new(ctx), executed: false,
    });

    // Auto-replenish
    if (self.presigns.length() < MIN_PRESIGNS) {
        let s = random_session(coordinator, ctx);
        self.presigns.push_back(coordinator.request_global_presign(
            self.dwallet_network_encryption_key_id, SECP256K1, TAPROOT, s,
            &mut ika, &mut sui, ctx,
        ));
    };
    self.return_payment_coins(ika, sui);
    id
}

// Vote
public fun vote(self: &mut Treasury, id: u64, approve: bool, ctx: &TxContext) {
    assert!(self.members.contains(&ctx.sender()), 0);
    let p = self.proposals.borrow_mut(id);
    assert!(!p.voters.contains(ctx.sender()) && !p.executed, 1);
    p.voters.add(ctx.sender(), approve);
    if (approve) { p.approvals = p.approvals + 1; };
}

// Execute after approval (Phase 2)
public fun execute(
    self: &mut Treasury, coordinator: &mut DWalletCoordinator,
    id: u64, ctx: &mut TxContext,
): ID {
    let p = self.proposals.borrow_mut(id);
    assert!(p.approvals >= self.approval_threshold && !p.executed, 2);
    let (mut ika, mut sui) = self.withdraw_payment_coins(ctx);

    let verified = coordinator.verify_partial_user_signature_cap(p.partial_cap.extract(), ctx);
    let approval = coordinator.approve_message(&self.dwallet_cap, TAPROOT, SHA256, p.message);
    let session = random_session(coordinator, ctx);
    let sign_id = coordinator.request_sign_with_partial_user_signature_and_return_id(
        verified, approval, session, &mut ika, &mut sui, ctx,
    );
    p.executed = true;
    self.return_payment_coins(ika, sui);
    sign_id
}

fun random_session(c: &mut DWalletCoordinator, ctx: &mut TxContext): SessionIdentifier {
    c.register_session_identifier(ctx.fresh_object_address().to_bytes(), ctx)
}
fun withdraw_payment_coins(self: &mut Treasury, ctx: &mut TxContext): (Coin<IKA>, Coin<SUI>) {
    (self.ika_balance.withdraw_all().into_coin(ctx), self.sui_balance.withdraw_all().into_coin(ctx))
}
fun return_payment_coins(self: &mut Treasury, ika: Coin<IKA>, sui: Coin<SUI>) {
    self.ika_balance.join(ika.into_balance());
    self.sui_balance.join(sui.into_balance());
}
```

## TypeScript: Calling Move Functions

```typescript
const tx = new Transaction();
tx.moveCall({
    target: `${PACKAGE_ID}::treasury::create`,
    arguments: [
        tx.object(coordinatorId),
        tx.object(ikaCoinId),
        tx.splitCoins(tx.gas, [1000000]),
        tx.pure.id(networkKeyId),
        tx.pure.vector('u8', Array.from(dkgData.userDKGMessage)),
        tx.pure.vector('u8', Array.from(dkgData.userPublicOutput)),
        tx.pure.vector('u8', Array.from(dkgData.userSecretKeyShare)),
        tx.pure.vector('u8', Array.from(sessionIdentifier)),
        tx.pure.vector('address', members),
        tx.pure.u64(threshold),
    ],
});
await suiClient.core.signAndExecuteTransaction({ transaction: tx, signer: keypair });
```

## Key Decision Points

- **Shared vs Zero-Trust**: Use shared for contract-owned signing (DAOs, treasuries, bots). Use zero-trust for user-held wallets.
- **Direct vs Future Sign**: Direct for immediate signing. Future for governance/multisig (two-phase).
- **Global vs dWallet-Specific Presign**: Global for most cases. dWallet-specific only for ECDSA with imported keys.
- **DKG vs Import**: DKG generates new distributed key (more secure). Import brings existing private key.

## Constants Module Pattern (Bitcoin Taproot)

```rust
module my_protocol::constants;
public macro fun curve(): u32 { 0 }
public macro fun signature_algorithm(): u32 { 1 }
public macro fun hash_scheme(): u32 { 0 }
```

## Chain-Specific Config Quick Reference

| Chain | Curve | Sig Algo | Hash |
|---|---|---|---|
| Bitcoin (Taproot) | 0 | 1 | 0 (SHA256) |
| Bitcoin (Legacy) | 0 | 0 | 2 (DoubleSHA256) |
| Ethereum | 0 | 0 | 0 (KECCAK256) |
| Solana | 2 | 0 | 0 (SHA512) |
| WebAuthn | 1 | 0 | 0 (SHA256) |
| Substrate | 3 | 0 | 0 (Merlin) |

