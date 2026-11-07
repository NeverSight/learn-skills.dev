---
name: pixverse-ai-image-and-video-generator
description: Generate and edit images, videos, speech, and music with PixVerse CLI; run effect templates, MiniApps, and connected Canvas workflows. Use for PixVerse generation, asset management, and creative production pipelines.
version: 1.34.0
homepage: https://pixverse.ai
source: https://github.com/PixVerseAI/skills
---

# PixVerse CLI

Generate media using the user's PixVerse account and credits. CLI access requires a subscription. Use `--json` for machine-readable results.

## Read only what the task needs

This is the entrypoint; the linked Markdown files are supporting instructions, not separately installed commands. Resolve links relative to this file, regardless of the working directory. Select one capability or workflow below; follow additional links only for a needed operation. Do not load the entire catalog, every related file, or all design references.

For a single operation, read its capability. For a multi-step deliverable, start with the workflow. Before executing a creation chain, read the [execution contract](references/execution-contract.md) once for output shapes, waiting, and recovery. For prompt advice or rewriting, select one strategy using the [prompt contract](references/prompt-contract.md).

## Setup and parameter discovery

1. Check `pixverse --version`. If missing, install with `npm install -g pixverse` (Node.js >= 22.12); an existing older installation need not be changed for unrelated tasks.
2. On CLI **1.4.0+**, query only the required mode/model: `pixverse capabilities create video --model v6 --json`. Use `pixverse capabilities create --json` to discover mode/model IDs if unknown. These queries are offline and need no login. Avoid the full `pixverse capabilities --json` bundle for a narrow task.
3. On older versions, use `pixverse create <mode> --help` and the relevant capability's static reference. This skill documents CLI 1.4.15; a static table does not prove an older installation supports a model or flag. If support cannot be established, report the required upgrade instead of submitting an invented combination.
4. Before account operations or generation, check `pixverse auth status --json` if login state is unknown. For `PIXVERSE_AUTH_PROFILE=chatgpt`, use [MCP pairing](references/auth-pairing.md) instead of ordinary login; retain this profile throughout the workflow. For ordinary login, run `pixverse auth login --json` and show the returned authorization URL; JSON mode does not open the browser automatically. See [auth and account](capabilities/auth-and-account.md) for access keys, configuration, and recovery.

Canvas capabilities and MiniApp schemas are live: query the relevant node/app before constructing a request. See [capability discovery](capabilities/capabilities.md). Do not infer Canvas node mappings from Create model names.

## Select an operation

| Task | Read |
|:---|:---|
| Text/image to video; reference generation or source-video editing | [create-video](capabilities/create-video.md) |
| Create or edit an image | [create-and-edit-image](capabilities/create-and-edit-image.md) |
| Modify a video at a keyframe | [modify-video](capabilities/modify-video.md) |
| Transfer motion from a video to a character | [motion-control](capabilities/motion-control.md) |
| Extend or upscale video | [post-process-video](capabilities/post-process-video.md) |
| Animate between keyframes | [transition](capabilities/transition.md) |
| Speech / voiceover | [create-voice](capabilities/create-voice.md) |
| Music / soundtrack | [create-music](capabilities/create-music.md) |
| Browse and run effects | [template](capabilities/template.md) |
| Discover and run preset apps | [miniapps](capabilities/miniapps.md) |
| Build, operate, or automatically arrange a Canvas graph | [canvas](capabilities/canvas.md) |
| Query/wait for an existing task | [task-management](capabilities/task-management.md) |
| Upload, inspect, download, or delete assets | [asset-management](capabilities/asset-management.md) |
| Organize saved folders | [saved-folders](capabilities/saved-folders.md) |
| Login, credits, usage, or creation defaults | [auth-and-account](capabilities/auth-and-account.md) |
| List or select workspaces | [workspace](capabilities/workspace.md) |

## Select a creative strategy

Explicit user constraints take priority over default creative advice. An instruction to optimize and generate authorizes that rewrite; an ordinary generation request does not authorize silently changing a supplied prompt. Do not run several optimizers sequentially.

| Task | Read |
|:---|:---|
| General prompt advice or models without a dedicated optimizer | [prompting-guide](capabilities/prompting-guide.md) |
| V6 prompt rewriting | [prompt-enhance](capabilities/prompt-enhance.md) |
| Seedance prompt structure, references, editing, or shot control | [seedance-prompt-optimize](capabilities/seedance-prompt-optimize.md) |
| Seedance emotional / atmospheric concept development | [seedance-vibe-creating](capabilities/seedance-vibe-creating.md) |
| Persistent characters | [character-design](capabilities/character-design.md) |
| Persistent props / items | [item-design](capabilities/item-design.md) |
| Mondo-style poster, cover, or album artwork | [mondo-poster-design](capabilities/mondo-poster-design.md) |

## Multi-step deliverables

| Task | Read |
|:---|:---|
| Text to finished video | [text-to-video-pipeline](workflows/text-to-video-pipeline.md) |
| Animate an existing image | [image-to-video-pipeline](workflows/image-to-video-pipeline.md) |
| Generate an image, then animate it | [text-to-image-to-video](workflows/text-to-image-to-video.md) |
| Iterative image edits | [image-editing-pipeline](workflows/image-editing-pipeline.md) |
| Modify, then enhance video | [modify-video-pipeline](workflows/modify-video-pipeline.md) |
| Motion transfer with post-processing | [motion-control-pipeline](workflows/motion-control-pipeline.md) |
| Video with optional extension, upscale, and soundtrack | [video-production](workflows/video-production.md) |
| Parallel or multi-output generation | [batch-creation](workflows/batch-creation.md) |
| Mondo poster production | [mondo-poster-pipeline](workflows/mondo-poster-pipeline.md) |
| Animate a Mondo poster | [mondo-poster-to-video-pipeline](workflows/mondo-poster-to-video-pipeline.md) |
| Four-shot storyboard and final edit | [storyboard-to-video](workflows/storyboard-to-video.md) |

## Execution essentials

- Create normally waits for completion. Save its result; do not create again to extract an ID or wait again for a completed result. For background work use `--no-wait`, retain all IDs, then wait/query existing tasks.
- Preserve the requested model, region, workspace, and creative constraints. Query supported parameters before selecting replacements. Text inputs (`--prompt`, `--text`, `--lyrics`) accept literal text, a file path, or `-` for stdin.
- `PIXVERSE_REGION` overrides `--region`; default is `global`. Login, active workspace, and creation defaults are isolated by region. CN does not support standalone voice/music or audio asset/task operations; model availability also differs. See the selected capability before submission.
- `--workspace-id <id>` overrides workspace for one invocation; `0` is personal. If the CLI resets an inaccessible active workspace to personal, re-establish the intended destination before retrying team work.
- Preserve successful outputs on partial failure. A nonzero exit can accompany usable batch results. A timeout is not proof of a failed submission. Follow the [execution contract](references/execution-contract.md), not a blind create retry.

For Windows shell syntax, see the [PowerShell pipeline](examples/windows/powershell-text-to-video.ps1). For updating this skill checkout, run [update.sh](scripts/update.sh) only from a clean `main` checkout; it supports fast-forward updates and does not stash or switch branches.
