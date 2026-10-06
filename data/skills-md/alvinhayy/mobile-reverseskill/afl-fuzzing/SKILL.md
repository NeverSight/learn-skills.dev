---
name: afl-fuzzing
description: Greybox fuzz Android native libraries (.so) on-device with AFL++ — cross-compile the fuzzer for Android arm64, harness a JNI parser with a stub JNIEnv, detect memory bugs with ASan/libdislocator, and validate the harness actually reaches the target.
category: mobile-security
author: alvinhayy
license: MIT
tags: [android, fuzzing, aflplusplus, frida, ndk, reverse-engineering, native]
---

# afl-fuzzing — Android native-library fuzzing with AFL++

Fuzz the C/C++ parsers bundled inside an Android app (barcode/QR recognizers, image
decoders, protocol handlers) — the classic memory-corruption attack surface reachable from
untrusted external input. Everything runs **offline on a local emulator/device**; nothing is
sent to any backend.

## When to use

- You have an APK (often a Flutter/native app) with interesting native `.so` files and want to
  find memory-safety bugs (OOB, UAF) in a parser that processes attacker-influenced data.
- You need a **coverage-oriented** campaign, not blind mutation, against a closed-source lib.

## Key facts that shape the approach

- The `.so` are **Android bionic ELF** — they cannot `dlopen` on a macOS/glibc host. **The
  fuzzer runs on the device/emulator.**
- Closed-source libs have no compile-time instrumentation → coverage needs **binary-only**
  instrumentation (AFL++ **frida-mode**) or you run **dumb mode** as a baseline.
- JNI functions expect a `JNIEnv*` and Java objects. You call them from a harness with a
  **stub `JNIEnv`** (a function-pointer table) instead of spinning up a JVM.

## Workflow

### 1. Build `afl-fuzz` for Android arm64 (runs on the emulator)
```bash
export NDK=$HOME/Library/Android/sdk/ndk/<version>
export CC=$NDK/toolchains/llvm/prebuilt/darwin-x86_64/bin/aarch64-linux-android36-clang
git clone --depth 1 https://github.com/AFLplusplus/AFLplusplus
( cd AFLplusplus && make afl-fuzz CC="$CC" NO_PYTHON=1 )   # produces an Android arm64 ELF
adb push AFLplusplus/afl-fuzz /data/local/tmp/afl-fuzz && adb shell chmod 755 /data/local/tmp/afl-fuzz
```

### 2. Find the target function's real signature — from the binary, not guesses
Many Java classes are absent from `classes.dex` (Flutter apps). Disassemble the `.so`:
```bash
llvm-objdump -d --disassemble-symbols=<Java_...symbol> lib<target>.so
```
Read which args are direct `ByteBuffer`s: the code calls `JNIEnv->GetDirectBufferAddress`
(vtable **index 230**, offset `0x730`; `index = offset / 8`). `GetByteArrayElements` = 184
(`0x5c0`), `GetArrayLength` = 171 (`0x558`).

### 3. Write a harness with a stub `JNIEnv`
Build a 300+ entry function-pointer table; wire only the JNI methods the target calls
(`GetDirectBufferAddress` → your fuzzed buffer; other slots → a benign zeroed-scratch stub so
rarely-reached paths don't NULL-deref). Call the **real exported JNI function**. See
[`harness/barhopper_harness.c`](harness/barhopper_harness.c) for a complete worked example
against Google ML Kit's `libbarhopper_v3.so` barcode/QR recognizer.

**Control false positives:** fix width/height, allocate the input buffer at exactly its
declared size, and preload **`libdislocator`** so an out-of-bounds access hits a guard page
and becomes SIGSEGV — a *real* bug at valid geometry, not a harness artifact.

### 4. Detect bugs
- Harnesses you compile yourself: build with `-fsanitize=address` (the emulator ships
  `libclang_rt.asan-aarch64-android.so`), set `ASAN_OPTIONS=abort_on_error=1`.
- Closed-source target: `AFL_PRELOAD=/data/local/tmp/libdislocator.so` page-guards allocations.

### 5. Run the campaign
Open AFL in its own terminal tab so the **live AFL status screen** is visible while you keep
monitoring the structured stats (see [`run-in-tab.sh`](../../scripts/run-in-tab.sh)):
```bash
# live TUI in a new tab (keep AFL_NO_UI OFF); mirrored to ~/.mre-runs/fuzz-*.log
LOG=$(scripts/run-in-tab.sh fuzz "adb shell 'cd /data/local/tmp/bh; LD_LIBRARY_PATH=. \
  AFL_PRELOAD=./libdislocator.so AFL_SKIP_BIN_CHECK=1 AFL_SKIP_CPUFREQ=1 \
  AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1 timeout 3600 \
  ./afl-fuzz -n -m none -t 1500 -i seeds -o out -- ./harness @@'")
# monitor from anywhere (clean stats, not the ANSI TUI):
adb shell 'tail -1 /data/local/tmp/bh/out/plot_data'   # total_execs, saved_crashes, ...
# headless alternative:
adb shell 'nohup sh /data/local/tmp/run_target.sh 3600 >/data/local/tmp/nohup.log 2>&1 &'
```

## ⚠ Validate the harness — the most important step

A harness that never reaches the decoder reports "0 crashes" and lies. **Always run a
positive control:**
- **Poison-pointer probe:** make `GetDirectBufferAddress` return `0x1`. If the target reads
  the buffer it crashes instantly; if it returns cleanly, **your harness isn't exercising the
  parser** and the negative result is meaningless.
- **Under-allocation:** shrink the real buffer while claiming full size — a real read past it
  must fault.

Real lesson from this skill's development: a barcode harness returned 0 crashes over thousands
of execs — the poison probe proved `recognizeBufferNative` never read the image, because
`createNative()` enabled *no* barcode formats. The fix was `createNativeWithClientOptions` with
an options proto. **Trust a negative only after a positive control passes.**

## Coverage upgrade (dumb → greybox)

Dumb mode (`-n`) finds only shallow bugs. For real coverage use **AFL++ frida-mode**
(`afl-frida-trace.so`). Its build targets a **Linux** host, so build it inside an **arm64
Linux container** (e.g. Colima) with the Linux NDK — it can't cross-build from macOS (it picks
the host `clang -target arm64-apple-macos`). Then `afl-fuzz -O -- ./harness @@`.
Ref: https://blog.quarkslab.com/android-greybox-fuzzing-with-afl-frida-mode.html

## Assets

- [`harness/barhopper_harness.c`](harness/barhopper_harness.c) — stub-JNIEnv harness (with
  compile-time `POISON_PTR` / `REALALLOC` / `CLAIM_W` knobs for positive controls).
- [`harness/demo_parse.c`](harness/demo_parse.c) — planted-bug harness to validate the pipeline.
- [`scripts/rebuild.sh`](scripts/rebuild.sh), [`scripts/run_barhopper.sh`](scripts/run_barhopper.sh),
  [`scripts/run_demo.sh`](scripts/run_demo.sh).
- [`README.md`](README.md) — full method writeup with the validation correction.

## Credits

Builds on [AFL++](https://github.com/AFLplusplus/AFLplusplus) and the Trail of Bits
[`aflpp`](https://github.com/trailofbits/skills) testing-handbook skill (AGPL-3.0). AFL++
itself is AGPL-3.0 — this skill's original harnesses/scripts/docs are MIT.
