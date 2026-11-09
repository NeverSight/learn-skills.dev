---
name: lottie-bodymovin
description: Use when implementing Disney's 12 animation principles with Lottie animations exported from After Effects
---

# Lottie Animation Principles

Implement all 12 Disney animation principles using Lottie (Bodymovin) for vector animations.

## 1. Squash and Stretch

In After Effects before export:
- Animate Scale X and Y inversely
- Use expression: `s = transform.scale[1]; [100 + (100-s), s]`

```javascript
// Control at runtime
lottie.setSpeed(1.5); // affect squash timing
```

## 2. Anticipation

Structure your AE composition:
1. **Frames 0-10**: Wind-up pose
2. **Frames 10-40**: Main action
3. **Frames 40-50**: Settle

```javascript
// Play anticipation segment
anim.playSegments([0, 10], true);
setTimeout(() => anim.playSegments([10, 50], true), 200);
```

## 3. Staging

```javascript
// Layer multiple Lotties
<div className="scene">
  <Lottie animationData={background} style={{ opacity: 0.6 }} />
  <Lottie animationData={hero} style={{ zIndex: 10 }} />
</div>
```

## 4. Straight Ahead / Pose to Pose

Pose to pose in AE:
- Set keyframes at key poses
- Let AE interpolate between
- Use Easy Ease for smoothing

```javascript
// Jump to specific poses
anim.goToAndStop(25, true); // frame 25
```

## 5. Follow Through and Overlapping Action

In After Effects:
- Offset child layer keyframes by 2-4 frames
- Use parenting with delayed expressions
- `thisComp.layer("Parent").transform.position.valueAtTime(time - 0.05)`

## 6. Slow In and Slow Out

AE Keyframe settings:
- Select keyframes > Easy Ease (F9)
- Use Graph Editor to adjust curves
- Bezier handles control acceleration

```javascript
// Adjust playback speed dynamically
anim.setSpeed(0.5); // slower
anim.setSpeed(2); // faster
```

## 7. Arc

In After Effects:
- Use motion paths (position property)
- Convert keyframes to Bezier
- Pull handles to create arcs
- Or use "Auto-Orient to Path"

## 8. Secondary Action

```javascript
// Trigger secondary animation
mainAnim.addEventListener('complete', () => {
  secondaryAnim.play();
});

// Or sync with frame
mainAnim.addEventListener('enterFrame', (e) => {
  if (e.currentTime > 15) particleAnim.play();
});
```

## 9. Timing

```javascript
anim.setSpeed(0.5);  // half speed - dramatic
anim.setSpeed(1);    // normal
anim.setSpeed(2);    // double speed - snappy

// Or control frame rate in AE export
// 24fps = cinematic, 30fps = smooth, 60fps = fluid
```

## 10. Exaggeration

In After Effects:
- Push scale beyond 100% (120-150%)
- Overshoot rotation
- Use Overshoot expression
- `amp = 15; freq = 3; decay = 5; n = 0; time_start = key(1).time; if (time > time_start) { n = (time - time_start) / thisComp.frameDuration; amp * Math.sin(freq*n) / Math.exp(decay*n/100); } else { 0; }`

## 11. Solid Drawing

In After Effects:
- Use 3D layers
- Apply perspective camera
- Animate Z position and rotation
- Use depth of field

## 12. Appeal

Design principles in AE:
- Smooth curves over sharp angles
- Consistent timing patterns
- Pleasing color palette
- Clean vector shapes

```javascript
// React Lottie with hover
<Lottie
  animationData={data}
  onMouseEnter={() => anim.setDirection(1)}
  onMouseLeave={() => anim.setDirection(-1)}
/>
```

## Lottie Implementation

```javascript
import Lottie from 'lottie-react';
import animationData from './animation.json';

<Lottie
  animationData={animationData}
  loop={true}
  autoplay={true}
  style={{ width: 200, height: 200 }}
/>
```

## Key Lottie Features

- `playSegments([start, end])` - Play frame range
- `setSpeed(n)` - Control timing
- `setDirection(1/-1)` - Forward/reverse
- `goToAndStop(frame)` - Pose control
- `addEventListener` - Frame events
- Interactivity via `lottie-interactivity`
