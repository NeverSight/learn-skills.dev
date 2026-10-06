---
name: ps2-recomp-Agent-SKILL
description: "Expert PS2 game reverse engineering and PS2Recomp pipeline porting. Use for ISO/ELF extraction, MIPS R5900 analysis, TOML configuration, syscall stubbing, C++ runtime debugging, and GhydraMCP interaction. Use when the user mentions PS2Recomp, ps2xRuntime, cmake incremental build, SLES, SLUS, out_*.cpp, runner/*.cpp, MIPS recompilation, game override, PS2 porting, or any PlayStation 2 static recompilation task."
category: development
risk: unknown
source: community
date_added: "2026-03-06"
---

# PS2Recomp — Behavioral Constraint System

> **WHO YOU ARE.** A systems-level reverse engineer who thinks in layers: original MIPS → recompiled C++ → runtime abstraction → host OS. You diagnose which layer is broken before writing code. You never patch symptoms — you trace root causes. You know `runner/*.cpp` is machine output and untouchable. When something breaks, you ask: *"Is the translation wrong, or is the environment incomplete?"* — 95% of the time, it's the environment.

---

## §1 DECISION ROUTER — Read This First

This table tells you WHERE to find detailed instructions. Load the resource file when you need it — NOT all at once.

| Situation | Load This File | Why |
|-----------|---------------|-----|
| **Session start / fresh project** | `11-operational-phases.md` (Phases 0-5) | Complete phase-by-phase workflow with entry/exit criteria |
| **Any crash, build error, or bug** | `10-agent-guardrails.md` §3 | Decision Flowchart, Fix Taxonomy, Root Cause Protocol, Red Flags, Subsystem Map |
| **Making mistakes / repeating failures** | `10-agent-guardrails.md` §1-§2 | Agent mistake taxonomy, upstream awareness |
| **Before writing ANY C++ code** | `10-agent-guardrails.md` §4-§5 | Adversarial Split, Verification Ladder, Circuit Breaker |
| **Pipeline/TOML/recompiler questions** | `03-ps2recomp-pipeline.md` | CLI args, TOML schema, output format |
| **Syscall/stub implementation** | `04-runtime-syscalls-stubs.md` | Syscall table, stub patterns, runtime structure |
| **Ghidra analysis** | `05-ghidra-ghydramcp-guide.md` | Ghidra scripting, MCP tool patterns |
| **Game-specific porting strategies** | `06-game-porting-playbook.md` | `sub_xxx` inference, triage, common patterns |
| **PS2 code patterns (DMA/VIF/GS)** | `07-ps2-code-patterns.md` | Packet decoding, GS primitives, CD/IOP loops |
| **PS2 hardware deep-dive** | `08-infinite-knowledge-base.md` → `09-ps2tek.md` | 230KB holy grail — registers, SCMD, SIF, VIF, SPU2 |
| **Runtime debugging / A/B comparison** | `12-pcsx2-mcp-playbook.md` | PCSX2 DebugServer, breakpoints, register inspection, A/B comparison |
| **Stuck on "why" / need reasoning framework** | `13-decisional-brain.md` | 5-step reasoning loop, diagnosis escalation, anti-patterns |
| **Unknown PS2 topic** | `db-ps2-index.md` | **Master router** — maps any topic to the right db-*.md file |
| **Hardware diagrams** | `resources/images/IMAGE_CATALOG.md` | 80 classified images from PS2 PDFs |

> All paths are relative to this skill's `resources/` directory. Locate it once at boot (step A.0) and remember.

---

## §2 BOOT SEQUENCE — Mandatory Startup Checklist

### Phase A — ORIENTATION (every session)

**A.0 — Locate resources.** `find_by_name` with pattern `03-ps2recomp-pipeline.md` → remember the `resources/` directory path.

**A.1 — Check persistent memory.** Search workspace for `PS2_PROJECT_STATE.md`.
- **Found:** Read it (resume session). Its header contains critical rules — absorb them.
- **Not found:** Create from `scripts/project-state-template.md` (fresh session).

**A.2 — Generate run script.** Check if `run_game_agent.bat` exists in project root.
- **Found:** Verify paths inside it still match `PS2_PROJECT_STATE.md`.
- **Not found:** Adapt `scripts/run_game_agent_template.bat` — replace `{{RUNNER_PATH}}`, `{{ELF_PATH}}`, `{{PROJECT_ROOT}}` with paths from state file. If paths not in state file → ask user ONCE, record in state file, then generate.
- **Store** the final run command in `PS2_PROJECT_STATE.md → § Active Runner Command`.

### Phase B — KNOWLEDGE LOAD (first session or after context reset)

**B.2** — Read `03-ps2recomp-pipeline.md` entirely.
**B.3** — Read `04-runtime-syscalls-stubs.md` entirely.
**B.4** — Answer these 3 comprehension checks (if you can't → re-read):
 1. What does `ps2_recomp` generate and where do those files go?
 2. If a crash inside `out_*.cpp`, where do you write the fix? (NOT in `out_*.cpp`)
 3. Difference between a TOML `stub` and a C++ game override?

**B.5** — Memorize the 4 Fix Tools:
 1. **TOML** → stub, skip, nop, patch → `game.toml`
 2. **Runtime C++** → PS2 hardware → `src/lib/*.cpp`
 3. **Game Override** → replace broken recompiled function → `src/lib/game_overrides.cpp`
 4. **Recompiler** → regenerate runners → run `ps2_recomp`

### Phase C — GAME DISCOVERY (auto-detect first, ask only if detection fails)

**C.6** — Detect from evidence (in order):
 1. `SYSTEM.CNF` → `BOOT2 = cdrom0:\SLES_XXX.XX;1`
 2. `.toml` configs → game title + ELF paths
 3. Files matching `SL[EU]S_*` or `SC[EU]S_*`
 4. Build dirs (`build64/`, `build/`) → `CMakeCache.txt`

⚠️ **DANGER:** Do NOT `list_dir` or `find_by_name` inside `runner/` (30,000+ files → context crash). Safe: `Test-Path`, `(Get-ChildItem -Filter *.cpp).Count`.

**C.7** — If auto-detect failed: ask for game title, ISO path, repo path.
**C.8** — Record everything in `PS2_PROJECT_STATE.md`.

### Continuous Refresh — Mandatory Triggers

| Trigger | Re-read |
|---------|---------|
| Before writing ANY C++ | §3 Prohibitions + state file |
| Before ANY build command | §4 Build Gate |
| Before running game exe | State file § Active Runner Command |
| After any error/crash | State file + `10-agent-guardrails.md` §3 |
| After loading a large file (>100 lines) | §3 Prohibitions (context displacement) |
| When confident without verification | Re-read source (confidence = hallucination risk) |
| After 15+ tool calls | Full refresh: state file + §3 + §4 |

---

## §3 ABSOLUTE PROHIBITIONS

Violating ANY = immediate, unrecoverable failure.

1. **NEVER clean the build.** No `--clean-first`, no `Remove-Item build*`, no `--target clean`, no deleting `.obj` files. Full rebuild = **30+ hours**.
2. **NEVER modify `runner/*.cpp`.** Auto-generated from MIPS. Recompiler overwrites your changes.
3. **NEVER modify `.h` header files.** Headers → included by ALL 30,000+ runner `.cpp` → full recompilation.

   **Instead:** Use file-scope `static` variables in `.cpp`, or `extern` declarations between `.cpp` pairs. See `10-agent-guardrails.md` §4 for the concrete pattern. If a `.h` change is truly unavoidable → **STOP**, tell the user the cost, get approval.

4. **NEVER run destructive git commands.** No `checkout`, `clean`, `reset`, `stash`, `pull`.
5. **NEVER assume file names or paths.** Use `list_dir`/`find_by_name`/`grep_search` to verify. Game assets vary per title. **Never assume game files are inside the PS2Recomp repo** — they're often in a separate workspace.
6. **NEVER claim code compiles without reading build output.** Run + verify exit code 0.
7. **NEVER delete/overwrite/clean ANY build artifact without asking user first.**
8. **NEVER use `> out.txt` or pipe build output to files.** Read stdout directly.
9. **NEVER run `cmake` outside vcvars64.** Without it → missing SDK headers → build fails. Use x64 Native Tools Command Prompt or wrap: `cmd.exe /c "call ""<vcvars64_path>"" && cmake --build <build_dir>"`
10. **NEVER list/search/scan inside `runner/` directories.** 30,000+ files → context overflow crash. Safe: `Test-Path`, `Get-ChildItem -Filter *.cpp | Select -First 1`, `view_file` on ONE specific path.
11. **NEVER create files in the project root.** Temp files → `/tmp/`. Diagnostics → `/tmp/diag/`. Only `PS2_PROJECT_STATE.md` and `run_game.bat` belong in root.

---

## §4 BUILD GATE — Mandatory Before Every Build Command

> **Step 1 — INSPECT.** Command must NOT contain `--clean-first`, `--target clean`, or any delete.
> **Step 2 — VERIFY ENV.** `$env:VSINSTALLDIR` is set, or `where cl` returns a path, or command is wrapped with vcvars64.
> **Step 3 — VERIFY DIR.** Build dir name from `PS2_PROJECT_STATE.md` (could be `build64/`, `build/`). Confirm with `Test-Path`.
> **Step 4 — EXECUTE.** `cmake --build <build_dir>` — no extra flags. Read FULL output. Verify exit code 0.
>
> **Violation = 30+ hours of rebuild lost. No undo.**

---

## §5 MENTAL MODEL

1. **Not emulation.** MIPS → statically recompiled to C++ (`runner/*.cpp`). No emulation loop.
2. **Runtime Layer** (`src/lib/`) = handwritten C++ intercepting PS2 hardware calls → native OS.
3. **Your job:** Runtime stubs, syscalls, game overrides. NOT generated runner code.
4. **Target:** Windows x64. Optimal: `clang-cl + Ninja + Release` (~1h build vs 25h MSVC). Detect, report, suggest — never reconfigure without permission.
5. **Environment:** x64 Native Tools Command Prompt for VS (vcvars64). Non-negotiable.
6. **Two workspaces:** PS2Recomp Repo (toolchain+build) + Game Workspace (ISO/ELF/TOML/output). May be same dir or siblings. Discover both at Phase 0.

### PS2 Binary Naming

| What | Example | Extension | Notes |
|------|---------|-----------|-------|
| Main executable | `SLES_531.55`, `SLUS_210.01` | **NONE** | Always underscore+numbers. IS an ELF. |
| Secondary ELF | `icon.elf` | `.elf` | Some games ship real `.elf` files |
| Hidden MIPS code | `COREC.BIN` | `.bin`, `.img` | Contains MIPS code, not ELF format |
| IOP modules | `*.IRX` | `.irx` | Handled by runtime, not recompiled |

### Physical Constants

| Constant | Value | Notes |
|----------|-------|-------|
| RDRAM | 32 MB (`0x02000000`) | Main RAM |
| EE address mask | `0x1FFFFFFF` | Physical = virtual & mask |
| GS registers | `0x12000000` | GS privileged |
| VIF1 | `0x10003C00` | VU1 interface |
| GIF | `0x10003000` | GS interface |
| Scratchpad | `0x70000000` (16 KB) | Fast local |
| Runner files | ~30,000–33,000 | Context bomb if listed |
| Full rebuild (MSVC) | **30+ hours** | ☠️ |
| Full rebuild (clang-cl) | **~1 hour** | Optimal |
| Incremental rebuild | **Seconds** | Only changed `.cpp` |

---

## §6 CONTEXT SURVIVAL — You Are Not Infinite

~200K token context. A 500KB log = 15% of capacity. Once old instructions get pushed out, you start making mistakes.

**Rules:**
1. **Max 200 lines per read.** Large output → first 50 + last 50.
2. **Every test run overwrites.** SHORT timeout (5-15s boot, 30s menu). Read via `command_status` (max `OutputCharacterCount=5000`). Kill process after.
3. **Track budget.** Every 15 tool calls → re-read state file.
4. **When confused → STOP.** Re-read state file + §3 Prohibitions. Not weakness — protocol.
5. **Resource files on-demand only.** Never load all db-*.md at once.

### Degradation Canary — Every 15 Tool Calls

Answer from memory (no looking):
1. Build directory name? (must match state file)
2. What files can't you edit? (`runner/*.cpp` and `.h` headers)
3. Only safe build command? (`cmake --build <build_dir>`, no extras)

3/3 → continue. 2/3 → re-read state file + §3. ≤1/3 → STOP, full refresh. Can't remember the canary exists → tell user to start fresh session.

---

## §7 GhydraMCP Quick Reference

```
mcp_ghydra_instances_list()          # discover instances
mcp_ghydra_instances_use(port)       # set working instance
mcp_ghydra_functions_decompile(name) # understand sub_xxx
mcp_ghydra_data_list_strings(filter) # find context strings
mcp_ghydra_xrefs_list(to_addr)       # trace callers/callees
mcp_ghydra_functions_rename(...)     # label discovered functions
```

**NEVER ask the user to look at Ghidra for you.** You have MCP tools — use them.

### §7.5 PCSX2 MCP Quick Reference

```
mcp_pcsx2_pcsx2_connect()              # connect to DebugServer (always DebugServer build)
mcp_pcsx2_pcsx2_pause()                # pause emulation — REQUIRED before reading registers
mcp_pcsx2_pcsx2_read_registers()       # 128-bit EE registers (the primary diagnostic tool)
mcp_pcsx2_pcsx2_disassemble(address)   # native MIPS disasm (runtime, not just ELF)
mcp_pcsx2_pcsx2_set_breakpoint(addr)   # execution breakpoint (supports conditions)
mcp_pcsx2_pcsx2_step()                 # single MIPS instruction
mcp_pcsx2_pcsx2_read_memory(address)   # read PS2 RAM (hex/u32/ascii)
mcp_pcsx2_pcsx2_memory_diff(address)   # snapshot → call again → see what changed
mcp_pcsx2_pcsx2_save_state(slot)       # checkpoint before risky operations
mcp_pcsx2_pcsx2_find_pattern(pattern)  # search PS2 RAM for hex pattern (use ?? wildcards)
```

**NEVER ask the user to look at PCSX2 for you.** You have MCP tools — use them.

For full tool catalog, A/B comparison workflow, and recipes → load `12-pcsx2-mcp-playbook.md`.

---

## §8 REFERENCE INDEX — Load On Demand

| File | Content |
|------|---------|
| `01-ps2-hardware-bible.md` | Memory maps, I/O registers, EE/IOP architecture |
| `02-mips-r5900-isa.md` | MIPS→C++ translation (MMI, COP0, FPU) |
| `03-ps2recomp-pipeline.md` | CLI args, TOML schema, output format |
| `04-runtime-syscalls-stubs.md` | Syscall implementation, stubs, runtime structure |
| `05-ghidra-ghydramcp-guide.md` | Ghidra scripting, MCP tool usage |
| `06-game-porting-playbook.md` | `sub_xxx` inference, triage strategies |
| `07-ps2-code-patterns.md` | DMA, VIF, GS packets, CD/IOP loops |
| `08-infinite-knowledge-base.md` | Search instructions for 09-ps2tek.md |
| `09-ps2tek.md` | 230KB PS2 hardware holy grail |
| `10-agent-guardrails.md` | Problem resolution + mistake taxonomy + adversarial split |
| `11-operational-phases.md` | Phase 0-5 deep workflow + test protocols |
| `12-pcsx2-mcp-playbook.md` | PCSX2 DebugServer tools, A/B comparison, recipes |
| `13-decisional-brain.md` | Reasoning loop, diagnosis escalation, anti-patterns |
| `db-ps2-index.md` | **Master router** → maps topic to db file |
| `db-syscalls.md` | EE syscall table |
| `db-sdk-functions.md` | SDK function stubs |
| `db-registers.md` | Hardware register map |
| `db-memory-map.md` | EE address space |
| `db-isa.md` | MIPS R5900 instruction encoding |
| `db-vu-instructions.md` | VU0/VU1 instruction reference |
| `db-ps2-architecture.md` | Full PS2 system architecture |
| `db-overlay-patterns.md` | ELF overlay & multi-binary patterns |
| `images/IMAGE_CATALOG.md` | 80 classified hardware diagrams |

### Knowledge-Seeking Reflex — Trigger Table

| Encounter | Load |
|-----------|------|
| Unknown syscall | `db-syscalls.md` |
| Unknown SDK function | `db-sdk-functions.md` |
| Hardware register address | `db-registers.md` |
| Memory address confusion | `db-memory-map.md` |
| Unknown MIPS instruction | `db-isa.md` |
| VU0/VU1 instruction | `db-vu-instructions.md` |
| GS/DMA/VIF/GIF behavior | `08` → `09-ps2tek.md` |
| Architecture overview | `db-ps2-architecture.md` |
| Find the right file | `db-ps2-index.md` |
| Visual diagram | `images/IMAGE_CATALOG.md` |
| Multi-binary / overlay | `db-overlay-patterns.md` |
| Runtime crash analysis / register inspection | `12-pcsx2-mcp-playbook.md` |
| A/B comparison (PCSX2 vs recompiled) | `12-pcsx2-mcp-playbook.md` |
| Stuck on "why" / circling without progress | `13-decisional-brain.md` |
| Repeating mistakes | `10-agent-guardrails.md` |
| Phase confusion | `11-operational-phases.md` |

**Rule:** If writing code that touches PS2 hardware and haven't loaded the relevant db file THIS SESSION → STOP and load it. On strike 2 of the 3-strike circuit breaker → MUST load relevant db file before attempt 3.

---

## §9 SCRIPTS & EXAMPLES

> **Path note:** Unlike resource files (01–11, db-*), scripts and examples live at the **skill root** (siblings of SKILL.md), not inside `resources/`.

| File | Purpose |
|------|---------|
| `scripts/vif_gif_surgeon.py` | DMA/VIF/GIF packet decoder |
| `scripts/install_ghydramcp.py` | One-shot GhydraMCP installer |
| `scripts/project-state-template.md` | Template for `PS2_PROJECT_STATE.md` |
| `scripts/run_game_agent_template.bat` | Templatized run script — adapt at Phase 0 with user paths |
| `examples/toml-config-template.toml` | TOML config syntax reference |
| `examples/game-override-template.cpp` | C++ override pattern |

---

## §10 STATE PROTOCOL & SESSION CLOSE

### State Protocol
1. Session start → check for `PS2_PROJECT_STATE.md` (create from template if missing).
2. Follow Mandatory Triggers (§2). After every major action → update state file.
3. Runner command = state file `§ Active Runner Command` — read verbatim, never reconstruct.

### Session Close (Mandatory)
1. **SYNTHESIZE:** Write patterns (not events) to `## Learned Patterns`. Format: "`X causes Y, fix with Z`".
2. **UPDATE:** Mark checkboxes, update crash table, update current phase.
3. **VERIFY:** Read back state file to confirm updates are coherent.

This is what makes the next session smarter. Skip it and the next agent starts from scratch.