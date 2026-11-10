---
name: minecraft-bot-qa
description: "Automated QA playthroughs of a Minecraft server with bot players on both Java (Mineflayer) and Bedrock (bedrock-protocol via Geyser/Floodgate). Use for joining a dev server as a bot, walking NPC dialogue, clicking every menu and GUI button, recording structured logs, judging results with deterministic assertions plus an optional Laya second opinion, and running an offline self-test of the tooling."
---

# Minecraft Bot QA Skill

## Scope

Use this skill to test a Minecraft 1.21.x server the way a player experiences it, with bots that join over the
real network path, and to judge the recorded results. It ships a Java bot kit, a Bedrock bot kit, a mock Bedrock
server, deterministic judges, an optional [Laya](https://huggingface.co/convaiinnovations/laya) second-opinion
model, and a worked example from a real quest server.

### Routing Boundaries
- `Use when`: the task is playing through quests or NPC dialogue with bots, clicking through chest or form menus on Java and Bedrock, checking that crossplay players see the same content, regression-testing a dev server, or judging bot logs.
- `Do not use when`: the task is writing plugin code or unit tests (`minecraft-plugin-dev`, `minecraft-testing`), operating or tuning the server itself (`minecraft-server-admin`), Geyser/Floodgate setup and triage (`minecraft-crossplay-ops`), or load-testing with many bots.

## Quick Start

All commands run from this skill directory. Bots need Node.js 20 or newer (Bedrock needs Node.js 24 or newer).

```bash
npm install --prefix ./scripts
node ./scripts/check-bot-setup.mjs --selftest
```

The self-test starts the bundled mock Bedrock server, runs the Bedrock menu bot against it, and judges the result.
It expects the healthy run to pass and a deliberately broken run (unresolved `%placeholders%`) to fail. If both
behave, the tooling works on your machine. Nothing touches a real server.

Optional second opinion from Laya:

```bash
python -m pip install -r ./scripts/requirements.txt
node ./scripts/check-bot-setup.mjs --selftest --with-laya
```

Every judge also works without Laya. Pass `--no-laya` (or set `NO_LAYA=1`) to skip it on purpose.

## Where Output Goes

Logs, results and sign-in caches are written to `QA_OUT_DIR` (default `./.bot-qa` in the current directory),
never inside the skill folder. Point it at your project:

```bash
export QA_OUT_DIR=./qa-output
```

Keep that folder and any `auth-cache*` folder out of Git. They can hold sign-in tokens and player names.

## Workflow A: Bedrock Menu Click-Through

The bot joins as a Bedrock player, runs your menu command, and presses every button of every form depth-first,
reopening the menu for each press. It never presses buttons that match the destructive pattern.

```bash
export BEDROCK_HOST=dev.example.net
export BEDROCK_PORT=19132
export BEDROCK_AUTH=microsoft
export PANEL_DIR=./path/to/your/panels
export MENU_COMMAND=/menu
node ./scripts/bedrock/bedrock_ping.js
node ./scripts/bedrock/bedrock_gui.js MyBedrockTester RUN1
python ./scripts/judges/judge_bedrock.py ./qa-output/results/bedrock-RUN1.json
```

- `PANEL_DIR` holds your CommandPanels-style YAML files. The judge compares what the bot saw against them.
- Use `BEDROCK_AUTH=offline` only on a test server with online-mode off.
- The Microsoft device code is written to `logs/msa-code-bedrock.txt` under `QA_OUT_DIR`. Open the link, enter the code, and the bot continues.
- Details, knobs and protocol notes: [references/bedrock-bots.md](references/bedrock-bots.md).

## Workflow B: Java Bot Walkthrough

`scripts/java/lib.js` gives you `connect`, a structured JSON-lines event log, pathfinding, and a vanilla-accurate
entity right-click. Build scenarios from it, or start with the probes.

```bash
export QA_HOST=dev.example.net
export QA_PORT=25565
export QA_AUTH=microsoft
node ./scripts/java/auth_only.js
node ./scripts/java/probe.js MyJavaTester
node ./scripts/java/explore_npc.js MyJavaTester "Example Guide" 25
```

- Put NPC spawn points in a JSON file and point `QA_NPCS` at it (see `scripts/java/npcs.example.json`).
- `scripts/java/dialogue.js` drives Typewriter-style chat dialogue (hotbar scroll plus jump to confirm) and `strategies.js` picks progressing answers with no model in the loop.
- Details: [references/java-bots.md](references/java-bots.md).

## Workflow C: Full Bedrock Quest Bot

`scripts/bedrock/bedrock_quest.js` is a thin Bedrock protocol client with a local control API and live dashboard, so
an operator (or an agent) can drive a quest step by step: move, click NPCs and blocks, craft, answer forms, write books.

```bash
export BOT_NAME=QuestBot
export CTRL_PORT=8777
node ./scripts/bedrock/bedrock_quest.js
```

Then open `http://127.0.0.1:8777/` for the timeline, or call `GET /do?c=state` and `GET /do?c=nearby%208` from any script.
The verb list and the protocol lessons behind it are in [references/bedrock-bots.md](references/bedrock-bots.md).

## Judging

Deterministic assertions are the ground truth: buttons match the menu files, no `%placeholders%`, no `null` or
stack traces in player text, every pressed button responds. Laya adds a second opinion on text quality and on each
form outcome, and it never overrides a failed assertion. Exit code `0` means the deterministic checks passed.
See [references/laya-judge.md](references/laya-judge.md) to install Laya, write your own assertions, or read results.

## Safety Rules

1. Run bots on a development server, never on a live server with real player data.
2. Use throwaway test accounts. Never commit `auth-cache*` folders, logs or results.
3. Take a locked backup before any run that can write to the world or to player data, and keep a way back.
4. Do not press destructive menu buttons; keep `MENU_DESTRUCTIVE` accurate for your menus.
5. Say plainly what was and was not verified. A bot cannot confirm visuals such as holograms, particle effects or how a real Bedrock client renders a UI.

The full dev-server routine (backups, reset, throttles, operator handoffs) is in
[references/dev-server-workflow.md](references/dev-server-workflow.md).

## Worked Example

`scripts/examples/quest-server/` holds the scenarios from a real Bible-themed Java and Bedrock quest server:
NPC story walkers, altar and basin offerings, flying to a menorah, crafting bread, signing a prayer book, the
final quiz, GUI click-throughs, and the story-specific judges. They show how to compose the core scripts and are
not meant to run against other servers. Walkthrough: [references/quest-server-example.md](references/quest-server-example.md).

## Troubleshooting

- `npm install` fails on `raknet-native`: the native RakNet build needs a compiler. Run `npm install --ignore-scripts --prefix ./scripts`; the Bedrock kit falls back to the pure-JS backend automatically (or set `BEDROCK_RAKNET=jsp-raknet`).
- Bedrock bot never spawns: check the UDP port with `bedrock_ping.js`, pin `BEDROCK_VERSION` if Geyser lags the client, and use `BEDROCK_WAIT=join` for mock servers.
- Bedrock block clicks do nothing: the client must keep sending movement input. The quest bot already does; custom bots must too.
- "You're opening panels too quickly": raise `BEDROCK_PANEL_GAP_MS`.
- Java bot kicked for version: set `QA_VERSION` to the server version, or leave it unset to auto-detect.

## Credits

This skill is built on open-source projects. It installs them as dependencies and does not copy their code.

- [Mineflayer](https://github.com/PrismarineJS/mineflayer) by PrismarineJS (MIT) drives the Java bots.
- [bedrock-protocol](https://github.com/PrismarineJS/bedrock-protocol) by PrismarineJS (MIT) drives the Bedrock bots.
- [Laya](https://github.com/NandhaKishorM/laya) by Nandha Kishor M and Convai Innovations (Apache-2.0; model on [Hugging Face](https://huggingface.co/convaiinnovations/laya)) gives the optional second opinion in the judges.
- Forks kept for reference: [AIKUSAN/mineflayer](https://github.com/AIKUSAN/mineflayer), [AIKUSAN/bedrock-protocol](https://github.com/AIKUSAN/bedrock-protocol) and [AIKUSAN/laya](https://github.com/AIKUSAN/laya). The kit installs the upstream releases, not the forks.
- [Geyser and Floodgate](https://geysermc.org) from the GeyserMC team let Bedrock players join Java servers.
