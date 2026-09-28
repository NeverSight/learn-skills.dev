---
name: reel-export
description: Turn any horizontal or square motion video into a 1080 x 1920 Instagram Reel or TikTok that uploads cleanly. Headline and logos inside the safe zone, H.264, yuv420p, limited colour range, bt709, a silent audio track when there is no sound, and an ffprobe check before upload. Use when someone says "make this a reel", "vertical version", "export for Instagram", "TikTok version", "9:16 cut", "reel export" or has a 16:9 or 4:5 video that needs to go on a vertical feed.
---

# Reel export

Most motion is built wide. This turns it into a vertical file with a hook on top that the apps accept without washing out the colours.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them.

## Step 1: Ask for four things, then wait

1. **The video.** Any MP4, any size.
2. **The headline,** two short lines, word for word. It is the hook people read with the sound off.
3. **Logos,** as attached files, if the video names a product or company.
4. **The background colour** around the video. Default: near-black `#0B0B0F`.

## Step 2: The safe zone

The app draws its own buttons, caption and profile over the edges of a Reel. Keep every word and logo:
- between y 360 and y 1420 (nothing in the bottom 500px)
- out of the right 120px

Put the headline at the top of that zone, then the video under it. A 16:9 video scaled to 1080 wide is 608 tall, so it sits well at y 660.

## Step 3: Build the overlay, then encode

Build a transparent 1080 x 1920 `overlay.png` in HTML with the headline and any logos, and screenshot it. Text you can style beats text burned in by ffmpeg. Then:

```
ffmpeg -y -i in.mp4 -loop 1 -i overlay.png -f lavfi -i anullsrc=r=48000:cl=stereo -filter_complex "color=c=0x0B0B0F:s=1080x1920:r=30[bg];[0:v]fps=30,scale=1080:-2,setsar=1[v];[bg][v]overlay=0:660:shortest=1[o];[o][1:v]overlay=0:0:shortest=1,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[out]" -map "[out]" -map 2:a -shortest -c:v libx264 -profile:v high -crf 18 -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 128k -movflags +faststart reel.mp4
```

This adds a silent AAC track. If the video has its own sound, swap `-map 2:a` for `-map 0:a`.

## Step 4: Check before upload

```
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,pix_fmt,color_range,color_space -of compact reel.mp4
```

Pass means: video `h264`, `1080` x `1920`, `yuv420p`, `color_range=tv`, `bt709`, plus one `aac` audio stream. If you see `hevc` or `color_range=pc`, encode again. Then pull one frame from the middle and look at it at phone size.

## What I learned the hard way

- **A phone recording is often HEVC and full range.** Uploaded as is, it can come out washed out or re-encoded badly. Always export a fresh H.264, limited-range file, including after any edit.
- **A logo over footage vanishes on light frames.** Put each logo (and its label) on its own dark rounded tile.
- **faststart matters.** Without `-movflags +faststart` the file cannot start playing until it has fully loaded.
- **Keep the hook to two lines.** Mine were short enough to read in a second: "This Mac launch" / "is 100% code".
