---
name: wuji-cli-doctor-manual
description: "Run an active Wuji Hand 2 thumb-opposition check. Use when a user needs to verify thumb-to-finger motion or investigate a possible hand mechanism issue."
metadata:
  author: wuji-technology
  version: "2026.9.22"
  requires:
    bins: ["wuji"]
  cliHelp: "wuji doctor manual --help"
---

# Wuji Doctor Manual

Use this command only when the operator has prepared a clear motion area and accepts that the
recipe drives the hand. The command requires the hand's serial number for every active run.

## Discover Recipes

```bash
wuji doctor manual --list
wuji doctor manual --list --sn <SN>
wuji doctor manual --list --json
```

Listing is a local query. It does not connect to a device or send a command. The current list
contains `thumb_opposition` for `wuji_hand_2`.

## Run Thumb Opposition

```bash
wuji doctor manual --recipe thumb_opposition --sn <SN>
wuji doctor manual --recipe thumb_opposition --sn <SN> --json
wuji doctor manual --recipe thumb_opposition --sn <SN> --jsonl
```

The recipe checks `joint_states` and `joint_diagnostics`, confirms the serial-number hand side,
then drives the index, middle, ring, and pinky in order. Each finger uses controller force
setpoints of 2 N, 4 N, and 6 N. These values are controller settings, not calibrated physical
force measurements.

The default timeout is 120 seconds. Set a value from 5 through 600 seconds with
`--timeout-s <SECONDS>`. Press Ctrl+C once to stop safely. The command unloads the hand before it
releases the device.

## Read the Result

The public report keeps `PASS`, `FAIL`, `UNSUPPORTED`, and `INDETERMINATE` as stable machine
statuses. It also explains the result in plain language. `PASS` means the hand completed the recipe
and reached a safe state. `FAIL` means the recipe completed with at least one failed public check.
Unsupported targets report `UNSUPPORTED`, and runs that stop before a safe verdict report
`INDETERMINATE`.

Human mode shows a compact result card with the device, serial number, visual status, explanation,
and next action. JSON and JSONL add a `summary` object with `label`, `message`, and `next_action`.
Internal builds may include per-finger and force-step details for support workflows. Public output
does not expose those details or internal measurements.

Human mode writes preconditions to stderr, and the final report to stdout. JSON and JSONL modes do
not emit preconditions. `--json` emits one final JSON document, and `--jsonl` emits one final JSON
Lines report. The command does not print repeated runtime progress logs.

Parameter errors return exit code 2. Unsupported devices, failed checks, and timeouts return 1.
Ctrl+C returns 9. If the command says that another program uses the device, close that program and
retry with the same serial number.
