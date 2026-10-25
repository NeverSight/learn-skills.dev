---
name: blender-setup
description: Quickly check the official Blender Lab MCP connection with fresh evidence, deepen failed checks, and report AI agent, Python, Blender and editor readiness with exact next actions. Use for setup and troubleshooting.
---

# Blender Setup

Audit the active AI agent's official Blender Lab MCP connection. Default to a read-only check. Repairs, installations, configuration edits, application startup and Blender scene changes require the user's requested scope. Do not restore or focus the user's editor during an audit.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Fresh Quick Pass, Then Targeted Diagnostics

Every invocation starts fresh. Check the active session, actual native tool catalog, and one allowed read-only Blender query; collect lightweight configuration and running-program/window evidence when available. Display all twelve rows even when some evidence is unknown. Use `execute_blender_code` with the read-only `QUERY` in [scripts/check_setup.py](scripts/check_setup.py), or an allowed summary tool if execution is excluded. Check both MCP errors and nested Blender errors. Never use a CLI/background execution tool to bypass the existing connection.

A healthy connection should not trigger another MCP client, package-import subprocess, installer, release search, or repeated full audit. Identify evidence as **direct**, **inferred**, or **unknown**. A working official Python stdio server can establish that its runtime works; it does not prove an unread TOML field, the exact host Python path/version, or editor visibility. Blender's embedded Python is separate from the MCP server's host interpreter. Recognize `uvx` as an isolated launcher with limited environment diagnostics; do not test its imports in unrelated shell Python.

If fresh evidence fails, contradicts a prerequisite, or leaves necessary readiness evidence unresolved, perform one bounded second pass on only those affected checks. Preserve independent successful results. Unsupported inspection remains BLOCKED with a useful next action. Retry a scene query once only for a clearly transient error. No saved report, previous success, or cached setup state establishes current readiness. Display results; do not automatically save diagnostic reports.

## Workflow

1. Identify the platform, active AI client/session and available native diagnostics. For Codex, identify the actual Codex home and named MCP registration; do not assume this helper can inspect another client.
2. Inspect the current tool catalog and perform one allowed read-only native scene query. Preserve initialization/tool discovery separately from successful live communication.
3. Inspect the active client's supported configuration without printing secrets. Accept direct Python/venv `-m blmcp` with optional `--transport stdio`, `-t stdio` or `--transport=stdio`; recognize `uvx` as limited. Explain duplicate tables and unsupported forms without replacing working registrations.
4. Report Python Available and Python Configured separately. On a failing connection, resolve the configured interpreter using its effective environment/working directory, then check version and required imports only through a reviewed safe launch. Never assume terminal Python is the same interpreter.
5. Identify Blender only through currently running programs. Never search its executable on disk, PATH, registry or installation directories, or use `BLENDER_PATH` to discover it. No process means installation unknown, not uninstalled.
6. Match the process reached by MCP using the native query's PID or verified bridge ownership. If several processes remain ambiguous, block instance-specific checks and ask which is intended. Do not substitute another instance's visible window.
7. Inspect that process's editor window read-only. Require a visible, non-minimized editor; maximization is unnecessary. Closed, minimized, hidden and unknown states have different next actions. This check is independent of MCP access.
8. Check official MCP installation, enablement/compatibility and bridge runtime as three distinct report rows. Use the effective configured host/port, including inherited environment values. A listener alone does not prove add-on identity; socket refusal cannot distinguish a disabled add-on from a stopped bridge.
9. Deepen only failed, conflicting or necessary missing evidence in a bounded second pass. Honor platform permissions and tool policy; keep unsafe SDK launching blocked. Report version discrepancies for compatibility review without automatic upgrades or erasing observed live access.
10. Present the twelve-row Step / Status / Comment table, the separate MCP and editor verdicts, platform limits, and exact next actions. Do not invent unobserved interpreter, package, add-on or Blender versions.

## Report

Use **title case** for report step labels, headings and readiness labels; preserve **AI**, **MCP** and **Python** spelling. Use **Pass**, **Fail** and **Blocked** for displayed statuses, and **sentence case** for comments and next actions. Preserve exact casing in names, identifiers, paths, versions and quoted UI text.

Official MCP Installed means the official Blender Lab add-on is present. Official MCP Configured means it is enabled and compatible with Blender; verify the expected endpoint separately. Official MCP Running means the official bridge is responding. An installed add-on does not prove enablement, and an enabled add-on does not prove bridge startup. If identity or state is unverified, report Blocked; a socket listener alone does not establish an official running bridge. With direct Preferences evidence, an installed but unchecked add-on passes Installed and fails Configured with **Check the box beside MCP**; an enabled entry showing **Start MCP Server** fails Running with that startup action.

Use the exact headers **Step**, **Status**, **Comment**, with these rows in order. Replace the descriptions with this invocation's evidence.

| Step | Status | Comment |
|---|---|---|
| 1. AI Agent Available | observed status | Current client/session evidence |
| 2. AI Agent Configured | observed status | That client's official MCP registration |
| 3. Python Available | observed status | Configured runtime available; label runtime inference |
| 4. Python Configured | observed status | Required libraries in that runtime; label inference or unknown metadata |
| 5. Blender Installed | observed status | Inferred from running programs; otherwise unknown |
| 6. Blender Running | observed status | Current Blender process evidence |
| 7. Blender Open | observed status | Connected editor visible and not minimized |
| 8. Official MCP Installed | observed status | Official Blender Lab add-on installation evidence |
| 9. Official MCP Configured | observed status | Add-on enabled and compatible with Blender |
| 10. Official MCP Running | observed status | Official bridge responding at the expected endpoint |
| 11. MCP Handshake / Tools | observed status | Current session initialization/tool discovery |
| 12. Live Blender Communication | observed status | Fresh read-only scene query |

Display statuses as **✅ Pass**, **❌ Fail**, **⛔ Blocked**. Each Fail comment must contain its concrete solution. Each Blocked comment names the missing evidence/prerequisite and safe next step. Keep passing evidence short; label inferred passes explicitly. Failed process inspection means unknown, not closed. When no Blender process is found, step 5 is Blocked/installation unknown, step 6 fails with **Open Blender**, and step 7 is Blocked.

Below the table report **MCP Readiness** and **Editor Readiness** separately. A minimized editor can require **Restore Blender from the taskbar** while MCP remains working. A successful handshake stays Pass if the scene query fails. A helper that verifies configuration or local bridge evidence does not prove that native tools are exposed in this conversation. If tools are absent, explain that reconnecting/restarting the AI client or starting a new thread may be needed; do not describe it as currently connected.

## Supplemental Helper and Compatibility

Use native session tools first. [scripts/check_setup.py](scripts/check_setup.py) requires Python 3.11+ for the helper itself and reads Codex TOML (`CODEX_HOME`, otherwise `~/.codex`); its display labels remain neutral. It cannot inspect the current tool catalog by itself. The Claude adapter must use Claude's configuration/status instead.

Resolve paths relative to the installed skill. Only when the outer launch is verified safe, invoke the helper with `--format markdown` or use its default JSON. `--server NAME` selects a named registration; `--config PATH` explicitly selects the applicable TOML when defaults or project/CLI overrides do not describe the active session. Do not claim an effective override was inspected unless you actually inspected it.

The native API [platform adapter](scripts/platform_checks.py) checks process names/PIDs without a PowerShell child launch or Blender binary lookup. Fresh normalized native evidence can be passed directly to `audit(native=...)` or via `--native-stdin` from the current invocation. Keys are `agent_available`, actual `tool_count`, and `scene` containing the unwrapped QUERY result; use `scene_error` or `handshake_error` for observed failures. Never feed an old report or hard-coded success values back as current evidence.

On a failing direct-Python setup, `--allow-python-probe` permits the import-only second pass **after** the outer launch and complete child chain have been reviewed. The existing [windowless runner](scripts/windowless.py) captures diagnostics, sets no-console creation and owns descendants through a Windows Job. An unknown launch boundary remains Blocked. The SDK fallback remains disabled: an SDK upgrade alone is not evidence that its retry/cancellation/cleanup paths are safe.

| Platform | Local Helper Support | Validation Limit |
|---|---|---|
| Windows 10 / Windows 11 | Shared native Win32 process, listener and editor checks; reviewed import-only diagnostics | Validate on the available Windows host; do not claim live Windows 10 tests if none ran. Isolated/sandbox desktops may block real window inspection. |
| macOS | Native MCP access and configuration evidence when available; best-effort libproc process-name adapter | macOS support is limited and untested live here. Editor/listener ownership and import-subprocess diagnostics are missing; report Blocked and use supported fresh evidence. Do not grant permissions or launch a generic fallback automatically. |
| Other platforms | Native connection checks where available | Local adapters are unsupported; report each unavailable check honestly. |

## Troubleshooting from Observed Failures

| Evidence | Concrete Next Action |
|---|---|
| Python runs, but `blmcp` or a dependency is missing | Install the official package into the **configured** interpreter/venv; register that same interpreter. Do not install into a different shell Python by accident. |
| Base Python rejects installation as externally managed / PEP 668 | Create a dedicated venv using a compatible installed Python and install there. Do not bypass the managed-environment protection. One host Python can serve hobby work and this venv; a venv does not require another Blender version. |
| Duplicate TOML server tables or competing command/args examples | Keep one complete registration per server, with one command/args pair. For Windows paths, use valid TOML literal strings or correctly escaped backslashes. |
| Configured Python resolves to a Windows app alias | Configure a real installed/venv interpreter; do not launch an alias that may open the Store. |
| Expanded Preferences MCP entry has an unchecked enable box | **Check the box beside MCP.** Expanded details prove neither enablement nor a running bridge; do not reinstall a visibly installed add-on. |
| MCP enabled but **Start MCP Server** is shown | Start its bridge using the expected host/port when repairs/startup are authorized; otherwise give this next action. |
| Bridge refuses connection, without reliable UI evidence | Check both add-on enablement and bridge startup. Do not assert which one failed. |
| `http://localhost:9876/` does not render in a browser | Check MCP/live scene communication. The add-on's local TCP bridge is not a required browser page; stdio is the AI client-to-server transport. |
| MCP tools appear but the scene query fails | Preserve the handshake Pass; diagnose the configured Blender bridge and add-on. |
| Previously worked, now fails | Recollect fresh runtime evidence and examine only the failed prerequisites; never trust a previous success as current state. |

Use [Blender's official MCP setup](https://www.blender.org/lab/mcp-server/) and [official source/releases](https://projects.blender.org/lab/blender_mcp) when compatibility or repairs need research. Architecture: AI client → official Python MCP server over stdio → official add-on inside Blender over local TCP. The host MCP server is launched by the AI client; the user does not need to run another LLM client inside Blender. Llama.cpp is an optional alternative client. Do not install community replacements or untagged development revisions as an audit side effect.

## Editor Readiness and Screenshots

Screenshot capture is authorized as part of requested Blender work. Before **every** editor/window/area screenshot call, freshly inspect the connected process's visible, non-minimized editor; do not reuse an earlier setup result. If closed, ask the user to open Blender. If minimized or hidden, say **Restore Blender from the taskbar** or ask them to show it; maximization is unnecessary. If inspection is unavailable, report unknown and ask the user to make the editor visible. Pause capture until resolved, then check again. Never restore, focus or maximize it yourself.

Inspect captured pixels. Both official full-window and area captures have returned black while minimized on the observed Windows workstation. Visibility is a prerequisite, not a guarantee: report black/stale captures and request show/restore before a fresh check and retry. Never substitute a render or old screenshot as fresh editor evidence. This prerequisite applies to editor screenshots, not saved render output.

For supplied `.snagx` files, inspect ZIP entries, extract the original full-resolution image to a temporary location, inspect it and use metadata if needed. Preserve the original archive. User-supplied screenshots are evidence at capture time, not current live proof; keep multiple or accidentally concatenated paths distinct.

After changes, run [scripts/test_check_setup.py](scripts/test_check_setup.py) through a reviewed safe outer launcher. Offline failure fixtures and Windows safety checks must not alter Blender. Use one native read-only live query for integration; never enable a blocked SDK probe to complete validation.
