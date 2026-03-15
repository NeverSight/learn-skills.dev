---
name: canister-security
description: "IC-specific security patterns for canister development in Motoko and Rust. Covers access control, anonymous principal rejection, reentrancy prevention (CallerGuard pattern), async safety (saga pattern), callback trap handling, cycle drain protection, and safe upgrade patterns. Use when writing or modifying any canister that modifies state, handles tokens, makes inter-canister calls, or implements access control."
license: Apache-2.0
metadata:
  title: Canister Security
  category: Security
---

# Canister Security

## What This Is

Security patterns for IC canisters in Motoko and Rust. The async messaging model creates TOCTOU (time-of-check-time-of-use) vulnerabilities where state changes between `await` calls. `canister_inspect_message` is NOT a reliable security boundary. Anyone on the internet can burn your cycles by sending update calls. This skill provides copy-paste correct patterns for access control, reentrancy prevention, async safety, and callback trap handling.

## Prerequisites

- For Motoko: `mops` package manager, `core = "2.0.0"` in mops.toml
- For Rust: `ic-cdk = "0.19"`, `candid = "0.10"`

## Security Pitfalls

1. **Relying on `canister_inspect_message` for access control.** This hook runs on a single replica without full consensus. A malicious boundary node can bypass it by forwarding the message anyway. It is also never called for inter-canister calls, query calls, or management canister calls. Always duplicate access checks inside every update method. Use `inspect_message` only as a cycle-saving optimization, never as a security boundary.

2. **Forgetting to reject the anonymous principal.** Every endpoint that requires authentication must check that the caller is not the anonymous principal (`2vxsx-fae`). In Motoko use `Principal.isAnonymous(caller)`, in Rust compare `msg_caller() != Principal::anonymous()`. Without this, unauthenticated callers can invoke protected methods — and if the canister uses the caller principal as an identity key (e.g., for balances), the anonymous principal becomes a shared identity anyone can use.

3. **Reading state before an async call and assuming it's unchanged after (TOCTOU).** When your canister `await`s an inter-canister call, other messages can interleave and mutate state. This is one of the most critical sources of DeFi exploits on IC. Use per-caller locking (CallerGuard pattern) to prevent concurrent operations. For financial operations, also consider the saga pattern (deduct before `await`, compensate on failure) — but implementing it correctly is complex due to edge cases like callback traps and call timeouts where the outcome is ambiguous.

4. **Trapping in `pre_upgrade`.** If `pre_upgrade` traps (e.g., serializing too much data exceeds the instruction limit), the canister becomes permanently non-upgradeable. Avoid storing large data structures in the heap that must be serialized during upgrade. In Rust, use `ic-stable-structures` for direct stable memory access. In Motoko, the `persistent actor` declaration stores all `let` and `var` variables automatically in stable memory — no manual serialization needed.

5. **Not monitoring cycles balance.** Every canister has a default `freezing_threshold` of 2,592,000 seconds (~30 days). When cycles drop below the threshold reserve, the canister freezes (rejects all update calls). When cycles reach zero, the canister is uninstalled — its code and memory are removed, though the canister ID and controllers survive. The real pitfall is not actively monitoring and topping up cycles. For production canisters holding valuable state, increase the freezing threshold and set up automated monitoring.
   ```bash
   # Check current settings (mainnet)
   icp canister settings show backend -e ic
   # Increase freezing threshold for high-value canisters
   icp canister settings update backend --freezing-threshold 7776000 -e ic  # 90 days
   ```

6. **Single controller with no backup.** If you lose the controller identity's private key, the canister becomes unupgradeable forever. There is no recovery mechanism. Always add a backup controller or governance canister:
   ```bash
   icp canister settings update backend --add-controller <backup-principal> -e ic
   ```
   When deploying, ask the developer if they have a backup controller principal to add.

7. **Calling `fetchRootKey()` in production.** `fetchRootKey()` fetches the root public key from the replica and trusts whatever it returns. On mainnet, the root key is hardcoded into the agent — calling `fetchRootKey()` there allows a man-in-the-middle to substitute a different key, breaking all verification. Only call `fetchRootKey()` in local development, guarded by an environment check. For frontends served by asset canisters, the root key is provided automatically.

8. **Exposing admin methods without guards.** Every update method is callable by anyone on the internet. Admin methods (migration, config, minting) must explicitly check the caller against an allowlist. There is no built-in role system — you must implement it yourself. Always include admin revocation — missing revocation is a common source of bugs.

9. **Storing secrets in canister state.** Canister memory on standard application subnets is readable by node operators. Never store private keys, API secrets, or passwords in canister state. For on-chain secret management, use vetKD (threshold key derivation).

10. **Allowing unbounded user-controlled storage.** If users can store data without limits, an attacker can fill the 4 GiB Wasm heap or stable memory, bricking the canister. Always enforce per-user storage quotas and validate input sizes.

11. **Trapping in a callback after state mutation.** If your canister mutates state before an inter-canister call and the callback traps, the pre-call mutations persist but the callback's mutations are rolled back. A malicious callee can exploit this to skip security-critical actions like debiting an account. Structure code so that critical state mutations happen before the async boundary and are correctly rolled back if a failure or trap occurs. Use `try/finally` (Motoko) or `Drop` guards (Rust) to ensure cleanup always runs. Keep cleanup code minimal — trapping in cleanup recreates the problem. Consider using `call_on_cleanup` for rollback logic and journaling for crash-safe state transitions.

12. **Unbounded wait calls preventing upgrades.** If your canister makes a call to an untrustworthy or buggy callee that never responds, the canister cannot be stopped (and therefore cannot be upgraded) while awaiting outstanding responses. Use bounded wait calls (timeouts) to ensure calls complete in bounded time regardless of callee behavior.

## How It Works

### IC Security Model

1. **Update calls** go through consensus — all nodes on a subnet execute the code and must agree on the result. Standard application subnets have 13 nodes; system and fiduciary subnets have more (28+). This makes update calls tamper-proof but slower (~2s).
2. **Query calls** run on a single replica — fast (~200ms) but the replica can return incorrect or malicious results. Replica-signed queries provide partial mitigation (the responding replica signs the response), but for full trust, use certified data or update calls for security-critical reads.
3. **Inter-canister calls** are async messages. Between sending a request and receiving the response, your canister can process other messages. State may change under you (see TOCTOU pitfall above).
4. **State rollback on trap.** If a message execution traps, all its state changes are rolled back. For inter-canister calls, the first execution (before `await`) and the callback (after `await`) are separate messages — a trap in the callback rolls back only the callback's changes, while the first execution's changes persist. This is why cleanup logic (like releasing locks) must go in cleanup context (`finally`/`Drop`), not regular callback code.

## Implementation

### Motoko

#### Access control

Uses the `shared(msg)` pattern to capture the deployer atomically — no separate `init()` call, no front-running risk.

```motoko
import Principal "mo:core/Principal";
import Set "mo:core/pure/Set";
import Runtime "mo:core/Runtime";

shared(msg) persistent actor class MyCanister() {

  // --- Authorization state ---
  // transient: recomputed on each install/upgrade from msg.caller (the controller)
  transient let owner = msg.caller;
  var admins : Set.Set<Principal> = Set.empty();

  // --- Guards ---

  func requireAuthenticated(caller : Principal) {
    if (Principal.isAnonymous(caller)) {
      Runtime.trap("anonymous caller not allowed");
    };
  };

  func requireOwner(caller : Principal) {
    requireAuthenticated(caller);
    if (caller != owner) {
      Runtime.trap("caller is not the owner");
    };
  };

  func requireAdmin(caller : Principal) {
    requireAuthenticated(caller);
    if (caller != owner and not Set.contains(admins, Principal.compare, caller)) {
      Runtime.trap("caller is not an admin");
    };
  };

  // --- Admin management ---

  public shared ({ caller }) func addAdmin(newAdmin : Principal) : async () {
    requireOwner(caller);
    admins := Set.add(admins, Principal.compare, newAdmin);
  };

  public shared ({ caller }) func removeAdmin(admin : Principal) : async () {
    requireOwner(caller);
    admins := Set.remove(admins, Principal.compare, admin);
  };

  // --- Endpoints ---

  public shared ({ caller }) func publicAction() : async Text {
    requireAuthenticated(caller);
    "ok";
  };

  public shared ({ caller }) func adminAction() : async () {
    requireAdmin(caller);
    // ... protected logic
  };
};
```

#### Reentrancy prevention (CallerGuard pattern)

Per-caller locking prevents a second call from the same caller while the first is awaiting a response. The guard must be released in the `finally` block — if the callback traps, `catch` state changes are rolled back, but `finally` runs in cleanup context where state changes persist.

```motoko
import Map "mo:core/Map";
import Principal "mo:core/Principal";
import Error "mo:core/Error";
import Result "mo:core/Result";

// Inside the persistent actor class { ... }
// otherCanister is application-specific — replace with your canister reference.

  let pendingRequests = Map.empty<Principal, Bool>();

  func acquireGuard(principal : Principal) : Result.Result<(), Text> {
    if (Map.get(pendingRequests, Principal.compare, principal) != null) {
      return #err("already processing a request for this caller");
    };
    Map.add(pendingRequests, Principal.compare, principal, true);
    #ok;
  };

  func releaseGuard(principal : Principal) {
    ignore Map.delete(pendingRequests, Principal.compare, principal);
  };

  public shared ({ caller }) func doSomethingAsync() : async Result.Result<Text, Text> {
    requireAuthenticated(caller);

    // 1. Acquire per-caller lock — rejects concurrent calls from same principal
    switch (acquireGuard(caller)) {
      case (#err(msg)) { return #err(msg) };
      case (#ok) {};
    };

    // 2. Make inter-canister call
    try {
      let result = await otherCanister.someMethod();
      #ok(result)
    } catch (e) {
      #err("call failed: " # Error.message(e))
    } finally {
      // Runs in cleanup context even if the callback traps — changes here persist.
      releaseGuard(caller);
    };
  };
```

#### inspect_message (cycle optimization only)

```motoko
// Inside persistent actor { ... }
// Method variants must match your public methods

system func inspect(
  {
    caller : Principal;
    msg : {
      #adminAction : () -> ();
      #addAdmin : () -> Principal;
      #removeAdmin : () -> Principal;
      #publicAction : () -> ();
      #doSomethingAsync : () -> ();
    }
  }
) : Bool {
  switch (msg) {
    // Admin methods: reject anonymous to save cycles on Candid decoding
    case (#adminAction _) { not Principal.isAnonymous(caller) };
    case (#addAdmin _) { not Principal.isAnonymous(caller) };
    case (#removeAdmin _) { not Principal.isAnonymous(caller) };
    case (#doSomethingAsync _) { not Principal.isAnonymous(caller) };
    // Public methods: accept all
    case (_) { true };
  };
};
```

### Rust

#### Access control (using CDK guard pattern)

The `guard` attribute runs a check before the method body. If the guard returns `Err`, the call is rejected before any method code executes. This is more robust than calling guard functions inside the method — you cannot forget to add it.

```rust
use ic_cdk::{init, update};
use ic_cdk::api::msg_caller;
use candid::Principal;
use std::cell::RefCell;

thread_local! {
    static OWNER: RefCell<Principal> = RefCell::new(Principal::anonymous());
    static ADMINS: RefCell<Vec<Principal>> = RefCell::new(vec![]);
}

// --- Guards (for #[update(guard = "...")] attribute) ---
// Must return Result<(), String>. Err rejects the call.

fn require_authenticated() -> Result<(), String> {
    if msg_caller() == Principal::anonymous() {
        return Err("anonymous caller not allowed".to_string());
    }
    Ok(())
}

fn require_owner() -> Result<(), String> {
    require_authenticated()?;
    OWNER.with(|o| {
        if msg_caller() != *o.borrow() {
            return Err("caller is not the owner".to_string());
        }
        Ok(())
    })
}

fn require_admin() -> Result<(), String> {
    require_authenticated()?;
    let caller = msg_caller();
    let is_authorized = OWNER.with(|o| caller == *o.borrow())
        || ADMINS.with(|a| a.borrow().contains(&caller));
    if !is_authorized {
        return Err("caller is not an admin".to_string());
    }
    Ok(())
}

// --- Init ---

#[init]
fn init(owner: Principal) {
    OWNER.with(|o| *o.borrow_mut() = owner);
}

// --- Endpoints ---

#[update(guard = "require_authenticated")]
fn public_action() -> String {
    "ok".to_string()
}

#[update(guard = "require_admin")]
fn admin_action() {
    // ... protected logic — guard already validated caller
}

#[update(guard = "require_owner")]
fn add_admin(new_admin: Principal) {
    ADMINS.with(|a| a.borrow_mut().push(new_admin));
}

#[update(guard = "require_owner")]
fn remove_admin(admin: Principal) {
    ADMINS.with(|a| a.borrow_mut().retain(|p| p != &admin));
}

ic_cdk::export_candid!();
```

#### Reentrancy prevention (CallerGuard pattern)

`CallerGuard` uses the `Drop` trait to release the lock when the guard goes out of scope — including when the callback traps (since ic-cdk 0.5.1, local variables go out of scope during cleanup). Never use `let _ = CallerGuard::new(caller)?` — this drops the guard immediately, making locking ineffective.

```rust
use std::cell::RefCell;
use std::collections::BTreeSet;
use candid::Principal;
use ic_cdk::update;
use ic_cdk::api::msg_caller;
use ic_cdk::call::Call;

// other_canister_id is application-specific — replace with your canister reference.

thread_local! {
    static PENDING: RefCell<BTreeSet<Principal>> = RefCell::new(BTreeSet::new());
}

struct CallerGuard {
    principal: Principal,
}

impl CallerGuard {
    fn new(principal: Principal) -> Result<Self, String> {
        PENDING.with(|p| {
            if !p.borrow_mut().insert(principal) {
                return Err("already processing a request for this caller".to_string());
            }
            Ok(Self { principal })
        })
    }
}

impl Drop for CallerGuard {
    fn drop(&mut self) {
        PENDING.with(|p| {
            p.borrow_mut().remove(&self.principal);
        });
    }
}

#[update]
async fn do_something_async() -> Result<String, String> {
    let caller = msg_caller();
    if caller == Principal::anonymous() {
        return Err("anonymous caller not allowed".to_string());
    }

    // Acquire per-caller lock — rejects concurrent calls from same principal.
    // Drop releases lock even if callback traps.
    let _guard = CallerGuard::new(caller)?;

    // Make inter-canister call
    let response = Call::bounded_wait(other_canister_id(), "some_method")
        .await
        .map_err(|e| format!("call failed: {:?}", e))?;
    let result: String = response.candid()
        .map_err(|e| format!("decode failed: {:?}", e))?;

    Ok(result)
    // _guard dropped here → lock released
}
```

#### inspect_message (cycle optimization only)

```rust
use ic_cdk::api::{accept_message, msg_caller, msg_method_name};
use candid::Principal;

/// Pre-filter to reduce cycle waste from spam.
/// Runs on ONE node. Can be bypassed. NOT a security check.
/// Always duplicate real access control inside each method or via guard attribute.
#[ic_cdk::inspect_message]
fn inspect_message() {
    let method = msg_method_name();
    match method.as_str() {
        // Admin methods: only accept from non-anonymous callers
        "admin_action" | "add_admin" | "remove_admin" | "do_something_async" => {
            if msg_caller() != Principal::anonymous() {
                accept_message();
            }
            // Silently reject anonymous — saves cycles on Candid decoding
        }
        // Public methods: accept all
        _ => accept_message(),
    }
}
```
