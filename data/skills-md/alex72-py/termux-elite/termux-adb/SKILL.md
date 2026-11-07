---
name: termux-adb
description: Set up and debug adb from Termux to the same phone using Wireless debugging (pairing code, connect port, unauthorized or offline devices) for the few tasks that need shell-level access. Use when the user mentions adb pair, adb connect, wireless debugging, android-tools, adb devices showing unauthorized or offline, or when another skill hands off a system setting that needs adb. Do NOT use for Termux:API permission errors (see termux-api), for USB debugging from a PC, or to change a system setting without confirmation.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "medium"
  triggers: "adb pair,adb connect,wireless debugging,adb devices,adb unauthorized,android-tools,adb shell,pairing code,adb from termux"
---
# Termux ADB

## Purpose
Establish and verify adb access from Termux to its own device only when a task needs shell-level privileges, and tear it down afterwards.

## When to use
- Setting up Wireless debugging so Termux can run `adb` against the same phone.
- `adb devices` shows nothing, `unauthorized`, or `offline`.
- Another skill needs an adb-only change, for example the phantom process limit in `background-processes`.

## When NOT to use
- Termux:API permission problems: `termux-api` owns those.
- Anything achievable without adb. adb is shell-user access to the whole device, not a convenience.

## Preconditions
Wireless debugging exists from Android 11 (API 30). Developer options must be enabled by the user. `sh scripts/check-adb.sh` prints adb state read-only; it never starts the adb server, pairs, or connects.

## Decision tree
1. `adb: absent`: the `android-tools` package is missing; installing it is a confirmed change.
2. `android_sdk` below 30: Wireless debugging is not available. Say so; a one-time setup from a computer is needed instead of improvising.
3. Wireless debugging is switched on by the user in Developer options, usually while connected to Wi-Fi.
4. Pair once. The "Pair device with pairing code" dialog shows an address, a pairing port, and a six-digit code: `adb pair <address>:<pairing-port>`, then enter the code. The dialog closes if Termux takes the whole screen, so use split-screen or a floating window.
5. Connect with the other port. The main Wireless debugging screen shows a different port: `adb connect <address>:<connect-port>`. Pairing persists, but the connect port changes when Wireless debugging is toggled or the network changes.
6. `adb devices`: `device` is ready. `unauthorized`: accept the prompt on the phone or pair again. `offline`: `adb disconnect`, toggle Wireless debugging, reconnect. Empty: not connected.
7. `connection refused` or `failed to connect`: usually the pairing port was used for connecting, or Wireless debugging was switched off.
8. adb runs as the `shell` user. That is more than Termux has and far less than root; do not describe it as root.
9. Before any change, read the current value with the matching getter (for example `adb shell settings get ...`) and record it.

## Example
- Situation: adb connect fails with connection refused right after a successful adb pair.
- Without the skill: Pairs again and again with new codes.
- With the skill: Notes the pairing port differs from the connect port, reads the connect port from the main Wireless debugging screen, connects, and confirms `adb devices` shows `device`.

## Safety
adb gives shell access to the whole device. Treat the pairing code as a secret and do not repeat it in logs. Keep Wireless debugging off when not needed and never leave `adb tcpip` listening on an untrusted network. Every setting change is system-wide: state the exact command and how to revert it, then get explicit confirmation.

## Verification
`adb devices` lists the device as `device`, and `adb shell getprop ro.build.version.sdk` returns the API level. After a change, read it back with the same getter used to record the original.

## Rollback
Restore each recorded setting to its original value, run `adb disconnect`, stop the server with `adb kill-server`, switch off Wireless debugging, and revoke authorizations in Developer options on a shared device.

## Handoffs
- `background-processes` when the goal is the phantom process limit.
- `termux-environment` for the Android level and native-versus-proot side.
- `termux-network` when the phone cannot reach its own address.
- `termux-api` when the real failure is a Termux:API permission.

## Report
adb state before and after, the one setting changed with its original value, and whether Wireless debugging was switched back off.
