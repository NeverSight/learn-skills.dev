---
name: claude-patch
description: "Patch Claude Code CLI binary to unlock hard-coded limitations. Use when the user wants to apply, revert, or check status of binary patches after upgrading Claude Code. Community-contributed patches for model restrictions, feature flags, and schema unlocks."
disable-model-invocation: true
argument-hint: "apply|revert|status|list [patch-name]"
metadata:
  author: huybuidac
  version: "2.0.0"
  compatibility: "macOS, Linux, and Windows 10/11 (arm64/x86_64). Requires Node.js on PATH; macOS additionally needs codesign (ships with Xcode CLT)."
---

# claude-patch

Binary patches for Claude Code CLI — unlock hard-coded limitations without waiting for upstream changes.

All scanning and patching runs through one cross-platform tool, [patches/patch-bin.js](patches/patch-bin.js). It handles ad-hoc re-signing on macOS and the rename-swap a locked `claude.exe` needs on Windows, so there are no per-platform scripts to choose between.

```bash
node patches/patch-bin.js scan   --patch <name> [--bin <path>]   # state + derived anchor + guards
node patches/patch-bin.js apply  --patch <name> [--bin <path>]
node patches/patch-bin.js revert --patch <name> [--bin <path>]
node patches/patch-bin.js status [--bin <path>]                  # scan every patch
node patches/patch-bin.js list                                   # registered patch ids
```

`--bin` defaults to the resolved `claude` on PATH. `scan` exits 1 when the state is `abnormal` or `patched-inert`, `status` when any patch is.

## Workflow

1. **Identify the binary** — run `scan`; it prints the resolved path, size, and state. Show the user the path and `claude --version` before proposing any write.
2. **Select the patch** — from the user's argument, or ask. Read `patches/<name>.md` for what it does and what it is tested on.
3. **Confirm** — never write without explicit user confirmation for this specific binary.
4. **Apply or revert** — `apply` handles guard checks, backup, the write, the sidecar, re-signing, and self-verification in one step, and refuses rather than guessing if anything is off.
5. **Report** — state the resulting marker count, and that a restart is needed. (Earlier docs claimed `subagent-model` took effect without one; that was never demonstrated and the one time it was checked, the session had been restarted.)

**Never report a patch as working from a marker count alone.** Since 2.1.250 a marker can sit in a binary that ignores it — see [Bytecode shadowing](#bytecode-shadowing). `scan` now catches this, but the durable check is behavioural: `claude mcp serve` speaks JSON-RPC on stdio, so an `initialize` + `tools/list` round-trip prints the live tool schemas without spending a token.

## Available patches

| Patch | Description |
|-------|-------------|
| [subagent-model](patches/subagent-model.md) | Unlock `model` param on Agent tool — use any model id per-call |
| [auto-compact-by-model](patches/auto-compact-by-model.md) | Model-aware extended-context compact targets (Claude ≈400K, GPT ≈300K) |
| [free-opus](patches/free-opus.md) | Drop the Opus-5-only `heron_brook` section that forbids spawning subagents/workflows |
| [resume-model](patches/resume-model.md) | Keep a session's model on `--resume` when this build does not recognise the id |

Commands: `apply <patch>`, `revert <patch>`, `status` (scan every patch), `list`.

## Safety rules

- **NEVER** patch without explicit user confirmation.
- **NEVER** patch if a context guard fails — `apply` enforces this, so do not work around it.
- If state is `abnormal`, abort and report. Both-zero (no anchor, no marker) means the fingerprint changed: re-derive it before doing anything else, never patch blind.
- **A marker is not proof the patch works.** `patched` means marker present *and* nothing shadowing it; `patched-inert` means the write landed on code that never runs.
- Every write is length-preserving and verified against the expected bytes at that offset first, so a stale offset aborts instead of corrupting the binary.
- Backups (`<binary>.bak.<ts>`) are ~290 MB each. Mention rotation after a version is confirmed working.

## Why anchors are derived, not hardcoded

Every literal anchor in this skill's history eventually matched 0 times, because the bundler renames minified identifiers every few builds. A count of 0 is indistinguishable from "the feature was removed", so a hardcoded anchor turns routine drift into a false abort.

Each patch therefore derives its anchor at scan time from landmarks that do not move — string literals the product ships (`.describe()` text, `source:"…"` labels) and positional locals the bundler assigns by position. Patch definitions document the derivation rule rather than the bytes. When adding a patch, find a landmark first; if the only stable thing you can find is a minified name, expect it to rot.

## Bundle multiplicity

The bun-compiled binary may embed the JS bundle more than once:

- macOS ≤ 2.1.132: **2 instances**; macOS ≥ 2.1.133: **1**
- Windows: **1** (all observed versions)

Never hard-assert a count — derivation counts landmarks and patches all of them.

## Bytecode shadowing

At **2.1.250** the binary began shipping a JSC bytecode copy of each module alongside the JS source and **running the bytecode**. The source is still complete and still what every patch here edits — it just stops being what executes. A source-only patch then leaves the marker in the file and changes nothing, which the old `scan` reported as a clean `patched`.

The fix is not to patch bytecode. bun's embedded module graph gives each module a `bytecode` slice, and an empty slice means "not cached, compile the source". So `apply` zeroes the 4-byte length of that slice for the module holding the patch site, and the source patch becomes live.

```
trailer magic "\n---- Bun! ----\n"
  byte_count u64 @ magic-32   →  base = (magic-32) - byte_count
  modules_ptr (u32 off, u32 len) @ magic-24
record = 52 bytes: name, contents, sourcemap, bytecode, module_info,
         bytecode_origin_path  (6× StringPointer{u32 offset, u32 len})
         + encoding, loader, module_format, side (4× u8)
```

The record is found by asking which module's `contents` range contains the patch offset — never by chunk name, which is content-hashed and changes every build. Layout is from bun's `src/standalone_graph/StandaloneModuleGraph.rs`; if the trailer does not decode, `scan` says so and `apply` warns rather than guessing.

Cost is one module compiled at startup instead of loaded: **~50 ms** measured on 2.1.250 for the 3.9 MB chunk holding the Agent tool (init 0.235s → 0.283s). Other modules keep their bytecode.

Two states matter:

- `patched-inert` — marker present, bytecode still shadows it. Re-run `apply`; it repairs in place (bytecode edit only, source untouched) rather than refusing.
- Binaries **≤ 2.1.239** run from source and need no bytecode edit. Their graph may not decode with the layout above, which is reported, not fatal.

Verified end to end on 2.1.250 macOS arm64: pristine → `apply` → Agent tool `model` loses its enum and a subagent really runs on `gpt-5.6-luna[1M]`; `revert` → enum returns.

## Revert

`revert` prefers the **sidecar** `<binary>.rtk-<patch>.json` that `apply` writes: it records the original bytes for each offset, so the reverse-patch is exact and immune to build mismatch. This matters because a patched binary alone cannot reconstruct a drifted alias — only its length survives. Its `graphEdits` array holds the original bytecode-slice lengths, restored the same way; a sidecar written before that field existed reverts the source sites and leaves the graph alone.

Without a sidecar (patched before they existed) it falls back to a **content-validated backup**: the candidate must itself scan as unpatched with matching landmarks and guards. Do **not** gate on file size — on macOS the backup is Apple-signed while the patched binary is ad-hoc signed, so their sizes legitimately differ. A `<binary>.preRevert.<ts>` snapshot is taken before any write, so the revert itself is undoable.

## Platform notes

- **macOS** — patching invalidates Anthropic's signature; `apply`/`revert` re-sign ad-hoc and verify. Gatekeeper may prompt on first launch.
- **Windows** — a running `claude.exe` is locked, so writes go to a copy that then takes the original's path (renaming a running image only updates the directory entry). Authenticode becomes `HashMismatch`; the binary still runs, though SmartScreen/AppLocker policy may object. A displaced `*.replacing.*` file may linger until the old process exits.
- **Auto-update** — each new Claude Code version ships a fresh, unpatched binary. Re-apply per version.

## Contributing

To add a new patch, create `${CLAUDE_SKILL_DIR}/patches/<name>.md` following [patches/TEMPLATE.md](patches/TEMPLATE.md), and register its derivation in `patch-bin.js`.
