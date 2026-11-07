---
name: coop-reverse-engineer
description: Reverse engineer a game or its engine to learn how its scripts, netcode, saves and level loading work, using agent tools such as REA, GhidraMCP, ida-pro-mcp, Ghidra headless, Frida and engine dumpers.
---

# Reverse engineer the game for co-op

1. Prefer source: open source ports, decompilations, shipped script source, SDKs.
2. Script layer: find or write an archive reader, dump scripts to text, round-trip test any packer.
3. Native layer: ask the owner before installing tools. Options: REA (`npx rea-agents setup`, owner runs it, restart the agent), GhidraMCP, ida-pro-mcp, or Ghidra headless decompile-all to one `.c` file plus a function index.
4. Engine dumpers: UE4SS and Dumper-7 for Unreal 4/5, Il2CppDumper or Cpp2IL for IL2CPP Unity, dnSpyEx for Mono Unity.
5. Map for co-op: netcode (if any), where story and AI logic run, what is client-only (UI, cutscenes, dialog), save and level transitions, single-instance checks.
6. Record byte signatures for the exact build you analysed.
7. Keep dumps and decompiled code in `local/`. Publish findings, names, offsets and your own code only.

Details: `playbook/reverse-engineering.md`, `playbook/tools.md`.
