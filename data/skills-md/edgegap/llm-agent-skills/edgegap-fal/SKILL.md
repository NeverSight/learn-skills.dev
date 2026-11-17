---
name: edgegap-fal
description: 'fal.ai + Edgegap: build a browser game with fal Agent (fal.ai, the media-generation agent) and make it online multiplayer on Edgegap with a matchmaker and one authoritative server per match, keeping solo play. Load this when someone says they made, or wants to make, a game with fal, fal.ai or fal Agent and wants Find Match, online play with friends, or real servers, or asks how to prompt fal Agent for game code that can go online. It has the fal Agent prompt that puts the rules in one DOM-free file the server can run, how to get the code and generated art out of a fal chat into a repo, the edgegap-threejs templates wired to that rules file, a GitHub Actions image build that Edgegap can pull, the dashboard path when the agent has no Edgegap API token, a GitHub Pages page, end-to-end tests, and clean-up so nothing runs non-stop. Worked example: netcode-sample-fal-orb-arena, verified on Edgegap. Games from other AI tools: edgegap-vibe-coded; a Node server already written: edgegap-threejs.'
metadata:
  version: "0.1.0"
---

# Edgegap for fal.ai games: fal Agent writes the game, Edgegap runs the matches

fal Agent (fal.ai) is an agent for images, video, 3D and audio, but it writes code when asked. This skill gets a playable single-player browser game out of it in a shape that can go online, then takes that game to online matches on Edgegap with the `edgegap-vibe-coded` and `edgegap-threejs` patterns:

```
fal Agent chat ──prompt (references/prompts.md)──> rules.js + main.js + index.html (+ generated art)
                                                      │ copied into client/, rules.js shared unchanged
                                                      v
page ──Find match──> Edgegap matchmaker ──starts──> one Node.js server per match near the players
     <──── wss://<id>.pr.edgegap.net:<port> ────     runs rules.js at 60 Hz, fills seats with bots,
                                                      stops itself when the match ends
solo mode still runs rules.js in the page, offline
```

**Verified on Edgegap** on 2026-11-09 with [netcode-sample-fal-orb-arena](https://github.com/edgegap/netcode-sample-fal-orb-arena) (Orb Arena, a top-down arena shooter for 4 ships): fal Agent wrote the rules, renderer and page in one answer on its free models; two headless players through `tests/e2e.mjs` and two real browser tabs on a GitHub Pages page were matched onto one deployment, played a full match and the deployment stopped itself 9 s after it. [references/walkthrough.md](references/walkthrough.md) goes file by file. The repo's README is the human version of this skill.

Not verified: fal Agent's paid models (they may answer differently), games where fal generated sprites are loaded at runtime (Orb Arena draws in code), two players on different networks.

## Who you are talking to

Often a creator who knows fal for images and video, not servers. Speak in outcomes ("each match gets its own server near its players and shuts down when the match ends, so you pay only while people play"), do the engineering yourself, and hand over only the account steps. Keep a record of the fal prompts used (`PROMPTS.md` or the README) if they want to show how the game was made.

## Phase 0: Get the game out of fal Agent in the right shape

1. **Prompt fal Agent** with the template in [references/prompts.md](references/prompts.md): the gameplay paragraph is theirs, the architecture paragraph stays as written. It asks for every rule in `rules.js` (no `window`, `document`, canvas, audio or timers), `setInput(world, id, input)` with plain values, `step(world, dt)` returning events, `botInput(world, id)` reading only positions, and the full content of each file. That shape is what lets the server import the same file in Phase 2.
2. **Check the game fits the network** (`edgegap-vibe-coded` Phase 0 table): drift, pushing, slow projectiles and turn-based play feel fine with no client prediction; precise platforming, rhythm and instant-hit aiming do not. If the idea is in the wrong column, change the design in the prompt (slower shots, a bit of slide) before fal writes it.
3. **Copy the code out.** fal answers in code blocks in the chat; copy each block into `client/` of a git repo (`rules.js`, `main.js`, `index.html`). If you drive the fal page from a browser tool, page scripts that read the blocks may be blocked: read the page text instead and re-indent, then diff the logic against the chat before committing. Images fal generated (a background, sprites) go in `client/assets/` with their prompts noted; they are the creator's media, not code.
4. **Run it locally** (`npx http-server client -p 8080`): ES modules don't load from `file://`.

✅ Check: the solo game plays against bots from `http://localhost:8080`, and `rules.js` has no DOM, canvas or timer code (`grep -nE "window|document|canvas|setTimeout|setInterval|requestAnimationFrame" client/rules.js` prints nothing).

If fal put the rules inside `main.js` anyway, move them into `rules.js` yourself before going on (`edgegap-vibe-coded` Phase 1); asking fal again with "all rules stay in rules.js" also works.

## Phase 1: The server, Find Match and local tests

Follow `edgegap-vibe-coded` Phases 1 and 2 with the `edgegap-threejs` templates. For a fal game:
- `server/` = `main.js`, `room.js`, `edgegap.js`, `util.js` from [`edgegap-threejs`'s server templates](../edgegap-threejs/assets/server/) unchanged, plus `server/game.js` that wraps `../client/rules.js` (Orb Arena's is about 70 lines, in the walkthrough): `addPlayer`/`removePlayer` call the rules with the room's player ids, `input` clamps every field, `start` builds a fresh world with the room's players (bots included), `update` runs `botInput` for bots then `step` and copies scores into the room, `result` ends on the rules' winner, `snapshot` sends rounded positions and the events.
- The page keeps fal's renderer: make it draw a plain view (`{players, projectiles, ...}`) built either from the solo world or from the server's snapshot, so one draw path serves both. Add Find match, Cancel and Play vs bots (`client/online.js`, `client/net.js`, `client/config.js` from the templates; `@edgegap/sdk` through an import map with the SRI hash).
- `tests/headless-player.mjs`: `playLikeABot()` builds `{players}` from the snapshot and calls the rules' `botInput`, so test matches end on score.
- `server/Dockerfile` copies `server/` and only `client/rules.js`.

✅ Check: `node tests/local-match.mjs` prints `PASS` (two headless players, full match), and two tabs on the local page with **Local server :7777** see the same match.

## Phase 2: Image, app version, matchmaker

Read [references/edgegap-setup.md](references/edgegap-setup.md). In short:
1. **Image from GitHub Actions** ([`server-image.yml`](../edgegap-threejs/assets/ci/server-image.yml) from `edgegap-threejs`): it runs the local match test, then pushes `registry.edgegap.com/<project>/<game>:<YYYYMMDD-HHMM>`. Keep `provenance: false` and `sbom: false` on `docker/build-push-action`: with the defaults, Orb Arena's first image failed every deployment with `Unable to pull image from registry`, and the same version pulled fine once the image was rebuilt without attestations. The developer sets the registry secrets in GitHub; you can set the `EDGEGAP_REGISTRY_PROJECT` variable.
2. **App version**: with an Edgegap API token, `edgegap_create_app_version` (port 7777 WS `gameport`, `tls_upgrade: true`, 256 vCPU units, restart `never`, max 30 minutes, quick-stop env vars). Without one (a hosted MCP client that can't pass the token, or the developer prefers it), the same settings in the dashboard: the setup reference lists every field, and the ports and env vars are added after the version is created.
3. **Matchmaker**: `matchmaker/arena.json` (2 to 4 players, a lone player after 20 s with bots) with the version name and every page origin in `allowed_cors_origins`. The developer creates and starts it in the dashboard; the "image not cached / not valid" warnings for a private image are expected. Its API URL and Auth Token go in `client/config.js` (client-safe; never the Edgegap API token).

✅ Check: the Actions summary shows the pushed tag, the version shows `7777 WS gameport` with TLS Upgrade on, and the matchmaker is ONLINE.

## Phase 3: Prove it, then clean up

1. `MM_URL=... MM_TOKEN=... node tests/e2e.mjs <profile> 2`, or the repo's **Matchmaker e2e** workflow when the agent's sandbox can't reach the matchmaker: both players on one deployment, a result, and the deployment stops itself. If deployments come and go in seconds, read the deployment log in the dashboard before anything else (pull errors show there, and container logs are gone once it stops).
2. Two browser tabs on the served page click **Find match** within 20 s and land in the same match. The page must be served from an origin in the CORS list: the agent's own `localhost` is not the developer's. GitHub Pages works for public repos on free plans ([`pages.yml`](../edgegap-threejs/assets/ci/pages.yml) from `edgegap-threejs`); a new site's first deploy can queue for minutes.
3. **Clean up, so nothing runs non-stop**: every match server stops itself; stop or delete the matchmaker when testing is over (the free tier stops it about 3 hours after each start anyway); unpublish the page if it should not stay up; list deployments and confirm none of yours are running. For a demo that must stay up, read [the public-demo reference of `edgegap-vibe-coded`](../edgegap-vibe-coded/references/public-demo.md) and say what it costs first.

## Phase 4: Hand-off

Tell the developer: the fal prompt and where the files came from, what was added, the app, version and matchmaker names, how to ship a new server build (new tag on the version), what wasn't tested, and what keeps costing money (only the matchmaker while it runs, and any deployment that didn't stop). If the repo becomes a public example, blank the matchmaker URL and token in `client/config.js` and write the steps with placeholders, as the Orb Arena README does.

## Reference files

- [references/prompts.md](references/prompts.md): the fal Agent prompt template, follow-up prompts, and the prompt for the coding agent.
- [references/edgegap-setup.md](references/edgegap-setup.md): image build, app version fields (MCP and dashboard), matchmaker config, GitHub Pages, and the pitfalls hit on the way.
- [references/walkthrough.md](references/walkthrough.md): Orb Arena from the fal chat to a verified online match, file by file.
- `edgegap-vibe-coded`: game fit, shared rules file, public demo. `edgegap-threejs`: server, client, CI and test templates, troubleshooting.
