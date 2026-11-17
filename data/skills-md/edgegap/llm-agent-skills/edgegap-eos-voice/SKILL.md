---
name: edgegap-eos-voice
description: 'Add in-game voice chat with EOS Voice (Epic Online Services) to an Unreal Engine game that runs on Edgegap dedicated servers. The game server is the trusted server: it checks each player''s EOS ID token, puts them in a match or team room from the Edgegap matchmaker data, gets room tokens from the EOS Voice Web API (EOS voice doesn''t run on Linux servers) and removes players who leave. Ships tested C++ drop-ins (device ID login so players need no Epic account, a replicated component that needs no game class edits, server token service), Developer Portal client policies, Edgegap env vars, local two-client test with fake audio, and fixes for pitfalls. Use for "add voice chat", "team voice", "proximity or party chat", "EOS voice", "push to talk", "players can''t hear each other", Vivox replacement, or voice on an Unreal game hosted on Edgegap. Needs a working Edgegap dedicated server first (edgegap-unreal). Not for Unity yet, lobby-only voice without a server, or Mumble.'
metadata:
  version: "0.1.3"
---

# EOS Voice on Edgegap dedicated servers (Unreal Engine)

Goal: players in a match talk to each other through EOS Voice, in rooms the **game server** decides (whole match, or per matchmaker team), and a player who leaves the server leaves voice. The job is done when two clients on an Edgegap deployment hear each other, proved by logs, not when it compiles.

Verified on **UE 5.5.4** from source (EOS SDK 1.16 bundled) with the [Edgegap Unreal sample](https://github.com/edgegap/game-sample-unreal-engine-topdown): two Windows clients matched by the Edgegap matchmaker onto one Linux deployment, in the same team room, hearing each other, and the leaving player removed from the room.

## How it works (explain this to the developer in two sentences, not more)

1. The client logs into EOS Connect with a **device ID** (no Epic account) on the EOSVoiceChat plugin's own EOS platform, then sends the server its Product User ID (PUID) and an **ID token** through a replicated `UEdgegapVoiceComponent`.
2. The server verifies the ID token (RS256, Epic's JWKS), picks the room from the player's IP and the matchmaker's `MM_TICKET_*` variables, calls `POST https://api.epicgames.dev/rtc/v1/{deployment}/room/{room}` with the player's IP, and sends the token to that player only.
3. The client joins with `IVoiceChat::JoinChannel`. On logout the server calls `DELETE …/participants/{puid}`, which also revokes the token.

The server uses the **Web API**, not the EOS SDK, because EOS Voice doesn't support Linux. Lobby-managed voice (EOS lobbies with `bEnableRTCRoom`) needs no server and is a fine choice for pre-match party chat, but then the server can't enforce team rooms.

## How to work

- Be the engineer: copy the files, edit Build.cs and config, run the builds and tests, read the logs. Hand the developer only the Developer Portal clicks and the secrets.
- **Secrets.** The trusted server's EOS client secret can mint tokens for any room: never in a game build, a repo, `DefaultGame.ini`, chat output or a command line. It lives in the git-ignored `Config/UserGame.ini` for local tests and in Edgegap app version variables (marked hidden) for deployments. Ask the developer to paste secrets into files themselves; read files without printing secret values.
- The **game client's** EOS ID and secret ship in every build by design (its policy has no Voice actions). Still keep real values out of a public repo: `Config/UserEngine.ini`.
- Unreal builds are slow; background them and never trigger an avoidable full rebuild (Phase 5 pitfall).
- Track the phases as a todo list.

## Phase 0: Preconditions

- The game already runs on an Edgegap dedicated server, ideally with the Edgegap matchmaker. If not, do `edgegap-unreal` first; voice on top of an unproven server only doubles the debugging.
- A C++ game module (voice is C++; Blueprints can call it later).
- The engine has `Engine/Plugins/Online/VoiceChat/EOSVoiceChat` and `Engine/Source/ThirdParty/EOSSDK` (UE 5.x from source has both). Note the EOS SDK version in `EOSSDK/SDK/Include/eos_version.h`: 1.16+ allows 64 players per room, older 16.
- Clients are Windows or Mac (the plugin's platforms). The server is Linux.

## Phase 1: EOS Developer Portal (the developer does this)

Read `references/eos-portal.md` and send the developer those exact steps: product IDs, two client policies (game client: User required, no Voice; trusted server: custom, User required off, Voice `createRoomToken`, `kick`, `mute`), one client per policy. The portal hides clients under **Product Settings → Clients tab**, not the left menu; the trusted-server policy shows a "credentials without requiring a user" warning, which is expected.

✅ Check: the developer has Product ID, Sandbox ID, Deployment ID, and two client ID/secret pairs, and has put them in the files from Phase 3.

## Phase 2: Drop in the code

1. Copy `assets/unreal/Source/*` into `Source/<Module>/`. Five classes, no edits to the game mode or player controller:
   - `EdgegapVoiceSettings.h`: on/off switch and options (config=Game).
   - `EdgegapVoiceClientSubsystem`: device ID login, ID token, join/leave, `VoiceMute` console command.
   - `EdgegapVoiceComponent`: the two RPCs; the server adds it to every PlayerController at login.
   - `EdgegapVoiceServerSubsystem`: token verification, rooms, Web API calls, logout cleanup.
2. Add the Build.cs block from `assets/unreal/Build.cs.txt` (OpenSSL for every target; `EOSSDK`, `EOSShared`, `VoiceChat`, `EOSVoiceChat` and `WITH_EDGEGAP_EOS_VOICE_CLIENT=1` only for Win64/Mac non-server targets).
3. Enable the plugin in the `.uproject` (`assets/unreal/uproject-plugin.json`), restricted to Win64 and Mac so the Linux server doesn't load the EOS SDK.
4. Append `assets/unreal/Config/DefaultGame-voice.ini` and `DefaultEngine-voice.ini`, replacing `<Module>`. `bEnabled=False` and placeholders in the committed files.

✅ Check: the editor target (Win64) and the Server target (Linux) both compile.

## Phase 3: Configure

- `Config/UserEngine.ini` (git-ignored, read by the plugin from `GEngineIni`): `[EOSVoiceChat]` with ProductId, SandboxId, DeploymentId, game client ClientId and ClientSecret.
- `Config/UserGame.ini` (git-ignored): `[/Script/<Module>.EdgegapVoiceSettings]` with `bEnabled=True`, and `ServerClientId`/`ServerClientSecret` for a local server.
- Check `.gitignore` covers `Config/User*.ini` before anyone writes a secret.

## Phase 4: Local test, two clients on one PC

Read `references/testing.md` §1. Server: `UnrealEditor.exe <uproject> /Game/<path>/<ServerMap> -server -log`. Client A with `-ExecCmds="EOSVoiceChat.FakeAudioInputEnabled 1"`; client B with `-EOSVoiceNewDeviceId`, started **only after A logs `Voice: logged into EOS`**.

✅ Check, in the logs: server `trusted voice server ready` and one `gets room` per player with **different PUIDs**; each client `joined room`; client B `<A's PUID> started talking`; after closing B, server `removed <B> … (204)`.

## Phase 5: Ship to Edgegap

Read `references/testing.md` §2.
1. Package the Linux server and build/push a **new image tag** (UTC timestamp `YYYYMMDD-HHMM`, also the app version name) (never reuse a tag a host may have pulled).
2. App version for that tag, with environment variables `EOS_VOICE_CLIENT_ID`, `EOS_VOICE_CLIENT_SECRET` (hidden), `EOS_VOICE_DEPLOYMENT_ID`, and optionally `EOS_VOICE_GAME_CLIENT_ID` (then tokens must be issued to the game client). Voice turns on in the server when `EOS_VOICE_CLIENT_ID` is set. The Edgegap MCP `edgegap_create_app_version` can't mark a variable hidden (it attaches the registry login itself through `registry_profile: "Edgegap"`); if that matters, the developer duplicates the previous version in the dashboard and change tag and variables (the dashboard refuses to save until the tag exists in the registry).
3. Point the matchmaker profile's `application.version` at it (a free-tier matchmaker stops after 3 hours: recreate it and update the client's URL and token).

✅ Check: two clients matched by the matchmaker into one deployment hear each other; the deployment log shows `gets room` lines and `removed … (204)` when a player quits. With a one-team profile the room is `<match>-team-<id>`, which proves the IP-to-ticket lookup; telling two teams apart needs clients on two networks (`references/testing.md` §2).

## Hand-off

What was added and where; how to turn voice off (unset the variables or `bEnabled=False`); `SetHardMuted` for game rules (dead players, penalties); next steps: push-to-talk binding, a mute/volume UI on `IVoiceChat`, `EOS_RTC_BlockParticipant` for platform block lists, parental controls, replacing device ID with the platform's login (Steam, consoles) and linking accounts.

## Reference files

- `references/eos-portal.md`: exact Developer Portal steps and what each ID is for.
- `references/testing.md`: local two-client test, Edgegap test, expected log lines.
- `references/troubleshooting.md`: symptom → cause → fix, every row from a real run.
- `assets/unreal/Source/`: the drop-in classes. `assets/unreal/Config/`: ini sections. `assets/unreal/Build.cs.txt`, `assets/unreal/uproject-plugin.json`.

Related: `edgegap-unreal` (server, packaging, matchmaker), `edgegap-launch` before going live.

Sources of truth: Epic's [Voice Interface overview](https://dev.epicgames.com/docs/epic-online-services/multiplayer/voice-and-rtc-interface/voice-interface/voice-overview), [Voice Web API](https://dev.epicgames.com/docs/web-api-ref/voice-web-api), [Connect Interface reference (ID tokens, device ID)](https://dev.epicgames.com/docs/epic-online-services/eos-fundamentals/connect-interface/connect-reference), Edgegap's [matchmaker injected variables](https://docs.edgegap.com/learn/matchmaking/matchmaker-in-depth), and the sample https://github.com/edgegap/game-sample-unreal-engine-topdown.
