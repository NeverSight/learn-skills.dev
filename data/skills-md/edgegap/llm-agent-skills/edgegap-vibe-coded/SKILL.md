---
name: edgegap-vibe-coded
description: 'Make a vibe-coded game online multiplayer on Edgegap: a single-player browser game made with an AI tool (Claude, Cursor, Codex, ChatGPT, Lovable, Bolt, v0, Replit, Websim...) that plays against bots in the page, turned into online matches with one authoritative server per match, Find Match and a matchmaker, while solo play keeps working. Load this first for "make my vibe-coded game multiplayer", "add online play to the game I made with AI", "play this with friends online", "my Lovable/Bolt game needs multiplayer", or which game ideas work online. It checks whether the game holds up with network delay, gets the code out of the AI tool into a repo, moves the rules into one file shared by page and server, and runs a public demo cheaply (matchmaker always on, servers stop fast, free-tier limits). Verified with Thin Ice Tussle. fal.ai: edgegap-fal; server and client templates: edgegap-threejs; games on Supabase: edgegap-supabase; Manus: edgegap-manus.'
metadata:
  version: "0.1.3"
---

# Edgegap for vibe-coded games: from single-player to online matches

Most vibe-coded games start the same way: one HTML page, a game loop, the player against bots, everything in the browser. This skill takes that game online without breaking it:

```
before: page = rules + bots + rendering + input              (solo only)
after:  page = rendering + input + Find Match ──> Edgegap matchmaker (always on)
                                                    │ 2-4 players, a lone player after 20 s
                                                    v
        page <── wss ── one Node.js server per match, near those players
                        runs the SAME rules file at 60 Hz, fills seats with bots,
                        stops itself when the match ends or empties
        solo mode still runs the rules file in the page, offline
```

**Verified on Edgegap** with two games built this way from scratch by an agent, each with tags `before` (single-player) and `after` (online):
- [netcode-sample-threejs-thin-ice-tussle](https://github.com/edgegap/netcode-sample-threejs-thin-ice-tussle) (2026-11-04): a Three.js ice brawler for 4, playable on [GitHub Pages](https://edgegap.github.io/netcode-sample-threejs-thin-ice-tussle/). End to end through the matchmaker, two browser tabs on the live page, a match both players left stopped about 12 s later, an abandoned match in two background tabs stopped at 48 s. The online diff is about 1,300 added lines across 25 files; the rules file did not change. [references/walkthrough.md](references/walkthrough.md) goes file by file.
- [netcode-sample-threejs-vibe-coded](https://github.com/edgegap/netcode-sample-threejs-vibe-coded) (2026-11-03): Orb Herders, a hover-drone arena game, same shape.
- [netcode-sample-fal-orb-arena](https://github.com/edgegap/netcode-sample-fal-orb-arena) (2026-11-09): Orb Arena, written by fal Agent from one prompt, Canvas 2D; `edgegap-fal` covers the fal side.

Not verified: two players on different networks or devices (each developer's own test), games whose source is React + Vite from Lovable, Bolt or v0 (the pattern is the same, the files move), Phaser or Babylon.js clients.

## Who you are talking to

The developer may never have run a server, used Docker or heard of a matchmaker. Speak in outcomes ("each match gets its own server near its players, and it shuts down when the match is over, so you only pay while people play"), do the engineering yourself, and hand over only the account steps nobody else can do. Write each prompt that moved the work forward into `PROMPTS.md` if the developer wants to show how the game was made (both samples do).

## Phase 0: Can this game go online as it is?

Read the game first, then tell the developer in a few lines.

**Where the code lives.** Online play needs the code in a folder you can edit and a git repo:
- Made in a coding agent (Claude Code, Cursor, Codex): it is already a folder.
- Made in Lovable, Bolt, v0, Replit or similar: connect the project to GitHub or download it, and work on that copy. These projects are usually React + Vite + TypeScript: the server can't import the page's `.tsx`, so the shared rules file becomes a plain `.js` module (or the server gets its own build step), and the page keeps its build.
- A single HTML file (a Claude or ChatGPT artifact, a Websim page): split it into `client/index.html`, `client/rules.js` and the rest first.
- No local Docker? The image can be built by GitHub Actions instead ([`server-image.yml`](../edgegap-threejs/assets/ci/server-image.yml) in `edgegap-threejs`).

**Does the game hold up with network delay?** The `edgegap-threejs` client draws what the server sends and eases toward it; there is no client-side prediction. A press reaches the server and comes back on screen in about one round trip plus up to 50 ms (20 snapshots a second). Tell the developer which kind their game is:

| Feels fine online | Needs care | Change the design or expect lag |
|---|---|---|
| Slippery or floaty movement (ice, hover, cars that drift), pushing and bumping, party games, collecting, arenas with slow projectiles, turn-based | Fast top-down shooters, sports with a ball, racing with tight corners | Precise platforming, rhythm, fighting games with frame timing, instant-hit aiming |

Thin Ice Tussle was picked for this: the ice is slippery anyway, so the delay barely shows on mobile data. For the right column, say so before starting, and offer the design change (a bit of slide, slower projectiles, a wind-up before hits) rather than promising prediction code.

**Where the rules live.** Find the game loop, the world state, the bot logic and what reads the DOM, Three.js or `Math.random` inside the rules. That decides how much Phase 1 moves.

Ask in one message only what you couldn't read: players per match (default 2 to 4), whether a lone player gets a match with bots after 20 s (default yes), where the page will be hosted, their Edgegap account, and whether this will be a public demo left running (Phase 4).

## Phase 1: One rules file for the page and the server

Don't port the rules to the server: move them into one module both sides import. Full steps in [`edgegap-threejs` server.md §9](../edgegap-threejs/references/server.md); in short:
1. `client/rules.js`: no `window`, `document`, Three.js, audio or timers. A world object, `addPlayer`/`removePlayer`, input on each player, `step(world, dt)` returning events (hit, fall, pickup), `botInput(world, me, memory, dt)` reading only positions. Seed or inject randomness if replays matter; otherwise `Math.random` is fine because only the server's world counts online.
2. Solo mode: the page keeps running `step()` itself with bots, exactly as before. Check it still plays the same.
3. The page's renderer draws a plain view of the world (`{players, tiles, ...}`), so the same draw code serves solo and online snapshots.

✅ Check: solo plays as it did in `before`, and nothing in `rules.js` touches the page.

## Phase 2: The server, the client, the tests

Load `edgegap-threejs` and follow its Phases 1 to 5 with this game:
- `server/` from its [server templates](../edgegap-threejs/assets/server/), with `server/game.js` wrapping `../client/rules.js` in the room contract (Thin Ice Tussle's is 67 lines, quoted in the walkthrough). Bots fill empty seats (`botFill`).
- The page gets Find Match (`@edgegap/sdk` `GroupAgent`), a Cancel, a queue timer so waiting never looks frozen, and the online loop that sends inputs and draws snapshots. Solo stays one button away.
- `tests/local-match.mjs` (two headless players driven by `botInput`, so matches end on score), then `parity.sh` from `edgegap-local-testing`, then one direct deployment, then the matchmaker and `e2e.mjs`.

✅ Check: two browser tabs on the local server see the same match; then two tabs on the real page get matched together on Edgegap and the deployment stops after the match.

## Phase 3: What the developer does

Only these, each with the exact link or value:
1. An Edgegap account and an API token, put in the agent's MCP settings (never in the game, the repo or chat).
2. Create the matchmaker in the dashboard from the config file you wrote (give its full path), and start it.
3. Secrets for the image workflow in GitHub, if CI builds the image.
4. Play it with someone on another network.

The app version needs no registry login from them: `edgegap_create_app_version` sends `registry_profile: "Edgegap"`; check `registry_credentials_set: true`.

## Phase 4: A public demo that stays up

When the game will sit on a public page with the matchmaker on all the time, read [references/public-demo.md](references/public-demo.md). The short version:
- Only the matchmaker runs non-stop. Every deployment stops itself fast: `EMPTY_TIMEOUT_S=10`, `FIRST_JOIN_TIMEOUT_S=45`, `IDLE_TIMEOUT_S=75` (with the client heartbeat), `RESULTS_SECONDS=8`, `REQUIRE_TICKET=1`, restart policy `never`, max duration 30 minutes as the backstop.
- The free tier's matchmaker stops about 3 hours after each start, and it allows one deployment at a time. A demo that must stay up needs a paid tier; tell the developer before they announce it.
- Edgegap's matchmaker has no cap on concurrent deployments and no per-player ticket limit. Say so plainly if the developer asks for one; a small gate service in front of the matchmaker is the option, not a config setting.
- The matchmaker's client token in the page is by design. Scan the repo for secrets before making it public.

## Phase 5: Hand-off

Tell the developer: what changed (the `before`/`after` diff if they tagged it), how to play solo and online, the app, version and matchmaker names, how to ship a new server build, what wasn't tested, and what keeps costing money (the matchmaker, and any deployment that didn't stop). Before finishing, stop every deployment you started and check with `edgegap_list_deployments` `only_agent_deployments: true`.

## Reference files

- [references/walkthrough.md](references/walkthrough.md): Thin Ice Tussle from `before` to `after`, file by file, with the prompts that drove each step.
- [references/public-demo.md](references/public-demo.md): always-on matchmaker, quick-stop servers, costs, the splash page, abuse limits, going public.
- `edgegap-threejs`: the server, client, Dockerfile, matchmaker and test templates; its troubleshooting covers connection and stop problems.
