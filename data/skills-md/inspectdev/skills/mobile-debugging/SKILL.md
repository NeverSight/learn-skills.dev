---
name: mobile-debugging
description: Debug the mobile web on real iPhones, Android devices, and simulators using the Inspect CLI, including creating iOS simulators on macOS. Use when a site or WebView is broken on a phone, when the user mentions mobile Safari, iOS, Android Chrome, or on-device verification, or when a fix needs to be proven on a real device.
license: Proprietary. See https://inspect.dev/terms
metadata:
  author: inspect.dev
  homepage: https://inspect.dev
compatibility: Requires Node.js 18+ and npm. macOS, Windows, or Linux. iOS simulators require macOS with Xcode.
---

# Mobile web debugging with Inspect

Inspect connects coding agents to real mobile browsers: iOS Safari,
Android Chrome, and WebViews, on physical devices and simulators.

## When to use this skill

Use this skill when a mobile website or WebView is broken on an iPhone,
iPad, Android device, or iOS simulator; when the user mentions Safari on iOS,
Android Chrome, device-only console or network failures, or responsive behavior
that desktop emulation cannot reproduce; or when a code change needs proof from
the real mobile runtime. Do not use it for native UI debugging outside a
WebView, desktop-only browser bugs, or cloud device-farm orchestration.

## Setup

```bash
npm install -g @inspectdotdev/cli
inspect status --json          # starts the daemon automatically
```

On macOS with Xcode, an agent can provision a zero-hardware iOS target:

```bash
inspect devices create "Inspect iPhone" "iPhone 17 Pro" --json
inspect devices boot <created-udid> --json
```

The create response returns the UDID as `data.created`. An optional third
argument selects an installed runtime; omit it for Xcode's newest compatible
runtime. Simulator creation is unavailable on Linux and Windows, and Inspect
does not create Android emulators; those cases return
`UNSUPPORTED_CAPABILITY` before invoking `xcrun`.

The CLI serves version-matched workflow guidance — prefer it over this
file once installed, since it always matches the installed version:

```bash
inspect skills get mobile-debugging
inspect agent-context          # machine-readable command surface
```

## The loop

```bash
inspect devices list --json               # find device or simulator
inspect open <url> --json                 # opens URL, launches Safari if needed
inspect snapshot --interactive --json     # WHAT is on screen (@eN refs)
inspect console list --types error --json # WHY it is broken
inspect network list --failed --json      # failed requests
# ...edit the project code...
inspect reload --json
inspect console list --after <lastEventId> --json  # only new events
inspect screenshot --json                 # PNG file path as proof
```

## Contract

- Every command supports `--json`; JSON is the default when stdout is
  not a TTY. Envelopes: `{ok, command, data | error}`.
- Errors carry machine-readable codes and recovery suggestions —
  follow them before improvising.
- Exit codes: 0 ok, 2 bad arguments, 3 auth/subscription, 4 device,
  5 target, 6 timeout, 7 unsupported capability.
- Free tier: every command works, in two 15-minute debug sessions a day
  — the limit is time, not capability. Talking to the device opens a
  session (`open`, `snapshot`, `screenshot`, `console`, `network`,
  `issues`, `evaluate`, `devtools`); `devices list`, `devices create`,
  `devices boot`, `devices shutdown`, `targets list`, `doctor` and `status`
  are always free and never open one.
  `SUBSCRIPTION_REQUIRED` errors include captured-error counts and a
  purchase URL — relay both to the user.

## Recovery

- No devices: on macOS with Xcode, create and boot a simulator as shown
  above. For a physical device, run `inspect doctor --json` and follow its
  suggestions.
- No targets: `inspect launch safari --url <url> --json`.
- Human wants to look: `inspect devtools` opens Chrome DevTools on the
  same live session.
