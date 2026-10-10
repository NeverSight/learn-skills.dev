---
name: meeting-brief
description: Transcribe meeting or call recordings, archive them under the project's arch/ folder, and brief you back as a spoken audio link instead of a wall of text. Use this whenever you point at audio or video recordings and want them transcribed, summarised, "read", or turned into a meeting report, and whenever you ask for a briefing, recap, or rundown of a call. Also use it for the audio-reply mode on its own ("send it as audio", "give me a link", "voice mode", "audio only", "1.5 velocity", "just talk to me"), where every answer is delivered as a presigned S3 audio link rather than text. Handles ElevenLabs Scribe v2 diarised transcription, the arch/ archive convention, ElevenLabs TTS at arbitrary playback speed, per-project AWS credential resolution, presigned private links, and deleting each clip once you have replied. Also owns the Meeting Capture browser extension (Meet, Zoom web and Teams web calls auto-record with no click into a private S3 inbox; video only from a manual start) and the ingest flow that pulls those recordings in, so "I just had a call", "process my meetings", "check the meeting inbox", "any new recordings" and "set up meeting recording" are this skill too, and any mention of a call starts by checking that inbox. Trigger it even when the words "transcribe" or "skill" never appear — "read my meeting", "what did we decide on the call", "brief me", "file this call" and "send that as audio" are all this skill.
---

# Meeting brief

Two things that compose: turn recordings into an archived meeting report, and talk back to you in audio instead of text.

Either half works alone. `/meeting-brief` on a folder of `.m4a` files does the first. "answer me in audio from now on" does the second.

## Hard rules

- **Never upload the user's audio to a public host.** Not tmpfiles, not 0x0.st, not transfer.sh, not a quick tunnel. These recordings can contain confidential information: salary negotiations, equity terms, revenue, customer names. The only sanctioned channel is a presigned S3 URL in a private bucket. This rule exists because it was broken once.
- **Presigned only, private ACL.** Never `--acl public-read`, never a bucket policy change, never a bucket whose name contains `public` or `assets`.
- **Delete each clip once the user replies.** Their next message is the signal they have listened. Run `unshare.sh` on the previous object before doing anything else in that turn.
- **Never echo an API key or secret** into the transcript. The scripts read them from the environment or a `.env` and never print them.

## AWS credentials come from the project, never from a global profile

A project can keep its own `.env` with its own AWS account, so credentials are resolved from the project rather than a global profile. `scripts/aws-env.sh` walks up from the working directory to the first `.env` that yields usable credentials.

Variable names are not always standardised. The resolver tries canonical `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` first, then the short forms `AWS_ACCESS_KEY` / `AWS_ACCESS_SECRET`. Region falls back to `us-east-1`, then gets corrected per bucket via `get-bucket-location`.

Set `MEETING_BRIEF_BUCKET` to the private bucket the audio should go to. It must have public access blocked; this skill uploads with a private ACL and shares only via presigned URL, and never makes anything world-readable.

## Flow A: recordings to archived report

```bash
S=.claude/skills/meeting-brief/scripts
OUT=/tmp/claude/<project>/meeting-<date>

$S/transcribe.sh $OUT *.m4a                     # parallel, diarised, resumable
$S/format-transcript.mjs $OUT/raw-<x>.json \
    --map speaker_0=Alice,speaker_1=Bob          # speaker-grouped, timestamped
```

Then read the transcripts, identify who is who from context, and write the report.

**Always pass keyterms.** `keyterms.txt` ships with this skill and `transcribe.sh` sends it automatically. Without it Scribe v2 mangles unusual product, company or tool names into similar-sounding common words, which then poisons every downstream summary. Add your project's nouns to that file as they come up.

Diarisation gives `speaker_0`, `speaker_1`, not names. Work out the mapping from the content before writing anything, and say in the summary which label is whom. For load-bearing facts (who owns a follow-up, who is off tomorrow, personal context) confirm WHO with the user before saving if the mapping is at all ambiguous, and write the draft as "I put X on speaker A and Y on speaker B, flip if backwards" so they can correct fast.

### Quota (`quota_exceeded`)

Scribe v2 charges about 1.1 credits per second of audio. On `quota_exceeded`, do not give up: most long meetings have silent gaps (pre-start setup, dead air, long pauses). Use `ffmpeg` to strip silence and retry:

```bash
ffmpeg -y -i input.m4a \
  -af "silenceremove=stop_periods=-1:stop_duration=2:stop_threshold=-40dB" \
  -c:a aac -b:a 64k trimmed.m4a
```

That removes 20-40% of duration with zero speech loss. Re-check duration (`ffprobe`) and recompute credits before resubmitting. Archive the ORIGINAL audio, never the trimmed copy: the trim is a transcription-time artifact, not the source of truth.

### Ingesting the recording (dating, sequencing, archive-first)

Recordings arrive however the project delivers them: a drop in the workspace root, an export in `~/Downloads`, a phone file, or an auto-upload to the S3 inbox. The name is usually generic (`meet.m4a`, `rec.m4a`, `audio 3.m4a`) and carries no reliable date. Four rules hold regardless of source:

- **Archive BEFORE summarising, always.** The moment transcription succeeds, write the `<audio>` + `.txt` pair into `arch/transcripts/` BEFORE the report, action items, or anything else, even if the user only asked "what did they decide". They should never have to ask for the archive. Verify it landed (checksum the copy against the source) rather than assuming.
- **The date is the RECORDING date, never today and never the download date.** A file's mtime is the copy/export time: for a fresh same-day drop that equals the meeting date, but an exported or re-shared file can be days off, and several files exported in one session share one mtime. Cross-check against the transcript (weekday mentions, "yesterday we shipped X", a recent-changes log) and the gap since the last `arch/transcripts/` file. Only ask the user when the evidence disagrees. If the source is an Apple Voice Memos original (`20260806 104557.m4a`), that filename IS the start time: match the shared copy back to it by byte size then checksum, and a match is proof, so no need to ask.
- **Sequence number:** take the highest existing `rec-NNN` in `arch/transcripts/` and use the next integer; say so in chat so the user can correct a skipped one. If the export name already carries a number (`Mi grabación 202.m4a` -> `rec-202`), keep it. Never leave a recording unarchived just because the number is uncertain.
- **A drop box is not storage.** When recordings land in a shared drop location (workspace root, a Downloads folder, an S3 inbox), MOVE the file into `arch/transcripts/` once the archived copy is checksum-verified, then delete the source so the next drop is unambiguous. Two or more audio files waiting at once means several meetings: process oldest first or ask which, never merge them.

### The archive convention

Archiving is an optional convention. Keep an `arch/` tree at the **workspace root**, spanning every repo in that workspace. If an `arch/README.md` already exists in the project, follow its layout; otherwise this is a sensible default:

```
arch/
  README.md
  meetings/     YYYY-MM-DD-<counterpart>-<topic>.md
  transcripts/  YYYY-MM-DD-rec-<N>.txt  +  the original .m4a alongside
  reports/      YYYY-MM-DD-<topic>.md
```

A typical report skeleton: TL;DR, Action items, Decisions, Things to remember, Open questions, What's done / in progress, Topics. Two conventions are worth keeping:

- **No em dashes anywhere.** Hyphens, colons, periods, parentheses.
- **Every action item needs a named owner.** "Someone should" is not an action item.
- Never paste a full transcript into the report. Link to the file under `transcripts/`.

Get real durations with `ffprobe` rather than estimating from file size:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 file.m4a
```

## Flow C: ingest from the S3 inbox (browser extension)

The `extension/` folder here is a browser extension that auto-records web meetings (Google
Meet, Zoom web, Teams web) and uploads them to a private S3 inbox, so you never have to
phone-record or hand over files. A recording lands as `inbox/<workspace>/<ts>-<title>.webm`
plus a `.json` sidecar (platform, title, meeting url, participants, start/end, mic-captured
flag, contentType). See `extension/README.md` for the capture side and
`ingest/presign-lambda/` for the endpoint.

**The inbox is the FIRST place to look whenever the user refers to a call**, not only when
they say "check the inbox". "I just had a call", "what did we decide on the call",
"transcribe my last meeting", "process my meetings" all start here, before asking for a
file. Only if the inbox has nothing that fits do you fall back to the project's dropped-file
locations (Flow A) and then ask.

```bash
I=.claude/skills/meeting-brief/ingest/ingest.sh   # set MEETING_INBOX_BUCKET + AWS creds (env or AWS_PROFILE)

$I list                                        # pending clips, newest first: title | start | participants
$I pull inbox/<ws>/<file>.webm /tmp/claude/<project>/meeting-in
```

Pick the clip by **time first** (a call "just had" ends within the last hour or two;
`startedAt`/`endedAt` are in the sidecar), then by title/participants matching who was named.
If two or more clips fit, list them and ask which, do not guess.

**Always convert to `.m4a` first, then run the normal Flow A on the `.m4a`:**

```bash
ffmpeg -v error -i clip.webm -vn -c:a aac -b:a 64k clip.m4a   # then transcribe clip.m4a
```

Two reasons it is not optional. A call whose tab was closed mid-call (sidecar `reason:
tab_closed` or `stalled`) arrives as a webm with no proper ending ("File ended prematurely"):
ffmpeg decodes it fine, Scribe may not. And a manual recording with video on is
`video/webm`; `-vn` drops the video. Keep the original video only if the user wants to rewatch.
The sidecar's `capture` says how it was recorded: `page` is automatic (call audio + the user's
mic taken inside the meeting page), `tab` is a manual popup recording.

**Routing: the meeting's subject decides the archive, not the session you are in and not
the tag.** The `workspace` tag is just the default set on the browser that recorded it (one
browser can record calls for several projects), so a call can easily arrive tagged for the
wrong one. Decide from what the meeting is about: the people on it, the title, the topics in
the transcript. Say in chat which project you filed it under and why, then archive straight
into that project's `arch/`.

If you cannot tell from the sidecar and do not want to spend credits transcribing it in the
wrong project, hand it over untouched: `$I retag <key> <workspace>`. Transcode to `.m4a`
with `ffmpeg` before archiving so the archive matches the usual `.m4a` convention. When the
pair is archived and checksum-verified:

```bash
$I done inbox/<ws>/<file>.webm                 # deletes the clip + sidecar from the inbox
```

The inbox is a drop box, not storage (same rule as any dropped recording in Flow A):
delete each clip only after its `arch/transcripts/` copy is verified.

### The capture side: install, ship a change, debug

- **How it records, and the one thing not to undo.** Automatic recordings happen inside the
  meeting page (`extension/capture.main.js`, a `world: MAIN` content script that wraps
  `RTCPeerConnection` and `getUserMedia`). Never move auto-start back to `chrome.tabCapture`:
  Chrome only allows tab capture after a click on the extension, so it cannot start on its own,
  and v0.1/v0.2 recorded nothing on the first real Meet call because of it. Tab capture is only
  the popup's manual Start, which is also the only way to get video. Full design in
  `extension/README.md`.
- **Install or update:** run the install one-liner your deployment prints
  (`curl -fsSL <your-endpoint>/install | sh`), then `chrome://extensions` -> Load unpacked
  (first time; `Cmd+Shift+G`, paste) or the reload arrow (update). Loaded unpacked from a
  stable folder, the extension keeps the same ID across updates, so the token in Options
  survives updates. Never load it from Downloads.
- **Ship a change to the extension:** edit `extension/`, bump `manifest.json` `version`, then
  `cd ingest/presign-lambda && BUCKET=<your-inbox-bucket> TOKEN=<current> ./deploy.sh`
  (with AWS creds for your account in the environment; the token is in the Lambda env, see
  `extension/README.md`). That re-bundles the zip served at `/extension`; re-run the install
  line and hit reload. Prove a recorder change on a real WebRTC call before calling it done
  (the README describes the Chromium harness).
- **"Did my call record?" and the inbox is empty:** ask the endpoint, not the code.

  ```bash
  aws cloudwatch get-metric-statistics --region us-east-1 --namespace AWS/ApiGateway \
    --metric-name Count --dimensions Name=ApiId,Value=<your-api-id> --statistics Sum --period 300 \
    --start-time $(date -u -d '-3 hours' +%FT%TZ) --end-time $(date -u +%FT%TZ)
  ```

  No requests during the call: the browser never tried (auto-record off, no token, an old
  build still on tab capture, or the page hook missed the call). 4xx: token or endpoint
  wrong. A presign with nothing in S3: the PUT failed. The popup's last-upload line is the
  browser's side of the same story.
- **Status:** confirmed on a real Google Meet call (2026-10-01, v0.3.0): started with no
  click (even alone in the call), mic captured, stopped on hang-up, uploaded, transcribed
  cleanly. Zoom web and Teams web use the same recorder but are not yet confirmed live. For a
  `meet.new` call the title is just the meeting code; a calendar meeting carries its name.
  Participant names are best-effort and often empty, so identify people from the transcript.

## Flow B: audio-reply mode

The user reads on their phone and often cannot skim a long answer. In this mode every substantive reply is spoken.

```bash
S=.claude/skills/meeting-brief/scripts

# 1. delete the clip from the previous turn; they have replied so they have heard it
$S/unshare.sh "s3://<bucket>/<previous-key>" <project-dir> <previous-local-file>

# 2. write the reply as a SPOKEN script, then
$S/say.sh reply.txt /tmp/claude/<project>/reply-<n>.mp3 1.5

# 3. private link
$S/share.sh /tmp/claude/<project>/reply-<n>.mp3 <project-dir>
```

Then post the URL with **two or three lines of text at most**: what the clip covers and anything they must act on. Not a transcript of the audio. The point of the mode is that they do not have to read.

Keep a note of the returned `s3://` URI and the local path so the next turn can delete them.

**Default speed is 1.5.** ElevenLabs' own `speed` setting maxes out at 1.2, so `say.sh` renders at normal speed and applies the change with `ffmpeg atempo`, chaining filters for anything outside 0.5-2.0. Pitch is preserved.

### Writing for the ear

Reading markdown aloud is unlistenable. Convert before calling `say.sh`:

- Spell numbers out: "four hundred ninety-nine a month", not "$499/mo".
- No file paths, no URLs, no code identifiers. Those go in the text message beside the link.
- No bullet characters, no headers, no bold. Use "First", "Second", "The next thing" instead.
- Say acronyms as letters where that is how they are said: "M R R", "U X", "U I".
- Warn about known transcription mangling up front if the summary depends on it.
- Blank lines between paragraphs. `say.sh` chunks on those boundaries and stitches with `previous_text` / `next_text` so prosody carries across the joins.

Default voice is a calm broadcast read (`onwK4e9ZLuTAKqWW03F9`). Override with `MEETING_BRIEF_VOICE`. Model defaults to `eleven_multilingual_v2` via `MEETING_BRIEF_MODEL`.

## Scripts

| Script | Does |
|---|---|
| `scripts/transcribe.sh <outdir> <audio>...` | Scribe v2, diarised, keyterms, parallel, skips existing output |
| `scripts/format-transcript.mjs <raw.json> [--map s0=Name,...]` | Timestamped, speaker-grouped transcript |
| `scripts/say.sh <script.txt> <out.mp3> [speed] [voice]` | Chunked TTS, stitched, speed-adjusted |
| `scripts/share.sh <file> [project-dir] [expires]` | Private S3 upload, presigned URL (7 day max) |
| `scripts/unshare.sh <s3-uri> [project-dir] [local-file]` | Deletes the object and optionally the local file |
| `scripts/aws-env.sh` | Per-project credential resolution, sourced by the above |
| `scripts/lib.sh` | ElevenLabs key loading |
| `scripts/extension-icons.mjs` | Regenerates the extension's toolbar icons (idle + recording) |
| `ingest/ingest.sh {list,pull,done,retag}` | The S3 meeting inbox (Flow C) |
| `ingest/presign-lambda/deploy.sh` | Redeploys the endpoint and re-bundles the extension zip served at `<your-endpoint>/extension` |

`ELEVENLABS_API_KEY` is read from the environment. `ELEVENLABS_ENV_FILE` can point at a local `.env` that defines it when it is not already in the environment.

## Environment notes

- **Backgrounding with `&` or `nohup` may not survive the tool call.** Use the Bash tool's `run_in_background` instead, which is the reliable way to hold a process.
- **A presigned URL is signed per HTTP method.** `curl -I` against a GET-signed URL returns 403 and that is correct, not a failure. Verify with a ranged GET: `curl -r 0-2000 "$URL"`.
- `ffmpeg` and `ffprobe` are required (install them with your package manager).
- Keep scratch files out of the repo (e.g. under `/tmp/claude/<project>/`).

## When not to use

- A short factual answer. Do not make the user play a clip to hear one sentence.
- Anything they need to copy and paste: paths, URLs, commands, IDs. Those must be text.
- Code review or diffs. Audio is useless for reading code.
