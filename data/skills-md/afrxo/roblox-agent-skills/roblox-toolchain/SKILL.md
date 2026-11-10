---
name: roblox-toolchain
description: >
  Filesystem-based Roblox development with Rojo + Wally + Luau LSP + StyLua + selene.
  Use when setting up, modifying, or debugging .project.json sync, package manifests,
  toolchain pinning, sourcemap regen, editor integration, CI builds, or any
  filesystem-to-DataModel question. Tooling layer only — language rules live in
  luau-expert; runtime behavior lives in roblox-dev; UI libraries live in roblox-ui.
---

# Roblox Rojo (Filesystem Workflow)

How to develop Roblox games with files on disk instead of inside Studio. Sources: [rojo.space](https://rojo.space) (official Rojo docs), [github.com/rojo-rbx/rojo](https://github.com/rojo-rbx/rojo) (Rojo source), [github.com/rojo-rbx/rokit](https://github.com/rojo-rbx/rokit) (Rokit toolchain manager — use this, not Aftman/Foreman), [github.com/UpliftGames/wally](https://github.com/UpliftGames/wally) (Wally package manager), [github.com/pesde-pkg/pesde](https://github.com/pesde-pkg/pesde) (Pesde — newer alternative package manager). Tooling: [stylua](https://github.com/JohnnyMorganz/StyLua), [selene](https://github.com/Kampfkarren/selene), [luau-lsp](https://github.com/JohnnyMorganz/luau-lsp).

For deep dives see:

- [`references/project-format.md`](references/project-format.md) — full `.project.json` schema
- [`references/sync-mapping.md`](references/sync-mapping.md) — every file extension Rojo recognizes and what it becomes
- [`references/wally-manifest.md`](references/wally-manifest.md) — full `wally.toml` + lockfile + command reference
- [`references/pesde-manifest.md`](references/pesde-manifest.md) — full `pesde.toml` schema, environments, Wally bridge
- [`references/luau-lsp-setup.md`](references/luau-lsp-setup.md) — sourcemap regen, LSP configuration

---

## Integration Policy

This skill describes preferred patterns; it does **not** authorize rewriting existing code. Apply rules to new code and to changes the user explicitly asks for. **Match the codebase's existing toolchain.** If the project uses Aftman, don't migrate to Rokit unprompted. If it uses Wally, don't suggest Pesde. If `default.project.json` follows a particular structure, extend it — don't rewrite it. Surface conflicts once and default to the existing setup.

Full rules: [`../../shared/integration-policy.md`](../../shared/integration-policy.md).

---

## Principles

- **One source of truth: the filesystem.** The repo is canonical; Studio is the build target.
- **Toolchain is pinned per project.** `rokit.toml` lists exact versions of `rojo`, `wally` (or `pesde`), `stylua`, `selene`, `luau-lsp`. Reproducible builds beat "works on my machine".
- **Sourcemap is rebuilt, not committed.** It's generated output. Regenerate on dependency change.
- **Build and lint in CI.** A green `main` means `rojo build` produces a valid `.rbxl` and lints pass.
- **`Packages/` is generated.** Wally writes it; you don't hand-edit it; it's `.gitignore`'d.

---

## Rojo Basics

### Install

Use **Rokit** (toolchain manager, successor to Foreman/Aftman) to pin versions per project:

```toml
# rokit.toml — drop-in compatible with foreman.toml / aftman.toml format
[tools]
rojo = "rojo-rbx/rojo@7.5.1"
wally = "UpliftGames/wally@0.3.2"
stylua = "JohnnyMorganz/StyLua@2.0.0"
selene = "Kampfkarren/selene@0.27.1"
```

Then `rokit install` in the project root pulls those exact versions. Don't rely on globally-installed tools — versions drift between machines.

**Why Rokit, not Aftman:** Aftman is unmaintained (third-party author no longer working in Roblox); Foreman is maintained by Roblox but oriented toward internal use. Rokit is community-maintained, drop-in compatible with both manifest formats, and substantially faster to install. Migrate by renaming `aftman.toml` → `rokit.toml`.

Common Rokit commands: `rokit init`, `rokit add OWNER/REPO`, `rokit install`, `rokit update`, `rokit list`, `rokit self-update`.

### Two modes

```bash
# Live sync — Studio plugin connects to this server, applies changes as you save.
rojo serve [path/to/project.json]

# One-shot build — produces a .rbxl (place) or .rbxm (model).
rojo build [path/to/project.json] --output build/place.rbxl
```

`rojo serve` is for development. `rojo build` is for CI and final publish. The Studio plugin (install via Studio's plugin tab, version-matched to the CLI) is what actually applies live changes.

### Project file location

Rojo looks for `default.project.json` in the current directory. Pass an explicit path to use any other `.project.json` file. A repo with multiple builds (game, plugin, library) typically has one project per target.

---

## `default.project.json` Structure

```json
{
  "name": "MyGame",
  "tree": {
    "$className": "DataModel",

    "ReplicatedStorage": {
      "$className": "ReplicatedStorage",
      "$path": "src/ReplicatedStorage"
    },

    "ServerScriptService": {
      "$className": "ServerScriptService",
      "$path": "src/ServerScriptService"
    },

    "StarterPlayer": {
      "$className": "StarterPlayer",
      "StarterPlayerScripts": {
        "$className": "StarterPlayerScripts",
        "$path": "src/StarterPlayerScripts"
      }
    },

    "Workspace": {
      "$className": "Workspace",
      "$properties": {
        "Gravity": 196.2
      }
    }
  }
}
```

- `name` (required) — used as the build artifact name.
- `tree` (required) — root Instance description.
- Inside `tree`:
  - `$className` — Instance class. Optional if `$path` resolves it or if the key is a service name.
  - `$path` — folder/file on disk to mount under this Instance.
  - `$properties` — properties to set (e.g. `Gravity`, `HttpEnabled`).
  - `$ignoreUnknownInstances` — if `true`, Rojo leaves Instances it didn't sync alone instead of deleting them.
  - Any other key = a child Instance description.

Other top-level fields: `servePort` (default `34872`), `servePlaceIds` (allowlist of place IDs to prevent accidentally syncing into the wrong game), `placeId`, `gameId`, `serveAddress`, `globIgnorePaths`, `emitLegacyScripts`.

**`emitLegacyScripts`** controls whether `*.server.luau`/`*.client.luau` produce legacy `Script`/`LocalScript` Instances or `Script` Instances with `RunContext` set. Documented default is `true`; verify against your installed Rojo version (`rojo --version` + release notes) before assuming. New projects should set `false` to use modern `RunContext` — see `roblox-dev` script-types section.

Full schema: [`references/project-format.md`](references/project-format.md).

---

## Filesystem → DataModel Mapping

This is the rule set you'll consult constantly. Memorize the common ones.

| Path on disk | Becomes |
|---|---|
| `dir/` (any directory) | `Folder` |
| `foo.luau` | `ModuleScript` named `foo` (Rojo also accepts legacy `.lua`) |
| `foo.server.luau` | `Script` named `foo` (server) |
| `foo.client.luau` | `LocalScript` named `foo` (client) |
| `dir/init.luau` | `ModuleScript` named `dir` (the directory becomes the script) |
| `dir/init.server.luau` | `Script` named `dir` (directory becomes server script) |
| `dir/init.client.luau` | `LocalScript` named `dir` (directory becomes local script) |
| `foo.rbxm` / `foo.rbxmx` | Model from binary/XML |
| `foo.csv` | `LocalizationTable` |
| `foo.txt` | `StringValue` |
| `foo.json` (not `.model.json` / `.project.json`) | `ModuleScript` returning the table |
| `foo.toml` | `ModuleScript` returning the table |
| `foo.model.json` | JSON-described model (hand-written, useful for `RemoteEvent` etc.) |
| `foo.project.json` | Nested project (composes into parent) |
| `foo.meta.json` | Metadata sidecar attached to the matching file/dir |

### `init.luau` semantics

A directory + `init.luau` becomes one `ModuleScript`, where the directory's other children become children of that script. Lets a script have submodules without a separate folder.

```
src/Inventory/
├── init.luau          # ModuleScript "Inventory"
├── add.luau           #   ModuleScript "add" (child of Inventory)
├── remove.luau        #   ModuleScript "remove"
└── types.luau         #   ModuleScript "types"
```

Only **one** `init.*` file per directory (`init.luau` xor `init.server.luau` xor `init.client.luau`).

### Meta files

`foo.meta.json` attaches Rojo-specific metadata to `foo.*`. Common uses:

```json
// init.meta.json — turn the parent folder into a Tool with a Grip
{
  "className": "Tool",
  "properties": {
    "Grip": [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
  }
}
```

```json
// foo.meta.json — disable a script
{
  "properties": { "Disabled": true }
}
```

```json
// hello.meta.json — let Rojo leave Instances under hello.txt alone
{
  "ignoreUnknownInstances": true
}
```

`className` works only in `init.meta.json`. `properties` works on any non-model file.

Full mapping table: [`references/sync-mapping.md`](references/sync-mapping.md).

---

## Recommended Project Layout

```
my-game/
├── rokit.toml                # toolchain pinning
├── default.project.json       # Rojo project file
├── wally.toml                 # package manifest
├── wally.lock                 # lockfile (committed)
├── stylua.toml                # formatter config
├── selene.toml                # linter config
├── sourcemap.json             # generated; .gitignore'd
├── Packages/                  # wally output; .gitignore'd
├── ServerPackages/            # wally output; .gitignore'd
├── DevPackages/               # wally output; .gitignore'd
├── .github/workflows/ci.yml   # CI
├── (editor config)            # .vscode/settings.json, .nvim, etc. — editor-specific
├── .gitignore
├── README.md
└── src/
    ├── ReplicatedStorage/
    │   ├── Shared/
    │   │   ├── init.luau
    │   │   └── ...
    │   └── Client/             # (optional) client-only scripts via RunContext
    ├── ServerScriptService/
    │   ├── init.server.luau
    │   └── Systems/
    └── StarterPlayer/
        └── StarterPlayerScripts/
            └── init.client.luau
```

Match `src/` directory names to their DataModel mount points. Reading the path tells you exactly where the code runs.

---

## Wally (Packages)

**Install via Rokit** (don't pull from a global). Add to `rokit.toml`:

```toml
[tools]
wally = "UpliftGames/wally@0.3.2"
```

Then `rokit install`. Commands:

```bash
wally init               # scaffold wally.toml
wally install            # download deps into Packages/
wally install --locked   # CI; fail if lockfile is stale
wally update [name...]   # bump deps
wally publish            # push your package to the registry
wally search <query>     # find packages
```

### `wally.toml`

```toml
[package]
name = "yourname/coolpkg"        # SCOPE/NAME, lowercase, dashes ok
version = "1.0.0"                # SemVer
license = "MIT"                  # SPDX
authors = ["Your Name <you@example.com>"]
realm = "shared"                 # "shared" or "server"
registry = "https://github.com/UpliftGames/wally-index"

[dependencies]
React = "jsdotlua/react@17.1.0"
Promise = "evaera/roblox-lua-promise@4.0.0"

[server-dependencies]
ProfileService = "loleris/profileservice@1.4.0"

[dev-dependencies]
Jest = "jsdotlua/jest@3.10.0"
```

### Realms

- **`shared`** — replicates to clients. Mount under `ReplicatedStorage`.
- **`server`** — server-only. Mount under `ServerStorage` or `ServerScriptService`.
- No `client` realm exists. Client-only deps live in `shared` and run on the client by import.

### Mounting Wally output in Rojo

```json
"ReplicatedStorage": {
  "$className": "ReplicatedStorage",
  "Packages": {
    "$path": "Packages"
  }
},
"ServerScriptService": {
  "$className": "ServerScriptService",
  "Packages": {
    "$path": "ServerPackages"
  }
}
```

Packages get installed into separate folders by realm. Shared → `Packages/`, server → `ServerPackages/`, dev → `DevPackages/`.

### Lockfile

`wally.lock` pins exact versions of every dep (transitive included). **Commit it.** `wally install --locked` in CI ensures everyone builds the same thing.

Full manifest fields, lockfile format, command list: [`references/wally-manifest.md`](references/wally-manifest.md).

---

## Pesde (Alternative Package Manager)

[**Pesde**](https://github.com/pesde-pkg/pesde) is a newer Luau-first package manager — designed to prevent runtime lock-in. It targets multiple Luau runtimes (`luau`, `lune`, `roblox`, `roblox_server`) from one tool, and can pull from existing **Wally** registries via a bridge. Worth using when:

- You want one package manager across pure-Luau, Lune, and Roblox projects.
- You need Wally packages **and** native pesde packages in the same project.
- You prefer npm/pnpm-style ergonomics over Wally's Cargo-style.

### `pesde.toml`

```toml
name = "yourname/coolpkg"
version = "1.0.0"
license = "MIT"

[target]
environment = "roblox"     # luau | lune | roblox | roblox_server
lib = "src/init.luau"

[indices]
default = "https://github.com/pesde-pkg/index"

[wally_indices]
default = "https://github.com/UpliftGames/wally-index"

[dependencies]
# Native pesde dep
hello = { name = "pesde/hello", version = "^1.0.0" }
# Wally dep via the bridge
React = { wally = "jsdotlua/react", version = "^17.1.0" }

[dev_dependencies]
Jest = { wally = "jsdotlua/jest", version = "^3.10.0" }
```

### Commands

```bash
pesde init        # scaffold pesde.toml
pesde add SCOPE/NAME   # add + install a dep
pesde install     # install all deps; writes pesde.lock
pesde run         # run [scripts] entries (uses Lune)
pesde publish
```

### Layout

- Native pesde deps install into a target-named folder (`roblox_packages/`, `luau_packages/`, etc.).
- Wally bridge deps still resolve through the wally-index repo.
- `pesde.lock` is the lockfile — commit it.
- For Roblox projects, pesde generates a Rojo-compatible sourcemap via a script package; pair with `rojo sourcemap`.

### When to pick which

| Need | Choice |
|---|---|
| Mature, Roblox-only, large existing ecosystem | Wally |
| Multi-runtime (Lune CLI tools, Roblox, plain Luau) | Pesde |
| Cargo-style ergonomics | Wally |
| npm/pnpm-style ergonomics + Wally bridge | Pesde |
| Existing project on Wally with no pain | Stay |

Wally and Pesde aren't drop-in equivalents — manifest formats and resolution semantics differ. Don't switch mid-project without reason.

---

## Sourcemap (Luau LSP)

Luau LSP needs to know where files map to in the DataModel for proper autocomplete and `require()` resolution. Rojo generates the map.

```bash
# Watch mode — regenerates on filesystem change
rojo sourcemap --watch --output sourcemap.json default.project.json

# One-shot
rojo sourcemap --output sourcemap.json default.project.json
```

Then point `luau-lsp` at it. Editor-specific:

- **VS Code (`luau-lsp` extension):** `"luau-lsp.sourcemap.sourcemapFile": "sourcemap.json"` in `.vscode/settings.json` (or workspace-level config).
- **Neovim / Helix / Sublime:** pass the sourcemap path as an LSP startup arg (`--definitions=...` / `--sourcemap=...`) or via your LSP client's settings; the `luau-lsp` binary documents the flags.
- **CLI mode:** `luau-lsp analyze --sourcemap sourcemap.json ...`. Verify the exact flag against your installed `luau-lsp --help`.

Regenerate after:

- Adding/removing files in the project.
- Running `wally install` (new package paths).
- Changing `default.project.json` mounts.

A common workflow: run `rojo sourcemap --watch` in a terminal alongside `rojo serve`. Both run for the duration of your session.

`sourcemap.json` is generated output — `.gitignore` it.

LSP setup details: [`references/luau-lsp-setup.md`](references/luau-lsp-setup.md).

---

## Linting & Formatting

### StyLua (formatter)

```toml
# stylua.toml
column_width = 100
line_endings = "Unix"
indent_type = "Tabs"          # or "Spaces" with indent_width = 4
quote_style = "AutoPreferDouble"
call_parentheses = "Always"

[sort_requires]
enabled = true                # alphabetize the require block; pairs with luau-expert guidance
```

Run via `stylua src/`. Most editors auto-format on save once the StyLua extension is installed.

### selene (linter)

```toml
# selene.toml
std = "roblox"                # roblox stdlib definitions

# Optional: per-rule tweaks
[config]
incorrect_standard_library_use = "warn"
```

`std = "roblox"` is the key bit — without it, selene flags every `Instance.new` and `task.wait`. Run via `selene src/`.

### Luau LSP (type-checker)

`luau-lsp` powers in-editor type checking, hover info, autocomplete. Combine with `--!strict` per-file (see `luau-expert` skill) for max coverage.

Project-level config (`.luaurc`):

```json
{
  "languageMode": "strict",
  "lint": {
    "*": true
  }
}
```

Verify the schema against [luau.org/lint](https://luau.org/lint) — `.luaurc` fields evolve.

---

## CI

A minimum-viable CI run:

1. **Setup Rokit** (`rokit install`) to install pinned tool versions.
2. **`wally install --locked`** — fail if lockfile drift.
3. **`stylua --check src/`** — fail if formatting drift.
4. **`selene src/`** — lint.
5. **`rojo sourcemap --output sourcemap.json default.project.json`** — generate map.
6. **`luau-lsp analyze`** with the sourcemap — type-check. Exact flag depends on installed version (`--sourcemap` or `--definitions`); check `luau-lsp --help`.
7. **`rojo build default.project.json --output build/place.rbxl`** — build artifact.
8. **(Optional)** Upload `place.rbxl` as artifact / publish.

Each step short-circuits the next. A green CI run means: pinned tools, locked deps, formatted, lint-clean, type-clean, builds.

GitHub Actions example sketched in [`examples/ci.yml`](examples/ci.yml).

---

## Verification Rules

- **Don't quote `.project.json` field names from memory** beyond `name`, `tree`, `$className`, `$path`, `$properties`. The full schema is short — check [`references/project-format.md`](references/project-format.md) before committing to less-common fields.
- **Don't quote Wally version semantics from memory.** Wally follows Cargo-style SemVer with `^` default; specifics for `~`, `=`, `*` should be checked against [Wally docs](https://github.com/UpliftGames/wally) before recommending non-default version specifiers.
- **`emitLegacyScripts` default has shifted across releases.** Confirm what version of Rojo the project uses (`rojo --version`) before assuming the `Script` vs `Script(RunContext=Server)` distinction.
- **Editor configs differ.** This skill covers the Luau LSP layer — `.vscode/settings.json` examples in references are illustrative; users on Neovim/Helix/Sublime configure equivalent fields.
- **Don't conflate Rojo with the engine.** `RunContext` placement / replication / DataModel semantics belong to `roblox-dev`. This skill stops at "the file ends up at this DataModel path".

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Globally-installed `rojo` / `wally` / `stylua` | Pin per-project via `rokit.toml` |
| New projects on Aftman or Foreman | Rokit (drop-in successor; community-maintained, faster) |
| Hand-edit `Packages/` | Treat as generated; `wally install` regenerates |
| Commit `Packages/` / `ServerPackages/` / `DevPackages/` | `.gitignore` them |
| Commit `sourcemap.json` | `.gitignore`; regenerate on demand |
| Forget `wally.lock` in git | Commit it; CI uses `--locked` |
| Multiple `init.*` in one folder | One init script per dir; use submodules instead |
| `init.client.luau` placed in `ServerScriptService` mount | Match script type to container |
| `selene` without `std = "roblox"` | Always set; otherwise every Roblox API trips lint |
| Edit Studio + filesystem simultaneously | Filesystem is canonical; close Studio when not running `rojo serve` |
| `rojo build` producing a place file checked in | CI artifact only; binary place files don't diff |
| Mounting `Packages` only under `ReplicatedStorage` and using server deps | Mount `ServerPackages` separately under server containers |
| Bare `*.luau` in a `StarterPlayerScripts` mount expecting client behavior | `*.client.luau` (legacy) or `Script` with `RunContext=Client` |
| Manually rerun `rojo sourcemap` after every save | Use `--watch` in a long-running terminal |
| `wally publish` from a dirty working tree | Tag a clean commit; publish from CI |
| `luau-lsp` without sourcemap | Generate sourcemap; LSP requires it for require() resolution |

---

## Examples

- [`examples/default.project.json`](examples/default.project.json) — typical place project covering all standard mounts.
- [`examples/wally.toml`](examples/wally.toml) — annotated Wally manifest with `[dependencies]`, `[server-dependencies]`, `[dev-dependencies]`.
- [`examples/pesde.toml`](examples/pesde.toml) — annotated Pesde manifest with `[target]`, `[indices]`, `[wally_indices]`, `[dependencies]`.
- [`examples/rokit.toml`](examples/rokit.toml) — toolchain pinning.
- [`examples/file-tree.md`](examples/file-tree.md) — full repo layout showing how filesystem maps to DataModel.
- [`examples/ci.yml`](examples/ci.yml) — GitHub Actions workflow: install Rokit → wally install --locked → stylua check → selene → rojo build.
