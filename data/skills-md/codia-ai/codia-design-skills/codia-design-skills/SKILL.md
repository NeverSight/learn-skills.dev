---
name: codia-design-skills
description: Create, edit, enhance, convert, and manage images, design resources, and visual assets with Codia Design Skills and the Codia Open API. Use when the user asks to generate images, posters, campaign creatives, product listing images, ecommerce assets, banners, thumbnails, or social variants; edit images by removing backgrounds, replacing backgrounds, erasing objects, removing authorized watermarks, upscaling, reframing, remixing, or using reference images; convert screenshots, UI mockups, images, PDFs, reports, or documents into editable design data, layers, PPTX slides, or SVG/vector assets; inspect or describe images; or manage Codia CLI setup, authentication, credits, usage, limits, and auto recharge.
version: 0.1.4
---

# Codia Design Skills

This is the root router skill for the Codia Design Skills pack. In the normal `npx skills add` install flow, agents load this top-level skill first. The feature and workflow skills under `skills/` are supporting instructions that this router reads when the request needs a specific capability.

Use Codia through the local `codia-design` CLI. The CLI performs authenticated requests to Codia Open API and writes local downloads when commands return files.

## Runtime Setup

Before running a Codia command, check whether the CLI is available.

macOS / Linux:

```bash
command -v codia-design
```

Windows PowerShell:

```powershell
Get-Command codia-design -ErrorAction SilentlyContinue
```

If `codia-design` is missing and the user allows global npm installs, install the runtime:

```bash
npm install -g @codia-ai/codia-design-cli
```

Then verify:

```bash
codia-design --help
codia-design auth status
```

If global npm install is blocked, tell the user to run the same install command manually, then continue after they confirm it is installed.

## Authentication

Check auth before billable work:

```bash
codia-design auth status
```

If disconnected, prefer browser login:

```bash
codia-design auth login --platform codex
```

If browser login is unavailable and the user provides an API key, bind it without echoing the value:

```bash
codia-design auth set --api-key api_key_xxx
```

The CLI stores auth state in `~/.codia/design-skills/config.json`. Never print this file or API keys.

## Routing Rules

Read the matching child skill before running commands that need parameters, model choices, polling behavior, or multi-step sequencing. Resolve paths relative to this root `SKILL.md`.

| User intent | Read |
|---|---|
| Broad Codia setup, auth, account checks, or fallback routing | `skills/codia-design/SKILL.md` |
| Product launch packs, ecommerce listing assets, marketplace visuals | `skills/codia-product-assets/SKILL.md` |
| Campaign posters, launch visuals, social creative sets, multi-size adaptations | `skills/codia-campaign-assets/SKILL.md` |
| PDF/report/document to editable design data, PPTX deck, or both | `skills/codia-document-deck/SKILL.md` |
| Text-to-image generation, posters, campaign visuals, backgrounds | `skills/codia-image-generate/SKILL.md` |
| Image-to-image generation from one or more references | `skills/codia-image-image-to-image/SKILL.md` |
| Controlled visual variations from an existing image | `skills/codia-image-remix/SKILL.md` |
| Reframe or adapt images to new aspect ratios | `skills/codia-image-reframe/SKILL.md` |
| Upscale or improve final image quality | `skills/codia-image-upscale/SKILL.md` |
| Remove image backgrounds or create transparent PNG cutouts | `skills/codia-remove-bg/SKILL.md` |
| Replace backgrounds with studio, lifestyle, or campaign scenes | `skills/codia-image-replace-bg/SKILL.md` |
| Erase unwanted objects, clutter, or defects from authorized images | `skills/codia-image-object-erase/SKILL.md` |
| Remove watermarks or overlays from authorized images | `skills/codia-image-watermark-remove/SKILL.md` |
| Describe, inspect, caption, or analyze an image | `skills/codia-image-describe/SKILL.md` |
| Convert screenshots, UI mockups, posters, or images into editable design data | `skills/codia-image-to-design/SKILL.md` |
| Convert images into Codia layering DSL | `skills/codia-image-layering/SKILL.md` |
| Convert selected PDF pages into editable design data | `skills/codia-pdf-to-design/SKILL.md` |
| Convert selected PDF pages into a downloadable PPTX deck | `skills/codia-pdf-to-ppt/SKILL.md` |
| Vectorize logos, icons, or images into SVG | `skills/codia-svg/SKILL.md` |
| Check credit balance | `skills/codia-credits/SKILL.md` |
| Inspect usage records and recent task costs | `skills/codia-usage/SKILL.md` |
| Read or update automatic recharge settings | `skills/codia-auto-recharge/SKILL.md` |

Prefer a workflow skill when the user asks for a real outcome with multiple deliverables. Prefer a feature skill when the request is a single clear operation.

## Common Workflow Choices

Use `skills/codia-product-assets/SKILL.md` when the user wants a product or ecommerce deliverable such as a listing image set, product launch asset pack, store banner, white-background product tile, or lifestyle scene variants.

Use `skills/codia-campaign-assets/SKILL.md` when the user wants campaign or social creative, such as a poster plus adapted 1:1, 4:5, 9:16, banner, or thumbnail versions.

Use `skills/codia-document-deck/SKILL.md` when the user wants to turn PDFs, reports, screenshots, or existing design files into editable design data, a PPTX deck, or both.

## Command Rules

- Prefer local file paths when the user provides local assets.
- Use `--out` for large JSON responses.
- Use `--download-dir DIR` when the user asks where outputs should go.
- Use `--no-download` only when the user explicitly wants JSON-only behavior.
- For PDFs, Codia page numbers are zero-based: page `0` is the first page.
- For `pdf-to-ppt`, use the CLI polling/download flow and validate the returned PPTX. Do not rasterize the PDF locally or create a substitute deck unless the user explicitly asks for a local fallback.
- For image generation, keep the first call simple when the user has not specified model or size. The CLI default is `seedream_5` at `2560x1440`.
- For watermark or object removal, proceed only when the image is user-owned or otherwise authorized.

## Account And Cost Checks

The CLI uses the public Open API v2 surface (`/v2/open/*`) and estimates billable credit cost before paid operations. After a billable command, it may query credits and warn if the remaining balance is low. That warning should not block the requested work unless the API itself rejects the request.

Useful commands:

```bash
codia-design credits
codia-design usage --page 1 --page_size 20
codia-design limits
```

## Output Expectations

Report the concrete result: local output file paths, downloaded PPTX path, image files, returned URLs, task IDs, and any API error messages. Do not include secrets, raw auth config, or unnecessary full JSON when a compact summary is enough.
