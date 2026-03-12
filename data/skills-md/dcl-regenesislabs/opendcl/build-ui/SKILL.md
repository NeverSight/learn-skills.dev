---
name: build-ui
description: Build 2D user interfaces for Decentraland scenes using React-ECS. Create HUDs, menus, health bars, scoreboards, dialogs, buttons, and input forms. Use when user wants to add UI, HUD, buttons, text overlays, menus, or on-screen elements.
---

# Building UI with React-ECS

Decentraland SDK7 uses a React-like JSX system for 2D UI overlays.

## Setup

### File: src/ui.tsx
```tsx
import ReactEcs, { ReactEcsRenderer, UiEntity, Label, Button } from '@dcl/sdk/react-ecs'

const MyUI = () => (
  <UiEntity
    uiTransform={{
      width: '100%',
      height: '100%',
      justifyContent: 'center',
      alignItems: 'center'
    }}
  >
    <Label value="Hello Decentraland!" fontSize={24} />
  </UiEntity>
)

export function setupUi() {
  ReactEcsRenderer.setUiRenderer(MyUI)
}
```

### File: src/index.ts
```typescript
import { setupUi } from './ui'

export function main() {
  setupUi()
}
```

### tsconfig.json (already configured by /init)

The SDK template already includes the required JSX settings — do NOT modify tsconfig.json:
- `"jsx": "react-jsx"`
- `"jsxImportSource": "@dcl/sdk/react-ecs-lib"`

## Core Components

### UiEntity (Container)
```tsx
import { Color4 } from '@dcl/sdk/math'

<UiEntity
  uiTransform={{
    width: 300,              // Pixels or '50%'
    height: 200,
    positionType: 'absolute', // 'absolute' or 'relative' (default)
    position: { top: 10, right: 10 }, // Only with absolute
    flexDirection: 'column',  // 'row' | 'column'
    justifyContent: 'center', // 'flex-start' | 'center' | 'flex-end' | 'space-between'
    alignItems: 'center',     // 'flex-start' | 'center' | 'flex-end' | 'stretch'
    padding: { top: 10, bottom: 10, left: 10, right: 10 },
    margin: { top: 5 },
    display: 'flex'           // 'flex' | 'none' (hide)
  }}
  uiBackground={{
    color: Color4.create(0, 0, 0, 0.8) // Semi-transparent black
  }}
/>
```

### Label (Text)
```tsx
import { Color4 } from '@dcl/sdk/math'

<Label
  value="Score: 100"
  fontSize={18}
  color={Color4.White()}
  textAlign="middle-center"
  font="sans-serif"
  uiTransform={{ width: 200, height: 30 }}
/>
```

### Button
```tsx
<Button
  value="Click Me"
  variant="primary"  // 'primary' | 'secondary'
  fontSize={16}
  uiTransform={{ width: 150, height: 40 }}
  onMouseDown={() => {
    console.log('Button clicked!')
  }}
/>
```

### Input
```tsx
import { Input } from '@dcl/sdk/react-ecs'
import { Color4 } from '@dcl/sdk/math'

<Input
  placeholder="Type here..."
  fontSize={14}
  color={Color4.White()}
  uiTransform={{ width: 250, height: 35 }}
  onChange={(value) => {
    console.log('Value changing:', value)
  }}
  onSubmit={(value) => {
    console.log('Submitted:', value)
  }}
/>
```

### Dropdown
```tsx
import { Dropdown } from '@dcl/sdk/react-ecs'

<Dropdown
  options={['Option A', 'Option B', 'Option C']}
  selectedIndex={0}
  onChange={(index) => {
    console.log('Selected:', index)
  }}
  uiTransform={{ width: 200, height: 35 }}
  fontSize={14}
/>
```

## State Management

Use module-level variables for UI state (React hooks are NOT available):

```tsx
import { Color4 } from '@dcl/sdk/math'

let score = 0
let showMenu = false

const GameUI = () => (
  <UiEntity uiTransform={{ width: '100%', height: '100%' }}>
    {/* HUD - always visible */}
    <Label
      value={`Score: ${score}`}
      fontSize={20}
      uiTransform={{
        positionType: 'absolute',
        position: { top: 10, left: 10 }
      }}
    />

    {/* Menu - conditionally shown */}
    {showMenu && (
      <UiEntity
        uiTransform={{
          width: 300,
          height: 400,
          positionType: 'absolute',
          position: { top: '50%', left: '50%' }
        }}
        uiBackground={{ color: Color4.create(0.1, 0.1, 0.1, 0.9) }}
      >
        <Label value="Game Menu" fontSize={24} />
        <Button
          value="Resume"
          variant="primary"
          onMouseDown={() => { showMenu = false }}
          uiTransform={{ width: 200, height: 40 }}
        />
      </UiEntity>
    )}
  </UiEntity>
)

// Update state from game logic
export function addScore(points: number) {
  score += points
}

export function toggleMenu() {
  showMenu = !showMenu
}
```

## Common UI Patterns

### Health Bar
```tsx
import { Color4 } from '@dcl/sdk/math'

let health = 100

const HealthBar = () => (
  <UiEntity
    uiTransform={{
      width: 200, height: 20,
      positionType: 'absolute',
      position: { bottom: 20, left: '50%' }
    }}
    uiBackground={{ color: Color4.create(0.3, 0.3, 0.3, 0.8) }}
  >
    <UiEntity
      uiTransform={{ width: `${health}%`, height: '100%' }}
      uiBackground={{ color: Color4.create(0.2, 0.8, 0.2, 1) }}
    />
  </UiEntity>
)
```

### Image Background
```tsx
<UiEntity
  uiTransform={{ width: 200, height: 200 }}
  uiBackground={{
    textureMode: 'stretch',
    texture: { src: 'images/logo.png' }
  }}
/>
```

### Screen Dimensions

Read screen size via `UiCanvasInformation`:

```typescript
import { UiCanvasInformation } from '@dcl/sdk/ecs'

engine.addSystem(() => {
  const canvas = UiCanvasInformation.getOrNull(engine.RootEntity)
  if (canvas) {
    console.log('Screen:', canvas.width, 'x', canvas.height)
  }
})
```

### Nine-Slice Textures

Use `textureSlices` for scalable UI backgrounds (buttons, panels) that don't stretch corners:

```tsx
<UiEntity
  uiTransform={{ width: 200, height: 100 }}
  uiBackground={{
    textureMode: 'nine-slices',
    texture: { src: 'images/panel.png' },
    textureSlices: { top: 0.1, bottom: 0.1, left: 0.1, right: 0.1 }
  }}
/>
```

### Hover Events

Respond to mouse enter/leave for hover effects:

```tsx
<UiEntity
  uiTransform={{ width: 100, height: 40 }}
  onMouseEnter={() => { isHovered = true }}
  onMouseLeave={() => { isHovered = false }}
  uiBackground={{ color: isHovered ? Color4.White() : Color4.Gray() }}
/>
```

### Flex Wrap

Allow UI children to wrap to the next line:

```tsx
<UiEntity uiTransform={{ flexWrap: 'wrap', width: 300 }}>
  {items.map(item => (
    <UiEntity key={item.id} uiTransform={{ width: 80, height: 80, margin: 4 }} />
  ))}
</UiEntity>
```

### Dropdown Extras

The `Dropdown` component supports additional props:

```tsx
<Dropdown
  options={['Option A', 'Option B', 'Option C']}
  selectedIndex={selectedIdx}
  onChange={(idx) => { selectedIdx = idx }}
  fontSize={14}
  color={Color4.White()}
  disabled={false}
/>
```

## Important Notes

- React hooks (`useState`, `useEffect`, etc.) are **NOT** available — use module-level variables
- The UI renderer re-renders every frame, so state changes are reflected immediately
- UI is rendered as a 2D overlay on top of the 3D scene
- Use `display: 'none'` in `uiTransform` to hide elements without removing them
- File extension must be `.tsx` for JSX support
- Only one `ReactEcsRenderer.setUiRenderer()` call per scene — combine all UI into one root component
