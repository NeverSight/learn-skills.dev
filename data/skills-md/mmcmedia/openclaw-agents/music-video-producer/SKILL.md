---
name: music-video-producer
description: Assemble music videos using Remotion (React-based video framework). Takes scene plans, video assets, lyrics, and audio to create final MP4 videos with synchronized lyrics and visual effects. Use when building music videos for PsalMix or any video composition task requiring programmatic video editing.
---

# Music Video Producer - Remotion Assembly

Build music videos programmatically using Remotion, syncing video clips, lyrics, and audio into polished final renders.

## Prerequisites

**Install Remotion:**
```bash
npm install remotion @remotion/cli
```

**Or create new Remotion project:**
```bash
npx create-video@latest
```

**Required inputs:**
1. Scene plan JSON (from creative-director)
2. Video assets (from video-asset-manager)
3. Audio file (MP3/WAV)
4. Lyrics file (.srt or plain text)

## Workflow

### 1. Set Up Remotion Project

**Project structure:**
```
music-video-project/
├── src/
│   ├── Root.tsx          # Main composition registration
│   ├── MusicVideo.tsx    # Main video component
│   ├── Scene.tsx         # Individual scene component
│   └── LyricOverlay.tsx  # Lyric display component
├── public/
│   ├── audio/
│   │   └── song.mp3
│   ├── assets/
│   │   ├── scene-01-sunrise.mp4
│   │   └── ...
│   └── lyrics.srt
├── package.json
└── remotion.config.ts
```

### 2. Build Remotion Composition

**Root.tsx** - Register composition:
```tsx
import { Composition } from 'remotion';
import { MusicVideo } from './MusicVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MusicVideo"
      component={MusicVideo}
      durationInFrames={6300} // 3:30 at 30fps
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```

**MusicVideo.tsx** - Main video logic:
```tsx
import { Audio, Sequence, useCurrentFrame } from 'remotion';
import { Scene } from './Scene';
import { LyricOverlay } from './LyricOverlay';
import sceneplan from '../scene-plan.json';

export const MusicVideo: React.FC = () => {
  const frame = useCurrentFrame();
  
  return (
    <>
      <Audio src="/audio/song.mp3" />
      
      {sceneplan.scenes.map((scene, i) => (
        <Sequence
          key={i}
          from={scene.startFrame}
          durationInFrames={scene.durationFrames}
        >
          <Scene
            videoSrc={scene.videoAsset}
            transition={scene.transition}
          />
          <LyricOverlay
            text={scene.lyrics}
            style={scene.lyricDisplay}
          />
        </Sequence>
      ))}
    </>
  );
};
```

**Scene.tsx** - Video clip display:
```tsx
import { Video, interpolate } from 'remotion';

export const Scene: React.FC<{ videoSrc: string; transition: string }> = ({
  videoSrc,
  transition
}) => {
  const frame = useCurrentFrame();
  
  const opacity = interpolate(
    frame,
    [0, 30, 60, 90],
    [0, 1, 1, 0], // fade in/out
    { extrapolateRight: 'clamp' }
  );
  
  return (
    <Video
      src={videoSrc}
      style={{ opacity }}
      muted
    />
  );
};
```

**LyricOverlay.tsx** - Lyric display:
```tsx
import { AbsoluteFill } from 'remotion';

export const LyricOverlay: React.FC<{ text: string; style: string }> = ({
  text,
  style
}) => {
  return (
    <AbsoluteFill style={{
      justifyContent: style === 'bottom' ? 'flex-end' : 'center',
      alignItems: 'center',
      padding: 40
    }}>
      <div style={{
        fontSize: 48,
        fontWeight: 'bold',
        color: 'white',
        textShadow: '2px 2px 4px rgba(0,0,0,0.8)',
        textAlign: 'center'
      }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};
```

### 3. Convert Scene Plan to Remotion Format

**Helper script:** `scripts/convert_scene_plan.js`

Converts creative-director JSON to Remotion-ready format with frame numbers:
```bash
node scripts/convert_scene_plan.js \
  --input scene-plan.json \
  --output src/scene-plan-frames.json \
  --fps 30
```

Adds `startFrame` and `durationInFrames` to each scene based on timestamps.

### 4. Render Video

**Preview in browser:**
```bash
npm start
```

**Render final MP4:**
```bash
npx remotion render MusicVideo output.mp4 --codec h264
```

**Render with quality settings:**
```bash
npx remotion render MusicVideo output.mp4 \
  --codec h264 \
  --crf 18 \
  --audio-bitrate 320k
```

**Render for social media (square):**
```bash
npx remotion render MusicVideo output-square.mp4 \
  --width 1080 \
  --height 1080 \
  --codec h264
```

### 5. Advanced Features

**Audio visualization:**
```tsx
import { useAudioData, visualizeAudio } from '@remotion/media-utils';

const audioData = useAudioData('/audio/song.mp3');
const visualization = visualizeAudio({
  fps: 30,
  frame,
  audioData,
  numberOfSamples: 16
});

// Render bars based on visualization array
```

**Captions from .srt:**
```tsx
import { parseSrt } from '@remotion/captions';

const captions = parseSrt(srtContent);
const currentCaption = captions.find(
  (c) => frame >= c.startFrame && frame < c.endFrame
);
```

**Dynamic text animations:**
```tsx
import { spring } from 'remotion';

const scale = spring({
  frame,
  fps: 30,
  config: { damping: 100 }
});
```

## Scripts

### `scripts/convert_scene_plan.js`

Convert scene plan timestamps to frame numbers - see file for implementation.

### `scripts/render_all_formats.sh`

Batch render multiple formats (YouTube, Instagram, TikTok) - see file for implementation.

## Reference Files

- `references/remotion-examples.md` - Code examples for common patterns
- `references/transition-effects.md` - Crossfade, wipe, zoom transitions
- `references/lyric-styles.md` - Typography and animation patterns

## Quality Checklist

Before final render:
- [ ] Audio syncs perfectly with video
- [ ] Lyrics display at correct times
- [ ] Scene transitions are smooth
- [ ] No visual glitches or artifacts
- [ ] Brand elements (logos) visible throughout
- [ ] Resolution is correct (1080p minimum)
- [ ] Audio quality is high (320kbps+)
- [ ] Preview full video before final render

## Deliverables

1. **Final MP4 video(s)** - Full render in desired format(s)
2. **Remotion project files** - Source code for future edits
3. **Render settings documentation** - Codec, bitrate, resolution used

## Troubleshooting

**Video stutters or drops frames:**
- Reduce preview quality (lower fps/resolution)
- Use `--concurrency 1` flag for rendering
- Pre-process heavy video files

**Audio out of sync:**
- Ensure all timestamps in scene plan are accurate
- Check fps matches between plan and composition
- Use `--enforce-audio-track` flag

**Render takes too long:**
- Use `--concurrency` flag to parallelize
- Consider cloud rendering (Remotion Lambda)
- Optimize video clip file sizes

## PsalMix Branding

For PsalMix videos, include:
- Logo watermark (lower right, 10% opacity)
- End card with "Stream clean music at psalmix.com"
- PsalMix brand colors in lyric styling
- Clean, family-friendly aesthetic throughout
