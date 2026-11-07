---
name: voicestudio-cli
description: Set up and use the Voice Studio CLI for shell scripts, batch processing, CI pipelines, or any non-MCP automation. Provides AI-powered text-to-speech, voice cloning, and voice design as composable shell commands. Use when the user wants to script Voice Studio from bash/zsh, render farms, GitHub Actions, or pipe its output into other tools (jq, ffmpeg, etc.).
license: MIT
metadata:
  author: Voice Studio
  version: "1.0"
---

# Voice Studio - CLI

## Platform support

> **macOS only right now.** Windows builds are in progress and not yet shipped. Linux is not planned. The CLI relies on Voice Studio.app's local sidecar; without the desktop app installed, no command works.

## What this is

This skill walks through using the `voicestudio` CLI for batch jobs and shell pipelines. It's a Python `typer` app distributed as the `voicestudio-cli` pip package; like the MCP server, it talks to the Voice Studio sidecar on `127.0.0.1:58391` and auto-launches the desktop app when needed.

Use this skill when the environment is **not** an MCP client - shell scripts, Makefiles, CI runners, batch scripts that pipe into `jq` / `ffmpeg` / `xargs`, or any case where you'd rather hand a non-agent process a deterministic command line than a tool-call API. For agentic / chat-driven use, prefer the `voicestudio-mcp` skill instead.

Requirements: **macOS 12+ on Apple Silicon (ARM64)**, Voice Studio.app installed, an active subscription or trial, Python 3.10+.

---

## One-minute install

```bash
pipx install voicestudio-cli
```

`pipx` is preferred - it isolates the dependency tree and puts the `voicestudio` script on your PATH cleanly. If you don't have `pipx`:

```bash
pip install voicestudio-cli
```

Verify:

```bash
voicestudio --help
voicestudio status
```

---

## What you get

Fourteen commands, all invoked as `voicestudio <subcommand>`:

```bash
voicestudio voices                                     # list all voices
voicestudio say "Hello world" --voice Storyteller --style natural
voicestudio say-with-profile "Hello" --profile-id 7
voicestudio clone sample.wav --name "MyVoice" --description "warm narrator"
voicestudio design "Welcome aboard" --as "calm British woman, late 30s"
voicestudio transcribe interview.wav --max-seconds 600
voicestudio history --limit 25
voicestudio download 142                               # re-download record id 142
voicestudio account                                    # paid / free tier + free generations left
voicestudio free                                       # unload all models to free RAM
voicestudio status                                     # which model is currently loaded
```

Run any command with `--help` for its full flag set. Every command takes an optional `--out PATH` to set the output file and (where it makes sense) `--json` for machine-readable output.

---

## Recipes

### Batch generate from a CSV

Read `text,voice` pairs out of `scripts.csv` and render one wav per line:

```bash
while IFS=, read -r line voice; do
  voicestudio say "$line" --voice "$voice" --out "out_${RANDOM}.wav"
done < scripts.csv
```

Tip: keep all lines on the same `voice` adjacent in the CSV - that avoids paying the model-swap cost between rows.

### Pipe voices into jq

List only custom (cloned) voices by name:

```bash
voicestudio voices --json | jq -r '.[] | select(.is_custom) | .name'
```

### Transcribe-then-speak loopback (voice mimicry test)

```bash
voicestudio transcribe interview.wav | xargs -I {} voicestudio say "{}" --voice "Storyteller"
```

Note: this triggers a model swap on every iteration (ASR -> TTS -> ASR ...). Fine for one-shots, painful for batches; if you have many files, transcribe them all first, then synthesize all the outputs.

---

## The `--json` flag

These commands support `--json` for programmatic consumption:

- `voicestudio voices --json` - array of voice objects (`id`, `name`, `language`, `is_custom`, ...).
- `voicestudio history --json` - array of generation records.
- `voicestudio account --json` - normalized account object: `tier` (`paid`/`free`), `paid`, `generations_remaining`/`generations_limit`/`generations_used` (free tier; else null), `plan`, `expires_at`, `summary`. Reads the Mac App Store entitlement + free-tier allowance. Script the free-tier check with `voicestudio account --json | jq '.generations_remaining'`.
- `voicestudio free --json` - `{ "unloaded": true }` after freeing all models.
- `voicestudio status --json` - `{ "service": "tts" | "clone" | ... | null }`.

Generation commands (`say`, `say-with-profile`, `clone`, `design`, `transcribe`, `download`) print the absolute output path on stdout - already script-friendly without `--json`.

---

## Things to know

- **Auto-launch.** If Voice Studio.app is not running, the first command will launch it. The first command may take ~45s before it returns; subsequent commands are fast.
- **One service at a time.** The sidecar loads one ML model at a time. Consecutive commands that hit different services (e.g. `say` then `transcribe` then `design`) each pay a 5-15s model-swap. Batch by service.
- **Output location.** `--out PATH` writes exactly to that path. Without `--out`, files land in `~/Documents/VoiceStudio/integrations-out/`. Override the default with the env var `VS_OUTPUT_DIR=/some/dir`.
- **Exit codes.** All commands exit `0` on success, `1` on failure with a friendly error message on stderr. Safe to use in `set -e` scripts.
- **Cloning input.** `voicestudio clone` wants ~10-30s of clean mono speech (wav or mp3). Anything shorter produces flaky profiles.
- **Entitlement gate.** Generation commands (`say`, `say-with-profile`, `clone`, `design`, `transcribe`) require a Mac App Store purchase or unspent free-tier generations. When neither applies the backend refuses with a 403 and the command exits `1` with a clear message. Read-only commands (`voices`, `profiles`, `history`, `account`, `status`, `free`, `download`) work regardless. Use `voicestudio account` to see the tier and remaining free generations in one shot.

---

## Performance (rough wall-clock per command)

End-to-end times including the model load on the first invocation of a given service. Subsequent same-service commands are much faster. Switching services adds a 5-15s swap.

| Command | Apple Silicon (M1 / M2 / M3 / M4) | Intel Mac |
|---|---|---|
| `say "1-2 sentences"` | 3-8s first, 1-3s after | 15-30s first, 5-12s after |
| `say "paragraph"` | 6-15s first, 3-8s after | 30-60s first, 12-25s after |
| `design "..." --as "..."` | 5-12s first, 2-6s after | 20-45s first, 8-20s after |
| `say-with-profile` | 4-10s first, 2-5s after | 18-35s first, 7-15s after |
| `transcribe audio.wav` (≤30s clip) | 2-5s | 5-15s |
| `clone audio.wav` (60s reference) | 5-15s with auto-transcription | 20-60s |

For CI use cases, set generous step timeouts.

---

## Troubleshooting

- **`LaunchError: no app bundle found`** - Voice Studio.app is not installed in `/Applications`. Either install it, or export `VS_APP_PATH=/path/to/Voice Studio.app` before invoking the CLI.
- **`BackendError 403 license_inactive`** - License is not active. Run `voicestudio license` to confirm, then activate via the desktop app's License screen.
- **Slow first call** - Cold-start. The sidecar is loading a model from disk. Re-running the same command immediately after is fast.
- **`ConnectionRefusedError` on 127.0.0.1:58391** - The sidecar didn't come up. Fully quit Voice Studio.app and re-run the CLI, or launch the app manually first.
- **Command not found after install** - `pipx`'s bin dir isn't on PATH. Run `pipx ensurepath` and restart your shell.
