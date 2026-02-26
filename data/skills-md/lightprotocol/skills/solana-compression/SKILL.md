---
name: solana-compression
description: "For client and program development on Solana ~160x cheaper and without rent-exemption for per-user state, DePIN registrations, or custom compressed accounts. Create, update, close, burn, and reinitialize compressed accounts."
metadata:
  source: https://github.com/Lightprotocol/skills
  documentation: https://www.zkcompression.com
  openclaw:
    requires:
      env: ["API_KEY"]  # Helius or Triton RPC key; only needed for devnet/mainnet
      config: ["~/.config/solana/id.json"]  # Solana keypair; only needed for devnet/mainnet
      bins: ["node", "solana", "anchor", "cargo", "light"]
allowed-tools: Bash(git:*), Bash(cargo:*), Bash(anchor:*), Bash(light:*), Read, Edit, Glob, Grep, Write, Task, WebFetch, WebSearch, mcp__deepwiki__ask_question
---

# Compressed PDA Programs

Build Solana programs with compressed accounts via CPI to the Light System Program. No rent-exemption required.

| Creation cost          | Solana account      | Compressed account   |
| :--------------------- | :------------------ | :------------------- |
| **PDA (128 bytes)**    | ~1,100,000 lamports | ~**5,000** lamports  |

## When to use compressed PDAs

- Per-user state (profiles, game state, credentials)
- DePIN device registrations
- Nullifier-based double-spend prevention
- Infrequently accessed accounts

## Choosing approach

| Criteria | Light-PDA (easy) | Compressed PDA (advanced) |
|----------|-----------------|--------------------------|
| When | Rent-free version of existing Anchor accounts | Custom compressed state with ZK proofs |
| Skill | `light-sdk` (Anchor macro pattern) | This skill (`solana-compression`) |
| Macro | `#[light_account(init)]` | `LightAccount::new_init()` manual CPI |
| Dependencies | `light-sdk`, `light-compressible` | `light-sdk`, `light-sdk-types` |

If you just want rent-free Anchor accounts, use the `light-sdk` skill instead. This skill is for programs that require manual CPI to the Light System Program (custom compressed state, ZK proofs, address derivation).

### Client-program interaction flow

```text
 ├─ Client
 │  ├─ Get ValidityProof from RPC.
 │  ├─ pack accounts with PackedAccounts into PackedAddressTreeInfo and PackedStateTreeInfo.
 │  ├─ pack CompressedAccountMeta.
 │  ├─ Build Instruction from PackedAccounts and CompressedAccountMetas.
 │  └─ Send transaction.
 │
 └─ Custom Program
    ├─ CpiAccounts parse accounts consistent with PackedAccounts.
    ├─ LightAccount instantiates from CompressedAccountMeta.
    │
    └─ Light System Program CPI
       ├─ Verify ValidityProof.
       ├─ Update State Merkle tree.
       ├─ Update Address Merkle tree.
       └─ Complete atomic state transition.
```

## Domain references

| Topic | Reference |
|-------|-----------|
| Program operations (create, update, close, burn, reinit) | [references/compressed-pdas.md](references/compressed-pdas.md) |
| Client SDK (TypeScript + Rust) | [references/client.md](references/client.md) |
| Nullifier PDAs (double-spend prevention) | [references/nullifier-pdas.md](references/nullifier-pdas.md) |
| Error codes (6000-16034) | [references/error-codes.md](references/error-codes.md) |

## Reference repos

**Basic operations** — create, update, close, reinit, burn (each with [Anchor](https://github.com/Lightprotocol/program-examples/tree/main/basic-operations/anchor) and [Native](https://github.com/Lightprotocol/program-examples/tree/main/basic-operations/native) variants)

**Counter** — full lifecycle (create, increment, decrement, reset, close):
- [counter/anchor](https://github.com/Lightprotocol/program-examples/tree/main/counter/anchor) — Anchor with Rust and TypeScript tests
- [counter/native](https://github.com/Lightprotocol/program-examples/tree/main/counter/native) — Native with `light-sdk` and Rust tests
- [counter/pinocchio](https://github.com/Lightprotocol/program-examples/tree/main/counter/pinocchio) — Pinocchio with `light-sdk-pinocchio` and Rust tests

**Other examples:**
- [create-and-update](https://github.com/Lightprotocol/program-examples/tree/main/create-and-update) — Create and update with a single validity proof in one instruction
- [read-only](https://github.com/Lightprotocol/program-examples/tree/main/read-only) — Create and read a compressed account onchain
- [account-comparison](https://github.com/Lightprotocol/program-examples/tree/main/account-comparison) — Compressed vs regular Solana accounts

**Nullifier:**
- [nullifier-program](https://github.com/Lightprotocol/nullifier-program) — Rent-free PDA for duplicate execution prevention. SDK: [`light-nullifier-program`](https://docs.rs/light-nullifier-program) | [example client](https://github.com/Lightprotocol/examples-light-token/blob/main/rust-client/actions/create_nullifier.rs)

**Airdrop claim:**
- [simple-claim](https://github.com/Lightprotocol/program-examples/tree/main/airdrop-implementations/simple-claim) — Compressed tokens decompressed to SPL on claim with cliff
- [merkle-distributor](https://github.com/Lightprotocol/program-examples/tree/main/airdrop-implementations/distributor) — SPL tokens with compressed PDA claim tracking, linear vesting, partial claims, clawback
- [example-token-distribution](https://github.com/Lightprotocol/example-token-distribution) — Simple client-side distribution

**ZK programs:**
- [zk-id](https://github.com/Lightprotocol/program-examples/tree/main/zk/zk-id) — Identity verification with Groth16 proofs
- [zk/nullifier](https://github.com/Lightprotocol/program-examples/tree/main/zk/nullifier) — Simple nullifier creation program

**Additional:** [examples-zk-compression](https://github.com/Lightprotocol/examples-zk-compression) — More ZK compression examples

Canonical source: [program-examples README](https://github.com/Lightprotocol/program-examples). If cloned locally, scope `Read`, `Glob`, `Grep` to these repositories and the current project directory only.

## Workflow

1. **Clarify intent**
   - Recommend plan mode, if it's not activated
   - Use `AskUserQuestion` to resolve blind spots
   - All questions must be resolved before execution
2. **Identify references**
   - Match task to [domain references](#domain-references) and [reference repos](#reference-repos)
   - Locate relevant documentation and examples
3. **Write plan file** (YAML task format)
   - Use `AskUserQuestion` for anything unclear — never guess or assume
   - Identify blockers: permissions, dependencies, unknowns
   - Plan must be complete before execution begins
4. **Execute**
   - Use `Task` tool with subagents for parallel research
   - Subagents load skills via `Skill` tool
   - Track progress with `TodoWrite`
5. **When stuck**: ask to spawn a read-only subagent with `Read`, `Glob`, `Grep`, and DeepWiki MCP access, loading `skills/ask-mcp`. Scope reads to skill references, example repos, and docs.

## Build and test

### Required commands

**Anchor programs:**
```bash
anchor build
anchor test
```

**Native programs:**
```bash
cargo build-sbf
cargo test-sbf
```

### Forbidden shortcuts

- Do NOT use `cargo build` (must use `cargo build-sbf`)
- Do NOT use `cargo test` (must use `cargo test-sbf`)
- Do NOT skip SBF compilation
- Tests MUST run against real BPF bytecode

### Failure recovery

On failure, spawn debugger agent with error context.

**Loop rules:**
1. Each debugger gets fresh context + previous debug reports
2. Each attempt tries something DIFFERENT
3. **NEVER GIVE UP** - keep spawning until fixed
4. Max 5 attempts per error

Do NOT proceed until all tests pass.

## SDK references

| Package | Link |
|---------|------|
| `light-sdk` | [docs.rs](https://docs.rs/light-sdk/latest/light_sdk/) |
| `light-client` | [docs.rs](https://docs.rs/light-client/latest/light_client/) |
| `@lightprotocol/stateless.js` | [API docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html) |
| `light-program-test` | [docs.rs](https://docs.rs/crate/light-program-test/latest) |

## DeepWiki fallback

If no matching pattern in reference repos:

```
mcp__deepwiki__ask_question("Lightprotocol/light-protocol", "How to {operation}?")
```


## Security

This skill provides code patterns and documentation references only.

- **Declared dependencies.** Devnet and mainnet examples require `API_KEY` (Helius or Triton RPC key) and read `~/.config/solana/id.json` for the payer keypair. Neither is needed on localnet. In production, load both from a secrets manager.
- **Filesystem scope.** `Read`, `Glob`, and `Grep` must be limited to the current project directory and the [reference repos](#reference-repos) listed above. Do not read outside these paths.
- **Subagent scope.** When stuck, the skill asks to spawn a read-only subagent with `Read`, `Glob`, `Grep` scoped to skill references, example repos, and docs.
- **Install source.** `npx skills add Lightprotocol/skills` from [Lightprotocol/skills](https://github.com/Lightprotocol/skills).
- **Audited protocol.** Light Protocol smart contracts are independently audited. Reports are published at [github.com/Lightprotocol/light-protocol/tree/main/audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits).
