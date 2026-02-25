---
name: text-animation-copier
description: Copy and recreate text animations from video examples using Remotion. This skill analyzes video frames to identify text animation patterns (timing, movement, styling, effects) and generates corresponding Remotion React components. Use when the user asks to replicate, copy, or recreate text animations from a video sample.
---

# Text Animation Copier for Remotion

Analyze and recreate text animations from video examples as Remotion React components with precise timing, styling, and effects.

## Quick Start

### Prerequisites

Before using this skill, ensure you have:
1. **ffmpeg installed** - Required for video frame extraction
2. **Remotion project set up** - Working remotion-animations repository
3. **Video URL or file path** - Direct link or local path to the video containing the animation

### Basic Workflow

When the user provides a video with a text animation to copy:

1. **Download and extract frames** from the video (use `claude-skills/video-viewing`)
2. **Analyze the animation** by examining key frames
3. **Identify animation properties** (timing, effects, positioning, styling)
4. **Generate Remotion component** that recreates the animation
5. **Test and refine** the animation in Remotion Studio

## Detailed Process

### Step 1: Download Video and Extract Frames

Use the `video-viewing` skill to download the video and extract frames:

```bash
python scripts/download_video.py "VIDEO_URL" -f
```

This downloads the video to `/mnt/user-data/outputs/` and extracts frames for analysis.

**Alternative:** If the user provides a local video file path, use ffmpeg directly:

```bash
# Extract frames at 1 frame per second
ffmpeg -i path/to/video.mp4 -vf fps=1 /tmp/frames/frame-%04d.png

# Extract frames at specific time interval (e.g., 00:07 to 00:13)
ffmpeg -i path/to/video.mp4 -ss 00:07 -to 00:13 -vf fps=2 /tmp/frames/frame-%04d.png
```

### Step 2: Analyze Animation by Examining Frames

The user will typically specify a time range (e.g., "00:07 - 00:13"). Extract and analyze frames from that range:

1. **Identify start and end frames** of the animation
2. **Examine key transition points** (when animation changes behavior)
3. **Ignore background video** - focus ONLY on text elements
4. **Document observations** about:
   - Text content and positioning
   - Font family, size, weight, color
   - Animation type (fade, slide, scale, rotate, flip, etc.)
   - Timing and easing curves
   - Multi-stage animations (e.g., bar fill, then text appear)
   - Special effects (3D transforms, shadows, glows, particles)

### Step 3: Identify Animation Properties

Based on frame analysis, document these key properties:

#### Timing Configuration
- **Duration**: Total animation length in seconds/frames
- **FPS**: Video frame rate (typically 30fps for web videos)
- **Key moments**: Frame numbers for important transitions
- **Easing**: Type of easing curve (linear, ease-in-out, cubic, bezier)

Example timing structure:
```typescript
const TIMING = {
  PHASE_1_START: 0,
  PHASE_1_END: 45,
  PHASE_2_START: 48,
  PHASE_2_END: 90,
  HOLD_END: 180,
};
```

#### Text Styling
- **Font family**: Arial, Helvetica, custom fonts
- **Font size**: In pixels
- **Font weight**: normal, bold, 300-900
- **Color**: Hex or rgba values
- **Letter spacing**: Additional spacing between characters
- **Text alignment**: left, center, right

#### Positioning
- **Alignment**: center, top-left, bottom-left, etc.
- **Offset values**: Distance from edges in pixels
- **Responsive positioning**: Use viewport width/height for centering

#### Animation Effects

Common text animation patterns:

**1. Fade In/Out**
```typescript
const opacity = interpolate(
  frame,
  [START_FRAME, END_FRAME],
  [0, 1],
  {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  }
);
```

**2. Slide In/Out**
```typescript
const translateX = interpolate(
  frame,
  [START_FRAME, END_FRAME],
  [-500, 0], // from left to center
  {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  }
);
```

**3. Scale Animation**
```typescript
const scale = interpolate(
  frame,
  [START_FRAME, END_FRAME],
  [0, 1],
  {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.elastic(1),
  }
);
```

**4. 3D Rotation/Flip**
```typescript
const rotateY = interpolate(
  frame,
  [START_FRAME, END_FRAME],
  [0, 360],
  {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  }
);

// Apply with CSS transform
transform: `rotateY(${rotateY}deg)`,
transformStyle: "preserve-3d",
perspective: "1000px"
```

**5. Bar Fill Animation**
```typescript
const barProgress = interpolate(
  frame,
  [BAR_START, BAR_END],
  [0, 1],
  {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.25, 0.1, 0.25, 1),
  }
);

// Apply to width
width: `${barProgress * 100}%`
```

**6. Staggered Animation (for multiple letters/words)**
```typescript
// Each letter starts with a delay
const letterStart = BASE_START + index * STAGGER_DELAY;
const letterEnd = letterStart + ANIMATION_DURATION;

const letterOpacity = interpolate(
  frame,
  [letterStart, letterEnd],
  [0, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);
```

**7. Spring Physics**
```typescript
const scale = spring({
  frame: frame - START_FRAME,
  fps: 30,
  config: {
    damping: 10,
    stiffness: 100,
    mass: 0.5,
  },
});
```

### Step 4: Generate Remotion Component

Create a new React component in `src/animations/text-animation-N/` following these patterns:

#### Component Structure Template

```typescript
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
  spring,
} from "remotion";

// Animation timing configuration (in frames, at 30fps)
// Reference video time range: HH:MM:SS - HH:MM:SS
const TIMING = {
  ANIMATION_START: 0,
  ANIMATION_END: 60,
  // Add more timing points as needed
};

// Configuration constants
const TEXT = "YOUR TEXT HERE";
const FONT_SIZE = 48;
const FONT_FAMILY = "Arial, sans-serif";
const TEXT_COLOR = "#FFFFFF";

export const TextAnimationN: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  // Calculate animation values based on current frame
  const opacity = interpolate(
    frame,
    [TIMING.ANIMATION_START, TIMING.ANIMATION_END],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.inOut(Easing.ease),
    }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "transparent", // Always transparent for overlays
      }}
    >
      {/* Your animation elements here */}
      <div
        style={{
          fontFamily: FONT_FAMILY,
          fontSize: `${FONT_SIZE}px`,
          color: TEXT_COLOR,
          opacity: opacity,
          // Add positioning, transforms, etc.
        }}
      >
        {TEXT}
      </div>
    </AbsoluteFill>
  );
};
```

#### Important Requirements

1. **Resolution**: Always use 1920x1080 (configured in Root.tsx)
2. **Transparent background**: `backgroundColor: "transparent"`
3. **Center positioning**: Use `width/2` and `height/2` for centering
4. **Timing precision**: Match the original video timing as closely as possible
5. **Clean code**: Add comments explaining each animation phase

### Step 5: Register the Composition

Add the new animation to `src/Root.tsx`:

```typescript
import { TextAnimationN } from "./animations/text-animation-N/TextAnimationN";

<Composition
  id="TextAnimationN"
  component={TextAnimationN}
  durationInFrames={180} // Adjust based on animation length
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{}}
/>
```

### Step 6: Test in Remotion Studio

```bash
npm start
```

This opens Remotion Studio at `http://localhost:3000` where you can:
- Preview the animation in real-time
- Scrub through frames to verify timing
- Compare with the original video
- Adjust values and see immediate results

### Step 7: Render the Animation

Once satisfied with the animation:

```bash
# Render as WebM with transparency (recommended)
npm run render:text-animation-N

# Or add custom render script to package.json:
npx remotion render src/index.ts TextAnimationN out/text-animation-N.webm --codec vp9 --pixel-format yuva420p
```

## Advanced Techniques

### Per-Letter Animation

For animations where each letter animates independently:

```typescript
const Letter: React.FC<{
  char: string;
  index: number;
  totalLetters: number;
}> = ({ char, index, totalLetters }) => {
  const frame = useCurrentFrame();

  // Stagger each letter's animation
  const letterDelay = index * 3; // 3 frames delay per letter
  const letterStart = TIMING.ANIMATION_START + letterDelay;

  const opacity = interpolate(
    frame,
    [letterStart, letterStart + 15],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <span style={{ opacity }}>
      {char}
    </span>
  );
};

// In main component:
const letters = TEXT.split("").map((char, i) => (
  <Letter key={i} char={char} index={i} totalLetters={TEXT.length} />
));
```

### Multi-Stage Animations

For complex animations with multiple sequential phases:

```typescript
// Phase 1: Slide in
const slideProgress = interpolate(
  frame,
  [TIMING.SLIDE_START, TIMING.SLIDE_END],
  [0, 1],
  {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  }
);

// Phase 2: Scale pulse (starts after slide completes)
const scaleProgress = interpolate(
  frame,
  [TIMING.SCALE_START, TIMING.SCALE_END],
  [1, 1.2],
  {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  }
);

// Phase 3: Fade out
const fadeOutProgress = interpolate(
  frame,
  [TIMING.FADEOUT_START, TIMING.FADEOUT_END],
  [1, 0],
  {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  }
);

// Combine all phases
const translateX = slideProgress * width;
const scale = frame >= TIMING.SCALE_START ? scaleProgress : 1;
const opacity = frame >= TIMING.FADEOUT_START ? fadeOutProgress : 1;
```

### Background Effects

For text with animated backgrounds (like TextAnimation2):

```typescript
// Background appears behind text with 3D rotation
<div
  style={{
    position: "absolute",
    width: charWidth + 20,
    height: fontSize + 20,
    backgroundColor: BACKGROUND_COLOR,
    transform: `rotateY(${bgRotateY}deg) scaleX(${bgScaleX})`,
    transformStyle: "preserve-3d",
    opacity: bgOpacity,
    zIndex: -1, // Behind text
  }}
/>
```

### Custom Easing Functions

For precise timing matches:

```typescript
// Built-in easing options:
Easing.linear           // Constant speed
Easing.ease             // Gentle start and end
Easing.in(Easing.quad)  // Accelerate
Easing.out(Easing.quad) // Decelerate
Easing.inOut(Easing.cubic) // Smooth S-curve
Easing.bezier(0.25, 0.1, 0.25, 1) // Custom cubic bezier

// Available easing functions:
// quad, cubic, poly, sin, exp, circle, back, bounce, elastic
```

## Technology Reference

### Core Remotion Hooks

- **`useCurrentFrame()`**: Returns current frame number
- **`useVideoConfig()`**: Returns `{ fps, width, height, durationInFrames }`
- **`interpolate(value, inputRange, outputRange, options)`**: Map values smoothly
- **`spring(options)`**: Physics-based animations
- **`Sequence`**: Layer multiple animations with offsets

### Essential Remotion Components

- **`<AbsoluteFill>`**: Full-screen positioned container
- **`<Sequence from={frame} durationInFrames={frames}>`**: Time-shifted animations
- **`<Audio>`**: Background music/sound effects
- **`<Video>`**: Embed video backgrounds
- **`<Img>`**: Static or animated images

### CSS Transform Properties

For 3D effects, use these transform properties:

```css
perspective: 1000px;              /* Enable 3D space */
transformStyle: preserve-3d;      /* Maintain 3D in children */
backfaceVisibility: hidden;       /* Hide back of element */

/* Transform functions: */
transform: translateX(px) translateY(px) translateZ(px)
          rotateX(deg) rotateY(deg) rotateZ(deg)
          scale(factor) scaleX() scaleY()
          skewX(deg) skewY(deg);
```

## Common Animation Patterns

### 1. Text Lower Third (like TextAnimation1)

- Colored bars that fill from left to right
- Text appears after bars complete
- Positioned in corner (typically bottom-left)

### 2. Flying Text with 3D Flip (like TextAnimation2)

- Text flies in from off-screen
- Each letter flips in 3D while moving
- Background boxes rotate into place behind letters
- Staggered timing for visual interest

### 3. Typewriter Effect

```typescript
const visibleChars = Math.floor(
  interpolate(
    frame,
    [START, END],
    [0, TEXT.length],
    { extrapolateRight: "clamp" }
  )
);

return <div>{TEXT.substring(0, visibleChars)}</div>;
```

### 4. Bounce In

```typescript
const bounceScale = spring({
  frame: frame - START_FRAME,
  fps: 30,
  config: {
    damping: 12,
    stiffness: 200,
    mass: 0.5,
  },
});
```

### 5. Glitch Effect

```typescript
const glitchOffset = Math.random() * 10 - 5;
const glitchActive = frame % 10 === 0; // Every 10 frames

return (
  <div style={{
    transform: glitchActive
      ? `translate(${glitchOffset}px, ${glitchOffset}px)`
      : 'none',
  }}>
    {TEXT}
  </div>
);
```

## Best Practices

### 1. Timing Precision
- **Convert time to frames**: For 30fps, 1 second = 30 frames
- **Match original timing**: Use video time codes to set TIMING constants
- **Account for delays**: Stagger animations for visual flow

### 2. Performance
- **Avoid complex calculations per frame**: Pre-calculate when possible
- **Use interpolate over manual math**: It's optimized and handles edge cases
- **Minimize re-renders**: Keep component logic simple

### 3. Code Organization
- **Constants at top**: TIMING, COLORS, SIZES in one place
- **Comments for phases**: Document what each animation phase does
- **Reusable components**: Extract repeated patterns (like Letter component)

### 4. Visual Fidelity
- **Match fonts closely**: Use web-safe fonts or load custom fonts
- **Color accuracy**: Use color picker on video frames
- **Positioning precision**: Measure distances in video frames

### 5. Testing Workflow
- **Test in Remotion Studio**: Immediate visual feedback
- **Compare side-by-side**: Play original video alongside your animation
- **Check all frames**: Scrub through to verify smooth transitions
- **Render and review**: Final render may look different from preview

## Troubleshooting

### Animation doesn't match timing
- Verify FPS matches original video (usually 30fps)
- Check TIMING constants are accurate
- Use `console.log(frame)` to debug frame values

### Text positioning is off
- Double-check `width` and `height` from `useVideoConfig()`
- Verify centering calculations: `width/2 - textWidth/2`
- Test different viewport sizes in Remotion Studio

### Animation is choppy
- Increase `durationInFrames` in composition
- Check easing function is smooth (not linear)
- Verify frame rate is consistent (30fps)

### 3D transforms not working
- Add `perspective: "1000px"` to parent
- Include `transformStyle: "preserve-3d"`
- Check browser supports 3D transforms

### Text doesn't appear
- Verify `opacity` is not 0
- Check `zIndex` stacking
- Ensure color contrasts with background
- Confirm frame range includes text appearance

## Example Workflows

### Example 1: Simple Fade In Text

User provides: Video with text fading in from 00:03 to 00:05

1. Download video and extract frames
2. Analyze frames: Text "HELLO" fades from 0% to 100% opacity
3. Calculate frames: 3s to 5s = frame 90 to 150 (at 30fps)
4. Create component with fade interpolation
5. Test and render

### Example 2: Multi-Line Text with Stagger

User provides: Video with 3 lines of text appearing sequentially from 00:10 to 00:15

1. Extract frames from 10-15 seconds
2. Identify: Line 1 appears at 10s, Line 2 at 12s, Line 3 at 14s
3. Calculate timing for each line (30fps)
4. Create component with 3 text elements, each with offset timing
5. Test stagger delays match original
6. Render

### Example 3: Complex Multi-Stage Animation

User provides: Video with text that slides in, rotates, then slides out from 00:20 to 00:30

1. Extract frames every 0.5 seconds
2. Identify phases:
   - Phase 1 (20-23s): Slide in from left
   - Phase 2 (23-26s): Rotate 360 degrees
   - Phase 3 (26-30s): Slide out to right
3. Create TIMING constants for each phase
4. Implement 3 separate interpolations
5. Combine transforms in style object
6. Test smooth transitions between phases
7. Render and compare

## Integration with Other Skills

This skill works best when combined with:

- **`claude-skills/video-viewing`**: For downloading videos and extracting frames
- **`remotion-best-practices`**: For advanced Remotion techniques
- **Video editing knowledge**: Understanding of timing, easing, keyframes

## Output Checklist

When delivering a text animation recreation, ensure:

- [ ] Component created in `src/animations/text-animation-N/`
- [ ] Registered in `src/Root.tsx`
- [ ] Resolution is 1920x1080
- [ ] Background is transparent
- [ ] Text is centered (if specified)
- [ ] Timing matches original video
- [ ] TIMING constants documented with comments
- [ ] Code is clean and well-commented
- [ ] Tested in Remotion Studio
- [ ] Render script added to package.json (optional)
- [ ] Original video time range noted in comments

## Quick Reference Commands

```bash
# Download video with frame extraction
python scripts/download_video.py "VIDEO_URL" -f

# Start Remotion Studio for testing
npm start

# Type check the code
npm run typecheck

# Render animation
npx remotion render src/index.ts TextAnimationN out/output.webm --codec vp9 --pixel-format yuva420p

# Extract specific time range from video
ffmpeg -i input.mp4 -ss 00:07 -to 00:13 -vf fps=2 output-%04d.png
```

## Useful Resources

- Remotion Documentation: https://www.remotion.dev/docs
- Remotion Easing Visualizer: https://www.remotion.dev/docs/easing
- Cubic Bezier Generator: https://cubic-bezier.com/
- CSS Transform Reference: https://developer.mozilla.org/en-US/docs/Web/CSS/transform

## Summary

This skill enables you to systematically analyze text animations in videos and recreate them as reusable Remotion components. The key is careful observation, precise timing conversion, and leveraging Remotion's powerful interpolation and animation capabilities.

Always prioritize matching the original animation's timing and visual feel over pixel-perfect reproduction. Small variations in easing or timing can make animations feel more natural while still capturing the essence of the original.
