---
name: debugging-with-ably-cli
description: >
  ALWAYS use when diagnosing Ably issues — messages not arriving, presence not
  updating, connection failures, auth errors (40101, 40142, 40160), channel
  lifecycle problems, push notification issues, Chat room issues, Spaces
  member/cursor issues, or any Ably error code. Provides Ably CLI commands to
  observe live traffic, inspect state, and simulate clients. Not for building
  new Ably integrations (use using-ably skill instead).
license: Apache-2.0
metadata:
  tags: ably, debugging, cli, realtime, presence, channels, diagnostics, errors, push
---

# Debugging with Ably CLI

The Ably CLI (`@ably/cli`, install via `npm install -g @ably/cli`) lets you observe, test, and simulate Ably operations from the terminal — faster than console.log or browser DevTools.

**Discovering commands:** Run `ably --help` for command groups, `ably <command> --help` for subcommands, flags, and examples. The CLI is self-documenting. This skill teaches **what's possible and when to use it**.

---

## 1. Diagnostic Decision Tree

```
Messages not arriving
├── Is anyone on the channel?        → list channels with a prefix filter
├── Was anything published?          → check channel history (2 min only without persistence)
├── Can I see messages live?         → subscribe to the channel
├── Test round-trip                  → subscribe in background, publish from main terminal
└── Check channel lifecycle          → subscribe to channel lifecycle logs, or inspect the channel in the dashboard

Presence not working
├── Who is actually present?         → subscribe to presence on the channel
├── Simulate a client joining        → enter presence with custom client-id and data
├── Check presence member count      → get channel occupancy
│   (stale members? ungraceful disconnects take ~15s to be removed)
└── Watch all presence events        → subscribe to logs filtered by channel.presence, or inspect the channel in the dashboard

Connection problems
├── Can I connect at all?            → test connection (try ws and xhr separately)
├── Is Ably up?                      → check service status
├── Watch connection lifecycle       → subscribe to connection lifecycle logs
└── Connection count vs plan limit   → check app stats in live mode

Auth errors
├── Is the API key valid?            → test connection with the specific key
├── What capabilities does key have? → list auth keys
├── Using tokens (JWT or Ably)?      → issue a test token via CLI to verify the key can create valid tokens
│   (CLI token issuance tests the key, not your app's authUrl/authCallback)
├── Token expired (40142)?           → check TTL and renewal config (authUrl/authCallback)
└── Look up the error code           → ask the support agent or fetch help.ably.io/error/{code}

Channel state / lifecycle issues
├── Watch channel events             → subscribe to channel lifecycle logs
├── Watch all app meta events        → subscribe to all logs
├── Check channel occupancy          → get or subscribe to occupancy
└── Check channel rules/config       → list channel rules (persistence, TLS, push, etc.)

Push notifications not working
├── Watch push delivery logs         → subscribe to push logs (meta channel)
├── Check push log history           → get push log history
├── Is push enabled on namespace?    → list channel rules, check push-enabled
└── Check integration rules          → list integrations, check source type and channel filter

Integration rules not firing
├── List all integrations            → list integrations to see rules, source types, status
├── Check source type matches        → source can be channel.message, channel.presence,
│                                      channel.lifecycle, or presence.message
├── Check channel filter             → filter pattern must match the channel name
├── Is the rule enabled?             → check integration status (enabled/disabled)
└── Check for delivery errors        → check log history — the log metachannel captures
                                       errors sending on integrations

Queue issues
├── Are queues configured?           → list queues
├── Is the integration routing to it?→ list integrations, check AMQP rule target
└── Check message flow               → subscribe to the source channel to verify messages exist

Chat room issues (@ably/chat)
├── Are messages flowing?            → subscribe to room messages
│   (if CLI sees messages but app doesn't → room.attach() likely missing)
├── Check room presence              → subscribe to room presence
├── Check occupancy                  → get room occupancy
├── Check underlying channel events  → inspect the room's channels in the dashboard, or subscribe to channel lifecycle logs and look for the room's channel names
└── Send a test message              → send a message to the room from CLI

Spaces issues (@ably/spaces)
├── Who is in the space?             → subscribe to space members
├── Watch cursors                    → subscribe to space cursors
├── Watch locations                  → subscribe to space locations
└── Check locks                      → get all locks in the space
```

---

## 2. Key Debugging Facts

- **Channel names are case-sensitive.** Mismatched names between publisher and subscriber is a common bug. List active channels to see what actually exists.
- **History defaults to 2 minutes.** Without persistence, history only covers Ably's connection recovery window. Check channel rules for `persisted: true`. If not enabled, tell the user and suggest enabling via channel rules or the dashboard.
- **Presence requires clientId AND capability.** The clientId must be set at connection time (not per-presence-enter). Entering presence requires the `presence` capability; subscribing to presence events requires `subscribe` capability. A client can observe who's present without entering itself. Without the right capability, presence operations fail with 40160.
- **Capability scope on channel names.** A key with `publish:["chat:*"]` allows publish on channels starting with `chat:` (e.g., `chat:room-1`), but NOT on a channel literally named `chat`. The colon separator and wildcard pattern matter — this is a common cause of 40160 errors.
- **Token expiry (40142).** Tokens have a TTL. If the client has no `authUrl` or `authCallback` configured for renewal, the token expires; any connection will fail and any other API requests will be refused. Test token issuance via the CLI to verify auth flow works independently of the app.
- **Presence removal delay.** Ungraceful disconnects take ~15 seconds to be removed by Ably.
- **Occupancy reveals duplicate subscriptions.** If subscriber count is much higher than expected, check for duplicate subscriptions (React StrictMode, missing useEffect cleanup, multiple Ably client instances).
- **Token vs key capabilities.** Keys and tokens issued from them can have different capabilities; the rights of a token is the intersection between the rights of the key, and the specific rights specified in the token. Debug 40160 errors by checking both the key capabilities AND the token creation code on the server.
- **Metachannel logs require `[meta]*` capability.** All `ably logs` commands subscribe to logs metachannels (`[meta]log`, `[meta]channel.lifecycle`, etc.). A key scoped to `*` does not match metachannels — the key needs `[meta]*` or `[*]*` in its capability resource list. The app's root API key has `[*]*` by default. If `ably logs` commands fail with 40160, check the key's capability scope. For deep inspection of a single channel (per-channel stats, regional breakdown, attached integrations), use `ably channels inspect <channel>` to open the dashboard's channel inspector — this uses privileged inspection metachannels (`[meta]inspect:*`) not currently available to the CLI.
- **Transport fallback.** If WebSocket is blocked, the SDK falls back to XHR streaming. Test both transports separately to confirm which works.
- **Non-default environments.** If the app uses a sandbox or custom environment, log in with `ably accounts login --endpoint <host>` to target the right cluster.
- **Error message text > error code.** Ably error codes are broad categories (e.g., 40000 covers many variants). Always read the error message text for the specific cause. Every code has a help page at `help.ably.io/error/{code}`, or use `ably support ask "error {code}"`.

---

## 3. CLI Authentication

The CLI needs credentials. Two approaches:

**Credentials from the project (quick, no login):**
Set `ABLY_API_KEY` as an environment variable. Find the key from the project's environment files and export it (e.g. `export ABLY_API_KEY=...`). Alternatively, if you have a token (e.g., from the app's auth server), use `ABLY_TOKEN` instead. If the key is for a production app, note this to the user before using it.

**Log in to the CLI (for extended debugging or account-level commands):**
`ably login` opens a browser for OAuth. Once logged in, use `ably apps list` and `ably apps switch` to target the right app, and `ably auth keys list` to see available keys and their capabilities.

If no credentials are available, ask the user to check that their Ably environment variables are set (e.g. `ABLY_API_KEY`) or to run `ably login` to authenticate.

---

## 4. What the CLI Can Do

### Observe (Read-Only)

Subscribe to channels, presence, occupancy, logs, and stats in real time — you see exactly what Ably sees.

- **Channel messages**: Subscribe to one or more channels. Supports wildcards and rewind (replay recent messages on attach).
- **Presence**: Watch who enters and leaves, with their client IDs and data payloads.
- **Occupancy**: Snapshot or live stream of publishers, subscribers, and presence members on a channel.
- **Logs (meta channels)**: Channel lifecycle, connection lifecycle, presence events, and push notification delivery logs. Filter by type (`channel.lifecycle`, `channel.occupancy`, `channel.presence`, `connection.lifecycle`, `push.publish`), rewind to catch recent events.
- **Push notification logs**: Dedicated push log stream and history — see delivery attempts, failures, and device targeting.
- **History**: Past messages on a channel (2 minutes without persistence — see Key Debugging Facts).
- **Stats**: App or account statistics with a live polling mode. Check connection counts against plan limits.
- **Channel list**: Currently active channels with prefix filtering.
- **Connection test**: Verify connectivity across transports (WebSocket, XHR) to isolate network or proxy issues.

### Simulate

Act as a participant — simulate one end of a conversation to test the other (client when debugging server, server when debugging client).

- **Publish**: Send messages with event names, JSON, or plain text. Publish repeatedly with configurable count and delay to simulate traffic.
- **Batch publish**: Publish to multiple channels in a single request.
- **Presence enter**: Join a channel with custom client ID and data (e.g., `{"role": "server"}`).
- **Chat**: Full room simulation — messages, presence, typing, reactions.
- **Spaces**: Members, cursors, locations, locks.
- **Benchmarking**: Publisher/subscriber throughput and latency testing with configurable rates and message sizes.

### Manage

Query and modify app configuration to diagnose config-related issues.

- **Channel rules (namespaces)**: Check and configure persistence, push, TLS-only, batching, conflation, and channel registry settings.
- **API keys**: List capabilities, create, revoke, switch active key.
- **Token issuance**: Issue JWTs (or Ably tokens if the app uses these) to test auth flows in isolation. Also revoke tokens.
- **Apps**: List, create, switch, configure.
- **Integrations**: List and inspect integration rules — webhooks, Lambda, Kafka, AMQP, and others. Check source types (channel.message, channel.presence, channel.lifecycle, presence.message), channel filters, and enabled/disabled status.
- **Queues**: List, create, and delete Ably message queues.

### Get Help

- **AI support agent** (powered by Inkeep): `ably support ask "your question"` — searches Ably docs and FAQs. Use `--continue` for follow-ups.
- **Service status**: `ably status` checks platform health.

---

## 5. Long-Running Commands

Many commands (`subscribe`, `presence enter`, `stats --live`, `occupancy subscribe`) are long-running — they stream output until Ctrl+C or `--duration N` expires. **Run these as background tasks** so they don't block your workflow. Start a subscribe in the background, reproduce the issue, then check the output.

---

## 6. Connection and Channel State Reference

### Connection States

| State | Meaning | Diagnostic |
|-------|---------|-----------|
| `connecting` | Attempting connection | Normal on startup; if stuck, check network/auth |
| `connected` | Active WebSocket | Healthy |
| `disconnected` | Temporary loss, SDK retries | Transient is normal; recurring = network issues → watch connection lifecycle logs |
| `suspended` | Offline >2 min, less frequent retries | Test connection to check connectivity |
| `failed` | Permanent failure, SDK won't retry | Almost always auth — test with the specific API key |
| `closed` | Explicitly closed by code | Search for `.close()` calls |

### Channel States

| State | Meaning | Diagnostic |
|-------|---------|-----------|
| `initialized` | Channel object created, not yet attached | Normal before first subscribe/publish |
| `attaching` | Requesting attach from server | If stuck, check connection state and auth capabilities |
| `attached` | Active — messages flowing | Healthy |
| `detaching` | Requesting detach | Normal during cleanup |
| `detached` | Not attached, no messages flowing | Check if `detach()` was called intentionally |
| `suspended` | Attach failed, will retry | Usually follows connection suspension — check connection state first |
| `failed` | Permanent channel failure | Often capability denied (40160) or invalid channel name |

---

## 7. Environment-Specific Gotchas

| Environment | Symptom | Root Cause | Diagnostic |
|-------------|---------|-----------|-----------|
| Next.js SSR | Connection fails during render | No WebSocket in server-side render | Guard with `typeof window` or `useEffect` |
| Serverless (Lambda, Edge) | Stale/frozen connections | Connection frozen between invocations | Use `Ably.Rest` server-side |
| React StrictMode | Duplicate messages, presence flicker | Double-render duplicates subscriptions | Check occupancy — much higher than expected = duplicates |
| CSP headers | WebSocket blocked | Ably domains not in `connect-src` | Test connection — ws fails, xhr works = CSP |
| Corporate proxy | WebSocket fails silently | Proxy blocking upgrade | Test connection — ws fails, xhr works = proxy |
| Mobile background | Messages missed after resume | OS kills WebSocket | Check channel history for messages sent during gap |
