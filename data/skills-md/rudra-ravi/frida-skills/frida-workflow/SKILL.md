---
name: frida-workflow
description: Plan Frida instrumentation across Android, iOS, native libraries, desktop processes, Gadget, agents, setup, discovery, hook strategy, tracing, and skill routing.
---

# Frida Workflow

Use this as the orchestration skill before writing or running Frida instrumentation.

## Operating Rules

1. Confirm authorization and target scope before instrumenting third-party software.
2. Research current Frida docs when behavior depends on version, device mode, Java bridge, Gadget, or CLI flags.
3. Record the exact Frida client, server, gadget, OS, architecture, package/bundle/process id, and attach/spawn mode.
4. Start with observation hooks, then move to mutation only after the target and call shape are proven.
5. Keep hooks small, reversible, and logged. Prefer precise class/function hooks over broad bypass scripts.

## Skill Routing

- Use `frida-setup-checklist` before hook work when host, device, version, or transport state is unknown.
- Use `frida-tools-reference` when choosing between `frida`, `frida-ps`, `frida-ls-devices`, `frida-trace`, `frida-discover`, `frida-kill`, or `frida-create`.
- Use `frida-tracing-discovery` when class, symbol, module, method, or call path is unknown.
- Use `frida-agent-builder` for TypeScript agents, reusable script projects, RPC exports, packaging, and multi-script organization.
- Use `frida-native-hooks` for `Interceptor`, `NativeFunction`, memory scanning, exports, imports, symbols, CModule, and hot native paths.
- Use `frida-android-hooks` for `Java.perform`, class loaders, overloads, JNI, Android pinning analysis, and APK-backed workflows.
- Use `frida-ios-hooks` for `ObjC`, Swift/Objective-C methods, modules, iOS pinning analysis, and rootless jailbreak constraints.
- Use `frida-tls-pinning` for TLS/SSL pinning analysis and bypass work across Java, ObjC, Flutter, React Native, BoringSSL/OpenSSL, Conscrypt, OkHttp, and SecTrust paths.
- Use `frida-anti-instrumentation` for anti-Frida, root/jailbreak, emulator, debugger, ptrace, port scan, thread-name, and integrity checks.
- Use `frida-data-extraction` when the goal is observing runtime data such as HTTP, headers, tokens, JSON, crypto inputs/outputs, preferences, files, SQLite, or memory buffers.
- Use `frida-codeshare-search` to search CodeShare, extract scripts, review source, and convert public snippets into local agents or `--codeshare` commands.
- Use `frida-script-review` before running public, generated, broad, native-pointer-heavy, or mutation-heavy scripts.
- Use `frida-troubleshooting` when attach/spawn fails, hooks do not fire, the target crashes, `ObjC`/`Java` is unavailable, or versions mismatch.

## Workflow

1. **Define the objective**: state the behavior to observe or change, expected proof, and rollback condition.
2. **Inventory the environment**:
   ```bash
   frida --version
   frida-ps -Uai
   frida-ls-devices
   ```
3. **Choose mode**:
   - Use spawn for early app initialization hooks.
   - Use attach for already-running processes.
   - Use Gadget when attach is blocked, no root/jailbreak path exists, or the instrumentation must load from inside the app.
4. **Discover before hooking**:
   - Native: enumerate modules, exports, imports, symbols, and readable strings.
   - Android: enumerate loaded classes/methods and confirm the correct class loader.
   - iOS: confirm `ObjC.available`, enumerate classes/modules, and resolve Swift symbols when needed.
5. **Hook minimally**: log entry, arguments, return values, thread/backtrace when useful, then narrow.
6. **Verify**: prove the hook fires with target behavior, no crash, and expected logs. Save commands and script version used.

## Practitioner Playbook

- Use Frida CodeShare and public snippets as reconnaissance and pattern libraries. Read the script before running it, then copy only the hooks that match the app's actual framework/version.
- Build a hook ladder: start at high-level APIs, log stack traces/callers, then move downward into framework, JNI/native, crypto, TLS, or syscall boundaries only when evidence points there.
- Prefer targeted scripts over "universal bypass" bundles once the target path is known. Broad bundles are useful to discover likely surfaces but hide which hook actually mattered.
- For obfuscated apps, follow data instead of names: URLs, headers, byte arrays, crypto inputs/outputs, file paths, reflection calls, dynamic DEX loads, and native library loads.
- Keep every experiment reproducible: exact command, target version, device, Frida version, script hash or filename, and the behavioral proof observed.
- When the target has anti-instrumentation, first prove whether detection is root/jailbreak, Frida artifacts, debugger/ptrace, emulator/device identity, package integrity, or timing.

## Current Frida Notes

- Frida 17 moved the Java runtime bridge out of GumJS; TypeScript/compiled agents may need `frida-java-bridge` as an npm dependency when bundling Java APIs.
- Keep Frida tools and remote `frida-server`/Gadget versions aligned. Mismatches are a common source of attach and protocol failures.
- `retval` in `Interceptor.onLeave()` is recycled; do not store it for later use. Convert or copy values inside the callback.
- Strings allocated with `Memory.allocUtf8String()`/UTF-16 helpers must be kept alive as long as the target may use them.

## References

Read `references/frida-sources.md` when the task needs current docs, version checks, or source attribution.
