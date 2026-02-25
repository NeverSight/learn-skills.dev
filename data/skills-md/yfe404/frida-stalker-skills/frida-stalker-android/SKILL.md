---
name: frida-stalker-android
description: "Trace native execution on Android with Frida Stalker (Frida 17+): call summaries, event parsing, transforms, and performance-safe start/stop patterns."
---

# Frida Stalker (Android)

## Overview

Use this skill when you need to trace native code execution on Android using Frida's `Stalker` API, with templates geared for ARM/ARM64 and performance-safe defaults.

This skill assumes Frida 17+ JavaScript semantics.

## When To Use This Skill

- User explicitly asks for "Frida Stalker" on Android.
- You need to measure native call activity (who got called, how often) with low overhead.
- You need ordered call events (call graph reconstruction) or coarse coverage.
- You need to inject logic on basic-block compilation through `transform(iterator)`.

## Quick Decision Guide

- Want call counts per target and don't care about ordering: use `onCallSummary`.
- Want ordered call/ret/block/compile events: use `onReceive` and decode with `Stalker.parse()`.
- Want instruction-level matching and callouts: use `transform(iterator)` (heavy; do it narrowly).
- Want to watch a small set of call targets: consider `Stalker.addCallProbe()`.

## Core API Facts (Frida 17+)

- `Stalker.follow([threadId, options])`
- Provide exactly one callback: `onReceive(events)` or `onCallSummary(summary)`.
- `Stalker.unfollow([threadId])`
- `Stalker.parse(events, { annotate, stringify })`
- `Stalker.flush()` drains buffered events early (otherwise periodic draining is controlled by `Stalker.queueDrainInterval`).
- `Stalker.garbageCollect()` should be called after `unfollow()` to free accumulated memory at a safe point.
- `Stalker.exclude({ base, size })` excludes a memory range from stalking (useful to skip noisy/system modules).
- Tuning:
- `Stalker.trustThreshold` default `1` (set `-1` for no trust, `0` to trust immediately, or `N` to trust after `N` executions).
- `Stalker.queueCapacity` default `16384` events.
- `Stalker.queueDrainInterval` default `250` ms (set `0` to disable periodic draining and call `Stalker.flush()` manually).

## Workflow

1. Define objective.
2. Choose thread(s).
3. Choose capture mode and filters.
4. Pick a template and adapt it.
5. Run, tune performance, and clean up.

If you are using the Frida MCP tools, also enable `$frida-mcp-workflow` and follow its phases (Idea -> Scripting -> Execution -> Notes).

## Templates

Start from these and keep scripts file-based.

- `templates/stalker-call-summary.js`: low-overhead call counting via `onCallSummary`.
- `templates/stalker-onreceive-parse.js`: receive binary events and decode with `Stalker.parse()`.
- `templates/stalker-start-stop-around-hook.js`: follow/unfollow only during a specific hooked function call.
- `templates/stalker-call-probe.js`: observe calls to a single target via `Stalker.addCallProbe()`.
- `templates/stalker-transform-skeleton.js`: minimal `transform(iterator)` skeleton with ARM/ARM64 safety check.
- `templates/stalker-filter-modules.js`: helper to select "app modules" on Android and exclude the rest.

## Quick Start

1. If you do not know the thread id yet, start with `templates/stalker-start-stop-around-hook.js`.
2. If you already know the thread id and want low overhead, use `templates/stalker-call-summary.js`.
3. If you need ordered events, use `templates/stalker-onreceive-parse.js` and keep event types narrow.
4. If you only care about calls to one target, start with `templates/stalker-call-probe.js`.

## MCP Usage Notes (If Available)

When driving this through the Frida MCP tools, prefer this flow:

1. Create or attach a session (`mcp__frida__create_interactive_session` / `mcp__frida__attach_to_process`).
2. Load the selected template with `mcp__frida__load_script`.
3. Start tracing through RPC exports using `mcp__frida__call_rpc_export` (templates expose `start()` / `stop()` when appropriate).
4. Use `mcp__frida__get_session_messages` to consume output.

Keep a script ledger (what is loaded, purpose, and teardown path). This is enforced by `$frida-mcp-workflow`.

## Android-Specific Notes (Practical)

- Thread choice matters more than you think.
- If you start stalking the wrong thread, you will see nothing, or only system noise.
- A safe pattern is to start stalking from inside an `Interceptor.attach()` callback, using `Process.getCurrentThreadId()` to capture the thread that is actually executing your target function.

- Module filtering is essential.
- On Android, app code is usually in modules whose `path` contains `/data/app/`, `/data/data/`, or an extracted APK split path.
- Exclude common noise sources (`libart.so`, `libc.so`, `liblog.so`, etc.) using `Stalker.exclude()` when you only care about your app's own native libs.

- 32-bit ARM note.
- If you use raw addresses on 32-bit ARM, Thumb functions require the low bit set. Prefer addresses returned by Frida APIs like `Process.getModuleByName(...).getExportByName(...)`.

- Avoid `Process.runOnThread()` unless you know what you're doing.
- It can interrupt a thread in non-reentrant code and cause deadlocks/crashes.

## Performance Rules Of Thumb

- Avoid `events.exec` unless you truly need instruction-level traces. It produces huge volumes of data.
- Prefer `onCallSummary` over `onReceive` when you can.
- Keep your callbacks lean; push heavy work to the host side when possible.
- Use `Stalker.exclude()` aggressively to reduce time spent in system libraries.
- Prefer manual draining (`Stalker.queueDrainInterval = 0` + `Stalker.flush()`) when you need deterministic windows.
- Call `Stalker.garbageCollect()` after unfollowing, especially if you repeatedly start/stop.

## Cleanup Checklist

- `Stalker.unfollow(threadId)`
- `Stalker.flush()`
- `Stalker.garbageCollect()`

## Troubleshooting

- No output at all.
- You are likely stalking the wrong thread, or your callback isn't being invoked (e.g., you followed a thread that never runs).

- Output is only system noise.
- Add module filters and exclusions. Start stalking from inside a hook where you know you're in app code.

- Target slows to a crawl or dies.
- Reduce enabled events, stop using `exec`, and switch to `onCallSummary`. Exclude large/noisy modules.

For deeper notes, see:
- `references/stalker-api.md`
- `references/android-filtering.md`
