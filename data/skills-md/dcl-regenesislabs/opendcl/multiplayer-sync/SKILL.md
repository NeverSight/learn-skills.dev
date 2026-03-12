---
name: multiplayer-sync
description: Synchronize state between players in Decentraland multiplayer scenes using CRDT-based networking. Use when user wants multiplayer, sync state, network entities, shared world state, or real-time collaboration.
---

# Multiplayer Synchronization in Decentraland

Decentraland scenes are inherently multiplayer. All players in the same scene share the same space. SDK7 uses CRDT-based synchronization.

## How Sync Works

- Entities must be explicitly synced using `syncEntity()` from `@dcl/sdk/network`.
- The Decentraland runtime uses CRDTs (Conflict-free Replicated Data Types) to resolve conflicts.
- Last-write-wins semantics for most components (Transform, Material, etc.).
- No server code needed — sync is built into the runtime.

## Basic Synced Entity

Use `syncEntity()` to mark an entity and its components for multiplayer sync:

```typescript
import { engine, Transform, MeshRenderer, Material } from '@dcl/sdk/ecs'
import { syncEntity } from '@dcl/sdk/network'
import { Vector3, Color4 } from '@dcl/sdk/math'

// Create entity
const sharedCube = engine.addEntity()
Transform.create(sharedCube, { position: Vector3.create(8, 1, 8) })
MeshRenderer.setBox(sharedCube)
Material.setPbrMaterial(sharedCube, { albedoColor: Color4.Red() })

// Sync this entity's Transform to all players
syncEntity(sharedCube, [Transform.componentId])

// When any player changes the transform, all players see it
function moveCube() {
  const transform = Transform.getMutable(sharedCube)
  transform.position.x += 1  // All players see this change
}
```

## Custom Synced Components

Define custom components and sync them between players:

```typescript
import { engine, Schemas } from '@dcl/sdk/ecs'
import { syncEntity } from '@dcl/sdk/network'

// Define a custom component
const ScoreBoard = engine.defineComponent('scoreBoard', {
  score: Schemas.Int,
  playerName: Schemas.String,
  lastUpdated: Schemas.Int64
})

// Create and sync the entity
const board = engine.addEntity()
ScoreBoard.create(board, { score: 0, playerName: '', lastUpdated: 0 })
syncEntity(board, [ScoreBoard.componentId])

// Update from any player — synced via CRDT
function addScore(points: number) {
  const data = ScoreBoard.getMutable(board)
  data.score += points
  data.lastUpdated = Date.now()
}
```

## Player-Specific Data

Use `PlayerIdentityData` to distinguish players:

```typescript
import { engine, PlayerIdentityData } from '@dcl/sdk/ecs'

engine.addSystem(() => {
  for (const [entity] of engine.getEntitiesWith(PlayerIdentityData)) {
    const data = PlayerIdentityData.get(entity)
    console.log('Player:', data.address, 'Guest:', data.isGuest)
  }
})
```

## Schema Types

Available schema types for custom components:

| Type | Usage |
|------|-------|
| `Schemas.Boolean` | true/false |
| `Schemas.Int` | Integer numbers |
| `Schemas.Float` | Decimal numbers |
| `Schemas.String` | Text strings |
| `Schemas.Int64` | Large integers (timestamps) |
| `Schemas.Vector3` | 3D coordinates |
| `Schemas.Quaternion` | Rotations |
| `Schemas.Color3` | RGB colors |
| `Schemas.Color4` | RGBA colors |
| `Schemas.Entity` | Entity reference |
| `Schemas.Array(innerType)` | Array of values |
| `Schemas.Map(valueType)` | Key-value maps |
| `Schemas.Optional(innerType)` | Nullable values |
| `Schemas.Enum(enumType)` | Enum values |

## Communication Patterns

### Global State (Shared Object)
```typescript
// One entity holds shared game state
const gameState = engine.addEntity()
const GameState = engine.defineComponent('gameState', {
  phase: Schemas.String,
  timeRemaining: Schemas.Int,
  isActive: Schemas.Boolean
})
GameState.create(gameState, { phase: 'waiting', timeRemaining: 60, isActive: false })
```

### Per-Player State
```typescript
// Track each player's state separately using their entity
engine.addSystem(() => {
  for (const [entity] of engine.getEntitiesWith(PlayerIdentityData)) {
    // Each player's entity is unique to them
    // Attach custom components to player entities for per-player data
  }
})
```

### Entity Enum IDs

Distinguish predefined entities from player-created ones using `entityEnumId`:

```typescript
syncEntity(door, [Transform.componentId], 1)   // predefined entity (enum ID 1)
syncEntity(door2, [Transform.componentId], 2)  // predefined entity (enum ID 2)
syncEntity(playerBox, [Transform.componentId]) // no enum ID = player-created, lives with the player
```

Predefined entities (with an `entityEnumId`) persist after the creating player leaves. Player-created entities (no enum ID) are removed when the player disconnects.

### Parent-Child Relationships

Use `parentEntity` to create entity hierarchies that sync correctly:

```typescript
import { parentEntity, getParent, getChildren } from '@dcl/sdk/ecs'

parentEntity(child, parent)
const parent = getParent(child)
const children = getChildren(parent)
```

### Connection State

Check if the player is connected to the sync room:

```typescript
import { isStateSynchronized } from '@dcl/sdk/ecs'

engine.addSystem(() => {
  if (!isStateSynchronized()) return // wait for sync
  // safe to read/write synced state
})
```

### MessageBus

Send custom messages between players (fire-and-forget, no persistence):

```typescript
import { MessageBus } from '@dcl/sdk/message-bus'

const bus = new MessageBus()
bus.on('hit', (data: { damage: number }) => {
  console.log('Took damage:', data.damage)
})
bus.emit('hit', { damage: 10 })
```

### Player Enter/Leave Events

Detect players entering or leaving the scene:

```typescript
import { onEnterScene, onLeaveScene } from '@dcl/sdk/observables'

onEnterScene.add((player) => {
  console.log('Player entered:', player.userId)
})
onLeaveScene.add((player) => {
  console.log('Player left:', player.userId)
})
```

### Offline Testing

Test multiplayer locally without a server using the offline adapter:

```json
{
  "worldConfiguration": {
    "fixedAdapter": "offline:offline"
  }
}
```

## Important Notes

- **Entities must be explicitly synced** via `syncEntity(entity, [componentIds])` — pass the `componentId` of each component to sync
- **CRDT resolution**: If two players change the same component simultaneously, last-write-wins
- **No server-side code**: Decentraland scenes run entirely client-side with CRDT sync
- **Entity limits apply**: Each synced entity counts toward the scene's entity budget
- **Custom schemas must be deterministic**: Same component name = same schema across all clients
- **Use `Schemas.Int64` for timestamps**: `Schemas.Number` corrupts large numbers (13+ digits). Always use `Schemas.Int64` for values like `Date.now()`
- For server-authoritative multiplayer with validation and anti-cheat, see the `authoritative-server` skill
