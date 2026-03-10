---
name: remix-agent-publish
description: Build and publish Remix games via the v1 REST API and Remix Game SDK
metadata:
  tags: remix, games, api, agent, publishing
---

## When to use

Use this skill when users want to automate game publishing on Remix (`remix.gg`) from AI agents or external services.

## How to use

- Read the `remix-api-auth` skill for authentication setup.
- Fetch OpenAPI spec at `https://api.remix.gg/docs/json` before generating API calls.
- Use the `remix-api-reference` skill for workflow guardrails (not as the method/path source of truth).
- For Phaser builds, use the `phaser-2d-arcade` skill.
- For lightweight 3D builds, use the `threejs-lite` skill.
- Use the `remix-game-sdk` skill when generating or fixing game code.
- Apply the `remix-submission-rules` skill for validation requirements.
- Follow the `remix-game-best-practices` skill for mobile-first and SDK-safe implementation.
- Use the `remix-rest-snippets` skill for client integration examples.
- Use the `remix-mcp-quickstart` skill for assistant workflows.

## Available Workflows

- `remix-game-creation` - Create a new game draft
- `remix-upload-game` - Upload version code
- `remix-add-image` - Generate and add images to a game
- `remix-add-sprite` - Generate and add sprites to a game
- `remix-shop-items` - Create and manage in-game shop items
- `remix-multiplayer` - Enable multiplayer support
- `remix-save-game` - Add save/load game state
- `remix-upload-asset` - Upload images, audio, or 3D models as hosted game assets

## Game Settings

Games can include a `.remix-settings.json` file for configuration. See workflow files for details on when and how to use game settings.

## Inline Validation

Before uploading code, run through the validation checklist in the `remix-submission-rules` skill to catch blockers early.

## REST API Workflow

All game management is done through REST API calls to `https://api.remix.gg`. The general pattern is:

1. Fetch the OpenAPI spec at `https://api.remix.gg/docs/json`
2. Use the spec to determine exact methods, paths, and schemas
3. Make authenticated REST calls with your API key
4. Check responses for success/error envelopes

See the `remix-rest-snippets` and `remix-api-reference` skills for details.

## Source of truth

When docs and runtime behavior disagree, defer to the server API source and OpenAPI docs:

- `https://api.remix.gg/docs`
- `https://api.remix.gg/docs/json`
- `apps/server-api/routes/agents.ts`
- `apps/server-api/lib/api-auth.ts`
- `apps/server-api/lib/agent-api.ts`
- `apps/server-api/app/[...path]/route.ts`
- `@remix-gg/sdk` (NPM package)
