---
name: remix-mcp-quickstart
description: Quickstart workflow for AI assistants using Remix publishing APIs
metadata:
  tags: remix, mcp, quickstart
---

## Recommended Flow

Base URL: `https://api.remix.gg`

1. Fetch OpenAPI JSON from `https://api.remix.gg/docs/json`.
2. Resolve exact methods/paths/schemas from the spec.
3. `GET /v1/metadata/categories` to fetch valid category enums.
4. `POST /v1/games`
5. Build game code against `window.RemixSDK` requirements, including SDK `<script>` in HTML `<head>` (`https://cdn.jsdelivr.net/npm/@remix-gg/sdk@latest/dist/index.min.js`) (see the `remix-game-sdk` skill)
6. Set required metadata:
   - Name: game metadata APIs
   - Category: game metadata APIs (1-3)
   - Icon: upload via `POST /v1/games/{gameId}/assets` or in Remix Studio/app flow
7. Upload binary assets (icon/sprites/audio) via `POST /v1/games/{gameId}/assets` or in Remix Studio/app flow.
8. `GET /v1/games/{gameId}/assets` to confirm hosted asset URLs.
9. `POST /v1/games/{gameId}/versions/{versionId}/code`
10. `GET /v1/games/{gameId}/versions/{versionId}/validate`
11. Optional: `GET /v1/games/{gameId}/launch-readiness?versionId={versionId}`
12. If blockers exist, patch code/metadata and repeat validation
13. `GET /v1/games/{gameId}/versions/{versionId}/status`

## Discovery / Inspection Endpoints

- `GET /v1/games`
- `GET /v1/games/{gameId}`
- `GET /v1/games/{gameId}/versions`
- `GET /v1/games/{gameId}/versions/{versionId}`
- `GET /v1/games/{gameId}/versions/{versionId}/code`
- `GET /v1/games/{gameId}/versions/{versionId}/thread`
- `GET /v1/games/{gameId}/assets`
- `GET /v1/games/{gameId}/items`

## Guardrails

- Never skip validation checks.
- Treat `blockers[]` as source of truth.
- Do not trust cached path/method memory when OpenAPI is available.
- Do not create extra versions from agent REST.
- Do not submit from agent REST.
- If docs are stale, check `https://api.remix.gg/docs`.
