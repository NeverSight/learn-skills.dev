---
name: rea-performance-crash-triage
description: Authorized crash dump forensics (Windows Minidump .dmp, Linux core, macOS .ips), dynamic runtime instrumentation (Frida, GDB, Rizin Debug), and CPU/memory performance profiling (Flameox flamegraphs) using REA MCP.
---

# REA Crash Forensics, Runtime Instrumentation & Performance Profiling Skill

## Scope & Authorization
Covers all first-party crash dump analysis, live runtime debugging, Frida hooking, and CPU/memory performance optimization tasks (including Category 9 of the 500+ REA Prompt Vault and any custom debugging/profiling request).

## Execution Pipeline
1. **Crash Dump & Exception Forensics:**
   - Use REA MCP tools: `inspect_recorded_crash`, `open_binary`, `resolve_containing_procedure`, `read_function_instructions`, and `inspect_address_context`.
   - Decode exception codes (`0xC0000005` Access Violation, `SIGSEGV`, heap corruption, stack overflow), unwind stack frames, map faulting instruction pointers (`RIP`/`EIP`/`PC`) to decompiled functions, and produce a root-cause fix.
2. **Dynamic Runtime Instrumentation (Frida / GDB / Rizin):**
   - Use REA MCP tools: `list_frida_devices`, `list_frida_processes`, `start_frida_session`, `instrument_with_frida`, `observe_native_calls`, `start_gdb_session`, `gdb_console`, `start_rizin_debug_session`, `rizin_debug_command`, `capture_process_scenario`, and `correlate_static_and_runtime`.
   - Trace live API calls, argument values, return buffers, and UI event dispatch (`observe_native_ui`, `trace_native_ui_action`).
3. **Performance Profiling & Bottleneck Elimination:**
   - Profile hot call paths using `flameox` flamegraphs and REA call graphs (`get_call_graph`).
   - Refactor O(N^2) loops, UI thread blocking calls, and heap contention into verified, zero-skeleton optimized implementations with benchmark tests.
