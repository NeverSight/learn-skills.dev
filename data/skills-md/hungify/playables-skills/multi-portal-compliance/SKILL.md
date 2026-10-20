---
name: multi-portal-compliance
description: Validate and port HTML5 web games across YouTube Playables, Poki, CrazyGames, GameDistribution, and Yandex Games using platform certification rules.
---

# Multi-Portal Compliance & Publishing Skill

Use this skill when building, auditing, or packaging this web game for **YouTube Playables**, **Poki**, **CrazyGames**, **GameDistribution**, or **Yandex Games**.

## Reference Checklists

- `references/upload-requirements-youtube.md` — YouTube Playables certification rules
- `references/upload-requirements-poki.md` — Poki upload & SDK rules
- `references/upload-requirements-crazygames.md` — CrazyGames upload & SDK rules
- `references/upload-requirements-gamedistribution.md` — GameDistribution upload & SDK rules
- `references/upload-requirements-yandex.md` — Yandex Games upload & SDK rules

## Sibling Portal SDK Skills (Installed in `.claude/skills/`)

- `youtube-playables-js-sdk` — Official `ytgame` v1 lifecycle, cloud save, audio, pause/resume, ads
- `poki-js-sdk` — PokiSDK lifecycle, commercialBreak, rewardedBreak
- `crazy-games-js-sdk` — CrazyGames SDK v3 ads, data, game events
- `game-distribution-js-sdk` — `gdsdk` integration
- `playgama-bridge-js-sdk` — Unified single-API bridge supporting YouTube, Poki, CrazyGames, Yandex, GD

## Automated Build & Certification Check

Run `bun run validate` (or `bun run zip`) before uploading to verify:

1. `index.html` exists at root and loads `https://www.youtube.com/game_api/v1` first.
2. Zero absolute asset paths (`/assets/...`) in built output.
3. All filenames strictly match `^[A-Za-z0-9_.-]+$`.
4. Total file count ≤ 8,000, single file < 30 MiB (warn > 512 KiB), initial/total bundle < 15 MiB / 250 MiB.
