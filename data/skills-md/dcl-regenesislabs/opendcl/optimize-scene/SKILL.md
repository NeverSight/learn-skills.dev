---
name: optimize-scene
description: Optimize Decentraland scene performance, reduce entity count, minimize triangle budgets, improve loading times, and stay within scene limits. Use when user wants to optimize, improve performance, fix lag, reduce load time, or check scene limits.
---

# Optimizing Decentraland Scenes

## Scene Limits (Per Parcel Count)

| Parcels | Max Entities | Max Triangles | Max Textures | Max Materials | Max Height |
|---------|-------------|---------------|-------------|--------------|-----------|
| 1 | 512 | 10,000 | 10 MB | 20 | 20m |
| 2 | 1,024 | 20,000 | 20 MB | 40 | 20m |
| 4 | 2,048 | 40,000 | 40 MB | 80 | 20m |
| 8 | 4,096 | 80,000 | 80 MB | 160 | 20m |
| 16 | 8,192 | 160,000 | 160 MB | 320 | 20m |

## Entity Count Optimization

### Reuse Entities
```typescript
// BAD: Creating new entity each time
function spawnBullet() {
  const bullet = engine.addEntity() // Creates entity every call
  // ...
}

// GOOD: Object pooling
const bulletPool: Entity[] = []
function getBullet(): Entity {
  const existing = bulletPool.find(e => !ActiveBullet.has(e))
  if (existing) return existing
  const newBullet = engine.addEntity()
  bulletPool.push(newBullet)
  return newBullet
}
```

### Remove Unused Entities
```typescript
engine.removeEntity(entity) // Frees the entity slot
```

### Use Parenting
Instead of separate transforms for each child, use entity hierarchy:
```typescript
const parent = engine.addEntity()
Transform.create(parent, { position: Vector3.create(8, 0, 8) })

// Children inherit parent transform
const child1 = engine.addEntity()
Transform.create(child1, { position: Vector3.create(0, 1, 0), parent })

const child2 = engine.addEntity()
Transform.create(child2, { position: Vector3.create(1, 1, 0), parent })
```

## Triangle Count Optimization

### Use Lower-Poly Models
- Small props: 100-500 triangles
- Medium objects: 500-1,500 triangles
- Large buildings: 1,500-5,000 triangles
- Hero pieces: Up to 10,000 triangles

### Use LOD (Level of Detail)
Show simpler models at distance:
```typescript
engine.addSystem(() => {
  // Check distance to player and swap models
  const playerPos = Transform.get(engine.PlayerEntity).position
  const objPos = Transform.get(myEntity).position
  const distance = Vector3.distance(playerPos, objPos)

  const gltf = GltfContainer.getMutable(myEntity)
  if (distance > 30) {
    gltf.src = 'models/building_lod2.glb' // Low poly
  } else if (distance > 15) {
    gltf.src = 'models/building_lod1.glb' // Medium poly
  } else {
    gltf.src = 'models/building_lod0.glb' // High poly
  }
})
```

### Use Primitives Instead of Models
For simple shapes, `MeshRenderer` is lighter than loading a .glb:
```typescript
MeshRenderer.setBox(entity)    // Very cheap
MeshRenderer.setSphere(entity) // Cheap
MeshRenderer.setPlane(entity)  // Very cheap
```

## Texture Optimization

- Use `.png` for UI/sprites with transparency
- Use `.jpg` for photos and textures without transparency
- Compress textures: 512x512 or 1024x1024 max for most use cases
- Use texture atlases (combine multiple textures into one image)
- Avoid 4096x4096 textures unless absolutely necessary
- Reuse materials across entities:
```typescript
// GOOD: Define material once, apply to many
Material.setPbrMaterial(entity1, { texture: Material.Texture.Common({ src: 'images/wall.jpg' }) })
Material.setPbrMaterial(entity2, { texture: Material.Texture.Common({ src: 'images/wall.jpg' }) })
// Same texture URL = shared in memory
```

## System Optimization

### Avoid Per-Frame Allocations
```typescript
// BAD: Creates new Vector3 every frame
engine.addSystem(() => {
  const target = Vector3.create(8, 1, 8) // Allocation!
})

// GOOD: Reuse constants
const TARGET = Vector3.create(8, 1, 8)
engine.addSystem(() => {
  // Use TARGET
})
```

### Throttle Expensive Operations
```typescript
let lastCheck = 0
engine.addSystem((dt) => {
  lastCheck += dt
  if (lastCheck < 0.5) return // Only run every 0.5 seconds
  lastCheck = 0
  // Expensive operation here
})
```

### Remove Systems When Not Needed
```typescript
const systemFn = (dt: number) => { /* ... */ }
engine.addSystem(systemFn)

// When no longer needed:
engine.removeSystem(systemFn)
```

## Loading Time Optimization

- Lazy-load 3D models (load on demand, not all at scene start)
- Use compressed .glb files (Draco compression)
- Minimize total asset size
- Use CDN URLs for large shared assets when possible
- Preload critical assets, defer non-essential ones

## Common Performance Pitfalls

1. **Too many systems**: Each system runs every frame. Combine related logic.
2. **Unnecessary component queries**: Cache `engine.getEntitiesWith()` results when the set doesn't change.
3. **Large GLTF files**: Optimize in Blender before export (decimate, remove hidden faces).
4. **Uncompressed audio**: Use .mp3 instead of .wav for music (10x smaller).
5. **Continuous raycasting**: Set `continuous: false` unless you need per-frame raycasting.
6. **Text rendering**: `TextShape` is expensive. Use `Label` (UI) for text that doesn't need to be in 3D space.
