---
name: video-edit
description: Edits a complete talking-head video end to end with free tools (Remotion, whisper.cpp, ffmpeg) - a vertical short (1080x1920) or a full horizontal YouTube video (1920x1080). Use when the user says edit, cut, captions, subtitles, motion design, montage, "make it a short", "edit my YouTube video", render, or gives a recording from video-agent/takes/. Transcribes locally with word timings, cuts silences and retakes against the script, adds punch-in zooms, word-by-word captions in the creator's accent color, a hook card, callouts and a progress bar, levels the voice to -14 LUFS, and writes an .srt, a cut list for CapCut or Premiere, chapters for a long video, and the post copy.
argument-hint: "<take file or slug> [short | long]"
allowed-tools: Bash(node -v) Bash(git --version) Bash(ffmpeg *) Bash(ffprobe *) Bash(npx remotion *) Bash(node sub.mjs *) Bash(npx tsc --noEmit)
---

# Video Edit

One raw take in, one finished video out: `video-agent/edits/<slug>/final.mp4`. Either a vertical short, or a full horizontal video for YouTube.

The tools are free and run on the creator's machine:

- **Remotion** (videos written in React) and its official TikTok template, which ships local speech-to-text with word timings (whisper.cpp).
- **ffmpeg** for the checks and the sound.

The look is fixed and simple: [references/style.md](references/style.md). The code that draws it is in [references/remotion-short.md](references/remotion-short.md).

## How to run it

- Preflight: `node -v && ffmpeg -version && git --version`. Anything missing: stop and send them to `/video-setup tools`.
- Talk in the creator's language. Say what you do in one line before each long step (install, transcription, render) and how long it takes.
- Read `video-agent/voice.md` for the language and the accent color. No voice file: ask both, or use English and `#FFD400`.
- `<slug>`: lowercase, dashes, no dots or spaces (the transcriber cuts file names at the first dot).
- Steps 1 and 2 run from the project root. From step 3 on, every command runs in `video-agent/studio/` and its paths are relative to it.

## 1. The take and the format

Use the file they name, else the newest file in `video-agent/takes/`. Check it:

```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,color_transfer -of compact "<take>"
```

- No audio stream: stop and say so.
- `color_transfer` is `smpte2084` or `arib-std-b67`: an HDR take (the iPhone default). Don't convert it: Remotion maps it to normal colors when it renders. Tell them to turn off HDR video in the camera settings for the next takes.
- Otherwise, a `.webm` or a variable frame rate (`r_frame_rate` and `avg_frame_rate` differ): convert it, Remotion and the ffmpeg cut both drift on those. The new file is the take from now on:
  ```bash
  ffmpeg -y -i "<take>" -vf fps=30 -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 "video-agent/takes/<slug>-30fps.mp4"
  ```
Then the format. They said it (`short`, `long`, "for YouTube", "a reel"): take it. Otherwise pick from the take and say which in one line:

| Format | Composition | When | Defaults |
|---|---|---|---|
| **Short** | `Short`, 1080x1920 | a take under 90 s, or they want a short, a reel, a TikTok | captions on, hook card, a callout every 8 to 10 s |
| **Long** | `Wide`, 1920x1080 | a horizontal take over 90 s, a full YouTube video, a tutorial, a vlog | captions on (ask: YouTube viewers often prefer the .srt alone, `showCaptions: false`), no hook card unless they want one, a callout every 30 to 60 s at most, chapters |

- Horizontal take in Short: it is cropped to the center. Warn them if they are not in the middle of the frame.
- Vertical take in Long: it would be cropped to a thin band. Don't; offer Short.
- Long: say the time first. Transcription runs at about real time on a laptop with the `medium` model (a 20-minute take, about 20 minutes; `small` is 2 to 3 times faster), and the render takes 3 to 5 s per second of video (a 15-minute cut, about 1 hour). Both run in the background.

`<comp>` below is `Short` or `Wide`.

Find the script it comes from: the matching script in `video-agent/scripts/` (same slug or same first line). No script is fine; the cuts then rely on the transcript only.

## 2. The studio (first time only)

Tell them first: about 1 GB of packages, then on the first transcription the speech engine and its model (0.5 to 1.5 GB) and a few minutes of setup.

```bash
git clone --depth 1 https://github.com/remotion-dev/template-tiktok video-agent/studio
cd video-agent/studio
npm i
```

- Delete `video-agent/studio/.git` so the studio is a plain folder of their project.
- Language, in `whisper-config.mjs`:
  - English: keep `WHISPER_MODEL = "medium.en"` and `WHISPER_LANG = "en"`.
  - Any other language: `WHISPER_MODEL = "medium"` (or `"small"` on a slower machine, 466 MB) and `WHISPER_LANG` = its code (`"fr"`, `"es"`, `"de"`, `"pt"`...).
- Add the `Short` and `Wide` compositions and the font package: follow [references/remotion-short.md](references/remotion-short.md) sections 1 to 3, then `npx tsc --noEmit`. A studio made before `Wide` existed: replace `src/Short/index.tsx` and `src/Root.tsx` with the current sections 2 and 3.
- Optional, better Remotion code from Claude: `npx skills add remotion-dev/skills`.

## 3. Transcribe

```bash
cp "../takes/<take file>" public/<slug>.mp4
node sub.mjs public/<slug>.mp4
```

It writes `public/<slug>.json`: one entry per word, `{ "text": " word", "startMs", "endMs", "confidence" }`. It skips a file that already has its JSON: delete the JSON to transcribe again.

Fix misheard words from the script (names, brands, numbers): change `text` only, never the times.

## 4. The cut list

Find the real silences, then list the gaps between words:

```bash
ffmpeg -nostats -i public/<slug>.mp4 -af silencedetect=noise=-35dB:d=0.3 -f null - 2>&1 | grep silence_
node -e 'const w=require("./public/<slug>.json"),G=350,B=100,A=150,s=(ms)=>(ms/1000).toFixed(2);let r=[{fromMs:Math.max(0,w[0].startMs-B)}];for(let i=1;i<w.length;i++){const g=w[i].startMs-w[i-1].endMs;if(g>G){console.error(`gap ${s(w[i-1].endMs)} -> ${s(w[i].startMs)} (${g} ms) after "${w[i-1].text.trim()}"`);r[r.length-1].toMs=w[i-1].endMs+A;r.push({fromMs:w[i].startMs-B})}}r[r.length-1].toMs=w[w.length-1].endMs+300;console.log(JSON.stringify(r))'
```

The second command prints every gap over 0.35 s with the word before it, then the kept `ranges` with the margins of [style.md](references/style.md). Then fix the ranges:

1. A gap that silencedetect does not report (a breath, a soft word, music): join its two ranges back.
2. Retakes: walk the script line by line. When a line (or its first 3 words) appears more than once, keep the last complete attempt and drop the ranges from the first attempt's first word to the start of the kept one.
3. Drop false starts (an "uh" or a half word before a restart), anything before the hook, and off-script talk.

Long video: same rules, with gaps over 0.5 s instead of 0.35 s (`G=500`): a full video needs some air, a thinking pause can stay. Keep asides that add something; cut the ones that go nowhere. With no script, a retake is a sentence said twice in a row: keep the last one.

Show the result before rendering, in a few lines:

```text
Take 1:42 → short 0:47 (-55 s)
- 38 pauses cut (41 s)
- 3 retakes dropped: line 2 (x2), line 7
- dropped "ok let me do that again" at 0:58
```

## 5. Motion

From the script's visual notes (or your own picks when there are none):

- **Hook card**: the on-screen hook, 6 words or fewer, one `*accent*` word, 2 to 3 s.
- **Callouts**: a number, a result or a tool name the person says, about one every 8 to 10 s, never two within 4 s (Long: one every 30 to 60 s at most, only the key numbers). `atMs` = that word's `startMs` in the JSON.

Write `public/<slug>.edit.json` (format in [remotion-short.md](references/remotion-short.md) section 4).

## 6. QC, then render

Render 3 or 4 stills: the hook (frame 30), a callout, a caption mid-video, the last second (Long: 6 to 8 stills spread over the video). Short only: lay the platforms' safe zone over each one:

```bash
npx remotion still <comp> out/<slug>-qc-30.png --frame=30 --props=public/<slug>.edit.json
ffmpeg -y -v error -i out/<slug>-qc-30.png -vf "drawbox=x=0:y=0:w=iw:h=230:color=red@0.35:t=fill,drawbox=x=0:y=1440:w=iw:h=480:color=red@0.35:t=fill,drawbox=x=850:y=900:w=230:h=540:color=red@0.35:t=fill" out/<slug>-qc-30-safe.png
```

Read each `-safe` PNG (Long: each still): no text in a red zone (the app's buttons, name and description cover it), captions below the face, hook card readable, callout not covering the eyes, accent color right. Fix the edit file, then:

```bash
npx remotion render <comp> out/<slug>.mp4 --props=public/<slug>.edit.json
```

About 3 to 5 s of render per second of video on a laptop. Run it in the background and say how long.

## 7. Sound

Music (only if they ask, royalty-free, e.g. the YouTube Audio Library) goes in first, 22 dB under the voice:

```bash
ffmpeg -y -i out/<slug>.mp4 -stream_loop -1 -i "<music file>" -filter_complex "[1:a]volume=-22dB[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k out/<slug>-music.mp4
```

Then level the render (`out/<slug>-music.mp4` when there is music). Remotion does not level the voice, and a plain `loudnorm` pass lands 2 to 3 LU too quiet on clips this short. Measure:

```bash
ffmpeg -nostats -i out/<slug>.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
```

Gain = -14 minus the `I:` value (e.g. I = -17.0 → `3.0dB`), with a limiter:

```bash
mkdir -p ../edits/<slug>
ffmpeg -y -i out/<slug>.mp4 -c:v copy -af "volume=<gain>dB,alimiter=limit=0.8:level=false" -c:a aac -b:a 192k -ar 48000 ../edits/<slug>/final.mp4
```

Measure `final.mp4` the same way: I between -15 and -13 and Peak under -1 dBFS is right.

## 8. Deliver

In `video-agent/edits/<slug>/`:

- `final.mp4`, ready to post.
- `captions.srt`: the words moved to the cut timeline, up to 7 words per cue, a new cue after each sentence. Platforms read it as closed captions.
  ```bash
  node -e 'const e=require("./public/<slug>.edit.json"),w=require("./public/"+e.captions),F=30,fr=(ms)=>Math.round(ms/1000*F);let at=0;const p=e.ranges.map(r=>{const f=fr(r.fromMs),n=Math.max(1,fr(r.toMs)-f),q={...r,s:(at-f)/F*1000};at+=n;return q});const o=w.flatMap(x=>{const q=p.find(q=>x.startMs>=q.fromMs&&x.startMs<q.toMs);return q?[{t:x.text.trim(),a:x.startMs+q.s,b:Math.min(x.endMs,q.toMs)+q.s}]:[]});const ts=(ms)=>new Date(Math.max(0,Math.round(ms))).toISOString().slice(11,23).replace(".",",");let c=[],n=0,out="";const flush=()=>{if(c.length)out+=`${++n}\n${ts(c[0].a)} --> ${ts(c[c.length-1].b)}\n${c.map(x=>x.t).join(" ")}\n\n`;c=[]};for(const x of o){c.push(x);if(c.length===7||/[.?!]$/.test(x.t))flush()}flush();process.stdout.write(out)' > ../edits/<slug>/captions.srt
  ```
- `edit.json`: a copy of `public/<slug>.edit.json`, to redo the video later.
- `post.md`: the text to paste when posting (below).
- Long only, in `post.md`: **chapters** for the YouTube description, one every 1 to 3 minutes where the topic changes, times on the cut timeline (from `captions.srt`), the first at `0:00`, at least 3, each 10 s or longer.

Then say: length, what was cut, where the files are, and offer one change ("shorter hook card? fewer callouts? another accent?"). A change = edit the JSON, render again (steps 6 and 7). Next: `/video-publish <slug>`.

## Post copy

`post.md`, written from the script and voice.md, in the language of the video:

- **Title** (YouTube Shorts): under 60 characters, the topic in the first 3 words. Long: under 70 characters, the promise of the video, true to it.
- **Caption**: the first 125 characters work on their own (apps cut there behind "more"). Then 1 or 2 short lines and one ask, the one from voice.md.
- **Search words**: the 2 or 3 words their viewer would type to find this video, written plainly in the title or the first line.
- **Hashtags**: 3 to 5 at the end, about the topic. No #fyp or #viral.
- Nothing the video doesn't say: no new number, claim or promise.

Run the humanize pass of `video-script` (its `references/humanize.md`) on it when that skill is installed.

```text
Title: Your hook is too long
Caption: Nobody hears word 12 of your hook. Cut it to 12 words and put the result first.
Try it on your next three videos.
Follow for one script fix a day.
#shortformvideo #videohooks #contentcreator
```

## CapCut, Premiere or no Remotion

Some creators prefer their editor, and Remotion needs a paid license for companies of more than 3 people. Do steps 1 to 4, write `public/<slug>.edit.json` with the ranges (`"hook": null`, `"callouts": []`), skip steps 5 to 7, and give them `captions.srt` (step 8) plus:

- `cuts.md`, the kept ranges to cut by hand:
  ```bash
  mkdir -p ../edits/<slug>
  node -e 'const e=require("./public/<slug>.edit.json"),t=(ms)=>new Date(ms).toISOString().slice(14,23);for(const r of e.ranges)console.log(t(r.fromMs)+" → "+t(r.toMs))' > ../edits/<slug>/cuts.md
  ```
- or a plain cut with ffmpeg alone:
  ```bash
  SEL=$(node -e 'const e=require("./public/<slug>.edit.json");console.log(e.ranges.map(r=>`between(t,${r.fromMs/1000},${r.toMs/1000})`).join("+"))')
  ffmpeg -y -i public/<slug>.mp4 -vf "select='$SEL',setpts=N/FRAME_RATE/TB" -af "aselect='$SEL',asetpts=N/SR/TB" -c:v libx264 -crf 18 -c:a aac ../edits/<slug>/cut.mp4
  ```

## Honest limits

- whisper.cpp mishears names and jargon: the script fixes them, check numbers by eye.
- The cuts are good, not perfect: a cut can clip a breath or a soft last syllable. Watch the result once before posting.
- Claude cannot hear the take: it trusts the timings and silencedetect. Bad audio (music, echo, two voices) makes both worse.
- The safe zone is a middle ground between TikTok, Reels and Shorts; each app moves its buttons a little.
- Remotion license: free for individuals, companies of up to 3 people and non-profits; bigger companies need a company license (remotion.pro/license).
