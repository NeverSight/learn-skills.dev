---
name: remotion-templates
description: Remotion video templates collection - curated templates, design principles, and patterns for AI coding agents
metadata:
  tags: remotion, video, react, animation, templates, captions, audio, 3d, social-media
---

## Purpose

This skill provides Claude Code and AI coding agents with comprehensive context for building production-ready videos using Remotion. It includes design principles, curated templates, and best practices.

## When to Use

Use this skill when:
- Creating video content programmatically with React
- Building podcast audiograms or audio visualizations
- Adding animated captions to videos (TikTok/Reels style)
- Creating 3D product showcases
- Building a video generation SaaS
- Making data visualization videos
- Generating social media content at scale

---

## Video Design Principles

### 1. Pacing & Rhythm
- **Fast cuts**: 1-2 seconds for energy (social media)
- **Medium pace**: 3-5 seconds for comprehension (tutorials)
- **Slow pace**: 5-10 seconds for emphasis (cinematic)
- **Match audio**: Sync transitions to beats/speech

### 2. Visual Hierarchy
- One focal point per frame
- Use motion to guide attention
- Contrast important elements
- Maintain consistent spacing

### 3. Text on Video Rules
- Maximum 7 words per frame
- High contrast (white on dark, or outlined)
- Leave text on screen long enough to read 2x
- Position in lower third or center
- Avoid edges (safe zone: 10% margin)

### 4. Animation Timing
| Element | Duration | Easing |
|---------|----------|--------|
| Text appear | 8-15 frames | easeOut |
| Text exit | 6-10 frames | easeIn |
| Scene transition | 15-30 frames | easeInOut |
| Logo reveal | 30-60 frames | spring |
| Quick cut | 0-3 frames | linear |

### 5. Frame Rates
- **30fps**: Standard video, social media
- **60fps**: Smooth motion, gaming content
- **24fps**: Cinematic feel
- **25fps**: European broadcast

### 6. Aspect Ratios
| Platform | Ratio | Resolution |
|----------|-------|------------|
| YouTube | 16:9 | 1920x1080 |
| TikTok/Reels | 9:16 | 1080x1920 |
| Instagram Feed | 1:1 | 1080x1080 |
| Instagram Story | 9:16 | 1080x1920 |
| Twitter | 16:9 | 1280x720 |
| LinkedIn | 16:9 | 1920x1080 |

---

## Quick Start

### Installation
```bash
# New project with template selection
npx create-video@latest

# Manual setup
mkdir my-video && cd my-video
npm init -y
npm install remotion @remotion/cli react react-dom
npm install -D typescript @types/react
```

### Project Structure
```
src/
├── index.ts           # registerRoot
├── Root.tsx           # Composition definitions
├── compositions/
│   ├── Main.tsx       # Main video
│   └── Intro.tsx      # Intro sequence
├── components/
│   ├── Text.tsx       # Animated text
│   └── Logo.tsx       # Logo reveal
└── assets/
    ├── fonts/
    ├── images/
    └── audio/
```

### Root.tsx Template
```tsx
import { Composition } from 'remotion';
import { Main } from './compositions/Main';

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="Main"
        component={Main}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "My Video"
        }}
      />
    </>
  );
};
```

---

## Core Patterns

### Animation Fundamentals
```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

const frame = useCurrentFrame();
const { fps, width, height, durationInFrames } = useVideoConfig();

// Linear interpolation (clamped)
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: 'clamp'
});

// Spring animation (bouncy)
const scale = spring({
  frame,
  fps,
  config: { damping: 12, stiffness: 200 }
});

// Delayed spring
const delayedScale = spring({
  frame: frame - 15, // 15 frame delay
  fps,
  config: { damping: 10 }
});
```

### Sequencing
```tsx
import { Sequence, AbsoluteFill } from 'remotion';

export const MyVideo = () => (
  <AbsoluteFill>
    <Sequence from={0} durationInFrames={60}>
      <Intro />
    </Sequence>
    <Sequence from={60} durationInFrames={120}>
      <MainContent />
    </Sequence>
    <Sequence from={180}>
      <Outro />
    </Sequence>
  </AbsoluteFill>
);
```

### Text Animation
```tsx
const TextReveal = ({ text }: { text: string }) => {
  const frame = useCurrentFrame();
  const words = text.split(' ');

  return (
    <div style={{ display: 'flex', gap: 10, justifyContent: 'center' }}>
      {words.map((word, i) => {
        const delay = i * 5;
        const opacity = interpolate(frame - delay, [0, 10], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp'
        });
        const y = interpolate(frame - delay, [0, 10], [20, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp'
        });

        return (
          <span key={i} style={{ opacity, transform: `translateY(${y}px)` }}>
            {word}
          </span>
        );
      })}
    </div>
  );
};
```

### Audio Sync
```tsx
import { Audio, useCurrentFrame, interpolate } from 'remotion';
import { getAudioDurationInSeconds } from '@remotion/media-utils';

// Volume envelope
const frame = useCurrentFrame();
const volume = interpolate(frame, [0, 30, 270, 300], [0, 1, 1, 0]);

<Audio src={staticFile('music.mp3')} volume={volume} />
```

---

## Template Catalog

### Captions & Subtitles

#### remotion-subtitles (17 Styles)
```bash
npm install @ahgsql/remotion-subtitles
```

```tsx
import { Subtitle } from '@ahgsql/remotion-subtitles';

// Available styles: bounce, fire, glitch, neon, typewriter,
// 3d, lightning, glowing, explosive, wave, slide, fade,
// zoom, rotate, flip, shake, pulse

<Subtitle
  src={staticFile('captions.srt')}
  style="bounce"
  fontSize={48}
  color="#ffffff"
  strokeColor="#000000"
  strokeWidth={2}
/>
```

#### TikTok-Style Captions
```tsx
const Caption = ({ text, highlight }: { text: string; highlight: number }) => {
  const words = text.split(' ');

  return (
    <div style={{
      position: 'absolute',
      bottom: '20%',
      width: '100%',
      textAlign: 'center',
      fontSize: 64,
      fontWeight: 900,
      textTransform: 'uppercase'
    }}>
      {words.map((word, i) => (
        <span
          key={i}
          style={{
            color: i === highlight ? '#FFE135' : '#FFFFFF',
            textShadow: '4px 4px 0 #000, -4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000'
          }}
        >
          {word}{' '}
        </span>
      ))}
    </div>
  );
};
```

### Audio Visualization

#### Waveform Visualizer
```tsx
import { useAudioData, visualizeAudio } from '@remotion/media-utils';

const Waveform = ({ src }: { src: string }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const audioData = useAudioData(src);

  if (!audioData) return null;

  const visualization = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: 64
  });

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
      {visualization.map((amplitude, i) => (
        <div
          key={i}
          style={{
            width: 8,
            height: amplitude * 200,
            backgroundColor: '#667eea',
            borderRadius: 4
          }}
        />
      ))}
    </div>
  );
};
```

#### Circular Audio Visualizer
```tsx
const CircularVisualizer = ({ audioData, frame, fps }) => {
  const visualization = visualizeAudio({ fps, frame, audioData, numberOfSamples: 32 });
  const radius = 150;

  return (
    <svg width={400} height={400} viewBox="0 0 400 400">
      {visualization.map((amp, i) => {
        const angle = (i / visualization.length) * Math.PI * 2;
        const x1 = 200 + Math.cos(angle) * radius;
        const y1 = 200 + Math.sin(angle) * radius;
        const x2 = 200 + Math.cos(angle) * (radius + amp * 100);
        const y2 = 200 + Math.sin(angle) * (radius + amp * 100);

        return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#667eea" strokeWidth={4} />;
      })}
    </svg>
  );
};
```

### 3D with Three.js

#### Setup
```bash
npm install @remotion/three three @react-three/fiber @react-three/drei
```

#### Phone Mockup
```tsx
import { ThreeCanvas } from '@remotion/three';
import { useFrame } from '@react-three/fiber';

const PhoneMockup = ({ videoSrc }: { videoSrc: string }) => {
  const frame = useCurrentFrame();
  const rotation = interpolate(frame, [0, 150], [0, Math.PI * 2]);

  return (
    <ThreeCanvas>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <mesh rotation={[0, rotation, 0]}>
        <boxGeometry args={[2, 4, 0.2]} />
        <meshStandardMaterial color="#1a1a2e" />
      </mesh>
    </ThreeCanvas>
  );
};
```

### Social Media Templates

#### Instagram Reel Intro
```tsx
const ReelIntro = ({ username, avatar }: Props) => {
  const frame = useCurrentFrame();
  const scale = spring({ frame, fps: 30, config: { damping: 12 } });

  return (
    <AbsoluteFill style={{ background: 'linear-gradient(135deg, #667eea, #764ba2)' }}>
      <div style={{
        transform: `scale(${scale})`,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100%'
      }}>
        <img
          src={avatar}
          style={{ width: 120, height: 120, borderRadius: '50%', border: '4px solid white' }}
        />
        <h1 style={{ color: 'white', fontSize: 48, marginTop: 20 }}>@{username}</h1>
      </div>
    </AbsoluteFill>
  );
};
```

#### YouTube Subscribe CTA
```tsx
const SubscribeCTA = () => {
  const frame = useCurrentFrame();
  const slideIn = interpolate(frame, [0, 20], [100, 0], { extrapolateRight: 'clamp' });
  const bellWiggle = Math.sin(frame * 0.5) * 10;

  return (
    <div style={{
      position: 'absolute',
      bottom: 50,
      right: 50,
      transform: `translateX(${slideIn}%)`,
      display: 'flex',
      alignItems: 'center',
      gap: 20,
      background: 'rgba(0,0,0,0.8)',
      padding: '20px 30px',
      borderRadius: 50
    }}>
      <div style={{
        background: '#FF0000',
        padding: '12px 24px',
        borderRadius: 4,
        color: 'white',
        fontWeight: 'bold'
      }}>
        SUBSCRIBE
      </div>
      <div style={{ transform: `rotate(${bellWiggle}deg)`, fontSize: 32 }}>
        🔔
      </div>
    </div>
  );
};
```

---

## Effects Library

### Glitch Effect
```tsx
const GlitchText = ({ text }: { text: string }) => {
  const frame = useCurrentFrame();
  const glitchOffset = Math.random() > 0.9 ? Math.random() * 10 - 5 : 0;

  return (
    <div style={{ position: 'relative' }}>
      <span style={{
        position: 'absolute',
        left: glitchOffset,
        color: 'cyan',
        clipPath: 'inset(0 0 50% 0)'
      }}>
        {text}
      </span>
      <span style={{
        position: 'absolute',
        left: -glitchOffset,
        color: 'magenta',
        clipPath: 'inset(50% 0 0 0)'
      }}>
        {text}
      </span>
      <span style={{ color: 'white' }}>{text}</span>
    </div>
  );
};
```

### Particle Field
```tsx
const Particles = ({ count = 50 }: { count?: number }) => {
  const frame = useCurrentFrame();
  const particles = useMemo(() =>
    Array.from({ length: count }, () => ({
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 4 + 2,
      speed: Math.random() * 0.5 + 0.2
    })),
    []
  );

  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: `${p.x}%`,
            top: `${(p.y + frame * p.speed) % 100}%`,
            width: p.size,
            height: p.size,
            borderRadius: '50%',
            background: 'rgba(255,255,255,0.5)'
          }}
        />
      ))}
    </AbsoluteFill>
  );
};
```

### Gradient Background
```tsx
const AnimatedGradient = () => {
  const frame = useCurrentFrame();
  const hue = (frame * 2) % 360;

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(
          ${frame}deg,
          hsl(${hue}, 70%, 50%),
          hsl(${(hue + 60) % 360}, 70%, 50%),
          hsl(${(hue + 120) % 360}, 70%, 50%)
        )`
      }}
    />
  );
};
```

---

## CLI Commands

```bash
# Development
npm run dev                    # Start Remotion Studio
npx remotion studio            # Same thing

# Render video
npx remotion render Main out.mp4
npx remotion render Main out.mp4 --props='{"title":"Hello"}'
npx remotion render Main out.mp4 --codec=h265 --crf=18

# Render still image
npx remotion still Main out.png --frame=30

# Common flags
--codec=h264|h265|vp8|vp9|prores
--crf=18           # Quality (lower = better, 15-23 typical)
--scale=2          # 2x resolution
--concurrency=4    # Parallel rendering
--muted            # No audio
```

---

## Deployment Options

### Remotion Lambda (AWS)
```bash
npm install @remotion/lambda
npx remotion lambda sites create
npx remotion lambda render [site-name] Main
```

### GitHub Actions
```yaml
- uses: remotion-dev/render@v1
  with:
    composition: Main
    output: video.mp4
```

### SST/Pulumi
```bash
git clone https://github.com/karelnagel/remotion-sst
```

---

## Recommended Templates by Use Case

| Use Case | Template | URL |
|----------|----------|-----|
| Podcast clips | template-audiogram | remotion-dev/template-audiogram |
| TikTok captions | remotion-subtitles | ahgsql/remotion-subtitles |
| Music videos | audio-visualizers | marcusstenbeck/remotion-audio-visualizers |
| Product demos | template-three | remotion-dev/template-three |
| Video SaaS | template-next-app-dir-tailwind | remotion-dev/template-next-app-dir-tailwind |
| Dev portfolios | github-stats | LukasParke/github-stats-remotion |
| Code tutorials | template-code-hike | remotion-dev/remotion |
| YouTube intros | fireship-intro | thecmdrunner/fireship-remotion-intro |

---

## Quick Reference

| Task | Code |
|------|------|
| Get frame | `useCurrentFrame()` |
| Get config | `useVideoConfig()` |
| Interpolate | `interpolate(frame, [0, 30], [0, 1])` |
| Spring | `spring({ frame, fps, config: { damping: 12 } })` |
| Sequence | `<Sequence from={30} durationInFrames={60}>` |
| Image | `<Img src={staticFile('img.png')} />` |
| Video | `<Video src={staticFile('vid.mp4')} />` |
| Audio | `<Audio src={staticFile('audio.mp3')} volume={0.5} />` |
| Static file | `staticFile('public/file.png')` |
| Full container | `<AbsoluteFill>` |

---

## Resources

- [Remotion Docs](https://remotion.dev/docs)
- [Remotion Showcase](https://remotion.dev/showcase)
- [Remotion Discord](https://remotion.dev/discord)
- [Template Gallery](https://remotion.dev/templates)
