---
name: genviral
description: Complete genviral Partner API automation. Create and schedule posts (video + slideshow) across TikTok, Instagram, and any supported platform. Includes slideshow generation, file uploads, template/pack management, analytics, and full content pipeline automation.
homepage: https://github.com/fdarkaou/genviral-skill
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: ["curl", "jq", "bash"]
---

# genviral Partner API Skill

> **TL;DR:** Wraps genviral's Partner API into 60+ bash commands. Core flow: `get-pack` → analyze images (metadata + vision) → `generate` with `pinned_images` → `render` → visual review (hard gate) → `create-post` → log to `workspace/performance/log.json`. TikTok copy flow: `copy-tiktok-preview` → `copy-tiktok-import` (with exactly one of `pack_id` or `pack_images`). Studio AI: `studio-models` → `studio-generate-image` (sync) or `studio-generate-video` → `studio-video-status --poll` (async). Folders: `create-folder` → `folder-items-add` to organize files/slideshows. Analytics correlation: treat `analyticsId`/`id`, `platformPostId`, and `genviralPostId` as different identifiers; use `genviralPostId` or `externalId` to map analytics rows back to created posts. Auth via `GENVIRAL_API_KEY`. Config in `defaults.yaml`. Instance data in `workspace/`.

## What This Skill Does

- **Multi-Platform Posting:** Video or slideshow posts across TikTok, Instagram, YouTube, Pinterest, LinkedIn, Facebook
- **Studio AI Generation:** Generate images (sync) and videos (async) via AI models through the API
- **File Management:** Upload videos/images to genviral's CDN; organize with folders
- **Folder Management:** Nested folders for uploads, AI images, AI videos, and slideshows
- **AI Slideshow Generation:** Photo carousels from prompts, rendered to images
- **Template System:** Reusable slideshow structures, convert winners to templates
- **Pack Management:** Image packs as slideshow backgrounds
- **Analytics:** KPIs, post-level metrics, tracked accounts, refresh triggers
- **Niche Intelligence:** One-call trend research (`trend-brief`) for hashtags, sounds, creators, posting windows, and hook angles
- **Content Pipeline:** Full automation from prompt to posted content
- **Performance Tracking:** Post log, hook tracking, weekly review
- **Hook Library:** Maintain and evolve a library of proven content hooks

## How It Works

1. Generate or upload media
2. Create a post targeting one or more accounts
3. Schedule or publish (for TikTok slideshows, optionally save as drafts so you can add trending audio before publishing — music selection requires human judgment for best results)
4. Track performance via analytics
5. Learn and optimize

Important analytics identity rule:
- `analyticsId` is the analytics-row ID (`id` is a legacy alias of the same value)
- `platformPostId` is the platform-native post/video ID
- `genviralPostId` is the originating Genviral post ID when correlation succeeds
- `externalId` is the originating Partner API `external_id` when present
- For BYO TikTok `MEDIA_UPLOAD`, the draft/inbox `publish_id` is not the final public TikTok video ID. Correlation is best-effort for recent unresolved drafts after the user actually publishes in TikTok, so older rows can still show `genviralPostId` / `externalId` as `null`.

All configuration in `defaults.yaml`. Secrets via environment variables. Everything posted shows up in the Genviral dashboard.

## First-Time Setup

If fresh install, read `docs/setup.md` and walk the user through onboarding conversationally:
1. Set API key and verify it works
2. List accounts and pick which to post to
3. Discuss image strategy (existing packs, create new, generate per post, or mix)
4. Optionally set up product context and brand voice together

No hardcoded defaults. Ask the user what they prefer and adapt. Everything done through this skill shows up in the Genviral dashboard, so the user always has full visibility and control.

## File Structure

```
genviral/
  SKILL.md                  # This file (kernel + routing)
  README.md                 # Human-facing overview
  defaults.yaml             # API config and defaults

  docs/
    setup.md                # Onboarding guide (conversational, 5 phases)
    api/
      accounts-files.md     # accounts, upload, list-files
      folders.md            # folder CRUD, move, ancestors, items management
      posts.md              # create-post, update-post, retry, list, get, delete
      slideshows.md         # generate/render/update + TikTok copy preview/import + text styles
      packs.md              # pack CRUD + smart image selection (MANDATORY reading for any pack workflow)
      templates.md          # template CRUD + create-from-slideshow
      analytics.md          # all analytics commands
      studio.md             # Studio AI: generate images/videos, list models, poll status
      subscription.md       # subscription status, credits, tier
      pipeline.md           # content pipeline, performance loop, CTA testing, platform tips
      errors.md             # error codes and troubleshooting
    references/
      analytics-loop.md     # Full analytics feedback loop and weekly review process
      competitor-research.md # How to research competitors
    prompts/
      slideshow.md          # Prompt templates for slideshow generation
      hooks.md              # Prompt templates for hook brainstorming

  workspace/                # All instance/customer data (override with GENVIRAL_WORKSPACE_DIR)
    content/
      scratchpad.md         # Working content plan and drafts
      calendar.json         # Upcoming planned posts
    context/
      product.md            # Product description, value props, target audience
      brand-voice.md        # Tone, style, do's and don'ts
      niche-research.md     # Platform research for the niche
    hooks/
      library.json          # Hook instances (grows over time, tracks performance)
      formulas.md           # Hook formula patterns and psychology
    performance/
      log.json              # CANONICAL post record (single source of truth)
      hook-tracker.json     # Hook and CTA tracking with metrics (the feedback loop)
      insights.md           # Agent learnings from performance data
      weekly-review.md      # Weekly review notes
      competitor-insights.md # Competitor research findings

  scripts/
    genviral.sh             # Main API wrapper (all commands)
    update-skill.sh         # Self-updater
```

## Command Routing

Load only what you need for the current task:

| Task | Read |
|------|------|
| Account discovery, file upload | `docs/api/accounts-files.md` |
| Folder management (create, list, move, delete, items) | `docs/api/folders.md` |
| Create, update, list, delete posts | `docs/api/posts.md` |
| Slideshow generation, TikTok copy import, rendering, editing, text styles | `docs/api/slideshows.md` |
| Pack management, image selection (ANY pack workflow) | `docs/api/packs.md` |
| Template creation and management | `docs/api/templates.md` |
| Analytics queries and target management | `docs/api/analytics.md` |
| Studio AI: generate images, videos, list models | `docs/api/studio.md` |
| Subscription: check credits, tier, renewal dates | `docs/api/subscription.md` |
| Research a specific niche quickly (trend + competitors + hooks) | `docs/api/analytics.md`, `docs/references/competitor-research.md`, `docs/prompts/hooks.md` |
| Full content pipeline, performance loop, CTA testing | `docs/api/pipeline.md` |
| Error codes, troubleshooting | `docs/api/errors.md` |

## Niche Research Mode (When user asks to research a niche)

When asked things like "research this niche", "find what works in this niche", or "give me niche intelligence":

1. Run `trend-brief` first for the niche keyword (`7d` baseline, then `24h` for freshness if needed).
2. Extract and report: top hashtags, top sounds, top creators, posting windows (UTC), recommended hook angles.
3. Run competitor deep-dive using `docs/references/competitor-research.md` (3-5 accounts minimum).
4. Produce a short actionable output with:
   - 3 hook angles to test
   - 2 CTA suggestions
   - 2 best posting windows
   - 5 hashtags to start with
   - 1 "gap to exploit" insight
5. Save findings to `workspace/performance/competitor-insights.md` and use them in subsequent content prompts.

## TikTok Copy Remix Mode (When user asks "make similar but new")

When the user wants to copy a TikTok slideshow idea but generate new visuals:

1. Run `copy-tiktok-preview` first and capture `preview_id`, source image URLs, and slide count.
2. Run `copy-tiktok-import` with exactly one pack source (`pack_id` or `pack_images`) so text overlays are extracted and mapped into editable slides.
3. Generate replacement images through Studio using `google/nano-banana-2` with each source slide image as reference input:
   - command: `studio-generate-image --model-id "google/nano-banana-2" --image-urls "<source_url>" --prompt "<product-aware transformation prompt>"`
4. Build prompts with product context from `workspace/context/product.md` so generated visuals stay relevant to the advertised product.
5. Replace slide backgrounds with generated URLs (`update --slides-file ...`) while preserving/editing imported text elements.
6. Render (`render`) and review (`review`) before posting; never skip visual QA.

## Analytics Correlation Mode (When user asks "match analytics back to posts")

1. Pull `analytics-posts --json`.
2. Prefer `genviralPostId` for matching analytics rows back to Genviral posts.
3. If you need the caller's own stable ID, use `externalId`.
4. Treat `analyticsId`/legacy `id` as the analytics-row identifier only.
5. Treat `platformPostId` as the platform-native TikTok/Instagram/YouTube post identifier only.
6. For BYO TikTok drafts (`MEDIA_UPLOAD`), do not assume a draft upload is correlated immediately. The draft `publish_id` becomes matchable only after the human posts from TikTok and Genviral resolves it to the final public TikTok video ID.

## Non-Negotiable Rules

These apply regardless of what docs you've loaded:

1. **ALWAYS use `pinned_images`** when generating a slideshow with a pack. Never call `generate` with just `--pack-id` — the server will pick random images. Read `docs/api/packs.md` before any pack workflow.

2. **ALWAYS visually review every rendered slide** before posting. If any slide fails readability, fix it. This is a hard gate — not a suggestion.

3. **ALWAYS log to `workspace/performance/log.json`** immediately after posting. This is the canonical record.

4. **ALWAYS add a hook-tracker entry** after posting. No tracking = no learning.

5. **Never use em-dashes** in any generated content.

6. **Respect `workspace/`** — all instance data lives here. Do not write state files to the skill root.

## Script Usage

```bash
/path/to/genviral/scripts/genviral.sh <command> [options]
```

Requires `GENVIRAL_API_KEY` as an environment variable (format: `public_id.secret`). Loads defaults from `defaults.yaml`. Set `GENVIRAL_WORKSPACE_DIR` to override the workspace path (defaults to `workspace/` relative to the skill dir).

## Auto-Updates

This skill includes a self-updater that keeps skill-owned files in sync with the latest version from `fdarkaou/genviral-skill`.

```bash
bash scripts/update-skill.sh           # check + apply if updates available
bash scripts/update-skill.sh --dry-run # preview only, no changes
bash scripts/update-skill.sh --force   # force re-apply even if already current
```

**What gets updated (skill-owned):** `README.md`, `SKILL.md`, `scripts/`, `docs/` (all subdirs)

**What never gets touched (user-owned):** `workspace/` — your data, context, hooks, and performance logs are always preserved.

---

## Notes

- Works with any platform genviral supports (TikTok, Instagram, etc.)
- Supports both video and slideshow posts
- Works with hosted and BYO accounts
- Posts can be scheduled or queued for immediate publishing
- TikTok slideshow drafts: use `post_mode: MEDIA_UPLOAD` to save to drafts inbox for audio addition
- BYO TikTok draft uploads (`MEDIA_UPLOAD`) create the Genviral post immediately, but the final public TikTok video ID exists only after the user publishes in TikTok. In `analytics-posts`, use `genviralPostId` or `externalId` for correlation; treat `analyticsId`/legacy `id` as the analytics-row ID and `platformPostId` as the TikTok-native ID.

## Meta Ads Skill (Included)

This repo includes the **meta-ads** skill in the `meta-ads/` directory — an autonomous Meta (Facebook/Instagram) Ads manager and 8-stage AI campaign builder that uses Genviral's Studio API for ad creative generation.

See [`meta-ads/SKILL.md`](meta-ads/SKILL.md) for full workflow and setup.

Also available standalone: [fdarkaou/meta-ads-skill](https://github.com/fdarkaou/meta-ads-skill)
