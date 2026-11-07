---
name: opencode-mesh
description: >
  Load this skill immediately when asked to use mesh,
  message/contact/communicate with another opencode session, discover peers, or
  explain mesh config/settings/how-it-works to user. Run mesh_peers first, then
  mesh_send to exactly one peer with body-only text; replies arrive as normal
  messages, reply by reverse send.
---

# OpenCode-Mesh

Message any session in 2 calls: peers first, exact target only. Run `mesh_peers`
to discover live peers, then `mesh_send` body-only text.

## Use it

1. Run `mesh_peers({})` and pick the top-ranked live target.
2. Send `mesh_send({target:"<exact ses_id | agent@repo>", text:"<body only>"})`;
   keep the `msg_` receipt.
3. Read the reply as a normal message; reply by reverse `mesh_send` to the
   sender id.

## Answers

1. Reach any session in 2 calls: `mesh_peers` discovers, `mesh_send` delivers,
   replies arrive as normal messages.
2. Never call `mesh_register` by hand: every open session is auto-registered;
   call only to set a custom description.
3. Never type the `[OC-MESH | SENDER: {agent} - {sessionID}]` header yourself:
   the system prepends exactly one; send body text only.
4. Sends inject one at a time per process over per-target FIFO; overflow past
   depth cap 100 rejects newest with `STORAGE_FULL`.
5. Find peers in the ranked union; target an exact id or singleton `agent@repo`,
   else 404 `PEER_NOT_FOUND` plus `didYouMean[0..5]` with nothing sent.
6. Freshness windows are heartbeat 5m, active 10m, subagent 30m, primary 48h,
   outbox 10m bound; attach is `ps`-detected with focus unknown.
7. Triple 1MB guard refuses with 413 `PAYLOAD_TOO_LARGE` at entry, prefixed, and
   body sites.
8. Wake is default: each message starts a Runner turn unless silent deposits
   history-only marked `(SILENT)`.
9. Stay quiet per message with `silent:true` (legacy `noReply:true`) or silence
   everything with `MESH_WAKE=0`.
10. Bodies pass verbatim by default; opt in with `MESH_QUARANTINE=1` to tag
    non-leading lookalikes.

## Fix it fast

- Run `mesh_peers` before every `mesh_send`; stale ids miss with 404 and send
  nothing.
- Track any send via `mesh_peers({receipt:"msg_…"})` for queued versus injected
  versus terminal state.
- On 404 read `didYouMean[0..5]`, re-run `mesh_peers`, resend to the exact id.
- History-only delivery needs `silent:true` per message or `MESH_WAKE=0` global;
  wake is default.
- Never hand-write header lookalikes mid-text: verbatim default passes them
  through, `MESH_QUARANTINE=1` tags them.
- Oversize text fails 413 before any send or queue; shrink `text` and retry.
- Fan-out stays off by default: `broadcast:true` or target `all` needs exact
  `MESH_BROADCAST=1` else 403 `BROADCAST_DISABLED`; prefer peer-to-peer.
- Keep pasted transcripts under `/tmp` roots free of passwords, tokens, and
  registry dumps.
- Loopback-only wire `127.0.0.1:4096`, dirs `0700` files `0600`, `Basic` via
  `OPENCODE_SERVER_PASSWORD`.

## Shapes

Run exact shapes only; no extra keys.

| Tool             | Required         | Optional                                                        |
| ---------------- | ---------------- | --------------------------------------------------------------- |
| `mesh_send`      | `target`, `text` | `silent`, `noReply` (legacy), `broadcast`                       |
| `mesh_peers`     | none             | `includeSelf`, `agent`, `description`, `cwd`, `repo`, `receipt` |
| `mesh_register`  | none             | `summary`, `description` (alias)                                |
| `mesh_broadcast` | `text`           | `silent`, `noReply` (legacy)                                    |

`mesh_register` upserts caller presence; returns registry snapshot, not ranked
union. `mesh_broadcast` aliases `mesh_send` with fixed `target all` plus
`broadcast true`.

Track queued rows by `id` via `mesh_peers({ receipt: "msg_…" })`; CLI carries no
receipt flag.

| State                  | Meaning                                                |
| ---------------------- | ------------------------------------------------------ |
| `queued`               | Row exists, inject pending                             |
| `injected-progressing` | 204 seen, reader unconfirmed                           |
| `dead-lettered`        | Max attempts plus past TTL                             |
| `failed-permanent`     | Terminal `fail_reason`, no such row, store unavailable |

Terminal check runs first; `fail_reason` wins over claimed or delivered. Send
shape stays `{ok, via, target, title, id}`; `via` reads `admitted`, `queued`, or
`mixed` on broadcast.

Wake is default; silent deposits history-only marked `(SILENT)`.

| Input                                     | Wire                                        |
| ----------------------------------------- | ------------------------------------------- |
| `MESH_WAKE=0`                             | `noReply true`, wins over per-message flags |
| `silent true`                             | `noReply true`                              |
| `noReply true` (legacy, `silent` omitted) | `noReply true`                              |
| Wake (omit both, `MESH_WAKE` unset)       | Omit `noReply` key                          |

Tool spells `silent`; CLI spells `--no-reply` with no `--silent` flag. Row
`silent 1` pins `noReply` on claim inject; row `0` wakes.

Send body-only text; never hand-write headers or wire keys. Direct POSTs
`agent`, `parts`, `messageID`, `model`, optional `variant`, plus `noReply`
spread to `/session/{id}/prompt_async?directory=`. Claim injects the same keys.
Loopback `127.0.0.1:4096` only; `Basic` header when password set, omitted when
unset; `x-opencode-directory` carries target scope.

## Internals

Claimer polls every 2s; claims own rows only, oldest first. Store runs WAL plus
`busy_timeout 5000` plus `synchronous FULL`. Crash rows release; clean shutdown
releases owned claims; success acks, failure releases. Presence auto-registers
on first touch; debounce one grace window; dispose deletes own ids only. Entry
sync keeps `description` plus `summary` in sync, `directory` plus `cwd` in sync,
derives `repo` from basename, falls back `title` to `description`, strips
`daemon` plus `serveUrl` plus `servePort` plus rank keys. Registry runs atomic
writes with cross-process lock; contention degrades, validation stays loud.

Wire carries receiver `agent` plus `model` as observed; never synthesize.
Slash-less model takes `opencode` prefix; absent token throws at parser,
resolves null at resolver. Precedence reads live, direct row, DB, registry; miss
reads null. Miss reasons read `live-throw`, `live-miss-parse`,
`direct-fetch-miss`, `direct-parse-fail`, `db-throw`, `db-row-absent`,
`db-parse-fail`, `registry-absent`, `registry-unknown-agent`,
`registry-no-model`. Unresolvable defers honestly: direct leg queues, claim leg
releases for redelivery.

Peers read join of DB existence plus registry overlay plus live confirmation.
Each id carries one `liveSource`: `status`, `heartbeat-recent`, `db-truth`,
`stale`. Null or empty view deletes zero; degraded reads registry-only. Rank
orders attach-first, directory, agent, busy plus recency, title; misses rank
last, never hides. Pick rank 1 first; `status` means send now, `stale` means
re-check first.

Password absent means no header; `port.auth` reads `none`. Env password wins;
Keychain runs only behind exact `OPENCODE_MESH_KEYCHAIN_PROVIDER=1`. Keychain
tries `/usr/bin/security` first with 5m cache, then `secret-tool lookup` on
Linux; `USER` sanitized to safe chars, miss sends no header. Default user reads `opencode`; `OPENCODE_SERVER_USERNAME`
overrides username only. Keep pasted transcripts under `/tmp` roots free of
passwords, tokens, registry dumps.

## V2 notes

V1 sections above apply unchanged; tool shapes, workflow, receipts, and
limits are identical. Only the wire underneath differs.

- Delivery posts `{text, delivery}` to `/api/session/:sessionID/prompt`
  instead of the V1 `prompt_async` envelope. Prefix text, bubbles, and the
  steer on wake versus queue on silent mapping behave the same.
- The loopback pin `127.0.0.1:4096` is the default only. V2 servers listen
  on their own ports, probed in order; set `MESH_ENUM_PORTS` to override.
- `attached` stays `ps`-detected. Serve-hosted sessions never attach; they
  read live through status and database truth instead.
- `via:admitted` means any 2xx. V1 answers 204 with no body, V2 answers
  200 with a body.
- After a server restart, live sessions rejoin within about one tick and
  queued rows deliver with no manual touch. Wait and re-check peers rather
  than re-registering by hand.

## Full docs

- Install:
  https://github.com/divisionseven/opencode-mesh/blob/main/docs/getting-started.md#section-2-install
- Settings and limits:
  https://github.com/divisionseven/opencode-mesh/blob/main/docs/getting-started.md#section-8-authentication
- Fixes:
  https://github.com/divisionseven/opencode-mesh/blob/main/docs/troubleshooting.md
- Wire proof:
  https://github.com/divisionseven/opencode-mesh/blob/main/ARCHITECTURE.md
- Send proof:
  https://github.com/divisionseven/opencode-mesh/blob/main/src/tools/mesh_send.ts
- Peers proof:
  https://github.com/divisionseven/opencode-mesh/blob/main/src/tools/mesh_peers.ts
- Header proof:
  https://github.com/divisionseven/opencode-mesh/blob/main/src/frontmatter.ts
- Silent proof:
  https://github.com/divisionseven/opencode-mesh/blob/main/src/wake.ts
- Limits proof:
  https://github.com/divisionseven/opencode-mesh/blob/main/src/constants.ts
- Read the linked shipped page for detail before quoting limits or TTLs.
- Send shape is `{ok, via, target, title, id}`; `via` is `admitted` on 204 (NOT
  delivered, NOT read) or `queued` with a row id.
