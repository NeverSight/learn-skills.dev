---
name: player-avatar
description: Work with player avatars in Decentraland scenes. Read player position and profile data, customize appearance with AvatarBase, trigger emotes with triggerEmote/triggerSceneEmote, read equipped wearables via AvatarEquippedData, attach objects to players with AvatarAttach, create NPC avatars with AvatarShape, and modify avatars in areas. Use when user wants player data, emotes, wearables, avatar attachments, or NPCs.
---

# Player and Avatar System in Decentraland

## Player Position and Movement

Access the player's position via the reserved `engine.PlayerEntity`:

```typescript
import { engine, Transform } from '@dcl/sdk/ecs'

function trackPlayer() {
  if (!Transform.has(engine.PlayerEntity)) return

  const playerTransform = Transform.get(engine.PlayerEntity)
  console.log('Player position:', playerTransform.position)
  console.log('Player rotation:', playerTransform.rotation)
}

engine.addSystem(trackPlayer)
```

### Distance-Based Logic

```typescript
import { Vector3 } from '@dcl/sdk/math'

function proximityCheck() {
  const playerPos = Transform.get(engine.PlayerEntity).position
  const npcPos = Transform.get(npcEntity).position
  const distance = Vector3.distance(playerPos, npcPos)

  if (distance < 5) {
    console.log('Player is near the NPC')
  }
}

engine.addSystem(proximityCheck)
```

## Player Profile Data

Get the player's name, wallet address, and guest status:

```typescript
import { getPlayer } from '@dcl/sdk/src/players'

function main() {
  const player = getPlayer()
  if (player) {
    console.log('Name:', player.name)
    console.log('User ID:', player.userId)
    console.log('Is guest:', player.isGuest)
  }
}
```

- `userId` — the player's Ethereum wallet address (or guest ID)
- `isGuest` — `true` if the player hasn't connected a wallet

## Avatar Attachments

Attach 3D objects to a player's avatar:

```typescript
import { engine, Transform, GltfContainer, AvatarAttach, AvatarAnchorPointType } from '@dcl/sdk/ecs'

const hat = engine.addEntity()
GltfContainer.create(hat, { src: 'models/hat.glb' })

// Attach to the local player's avatar
AvatarAttach.create(hat, {
  anchorPointId: AvatarAnchorPointType.AAPT_NAME_TAG
})
```

### Anchor Points

```typescript
AvatarAnchorPointType.AAPT_NAME_TAG      // Above the head
AvatarAnchorPointType.AAPT_RIGHT_HAND    // Right hand
AvatarAnchorPointType.AAPT_LEFT_HAND     // Left hand
AvatarAnchorPointType.AAPT_POSITION      // Avatar root position
```

### Attach to a Specific Player

```typescript
AvatarAttach.create(hat, {
  avatarId: '0x123...abc',  // Target player's wallet address
  anchorPointId: AvatarAnchorPointType.AAPT_RIGHT_HAND
})
```

## Triggering Emotes

### Default Emotes

```typescript
import { triggerEmote } from '~system/RestrictedActions'

// Play a built-in emote
triggerEmote({ predefinedEmote: 'robot' })
triggerEmote({ predefinedEmote: 'wave' })
triggerEmote({ predefinedEmote: 'clap' })
```

### Custom Scene Emotes

```typescript
import { triggerSceneEmote } from '~system/RestrictedActions'

// Play a custom emote animation (file must end with _emote.glb)
triggerSceneEmote({
  src: 'animations/Snowball_Throw_emote.glb',
  loop: false
})
```

**Notes:**
- Emotes play only while the player is standing still — walking or jumping interrupts them
- Custom emote files must have the `_emote.glb` suffix

## NPC Avatars

Create avatar-shaped NPCs using `AvatarShape`:

```typescript
import { engine, Transform, AvatarShape } from '@dcl/sdk/ecs'
import { Vector3 } from '@dcl/sdk/math'

const npc = engine.addEntity()
Transform.create(npc, { position: Vector3.create(8, 0, 8) })

AvatarShape.create(npc, {
  id: 'npc-1',
  name: 'Guard',
  bodyShape: 'urn:decentraland:off-chain:base-avatars:BaseMale',  // or BaseFemale
  wearables: [
    'urn:decentraland:off-chain:base-avatars:eyebrows_00',
    'urn:decentraland:off-chain:base-avatars:mouth_00',
    'urn:decentraland:off-chain:base-avatars:eyes_00',
    'urn:decentraland:off-chain:base-avatars:blue_tshirt',
    'urn:decentraland:off-chain:base-avatars:brown_pants',
    'urn:decentraland:off-chain:base-avatars:classic_shoes',
    'urn:decentraland:off-chain:base-avatars:short_hair'
  ],
  hairColor: { r: 0.92, g: 0.76, b: 0.62 },  // RGB values 0-1
  skinColor: { r: 0.94, g: 0.85, b: 0.6 },   // RGB values 0-1
  emotes: []
})
```

### Mannequin (Show Only Wearables)

Display just the wearables without a full avatar body:

```typescript
AvatarShape.create(mannequin, {
  id: 'mannequin-1',
  name: 'Display',
  wearables: [
    'urn:decentraland:matic:collections-v2:0x90e5cb2d673699be8f28d339c818a0b60144c494:0'
  ],
  show_only_wearables: true
})
```

NPC avatars are static — they display the avatar model but don't move or animate on their own. Combine with Animator or Tween for movement.

## Avatar Modifier Areas

Modify how avatars appear or behave in a region:

```typescript
import { engine, Transform, AvatarModifierArea, AvatarModifierType } from '@dcl/sdk/ecs'
import { Vector3 } from '@dcl/sdk/math'

const modifierArea = engine.addEntity()
Transform.create(modifierArea, {
  position: Vector3.create(8, 1.5, 8),
  scale: Vector3.create(4, 3, 4)
})

AvatarModifierArea.create(modifierArea, {
  area: { box: Vector3.create(4, 3, 4) },
  modifiers: [AvatarModifierType.AMT_HIDE_AVATARS],
  excludeIds: ['0x123...abc']  // Optional: exclude specific players
})
```

### Available Modifiers

```typescript
AvatarModifierType.AMT_HIDE_AVATARS       // Hide all avatars in the area
AvatarModifierType.AMT_DISABLE_PASSPORTS  // Disable clicking on avatars to see profiles
AvatarModifierType.AMT_DISABLE_JUMPING    // Prevent jumping in the area
```

### Movement Constraints

```typescript
// Prevent jumping in a specific area
const constraintArea = engine.addEntity()
Transform.create(constraintArea, {
  position: Vector3.create(8, 5, 8),
  scale: Vector3.create(6, 10, 6)
})

AvatarModifierArea.create(constraintArea, {
  area: { box: Vector3.create(6, 10, 6) },
  modifiers: [AvatarModifierType.AMT_DISABLE_JUMPING]
})
```

## Teleporting the Player

**You MUST use `movePlayerTo` from `~system/RestrictedActions` to move or teleport the player.** Setting `Transform.getMutable(engine.PlayerEntity).position` does NOT work — the runtime ignores direct writes to the player transform.

```typescript
import { movePlayerTo } from '~system/RestrictedActions'

// Move player to a position
void movePlayerTo({
  newRelativePosition: Vector3.create(8, 0, 8)
})

// Move player with camera direction
void movePlayerTo({
  newRelativePosition: Vector3.create(8, 0, 8),
  cameraTarget: Vector3.create(8, 1, 12)
})
```

### Avatar Change Listeners

React to avatar changes in real-time:

```typescript
import { AvatarEmoteCommand, AvatarBase, AvatarEquippedData } from '@dcl/sdk/ecs'

// Detect when any player triggers an emote
AvatarEmoteCommand.onChange(engine.PlayerEntity, (cmd) => {
  if (cmd) console.log('Emote played:', cmd.emoteUrn)
})

// Detect avatar appearance changes (wearables, skin color, etc.)
AvatarBase.onChange(engine.PlayerEntity, (base) => {
  if (base) console.log('Avatar name:', base.name)
})

// Detect equipment changes
AvatarEquippedData.onChange(engine.PlayerEntity, (equipped) => {
  if (equipped) console.log('Wearables changed:', equipped.wearableUrns)
})
```

### Additional Anchor Points

Beyond the commonly used anchor points, the full list includes:

- `AvatarAnchorPointType.AAPT_POSITION` — avatar feet position
- `AvatarAnchorPointType.AAPT_NAME_TAG` — above the name tag
- `AvatarAnchorPointType.AAPT_LEFT_HAND` / `AAPT_RIGHT_HAND`
- `AvatarAnchorPointType.AAPT_HEAD` — head bone
- `AvatarAnchorPointType.AAPT_NECK` — neck bone

## Best Practices

- Always check `Transform.has(engine.PlayerEntity)` before reading player data — it may not be ready on the first frame
- Use `getPlayer()` to check `isGuest` before attempting wallet-dependent features
- `AvatarAttach` requires the target player to be in the same scene — attachments disappear when the player leaves
- Custom emote files must use the `_emote.glb` naming convention
- Use `AvatarModifierArea` with `AMT_HIDE_AVATARS` for private rooms or puzzle areas
- Add `excludeIds` to modifier areas when you want specific players (like the scene owner) to remain visible
- **Never use `Transform.getMutable(engine.PlayerEntity)` to move the player** — it does not work. Always use `movePlayerTo` from `~system/RestrictedActions`
- `Transform.get(engine.PlayerEntity)` is valid for **reading** position only

For component field details, see `{baseDir}/../../context/components-reference.md`.
