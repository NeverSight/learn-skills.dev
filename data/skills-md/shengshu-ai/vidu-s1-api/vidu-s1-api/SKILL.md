---
name: vidu-s1-api
description: >-
  Integrate the Vidu S1 real-time interactive digital-human (数字人)
  streaming video API. Use this whenever the user is building against Vidu's
  live avatar service — creating a live session, joining the Aliyun RTC channel,
  driving the control WebSocket, handling NOT_READY retries, heartbeats, hangups,
  billing, or voice cloning. Trigger on mentions of Vidu S1, vidu live API,
  数字人接入, /live/v1/lives, conn_init, live_bot, or "接入 vidu 实时数字人".
  Encodes the non-obvious protocol gotchas that the public doc gets wrong.
---

# Vidu S1 Live API Integration

Vidu S1 is a streaming, real-time, two-way interactive
digital-human video service. You create a "live session", the media flows over an
**Aliyun RTC** channel (not HTTP), and a persistent **WebSocket** carries control
signaling (start / hangup). This skill encodes the end-to-end flow and — more
importantly — the field-tested pitfalls, several of which contradict the public
doc. When the doc and this skill disagree, **this skill wins** (it reflects
vendor clarifications).

## Before you write any code

Establish these with the user. They are prerequisites, not code:

1. **API Key** from https://platform.vidu.cn/api-keys. Users may store it as either
   `vda_xxx` or `Token vda_xxx`, but every Vidu HTTP/WS request must send
   `Authorization: Token vda_xxx`. Placeholder values like `vda_your_api_key_here`
   are not configured keys.
2. **Avatar image** — a single-person image, as a public URL or base64 data URI.
3. **Persona text** — a free-form description of who the digital human is.
4. **Aliyun RTC SDK** — must be downloaded and integrated separately; media does
   NOT come over HTTP. SDK: https://help.aliyun.com/zh/live/introduction-to-real-time-audio-and-video-artc-sdk
5. **Host domain** — `api.vidu.cn` (China) or `api.vidu.com` (overseas). The doc
   writes `{host}` as a placeholder; always substitute a real domain.

## The 6-step flow

```
1. POST /live/v1/lives          → create session, get live_id + RTC credentials
2. Aliyun RTC joinChannel        → publish your mic (+cam for video), subscribe to the bot
3. WebSocket connect + conn_init → announce "I'm ready"
4. Wait for conn_init_ack        → success:true means the bot is live (billing starts here)
5. Interaction                   → keep the heartbeat alive, handle forced hangup
6. Hangup + leaveChannel         → send hangup, close WS, leave RTC, optionally query the bill
```

Read `references/api-reference.md` for exact request/response schemas, error codes,
and pricing. Read `references/websocket-protocol.md` for the WS message envelope,
message types, heartbeat rules, and every hangup reason. Read `references/voices.md`
for the system voice list.

### Step 1 — Create the session

`POST https://{host}/live/v1/lives` with the avatar block. You get back a `live`
object (save `live.id` — every later step needs it) and an `rtc` object (credentials
for step 2). The session starts in `status: waiting`.

### Step 2 — Join the Aliyun RTC channel

Use `rtc.token` and `rtc.user_id` to `joinChannel`. Some Aliyun RTC Web SDK
versions accept the single token form, while others require an auth-info object
such as `{ appId, channelId, userId, token, timestamp }` built from the `rtc`
response. If join fails, check the SDK version's expected `joinChannel` signature
before changing Vidu credentials. Then:
- **Publish your microphone** — required, or the digital human can't hear the user.
- **Publish your camera** — only in `video` mode.
- **Subscribe to the digital-human media stream** — usually
  `live-bot-{creatorID}-{liveID}`, but treat `live-video-push-{creatorID}-{liveID}`
  as a valid media source too.

Role → RTC user-id format:

| Role | user id |
|---|---|
| User (you) | `live-user-{creatorID}-{liveID}` |
| Digital human (bot) | `live-bot-{creatorID}-{liveID}` |
| Video push | `live-video-push-{creatorID}-{liveID}` |

### Step 3–4 — WebSocket + conn_init handshake

Connect to `wss://{host}/live/ws/live/connect?live_id={live_id}` with the
`Authorization: Token vda_xxx` **header**. Immediately send a `conn_init` message,
then wait for `conn_init_ack`:
- `success: true` → the bot is live. **Billing starts now.**
- `success: false, error_code: NOT_READY` → **expected in video mode.** Close the WS,
  wait, reconnect, retry with exponential backoff (2s → 4s → 8s). This is not an error.
  Ignore close/message events from the socket you intentionally closed for this retry.
- `success: false, error_code: LIVE_CONN_INIT_FAILED` → fatal. Go back to step 1 and
  create a new session.

### Step 5 — Stay alive and handle hangups

The server pings every 5s; your client must send *any* message within 15s or it's
dropped as a dead connection. Most WS libraries auto-reply to pings — confirm yours
is enabled on the actual upstream Vidu connection. In a browser → backend proxy →
Vidu design, this means the backend WS client must reply to Vidu pings. Listen for
a `type:6` hangup message, **and** add a fallback listener on the WS's abnormal-close
event, because the server can drop you without a clean message.

### Step 6 — End the call

Send a `hangup` message over the WS, close the WS, then call the RTC SDK's
`leaveChannel()`. Optionally `GET /live/v1/lives/{live_id}` to read the bill
(`billed_seconds`, `credits_cost`).

## Pitfalls (read before implementing — these override the doc)

These are field-tested integration gotchas.

1. **Do not assume a fixed `live_duration`.**
   It is returned by the create API and may vary by the current service policy
   (real responses have returned `7200`). Treat the returned positive integer as
   authoritative and design the UX around that session-specific cap.

2. **Use `rtc.token_expire_at`; do not assume a fixed token lifetime.**
   Treat the token as valid for its live session only. Don't cache/reuse it across
   sessions — get fresh credentials from step 1 each time. If it expires, create a
   new session.

3. **WebSocket auth uses the `Authorization: Token vda_xxx` header — query params are
   NOT supported.** Browsers cannot set custom `Authorization` headers on native
   WebSocket connections, and the header carries your raw Vidu token, so **proxy the
   WebSocket through your own server**. Same applies to HTTP calls: never ship
   `vda_xxx` to untrusted clients.

4. **`video` mode WILL return `NOT_READY` on first connect — always.** This is the SIP
   side warming up, not a failure. You must implement the disconnect → backoff →
   reconnect loop, or video mode will appear broken.

5. **Aliyun RTC is a separate SDK integration, not an HTTP call.** Budget for
   downloading and wiring up the ARTC SDK. Forgetting this is the most common
   "why can't I see/hear the avatar" bug.

6. **Do not combine SDK auto-subscribe with repeated manual subscribe.** Disable
   default remote auto-subscribe when manually selecting the bot/media user, and
   dedupe in-flight/completed subscribe and view-attachment work. Multiple RTC events
   can announce the same media user and otherwise look like duplicate streams or lag.

7. **Guard against stale RTC and WS events.** A previous RTC session or upstream WS can
   still emit late events after a retry, hangup, or new session. Ignore events unless
   they belong to the currently active RTC session/socket, or they can corrupt the new
   session's status, subscription state, or video view binding.

8. **Billing starts at `on_live`** (the moment `conn_init_ack` returns `success:true`),
   not at session creation. Duration rounds *up* to even seconds (11s bills as 12s).
   The account needs a **minimum ~45 credits** (enough for 30s) to start a session;
   mid-session it keeps deducting and auto-disconnects when credits hit zero.

9. **Audio and audio+video modes are priced identically** right now — mode choice is a
   product decision, not a cost lever.

10. **The GET session response top-level shape is stable: `{ "live": { ... } }`.** Parse
   `live.id`, `live.status`, `live.billed_seconds` off that wrapper — don't expect the
   fields at the root.

11. **`GET /live/v1/voices` returns ONLY custom cloned voices, by design.** The system
   voice list is separate — see `references/voices.md`. Don't treat an "empty" voices
   response as an error; it just means no custom clones yet.

## Voice selection

Default voice is `Tina`. Pass `avatar.voice` to pick another. System voices and their
supported languages are in `references/voices.md`. To clone a voice, `POST
/live/v1/voices/clone` (see `references/api-reference.md`); first 10 clones per user
are free, then 899 credits each.
