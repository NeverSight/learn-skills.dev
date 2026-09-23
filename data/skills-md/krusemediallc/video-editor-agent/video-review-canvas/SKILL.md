---
name: video-review-canvas
description: >
  Publish a finished (or draft) video cut to a frame.io-style review canvas on here.now —
  a player with a frame-accurate scrubber, persistent timeline notes, version comparison, replies, resolution and evidence,
  and a clickable beat map — then read those notes back before the next cut. Use this to
  DELIVER any video edit for review: reel recuts, brand-deal edits, motion-graphics ads,
  carousel videos, YouTube cuts, sizzle reels. Trigger whenever a cut is ready to show, or on
  "send me the video", "put this on a canvas", "let me leave notes on the timeline",
  "frame.io style", "get me a link to review this", "publish the new version", or "what notes
  did I leave?" — even if the canvas is never named. Delivering a cut as a bare file
  attachment or a local preview link instead of a canvas link is the failure this skill
  exists to prevent. NOT for image or slide galleries (plain here-now publish), and not for
  making the video itself (branded-ad-edit / hyperframes).
---

# Video Review Canvas

Every cut the reviewer sees goes on a here.now canvas: the video, a scrubber that reports the
exact frame, notes they pin by clicking the timeline, and a beat map naming what each moment
is supposed to be doing. The notes persist in here.now **Site Data**, so the next session
reads them back and works the list.

**The reply delivering a cut must LEAD with the canvas URL, pasted in full, every single
round — even when it's the same link as last time.** This has failed in practice: the
reviewer had to ask twice for the link on a real delivery. A file card without the link reads
as "not delivered", and "it's on the canvas" without the URL doesn't count. Send files as an
extra *after* the link, never instead of it.

## Prerequisites

- **node >= 20** (the scripts use `fetch` and top-level `await`).
- **ffprobe** on `PATH`, or point the `FFPROBE` env var at the binary (part of ffmpeg).
- **The `here-now` skill** for publishing, with credentials at `~/.herenow/credentials`.
  If you don't have it, agent docs live at <https://here.now/docs> (fetch with
  `User-Agent: claude`).

## Why a canvas and not a file

A file attachment gets you "the middle bit feels slow." A canvas gets you "at 0:14.3 the chip
lands before he says the word." The timestamp is the difference between a vague note and an
actionable one, so everything here optimises for making it trivial to pin a precise moment:
frame stepping with the arrow keys, a frame counter next to the clock, and a beat map that
tells the reviewer what each section was *trying* to do so they can say it missed.

## Build and publish

### 1. Write the config

One JSON file. The beat map is the part that earns its keep — name every card, cut, or
section, and say in one line what it's for. That framing is what turns "I dunno, something's
off" into a specific note.

```jsonc
{
  "video":   "videos/product-launch/output-v2.mp4",
  "outDir":  "videos/product-launch/review",
  "title":   "Product launch ad",
  "version": "v1",
  "eyebrow": "STUDIO · EDIT REVIEW",
  "blurb":   "Motion graphic on every line, in the brand's palette, cut like the reference ad.",
  "author":  "Reviewer",
  "accents": ["#0082fb", "#a033ff", "#ff5c87"],
  "facts":   ["30.03s · 1080×1920 · 30fps", "8 designed cards", "39 SFX hits + music bed"],
  "beats": [
    { "t": 0.00,  "n": "Hook — full-bleed", "s": "Hard open on the subject's face, hard cut on the key word.", "tone": "mute" },
    { "t": 0.62,  "n": "Card 1 · The unlock", "s": "Real screenshot + green headline stamp." },
    { "t": 17.40, "n": "Card 5 · BEFORE", "s": "The old painful workflow, red stamp.", "tone": "red" },
    { "t": 19.24, "n": "Card 6 · NOW", "s": "Feature toggle flips ON on the word \"flip\".", "tone": "green" },
    { "t": 23.00, "n": "Card 7 · One catch", "s": "The honest caveat.", "tone": "amber" }
  ]
}
```

`tone` (`""` | `red` | `green` | `amber` | `mute`) tints the beat's left rule, so the emotional
arc of the edit is readable at a glance in the sidebar. Match it to the caption colour ranges
if the edit has them.

### Editor's notes (optional `notes` array)

The beat map says what each moment *is*. `notes` says what you **did to the cut and what still
needs a human decision** — the things with no single timestamp. It renders as a third sidebar
card above the beat map, same tones, and `b` may contain `<b>`.

```jsonc
"notesHint": "What I changed, what I left alone, and what needs your call.",
"notes": [
  { "n": "35 cuts, 17.71s out, zero copy cut", "tone": "green",
    "b": "33 pauses plus two flubs. <b>Not one word of the script was removed.</b>" },
  { "n": "Runtime is 1:41, the plan said 55 to 70s", "tone": "amber",
    "b": "Trim menu with timecodes below. <b>I did not cut copy to fix this</b> — that is your call." }
]
```

On a paid brand deliverable this card is the point of the canvas: it is where a proposed copy
trim gets timecodes and a runtime, so the reviewer can approve or reject it without opening an
NLE. Put anything that could get the video rejected by the brand at the top, toned `red`.

### 2. Build

```bash
node .claude/skills/video-review-canvas/scripts/build-canvas.mjs <config.json>
```

It ffprobes the video for real duration/fps (so the frame counter is honest), copies the media
in under a version-stamped filename, drops the Site Data manifest, and prints the publish command.

### 3. Publish

Publish the output directory with the `here-now` skill's `publish.sh` (set `HERENOW_PUBLISH`
to its path if it isn't at the default install location):

```bash
bash "${HERENOW_PUBLISH:-$HOME/.agents/skills/here-now/scripts/publish.sh}" <outDir> \
  --title "<Title> — V1 review" --client claude-code
```

Add `--slug <existing-slug>` to update in place and **keep the URL stable across versions** —
one durable link per project is easier for the reviewer than a new link every round.

### 4. Smoke-test before you send the link

Never hand over an untested canvas. Two `curl`s and you know it works:

```bash
U=https://<slug>.here.now
curl -s -o /dev/null -w "%{http_code}\n" "$U/"                       # 200
curl -s -r 0-1000 -o /dev/null -w "%{http_code}\n" "$U/<video>.mp4"  # 206 (range = it streams)
curl -s "$U/.herenow/data/comments?limit=5"                          # {"records":[...]}
```

If you want to prove the write path too, POST with an `Origin` header (see gotcha 2) and a
throwaway `version` like `"probe"` — the page filters by version, so the probe stays invisible.

## Reading notes back

```bash
node .claude/skills/video-review-canvas/scripts/read-notes.mjs <slug> [version]
```

Prints each note with its stable record ID, version, status, replies and evidence, sorted by version and timestamp. Work them in timeline order against the actual frames —
seek to each one and look before deciding what it means. A round where you publish but never
GET the store is a round of feedback silently dropped.

## Version comparison and revision tracking

Existing single-video configs still work, including `download`, `downloadName`,
`downloadLabel` and additional `downloads`. Add `versions` to keep old media
available at the same URL:

```json
{
  "title": "Product launch ad",
  "outDir": "review",
  "version": "v2",
  "author": "Reviewer",
  "versions": [
    {"version": "v1", "label": "First cut", "video": "output-v1.mp4",
     "beats": [{"t": 0, "n": "Hook", "s": "Opening statement"}]},
    {"version": "v2", "label": "Revised cut", "video": "output-v2.mp4"}
  ],
  "download": "output-v2.mp4",
  "downloadName": "master-v2.mp4"
}
```

Paths resolve relative to the config. Version IDs must be unique, filename-safe
strings up to 20 characters. Each version is probed independently; use its own
beat map. `version` selects the initial cut; it defaults to the last listed one.
Each version's SHA-256 is saved in `review-config.json`. Before writing anything,
the builder checks every existing version receipt and media filename. Rebuilding
with the same bytes is allowed; changed media needs a new version ID and file.
Receipts remain in the config for versions hidden from the picker. The guard also
applies when a project title changes, the input is already inside the review
directory, or a download alias would overwrite old version media, so existing
comments/evidence retain their meaning.
A selected comparison plays beside the main video, muted and synchronized to
elapsed time plus the editable comparison offset. This is not automatic alignment
of differently edited timelines. **Compare this change** uses a note's before/after
evidence points to set the correct offset for that specific change.

Every note has a stable record ID. Reviewers can reply, mark it resolved/reopen it,
and attach before/after version + frame pairs with a description of the change.
Evidence opens both actual rendered videos at those points. Retain those video
versions in the config; a missing version is reported instead of seeking in the
wrong cut. Notes from **all versions** are shown initially, with status and version
filters. Frame pins store an integer frame, its unrounded `t = frame / fps`, and
FPS. Use CFR review encodes for exact frame indexing; VFR sources should first be
normalized for review. The model preserves fractional rates such as 30000/1001.

The existing `comments` collection remains compatible. Replies, status changes
and evidence append records to `reviewEvents`, keyed by `commentId`, without
rewriting original feedback. Like the original comments, these collections allow
public read/insert; no owner key is embedded in the browser. A shared review URL
is a collaborative workspace, not authenticated sign-off. Republish the generated
`.herenow/data.json` with the page to enable the new collection. Old sites without
that collection can still be read. Load/save errors are visible and a failed load
does not replace the currently displayed notes.

### Agent readback and export

The **Export review JSON** button downloads raw `comments`/`events` and a replayed
`notes` list containing status, replies, evidence and history (`schemaVersion: 2`).
The command-line reader uses the same replay model and follows paginated responses:

```bash
node .claude/skills/video-review-canvas/scripts/read-notes.mjs <slug> --json
node .claude/skills/video-review-canvas/scripts/read-notes.mjs <slug> v1 --out revisions-v1.json
node .claude/skills/video-review-canvas/scripts/read-notes.mjs --file review-revisions.json --json
```

Pass the record's stable `id` to any future event writer; never use its visible
list number, timestamp alone or the new cut's absolute seconds as identity.

### Local demo without publishing

Set `"storage": {"mode": "local", "key": "my-review-demo"}` and serve the generated
directory with a local HTTP server. This explicitly uses browser localStorage,
with a visible local-only notice. Comments, replies, status and evidence survive
refresh. The key isolates projects; keep it stable to resume a demo. Clearing site
data clears this local review, so export JSON for backup or agent readback.
The default is `{"mode":"remote"}` for here.now Site Data.

Optional `reviewData` seeds a local demo only on its first use:

```json
{
  "reviewData": {
    "comments": [{"id":"note-1", "createdAt":"2026-09-18T12:00:00Z",
      "data":{"version":"v1","t":1,"frame":30,"fps":30,
        "text":"Tighten this pause.","author":"Reviewer"}}],
    "events": [{"id":"event-1", "createdAt":"2026-09-18T12:01:00Z",
      "data":{"commentId":"note-1","kind":"status",
        "status":"resolved","author":"Editor"}}]
  }
}
```

`assets/review-model.mjs` is DOM-free and exposes `framePin`, `replayReviews`,
`revisionExport`, `createLocalStore` and `createRemoteStore` for integrations.
Run local coverage with:

```bash
node --test .claude/skills/video-review-canvas/tests/*.test.mjs
```

## Shipping a new version

1. Render the new cut as a **new file** — never overwrite an approved one.
2. Bump `version` in the config (`v2`) and rebuild. The video filename gets the new suffix
   automatically and the version picker identifies the round. Include previous media in `versions`
   for comparison. Notes from all versions remain visible by default; reviewers can filter them.
3. Update `blurb` to say what changed in this cut — it's the changelog the reviewer reads first.
4. Publish with `--slug` to the same URL.
5. Reply, leading with the link, and say which of the reviewer's notes you addressed.

## Cap the review encode

A CRF-16 master peaks at 16-21 Mbps on motion-heavy beats and can stutter in a phone browser
even when the file is perfect — which reads to the reviewer as "it skips around". Publish a
capped copy to the canvas (`-crf 22 -maxrate 6M -bufsize 12M`, faststart) and keep the master for
posting. Measure per-second bitrate on both before deciding a "glitch" is in the edit:
`ffprobe -select_streams v:0 -show_entries packet=pts_time,size` summed per second.

## Gotchas

Each of these cost real time.

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | "Why isn't the new cut on here.now?" — the reviewer sees the old video | same video filename, so the browser serves its cache | version-stamp the filename every round (`build-canvas.mjs` does this); also bump the on-page version label so the round is visible |
| 2 | `POST /.herenow/data/comments` → 403 `forbidden` from curl, but fine in the browser | public Site Data writes require a matching `Origin` header; browsers send it, curl doesn't | `-H "Origin: https://<slug>.here.now"` when testing by hand |
| 3 | Can't delete a test record even with the owner bearer key | the delete op is refused regardless of `access.delete` | don't try — give throwaway records a distinct `version` and let the page's version filter hide them |
| 4 | Notes from v1 appear on v2 | the store intentionally keeps all rounds visible | use the Versions filter for the current cut; resolve addressed notes instead of hiding them |
| 5 | Notes land a beat late | the reviewer pins while playing, seeing a frame that's already gone | the composer pauses and records the exact integer frame plus its unrounded timestamp; keep the frame counter visible so the reviewer can verify |
| 6 | Beat map text runs together into one line | `.bn`/`.bs` are inline spans | they're `display:block` in the shipped template — keep it that way if you retint |
| 7 | Script dies with `ENOENT` on a path containing `%20` | `new URL(import.meta.url).pathname` percent-encodes; project paths often contain spaces | `fileURLToPath(import.meta.url)` |
| 8 | Canvas published but the reviewer never opened it | the reply buried the link or omitted it | first line of the reply is the bare URL |

## Files

| File | What it is |
|---|---|
| [scripts/build-canvas.mjs](scripts/build-canvas.mjs) | config + video → publishable canvas dir (probes fps/duration, version-stamps the media) |
| [scripts/read-notes.mjs](scripts/read-notes.mjs) | pull the pinned notes back off a published canvas |
| [assets/canvas-template.html](assets/canvas-template.html) | the page itself — retint the three `--a1/2/3` accent tokens per project, leave the rest |
| [assets/data.json](assets/data.json) | the here.now comments + append-only review events manifest |
| [assets/review-model.mjs](assets/review-model.mjs) | shared frame, event replay, persistence and export model |
| [assets/review-app.mjs](assets/review-app.mjs) | version/compare playback, notes, replies, status and evidence UI |
| [tests/review.test.mjs](tests/review.test.mjs) | local model, persistence, builder compatibility and escaping checks |

Requires `ffprobe` (or `FFPROBE` env var), node >= 20, and here.now credentials at
`~/.herenow/credentials` (the `here-now` skill's `publish.sh`). Related: `branded-ad-edit`,
`talking-head-recut`, `hyperframes-cli`.
