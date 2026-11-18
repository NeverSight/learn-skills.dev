---
name: proofread
description: Transcribe a video with Sonilo and translate the transcript into editable .srt files — one per target language, plus the detected source language — so the wording can be read and corrected before anything is dubbed. Nothing is spoken and no video is produced; this is the step before dubbing, and the corrected files go back to the dubbing tool as subtitles so the dub speaks exactly the approved lines. Use when the user wants to review, approve or fix the translation before dubbing, wants editable subtitles or a transcript of a video, or wants the dub to say their exact wording. Billed per target language (a transcript-only run counts as one), with 2 free-trial runs on self-serve accounts — confirm the language list with the user before calling.
license: MIT
compatibility: "Requires Sonilo through either transport — the MCP server connected, or the `sonilo` CLI installed and signed in — plus credentials: a `sonilo login` sign-in, the hosted OAuth plugin, or SONILO_API_KEY. See the setup-api-key skill."
allowed-tools: Bash, Read, Write, mcp__sonilo__*
---

# Sonilo Proofread

Transcribe a video and translate the transcript into the target languages,
returning **one editable `.srt` per language plus the source-language
transcript**. Nothing is voiced, nothing is re-rendered, no video comes back.

This is the step **before** [auto-dubbing](../auto-dubbing): the user reads and
corrects the translated scripts, and the corrected files then go to `dubbing`
as `subtitles`, so the dub speaks exactly the approved wording instead of the
pipeline's own translation.

> **Setup:** See the [setup-api-key](../setup-api-key) skill.

> ⚠️ **Cost — read before calling:** this is billed **per target language** — video seconds × the number of target languages, at $0.001/sec with a 10-second billing floor. A transcript-only request (no `languages`) counts as one. Self-serve accounts get **2 free-trial runs**; after that it bills normally. Confirm the exact language list with the user before calling; do not guess a long list "to be helpful."

## When to reach for this

Use it when:

- **The user wants to see or fix the translation before it is spoken.** "Let me
  check the Spanish first", "our team has to approve the copy", "the product
  name keeps getting mangled" — all of it is this call, not a dub followed by a
  re-dub.
- **The user wants editable subtitles** or a plain transcript of a video, with
  no dubbing in sight. Omit `languages` for the source-language transcript
  alone.
- **A previous dub said the wrong thing.** Proofread, correct the script, then
  dub with `subtitles`. Re-dubbing without a script just pays for the same
  translation twice.

Do **not** use it when the user just wants the video dubbed and has no interest
in the wording — that is one `dubbing` call, and inserting a proofread in front
of it is an extra charge they did not ask for.

## Transport: MCP or CLI

Pick one at the start of the session and stay on it. Do not mix the two inside
a single job, and do not announce the choice.

1. **Sonilo MCP tools visible in this session** (`proofread` and friends) — use them. This is the preferred path: it needs no shell, and it is the only one that survives a very long generation. If a call fails to authenticate — rather than failing on its inputs — this transport is not usable in this session: go to 2 instead of retrying it.
2. **No usable Sonilo MCP tools, but `sonilo account` exits 0** — use the CLI commands below. Same API, same account, same credential file. Probe with `sonilo account`, not `sonilo whoami`: whoami exits 0 even when signed out, so it cannot tell the two states apart.
3. **Neither** — stop and run the [setup-api-key](../setup-api-key) skill. Do not call `api.sonilo.com` with curl to work around it; both transports handle uploads, polling and retries that a bare request does not.

### One difference between the two MCP servers

`proofread` takes a **local file only on the local server**. The hosted (OAuth
plugin) server is URL-only: it exposes `video_url`, `languages` and
`source_language` and nothing else — no `video_path` to read a file from, and
no `output_directory`, because it has no filesystem. There the `.srt` URLs come
back on the task and you fetch them yourself. If the user's video is a local
file and you are on the hosted server, do not try `video_path` — it is not a
parameter there. Upload the file with the hosted server's `create_upload_url`
tool and pass the `file_url` it returns as `video_url` (steps in
[preflight](../references/preflight.md), Step 4), or use the CLI or an SDK.

Unlike `dubbing`, this call is quick: a few-minute clip with a handful of
languages typically finishes in well under a minute, so the ordinary timeout is
enough and there is no submit-and-poll dance to plan for.

## Quick Start

### MCP tool call (recommended)

```
proofread(
    video_path="~/Desktop/product-demo.mp4",
    languages=["es", "fr"]
)
```

On the **hosted** server, pass a URL instead — it is the only input there:

```
proofread(video_url="https://example.com/product-demo.mp4", languages=["es", "fr"])
```

The transcript alone, with no translation, is the same call with `languages`
left out:

```
proofread(video_path="~/Desktop/product-demo.mp4")
```

A hint for the spoken language, for short or noisy audio:

```
proofread(video_path="~/Desktop/product-demo.mp4", languages=["es"], source_language="en")
```

On the local server the files are saved for you (see [Output
Files](#output-files)); `output_directory` says where.

### Python (`pip install sonilo`)

```python
from sonilo import Sonilo

client = Sonilo()  # reads SONILO_API_KEY

result = client.proofread.generate(
    video="product-demo.mp4",
    languages=["es", "fr"],
    # Optional hint; omit to have the spoken language detected.
    source_language="en",
)
print(result.source_language, result.cue_count)

# Writes scripts/proofread.<language>.srt — including the source language.
for language, path in result.save_all("./scripts").items():
    print(language, path)

for language, issues in result.warnings.items():
    for issue in issues:
        print(language, issue.cue, issue.code, issue.severity)
```

### JavaScript / TypeScript (`npm install sonilo`)

```ts
import { SoniloClient } from "sonilo";
import type { ProofreadResult } from "sonilo";

const client = new SoniloClient(); // reads SONILO_API_KEY

const result: ProofreadResult = await client.proofread.generate({
  video: "./product-demo.mp4",
  languages: ["es", "fr"],
  sourceLanguage: "en", // optional hint
});
console.log(result.source_language, result.cue_count);

// Presigned .srt URLs — they expire, so fetch them promptly. There are no
// download helpers on this result; use download()/fetch() as elsewhere.
for (const [language, url] of Object.entries(result.subtitles ?? {})) {
  console.log(language, url);
}
```

### CLI (`npm install -g sonilo-cli` or `pip install sonilo-cli`)

```bash
sonilo proofread --video clip.mp4 --languages es,fr --output scripts/clip.srt
# writes scripts/clip.en.srt (the detected source), scripts/clip.es.srt, scripts/clip.fr.srt
```

`--output` is a **filename template, not one destination**, exactly as it is on
`sonilo dubbing`: the language code is spliced in before the extension, and
missing directories are created. It defaults to `proofread.srt`. After the
files, the command prints the detected source language, the cue count, and one
line per non-blocking warning.

```bash
# Transcript only, from a URL, with a hint for the spoken language.
sonilo proofread --video-url https://example.com/clip.mp4 --source-language en

# --timeout is the CLI's own wait (default 2700 seconds). If it does expire, the
# task keeps running server-side.
sonilo proofread --video clip.mp4 --languages ja --timeout 300
sonilo tasks wait <task-id>
```

### cURL (raw REST API, no MCP host)

```bash
curl -X POST "https://api.sonilo.com/v1/proofread" \
  -H "Authorization: Bearer $SONILO_API_KEY" \
  -F "video=@product-demo.mp4" \
  -F 'languages=["es","fr"]' \
  -F "source_language=en"
# -> 202 {"task_id": "...", "status": "processing"}

curl "https://api.sonilo.com/v1/tasks/<task_id>" -H "Authorization: Bearer $SONILO_API_KEY"
```

`languages` is a **JSON array string**, the same wire shape as dubbing's.
`video_url` is accepted instead of an uploaded file and **must be https** — the
backend fetches the source itself and rejects plain http. Pass one or the
other, never both.

## Tool

| Tool | Description |
|------|-------------|
| `proofread(video_path? \| video_url?, languages?, source_language?, output_directory?)` | Transcribe a video and translate the transcript into the requested languages; one editable `.srt` per language plus the source-language transcript. Voices nothing and produces no video. `video_path` and `output_directory` exist on the local server only — the hosted server is `video_url`-only. |

## Parameters

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `video_path` | string | — | Local server only. Absolute path, or relative to `SONILO_MCP_BASE_PATH`. Max **300s (5 min)**, max **300 MB**, and **the video must have an audio track** — there is nothing to transcribe without one, so a video lacking one is rejected rather than transcribed. |
| `video_url` | string | — | **Must be https** (not just http). Exactly one of `video_path`/`video_url`. The only input the hosted server accepts. Same 300s / 300 MB / audio-track rules. |
| `languages` | list[str] | — (transcript only) | Target languages to translate the transcript into, e.g. `["es", "fr"]`. **The same codes as `dubbing`** — see the [auto-dubbing](../auto-dubbing) skill's `languages` row for the list and for what `pt_br`, `es_419`, `pa_in` and `sd_in` mean — so a proofread script can go straight into a dub. Omit it, or pass `[]`, for the source-language transcript alone. An unsupported code is a `422` before anything is charged. **Billed per language**, so this list is the price. |
| `source_language` | string | — (detected) | A hint telling transcription which language to expect, one of the same codes. It helps on short, noisy or mixed-language audio. Omit it to have the language detected; either way the result reports the language the transcript is actually in, and that detected code keys the source-language file. Free — it is a hint, not an extra language. |
| `output_directory` | string | `SONILO_MCP_BASE_PATH` | Local server only. Absolute, or relative to the base path. |

## What comes back

```json
{
  "task_id": "…",
  "status": "succeeded",
  "source_language": "en",
  "subtitles": {
    "en": "https://…/en.srt",
    "es": "https://…/es.srt",
    "fr": "https://…/fr.srt"
  },
  "cue_count": 65,
  "warnings": {
    "fr": [
      {"cue": 33, "code": "high_text_speed", "severity": "warning", "characters_per_second": 26.92}
    ]
  },
  "duration_seconds": 206.32
}
```

- **`subtitles`** maps a language code to a downloadable `.srt` URL, and
  **always includes the detected source language** on top of every requested
  target — so a one-language request comes back with two files, and a request
  with no `languages` at all still comes back with one. The URLs are presigned
  and expire: save the files rather than handing the user a link.
- **`source_language`** is the language the transcript is in, whatever hint was
  sent. It is the key the source-language file appears under.
- **`cue_count`** is the number of subtitle cues in the source script. Every
  language has the same count.
- **`warnings`** maps a language to **non-blocking** issues in its script, and
  is empty when there are none. Each issue carries `cue` (1-based), `code`,
  `severity`, plus whatever measurement that code brought with it (e.g.
  `characters_per_second` on `high_text_speed`). A warning **never** withholds a
  file or fails the task — surface it as something the user may want to tighten
  while editing, not as an error.

## Proofread → Edit → Dub

The two calls are halves of one workflow. Run them in this order:

1. **Proofread** the video into the target languages.
2. **Hand the `.srt` files to the user to read and correct.** That is the whole
   point of the call — do not silently pass them straight through. Rewriting
   them yourself is a translation the user never approved.
3. **Dub with `subtitles`**, keyed by language, so the dub speaks those lines
   verbatim:

   ```
   dubbing(
       video_path="~/Desktop/product-demo.mp4",
       languages=["es", "fr"],
       subtitles={"es": "./scripts/clip.es.srt", "fr": "./scripts/clip.fr.srt"}
   )
   ```

   ```bash
   sonilo dubbing --video clip.mp4 --languages es,fr \
     --subtitle es=scripts/clip.es.srt --subtitle fr=scripts/clip.fr.srt
   ```

**Drop the source-language file.** Proofread always returns it; `dubbing`'s
`subtitles` keys must equal its `languages` **exactly**, so passing the source
language through is an extra key and a `422`. The same goes the other way: every
language being dubbed needs a script, so if the user only corrected two of three
files, ask for the third rather than dropping `subtitles` — a bare `languages`
list would silently deliver the pipeline's own translation instead.

See the [auto-dubbing](../auto-dubbing) skill for the rest of the script rules
(`.srt`/`.vtt` only, 1 MiB each, target-language text, and `export_srt` to get
each language's lines re-timed against the delivered audio).

## Workflow Tips

- **Always ask which language(s)** before calling — the list is what you are
  billed for, and unlike `dubbing` there is no server-side default here: omit
  `languages` and you get the transcript alone, charged as one language.
- **Proofread is cheap next to a wrong dub.** It is per second at $0.001 with a
  10-second floor, while a dub the user rejects is a full per-language charge
  thrown away. If the user cares about the wording at all, proofread first.
- **Use `source_language` when the audio is hard.** Short clips, background
  noise, or a speaker switching languages are exactly where detection slips, and
  a hint costs nothing.
- **It transcribes speech.** A video with no audio track is rejected outright,
  and one whose audio has no speech comes back `failed` with
  `TRANSCRIPTION_EMPTY` — a caller-input verdict, not a backend fault. Check the
  clip before re-running it.
- **This is not the music or SFX skills** ([text-to-music](../text-to-music),
  [video-to-music](../video-to-music), [text-to-sfx](../text-to-sfx),
  [video-to-sfx](../video-to-sfx)) and it is not
  [video-analysis](../video-analysis), which briefs the *sound* of a video. This
  one only reads out the words.
- Check `get_account_services` (see the [account](../account) skill) if you are
  unsure whether the account's 2 free runs remain before calling.

## Recovering a Timed-Out Call

`proofread` is async: the backend accepts and charges the task, then a worker
runs it. If the call's own wait is interrupted, the error message — or the task
id printed at submission — gives you a `task_id`. Call `get_sfx_task(task_id)` —
`get_generation_task(task_id)` on the hosted server — to check status and
download the finished `.srt` files; see [task-recovery](../task-recovery). On
the CLI, `sonilo tasks wait <task-id>` resumes the wait.

Do **not** re-run `proofread` after a timeout. That is a second charge for
scripts you already own.

## Output Files

On the local MCP server, one `.srt` per language lands in `output_directory`,
named `proofread-<first 8 chars of the task id>.<language>.srt` — there is no
prompt to name files after, so the task id is the only stable name. The set
always includes the detected source language. After the files, the tool reports
the detected `source_language` and `cue_count`, then one note per warning; a
language whose `.srt` could not be downloaded is a note carrying the task id,
not a failure.

On the CLI, the files follow the `--output` template
(`--output scripts/clip.srt` writes `scripts/clip.en.srt`,
`scripts/clip.es.srt`, …), so `--output` names the template, not one file.

The hosted server and the raw API return the URLs instead; fetch them before
they expire.

## Error Handling

Common errors: `401` invalid key, `402` insufficient balance / trial exhausted,
`413` file too large, `422` invalid parameters (an unsupported language code,
both or neither of `video_path`/`video_url`, a non-https `video_url`), `429`
rate limit. An unsupported language code is a `422` before anything is charged.

A video over the 300s cap, over 300 MB, or with no audio track is rejected
rather than transcribed. Both MCP servers check the duration before the request
is made, and the hosted server also checks for an audio track, so those reach
you as a tool error rather than as an HTTP status; the local server leaves the
audio-track check to the API.

A failed task carries an `error.code` of `SOURCE_DOWNLOAD_FAILED`,
`SOURCE_PROCESSING_FAILED`, `TRANSCRIPTION_EMPTY`, `TRANSCRIPTION_FAILED`,
`TRANSLATION_FAILED`, `PREFLIGHT_BLOCKED`, `PREFLIGHT_UNAVAILABLE` or
`TRANSFER_FAILED`, and is refunded. `TRANSCRIPTION_EMPTY` means the audio had
no speech in it — re-running the same clip cannot fix that.

A `503` means proofread is temporarily disabled server-side; it is not a key or
balance problem and no retry loop will fix it. See the [account](../account)
skill to check trial/usage before a call.
