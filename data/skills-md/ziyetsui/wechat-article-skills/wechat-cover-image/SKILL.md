---
name: wechat-cover-image
description: Use when the user says "@公众号封面", "公众号封面图", "给这篇公众号配封面", "根据改写文章生成封面", asks for YouMind/“这种封面”/Dan Koe/Claude Code cover style, or wants to generate a WeChat public-account cover image from a rewritten article using APiYi ChatGPT/GPT Image 2 with either the default neo-classical engraved collage style or a selected style card.
---

# WeChat Cover Image

Generate a WeChat public-account cover image from a rewritten article. The default visual style is a neo-classical engraved collage editorial cover: 19th-century engraving linework, high-contrast black-and-white figures, saturated flat color fields, symbolic composition, and modern op-ed/concept-art clarity.

## Inputs

Expected inputs:

- Rewritten article text, draft, outline, or final title.
- Optional cover title, visual metaphor, output folder, model choice, or whether to actually call the image API.
- Optional cover style card or style request from `wechat-style-studio`.

If the article is missing, ask for the article. If only the topic/title is provided, generate a cover prompt from that title and mark the concept as inferred.

## Optional YouMind Cover Style

If the user mentions YouMind, Dan Koe, Claude Code, “这种封面/那种封面”, or a style chosen from `wechat-style-studio`, use `wechat-style-studio` first.

- Read `wechat-style-studio/SKILL.md`.
- Read `references/style-index.json` first, then load only the selected `references/styles/<style-id>.md` card.
- Treat the selected card's `封面 Skill` as the visual-style override.
- Preserve the selected cover class, palette, brightness/saturation/contrast, composition strategy, visual metaphor, and text strategy.
- Keep WeChat constraints: horizontal `2.35:1`, center-safe square crop, thumbnail readability, and minimal text.

Use the default neo-classical engraved collage editorial style only when no selected cover style is provided.

## WeChat Cover Size

Use these defaults for public-account article covers:

- Main article cover: `900x383` px, about `2.35:1`.
- Secondary/square cover: `500x500` px or `200x200` px depending on publishing UI and use case.
- Safe area: keep the key figure, visual metaphor, and any short text near the center so square crops still work.

Because `gpt-image-2` requires generated sizes to use dimensions divisible by 16, generate at `1808x768` first, then crop/resize to exact WeChat outputs.

## API Setup

Use APiYi token management at:

```text
https://api.apiyi.com/token
```

Do not write API keys into this skill or committed files. Before generation, require one of:

```bash
export APIYI_API_KEY="..."
# or
export YI_API_KEY="..."
```

The default API base is:

```text
https://api.apiyi.com/v1
```

## Workflow

### Step 1: Read The Article

Extract:

- Core judgment.
- Emotional temperature.
- Target reader pressure.
- One visual metaphor that can be understood without reading the article.
- 3-6 short keywords that can appear as tiny labels if needed.

### Step 2: Choose A Cover Concept

Prefer one strong concept, not a collage of many ideas.

Good concepts:

- A central decision-maker, traveler, founder, or thinker standing at the threshold of a path.
- A winding road from tunnel/darkness toward a bright doorway, market, machine, or future signal.
- Symbolic checkpoints that map to the article's core stages: users, product, cashflow, market, freedom, feedback, courage, time.
- A classical figure plus modern flat color blocks, machinery, targets, cubes, pipes, audience silhouettes, charts, or doors.
- One editorial metaphor with allegorical weight rather than a literal infographic.

Avoid:

- Photorealistic portraits or glossy 3D renderings.
- Corporate SaaS illustration.
- Glossy cyberpunk, anime, decorative gradients, or polished vector art.
- Dense infographic text.
- Full article title rendered as long Chinese text.
- Stock-photo vibes, realistic office scenes, fake UI screenshots, and fake logos.

### Step 3: Build The Prompt

Write the image prompt in English with any necessary short Chinese text explicitly quoted. Keep in-image text minimal.

If a selected YouMind cover style is provided, build the prompt from that card's `封面 Skill` instead of forcing the default neo-classical engraved block below. Keep the chosen style's visual category, palette, composition, and avoid rules, while adapting the central concept to the current article.

Prompt structure:

```text
Create a horizontal WeChat public-account article cover, 2.35:1 aspect ratio, in a neo-classical engraved collage editorial illustration style.

Central concept: <one symbolic editorial metaphor from the article>.

Style: rooted in 19th-century copperplate engraving, woodcut, and etching. Black-and-white engraved figures and objects with dense hatching, cross-hatching, stippling, etched contours, antique printed-paper grain, and crisp high-contrast linework. Combine these classical engraved elements with bold saturated flat color fields such as burnt orange, cobalt blue, warm parchment, black, and small accents of gold or red. The mood is intellectual, allegorical, controlled, slightly ironic, and contemporary editorial.

Composition: modern op-ed / magazine cover logic, not naturalistic realism. Use a strong silhouette and a poster-like layout that remains readable as a small thumbnail. Prefer one central human figure or symbolic object, a winding path or threshold, and a few surreal collage elements. Keep the key subject and main metaphor centered within the safe square crop while using the full wide frame for secondary symbols.

Text: no full article title. Use no text by default. If labels are essential, use only 1-4 tiny Chinese labels, each 2-4 characters, integrated like editorial annotations.

Avoid: photorealism, glossy 3D, anime, polished vector art, corporate SaaS illustration, decorative gradients, long text, fake logos, watermarks, UI screenshots, and literal step-by-step infographics.
```

For Founder-style articles, prefer this reusable pattern:

```text
Create a horizontal WeChat public-account article cover, 2.35:1 aspect ratio, in a neo-classical engraved collage editorial illustration style.

Scene: an engraved young founder/traveler stands near the center holding a compass and notebook, facing a winding elevated path that begins in a dark tunnel and leads toward a glowing doorway. Along the path, place symbolic checkpoints for "<label1>", "<label2>", "<label3>", and "<label4>" using simple engraved icons such as audience silhouettes, a product cube, a cashflow coin/pipe, a target, or a market machine. Use large flat color fields: burnt orange on the left/middle, cobalt blue on the right, warm parchment paper texture, and black engraved linework.

Text: no title. Optional tiny Chinese labels only: "<label1>", "<label2>", "<label3>", "<label4>".

Style and avoid rules: <use the default style block above>.
```

### Step 4: Generate The Image

Use the bundled script:

```bash
python3 /Users/ziye/.agents/skills/wechat-cover-image/scripts/generate_cover.py \
  --prompt "<final image prompt>" \
  --output-dir "<target-output-folder>" \
  --basename "<slug>"
```

Defaults:

- Model: `gpt-image-2`
- API base: `https://api.apiyi.com/v1`
- Generation size: `1808x768`
- Quality: `high`
- Exact main output: `900x383`
- Square output: `500x500`

For lower predictable per-image cost, use `--model gpt-image-2-all` and put the aspect ratio into the prompt. For strict size with the lower fixed-price reverse channel, use `--model gpt-image-2-vip --size 2048x864` if that size is accepted by the token/model.

### Step 5: Validate

Check:

- The final main cover is exactly `900x383`.
- The square cover is exactly `500x500`.
- The key concept remains visible in the center crop.
- There is no long or unreadable text.
- The image matches the neo-classical engraved collage editorial style.
- The image has etched line texture, high contrast, restrained saturated color fields, and strong thumbnail readability.

If generation fails, report the API error and keep the final prompt so the user can retry.

## Style DNA

### 中文风格名

新古典雕版拼贴编辑插画风格

### English Style Name

Neo-classical Engraved Collage Editorial Illustration Style

### Visual Rules

- Root the image in 19th-century engraving, copperplate etching, woodcut, and antique printed illustration.
- Use dense hatching, cross-hatching, stippling, etched contours, halftone dots, and visible paper grain to build volume.
- Combine black-and-white engraved subjects with bold saturated flat-color backgrounds.
- Prefer a restrained but intense palette: black, white, warm parchment, burnt orange/red, cobalt blue, and a small gold or red accent.
- Keep contrast very high: crisp black contour, white highlights, and clearly separated flat color planes.
- Compose like an editorial/op-ed cover rather than a naturalistic scene.
- Prioritize symbolism, metaphor, and conceptual clarity over literal illustration.
- Use collage logic: classical figures, modern machinery, geometric blocks, paths, doors, targets, audiences, and surreal juxtapositions can coexist.
- Simplify the background into flat planes, grain, stripes, or minimal spatial cues.
- Make the image poster-readable from a distance and robust as a WeChat thumbnail.
- Keep the mood intellectual, controlled, allegorical, slightly ironic, and serious enough for opinion essays.
- Avoid pure vintage nostalgia; the target is classical engraving technique fused with contemporary editorial concept design.

## Output Shape

Return:

```text
## 封面概念
<one-sentence concept>

## 生成提示词
<final prompt>

## 输出文件
- 主封面：<path>-900x383.jpg
- 方形封面：<path>-500x500.jpg
- 原始图：<path>-raw.<ext>

## 检查结果
- 尺寸：
- 中心安全区：
- 风格一致性：
```
