---
name: python-native-build
description: Diagnose a failed Python install on Termux or Android (compiler or header errors, Rust or maturin builds, no wheel for this platform, glibc wheels that fail at import, externally-managed-environment) and pick the smallest fix, preferring Termux-packaged libraries (the main repo, then tur-repo with consent) over source builds. Use when pip or uv fails, when a build error mentions clang, cc, cargo, rustc or a missing .h file, or when an import fails right after a successful install. Do NOT use for slow downloads, pure-Python packages that install fine, or Node problems (see node-native-build).
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "medium"
  triggers: "pip failed,python package install,wheel unavailable,build error,externally-managed-environment,failed building wheel,cargo failed,cannot locate symbol,pip install cryptography,install numpy,install scipy,install pandas,no matching distribution"
---
# Python Native Build

## Purpose
Separate a Python packaging problem from a missing Termux toolchain, an unsupported Android wheel, or the wrong environment boundary, then apply the smallest change that fixes it.

## When to use
- `pip` or `uv` fails with compiler errors, missing headers, linker errors, Rust build errors, or `No matching distribution`.
- A package installs but fails on import.
- `error: externally-managed-environment`.

## When NOT to use
- Slow installs. Do not add a toolchain because a build is merely slow.
- Failures before pip runs (`pkg` errors): use `package-troubleshooting`.
- Node packages: use `node-native-build`.

## Preconditions
Capture, read-only: `python -VV`, `python -m pip --version`, `uname -m`, the active prefix, whether a venv is active, the exact package and version, and the first meaningful error (not the last line). `sh scripts/check-toolchain.sh` prints the toolchain facts.

## Decision tree
1. Classify first. Read `environment_class` from the `termux-environment` helper. Only `termux-native` follows the Termux steps below. `proot` and every other class use that system's own package manager and normal PEP 668 rules, with no Termux package names and no `tur-repo`. `unknown`: ask.
2. Native Termux install ladder for a Python library. Stop at the first rung that works and do not skip down:
   a. The Termux main repository: `pkg search python-<name>`. numpy and cryptography live here (`python-numpy`, `python-cryptography`), not in `tur-repo`. Install the package with `pkg`, not pip.
   b. `tur-repo`, the community repository: heavier libraries such as scipy and pandas have been distributed there. `tur_repo` in the helper shows whether it is enabled. Enabling it widens trust: ask, then search again. Placement changes over time, so trust `pkg search`, not memory.
   c. A venv with `--system-site-packages`, so packaged libraries stay visible, then pip for the remaining pure-Python dependencies. If a project pins a version that conflicts with the packaged one, say so and continue at e.
   d. A third-party wheel index is its own trust decision: ask first.
   e. Compile from source (steps 6 to 9).
3. `externally-managed-environment`: Termux marks its Python as externally managed (PEP 668), as other distributions do. Fix in order: a packaged library (rung a or b), else a venv (add `--system-site-packages` to keep packaged libraries visible), else `pipx install --system-site-packages` for command-line apps. `--break-system-packages` is a last resort that lets pip overwrite files `pkg` owns; never the default, and never delete the `EXTERNALLY-MANAGED` marker.
4. `failed building wheel` for a library that has a package (rung a or b): do not repair the compile. Install the package; the build error is the symptom of skipping the ladder.
5. No compatible wheel and no sdist support: say so and offer a substitute or a proot environment. Do not loop on `--no-binary`.
6. Source build: name the missing executable (`clang`, `make`, `cmake`, `pkg-config`, `rustc`, `cargo`) and the missing header or library separately. Termux headers ship inside the main package (`openssl`, `libffi`, `libxml2`, `libjpeg-turbo`), not in `-dev` packages.
7. Rust or maturin based builds (for example pydantic-core, or cryptography when a project pins a version the package does not match): need `rust` and `binutils`, and some require `ANDROID_API_LEVEL` set to the device API level (`getprop ro.build.version.sdk`). Check the project's build error before setting it.
8. Scientific stacks that fail linking math symbols may need `MATHLIB=m` in the environment. For numpy the package is the answer: community reports of building it needed `MATHLIB=m`, `LDFLAGS=-lpython3.<minor>`, and `--no-build-isolation` together, which is fragile and Python-version specific. Verify against the actual error first.
9. Installs fine, import fails with `cannot locate symbol` or a missing `libc.so.6`: a glibc (manylinux) wheel landed on Bionic. Treat as step 5.
10. Build dies with `Killed` or signal 9: lower parallelism (`MAKEFLAGS=-j1`, `CMAKE_BUILD_PARALLEL_LEVEL=1`) and see `background-processes`.
11. Do not use `--no-build-isolation` until the build requirements are understood; it hides the real dependency boundary.

## Failure signatures
| Signature | Layer | Next step |
| --- | --- | --- |
| `clang: not found`, `command 'cc' failed` | no compiler | install `clang` after confirmation |
| `fatal error: 'x.h' file not found` | missing library | find the owning package with `pkg search`, install it |
| `unable to find library -lx` | missing or wrong library | same as above; check `$PREFIX/lib` |
| `can't find Rust compiler` or MSRV error | no or old Rust | install or upgrade `rust` |
| `No matching distribution found` | no wheel for platform | step 2 or 5 |
| `error: externally-managed-environment` | PEP 668 marker | step 3 |
| `Failed building wheel` for numpy, cryptography, scipy, or pandas | packaged library skipped | steps 2 and 4 |
| `cannot locate symbol` at import | glibc wheel on Bionic | step 9 |

## Example
- Situation: pip install cryptography fails on a phone with can't find Rust compiler or failed building wheel.
- Without the skill: Installs `rust` and retries, or adds `--break-system-packages` and `--no-build-isolation`, compiling a library that Termux already ships.
- With the skill: Reads `environment_class: termux-native`, finds `python-cryptography` with `pkg search` in the main Termux repo (not tur-repo), installs that package after confirmation, uses a venv with `--system-site-packages` if the project needs one, and verifies with `import cryptography` and `pip check`.

## Safety
Installing packages, creating venvs, and exporting build flags change the environment: state the exact change and confirm. Third-party package repositories (for example tur-repo) and third-party wheel indexes widen the trust boundary; ask before adding one.

## Verification
Re-run the original install, then `python -c "import <module>"` and `python -m pip check`. Report what remains unsupported on Android.

## Rollback
Record every package and venv created for this attempt. Remove only those, and never delete a user environment without explicit approval.

## Handoffs
- `termux-environment` when architecture, Python, or toolchain facts are missing.
- `package-troubleshooting` when `pkg` itself fails.
- `proot-boundaries` when the package needs glibc.
- `background-processes` when the build is killed.
- `node-native-build` when the failing package is a Node module.

## Report
Root cause in one line (layer plus first real error), the single change applied, the verification result, and any limit that remains.
