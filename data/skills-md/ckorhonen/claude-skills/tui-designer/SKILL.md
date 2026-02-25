---
name: tui-designer
description: Design and implement retro/cyberpunk/hacker-style terminal UIs. Covers React (Tuimorphic), SwiftUI (Metal shaders), and CSS approaches. Use when creating terminal aesthetics, CRT effects, neon glow, scanlines, phosphor green displays, or retro-futuristic interfaces.
---

# TUI Designer - Retro/Cyberpunk Terminal UI Expert

Expert guidance for designing and implementing text-based user interfaces with authentic retro computing aesthetics: CRT monitors, phosphor glow, scanlines, and cyberpunk neon.

## When to Use This Skill

Use this skill when:
- Creating terminal-style or hacker aesthetic UIs
- Implementing CRT monitor effects (scanlines, glow, barrel distortion)
- Building cyberpunk/synthwave/retrowave interfaces
- Using Tuimorphic components in React
- Implementing Metal shaders for retro effects in SwiftUI
- Designing neon glow text and UI elements
- Choosing color palettes for retro computing aesthetics
- Working with monospace fonts and box-drawing characters

## Design Principles

### The Retro/Cyberpunk Aesthetic

This aesthetic draws from:
- **CRT monitors**: Phosphor glow, scanlines, screen curvature, flicker
- **Terminal interfaces**: Monospace fonts, box-drawing characters, green/amber text
- **Cyberpunk fiction**: Neon colors, dark backgrounds, high contrast
- **1980s computing**: ASCII art, limited color palettes, blocky graphics

### Visual Elements Checklist

- [ ] Dark background (near-black with subtle color tint)
- [ ] Monospace typography throughout
- [ ] Box-drawing characters for borders and frames
- [ ] Neon glow on text and/or borders
- [ ] Scanline effect (subtle horizontal lines)
- [ ] Limited color palette (1-3 accent colors)
- [ ] High contrast between text and background
- [ ] Optional: CRT curvature, chromatic aberration, flicker

## Quick Reference: Color Palettes

### Phosphor Green (Classic Terminal)
| Role | Hex | Usage |
|------|-----|-------|
| Bright | `#00ff00` | Primary text, highlights |
| Medium | `#00cc00` | Secondary text |
| Dark | `#009900` | Dimmed elements |
| Background | `#001100` | Main background |
| Deep BG | `#000800` | Panel backgrounds |

### Cyberpunk Neon
| Role | Hex | Usage |
|------|-----|-------|
| Cyan | `#00ffff` | Primary accent |
| Magenta | `#ff00ff` | Secondary accent |
| Electric Blue | `#0066ff` | Tertiary |
| Hot Pink | `#ff1493` | Warnings |
| Background | `#0a0a1a` | Main background |

### Amber CRT
| Role | Hex | Usage |
|------|-----|-------|
| Bright | `#ffb000` | Primary text |
| Medium | `#cc8800` | Secondary |
| Dark | `#996600` | Dimmed |
| Background | `#1a1000` | Main background |

See [color-palettes.md](references/color-palettes.md) for complete specifications.

## Typography

### Recommended Fonts

**Web:**
```css
font-family: 'GNU Unifont', 'IBM Plex Mono', 'JetBrains Mono',
             'SF Mono', 'Consolas', monospace;
```

**SwiftUI:**
```swift
.font(.system(size: 14, weight: .regular, design: .monospaced))
```

### Box-Drawing Characters

```
Light:   ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼
Heavy:   ━ ┃ ┏ ┓ ┗ ┛ ┣ ┫ ┳ ┻ ╋
Double:  ═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬
Rounded: ╭ ╮ ╰ ╯
```

See [typography-guide.md](references/typography-guide.md) for complete reference.

## Copywriting

Terminal interfaces have a distinct voice: terse, technical, authoritative. Use these defaults unless the project specifies otherwise.

### Core Principles

1. **Terse and Direct** - Every word earns its place
2. **Technical Authority** - The system knows what it's doing
3. **Mechanical Precision** - No hedging, apologies, or filler

### Text Formatting

| Element | Case | Example |
|---------|------|---------|
| Headers/Titles | UPPERCASE | `SYSTEM STATUS` |
| Labels | UPPERCASE | `CPU USAGE:` |
| Status indicators | UPPERCASE | `ONLINE`, `OFFLINE` |
| Commands/Input | lowercase | `> run diagnostic` |
| Body text | Sentence case | `Connection established` |

### Message Prefixes

```
[SYS] System message       [ERR] Error
[USR] User action          [WRN] Warning
[INF] Information          [NET] Network
```

### Vocabulary Quick Reference

| Action | Terminal Verbs |
|--------|---------------|
| Start | INITIALIZE, BOOT, LAUNCH, ACTIVATE |
| Stop | TERMINATE, HALT, ABORT, KILL |
| Save | WRITE, COMMIT, STORE, PERSIST |
| Load | READ, FETCH, RETRIEVE, LOAD |
| Delete | PURGE, REMOVE, CLEAR, WIPE |

| State | Terminal Words |
|-------|---------------|
| Working | PROCESSING, EXECUTING, RUNNING |
| Done | COMPLETE, SUCCESS, FINISHED |
| Failed | ERROR, FAULT, ABORTED |
| Ready | ONLINE, AVAILABLE, ARMED |

### Common Patterns

```
> INITIALIZING SYSTEM...
> LOADING MODULES [████████░░] 80%
> AUTHENTICATION COMPLETE
> SYSTEM READY

ERROR: ACCESS DENIED
ERR_CONNECTION_REFUSED: Timeout after 30s
WARNING: Low disk space (< 10%)

CONFIRM DELETE? [Y/N]
SELECT OPTION [1-5]:
```

### Avoid

- "Please", "Sorry", "Oops"
- "Just", "Maybe", "Might"
- Excessive exclamation points
- Emoji (unless specifically requested)

See [copywriting-guide.md](references/copywriting-guide.md) for complete voice and tone reference.

---

## Platform: React with Tuimorphic

[Tuimorphic](https://github.com/douglance/tuimorphic) is a React component library providing 37 terminal-styled, accessible UI components.

### Quick Start

```bash
npm install tuimorphic
```

```tsx
import { Button, Card, Input } from 'tuimorphic';
import 'tuimorphic/styles.css';

function App() {
  return (
    <div className="theme-dark tint-green">
      <Card>
        <h1>SYSTEM ACCESS</h1>
        <Input placeholder="Enter command..." />
        <Button variant="primary">EXECUTE</Button>
      </Card>
    </div>
  );
}
```

### Theme Configuration

Apply themes via CSS classes on a parent element:

```jsx
// Dark mode with green tint
<div className="theme-dark tint-green">

// Light mode with cyan tint
<div className="theme-light tint-blue">
```

**Available tints:** `tint-green`, `tint-blue`, `tint-red`, `tint-yellow`, `tint-purple`, `tint-orange`, `tint-pink`

### Key Components

| Component | Usage |
|-----------|-------|
| `Button` | Actions with `variant="primary\|secondary\|ghost"` |
| `Input` | Text input with terminal styling |
| `Card` | Container with box-drawing borders |
| `Dialog` | Modal dialogs |
| `Menu` | Dropdown menus |
| `CodeBlock` | Syntax-highlighted code |
| `Table` | Data tables |
| `Tabs` | Tabbed navigation |
| `TreeView` | File tree display |

See [tuimorphic-reference.md](references/tuimorphic-reference.md) for complete API.

### Adding Neon Glow

Enhance Tuimorphic with CSS glow effects:

```css
/* Neon text glow */
.neon-text {
  color: #0ff;
  text-shadow:
    0 0 5px #fff,
    0 0 10px #fff,
    0 0 20px #0ff,
    0 0 40px #0ff,
    0 0 80px #0ff;
}

/* Neon border glow */
.neon-border {
  border-color: #0ff;
  box-shadow:
    0 0 5px #0ff,
    0 0 10px #0ff,
    inset 0 0 5px #0ff;
}

/* Flickering animation */
@keyframes flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.95; }
  52% { opacity: 1; }
  54% { opacity: 0.9; }
}

.flicker {
  animation: flicker 3s infinite;
}
```

---

## Platform: SwiftUI with Metal Shaders

iOS 17+ supports Metal shaders directly in SwiftUI via `.colorEffect()`, `.distortionEffect()`, and `.layerEffect()`.

### CRT Effect Implementation

**CRT.metal:**
```metal
#include <metal_stdlib>
#include <SwiftUI/SwiftUI.h>
using namespace metal;

[[stitchable]] half4 crtEffect(
    float2 position,
    SwiftUI::Layer layer,
    float time,
    float2 size,
    float scanlineIntensity,
    float distortionStrength
) {
    float2 uv = position / size;

    // Barrel distortion
    float2 center = uv - 0.5;
    float dist = length(center);
    float2 distorted = center * (1.0 + distortionStrength * dist * dist);
    float2 samplePos = (distorted + 0.5) * size;

    // Bounds check
    if (samplePos.x < 0 || samplePos.x > size.x ||
        samplePos.y < 0 || samplePos.y > size.y) {
        return half4(0, 0, 0, 1);
    }

    // Sample color
    half4 color = layer.sample(samplePos);

    // Scanlines
    float scanline = sin(position.y * 3.14159 * 2.0) * scanlineIntensity;
    color.rgb *= 1.0 - scanline;

    // Subtle color shift (chromatic aberration)
    color.r *= 1.0 + 0.02 * sin(time * 2.0);
    color.b *= 1.0 - 0.02 * sin(time * 2.0);

    // Slight flicker
    color.rgb *= 1.0 + 0.01 * sin(time * 60.0);

    return color;
}
```

**SwiftUI View Modifier:**
```swift
struct CRTEffectModifier: ViewModifier {
    @State private var startTime = Date()
    var scanlineIntensity: Float = 0.1
    var distortionStrength: Float = 0.1

    func body(content: Content) -> some View {
        TimelineView(.animation) { timeline in
            let time = Float(timeline.date.timeIntervalSince(startTime))
            GeometryReader { geo in
                content
                    .layerEffect(
                        ShaderLibrary.crtEffect(
                            .float(time),
                            .float2(geo.size),
                            .float(scanlineIntensity),
                            .float(distortionStrength)
                        ),
                        maxSampleOffset: .init(width: 10, height: 10)
                    )
            }
        }
    }
}

extension View {
    func crtEffect(
        scanlines: Float = 0.1,
        distortion: Float = 0.1
    ) -> some View {
        modifier(CRTEffectModifier(
            scanlineIntensity: scanlines,
            distortionStrength: distortion
        ))
    }
}
```

**Usage:**
```swift
Text("SYSTEM ONLINE")
    .font(.system(size: 24, weight: .bold, design: .monospaced))
    .foregroundColor(.green)
    .crtEffect(scanlines: 0.15, distortion: 0.08)
```

### Neon Glow in SwiftUI

```swift
extension View {
    func neonGlow(color: Color, radius: CGFloat = 10) -> some View {
        self
            .shadow(color: color.opacity(0.8), radius: radius / 4)
            .shadow(color: color.opacity(0.6), radius: radius / 2)
            .shadow(color: color.opacity(0.4), radius: radius)
            .shadow(color: color.opacity(0.2), radius: radius * 2)
    }
}

// Usage
Text("NEON")
    .font(.system(size: 48, design: .monospaced))
    .foregroundColor(.cyan)
    .neonGlow(color: .cyan, radius: 15)
```

See [metal-shaders-ios.md](references/metal-shaders-ios.md) for complete shader code.

---

## Platform: CSS/Vanilla Web

### Scanlines Overlay

```css
.crt-container {
    position: relative;
    background: #000800;
}

.crt-container::after {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        rgba(0, 0, 0, 0.15),
        rgba(0, 0, 0, 0.15) 1px,
        transparent 1px,
        transparent 2px
    );
    pointer-events: none;
}
```

### Neon Text Effect

```css
.neon-text {
    color: #0ff;
    text-shadow:
        /* White core */
        0 0 5px #fff,
        0 0 10px #fff,
        /* Colored glow layers */
        0 0 20px #0ff,
        0 0 30px #0ff,
        0 0 40px #0ff,
        0 0 55px #0ff,
        0 0 75px #0ff;
}
```

### CRT Curvature (CSS Transform)

```css
.crt-screen {
    border-radius: 20px;
    transform: perspective(1000px) rotateX(2deg);
    box-shadow:
        inset 0 0 50px rgba(0, 255, 0, 0.1),
        0 0 20px rgba(0, 255, 0, 0.2);
}
```

### WebGL CRT with CRTFilter.js

```html
<script type="module">
import { CRTFilterWebGL } from 'crtfilter';

const canvas = document.getElementById('crt-canvas');
const crt = new CRTFilterWebGL(canvas, {
    scanlineIntensity: 0.15,
    glowBloom: 0.3,
    chromaticAberration: 0.002,
    barrelDistortion: 0.1,
    staticNoise: 0.03,
    flicker: true,
    retraceLines: true
});

crt.start();
</script>
```

See [crt-effects-web.md](references/crt-effects-web.md) for complete techniques.

---

## Effect Patterns

### Scanlines

| Platform | Implementation |
|----------|---------------|
| CSS | `repeating-linear-gradient` pseudo-element |
| SwiftUI | Metal shader with `sin(position.y * frequency)` |
| WebGL | Fragment shader brightness modulation |

### Bloom/Glow

| Platform | Implementation |
|----------|---------------|
| CSS | Multiple `text-shadow` with increasing blur |
| SwiftUI | Multiple `.shadow()` modifiers |
| WebGL | Gaussian blur pass + additive blend |
| Three.js | `UnrealBloomPass` with `luminanceThreshold` |

### Chromatic Aberration

| Platform | Implementation |
|----------|---------------|
| CSS | Three overlapping elements with color channel offset |
| SwiftUI | Sample texture at offset positions per RGB channel |
| WebGL | Sample UV with slight offset per channel |

### Flicker

| Platform | Implementation |
|----------|---------------|
| CSS | `@keyframes` animation varying opacity 0.9-1.0 |
| SwiftUI | Timer-driven opacity or shader time-based |
| WebGL | Time-based noise multiplier |

---

## Performance Considerations

### CSS Effects
- `box-shadow` and `text-shadow` are GPU-accelerated but expensive with many layers
- Limit to 4-5 shadow layers for glow effects
- Use `will-change: transform` for animated elements
- Consider `prefers-reduced-motion` media query

### SwiftUI/Metal
- Metal shaders run at 60-120fps on all devices supporting iOS 17+
- `.layerEffect()` processes every pixel - keep shaders simple
- Pre-compile shaders with `.compile()` (iOS 18+)
- Test on older devices (A12 minimum for iOS 17)

### WebGL
- CRTFilter.js uses hardware acceleration, minimal performance impact
- Bloom effects in Three.js require render-to-texture passes
- Consider lower resolution render targets for mobile

### General
- Reduce effect intensity on mobile devices
- Provide option to disable effects for accessibility
- Profile with actual content, not just empty screens

---

## Templates

Ready-to-use starter files:

- [react-tuimorphic-starter.tsx](templates/react-tuimorphic-starter.tsx) - React app with Tuimorphic
- [swiftui-crt-view.swift](templates/swiftui-crt-view.swift) - SwiftUI view with CRT effect
- [crt-shader.metal](templates/crt-shader.metal) - Complete Metal shader
- [neon-glow.css](templates/neon-glow.css) - CSS neon effects

---

## Resources

### Libraries
- [Tuimorphic](https://github.com/douglance/tuimorphic) - React terminal UI components
- [Inferno](https://github.com/twostraws/Inferno) - Metal shaders for SwiftUI
- [CRTFilter.js](https://github.com/nicholashamilton/crtfilter) - WebGL CRT effects
- [@react-three/postprocessing](https://github.com/pmndrs/react-postprocessing) - React Three.js effects

### Documentation
- [SwiftUI Metal Shaders](https://developer.apple.com/documentation/swiftui/view/layereffect(_:maxsampleoffset:isenabled:))
- [CSS text-shadow](https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow)

### Inspiration
- [SRCL / Sacred Computer](https://srcl.org/) - Design influence for Tuimorphic
- [Cool Retro Term](https://github.com/Swordfish90/cool-retro-term) - Terminal emulator with CRT effects
