---
name: digital-signage
description: >
  Build a digital-signage module in a Next.js App Router app: an ad media
  library, per-screen playlists, a display registry, device pairing and a
  fullscreen TV player. Use when: (1) building or extending in-venue screens,
  digital menu boards, lobby or waiting-room displays, or an advertising-slot
  system, (2) implementing playlist scheduling, media upload with duration and
  orientation handling, device pairing by PIN or provisioning URL, screen
  health monitoring, or remote screen control, (3) auditing a player that
  freezes, never refreshes or shows portrait media sideways, (4) the user
  mentions: digital signage, display screens, TV player, ad playlist, signage
  module, kiosk display, screen management, proof of play, /api/display/pair,
  /api/display/playlist, ETag, 304 Not Modified, SIGNAGE_TOKEN_PEPPER, wake
  lock, video stall, firebase-admin, Supabase RLS. Carries player internals that recover from video
  stalls, rotate for portrait screens and survive TV-browser quirks, and a data and auth model with hashed
  per-device tokens and venue-scoped playlists, each pinned by a behaviour contract or a route test.
  Next.js App Router; the data layer is a seam, with Firestore and Supabase/Postgres both carried. Not web
  ad serving and not an interactive kiosk.
---

# Digital Signage: Displays and Ads

A screen in a venue is not a web page. It runs unattended for months on a cheap
TV stick, nobody is watching the console, and the failure mode is a frozen frame
that no one notices for a week. Every decision below exists to survive that.

This skill carries a complete module: admin CRUD for media and playlists, a
display registry, PIN and provisioning-URL pairing, a fullscreen player, and the
operational layer (health, preview, remote control) that makes it manageable.

## When to use

Building or extending screens that loop media in a physical space, on Next.js
App Router with Firestore or Supabase/Postgres.

## When NOT to use

- **Web ad serving** (impressions, bidding, tracking pixels, third-party tags):
  a different problem with different infrastructure.
- **Interactive kiosks** where the user taps to transact. Signage is one-way.
- **A single embedded video** on a marketing page. Use a `<video>` tag.
- Generic Next.js, CMS, or auth setup, which is assumed to exist.

## Architecture

```
 ADMIN (browser)                     SERVER                      DEVICE (TV)
 ---------------                     ------                      -----------
 media upload ---------------> object storage <---- public/signed URL --+
 ad CRUD ---------+                                                     |
 playlist edit ---+--> /api/admin/*  --> ads + displays --+             |
 issue command ---+      (staff auth)      (scoped)       |             |
                                                          v             |
 pair screen <----- PIN -----------> /api/display/pair    |             |
                                     mints per-display    |             |
                                     token                v             |
                                    /api/display/playlist <--- poll ----+
                                     ^ resolves adIds to ads            |
                                     +-- carries telemetry up,          |
                                         commands down            player loop
```

One request type sustains the whole runtime: the device polls
`/api/display/playlist`, sending telemetry up and receiving content and commands
down. Everything operational rides that channel.

## Critical facts

1. **The playlist is an ordered array on the display, not a separate entity.** `display.adIds: string[]`
   *is* the playlist: order is free, no joins, one read. Introduce a standalone playlist entity only when the
   same content must run on several screens; see [data-model.md](references/data-model.md) for the trade-off
   and [extensions.md](references/extensions.md) for the migration.
2. **Poll; do not stream.** A 30 to 60 s poll is cheaper, survives sleeping network stacks, and reconnects
   for free. Realtime is an optional upgrade, not the baseline. Cache the response with an ETag or you pay
   for a full read per screen per poll.
3. **Media uploads go from the browser straight to storage**, never through an API route. Route handlers
   have body-size limits and burn compute proxying bytes.
4. **The device is untrusted and unattended.** It holds a long-lived credential in `localStorage` on hardware
   anyone can walk up to. That credential must be per-screen and revocable.
5. **The player must never be able to stop.** Every media element gets a timeout, an error handler, and a
   way to skip. A broken asset advances; it does not wedge.

## Hard rules

> **Never style a device component through the host's CSS pipeline.** Use inline styles: TV browsers run years
> behind current, and a stylesheet or purge step must not be able to break a screen nobody is watching.

> **Never derive the poll interval from render state.** Poll on a stable interval and read slide state from a
> ref. A timer whose effect depends on the slide index is recreated on every slide, so a refresh longer than a
> slide would never fire; the behaviour contract pins the poll to wall-clock time.

> **Never issue one shared token to every screen.** Mint a per-display token at pairing, store only its hash,
> and make revocation a single row update.

> **Never trust a client-supplied tenant/location scope.** Derive it server-side from the staff session or the
> display row the token resolves to, never from a header, cookie, query parameter or default venue, and
> enforce it on every `[id]` route, returning **404, not 403**, so ids cannot be probed.

> **Never overload one boolean as both "paused" and "deleted".** Use `active` for operator intent and a
> separate `deletedAt` for lifecycle, or a deleted item reappears the moment someone toggles it back on.

> **Never start an image's duration timer before `onLoad`.** On a slow TV the slide will otherwise expire
> before it is visible.

> **Never carry durable screen state in a one-shot command.** Deliver blank and takeover as `mode` on every
> poll so they survive the daily reload and a power cycle; keep the ack-cleared channel for one-shots like
> reload, and persist a reload's ack **before** reloading, or the server re-delivers it forever.

## Quick start

0. Fill in the seam contract and confirm the domain rename: [adaptation.md](references/adaptation.md). An app
   with no staff auth, venues or PIN gets them built for real on its backend, as that file says: never a demo
   venue, a default PIN, a placeholder secret or fallback data for an unreachable database. A missing
   variable fails when its route runs, not at build. The package registry is not an external service:
   `npm install` what the templates import (`zod`, the backend's SDK, `vitest`), never a hand-written client.
   Every code block is a template: write it to the path its first line names, changing only the renames
   adaptation.md allows. A template you think is wrong is reported in your closing summary, not rewritten.
1. Model the entities and pick array or junction table: [data-model.md](references/data-model.md).
2. Create tables or collections, indexes, security rules and the media bucket:
   [firestore-backend.md](references/firestore-backend.md) or
   [supabase-backend.md](references/supabase-backend.md).
3. Build the device and admin endpoints, one route file per row of the route table and never a catch-all
   route, with pairing and token verification: [api-routes.md](references/api-routes.md).
4. Get a screen paired with [pairing.md](references/pairing.md), then drop in the player loop from
   [player-runtime.md](references/player-runtime.md).
5. Build the back-office (media library, display list, playlist editor) from
   [admin-ui.md](references/admin-ui.md), then health, preview and remote control from
   [operations.md](references/operations.md).
6. Keep the measured numbers as the templates set them: the 10 MB upload limit, the 60 s poll, the 15 s video
   stall and the 3x-duration watchdog. Verify against the behaviour contract table in
   [player-runtime.md](references/player-runtime.md) (pull the network cable, delete the current ad mid-loop,
   issue a reload) and ship the player-machine and route tests unmodified, on vitest, as regression cover.
7. Hand over a tracked `.env.example` listing every variable the code reads, empty, and say in your closing
   summary that `SIGNAGE_TOKEN_PEPPER` must be set in every environment and that rotating it unpairs every
   screen.

## Reference directory

Load the reference matching the task; for greenfield design, read `data-model.md` first. Code in
`api-routes.md` and `operations.md` targets Firestore; `supabase-backend.md` defines every substitution.

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Fitting this into an existing app | adapt, rename, seam, integrate, tenant, host app, no auth yet, .env.example | [adaptation.md](references/adaptation.md) |
| Entities, fields, playlist shape | schema, model, Ad, Display, playlist, junction, soft delete | [data-model.md](references/data-model.md) |
| Firestore/Firebase backend | Firestore, firebase-admin, security rules, composite index, Firebase Storage | [firestore-backend.md](references/firestore-backend.md) |
| Supabase/Postgres backend | Supabase, Postgres, RLS, migration, storage bucket, Realtime | [supabase-backend.md](references/supabase-backend.md) |
| Endpoints, pairing, tokens, caching | API route, pairing, PIN, token, ETag, scope check, zod | [api-routes.md](references/api-routes.md) |
| Getting a screen paired | pairing, PIN, provisioning URL, hub, credential, unpair | [pairing.md](references/pairing.md) |
| The TV player loop | player, loop, crossfade, video stall, rotation, portrait, wake lock, offline | [player-runtime.md](references/player-runtime.md) |
| Back-office UI | admin, upload, media library, playlist editor, provisioning URL | [admin-ui.md](references/admin-ui.md) |
| Health, preview, remote control | heartbeat, last seen, offline, preview, reload, blank, emergency takeover, audit log | [operations.md](references/operations.md) |
| Scheduling, reuse, reporting | dayparting, start date, campaign, shared playlist, proof of play, precache, multi-zone | [extensions.md](references/extensions.md) |
| Why the templates differ from a naive port | provenance, ledger, rationale, kept, added | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
