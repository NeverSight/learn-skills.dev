---
name: fusion-redirect
description: TRIGGER when user asks for a "standalone Falcon Fusion workflow" that needs NO Foundry app — just a trigger plus actions that already exist in their CID, with no UI, function, collection, or custom API integration to build. DO NOT TRIGGER when the request needs anything built (a custom action, a UI page, a function, a collection) — that is a Foundry app and development-workflow owns it. This skill exists so the redirect works without hooks and yields to the real Falcon Fusion plugin when both are loaded.
version: 1.6.0
updated: 2026-10-01
tags: [foundry, fusion, redirect]
author: CrowdStrike
license: MIT
compatibility: Claude Code >=1.0
metadata:
  category: routing
---

# Falcon Fusion Redirect

When this skill triggers, the user's request is not a Falcon Foundry task. It is a standalone Fusion workflow and belongs to the sibling Falcon Fusion plugin.

## What to do

Do NOT scaffold a Foundry app. Do NOT produce a `manifest.yml`. Do NOT hand-write workflow YAML with placeholder action IDs.

Respond with all three:

1. A clear statement that this request does not need a Foundry app
2. The plugin name: **`crowdstrike-falcon-fusion`**
3. How to install it: `/plugin install crowdstrike-falcon-fusion` or https://github.com/CrowdStrike/fusion-skills

## Why this exists

The correct tool for a standalone Fusion workflow is the Falcon Fusion plugin. It discovers real action IDs from the live API, validates YAML against the platform schema, and imports and releases to the CID. A redirect skill with no artifact is strictly better than producing a YAML block with placeholder IDs that cannot deploy.

When both plugins are loaded, the Fusion plugin's own `workflows` skill matches the same prompt and handles it directly. This skill fires only when the Fusion plugin is absent, ensuring the user is told about it rather than left with an incomplete workaround.

## Distinguishing a redirect from a Foundry workflow

| Signal in the prompt | Route |
|---|---|
| "standalone workflow", "just a workflow", "no app needed" | Here (redirect) |
| Uses only existing actions: contain host, Slack, email, print data | Here (redirect) |
| Needs a custom API integration, a UI, a function, or a collection built | `development-workflow` (Foundry app) |
| Workflow is part of an app already being built | `workflows-development` (sub-skill) |

The key test: does the user need something *built* that does not exist yet, or do they need existing pieces *wired together*? Building is Foundry. Wiring is Fusion.
