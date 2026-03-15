---
name: react-bits
description: Build stunning animated React UIs using the react-bits component library — 110+ free, customizable text animations, UI components, and backgrounds.
---

# React Bits

**React Bits** (<https://reactbits.dev>) is the largest open-source library of animated, interactive React components. 110+ components across four categories, fully customizable via props, copy-paste ready.

> GitHub: <https://github.com/DavidHDev/react-bits> — 35k+ stars

---

## Installation

Each component is copy-paste or CLI installable via shadcn/jsrepo. No monolithic package install needed.

```bash
# Via shadcn (recommended)
npx shadcn@latest add @react-bits/<ComponentName>-TS-TW

# Examples
npx shadcn@latest add @react-bits/BlurText-TS-TW
npx shadcn@latest add @react-bits/AnimatedContent-TS-TW
npx shadcn@latest add @react-bits/Aurora-TS-TW

# Via jsrepo
npx jsrepo add github/DavidHDev/react-bits/src/ts-tailwind/<Category>/<ComponentName>
```

**4 variants per component** — choose based on your stack:
- `JS-CSS` — JavaScript + plain CSS
- `JS-TW` — JavaScript + Tailwind
- `TS-CSS` — TypeScript + plain CSS
- `TS-TW` — TypeScript + Tailwind (recommended)

---

## Component Categories

### 🌀 Animations (30+ components)
Scroll-triggered and interactive animation wrappers.

| Component | Description | Key Props |
|-----------|-------------|-----------|
| `AnimatedContent` | Slide/fade in on scroll (GSAP + ScrollTrigger) | `distance`, `direction`, `duration`, `ease`, `threshold` |
| `FadeContent` | Simple opacity fade on scroll | `blur`, `duration`, `threshold` |
| `Magnet` | Magnetic cursor attraction | `padding`, `disabled`, `magnetStrength` |
| `GlareHover` | 3D glare effect on hover | `glareColor`, `glareOpacity`, `glareAngle` |
| `StarBorder` | Animated star border around element | `color`, `speed`, `thickness` |
| `ElectricBorder` | Electrified animated border | `glowColor`, `animationDuration` |
| `ClickSpark` | Spark particles on click | `sparkColor`, `sparkSize`, `sparkCount` |
| `PixelTransition` | Pixel dissolve transition | `firstContent`, `secondContent`, `gridSize` |
| `ImageTrail` | Images follow cursor trail | `items`, `variant`, `rotationRange` |
| `LogoLoop` | Horizontal logo marquee | `items`, `speed`, `direction` |
| `Ribbons` | 3D ribbon animations | `colors`, `baseSpring`, `baseFriction` |
| `MetallicPaint` | Metallic paint fluid effect | `imageUrl`, `params` |
| `StickerPeel` | Sticker peel reveal effect | `width`, `height`, `peelPosition` |

### 🖼️ Backgrounds (35+ components)
Full-screen animated backgrounds.

| Component | Description | Key Props |
|-----------|-------------|-----------|
| `Aurora` | Northern lights animated gradient | `colorStops`, `blend`, `amplitude`, `speed` |
| `Particles` | Canvas particle system | `particleColors`, `particleCount`, `speed`, `moveParticlesOnHover` |
| `Waves` | Fluid wave animation | `lineColor`, `backgroundColor`, `waveSpeedX` |
| `Silk` | Silky fluid shader background | `speed`, `scale`, `color`, `noiseIntensity` |
| `Orb` | Glowing orb background | `hue`, `hueSpeed`, `forceField` |
| `Iridescence` | Rainbow iridescent shader | `color`, `speed`, `amplitude` |
| `Hyperspeed` | Hyperspace star warp | `preset` (one of 5 presets) |
| `Galaxy` | Animated galaxy background | `mouseRepulsion`, `density`, `speed` |
| `LiquidChrome` | Chrome liquid shader | `baseColor`, `speed`, `amplitude` |
| `Threads` | Flowing thread lines | `color`, `amplitude`, `distance`, `enableMouseInteraction` |
| `DotGrid` | Animated dot grid | `dotColor`, `glowColor`, `dotSize`, `gap` |
| `GridMotion` | Motion grid of items | `items`, `gradientColor` |
| `Squares` | Animated square grid | `direction`, `speed`, `squareSize`, `borderColor` |
| `Balatro` | Balatro card game aesthetic | `color`, `mouseInteraction` |
| `Noise` | Static noise texture | `patternSize`, `patternAlpha`, `grainSpeed` |
| `Lightning` | Lightning bolt background | `hue`, `xOffset`, `speed` |

### 🧩 Components (35+ components)
Interactive UI elements.

| Component | Description | Key Props |
|-----------|-------------|-----------|
| `GlassIcons` | Glassmorphism icon grid | `items`, `theme` |
| `TiltedCard` | 3D tilt card on hover | `imageSrc`, `captionText`, `containerHeight` |
| `SpotlightCard` | Spotlight follows cursor | `spotlightColor` |
| `Dock` | macOS-style dock | `items`, `magnification`, `panelHeight` |
| `Carousel` | Smooth animated carousel | `items`, `baseWidth`, `autoplay` |
| `CircularGallery` | 3D circular image gallery | `items`, `bend`, `textColor` |
| `MagicBento` | Animated bento grid layout | `textAutoHide`, `enableStars` |
| `Masonry` | Masonry image grid | `items`, `columns`, `gap` |
| `CardSwap` | Swipeable card stack | `cardDistance`, `verticalDistance`, `delay` |
| `InfiniteMenu` | Infinite scroll 3D menu | `items` |
| `FlowingMenu` | Flowing animated menu | `items` |
| `ElasticSlider` | Elastic spring slider | `defaultValue`, `elasticity` |
| `Counter` | Animated number counter | `value`, `fontSize`, `places` |
| `Folder` | Interactive file folder | `color`, `items`, `open` |
| `Stack` | Stacked card interaction | `randomRotation`, `sensitivity` |
| `ChromaGrid` | Chromatic image grid | `items`, `radius`, `damping` |
| `ScrollStack` | Stack on scroll | `items`, `itemDistance` |
| `ProfileCard` | 3D profile card | `name`, `title`, `avatarUrl` |
| `GooeyNav` | Gooey effect navigation | `items`, `particleCount` |
| `Stepper` | Animated step progress | `steps`, `initialStep` |
| `FluidGlass` | Fluid glass morphism | `width`, `height` |

### ✍️ Text Animations (25+ components)
Animated text effects.

| Component | Description | Key Props |
|-----------|-------------|-----------|
| `BlurText` | Words/letters blur in | `text`, `delay`, `animateBy`, `direction` |
| `SplitText` | Split text animation | `text`, `delay`, `animationFrom`, `animationTo` |
| `GlitchText` | Glitch effect on text | `speed`, `enableShadows`, `enableOnHover` |
| `GradientText` | Animated gradient text | `colors`, `animationSpeed`, `showBorder` |
| `ShinyText` | Metallic shiny text | `text`, `disabled`, `speed`, `className` |
| `FuzzyText` | Fuzzy hover distortion | `fontSize`, `fontWeight`, `color`, `enableHover` |
| `DecryptedText` | Matrix-style decrypt | `text`, `speed`, `revealDirection`, `sequential` |
| `ScrambledText` | Character scramble effect | `radius`, `duration`, `speed`, `scrambleChars` |
| `TextPressure` | Pressure-variable font | `text`, `flex`, `alpha`, `stroke` |
| `RotatingText` | Word rotation animation | `texts`, `staggerDuration`, `transition` |
| `CountUp` | Count up animation | `from`, `to`, `duration`, `separator` |
| `ASCIIText` | 3D ASCII art text | `text`, `enableWaves` |
| `ScrollFloat` | Text floats on scroll | `text`, `scrollStart`, `scrollEnd` |
| `ScrollVelocity` | Velocity-based marquee | `texts`, `velocity`, `damping` |
| `ScrollReveal` | Reveal text on scroll | `textColor`, `fillColor`, `threshold` |
| `VariableProximity` | Font varies with mouse | `label`, `fromFontVariationSettings`, `toFontVariationSettings` |
| `TrueFocus` | Focus blur on words | `sentence`, `blurAmount`, `animationDuration` |
| `CurvedLoop` | Text on curved path | `lines`, `radius`, `fontSize` |

---

## Usage Patterns

### Pattern 1: Scroll-triggered section reveal
```tsx
import AnimatedContent from '@/components/ui/AnimatedContent';

export function Section() {
  return (
    <AnimatedContent distance={60} direction="vertical" duration={0.7} delay={0.1}>
      <h2>Your Content</h2>
    </AnimatedContent>
  );
}
```

### Pattern 2: Animated hero background
```tsx
import Aurora from '@/components/ui/Aurora';
import BlurText from '@/components/ui/BlurText';

export function Hero() {
  return (
    <div className="relative h-screen">
      <Aurora colorStops={["#3A1C71", "#D76D77", "#FFAF7B"]} blend={0.5} amplitude={1.0} speed={0.5} />
      <div className="absolute inset-0 flex items-center justify-center">
        <BlurText text="Welcome to the Future" delay={150} animateBy="words" direction="top" className="text-6xl font-bold text-white" />
      </div>
    </div>
  );
}
```

### Pattern 3: Interactive card grid
```tsx
import TiltedCard from '@/components/ui/TiltedCard';

export function CardGrid() {
  return (
    <div className="grid grid-cols-3 gap-6">
      {items.map(item => (
        <TiltedCard
          key={item.id}
          imageSrc={item.image}
          captionText={item.title}
          containerHeight="300px"
          rotateAmplitude={12}
          scaleOnHover={1.05}
          showMobileWarning={false}
        />
      ))}
    </div>
  );
}
```

### Pattern 4: Animated navigation dock
```tsx
import Dock from '@/components/ui/Dock';
import { Home, Settings, User } from 'lucide-react';

const items = [
  { icon: <Home size={18} />, label: 'Home', onClick: () => {} },
  { icon: <User size={18} />, label: 'Profile', onClick: () => {} },
  { icon: <Settings size={18} />, label: 'Settings', onClick: () => {} },
];

export function Nav() {
  return <Dock items={items} magnification={60} distance={100} panelHeight={68} />;
}
```

### Pattern 5: Text scramble on hover
```tsx
import DecryptedText from '@/components/ui/DecryptedText';

export function HoverText() {
  return (
    <DecryptedText
      text="Hover to reveal"
      speed={50}
      maxIterations={20}
      revealDirection="center"
      enableHoverEffect={true}
      animateOn="hover"
      className="text-2xl font-mono"
    />
  );
}
```

---

## Dependencies by Component

Most components use one of these — install as needed:

```bash
# Motion (most text animations + components)
npm install motion

# GSAP (AnimatedContent, some animations)
npm install gsap

# Three.js (3D components: ASCIIText, ModelViewer, Hyperspeed)
npm install three @types/three

# OGL (shader backgrounds: Silk, Iridescence, LiquidChrome)
npm install ogl
```

---

## Component Source URLs

Browse and copy source at:
- **Docs**: <https://reactbits.dev>
- **GitHub source**: `https://github.com/DavidHDev/react-bits/tree/main/src/ts-tailwind/<Category>/<ComponentName>/`

Categories in source: `Animations/`, `Backgrounds/`, `Components/`, `TextAnimations/`

---

## Creative Tools

React Bits also provides free browser-based tools at <https://reactbits.dev/tools>:
- **Background Studio** — customize animated backgrounds, export as video/image/code
- **Shape Magic** — inner rounded corners between shapes, export SVG/React/clip-path
- **Texture Lab** — apply noise, dithering, ASCII effects to images/videos
