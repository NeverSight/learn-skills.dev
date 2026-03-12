---
name: advanced-rendering
description: Advanced rendering features in Decentraland scenes. Use Billboard to make entities face the camera, TextShape for 3D text, advanced PBR material properties like metallic/roughness/transparency, GltfNodeModifiers for per-node visibility and material overrides in GLTF models, and VisibilityComponent to show/hide entities. Use when user wants billboards, 3D text, text labels, material effects, transparency, glow, or model node control.
---

# Advanced Rendering in Decentraland

## Billboard (Face the Camera)

Make entities always rotate to face the player's camera:

```typescript
import { engine, Transform, Billboard, BillboardMode, MeshRenderer } from '@dcl/sdk/ecs'
import { Vector3 } from '@dcl/sdk/math'

const sign = engine.addEntity()
Transform.create(sign, { position: Vector3.create(8, 2, 8) })
MeshRenderer.setPlane(sign)

// Rotate only on Y axis (most common — stays upright)
Billboard.create(sign, {
  billboardMode: BillboardMode.BM_Y
})
```

### Billboard Modes

```typescript
BillboardMode.BM_Y      // Rotate on Y axis only (stays upright) — most common
BillboardMode.BM_ALL    // Rotate on all axes (fully faces camera)
BillboardMode.BM_X      // Rotate on X axis only
BillboardMode.BM_Z      // Rotate on Z axis only
BillboardMode.BM_NONE   // No billboard rotation
```

- Prefer `BM_Y` over `BM_ALL` for most use cases — it looks more natural and is cheaper to render.
- `BM_ALL` is useful for particles or effects that should always directly face the camera.

## TextShape (3D Text)

Render text directly in 3D space:

```typescript
import { engine, Transform, TextShape, TextAlignMode } from '@dcl/sdk/ecs'
import { Vector3, Color4 } from '@dcl/sdk/math'

const label = engine.addEntity()
Transform.create(label, { position: Vector3.create(8, 3, 8) })

TextShape.create(label, {
  text: 'Hello World!',
  fontSize: 24,
  textColor: Color4.White(),
  outlineColor: Color4.Black(),
  outlineWidth: 0.1,
  textAlign: TextAlignMode.TAM_MIDDLE_CENTER
})
```

### Text Alignment Options

```typescript
TextAlignMode.TAM_TOP_LEFT
TextAlignMode.TAM_TOP_CENTER
TextAlignMode.TAM_TOP_RIGHT
TextAlignMode.TAM_MIDDLE_LEFT
TextAlignMode.TAM_MIDDLE_CENTER
TextAlignMode.TAM_MIDDLE_RIGHT
TextAlignMode.TAM_BOTTOM_LEFT
TextAlignMode.TAM_BOTTOM_CENTER
TextAlignMode.TAM_BOTTOM_RIGHT
```

### Floating Label (Billboard + TextShape)

Combine Billboard and TextShape to create labels that always face the player:

```typescript
const floatingLabel = engine.addEntity()
Transform.create(floatingLabel, { position: Vector3.create(8, 4, 8) })

TextShape.create(floatingLabel, {
  text: 'NPC Name',
  fontSize: 16,
  textColor: Color4.White(),
  outlineColor: Color4.Black(),
  outlineWidth: 0.08,
  textAlign: TextAlignMode.TAM_BOTTOM_CENTER
})

Billboard.create(floatingLabel, {
  billboardMode: BillboardMode.BM_Y
})
```

## Advanced PBR Materials

### Metallic and Roughness

```typescript
import { engine, Transform, MeshRenderer, Material, MaterialTransparencyMode } from '@dcl/sdk/ecs'
import { Color4, Color3 } from '@dcl/sdk/math'

// Shiny metal
Material.setPbrMaterial(entity, {
  albedoColor: Color4.create(0.8, 0.8, 0.9, 1),
  metallic: 1.0,
  roughness: 0.1
})

// Rough stone
Material.setPbrMaterial(entity, {
  albedoColor: Color4.create(0.5, 0.5, 0.5, 1),
  metallic: 0.0,
  roughness: 0.9
})
```

### Transparency

```typescript
// Alpha blend — smooth transparency
Material.setPbrMaterial(entity, {
  albedoColor: Color4.create(1, 0, 0, 0.5), // 50% transparent red
  transparencyMode: MaterialTransparencyMode.MTM_ALPHA_BLEND
})

// Alpha test — cutout (binary visible/invisible based on threshold)
Material.setPbrMaterial(entity, {
  texture: Material.Texture.Common({ src: 'assets/cutout.png' }),
  transparencyMode: MaterialTransparencyMode.MTM_ALPHA_TEST,
  alphaTest: 0.5
})
```

### Emissive (Glow Effects)

```typescript
// Glowing material (emissiveColor uses Color3, not Color4)
Material.setPbrMaterial(entity, {
  albedoColor: Color4.create(0, 0, 0, 1),
  emissiveColor: Color3.create(0, 1, 0),  // Green glow
  emissiveIntensity: 2.0
})

// Emissive with texture
Material.setPbrMaterial(entity, {
  texture: Material.Texture.Common({ src: 'assets/diffuse.png' }),
  emissiveTexture: Material.Texture.Common({ src: 'assets/emissive.png' }),
  emissiveIntensity: 1.0,
  emissiveColor: Color3.White()
})
```

### Texture Maps

```typescript
Material.setPbrMaterial(entity, {
  texture: Material.Texture.Common({ src: 'assets/diffuse.png' }),
  bumpTexture: Material.Texture.Common({ src: 'assets/normal.png' }),
  emissiveTexture: Material.Texture.Common({ src: 'assets/emissive.png' })
})
```

## GltfContainer Visibility Masks

Control visibility and collision of specific mesh layers within a GLTF model using collision masks:

```typescript
import { engine, Transform, GltfContainer, ColliderLayer } from '@dcl/sdk/ecs'
import { Vector3 } from '@dcl/sdk/math'

const model = engine.addEntity()
Transform.create(model, { position: Vector3.create(4, 0, 4) })

GltfContainer.create(model, {
  src: 'models/myModel.glb',
  visibleMeshesCollisionMask: ColliderLayer.CL_PHYSICS | ColliderLayer.CL_POINTER,
  invisibleMeshesCollisionMask: ColliderLayer.CL_PHYSICS
})
```

## VisibilityComponent

Show or hide entities without removing them:

```typescript
import { engine, VisibilityComponent } from '@dcl/sdk/ecs'

// Hide an entity
VisibilityComponent.create(entity, { visible: false })

// Toggle visibility
const visibility = VisibilityComponent.getMutable(entity)
visibility.visible = !visibility.visible

// Useful for LOD (Level of Detail)
function lodSystem() {
  const playerPos = Transform.get(engine.PlayerEntity).position

  for (const [entity, transform] of engine.getEntitiesWith(Transform, MeshRenderer)) {
    const distance = Vector3.distance(playerPos, transform.position)

    if (distance > 30) {
      VisibilityComponent.createOrReplace(entity, { visible: false })
    } else {
      VisibilityComponent.createOrReplace(entity, { visible: true })
    }
  }
}

engine.addSystem(lodSystem)
```

### Per-Node Material Overrides (GltfNodeModifiers)

Override materials on specific nodes within a GLTF model without modifying the model file:

```typescript
import { GltfNode, GltfNodeState } from '@dcl/sdk/ecs'

// Hide a specific node in a model
GltfNode.create(entity, { path: 'RootNode/Armor', visible: false })

// Override a node's material
GltfNode.create(entity, {
  path: 'RootNode/Helmet',
  materialOverride: Material.Texture.Common({ src: 'images/custom-skin.png' })
})
```

### Avatar Texture

Generate a texture from a player's avatar:

```typescript
Material.setPbrMaterial(portraitFrame, {
  texture: Material.Texture.Avatar({ userId: '0x...' })
})
```

### Texture Modes

Control how textures are filtered and wrapped:

```typescript
import { TextureFilterMode, TextureWrapMode } from '@dcl/sdk/ecs'

Material.setPbrMaterial(entity, {
  texture: Material.Texture.Common({
    src: 'images/pixel-art.png',
    filterMode: TextureFilterMode.TFM_POINT,    // crisp pixels (no smoothing)
    wrapMode: TextureWrapMode.TWM_REPEAT        // tile the texture
  })
})
```

Filter modes: `TFM_POINT` (pixelated), `TFM_BILINEAR` (smooth), `TFM_TRILINEAR` (smoothest).
Wrap modes: `TWM_REPEAT` (tile), `TWM_CLAMP` (stretch edges), `TWM_MIRROR` (mirror tile).

## Best Practices

- Use `BillboardMode.BM_Y` instead of `BM_ALL` — looks more natural and renders faster
- Keep `fontSize` readable (16-32 for in-world text)
- Add `outlineColor` and `outlineWidth` to TextShape for legibility against any background
- Use `emissiveColor` with a dark `albedoColor` for maximum glow visibility
- `MTM_ALPHA_TEST` is cheaper than `MTM_ALPHA_BLEND` — use cutout when smooth transparency isn't needed
- Combine Billboard + TextShape for floating name labels above NPCs or objects
- Use VisibilityComponent for LOD systems instead of removing/re-adding entities
