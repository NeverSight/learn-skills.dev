---
name: hyperstack-build
description: Build custom Hyperstack stacks from Solana program IDLs using the Rust DSL. Covers entity definitions, field mappings, views, computed fields, PDA resolution, and deployment with the hs CLI. Use when the user wants to create their own real-time data streaming stack.
allowed-tools: Bash(hs:*) Bash(npx:hyperstack-cli*) Bash(cargo:*)
---

# Building Hyperstack Stacks

A stack watches Solana programs and maps on-chain state into structured, streamable entities. The workflow is: **explore the IDL, understand what the user needs, write the Rust definition, build, deploy.**

## 1. Prerequisites

Required: Rust toolchain, Hyperstack CLI (`hs`), an IDL JSON file. Run once:

```bash
OS="$(uname -s 2>/dev/null || echo Windows)"

if ! command -v cargo &>/dev/null; then
  if [ "$OS" = "Darwin" ] || [ "$OS" = "Linux" ]; then
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path
    source "$HOME/.cargo/env"
  else
    curl -sSLo /tmp/rustup-init.exe https://win.rustup.rs/x86_64
    /tmp/rustup-init.exe -y
    export PATH="$USERPROFILE/.cargo/bin:$PATH"
  fi
fi

if command -v hs &>/dev/null; then
  HS_CLI="hs"
elif command -v hyperstack-cli &>/dev/null; then
  HS_CLI="hyperstack-cli"
else
  cargo install hyperstack-cli
  HS_CLI="hs"
fi
```

> All examples use `hs`. If installed via cargo (`cargo install hyperstack-cli`) or npm (`npm install -g hyperstack-cli`).

## 2. Get the IDL

If the user already has the IDL, place it in `idl/` and skip to step 3.

If not, try in order:
1. Program GitHub repo — look for `target/idl/*.json` or `idl/*.json`
2. `anchor idl fetch <PROGRAM_ID> --provider.cluster mainnet -o idl/program.json`
3. Protocol SDK packages (NPM or crates.io often bundle the IDL)
4. Block explorers (Solscan, Solana.fm — "IDL" tab on the program page)
5. Source generators (Kinobi/Codama) as a last resort

## 3. Explore the IDL

Do this before writing any Rust. Always pass `--json` for machine-readable output.

**Survey** — get the full inventory:

```bash
hs idl summary idl/program.json
hs idl relations idl/program.json --json
hs idl types idl/program.json --json
hs idl events idl/program.json --json
```

`relations` is the most important output — it classifies accounts as Entity, Infrastructure, Role, or Other. Entity accounts are what you'll typically map to `#[entity]` structs.

**Match user intent** — adapt depth to how specific the user's request is:

- **Clear data requirements** — Use `hs idl search`, `hs idl type <name>`, and `hs idl instruction <name>` to confirm each requested field maps to a concrete account field, instruction arg, or event field.
- **App idea but unclear data model** — Use `relations`, `type-graph`, and `pda-graph` to identify entity candidates and relationships. Propose a data model, then proceed once confirmed.
- **No indication** — Use `relations`, `events`, and `search` to surface what the program tracks. Present a short menu of what's possible and narrow scope before coding.

**Close gaps** — before writing code, verify every cross-account link:

```bash
hs idl account-usage idl/program.json <account> --json
hs idl links idl/program.json <account-a> <account-b> --json
hs idl connect idl/program.json <new-account> --existing <a,b> --suggest-hs --json
```

`connect --suggest-hs` output maps directly to `register_from` and `#[aggregate]` decisions in the DSL.

See `references/cli-reference.md` for the full `hs idl` command set.

## 4. Project Setup

```bash
cargo new --lib my-stack && cd my-stack
mkdir -p idl
# copy IDL file(s) into idl/
```

`Cargo.toml`:
```toml
[dependencies]
hyperstack = "0.1"

[build-dependencies]
hyperstack-build = "0.1"

[package.metadata.hyperstack]
idls = ["idl/program.json"]
```

`hyperstack.toml`:
```toml
[project]
name = "my-stack"
```

## 5. Write the Stack Definition

A stack is a Rust module with `#[hyperstack]` containing one or more `#[entity]` structs. Each entity has a primary key and sections (nested structs deriving `Stream`). Fields use mapping macros to declare their data source.

```rust
use hyperstack::prelude::*;

#[hyperstack(idl = ["idl/program.json"])]
mod my_stack {
    use hyperstack::macros::Stream;
    use serde::{Deserialize, Serialize};

    #[entity(name = "Token")]
    #[view(name = "by_volume", sort_by = "metrics.total_volume", order = "desc")]
    pub struct Token {
        pub id: TokenId,
        pub state: TokenState,
        pub metrics: TokenMetrics,
    }

    #[derive(Debug, Clone, Serialize, Deserialize, Stream)]
    pub struct TokenId {
        #[map(program_sdk::accounts::Pool::mint, primary_key, strategy = SetOnce)]
        pub mint: String,
    }

    #[derive(Debug, Clone, Serialize, Deserialize, Stream)]
    pub struct TokenState {
        #[map(program_sdk::accounts::Pool::reserves, strategy = LastWrite)]
        pub reserves: Option<u64>,

        #[snapshot(from = program_sdk::accounts::Pool, strategy = LastWrite)]
        pub pool: Option<Pool>,
    }

    #[derive(Debug, Clone, Serialize, Deserialize, Stream)]
    pub struct TokenMetrics {
        #[aggregate(from = program_sdk::instructions::Swap, field = args::amount, strategy = Sum, lookup_by = accounts::pool)]
        pub total_volume: Option<u64>,

        #[aggregate(from = program_sdk::instructions::Swap, strategy = Count, lookup_by = accounts::pool)]
        pub swap_count: Option<u64>,

        #[derive_from(from = [program_sdk::instructions::Swap], field = __timestamp)]
        pub last_trade_at: Option<i64>,
    }
}
```

Key rules:
- The SDK module name is derived from the IDL's program name: `program_name` becomes `program_name_sdk`
- Account paths: `program_sdk::accounts::AccountType::field_name`
- Instruction paths: `program_sdk::instructions::InstructionName`
- Every entity needs exactly one `primary_key` field
- Section structs must derive `Stream`, `Debug`, `Clone`, `Serialize`, `Deserialize`

**Enriching with off-chain data:** If the user needs data that isn't on-chain (token metadata, images from metadata URIs, external API data), use `#[resolve]`. Two resolver types are available:
- **Token metadata** — `#[resolve(address = "mint_addr")]` or `#[resolve(from = "id.mint")]` on an `Option<TokenMetadata>` field. Fetches name, symbol, decimals, logo from the DAS API. Also provides `ui_amount`/`raw_amount` computed methods for human-readable token amounts.
- **URL fetching** — `#[resolve(url = field.path, extract = "json.path")]` on any field. Fetches JSON from a URL stored in another entity field and extracts a value by path. Use for NFT images, off-chain config, API responses.

See `references/dsl-reference.md` for every macro, strategy, transform, resolver, and cross-account resolution pattern.

## 6. Build & Deploy

```bash
cargo build                          # generates .hyperstack/*.stack.json
hs auth login                        # authenticate
hs up my-stack                       # push + build + deploy
hs sdk create typescript my-stack    # generate SDK
hs status                            # verify
hs explore my-stack --json           # inspect live schema
```

Branch deploys: `hs up my-stack --branch staging` / `hs stack stop my-stack --branch staging`.

See `references/cli-reference.md` for full CLI options.
