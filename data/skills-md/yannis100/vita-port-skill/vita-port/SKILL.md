---
name: vita-port
description: Port games and game engines to the Sony PS Vita (PSVita / PS TV) as VPK homebrew using VitaSDK, vdpm, vitaGL, SDL2 and GXM. Use this whenever the user mentions PS Vita, PSVita, Vita homebrew, VPK, VitaSDK, vitaGL, HENkaku, Vita3K, ux0:data, or asks to "port X to Vita" or get a game or engine running on a Cortex-A9 ARM handheld, even if they do not name the tools. Covers feasibility triage, CMake and toolchain setup, heap/stack/memory budget, OpenGL to vitaGL, input mapping, LiveArea packaging, debugging crashes, profiling and measuring performance claims, automating a build/deploy/screenshot loop on a real console (vita-agent-use, psp2-tooling, vitacompanion), and release conventions.
---

# Porting a game to the PS Vita

A Vita port is mostly three jobs: make the code build for 32-bit ARM with newlib, give it a
platform layer that fits the Vita's memory, GPU and controls, and package it as a VPK that
installs and starts. Most failures come from the second job (memory budget, shaders), so the
workflow below front-loads the checks that catch those early.

## Ground rules

- **Legal scope.** Port only code the user has the right to build (open source, or their own).
  The VPK must never contain commercial game data or Sony modules such as `libshacccg.suprx`.
  End users copy their own assets to `ux0:data/<app>/`. If the request is to port a closed-source
  commercial game by redistributing its assets, say so and stop; offering an engine
  re-implementation that reads the user's own files is fine.
- **Facts age.** The reference files were written in 2026-10 against VitaSDK series 2026.08 and
  vitaGL at commit `cdbba42` (re-checked at `a85cb8d`, 2026-10-13). Run `vdpm status` and check
  the repo before trusting a flag name. `references/vitagl.md` lists names that older tutorials
  and ports use but that no longer exist.
- **State assumptions about the user's files instead of asserting them.** Unless you have read the
  file, say "assuming your copy is version X (check with ...)" for the game version, build, jar hash,
  data format or install path. A port that validates inputs fails on a mismatch the user was told
  could not happen.
- **Say what you did not verify.** You can usually build a VPK here, but you cannot run it on
  hardware. Items tagged *(unverified)* in the references need an on-device test. Tell the user
  which claims in your report are build-verified and which are untested on a Vita.
- **Measure before you claim, and state the condition in full.** An aggregate of a criterion you
  have not fully written down is fiction, and a screenshot filename is an expectation, not evidence.
  `references/measurement.md` has the twelve ways this went wrong on a real port, plus what an emulator
  can and cannot resolve. Read it before optimising or before writing a performance claim.

## Workflow

Do the steps in order. Each ends with something checkable.

### 1. Triage: is it feasible, and which kind of port?

Search first — there is no single authoritative Vita-port masterlist, so cast a wide net: GitHub topic
search (`topic:psvita-homebrew`, `topic:vitasdk`) and plain `"<game> vita"` / `"<game> psvita"` searches,
plus r/vitahacks and r/vitapiracy release threads (Reddit's JSON API is bot-blocked; use pullpush.io /
arctic-shift archives or web search). VitaDB (`vitadb.rinnegatamante.it`) is a JS SPA, not
curl-harvestable — check it in a browser. A port or a matching engine may already exist, and forking beats
starting over.

**Seek a portable codebase before porting.** The original project may be written in a language with no Vita
runtime (Dart/Flutter, Kotlin, Java, C#, Electron), or be closed source with only a decomp/recomp route.
Before committing to a from-scratch port or a VM/AOT workaround, search for an existing **C/C++ or
platform-agnostic reimplementation** of the same project: translations of the save/format logic, forks with a
core separated from UI, GPL engine rewrites, or decomp/recomp trees. Model: **PKSM (FlagBrew)** — a Pokémon
save manager whose save logic lives in a portable `core/` (PKSM-Core) plus a shared `common/` layer, with only
the 3DS front-end (`3ds/`) platform-specific and host-run tests that build with no console SDK. It is 3DS-only
in-tree, yet its structure is the template for "portable core, replaceable UI": a Vita front-end can sit on the
same core, and a Java/Kotlin-only app with a C++ format core is ported by finding that core, not by abandoning
the request. Fork beats starting over — the same rule as for existing Vita ports, applied one level down: fork
the portable core, write the UIs you need.

Then read the source with the audit script:

```bash
python3 ~/.claude/skills/vita-port/scripts/audit_source.py <source-dir>
```

It flags code that does not map to the Vita (fork, mmap, dlopen, x86 intrinsics, GL 3+ features,
64-bit assumptions) and prints the usual remedy. Pick the port type from `references/port-types.md`:

| Situation | Route |
|---|---|
| C/C++ source, SDL2, 2D or software rendering | stock `sdl2` package, SDL_Renderer on GXM |
| C/C++ source, OpenGL 1.x / 2.x / GLES2 | vitaGL (directly, or `sdl2_vitagl`) |
| 3DS/Citro3D code (e.g., MKW-3DS) | API emulation layer (`libctru`/`citro3d` reimplementation on Vita) → vitaGL; see `references/port-types.md` section 6 and [mkwiita](https://github.com/boomannotjeff/mkwiita) |
| Engine reimplementation (data files supplied by user) | check for an upstream Vita backend first |
| Decompilation or custom renderer (e.g. Direct3D 8) | write a GXM backend |
| Closed-source game with a recomp/decomp route (N64, x86 PC, PS1, PS2 lifts) | static recompilation → C, then native ARM build; see references/static-recomp.md |
| Android game with an ARMv7 `.so` (non-NDK, has JNI_OnLoad entrypoint) | so-loader boilerplate (`soloader-boilerplate`), FalsoJNI; see references/so-loader.md section 2 |
| Android NDK game (`ANativeActivity_onCreate` present) | so-loader boilerplate with `NDK_PORT=ON`, FalsoNDK submodule; see references/so-loader.md section 2 |
| Game written for a runner (Lua, GameMaker, Godot 3) | port or reuse the runner, not the game |
| Java / libGDX game (GL 2.0 class) | ahead-of-time translation: TeaVM C backend (Vita precedent) or Clearwing VM (real threads, GPL); compare them in the plan; see `references/java-teavm.md` |

**Set expectations about "port any game".** Community guides circulate claims that any game can be
ported with the right tooling. Tooling is not the limit; the console is. A port is feasible when the
code maps to a 32-bit ARM CPU with no 64-bit assumptions, a fixed 960x544 framebuffer, ~256 MiB (365
with `ATTRIBUTE2=12`), no compute or tessellation, and no JIT that only emits x86. Modern renderer
features, large working sets, and 64-bit-only engines are architectural mismatches, not packaging
problems — no amount of automation changes that. Say which category the user's game falls into early,
and prefer "this needs a reimplementation of X" over an open-ended effort estimate.

Decline or scope down, and say why, when the game needs: GL 3.3+ core / geometry / compute shaders,
64-bit-only code, a JIT that only emits x86 (ARM JITs work; `references/runtime.md` section 4b), Unity IL2CPP, Java whose core needs what TeaVM and vitaGL lack (runtime
class loading, AWT/ImageIO, `Gdx.gl30` / GLSL 330; see the limitations table in `references/java-teavm.md`
section 2), or more than roughly 365 MiB of RAM.

**Closed-source commercial games** (Steam titles, Unity games): do not start building. Search for an
existing community port first (VitaDB, GitHub, GameBrew); some exist and are distributed as patches the
user applies to their own copy (Hollow Knight Vita is the model; see `references/port-types.md`
section 7), or as a local build pipeline run on the user's own files (STSPSVITA for Java/libGDX;
`references/java-teavm.md`). If one exists, point the user to it, state that you have not tested it, and list its stated
requirements. If none exists, say so only after searching, explain what a from-scratch port would take,
and offer alternatives. Never fabricate a placeholder VPK and call it the game.

### 2. Toolchain

```bash
bash ~/.claude/skills/vita-port/scripts/check_env.sh
```

It reports whether `VITASDK`, `arm-vita-eabi-gcc`, `vdpm`, `cmake` and the common packages are
present, and prints the install commands that are missing. Install details and package names are in
`references/toolchain.md`. If no SDK can be installed, still write the CMake and platform layer, and
tell the user the build was not run.

### 3. Build skeleton that produces a VPK

Start from `assets/CMakeLists.vita.txt` (guarded by `if(VITA)` so the desktop build still works)
and generate placeholder LiveArea images so the first VPK installs:

```bash
python3 ~/.claude/skills/vita-port/scripts/make_placeholder_assets.py <project>/sce_sys
```

Get a trivial window or clear-screen program through `cmake --build` and `check_vpk.py` before
touching the game's code. A skeleton that links proves the toolchain, title ID and stubs are right,
which makes later errors attributable to the port.

### 4. Dependencies

Prefer `vdpm install <pkg>`; package names are case-sensitive. If a library is missing, write a
`VITABUILD` or cross-compile with `--host=arm-vita-eabi` and `-DCMAKE_TOOLCHAIN_FILE=...`
(recipes in `references/toolchain.md`). Static libraries only. GCC 15 defaults to a newer C
standard, so pass `-std=gnu11` for older C code.

### 5. Platform layer

Keep Vita code behind `#ifdef __vita__` (or a `vita/` directory) so upstream merges stay easy. Copy
`assets/vita_runtime.c` into the project: it sets the newlib heap, the main-thread stack and the clocks,
and it ships `vita_pin_thread_to_core()` for threads you do want pinned. Those are the settings ports
most often forget.

Then decide thread placement deliberately rather than inheriting it. That asset pins nothing by itself,
and neither does most ported code: a port that never calls `sceKernelChangeThreadCpuAffinityMask` still
reaches all three user cores (mask `_ALL` = `0x70000`), but by accident of the scheduler, and it cannot
answer "which core is the render thread on". A Vita is a quad-core Cortex-A9 and a game may use **three**
cores. Copy `assets/cpu_placement.{hpp,cpp}` for the deliberate version: a thread census (free, leave it
on), runtime-toggled pinning (no plugin), and a 4th-core probe that TESTS for CapUnlocker by asking and
reading the mask back instead of assuming. `references/runtime.md` section 5c has the measured return
codes; the same file has the other numbers (memory budget, threads, files, input, audio).

**Memory budget.** The newlib heap, `sceLibcHeapSize`, thread stacks, vitaGL's RAM pool, and any
`sceKernelAllocMemBlock` arenas all count against the MAIN budget (256 MiB default, up to 365 MiB
with `ATTRIBUTE2=12`). See `references/runtime.md` section 2.

**Float-Point Contract.** When the game uses physics, replay, or deterministic simulation, add to compiler flags:
```
-ffp-contract=off  # Prevent fused multiply-add (FMA), keeping IEEE single-precision bit-for-bit
```
Some games rely on platform-specific memory being zeroed. Two complementary strategies:
1. Compiler: `-ftrivial-auto-var-init=zero` (GCC 13+, zero-initializes automatics)
2. Runtime: overload `operator new` to return `calloc` memory (C++)

Reference: [mkwiita's zeroed_new.cpp](https://github.com/boomannotjeff/mkwiita/blob/master/platform/vita/src/zeroed_new.cpp)

**First boot.** Trace the no-arguments, empty-config start path before the first test: on a Vita nothing
passes `--rom`-style flags and the desktop UI that asks for the data file is usually stubbed, which
shows as a blank screen. Probe `ux0:data/<name>/` for the user's files (only formats your reader
supports) and say on screen when they are missing.

Typical replacements: window and input (dual sticks, no L2/R2/L3/R3, front and rear touch, gyro),
data paths (`app0:` is read-only, write to `ux0:data/<name>/`), audio (48 kHz S16), networking
(load `SCE_SYSMODULE_NET`), threads (3 user cores), timing.

### 6. Graphics

- SDL2 2D: nothing special beyond the 960x544 target.
- GL: follow `references/vitagl.md`. Rewrite GLSL 3.x to ES 1.00 style, bind attribute locations
  before link, size the memory pools, and document that users need `libshacccg.suprx` in
  `ur0:data/`.
- Custom GXM backend: see the Halo CE pattern in `references/port-types.md`.

### 7. Package and check

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build
python3 ~/.claude/skills/vita-port/scripts/check_vpk.py build/<name>.vpk
```

`check_vpk.py` verifies the title ID (exactly 9 characters), version format, the eboot's SELF
header, and LiveArea file presence, sizes and indexed-colour PNG type. These are the causes of most
"installs but bubble is missing" and `0x8010113D` errors.

### 8. Test, debug and measure

Vita3K can run a VPK for a first look, but it hides memory-budget and permission problems and does
not run plugin-dependent builds, so a Vita3K pass is not proof. It also **cannot resolve a 1-2 ms
timing change** — its noise is far larger — so use it for structure (pixel assertions, draw counts,
state transitions) and take time to hardware.

On hardware, the loop is: deploy → launch → **see the screen** → read logs → measure → fix. Two
community tools make that loop tight, and both are **firmware 3.65 only**:

- **`vita-agent-use`** gives an agent screenshots, timed button/stick/touch input, VPK deploy, launched
  apps and pushed crash/log events — so the agent can drive the game to a screen, look at it, and
  iterate without a human touching the console.
- **`psp2-tooling`** gives real profiling and debugger access: per-core CPU profiles with call stacks,
  GPU Razor metrics and frame captures, hardware breakpoints, and core dumps on demand. It needs Sony
  DevKit `os0:kd` modules the user must obtain themselves (never redistribute them).

Both are optional. Without them, use vitacompanion (FTP 1337, commands 1338) plus a log file and a
heartbeat the app writes itself. `references/agent-loop.md` covers the setup, the safety model, the
operating rules that freeze a console if skipped, and the fallback; `references/measurement.md`
covers turning what you see into a number you can trust.

**Vita3K caveat (community report):** some ports do not run under Vita3K at all (e.g. the gunbro port), even
when there are no Vita3K/PSV gaps for the game. A Vita3K pass is a convenience, never proof. For games that
won't start under Vita3K, plan hardware-only validation (vitacompanion + vita-parse-core) from the start.

### 9. Hand-off

Deliver the VPK build instructions plus a README with an end-user section (exact `ux0:data/<name>/`
layout, required modules, where users get legal data) and a developer section (build commands,
dependencies). Credit upstream projects and keep licences: GPL engines stay GPL, vitaShaRK is
LGPL-3.0. Use a unique 9-character title ID of the form `XXXXYYYYY`.

## Reference files

| File | Read it when |
|---|---|
| `references/toolchain.md` | installing VitaSDK, writing CMake or Makefile builds, cross-compiling deps, packaging tools, reviving an old port on the current SDK |
| `references/runtime.md` | choosing heap, stack, memory blocks, `ATTRIBUTE2`, JIT memory, kubridge (versions, firmware limits), clocks and frame pacing, threads, paths and launch params, input (incl. PS TV pads), audio, hardware limits |
| `references/vitagl.md` | the game uses OpenGL, GLES or shaders; vitaGL init, flags, limits, renamed APIs, GXP binaries, shader speed, SDL options |
| `references/port-types.md` | picking the route; reference repos; so-loaders (see `references/so-loader.md`), runners; the decompilation / direct-GXM example; cross-platform API emulation (libctru on Vita, TEV→GLSL, software DSP) |
| `references/so-loader.md` | Android .so loader architecture, symbol resolution, hooking, FalsoJNI/FalsoNDK, shader caching, debugging |
| `references/api-emulation.md` | cross-platform API emulation (libctru on Vita, TEV→GLSL, software DSP) |
| `references/java-teavm.md` | the game is Java / libGDX: TeaVM C backend, classlib gaps, runtime patches, memory split, local-build legal model |
| `references/debugging.md` | install errors, boot crashes, black screens, link errors, crash dumps, tools |
| `references/agent-loop.md` | automating the build→deploy→see→measure→fix loop on a real console (vita-agent-use, psp2-tooling, vitacompanion fallback) |
| `references/measurement.md` | before optimising or claiming a gain: what an emulator can resolve, how to instrument, how to read a screenshot numerically, how to report what you measured |
| `assets/cpu_placement.{hpp,cpp}` | you want a thread census, CPU pinning, or to know whether the 4th core (CapUnlocker) is available; see `references/runtime.md` section 5c |
| `scripts/vita_hot_order.py` | code is slow and you want a build-level win with no source change: turns a CPU profile into a linker fragment that puts the hottest functions at the start of `.text` (see `references/toolchain.md` section 3c) |

## Final report checklist

When you finish, state: which port route you chose and why; what was built (and with which SDK
version) versus only written; what was never run on a console; the memory settings you chose and
their basis; and what the end user must supply (assets, `libshacccg.suprx`, plugins with the
minimum version and supported firmware, e.g. kubridge v0.3.1_hotfix on 3.60/3.65 for `MemProtect`).

If you touched threads, also state which core each thread is meant to run on, whether that is
merely intended or actually applied, and whether the placement was measured. "It uses all the cores"
is not an answer; the census line and the chosen mask are.
