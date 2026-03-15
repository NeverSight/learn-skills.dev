---
name: playdate-dev
description: Playdate game development in Lua with the Playdate SDK, including game loop, sprites, graphics, input (crank, buttons, accelerometer), UI, performance, metadata (pdxinfo), and simulator/device workflow. Use when asked to make a Playdate game, implement Playdate-specific mechanics, or apply Playdate design and accessibility guidelines.
---

# Playdate Dev

## Overview
Build and troubleshoot Playdate games in Lua with Playdate-specific constraints, input, and SDK workflows.

## Quick Start Workflow
1. Clarify the request scope (gameplay goal, target device vs simulator, SDK version, release vs prototype).
2. Choose inputs and accessibility (buttons, crank, accelerometer; provide alternatives; respect reduce-flashing setting).
3. Choose rendering approach (sprites vs immediate draw, image sizes, refresh rate, 1x vs 2x scale).
4. Implement the core loop (define `playdate.update()`, update game state, call `playdate.graphics.sprite.update()` and `playdate.timer.updateTimers()` when used).
5. Add metadata and launcher assets (`pdxinfo`, buildNumber, launcher card and icon sizes).
6. Test in the Simulator and on hardware (screen legibility, crank feel, audio balance, performance).

## Starter Project
- Copy `assets/lua-starter` into a new project folder.
- Keep `Source/main.lua` and `Source/pdxinfo` in the source root.
- Replace placeholder values in `pdxinfo` and extend the update loop.

## Implementation Notes
- Use `references/inside-playdate-lua.md` for Lua API names, file layout, and workflow details.
- Use `references/designing-for-playdate.md` for screen, text, input, audio, UI, and launcher guidance.
- Use Context7 `/websites/sdk_play_date` to spot-check API changes, then confirm Lua behavior in the latest SDK docs.

## Resources
- `references/designing-for-playdate.md`
- `references/inside-playdate-lua.md`
- `assets/lua-starter/`
