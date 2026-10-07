---
name: roblox-tooling
description: Professional Roblox toolchain - Studio Script Sync vs Rojo, Rokit, Wally/pesde packages, luau-lsp with sourcemaps, StyLua, selene, darklua, Lune, roblox-ts, .luaurc, git, GitHub Actions CI and Open Cloud publishing. Use when creating a Roblox repo, configuring VS Code/Cursor, adding packages, fixing sourcemap/require typing, or automating builds and deploys.
---

# Roblox tooling

## Pick a sync model

| Need | Use |
| --- | --- |
| Edit scripts in an external editor / git for code only; keep Studio as source of truth; Team Create | **Studio Script Sync** (built in: right-click a folder → **Sync to…**) |
| Whole project as files, file system is the source of truth, CI builds, packages | **Rojo** (`rojo serve` + Studio plugin) |

Script Sync syncs only `Script`/`LocalScript`/`ModuleScript`/`Folder` (≤ 10,000 scripts per synced
root, ≤ 128 roots); don't sync scripts that carry attributes/tags (they're not written to disk).
Pair either with the **Luau Language Server** VS Code extension + its **Luau Language Server Companion**
Studio plugin (sends the DataModel tree so requires and instance paths type-check).

## Rokit: pinned toolchain

```toml
# rokit.toml (commit it; run `rokit install`)
[tools]
rojo = "rojo-rbx/rojo@7.7.0"
wally = "UpliftGames/wally@0.3.2"
lune = "lune-org/lune@0.10.5"
stylua = "JohnnyMorganz/StyLua@2.5.2"
selene = "Kampfkarren/selene@0.31.0"
luau-lsp = "JohnnyMorganz/luau-lsp@1.70.1"
darklua = "seaofvoices/darklua@0.19.0"
```

Install Rokit: `curl -sSf https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.sh | bash`
(Windows: `install.ps1`). Add tools with `rokit add owner/repo`. Versions above are current as of
September 2026; bump deliberately. (Aftman and Foreman are older equivalents.)

## Rojo project

```json
{
  "name": "my-game",
  "tree": {
    "$className": "DataModel",
    "ReplicatedStorage": {
      "Shared": { "$path": "src/shared" },
      "Packages": { "$path": "Packages" }
    },
    "ServerScriptService": {
      "Server": { "$path": "src/server" },
      "ServerPackages": { "$path": "ServerPackages" }
    },
    "StarterPlayer": {
      "StarterPlayerScripts": {
        "Client": { "$path": "src/client" }
      }
    },
    "Workspace": {
      "$properties": { "StreamingEnabled": true }
    }
  }
}
```

File mapping: `Foo.luau` → ModuleScript, `Foo.server.luau` → Script, `Foo.client.luau` → LocalScript,
folder with `init.luau`/`init.server.luau`/`init.client.luau` → that script with children,
`*.meta.json` → properties/attributes, `*.model.json`/`.rbxm`/`.rbxmx` → instances, `*.json`/`*.toml`/`*.txt`
→ ModuleScript returning data / StringValue. Commands: `rojo serve`, `rojo build -o game.rbxl`,
`rojo sourcemap default.project.json -o sourcemap.json` (for luau-lsp), `rojo upload` / Open Cloud for
publishing. Keep maps/art in Studio (or `.rbxm` files) and code in Rojo — partially managed trees are fine.

## Packages

- **Wally** (`wally.toml`, `wally install` → `Packages/`, `ServerPackages/` for `realm = "server"`):
  ```toml
  [dependencies]
  React = "jsdotlua/react@17.2.1"
  ReactRoblox = "jsdotlua/react-roblox@17.2.1"
  [server-dependencies]
  ProfileStore = "lm-loleris/profilestore@1.0.3"
  ```
  Wally thunks lose types: run `wally-package-types --sourcemap sourcemap.json Packages/` after install.
  Check each package's page on wally.run for its exact name/version.
- **pesde** (`pesde.toml`): newer manager for Roblox/Lune/Luau that can also depend on Wally packages.
- Commit `wally.lock`/`pesde.lock`; don't commit `Packages/`.

## Code quality

- **luau-lsp** (editor + CLI) — type checking against Roblox definitions. CLI:
  `luau-lsp analyze --definitions=@roblox=globalTypes.d.luau --sourcemap=sourcemap.json --base-luaurc=.luaurc src/`
  (definitions: `https://raw.githubusercontent.com/JohnnyMorganz/luau-lsp/main/scripts/globalTypes.d.luau`).
  Enable the new solver in the editor (`luau-lsp.fflags.enableNewSolver`) to match Studio.
- **StyLua** — formatter. `stylua.toml`: `indent_type = "Tabs"`, `column_width = 120`. `stylua --check src`.
- **selene** — linter. `selene.toml`: `std = "roblox"` (generate/refresh with `selene generate-roblox-std`).
- **darklua** — code transforms (e.g. convert string requires, bundle) for publishing pipelines.
- `.luaurc` — per-directory type-check mode and require aliases:
  ```json
  { "languageMode": "strict", "aliases": { "Shared": "src/shared", "Packages": "Packages" } }
  ```
  Roblox resolves string requires relative to the DataModel (`./`, `../`, `@self`, `@game`); custom
  `.luaurc` aliases need tooling (luau-lsp/darklua) that understands your mapping.

## Lune

Standalone Luau runtime for scripts outside Roblox: build steps, place file manipulation
(`@lune/roblox` reads/writes `.rbxl`/`.rbxm`), asset pipelines, running pure-Luau unit tests, calling
Open Cloud with `@lune/net`. `lune run scripts/build`.

## roblox-ts

If the repo has `tsconfig.json`, `package.json` with `roblox-ts` and `@rbxts/types`, write TypeScript:
`npx rbxtsc -w` compiles `src/*.ts` to `out/*.luau`, and Rojo syncs `out/`. Use `@rbxts/services`,
`@rbxts/*` packages from npm. Don't hand-edit generated Luau.

## Git and CI

`.gitignore`: `*.rbxl.lock`, `*.rbxlx.lock`, `Packages/`, `ServerPackages/`, `sourcemap.json`, build outputs.
A ready-to-use GitHub Actions workflow (install tools, format check, lint, type-check, build, publish via
Open Cloud): [references/ci-workflow.md](references/ci-workflow.md).

## Related skills

`roblox-testing` (running tests in CI), `roblox-open-cloud` (publishing, Luau execution),
`roblox-studio-mcp` (driving Studio from an agent), `roblox-luau`.
