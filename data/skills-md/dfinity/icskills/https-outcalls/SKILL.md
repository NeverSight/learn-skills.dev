---
name: https-outcalls
description: "Make HTTPS requests from canisters to external web APIs. Covers transform functions for consensus, cycle cost management, response size limits, and idempotency patterns. Use when a canister needs to call an external API, fetch data from the web, or make HTTP requests. Do NOT use for EVM/Ethereum calls — use evm-rpc instead."
license: Apache-2.0
compatibility: "icp-cli >= 0.1.0"
metadata:
  title: HTTPS Outcalls
  category: Integration
---

# HTTPS Outcalls

## What This Is

HTTPS outcalls allow canisters to make HTTP requests to external web services directly from on-chain code. Because the Internet Computer runs on a replicated subnet (multiple nodes execute the same code), all nodes must agree on the response. A transform function strips non-deterministic fields (timestamps, request IDs, ordering) so that every replica sees an identical response and can reach consensus.

## Prerequisites

- For Motoko: `mo:core` 2.0 and `ic >= 2.1.0` in mops.toml
- For Rust: `ic-cdk >= 0.19`, `serde_json` for JSON parsing

## Canister IDs

HTTPS outcalls use the IC management canister:

| Name | Canister ID | Used For |
|------|-------------|----------|
| Management canister | `aaaaa-aa` | The `http_request` management call target |

You do not deploy anything extra. The management canister is built into every subnet.

## Mistakes That Break Your Build

1. **Forgetting the transform function.** Without a transform, the raw HTTP response often differs between replicas (different headers, different ordering in JSON fields, timestamps). Consensus fails and the call is rejected. ALWAYS provide a transform function.

2. **Not attaching cycles to the call.** HTTPS outcalls are not free. The calling canister must attach cycles to cover the cost. If you attach zero cycles, the call fails immediately. Both Motoko and Rust have wrappers that compute and attach the required cycles automatically: in Motoko, use `await Call.httpRequest(args)` from the `ic` mops package (`import Call "mo:ic/Call"`); in Rust, use `ic_cdk::management_canister::http_request` (available since ic-cdk 0.18). Under the hood, both use the `ic0.cost_http_request` system API to calculate the exact cost from `request_size` and `max_response_bytes`.

3. **Using HTTP instead of HTTPS.** The IC only supports HTTPS outcalls. Plain HTTP URLs are rejected. The target server must have a valid TLS certificate.

4. **Exceeding the 2MB response limit.** The maximum response body is 2MB (2_097_152 bytes). If the external API returns more, the call fails. Use the `max_response_bytes` field to set a limit and design your queries to return small responses.

5. **Omitting `max_response_bytes`.** If you do not set `max_response_bytes`, the system assumes the maximum (2MB) and charges cycles accordingly — roughly 21.5 billion cycles on a 13-node subnet. Always set this to a reasonable upper bound for your expected response.

6. **Non-idempotent POST requests without caution.** Because multiple replicas make the same request, a POST endpoint that is not idempotent (e.g., "create order") will be called N times (once per replica, typically 13 on a 13-node subnet). Use idempotency keys or design endpoints to handle duplicate requests.

7. **Not handling outcall failures.** External servers can be down, slow, or return errors. Always handle the error case. On the IC, if the external server does not respond within the timeout (~30 seconds), the call traps.

8. **Calling localhost or private IPs.** HTTPS outcalls can only reach public internet endpoints. Localhost, 10.x.x.x, 192.168.x.x, and other private ranges are blocked.

9. **Forgetting the `Host` header.** Some API endpoints require the `Host` header to be explicitly set. The IC does not automatically set this from the URL.

## Implementation

### Motoko

The management canister types are imported via `import IC "ic:aaaaa-aa"` (compiler-provided). The `ic` mops package (`import Call "mo:ic/Call"`) provides `Call.httpRequest` which auto-computes and attaches the required cycles.

```motoko
import Blob "mo:core/Blob";
import Nat "mo:core/Nat";
import Text "mo:core/Text";
import IC "ic:aaaaa-aa";
import Call "mo:ic/Call";

persistent actor {

  // Transform function: strips headers so all replicas see the same response for consensus.
  // MUST be a `shared query` function.
  public query func transform({
    context : Blob;
    response : IC.http_request_result;
  }) : async IC.http_request_result {
    {
      response with headers = []; // Strip headers -- they often contain non-deterministic values
    };
  };

  // GET request: fetch a JSON API
  public func getIcpPriceUsd() : async Text {
    let url = "https://api.coingecko.com/api/v3/simple/price?ids=internet-computer&vs_currencies=usd";

    let request : IC.http_request_args = {
      url = url;
      max_response_bytes = ?(10_000 : Nat64); // Always set — omitting defaults to 2MB and charges accordingly
      headers = [
        { name = "User-Agent"; value = "ic-canister" },
      ];
      body = null;
      method = #get;
      transform = ?{
        function = transform;
        context = Blob.fromArray([]);
      };
      is_replicated = null;
    };

    // Call.httpRequest computes and attaches the required cycles automatically
    let response = await Call.httpRequest(request);

    switch (Text.decodeUtf8(response.body)) {
      case (?text) { text };
      case (null) { "Response is not valid UTF-8" };
    };
  };

  // POST transform: also discards the body because httpbin.org includes the
  // sender's IP in the "origin" field, which differs across replicas.
  public query func transformPost({
    context : Blob;
    response : IC.http_request_result;
  }) : async IC.http_request_result {
    {
      response with
      headers = [];
      body = Blob.fromArray([]);
    };
  };

  // POST request: send JSON data
  public func postData(jsonPayload : Text) : async Text {
    let url = "https://httpbin.org/post";

    let request : IC.http_request_args = {
      url = url;
      max_response_bytes = ?(50_000 : Nat64);
      headers = [
        { name = "Content-Type"; value = "application/json" },
        { name = "User-Agent"; value = "ic-canister" },
        // Idempotency key: prevents duplicate processing if multiple replicas hit the endpoint
        { name = "Idempotency-Key"; value = "unique-request-id-12345" },
      ];
      body = ?Text.encodeUtf8(jsonPayload);
      method = #post;
      transform = ?{
        function = transformPost;
        context = Blob.fromArray([]);
      };
      is_replicated = null;
    };

    // Call.httpRequest computes and attaches the required cycles automatically
    let response = await Call.httpRequest(request);

    if (response.status == 200) {
      "POST successful (status 200)";
    } else {
      "POST failed with status " # Nat.toText(response.status);
    };
  };
};
```

### Rust

```toml
# Cargo.toml
[package]
name = "https_outcalls_backend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
ic-cdk = "0.19"
candid = "0.10"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

```rust
use ic_cdk::api::canister_self;
use ic_cdk::management_canister::{
    http_request, HttpHeader, HttpMethod, HttpRequestArgs, HttpRequestResult,
    TransformArgs, TransformContext, TransformFunc,
};
use ic_cdk::{query, update};
use serde::Deserialize;

/// Transform function: strips non-deterministic headers so all replicas agree.
/// MUST be a #[query] function.
#[query(hidden = true)]
fn transform(args: TransformArgs) -> HttpRequestResult {
    HttpRequestResult {
        status: args.response.status,
        body: args.response.body,
        headers: vec![], // Strip all headers for consensus
        // If you need specific headers, filter them here:
        // headers: args.response.headers.into_iter()
        //     .filter(|h| h.name.to_lowercase() == "content-type")
        //     .collect(),
    }
}

/// GET request: Fetch JSON from an external API
#[update]
async fn fetch_price() -> String {
    let url = "https://api.coingecko.com/api/v3/simple/price?ids=internet-computer&vs_currencies=usd";

    let request = HttpRequestArgs {
        url: url.to_string(),
        max_response_bytes: Some(10_000),
        method: HttpMethod::GET,
        headers: vec![
            HttpHeader {
                name: "User-Agent".to_string(),
                value: "ic-canister".to_string(),
            },
        ],
        body: None,
        transform: Some(TransformContext {
            function: TransformFunc::new(canister_self(), "transform".to_string()),
            context: vec![],
        }),
        is_replicated: None,
    };

    // http_request calls automatically attaches the required cycles
    match http_request(&request).await {
        Ok(response) => {
            let body = String::from_utf8(response.body)
                .unwrap_or_else(|_| "Invalid UTF-8 in response".to_string());

            if response.status != candid::Nat::from(200u64) {
                return format!("HTTP error: status {}", response.status);
            }

            body
        }
        Err(err) => {
            format!("HTTP outcall failed: {:?}", err)
        }
    }
}

/// Typed response parsing example
#[derive(Deserialize)]
struct PriceResponse {
    #[serde(rename = "internet-computer")]
    internet_computer: PriceData,
}

#[derive(Deserialize)]
struct PriceData {
    usd: f64,
}

#[update]
async fn get_icp_price_usd() -> String {
    let body = fetch_price().await;

    match serde_json::from_str::<PriceResponse>(&body) {
        Ok(parsed) => format!("ICP price: ${:.2}", parsed.internet_computer.usd),
        Err(e) => format!("Failed to parse price response: {}", e),
    }
}

/// POST transform: strips headers AND body because httpbin.org includes the
/// sender's IP in the "origin" field, which differs across replicas.
#[query(hidden = true)]
fn transform_post(args: TransformArgs) -> HttpRequestResult {
    HttpRequestResult {
        status: args.response.status,
        body: vec![],
        headers: vec![],
    }
}

/// POST request: Send JSON data to an external API
#[update]
async fn post_data(json_payload: String) -> String {
    let url = "https://httpbin.org/post";

    let request = HttpRequestArgs {
        url: url.to_string(),
        max_response_bytes: Some(50_000),
        method: HttpMethod::POST,
        headers: vec![
            HttpHeader {
                name: "Content-Type".to_string(),
                value: "application/json".to_string(),
            },
            HttpHeader {
                name: "User-Agent".to_string(),
                value: "ic-canister".to_string(),
            },
            // Idempotency key: prevents duplicate processing across replicas
            HttpHeader {
                name: "Idempotency-Key".to_string(),
                value: "unique-request-id-12345".to_string(),
            },
        ],
        body: Some(json_payload.into_bytes()),
        transform: Some(TransformContext {
            function: TransformFunc::new(canister_self(), "transform_post".to_string()),
            context: vec![],
        }),
        is_replicated: None,
    };

    // http_request automatically attaches the required cycles
    match http_request(&request).await {
        Ok(response) => {
            if response.status == candid::Nat::from(200u64) {
                "POST successful (status 200)".to_string()
            } else {
                format!("POST failed with status {}", response.status)
            }
        }
        Err(err) => {
            format!("HTTP outcall failed: {:?}", err)
        }
    }
}
```

### Cycle Cost Estimation

The `ic0.cost_http_request` system API computes the exact cycle cost at runtime, so canisters do not need to hard-code the formula. Both `Call.httpRequest` from the `ic` mops package (Motoko) and `ic_cdk::management_canister::http_request` (Rust) call it internally and attach the required cycles automatically. For manual use: in Motoko, `Prim.costHttpRequest(requestSize, maxResponseBytes)` (via `import Prim "mo:⛔"`); in Rust, `ic_cdk::api::cost_http_request(request_size, max_res_bytes)`.

`request_size` is the sum of byte lengths of the URL, all header names and values, the body, the transform function name, and the transform context.

For reference, the underlying formula on a 13-node subnet (n = 13) is:

```text
Base cost:                      49_140_000 cycles  (= (3_000_000 + 60_000*13) * 13)
+ per request byte:              5_200 cycles      (= 400 * 13)
+ per max_response_bytes byte:  10_400 cycles      (= 800 * 13)

IMPORTANT: The charge is against max_response_bytes, NOT actual response size.
If you omit max_response_bytes, the system assumes 2MB and charges ~21.5B cycles.
```

Unused cycles are refunded to the canister, so it is safe to over-budget.

## Deploy & Test

### Local Deployment

```bash
# Start the local replica
icp network start -d

# Deploy your canister
icp deploy backend
```

Note: HTTPS outcalls work on the local replica. icp-cli proxies the requests through the local HTTP gateway.

### Mainnet Deployment

```bash
# Ensure your canister has enough cycles (check balance first)
icp canister status backend -e ic

# Deploy
icp deploy -e ic backend
```

## Verify It Works

```bash
# 1. Test the GET outcall (fetch price)
icp canister call backend fetchPrice
# Expected: Something like '("{\"internet-computer\":{\"usd\":12.34}}")'
# (actual price will vary)

# 2. Test the POST outcall
icp canister call backend postData '("{\"test\": \"hello\"}")'
# Expected: JSON response from httpbin.org echoing back your data

# 3. If using Rust with the typed parser:
icp canister call backend get_icp_price_usd
# Expected: '("ICP price: $12.34")'

# 4. Check canister cycle balance (outcalls consume cycles)
icp canister status backend
# Verify the balance decreased slightly after outcalls

# 5. Test error handling: call with an unreachable URL
# Add a test function that calls a non-existent domain and verify
# it returns an error message rather than trapping
```

### Debugging Outcall Failures

If an outcall fails:

```bash
# Check the replica log for detailed error messages
# Local: icp output shows errors inline
# Mainnet: check the canister logs

# Common errors:
# "Timeout" -- external server took too long (>30s)
# "No consensus" -- transform function is missing or not stripping enough
# "Body size exceeds limit" -- response > max_response_bytes
# "Not enough cycles" -- attach more cycles to the call
```

### Transform Debugging

If you get "no consensus could be reached" errors, your transform function is not making responses identical. Common culprits:

1. **Response headers differ** -- strip ALL headers in the transform
2. **JSON field ordering differs** -- parse and re-serialize the JSON in the transform
3. **Timestamps in response body** -- extract only the fields you need

Advanced transform that normalizes JSON:

```rust
#[query]
fn transform_normalize(args: TransformArgs) -> HttpRequestResult {
    // Parse and re-serialize to normalize field ordering
    let body = if let Ok(json) = serde_json::from_slice::<serde_json::Value>(&args.response.body) {
        serde_json::to_vec(&json).unwrap_or(args.response.body)
    } else {
        args.response.body
    };

    HttpRequestResult {
        status: args.response.status,
        body,
        headers: vec![],
    }
}
```
