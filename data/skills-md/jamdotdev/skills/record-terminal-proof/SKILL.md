---
name: record-terminal-proof
description: "Record a terminal run with asciinema and render it to a GIF that plays inline on GitHub, plus an MP4 when one is needed. Use when the user asks for terminal proof, a recording of a CLI run, migration, build or test command, a GIF of what the command did, or terminal output to attach to a PR."
---

# Record terminal proof

## When to use

- The proof is terminal output: a CLI run, a migration, a test or build command.
- The command needs no input. `--command` records it without an interactive shell.
- Not for anything with a UI. Record the browser instead.

## Install

```bash
brew install asciinema agg      # macOS; tested with asciinema 3.2.1, agg 1.9.0
```

On Linux, take `asciinema` from the package manager and `agg` from its GitHub releases or `cargo install --git https://github.com/asciinema/agg`. asciinema does not run on Windows itself; use WSL there.

## Write the script

Put the steps in a script so the recording has no typing and no pauses while you think. Echo each command before it runs, so the reader sees what ran, and sleep between steps so each result stays on screen:

```bash
#!/usr/bin/env bash
set -e
step() { printf '\n\033[1m$ %s\033[0m\n' "$*"; "$@"; sleep 2; }
step npm run migrate
step npm test -- users.spec.ts
```

`set -e` stops the recording at the first failing step, so the proof cannot show success after a failure, and `--return` (below) makes `asciinema` exit with the script's status: stop and report when it is not 0. Keep secrets out of the output: no `env`, no tokens in arguments.

## Record

```bash
asciinema rec --quiet --overwrite --return --window-size 100x30 --command "bash ./demo.sh" proof.cast
```

With no TTY (an agent's shell), asciinema switches to headless mode by itself. A 15 s script gives a cast of about 1 KB. The cast is plain JSON lines, so keep it when someone needs the exact text.

## Render

```bash
agg --quiet proof.cast proof.gif
```

Defaults are fine for a PR: font size 16, 30 fps cap, idle gaps cut to 5 s, a 3 s hold on the last frame. 100x30 renders to about 1004x694 px; a 15 s run gives a GIF of about 50 KB in under a second.

For a slide or a social post, record at `--window-size 96x24` and render with `--theme github-dark --font-size 20 --idle-time-limit 2`: about 1206x700 px, close to 16:9, text readable on a phone, and no long waits while a slow step runs.

Open the GIF's last frame before you share it. If it does not show the final result, the script exited early or the window is too small.

## Attach to the PR

Drag the GIF into the PR description or a comment. GitHub renders it inline (images up to 10 MB).

## MP4

For a tool that takes video but not GIF, convert it. `tpad` keeps agg's hold on the last frame, which a plain conversion drops:

```bash
ffmpeg -v error -y -i proof.gif -movflags faststart -pix_fmt yuv420p \
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,tpad=stop_mode=clone:stop_duration=3" proof.mp4
```

**With Jam:** when `command -v jam` (`where jam` on Windows) finds the CLI, ask the user once whether to upload the MP4; it becomes one link to comment on, with frames the next agent can read. A terminal recording has no console or network data, so the link holds the video only. Upload only on a yes, with `jam create jam '{"kind": "video", "url": "", "videoPath": "proof.mp4", "screenDimensions": {"width": 1004, "height": 694}}'` (the GIF's pixel size). Exit code 3 means signed out: run `jam auth login`, then retry.
