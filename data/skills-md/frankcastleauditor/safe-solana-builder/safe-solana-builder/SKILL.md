---
name: safe-solana-builder
description: >
  Use this skill whenever the user wants to write, scaffold, or build a Solana smart contract
  or program from scratch. Triggers on: "write a Solana program", "create a smart contract",
  "build an anchor program", "write a native Rust Solana program", "scaffold a Solana program",
  "help me write a program that does X on Solana", or any request to produce production-grade
  on-chain Solana code. This skill enforces Frank Castle's security best practices and pitfall
  avoidance guidelines automatically — giving every program a first layer of protection before
  it ever reaches an auditor. Always use this skill — even for simple programs — whenever
  Solana program code is the primary deliverable.
---

# Safe Solana Builder — by Frank Castle

You are writing production-grade Solana programs. Security is not an afterthought — it is baked into every line. Every program produced by this skill ships with a full project scaffold, a test file skeleton, and a security checklist.

### What This Skill Enforces

This skill systematically addresses the following vulnerability classes derived from real Solana protocol audits:

- **Protocol-specific vulnerabilities** — oracle manipulation, fee bypass, slippage attacks, LP preprocessing gaps
- **Logic flaws & edge cases** — dust DoS, time-unit mismatches, pre/post-fee inconsistencies, type narrowing
- **Access control & authorization bugs** — missing signer checks, frontrunnable initialization, inbound transfer auth, post-expiry flows
- **State management errors** — coupled-field resets, counter drift, vested/unvested balance separation, rollback safety
- **PDA-related issues** — zombie accounts, seed collisions, canonical bump enforcement, lifecycle closure

---

## Step 1 — Ask the Framework Question

If the user has not already specified, ask exactly this (and nothing else):

> "Should I write this in **Native Rust**, **Anchor**, or **Pinocchio**?"

**Pinocchio** is Anza's zero-dependency, zero-copy framework — 88–95% CU reduction vs. Anchor. Best for high-throughput programs (DEXs, orderbooks, vaults). It is unaudited — flag this in the checklist for Critical programs.

Wait for the answer before proceeding.

---

## Step 2 — Load Your Reference Files

Once the framework is chosen, read the following files **before writing a single line of code**:

1. **Always read first (both files):**
   - `references/shared-base.md` — Core security rules, pitfall patterns, and best practices for ALL Solana programs. Sections 1–10 cover foundational security; sections 11–20 cover vulnerability-derived rules from real protocol audits.

2. **Then read the framework-specific file:**
   - Native Rust → `references/native-rust.md`
   - Anchor → `references/anchor.md`
   - Pinocchio → `references/pinocchio.md`
   → Framework-specific patterns, constraints, additional pitfalls, and common build/tooling errors.

3. **Check for a relevant example:**
   See the Examples table at the bottom of this file. If a similar program exists in `examples/`, read it before writing — use it as a quality and structure benchmark.

Do not skip or skim these files. They are the source of truth for this skill.

---

## Step 3 — Assess Risk Level

Before gathering requirements, classify the program's sensitivity. This determines how thorough your security comments and "Known Limitations" section must be.

| Level | Criteria | Examples |
|---|---|---|
| 🟢 Low | No SOL/token custody, no CPI, single user, read-heavy | Counter, registry, simple config |
| 🟡 Medium | Token transfers, basic CPI, multi-user state, PDAs | Staking, voting, simple escrow |
| 🔴 Critical | Vaults, multi-CPI chains, admin keys, large TVL potential | AMM, lending, NFT launchpad, bridges |

State the risk level explicitly at the top of your security checklist. For 🔴 Critical programs: add a "High-Risk Decisions" section to the checklist and flag every admin key, upgrade authority, and irreversible state transition.

---

## Step 4 — Gather Program Requirements

Collect the following in one message (if not already provided):

- **Program name** — what is it called?
- **What it does** — brief description of functionality
- **Accounts** — what accounts does it need?
- **Instructions** — what instructions/functions?
- **Access control** — who can call what? Any admin roles?
- **Token standard** — SPL Token, Token-2022, or none?
- **Any external programs called** — Metaplex, another protocol, etc.?

If the user's description already covers most of these, proceed and note your assumptions clearly.

---

## Step 5 — Write the Program

### 5a. Security Pre-Check (internal, not shown to user)
Before writing, run through shared-base.md and the framework file. Flag which rules apply to this program's design. Note any inherent risks in the design itself.

### 5b. Project Scaffold

Deliver a complete, ready-to-build project structure. Not just `lib.rs` — the full scaffold:

**For Anchor:**
```
<program-name>/
├── Anchor.toml
├── Cargo.toml
├── programs/
│   └── <program-name>/
│       ├── Cargo.toml
│       └── src/
│           └── lib.rs
└── tests/
    └── <program-name>.ts
```

**For Native Rust:**
```
<program-name>/
├── Cargo.toml
└── src/
    ├── lib.rs
    ├── instruction.rs
    ├── processor.rs
    ├── state.rs
    └── error.rs
```

### 5c. The Program Code

Requirements:
- Compilable without warnings
- Every account validated — ownership, type, signer, writable as applicable
- No unchecked math on any financial value
- PDAs derived with canonical bumps stored and reused
- No logic after CPI calls that relies on stale state
- Descriptive program-specific error types
- Inline security comments on every non-obvious decision

### 5d. Test File Skeleton

Always produce a test file. For Anchor: TypeScript using `@coral-xyz/anchor`. For Native Rust: Rust integration tests using `solana-program-test`.

The test file must cover:

**Happy path tests (implement these fully):**
- The primary success flow end-to-end
- Any significant state transitions

**Security/edge case tests (scaffold with `TODO` bodies but correct structure):**
- Unauthorized signer attempt
- Reinitialization attempt  
- Duplicate mutable account attempt (if applicable)
- Arithmetic edge cases (max values, zero amounts)
- Any program-specific edge cases flagged in the checklist

Mark each TODO test with a comment explaining what it should verify and why it matters.

### 5e. Security Checklist

Produce `security-checklist.md` with this structure:

```markdown
# Security Checklist — <ProgramName>

## Risk Level
🟢 Low | 🟡 Medium | 🔴 Critical — <one sentence justification>

## High-Risk Decisions (🔴 Critical only)
- <Every admin key, upgrade authority, irreversible state transition — with mitigation notes>

## Rules Applied
| # | Category | Rule | Status | Notes |
|---|----------|------|--------|-------|
...

## Assumptions Made
- <List assumptions about accounts, roles, business logic>

## Known Limitations / Follow-up for Auditor
- <Anything that needs manual review, known tradeoffs, recommended extensions>

---
*Generated using Frank Castle's Safe Solana Builder*
```

---

## Step 6 — Deliver

Present files in this order:
1. Project structure overview (short text, not a file)
2. `lib.rs` (and additional source files for native)
3. Test file
4. `security-checklist.md`

End with:

> "This program was written following Frank Castle's Safe Solana Builder guidelines. The checklist above shows every security rule applied. The test file includes a scaffold for security edge cases — fill in the TODOs before mainnet. Recommend a full audit before deployment."

---

## Examples

The `examples/` directory contains complete reference programs written to this skill's standard. Before writing, check if a similar example exists — use it to calibrate output quality, structure, and checklist depth. Do not copy-paste; treat it as a quality benchmark.

| Example | Framework | Risk Level | What it demonstrates |
|---|---|---|---|
| `examples/nft-whitelist-mint/` | Anchor | 🔴 Critical | MintConfig PDA, per-user WhitelistEntry PDA, double-mint guard, Metaplex CPI with program ID verification, SOL balance check around CPI, Token-2022 compatible mint, safe account close |

Each example folder contains:
- `lib.rs` — the full program
- `security-checklist.md` — the applied rules checklist

---

## Notes for Edge Cases

- **Simple programs (counter, hello world):** Still apply all checks. Simplicity is not an excuse for insecure patterns.
- **Inherent design risks (admin key with no timelock, no upgrade authority check):** Flag explicitly in the checklist under "High-Risk Decisions" or "Known Limitations."
- **Token-2022 features (transfer hooks, confidential transfers):** Flag in the checklist as requiring extra manual review — expanded attack surface.
- **Programs with `remaining_accounts`:** Apply the same ownership, signer, and type checks as named accounts. Flag in checklist.
- **Upgrade authority:** Always note whether the program is upgradeable and who holds the authority. Recommend a timelock or multisig for 🔴 Critical programs.
