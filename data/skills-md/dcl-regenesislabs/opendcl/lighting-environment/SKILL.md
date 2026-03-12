---
name: lighting-environment
description: Add dynamic lighting and control environment settings in Decentraland scenes. Create point, spot, and directional lights with LightSource, configure shadows, control day/night cycle with SkyboxTime, detect realm info, and use emissive materials for glow effects. Use when user wants lights, shadows, skybox, day-night cycle, or glowing materials.
---

# Lighting and Environment in Decentraland

## Point Lights

Emit light in all directions from a position:

```typescript
import { engine, Transform, LightSource } from '@dcl/sdk/ecs'
import { Vector3, Color3 } from '@dcl/sdk/math'

const light = engine.addEntity()
Transform.create(light, { position: Vector3.create(8, 3, 8) })

LightSource.create(light, {
  type: LightSource.Type.Point({}),
  color: Color3.White(),
  intensity: 300  // candela
})
```

### Colored Point Light

```typescript
LightSource.create(light, {
  type: LightSource.Type.Point({}),
  color: Color3.create(1, 0.5, 0),  // Warm orange
  intensity: 200,
  range: 15  // Maximum distance in meters
})
```

## Spot Lights

Emit a cone of light in a direction:

```typescript
import { Quaternion } from '@dcl/sdk/math'

const spotlight = engine.addEntity()
Transform.create(spotlight, {
  position: Vector3.create(8, 4, 8),
  rotation: Quaternion.fromEulerDegrees(-90, 0, 0)  // Point downward
})

LightSource.create(spotlight, {
  type: LightSource.Type.Spot({ innerAngle: 25, outerAngle: 45 }),
  color: Color3.White(),
  intensity: 800
})
```

- `innerAngle` — full-brightness cone angle (degrees)
- `outerAngle` — outer fade angle (degrees)
- The light direction follows the entity's forward vector (set via Transform rotation)

## Shadows

Enable shadows on point or spot lights:

```typescript
LightSource.create(spotlight, {
  type: LightSource.Type.Spot({ innerAngle: 25, outerAngle: 45 }),
  shadow: true,
  intensity: 800
})
```

### Shadow Mask Textures (Gobos)

Project a pattern through the light:

```typescript
const maskedLight = LightSource.getMutable(spotlight)
maskedLight.shadowMaskTexture = Material.Texture.Common({
  src: 'assets/scene/images/lightmask1.png'
})
```

## Toggling Lights

```typescript
// Toggle on/off
const lightData = LightSource.getMutable(light)
lightData.active = !lightData.active
```

## Light Limits

- Maximum **one active light per parcel** (16m x 16m)
- The renderer auto-culls lights based on quality settings and proximity
- Up to ~3 shadowed lights visible at once
- Intensity is in candela — visible distance grows roughly with `sqrt(intensity)`

## SkyboxTime (Day/Night Cycle)

### Fixed Time in scene.json

Set a permanent time of day without code:

```json
{
  "skyboxConfig": {
    "fixedTime": 36000
  }
}
```

Time values: 0 = midnight, 36000 = noon, 54000 = dusk, 72000 = midnight again.

### Read Current World Time

```typescript
import { getWorldTime } from '~system/Runtime'

executeTask(async () => {
  const time = await getWorldTime({})
  console.log('Seconds since midnight:', time.seconds)
})
```

### Change Time Dynamically

```typescript
import { SkyboxTime, TransitionMode } from '~system/Runtime'

// Set time of day (must target root entity)
SkyboxTime.create(engine.RootEntity, { fixed_time: 36000 })  // Noon

// Change with transition direction
SkyboxTime.createOrReplace(engine.RootEntity, {
  fixed_time: 54000,  // Dusk
  direction: TransitionMode.TM_BACKWARD
})
```

### Day/Night Cycle System

```typescript
let currentTime = 36000
const CYCLE_SPEED = 100  // Time units per second

function dayNightCycle(dt: number) {
  currentTime = (currentTime + CYCLE_SPEED * dt) % 72000
  SkyboxTime.createOrReplace(engine.RootEntity, {
    fixed_time: currentTime
  })
}

engine.addSystem(dayNightCycle)
```

## Realm Info

Detect which realm (server) the player is connected to:

```typescript
import { getRealm } from '~system/Runtime'

executeTask(async () => {
  const realm = await getRealm({})
  console.log('Realm:', realm.realmInfo?.realmName)
  console.log('Network:', realm.realmInfo?.networkId)
  console.log('Base URL:', realm.realmInfo?.baseUrl)
})
```

## Emissive Materials (Glow Effects)

For a visual glow without casting light on surroundings:

```typescript
import { engine, Material } from '@dcl/sdk/ecs'
import { Color4, Color3 } from '@dcl/sdk/math'

// Self-illuminated material (emissiveColor uses Color3, not Color4)
Material.setPbrMaterial(entity, {
  albedoColor: Color4.create(0, 0, 0, 1),
  emissiveColor: Color3.create(0, 1, 0),  // Green glow
  emissiveIntensity: 2.0
})
```

### Combining Emissive + LightSource

For an object that both glows visually and casts light:

```typescript
// Visual glow on the mesh
Material.setPbrMaterial(bulb, {
  emissiveColor: Color3.create(1, 0.9, 0.7),
  emissiveIntensity: 1.5
})

// Actual light emission
LightSource.create(bulb, {
  type: LightSource.Type.Point({}),
  color: Color3.create(1, 0.9, 0.7),
  intensity: 200,
  range: 10
})
```

### Shadow Types

LightSource supports three shadow modes:

- `PBLightSource_ShadowType.ST_NONE` — no shadows (cheapest)
- `PBLightSource_ShadowType.ST_HARD` — crisp shadows (medium cost)
- `PBLightSource_ShadowType.ST_SOFT` — smooth, blurred shadows (most expensive)

```typescript
import { LightSource, PBLightSource_ShadowType } from '@dcl/sdk/ecs'

LightSource.create(spotEntity, {
  type: LightSourceType.LST_SPOT,
  intensity: 50,
  shadow: PBLightSource_ShadowType.ST_SOFT
})
```

## Best Practices

- Stay within the **one light per parcel** budget — plan light placement around scene parcels
- Use emissive materials for decorative glow that doesn't need to illuminate surroundings
- Combine emissive materials with LightSource for realistic light fixtures (lamp = emissive mesh + point light)
- Use spot lights with shadows for dramatic effects (stage lighting, flashlights)
- Keep shadow count low (max ~3 visible) — disable `shadow` on lights that don't need it
- Set `range` on lights to limit their influence and save performance
- Use `SkyboxTime` for atmosphere — nighttime scenes with point lights create dramatic environments
