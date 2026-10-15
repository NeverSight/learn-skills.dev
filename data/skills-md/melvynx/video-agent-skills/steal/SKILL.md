---
name: steal
description: Copies another creator's editing style into a named style that short-editing applies to your own takes. Use when the user says steal, "copy the style of", "edit like @x", "make a style from this reel", "vole le style de", or gives a reel or short as the model for a look. Downloads the reel (yt-dlp, or Treg for Instagram and TikTok), MEASURES the style with ffmpeg instead of eyeballing it (contact sheets, hard cuts per second, a spectrogram for the beat and the sound effects on the cuts, the music level under the voice, the face size and the zooms), writes video-agent/styles/<name>.md, then edits a test video with short-editing and compares it frame by frame with the original.
argument-hint: "<reel URL or video file> [style name]"
allowed-tools: Bash(yt-dlp *) Bash(ffmpeg *) Bash(ffprobe *) Bash(treg catalog *) Bash(treg balance)
---

# Steal

Someone's edit works and you want it on your own videos. This skill measures their edit, writes it down as a style, and proves it on one of your takes before you use it.

Output:

- `video-agent/styles/<name>.md`: the style, read by `/short-editing <take> style <name>`.
- `video-agent/styles/<name>/`: its stills, sound effects and stickers.
- `video-agent/edits/<slug>-<name>/final.mp4`: the test video.

Read [references/learnings.md](references/learnings.md) before you start. Each rule in it comes from a copy that got rejected.

## How to run it

- Preflight: `ffmpeg -version && yt-dlp --version`. Missing: `/studio-setup tools`.
- Talk in the creator's language. Say what you do in one line before each long step.
- `<name>`: the creator's handle in lowercase with dashes, unless the user names the style.
- Scratch files go in `video-agent/.tmp/steal-<name>/` (`W` below).

## 1. Get the reel

- A local file: use it.
- A YouTube link: `yt-dlp -o "W/reel.%(ext)s" "<url>"`.
- Instagram or TikTok: try `yt-dlp` first. If it is blocked (login wall), and Treg is set up (`treg balance` answers), `treg catalog search "download an Instagram reel video file"`, then `treg catalog get <id>` for the price, then `treg call <id> --query url=<url>` and download the video URL it returns. Otherwise ask the user to save the video and give you the file.
- When you can, study 2 or 3 reels of the same format. One reel can be the exception.

## 2. Measure

Do all three passes. A style copied from the frames alone misses half of it: the sound and the rhythm.

**Faster with sub-agents.** If your agent can run sub-agents (Claude Code, Codex), make the sheets and `cuts.txt` yourself (first block below), then hand Frames, Sound and Zooms to three sub-agents at the same time. Give each one the absolute paths, its section copied whole, and one file to write: `W/notes-frames.md`, `W/notes-sound.md`, `W/notes-zooms.md`, numbers and timestamps only, never playing audio aloud. Look at the sheets yourself while they work: you judge the look, they bring the numbers. Then write the style from their notes. Without sub-agents, do the passes one after the other.

### Frames and cuts

```bash
ffmpeg -v error -y -i W/reel.mp4 -vf "fps=2,scale=270:480,tile=8x3:padding=4:color=black" W/sheet-%02d.jpg
ffmpeg -hide_banner -i W/reel.mp4 -vf "scdet=threshold=12" -an -f null - 2>&1 | grep -o "scd.time: [0-9.]*" | cut -d' ' -f2 > W/cuts.txt
ffprobe -v error -show_entries format=duration -of csv=p=0 W/reel.mp4
```

- Each sheet holds 24 tiles at 2 per second. Sheet N, tile i (from 0) shows second 12(N-1) + i/2.
- Seconds per shot = duration / (number of lines in `cuts.txt` + 1).

Read EVERY sheet and write down:

- **Layouts**: full camera, split screen (where the seam sits), flat color with text, cut-out person on a color, B-roll, screenshots.
- **Captions, per layout**: font feel (condensed, rounded, serif), case, weight, size, where they sit on the body, how a word appears, which word gets emphasised and how.
- **Stickers and images**: type, border, size, when they land (on the word that names them?), whether they stack.
- **Hook** (first 2 s), **CTA** (last 3 s), **color grade** (bright and flat, or contrasty and dark).

Save 6 to 10 key stills to `video-agent/styles/<name>/`:

```bash
ffmpeg -v error -y -ss <seconds> -i W/reel.mp4 -frames:v 1 video-agent/styles/<name>/t<seconds>.jpg
```

### Sound

```bash
ffmpeg -v error -y -i W/reel.mp4 -lavfi "showspectrumpic=s=3000x500:legend=0:scale=log:stop=11000" W/spectrum.png
```

- The image is 3000 px wide, so a cut at t seconds sits at x = 3000 × t / duration. Read it next to `cuts.txt`.
- A bright thin vertical stroke high up = a click. Wide and low = a boom. A rising smear = a whoosh. A dark gap across the steady music band = the beat drops out.
- Zoom on one cut to see its hit: `ffmpeg -v error -y -ss <cut - 1> -t 2 -i W/reel.mp4 -lavfi "showspectrumpic=s=1000x500:legend=0:scale=log:stop=11000" W/cut-<n>.png`.
- **Beat**: count the regular low strokes over 10 s on the spectrogram (or tap along while it plays): strokes per 10 s × 6 = BPM.

**Music level under the voice** (optional, needs `ELEVENLABS_API_KEY` in `video-agent/.env`, uses a few credits, say so first):

```bash
set -a; . video-agent/.env; set +a
ffmpeg -v error -y -i W/reel.mp4 -vn -ac 1 -ar 44100 W/full.wav
curl -s -X POST https://api.elevenlabs.io/v1/audio-isolation -H "xi-api-key: $ELEVENLABS_API_KEY" -F audio=@W/full.wav -o W/voice.mp3
ffmpeg -v error -y -i W/voice.mp3 -ac 1 -ar 44100 W/voice.wav
for f in full voice; do ffmpeg -v error -i W/$f.wav -af "asetnsamples=882,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-" -f null - | grep -o "RMS_level=.*" | cut -d= -f2 > W/rms-$f.txt; done
paste W/rms-voice.txt W/rms-full.txt | awk '$1<-40{print $2}' | sort -n | awk '{a[NR]=$1}END{print "music while the voice is silent:", a[int(NR/2)+1], "dB over", NR/50, "s"}'
awk '$1>-30' W/rms-voice.txt | sort -n | awk '{a[NR]=$1}END{print "voice while talking:", a[int(NR/2)+1], "dB"}'
```

- These commands measure the level every 20 ms. The music is the full mix in the moments the isolated voice is silent.
- Music under the voice = the voice level minus the music level.
- Under 1 s of silence (an edit with every pause cut) is too little to trust: judge it on the spectrogram.
- Never subtract the isolated voice from the mix: it is not in phase with the original, so the result comes out louder than the voice.
- Without a key, judge the level on the spectrogram.

Write down where the music starts and which event gets which sound: cut, sticker, zoom, impact.

### Zooms

On the sheets, measure the face height as a share of the frame height on 10 tiles or so, and list the jumps in face size from one tile to the next:

- a jump at a cut = a change of framing between two shots
- a jump inside a shot = a punch-in
- a slow growth over a shot = a push

Write the range (e.g. face 12 to 25 % of the frame), the punch-ins per 10 s, and whether there is a push. These numbers are the ceiling for your copy.

## 3. Write the style

`video-agent/styles/<name>.md`, in the user's language, with the same sections as `short-editing`'s [style.md](../short-editing/references/style.md). Each line gives a value and the measurement behind it:

```markdown
# Style: <name>

Copied from <link>, measured on <date>. Applied on top of short-editing's style.md: what is not here stays as there.

## Cuts
- hard cut every 1.4 s on average (35 cuts in 50 s); no fade, no transition
## Framing
- face 12 to 25 % of the frame; punch-in 1.1 at most, about every 4 s, held until the next cut; slow push 0.6 %/s
## Captions
- ...
## Stickers and images
- ...
## Sound
- boom bap beat ~90 BPM from the hook impact, 12 dB under the voice, drops out 0.3 s on punch-ins
- a dry high click on most cuts (sfx/cut.wav), a pop on each sticker (sfx/pop.wav)
## Grade
- ffmpeg: eq=contrast=1.08:saturation=0.9,vignette=PI/5,unsharp=5:5:0.4
## Left out
- the AI video clips: replaced by your own footage or a callout
## How short-editing applies it
- the components to add to the composition and the props they take
```

**Sound effects** (in `video-agent/styles/<name>/sfx/`):

- With an ElevenLabs key, generate 2 or 3 takes per sound and keep the one closest to the original on the spectrogram:
  ```bash
  curl -s -X POST https://api.elevenlabs.io/v1/sound-generation -H "xi-api-key: $ELEVENLABS_API_KEY" -H "content-type: application/json" -d '{"text":"single dry short high click, tight transient, no reverb","duration_seconds":0.5}' -o video-agent/styles/<name>/sfx/cut-a.mp3
  ```
- Otherwise, use a royalty-free library.

**Stickers**:

1. Generate them with `/codex-images`. Use the user's REAL photos as the face reference, never a generated face. Ask for a flat #00FF00 background, no shadow, no text.
2. Key the background out to a transparent PNG:
   ```bash
   ffmpeg -v error -y -i sticker.png -vf "colorkey=0x00FF00:0.3:0.08,despill=type=green" -pix_fmt rgba sticker-cut.png
   ```

**Logos**: every app named on screen shows its real logo, never a letter in a circle.

## 4. Test it

1. Pick a 10 to 20 s take of the user from `video-agent/takes/`.
2. Run `/short-editing <take> style <name>`. It reads the style file and adds what it describes to the composition: stickers on the word that names them, sound effects on the cuts, the grade.
3. The slug is `<take slug>-<name>`.

## 5. Compare before showing

Put the original on top and the copy below, at the same seconds:

```bash
ffmpeg -v error -y -i W/reel.mp4 -i video-agent/edits/<slug>/final.mp4 -filter_complex "[0:v]fps=1,scale=216:384,trim=end_frame=15,tile=15x1[a];[1:v]fps=1,scale=216:384,trim=end_frame=15,tile=15x1[b];[a][b]vstack" -frames:v 1 W/compare.jpg
```

Go tile by tile:

- type size and weight
- sticker and logo size (they fill the space like in the original)
- grade
- no fade where the original cuts hard
- captions off the mouth
- nothing upside down

Run the spectrogram on the copy too: the hits must land on the cuts, the beat must sit at the same level under the voice. Measure the face size on its sheets: no more zooms than the original, the face never bigger.

With sub-agents, give the compare sheet, the key stills and the list above to a fresh-eyes sub-agent while you check the sound and the zooms: it reports every tile that differs. Fix every gap before showing. The user should never be the one to spot it.

## 6. Deliver

Open `final.mp4`, then tell the user in a few lines:

- what was measured (seconds per shot, BPM, music level, zooms)
- what was copied, and what was left out and why
- where the style lives

From now on, `/short-editing <take> style <name>` uses it. Each time the user rejects something, write it in the style file. When the lesson is general, add it to [references/learnings.md](references/learnings.md).
