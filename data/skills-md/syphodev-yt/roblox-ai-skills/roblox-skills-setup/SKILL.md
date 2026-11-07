---
name: roblox-skills-setup
description: Set up the free Roblox game-creation skills on THIS machine - check which tools are installed (Python, Rojo, Wally, Lune, Selene, StyLua, Blender, the Roblox Studio MCP), walk the user through anything missing, then write each skill's personal LOCAL.md (folders, tool paths, rig file, VFX library location, env var names for keys) by asking the user and auto-detecting what it can, and finish with a smoke test. Use this the first time after installing the skills, whenever a skill says "LOCAL.md not found", when the user moves folders or installs a new tool, or when they ask "how do I set these skills up", "what do I need installed", or "why can't the skill find Blender/Rojo/my library".
---

# Set up the Roblox skills on this machine

The skills in this pack were written on someone else's computer. Everything
specific to a machine (where your games live, where Blender is, which rig you
animate, where your harvested VFX go) lives in one file per skill, `LOCAL.md`,
next to its `SKILL.md`. Each skill reads its `LOCAL.md` first. This skill
writes those files with the user, so nothing has to be edited by hand.

`LOCAL.md` belongs to the user. Never copy one into anything shared.

## Rules

- **Ask, do not assume.** Offer what you detected as the default, and let the
  user confirm or change it.
- **Never write a secret into a file.** API keys live in environment
  variables. `LOCAL.md` records only the variable NAME. Show the user how to
  set the variable themselves; do not ask them to paste a key into the chat.
- **Install nothing without a yes.** Explain what a missing tool is for and
  give the link or command; the user decides. Optional tools stay optional.
- **Only configure what they will use.** If they never want 3D models, skip
  Blender. Never set up Kaggle: its terms ban these skills' use. A skill they skip keeps its template and can be set up
  later by running this skill again.

## Step 1: check the machine

```bash
python ~/.claude/skills/roblox-skills-setup/scripts/check_setup.py
```

Show the user the table. If the Studio MCP line says it is not in Claude
Code's config files, that is not an error by itself: it is often registered
another way. The live check in Step 5 is what counts. Then ask which parts they want to use. A sensible
order for someone new:

1. **Code** (`roblox-code`): Rojo, Wally, Lune, Selene, StyLua. Free.
   Easiest route is a toolchain manager: install Rokit (or Aftman), then
   `rokit add rojo-rbx/rojo`, `rokit add UpliftGames/wally`,
   `rokit add lune-org/lune`, `rokit add Kampfkarren/selene`,
   `rokit add JohnnyMorganz/StyLua` (repo names can change; check each
   project's README). The scaffolder also writes these into the game's own
   toolchain file.
2. **Roblox Studio MCP.** The official one that ships with Roblox Studio. In
   Studio, enable it from the Assistant / MCP settings, then add it to Claude
   Code as the setup screen describes. Confirm with `claude mcp list`. Every
   skill that touches Studio uses this server; use one Studio connection at a
   time.
3. **UI, maps, VFX, SFX**: Python only, plus Studio.
4. **3D models and animation**: Blender 4.x. 3D models also need a GPU
   for the mesh step (a Hugging Face Space with `HF_TOKEN`). **Do not use Kaggle**: its terms ban this use and it got
   an account banned. Read `roblox-3d-model/references/licences.md` before
   using a model: some model licences exclude some regions or commercial use.
5. **Permanent uploads** (optional): a free Roblox Open Cloud API key with
   asset upload permission, in `ROBLOX_API_KEY`, and your `ROBLOX_USER_ID`.
   Without it, assets still work inside a Studio session.

## Step 2: environment variables (the user does this)

Tell them how, for their OS, and wait until they say it is done:

- Windows (PowerShell): `setx ROBLOX_API_KEY "paste-here"` then restart the
  terminal and Claude Code.
- macOS / Linux: add `export ROBLOX_API_KEY="paste-here"` to `~/.zshrc` or
  `~/.bashrc`, then open a new terminal.

Re-run `check_setup.py`; it reports "set" without showing the value.

## Step 3: write each LOCAL.md

For every installed skill the user wants, read its `LOCAL.template.md`, fill
each value with the user (detected default first), and write `LOCAL.md` in
the same folder. Keep the template's headings so the skill can find things. If a template says
the skill needs no machine settings, skip it; that skill is ready as installed.
Useful defaults to offer:

| Setting | Default to offer |
|---|---|
| Games folder | `~/Projects/Roblox-Games` (create it if they agree; the scripts look there by default, or wherever `ROBLOX_GAMES_HOME` points) |
| Blender | the path `check_setup.py` found |
| VFX library | `~/Roblox-VFX-Library` (OUTSIDE the skill folder, always) |
| SFX notes / picks | `~/Roblox-SFX` |
| R15 / R6 rig `.blend` | ask; there is no default. A free public rig works |

Add a short `## My preferences` section at the end of each `LOCAL.md` if the
user has any (art style, colours they like, things they never want). The
skills read it.

## Step 4: the VFX library (explain this, it surprises people)

`roblox-vfx` ships with **no effects**. It is a harvester: you build your own
library from VFX packs you have the right to use.

1. On the Creator Store, find free VFX packs you like and click **Get** so
   they are in YOUR inventory. This step is manual on purpose: Studio refuses
   to load an asset your account does not own, even a free one.
2. Open a test place, insert the packs from your Toolbox inventory.
3. Ask Claude to "harvest the VFX in this place" with `roblox-vfx`. It reads
   every emitter's properties out of Studio into JSON recipes in your library
   folder, then classifies them so you can search ("ice ring", "fire burst").
4. Check each pack's own terms before using its effects in a published game.

## Step 5: smoke test

Run what the user set up, and report pass/fail honestly:

- Code: scaffold a throwaway project with `roblox-code` and run its four
  gates (build, test, lint, format). All four should pass on a fresh scaffold.
- Map: `python scripts/prove.py minimal` in the `roblox-map` folder. Expect
  `RESULT: WARN` (only P11, empty space, which is normal for a two-deck test
  map). Then `python scripts/plan.py minimal --prove -o plan.png` and open it.
- UI: in the `roblox-ui` folder, `python scripts/ui_build.py examples/coin_hud.json --out build`
  and open `build/CoinHud.png`. Then `python scripts/verify_ui.py examples/coin_hud.json`
  should report 0 failures.
- Studio: with Studio open, ask for `get_studio_state` through the MCP.
- Blender: `blender --version` from the path in `LOCAL.md`.

Then tell the user the front door: `/create-roblox-game` with the kind of game
they want to make, or any single skill by name.

## Re-running

Safe to run any time. Never overwrite an existing `LOCAL.md` without showing
the user what would change and getting a yes.
