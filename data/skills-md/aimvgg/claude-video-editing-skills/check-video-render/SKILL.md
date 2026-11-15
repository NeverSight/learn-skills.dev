---
name: check-video-render
description: "Checks a finished video render before anyone watches or posts it. A script gates frame count, audio that runs to the last frame, silent tails, loudness and true peak, faststart and Chrome playback, and lists scene cuts. Then it walks through the checks that need eyes and ears, such as faces inside punch-ins, text at phone size, generated residue and the rights and consent ledger. Built for AI music videos and hype videos, and works on any MP4 export. Use after every render or export and before sending a draft or posting, for 'is it ready to post?', 'check this render', 'QC this export', 'why does the end go silent?', 'it won't play in Chrome' or 'did ffmpeg drop frames?'."
license: Apache-2.0
compatibility: "Needs Python 3, ffmpeg and ffprobe."
---

# Check a render

Run the script first; it catches the mechanical failures. Then do the checks that need eyes.

Run it from the user's project folder. In the commands below, replace `<skill folder>` with the absolute path of the folder that holds this `SKILL.md`, the path you read it from. Never type the placeholder itself. If you do not know that path, look in the skills folder your agent installed it to, and ask the user if it is not there.

## 1. Run the script

```bash
python3 -I "<skill folder>/scripts/check.py" out/video.mp4 --frames 902 --fps 30 --lufs -14 --cuts
```

Pass `--frames` and `--fps` from the plan. Without `--fps` the frame rate is printed, not checked. Other flags are `--lufs-tol` (default 1), `--tp` (default -1 dBTP) and `--allow-silent-tail`, which you pass only when the plan ends in silence on purpose. Exit 0 means every check passed, 1 means at least one failed, and 2 means the script could not read the file. The last line of output is a JSON summary.

It fails on:

- **Frame count** different from the plan. ffmpeg `-shortest` once cut 3 frames off a 902-frame video. Drop `-shortest` and trim to the planned frame count yourself.
- **Audio shorter than video** by more than a frame, or **a silent tail**. A mix filter (`amix`, sidechain) ended early once and the last second went silent in the shipped file.
- **Loudness** off target and **true peak** above -1 dBTP, measured on the encoded file. The script checks -14 LUFS unless you pass `--lufs`. Use -14 for most platforms, or the reference's own level for a remake. AAC at 320k raised the true peak; 256k did not. To fix loudness, run ffmpeg `loudnorm=I=-14:TP=-1.5` on the mix before the final encode, then check again.
- **Browser playability.** H.264 above level 5.1 (for example a CRF 8 master at level 6.2) fails to decode in Chrome. Keep the master for a desktop player and make a share copy for everything else.

  ```bash
  ffmpeg -i out/video.mp4 -c:v libx264 -profile:v high -level 4.2 -pix_fmt yuv420p -crf 19 -maxrate 20M -bufsize 40M -c:a aac -b:a 256k -movflags +faststart out/video.share.mp4
  ```
- **Frame rate** different from `--fps`, when you pass it.
- **No audio stream.**
- **Not H.264 in `yuv420p`.** A 4:4:4 or 10-bit master fails here too. Judge it in a desktop player and check the share copy.
- **No faststart.** The `moov` box comes after the media, so a browser has to download the whole file before it plays. Fix it with `ffmpeg -i in.mp4 -c copy -movflags +faststart out.mp4`.

Run the script on the MP4 you will share. The faststart and browser checks do not apply to MKV or WebM masters.

`--cuts` lists every frame scoring over 7 on `scdet`. Compare it with the cuts you planned. An extra cut means a shot runs into the next shot of its source.

## 2. Look

- **Contact sheets.** Tile the start, middle and end of every shot. Read them yourself; agents and people both miss things at playback speed.
- **Faces in punch-ins.** For every zoom, punch or crop, run a face detector (for example MediaPipe) on each frame of the punch-in. Fail it when the face is outside the crop in more than 15% of those frames. Write down any deliberate exception, such as a punch onto a sweater.
- **Last frames of generated takes.** Step through them. Video models can add a flash or a morph at the end.
- **Text.** Check every tag and title at phone size. A second line under a tag is often unreadable; cut it. Interpolated frames smear text.
- **Generated residue.** Look for the old subject's face, jersey numbers or logos leaking through a swap.

## 3. Listen

Compare the render against the reference or the previous cut. Check momentary and short-term loudness, true peak, the level of six frequency bands each second, stereo width and a spectrogram overlay. Listen to every seam and the last two seconds.

## 4. Rights and consent ledger

Before anything is shared, every clip in the video has a row with its public URL, source seconds and what it is used for. Every real person who is swapped or impersonated has consent recorded, in `consent.json` in the project when `v2v-video-to-video-swap` made the swap. Commercial music, sports and film footage are flagged so the user decides where to post. The ledger is what the recipe cites.

## About

Made free and open source by [Arcmira](https://arcmira.com), the search engine for what people say in podcasts and videos. This skill is one of the [Claude video editing skills](https://github.com/aimvgg/claude-video-editing-skills), written while making real hype videos and AI music videos. Shipped by [Zeal](https://x.com/zealcaiden).
