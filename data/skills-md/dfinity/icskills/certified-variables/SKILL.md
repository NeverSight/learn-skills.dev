---
name: certified-variables
description: "Serve cryptographically verified responses from query calls using Merkle trees and subnet BLS signatures. Covers certified data API, RbTree/CertTree construction, witness generation, and frontend certificate validation. Use when query responses need verification, certified data, or response authenticity proofs."
license: Apache-2.0
compatibility: "icp-cli >= 0.1.0"
metadata:
  title: Certified Variables
  category: Security
---

# Certified Variables & Certified Assets

## What This Is

Query responses on the Internet Computer come from a single replica and are NOT verified by consensus. A malicious or faulty replica could return fabricated data. Certification solves this: the canister stores a hash in the subnet's certified state tree during update calls, and then query responses include a certificate signed by the subnet's threshold BLS key proving the data is authentic. The result is responses that are both fast (no consensus delay) AND cryptographically verified.

## Prerequisites

- Rust: `ic-certified-map` crate (for Merkle tree), `ic-cdk` (for `certified_data_set` / `data_certificate`)
- Motoko: `CertifiedData` module (included in mo:core/mo:base), `ic-certification` package (`mops add ic-certification`) for Merkle tree with witness support
- Frontend: `@icp-sdk/core` (agent, principal), `@dfinity/certificate-verification`

## Canister IDs

No external canister IDs required. Certification uses the IC system API exposed through CDK wrappers:
- `ic_cdk::api::certified_data_set` (Rust) / `CertifiedData.set` (Motoko) -- called during update calls to set the certified hash (max 32 bytes)
- `ic_cdk::api::data_certificate` (Rust) / `CertifiedData.getCertificate` (Motoko) -- called during query calls to retrieve the subnet certificate

The IC root public key (needed for client-side verification):
- Mainnet: `308182301d060d2b0601040182dc7c0503010201060c2b0601040182dc7c05030201036100814c0e6ec71fab583b08bd81373c255c3c371b2e84863c98a4f1e08b74235d14fb5d9c0cd546d9685f913a0c0b2cc5341583bf4b4392e467db96d65b9bb4cb717112f8472e0d5a4d14505ffd7484b01291091c5f87b98883463f98091a0baaae`
- Local: available from `icp` (agent handles this automatically)

## Mistakes That Break Your Build

1. **Trying to store more than 32 bytes of certified data.** The `certified_data_set` API accepts exactly one blob of at most 32 bytes. You cannot certify arbitrary data directly. Instead, build a Merkle tree over your data and certify only the root hash (32 bytes). The tree structure provides proofs for individual values.

2. **Calling `certified_data_set` in a query call.** Certification can ONLY be set during update calls (which go through consensus). Calling it in a query traps. Pattern: set the hash during writes, read the certificate during queries.

3. **Forgetting to include the certificate in query responses.** The certificate is obtained via `data_certificate()` during query calls. If you return data without the certificate, clients cannot verify anything. Always return a tuple of (data, certificate, witness).

4. **Not updating the certified hash after data changes.** If you modify the data but forget to call `certified_data_set` with the new root hash, query responses will fail verification because the certificate proves a stale hash.

5. **Building the witness for the wrong key.** The witness (Merkle proof) must correspond to the exact key being queried. A witness for key "users/alice" will not verify key "users/bob".

6. **Assuming `data_certificate()` returns a value in update calls.** It returns `null`/`None` during update calls. Certificates are only available during query calls.

7. **Certifying data at canister init but not on upgrades.** After a canister upgrade, the certified data is cleared. You must call `certified_data_set` in both `#[init]` and `#[post_upgrade]` (Rust) or `system func postupgrade` (Motoko) to re-establish certification.

8. **Not validating certificate freshness on the client.** The certificate's state tree contains a `/time` field with the timestamp when the subnet produced it. Clients MUST check that this timestamp is recent (recommended: within 5 minutes of current time). Without this check, an attacker could replay a stale certificate with outdated data. Always verify `certificate_time` is within an acceptable delta before trusting the response.

## How Certification Works

```
UPDATE CALL (goes through consensus):
  1. Canister modifies data
  2. Canister builds/updates Merkle tree
  3. Canister calls certified_data_set(root_hash)  -- 32 bytes
  4. Subnet includes root_hash in its certified state tree

QUERY CALL (single replica, no consensus):
  1. Client sends query
  2. Canister calls data_certificate() -- gets subnet BLS signature
  3. Canister builds witness (Merkle proof) for the requested key
  4. Canister returns: { data, certificate, witness }

CLIENT VERIFICATION:
  1. Verify certificate signature against IC root public key
  2. Extract root_hash from certificate's state tree
  3. Verify witness: root_hash + witness proves data is in the tree
  4. Trust the data
```

## Implementation

### Rust

**Cargo.toml:**

```toml
[package]
name = "certified_vars_backend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
candid = "0.10"
ic-cdk = "0.19"
ic-certified-map = "0.4"
serde = { version = "1", features = ["derive"] }
serde_bytes = "0.11"
ciborium = "0.2"
```

**Complete certified key-value store:**

```rust
use candid::{CandidType, Deserialize};
use ic_cdk::{init, post_upgrade, query, update};
use ic_certified_map::{AsHashTree, RbTree};
use serde_bytes::ByteBuf;
use std::cell::RefCell;

thread_local! {
    // RbTree is a Merkle-tree-backed map: keys and values are byte slices
    static TREE: RefCell<RbTree<Vec<u8>, Vec<u8>>> = RefCell::new(RbTree::new());
}

// Update the certified data hash after any modification
fn update_certified_data() {
    TREE.with(|tree| {
        let tree = tree.borrow();
        // root_hash() returns a 32-byte SHA-256 hash of the entire tree
        ic_cdk::api::certified_data_set(&tree.root_hash());
    });
}

#[init]
fn init() {
    update_certified_data();
}

#[post_upgrade]
fn post_upgrade() {
    // Assumes data has already been deserialized from stable memory into the TREE.
    // CRITICAL: re-establish certification after upgrade — certified_data is cleared on upgrade.
    update_certified_data();
}

#[update]
fn set(key: String, value: String) {
    TREE.with(|tree| {
        let mut tree = tree.borrow_mut();
        tree.insert(key.as_bytes().to_vec(), value.as_bytes().to_vec());
    });
    // Must update certified hash after every data change
    update_certified_data();
}

#[update]
fn delete(key: String) {
    TREE.with(|tree| {
        let mut tree = tree.borrow_mut();
        tree.delete(key.as_bytes());
    });
    update_certified_data();
}

#[derive(CandidType, Deserialize)]
struct CertifiedResponse {
    value: Option<String>,
    certificate: ByteBuf,      // subnet BLS signature
    witness: ByteBuf,          // Merkle proof for this key
}

#[query]
fn get(key: String) -> CertifiedResponse {
    // data_certificate() is only available in query calls
    let certificate = ic_cdk::api::data_certificate()
        .expect("data_certificate only available in query calls");

    TREE.with(|tree| {
        let tree = tree.borrow();

        // Look up the value
        let value = tree.get(key.as_bytes())
            .map(|v| String::from_utf8(v.clone()).unwrap());

        // Build a witness (Merkle proof) for this specific key
        let witness = tree.witness(key.as_bytes());

        // Serialize the witness as CBOR
        let mut witness_buf = vec![];
        ciborium::into_writer(&witness, &mut witness_buf)
            .expect("Failed to serialize witness as CBOR");

        CertifiedResponse {
            value,
            certificate: ByteBuf::from(certificate),
            witness: ByteBuf::from(witness_buf),
        }
    })
}

// Batch set multiple values in one update call (more efficient)
#[update]
fn set_many(entries: Vec<(String, String)>) {
    TREE.with(|tree| {
        let mut tree = tree.borrow_mut();
        for (key, value) in entries {
            tree.insert(key.as_bytes().to_vec(), value.as_bytes().to_vec());
        }
    });
    // Single certification update for all changes
    update_certified_data();
}
```

### HTTP Certification (v2) for Custom HTTP Canisters

For canisters serving HTTP responses directly (not through the asset canister), responses must be certified so the HTTP gateway can verify them.

**Additional Cargo.toml dependency:**

```toml
[package]
name = "http_certified_backend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
ic-http-certification = "3.1"
```

**Certifying HTTP responses:**

> **Note:** The HTTP certification API is evolving rapidly. Verify these examples against the latest [ic-http-certification docs](https://docs.rs/ic-http-certification) before use.

```rust
use ic_http_certification::{
    HttpCertification, HttpCertificationPath, HttpCertificationTree,
    HttpCertificationTreeEntry, HttpRequest, HttpResponse,
    DefaultCelBuilder, DefaultResponseCertification,
};
use std::cell::RefCell;

thread_local! {
    static HTTP_TREE: RefCell<HttpCertificationTree> = RefCell::new(
        HttpCertificationTree::default()
    );
}

// Define what gets certified using CEL (Common Expression Language)
fn certify_response(path: &str, request: &HttpRequest, response: &HttpResponse) {
    // Full certification: certify both request path and response body
    let cel = DefaultCelBuilder::full_certification()
        .with_response_certification(DefaultResponseCertification::certified_response_headers(
            vec!["Content-Type", "Content-Length"],
        ))
        .build();

    // Create the certification from the CEL expression, request, and response
    let certification = HttpCertification::full(&cel, request, response, None)
        .expect("Failed to create HTTP certification");

    let http_path = HttpCertificationPath::exact(path);

    HTTP_TREE.with(|tree| {
        let mut tree = tree.borrow_mut();
        let entry = HttpCertificationTreeEntry::new(http_path, certification);
        tree.insert(&entry);

        // Update canister certified data with tree root hash
        ic_cdk::api::certified_data_set(&tree.root_hash());
    });
}
```

### Motoko

**Using CertifiedData module:**

```motoko
import CertifiedData "mo:core/CertifiedData";
import Blob "mo:core/Blob";
import Nat8 "mo:core/Nat8";
import Text "mo:core/Text";
import Map "mo:core/Map";
import Array "mo:core/Array";
import Iter "mo:core/Iter";
// Requires: mops add sha2
import Sha256 "mo:sha2/Sha256";

persistent actor {

  // Simple certified single-value example:
  var certifiedValue : Text = "";

  // Set a certified value (update call only)
  public func setCertifiedValue(value : Text) : async () {
    certifiedValue := value;
    // Hash the value and set as certified data (max 32 bytes)
    let hash = Sha256.fromBlob(#sha256, Text.encodeUtf8(value));
    CertifiedData.set(hash);
  };

  // Get the certified value with its certificate (query call)
  public query func getCertifiedValue() : async {
    value : Text;
    certificate : ?Blob;
  } {
    {
      value = certifiedValue;
      certificate = CertifiedData.getCertificate();
    }
  };
};
```

**Certified key-value store with Merkle tree (advanced):**

For certifying multiple values with per-key witnesses, use the `ic-certification` mops package (`mops add ic-certification`). It provides a real Merkle tree (`CertTree`) that can generate proofs for individual keys:

```motoko
import CertifiedData "mo:core/CertifiedData";
import Blob "mo:core/Blob";
import Text "mo:core/Text";
// Requires: mops add ic-certification
import CertTree "mo:ic-certification/CertTree";

persistent actor {

  // CertTree.Store is stable -- persists across upgrades
  let certStore : CertTree.Store = CertTree.newStore();
  let ct = CertTree.Ops(certStore);

  // Set certified data on init
  ct.setCertifiedData();

  // Set a key-value pair and update certification
  public func set(key : Text, value : Text) : async () {
    ct.put([Text.encodeUtf8(key)], Text.encodeUtf8(value));
    // CRITICAL: call after every mutation to update the subnet-certified root hash
    ct.setCertifiedData();
  };

  // Delete a key and update certification
  public func remove(key : Text) : async () {
    ct.delete([Text.encodeUtf8(key)]);
    ct.setCertifiedData();
  };

  // Query with certificate and Merkle witness for the requested key
  public query func get(key : Text) : async {
    value : ?Blob;
    certificate : ?Blob;
    witness : Blob;
  } {
    let path = [Text.encodeUtf8(key)];
    // reveal() generates a Merkle proof for this specific path
    let witness = ct.reveal(path);
    {
      value = ct.lookup(path);
      certificate = CertifiedData.getCertificate();
      witness = ct.encodeWitness(witness);
    }
  };

  // Re-establish certification after upgrade
  // (CertTree.Store is stable, so the tree data survives, but certified_data is cleared)
  system func postupgrade() {
    ct.setCertifiedData();
  };
};
```

### Frontend Verification (TypeScript)

Uses `@dfinity/certificate-verification` which handles the full 6-step verification:
1. Verify certificate BLS signature against IC root key
2. Validate certificate freshness (`/time` within `maxCertificateTimeOffsetMs`)
3. CBOR-decode the witness into a HashTree
4. Reconstruct the witness root hash
5. Compare reconstructed root hash with `certified_data` from the certificate
6. Return the verified HashTree for value lookup

```typescript
import { verifyCertification } from "@dfinity/certificate-verification";
import { lookup_path, HashTree } from "@icp-sdk/core/agent";
import { Principal } from "@icp-sdk/core/principal";

const MAX_CERT_TIME_OFFSET_MS = 5 * 60 * 1000; // 5 minutes

async function getVerifiedValue(
  rootKey: ArrayBuffer,
  canisterId: string,
  key: string,
  response: { value: string | null; certificate: ArrayBuffer; witness: ArrayBuffer }
): Promise<string | null> {
  // verifyCertification performs steps 1-5:
  //  - verifies BLS signature on the certificate
  //  - checks certificate /time is within maxCertificateTimeOffsetMs
  //  - CBOR-decodes the witness into a HashTree
  //  - reconstructs root hash from the witness tree
  //  - compares it against certified_data in the certificate
  // Throws CertificateTimeError or CertificateVerificationError on failure.
  const tree: HashTree = await verifyCertification({
    canisterId: Principal.fromText(canisterId),
    encodedCertificate: response.certificate,
    encodedTree: response.witness,
    rootKey,
    maxCertificateTimeOffsetMs: MAX_CERT_TIME_OFFSET_MS,
  });

  // Step 6: Look up the specific key in the verified witness tree.
  // The path must match how the canister inserted the key (e.g., key as UTF-8 bytes).
  const leafData = lookup_path([new TextEncoder().encode(key)], tree);

  if (!leafData) {
    // Key is provably absent from the certified tree
    return null;
  }

  const verifiedValue = new TextDecoder().decode(leafData);

  // Confirm the canister-returned value matches the witness-proven value
  if (response.value !== null && response.value !== verifiedValue) {
    throw new Error(
      "Response value does not match witness — canister returned tampered data"
    );
  }

  return verifiedValue;
}
```

For asset canisters, the HTTP gateway (boundary node) verifies certification transparently using the [HTTP Gateway Protocol](https://docs.internetcomputer.org/references/http-gateway-protocol-spec) -- no client-side code needed.

## Deploy & Test

```bash
# Deploy the canister
icp deploy backend

# Set a certified value (update call -- goes through consensus)
icp canister call backend set '("greeting", "hello world")'

# Query the certified value
icp canister call backend get '("greeting")'
# Returns: record { value = opt "hello world"; certificate = blob "..."; witness = blob "..." }

# Set multiple values
icp canister call backend set '("name", "Alice")'
icp canister call backend set '("age", "30")'

# Delete a value
icp canister call backend delete '("age")'

# Verify the root hash is being set
# (No direct command -- verified by the presence of a non-null certificate in query response)
```

## Verify It Works

```bash
# 1. Verify certificate is present in query response
icp canister call backend get '("greeting")'
# Expected: certificate field is a non-empty blob (NOT null)
# If certificate is null, you are calling from an update context (wrong)

# 2. Verify data integrity after update
icp canister call backend set '("key1", "value1")'
icp canister call backend get '("key1")'
# Expected: value = opt "value1" with valid certificate

# 3. Verify certification survives canister upgrade
icp canister call backend set '("persistent", "data")'
icp deploy backend  # triggers upgrade
icp canister call backend get '("persistent")'
# Expected: certificate is still non-null (postupgrade re-established certification)
# Note: data persistence depends on stable storage implementation

# 4. Verify non-existent key returns null value with valid certificate
icp canister call backend get '("nonexistent")'
# Expected: value = null, certificate = blob "..." (certificate still valid)

# 5. Frontend verification test
# Open browser developer tools, check network requests
# Query responses should include IC-Certificate header
# The service worker (if using asset canister) validates automatically
# Console should NOT show "Certificate verification failed" errors

# 6. For HTTP certification (custom HTTP canister):
curl -v https://CANISTER_ID.ic0.app/path
# Expected: Response headers include IC-Certificate
# HTTP gateway verifies the certificate before forwarding to client
```
