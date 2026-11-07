---
name: Figma
description: Control Figma from the shell via Flue - a plugin bridge to the Figma Plugin API without an MCP server.
---
This skill lets a coding agent operate **Figma** (desktop app) through [Flue](https://github.com/SFKislev/flue), a local shell-to-application bridge. The agent runs `figma_bridge.py` commands (compact `build`, `tree`, `set`, `shot`, `sheet`, or raw JS with `eval`) and gets structured JSON back. A small development plugin, **Flue Bridge**, runs in the open file and carries the jobs into the Plugin API.

> agent shell -> `figma_bridge.py` -> local daemon <- polled by the Flue Bridge plugin -> Figma Plugin API

## When to use
The human requests work performed **inside Figma** - inspect the open file, build or restyle frames and components, apply effects, import images, review a design visually. A CLI agent cannot act inside Figma without a bridge like Flue.

## How to proceed
1. **Read `FLUE.md` in this directory first.** It explains how Flue works, the bridge contract and safety expectations.
2. **If Flue is installed:** also read `adapters/figma_adapter/APP.md` (commands, spec format, connection recovery) and, for visual design work, `adapters/figma_adapter/docs/design-recipes.md`.
3. **If Flue is not installed:** tell the human. The install command is `pip install flue && flue setup`. Do not install without explicit approval in the current session.
4. **First run:** the human imports the plugin once (Figma desktop > Plugins > Development > Import plugin from manifest...) and opens it in the file. Then `figma_bridge.py pair` approves it; no code to type.

## Other apps
Flue also supports Photoshop, Illustrator, Premiere, After Effects, InDesign, Audition, Blender, Houdini, 3ds Max, Unity, and Microsoft Office through the same contract. One install covers all adapters.

## Safety
Flue acts inside the human's live design file. Treat the human as the driver; prefer small, inspectable steps; every call is one undo step; do not save, publish or delete unless explicitly asked. Flue is MIT-licensed and reviewable on GitHub / PyPI before use.
