---
name: node-native-build
description: Diagnose npm and Node installs that fail on Termux (node-gyp errors such as android_ndk_path, missing compilers, packages with no android binary, optional platform dependencies, out-of-memory builds) and pick the smallest fix, including WASM fallbacks. Use when npm install, yarn, pnpm, or node-gyp fails, or a package reports an unsupported platform android. Do NOT use for Python builds (see python-native-build) or for JavaScript logic errors.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "medium"
  triggers: "npm install failed,node-gyp,android_ndk_path,unsupported platform android,gyp err,cannot find module native,npm build error,javascript package compile,native addon,npm native module"
---
# Node Native Build

## Purpose
Tell apart a missing toolchain, a node-gyp configuration problem, and a package that simply ships no binary for Android, then apply the smallest fix.

## When to use
- `npm install`, `yarn`, or `pnpm` fails while compiling or fetching a native addon.
- `gyp ERR!`, `Undefined variable android_ndk_path`, or `Unsupported platform: android`.
- `Cannot find module '@scope/pkg-android-arm64'` or a similar optional dependency error.

## When NOT to use
- Python packages: `python-native-build`.
- Failures in your own JavaScript.
- `pkg` errors before npm ran: `package-troubleshooting`.

## Preconditions
Run `sh scripts/check-node-toolchain.sh`. Capture the first `gyp ERR!` or build error, the package and version, and whether `process.platform` reports `android` (it does on Termux Node).

## Decision tree
1. The platform string is `android`, not `linux`. Packages that choose binaries by `os` and `cpu` may have no matching optional dependency.
2. `Undefined variable android_ndk_path in binding.gyp`: node-gyp needs the variable defined. The common fix is a user include file at `~/.gyp/include.gypi` containing `{'variables': {'android_ndk_path': ''}}`. Creating it is a confirmed change. A per-shell alternative is `export GYP_DEFINES="android_ndk_path=''"`. Cause: Termux's Node reports its OS as android, so node-gyp enables NDK-only branches; upstream node-gyp is addressing it, so a newer node-gyp may not need the workaround.
3. Missing compiler: node-gyp needs `python`, `make`, and `clang` (and `pkg-config` for some addons) from Termux packages.
4. `No module named 'distutils'` on newer Python: use a node-gyp version that no longer needs it instead of patching Python.
5. No Android binary exists for a package: prefer its WASM build when one exists (for example the `-wasm` variants some bundlers and image tools publish), a Termux-packaged equivalent, or proot with glibc. Do not fake the platform.
6. A build that dies with `Killed`: lower parallelism and memory pressure (see `background-processes`), and raise `NODE_OPTIONS=--max-old-space-size` only within real device RAM.
7. `--ignore-scripts` can confirm that a postinstall step is the failing part, but it leaves the addon unbuilt; say so and do not present it as the fix.
8. Tools that hard-code `/tmp` fail; Termux uses `$TMPDIR`.

## Example
- Situation: npm install fails with Undefined variable android_ndk_path in binding.gyp.
- Without the skill: Fakes the platform string or moves the whole project into proot.
- With the skill: Confirms `python`, `make`, and `clang` are present, applies the documented fix for the missing variable after confirmation, re-runs the install, and verifies with a `require`.

## Safety
Installing packages, creating `~/.gyp/include.gypi`, and global npm installs change the environment: state the exact change and confirm. Do not run install scripts from packages the user did not choose.

## Verification
Re-run the original install, then `node -e "require('<package>')"` and `npm ls <package>`.

## Rollback
Delete only files created for this attempt (for example `~/.gyp/include.gypi`) and `npm uninstall` only packages added for it.

## Handoffs
- `termux-environment` for architecture and Android level.
- `package-troubleshooting` when installing the toolchain fails.
- `background-processes` when builds are killed.
- `proot-boundaries` when a glibc-only binary is required.
- `python-native-build` when the failing step is a Python dependency of node-gyp.

## Report
The first real error, whether it is toolchain, gyp configuration, or missing Android binary, the change applied, and the import check result.
