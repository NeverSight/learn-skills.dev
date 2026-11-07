---
name: craft-anything
description: >-
  Craft Anything is ArtCraft's open-source, pure-Rust reverse-engineering and rebuilding workbench:
  point it at a website, desktop app, phone app, game or file, and it studies the original with real
  inspection tools (disassembler, decompiler, archives, browsers, databases, packet captures),
  has a coding agent (Claude Code first) build a new project in the stack you name, compares the
  result against the original at three screen widths or via the built program's own self-test, and
  refines until it matches. Trigger this skill whenever the user mentions Craft Anything (or
  `craft-anything-cli`, `craft.json`, `.cany`, "rebuild this website/app/game", "how does X work
  under the hood"), asks to inspect or reverse-engineer software they own, wants an agent-driven
  study→build→check pipeline, asks about its 298-tool engine, its MCP server, Clean room vs Deep
  mode, or its project folder layout — and equally when they never name it but describe the job
  ("figure out how this site is built", "make me a clone of this app", "disassemble this binary and
  tell me what it does"). Do not assume Ida-Pro-style or Ghidra-style behaviour: read this first.
---

# Craft Anything

**Audit basis:** this checkout is tag `v0.2.0`, commit `b09b99aaa7985ebbc3d0fef467c4b688d4727cc1` ("Release 0.2.0", 2026-11-01; shallow clone of the release tag). The installed `/Applications/Craft Anything.app` reports `CFBundleShortVersionString` 0.2.0 (bundle id `ai.storyteller.craft-anything`) and its binary prints `craft-anything 0.2.0`, so the bundle matches this source; the GUI was never launched. Every number below was measured from this tree, not copied from the README (the README's "284 tools" predates the generated tool list; see the counts section).

v0.1.0 → v0.2.0: the **engine tool surface is unchanged** (298 tools / 17 toolsets, `docs/tools.md` byte-identical). The wave is in the **agent/AI layer**: an **OpenCode adapter** (`crates/ai/src/cli_agents/adapters/opencode.rs` — invokes `opencode run`, without `run` OpenCode reads its first argument as a folder to open), npm-installed coding agents start on Windows, local model servers (LM Studio et al.) accept the tools because boolean sub-schemas are sent as objects, failed agent runs are explained with a keepable log (`failure_log.rs`), the build activity feed shows what the build is doing now and how long it has been quiet (`rebuild/activity.rs`), **"Try again" resumes where a build stopped** (`crates/engine/src/journal.rs`), deadlocks are stopped as they form with a lock watchdog, crashing programs are named by their error instead of the last stack line, CJK scripts render in release builds (fonts and licences ship), a builder writing `/app/…` paths builds the app instead of being refused, `doctor` calls a local AI server reachable only when it answers with its models (and no longer offers another program squatting on the model-server port), agent checks that only probed the version say so, and the coding agent's cost is labelled an estimate. Claude Code remains the first-class, verified builder; Codex and OpenCode adapters exist but are unverified.

## Overview

Craft Anything is "See how any website, app or game works, then have AI build your own version" — an open-source, clean-room engine in pure Rust by the ArtCraft/storytold project (`README.md`, MIT OR Apache-2.0). It works in four steps — **Study → Build → Check → Ready** — asking the person question/approval cards when a decision is theirs (`README.md` "How it works"). Two UI modes drive the same engine: **Simple** (a project page with the four steps) and the **Advanced** workbench (functions, pseudo-C, disassembly, hex, call graphs, evidence ledger, agent console). **Clean room** (default) inspects only what a visitor can see — screenshots, visible text, measured layout, colours, fonts — and refuses look-inside tools; **Deep** reads code and files with the built-in engines and Ghidra when installed (`README.md` "Clean room or Deep"; `crates/engine/src/tools/deep.rs`). Building needs a coding agent signed in on your machine — **Claude Code** is supported first (your own unmodified `claude`, your own sign-in); a Codex adapter exists but is unverified (README "AI"; `docs/claude-code.md`). **Status: early alpha** — website rebuilds with three-width checks and game rebuilds in Unity/Unreal/Godot work today; app/game behaviour checks are partial; some engine tools are tested only against stand-ins (`README.md` Status; `docs/STATUS.md`; `docs/tool-status.md`). Source: GitHub `storytold/craft-anything`.

## Capabilities (verified)

### One tool registry, three surfaces

- **298 engine tools in 17 toolsets** at this tag, generated into `docs/tools.md` by `cargo xtask tools` and kept honest by a test floor (`MIN_TOOLS = 271`, `crates/engine/src/tool_list.rs:9`). Each tool is simultaneously an **MCP tool**, a **CLI command** (`craft-anything-cli <id with dashes>`) and a callable tool for the coding agent; the AI and setup layers add more on top (`rebuild_*`, `assets_key_*`, `setup_*`). Toolsets: `core` 34, `native` 55, `apple` 14, `formats` 36, `managed` (.NET) 8, `android` 14, `java` 6, `adb` 24, `browser` 22, `javascript` 11, `runtime` 14, `frida` 9, `application` 17, `database` 1, `projects` 18, `setup` 9, `build` 6 (`docs/tools.md`). The README's "284 tools (271 in the engine)" is stale — trust the generated list and `craft-anything-cli commands`.
- **Results are evidence, not answers**: every result carries confidence, coverage and limitations; big ones come back as a summary and page with `core_evidence_browse`. The discipline rules (predict-then-check, cite evidence ids, absence is not proof) are appended to every guided prompt (`crates/mcp/src/prompts.rs` `DISCIPLINE`).
- **MCP server** (`craft-anything-cli mcp`): stdio JSON-RPC; tools default to Essentials plus enabled toolsets, `--all-tools` lists everything; `--inbox DIR` posts `core_person_ask`/`core_action_approve` cards for the desktop app to answer (`apps/craft-anything-cli/src/main.rs` `Mcp`). **6 guided prompts** (`crates/mcp/src/prompts.rs` `PROMPTS`).
- **CLI subcommands** (`apps/craft-anything-cli/src/main.rs` `Command`): `mcp`, `setup`, `doctor`, `uninstall`, `commands`, `capabilities`, `triage <path>`, `report [--html] [--out] [--no-evidence]`, `chat`, `rebuild`, `ai`, a hidden `builder-notes` hook, and **`Tool(Vec<String>)` pass-through** so every engine tool id is a subcommand. Unknown flags are refused.
- **Rebuild from the terminal** (questions asked in the terminal): `craft-anything-cli rebuild <target|"-" for none> "<request>"` with `--rounds N` (default 2), `--backend`, `--unattended`, `--projects-dir`, `--project-folder` + `--existing edit|start-from`, `--continue-in` + `--resume`, `--deep` / `--clean-room` (`apps/craft-anything-cli/src/rebuild_cmd.rs`).

### Study (the inspection engine)

- Its own pure-Rust **decoders, disassembler and decompiler** work without outside programs; Deep mode additionally uses **Ghidra** when installed (`README.md` "Under the hood"). Native programs (ELF/Mach-O/PE), .NET (incl. IL2CPP, bundles), Java (with decompilation), Android (adb, APK/AXML/ARSC signing), Apple (runtime, codesign, CAR), Electron (asar, fuse, runtime), JavaScript/JS bundles, websites (CDP browser automation), firmware, packet captures, databases, game archives — one toolset each (`crates/engine/src/tools/`, `crates/formats/src/`).
- External engines are optional and detected: Ghidra, Cutter, rizin, GDB, Frida, adb, jadx, CDP browsers (`crates/engines/src/`); `craft-anything-cli doctor` checks the install, registrations, engines, AI backends and the MCP server.
- "Just look inside" opens a target for questions without building anything (Deep mode).

### Build, check, refine

- The builder is **your own Claude Code** (first-class; Codex adapter built but unverified). Craft Anything never sees your account; generated pictures and 3D models are opt-in with your own fal.ai key (`README.md` "AI").
- **Checks**: websites are compared at three screen widths; games run the generated program's own `--self-test` against `checks/round-N/self-test.json`; app runs are compared; each round writes into `checks/` and the agent refines what doesn't match (`README.md` Status; `crates/engine/src/self_test.rs`; `docs/file-formats.md`).
- **Plugins**: MCP servers, and WASM components in builds with the `wasm-plugins` option (`crates/engine/src/plugins.rs`; `crates/engines/src/wasm_plugin.rs`).

### Project folder and file formats (all versioned, migration steps on open)

- New projects go to `Documents/Craft Anything` (Settings → General) unless `--project-folder`. Layout: `craft.json` (request, target, status, history), `capture/`, `app/` (the generated project), `checks/`, `investigation.cany/` (evidence ledger), `inbox/` (open questions) (`README.md` "Get started").
- Version constants in code: `craft.json` `MANIFEST_VERSION` **2** (`crates/engine/src/workspace.rs`), `config.toml` `SETTINGS_VERSION` **3** (`crates/engine/src/settings.rs`), `investigation.cany/project.toml` `FORMAT_VERSION` **1** (`crates/engine/src/project.rs`) — each with a compile-time assertion that the migration-step list has one step per version. Newer files: `craft.json` = read-only, saving refused; `project.toml` = refused with "update Craft Anything"; plus versioned `transcript.json`, `usage.json`, `questions.json`, `pinned/<n>/pin.json`, `feed.json`, `mechanics.json` and `standin.json`. **A newer file is never downgraded or overwritten.** ⚠️ **Repo-doc drift:** `docs/file-formats.md`'s table still says manifest 1 / settings 2 — it lags the constants (measured in code at v0.1.0 and v0.2.0 alike); trust the constants.

## Known limitations and not-implemented

Do not assign these at v0.2.0:

- **Building with API keys and other coding agents is built but not yet run live**; only Claude Code is verified (`README.md` Status).
- **Behaviour checks for apps and games are partial**; website checks are the mature path.
- **Some engine tools are tested only against stand-ins** (`standin_tools.rs`; `docs/tool-status.md` marks each tool).
- The README's clone URL says `craftanything` but the repo is `storytold/craft-anything` (README "Get started"; repo URL verified).
- The first public release (installers in CI) and the managed tier are still "next"; the browser build is a viewer, not the full workbench (`apps/craft-anything-web`).
- It **never bypasses DRM, logins or anti-cheat**, and the builder is told not to copy logos/photos/text without confirmation of ownership — respect that when writing requests (`README.md` "Responsible use").

## How to operate

- GUI: `open -a "Craft Anything"`; binary `/Applications/Craft Anything.app/Contents/MacOS/craft-anything` (`--version` prints `craft-anything 0.1.0`). **The macOS bundle contains no CLI** — get `craft-anything-cli` from the release assets or `cargo install --path apps/craft-anything-cli --locked`; keep versions matched.
- Mode: switch Clean room/Deep in the title bar or Settings, `settings_set deep_mode true`, or `--deep`/`--clean-room` per CLI run.
- Typical agent flow:
  ```sh
  craft-anything-cli doctor                      # what's missing (agents, engines, AI)
  craft-anything-cli capabilities                # toolsets, availability, engines
  craft-anything-cli triage ./target.bin         # first look, evidence records
  craft-anything-cli rebuild https://example.com "Recreate this website" --rounds 2
  craft-anything-cli rebuild - "A snake game in Rust"
  craft-anything-cli rebuild https://example.com "Make the header blue" --continue-in "<folder>"
  craft-anything-cli report --out report.md      # readable report from the ledger
  ```
- Settings live in `config.toml` (`engine::settings::config_dir()`, version 2); `LIGHTCRAFT`-style env overrides are not a thing here — check `craft-anything-cli doctor` output for paths.

## Working with an AI agent

- **You are also the builder Craft Anything drives.** When its coding-agent bridge launches you, read the inbox/notes flow: the person's answers arrive via the `builder-notes` hook; approval-required actions go through `core_action_approve` rather than being assumed.
- **Study first, honestly**: keep the investigation memory current (`core_investigation_show`, `core_brief_write`, `core_plan_update`, `core_hypothesis_record`, `core_finding_record`, `core_handoff_write`) — the MCP prompts enforce this discipline and it makes your answers auditable.
- **Respect the mode.** In Clean room the look-inside tools refuse; don't try to work around them. Switching to Deep is the person's decision.
- **Prepare inputs** in formats the toolsets open (archives, binaries, captures, DB dumps); use `core_archive_extract` rather than shelling out, so evidence lands in the ledger.
- **Verify rebuilds** from `checks/` outputs and the per-round comparison reports; a "Ready" step is a claim — open the result and re-check before telling the person it matches.
- **What not to attempt:** bypassing DRM/logins/anti-tamper (refused by design), promising Codex builds, editing `craft.json`/`.cany` by hand while a run is active, quoting the README's 284-tool number, assuming Ghidra is present (check `doctor`).

## Verification protocol

1. **Round-trip on a throwaway target first**: rebuild a tiny known website with `--rounds 1`, then read `craft.json`, `checks/round-1/` and `app/` before real work.
2. **Cite evidence ids** for every claim about the original; absence is not proof.
3. **Version your project folders** (copy the whole folder; every file carries a version and a newer file refuses saves).
4. **One project per run**: never edit a project folder while a rebuild is active; `--resume` exists for continuation.
5. **Update between projects**: this skill is pinned to v0.2.0; re-run `doctor` after updates.

## Sources & evidence

- Repo: https://github.com/storytold/craft-anything — inspected at tag **v0.2.0**, commit `b09b99aaa7985ebbc3d0fef467c4b688d4727cc1` ("Release 0.2.0", 2026-11-01), inspection date **2026-11-02**; the v0.1.0 ref was fetched for set diffs. Apache-2.0 and MIT (`LICENSE-APACHE`/`LICENSE-MIT`).
- Installed `/Applications/Craft Anything.app`: `CFBundleShortVersionString` 0.2.0, `CFBundleIdentifier` `ai.storyteller.craft-anything`, binary prints `craft-anything 0.2.0`; the bundle contains only `craft-anything`, no CLI.
- Read: `README.md`, `Cargo.toml`, `docs/{tools,STATUS,tool-status,claude-code,file-formats,pitfalls,extending,tool-ids}.md`, `apps/craft-anything-cli/src/{main,rebuild_cmd,setup_cmd,ai_cmd}.rs`, `crates/engine/src/{tool_list,registry,project,settings,self_test,plugins}.rs`, `crates/engine/src/tools/` (list), `crates/engine/src/versioned.rs`, `crates/mcp/src/{lib,prompts}.rs`, `crates/engines/src/` (list), `crates/formats/src/` (list), `crates/ai/`, `crates/setup/`.
- Counts recomputed from source at v0.2.0 (all unchanged from v0.1.0): **298 engine tools in 17 toolsets** (`docs/tools.md` generated list, item count 298; `MIN_TOOLS = 271`), 6 MCP prompts, 13 CLI subcommands + tool pass-through, 11 versioned-file rows in `docs/file-formats.md`; version constants from code: `MANIFEST_VERSION`/`FORMAT_VERSION`/`SETTINGS_VERSION` = 2/1/3 (⚠️ `docs/file-formats.md`'s table still shows 1/2/1 — stale repo doc).
- Workspace: 13 crates (`ai`, `analysis`, `disasm`, `engine`, `engines`, `evidence`, `formats`, `js`, `mcp`, `platform`, `setup`, `testkit`, `ui-egui`) + 3 apps (desktop, CLI, web).
- Evidence table: `evidence.md` next to this file.
