---
name: authoritative-server
description: Build multiplayer scenes with a headless authoritative server that controls game state, validates changes, and prevents cheating. Install @dcl/sdk@auth-server and run with hammurabi-server. Use isServer() to branch logic, registerMessages() for client-server communication, validateBeforeChange() for server-only components, Storage for persistence, and EnvVar for configuration. Use when user wants authoritative server, anti-cheat, server-side validation, persistent storage, environment variables, or server messages.
---

# Authoritative Server Pattern

Build multiplayer Decentraland scenes where a **headless server** controls game state, validates changes, and prevents cheating. The same codebase runs on both server and client, with the server having full authority.

For basic CRDT multiplayer (no server), see the `multiplayer-sync` skill instead.

## Setup

### 1. Install the auth-server SDK branch (MANDATORY)

You **must** use the `auth-server` tag — the standard `@dcl/sdk` does NOT include authoritative server APIs (`isServer`, `registerMessages`, `Storage`, `EnvVar`, etc.):

```bash
npm install @dcl/sdk@auth-server
```

### 2. Configure scene.json

Your `scene.json` **must** include these properties:

- **`authoritativeMultiplayer: true`** — enables the authoritative server runtime.
- **`worldConfiguration.name`** — identifies the world for deployment, Storage, and EnvVar.
- **`logsPermissions`** — array of wallet addresses allowed to see server logs in the console. Without this, server `console.log()` output is hidden.

```json
{
  "authoritativeMultiplayer": true,
  "worldConfiguration": {
    "name": "my-world-name.dcl.eth"
  },
  "logsPermissions": ["0xYourWalletAddress"]
}
```

### 3. Run the scene

Just use the normal preview — it automatically starts the authoritative server in the background when `authoritativeMultiplayer: true` is set in scene.json.

> **Debugging note (do NOT tell the user to run this):** Under the hood, the preview runs `npx @dcl/hammurabi-server@next`. If the auth server isn't starting, check that the hammurabi process is running and look for errors in its output.

## Server/Client Branching

Use `isServer()` to branch logic in a single codebase:

```typescript
import { isServer } from '@dcl/sdk/network'

export async function main() {
  if (isServer()) {
    // Server-only: game logic, validation, state management
    const { server } = await import('./server/server')
    server()
    return
  }

  // Client-only: UI, input, message sending
  setupClient()
  setupUi()
}
```

The server runs your scene code headlessly (no rendering). It has access to all player positions via `PlayerIdentityData` and manages all authoritative game state.

## Synced Components with Validation

Define custom components that sync from server to all clients. **Always** use `validateBeforeChange()` to prevent clients from modifying server-authoritative state.

### Custom Components (Global Validation)

```typescript
import { engine, Schemas } from '@dcl/sdk/ecs'
import { AUTH_SERVER_PEER_ID } from '@dcl/sdk/network/message-bus-sync'

export const GameState = engine.defineComponent('game:State', {
  phase: Schemas.String,
  score: Schemas.Number,
  timeRemaining: Schemas.Number
})

// Restrict ALL modifications to server only
GameState.validateBeforeChange((value) => {
  return value.senderAddress === AUTH_SERVER_PEER_ID
})
```

### Built-in Components (Per-Entity Validation)

For built-in components like `Transform` and `GltfContainer`, use per-entity validation so you don't block client-side transforms on the player's own entities:

```typescript
import { Entity, Transform, GltfContainer } from '@dcl/sdk/ecs'
import { AUTH_SERVER_PEER_ID } from '@dcl/sdk/network/message-bus-sync'

type ComponentWithValidation = {
  validateBeforeChange: (entity: Entity, cb: (value: { senderAddress: string }) => boolean) => void
}

function protectServerEntity(entity: Entity, components: ComponentWithValidation[]) {
  for (const component of components) {
    component.validateBeforeChange(entity, (value) => {
      return value.senderAddress === AUTH_SERVER_PEER_ID
    })
  }
}

// Usage: after creating a server-managed entity
const entity = engine.addEntity()
Transform.create(entity, { position: Vector3.create(10, 5, 10) })
GltfContainer.create(entity, { src: 'assets/model.glb' })
protectServerEntity(entity, [Transform, GltfContainer])
```

### Syncing Entities

After creating and protecting an entity, sync it to all clients:

```typescript
import { syncEntity } from '@dcl/sdk/network'

syncEntity(entity, [Transform.componentId, GameState.componentId])
```

## Messages

Use `registerMessages()` for client-to-server and server-to-client communication:

### Define Messages

```typescript
import { Schemas } from '@dcl/sdk/ecs'
import { registerMessages } from '@dcl/sdk/network'

export const Messages = {
  // Client -> Server
  playerJoin: Schemas.Map({ displayName: Schemas.String }),
  playerAction: Schemas.Map({ actionType: Schemas.String, data: Schemas.Number }),

  // Server -> Client
  gameEvent: Schemas.Map({ eventType: Schemas.String, playerName: Schemas.String })
}

export const room = registerMessages(Messages)
```

### Send Messages

```typescript
// Client sends to server
room.send('playerJoin', { displayName: 'Alice' })

// Server sends to ALL clients
room.send('gameEvent', { eventType: 'ROUND_START', playerName: '' })

// Server sends to ONE client
room.send('gameEvent', { eventType: 'YOU_WIN', playerName: 'Alice' }, { to: [playerAddress] })
```

### Receive Messages

```typescript
// Server receives from client
room.onMessage('playerJoin', (data, context) => {
  if (!context) return
  const playerAddress = context.from  // Wallet address of sender
  console.log(`[Server] Player joined: ${data.displayName} (${playerAddress})`)
})

// Client receives from server
room.onMessage('gameEvent', (data) => {
  console.log(`Event: ${data.eventType}`)
})
```

### Wait for State Sync

Before sending messages from the client, wait until state is synchronized:

```typescript
import { isStateSynchronized } from '@dcl/sdk/network'

engine.addSystem(() => {
  if (!isStateSynchronized()) return

  // Safe to send messages now
  room.send('playerJoin', { displayName: 'Player' })
})
```

## Server Reading Player Positions

The server can read **actual** player positions — critical for anti-cheat:

```typescript
import { engine, PlayerIdentityData, Transform } from '@dcl/sdk/ecs'

engine.addSystem(() => {
  for (const [entity, identity] of engine.getEntitiesWith(PlayerIdentityData)) {
    const transform = Transform.getOrNull(entity)
    if (!transform) continue

    const address = identity.address
    const position = transform.position
    // Use actual server-verified position, not client-reported data
  }
})
```

Never trust client-reported positions. Always read `PlayerIdentityData` + `Transform` on the server.

## Storage

Persist data across server restarts. **Server-only** — guard with `isServer()`.

```typescript
import { Storage } from '@dcl/sdk/server'
```

### World Storage (Global)

Shared across all players:

```typescript
// Store
await Storage.world.set('leaderboard', JSON.stringify(leaderboardData))

// Retrieve
const data = await Storage.world.get<string>('leaderboard')
if (data) {
  const leaderboard = JSON.parse(data)
}

// Delete
await Storage.world.delete('oldKey')
```

### Player Storage (Per-Player)

Keyed by player wallet address:

```typescript
// Store
await Storage.player.set(playerAddress, 'highScore', String(score))

// Retrieve
const saved = await Storage.player.get<string>(playerAddress, 'highScore')
const highScore = saved ? parseInt(saved) : 0

// Delete
await Storage.player.delete(playerAddress, 'highScore')
```

Storage only accepts strings. Use `JSON.stringify()`/`JSON.parse()` for objects and `String()`/`parseInt()` for numbers.

Local development storage is at `node_modules/@dcl/sdk-commands/.runtime-data/server-storage.json`.

## Environment Variables

Configure your scene without hardcoding values. **Server-only** — guard with `isServer()`.

```typescript
import { EnvVar } from '@dcl/sdk/server'

// Read a variable with default
const maxPlayers = parseInt((await EnvVar.get('MAX_PLAYERS')) || '4')
const debugMode = ((await EnvVar.get('DEBUG')) || 'false') === 'true'
```

### Local Development

Create a `.env` file in your project root:

```
MAX_PLAYERS=8
GAME_DURATION=300
DEBUG=true
```

Add `.env` to your `.gitignore`.

### Deploy to Production

```bash
# Set a variable
npx sdk-commands deploy-env MAX_PLAYERS --value 8

# Delete a variable
npx sdk-commands deploy-env OLD_VAR --delete
```

Deployed env vars take precedence over `.env` file values.

## Recommended Project Structure

```
src/
├── index.ts              # Entry point — isServer() branching
├── client/
│   ├── setup.ts          # Client initialization, message handlers
│   └── ui.tsx            # React ECS UI reading synced state
├── server/
│   ├── server.ts         # Server init, systems, message handlers
│   └── gameState.ts      # Server state management class
└── shared/
    ├── schemas.ts        # Synced component definitions + validateBeforeChange
    └── messages.ts       # Message definitions via registerMessages()
```

Put synced components and messages in `shared/` so both server and client import the same definitions. Keep server logic (Storage, EnvVar, game systems) in `server/`. Keep UI and client input in `client/`.

## Testing & Debugging

- **Log prefixes**: Use `[Server]` and `[Client]` prefixes in `console.log()` to distinguish server and client output in the terminal.
- **Stale CRDT files**: If you see "Outside of the bounds of written data" errors, delete `main.crdt` and `main1.crdt` files and restart.
- **Storage inspection**: Check `node_modules/@dcl/sdk-commands/.runtime-data/server-storage.json` to inspect persisted data during local development.
- **Timers**: `setTimeout`/`setInterval` are available via runtime polyfill. For game logic, prefer `engine.addSystem()` with a delta-time accumulator to stay in sync with the frame loop.
- **Entity sync issues**: Verify you call `syncEntity(entity, [componentIds])` with the correct component IDs (`MyComponent.componentId`).

## Important Notes

- **Use `Schemas.Int64` for timestamps**: `Schemas.Number` corrupts large numbers (13+ digits). Always use `Schemas.Int64` for values like `Date.now()`.
- **State sync readiness**: Clients must wait for `isStateSynchronized()` (from `@dcl/sdk/network`) to return `true` before sending messages.
- **Custom vs built-in validation**: Custom components use global `validateBeforeChange((value) => ...)`. Built-in components (Transform, GltfContainer) use per-entity `validateBeforeChange(entity, (value) => ...)`.
- **Single codebase**: Both server and client run the same `index.ts` entry point. Use `isServer()` to branch.
- **No Node.js APIs**: The DCL runtime uses sandboxed QuickJS — no `fs`, `http`, etc. `setTimeout`/`setInterval` are supported. Use SDK-provided APIs (Storage, EnvVar, engine systems) for server-side operations.
- **SDK branch (MANDATORY)**: The auth-server pattern requires `npm install @dcl/sdk@auth-server`, not the standard `@dcl/sdk`. Without it, `isServer()`, `registerMessages()`, `Storage`, and `EnvVar` are unavailable.
- **scene.json required fields**: `authoritativeMultiplayer: true` must be set, and `logsPermissions: ["0xWalletAddress"]` must list wallet addresses that should see server logs.
- For basic CRDT multiplayer without a server, see the `multiplayer-sync` skill.
