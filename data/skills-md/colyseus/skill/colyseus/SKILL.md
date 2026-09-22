---
name: colyseus
description: "Colyseus 0.18 multiplayer game servers and clients: rooms, Schema state synchronization, state callbacks, reconnection, matchmaking, client SDKs, client-side prediction. Use when colyseus, @colyseus/schema, @colyseus/sdk or colyseus.js appears in the task or in package.json, before writing any Room or Schema code, and when a project contains pre-0.17 code such as getStateCallbacks(), Room<State> generics, onLeave(client, consented), @filter() or new Server()."
license: MIT
metadata:
  version: "0.18.0"
  documentation: https://docs.colyseus.io
---

# Colyseus

Colyseus is an authoritative multiplayer framework for Node.js. The server owns
the state; clients send input and receive binary delta patches.

The APIs moved substantially in 0.17 and again in 0.18, and most model training
data predates both. Assume your recall of Colyseus is out of date, and check
before you write.

## Step 1: establish the version. Do not skip this.

Read the project's `package.json` (or `pnpm-lock.yaml` / `yarn.lock`) for
`colyseus` and `@colyseus/schema`.

| Installed | What to do |
| --- | --- |
| `colyseus` 0.18.x, `@colyseus/schema` 5.x | Use this skill's guidance directly. |
| 0.17.x | Read `https://docs.colyseus.io/migrating/0.18.md` to see what does **not** yet apply, then follow 0.17 idioms. |
| 0.16.x or older | Follow the version's own docs. Do **not** apply anything below. Version-specific sites: `https://0-16-x.docs.colyseus.io/`. |
| Nothing installed yet | Scaffold with `npm create colyseus-app@latest`, which is 0.18. |

If the version is ambiguous, ask rather than guess. Writing 0.18 APIs into a
0.16 project produces code that fails at import time, and writing 0.16 APIs into
a 0.18 project produces code that fails at runtime or silently desynchronizes.

## Step 2: what memory gets wrong

Left column is what an out-of-date recall produces. Check your own output for
it, and recognize it in existing projects.

| Do not write | Write instead | Why |
| --- | --- | --- |
| `import { Client } from "colyseus.js"` | `import { Client } from "@colyseus/sdk"` | The JS client package was renamed. |
| `class MyRoom extends Room<MyState>` | `class MyRoom extends Room` with `state = new MyState()` | The generic is now an options object, `Room<{ state, metadata, client }>`. A bare state type no longer type-checks. |
| `Client<UserData, AuthData>` | `Client<{ userData: UserData, auth: AuthData }>` | Same change on the client type. |
| `onCreate() { this.onMessage("x", fn) }` | `messages = { x: fn }` as a class property | The declarative map is the primary API. `this.onMessage()` still works and returns an unbind function. |
| `@type("string") name: string` only | `schema({ name: t.string() }, "MyState")` | The builder is the primary style and needs no compiler flags. Decorators remain supported. |
| `schema({ name: "string" })` | `schema({ name: t.string() })` | Raw string field types throw at definition time in schema 5. They remain valid as collection child types: `t.array("string")`. |
| `client.id` | `client.sessionId` | `client.id` was **removed** in 0.18. |
| `async onLeave(client, consented: boolean)` | `onLeave(client, code: CloseCode)` | The second argument is a close code. `4000` is truthy, so `if (!consented)` never runs and reconnection is silently never allowed. See the reconnection shape below. |
| `Protocol.WS_CLOSE_CONSENTED` | `CloseCode.CONSENTED` from `"colyseus"` | `Protocol.WS_*` moved to `CloseCode`. `4000`–`4010` are reserved; custom codes use `4011`–`4999`. |
| `this.setSeatReservationTime(15)` | `this.seatReservationTimeout = 15` | The method became a property. |
| `this.setMetadata({ status: "x" })` expecting a merge | `this.setMetadata({ ...this.metadata, status: "x" })` | 0.18 **replaces** metadata wholesale instead of shallow-merging. Same for `setMatchmaking({ metadata })`. |
| `@filter()` / `@filterChildren()` | `@view()` on the field, `client.view = new StateView()` in `onJoin` | Per-client filtering is opt-in through views. |
| `this.setSimulationInterval(fn)` | `this.setTimestep(fn)` | Renamed. The old name forwards, so it is not broken, but new code should use `setTimestep()`. For predicted games use `setFixedTimestep(step, tickRate)`. |
| A `Schema` with 64+ fields | Move the overflow onto a nested child `Schema` | 0.18 caps a `Schema` at 63 fields and throws at definition time. Inherited fields count. |
| `@colyseus/fossil-delta-serializer` | `@colyseus/schema` | Removed in 0.18. |

Two more that bite in production:

- **Playground** returns 404 on production mounts (`NODE_ENV=production`) unless
  you pass a guard middleware via its `use` option.
- **`@colyseus/auth` password hashing changed** in 0.18. Pre-0.18 hashes cannot
  be verified by the new hasher, so existing email/password users must reset
  their passwords. The legacy `scrypt` hasher and its global `AUTH_SALT` are
  deprecated.

### Shapes that changed, not just names

Three places where pre-0.17 code has a different structure, so a rename table
cannot show the fix. The left side is what to recognize.

**Server definition.** `new Server()` + `gameServer.define()`, and the
`@colyseus/tools` `config({ initializeGameServer })` wrapper, both became
`defineServer()`:

```diff
-import config from "@colyseus/tools";
-export default config({
-    initializeGameServer: (gameServer) => {
-        gameServer.define("my_room", MyRoom);
-    },
-    initializeExpress: (app) => {},
-});
+import { defineServer, defineRoom } from "colyseus";
+export default defineServer({
+    rooms: { my_room: defineRoom(MyRoom) },
+    express: (app) => {},
+});
```

**State callbacks.** The handler is no longer a callable wrapper around state
objects. It is an object whose methods take the collection name, or the
instance:

```diff
-import { Client, getStateCallbacks } from "colyseus.js";
-const $ = getStateCallbacks(room);
-$(room.state).players.onAdd((player, sessionId) => {
-    $(player).listen("x", (value, previous) => { /* ... */ });
+import { Client, Callbacks } from "@colyseus/sdk";
+const callbacks = Callbacks.get(room);
+callbacks.onAdd("players", (player, sessionId) => {
+    callbacks.listen(player, "x", (value, previous) => { /* ... */ });
 });
```

`callbacks.onRemove("players", fn)`, `callbacks.onChange(player, fn)`,
`callbacks.bindTo(player, sprite)`, and `callbacks.listen("phase", fn)` for a
root property all follow the same form. Every registration returns an unbind
function. `onAdd` fires immediately for items already present.

**Reconnection.** It moved out of `onLeave` into its own hooks, and the client
no longer reconnects by hand:

```diff
-async onLeave(client, consented: boolean) {
-    try {
-        if (consented) throw new Error("consented leave");
-        await this.allowReconnection(client, 20);
-    } catch (e) {
-        this.state.players.delete(client.sessionId);
-    }
-}
+onDrop(client: Client, code: number) {
+    this.allowReconnection(client, 30); // no await; the outcome routes to the hooks below
+}
+onReconnect(client: Client) { /* mark the player connected again */ }
+onLeave(client: Client, code: number) {
+    this.state.players.delete(client.sessionId); // gone for good
+}
```

```diff
-room.onLeave(async () => {
-    room = await client.reconnect(room.reconnectionToken); // new instance: re-attach everything
-});
+room.onDrop(() => showReconnectingUI());      // the SDK is already retrying
+room.onReconnect(() => hideReconnectingUI()); // same instance, callbacks intact
+room.onLeave((code) => {
+    if (code === CloseCode.FAILED_TO_RECONNECT) offerRejoin();
+});
```

`client.reconnect(token)` still exists for a page reload. It returns a new
`Room`, so re-attach callbacks in that one case.

#### How the lifecycle runs

Room: `onCreate → … → onDispose`. Per client:
`onAuth → onJoin → (onDrop → onReconnect)* → onLeave`.

1. Any non-consented close fires `onDrop` on both sides. The server calls
   `allowReconnection(client, seconds)`; the SDK retries with backoff on the
   same `room` instance.
2. Success fires `onReconnect` on both sides. The server sends a full snapshot
   that is reconciled in place: existing callbacks stay attached, `onAdd` and
   `onRemove` fire for what changed while offline, queued `room.send()` calls
   flush.
3. Timeout or denial fires `onLeave` on both sides; the client receives
   `FAILED_TO_RECONNECT` (`4003`). `onLeave` means gone for good: remove the
   player there, never in `onDrop`.

`room.leave()` (`CONSENTED`, `4000`) skips `onDrop`. A room without `onDrop`
receives every disconnect in `onLeave` and may call `allowReconnection()` there
when `code !== CloseCode.CONSENTED`.

## Step 3: the canonical 0.18 shapes

Each block ends with the reference section that documents it in full. The
`references/<file> § "Heading"` form names a heading in a bundled reference;
jump to it with `grep -n` rather than reading the whole file.

### Server

`src/index.ts`:

```ts
import { listen } from "@colyseus/tools";
import app from "./app.config.js";

listen(app);
```

`src/app.config.ts`:

```ts
import { defineServer, defineRoom } from "colyseus";
import { MyRoom } from "./rooms/MyRoom.js";

export const server = defineServer({
    rooms: {
        my_room: defineRoom(MyRoom),
    },
});

export default server;
```

The named export is what a TypeScript client imports for end-to-end types.
Reference: `references/room.md § "Defining a Room"`; server options,
transport, presence and driver: `https://docs.colyseus.io/server.md`.

### State

`src/rooms/schema/MyRoomState.ts`:

```ts
import { schema, t, type SchemaType } from "@colyseus/schema";

export const Player = schema({
    x: t.number(),
    y: t.number(),
    connected: t.boolean().default(true),
}, "Player");
export type Player = SchemaType<typeof Player>;

export const MyRoomState = schema({
    players: t.map(Player),
}, "MyRoomState");
export type MyRoomState = SchemaType<typeof MyRoomState>;
```

`schema()` returns a real class, so `new MyRoomState()` and `instanceof` both
work; the `export type` alias makes the same name usable as a type. Pass the
name argument for every structure: it is what the serializer, debug output and
code generation identify the class by. Collections start empty without a
default.
Reference: `references/schema.md § "Defining a Schema structure"`; field
types and bandwidth: `references/schema.md § "Data Types"`; per-client
filtering: `references/schema.md § "View tags"`.

### Room

`src/rooms/MyRoom.ts`:

```ts
import { Room, Client, CloseCode, validate } from "colyseus";
import { z } from "zod";
import { MyRoomState, Player } from "./schema/MyRoomState.js";

export class MyRoom extends Room {
    maxClients = 4;
    state = new MyRoomState();

    messages = {
        // validate() rejects a malformed payload before it reaches the handler
        move: validate(z.object({ x: z.number(), y: z.number() }), (client: Client, { x, y }) => {
            const player = this.state.players.get(client.sessionId);
            player.x = x;
            player.y = y;
        }),
        // return a value to answer a client's room.request()
        "get-profile": async (client: Client, { userId }: { userId: number }) => {
            return await db.profiles.findById(userId);
        },
    };

    onCreate(options: any) {}

    onJoin(client: Client, options: any) {
        this.state.players.set(client.sessionId, new Player());
    }

    onDrop(client: Client, code: CloseCode) {
        this.allowReconnection(client, 30);
        this.state.players.get(client.sessionId).connected = false;
    }

    onReconnect(client: Client) {
        this.state.players.get(client.sessionId).connected = true;
    }

    onLeave(client: Client, code: CloseCode) {
        this.state.players.delete(client.sessionId);
    }

    onDispose() {}
}
```

Reference: `references/room.md § "Message Handling"`; reconnection:
`references/room.md § "Complete Server Example"`; timers:
`references/room.md § "Clock"`.

### Client

```ts
import { Client, Callbacks, CloseCode } from "@colyseus/sdk";
import type { server } from "../../server/src/app.config.js";

// typeof server types room names, options, state and messages end to end
const client = new Client<typeof server>("http://localhost:2567");
const room = await client.joinOrCreate("my_room");

const callbacks = Callbacks.get(room);
callbacks.onAdd("players", (player, sessionId) => {
    callbacks.listen(player, "x", (x) => { /* move the sprite */ });
});
callbacks.onRemove("players", (player, sessionId) => { /* destroy the sprite */ });

room.send("move", { x: 1, y: 2 });
const profile = await room.request("get-profile", { userId: 42 });

room.onDrop(() => { /* show reconnecting UI */ });
room.onReconnect(() => { /* hide it */ });
room.onLeave((code) => {
    if (code === CloseCode.FAILED_TO_RECONNECT) { /* offer a rejoin */ }
});
```

Reference: `references/client-sdk.md § "State Sync Callbacks (Recommended)"`;
`references/client-sdk.md § "Request/Response"`;
`references/client-sdk.md § "Automatic Reconnection"`; the page-reload case:
`references/client-sdk.md § "Manual Reconnection"`.

## Step 4: where to look

Read the bundled reference before writing non-trivial code in that area. They
are the full documentation text, generated from the site, 1,200–2,200 lines
each; the section pointers above land you in the right part.

| Task | Read |
| --- | --- |
| Defining or changing synchronized state, collections, filtering | `references/schema.md` |
| Room lifecycle, messages, request/response, timers, reconnection | `references/room.md` |
| Connecting, joining, sending, state callbacks, reconnection on the client | `references/client-sdk.md` |
| Client prediction, reconciliation, lag compensation, fixed timestep | `references/netcode.md` |

Everything else is on the site, and every page is available as raw markdown by
appending `.md`:

| Topic | URL |
| --- | --- |
| Matchmaking, lobby, queue, visibility | `https://docs.colyseus.io/matchmaker.md` |
| HTTP routes: `createEndpoint`, `createRouter`, middleware, CORS | `https://docs.colyseus.io/server/http-routes.md` |
| Authentication | `https://docs.colyseus.io/auth.md` |
| Database and persistence | `https://docs.colyseus.io/database.md` |
| Server config, transport, presence, driver | `https://docs.colyseus.io/server.md` |
| Scaling out | `https://docs.colyseus.io/scalability.md` |
| Deployment | `https://docs.colyseus.io/deployment.md` |
| Colyseus Cloud | `https://docs.colyseus.io/cloud.md` |
| Unit testing with `@colyseus/testing` | `https://docs.colyseus.io/tools/unit-testing.md` |
| Playground, monitor, load testing | `https://docs.colyseus.io/tools.md` |
| Command pattern (`@colyseus/command`) | `https://docs.colyseus.io/recipes/command-pattern.md` |
| Upgrading from an earlier version | `https://docs.colyseus.io/migrating/0.18.md` |
| Full index of every page | `https://docs.colyseus.io/llms.txt` |

When a task needs a page that is neither bundled nor listed, fetch
`https://docs.colyseus.io/llms.txt` and pick from it rather than guessing a URL.

## Symptoms in an existing project

What pre-0.17 code looks like when it runs against 0.18. The silent ones are
the ones to look for.

| You see | Cause | Fix |
| --- | --- | --- |
| Players never get to reconnect; no error | `onLeave`'s second argument is a close code, so `if (!consented)` never runs | `onDrop()`, or compare `code !== CloseCode.CONSENTED` |
| Metadata fields vanish after `setMetadata({ x })` | 0.18 replaces instead of merging | Spread `this.metadata` |
| `client.id` is `undefined` | Removed | `client.sessionId` |
| `Cannot find module "colyseus.js"`, or `getStateCallbacks` is not exported | Package renamed, handler API changed | `@colyseus/sdk`, `Callbacks.get(room)` |
| Throws at schema definition mentioning `"string"` or another type name | Raw string field types | `t.string()` and friends |
| Throws at schema definition about the field count | 63-field cap, parents included | Nest a child schema |
| `Room<MyState>` no longer type-checks | The generic is an options object | Drop it and assign `state = new MyState()` |
| Playground 404 in production | Locked down in 0.18 | Pass a guard middleware via `use` |

## Working rules

- The server is authoritative. Client code must never be the only thing
  enforcing a rule; validate in the room.
- Only the server mutates `state`. Clients send messages or input and react to
  callbacks.
- Prefer the declarative `messages` map over imperative `onMessage()` calls, and
  validate payloads. Never trust a `sessionId` supplied in a message body; use
  the `client` argument the handler receives.
- Schema is for synchronized state only. Messages and request payloads are
  plain objects.
- Keep synchronized state small. It is broadcast on every patch, so anything a
  client does not need belongs outside the schema.
- After changing state structure, check the 63-field cap on every affected
  class, parents included.
- Use `this.clock.setTimeout()` and `this.clock.setInterval()`, not the
  globals; room timers are cleared on dispose.
- Remove a player in `onLeave`, never in `onDrop`; a dropped client may come
  back.
