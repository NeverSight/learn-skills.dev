---
name: storefront-branding
description: Guided review-first branded demo workflow for Storefront Next storefronts. Use when the user asks to create or refine a demo brand from a customer URL, says things like "quiero hacer un nuevo branding para https://...", wants a localhost preview review session with overrides.json, or wants the final approved brand applied to branding-presets.ts, app.css, and .env.
---

# Storefront Branding

## Overview

Use this skill to run the branded demo flow for a Storefront Next project and to bootstrap the branding hooks when the target repo is still a clean template.

This skill is self-contained:

- `scripts/webcrawler/` vendors the crawler/runtime used by the preview and apply flow. If `node_modules` is absent, `scripts/webcrawler/scripts/run-webcrawler.sh` installs the pinned dependency set from `package-lock.json` on first run.
- `scripts/bootstrap-storefront-next-template.mjs` bootstraps the required branding hooks into a clean `storefront-next-template` clone.
- `references/branded-demo-playbook.md` contains the agent-facing version of the branded demo workflow that previously lived only in repo docs.
- `references/storefront-next-template-bootstrap.md` explains how to wire a clean `storefront-next-template` clone before running the crawler.
- `references/storefront-next-hooks.md` defines the hook contract that the workflow expects.
- `assets/template-bootstrap/src/config/branding-presets.ts` is the minimal starter file for a stock template.
- `scripts/audit-storefront-next.mjs` verifies whether a repo is ready for the workflow.

## Workflow

1. Determine the brand id.
   - Prefer an explicit user-provided name.
   - Otherwise derive it from the site or domain and keep it lowercase/hyphenated.

2. Audit the storefront before running the crawler.
   - Run:

```bash
node ./.agents/skills/storefront-branding/scripts/audit-storefront-next.mjs [target-path]
```

   - Confirm these hook points exist and are wired for branding: `src/config/branding-presets.ts`, `src/app.css`, `src/root.tsx`, `src/routes/_app._index.tsx`, `src/components/header/index.tsx`, and `PUBLIC__app__global__branding__name` in `.env.default` or `.env`.
   - If the audit fails for a clean `storefront-next-template`, run:

```bash
node ./.agents/skills/storefront-branding/scripts/bootstrap-storefront-next-template.mjs [target-path]
```

   - The bootstrap script copies the bundled template-ready files, reruns the audit, and exits non-zero if the repo does not still look like the stock template. Use `--force` only when you intentionally want to overwrite those template files.
   - If the repo is not a stock template, use `references/storefront-next-hooks.md` and adapt the equivalent files rather than forcing exact paths.
   - Do not depend on repo-level docs to understand or complete the integration.

3. Treat the first pass as preview-only.
   - Do not patch the storefront on the first request unless the user explicitly says to skip review.
   - Prefer the guided review session for conversational requests such as "quiero hacer un nuevo branding para https://...":

```bash
./.agents/skills/storefront-branding/scripts/start-brand-review.sh "<url>" [brand-id]
```

   - This command creates `.webcrawler/<brand-id>/overrides.json` immediately, generates the first preview, starts a localhost review server, and lets the user save overrides, regenerate the preview, and apply the final brand directly from the browser.
   - If a local review server is not wanted, fall back to the lower-level preview command:

```bash
./.agents/skills/storefront-branding/scripts/preview-brand.sh "<url>" "<brand-id>"
```

   - Add `--display-name "<name>"`, `--overrides "<file>"`, or other extra brand arguments after the first two positional arguments when needed.

4. Return the preview to the user.
   - Always report these paths:
     - `.webcrawler/<brand-id>/preview.html`
     - `.webcrawler/<brand-id>/page.json`
     - `.webcrawler/<brand-id>/analysis.json`
   - If `start-brand-review.sh` was used, return the localhost preview URL printed by the script and tell the user they can save/regenerate/apply from the preview UI itself.
   - If the lower-level preview command was used and the user explicitly wants a localhost URL, serve `.webcrawler/<brand-id>/` with a simple local static server available in the environment and give them `http://127.0.0.1:<port>/preview.html`.

5. Tell the user exactly how to review the preview.
   - Open `preview.html`.
   - In `Selected assets`, click `Change image` on the slot to adjust.
   - In `Detected candidate families`, pick a family or expand variations to choose a specific size/format.
   - In `Brand colors`, adjust the detected color tokens when the palette needs manual tuning.
   - Copy the `Overrides JSON` block and send it back, or save/regenerate directly from the guided localhost review session.

6. When the user sends overrides JSON, save it and regenerate the preview only.

```bash
./.agents/skills/storefront-branding/scripts/preview-brand.sh \
  "<url>" \
  "<brand-id>" \
  --overrides ".webcrawler/<brand-id>/overrides.json"
```

   - Keep the same brand id and output directory on every iteration.
   - Return the refreshed preview path or localhost URL.
   - Repeat until the user explicitly approves the result.
   - If the preview is running inside the guided review session, the user can save overrides and trigger regeneration directly from the browser instead of pasting JSON back into chat.

7. Only after approval, apply the brand to the storefront.

```bash
./.agents/skills/storefront-branding/scripts/apply-brand.sh \
  "<url>" \
  "<brand-id>" \
  --replace \
  --overrides ".webcrawler/<brand-id>/overrides.json"
```

   - `apply-brand.sh` already targets the current storefront, writes into `.webcrawler/<brand-id>/`, and runs `typecheck` plus `build`.
   - Add `--push` only when the user explicitly asks to deploy or push.

## Guardrails

- Never depend on repo-level docs. The skill must stay usable when copied into another repo on its own.
- When the target is a clean template, prefer the bundled bootstrap file over recreating `src/config/branding-presets.ts` from scratch.
- Never call `workflow` on the first pass unless the user explicitly opts out of review.
- Never hand-edit `branding-presets.ts` to partially apply overrides. Regenerate from the crawler artifacts so imagery and copy stay aligned.
- Prefer distinct image families and distinct extracted text context across slots. If manual overrides introduce duplicates, call that out before applying.
- Treat color token edits as part of the preview state. Saving, regenerating, or applying should use the latest visible token values, not reset to the original extraction.
- Keep generated artifacts under `.webcrawler/<brand-id>/`.
- If the user wants more than one refinement round, keep using `brand --overrides` until they approve the final preview.
- Read `references/branded-demo-playbook.md` when you need the slot model, image selection rules, override loop details, or the recommended conversation flow.

## What To Return

- After the initial run: the preview path or localhost URL, the main artifact paths, and a short instruction to send back `Overrides JSON`.
- When the guided review session is active: the localhost preview URL, the artifact directory, and a short note that `overrides.json` already exists and can be saved/regenerated from the browser UI.
- After each override round: the refreshed preview path or URL and whether duplicate warnings remain.
- After the final apply: the applied brand id, the artifact directory, and which follow-up steps ran (`typecheck`, `build`, `push`).
