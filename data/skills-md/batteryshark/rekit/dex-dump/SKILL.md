---
name: dex-dump
description: "Dump decrypted DEX and CompactDex images from a RUNNING Android app's memory with Rekit's clean-room Apache-2.0 device tool (ptrace on a rooted aarch64 device). Defeats class-loading packers by reading the image after the app decrypts it. Does not launch the app or execute a sample on the host. BYO rooted device + adb; build the device tool from the included Rust source."
---

# dex-dump — Android DEX Dumper

Dump decrypted DEX and CompactDex images from a **running** Android app's memory
using Rekit's original `dex-dumper` (ptrace attach on a rooted device).

## What it does

Android packers that encrypt/load DEX at runtime only materialize the *real* DEX in
memory after their class loader decrypts it — so the on-disk APK holds an encrypted
stub, not the real code. This skill pushes a device-side dumper, ptrace-attaches to
the already-running app, and reads the decrypted DEX out of memory.

**Does not execute a sample on the host.** Invasive only on the connected device.

## Prerequisites

- `adb` on PATH (Android Platform Tools).
- A **rooted aarch64** Android device connected via USB (`dex-dumper` uses `ptrace`;
  the runner verifies either `adb root` or a working `su -c`).
- A device binary built once with `bin/rekit install dex-dump`. Building requires
  Rust 1.74+, the `aarch64-linux-android` target, and Android NDK r25+; set
  `ANDROID_NDK_HOME` first.
- The target app must be **running and past its splash screen** — the packer must
  have decrypted the real DEX. Launch the app and navigate past any splash/loader
  before running.

## Usage

```bash
# explicit package
rekit run dex-dump com.example.app ./out

# auto-detect the foreground app
rekit run dex-dump auto ./out

# specific device serial (multiple devices connected)
rekit run dex-dump com.example.app ./out --device 1234567890abcdef
```

Result is a single JSON object on stdout: `{ok, package, pid, dexFiles, fileCount,
outputDir}`. Multiple DEX files are normal for packed apps — pull all of them.

## Notes

- `--keep-tool` leaves `rekit-dex-dumper` on the device (default cleans up both the
  tool and the dumped files after pulling).
- The runner never launches the target. If `pidof` returns empty, launch the app
  yourself and wait until its loader has decrypted the DEX.
- Pair the pulled DEX with your Android decompiler (jadx / dex2jar) and any class
  deobfuscation step.

## Source and license

The dependency-free Rust source, host tests, build instructions, and clean-room
provenance statement live in [`scripts/dex-dumper/`](scripts/dex-dumper/README.md).
The implementation and binaries built from it are licensed Apache-2.0 under Rekit's
root license. No panda-dex-dumper source or binary is included.
