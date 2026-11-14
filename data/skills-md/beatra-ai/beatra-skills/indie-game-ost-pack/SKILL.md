---
name: "indie-game-ost-pack"
description: "Build an original indie game OST pack of 8 to 15 instrumental tracks for title, explore, battle, shop, and victory. This game soundtrack studio and game BGM generator writes loop-friendly game music you own and can use commercially, then delivers a labeled soundtrack you can audition in-engine. Use it as a game music pack for indie game OST, game background music, game BGM, battle music, explore music, shop music, and original game soundtrack work."
---

# Indie Game OST Pack

Turn a game brief into a labeled original soundtrack. The normal delivery
is a pack of 8 to 15 instrumental beds, not one song.

## Scope and adjacent routes

Use this Skill when an indie game, mini-game, or interactive title needs a
reusable set of original loop-friendly instrumentals the studio can own
and use commercially.

Route one instrumental written for a specific video cut to
`short-video-bgm-studio`. Route a livestream or store playlist to
`livestream-bgm-pack`. Route a brand jingle or sonic logo to
`brand-jingle-studio`. Route a short-drama episode score to
`short-drama-score-pack`. Route a song with lyrics to
`beatra-ai-music-creator`. Route spoken game lines to
`game-script-voice-pack`.

## Inputs and defaults

The hard inputs are:

- the game's setting or genre;
- how many tracks the pack should contain, or permission to use the default
  of 10;
- the mood the soundtrack should hold.

Reuse already-known world, combat intensity, UI needs, and exclusions.
Ask only when a missing answer changes the pack size or the paid slots.
A count outside 8 to 15 is still doable: confirm that pack size and its
live cost instead of treating it as impossible.

Safe defaults:

- 10 tracks unless the user names a count between 8 and 15.
- Slot mix: title, explore, battle, shop, victory, game-over, and quiet
  hub beds.
- `instrumental: true` with lyrics absent.
- `model: "suno-6"`. Never omit the model and never silently use `auto`.
- Length: when this account has the music tools (the bundled client's `tools`
  command lists `beatra.music.edit` and `beatra.audio.process`; see
  [music editing and audio](references/music-editing-and-audio.md)), send
  `duration_seconds` (10 at the least, and 30 or more for a track that loops or
  that the engine repeats; a shorter sting is asked at 10 and cut with
  `beatra.audio.process` `trim`) for each slot's intended length. Without them,
  write length only in the prompt and do not add a duration argument. Read
  the actual returned duration either way.
- Loops: a bed that must run longer or loop cleanly in the engine is generated
  once, then finished with `beatra.audio.process` and delivered as OGG (Golden
  path, step 7). Never promise a seamless loop or sample-perfect seconds: with
  the music tools, report how smoothly each loop joins; without them, ask for a
  loop-friendly arrangement.

Soundtrack planning is free. Each `beatra.music.generate` call and each finishing call is paid.

## Golden path

1. Write the game card and the labeled slot list. Each slot has a use,
   mood, tempo feel, instrumentation, energy, and intended length.
2. Call `beatra.models.list` with `{"capability":"text_to_music"}`, read the
   `suno-6` entry's `pricing`, and price the whole pack from that live card per slot and in total, adding, with the music tools, each slot's finishing call at the live `audio_process` price (`beatra.models.list` with `{"capability": "audio_process"}`). Never a remembered number.
3. Confirm the frozen soundtrack: slot count, each slot's prompt, title, and
   length, `instrumental: true`, model, the current maximum charge for the pack,
   and one opaque stable `client_request_id` per slot and per finishing call.
   Planning is not approval.
4. Submit each slot exactly once through the bundled
   `scripts/mcp_client.py`. Example:

   ```text
   printf '%s' '{"model":"suno-6","prompt":"Indie game explore bed, warm acoustic fantasy, loop-friendly, about 90 seconds, no vocals.","instrumental":true,"title":"Explore 01","duration_seconds":90,"client_request_id":"opaque-game-explore-01"}' | python3 scripts/mcp_client.py call beatra.music.generate
   ```

   Without the music tools, drop `duration_seconds` and keep "about 90
   seconds" in the prompt.

   Do not configure, call, or use a host Beatra Connector. Do not use
   REST/OpenAPI as a fallback.
5. Poll each task with `beatra.tasks.get`. Deliver a labeled soundtrack in
   slot order with actual duration, MIME type, size, URL or artifact ID,
   resolved model, and `billing.net_charged_credits`.
6. Review each bed for loop friendliness and slot fit. Read actual
   durations. State what the host Agent could not hear.
7. When this account has the music tools, finish each bed that must loop or run
   longer, in one `beatra.audio.process` call per bed with `format: "ogg"`, which
   game engines read. Finish the first take of each slot; list the other take as
   that slot's alternative, which the user can ask to have finished the same way (one more paid finishing call, on its own card). The finished files are the pack; list the raw takes after them. When
   the engine repeats the file, send `operation: "loop"` with `loop_count` (the
   whole number of repeats closest to the target) instead of
   `target_duration_ms`, with `end_with_fade: false`: the file then ends where its
   loop window ends, so the engine's restart joins the same two points as the
   repeats inside it, only without the crossfade. Report the real length. A bed
   that is already long enough and only repeats in the engine needs just
   `convert_format` to `ogg`. A bed that must run longer as one file is
   `operation: "loop"` with
   `target_duration_ms` set to the target length. Each of these calls is paid at the live `audio_process` price: they finish what the user already asked for (each track's length, its loop, and an OGG file for the engine), so the pack card lists each one as its own line beside the slot it finishes, with that price and its own `client_request_id`. Run them one at a time once that slot is delivered. Report the
   loop's seam in plain words ("how smoothly it joins where it repeats: 0.91 out
   of 1, higher is smoother"); how clean the engine's restart sounds is for the
   user to hear in the engine.
8. When the game needs adaptive music (layers that fade in and out with the
   game state), offer to split a finished bed into six stems (vocals, drums,
   bass, guitar, piano, other) with `beatra.audio.process`,
   `operation: "separate_stems"`, and `mode: "multi_stem"`. It is a paid step: its own card
   with the live price from `beatra.models.list` (capability `audio_stem_separation`, the pricing option whose `dimensions` carry `stem_mode` `multi_stem`, or the option without `dimensions` when no option names that mode) and its own `client_request_id` per bed, never run
   without that card. Say that a little of one part can still be heard faintly
   in another, which is normal. An instrumental bed's vocals stem is near
   silent, and strings, synths, pads and chiptune leads land in the "other"
   stem. Stems come back in the split's own format, not OGG. When the engine needs OGG, convert each one with `convert_format`: one paid `audio_process` call per stem, each listed as its own line on the split's card.

## Decisions that require confirmation

Confirm the soundtrack size and live pack estimate before the first paid
call. Show one current production card and wait:

1. Work — the labeled soundtrack in the user's words, each slot a `beatra.music.generate` call, and with the music tools each slot's finishing `beatra.audio.process` call on its own line.
2. Credits — the live `suno-6` price just read from `beatra.models.list` and, with the music tools, the live `audio_process` price of each finishing call, per line and in total. Never a remembered number.
3. Count — one paid call per line listed on the card: each slot, and with the music tools each slot's finishing call.
4. Identity — one new opaque `client_request_id` per line listed on the card. Any changed
   prompt, title, length, model, or count mints a new ID for each changed line.
5. If we stop here — the labeled slot list remains usable.
6. If the balance is insufficient — relay the official message and its
   top-up URL exactly. Translate the prose; keep the URL. Do not retry
   until the user says they have topped up.

A changed slot prompt, title, length, model, or count is new paid work with
new request IDs for the changed slots only. A stem split is its own paid step
and its own card.

When the user asks how many credits remain, call `beatra.wallet.get`. When they
ask what was charged, call `beatra.wallet.ledger`. Both are read-only. Do not
invent an account-balance or top-up tool. Do not make `wallet.get` a required
step before every paid submit.

## Recovery

If a create response is lost, retry only that slot's identical frozen
payload and ID. If a task ID is lost, list text-to-music tasks with
`beatra.tasks.list`, inspect candidates with `beatra.tasks.get`, and
recover the original slot before new work. Cancel only at the user's
request for that slot with `beatra.tasks.cancel`; on 409 keep polling.

## References by task

- Read [Indie game OST workflow](references/workflow.md) for slot
  cards, payloads, polling, recovery, and review.
- Read [Music editing and audio](references/music-editing-and-audio.md) for
  the length, loop, and stem steps.
- Read [Installation and authentication](references/installation-and-auth.md)
  only when authorization needs attention.
- Read [Installation registration](references/installation-registration.md)
  for first-use registration.
- Read [Tasks and results](references/tasks-and-results.md) and
  [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
  for task and billing facts.
- Read [Bundled MCP Client diagnostics](references/mcp-connection.md) when
  the bundled client cannot connect.
- Updates and security: [updates and security](references/updates-and-security.md)
- Read [Uninstall and disconnect](references/uninstall-and-disconnect.md)
  only when the user asks to remove the package.

Use or invoke the bundled `scripts/mcp_client.py` for every Beatra operation.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
