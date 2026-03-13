---
name: lens-studio-world-query
description: Reference guide for world understanding and scoring in Lens Studio — covering WorldQueryModule HitTestSession (HitTestSessionOptions.filter for jitter smoothing, semantic surface classification for floor/wall/ceiling/table detection, null result handling, per-frame performance), SIK InteractionManager targeting interactor ray pattern, Physics.createGlobalProbe().rayCast for scene-collider hits with collision layer filtering, aligning objects to surface normals using quat.lookAt, and the LeaderboardModule (create/retrieve with TTL and OrderingType, submitScore, getLeaderboardInfo with UsersType.Global/Friends). Use this skill when detecting real floors/walls/tables to place AR content, raycasting for hover or interaction against scene objects, or adding a global in-lens leaderboard — differentiates from spectacles-lens-essentials (physics/SIK) and from spectacles-cloud (Supabase persistence).
---

# Lens Studio World Query — Reference Guide

"World query" covers two related capabilities: detecting real-world surfaces (using the device's depth and mesh data) and raycasting against scene geometry (using physics). Most Spectacles lenses need at least one of these.

---

## World Query Module (Real Surfaces)

`WorldQueryModule` lets you cast a ray and find where it hits real-world surfaces recognised by the Spectacles depth sensor.

```typescript
const WorldQueryModule = require('LensStudio:WorldQueryModule')
```

### Creating a hit test session

```typescript
onAwake(): void {
  const options = HitTestSessionOptions.create()
  options.filter = true  // smooth / filter jitter (recommended)

  this.hitTestSession = WorldQueryModule.createHitTestSessionWithOptions(options)
}
```

### Performing a hit test

```typescript
// rayStart and rayEnd are world-space vec3 positions
this.hitTestSession.hitTest(rayStart, rayEnd, (result) => {
  if (result === null) {
    // No surface found along the ray
    indicator.enabled = false
    return
  }

  // result.position — world position of the hit point
  // result.normal  — surface normal at the hit point
  const hitPos = result.position
  const hitNormal = result.normal

  indicator.getTransform().setWorldPosition(hitPos)
  indicator.getTransform().setWorldRotation(
    quat.lookAt(hitNormal.cross(vec3.up()), hitNormal)
  )
  indicator.enabled = true
})
```

### Typical hit test using SIK targeting interactor (Spectacles)

```typescript
import { InteractorInputType } from 'SpectaclesInteractionKit.lspkg/Core/Interactor/Interactor'
import { SIK } from 'SpectaclesInteractionKit.lspkg/SIK'

this.createEvent('UpdateEvent').bind(() => {
  // Get the currently active targeting interactor (the hand pointing at something)
  const primaryInteractor = SIK.InteractionManager
    .getTargetingInteractors()
    .shift()

  if (primaryInteractor && primaryInteractor.isActive() && primaryInteractor.isTargeting()) {
    const rayStart = primaryInteractor.startPoint
    const rayEnd   = primaryInteractor.endPoint

    this.hitTestSession.hitTest(rayStart, rayEnd, (result) => {
      if (result) this.placeObject(result.position, result.normal)
    })
  }
})
```

### Typical hit test in UpdateEvent (camera gaze, phone or Spectacles)

```typescript
this.createEvent('UpdateEvent').bind(() => {
  const origin = cameraTransform.getWorldPosition()
  const forward = cameraTransform.forward
  const rayEnd = origin.add(forward.uniformScale(5)) // 5-metre ray

  this.hitTestSession.hitTest(origin, rayEnd, (result) => {
    if (result) this.placeObject(result.position, result.normal)
  })
})
```

---

## Semantic Hit Testing (Spectacles only)

Semantic hit testing classifies the surface type at the hit point — useful for only placing content on floors, tables, or walls.

```typescript
onAwake(): void {
  const options = HitTestSessionOptions.create()
  options.filter = true
  options.surfaceClassification = true  // enable surface type detection

  this.hitTestSession = WorldQueryModule.createHitTestSessionWithOptions(options)
}

// In the hit callback:
this.hitTestSession.hitTest(rayStart, rayEnd, (result) => {
  if (!result) return

  // result.classification — the detected surface type
  switch (result.classification) {
    case HitTestSessionOptions.SurfaceClassification.Floor:
      print('Hit floor — safe to place furniture')
      break
    case HitTestSessionOptions.SurfaceClassification.Wall:
      print('Hit wall — mount picture here')
      break
    case HitTestSessionOptions.SurfaceClassification.Ceiling:
      print('Hit ceiling')
      break
    case HitTestSessionOptions.SurfaceClassification.Table:
      print('Hit table — place small object')
      break
    default:
      print('Hit unclassified surface')
  }
})
```

> **Note:** Semantic hit testing is only available on Spectacles. Phone lenses should use basic hit test (no `surfaceClassification`). The classification is unavailable in the Lens Studio desktop simulator — test on-device.

---

## Aligning Objects to Hit Surfaces

After a hit test, orient an object so it sits flat on the detected surface:

```typescript
function alignToSurface(obj: SceneObject, position: vec3, normal: vec3): void {
  obj.getTransform().setWorldPosition(position)

  // If the surface is nearly horizontal (floor/ceiling), use a stable up vector
  const EPSILON = 0.01
  const isHorizontal = 1 - Math.abs(normal.normalize().dot(vec3.up())) < EPSILON

  const lookDir = isHorizontal ? vec3.forward() : normal.cross(vec3.up())
  obj.getTransform().setWorldRotation(quat.lookAt(lookDir, normal))
}
```

---

## Physics Raycasting (Scene Geometry)

Use `Physics.createGlobalProbe()` to cast rays against **scene colliders** (not real-world surfaces). This is the tool for hover detection, interaction, and projectile collision:

```typescript
const probe = Physics.createGlobalProbe()

probe.rayCast(
  rayStart.getTransform().getWorldPosition(),
  rayEnd.getTransform().getWorldPosition(),
  (hit) => {
    if (hit) {
      print('Hit object: ' + hit.collider.getSceneObject().name)
      print('Hit position: ' + JSON.stringify(hit.position))
      print('Hit normal: ' + JSON.stringify(hit.normal))

      if (markerObject) {
        markerObject.getTransform().setWorldPosition(hit.position)
      }
    }
  }
)
```

### Gaze ray from camera

```typescript
const cam = scene.findByName('Camera').getComponent('Camera') as Camera
const camT = cam.getSceneObject().getTransform()
const origin = camT.getWorldPosition()
const direction = camT.forward
const rayLength = 50

probe.rayCast(origin, origin.add(direction.uniformScale(rayLength)), (hit) => {
  if (hit) handleGazeHit(hit)
})
```

### Layers and filtering

```typescript
const probe = Physics.createGlobalProbe()
probe.collisionMask = CollisionLayer.getMask(['Default']) // only hit Default layer
```

---

## WorldQueryModule vs Physics Raycasting

| | `WorldQueryModule.hitTest` | `Physics.createGlobalProbe().rayCast` |
|---|---|---|
| Hits | Real-world surfaces (depth mesh) | Scene colliders only |
| Use for | Placing content in the room | Interaction, collision detection |
| Async? | Yes (callback) | Yes (callback) |
| Available in simulator? | Limited / No | Yes |
| Semantic labels? | Yes (Spectacles only) | No |

---

## Leaderboard Module

Lens Studio's Leaderboard module stores globally visible scores via Snap's Lens Cloud.

### Setup
```typescript
const leaderboardModule = require('LensStudio:LeaderboardModule')
```

Or inject via `@input`:
```typescript
@input leaderboardModule: LeaderboardModule
```

### Create or retrieve a leaderboard

```typescript
const options = Leaderboard.CreateOptions.create()
options.name = 'MY_LEADERBOARD'
options.ttlSeconds = 86400 // 24 hours; 0 = permanent
options.orderingType = Leaderboard.OrderingType.Descending // higher = better

leaderboardModule.getLeaderboard(
  options,
  (leaderboard) => {
    // leaderboard is ready
    submitScore(leaderboard, 42)
  },
  (status) => print('Failed to get leaderboard: ' + status)
)
```

### Submit a score

```typescript
function submitScore(leaderboard: any, score: number): void {
  leaderboard.submitScore(
    score,
    (userInfo) => {
      print('Score submitted! User: ' + userInfo.snapchatUser.displayName)
    },
    (status) => print('Submit failed: ' + status)
  )
}
```

### Read the leaderboard

```typescript
const retrieval = Leaderboard.RetrievalOptions.create()
retrieval.usersLimit = 10
retrieval.usersType = Leaderboard.UsersType.Global // or Friends, User

leaderboard.getLeaderboardInfo(
  retrieval,
  (otherRecords, currentUserRecord) => {
    if (currentUserRecord) {
      print('My score: ' + currentUserRecord.score)
    }
    otherRecords.forEach((record, i) => {
      if (record?.snapchatUser) {
        print(`#${i + 1}: ${record.snapchatUser.displayName} — ${record.score}`)
      }
    })
  },
  (status) => print('Fetch failed: ' + status)
)
```

---

## Common Gotchas

- **Hit test results are async** — never read `result` synchronously before the callback fires.
- **`filter: true`** on hit test sessions smooths jittery hit positions. Disable it only if you need raw sensor accuracy.
- **Ray length matters** — a ray that misses all surfaces returns `null`. If you expect a hit, try multiple lengths (0.5×, 1×, 2× of your target) before giving up.
- **World Query is unavailable in the Lens Studio simulator** on desktop — test surface placement on-device.
- **Semantic classification** requires `surfaceClassification = true` in options and is Spectacles-only.
- **Leaderboard names are global** within a lens. Different lenses cannot share a leaderboard by name.
- **Leaderboard `ttlSeconds = 0`** means the record never expires, which could fill up quota. Use a TTL appropriate for your game's session length.
