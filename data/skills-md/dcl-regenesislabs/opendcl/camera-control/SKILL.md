---
name: camera-control
description: Control camera behavior in Decentraland scenes. Switch between first-person and third-person with CameraMode, force camera in regions with CameraModeArea, create cinematic scripted cameras with VirtualCamera, and read camera position/rotation via MainCamera. Use when user wants camera control, cinematic views, cutscenes, or camera mode switching.
---

# Camera Control in Decentraland

## Reading Camera State

Access the camera's current position and rotation via the reserved `engine.CameraEntity`:

```typescript
import { engine, Transform } from '@dcl/sdk/ecs'

function trackCamera() {
  if (!Transform.has(engine.CameraEntity)) return

  const cameraTransform = Transform.get(engine.CameraEntity)
  console.log('Camera position:', cameraTransform.position)
  console.log('Camera rotation:', cameraTransform.rotation)
}

engine.addSystem(trackCamera)
```

## Camera Mode Detection

Check whether the player is in first-person or third-person:

```typescript
import { engine, CameraMode, CameraType } from '@dcl/sdk/ecs'

function checkCameraMode() {
  if (!CameraMode.has(engine.CameraEntity)) return

  const cameraMode = CameraMode.get(engine.CameraEntity)
  if (cameraMode.mode === CameraType.CT_FIRST_PERSON) {
    console.log('First person camera')
  } else if (cameraMode.mode === CameraType.CT_THIRD_PERSON) {
    console.log('Third person camera')
  }
}

engine.addSystem(checkCameraMode)
```

### Camera Mode Values

```typescript
CameraType.CT_FIRST_PERSON  // First-person view
CameraType.CT_THIRD_PERSON  // Third-person view (default)
```

## CameraModeArea (Force Camera in a Region)

Force a specific camera mode when the player enters an area:

```typescript
import { engine, Transform, CameraModeArea, CameraType } from '@dcl/sdk/ecs'
import { Vector3 } from '@dcl/sdk/math'

const fpArea = engine.addEntity()
Transform.create(fpArea, { position: Vector3.create(8, 1.5, 8) })

CameraModeArea.create(fpArea, {
  area: Vector3.create(6, 4, 6),         // 6x4x6 meter box
  mode: CameraType.CT_FIRST_PERSON       // Force first-person inside
})
```

When the player leaves the area, the camera reverts to their preferred mode.

## VirtualCamera (Cinematic Cameras)

Create scripted camera positions for cutscenes or special views:

```typescript
import { engine, Transform, VirtualCamera, MainCamera } from '@dcl/sdk/ecs'
import { Vector3, Quaternion } from '@dcl/sdk/math'

const cinematicCam = engine.addEntity()
Transform.create(cinematicCam, {
  position: Vector3.create(8, 5, 2),
  rotation: Quaternion.fromEulerDegrees(-20, 0, 0)
})

VirtualCamera.create(cinematicCam, {
  defaultTransition: {
    transitionMode: VirtualCamera.Transition.Speed(1.0)
  }
})

// Activate the virtual camera
MainCamera.getMutable(engine.CameraEntity).virtualCameraEntity = cinematicCam

// Return to normal camera
MainCamera.getMutable(engine.CameraEntity).virtualCameraEntity = undefined
```

### Transition Modes

```typescript
VirtualCamera.Transition.Speed(1.0)  // Speed-based smooth transition
VirtualCamera.Transition.Time(2)     // Time-based transition (2 seconds)
```

### Look-At Target

Make the virtual camera track an entity:

```typescript
const target = engine.addEntity()
Transform.create(target, { position: Vector3.create(8, 1, 8) })

VirtualCamera.create(cinematicCam, {
  lookAtEntity: target,
  defaultTransition: {
    transitionMode: VirtualCamera.Transition.Speed(2.0)
  }
})

// Activate
MainCamera.getMutable(engine.CameraEntity).virtualCameraEntity = cinematicCam
```

## Tracking Camera Position

Poll camera position each frame for camera-triggered events:

```typescript
import { engine, Transform } from '@dcl/sdk/ecs'
import { Vector3 } from '@dcl/sdk/math'

let lastNotifiedZone = ''

function cameraZoneSystem() {
  if (!Transform.has(engine.CameraEntity)) return

  const camPos = Transform.get(engine.CameraEntity).position
  let currentZone = ''

  if (camPos.y > 10) {
    currentZone = 'sky'
  } else if (camPos.x < 4) {
    currentZone = 'west'
  } else {
    currentZone = 'center'
  }

  if (currentZone !== lastNotifiedZone) {
    lastNotifiedZone = currentZone
    console.log('Camera entered zone:', currentZone)
  }
}

engine.addSystem(cameraZoneSystem)
```

## Common Patterns

### Camera-Triggered Events

Use the camera position to trigger actions when the player looks at a specific area:

```typescript
function cameraLookTrigger() {
  const camTransform = Transform.get(engine.CameraEntity)
  const targetPos = Vector3.create(8, 2, 8)
  const distance = Vector3.distance(camTransform.position, targetPos)

  if (distance < 5) {
    // Player is close — check if camera is pointing at target
    // Use raycasting for precise look detection (see add-interactivity skill)
  }
}

engine.addSystem(cameraLookTrigger)
```

### Following an NPC

Move camera to track an NPC by updating a VirtualCamera's Transform:

```typescript
function followNpcCamera(dt: number) {
  const npcPos = Transform.get(npcEntity).position
  const camTransform = Transform.getMutable(cinematicCam)

  // Position camera behind and above the NPC
  camTransform.position = Vector3.create(
    npcPos.x - 2,
    npcPos.y + 3,
    npcPos.z - 2
  )
}

engine.addSystem(followNpcCamera)
```

## Best Practices

- Only one VirtualCamera should be active at a time
- Use `CameraModeArea` to force first-person in tight indoor spaces
- Keep transition speeds between 0.5 and 3.0 for comfortable camera movement
- Always provide a way for the player to exit forced camera modes (e.g., leave the area)
- Read camera state via `engine.CameraEntity` — never try to write to it directly
- For look-at detection, combine camera position with raycasting (see `add-interactivity` skill)
- Camera control is read-only outside of VirtualCamera and CameraModeArea — you cannot directly move the player's camera
