---
name: frontend-rive
description: State-driven interactive animations with built-in state machines. Use when animations must REACT to user input (hover, click, drag), have multiple states/transitions, or respond to data values (progress bars, counters). Ideal for animated buttons, toggles, checkboxes, characters. For simple play/loop animations use Lottie instead.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Rive

Interactive animations with built-in state machines. Animation logic inside the .riv file.

## When to Use

- Animations that REACT to input (hover, click, data)
- Animated buttons, toggles, checkboxes
- Progress indicators driven by values
- Multi-state characters/icons
- Complex state transitions

## When NOT to Use

- Simple decorative loops → Lottie
- Static illustrations → SVG
- Quick spinners → CSS/Lottie

## Key Concept: State Machines

```
┌─────────────────────────────────┐
│         Rive State Machine      │
│   ┌──────┐  hover  ┌───────┐    │
│   │ Idle │ ──────► │ Hover │    │
│   └──────┘         └───────┘    │
│       ▲    click       │        │
│       └──────────── ◄──┘        │
│                                 │
│   Inputs: hover (bool), click   │
└─────────────────────────────────┘
You control inputs → Rive handles animations
```

## Process

**SETUP → CONNECT → CONTROL**

1. Install: `npm install @rive-app/react-canvas`
2. Load .riv file with state machine
3. Get inputs via `useStateMachineInput`
4. Connect to UI events

## Quick Start

```tsx
import { useRive, useStateMachineInput } from '@rive-app/react-canvas';

function InteractiveButton() {
  const { rive, RiveComponent } = useRive({
    src: '/button.riv',
    stateMachines: 'ButtonState',
    autoplay: true,
  });

  const hover = useStateMachineInput(rive, 'ButtonState', 'hover');
  const press = useStateMachineInput(rive, 'ButtonState', 'pressed');

  return (
    <RiveComponent
      onMouseEnter={() => hover && (hover.value = true)}
      onMouseLeave={() => hover && (hover.value = false)}
      onMouseDown={() => press && (press.value = true)}
      onMouseUp={() => press && (press.value = false)}
    />
  );
}
```

## Input Types

```yaml
Boolean:  input.value = true/false     # hover, isActive
Number:   input.value = 75             # progress (0-100)
Trigger:  input.fire()                 # onClick, onComplete
```

## Common Patterns

```yaml
Toggle:
  - Boolean input "isOn"
  - onClick: toggle value

Progress:
  - Number input "progress" (0-100)
  - useEffect: sync with prop

Notification Bell:
  - Number input "count"
  - Trigger input "ring"
  - onClick: fire() trigger
```

## Decision: Rive vs Lottie

| Need | Use |
|------|-----|
| Just plays/loops | Lottie |
| Reacts to hover | Rive |
| Controlled by data | Rive |
| Multiple states | Rive |
| Simple loader | Lottie |

## Layout & Sizing

```tsx
// Container controls size
<div className="w-64 h-64">
  <RiveComponent />
</div>

// Responsive with aspect ratio
<div className="w-full aspect-video max-w-2xl">
  <RiveComponent />
</div>
```

## SSR & Hydration

```tsx
// Always 'use client'
'use client'

// Dynamic import for heavy animations
const Animation = dynamic(() => import('./RiveAnimation'), { ssr: false })

// Or mounted check
const [mounted, setMounted] = useState(false)
useEffect(() => setMounted(true), [])
if (!mounted) return <Skeleton />
```

## Performance

```tsx
// Lazy load
const Rive = dynamic(() => import('./RiveComponent'), { ssr: false })

// Pause when not visible
const { ref, inView } = useInView()
useEffect(() => { inView ? rive?.play() : rive?.pause() }, [inView])
```

## Troubleshooting

```yaml
"Animation not playing":
  → Check autoplay: true
  → Check stateMachines name (case-sensitive)
  → Check .riv path in public/

"Inputs undefined":
  → Always check: if (input) input.value = x
  → Verify input names match Rive editor

"Hydration mismatch":
  → Add 'use client'
  → Use dynamic(() => ..., { ssr: false })

"Wrong size":
  → Container needs explicit width/height
  → Use aspect-ratio utilities
```

## References

- **[patterns.md](references/patterns.md)** — Toggle, Checkbox, Progress, Like button, Form integration

## External Resources

- https://rive.app/docs/runtimes/react — React runtime docs
- https://rive.app/community — Free .riv files
- For latest API → use context7 skill
