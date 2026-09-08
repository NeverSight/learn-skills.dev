---
name: cloud-engine-canisters
description: "Rules for canister code on a cloud engine (CloudEngine subnet, e.g. OpenCloud). Engine canisters hold 0 cycles: never attach cycles you computed: drop `(with cycles = …)` clauses (failure: IC0504). Cross-subnet calls must be bounded-wait and cycle-free (`(with timeout = N)`, `Call::bounded_wait`) or rejected: 'Unbounded-wait calls and calls with cycles are not allowed to CloudEngine subnets'. HTTPS outcalls use the ordinary wrapper and are free; never via the proxy: no transform applies ('Replicas had different responses') and its budget drains into InsufficientCycles: move the outcall, don't top up. Cycle-bearing cross-subnet calls go through the engine's proxy canister: XRC, and threshold ECDSA/Schnorr and vetKD (Bitcoin, Ethereum, VetKeys); hand-encode the arguments; the ic-vetkeys and ic-cdk helpers attach cycles. Derived keys belong to the proxy. Use when writing or debugging engine canister code, signing or deriving keys, or on these errors. Do NOT use for deploying a proxy (deploy-to-cloud-engine)."
license: Apache-2.0
compatibility: "A cloud engine (CloudEngine subnet) to run on, plus a deployed proxy canister for any chain-key or XRC call; Motoko examples need moc >= 0.14.2 (parenthetical `(with cycles = …)` / `(with timeout = N)` call attributes) and `to_candid` / `from_candid`, Rust examples need ic-cdk >= 0.18 (bounded-wait `Call` API)"
metadata:
  title: Cloud Engine Canisters
  category: CloudEngine
---

# Cloud Engine Canisters

## What This Is

A **cloud engine** is a user-owned slice of Internet Computer capacity, administered from a web console (see the `deploy-to-cloud-engine` skill for getting code onto one). Engines run on a dedicated **`CloudEngine` subnet type** with a **free cycles cost schedule**: nothing an engine canister does is metered in cycles — execution, storage, messaging, and HTTPS outcalls all cost zero — and engine canisters hold a **0 cycles balance by design**.

That model comes with protocol-enforced call rules. Code that works on a normal Application subnet can fail on an engine, and the failures look like cycles or consensus problems rather than what they are: code written for the wrong subnet type. The rules:

| Rule | On a cloud engine |
|------|-------------------|
| 1 | **Never attach cycles** to any call — remove `(with cycles = …)` and cycle-attaching wrappers |
| 2 | **Cross-subnet calls must be bounded-wait** — `(with timeout = N)` in Motoko, `Call::bounded_wait` in Rust |
| 3 | **HTTPS outcalls: ordinary code, zero cost** — keep the standard wrapper, transform on your own canister, never through the proxy |
| 4 | **Cycle-bearing cross-subnet targets** (XRC, threshold signing, vetKD) go **through the console proxy canister** |

## Rule 1 — Never attach a cycles amount you computed yourself

Engine canisters hold 0 cycles and there is nothing to pay for: under the engine's free cost schedule every fee an Application-subnet canister would pay (execution, message transmission, HTTPS outcalls, threshold signing, vetKD, storage) is charged as zero.

- **Inter-canister calls you write: no cycles clause at all.** There is nothing to buy — every fee on an engine is charged as zero — so a cycles attachment is never *needed*, independently of whether the protocol tolerates it. Write `await service.method(args)`, never `await (with cycles = 1_000_000) service.method(args)`. Verified on a live engine canister (`Cycles: 0`): **any non-zero amount fails** with

  ```
  Canister <id> is out of cycles, error code Some("IC0504")
  ```

  Do not "fix" this by zeroing the amount. The platform team's guidance is simply **not to mention cycles at all** on an engine call, and a `cycles = 0` left in place is noise that breaks again the moment the amount becomes non-zero (a computed fee, a copied constant). If you see `IC0504` from an engine canister, some call is attaching a non-zero amount.
- **Rust:** the same rule — never call `.with_cycles(…)` on a `Call` builder. (The platform team states the Motoko rule as "just don't mention cycles"; omitting `.with_cycles` is its Rust equivalent.)
- **Management-canister calls keep their standard wrapper.** `Call.httpRequest` (Motoko, `mo:ic`) and `ic_cdk::management_canister::http_request` (Rust) ask the `ic0.cost_*` system API for the fee, and that API is cost-schedule aware: on an engine it returns **0**, so the wrapper attaches nothing and the same source stays portable to an Application subnet. What breaks is substituting a hardcoded or hand-computed fee — never take a number from the `https-outcalls` cost tables and attach it on an engine.
- The one exception: cycles that a **cross-subnet target** charges are placed *inside* `ProxyArgs.cycles` of the console proxy (Rule 4), never attached to a call your canister sends.

## Rule 2 — Cross-subnet calls must be bounded-wait

The protocol rejects any cross-subnet (XNet) request **from or to** a CloudEngine subnet that is unbounded-wait (guaranteed-response) or carries cycles. The caller gets a reject with exactly this text:

```
Unbounded-wait calls and calls with cycles are not allowed to CloudEngine subnets
```

Verified live from an engine canister: a plain `await` to a canister on another subnet comes back as that exact `#system_fatal` reject, while the same call with `(with timeout = 30)` and no cycles clause succeeds.

Make every cross-subnet call bounded-wait and cycle-free:

```motoko
// Motoko: `timeout : Nat32` is in seconds
let result = await (with timeout = 30) service.method(args);
```

```rust
// Rust, ic-cdk >= 0.18 — bounded_wait defaults to a 300-second timeout (the IC maximum)
let reply: T = Call::bounded_wait(canister_id, "method")
    .with_arg(arg)
    .await?          // Err on reject / SYS_UNKNOWN — handle, do not unwrap
    .candid()?;      // decode the reply
```

- **Same-subnet calls are exempt**: canisters on the same engine may call each other unbounded-wait. Bounded-wait is still the better default — an unbounded-wait call to an unresponsive callee blocks the caller's upgrades indefinitely (see the `multi-canister` skill).
- The restriction applies in **both directions**: a canister on a normal subnet calling *into* an engine canister must also use a bounded-wait, cycle-free call.
- A bounded-wait call can complete with `SYS_UNKNOWN` (outcome unknown). Handle it — the `multi-canister` skill covers the patterns.

## Rule 3 — HTTPS outcalls: ordinary code, zero cost

HTTPS outcalls execute on the engine's own subnet, and the cost API reports them as free there, so the standard wrapper works unchanged — there is no engine-specific outcall code:

```motoko
import IC "mo:ic/Types";
import Call "mo:ic/Call";

// Build `request : IC.HttpRequestArgs` exactly as in the https-outcalls skill,
// with the transform query on THIS canister. Call.httpRequest asks the cost API,
// which returns 0 on an engine, so nothing is attached.
let response = await Call.httpRequest(request);
```

- **Keep the wrapper; never swap in a hardcoded fee** (Rule 1). `ic_cdk::management_canister::http_request` behaves the same way in Rust. This is how outcalls are written in engine apps running today.
- Everything else about outcalls is unchanged — transform function on your own canister, `max_response_bytes`, idempotency. Engines support the **full** outcall feature set per the platform team, replicated or not, so `is_replicated = ?false` is available for non-idempotent or rate-limited APIs — and for bulk workloads, where a replicated call multiplies every request by the replica count. Load the `https-outcalls` skill for those.
- **Never route HTTPS outcalls through the console proxy canister.** The platform team is explicit: all HTTP outcalls should be direct, and the proxy exists only for mainnet services that require cycles. The IC requires the transform function to live on the canister that issues `http_request` — behind the proxy that is the proxy itself, and the proxy exposes no transform method (verified against its live interface, and the team confirms none is planned). Untransformed responses differ across replicas for most real APIs, and the call fails with:

  ```
  SYS_TRANSIENT: No consensus could be reached. Replicas had different responses
  ```

  A proxied outcall also **pays**. The proxy sits on a normal Application subnet, so it is charged the real outcall fee out of the balance you funded, while the same call issued from your engine canister is charged nothing. At migration scale — thousands of calls — that balance drains and every call starts failing with `ProxyError::InsufficientCycles`. That is a symptom of proxying outcalls, not of an under-funded engine.

  Both failures have the same fix: issue the outcall directly from your canister (free, works). Neither is fixed by retries or by topping the proxy up.

## Rule 4 — Cross-subnet cycle-bearing calls via the console proxy

Two separate facts land in the same place. The Rule 2 restriction means an engine canister **cannot** send a cross-subnet message carrying cycles — and, per the platform team, **cloud engines do not provide threshold signing at all**, so those facilities have to be reached on mainnet. Either way the call cannot be made directly:

- **threshold ECDSA / Schnorr** signing (`sign_with_ecdsa`, `sign_with_schnorr`) and their public-key methods, and **vetKD** (`vetkd_derive_key`, `vetkd_public_key`) — not available on an engine; use mainnet's via the proxy,
- the **exchange-rate canister** (XRC) — a mainnet canister that charges cycles,
- any other canister that must be called **with cycles** across a subnet boundary.

This is the proxy's entire purpose: reaching mainnet services that require cycles. It is **not** for HTTPS outcalls (Rule 3).

The workaround is the **console proxy canister**: deployed on a normal Application subnet and funded with cycles. Your engine canister makes a cheap, cycle-less, bounded-wait call to the proxy, which re-issues it locally **with the cycles attached** and relays the raw reply back. Same-subnet or cycle-less calls do **not** need it — and neither do HTTPS outcalls (Rule 3).

### Getting a proxy

The proxy is not something your canister code creates: it is deployed and funded outside the app, then its canister id is handed to the app as configuration. Two different canisters can play the role, and they are **not** interchangeable:

| | **Console proxy** (the engine's) | **Self-deployed proxy** (`icp new … --subfolder proxy`) |
|---|---|---|
| Who may call it | The engine's **canister-id ranges**, plus controllers | **Controllers only** |
| Your engine canisters can call it | Yes, with no extra setup | Only if you add each of them as a controller |
| Threshold-key derivation | **Caller-isolated** (see below) | No isolation: raw pass-through |
| Funded with | A card, from the console | Cycles you already hold (`icp cycles mint`) |

For engine canisters, **use the console proxy**. A self-deployed proxy is the right tool for calls *you* make from the CLI (`icp canister call --proxy`, `icp deploy --proxy`), and the console proxy cannot serve that purpose, because it rejects ingress calls from any principal that is not one of its controllers, which your CLI identity is not.

Deploying and funding either one is not a canister-code task. It is covered in the **`deploy-to-cloud-engine`** skill; from here you need only the resulting **proxy canister id**. Take it from the user or from the app's configuration, never hardcode a guess, and read the derivation warning below before assuming one proxy id can be swapped for another.

### Call through the proxy from your canister

Instead of calling the target canister directly, call the proxy's `proxy` method with the target id, method name, candid-encoded argument bytes, and the cycles to attach. Its candid interface:

```candid
type ProxyArgs = record { canister_id : principal; method : text; args : blob; cycles : nat };
type ProxySucceed = record { result : blob };
type ProxyError = variant {
  InsufficientCycles : record { available : nat; required : nat };
  CallFailed : record { reason : text };
  UnauthorizedUser;
};
type ProxyResult = variant { Ok : ProxySucceed; Err : ProxyError };
service : {
  proxy : (ProxyArgs) -> (ProxyResult);
  get_allowed_ranges : () -> (vec record { start : principal; end : principal }) query;
};
```

- `args` is the **candid-encoded argument of the _target_ method** (you encode it); `result` is the target's **raw reply bytes** (you decode it).
- `cycles` is what the proxy attaches to the relayed call — size it to what the target charges (e.g. the XRC or signing fee). The platform team confirms the **caller** chooses how much the proxy attaches, and the proxy receives `args` as an **opaque blob**, so it cannot size the amount for you: a constant you pass is exactly what it will require, and the `required` field of `InsufficientCycles` echoes your own number back rather than reporting a proxy-side reservation. Do **not** attach cycles to the outer `proxy` call itself; the engine subnet forbids that and it is unnecessary.
- Handle `ProxyError`: `InsufficientCycles` means the proxy's balance is too low (top it up in the console), `UnauthorizedUser` means the caller is outside the engine's range, `CallFailed` carries the downstream reject reason.
- **Over-attaching is safe; under-attaching is not.** The callee refunds what it does not consume, and the refund goes back to the **proxy** (the proxy is the caller on that leg), so a generous `cycles` figure costs nothing and survives a fee increase. `available` in `InsufficientCycles` is the proxy's *liquid* balance (its freezing reserve is already excluded), so a proxy can report `InsufficientCycles` while still showing a balance in the console.
- **A `CallFailed` is not proof the call did not happen.** The proxy relays with a bounded-wait call, so a downstream `SYS_UNKNOWN` reaches you as `CallFailed` with that reject code in `reason`. The target may have executed and the cycles may already be spent. Treat it as "outcome unknown", not "failed": the `multi-canister` skill covers the patterns.

Motoko sketch (Rust is analogous with `candid::encode_one` / `decode_one`):

```motoko
// `proxy` is an actor typed to the candid interface above.
let arg = to_candid (request);                    // encode the TARGET method's argument
let res = await (with timeout = 30) proxy.proxy({
  canister_id = xrcPrincipal;
  method = "get_exchange_rate";
  args = arg;
  cycles = 1_000_000_000;                         // the XRC fee the proxy forwards
});
switch (res) {
  case (#Ok { result }) { let ?reply = from_candid (result) else return; /* … */ };
  case (#Err e) { /* InsufficientCycles | CallFailed | UnauthorizedUser */ };
};
```

### Threshold keys through the proxy (read this before deriving keys)

Threshold ECDSA, Schnorr, and vetKD are the proxy's main job on an engine, and the one place where getting the call *wrong* costs more than an error message: a key you cannot reproduce is a Bitcoin or Ethereum address whose funds you cannot move.

**The helper libraries do not work here.** `ic-vetkeys`, `ic-cdk-management-canister`, and Motoko's `mo:ic-vetkeys/ManagementCanister` all call `aaaaa-aa` directly and attach the fee for you. On an engine that is a cross-subnet, cycle-bearing call: rejected twice over (Rules 1 and 2). Their convenience is exactly what you must give up: encode the management-canister argument yourself and send it through the proxy. The `vetkeys` skill's code is written for a normal subnet and needs this rewrite before it will run on an engine.

**What the proxy rewrites.** For the six key methods (`sign_with_ecdsa`, `ecdsa_public_key`, `sign_with_schnorr`, `schnorr_public_key`, `vetkd_derive_key`, `vetkd_public_key`) the console proxy decodes your argument, **isolates the derivation to you**, and re-encodes it:

- ECDSA / Schnorr: your calling canister's principal is inserted as the **first element of `derivation_path`**.
- vetKD: your principal is prepended to `context`, **length-tagged**: one byte holding the principal's length, then the principal bytes, then your context.
- On the three `*_public_key` methods, `canister_id` is additionally forced to `None`.

The principal comes from `msg_caller()`, so it cannot be forged and one engine canister can never reach another's keys. (Verified: `cargo test -p proxy-canister --lib`, 10/10; `ecdsa_sign_prepends_caller_and_preserves_the_rest`, `vetkd_prefixes_caller_into_context_length_tagged`, `distinct_callers_get_distinct_derivations`.)

**Fees.** `ecdsa_public_key`, `schnorr_public_key`, and `vetkd_public_key` are **free**: pass `cycles = 0`. The paying methods are charged by the subnet that holds the key, not yours:

| Key name | `sign_with_ecdsa` / `sign_with_schnorr` / `vetkd_derive_key` |
|---|---|
| `key_1` (production) | 26_153_846_153 |
| `test_key_1` (testing) | 10_000_000_000 |

Round up rather than passing the exact figure: the unused remainder is refunded to the proxy.

**Worked example: ECDSA, Motoko.** Declare the management-canister types yourself; field names and variant tags must match the candid interface exactly, because the proxy decodes and re-encodes the blob; a missing or misnamed field, or an unknown variant tag, fails the decode (surfacing as `CallFailed`, not a mis-derived key). A field the proxy does not model is not caught: candid's record subtyping skips it on decode and the re-encode drops it.

```motoko
type EcdsaKeyId = { curve : { #secp256k1 }; name : Text };
type EcdsaPublicKeyArgs = { canister_id : ?Principal; derivation_path : [Blob]; key_id : EcdsaKeyId };
type EcdsaPublicKeyReply = { public_key : Blob; chain_code : Blob };
type SignWithEcdsaArgs = { message_hash : Blob; derivation_path : [Blob]; key_id : EcdsaKeyId };
type SignWithEcdsaReply = { signature : Blob };

let mgmt = Principal.fromText("aaaaa-aa");
let keyId : EcdsaKeyId = { curve = #secp256k1; name = "key_1" };
let signFee = 30_000_000_000;   // >= 26_153_846_153; the excess comes back

// One helper for every proxied management call.
func viaProxy(method : Text, arg : Blob, cycles : Nat) : async Blob {
  let res = await (with timeout = 30) proxy.proxy({
    canister_id = mgmt;   // the TARGET, not the proxy
    method = method;
    args = arg;
    cycles = cycles;      // 0 for the *_public_key methods
  });
  switch (res) {
    case (#Ok { result }) { result };
    case (#Err e) { Runtime.trap("proxy: " # debug_show e) };  // real code: return an error
  };
};

// Address: free, no cycles.
let pkArg = to_candid ({
  canister_id = null;                              // forced to null by the proxy anyway
  derivation_path = [Text.encodeUtf8("user-42")];  // your own path; the proxy prefixes itself
  key_id = keyId;
} : EcdsaPublicKeyArgs);
let ?pk : ?EcdsaPublicKeyReply = from_candid (await viaProxy("ecdsa_public_key", pkArg, 0))
  else Runtime.trap("decode ecdsa_public_key");

// Signature: pays the fee. `message_hash` must be exactly 32 bytes.
let sigArg = to_candid ({
  message_hash = messageHash;
  derivation_path = [Text.encodeUtf8("user-42")];  // the SAME path as above
  key_id = keyId;
} : SignWithEcdsaArgs);
let ?sig : ?SignWithEcdsaReply = from_candid (await viaProxy("sign_with_ecdsa", sigArg, signFee))
  else Runtime.trap("decode sign_with_ecdsa");
```

Note that `sign_with_ecdsa` has **no** `canister_id` field: the key it signs with is always the caller's, and behind the proxy the caller is the proxy. That is precisely why the public key you publish and the signature you produce must both come through the **same** proxy.

**Worked example: vetKD, Motoko.** Same shape, different types. `vetkd_public_key` is free; `vetkd_derive_key` pays.

```motoko
type VetkdKeyId = { curve : { #bls12_381_g2 }; name : Text };
type VetkdPublicKeyArgs = { canister_id : ?Principal; context : Blob; key_id : VetkdKeyId };
type VetkdPublicKeyReply = { public_key : Blob };
type VetkdDeriveKeyArgs = {
  input : Blob; context : Blob; transport_public_key : Blob; key_id : VetkdKeyId
};
type VetkdDeriveKeyReply = { encrypted_key : Blob };

let vetKeyId : VetkdKeyId = { curve = #bls12_381_g2; name = "key_1" };

let dkArg = to_candid ({
  input = Text.encodeUtf8("note-7");
  context = Text.encodeUtf8("my-app");     // the proxy length-tags its prefix onto this
  transport_public_key = transportPk;
  key_id = vetKeyId;
} : VetkdDeriveKeyArgs);
let ?dk : ?VetkdDeriveKeyReply = from_candid (await viaProxy("vetkd_derive_key", dkArg, 30_000_000_000))
  else Runtime.trap("decode vetkd_derive_key");
```

**Rust** is the same flow with `candid::encode_one` / `decode_one` and a bounded-wait call, see the shape in the `Call::bounded_wait(proxy_id, "proxy")` example under Rule 2.

**The derived key belongs to the proxy, not to your app.** The management canister derives from *its* caller, which is the proxy, so the key you get depends on **which proxy canister id you went through**:

- Point the app at a different proxy (a second one from the console's "Deploy another proxy", or a self-deployed one) and every address changes. The old address is not recoverable from the new proxy.
- **Deleting a proxy destroys access to its keys.** The console's delete button refunds the remaining cycles; it cannot give back the derivation. Any Bitcoin or Ethereum funds held at an address derived through that proxy become permanently unspendable. Treat the proxy id of a signing app as permanent infrastructure, and never delete a proxy to "save cycles" without first moving every asset off the addresses derived through it.
- A self-deployed upstream proxy does **no** isolation at all (no principal prefix, no forced `canister_id = None`), so its keys differ again from the console proxy's: the two are not substitutes even before the id changes.
- Anything reproducing a derivation off-chain (deriving the same public key in a frontend, say) must replicate the prefix the proxy injects, including vetKD's length tag.

## Common Pitfalls

1. **Attaching a cycles amount to a call you write.** A `(with cycles = N)` clause on an inter-canister call from an engine canister is never needed, and any non-zero `N` fails with `IC0504` / `is out of cycles` (verified live). Remove the clause entirely rather than setting `cycles = 0`: a zero is accepted, so it hides the mistake instead of fixing the habit. Nothing an engine canister does needs cycles: outcall, signing, and messaging fees are all zero under the engine's free cost schedule.
2. **Unbounded-wait cross-subnet calls.** A plain `await service.method(args)` to a canister on another subnet is unbounded-wait and is rejected with "Unbounded-wait calls and calls with cycles are not allowed to CloudEngine subnets". Use `(with timeout = N)` in Motoko or `Call::bounded_wait` in Rust — and handle `SYS_UNKNOWN`. Same-subnet (engine-local) calls are exempt.
3. **Rewriting outcall code for an engine — or hardcoding its fee.** Outcalls need no engine-specific form: keep `Call.httpRequest` (Motoko) or `ic_cdk::management_canister::http_request` (Rust), because the `ic0.cost_*` API they consult is cost-schedule aware and returns 0 on an engine. The mistake is replacing that call with a hand-computed fee from an Application-subnet cost table, which attaches a non-zero amount against a 0 balance.
4. **Routing HTTPS outcalls through the console proxy.** Two different failures, one cause. Consensus: `SYS_TRANSIENT: No consensus could be reached. Replicas had different responses`, because the transform must live on the calling canister — behind the proxy that is the proxy itself, and it exposes none (nor is one planned). Cost: the proxy is on a normal Application subnet, so it pays the real outcall fee from the balance you funded, and a bulk workload drains it into `ProxyError::InsufficientCycles`. Issue outcalls directly from your canister instead: on an engine they are free and unmetered, so no budget exists to exhaust.
5. **Topping up an engine canister with cycles.** Engine canisters hold 0 cycles by design; you cannot and need not send cycles to them. A "0 cycles" reading from an engine canister is normal, not an emergency — do not add top-up logic or cycles-balance alarms ported from Application-subnet apps.
6. **Calling the XRC / threshold signing / vetKD directly from an engine canister.** Cloud engines do not provide threshold signing at all (platform team), so `sign_with_ecdsa` / `sign_with_schnorr` / vetKD must be reached on mainnet — and a cross-subnet, cycle-bearing call is exactly what a CloudEngine-subnet canister cannot send. Route them through the funded console proxy (Rule 4). Plain same-subnet or cycle-less calls do not need the proxy.
7. **Attaching cycles to the outer `proxy` call.** The engine subnet forbids cycle-bearing cross-subnet messages — that is the whole reason for the proxy. Put the cycles inside `ProxyArgs.cycles` (the proxy attaches them locally); never `with cycles` on the call to `proxy` itself.
8. **Topping up the proxy without first asking what it was relaying.** On `ProxyError::InsufficientCycles`, check the call type before treating it as a funding problem. **An HTTPS outcall does not belong on the proxy at all** (Rule 3, pitfall 4): move it onto your own canister, where it is free, rather than buying budget for work that should cost nothing; raising the balance only delays the same stall. A drained balance is a genuine funding problem only for the proxy's real jobs (XRC, threshold signing, vetKD): top it up, or enable auto top-up, in the **Proxy canisters** section of the engine's **Canisters** page. Deploying and funding the console proxy is a console action, not an `icp` command, see `deploy-to-cloud-engine`.
9. **Expecting a direct-call key through the proxy.** Threshold-key derivation via the proxy is caller-isolated, so the derived key/address is not the same as a direct management-canister call. Fetch the public key and sign through the proxy consistently; do not mix direct and proxied key calls for the same identity.
10. **Using a chain-key helper library on an engine.** `ic-vetkeys`, `ic-cdk-management-canister`, and `mo:ic-vetkeys/ManagementCanister` call `aaaaa-aa` directly and attach the fee themselves: a cross-subnet, cycle-bearing call, which the engine rejects under Rules 1 and 2. Their whole value proposition (correct types, automatic cycles) is what has to go: hand-encode the management-canister argument and relay it through the proxy. Code copied from the `vetkeys` skill will not run on an engine unmodified.
11. **Deleting or swapping the proxy of a signing app.** The management canister derives keys from *its* caller (the proxy), so the proxy's canister id is part of every address the app owns. Deleting a proxy (the console refunds its cycles) or repointing the app at another one silently produces different addresses and leaves any Bitcoin or Ethereum funds at the old ones permanently unspendable. A signing app's proxy id is permanent infrastructure, not a fungible resource.
12. **Reading `CallFailed` as "it did not happen".** The proxy relays with a bounded-wait call, so a downstream `SYS_UNKNOWN` arrives as `ProxyError::CallFailed` with that reject code in `reason`. The target may have run and the cycles may be gone. Retrying a signature is harmless; retrying a stateful call on this basis is not: treat it as an unknown outcome (see `multi-canister`).
13. **Calling the console proxy from the CLI.** `icp canister call --proxy <console-proxy-id>` fails: the console proxy admits only the engine's canister-id ranges and its own controllers, and an ingress call from your CLI identity is neither (it is rejected by `inspect_message` before it reaches replicated state). For CLI-side proxying, deploy your own proxy (`icp new … --subfolder proxy`) which authorizes controllers, i.e. you.

## Additional References

- Load `deploy-to-cloud-engine` for getting the app onto the engine: CLI identity linking, subnet-targeted deploy, console app metadata, and for **deploying and funding the proxy** this skill's Rule 4 depends on, including the card-funded console flow, automatic top-up, and the self-deployed CLI alternative.
- Load `vetkeys` for what vetKD is and how its keys are used (IBE, encrypted maps, transport keys). Its call code targets a normal subnet and attaches cycles through helper libraries: on an engine, keep the concepts and replace the calls with the proxied form above.
- Load `https-outcalls` for everything about outcalls that is not engine-specific: transform functions, `max_response_bytes`, idempotency, debugging consensus failures.
- Load `multi-canister` for inter-canister call design, bounded vs unbounded wait semantics, and `SYS_UNKNOWN` handling.
