---
name: capstone-cross-platform
description: >-
  Guides Capstone cross-compiles and platform-specific CMake notes for Linux
  targets, Android NDK, Windows, and macOS. Use when cross-building Capstone,
  using cross_configs toolchain files, QEMU smoke tests, Android ABI builds,
  Windows MSVC/CMake, or macOS universal vs thin binaries.
---

# Capstone cross-platform builds

## Prefer CMake toolchains

Example configs live in `cross_configs/`, named
`<targetOS>_<targetMachine>_<hostOS>.cmake`.

```bash
cmake -DCMAKE_TOOLCHAIN_FILE=cross_configs/<file>.cmake \
  -DCAPSTONE_BUILD_STATIC_LIBS=ON -S . -B build
cmake --build build
```

Static ON here matches the `BUILDING.md` example; shared stays OFF by default
unless you enable it.

## Android

Use the NDK CMake toolchain (most reliable path in current docs):

```bash
cmake -B build \
  -DCMAKE_TOOLCHAIN_FILE=$NDK_PATH/build/cmake/android.toolchain.cmake \
  -DANDROID_NDK=$NDK_PATH \
  -DANDROID_ABI=arm64-v8a
cmake --build build
```

Legacy `./make.sh cross-android ...` is deprecated Make-only.

## Host platform notes

- **Windows**: `cmake.exe -B build` then `--build --config Release`. See also
  `windows/` for kernel memory helpers (not a full VS solution for the core).
- **macOS**: without `CAPSTONE_BUILD_MACOS_THIN=ON`, CMake sets
  `CMAKE_OSX_ARCHITECTURES` to `x86_64;arm64` (universal2), with `ARCHFLAGS`
  overrides for cibuildwheel-style builds.
- **QEMU**: after a cross build, run binaries with the sysroot prefix shown in
  `BUILDING.md` (example uses `qemu-s390x-static` and `cstool`).

## Agent rules

1. Point to an existing `cross_configs` file or Android/NDK docs; do not invent
   toolchain files.
2. Treat `COMPILE_MAKE.TXT` cross recipes (mingw, iOS make.sh, Android make.sh,
   Cygwin) as legacy only.
3. Do not claim Meson or a maintained `.travis.yml` cross matrix.

## More detail

- Config inventory and Windows/macOS edges: [reference.md](reference.md)
- Copy-paste commands: [examples.md](examples.md)
