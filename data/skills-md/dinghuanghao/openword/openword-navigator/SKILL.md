---
name: openword-navigator
description: Operate OpenWord end-to-end for live adventure sessions. Use when needs to download/install/start OpenWord, guide a human player in the browser, or play autonomously through REST API (create/load game, do_action loop, state/image retrieval), including configuring GEMINI_API_KEY and sharing interesting scenes and choices during play.
---

# OpenWord Player

Read `references/session-runbook.md` before running a session.
Treat repository `README.md` as the source of truth for install/startup/API details, and re-check it when commands fail or look outdated.

## Session Workflow

1. Ask the user which mode to run before gameplay starts.
2. Prepare runtime (download/install/start, browser, key setup).
3. Branch to human-guided mode or AI REST mode.
4. For every turn in both modes (including AI-driven sessions), show `last_scene_image_path + narrative + player_profile` as a natural user-facing update (avoid raw field-label dump).

Use this exact mode-selection question:

`主人你想自己玩，还是我来玩？`

If the user does not choose, default to human-guided mode.

## Runtime Preparation

1. If repository does not exist locally, run:
`git clone https://github.com/dinghuanghao/openword.git`
2. Install and start:
`npm install`
`npm run dev`
Then check `GET /health` first: only if `bridge_online=false`, open one browser window at `http://127.0.0.1:<PORT>` (default `30000`) and re-check once; if already connected, do not open a new window.
3. `GEMINI_API_KEY` load order is: shell environment variable -> repo `.env` -> key modal/Settings.
4. `PORT` is optional (default `30000`); ensure browser opens `http://127.0.0.1:<PORT>`.
5. Confirm the game can reach interactive state before sending turns.

## Human-Guided Mode

1. Confirm user can input actions in the browser.
2. Help user craft opening world prompt and style.
3. For each turn, provide a short recap and 3 action options with different risk/reward.
4. Let the user pick or rewrite the action.
5. Remind controls only when relevant:
`机器人按钮` toggles built-in Auto Player, `Esc` exits auto mode/panels, Settings has `Connect API Bridge`.

## AI REST Mode

Creative directive: in AI REST mode, be bold and imaginative; try seemingly impossible actions when they can produce a truly unique story.

1. Ensure one browser tab is online at `http://127.0.0.1:<PORT>` (default `30000`); before opening a new tab/window, check `GET /health`: if `bridge_online=true`, do not open; if `bridge_online=false`, open only one tab/window and re-check once.
2. BFF/`Connect API Bridge` should be connected by default; do not ask the user to click it unless troubleshooting a bridge failure.
3. Check server health (`GET /health`).
4. Start or resume game via REST (`create_game` or `load_game`).
   - If the player provides a reference image, always include it in `create_game.image_path`.
   - If the player does not provide a reference image, do not send `image_path`.
   - When `image_path` is used, prefer an absolute path.
5. Loop:
call `get_current_game_state` -> choose a high-impact next action -> call `do_action` -> immediately show a natural-language update synthesized from `last_scene_image_path + narrative + player_profile` to the user.
6. After each turn update, either continue autonomously or pause at key nodes for user input.
7. Prefer visual style `3D Pixel Art` (voxel) or `Claymation` (clay); avoid frequent style switching in one session.

Use `scripts/openword_rest.sh` first (curl-only).  
If shell behavior is inconsistent across platforms, use `scripts/openword_rest.py` with the same commands/arguments.
If `PORT` is not `30000`, set:
`OPENWORD_BASE_URL="http://127.0.0.1:<PORT>"`.

## REST API Schema

| Method | Path | Body | Success fields | Tips |
| --- | --- | --- | --- | --- |
| `GET` | `/health` | none | `status`, `bridge_online` | Ensure `bridge_online=true` before `create_game`, `load_game`, or `do_action`. |
| `POST` | `/api/create_game` | `{ "description": string, "style": string, "image_path"?: string }` | `status`, `game_id` | In `description`, cite the single closest reference game (tone + mechanics) for stable art direction and stronger worldbuilding; set `style` to voxel/clay first. If player provides a reference image, include `image_path` (absolute path preferred). |
| `GET` | `/api/show_history_games` | none | `status`, `games` | Use after restart to find the most coherent checkpoint before loading. |
| `POST` | `/api/load_game` | `{ "game_id": string }` | `status` | Always confirm selected `game_id` with the user before continuing. |
| `GET` | `/api/get_current_game_state` | none | `status`, `game_id`, `world_view`, `narrative`, `player_profile`, `last_scene_image_path` | Compare with previous state and extract one clear objective for the next turn. |
| `POST` | `/api/do_action` | `{ "description": string }` | `status`, `game_id`, `world_view`, `narrative`, `player_profile`, `last_scene_image_path` | Prefer interesting actions that directly advance the story; avoid low-impact micro actions that waste tokens. |

## Interaction Contract

Never run long silent streaks. Keep the user in the loop even when AI plays.

1. After every turn, show one natural-language update based on `last_scene_image_path + narrative + player_profile` before the next action; do not print rigid prefixes like `last_scene_image_path:`, `narrative:`, `player_profile:`.
2. At meaningful branch points, ask user preference before committing.
3. Surface scene image paths and display scene images when possible.
4. Highlight interesting moments:
scene changes, risky decisions, major rewards, unexpected twists.

## Failure Handling

1. `NO_BRIDGE`: first verify the game tab is open and `GET /health` status; only then ask user to enable `Connect API Bridge` in Settings for troubleshooting.
2. Bridge occupied: another tab owns the bridge; disconnect that tab first.
3. Missing key/model errors: check `GEMINI_API_KEY` in shell env first, then repo `.env`; if still missing, ask user to configure key modal/Settings.
4. Slow/timeout calls: increase timeout, avoid overlapping requests. Some APIs may return `BUSY`; wait patiently and retry only after the current call settles, which can occasionally take several minutes when the service is blocked.
