---
name: lynx-recorder
description: Record Lynx page interactions into a TestBench replay file using agent-lynx. Use when asked to start or stop a recording, capture page interactions for replay, or troubleshoot recording capture. For inspecting or editing an existing fixture, use lynx-recorder-fixture.
---

# Lynx Recorder

Record Lynx page interactions and produce a TestBench replay file. The saved
`.json` file may contain base64(zlib(JSON)); use `lynx-recorder-fixture` to inspect
or edit its contents.

## `agent-lynx` CLI

**This skill contains no scripts.** Recording is the `recorder` subcommand of
the public `agent-lynx` CLI:

```bash
agent-lynx recorder start [options]
agent-lynx recorder end [options]
```

The `agent-lynx` CLI is normally available on `PATH`. If
`command -v agent-lynx` fails, use `npx` instead, for example:

```bash
npx --yes agent-lynx recorder start [options]
```

The `agent-lynx` CLI on `PATH` and the `npx` command are the supported
execution forms.
This skill does not provide a local `scripts/index.mjs` entry.

## Commands

### `recorder start`

```bash
agent-lynx recorder start [--client <clientId>]
```

- `-c, --client <clientId>` (optional) — Target client. If omitted, the first available client is used.

### `recorder end`

```bash
agent-lynx recorder end [--client <clientId>] [--output <path>]
```

- `-c, --client <clientId>` (optional) — Target client. If omitted, the first available client is used.
- `-o, --output <path>` (optional) — Output file or directory. If omitted, defaults to `~/.lynx-devtool/files/lynxrecorder/recording-<clientId>-<timestamp>.json`.

## Workflow

1. **Start before opening the page.** Run `recorder start`. Capture must begin *before* the target page loads so the recording includes `loadTemplate`.
2. **If `start` reports `restartRequired: true`**, `enable_debug_mode` was just enabled — restart the app and run `recorder start` again (see Notes).
3. **Open and interact.** Open (or reload) the target Lynx page and perform the interactions to capture.
4. **Stop and save.** Run `recorder end --output ./my-recording.json`. Report the absolute path(s) returned in `savedFiles` to the user.

## Notes

- **A replayable recording requires `loadTemplate`.** Open or reload the target page *after* `recorder start`. A recording started against an already-open page still captures interactions but **cannot be replayed**.
- **First-time `enable_debug_mode` may need a restart.** `start` enables `enable_debug_mode` if it is off; when the platform persists that switch, `start` returns `{ success: false, restartRequired: true }`. Restart the app, then run `start` again.
- **The target must be a recorder build.** If `start` reports `Recording.start is not implemented`, the app/engine was built without `ENABLE_TESTBENCH_RECORDER` (not a dev/recorder build). Use a recorder-capable build.
- **One client by default.** Omitting `--client` picks the first available client. When multiple devices or apps are connected, pass `--client` explicitly.

## Output

`end` prints a single JSON object on success:

```json
{
  "success": true,
  "message": "Recording ended successfully.",
  "savedFiles": ["/abs/path/recording.json"],
  "diagnostics": [
    {
      "file": "/abs/path/recording.json",
      "fileSizeBytes": 12345,
      "healthy": true,
      "actions": 42,
      "hasTemplate": true,
      "functionDistribution": { "loadTemplate": 1, "SendTouchEvent": 12 },
      "verdict": "Valid recording — includes template load and interaction data"
    }
  ]
}
```

`diagnostics.verdict` classification:

- **`hasTemplate: true`** → valid, replayable.
- Touch events present but **no `loadTemplate`** → useful for analyzing interactions, **not replayable**.
- Actions present but **no `loadTemplate`** → useful for inspecting JSB calls / data updates, **not replayable**.
- **0 actions** → empty recording; nothing was captured.
- **Cannot parse** → the file is not a valid TestBench recording.

## Troubleshooting

| Symptom | Cause | Action |
|---|---|---|
| `start` returns `restartRequired: true` | `enable_debug_mode` was just enabled and persisted | Restart the app, then run `recorder start` again |
| `start` errors `Recording.start is not implemented` | Not a dev/recorder build (no `ENABLE_TESTBENCH_RECORDER`) | Use a recorder-capable build of the app/engine |
| Recording has no `loadTemplate` (not replayable) | Page was already open, or not reloaded after `start` | Re-record: run `start` first, then open/reload the page |
| Empty recording (0 actions) | No page activity between `start` and `end` | Ensure the page is opened and interacted with during recording |
| `end` times out | Device disconnected, or `start` was never called | Verify the connection; ensure `start` ran first |
| No available clients | Device not connected or app not running | Connect the device via USB and open the DevTool-enabled app |
