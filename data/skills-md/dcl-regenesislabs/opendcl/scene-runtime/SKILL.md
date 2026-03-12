---
name: scene-runtime
description: Scene runtime APIs — async tasks, HTTP fetch, WebSockets, realm/scene info, timers, restricted actions, portable experiences, testing framework
---

# Scene Runtime APIs

Cross-cutting runtime APIs available in every Decentraland SDK7 scene.

## Async Tasks

The scene runtime is single-threaded. Wrap any async work in `executeTask()`:

```typescript
import { executeTask } from '@dcl/sdk/ecs'

executeTask(async () => {
  const res = await fetch('https://api.example.com/data')
  const data = await res.json()
  console.log(data)
})
```

## HTTP: fetch & signedFetch

**Plain fetch** works for public APIs:
```typescript
const res = await fetch('https://api.example.com/data')
```

**signedFetch** proves the player's identity to your backend. Use `getHeaders()` to obtain only the signed headers (useful when a library manages its own fetch):
```typescript
import { signedFetch, getHeaders } from '~system/SignedFetch'

// Full signed request
const res = await signedFetch({ url: 'https://your-server.com/api', init: { method: 'POST', body: JSON.stringify(payload) } })

// Get signed headers only (for custom fetch calls)
const { headers } = await getHeaders({ url: 'https://your-server.com/api' })
```

> **Permission**: External HTTP requires `"ALLOW_TO_MOVE_PLAYER_INSIDE_SCENE"` or no special permission for plain fetch; `signedFetch` needs the player to have interacted with the scene.

## WebSocket

```typescript
const ws = new WebSocket('wss://your-server.com/ws')
ws.onopen = () => ws.send('hello')
ws.onmessage = (event) => console.log(event.data)
ws.onclose = () => console.log('disconnected')
```

## Scene & Realm Information

```typescript
import { getSceneInformation, getRealm } from '~system/Runtime'
import { getExplorerInformation } from '~system/EnvironmentApi'

executeTask(async () => {
  // Scene info: URN, content mappings, metadata JSON, baseUrl
  const scene = await getSceneInformation({})
  const metadata = JSON.parse(scene.metadataJson)
  console.log(scene.urn, scene.baseUrl, metadata)

  // Realm info: baseUrl, realmName, isPreview, networkId, commsAdapter
  const realm = await getRealm({})
  console.log(realm.realmInfo?.realmName, realm.realmInfo?.isPreview)

  // Explorer info: agent string, platform, configurations
  const explorer = await getExplorerInformation({})
  console.log(explorer.agent, explorer.platform)
})
```

## World Time

```typescript
import { getWorldTime } from '~system/EnvironmentApi'

executeTask(async () => {
  const { seconds } = await getWorldTime({})
  // seconds = coordinated world time (cycles 0-86400 for day/night)
})
```

## Read Deployed Files

Read files deployed with the scene at runtime:

```typescript
import { readFile } from '~system/Runtime'

executeTask(async () => {
  const result = await readFile({ fileName: 'data/config.json' })
  const text = new TextDecoder().decode(result.content)
  const config = JSON.parse(text)
})
```

## EngineInfo Component

Access frame-level timing:

```typescript
import { EngineInfo } from '@dcl/sdk/ecs'

engine.addSystem(() => {
  const info = EngineInfo.getOrNull(engine.RootEntity)
  if (info) {
    console.log(info.frameNumber, info.tickNumber, info.totalRuntime)
  }
})
```

## Restricted Actions

These require player interaction before they can execute. Import from `~system/RestrictedActions`:

```typescript
import {
  movePlayerTo,
  teleportTo,
  triggerEmote,
  changeRealm,
  openExternalUrl,
  openNftDialog,
  triggerSceneEmote,
  copyToClipboard,
  setCommunicationsAdapter
} from '~system/RestrictedActions'

// Move player within scene bounds
movePlayerTo({ newRelativePosition: { x: 8, y: 0, z: 8 } })

// Teleport to coordinates in Genesis City
teleportTo({ worldCoordinates: { x: 50, y: 70 } })

// Play a built-in emote
triggerEmote({ predefinedEmote: 'wave' })

// Open URL in browser (prompts user)
openExternalUrl({ url: 'https://decentraland.org' })

// Open NFT detail dialog
openNftDialog({ urn: 'urn:decentraland:ethereum:erc721:0x06012c8cf97BEaD5deAe237070F9587f8E7A266d:558536' })

// Copy text to clipboard
copyToClipboard({ value: 'Hello from Decentraland!' })

// Change realm
changeRealm({ realm: 'other-realm.dcl.eth', message: 'Join this realm?' })
```

## Timers

**setTimeout / setInterval** are supported via the QuickJS runtime polyfill:

```typescript
setTimeout(() => console.log('delayed'), 2000)
const id = setInterval(() => console.log('tick'), 1000)
clearInterval(id)
```

**System-based timers** (recommended for game logic — synchronized with the frame loop):

```typescript
let elapsed = 0
engine.addSystem((dt: number) => {
  elapsed += dt
  if (elapsed >= 3) {
    elapsed = 0
    // Do something every 3 seconds
  }
})
```

## Component.onChange() Listener

React to component changes on any entity:

```typescript
Transform.onChange(engine.PlayerEntity, (newValue) => {
  if (newValue) {
    console.log('Player moved to', newValue.position)
  }
})
```

## Utility: removeEntityWithChildren

Recursively remove an entity and all its children:

```typescript
import { removeEntityWithChildren } from '@dcl/sdk/ecs'

removeEntityWithChildren(engine, parentEntity)
```

## Portable Experiences

Scenes that persist across world navigation:

```typescript
import { spawn, kill, exit, getPortableExperiencesLoaded } from '~system/PortableExperiences'

// Spawn a portable experience by URN
const result = await spawn({ urn: 'urn:decentraland:entity:bafk...' })

// List currently loaded portable experiences
const loaded = await getPortableExperiencesLoaded({})

// Kill a specific portable experience
await kill({ urn: 'urn:decentraland:entity:bafk...' })

// Exit self (if this scene IS a portable experience)
await exit({})
```

## Testing Framework

SDK7 includes a testing framework for automated scene tests:

```typescript
import { test, assert, assertEquals, assertComponentValue } from '@dcl/sdk/testing'
import { setCameraTransform } from '@dcl/sdk/testing'

test('cube is at correct position', async (context) => {
  // Set up camera for the test
  setCameraTransform({ position: { x: 8, y: 1, z: 8 } })

  // Wait for systems to run
  await context.helpers.waitNTicks(2)

  // Assert component values
  assertComponentValue(cubeEntity, Transform, {
    position: Vector3.create(8, 1, 8)
  })

  // Basic assertions
  assert(Transform.has(cubeEntity), 'Entity should have Transform')
  assertEquals(1 + 1, 2)
})
```

Run tests with:
```bash
npx @dcl/sdk-commands test
```

## Best Practices

- Always wrap async code in `executeTask()` — bare promises will be silently dropped
- Use `signedFetch` (not plain `fetch`) when your backend needs to verify the player's identity
- Prefer system-based timers over `setTimeout`/`setInterval` for game logic — they stay in sync with the frame loop
- Check `realm.realmInfo?.isPreview` to detect preview mode and enable debug features
- Use `readFile()` for data files (JSON configs, level data) deployed alongside the scene
- `removeEntityWithChildren()` is essential when cleaning up complex entity hierarchies
