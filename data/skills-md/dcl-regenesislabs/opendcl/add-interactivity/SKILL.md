---
name: add-interactivity
description: Add click handlers, hover effects, pointer events, triggers, and raycasting to Decentraland scene entities. Use when user wants to make objects clickable, add interactions, detect player proximity, or handle user input.
---

# Adding Interactivity to Decentraland Scenes

## Pointer Events (Click / Hover)

### Using the Helper System (Recommended)
```typescript
import { engine, Transform, MeshRenderer, pointerEventsSystem, InputAction } from '@dcl/sdk/ecs'
import { Vector3 } from '@dcl/sdk/math'

const cube = engine.addEntity()
Transform.create(cube, { position: Vector3.create(8, 1, 8) })
MeshRenderer.setBox(cube)

// Add click handler
pointerEventsSystem.onPointerDown(
  {
    entity: cube,
    opts: {
      button: InputAction.IA_POINTER,    // Left click
      hoverText: 'Click me!',
      maxDistance: 10
    }
  },
  (event) => {
    console.log('Cube clicked!', event.hit?.position)
  }
)
```

### Available Input Actions
```typescript
InputAction.IA_POINTER   // Left click / primary
InputAction.IA_PRIMARY   // E key
InputAction.IA_SECONDARY // F key
InputAction.IA_ACTION_3  // Key 1
InputAction.IA_ACTION_4  // Key 2
InputAction.IA_ACTION_5  // Key 3
InputAction.IA_ACTION_6  // Key 4
```

### Pointer Up (Release)
```typescript
pointerEventsSystem.onPointerDown(
  { entity: cube, opts: { button: InputAction.IA_POINTER, hoverText: 'Hold me' } },
  () => { console.log('Pressed!') }
)

pointerEventsSystem.onPointerUp(
  { entity: cube, opts: { button: InputAction.IA_POINTER } },
  () => { console.log('Released!') }
)
```

### Removing Handlers
```typescript
pointerEventsSystem.removeOnPointerDown(cube)
pointerEventsSystem.removeOnPointerUp(cube)
```

### Important: Colliders Required
Pointer events only work on entities with a **collider**. Add one if your entity doesn't have a mesh:
```typescript
import { MeshCollider } from '@dcl/sdk/ecs'
MeshCollider.setBox(entity) // Invisible box collider
```

For GLTF models, set the collision mask:
```typescript
GltfContainer.create(entity, {
  src: 'models/button.glb',
  visibleMeshesCollisionMask: ColliderLayer.CL_POINTER
})
```

## Trigger Areas (Proximity Detection)

Detect when the player enters, exits, or stays inside an area:

```typescript
import { engine, Transform, TriggerArea } from '@dcl/sdk/ecs'
import { triggerAreaEventsSystem } from '@dcl/sdk/ecs'
import { Vector3 } from '@dcl/sdk/math'

const area = engine.addEntity()
TriggerArea.setBox(area) // or TriggerArea.setSphere(area)
Transform.create(area, {
  position: Vector3.create(8, 0, 8),
  scale: Vector3.create(4, 4, 4) // Size the area via Transform.scale
})

// Register enter/exit/stay events
triggerAreaEventsSystem.onTriggerEnter(area, (event) => {
  console.log('Entity entered trigger:', event.trigger.entity)
})

triggerAreaEventsSystem.onTriggerExit(area, () => {
  console.log('Entity exited trigger')
})

triggerAreaEventsSystem.onTriggerStay(area, () => {
  // Called every frame while an entity is inside
})
```

By default, trigger areas react to the player layer. Use `ColliderLayer` to restrict which entities activate the area:

```typescript
import { ColliderLayer, MeshCollider } from '@dcl/sdk/ecs'

// Area that only reacts to custom layers
TriggerArea.setBox(area, ColliderLayer.CL_CUSTOM1 | ColliderLayer.CL_CUSTOM2)

// Mark a moving entity to activate the area
const mover = engine.addEntity()
Transform.create(mover, { position: Vector3.create(8, 0, 8) })
MeshCollider.setBox(mover, ColliderLayer.CL_CUSTOM1)
```

## Raycasting

Cast rays to detect objects in a direction:

```typescript
import { engine, Raycast, RaycastResult, RaycastQueryType } from '@dcl/sdk/ecs'
import { Vector3 } from '@dcl/sdk/math'

const rayEntity = engine.addEntity()
Raycast.create(rayEntity, {
  direction: { $case: 'localDirection', localDirection: Vector3.Forward() },
  maxDistance: 16,
  queryType: RaycastQueryType.RQT_HIT_FIRST,
  continuous: false // Set true for continuous raycasting
})

// Check results
engine.addSystem(() => {
  const result = RaycastResult.getOrNull(rayEntity)
  if (result && result.hits.length > 0) {
    const hit = result.hits[0]
    console.log('Hit entity:', hit.entityId, 'at', hit.position)
  }
})
```

## Global Input Handling

Listen for key presses anywhere (not entity-specific):

```typescript
import { inputSystem, InputAction, PointerEventType } from '@dcl/sdk/ecs'

engine.addSystem(() => {
  // Check if E key was just pressed this frame
  if (inputSystem.isTriggered(InputAction.IA_PRIMARY, PointerEventType.PET_DOWN)) {
    console.log('E key pressed!')
  }

  // Check if a key is currently held down
  if (inputSystem.isPressed(InputAction.IA_SECONDARY)) {
    console.log('F key is held!')
  }
})
```

## Toggle Pattern (Click to Switch States)

Common pattern for toggleable objects:

```typescript
let doorOpen = false

pointerEventsSystem.onPointerDown(
  { entity: door, opts: { button: InputAction.IA_POINTER, hoverText: 'Toggle door' } },
  () => {
    doorOpen = !doorOpen
    const mutableTransform = Transform.getMutable(door)
    mutableTransform.rotation = doorOpen
      ? Quaternion.fromEulerDegrees(0, 90, 0)
      : Quaternion.fromEulerDegrees(0, 0, 0)
  }
)
```

### Raycast System Helpers

Use `raycastSystem` for convenient raycasting without manual component management:

```typescript
import { raycastSystem, RaycastQueryType, ColliderLayer } from '@dcl/sdk/ecs'

// Register a continuous local-direction raycast
raycastSystem.registerLocalDirectionRaycast(
  { entity: myEntity, opts: { queryType: RaycastQueryType.RQT_HIT_FIRST, direction: Vector3.Forward(), maxDistance: 16, collisionMask: ColliderLayer.CL_POINTER } },
  (result) => {
    if (result.hits.length > 0) {
      console.log('Hit:', result.hits[0].entityId)
    }
  }
)

// Register a global-direction raycast
raycastSystem.registerGlobalDirectionRaycast(
  { entity: myEntity, opts: { queryType: RaycastQueryType.RQT_HIT_FIRST, direction: Vector3.Down(), maxDistance: 20 } },
  (result) => { /* handle hits */ }
)

// Remove raycast from entity
raycastSystem.removeRaycasterEntity(myEntity)
```

## Best Practices

- Always set `maxDistance` on pointer events (8-16m is typical)
- Always set `hoverText` so users know they can interact
- Clean up handlers when entities are removed
- Use `MeshCollider` for invisible trigger surfaces
- For complex interactions, use a system with state tracking
- Test interactions in preview — hover text should be visible and clear
