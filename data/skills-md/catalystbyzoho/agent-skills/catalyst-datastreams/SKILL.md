---
name: catalyst-datastreams
description: "Catalyst Data Streams — real-time publish/subscribe channels over WebSocket. Publish from a function with publishData / publish_data, issue a token pair with getTokenPair / get_token_pair, subscribe with DataStreamsWebSocket / ZCDataStreamsWebSocket (Node.js, browser, Java, Python), sendAck, live/earliest/resume subscribe types, 48-hour retention, User Roles vs Custom Logic access control. Trigger on 'Data Streams', 'datastreams', 'real-time channel', 'live updates', 'pub/sub', 'WebSocket subscriber', 'token pair', 'wss-id', 'app_user_id is missing', 'Invalid access control source', 'Authentication failed 3000', '@zcatalyst/datastreams', or 'zcatalyst_sdk.datastreams'."
metadata:
  version: "2.0.0"
---

## How It Works

1. **Channels and access control are console-only.** Create the channel and choose its access control in Console → Cloud Scale → Data Streams; no SDK, REST, or MCP tool creates channels. Ask the user for the channel ID and its access control type, or list channels with `getAllChannels()` (`control_type` 0 = User Roles, 1 = Custom Logic). Load `references/datastreams-basics.md` for concepts, the token rules, subscribe types, acknowledgement, and the REST API.

2. **Pick the token identifier from the access control — it is not interchangeable.**
   - **User Roles** → `userId` = an app user's ID from Catalyst Authentication. A console admin's user ID is rejected; `connectionName` fails with "Mandatory parameter app_user_id is missing."
   - **Custom Logic** → `connectionName`, and the token must be generated **inside the Advanced I/O function selected as the channel's access control**. That function is the token endpoint: it runs your check, then calls `getTokenPair`. Catalyst never calls it on its own. From any other function or REST: "Invalid access control source!". User-ID tokens on these channels are issued but the WebSocket rejects them (`3000`).

3. **Server code (publish, token pair, channel reads) — load the runtime reference.**
   - Node.js / JavaScript → `references/datastreams-javascript-basics.md`. Initialize with the app: `new DataStreams(await zcAuth.init(req))`. Advanced I/O handlers get Node's raw `req`/`res`: no `req.body`, `res.status()`, or `res.json()`.
   - Python → `references/datastreams-python-basics.md`. Requires `zcatalyst-sdk` 1.5.0+ (Python 3.10+). `app = zcatalyst_sdk.initialize(req=request)`, then `app.datastreams()` (plural). Pass `get_token_pair` a **string** channel ID and a keyword `user_id=` / `connection_name=`; the result's keys are hyphenated (`token["wss-id"]`). The subscriber does nothing until `connect()`.
   - Java → `references/datastreams-java-basics.md`. Dependency is `com.zoho.catalyst:java-sdk` (2.5.0+) from `https://maven.zohodl.com`; no `datastreams` artifact exists.
   - `publishData`, `getAllChannels`, `getChannelDetails` and `getLiveCount` are **admin** methods: server only, never in browser or mobile code. `getTokenPair` also exists in the browser SDK, but a Custom Logic token must come from the configured function.

4. **Subscriber code — read the token correctly and always acknowledge.** The token pair's keys are hyphenated: pass `token['wss-id']` as `zuid`, plus `token.url` and `token.key`. Subscribe only after the `open` event. Call `sendAck()` after every message, or the next message is never delivered. Messages carry `data` (always a string) and `streamingId` (plus `url`/`method` on API-operation messages). To reconnect, release the old session (old token → `unsubscribe()`), take a fresh token, `subscribe('0')`, and reload state from your own store; resuming a dropped session with `'-2'` redelivers missed messages twice and replays the 48-hour retention. Unsubscribe before every deliberate close; the `error` event with code `1000` that follows your own `unsubscribe()` is expected. In Node, `getLiveCount()` returns `{ status, data: { connections } }`. Java: `subscribe()` throws the checked `ZCDataStreamException`, and outside a Catalyst function create the client with `new ZCDataStreamsWebSocket(config)`, not `ZCDatastream.getInstance()`.

5. **Verify end to end before reporting success.** Open a subscriber, check `getLiveCount()` shows it, publish a test message, and confirm the subscriber received it. For anything the references do not cover, fetch the page under <https://docs.catalyst.zoho.com/en/cloud-scale/help/data-streams/> as Markdown (`<page-url>/index.md`), and prefer the references where they disagree.

## Security Checklist

- `publishData` and the channel-read methods are admin operations: run them only in a Catalyst function, never in a browser or mobile app.
- Protect the token endpoint. Anyone who can call it can subscribe to the channel, so authenticate the caller before issuing a token.
- On Custom Logic channels, the configured function is the only gatekeeper: put the real validation there before calling `getTokenPair`.
- Do not log or return the token `key` anywhere except to the client that asked for it.

## Triggers

Use this skill for: "Data Streams", "Catalyst Data Streams", "datastreams", "real-time channel", "live updates", "push updates to the browser", "pub/sub", "publish data", `publishData`, `getTokenPair`, "token pair", "wss-id", `DataStreamsWebSocket`, `ZCDataStreamsWebSocket`, `ZCDatastream`, "WebSocket subscriber", `sendAck`, "subscribe type", "resume from last message", "live count", `getLiveCount`, "channel access control", "User Roles channel", "Custom Logic channel", "app_user_id is missing", "Invalid access control source", "Authentication failed 3000", "reconnect", "duplicate messages after reconnect", "DUPLICATE_VALUE", `@zcatalyst/datastreams`, `zcatalyst_sdk`, `get_token_pair`, `publish_data`, `send_ack`, or "Data Streams Python".

## References

| Reference | Load when the query is about… |
|-----------|-------------------------------|
| `references/datastreams-basics.md` | Concepts, channels, access control (User Roles vs Custom Logic), which token identifier to use, token pair shape, subscribe types, acknowledgement, retention, message fields, REST API endpoints and scopes |
| `references/datastreams-javascript-basics.md` | Node.js functions (init, publish, token endpoint, Custom Logic function, channel reads), Node and browser subscribers, package versions |
| `references/datastreams-python-basics.md` | Python functions and subscribers: `zcatalyst-sdk` 1.5.0+, `app.datastreams()`, `get_token_pair` argument rules, `DataStreamsWebSocket` with `connect()` and `set_on_*` callbacks, deploying Python functions |
| `references/datastreams-java-basics.md` | Java functions and subscribers: Maven setup, `ZCDatastream`, `ZCDataStreamsWebSocket`, checked exceptions, running outside Catalyst |
