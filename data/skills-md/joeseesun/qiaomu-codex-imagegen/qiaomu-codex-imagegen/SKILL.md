---
name: qiaomu-codex-imagegen
description: |
  Generate or edit images with Codex's built-in image generation from any agent, through an MCP tool or a plain CLI. For every image request it first proposes at least four divergent style directions (24 distilled templates, 48 presets, 20 Mondo poster artists), lets the user pick, expands the prompt, generates, and checks the result. Scenario craft for 视频封面, 视频海报, 小红书配图, 公众号封面, X 封面, 朋友圈海报, 书籍封面, 专辑封面, 产品海报, 人物写真, 节气海报, 展览海报, PPT 页面, 图生图. Use for 生图, 配图, 海报, 封面, "给我几个风格", "用 Codex 画一张". Excludes: editing photos with local tools, charts or diagrams from data, UI mockups, video generation, or anything that needs an API key-based image service.
license: MIT
metadata:
  version: 0.3.0
  author: 向阳乔木 (https://x.com/vista8)
---

# Qiaomu Codex ImageGen

Codex ships an image generator that other agents cannot call. This package relays to it (`codex app-server`) and adds the craft that makes the pictures usable: a library of 24 templates (48 presets) distilled from 689 reference prompts, Mondo poster techniques, scenario presets, and a rule set for facts, text and identity.

## How to call it

1. **MCP tools present** (`suggest_directions`, `compose_prompt`, `generate_image`, `search_prompts`, `get_prompt`, `build_prompt`, `list_catalog`; in Claude Code `mcp__qiaomu-codex-imagegen__*`): use them.
2. **No MCP**: run the CLI from this skill's folder: `node scripts/cli.mjs suggest|compose|generate|search|prompt|list` (see `--help`).
3. Neither available: tell the user to install (README). Requires the Codex CLI, logged in. Never fake an image with code.

## The workflow: suggest, choose, compose, generate, check

### 1. Intake (no tool call yet)

Extract: **topic**, **deliverable** (what it is for), ratio, **text mode**, facts that must be exact, references and the role of each (`identity` person, `product` real packaging, `style`, `layout`), must-keep, must-avoid.

- Text mode: `none` (no text), `exact_short` (only the short text you list), `typeset_later` (text-free base with room for the title).
- **Posters, covers, cards and slides need a typographic layer.** A finished poster has a hierarchy: headline, subtitle, one or two info lines, a small tag. With only a headline, or none, the result is concept art, not a poster. So for these deliverables use `exact_short` and give a complete short copy set: `headline` plus `copy` as lines separated by `｜`. Take the lines from the user's facts. If they gave none, ask, or write clearly fictional sample lines and say so; never invent real prices, dates of real events, names, statistics.
- `none` fits portraits and photos (T09–T11), product macros that carry no information, and base images the user will typeset. Keep every string short and read the result: models misspell, especially long Chinese.
- Ask only blocking questions, at most three: a missing subject, a real person's identity reference, or facts that must appear. Fill low-risk gaps with a stated default.

### 2. Suggest at least four divergent directions

Call `suggest_directions` with the topic, deliverable and any headline/text mode. It returns **four or more directions with different visual mechanisms** (typography-led, graphic structure, photographic, product macro, material/space, plus a Mondo artist option for poster-like work). Never mix two mechanisms into one image.

Present them to the user briefly, one numbered item each:

- name and template id,
- **one concrete sentence of what this topic would look like in that mechanism** (write it yourself from `mechanism` and the topic, not a copy of the lock text),
- what you still need from them (subject, data, reference photo),
- look at one `references[].image` thumbnail per direction when available, so your sentence matches the real look.

Then ask which to make: one, several, "all", or "你定". Offer to exclude these and propose more (`exclude`).

**Skip the question** when the user already fixed the style ("用 Mondo 风格", "T03", "就这个风格") or said to go ahead ("直接出", "你定"). For "你定", pick the two best-fitting directions from different families and say which and why.

### 3. Compose the prompt

For each chosen template direction call `compose_prompt` with concrete variables:

- Map the topic to **one visible silhouette, action or relation**, and say how it connects to the topic. At most one main symbol and one cross-over action.
- Colours are **roles** (background, primary, accent, ink), not fixed hex values. Material belongs where the preset puts it; do not overlay noise on everything.
- No invented facts: prices, statistics, titles, names, dates, weather, quotes, QR codes, logos.
- `missing_required` non-empty → ask for exactly that. `weak_variables` → they still hold generic defaults, fill them first.
- Preset with `structural_override` → rewrite the prompt by hand: delete the base sentences the override replaces, keep no conflicting structure, then send the result as `raw_prompt` with the `避免：…` line.
- Typographic templates with no text: tell the user the base image only satisfies the style after the title is typeset.
- Give `copy` as `｜`-separated lines; when strings include dates or numbers, list them all so the whitelist matches exactly (or pass a full `text_rule`).

Mondo directions skip this step: `generate_image { prompt, style: <artist>, preset: <video-cover|poster|…> }`.

Full rules and the canonical agent instruction: [references/design-system/agent-guide.md](references/design-system/agent-guide.md).

### 4. Generate

Default **one image per chosen direction**, up to four, each its own `generate_image` call (they can run in parallel). Use `count` only for variants of the same direction. Say that it takes 30–180 s and spends Codex quota. `out_dir` goes inside the user's project when they name one; `reference_images` take absolute paths (identity photo, product shot, style reference, or the image to edit).

Series: lock template, type hierarchy, colour roles, texture placement and cross-over action; change one or two of scene, narrative focus, hue, module span. Pass the first image as `reference_images` for the rest.

### 5. Check and deliver

Read each saved image and test it against `acceptance_checks` (the tool prints them): first-glance focus, relations that must hold, materials only where intended, exact text and identity, nothing invented. State pass or the specific failed relation.

**With the local corpus pack installed, compare against the references:** put the result next to one or two `references[].image` of the same template (`suggest_directions` lists them). If yours is plainly less designed (bare subject, no typographic hierarchy, no secondary layer), that is a failure too: complete the copy set or the missing layer and regenerate once.

On failure change only the sentence that carries that relation and regenerate once; do not stack "more premium" adjectives. Transparent regions in a result are flattened onto white automatically (`transparent_background: true` keeps them). Deliver absolute paths, the direction used, and the sidecar `.json` (exact prompt) next to each image. Only say "generated" for images you actually produced and looked at.

## Rules

- Each generation spends the user's quota: no test generations, `count` above 3 only if asked.
- People: prefer silhouettes, back views, hands or symbols unless a face is asked for. Identity consistency needs an identity reference photo; without one say the person is fictional. Never make deceptive material with a real person's likeness.
- Facts and numbers come only from the user; complex charts and long copy are typeset afterwards, not drawn by the model.
- Reference corpus: `search_prompts` / `get_prompt` read the local pack of 689 reference prompts (installed on the user's machine only). Use them to study how a mechanism is described; never send a corpus prompt unchanged as the user's prompt.
- Simple route: `prompt` + `preset` + `style` (66 styles, 20 Mondo artists) when the user wants a quick image without the direction step.

## Output contract

Reply with: absolute path(s), pixel size, direction (template/preset or Mondo artist) per image, assumptions made, acceptance result, and where the prompt sidecar is. On failure give the tool's error and the one fix to try (Codex login, shorten the prompt, check the reference path).

## Resources

- [Agent guide](references/design-system/agent-guide.md): the rule set, input/output shapes, routing table
- [Template library](references/design-system/template-library.md): 24 templates, locks, presets, evidence; machine-readable `templates.json`, `routing.json`; [filled examples](references/design-system/filled-examples.md)
- [Scenarios](references/scenarios.md): ratios and safe areas per platform; [prompt craft](references/prompt-craft.md); [Mondo poster craft](references/mondo-poster.md) with [artist styles](references/mondo/artist-styles.md)
- `references/styles.json` (66 styles), `mondo-artists.json` (20), `presets.json` (13 scenarios)

Copyright (c) 向阳乔木. X https://x.com/vista8, GitHub https://github.com/joeseesun/. Template library distilled from public-area samples of https://vip.xiaoxiaodong.ai/open-source; Mondo material from [qiaomu-mondo-poster-design](https://github.com/joeseesun/qiaomu-mondo-poster-design) (MIT).
