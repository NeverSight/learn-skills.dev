---
name: edgegap-supabase
description: 'Supabase + Edgegap: use Supabase as the backend of a multiplayer game (sign-in, player profiles, leaderboards, match history) while Edgegap runs one authoritative game server per match, end to end. Load this before using any Edgegap MCP tool on a project that has or wants Supabase (@supabase/supabase-js, a supabase/ folder, Supabase Auth, Edge Functions, Row Level Security). Templates verified on Edgegap with a Three.js game: anonymous sign-in, Postgres schema with RLS, an Edge Function that holds the Edgegap matchmaker token and ties tickets to users, a game server that verifies Supabase access tokens with JWKS and holds no Supabase key, results reported through a second Edge Function and checked in Postgres, a live Realtime leaderboard, headless e2e. Use for "Supabase as my game backend", "only signed-in players can find a match", "save match results/wins from the game server", "leaderboard with Supabase", "Supabase auth + dedicated servers". Nakama: edgegap-nakama; PlayFab: edgegap-playfab.'
metadata:
  version: "0.1.1"
---

# Edgegap with Supabase: Supabase is the backend, Edgegap runs the matches

Goal: a multiplayer game where **Supabase** signs players in and keeps everything that outlives a match (profiles, wins, match history, leaderboard), and **Edgegap** starts one authoritative game server per match near its players. Done means two signed-in players found each other through Supabase, played a whole match on one Edgegap deployment, the result landed in Supabase, and the deployment stopped itself; not that the functions deploy.

```
browser --supabase.auth.signInAnonymously()--> Supabase Auth (+ profile row by trigger)
browser --functions.invoke("matchmaking", join/status/cancel)--> Edge Function --POST /groups, GET member--> Edgegap Matchmaker --deploys near players--> Edgegap
browser <--{status, ticket_id, url: wss://<fqdn>:<port>}--
browser ==wss, hello{ticket, Supabase access token}==> Node.js game server: verifies the token (JWKS), checks the ticket (MM_TICKET_IDS), runs the match
game server --POST report-match + shared secret--> Edge Function --record_match()--> Postgres: every ticket must be its player's, unused
browser <--Realtime: profiles changed--   game server --DELETE $ARBITRIUM_DELETE_URL--> stopped
```

Verified on 2026-11-03 with [netcode-sample-threejs-supabase](https://github.com/edgegap/netcode-sample-threejs-supabase) (Sumo Push from the Three.js minigames), a hosted Supabase project on the free plan, Supabase CLI 3.0.0, supabase-js 2.118.0 and the Edgegap free tier: `assets/tools/e2e.mjs` signed in two headless players, queued them through the Edge Function, both landed on one deployment in about 15 s, played a full match with their access tokens, the server's report created the match and updated both profiles, and the deployment stopped itself 14 s after the match. A browser did the same alone (matched after the 20 s expansion, with bots) and its leaderboard updated live. Checked against the live project: players can't change their wins, insert tickets or call `record_match()`; a missing or forged token is refused by the game server; `report-match` refuses a wrong secret, a ticket that isn't the player's, and a replayed report; a human winner gets the win. Not run: a non-Node game server (Unity, Godot, Unreal) verifying the token, email/OAuth sign-in, Supabase's local stack (`supabase start`), team profiles. Say so when those matter.

Why this shape, so you can defend it:
- **The browser holds no secret.** It has the project URL and the publishable key (made to ship, limited by Row Level Security). The matchmaker token lives in Edge Function secrets, so only signed-in players can queue, and each ticket is recorded against a Supabase user.
- **The game server holds no Supabase key.** It verifies access tokens against the project's public signing keys (JWKS), so it learns who each player is with no secret and no call per player. It reports results with a shared secret; even a leaked secret can't award wins, because `record_match()` only accepts players with their own unused ticket.
- **The server decides results.** Players send inputs; the server owns rules and the winner. Nothing done in devtools reaches the leaderboard.
- **Supabase is not the matchmaker.** Edgegap's matchmaker groups players and places the server near them; Supabase only gates and records. Don't rebuild queues in Postgres.

## How to work

- **Be the engineer.** Write the schema, functions, server and client changes, run the Supabase CLI (`npx supabase`), Docker and the Edgegap MCP tools. Hand the developer only account steps: `npx supabase login`, creating the matchmaker in the dashboard and pasting its URL and token.
- **One layer at a time**: game on a local server → Supabase project (schema, sign-in, RLS checked) → server verifying tokens locally → image and app version → matchmaker → Edge Functions → e2e on Edgegap → browser.
- **Secrets** (full rules: [the edgegap skill's agent rules](../edgegap/references/agent-rules.md)): the Edgegap API token never goes anywhere in this design. The matchmaker token and the game server secret go in `npx supabase secrets set`; the game server secret also in a **hidden** env var on the app version. The Supabase secret / service role key never leaves Supabase (Edge Functions get it injected). The publishable key may ship in the page.
- **Hosted Supabase changes need consent.** Creating a project, `db push`, `config push`, `secrets set` and `functions deploy` change the developer's account: ask once for the plan, then pass `--yes` (the CLI refuses in agent mode without it).

## Phase 0: Understand the game

Read, don't ask: the client (renderer, bundler or none, existing Supabase usage), the server (Node `ws`, Colyseus, an engine build), what "a result" is (winner, scores, placements), and whether players already sign in (Supabase Auth with email/OAuth, or nothing yet).

- No game server yet, browser game: build it with `edgegap-threejs` first (room, phases, self-stop, Dockerfile), then come back. This skill's server and client templates patch that skill's files.
- Colyseus server: `edgegap-colyseus` for hosting; take this skill's Supabase pieces (schema, functions, `server/supabase.js` in `onAuth`).
- Engine server (Unity, Godot, Unreal): the schema, Edge Functions and client flow are the same over HTTP; the server needs a JWT library to verify ES256 tokens against JWKS (`references/game-server.md` §4). Not verified on Edgegap.

Ask, in one message, only what you couldn't infer: their Supabase organization (or permission to create a project), whether players already have accounts, and what the leaderboard ranks.

## Phase 1: Supabase project and schema

Read `references/supabase.md`.
1. `npx supabase login` (the developer, in a terminal: it opens a browser), `npx supabase orgs list`, `npx supabase projects create <name> --org-id <id> --region <region> --db-password <generated> --yes`, `npx supabase init`, `npx supabase link --project-ref <ref>`.
2. Copy `assets/supabase/migrations/` and adapt: what a profile holds, what `record_match()` counts. Keep the ticket checks. `npx supabase db push --remote --yes`.
3. Anonymous sign-ins on: add `assets/supabase/config.toml.snippet` and `npx supabase config push --yes` on a project made for this, or flip **Allow anonymous sign-ins** in the dashboard on an existing one (config push sends every Auth setting in `config.toml`).
4. `curl https://<ref>.supabase.co/auth/v1/.well-known/jwks.json` lists at least one key (new projects sign with ES256). An empty list means legacy HS256 signing: switch the project to asymmetric JWT signing keys in the dashboard first (`references/game-server.md` §4).

✅ Check: a headless `signInAnonymously()` gets a user and a `profiles` row; that player can rename themselves but `update({wins: 99})`, `insert` into `tickets` and `rpc("record_match")` are refused.

## Phase 2: Game server checks players and reports results

Read `references/game-server.md`.
1. Copy `assets/server/supabase.js` into `server/`, `npm i jose`, apply `assets/server/room.js.patch` to the `edgegap-threejs` room (`git apply`): async `identify()` on hello, one connection per user, `report()` on finish.
2. The server reads `SUPABASE_URL` (public) and `GAME_SERVER_SECRET`. Without `SUPABASE_URL` it lets anyone in (local dev).

✅ Check: `SUPABASE_URL=... node server/main.js`; a headless client with a real access token gets `welcome`, one with no token or a forged one gets `error: Not signed in`.

## Phase 3: Image, app version, matchmaker

As in `edgegap-threejs` Phase 3–4 (WS port `gameport`, TLS Upgrade, 256 CPU / 512 MB), plus env: `SUPABASE_URL`, `GAME_SERVER_SECRET` (hidden; generate 32 random bytes hex), `REQUIRE_TICKET=1`. Matchmaker from `assets/matchmaker/sumo.json`. The browser never calls the matchmaker, so CORS origins don't matter for it; keep the list valid.

## Phase 4: Edge Functions

1. Copy `assets/supabase/functions/` (`_shared`, `matchmaking`, `report-match`) and the `[functions.*] verify_jwt = false` blocks: both functions check callers themselves.
2. `npx supabase secrets set EDGEGAP_MM_URL=<url> EDGEGAP_MM_TOKEN=<token> GAME_SERVER_SECRET=<secret> --yes`, then `npx supabase functions deploy matchmaking --yes` and `report-match`.

✅ Check: `report-match` without the secret → 403; with it and a made-up ticket → 422.

## Phase 5: Client

Read `references/client.md`. `assets/client/backend.js` is all the Supabase client code: anonymous sign-in, profile, rename, Realtime leaderboard, Find Match through the function, the access token for the hello. `assets/client/shell.js` is `edgegap-threejs`'s shell with that wired in (menu name/record/leaderboard, Find Match, token in the hello); `index.html` loads supabase-js 2.118.0 as a UMD script with its SRI hash; `config.js` takes the URL and publishable key.

## Phase 6: End-to-end test and hand-off

1. `edgegap_list_deployments` for the app: nothing of yours left running. Matchmaker inspect shows no stale tickets.
2. `SUPABASE_URL=... SUPABASE_PUBLISHABLE_KEY=... node tools/e2e.mjs 2` (`assets/tools/e2e.mjs`): sign-in, Find Match through the function, one deployment, full match with tokens, the match and both profiles read back from Supabase, `report-match` refusing a wrong secret, self-stop. Anonymous sign-ins are limited to 30 per hour per IP by default.
3. A real browser (two different browser profiles or a private window: one profile shares one session) clicks **Find match**.
4. Debug with `references/troubleshooting.md`.

Cancel matters: a search left in the queue can start a server nobody joins. The template cancels on the Cancel button, on a new Find Match and on page close (`references/client.md` §3); keep that when you change the client.

Hand-off: Supabase project ref and what's in it, app/version/matchmaker names, which secrets live where (never their values), how to ship a new server build (`edgegap-threejs` §5 of `deploy.md`), what wasn't tested, before launch: `inspect: false`, a lower `FIRST_JOIN_TIMEOUT_S` for servers whose players left before joining, link email/OAuth to anonymous users so progress survives devices, a cleanup job for old `tickets` rows, `edgegap-launch`.

## Reference files

- `references/supabase.md`: CLI 3 workflow, schema and RLS walkthrough, `record_match()`, secrets, the matchmaking function and the Edgegap group API it calls, Realtime.
- `references/game-server.md`: verifying access tokens (JWKS, issuer, audience), the hello handshake, reporting, retries, other server languages.
- `references/client.md`: supabase-js without a bundler, sign-in and session reuse, Find Match polling, upgrading anonymous users.
- `references/troubleshooting.md`: symptom → fix.
- `assets/`: `supabase/` (migration, functions, config snippet), `server/` (`supabase.js`, `room.js.patch`), `client/` (`backend.js`, `shell.js`, `index.html`, `config.js`, CSS), `matchmaker/sumo.json`, `tools/` (e2e and headless player).

Related skills in this pack: `edgegap` (platform and safety rules), `edgegap-threejs` (the game server and client this builds on), `edgegap-colyseus`, `edgegap-matchmaking`, `edgegap-nakama` and `edgegap-playfab` (other backends), `edgegap-troubleshoot`, `edgegap-launch`.

Sources of truth: https://supabase.com/docs/guides/auth/auth-anonymous, https://supabase.com/docs/guides/auth/signing-keys, https://supabase.com/docs/guides/functions, https://supabase.com/docs/guides/database/postgres/row-level-security, https://docs.edgegap.com/learn/matchmaking, https://github.com/edgegap/netcode-sample-threejs-supabase.
