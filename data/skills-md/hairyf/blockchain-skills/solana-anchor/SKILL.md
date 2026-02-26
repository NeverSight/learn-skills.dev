---
name: solana-anchor
description: Agent-oriented skills for the Anchor framework—Solana program structure, accounts, CPI, IDL, clients, and tooling.
metadata:
  author: Hairy
  version: "2026.2.25"
  source: Generated from https://github.com/solana-foundation/anchor, scripts located at https://github.com/antfu/skills
---

> Skill based on Anchor (Solana program framework), generated from `sources/solana-anchor/docs/` at 2026-02-25.

Anchor is a Solana program framework: Rust eDSL with macros (`declare_id`, `#[program]`, `#[derive(Accounts)]`, `#[account]`), IDL generation, TypeScript/Rust clients, and CLI for build, test, and deploy. Use this skill when implementing or reviewing Anchor programs, CPIs, account validation, and client integration.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Program Structure | declare_id, #[program], #[derive(Accounts)], #[account], Context, discriminators | [core-program-structure](references/core-program-structure.md) |
| CPI | Cross-program invocation, CpiContext, PDA signers, invoke/invoke_signed | [core-cpi](references/core-cpi.md) |
| IDL | Interface Description Language, instructions/accounts/discriminators, client use | [core-idl](references/core-idl.md) |
| PDA | Program Derived Addresses, seeds, bump, seeds::program, init, IDL resolution | [core-pda](references/core-pda.md) |
| Workspace | init, new, program layout, build/test/deploy flow | [core-workspace](references/core-workspace.md) |
| Realloc | Resize accounts, realloc::payer, realloc::zero | [core-realloc](references/core-realloc.md) |
| Close Account | close = target, rent reclamation | [core-close-account](references/core-close-account.md) |
| Remaining Accounts | ctx.remaining_accounts, variadic instructions, CPI | [core-remaining-accounts](references/core-remaining-accounts.md) |

## References (Program & Config)

| Topic | Description | Reference |
|-------|-------------|-----------|
| Account Types | Account, Signer, Program, AccountLoader, UncheckedAccount, etc. | [references-account-types](references/references-account-types.md) |
| Account Constraints | init, mut, seeds/bump, has_one, close, realloc, SPL, #[instruction] | [references-account-constraints](references/references-account-constraints.md) |
| Anchor.toml | provider, scripts, workspace, programs, test, toolchain, hooks | [references-anchor-toml](references/references-anchor-toml.md) |
| CLI | build, deploy, test, idl, keys, migrate, upgrade, verify | [references-cli](references/references-cli.md) |
| Space | Account size calculation, InitSpace, type sizes | [references-space](references/references-space.md) |
| Type Conversion | Rust ↔ TypeScript type mapping for IDL/client | [references-type-conversion](references/references-type-conversion.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Events | emit!, emit_cpi!, addEventListener, decoding | [features-events](references/features-events.md) |
| Errors | #[error_code], err!, require! and variants | [features-errors](references/features-errors.md) |
| Zero-Copy | AccountLoader, load_init/load_mut/load, init vs zero | [features-zero-copy](references/features-zero-copy.md) |
| declare_program! | IDL-based CPI and Rust client generation | [features-declare-program](references/features-declare-program.md) |
| Tokens (SPL) | anchor-spl, mints, token accounts, ATAs, Token 2022, InterfaceAccount | [features-tokens](references/features-tokens.md) |
| Token 2022 Extensions | ExtensionType, tlv_data, extension lifecycle, anchor-spl token_2022_extensions | [features-token-extensions](references/features-token-extensions.md) |
| Example Programs | Curated program-examples repo—Basics, Tokens, Token 2022—when to use each | [features-examples](references/features-examples.md) |
| Testing | Mollusk (Rust instruction harness), LiteSVM (Rust/TS/Python VM) | [features-testing](references/features-testing.md) |
| Upgrade and Migrate | anchor upgrade, migrate script, upgrade authority | [features-upgrade-migrate](references/features-upgrade-migrate.md) |

## Clients

| Topic | Description | Reference |
|-------|-------------|-----------|
| TypeScript | Program, methods, accounts, signers, rpc/transaction/instruction, fetch | [clients-typescript](references/clients-typescript.md) |
| Rust | anchor-client, declare_program!, request/instructions/send, account fetch | [clients-rust](references/clients-rust.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Security | Sealevel attacks, constraints, UncheckedAccount usage | [best-practices-security](references/best-practices-security.md) |
| Constraints and Validation | When to use which constraints, avoid UncheckedAccount pitfalls | [best-practices-constraints](references/best-practices-constraints.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Verifiable Builds | anchor build --verifiable, verify, Docker | [advanced-verifiable-builds](references/advanced-verifiable-builds.md) |
| AVM | Anchor Version Manager, install, use, list | [advanced-avm](references/advanced-avm.md) |
