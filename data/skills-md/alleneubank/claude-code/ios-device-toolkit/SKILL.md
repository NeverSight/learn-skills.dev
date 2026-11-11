---
name: ios-device-toolkit
description: Use when interacting with USB-attached iOS devices via pymobiledevice3 — screenshots, syslog, crash reports, app install/launch/pull, file transfer, sysmon perf, TCP port forwarding, WebInspector/CDP, and device diagnostics.
---

# iOS Device Toolkit

Drive a physical iOS device over USB with `pymobiledevice3`. This skill covers the high-value workflows; deep reference per area is in `references/`.

- Capture, logs, crashes → `references/capture.md`
- Apps, app sandbox files, AFC media, debugserver → `references/apps-files.md`
- Device info, perf, springboard, webinspector, tunneling → `references/diagnostics-perf.md`

## Install

```bash
# uv (preferred) or pipx
uv tool install pymobiledevice3
pipx install pymobiledevice3

pymobiledevice3 version   # confirm; tested at 7.0.7
```

## Prerequisites

1. **Physical iOS device** attached via USB (or Wi-Fi-paired through usbmuxd).
2. **Developer Mode** enabled on device (Settings → Privacy & Security → Developer Mode). Verify with `pymobiledevice3 mounter query-developer-mode-status`.
3. **Trusted** computer — accept "Trust This Computer" prompt on the device after first connect.
4. **iOS 17+ only**: a long-running `tunneld` daemon is required for any developer-mode service (screenshots, DVT instruments, debugserver, pcap-with-process, etc.). Start it once per boot:
   ```bash
   sudo pymobiledevice3 remote tunneld
   ```
   The CLI auto-retries developer commands through tunneld; you no longer need `--tunnel ""` on every call in 7.x, though it still works.

## Device selection

For a single attached device, no flag is needed. For multiple, scope every call with one of:

- `--udid <UDID>` — usbmux-discovered device
- `--tunnel <UDID>` — tunneld-discovered device (developer services on iOS 17+)
- `PYMOBILEDEVICE3_UDID=<UDID>` / `PYMOBILEDEVICE3_TUNNEL=<UDID>` env vars — set once, all subsequent invocations inherit

Discover UDIDs:

```bash
pymobiledevice3 usbmux list             # USB + Wi-Fi devices known to usbmuxd
xcrun devicectl list devices            # Apple's own listing (macOS)
pymobiledevice3 lockdown info | head    # full lockdown dump for the default device
```

Caveat: `--tunnel ""` (empty string) prompts interactively. In non-interactive shells, pass the UDID directly.

## Quick reference

```bash
# --- Device info ---
pymobiledevice3 usbmux list
pymobiledevice3 lockdown info
pymobiledevice3 diagnostics battery
pymobiledevice3 mounter list

# --- Capture ---
# Screenshot (iOS 17+, DVT path — works where the deprecated developer screenshot fails)
pymobiledevice3 developer dvt screenshot ~/Desktop/shot.png
# Live syslog
pymobiledevice3 syslog live
# Crash reports
pymobiledevice3 crash ls
pymobiledevice3 crash pull ~/ios-crashes
# Packet capture (filter by process is optional)
pymobiledevice3 pcap --out trace.pcap --process Safari

# --- Apps ---
pymobiledevice3 apps list --user                            # only user-installed
pymobiledevice3 apps install ./MyApp.ipa
pymobiledevice3 apps uninstall com.example.MyApp
pymobiledevice3 developer dvt launch com.example.MyApp
pymobiledevice3 developer dvt process-id-for-bundle-id com.example.MyApp
pymobiledevice3 developer dvt kill <PID>

# --- Files (app sandbox + media) ---
pymobiledevice3 apps pull com.example.MyApp Documents/log.txt ./log.txt
pymobiledevice3 apps push com.example.MyApp ./seed.json Documents/seed.json
pymobiledevice3 afc pull DCIM/100APPLE/IMG_0001.HEIC ./
pymobiledevice3 afc ls -r DCIM

# --- Perf ---
pymobiledevice3 developer dvt sysmon system            # one-shot system stats
pymobiledevice3 developer dvt sysmon process           # per-process loop
pymobiledevice3 developer dvt proclist                 # PID + start times
pymobiledevice3 developer dvt energy <PID> [<PID>...]

# --- Networking / port forwarding ---
pymobiledevice3 usbmux forward 8080 8080               # local:8080 -> device:8080
pymobiledevice3 webinspector opened-tabs               # requires Safari Web Inspector enabled on device
pymobiledevice3 webinspector cdp                       # CDP server for WebView debugging
```

## Common gotchas

- **"InvalidServiceError" / "Failed to start service" on iOS 17+** → tunneld is not running. Start `sudo pymobiledevice3 remote tunneld` and retry. Confirm with `ps aux | grep tunneld`.
- **"DeveloperDiskImage not mounted"** → `pymobiledevice3 mounter auto-mount`.
- **Deprecated screenshot API hangs on iOS 17+** → use the DVT variant: `developer dvt screenshot` (not `developer screenshot`).
- **`--tunnel ""` hangs in scripts** → empty string means interactive picker; pass the UDID explicitly.
- **Permissions on Linux** → usbmuxd typically needs to be running; on macOS it's built in.
- **Pairing lost after iOS update** → `pymobiledevice3 lockdown unpair && pymobiledevice3 lockdown pair`.

## Scripting tips

- Set `PYMOBILEDEVICE3_UDID` (and `PYMOBILEDEVICE3_TUNNEL` for developer services) once at the top of a script to avoid repeating flags.
- For capture-and-open recipes (screenshot + `open`, syslog tail + `grep`, etc.), wrap in a shell function rather than re-typing the full path each time.
- Most subcommands accept `--rsd HOST PORT` as an alternative to `--tunnel`, useful when you already have an RSD address from a manual `pymobiledevice3 remote start-tunnel`.
