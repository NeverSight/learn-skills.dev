---
name: vita-app-port
description: Port Android applications and non-game tools to the PS Vita (PSVita / PS TV) as VPK homebrew using the Android .so loader or native VitaSDK builds. Use when the user asks to port an Android app, utility, manager, emulator frontend, or CLI tool to Vita, HENkaku, Vita3K, or ux0:data.
---

# Porting an Android App or Tool to the PS Vita

This skill is the application companion to the `vita-port` skill. It ports **non-game apps**:
file managers, emulator frontends, dev tools, productivity and system utilities. Games stay in
`vita-port`. The two skills share the same repository, so the `vita-port` references (toolchain,
so-loader, debugging, packaging) are installed alongside and are reused here.

Most of the work is identical to a game port: same toolchain, same VPK packaging, same debug flow.
The differences are in triage, platform layer, and input. Those differences are documented here.

## Ground rules

- **Legal scope.** Port only apps the user has the right to build (open source, or their own).
  The VPK must never contain a commercial app's data or Sony modules such as `libshacccg.suprx`.
  End users copy their own data to `ux0:data/<app>/`.
- **State assumptions about the user's files instead of asserting them.** Unless you have read the
  file, say "assuming your copy is version X (check with ...)" for APK version, ABI, or data path.
- **Say what you did not verify.** You can build a VPK here, but you cannot run it on hardware.
  Tell the user which claims are build-verified and which are untested on a Vita.

## Workflow

Do the steps in order. Each ends with something checkable.

### 1. Triage: is it feasible, and which route?

**Search for a portable core before triaging by language.** The route can flip based on which codebase you
port. Before deciding "Java/Kotlin-only → not feasible" or "no native `.so` → stop", check whether a
platform-agnostic C/C++ reimplementation of the app's logic exists (forks, format-translation projects, apps
with a core submodule separated from their Android/JS UI). Model: **PKSM (FlagBrew)** — a save manager whose
`core/` (PKSM-Core) is pure portable C++ with no Android/3DS guards, whose shared `common/` layer adds only
UI- and net-agnostic logic, and whose platform code is a thin front-end (`3ds/`); its own test suite
(`tests/`) builds on a plain host g++ with no console SDK, proving the core is portable. If such a core
exists, port the core and write a Vita UI for it — that is a native-VitaSDK route, not a decline.

Check the APK's ABI and entry points first. Use the scripts from the `vita-port` skill:

```bash
python3 ~/.roo/skills/vita-port/scripts/audit_source.py <source-dir>
```

Pick the route from this table:

| Situation | Route |
|---|---|
| Android APK with an `armeabi-v7a` `.so` and no game-style graphics | .so loader (soloader-boilerplate), FalsoJNI; no GLES needed |
| Android APK with an `armeabi-v7a` `.so` that draws through GLES | .so loader + vitaGL; see references/so-loader.md |
| Open-source C/C++ app or CLI (Android, or Unix-like) | native VitaSDK build (stock SDK), SDL2 or plain console |
| Java/Kotlin-only app (no native `.so`) | not feasible: no Dalvik on Vita; say so and stop |
| `arm64-v8a`-only app | not feasible: Vita is ARMv7; say so and stop |
| Unity-based app (`libunity.so`) | decline: the same Unity constraint as games applies |

Decline or scope down, and say why, when the app needs: a Dalvik/JVM, 64-bit-only code, Google Play
Services (GMS), foreground services, or more than roughly 365 MiB of RAM.

### 2. Toolchain

- .so loader route: **VitaSDK-softfp** (Android `armeabi-v7a` is soft-float ABI); see
  `references/toolchain.md` in the `vita-port` skill.
- Native route: stock VitaSDK, `arm-vita-eabi-gcc`.

Verify with `check_env.sh` from the `vita-port` skill. If no SDK can be installed, still write the
build files and tell the user the build was not run.

### 3. Build skeleton that produces a VPK

Reuse the `vita-port` skill's skeleton: `assets/CMakeLists.vita.txt` guarded by `if(VITA)`, and
placeholder LiveArea images via `make_placeholder_assets.py`. Get a trivial window or hello-world
program through `cmake --build` and `check_vpk.py` before touching the app's code.

### 4. Platform layer for apps

The app-specific replacements, in `references/app-runtime.md`:

- No game loop, no 60 FPS target; vsync off is acceptable for tools. Screen can sleep after idle.
- Input: many apps are touch-only. Map 1920x1080 front-touch to 960x544. Back button = Android Back.
- No physical shoulder/Stick mapping is needed unless the app uses it.
- Text entry: use the Vita IME (`SceIme`) for dialogs and the on-screen keyboard (see app-runtime.md).
- Data paths: `app0:` is read-only; write to `ux0:data/<name>/`. Redirect Android paths
  (`/proc/cpuinfo`, `/dev/urandom`, `/sdcard/`) to `ux0:data/<name>/` equivalents.
- AAssetManager bridge: map `assets/<path>` to `ux0:data/<name>/assets/`.
- Networking: load `SCE_SYSMODULE_NET` and handle permissions (see app-runtime.md).
- No background services: Vita apps are foreground only. State this in the README.

### 5. Graphics (only if the app draws)

- SDL2 or plain software: nothing beyond the 960x544 target.
- GLES through the .so loader: follow `references/vitagl.md` (ES 1.00 dialect, bound attribute
  locations, memory pools, `libshacccg.suprx` note).

### 6. Package and check

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build
python3 ~/.roo/skills/vita-port/scripts/check_vpk.py build/<name>.vpk
```

Title ID exactly 9 characters, livear area present, indexed-colour PNGs. Same rules as games.

### 7. Test and debug

- Vita3K first look. Note the caveat from `vita-port`: some builds do not run under Vita3K at all;
  it is a convenience, never proof. On hardware use vitacompanion and `vita-parse-core`.
- App-specific errors: missing `kubridge` (error `0x80101051`), AAsset path not found, and IME or
  dialog crashes. See `references/so-loader.md` and `references/debugging.md` (vita-port skill).

### 8. Hand-off

Deliver build instructions plus a README with an end-user section (exact `ux0:data/<name>/`
layout, required modules like kubridge, where users get legal data) and a developer section (build
commands, dependencies). Credit upstream projects and keep licences. Use a unique 9-character title
ID of the form `XXXXYYYYY`.

## Reference files

| File | Read it when |
|---|---|
| `references/app-runtime.md` | app-specific platform layer: IME, dialogs, permissions, paths, input |
| `vita-port` skill `references/toolchain.md` | installing VitaSDK / VitaSDK-softfp, cross-compiling |
| `vita-port` skill `references/so-loader.md` | the .so loader route, symbol tables, kubridge |
| `vita-port` skill `references/debugging.md` | install errors, crash dumps, Vita3K vs hardware |
| `vita-port` skill `scripts/check_vpk.py` | VPK validation (title ID, SELF, LiveArea) |
