---
name: advanced-input
description: Advanced input handling in Decentraland scenes. Use PointerLock to detect cursor capture state, InputModifier to freeze or restrict player movement, PrimaryPointerInfo for cursor position and world ray, inputSystem.getInputCommand for per-entity input polling, and keyboard patterns for WASD movement controls. Use when user wants custom input, cursor control, movement restriction, keyboard handling, FPS controls, or input polling.
---

# Advanced Input Handling in Decentraland

For basic click/hover events, see the `add-interactivity` skill. This skill covers advanced input patterns.

## Pointer Lock State

Detect whether the cursor is captured (first-person mode) or free:

```typescript
import { engine, PointerLock } from '@dcl/sdk/ecs'

function checkPointerLock() {
  const isLocked = PointerLock.get(engine.CameraEntity).isPointerLocked

  if (isLocked) {
    // Cursor is captured — player is in first-person control
  } else {
    // Cursor is free — player can click UI elements
  }
}

engine.addSystem(checkPointerLock)
```

### Pointer Lock Change Detection

```typescript
PointerLock.onChange(engine.CameraEntity, (pointerLock) => {
  if (pointerLock?.isPointerLocked) {
    console.log('Cursor locked')
  } else {
    console.log('Cursor unlocked')
  }
})
```

## Cursor Position and World Ray

Get the cursor's screen position and the ray it casts into the 3D world:

```typescript
import { engine, PrimaryPointerInfo } from '@dcl/sdk/ecs'

function readPointer() {
  const pointerInfo = PrimaryPointerInfo.get(engine.RootEntity)
  console.log('Cursor position:', pointerInfo.screenCoordinates)
  console.log('Cursor delta:', pointerInfo.screenDelta)
  console.log('World ray direction:', pointerInfo.worldRayDirection)
}

engine.addSystem(readPointer)
```

## Input Polling with inputSystem

### Per-Entity Input Commands

Check if a specific input action occurred on a specific entity:

```typescript
import { engine, inputSystem, InputAction, PointerEventType } from '@dcl/sdk/ecs'

function myInputSystem() {
  // Check for click on a specific entity
  const clickData = inputSystem.getInputCommand(
    InputAction.IA_POINTER,
    PointerEventType.PET_DOWN,
    myEntity
  )

  if (clickData) {
    console.log('Entity clicked via system:', clickData.hit.entityId)
  }
}

engine.addSystem(myInputSystem)
```

### Global Input Checks

```typescript
function globalInputSystem() {
  // Was the key just pressed this frame?
  if (inputSystem.isTriggered(InputAction.IA_PRIMARY, PointerEventType.PET_DOWN)) {
    console.log('E key pressed!')
  }

  // Is the key currently held down?
  if (inputSystem.isPressed(InputAction.IA_SECONDARY)) {
    console.log('F key is held!')
  }
}

engine.addSystem(globalInputSystem)
```

## All InputAction Values

| InputAction | Key/Button |
|-------------|-----------|
| `IA_POINTER` | Left mouse button |
| `IA_PRIMARY` | E key |
| `IA_SECONDARY` | F key |
| `IA_ACTION_3` | 1 key |
| `IA_ACTION_4` | 2 key |
| `IA_ACTION_5` | 3 key |
| `IA_ACTION_6` | 4 key |
| `IA_JUMP` | Space key |
| `IA_FORWARD` | W key |
| `IA_BACKWARD` | S key |
| `IA_LEFT` | A key |
| `IA_RIGHT` | D key |
| `IA_WALK` | Shift key |

## Event Types

```typescript
PointerEventType.PET_DOWN         // Button/key pressed
PointerEventType.PET_UP           // Button/key released
PointerEventType.PET_HOVER_ENTER  // Cursor enters entity
PointerEventType.PET_HOVER_LEAVE  // Cursor leaves entity
```

## InputModifier (Movement Restriction)

Restrict or freeze the player's movement:

```typescript
import { engine, InputModifier } from '@dcl/sdk/ecs'

// Freeze player completely
InputModifier.create(engine.PlayerEntity, {
  mode: InputModifier.Mode.Standard({ disableAll: true })
})

// Restrict specific movement
InputModifier.createOrReplace(engine.PlayerEntity, {
  mode: InputModifier.Mode.Standard({
    disableRun: true,
    disableJump: true,
    disableEmote: true
  })
})

// Restore normal movement
InputModifier.deleteFrom(engine.PlayerEntity)
```

**Important:** InputModifier only works in the DCL 2.0 desktop client. It has no effect in the web browser explorer.

### Cutscene Pattern

Freeze the player during a cinematic sequence:

```typescript
function startCutscene() {
  // Freeze player
  InputModifier.create(engine.PlayerEntity, {
    mode: InputModifier.Mode.Standard({ disableAll: true })
  })

  // ... play cinematic with VirtualCamera ...

  // After cutscene ends, restore movement
  // InputModifier.deleteFrom(engine.PlayerEntity)
}
```

## WASD Movement Pattern

Poll movement keys to control custom entities:

```typescript
import { engine, inputSystem, InputAction, PointerEventType, Transform } from '@dcl/sdk/ecs'
import { Vector3 } from '@dcl/sdk/math'

const MOVE_SPEED = 5

function customMovementSystem(dt: number) {
  const transform = Transform.getMutable(controllableEntity)
  let moveX = 0
  let moveZ = 0

  if (inputSystem.isPressed(InputAction.IA_FORWARD)) moveZ += 1
  if (inputSystem.isPressed(InputAction.IA_BACKWARD)) moveZ -= 1
  if (inputSystem.isPressed(InputAction.IA_LEFT)) moveX -= 1
  if (inputSystem.isPressed(InputAction.IA_RIGHT)) moveX += 1

  transform.position.x += moveX * MOVE_SPEED * dt
  transform.position.z += moveZ * MOVE_SPEED * dt
}

engine.addSystem(customMovementSystem)
```

## Combining Input Patterns

### Action Bar with Number Keys

```typescript
function actionBarSystem() {
  if (inputSystem.isTriggered(InputAction.IA_ACTION_3, PointerEventType.PET_DOWN)) {
    console.log('Slot 1 activated')
    useAbility(1)
  }
  if (inputSystem.isTriggered(InputAction.IA_ACTION_4, PointerEventType.PET_DOWN)) {
    console.log('Slot 2 activated')
    useAbility(2)
  }
  if (inputSystem.isTriggered(InputAction.IA_ACTION_5, PointerEventType.PET_DOWN)) {
    console.log('Slot 3 activated')
    useAbility(3)
  }
  if (inputSystem.isTriggered(InputAction.IA_ACTION_6, PointerEventType.PET_DOWN)) {
    console.log('Slot 4 activated')
    useAbility(4)
  }
}

engine.addSystem(actionBarSystem)
```

## Best Practices

- Use `isTriggered()` for one-shot actions (fire weapon, open door) — it returns true only on the frame the key is first pressed
- Use `isPressed()` for continuous actions (movement, holding a shield) — it returns true every frame while held
- `getInputCommand()` gives hit data (position, entity) — use it when you need to know what was clicked
- Prefer `pointerEventsSystem.onPointerDown()` for simple entity clicks — use `inputSystem` for complex multi-key or polling patterns
- InputModifier only works in the DCL 2.0 desktop client — test with the desktop client if your scene relies on it
- WASD keys (`IA_FORWARD`, etc.) also control player movement — polling them reads the movement state but doesn't override it

For basic pointer events and click handlers, see the `add-interactivity` skill.
