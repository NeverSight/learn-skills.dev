---
name: hz-xr-simulator-control
license: Apache-2.0
description: Routes Meta VR and Horizon OS simulator work to the right `metavr` command group, and drives a running Meta XR Simulator via `metavr xrsim` — runtime, device, input, compositor layers and MP4 recording. Use when a goal concerns a simulated headset rather than a physical one, when choosing between `xrsim`, `ssim`, `capture` and `tapedeck`, or when a `metavr xrsim` command returns a connection error. For installing the simulator or configuring it into a Unity, Unreal or native OpenXR project, use hz-xr-simulator-install-and-configure instead.
allowed-tools: Bash(metavr:*), Bash(hzdb:*)
---

# XR Simulator Control

`metavr` is overwhelmingly a **physical Quest or Glasses** CLI: `device`, `app`, `capture`, `input`, `log`,
`files` and `ui` all talk to a headset over ADB. `xrsim` is one group among them and drives a
**simulated** headset instead. Choosing the wrong group is the most common failure here, and it
is quiet: `metavr device list` prints `No devices connected` and exits 0, so the wrong answer
looks healthier than the right one.

This skill drives a simulator that already exists. Installing one, or wiring it into a project,
belongs to `hz-xr-simulator-install-and-configure`.

## Which Command Group

| The goal concerns | Use | Not |
|---|---|---|
| The simulated headset model, IPD, refresh rate | `metavr xrsim device …` | `metavr device …` (physical, ADB) |
| The simulator frontend process | `metavr xrsim app …` | `metavr app …` (APKs on a headset) |
| Simulated hands and controllers | `metavr xrsim input …` | `metavr input …` (keyevents to hardware) |
| The simulator's synthetic room | `metavr xrsim env …` | — |
| Compositor layers, simulated frame rate | `metavr xrsim layer` / `xrsim runtime fps` | — |
| The simulator's own logs | `metavr xrsim runtime logs` | `metavr log` / `metavr adb logcat` (device logcat) |
| What the simulated headset renders | `metavr xrsim record` | `metavr capture` (physical device screen) |
| Recording and replaying an app's OpenXR calls on a real headset | `metavr tapedeck` | `metavr xrsim record` (compositor pixels, not a call stream) |
| The SpatialSim emulator | `metavr ssim` | `metavr xrsim` (a **different** simulator) |

Read the `Use` column as the right tool for that goal and `Not` as the one you might reach for by
mistake. The last two rows are in this table because they are the mistakes, not because they are
this skill's job.

Three are worth stating outright, because a plausible command exists on both sides:

- **"Record an OpenXR session"** is the most confusable intent in the CLI. `xrsim record` captures
  the simulator's compositor output to MP4; `tapedeck` captures and replays an app's OpenXR call
  stream on a physical device. They are not substitutes.
- **"The simulator"** is ambiguous inside this binary. `ssim` is the SpatialSim emulator, `xrsim`
  is the Meta XR Simulator.
- **`device`, `app` and `input` exist both at the top level and under `xrsim`**, so the same verb
  means different things depending on the group. `capture` does not: there is no `xrsim capture`,
  and the simulator equivalent is `xrsim record`.

## The Three Connection Tiers

Once you are inside `xrsim`, what a command needs decides which error you get.

| Tier | Commands | Needs |
|---|---|---|
| Local | `readme`, `runtime logs`, and on Linux bare `record --output … --duration …` | nothing running |
| Lifecycle | `app launch`/`quit`/`ensure-running` | nothing running — these *manage* the frontend |
| Frontend | `runtime activate`/`deactivate`/`list`, `env set`/`list` | the frontend app |
| Runtime | `runtime ping`/`status`/`info`/`fps`, `device *`, `input *`, `layer *`, `record start`/`stop`/`status` | the frontend **and** a connected XR app |

`device list` and `device refresh-rates` read like static catalogs but come from the live runtime.
`input sources` prints a fixed list yet still needs a connection, because the `input` group opens
one before it dispatches.

Two that a reasonable guess gets wrong in the other direction:

- **The `app` group is how you fix a down frontend, not something blocked by one.** `app launch`
  and `app ensure-running` start it if it is absent. `app quit` asks the frontend on `--port` to
  close; `--force` terminates that same process instead, and `--all` is the explicit escape hatch
  for stopping every MetaXRSimulator on the host. Treating lifecycle commands as frontend-tier
  rules out the recovery.
- **Bare `record` is local on Linux.** Without `--runtime-addr` it never connects — it captures the
  framebuffer through `ffmpeg`, so it needs `ffmpeg` on `PATH` but neither tier. The `record start`
  / `stop` / `status` subcommands are runtime-tier and additionally refuse to run on Linux without
  `--runtime-addr`.

Each error names exactly one hop, so do not retry blindly.

| Message | What broke | Fix |
|---|---|---|
| `XR Simulator is not running…` | nothing listening on the frontend port | start the app, or pass `--port` |
| `XR Simulator is running but no app is connected…` | frontend up, no OpenXR app attached | launch the app under test |
| `Runtime at <addr> is no longer responding…` | the attached app died | restart it; the stale endpoint clears itself |
| `Meta XR Simulator is not installed in a registered system or MQDH location` | the frontend binary was never found | an install problem — see `hz-xr-simulator-install-and-configure` |
| `native recording subcommands require --runtime-addr on Linux` | `record start`/`stop`/`status` on Linux | pass `--runtime-addr`, or use bare `record --output … --duration …` |
| `ffmpeg is required to record XR Simulator MP4s` | the Linux `record` path has no `ffmpeg` | install `ffmpeg` |

**Check liveness with a frontend-tier command before asking runtime-tier questions.** A refused
connection returns `XR Simulator is not running` immediately, and `--timeout` is the total
connection budget rather than a fresh budget for every retry. `runtime list` also distinguishes a
reachable frontend with no attached app from a missing frontend, while `runtime status` requires
an attached runtime.

So diagnose in tier order — cheapest first, stopping at the first failure:

```bash
metavr xrsim runtime logs                             # local: paths resolve with nothing running
metavr xrsim runtime list --format json --timeout 2   # frontend reachable? how many runtimes?
metavr xrsim runtime status --format json             # only once a runtime is attached
```

`runtime logs` goes first precisely because it is the one that still answers when everything else
is down: when `runtime list` fails, the log paths are what say *why* the frontend will not come up,
and the `XR Simulator is not running` row above cannot tell you that.

`runtime list` returning `[]` is the frontend being up with no app connected — a different failure
from the frontend being down, needing a different fix. More than one entry is its own trap: the
runtime-tier groups follow the frontend's *current* endpoint, so pin one with `--runtime-addr`
rather than guessing which answered.

## Safe Frontend Shutdown

Scope routine shutdown to the frontend's port. The default sends a close request so a live OpenXR
session can tear down cleanly; use `--force` only after that scoped close fails. Never use `--all`
as ordinary cleanup because it stops every MetaXRSimulator on the host.

```bash
metavr xrsim --port 33794 app quit
metavr xrsim --port 33794 app quit --force  # only after graceful close fails
metavr xrsim app quit --all                 # only when every instance must stop
```

The quit report names the scoped `pid` and whether the operation was `forced`, alongside
`was_running`, `killed`, and `confirmed_stopped`. For `--all`, the table renders `all` in the PID
column; the JSON payload omits the internal scope marker.

## Two Things That Bite

1. **A setter reports what the runtime holds, not merely what was requested.** `device set`,
   `device ipd`, and `device refresh-rate` read settings back into an `OBSERVED` column. Without
   `--wait`, that is one immediate read and may still show the old value; with `--wait`, the
   command waits for convergence or exits with a timeout. Treat `unknown` as a failed read-back,
   never as confirmation that the requested value applied.
2. **`runtime status` is fault-tolerant by default.** It can exit 0 after a section fails, so check
   `device_error` / `input_error` / `fps_error`. In automation, pass `--strict`: any failed query
   then produces a non-zero exit while the report is still printed for diagnosis.

## XR Operator Port Consistency

When Meta XR Operator controls the app through a non-default port, set
`AGENTICXR_MCP_PORT` to the same value for the in-app layer and the process running metavr. The
proxy receives the resulting backend URL from metavr; mismatched environments point the proxy at
a different port from the layer. Restart the affected app and MCP server after changing the
variable.

For everything else — exact flags, output shapes, the two recording engines — `metavr xrsim readme`
and `metavr xrsim --help` are authoritative and always current. Ask the binary rather than guessing.

## References

- [`references/commands.md`](references/commands.md) — tier per group, the irregular corners of the surface, what the output means
- GitHub: `https://github.com/meta-quest/agentic-tools/tree/main/skills/hz-xr-simulator-control`
- `hz-xr-simulator-install-and-configure` — installing the simulator and configuring it into a project
- `hz-vr-debug` — debugging against a physical device
