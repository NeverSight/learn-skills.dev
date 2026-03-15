---
name: debug-tauri-devtools
description: Use skill if you are debugging a live Tauri app with CrabNebula DevTools to inspect Rust logs, IPC calls, runtime config, plugin permissions, or bundled assets.
---

# Debug Tauri DevTools

Use CrabNebula DevTools for the part of a Tauri app that browser DevTools cannot
see: Rust-side logs, IPC spans, resolved runtime config, capability state,
plugin wiring, and bundled asset resolution.

## Trigger

Activate when the user reports or the agent observes any of these:

- a Tauri `invoke()` call fails, hangs, is unexpectedly slow, or returns wrong data
- a Rust panic/error exists but the failing module or span is unclear
- a plugin, capability, or window-scope permission appears broken
- an asset loads in dev but not in build, or exists locally but not in the bundle
- behavior differs across desktop/mobile or debug/build modes
- you are about to add `println!()`, guess at serde/config issues, or inspect the browser Network tab for Tauri IPC
- CrabNebula DevTools needs to be installed, configured, or is not connecting

## When NOT to use this skill

Do not activate for:

- DOM, CSS, layout, browser-only JavaScript, or framework component debugging
- HTTP/fetch/WebSocket debugging that lives in the browser network stack
- static code review without a live runtime symptom
- cases where the problem is already proven and you only need to implement a fix

Use browser DevTools for webview problems. Use CrabNebula DevTools when the
unknown lives behind the webview.

## First-time setup

If DevTools is not installed in the project, complete installation before
entering the debugging workflow:

1. **Check**: search `src-tauri/Cargo.toml` for `tauri-plugin-devtools`. If absent, or if `lib.rs` does not register the plugin with `.plugin(tauri_plugin_devtools::init())`, DevTools is not installed.
2. **Install**: follow the steps in `references/setup/installation-and-config.md`. Use the "Which Pattern to Use" table to pick the right initialization pattern for your project.
3. **Restart**: stop the running app and restart with `cargo tauri dev`. First run after adding DevTools triggers a longer compilation — wait for the WebSocket URL to appear in terminal output.
4. **Verify**: confirm DevTools connects — Console tab should show initialization logs, Config → Plugins should list registered plugins, and invoking any `#[tauri::command]` should produce an entry in the Calls tab.
5. **Continue**: after verification, proceed to Phase 2 below.

> **Note:** Tauri IPC commands (`#[tauri::command]`) are automatically instrumented by Tauri core. They appear in the Calls tab without any additional code.

## Rust-side visibility map

> All "Open first" instructions below require DevTools to be connected.
> If DevTools is not running, complete the First-time setup section above.

| If the symptom is... | Open first | Capture this evidence |
|---|---|---|
| Rust panic, missing log source, noisy tracing, or startup failure | **Console** | level, target module, message, fields, startup timestamp |
| `invoke()` error, wrong response, serialization mismatch, hang, or slow command | **Calls** | command name, Arguments, Response, Status, Duration, child spans |
| Permission error, plugin not initialized, wrong window scope, or config mismatch | **Config**, then **Console** | Security capabilities, Plugins section, startup errors, resolved overrides |
| Asset missing, wrong runtime path, or dev/build difference | **Sources**, then **Config** | whether the file exists in the bundle, exact runtime path, bundle/resources/CSP settings |
| Desktop works but mobile breaks | **Console** + **Calls** on device | platform-specific errors, path differences, permission/init differences |

> ⚠️ **Steering:** The visibility map assumes DevTools is connected and showing data. If DevTools shows a blank dashboard or no data, this is ITSELF the problem to solve — go to `references/setup/installation-and-config.md`, not Phase 2.

Use the minimal reading sets at the bottom of this file to load the right references for each symptom category.

## Workflow

Follow this order. Do not skip from symptom straight to code edits.

### Phase 1 — Establish the failing path

> ⚠️ **Steering:** Do NOT skip the DevTools detection check. In derailment testing, agents jumped straight to debugging without DevTools installed, wasting an entire diagnosis cycle. Always verify `tauri-plugin-devtools` in Cargo.toml first.

- Name the exact action that reproduces the issue.
- Note expected vs actual behavior.
- Record environment: `cargo tauri dev`, debug build, release build, desktop platform, or mobile target.
- **DevTools check**: search `src-tauri/Cargo.toml` for `tauri-plugin-devtools`. If absent, or if `lib.rs` does not call `.plugin(tauri_plugin_devtools::init())`, DevTools is not installed. Follow the First-time setup section above, then return here and continue to Phase 2.

### Phase 2 — Observe before theorizing

> ⚠️ **Steering:** If operating as an AI agent without visual DevTools UI, do NOT claim you "opened the Calls tab." Instead, use terminal output from `cargo tauri dev` (DevTools subscriber prints to stderr) or ask the user for screenshots. Fabricating visual evidence is a P0 failure.

- Start in the single tab that matches the symptom (see visibility map).
- Capture exact evidence before browsing other surfaces:
  - **Console**: target path, error text, fields, panic location
  - **Calls**: command, args, response/error, timing, nesting
  - **Config**: capabilities, plugin registration, build/bundle/security values
  - **Sources**: bundled file presence, exact path, case-sensitive mismatches
- Prefer built-in DevTools filters and sorting before changing code or `RUST_LOG`.

**Agent-mode evidence gathering:** When operating without a visual DevTools UI (e.g., an AI agent in a terminal), evidence comes from: (1) terminal output from `cargo tauri dev` — DevTools subscriber prints tracing events to stderr, (2) adding `tracing_subscriber::fmt` as a secondary output layer for structured logs, (3) asking the user to share DevTools screenshots or tab exports. Use these sources in place of the visual tab instructions above.

> **Shortcut for capability/permission errors:** If the symptom is clearly a permission error and capability files are accessible, you may inspect `src-tauri/capabilities/*.json` directly to identify missing permission identifiers. Cross-reference with the error message and `references/plugins/capabilities-and-permissions.md`. If the fix is unambiguous (a specific permission string is missing), proceed directly to Phase 5. Use DevTools for verification in Phase 6 if available.

### Phase 3 — Form 1–3 falsifiable hypotheses

> ⚠️ **Steering:** Every hypothesis MUST map to a Phase 4 routing entry. In testing, agents formed hypotheses about sequential processing but had no routing to investigate it — the diagnosis stalled. If your hypothesis does not match a routing entry, you likely need `references/performance/profiling-and-optimization.md`.

Each hypothesis must identify:

1. the suspected failure mode
2. the exact evidence that would confirm it (from DevTools or static inspection)
3. the next inspection surface or reference (refer to the Phase 4 routing list below)

Good hypothesis shapes:

- "JS arguments do not match the Rust `Deserialize` struct."
- "The command is blocked on uninstrumented file I/O or lock contention."
- "The plugin is registered, but the capability or window scope is missing."
- "The asset exists in source control but is absent from the bundle."
- "Mobile uses a platform-specific path or permission assumption that desktop does not."
- "Items are processed sequentially — duration scales linearly with input count."
- "The Tauri ACL permission identifier is missing vs an OS-level permission error."

### Phase 4 — Inspect the hypothesis path

> ⚠️ **Steering:** Before adding `#[tracing::instrument]`, verify that `tracing = "0.1"` is in Cargo.toml [dependencies]. Missing this dependency causes a compile error that agents misdiagnosed as a Tauri issue.

> Before inspecting, review the Decision Rules section below — it contains
> key conditional routing for common evidence patterns.

Use the narrowest inspection path that can confirm or reject the hypothesis:

- **Rust handler / serde / async / state issue** → `Calls` + `references/rust/backend-debugging.md`
- **Need deeper span detail** → `references/devtools-ipc-span-anatomy.md`
- **Permission / capability / plugin init issue** → `Config` + `Console` + `references/plugins/capabilities-and-permissions.md`
- **Sequential/parallel processing or O(n) scaling** → `Calls` + `references/performance/profiling-and-optimization.md`
- **Log visibility or missing dependency logs** → `references/rust/logging-and-tracing.md`
- **Subscriber / `tauri-plugin-log` / custom integration question** → `references/devtools-integration-patterns.md`
- **Asset / bundle / build-mode mismatch** → `Sources` + `Config` + `references/devtools-common-debugging-scenarios.md`
- **Mobile-only divergence** → `references/mobile/android-ios-debugging.md`
- **Performance bottleneck or profiling needed** → `references/performance/profiling-and-optimization.md`
- **Need tool internals or pipeline limits** → `references/devtools-architecture-deep-dive.md`

If evidence is still incomplete, add visibility instead of guessing. See
Guardrails for what NOT to do when adding instrumentation.

- Ensure `tracing = "0.1"` is in `[dependencies]` in `Cargo.toml`. For async instrumentation with `.instrument()`, also add `use tracing::Instrument;`.
- **For slow/missing spans**: add `#[tracing::instrument]` to internal Rust functions. If the slow code is inline (not in a separate function), use manual spans: `let _span = tracing::info_span!("process_item", item = %item).entered();` around the slow section.
- **For panics**: enable `RUST_BACKTRACE=1`.
- **For missing dependency logs**: use the `split()/attach_logger()` pattern (see `references/devtools-integration-patterns.md`).
- **For dev/build or desktop/mobile differences**: compare the same repro in both environments before changing code.

### Phase 5 — Separate diagnosis from repair

> ⚠️ **Steering:** A "narrow fix" means targeting the confirmed bottleneck — e.g., parallelizing a loop proven slow by span evidence. Do NOT interpret "avoid refactors" as "never change code structure." The guardrail prevents speculative changes, not evidence-based structural fixes.

Only edit app code/config after one hypothesis is confirmed by evidence. See
Guardrails on keeping diagnosis and repair separate.

When you do change something:

- Fix the narrow failing path, not nearby speculative code. A "narrow fix" targets the confirmed bottleneck — for example, parallelizing a sequential loop proven slow. This is not a "refactor" in the guardrail sense. A "refactor" would be restructuring unrelated code, renaming modules, or adding abstractions not required by the fix.
- For the fix approach, consult the reference file that matches the confirmed diagnosis — e.g., `references/performance/profiling-and-optimization.md` for performance issues, `references/plugins/capabilities-and-permissions.md` for permission issues.
- Keep temporary tracing in place until the verification pass.
- Avoid cleanup refactors until the bug is proven fixed.

### Phase 6 — Verify in the same surface

> ⚠️ **Steering:** You MUST restart `cargo tauri dev` after code changes. Agents frequently forgot this step and verified against stale runtime state, declaring bugs "fixed" when the old binary was still running.

Rebuild the app (e.g., restart `cargo tauri dev`), reconnect DevTools, and
reproduce the same user action or invoke call. Confirm the evidence changed
where it originally failed:

- **Calls**: status, response, duration, or child span structure is now correct. Compare duration against the classification table in `references/devtools-tab-reference.md` — "correct" means the symptom is resolved and the absolute duration falls in an acceptable range for the use case.
- **Console**: error/panic is gone or replaced by the expected trace sequence
- **Config**: missing capability/plugin/config value is now present in resolved config
- **Sources**: missing asset/path mismatch is resolved at runtime
- **Mobile/build comparisons**: previously divergent evidence now matches the expected platform behavior

Remove DEBUG-ONLY temporary instrumentation (e.g., extra `tracing::debug!()` events added solely for this diagnosis). KEEP structural instrumentation (`#[tracing::instrument]` on meaningful functions) for ongoing visibility.

## Decision rules

- If DevTools is not installed in the project, install it before any debugging. All other decision rules require DevTools to be running.
- If one child span dominates the total duration, optimize that child first.
- If the parent span is slow but child spans are missing or too small, instrument internal Rust code before refactoring.
- If the Calls response already shows a permission error (or the browser console shows an `invoke()` rejection), inspect resolved capabilities and window scope before touching the command handler.
- If no IPC call appears at all, check whether the frontend actually invoked the command, whether the command name is wrong, whether a capability blocked it, or whether DevTools was initialized too late.
- If Console is noisy, use UI filters first; only narrow `RUST_LOG` when throughput is too high to reason about.
- If release builds have no DevTools data, treat that as expected `#[cfg(debug_assertions)]` behavior and reproduce with a debug-capable target before drawing conclusions.
- If desktop and mobile differ, compare Console and Calls evidence on both platforms before sharing a fix.
- If the error message contains "not allowed" or "capability", this is a Tauri ACL error. If it contains "os error 13" or "Permission denied", this is an OS-level error. These require completely different fixes — do not confuse them.
- If you cannot visually inspect DevTools (e.g., you are an AI agent), use `cargo tauri dev` terminal output as your primary evidence source. The DevTools subscriber prints tracing events to stderr.

## Common agent mistakes

| Mistake | Impact | Prevention |
|---|---|---|
| Skipping DevTools installation check | Entire diagnosis cycle wasted on tool that isn't installed | Always run Phase 1 DevTools check first |
| Using `println!()` instead of `tracing` | Output doesn't appear in DevTools, diagnosis fails | Use `tracing::info!()`, `tracing::debug!()` etc. |
| Fabricating DevTools visual evidence | Agent claims to "see" tab data it cannot access | Use terminal output or ask user for screenshots |
| Forgetting `tracing` dependency | Compile error misdiagnosed as Tauri issue | Check Cargo.toml for `tracing = "0.1"` before instrumenting |
| Not restarting after code changes | Verification against stale binary | Always restart `cargo tauri dev` in Phase 6 |
| Confusing ACL vs OS permission errors | Wrong fix applied (capability vs filesystem) | Check error message: "not allowed" = ACL, "os error" = OS |
| Using `fs:read` instead of `fs:allow-read-text-file` | Invalid Tauri v2 permission identifier | Always use full v2 ACL identifiers |
| Running `cargo tauri dev` from `src-tauri/` | `beforeDevCommand` fails (can't find package.json) | Run from project root where `package.json` lives |

## Guardrails

- Do not use Browser Network tools as proof for Tauri IPC behavior.
- Do not change serde structs, capability files, plugin order, or asset paths without first reading the runtime evidence that points there.
- Do not use `println!()` as your primary Rust debugging surface; use `tracing` so the data stays in DevTools.
- Do not instrument every function. Add spans only where evidence is missing.
- Do not convert a diagnosis task into a broad refactor.
- Do not claim a root cause until you can point to a concrete log, span, config value, permission, or asset path and point to the exact evidence.

## Do this, not that

| Do this | Not that |
|---|---|
| Read **Calls** Arguments/Response before touching Rust command types | Guess at serde mismatches from source alone |
| Check **Config** Security and Plugins sections before editing capability files | Blindly patch `src-tauri/capabilities/*.json` |
| Use `tracing` macros and targeted `#[tracing::instrument]` | Scatter `println!()` or instrument everything |
| Use **Sources** as runtime truth for bundled files | Assume the dev server path matches the build bundle |
| Compare desktop vs mobile or dev vs build evidence in the same tab | Port a desktop fix to mobile/build without proof |
| Keep diagnosis and repair as separate steps | Make speculative code edits while the cause is still ambiguous |

## Recovery paths

- **DevTools will not connect or shows no data** → `references/setup/installation-and-config.md`
- **`tauri-plugin-log` conflicts or dependency logs are missing** → `references/rust/logging-and-tracing.md`, `references/devtools-integration-patterns.md`
- **The command is slow or hung but the waterfall is too shallow** → `references/devtools-ipc-span-anatomy.md`, `references/rust/backend-debugging.md`
- **Known symptom, unclear next move** → `references/devtools-common-debugging-scenarios.md`
- **Need field-by-field help with tabs, filters, or exports** → `references/devtools-tab-reference.md`
- **Need performance or overhead guidance beyond one command** → `references/performance/profiling-and-optimization.md`
- **Need to understand pipeline limitations or internal behavior** → `references/devtools-architecture-deep-dive.md`
- **Permission/capability error without DevTools** → Inspect `src-tauri/capabilities/*.json` directly. Compare with `references/plugins/capabilities-and-permissions.md` Common Plugin Permission Identifiers table. Add the missing permission identifier and restart the app.

## Minimal reading sets

### First-time installation

- `references/setup/installation-and-config.md`
- If your project uses `tauri-plugin-log`, also read `references/devtools-integration-patterns.md`

### DevTools setup or connectivity is the problem

- `references/setup/installation-and-config.md`
- `references/rust/logging-and-tracing.md`
- `references/devtools-integration-patterns.md`

### An IPC command fails, hangs, returns wrong data, or is slow

- `references/devtools-ipc-span-anatomy.md`
- `references/devtools-common-debugging-scenarios.md`
- `references/rust/backend-debugging.md`
- `references/performance/profiling-and-optimization.md`

### I need better Rust-side visibility

- `references/rust/logging-and-tracing.md`
- `references/rust/backend-debugging.md`
- `references/devtools-tab-reference.md`

### A plugin, capability, or resolved config looks wrong

- `references/plugins/capabilities-and-permissions.md`
- `references/devtools-tab-reference.md`
- `references/devtools-common-debugging-scenarios.md`

### Permission error on a specific command (quick path)

- `references/plugins/capabilities-and-permissions.md` — may be the only file needed

### It works in dev/desktop but breaks in build/mobile or assets are missing

- `references/devtools-common-debugging-scenarios.md`
- `references/mobile/android-ios-debugging.md`
- `references/setup/installation-and-config.md`
- `references/devtools-tab-reference.md`

### I need subscriber, performance, or internal pipeline details

- `references/devtools-integration-patterns.md`
- `references/performance/profiling-and-optimization.md`
- `references/devtools-architecture-deep-dive.md`

## Reference routing

| File | Load when |
|---|---|
| `references/setup/installation-and-config.md` | DevTools is not installed, not connecting, registered too late, or you need debug-only/build-mode setup rules. |
| `references/rust/logging-and-tracing.md` | Console evidence is missing/noisy, you need `tracing` guidance, `RUST_LOG` strategy, or `tauri-plugin-log` bridging. |
| `references/rust/backend-debugging.md` | The problem lives in command handlers, state, serde, async blocking, deadlocks, panics, or external Rust debugging tools. |
| `references/devtools-ipc-span-anatomy.md` | You need to interpret waterfall timing, nesting, gap analysis, missing spans, or targeted span instrumentation. |
| `references/devtools-common-debugging-scenarios.md` | The symptom matches a known pattern and you want the fastest route from observation to likely root cause. |
| `references/devtools-tab-reference.md` | You need tab columns, filters, sorting, export behavior, or precise UI field meanings. |
| `references/plugins/capabilities-and-permissions.md` | Permissions, capabilities, plugin initialization, window scope, or dev/build config resolution is suspect. |
| `references/mobile/android-ios-debugging.md` | The bug is mobile-only or you need Android/iOS connection, logging, or platform-specific debugging steps. |
| `references/performance/profiling-and-optimization.md` | Calls show slow spans, redundant invokes, profiling questions, or you need to reason about overhead and optimization tradeoffs. |
| `references/devtools-integration-patterns.md` | You need subscriber wiring, `tauri-plugin-log` coexistence, cfg patterns, or advanced integration guidance. |
| `references/devtools-architecture-deep-dive.md` | You need internal pipeline, gRPC server, threading, or architecture-level constraints to explain missing/odd behavior. |

## Final reminder

Use CrabNebula DevTools to collect runtime truth, not to justify a hunch. Stay
in observation-first mode until you can name the failing command, log target,
config value, permission, or asset path and point to the exact evidence.
