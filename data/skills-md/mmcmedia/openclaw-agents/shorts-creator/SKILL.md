---
name: shorts-creator
description: Create vertical 9:16 video clips from full music videos for Instagram Reels, TikTok, and YouTube Shorts. Takes full-length music video and extracts key moments, re-frames for mobile, and optimizes for social platforms. Use when creating short-form social content from PsalMix music videos or any video content.
---

# Shorts Creator - Social Media Clip Generator

Transform full-length music videos into platform-optimized vertical clips for Instagram Reels, TikTok, and YouTube Shorts.

## Workflow

### 1. Input Requirements

**Required:**
- Full music video MP4 (from music-video-producer)
- Lyrics file (.srt or plain text)
- Audio file (MP3/WAV)
- Scene plan JSON (from creative-director)

**Optional:**
- Target platforms (Instagram/TikTok/YouTube/All)
- Clip strategy (chorus-focused, lyric highlights, full song segments)
- Brand overlays (logo, CTA, @handle)

### 2. Clip Selection Strategy

**Auto-detect best moments:**
1. **Chorus/Hook** - Most repeatable, catchy section
2. **Lyric highlights** - Powerful lines with visual impact
3. **First 15 seconds** - Hook viewers immediately
4. **Peak energy moments** - Musical climax, beat drops

**Manual selection:**
- Specify timestamp ranges (e.g., "1:15-1:45")
- Choose specific scenes by number
- Target specific lyrics

### 3. Platform Specifications

**Instagram Reels:**
- Aspect ratio: 9:16 (1080x1920)
- Duration: 15-90 seconds (optimal: 30-45s)
- Format: MP4, H.264
- Max file size: 4GB

**TikTok:**
- Aspect ratio: 9:16 (1080x1920)
- Duration: 15-60 seconds (optimal: 21-34s)
- Format: MP4, H.264
- Max file size: 287MB

**YouTube Shorts:**
- Aspect ratio: 9:16 (1080x1920)
- Duration: Up to 60 seconds
- Format: MP4, H.264
- Max file size: 256GB

### 4. Clip Generation Process

**Using FFmpeg (via script):**

```bash
# Extract segment (1:15 to 1:45)
python scripts/extract_clip.py \
  --input full-video.mp4 \
  --start 75 \
  --duration 30 \
  --output clip-01.mp4

# Convert to vertical 9:16
python scripts/reframe_vertical.py \
  --input clip-01.mp4 \
  --output clip-01-vertical.mp4 \
  --strategy zoom-center

# Add platform branding
python scripts/add_branding.py \
  --input clip-01-vertical.mp4 \
  --output clip-01-final.mp4 \
  --platform instagram \
  --logo assets/psalmix-logo.png \
  --cta "Full video on YouTube 🎵"
```

### 5. Re-framing Strategies

**Options for landscape → vertical:**

**A. Zoom & Pan (Recommended)**
- Zoom into video center
- Crops sides, keeps focus on main subject
- Smooth pan follows action/lyrics
- Best for: Videos with centered subjects

**B. Letterbox with Background**
- Add blurred/colored background
- Original video stays 16:9 in center
- Fills vertical space with aesthetic bars
- Best for: Scenic, wide-shot videos

**C. Split Screen**
- Top 50%: Original video (small)
- Bottom 50%: Zoomed/cropped detail
- Best for: Lyric-focused content

**D. Dynamic Crop**
- Intelligently crops to follow motion
- AI-detects faces/main subjects
- Keeps important content in frame
- Best for: Action-heavy videos

### 6. Overlay Elements

**Platform-specific CTAs:**
- Instagram: "Full song on YouTube 🎵 Link in bio"
- TikTok: "Full video on my page! #PsalMix"
- YouTube: "Subscribe for more clean music 🎶"

**Branding:**
- Logo: Lower right corner (small, 10% opacity)
- Handle: Bottom center "@psalmix" (last 3 seconds)
- Artist credit: Top overlay "Song: [Title] by [Artist]"

**Engagement hooks:**
- First 2 seconds: "Wait for the drop 🔥"
- Last 3 seconds: "Tag someone who needs this ❤️"
- Mid-clip: "Send this to your bestie 💯"

### 7. Batch Processing

**Generate multiple clips from one video:**

```bash
python scripts/batch_clips.py \
  --input full-video.mp4 \
  --scene-plan scene-plan.json \
  --strategy chorus-focus \
  --platforms instagram,tiktok,youtube \
  --output-dir clips/
```

**Outputs:**
```
clips/
├── instagram/
│   ├── chorus-15s.mp4
│   ├── hook-30s.mp4
│   └── lyric-highlight-45s.mp4
├── tiktok/
│   ├── chorus-21s.mp4
│   └── hook-30s.mp4
└── youtube/
    ├── chorus-30s.mp4
    └── full-song-60s.mp4
```

### 8. Optimization Best Practices

**For maximum engagement:**
- **First 3 seconds:** Hook viewer with best moment
- **Captions ON:** 85% watch without sound
- **High contrast:** Pops on small screens
- **Bold text:** Readable on mobile
- **Trending audio:** Use original audio + hashtags

**For algorithm:**
- Post at peak times (7-9pm)
- Use 3-5 relevant hashtags
- Engage in comments within 1 hour
- Cross-post to Stories
- Pin top-performing clips

## Scripts

### `scripts/extract_clip.py`

Extract time segment from full video:
```bash
python scripts/extract_clip.py \
  --input video.mp4 \
  --start 75 \
  --duration 30 \
  --output clip.mp4
```

### `scripts/reframe_vertical.py`

Convert landscape to 9:16 vertical:
```bash
python scripts/reframe_vertical.py \
  --input clip.mp4 \
  --output vertical.mp4 \
  --strategy zoom-center
```

### `scripts/add_branding.py`

Add logo, CTA, platform-specific overlays:
```bash
python scripts/add_branding.py \
  --input vertical.mp4 \
  --output branded.mp4 \
  --platform instagram \
  --logo logo.png
```

### `scripts/batch_clips.py`

Generate multiple clips automatically:
```bash
python scripts/batch_clips.py \
  --input video.mp4 \
  --scene-plan scene-plan.json \
  --platforms instagram,tiktok \
  --output-dir clips/
```

## Reference Files

- `references/platform-specs.md` - Detailed requirements for each platform
- `references/ffmpeg-commands.md` - Common FFmpeg recipes for video editing
- `references/engagement-hooks.md` - Proven text overlays and CTAs

## PsalMix Branding

**Logo placement:**
- Position: Lower right corner
- Size: 80x80px
- Opacity: 15% (subtle)
- Duration: Full clip

**Colors:**
- Primary: #667eea (Purple gradient)
- Text: White with black shadow
- Background: Dark overlay (50% opacity) for readability

**CTAs:**
- "Stream clean music at psalmix.com 🎵"
- "Christian music you can trust ✨"
- "Family-friendly vibes only 🙏"

## Quality Checklist

Before publishing clips:
- [ ] Aspect ratio is exactly 9:16 (1080x1920)
- [ ] Audio syncs perfectly (no drift)
- [ ] Captions are readable on mobile
- [ ] Logo/branding visible but not distracting
- [ ] First 3 seconds hook viewer
- [ ] CTA visible in last 3 seconds
- [ ] File size under platform limits
- [ ] Tested on actual device (iPhone/Android)
- [ ] Hashtags and caption ready

## Deliverables

1. **Platform-specific clips** - Optimized MP4 for each target platform
2. **Caption templates** - Suggested text for each clip
3. **Hashtag suggestions** - Trending + evergreen tags
4. **Posting schedule** - Optimal times for each platform

## Advanced Features

**A/B Testing clips:**
- Generate 2-3 variations per clip
- Different hooks, CTAs, text overlays
- Test which performs best
- Double down on winners

**Trend integration:**
- Overlay trending sounds (TikTok)
- Use popular hashtag challenges
- Remix format (duet/stitch opportunities)

**Analytics tracking:**
- Encode UTM parameters in CTA links
- Track views/engagement per clip
- Iterate based on performance
