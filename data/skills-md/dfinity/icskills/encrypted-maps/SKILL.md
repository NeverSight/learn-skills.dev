---
name: encrypted-maps
description: "Add access-controlled, end-to-end encrypted key-value storage to a canister with the vetKeys EncryptedMaps library (ic-vetkeys for Rust and Motoko backends, @icp-sdk/vetkeys for the frontend). Values are encrypted client-side under vetKeys and shared between principals with per-user access rights (Read, ReadWrite, ReadWriteManage). Use when building a password manager, encrypted notes, a secure vault, or any app that stores and shares encrypted data on-chain. Start here for encrypted storage; escalate to the vetkeys skill only for BLS signatures, custom IBE, or timelock encryption."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2"
metadata:
  title: Encrypted Maps
  category: Security
---

# Encrypted Maps (vetKeys)

`EncryptedMaps` is a ready-made vetKeys library for **access-controlled, end-to-end encrypted key-value storage**. Each map is owned by a principal and holds `mapKey → value` entries; **values are encrypted on the client** under a vetKey and the canister only ever stores ciphertext. Owners share maps with other principals at three access levels. This is the default starting point for any encrypted-storage app (password manager, encrypted notes, vault).

Use the **`vetkeys` skill** instead when you need lower-level primitives: identity-based encryption (IBE), threshold BLS signatures, timelock encryption, or your own symmetric-key scheme.

| Layer | Rust | Motoko | Frontend |
|-------|------|--------|----------|
| Package | `ic-vetkeys` **0.9** | `ic-vetkeys` **0.6** (moc ≥ 1.13.0, core ≥ 2.6.1) | `@icp-sdk/vetkeys` **0.5** |
| Backend | `export_encrypted_maps_canister!` macro | `EncryptedMapsCanister` mixin | `@icp-sdk/vetkeys/encrypted_maps` |

> Use `@icp-sdk/vetkeys` (≥0.5), not the legacy `@dfinity/vetkeys` (frozen at 0.4). Frontend agent/identity come from `@icp-sdk/core`, not `@dfinity/agent`.

## Concepts

- **Map** — identified by `(mapOwner: Principal, mapName: bytes)`. Contains `mapKey → encryptedValue` entries. `mapName` and `mapKey` are byte arrays, **max 32 bytes** each.
- **Access rights** — `Read`, `ReadWrite`, `ReadWriteManage` (manage = may grant/revoke others). The owner always has full rights.
- **Client-side encryption** — the frontend fetches a per-map vetKey and encrypts/decrypts locally; the canister enforces access control and stores ciphertext. Sharing a map re-encrypts the map key for the new user automatically.
- **Key name & domain separator are immutable** once any value is encrypted — they feed key derivation, so changing them makes stored values undecryptable. See pitfalls.

## Backend — the whole canister in a few lines

The generator emits the `#[init]`/`#[post_upgrade]`, the stable state, and every endpoint the `@icp-sdk/vetkeys` frontend expects — so the Candid matches the client by construction. Do not hand-write the ~200 lines of delegation.

### Rust — `export_encrypted_maps_canister!`

```rust
use ic_stable_structures::memory_manager::{MemoryId, MemoryManager, VirtualMemory};
use ic_stable_structures::DefaultMemoryImpl;
use std::cell::RefCell;

type Memory = VirtualMemory<DefaultMemoryImpl>;

thread_local! {
    static MEMORY_MANAGER: RefCell<MemoryManager<DefaultMemoryImpl>> =
        RefCell::new(MemoryManager::init(DefaultMemoryImpl::default()));
}

fn memory(id: u8) -> Memory {
    MEMORY_MANAGER.with(|m| m.borrow().get(MemoryId::new(id)))
}

// Arg 1: the domain separator that isolates this app's derived keys (keep it
// stable forever). Then four Memory instances, in order: domain-separator config,
// access control, shared keys, encrypted values.
ic_vetkeys::export_encrypted_maps_canister!(
    "password_manager_app",
    [memory(0), memory(1), memory(2), memory(3)],
);

ic_cdk::export_candid!();
```

The generated `#[init]` takes the vetKD key name (`test_key_1` / `key_1`) as a `String` argument — pass it via `init_args` in `icp.yaml`.

### Motoko — `EncryptedMapsCanister` mixin

```motoko
import EncryptedMapsCanister "mo:ic-vetkeys/encrypted_maps/Canister";
import EncryptedMaps "mo:ic-vetkeys/encrypted_maps/EncryptedMaps";
import Types "mo:ic-vetkeys/Types";
import Runtime "mo:core/Runtime";

persistent actor PasswordManager {
  // `transient`: the key name is baked into `encryptedMapsState` at install and never re-read.
  transient let keyName = Runtime.envVar<system>("VETKD_KEY_NAME") ?? "test_key_1";

  // Arg 2 is the domain separator; like the key name it must stay stable for the life of the canister.
  let encryptedMapsState = EncryptedMaps.newEncryptedMapsState<Types.AccessRights>(
    { curve = #bls12_381_g2; name = keyName },
    "password_manager_app",
  );

  // The mixin contributes the full endpoint set (vetKD key, access control, map-name, value endpoints)
  // as snake_case methods, exactly what the frontend client calls.
  include EncryptedMapsCanister(encryptedMapsState);
};
```

In a `persistent actor` the `encryptedMapsState` binding is stable and persists across upgrades with no `stable` keyword; the actor owns it, so it stays a plain, migratable variable. Set `VETKD_KEY_NAME` at deploy time via canister settings (see the `icp-cli` skill).

## Frontend (TypeScript)

```typescript
import { HttpAgent, type Identity } from "@icp-sdk/core/agent";
import { safeGetCanisterEnv } from "@icp-sdk/core/agent/canister-env";
import {
  DefaultEncryptedMapsClient,
  EncryptedMaps,
  IndexedDbDerivedKeyMaterialCache,
  type AccessRights,
} from "@icp-sdk/vetkeys/encrypted_maps";

export async function createEncryptedMaps(
  identity: Identity, canisterId: string, host: string,
): Promise<EncryptedMaps> {
  // rootKey from the canister env (never fetchRootKey() in shipped code); undefined on mainnet
  const rootKey = safeGetCanisterEnv()?.IC_ROOT_KEY;
  const agent = await HttpAgent.create({ identity, host, rootKey });
  // Since 0.5.0 derived key material is cached in memory only by default.
  // Opt into cross-reload persistence, namespaced by principal; clearCache() on logout.
  const cache = new IndexedDbDerivedKeyMaterialCache(`vetkeys-${identity.getPrincipal().toText()}`);
  return new EncryptedMaps(new DefaultEncryptedMapsClient(agent, canisterId), { cache });
}
```

```typescript
const owner = myPrincipal;                              // Principal from @icp-sdk/core/principal
const mapName = new TextEncoder().encode("my-vault");   // ≤ 32 bytes
const mapKey  = new TextEncoder().encode("github.com"); // ≤ 32 bytes

// Store / read / remove (encryption happens client-side)
await encryptedMaps.setValue(owner, mapName, mapKey, new TextEncoder().encode("s3cr3t"));
const value = await encryptedMaps.getValue(owner, mapName, mapKey); // Uint8Array (empty if absent)
await encryptedMaps.removeEncryptedValue(owner, mapName, mapKey);

// Share the map with another principal (AccessRights is a Candid variant, not a string)
const rights: AccessRights = { ReadWrite: null };        // or { Read: null } / { ReadWriteManage: null }
await encryptedMaps.setUserRights(owner, mapName, otherPrincipal, rights);
const theirRights = await encryptedMaps.getUserRights(owner, mapName, otherPrincipal);

// Everything the caller can access (owned + shared)
const maps = await encryptedMaps.getAllAccessibleMaps();

await encryptedMaps.clearCache();                        // on logout / identity switch
```

## KeyManager — the layer beneath (use only when EncryptedMaps doesn't fit)

`EncryptedMaps` is built on **`KeyManager`**, which derives and shares access-controlled vetKeys keyed by name. Reach for `KeyManager` directly only when you need access-controlled **key derivation** (e.g. handing each client a per-resource symmetric or IBE key to use themselves) rather than encrypted key-value **storage** — most apps want `EncryptedMaps`.

Caveat: there is **no ready-made canister generator for KeyManager yet** ([dfinity/vetkeys#422](https://github.com/dfinity/vetkeys/issues/422)) — unlike EncryptedMaps, you wire the endpoints by hand. In Rust, `ic_vetkeys::key_manager::KeyManager::init` takes the domain separator, the `VetKDKeyId`, and three `Memory` instances (config, access control, shared keys), and exposes `get_vetkey_verification_key`, `get_encrypted_vetkey`, `get_user_rights`, `set_user_rights`, `remove_user`. Motoko mirrors this via `KeyManager.newKeyManagerState` + the `KeyManager` class; the frontend uses `@icp-sdk/vetkeys/key_manager` (`KeyManager` + `DefaultKeyManagerClient`).

## Pitfalls

1. **Use the generator, don't hand-write endpoints.** Rust `export_encrypted_maps_canister!`, Motoko `include EncryptedMapsCanister(state)`. Hand-written delegation drifts from the Candid the frontend client expects and breaks silently.

2. **Domain separator and vetKD key name are immutable once data exists.** Both feed key derivation; changing either makes every stored value undecryptable. In Motoko the `VETKD_KEY_NAME` env var is captured into stable state at first install — editing it on a later upgrade is silently ignored (only a `reinstall`, which drops all data, switches keys). Because `test_key_1` is also a valid mainnet key, a production deploy that forgets to set `VETKD_KEY_NAME` silently runs on it — assert the expected key at deploy time.

3. **Derived key material is in-memory by default since 0.5.0** (was IndexedDB). Pass `IndexedDbDerivedKeyMaterialCache` to persist it across reloads, and call `clearCache()` on logout / identity change. Old `@dfinity/vetkeys` 0.1–0.4 IndexedDB entries remain at rest after upgrading — clear them once.

4. **Client construction changed.** `DefaultEncryptedMapsClient` takes a ready `HttpAgent` (`await HttpAgent.create({ identity, host, rootKey })`), not `HttpAgentOptions`. Agent/identity come from `@icp-sdk/core`.

5. **`AccessRights` is a Candid variant, not a string** — `{ ReadWrite: null }`, not `"ReadWrite"`. Three levels: `Read`, `ReadWrite`, `ReadWriteManage`.

6. **`mapName` and `mapKey` are byte arrays, ≤ 32 bytes each** — encode strings with `TextEncoder`.

7. **Keep per-value app state consistent via the control-plane variant.** If you store metadata alongside each value, use `custom_value_endpoints` (Rust) / `EncryptedMapsControlPlaneCanister` (Motoko) and own the value endpoints — see `references/metadata.md`. Don't also expose the library's raw value mutators, or the two stores desync.

8. **Don't re-init state on upgrade.** The macro/mixin generate the lifecycle hooks; stable memory survives upgrades. Adding your own `post_upgrade` that rebuilds state corrupts it.

9. **Cycles.** `vetkd_derive_key` (used under the hood) costs cycles — `test_key_1` and `key_1` cost the same locally and on mainnet, and the library attaches the right amount (excess refunded). Keep the canister funded. (See the `vetkeys` skill for the cost table.)

## Additional References

- Metadata / custom value endpoints: `references/metadata.md`
- Lower-level vetKeys (IBE, BLS, timelock, symmetric, offline derivation): the **`vetkeys`** skill
- Canonical examples: `motoko/vetkeys/password_manager`, `rust/vetkeys/password_manager` in [dfinity/examples](https://github.com/dfinity/examples/tree/master/rust/vetkeys)

## Deploy & verify

Provisioning and generic deploy steps belong to the **`icp-cli`** skill. EncryptedMaps-specific checks:

```bash
icp deploy backend                                         # local replica provisions test_key_1
# From the frontend: setValue then getValue round-trips the plaintext for the owner;
# a principal without rights gets an access-control error on getValue.
```
