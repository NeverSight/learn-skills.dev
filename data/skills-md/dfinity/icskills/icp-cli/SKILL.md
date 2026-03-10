---
name: icp-cli
description: "Guides use of the icp command-line tool for building and deploying Internet Computer applications. Covers project configuration (icp.yaml), recipes, environments, canister lifecycle, and identity management. Use when building, deploying, or managing any IC project. Use when the user mentions icp, dfx, canister deployment, local network, or project setup. Do NOT use for canister-level programming patterns like access control, inter-canister calls, or stable memory — use domain-specific skills instead."
license: Apache-2.0
metadata:
  title: ICP CLI
  category: Infrastructure
---

# ICP CLI

## What This Is

The `icp` command-line tool builds and deploys applications on the Internet Computer. It replaces the legacy `dfx` tool with YAML configuration, a recipe system for reusable build templates, and an environment model that separates deployment targets from network connections. Never use `dfx` — always use `icp`.

## Prerequisites

- For Rust canisters: `rustup target add wasm32-unknown-unknown`
- For Motoko canisters: `npm i -g ic-mops` and `moc` version defined in `mops.toml` (templates include this; for manual projects add `[toolchain]` with `moc = "<version>"`)
- For frontend assets: Node.js >= 20

## Common Pitfalls

1. **Using `dfx` instead of `icp`.** The `dfx` tool is legacy. All commands have `icp` equivalents — see `references/dfx-migration.md` for the full command mapping. Never generate `dfx` commands or reference `dfx` documentation. Configuration uses `icp.yaml`, not `dfx.json` — and the structure differs: canisters are an array of objects, not a keyed object.

2. **Using `--network ic` to deploy to mainnet.** icp-cli uses environments, not direct network targeting. The correct flag is `-e ic` (short for `--environment ic`).
   ```bash
   # Wrong
   icp deploy --network ic
   # Correct
   icp deploy -e ic
   ```
   Note: `-n` / `--network` targets a network directly and works with canister IDs (principals). Use `-e` / `--environment` when referencing canisters by name. For token and cycles operations, use `-n` since they don't reference project canisters.

3. **Using a recipe without a version pin.** icp-cli rejects unpinned recipe references. Always include an explicit version. Official recipes are hosted at [dfinity/icp-cli-recipes](https://github.com/dfinity/icp-cli-recipes).
   ```yaml
   # Wrong — rejected by icp-cli
   recipe:
     type: "@dfinity/rust"

   # Correct — pinned version
   recipe:
     type: "@dfinity/rust@v3.2.0"
   ```

4. **Writing manual build steps when a recipe exists.** Official recipes handle Rust, Motoko, and asset canister builds. Use them instead of writing shell commands:
   ```yaml
   # Unnecessary — use a recipe instead
   build:
     steps:
       - type: script
         commands:
           - cargo build --target wasm32-unknown-unknown --release
           - cp target/.../backend.wasm "$ICP_WASM_OUTPUT_PATH"

   # Preferred
   recipe:
     type: "@dfinity/rust@v3.2.0"
     configuration:
       package: backend
   ```

5. **Not committing `.icp/data/` to version control.** Mainnet canister IDs are stored in `.icp/data/mappings/<environment>.ids.json`. Losing this file means losing the mapping between canister names and on-chain IDs. Always commit `.icp/data/` — never delete it. Add `.icp/cache/` to `.gitignore` (it is ephemeral and rebuilt automatically).

6. **Using `icp identity use` instead of `icp identity default`.** The dfx command `dfx identity use` became `icp identity default`. Similarly, `dfx identity get-principal` became `icp identity principal`, and `dfx identity remove` became `icp identity delete`.

7. **Confusing networks and environments.** A network is a connection endpoint (URL). An environment combines a network + canisters + settings. You deploy to environments (`-e`), not networks. Multiple environments can target the same network with different settings (e.g., staging and production both on `ic`).

8. **Forgetting that local networks are project-local.** Unlike dfx which runs one shared global network, icp-cli runs a local network per project. You must run `icp network start -d` in your project directory before deploying locally. The local network auto-starts with system canisters and seeds accounts with ICP and cycles.

9. **Not specifying build commands for asset canisters.** dfx automatically runs `npm run build` for asset canisters. icp-cli requires explicit build commands in the recipe configuration:
    ```yaml
    canisters:
      - name: frontend
        recipe:
          type: "@dfinity/asset-canister@v2.1.0"
          configuration:
            dir: dist
            build:
              - npm install
              - npm run build
    ```

10. **Expecting `output_env_file` or `.env` with canister IDs.** dfx writes canister IDs to a `.env` file (`CANISTER_ID_BACKEND=...`) via `output_env_file`. icp-cli does not generate `.env` files. Instead, it injects canister IDs as environment variables (`PUBLIC_CANISTER_ID:<name>`) directly into canisters during `icp deploy`. Frontends read these from the `ic_env` cookie set by the asset canister. Remove `output_env_file` from your config and any code that reads `CANISTER_ID_*` from `.env` — use the `ic_env` cookie instead (see Canister Environment Variables below).

11. **Expecting `dfx generate` for TypeScript bindings.** icp-cli does not have a `dfx generate` equivalent. Use `@icp-sdk/bindgen` (a Vite plugin) to generate TypeScript bindings from `.did` files at build time. The `.did` file must exist on disk — either commit it to the repo, or generate it with `icp build` first (recipes auto-generate it when `candid` is not specified). See `references/binding-generation.md` for setup details.

12. **Misunderstanding Candid file generation with recipes.** When using the Rust or Motoko recipe:
    - If `candid` is **specified**: the file must already exist (checked in or manually created). The recipe uses it as-is and does **not** generate one.
    - If `candid` is **omitted**: the recipe auto-generates the `.did` file from the compiled WASM (via `candid-extractor` for Rust, `moc` for Motoko). The generated file is placed in the build cache, not at a predictable project path.

    For projects that need a `.did` file on disk (e.g., for `@icp-sdk/bindgen`), the recommended pattern is: generate the `.did` file once, commit it, and specify `candid` in the recipe config. To generate it manually:

    **Rust** — build the WASM first, then extract the Candid interface:
    ```bash
    cargo install candid-extractor  # one-time setup
    icp build backend
    candid-extractor target/wasm32-unknown-unknown/release/backend.wasm > backend/backend.did
    ```

    **Motoko** — use `moc` directly with the `--idl` flag:
    ```bash
    $(mops toolchain bin moc) --idl $(mops sources) -o backend/backend.did backend/app.mo
    ```

## How It Works

### Project Creation

`icp new` scaffolds projects from templates. Without flags, an interactive prompt launches. For scripted or non-interactive use, pass `--subfolder` and `--define` flags directly. Available templates and options: [dfinity/icp-cli-templates](https://github.com/dfinity/icp-cli-templates).

### Build → Deploy → Sync

```text
Source Code → [Build] → WASM → [Deploy] → Running Canister → [Sync] → Configured State
```

`icp deploy` runs all three phases in sequence:
1. **Build** — Compile canisters to WASM (via recipes or explicit build steps)
2. **Deploy** — Create canisters (if new), apply settings, install WASM
3. **Sync** — Post-deployment operations (e.g., upload assets to asset canisters)

Run phases separately for more control:
```bash
icp build                     # Build only
icp deploy                    # Full pipeline (build + deploy + sync)
icp sync my-canister          # Sync only (e.g., re-upload assets)
```

### Environments and Networks

Two implicit environments are always available:

| Environment | Network | Purpose |
|-------------|---------|---------|
| `local` | `local` (managed, localhost:8000) | Local development |
| `ic` | `ic` (connected, https://icp-api.io) | Mainnet production |

The `ic` network is protected and cannot be overridden.

Custom environments enable multiple deployment targets on the same network:

```yaml
environments:
  - name: staging
    network: ic
    canisters: [frontend, backend]
    settings:
      backend:
        compute_allocation: 5

  - name: production
    network: ic
    canisters: [frontend, backend]
    settings:
      backend:
        compute_allocation: 20
        freezing_threshold: 7776000
```

### Install Modes

```bash
icp deploy                    # Auto: install new, upgrade existing (default)
icp deploy --mode upgrade     # Preserve state, run upgrade hooks
icp deploy --mode reinstall   # Clear all state (dangerous)
```

## Configuration

### Rust canister

```yaml
canisters:
  - name: backend
    recipe:
      type: "@dfinity/rust@v3.2.0"
      configuration:
        package: backend
        candid: backend.did  # optional — if specified, file must exist (auto-generated when omitted)
```

### Motoko canister

```yaml
canisters:
  - name: backend
    recipe:
      type: "@dfinity/motoko@v4.1.0"
      configuration:
        main: src/backend/main.mo
        candid: backend.did  # optional — if specified, file must exist (auto-generated when omitted)
```

### Asset canister (frontend)

```yaml
canisters:
  - name: frontend
    recipe:
      type: "@dfinity/asset-canister@v2.1.0"
      configuration:
        dir: dist
        build:
          - npm install
          - npm run build
```

For multi-canister projects, list all canisters in the same `canisters` array. icp-cli builds them in parallel. There is no `dependencies` field — use Canister Environment Variables for inter-canister communication.

### Custom build steps (no recipe)

When not using a recipe, only `name`, `build`, `sync`, `settings`, and `init_args` are valid canister-level fields. There are no `wasm`, `candid`, or `metadata` fields — handle these in the build script instead:

- **WASM output**: copy the final WASM to `$ICP_WASM_OUTPUT_PATH`
- **Candid metadata**: use `ic-wasm` to embed `candid:service` metadata
- **Candid file**: the `.did` file is referenced only in the `ic-wasm` command, not as a YAML field

```yaml
canisters:
  - name: backend
    build:
      steps:
        - type: script
          commands:
            - cargo build --target wasm32-unknown-unknown --release
            - cp target/wasm32-unknown-unknown/release/backend.wasm "$ICP_WASM_OUTPUT_PATH"
            - ic-wasm "$ICP_WASM_OUTPUT_PATH" -o "$ICP_WASM_OUTPUT_PATH" metadata candid:service -f backend/backend.did -v public --keep-name-section
```

### Available recipes

| Recipe | Purpose |
|--------|---------|
| `@dfinity/rust` | Rust canisters with Cargo |
| `@dfinity/motoko` | Motoko canisters |
| `@dfinity/asset-canister` | Asset canisters for static files |
| `@dfinity/prebuilt` | Pre-compiled WASM files |

Use `icp project show` to see the effective configuration after recipe expansion.

### Canister Environment Variables

icp-cli automatically injects all canister IDs as environment variables during `icp deploy`. Variables are formatted as `PUBLIC_CANISTER_ID:<canister-name>` and injected into every canister in the environment.

**Frontend → Backend** (reading canister IDs in JavaScript):

Asset canisters expose injected variables through a cookie named `ic_env`, set on all HTML responses. Use `@icp-sdk/core` to read it:
```js
import { safeGetCanisterEnv } from "@icp-sdk/core/agent/canister-env";

const canisterEnv = safeGetCanisterEnv();
const backendId = canisterEnv?.["PUBLIC_CANISTER_ID:backend"];
```

**Backend → Backend** (reading canister IDs in canister code):
- Rust: `ic_cdk::api::env_var_value("PUBLIC_CANISTER_ID:other_canister")`
- Motoko (motoko-core v2.1.0+):
  ```motoko
  import Runtime "mo:core/Runtime";
  let otherId = Runtime.envVar("PUBLIC_CANISTER_ID:other_canister");
  ```

Note: variables are only updated for canisters being deployed. When adding a new canister, run `icp deploy` (without specifying a canister name) to update all canisters with the complete ID set.

## Additional References

For detailed guides on specific topics, consult these reference files when needed:

- **`references/binding-generation.md`** — TypeScript binding generation with `@icp-sdk/bindgen` (Vite plugin, CLI, actor setup)
- **`references/dev-server.md`** — Vite dev server configuration to simulate the `ic_env` cookie locally
- **`references/dfx-migration.md`** — Complete dfx → icp migration guide (command mapping, config mapping, identity/canister ID migration, frontend package migration, post-migration verification checklist)
