---
name: multiversx-cross-contract-calls
description: Make cross-contract calls in MultiversX smart contracts. Use when calling another contract, handling callbacks, managing back-transfers, using typed proxies, or sending tokens via the Tx builder API (.tx().to()).
---

# MultiversX Cross-Contract Calls — Tx Builder API Reference

Complete reference for cross-contract calls, callbacks, back-transfers, and proxies in MultiversX smart contracts (SDK v0.64+).

## Tx Builder Chain

Every cross-contract interaction starts with `self.tx()` and chains builder methods:

```
self.tx()
    .to(address)                        // recipient (ManagedAddress or &ManagedAddress)
    .typed(ProxyType)                   // type-safe proxy (recommended)
    // OR .raw_call("endpoint_name")    // raw call without proxy
    .egld(&amount)                      // payment: EGLD
    // OR .single_esdt(&id, nonce, &amount) // payment: single ESDT
    // OR .payment(payment)             // payment: Payment / EgldOrEsdtTokenPayment
    .gas(gas_limit)                     // explicit gas (required for promises)
    .returns(ReturnsResult)             // result handler(s)
    .sync_call()                        // execution method
```

### Builder Methods

| Category | Method | Description |
|----------|--------|-------------|
| **Target** | `.to(address)` | Set recipient address |
| **Proxy** | `.typed(ProxyType)` | Use generated proxy for type-safe calls |
| **Raw** | `.raw_call("endpoint")` | Manual endpoint call (no proxy) |
| **Payment** | `.egld(&amount)` | Attach EGLD |
| | `.single_esdt(&token_id, nonce, &amount)` | Attach single ESDT |
| | `.esdt(esdt_payment)` | Attach `EsdtTokenPayment` |
| | `.payment(payment)` | Attach any payment type |
| | `.egld_or_single_esdt(&id, nonce, &amount)` | Attach EGLD or ESDT |
| **Gas** | `.gas(amount)` | Set gas limit |
| | `.gas_for_callback(amount)` | Reserve gas for callback |
| **Args** | `.argument(&arg)` | Add single argument (raw calls) |
| | `.arguments_raw(buffer)` | Add pre-encoded arguments |
| **Results** | `.returns(handler)` | Add result handler (can chain multiple) |
| **Callback** | `.callback(closure)` | Set callback for async calls |

### Execution Methods

| Method | Type | Description |
|--------|------|-------------|
| `.sync_call()` | Synchronous | Same-shard atomic. Panics if callee fails. |
| `.sync_call_fallible()` | Synchronous | Same-shard. Returns `Result` on callee error (use with `ReturnsHandledOrError`). |
| `.sync_call_readonly()` | Synchronous | Read-only call. Cannot modify state. |
| `.register_promise()` | Async (v2) | Cross-shard. Requires `.gas()`. Multiple promises per tx OK. |
| `.async_call_and_exit()` | Async (v1) | Legacy. Only 1 per tx. Exits immediately. Prefer `register_promise()`. |
| `.transfer()` | Transfer | Send tokens without calling an endpoint. |

## Simple Transfers (No Endpoint Call)

```rust
// Send EGLD
self.tx().to(&recipient).egld(&amount).transfer();

// Send ESDT
self.tx().to(&recipient).payment(payment.clone()).transfer();

// Send specific ESDT
self.tx().to(&recipient).single_esdt(&token_id, nonce, &amount).transfer();
```

## Synchronous Calls (Same-Shard)

### Typed Proxy Call
```rust
// Basic sync call with typed result
let result: BigUint = self.tx()
    .to(&pool_address)
    .typed(proxy_pool::LiquidityPoolProxy)
    .get_reserve()
    .returns(ReturnsResult)
    .sync_call();
```

### Sync Call with Payment
```rust
self.tx()
    .to(&accumulator_address)
    .typed(proxy_accumulator::AccumulatorProxy)
    .deposit()
    .payment(revenue)
    .returns(ReturnsResult)
    .sync_call();
```

### Multiple Return Values
```rust
// Chain multiple .returns() for multi-value returns
let (result, back_transfers) = self.tx()
    .to(&pool_address)
    .typed(proxy_pool::PoolProxy)
    .withdraw(amount)
    .returns(ReturnsResult)
    .returns(ReturnsBackTransfersReset)
    .sync_call();
```

### Fallible Sync Call
```rust
// Use with ReturnsHandledOrError to not panic on callee error
let outcome: Result<BigUint, u32> = self.tx()
    .to(&address)
    .typed(SomeProxy)
    .some_endpoint()
    .returns(
        ReturnsHandledOrError::new()
            .returns(ReturnsResult)
    )
    .sync_call_fallible();

match outcome {
    Ok(value) => { /* success */ },
    Err(error_code) => { /* callee returned error */ },
}
```

### Raw Call (No Proxy)
```rust
let result: ManagedBuffer = self.tx()
    .to(&address)
    .raw_call("getStatus")
    .argument(&token_id)
    .returns(ReturnsResult)
    .sync_call();
```

## Result Handlers

| Handler | Returns | Description |
|---------|---------|-------------|
| `ReturnsResult` | Decoded return type | Decodes endpoint return value |
| `ReturnsBackTransfersReset` | `BackTransfers` | **Recommended.** Resets back-transfers before call, returns them after. |
| `ReturnsBackTransfers` | `BackTransfers` | Returns back-transfers without resetting (may include leftovers from prior calls). |
| `ReturnsBackTransfersEgld` | `BigUint` | Only the EGLD portion of back-transfers |
| `ReturnsBackTransfersSingleEsdt` | `EsdtTokenPayment` | Single ESDT back-transfer (panics if != 1) |
| `ReturnsNewManagedAddress` | `ManagedAddress` | Address of newly deployed contract |
| `ReturnsHandledOrError` | `Result<T, u32>` | Wraps other handlers; returns error code on failure |

Chain multiple handlers:
```rust
.returns(ReturnsResult)
.returns(ReturnsBackTransfersReset)
.sync_call()
// Returns tuple: (result, back_transfers)
```

## Back-Transfers

Tokens sent back to the caller during a cross-contract call.

### BackTransfers Struct

```rust
pub struct BackTransfers<A: ManagedTypeApi> {
    pub payments: MultiEgldOrEsdtPayment<A>,
}

impl BackTransfers {
    fn egld_sum(&self) -> BigUint              // Sum of all EGLD back-transfers
    fn to_single_esdt(self) -> EsdtTokenPayment // Exactly 1 ESDT (panics otherwise)
    fn into_payment_vec(self) -> PaymentVec     // Convert to ManagedVec<Payment>
    fn into_multi_value(self) -> MultiValueEncoded<EgldOrEsdtTokenPaymentMultiValue>
}
```

### Using Back-Transfers with Result Handlers (Recommended)

```rust
let back_transfers = self.tx()
    .to(&dex_address)
    .typed(DexProxy)
    .swap(token_out, min_amount)
    .payment(input_payment)
    .returns(ReturnsBackTransfersReset)  // ← always use Reset variant
    .sync_call();

// Process returned tokens
let result_payments = back_transfers.into_payment_vec();
for payment in result_payments.iter() {
    vault.deposit(&payment.token_identifier, &payment.amount);
}
```

### Manual Back-Transfer Retrieval

```rust
// Manual approach (less preferred — use result handlers instead)
self.tx().to(&addr).typed(Proxy).some_call().sync_call();
let bt = self.blockchain().get_back_transfers();
self.blockchain().reset_back_transfers(); // MUST reset to prevent double-read
```

## Async Calls (Cross-Shard) — Promises

### Register Promise with Callback

```rust
self.tx()
    .to(&provider)
    .typed(proxy_delegation::DelegationProxy)
    .delegate()
    .egld(&payment)
    .gas(12_000_000u64)
    .callback(
        self.callbacks().delegation_callback(
            provider.clone(),
            &payment,
            &caller,
        ),
    )
    .gas_for_callback(10_000_000u64)
    .register_promise();
```

### Callback Implementation

```rust
#[promises_callback]
fn delegation_callback(
    &self,
    contract_address: ManagedAddress,
    staked_amount: &BigUint,
    caller: &ManagedAddress,
    #[call_result] result: ManagedAsyncCallResult<()>,
) {
    match result {
        ManagedAsyncCallResult::Ok(()) => {
            // Success — process result
            let ls_amount = self.calculate_ls(staked_amount);
            let user_payment = self.mint_ls_token(ls_amount);
            self.tx().to(caller).esdt(user_payment).transfer();
        },
        ManagedAsyncCallResult::Err(_) => {
            // Failure — refund
            self.tx().to(caller).egld(staked_amount).transfer();
        },
    }
}
```

Key callback rules:
- Use `#[promises_callback]` annotation (not `#[callback]` which is legacy)
- `#[call_result]` parameter receives `ManagedAsyncCallResult<T>` where `T` matches callee return
- Callback arguments are passed via `self.callbacks().my_callback(arg1, arg2)` — they're serialized into a `CallbackClosure`
- In callbacks, `self.call_value().all()` gets tokens sent back
- Multiple `register_promise()` calls allowed in a single transaction

### Promise without Callback

```rust
// Fire-and-forget (no callback needed)
self.tx()
    .to(&address)
    .typed(Proxy)
    .some_endpoint()
    .gas(5_000_000u64)
    .register_promise();
```

## Typed Proxy Pattern

Proxies are generated from contract interfaces. They provide type-safe endpoint calls.

### Proxy Generation

Proxies are auto-generated by the framework from contract trait definitions. The generated proxy module is typically in a `proxy/` directory or a `proxy_*.rs` file.

```rust
// In your contract, use the proxy:
use crate::proxy_pool;

// Call via typed proxy
self.tx()
    .to(&pool_address)
    .typed(proxy_pool::LiquidityPoolProxy)
    .deposit(token_id, amount)
    .payment(payment)
    .returns(ReturnsResult)
    .sync_call();
```

### Deploy via Proxy

```rust
let new_address: ManagedAddress = self.tx()
    .typed(proxy_pool::LiquidityPoolProxy)
    .init(base_asset, max_rate, threshold)
    .from_source(self.template_address().get())
    .code_metadata(CodeMetadata::UPGRADEABLE | CodeMetadata::READABLE)
    .returns(ReturnsNewManagedAddress)
    .sync_call();
```

## Common Patterns

### Swap and Forward Results
```rust
let back_transfers = self.tx()
    .to(&dex)
    .typed(DexProxy)
    .swap(token_out, min_out)
    .payment(input)
    .returns(ReturnsBackTransfersReset)
    .sync_call();

let output = back_transfers.into_payment_vec();
let caller = self.blockchain().get_caller();
for payment in output.iter() {
    self.tx().to(&caller).payment(payment.clone()).transfer();
}
```

### Multi-Step with Back-Transfer Tracking
```rust
// Step 1: withdraw from pool
let (withdrawn_amount, bt1) = self.tx()
    .to(&pool)
    .typed(PoolProxy)
    .withdraw(shares)
    .returns(ReturnsResult)
    .returns(ReturnsBackTransfersReset)
    .sync_call();

// Step 2: deposit into another pool
self.tx()
    .to(&other_pool)
    .typed(OtherPoolProxy)
    .deposit()
    .payment(bt1.into_payment_vec().get(0).clone())
    .returns(ReturnsResult)
    .sync_call();
```

## Anti-Patterns

```rust
// BAD: Using ReturnsBackTransfers without reset — may include stale data
.returns(ReturnsBackTransfers).sync_call()

// GOOD: Always use Reset variant
.returns(ReturnsBackTransfersReset).sync_call()

// BAD: Missing gas on register_promise — will panic
self.tx().to(&addr).typed(Proxy).call().register_promise();

// GOOD: Always set gas for async calls
self.tx().to(&addr).typed(Proxy).call().gas(10_000_000u64).register_promise();

// BAD: Using legacy send() API
self.send().direct_egld(&to, &amount);

// GOOD: Use Tx builder API
self.tx().to(&to).egld(&amount).transfer();

// BAD: Manual back-transfer without reset
let bt = self.blockchain().get_back_transfers();
// Forgot reset — next call will see same transfers again!

// GOOD: Always reset after manual retrieval
let bt = self.blockchain().get_back_transfers();
self.blockchain().reset_back_transfers();
// Or better: use ReturnsBackTransfersReset in the result handler

// BAD: Using #[callback] with register_promise
#[callback]  // ← This is for legacy async_call_and_exit only
fn my_callback(&self) { }

// GOOD: Use #[promises_callback] for register_promise
#[promises_callback]
fn my_callback(&self) { }
```
