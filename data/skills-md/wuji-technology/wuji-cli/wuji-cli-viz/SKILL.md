---
name: wuji-cli-viz
description: "Visualize live Wuji Hand 2 or Wuji Glove data with the official Rerun Web Viewer using `wuji viz`. Use when a user wants to inspect hand pose, per-taxel forces, per-finger resultant force, force history, live visualization faults, interactive device selection, or Hand 2 runtime tactile zeroing."
compatibility: Requires Wuji CLI installed with the wuji executable available on PATH.
metadata:
  author: wuji-technology
  version: "2026.9.22"
  requires:
    bins:
      - wuji
  cliHelp: "wuji viz --help"
---

## Start a Viewer

`viz` supports Wuji Hand 2 and Wuji Glove. Without `--sn`, it scans for both device types:

```bash
wuji viz
```

It counts both supported device types together and connects directly only when exactly one supported device is found. In an interactive terminal, multiple supported devices open a searchable selector whose summary shows SN and Device Type. The highlighted item shows Transport and Address on separate detail lines, plus USB Port or IP only when that field is present. Only the selected device is connected. Pressing Esc or Ctrl+C at the selector writes `Cancelled.` to stderr, exits with code 9, and does not connect or fall back to another device. A connection failure also does not fall back.

Use `wuji viz --sn <SN>` to select a specific supported device. Structured output and unattended invocations require `--sn` when multiple supported devices are present; they never open the selector.

The command prints the viewer URL and opens it in the default browser. It keeps the device session and
Viewer running until stopped. When an Agent starts it from a chat, stop it by asking the Agent to stop
`viz`; do not tell the user to press Ctrl+C in the chat. Ctrl+C is appropriate only when the user is
running `viz` directly in its own terminal.

Use `--no-open` when the host is actually headless, or when the user explicitly asks not to open the
browser or to open the printed URL manually. Do not infer this option merely because an Agent is running
the command:

```bash
wuji viz --no-open
```

For a machine-readable startup report, use `--json` for formatted JSON or `--jsonl` for one compact JSON line. Choose zeroing behavior using the device-specific rules in **Agent Execution Contract**. This example assumes a headless host and a Hand 2 with tactile hardware or unknown tactile capability, without unloaded-fingertip confirmation:

```bash
wuji viz --sn <HAND2_SN> --no-zero --no-open --jsonl
```

After the Viewer is ready, stdout emits exactly one startup report and flushes it before the command continues running:

```json
{
  "status": "running",
  "device": {
    "sn": "WH2-...",
    "handedness": "left"
  },
  "viewer": {
    "url": "http://127.0.0.1:...",
    "lan": false
  }
}
```

Live sensor frames remain in the Viewer; they are not written to stdout. Progress, warnings, and errors remain on stderr. A failure before Viewer readiness leaves stdout empty and writes the normal structured error envelope to stderr. A later runtime failure keeps the startup report on stdout and writes the error envelope to stderr. Ctrl+C does not add a second structured record.

The command does not record an RRD file and does not accept `--address` or `--handedness` as device selectors.

The selected device determines the Viewer page:

- Wuji Hand 2 shows its live hand pose and, when available, fingertip tactile data.
- Wuji Glove shows its live hand and sensor visualization.

`viz` is live-only: it does not record an RRD or load/replay MCAP/RRD files.

## Interpret the Requested Device

Use the user's device wording to constrain selection:

- “hand”, “Hand 2”, “二代手”, or “手” means `wuji_hand_2`.
- “glove”, “Wuji Glove”, or “手套” means `wuji_glove`.

When the user names one category, filter discovery to that category and never fall back to the other
one. If no device of the requested category is available, report that fact instead of starting a
different device type.

## Agent Execution Contract

When this skill is selected for a request to start, inspect, or test `wuji viz`, execute the live
command on the user's machine; do not only paste a command for the user to run. If the installed
`wuji` binary or a supported device is unavailable, report that concrete blocker instead of claiming
that the Viewer was started.

If the user supplies an executable path, use that exact path for device discovery and every `viz`
command; do not replace it with the bare `wuji` command or silently select another installed version.

Choose the invocation from the user's intent before starting the long-running process:

1. **Select the device.** If the user names an SN, pass `--sn <SN>`. Otherwise, first run
   `wuji devices --json`, filter to `wuji_hand_2` and `wuji_glove`, and use an explicitly identified
   single candidate. In an Agent or other non-interactive process, never start the selector without
   `--sn`; if multiple supported devices remain, stop and ask the user which SN to use rather than
   guessing. Do not use `--address` or `--handedness` as selectors.
2. **Choose zeroing behavior by device.** For Wuji Glove or a Hand 2 already confirmed to have no
   tactile hardware, omit `--no-zero` and don't ask for unloaded-fingertip confirmation. For a Hand 2
   with tactile hardware or unknown tactile capability, add `--no-zero` when the user requests a
   read-only start, asks to skip zeroing, or hasn't explicitly confirmed all five fingertips are
   unloaded. Only omit it when that confirmation is present and neither read-only nor skip-zeroing
   was requested. Apply this rule to graphical, interactive, and Agent-managed launches. Use existing
   device evidence for capability information, not zero force values or missing data. Don't add a
   separate probe just to select this flag. Do not announce zeroing, unloaded-fingertip checks, or
   `--no-zero` in ordinary progress messages. Surface actual CLI zeroing errors or safety gates and
   stop. For Wuji Glove, never perform or mention Hand 2 zeroing.
3. **Choose browser and output handling.** On a graphical desktop, the default command opens the browser:
   use `wuji viz` or `wuji viz --sn <SN>` without `--no-open`. On a headless host, add `--no-open`;
   never add it merely because an Agent is running. Use `--jsonl` (or `--json`) only when the caller
   explicitly needs a machine-readable startup record. Parse the URL only after the `status: "running"`
   record; progress, warnings, and errors are on stderr.
4. **Choose network exposure deliberately.** Keep the default loopback binding for local use. Add
   `--lan` or `--bind <local-IP>` only when the user explicitly needs a remote browser and the network is
   trusted; these modes have no authentication or TLS.
5. **Keep the session alive.** A successful start is not process completion: `viz` continues streaming.
   When an Agent launches it from a chat, keep it in the Agent-managed terminal/session and return the
   URL without telling the user to press Ctrl+C; that key may interrupt the whole Agent conversation.
   If the user wants to stop it, stop the exact `viz` session/process through the Agent. Mention Ctrl+C
   only when the user is operating `viz` directly in its own terminal. Do not launch a second Viewer
   page unless the first one is closed. On disconnect, the Viewer keeps the last state and the command
   does not reconnect automatically. If zeroing reports a partial or failed operation, stop and report
   it; do not retry automatically.

Common invocations:

```bash
# Local interactive desktop, Hand 2 with tactile capability unknown and no unload confirmation
wuji viz --no-zero

# Graphical desktop, Hand 2 with unloaded fingertips confirmed and zeroing allowed
wuji viz --sn <HAND2_SN>

# Graphical desktop, Hand 2 with tactile hardware or unknown capability, no unload confirmation
wuji viz --sn <HAND2_SN> --no-zero

# Graphical desktop, Hand 2 already confirmed to have no tactile hardware
wuji viz --sn <HAND2_SN>

# Graphical desktop, explicit Wuji Glove (opens the browser)
wuji viz --sn <GLOVE_SN>

# Explicitly requested manual URL / machine-readable Glove startup
wuji viz --sn <GLOVE_SN> --no-open --jsonl

# User will open the Glove URL manually on this trusted machine
wuji viz --sn <GLOVE_SN> --no-open

# Remote browser on a trusted LAN, Hand 2 with tactile hardware or unknown capability
wuji viz --sn <HAND2_SN> --no-zero --lan --no-open
```

## Hand 2 Tactile Behavior

Hand 2 automatically adapts its tactile visualization to the connected hardware:

- With tactile hardware, show the tactile view and force history.
- Without tactile hardware, show joint pose only and hide tactile panels and force history while keeping
  the complete hand model visible.
- If tactile availability is incomplete, keep the common layout and leave unavailable finger views empty.

Do not infer tactile availability from force values. If startup cannot determine tactile availability,
preserve a safe visualization and skip any device-changing zero operation.

## Control Runtime Tactile Zeroing

The command's default invocation handles tactile zeroing according to the selected Hand 2's available
hardware. A no-tactile Hand 2 and Wuji Glove skip this operation automatically; `--no-zero` is meaningful
only for a tactile-equipped Hand 2.

When the selected device is a Wuji Glove, user-facing progress should simply say that Glove
visualization is starting. Do not expose Hand 2-only zeroing details such as “read-only”, “skip zeroing”,
or `--no-zero` in the status message.

For a Hand 2 with tactile hardware or unknown tactile capability, use `--no-zero` to prevent zeroing:

```bash
wuji viz --sn <HAND2_SN> --no-zero
```

Only when the CLI actually performs zeroing does it check all five tactile sensors for the expected
model and readiness, capture their readings as the runtime zero baseline, and wait for all five to
return to `Ready` before starting subscriptions and the Viewer. During that operation, keep every
fingertip unloaded until the terminal prints `Tactile zero: ready.`

With `--no-zero`, skip these zeroing-specific checks, baseline capture, and completion wait. Don't ask
for unloaded-fingertip confirmation for zeroing or wait for `Tactile zero: ready.` in this branch.
Normal tactile capability discovery and visualization initialization still run.

Follow the device-specific invocation rules in **Agent Execution Contract**. Glove and confirmed
no-tactile Hand 2 launches don't require unloaded-fingertip confirmation or `--no-zero`. Unknown
tactile capability isn't evidence that a Hand 2 has no tactile hardware. The CLI remains responsible
for checking the actual zeroing conditions. When zeroing is allowed, keep all five fingertip surfaces
unloaded until the terminal reports `Tactile zero: ready.` A load present during zeroing becomes part
of the baseline. The operation does not write the persistent tactile model. If the command reports
that zeroing may be partial, stop and report the error. Don't retry without user direction.

## Read the Page

For a tactile-equipped Hand 2, the Viewer contains:

- a 3D Wuji Hand 2 model driven by live joint states;
- per-taxel solid force arrows on the hand;
- one resultant force arrow for each finger;
- five fingertip 3D panels;
- five resultant-force magnitude series over a rolling 60-second window.

A no-tactile Hand 2 uses a joint-pose-only layout: hide the tactile matrix, fingertip panels, and
resultant-force history, while retaining the complete URDF, including fingertip shell meshes. Do not
remove fingertip shell geometry from the URDF to hide tactile data; those meshes are part of the hand
model. A partial tactile Hand 2 keeps the five panel slots and leaves unavailable fingers empty.

The Viewer opens in Rerun's dark theme by default with a solid black 3D background.

Force directions and magnitudes use the Viewer’s displayed coordinate convention. The Viewer displays
per-finger resultant forces and their history when tactile data is available.

## Handle Faults

Detailed warnings and errors are printed in the terminal. The Viewer page does not add an in-panel health marker:

- after a fingertip has produced a valid frame, a fault retains that frame; check the terminal for the affected finger and reason while other streams continue updating;
- a joint-stream fault retains the last valid hand pose, if any, while fingertip panels continue updating;
- missing tactile data leaves the hand pose available;
- Glove updates are rendered at no more than 60 Hz from the latest available state; an invalid frame in
  one stream retains that stream's last valid view while unaffected streams continue updating;
- When the device supports rate control, Glove startup requests `emf_poses`, `tactile`, `tactile_zones`, and
  palm IMU upstream data at 60 Hz and reports the actual rates; unsupported rate control produces a warning
  while the Viewer remains capped at 60 Hz.
- after a device disconnect, the Viewer retains the last state and the command reports the failure; stop
  the Agent-managed session through the Agent, or use Ctrl+C only in a standalone terminal.

The command does not reconnect automatically.

## Share on a Trusted LAN

By default, the Viewer uses loopback. To expose it on the machine's private network address:

```bash
wuji viz --lan --no-open
```

`--lan` selects a private address on the default route. If that route points to the wrong interface, select a specific local address instead:

```bash
wuji viz --bind 10.42.0.7 --no-open
```

`--lan` and `--bind` are mutually exclusive. Non-loopback access has no authentication and no TLS. Use it only on a trusted network and share the printed URL only with intended viewers. Supported usage is limited to one active viewer page per `wuji viz` session. Close the existing page before opening another.
