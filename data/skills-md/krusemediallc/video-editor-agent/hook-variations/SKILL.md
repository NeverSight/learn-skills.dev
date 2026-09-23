---
name: hook-variations
description: >-
  Combine ONE finished body cut with MANY hook clips to produce one standalone video per
  hook — the hook A/B batch you upload as separate ad creatives. Use whenever someone wants
  to "add all these hooks to this body", "combine this video with every hook in that folder",
  "make 21 versions with different openers", "swap the hook", "build hook variants", "test
  these hooks against the same body", or hands over one body file plus a folder of hooks and
  expects N finished videos out. Also use for the same shape with different words: intro
  variants, opener tests, cold-open A/B sets, or re-running an existing variant batch against
  a NEW cut of the body. Joins losslessly (body frames stay bit-identical), matches hook
  loudness to the body so the seam does not jump, and verifies with AVFoundation because an
  ffmpeg-only check cannot catch the parameter-set freeze that makes these files play fine
  in ffmpeg and stall in QuickTime. Do NOT use for editing a single video, adding captions,
  or cutting the hooks themselves out of a longer recording.
---

# hook-variations — one body × N hooks

You have one finished body cut and a folder of hooks. You are producing one standalone
video per hook, each good enough to upload as its own ad creative.

The join itself is four lines of ffmpeg. Everything in this skill exists because the
obvious four lines produce files that look correct in every tool you would naturally reach
for and are broken on the user's disk. **A hook batch has been delivered broken before,
after passing a thorough QA pass, because the build and the QA used the same decoder.**

## Shape of the deliverable

`hook → body`, hook first. The hook is the scroll-stopper; the body is the payload that
does not change between variants.

Before you build, read the body's first few seconds. Bodies often open with their own
bridge line ("I'm about to show you the easiest way…"). That is usually a *transition into*
the payload, not a competing hook, and it should stay — but it is the user's call, so say
which way you read it and offer the alternative in one line rather than silently trimming.
Never cut body content to make the join feel tighter without asking.

## Do this in order

### 1. Pre-flight — always, it takes ten seconds

```bash
python3 scripts/probe_join.py --body <cut.mp4> --hooks <hooks/>
```

This prints, per hook: geometry, timebase, audio-tail overrun, whether its avcC matches the
body, and its loudness delta — plus what the build will have to do about each. Read it
before building. Every trap below shows up in that table, and it tells you whether the
hooks can be stream-copied (free, lossless) or need a re-encode.

If geometry differs (resolution, fps, pix_fmt), stop: these are not drop-in hooks and
scaling them is a separate decision to raise with the user.

### 2. Build

```bash
python3 scripts/build_variants.py --body <cut.mp4> --hooks <hooks/> --out <variants/> \
  --preset slow --crf 18            # match how the BODY was encoded
```

`--preset`/`--crf` matter only for hooks that need re-encoding, and they must match the
body's own encode. Find them in the body's build script or ask; guessing produces a
parameter-set mismatch, which the build refuses to mux (see trap 3).

Writes the variants plus `variants.json` (the manifest every later step reads).

### 3. Verify — the step that is not optional

```bash
swiftc -O scripts/avtest.swift -o scripts/avtest     # once per machine
python3 scripts/verify_variants.py --body <cut.mp4> --hooks <hooks/> --out <variants/>
```

Do not report success off the build's own "OK" lines. See **Why ffmpeg cannot sign this
off** below — this is the single most important paragraph in the skill.

### 4. Name them

Route through the **naming-convention** skill. Variant batches are unusable when every file
is `ad-v5-hook-07.mp4`; the filename has to carry what differs. That skill also covers the
trap of inheriting a wrong subject label from an upstream cut list.

### 5. Deliver

Route through **video-review-canvas**, and lead the reply with the URL. For a batch, publish
720p proxies rather than the masters — a set of 21 two-minute 1080×1920 masters is well over
a gigabyte and too heavy to publish, while the canvas exists to judge the cut and the seam.
```bash
python3 scripts/build_review.py --out <variants/> --version v1 --map <subjects.json>
```

`--map` is the naming-convention subjects file, which gives each card a real title
("Lookalike sunglasses · Lego-style ad") instead of "Hook 20". Each card also prints the
master's filename, so canvas ↔ disk is a direct match when a reviewer says "number 7 is the
one". Proxies that already exist are skipped, so re-running after a rename costs seconds.
Bump `--version` every round: it stamps the proxy filenames, and without that the browser
serves the previous cut from cache and you get "why isn't the new one there?".

---

## The four traps

Three of these fail silently. That is what makes them worth knowing rather than
rediscovering.

### 1. Timebase — the concat demuxer does not rescale the second file

It takes its output timebase from the *first* file. Hooks at `1/15360` in front of a body at
`1/30000` stretch the body's timestamps by 1.95× — a 121-second file that reports 236s and
15.36fps. No warning. Fixed by remuxing both to a common timescale.

### 2. Audio overrun — the offset comes from the container, not the video

AAC frames are 1024 samples, which never lands on a 30fps boundary, so a hook's audio
routinely runs tens of milliseconds past its last video frame. The demuxer offsets the next
file by the **container** duration, so the body starts off the frame grid and stays
lip-sync drifted for its whole length. Doing the video pass **video-only** fixes this at the
root: a video-only container's duration *is* its video duration.

Also pin `duration` in the concat list to the hook's exact `frames/fps`. Some mp4 muxers
write a track duration derived from a millisecond-rounded value (e.g. 801990 ticks instead
of 802000), which starts the body a third of a frame early. That directive is only
trustworthy once both files share a timebase — with a mismatch it *compounds* the offset
instead of setting it, which makes it look like a dead end if you try it too early.

### 3. Parameter sets — the one that ships broken

If the hook and body were encoded with different settings, they carry different SPS **and**
PPS. An mp4 `avc1` track holds exactly one `avcC`, and concat writes the first file's.

ffmpeg plays the result perfectly, because it honours the in-band SPS/PPS the demuxer
inserts at each IDR. **AVFoundation — QuickTime, Finder, Photos, most upload validators —
ignores in-band parameter sets in an `avc1` track and reads only `avcC`.** So the hook plays
and the picture freezes on the body's first frame while audio runs on.

The fix is to make both halves share one parameter set. Re-encode the **hook**, not the
body: the hook is short and the body is the long, approved, quality-critical half. Matching
the body's preset/CRF/pix_fmt gets the PPS and level to agree; **`setsar=1` is usually the
last byte**, because a body that signals square pixels explicitly
(`aspect_ratio_info_present_flag=1`) will not match a plain re-encode that omits it.

There is a tell you will probably see before the freeze: `framemd5` over `-c copy` reporting
exactly the keyframes as changed. That is the demuxer inserting parameter sets mid-stream.
It is easy to read as "correct and required" and move on — it is in fact the symptom. **If
two halves need different parameter sets inserted at a boundary, one `avcC` cannot describe
both. Go read `avcC`.**

### 4. Loudness — hooks are usually much quieter than the body

Hooks cut straight from a raw mix commonly sit 10–20 LU below a body that has been through
a loudnorm pass. Joined raw, every variant is a hook you can barely hear followed by the
body arriving at full level. Match each hook to the body's integrated LUFS.

Two things about doing that:

- **`loudnorm:linear=true` cannot do it when the lift is large.** A +15 dB lift would put
  peaks above 0 dBTP, so linear mode caps the gain to protect the ceiling and lands several
  LU short. Static gain *then* a limiter reaches the target; the limiter only touches the
  loudest transients.
- **`alimiter` limits sample peaks, not true peaks.** Inter-sample peaks overshoot it, so a
  ceiling of −1.0 dBFS has shipped files at −0.1 dBTP, hot enough to clip in a platform
  transcode. The default here is 0.79 (−2.05 dBFS), which lands around −1.1 to −1.6 dBTP.

## Why ffmpeg cannot sign this off

A set of variants once passed all of this: every frame decoded, pixel-identical to source,
constant 30fps, zero audio lag, loudness verified. And every file froze after the hook in
QuickTime.

The build used libavcodec. The check used libavcodec. libavcodec is the most permissive
decoder in the chain, and it papers over exactly the defect that was present. **A check that
shares a blind spot with the thing it checks proves nothing** — the failure was found by the
user pressing play, which is the worst possible QA loop.

So `verify_variants.py` shells out to `avtest`, a small Swift `AVAssetImageGenerator` probe,
and decodes 12 points across every file with AVFoundation. It also asserts the file's `avcC`
equals the body's. Those two checks are the only ones that would have caught it. Build
`avtest` once per machine with `swiftc -O scripts/avtest.swift -o scripts/avtest`; if it is
missing, the verifier reports the probe as a FAILURE rather than quietly skipping it.

The generalisation is worth carrying beyond this skill, and it is the repo's own rule in a
sharper form: **verify in the medium the user will consume, with a different tool than you
built with.**

## Two more things that will bite

**Workers do not inherit module globals.** `ProcessPoolExecutor` uses the `spawn` start
method on macOS, so each worker re-imports the module with its *own* argv — CLI flags are
gone there. A verifier that read its paths from globals had all five workers fall back to
defaults and check a *different folder* while the parent printed the labels you asked for:
21 confident "ALL PASS" lines about files nothing had opened. Caught only because a frame
count came back 3 short. `verify_variants.py` passes config into the worker as arguments and
prints the folder and body under test at the top of every run — if that header does not name
what you meant, stop.

**Properties inherited from the body are not yours to fix silently.** A body whose audio
ends before its picture (or vice versa) will hand every variant the same quirk. Pad to hold
sync, then *say so* — e.g. "the last 2 frames are silent, that comes from the body, want the
tail trimmed?" Do not quietly alter the body's own timing to tidy it up.

## Re-running against a new cut of the body

Common: the body gets a revision and the whole batch is rebuilt. Everything is
parameterised, so it is the same commands with a different `--body` and `--out`. Keep each
body's variants in **its own folder** and keep the old set unless told otherwise — these are
usually net-new creatives, not replacements.

Do not assume a new body cut matches the old one's encode. `probe_join.py` on the new body
answers it in seconds, and the answer decides whether hooks can be copied or must be
re-encoded.

## Files

| Path | What it is |
|---|---|
| `scripts/probe_join.py` | pre-flight compatibility table: geometry, timebase, audio tail, avcC, loudness |
| `scripts/build_variants.py` | the build; copies hooks that already match, re-encodes those that do not |
| `scripts/verify_variants.py` | full verification incl. the AVFoundation probe and avcC assertion |
| `scripts/avtest.swift` | 30-line AVFoundation decode probe (`swiftc -O` it once per machine) |
| `scripts/build_review.py` | 21-up gallery review canvas from `variants.json` |
| `assets/canvas_template.html` | the canvas page (per-variant comment box, timeline stamping) |
| `assets/data.json` | here.now Site Data manifest that turns on the per-variant comment store |

Related skills: **naming-convention** (name the batch), **video-review-canvas** (deliver
it), **edl-tighten** (if the hooks themselves still need cutting out of a longer recording).
