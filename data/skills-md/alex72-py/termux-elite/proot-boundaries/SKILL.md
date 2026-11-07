---
name: proot-boundaries
description: Decide whether a failure belongs to native Termux or a proot distro and which side should own the package, interpreter, and project path. Use when something works in one environment but not the other, when Ubuntu or Debian runs under Termux, when a glibc-only binary is needed, or before installing, backing up, or resetting a proot distro. Do NOT use for ordinary native Termux package errors, and never use proot-distro reset or remove as a generic repair.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "medium"
  triggers: "proot,proot-distro,ubuntu in termux,native termux,glibc,works in proot,debian in termux"
---
# Native Termux and proot Boundaries

## Purpose
Stop packages, paths, and assumptions from leaking between native Termux and a proot distro, and pick the side that should own a given task.

## When to use
- A command behaves differently in a proot Ubuntu or Debian than in native Termux.
- An Android-facing feature (Termux:API, storage links) is missing inside proot.
- A prebuilt glibc binary or wheel is needed.
- Before installing, backing up, resetting, or removing a distro.

## When NOT to use
- The shell is clearly native Termux and the error is a plain `pkg` or build error: use `package-troubleshooting` or `python-native-build`.
- As a reason to move work into proot by default. Proot costs storage, I/O speed, and ptrace overhead.

## Preconditions
Run `sh scripts/detect-boundary.sh`. Treat a prompt label as unreliable; use `$PREFIX`, `tracer_pid`, `os_release_id`, and the installed distro list as evidence.

## Decision tree
1. Native Termux uses Android and Bionic conventions and `pkg`. A proot distro has its own userspace, libc (usually glibc), and package manager, but still runs under Android's process and storage limits.
2. Android-facing commands (`termux-*`, storage links) belong to the native side.
3. Install build dependencies on the side that launches the process. Binaries do not move across the boundary.
4. Choose proot when the task needs glibc-only prebuilt binaries or Debian packages that Termux lacks. Choose native when it needs Termux:API, shared storage, services, or speed.
5. The network is shared with the host. Ports and `localhost` behave the same on both sides.
6. Files are not shared unless bound. A project under the distro's `/root` is not under Termux `$HOME`, and the reverse needs a bind at login.
7. There is no systemd and no real init inside proot. Service questions go to `termux-services` on the native side.
8. Cross-boundary paths and networking must be tested, not assumed.

## Example
- Situation: A vendor CLI that needs glibc fails to start in Termux.
- Without the skill: Installs libraries piecemeal on the native side hoping the binary finds them.
- With the skill: Chooses a proot distro for that tool, installs its dependencies on the proot side, binds the project directory at login, and keeps `termux-*` calls on the native side.

## Safety
Installing, resetting, or removing a distro is destructive to everything inside it. Back up first (`proot-distro backup <alias>` where the installed version supports it, or `termux-backup`), name exactly what will be lost, and get confirmation. Do not recommend `proot-distro reset` or `remove` as a generic repair.

## Verification
Report which side owns the process, package manager, interpreter, and project path, then run the failing command on that side.

## Rollback
Keep the distro backup until the new setup is verified. Restore only after confirmation.

## Handoffs
- `termux-environment` for a fuller snapshot.
- `package-troubleshooting` for native `pkg` errors.
- `python-native-build` when a glibc wheel is the real problem.
- `storage-permissions` when a path is invisible inside proot.
- `termux-backup` before any destructive distro operation.

## Report
Which side owns each of process, package manager, interpreter, and project path, and whether proot is justified or native Termux is enough.
