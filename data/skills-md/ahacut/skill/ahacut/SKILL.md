---
name: ahacut
description: "Generate timeline-synced motion-graphics b-roll video from subtitles (SRT), a plain script, or an audio file (mp3/wav) via the Ahacut platform. Use when the user wants b-roll, motion graphics, animated captions/typography, or to turn an SRT / script / voiceover into a downloadable video track."
license: MIT
compatibility: Requires curl. python3 or jq recommended (needed for audio uploads and `wait`). ffmpeg's ffprobe optional (auto-detects audio length). Get an API key at app.ahacut.com → API keys.
metadata:
  author: Ahacut
  version: "0.1.0"
  category: video
  website: https://ahacut.com
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/ahacut.sh *) Bash(curl *)
---

# Ahacut — AI Motion-Graphics B-Roll Engine

Turn what's being said into b-roll that's already in sync: upload subtitles, a script,
or an audio file and get back a full-length motion-graphics video track (animated text,
numbers, logos, concepts) timed to the words — rendered in the cloud, no local setup.

## Setup

Configure the API key once (get it at **app.ahacut.com → API keys**):

```bash
${CLAUDE_SKILL_DIR}/scripts/ahacut.sh login ak_xxxxxxxx
${CLAUDE_SKILL_DIR}/scripts/ahacut.sh status   # verify + show credit balance
```

(`AHACUT_API_KEY` env var also works and overrides the saved key.)

## Three input modes

| Mode | Command | Use when |
|------|---------|----------|
| **Subtitles (precise)** | `generate-srt <file.srt>` | You have an SRT — cuts land exactly on subtitle timings |
| **Script + duration** | `generate-text <file\|-> <seconds>` | Plain narration text; the AI splits it into scenes and paces them to fit the total length |
| **Audio (mp3/wav)** | `generate-audio <file> [seconds]` | A voiceover/clip — it's transcribed to subtitles, b-roll is generated, and your original audio is muxed back under the video |

**Overlay mode**: add `--overlay` to any `generate-*` command to get a **transparent overlay
track** instead of full-screen b-roll — a ProRes 4444 `.mov` with alpha, designed to sit **on
top of talking-head footage** in any editor (lower-thirds, corner cards, term cards; large
areas stay fully transparent so the speaker shows through). It is silent by design (the voice
lives on the footage below) and the result URL is `.job.result.overlay` (a `.mov`).

**⚠️ Palette: pin it whenever one film is submitted as more than one job.** The server picks
the colour scheme by **hashing the script of that job** — so cutting a film into N jobs gives you
N different colour schemes and the finished timeline looks like it was made by N people. Add
`--palette <id>` to every job of the same film. Ids: `editorial-slate` / `red-alert` /
`deep-teal` / `violet-night` / `amber-doc` / `cyan-steel` (run `limits` for the hex values).
Omit it only when the whole film is a single job.

**Style brief**: `--style-brief "<text>"` (≤500 chars) passes a style preference to the scene
designer. It is a preference, not narration — it is never rendered as on-screen copy.

**Sound effects**: `--sfx` (any generate cmd, Beta, no extra credits) adds a sound-design pass.
The job then also yields `with_sfx` (the final video with the effects mixed in — `download`
prefers it automatically) plus `sfx_wav` / `sfx_cues` / `sfx_jianying` artifacts. The stage is
best-effort: if it fails the job still finishes, just without these artifacts — check for
`.job.result.with_sfx` before assuming the download has sound.

**Caller context** (agents: read this): `--context "<text>"` / `--context-file <path>`
(≤2000 chars) hands the scene designer **your** view of the film.

You only need it when you are **splitting one film into several jobs** — which is what agents do
and web users never do. In that case each job arrives here as a few seconds of orphaned text: the
designer cannot tell whether this beat is setup or payoff, what was said thirty seconds earlier,
or what the neighbouring beats already look like. It ends up composing every job as if it were a
standalone film, which is how you get the same big-type card over and over.

You are the one holding that context, so pass it down. Useful things to put in it:

- what the whole film argues, and where this job sits in that arc
- what the surrounding material is doing (talking head? stock footage? a chart you already used?)
- the visual direction you already decided for this stretch — **if you want a generated
  photographic backdrop, say so here**; the designer honours it
- anything that should not repeat, so consecutive jobs don't converge on one layout

It is guidance, not narration — like `--style-brief`, it never appears on screen. Per-job (unlike
`--palette`, which you keep identical across the film).

```bash
$S generate-srt beat_07.srt --palette deep-teal --context-file beat_07.context.md
```

Each `generate-*` returns a **job** (with an `id` and a `hold_credits` estimate). Generation runs
async in the cloud — poll it with `wait <id>` (or `job <id>`), then read the result URLs.

## All commands

```
login <key> | logout | status | limits | list
generate-srt <file.srt> [--overlay] [--sfx] [--palette <id>] [--style-brief <text>] [--context <text>|--context-file <path>]
generate-text <file|-> <seconds> [--overlay] [--sfx] [--palette <id>] [--style-brief <text>] [--context <text>|--context-file <path>]
generate-audio <file> [seconds] [--overlay] [--sfx] [--palette <id>] [--style-brief <text>] [--context <text>|--context-file <path>]
job <id>                    # status + result download URLs
wait <id> [timeout=1800]    # poll until done/failed, prints the final job
download <id> [out]         # save finished video LOCALLY, prints the local path
download <id> [out] --artifact=<name>   # other deliverables: jy_draft / scenes_zip / with_sfx / sfx_wav / sfx_cues / sfx_jianying
draft <id> [dir] [--force]  # install the JianYing (剪映) draft into the local JianYing drafts folder
```

All go through `${CLAUDE_SKILL_DIR}/scripts/ahacut.sh`. Output is JSON — read `.job.status`
(`queued → authoring → render_ready → running → done|failed`) and, when `done`,
`.job.result.with_audio` / `.job.result.broll` (or `.job.result.overlay` for `--overlay` jobs;
signed download URLs) and `.job.charged_credits`.

## Delivering the result (important)

The result URLs are **remote signed links**. Most agent frameworks can only hand the user a
**local file**, not a URL — so after the job is `done`, **download it to a local file first**,
then deliver that path:

```bash
$S wait <job_id>
LOCAL=$($S download <job_id>)     # saves the mp4 locally, prints its absolute path
# now deliver "$LOCAL" via your normal file-delivery mechanism
```

Prefer `.with_audio` (b-roll + the original voiceover) over `.broll` (visuals only) — `download`
picks `.with_audio` automatically when present. Do **not** pass a remote URL to a delivery tool
that expects a local file (that yields an empty/failed artifact).

## JianYing (剪映) users: install the draft directly

Every finished job also ships `.job.result.jy_draft` — a **ready-made JianYing draft**: each
scene is a clean clip already placed at its exact timecode on the timeline. If the user edits
in JianYing (剪映专业版) on THIS machine, skip the download-and-import dance entirely:

```bash
$S draft <job_id>       # downloads + installs into the local JianYing drafts folder
```

Then tell the user to open JianYing — the draft (named `ahacut_…`) is in the draft list with
the timeline already laid out. Rules the command enforces (worth knowing):

- **JianYing must be fully quit** during install — drafts written while it runs get flagged
  as "corrupted" (they aren't; it's a race with JianYing's async takeover). The command aborts
  with a clear message if it detects JianYing running; `--force` overrides.
- If no local JianYing install is found, it extracts to the current directory and prints
  where to move the folder manually (also useful for handing off to another machine:
  `draft <id> <dir>` extracts to `<dir>` without installing).
- **Handing the zip to a human on another machine?** The zip already contains double-click
  installers — `Install-Mac.command` (macOS; first run: right-click → Open) and
  `Install-Windows.bat` (Windows). Tell them to unzip and double-click the one for their OS;
  it finds the drafts folder itself and opens the JianYing download page if it isn't installed.
  Do NOT run those installers yourself — they pause for keyboard input (designed for humans);
  `draft <id>` is the non-interactive equivalent for agents.
- If JianYing complains about missing media on open: click 链接媒体 and point it at the
  `assets/` folder inside the draft.

## Workflow patterns

### From an SRT (most precise)
```bash
S=${CLAUDE_SKILL_DIR}/scripts/ahacut.sh
$S generate-srt captions.srt            # -> note the job id
$S wait <job_id>                        # waits, prints final job with result URLs
# download the track from .job.result.with_audio (or .broll)
```

### From a script + length
```bash
$S generate-text script.txt 90          # 90-second video; or:  echo "my script" | $S generate-text - 90
$S wait <job_id>
```

### From a voiceover
```bash
$S generate-audio voiceover.mp3         # auto-detects length if ffprobe present; else: generate-audio voiceover.mp3 120
$S wait <job_id>
```

## Notes for the agent

- **Check `status` / `limits` first** if unsure — `limits` shows max file size, max video length,
  whether audio mode is enabled, and the trial cap.
- **Cost**: jobs hold credits up front (≈ seconds × rate) and settle on completion; a failed render
  is auto-refunded. Tell the user the `hold_credits` / `charged_credits` from the JSON.
- **Don't poll in a tight loop** — use `wait`, which backs off (4s) and prints progress.
- Audio mode needs the server to have object storage + the speech-to-text backend enabled; if
  `limits.audioEnabled` is false, use SRT or text mode instead.
- Never print the full API key back to the user.
