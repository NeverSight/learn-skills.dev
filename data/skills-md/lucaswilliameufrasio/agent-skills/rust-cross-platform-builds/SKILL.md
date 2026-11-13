---
name: rust-cross-platform-builds
description: >-
  Speed up and harden Rust release builds for a different OS or CPU architecture.
  Use whenever an ARM64/container deployment spends a long time compiling Rust
  under QEMU, the user mentions Zig or cargo-zigbuild, a cross linker/sysroot,
  glibc compatibility, or asks for a build-time comparison—even if they only
  ask to make deployment faster.
---

# Fast, reliable Rust cross-platform builds

Cross-compile Rust on a development machine or CI runner that has suitable
resources, then package the finished artifact for the target platform. Zig with
`cargo-zigbuild` is a useful default for Linux GNU targets: it avoids running
Rust's compiler under CPU emulation, while still allowing Buildx to assemble the
target image. Preserve runtime behavior and prove the resulting binary works on
the actual target ABI.

## Inspect before changing the pipeline

1. Read the repository instructions, Cargo workspace/configuration, lockfile,
   current Dockerfile/build scripts, CI workflow, runtime image, and documented
   release command. Find which stage is slow before replacing it.
2. Identify the build host architecture, target triple, libc family and minimum
   runtime version, CPU/memory limits, and whether native dependencies are used.
   Look for dependencies such as OpenSSL, SQLite, compression libraries, or
   C/C++ build scripts; a Rust target alone does not cross-compile their native
   parts.
3. Preserve the project's feature flags, TLS behavior, linker settings, release
   profile, migrations, assets, and runtime contract. Treat changing OpenSSL to
   Rustls, static linking, or the minimum libc version as a separate design
   decision—not as an invisible build optimization.
4. For a consequential change spanning Cargo, Docker, and deployment, record the
   decision in the repository's existing ADR/design format before implementation.

## Choose and configure the cross-build

For Linux GNU targets, pin compatible Zig and `cargo-zigbuild` versions using
the repository's tool manager or CI setup, and install the Rust standard library
for the target. Prefer the repository's existing version-management conventions
over global, floating installs.

Map the requested platform to its Rust target triple, for example:

| Platform | Rust target |
| --- | --- |
| `linux/amd64` | `x86_64-unknown-linux-gnu` |
| `linux/arm64` | `aarch64-unknown-linux-gnu` |

Use the runtime's actual libc baseline, not an arbitrary value. `cargo-zigbuild`
accepts the GNU target with a glibc suffix, such as
`aarch64-unknown-linux-gnu.2.36`; the selected baseline must be no newer than
the oldest runtime that will execute the binary. Match the container's libc
family: a GNU/glibc binary is not interchangeable with a musl runtime.

When a crate links to native libraries, provide a target-architecture sysroot
based on the intended runtime distribution or a compatible SDK. Point
`pkg-config` at that sysroot (`PKG_CONFIG_ALLOW_CROSS=1`,
`PKG_CONFIG_SYSROOT_DIR`, and target-only `PKG_CONFIG_LIBDIR`) so it cannot
silently select host headers or libraries. Configure target C compilers/linkers
where native build scripts require them. Do not copy arbitrary host libraries
into a target sysroot.

Build with the repository's equivalent of:

```sh
cargo zigbuild --locked --release \
  --target aarch64-unknown-linux-gnu.2.36
```

Adapt target, baseline, binary selection, features, and flags to the project.
Keep Cargo's registry and target caches so ordinary subsequent builds can reuse
work; avoid `cargo clean` as a routine response to a slow build.

## Separate compilation from image packaging

1. Compile the backend on the build host/CI runner. Build frontend assets there
   too when they do not require target execution.
2. Give Buildx a minimal, temporary context containing only the compiled
   artifact, required assets/migrations, and the production Dockerfile. Use
   Buildx for image assembly and target-platform metadata, not for running
   `cargo build` under QEMU.
3. Keep target runtime dependencies in the runtime image. Some target-platform
   package-installation commands may still run under emulation; minimize those
   steps and distinguish their time from Rust compilation.
4. Never use a production VPS as a compiler, test runner, or dependency installer.
   Transfer only the completed artifact/image through the project's authorized
   release process. Do not deploy merely to validate a local build.

## Benchmark without misleading yourself or overloading the host

First ask whether the user wants a component comparison (Rust compile only) or
an end-to-end comparison (image/release build). Report both only when both were
actually measured.

- Compare the same source revision, target, release profile, feature set,
  dependency versions, hardware, and resource limits. Record Rust/Zig/
  cargo-zigbuild/Buildx versions and cache state.
- Separate Rust compile, frontend build, sysroot preparation, image packaging,
  transfer, and total wall time. A cached `cargo zigbuild` taking under a second
  is not comparable to a cold, emulated Docker build.
- For a cold comparison, isolate output/cache directories rather than deleting
  shared caches. Confirm enough disk space first. Make the cache-mount behavior
  explicit: `buildx --no-cache` does not necessarily clear persistent cache
  mounts.
- Run heavy baseline and candidate builds one at a time. Estimate duration and
  resource use before starting; cap Cargo jobs and use a bounded foreground run
  when the machine is shared or interactive. Do not launch a long emulated,
  no-cache build in the background or run it alongside tests/builds. If the
  estimate could disrupt the host, stop and ask before proceeding.
- Prefer comparing just the Rust compile stages when that answers the question;
  a full legacy Docker build may spend a long time emulating Rust, frontend, and
  package installation, which obscures the source of the improvement.
- Report exact command, elapsed wall time, relevant stage times, cache status,
  conditions, and failures. Give speedup as `baseline / candidate` only for
  comparable measurements. Label cached, interrupted, estimated, or otherwise
  unmatched runs clearly; never turn an unmeasured remainder into a claim.

## Verify binary and runtime compatibility

Before packaging or handoff:

1. Confirm the binary's architecture and ELF interpreter. Inspect dynamic
   dependencies and required glibc symbol versions (for example with `file` and
   `readelf -h`, `readelf -d`, and `readelf --version-info`).
2. Compare required shared libraries and glibc symbols with the actual runtime
   image. Ensure OpenSSL or other native libraries resolve to target-architecture
   runtime packages.
3. Build the image for the target and run a bounded smoke/readiness test in a
   local target-capable environment when available. Validate startup and the
   project's health contract without connecting to production dependencies.
4. Run the repository's relevant format, lint, tests, and build checks. Do not
   claim success for checks that were skipped.

## Report

Summarize the bottleneck found, target/toolchain and runtime baseline, files or
commands changed, validation results, and remaining constraints. Include a
before/after table with separate compile and end-to-end columns when available;
state cache and machine conditions beside every timing. If no fair comparison
could be run, say why and give the smallest safe next measurement instead of
claiming a speedup.
