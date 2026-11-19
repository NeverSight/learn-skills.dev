---
name: long-poster
description: Create vertical long-form posters from any content. Use this whenever the user asks for a 长图, long poster, vertical infographic, social media poster, WeChat/Feishu/Xiaohongshu/Bilibili image, event/course/product promo long image, or asks to turn notes into an HTML + PNG poster. The skill must research style directions live, show 3 clearly different demos first, open the preview for user judgment, then produce final editable HTML plus high-resolution PNG.
---

# Long Poster

Create vertical long-form posters that work as both editable HTML and high-resolution PNG exports.

This skill is for continuous scroll posters, not slide decks. Do not use `.slide { height: 100vh }` patterns unless the user explicitly asks for slides. A long poster is a single vertical canvas with sections, rhythm, and export constraints.

## Success Standard

Use `references/scoring-rubric.md` for evals and self-checks. A result is successful only when it reaches at least 90%: 9 of 10 rubric checks must pass.

Every saved run must include two evidence artifacts:

- `output.md`: concise handoff with the preview/final file paths and a "Rubric Evidence" section.
- `rubric-evidence.json`: 10 checks in rubric order, each with `passed` and `evidence`.

Before handing work back to the user, run this short gate mentally or with `scripts/score-run.js` when evaluating saved outputs:

- Did I parse content, audience, channel, CTA, and hierarchy?
- Did I keep it as one continuous vertical poster rather than slides?
- Did I choose three content-specific style directions, not a fixed menu?
- Are the three directions visibly different in at least three dimensions?
- Did each direction include source, fit, visual system, difference, and risk?
- Did I create real demos using real content and a preview index?
- Did I open the preview or report the preview path?
- Did I stop for user confirmation before final production?
- Did I state or deliver editable HTML plus 3x PNG at least 1200px wide?
- If the poster is too tall, did I produce designed multi-panel images instead of hard slicing when feasible?
- Did I route hero/key visual needs through the Image Asset Step, using Codex native GPT Image 2 / `image-2` when appropriate?
- Did I verify or commit to verifying dimensions, decodability, overflow, full height, multi-panel output, and the `image-2`/`imagegen` boundary?

## Core Workflow

1. **Understand the content**
   - Extract the topic, audience, channel, call to action, required facts, and rough content hierarchy.
   - If content is sparse, make a compact poster with fewer sections instead of padding it with generic copy.
   - If content is dense, group it into clear vertical sections and avoid cramming.

2. **Research and propose 3 style directions**
   - Do live design thinking and, when useful, web research for design history, visual culture, current poster examples, or domain references.
   - Do not rely on a fixed preset list. The three directions should be chosen for this specific content.
   - Each direction must name a recognizable design history movement, visual culture, or contemporary design language.
   - The three directions must differ in at least 3 of these dimensions: layout structure, typography mood, color system, graphic language, content density, image treatment, motion/interaction.
   - Avoid presenting three near-identical directions that only swap colors.

3. **Create 3 demo previews**
   - Build small HTML demos or first-screen/short-poster previews for all three directions.
   - Create a local preview index that shows all three side by side or stacked.
   - Automatically open the preview page for the user to judge.
   - In the preview handoff, explicitly state the final export contract: editable HTML plus `poster-3x.png`, PNG width at least `1200px`, and multi-panel PNGs for very tall posters.
   - In the preview handoff, explicitly state that final production will run a horizontal overflow check and full-height completeness check.
   - Stop and wait for the user to choose one direction or request a mix.

4. **Generate the final poster**
   - Produce a single editable HTML file with inline CSS and JS where possible.
   - Keep output portable: local assets should be copied next to the HTML or embedded.
   - Use responsive CSS with `clamp()` for text and spacing.
   - Maintain a stable poster width, usually `430px` CSS width unless the user asks otherwise.
   - For long outputs, wrap natural chunks in `.poster-panel` or `[data-poster-panel]` sections so the exporter can create multi-panel images without cutting through content.
   - Follow the Image Asset Step when the poster needs a hero image, product render, atmosphere image, mascot, icon scene, or other generated visual.

## Image Asset Step

Use this step whenever the poster would benefit from a main visual or generated supporting image.

1. **Decide whether an image is needed**
   - Use generated imagery when a hero visual, abstract product scene, campaign image, or strong visual hook will improve the poster.
   - Do not force generated imagery for dense operational posters where typography, grid, and diagrams work better.

2. **Prefer Codex native GPT Image 2 / `image-2`**
   - Codex native image generation (`image-2`, GPT Image 2) can create visual assets directly in Codex and does not require `OPENAI_API_KEY`.
   - Use native `image-2` for one-off hero/key visuals and fast creative exploration.
   - Prompt it for clean bitmap assets with no embedded text, no logo, no watermark, and clear safe margins.
   - Ask for the intended role and aspect ratio, for example: `vertical poster hero, 4:5`, `wide header texture, 16:9`, or `square icon scene, 1:1`.

3. **Use `imagegen` CLI only for reproducible or batch generation**
   - The `imagegen` skill CLI is a reproducible/batch alternative and requires `OPENAI_API_KEY`.
   - Use it when the user asks for repeatable generation, scripted batch assets, or regeneration from stored prompts.

4. **Integrate the asset**
   - Save or reference the generated asset next to the HTML when the environment exposes a file path.
   - If no local file path is available, keep the HTML functional with CSS/SVG fallback and report that the native generated image is a separate visual asset.
   - Do not place generated images behind dense text unless contrast and legibility are verified.

5. **Verify the asset**
   - Check that the image has no unwanted text, watermark, malformed logo, or obvious crop problem.
   - Check that it is high enough resolution for the final PNG export.
   - Record in `output.md` whether native `image-2` was used, whether `imagegen` CLI was used, or why generated imagery was not needed.

6. **Export high-resolution PNG**
   - Export `poster-3x.png` by default with `deviceScaleFactor=3`.
   - The exported PNG width should be at least `1200px`; if not, increase scale.
   - For very tall posters, prefer designed multi-panel PNG files to avoid preview truncation in chat apps, WeChat, Feishu, and similar clients.
   - Multi-panel output means `panels/panel-01.png`, `panel-02.png`, etc., where each panel is a complete designed card. Do not cut text, QR codes, charts, faces, or section titles across boundaries.
   - Use hard `segments/part-xx.png` slicing only as a fallback when the HTML has no usable panel boundaries and the user still needs it.

7. **Verify before delivery**
   - Check actual PNG pixel dimensions.
   - Check horizontal overflow in the rendered page.
   - Check that the PNG height matches the rendered poster height at export scale.
   - If the poster is very tall, explain that embedded previews may crop it and point to the multi-panel files.

## Output Contract

Final delivery should include:

- `index.html` or a clearly named editable HTML file.
- `poster-3x.png` or equivalent high-resolution PNG.
- `panels/panel-01.png`, `panel-02.png`, etc. when the full PNG is taller than typical preview limits.
- `segments/part-01.png`, `part-02.png`, etc. only when hard slicing fallback was unavoidable.
- A short note with pixel dimensions and verification status.
- The note must explicitly report horizontal overflow status, full-height completeness status, and whether multi-panel output or hard-segment fallback was generated.
- If any visual asset generation path was considered, the note must explicitly say whether Codex native `image-2` was used, or whether `imagegen` CLI would require `OPENAI_API_KEY`.
- If GPT Image 2 / `image-2` generated a visual asset, the note must include the asset role, prompt intent, file/path status, and visual QA status.

## Preview Handoff Template

After opening the three-style preview, respond with this information and then stop:

```markdown
已打开 3 个风格 demo 预览：[preview path]

请选择 A / B / C，或指定混合方式。确认前我不会生成最终长图。

最终交付标准：可编辑 HTML + `poster-3x.png`；PNG 默认 3x，宽度不低于 1200px；超长图优先输出多宫格 `panels/panel-xx.png`，每张都是完整设计卡片；硬切分 `segments/part-xx.png` 只做兜底。最终会检查横向溢出、PNG 可解码、像素尺寸和底部完整性。若需要生成主视觉，Codex 原生 `image-2` 不依赖 API Key；`imagegen` CLI 才需要 `OPENAI_API_KEY`。
```

Keep the wording concise, but do not omit the contract.

When saving outputs for a preview-stage run, `output.md` must also contain:

```markdown
## Content Parse
- Topic:
- Audience:
- Channel:
- CTA:
- Hierarchy:

## Format
- Continuous vertical long poster, not 100vh slides.

## Preview Artifacts
- style-a.html:
- style-b.html:
- style-c.html:
- preview-index.html:

## Rubric Evidence
- 1 Content parsing: pass, evidence...
- 2 Continuous long-poster format: pass, evidence...
- 3 Live style reasoning: pass, evidence...
- 4 Three distinct style directions: pass, evidence...
- 5 Direction brief quality: pass, evidence...
- 6 Real demo preview: pass, evidence...
- 7 Automatic preview handoff: pass, evidence...
- 8 User confirmation gate: pass, evidence...
- 9 Final output contract: pass, evidence...
- 10 Export verification and image boundary: pass, evidence...
```

`rubric-evidence.json` must use this shape:

```json
{
  "threshold": 0.9,
  "checks": [
    {"passed": true, "evidence": "Topic/audience/channel/CTA/hierarchy captured in output.md"}
  ]
}
```

Keep all 10 checks in the same order as `references/scoring-rubric.md`.

## Final Run Rules

If the user explicitly asks for final HTML + PNG and has already chosen a direction, produce the final output directly.

If the user explicitly asks for final HTML + PNG but has not chosen a direction, still present three researched directions first. If the user also signals they want direct production in the same turn, choose the strongest direction, state that assumption in `output.md`, and produce the final files. Otherwise stop after the preview handoff.

For final HTML, add `.poster-panel` or `[data-poster-panel]` to natural sections so multi-panel export is available.

Final `output.md` must report:

- Chosen direction and why.
- HTML path.
- Full PNG path and pixel dimensions.
- Whether PNG width is at least 1200px.
- Horizontal overflow status.
- PNG decodability status.
- Full-height completeness status.
- `panels/` path for multi-panel output, or why hard `segments/` fallback was used.
- Codex native `image-2` vs `imagegen` CLI API-key boundary.
- Image asset status: `image-2 used`, `imagegen CLI used`, or `no generated imagery needed`, plus visual QA notes.

## Style Direction Brief

For each of the 3 preview directions, use this format:

```markdown
### Direction A — [Name]
- Source: [design movement / visual culture / contemporary reference]
- Fit: [why it matches this content and audience]
- Visual system: [layout, type, color, graphics]
- Difference: [how it differs from the other two directions]
- Risk: [what could go wrong]
```

## Preview Rules

- Preview before final production. The preview is a decision tool, not a finished poster.
- Make previews visibly different at first glance.
- Use real content fragments from the user, not lorem ipsum.
- Open the preview page automatically when the environment supports it.
- If opening fails, provide the local preview path.
- After opening the preview, stop. Do not generate the final full poster until the user chooses a direction or gives a clear mix instruction.
- The preview response must include the future export standard: HTML plus high-resolution PNG, default 3x, width at least 1200px, and designed multi-panel images for tall outputs.

## Export Rules

Use `scripts/export-poster.js` when available. It renders HTML with Playwright/Chrome, exports a high-DPI PNG, checks horizontal overflow, verifies dimensions, and can export designed panels for very tall posters.

Recommended command shape:

```bash
node scripts/export-poster.js path/to/poster.html --out path/to/poster-3x.png --scale 3 --split
```

When `--split` is used, the script first exports `.poster-panel` or `[data-poster-panel]` elements as `panels/panel-xx.png`. Hard `segments/part-xx.png` output is fallback only.

If Playwright's bundled browser is missing, use a local Chrome executable when available.

Use `scripts/score-run.js path/to/run/outputs` to score saved eval outputs against the 90% success gate.

## Common Failure Modes

- **Only changing colors across three demos**: reject and redesign the candidates.
- **PNG looks incomplete in chat preview**: check the actual file dimensions; if complete, deliver designed multi-panel PNGs too.
- **Hard slicing a long poster**: prefer `.poster-panel` sections and export `panels/panel-xx.png`; only hard slice as fallback.
- **Low-resolution export**: increase scale until width is at least 1200px.
- **Slide deck leakage**: do not create many `100vh` slides; long posters are continuous canvases.
- **API key confusion**: Codex native `image-2` does not need `OPENAI_API_KEY`; `imagegen` CLI does.
- **Weak image integration**: do not merely mention `image-2`; decide whether generated imagery is needed, choose native `image-2` or `imagegen` CLI, and report asset QA.

## When to Use Web Research

Browse when the design direction depends on current examples, a niche visual culture, a named brand/category, or when the user asks for modern/trendy/current aesthetics. Use primary or reputable sources where possible, and summarize the visual implications rather than dumping research notes.

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- When the user confirms a preview direction (for example A/B/C), preserve that direction as the base visual system and move directly into final production instead of re-proposing directions.
- For long posters and similar visual-output tasks, treat image-model augmentation as a normal design lever, not a niche option for one theme. Include generated-image roles in the style directions when visuals can materially improve the result.
- When proposing directions, make the image policy explicit enough for the user to choose: whether to use generated imagery, what role it plays, and whether text, faces, logos, real people, product marks, or brand marks are allowed.
- Generated visuals should reinforce the poster's subject matter and chosen direction. Prefer several purposeful assets for different roles over one repeated decorative image when the layout benefits from it.
- For very tall social posters, prefer designed 9:16 poster-panel sections that can each be exported as a complete shareable PNG, while also exporting the full long PNG.
- Final handoff should be short but include exact file paths, dimensions, overflow status, full-height completeness, panel output, and image generation boundary.

### Known Fixes & Workarounds
- Do not place generated imagery behind dense text. Use it as framed inserts, hero panels, or section strips unless contrast is verified.
- Do not hard-code no text, no logo, or no faces as universal rules. Those constraints should come from the user's prompt or from options the user selects after seeing the directions.
- When the user has not specified image constraints, present the default tradeoff clearly: generated assets with no embedded text/logo/identifiable face are usually easier to integrate cleanly, while text/logo/faces can be used when the user explicitly wants them.
- Treat decorative elements that exceed the viewport as horizontal overflow even if visually intentional; pull them back into bounds and re-export until overflowCount is 0.
- After export, visually inspect panel PNGs for text clipping, awkward line breaks, image overlap, and bottom completeness; patch typography/layout and rerun export when needed.
- If the default Node environment lacks Playwright, use the Codex desktop workspace runtime by setting NODE_PATH to the bundled node_modules and running the bundled Node executable.

### Custom Instruction Injection

### Poster Finalization Pattern
- After the user chooses a preview direction, use that exact direction as the final visual base.
- In preview directions, include generated-image strategy when it can improve the poster: asset role, visual style, integration location, and whether text/faces/logos/real marks are included or avoided. Let the user choose these constraints when they are not already specified.
- If the user asks for 生图模型效果图 or richer visuals, generate 2-3 subject-specific image-2 assets aligned to the chosen direction. Copy the assets next to the HTML and record source/status in output.md.
- Keep critical poster copy as HTML unless the user explicitly wants text embedded in generated imagery. If generated images include text, faces, logos, or real marks, verify they match the user's chosen direction and do not damage legibility or trust.
- For long WeChat/social posters, build natural .poster-panel / data-poster-panel sections, ideally complete 9:16 cards, so the final export includes both poster-3x.png and panels/panel-xx.png.
- Before final handoff, rerun export until PNG width >= 1200px, PNG decodes, full height matches render, overflowCount is 0, and panel visual QA catches no clipped text, bad line breaks, or image-text overlap.