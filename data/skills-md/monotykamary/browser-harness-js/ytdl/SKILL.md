---
name: ytdl
description: >-
  Download YouTube videos browser-natively — no `yt-dlp`, no client impersonation,
  no n-signature solver. The browser plays the video (auth, poToken, n-solving,
  SABR demux all done by the page itself); ytdl records the demuxed media the
  player feeds to MediaSource via a `SourceBuffer.appendBuffer` hook and muxes
  to MP4 with ffmpeg. If the user can watch the video, it's downloadable —
  made-for-kids, age-gated, and members-only work as long as a logged-in tab
  can play them. Use when the user wants to download, save, or fetch a YouTube
  video (audio or video) to disk.
setup: bash <skill-dir>/scripts/setup
compatibility: Requires `browser-harness-js` on PATH + a Chromium browser with remote debugging (see the `cdp` skill) and a logged-in YouTube tab for gated content. `ffmpeg` on PATH to mux video+audio into MP4.
---

# ytdl — browser-native YouTube downloader

A thin `browser-harness-js` heredoc, exactly like `gsearch`/`xsearch`. There is
**no Bun program, no vendored solver, no HTTP client impersonation**. Every
hard thing YouTube does to play a video — cookies, poToken, the n-signature,
the SABR multiplex, adaptive-bitrate selection — the page already does for
playback. ytdl just records the result.

```bash
ytdl "https://www.youtube.com/watch?v=..."            # best quality → ~/Downloads
ytdl "https://www.youtube.com/shorts/<id>"            # Shorts — normalized to watch?v=
ytdl "https://www.youtube.com/watch?v=..." -q 360p    # 360p
ytdl "https://www.youtube.com/watch?v=..." -q 1080p   # 1080p (ffmpeg mux)
ytdl "https://www.youtube.com/watch?v=..." -q audio   # audio only
ytdl "https://www.youtube.com/watch?v=..." --info      # title / duration / qualities
ytdl "https://www.youtube.com/watch?v=..." -o Name -d ~/Videos
```

## Quality targets

| `-q`     | what happens | needs ffmpeg? |
|----------|--------------|---------------|
| `360p` / `480p` / `720p` / `1080p` / `1440p` / `2160p` | force that player quality, capture, mux | yes |
| `best`   | let the player pick (highest it offers) | yes |
| `audio`  | force the smallest video, keep only the audio buffer | no |

ffmpeg is a **muxer only** here — the player delivers video and audio as
separate ISO-BMFF (fragmented-MP4) streams, so they need combining into one
file. It never re-encodes (`-c copy`); the output stays pure (lossless) at
YouTube's own codecs. If you need a QuickTime/iOS-friendly file, re-encode the
output yourself in one step — see Traps.

## How it works

All inside one `browser-harness-js <<EOF` heredoc, gsearch-style:

1. **Connect** to the browser's shared CDP session (or `session.connect()`).
2. **`Page.addScriptToEvaluateOnNewDocument`** — inject the MSE hook *before*
   any page JS runs:
   - Wrap `MediaSource.prototype.addSourceBuffer` (via `Object.defineProperty`)
     so each `SourceBuffer` is tagged with its mime (video/mp4 vs audio/mp4).
   - On each SourceBuffer, define an OWN `appendBuffer` property that records
     the bytes (the demuxed ISO-BMFF fragment) before calling the original.
     An own property is required — `SourceBuffer.prototype.appendBuffer` is a
     non-writable native method, so reassigning the prototype silently no-ops.
3. **`Target.createTarget` foreground** → `Page.navigate` to the watch URL →
   wait `networkIdle`, then poll for `#movie_player` + `<video>`. Foreground is
   required: background tabs have flaky autoplay, and if the player never
   starts, MediaSource is never fed and nothing is captured.
4. **Disable autonav**, then **force quality** (`player.setPlaybackQualityRange(q,q)`,
   best-effort) and **play muted at 16×** so the player fetches+appends every
   segment fast. Autonav is turned off by clicking `.ytp-autonav-toggle` (state
   read from `aria-label` / `data-tooltip-title`: "Autoplay is on" → "... off")
   BEFORE play, so the player can never autoplay into the next video — the real
   fix for the background-tab case, since even a throttled tab that never
   latches has no next-video to run away to. The player's own SABR client
   requests the whole timeline as it plays through. This is the whole model:
   view the video, sped up.
5. **Wait until the whole timeline is buffered** (`buffered.end >= duration-0.5`;
   the player buffers ahead), then **freeze capture + pause atomically** in one
   page-side call. We break the FIRST time the timeline is full and never
   re-check, so autoplay advancing to the next video doesn't matter — we've
   already stopped. A `__capDone` flag makes the hook pass appends through (stop
   recording) the instant coverage completes, so nothing after this enters the
   captured buffers. The same poll **re-asserts `muted` + `playbackRate=16` each
   tick** — the player can clobber them on a quality switch, ad, or re-init,
   which would un-mute the 16× audio mid-capture.
6. **Drain captured buffers to disk DURING playback** (interleaved with the
   coverage poll, ~every 1 s). Page-side `__drainNew(i,maxBytes)` returns up to
   `maxBytes` of the bytes appended since the last call, advancing a per-buffer
   `(_chunkIdx,_chunkOff)` cursor, base64-encoded; the REPL decodes with
   `Buffer.from(b64,'base64')` and `fs.appendFileSync`s each slice to a per-buffer
   temp file. `__drainNew` never emits more than `maxBytes` even when a single
   fmp4 segment exceeds it — it slices a too-big chunk across two drains (a 1440p
   segment is often 1–4 MB), which is the fix for the crash that dropped the
   socket. By latch-time nearly all the media is already on disk, so the
   post-pause pass pulls only the tail and the tab closes right after. **Pick the
   largest drained video + largest audio file** (the player can create more than
   one MediaSource on a quality switch; the small init-segment duplicates get
   unlinked) and hand their paths to ffmpeg.
7. **ffmpeg** `-i video -i audio -c copy -movflags +faststart out.mp4` (bash,
   after the heredoc returns the temp-file paths).
8. **`closeTab`** in `try/finally`, fire-and-forget — exact gsearch/xsearch
   teardown.

## Why capture at MediaSource, not googlevideo

The logged-in web client now plays everything via **SABR**
(`application/vnd.yt-ump`), a protobuf multiplex — not discrete itag URLs with
HTTP ranges. Adding `&range=` to a SABR URL returns a 31-byte
`sabr.malformed_config` error; there's no media-bytes URL to range-download at
the playback layer. (yt-dlp sidesteps this by impersonating a SABR-*free*
`android_vr` client — which is the client-impersonation scaffolding this skill
deliberately drops.)

The one place the demuxed media exists in the clear is
`SourceBuffer.appendBuffer` — the ISO-BMFF fragments the player hands to
`<video>` for playback. Capturing there is SABR-agnostic, auth-agnostic, and
gating-agnostic: the page did all of it; we record the output. This is
literally "watch it → record it."

## Files

All paths relative to `<skill-dir>`.

- `scripts/ytdl` — the bash CLI (a `browser-harness-js` heredoc, no `#!bun`)
- `scripts/setup` — symlink `ytdl` + `browser-harness-js` onto PATH
- (no `lib/` — the whole solver/client-table/download scaffolding is gone)

## Traps

- **The MSE hook must inject via `Page.addScriptToEvaluateOnNewDocument`, not a post-load `Runtime.evaluate`.** The player grabs `MediaSource`/`addSourceBuffer` references while it boots; injecting before any page JS runs is the only way to patch them in time. The hook runs in the main world (no `worldName`), where the player lives.
- **Patch `appendBuffer` as an OWN property on each `SourceBuffer` instance, never on the prototype.** `SourceBuffer.prototype.appendBuffer` is a non-writable native method — `sb.appendBuffer = fn` on the prototype silently no-ops; `Object.defineProperty(SourceBuffer.prototype, 'appendBuffer', …)` fails to take effect. Defining an own property on the instance shadows the prototype method correctly. (`addSourceBuffer` *can* be patched on the prototype via `defineProperty` — it's writable.)
- **Use a foreground tab.** Background-tab autoplay is unreliable; if the player doesn't start, MediaSource is never fed and capture is empty. `createTarget({ url: 'about:blank' })` (no `background: true`). Autonav is also disabled before play (see below) so a backgrounded/throttled tab can't run away to the next video.
- **Disable autonav before play, not after.** YouTube's `.ytp-autonav-toggle` controls autoplay-next; click it OFF (state is `aria-label`/`data-tooltip-title` = "Autoplay is on" vs "... off") BEFORE calling `play()`. This is the real fix for the background-tab case: even if the tab is throttled and the coverage poll never latches, there is no next-video autoplay to run away to. Don't try to defeat autoplay by reacting to `ended`/`timeupdate` — by then the next video has already loaded.
- **Coverage is driven by playback, not by range requests.** The player only appends segments it plays, so ytdl plays through at 16× and waits for the whole timeline to be buffered (`buffered.end >= duration-0.5`). Don't try to harvest a URL and range-fetch — see "Why capture at MediaSource." For very long videos this is bounded by real-time/16; a 1h video takes ~4 min of 16× playback.
- **The coverage loop must latch, not re-check.** We break the FIRST time the timeline is fully buffered and never re-evaluate — so YouTube autoplaying into the next video (which resets `currentTime`) doesn't matter: capture is already frozen. Don't rewrite the loop to poll `currentTime ≈ duration` every tick; autoplay will reset `currentTime` to ~0 and the check goes false again, spinning until a watchdog. The `__capDone` freeze-on-latch keeps the next video's segments out of the buffers.
- **A fragmented-webm capture may log `[matroska,webm] File ended prematurely` from ffmpeg — it's benign.** MSE-captured opus/vp9 segments end mid-EBML-element (there's no graceful close on a live capture). ffmpeg still muxes the full duration correctly (decode-tested, exit 0); the warning is about the input container's framing, not missing data. mp4-captured (AV1/H264) buffers don't hit this.
- **Quality forcing is best-effort.** `player.setPlaybackQualityRange(q,q)` is honored on most content, but SABR manages bitrate server-side and may ignore it. `--info` shows `getAvailableQualityLevels()`; the returned JSON includes `actualQuality` so you can see what was really played. If the forced quality wasn't honored, the capture is whatever the player chose.
- **`--info` opens the watch page** (one page load) to read title/duration/qualities — it's not free, but it's a normal watch-page hit, not a probe storm.
- **Bytes cross the CDP boundary as base64** in **256 KB** (3-aligned) slices via `Runtime.evaluate` `returnByValue`, decoded with `Buffer.from(b64,'base64')` and appended. The slice size is divisible by 3 so each slice's base64 is independently decodable (no interior `=` padding). Don't slice at a non-multiple-of-3 offset or the concatenation decodes to garbage.
- **Drain captured buffers to disk DURING playback, not after, and keep each CDP response SMALL.** `__drainNew(i,maxBytes)` is called on a ~1 s cadence inside the coverage loop — a page-side `(_chunkIdx,_chunkOff)` cursor tracks bytes already flushed, so each call returns only what was appended since the last, base64-encoded, and the REPL appends to a per-buffer temp file. By latch-time nearly all the media is on disk; the post-pause pass pulls only the tail, so the tab closes immediately at the latch signal (closeTab is fire-and-forget in `finally`, so it can't fire until the snippet returns — draining during the loop keeps that return fast). Doing the whole pull *after* pausing blocks the return and left the tab open for the entire multi-MB drain — this was the "tab stays open ~30 s after the video stops" symptom. The bytes live in page memory and the tab can't close until they're off, so closing at latch *requires* draining during playback.
- **`__drainNew` must never emit more than `maxBytes`, even for a multi-MB segment.** A 1440p fmp4 segment is often 1–4 MB, far over the 256 KB slice cap. The original drain had a `if (to===from) force one whole chunk through` branch that emitted the whole segment in one CDP frame — that single multi-MB `returnByValue` **closes the debug socket** (1006) on Dia. The fix slices a too-big chunk across two drains: this call returns its head and leaves `_chunkOff` pointing into it for the next call. Never reintroduce the force-one-chunk path.
- **In `drainOne`, append the slice BEFORE testing `done`.** `__drainNew` returns `done:true` on the *same* call that yields the final bytes (the cursor reaches the end mid-call), so `if (s.done) return` before appending silently drops that last slice and truncates/corrupts the muxed file (ffmpeg then logs EBML `exceeds max length` / `Invalid data`). Always append `s.b64` first, then check `s.done`.
- **Never send a 4 MB `returnByValue` frame.** A single 4 MB base64 response (~5.6 MB JSON in one CDP frame) **closes the debug WebSocket** on some browsers (reproduced on Dia: the socket drops `rs→3` on the very first 4 MB slice, while a 256 KB slice survives). This masqueraded as a "capture stops before the video finishes" failure because the post-pause pull — which used 4 MB slices — killed the socket immediately. The slice size is now **256 KB** (`262143`, 3-aligned); keep it small. `__drainNew` enforces it per call (slicing big chunks across drains); `__pullBuffer` (absolute-offset slice pull) is retained in the hook as a verified reference/fallback but is not on the hot path — the drain + final tail both use `__drainNew`.
- **Output container follows the video mime.** `video/mp4` → `.mp4`; `video/webm` → `.webm`. ffmpeg is invoked with `-c copy`, so a webm video is muxed to `.webm`. If codecs mismatch the container, ffmpeg copy will fail — that's a codec/container issue, not a capture issue.
- **The pure output isn't QuickTime/iOS-friendly.** YouTube typically serves AV1 video + Opus audio; `-c copy` preserves those (VLC/browsers play them fine), but QuickTime / AVFoundation / iOS refuse them (no AV1-in-MP4 decoder, no Opus-at-all). The skill stays pure on purpose — lossless stream-copy, no size/quality penalty (a re-encode quadrupled the size and is lossy in testing). If you need QuickTime/iOS, re-encode the output yourself in one step: `ffmpeg -y -i "out.mp4" -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 192k "out-qt.mp4"`.
- **Re-assert `muted` + `playbackRate` every poll tick.** YouTube's player resets `muted`/`playbackRate` on a quality switch, ad, or player re-init; a one-shot set at play-start gets clobbered and you'll hear the 16× chipmunk audio. The coverage poll re-asserts both each 250 ms — keep that if you touch the loop.
- **Reset `currentTime` to 0 at play-start.** A signed-in account restores the last watch position ("resume from where you left off") on a bare `watch?v=ID` URL with no `t=` — if the account previously watched part of the video, the player starts partway through and the MSE capture only covers from the resume point onward (the `buffered.end >= dur-0.5` check still passes, since the player buffers ahead to the end). `extract_id` already strips any `t=`/`start=` URL param, but resume position is account-side, not URL-side, so the play-start nudge also forces `v.currentTime = 0` after metadata loads. Keep it — without it, resumed videos download missing their beginning.
- **ffmpeg runs with `-y` (overwrite).** Re-running the same video overwrites the prior output instead of hitting ffmpeg's interactive `Overwrite? [y/N]` prompt, which fails non-interactively and silently leaves a stale file. Don't drop `-y`.
- **YouTube Shorts (`/shorts/<id>`) are normalized to `watch?v=<id>`.** A Short is just a video; the Shorts page is a different UI shell around the same `#movie_player`, so `extract_id` pulls the 11-char id from `youtube.com/shorts/<id>` and the rest of the pipeline captures it in the regular watch player — the autonav toggle, quality forcing, and MSE-hook selectors all target the watch page. Don't try to drive the Shorts shell directly: its swipe-to-next autonav is a different control (`.ytp-autonav-toggle` is absent) and its layout hides the controls ytdl relies on.
- **Live / Premiere uses HLS**, not MediaSource segments — not supported by this skill.
