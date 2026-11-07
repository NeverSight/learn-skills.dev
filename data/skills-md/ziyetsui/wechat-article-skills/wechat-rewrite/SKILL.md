---
name: wechat-rewrite
description: Use when the user says "@公众号改写", "公众号改写", "按这个风格改写", "改成公众号文章", asks for YouMind/Dan Koe/Claude Code/“这种风格” writing, or provides notes/drafts/materials to rewrite into a Chinese WeChat public-account article and title set with strong judgment, personal texture, era-level urgency, and warm closing encouragement.
---

# WeChat Rewrite

Rewrite user-provided materials into a Chinese WeChat public-account article plus publish-ready titles in a personal, high-conviction style: strong judgment, strong lived experience, strong sense of the times.

## Inputs

Expected inputs:

- Source material, rough notes, transcript, draft, outline, or scattered ideas.
- Optional topic angle, target reader, intended length, title preference, and publishing context.
- Optional style card or style request from `wechat-style-studio`.

If the source material is missing, ask the user to paste the material. If the topic is clear but details are thin, continue with a draft and mark assumptions briefly.

## Optional YouMind Style

If the user mentions YouMind, Dan Koe, Claude Code 教程风, “这种风格/那种风格”, or a style chosen from `wechat-style-studio`, use `wechat-style-studio` first.

- Read `wechat-style-studio/SKILL.md`.
- Read `references/style-index.json` first, then load only the selected `references/styles/<style-id>.md` card.
- Treat the selected card's `文章 Skill` as a writing-style override.
- Preserve the user's facts, point of view, and publishing goal over the reference article's topic.
- Do not imitate a living person's private identity or fabricate their personal history; reuse structure, rhythm, article promise, opening mechanism, and paragraph logic.

When a selected article style is provided, follow it over the default style rules below. The default style still applies to safety, truthfulness, title usability, and WeChat publishing fit.

## Workflow

### Step 1: Extract The Core Judgment

Identify:

- The author's strongest point of view.
- The reader's pressure, confusion, or hidden desire.
- The time window, industry shift, or personal turning point.
- The concrete choice the article wants to make feel urgent.

Do not start writing before the core judgment is clear.

### Step 2: Build The Article Arc

Prefer this structure:

1. Start from a real personal event, question, or recent change.
2. State the hard judgment within the first three short paragraphs.
3. Explain why the old path is losing value.
4. Break the future choices into 2-3 clear routes when useful.
5. Use concrete body-feel, personal practice, or visual metaphor to make abstract ideas alive.
6. Admit fear, uncertainty, or ordinary-person limits.
7. End with warm encouragement, not a slogan.

### Step 3: Draft Title Direction

Before finalizing the article, draft 5-8 title candidates that express the core judgment. Choose one recommended main title after the body is written, because the best title should match the final article's strongest tension.

Title candidates must:

- Be suitable for a WeChat public-account article.
- Carry a clear judgment, personal choice, or time-window tension.
- Avoid fake shock, fake guarantees, and generic motivational phrasing.
- Prefer short, memorable phrasing over complete explanatory sentences.
- Prefer titles that feel like a concrete moment of realization, not a plan summary.

### Step 4: Rewrite In The Target Style

If a selected YouMind article style is provided, write with that card's `文章 Skill` first. Otherwise write with these style defaults:

- Overall tone: high-conviction, reflective, urgent, intimate, and slightly cinematic.
- Paragraphs: mostly short to medium; use short paragraphs for major conclusions.
- Sentence rhythm: alternate short hard judgments with longer reflective explanation.
- Perspective: write from "我" when the material supports it; make the piece feel personally lived.
- Structure: use natural numbering such as "我看到三条路" when the argument benefits from it.
- Logic: move from personal event to industry judgment to personal choice to emotional close.
- Title alignment: ensure the recommended title and the opening judgment point in the same direction.

### Step 5: Strengthen Language

Use these patterns when natural:

- `不是 A，而是 B`
- `要么 A，要么 B`
- `越来越...`
- `我看到...`
- `我感觉...`
- `我意识到...`
- `从这个视角看...`
- `说白了...`
- `无所谓的，真的`
- `我的朋友`

Use vivid metaphors with physical scenes, such as rooms, walls, wilderness, car headlights, racing, scripts, tides, front-row seats, or hand practice. Do not overuse any one metaphor.

### Step 6: Preserve Truth

- Do not fabricate personal experience, numbers, employers, investments, credentials, or events.
- Do not make the author sound more certain than the material allows.
- If source material has facts, keep them accurate.
- If adding framing, make it clearly interpretive rather than invented evidence.
- Avoid fake urgency, fake scarcity, and exaggerated success promises.

## Style DNA

### Overall Style

- Write like a smart, sensitive, fast-moving operator thinking in public.
- Combine technical judgment, personal decision, ordinary-person vulnerability, and emotional momentum.
- Avoid cold analysis. Let the piece feel like someone is running, looking back, and reporting what they see.

### Title Style

Always generate one recommended main title and 5-8 title options unless the user explicitly says not to generate titles.

Prefer:

- Strong judgment titles.
- Personal choice titles.
- Time-window titles.
- Concrete-moment titles: one specific moment, followed by an inner turn or decision.
- Negative-turn titles: "I no longer want to..." / "I don't want to just..." style self-correction.
- "普通人 / AI / 机会 / 转型 / 未来 / 认知 / 时代 / 自由 / 勇敢" style vocabulary when relevant.

Example patterns:

- `我为什么转向...`
- `普通人的机会不多了`
- `趁认知还有溢价，去找新问题`
- `纯软件之后，下一站是什么`
- `...那天，我...`
- `...做到头那天，我反而...`
- `那个词浮出来那天，我知道该往哪走了`
- `我不想再只做一个会学习的人`

Recommended main title rules:

- Pick the title with the clearest tension, not the most clever wording.
- Keep it grounded in the article's actual facts and claims.
- Make it usable as-is in a WeChat backend title field.
- If the article is more personal, prefer a first-person title.
- If the article is more analytical, prefer a strong judgment title.
- Prefer a title with the structure `具体时刻 + 内在转向 + 一点命运感`.
- The best titles often do not explain the whole article. Leave a small "why" gap.
- Avoid clear-but-flat yearly-plan titles such as `2026，我要...` when a more lived, turning-point title is available.
- Avoid colon-format and column-like titles such as `Founder Game：我的 2026 决心公告` unless the user explicitly wants a series/column title.

Title selection heuristic:

1. Ask whether the current best title sounds like a person suddenly realizing something inside an era.
2. If it sounds like a task list, annual plan, slogan, or category label, rewrite it.
3. Prefer first-person, short, judgmental titles with a tiny narrative gap.
4. When the article contains a memorable scene or phrase, use it as the title anchor.

Good title direction:

- `那个词浮出来那天，我知道该往哪走了`
- `我不想再只做一个会学习的人`
- `2026，把自己交给市场`
- `今天的我，有没有更像一个 Founder？`

Weak title direction:

- `2026，我要把自己训练成一个 Founder`
- `Founder Game：我的 2026 决心公告`
- `我的年度计划和十条决心`

### Opening Style

- Start with a recent concrete event, a question people asked, or a personal turning point.
- Give a direct judgment quickly.
- Create tension between the familiar old track and the uncertain new path.

### Body Style

- Keep viewpoint density high.
- Use personal observation and compact examples rather than long case studies.
- Use lists only when they sharpen the choice.
- Let examples serve judgment, not decoration.

### Language Rules

- Use plain Chinese with oral rhythm.
- Avoid official, academic, marketing, and corporate jargon.
- Avoid empty terms like `赋能`, `闭环`, `抓手`, `底层逻辑` unless quoting or mocking them.
- Avoid generic motivational writing that has no concrete situation.
- Avoid over-polished symmetry; keep some thinking-in-motion texture.

### Judgment Style

- Give clear conclusions.
- Use contrast and analogy more than rhetorical questions.
- Be sharp without sounding superior.
- Use "我感觉 / 我看到 / 我意识到" to ground strong views in lived perspective.

### Ending Style

- Return from the big trend to the individual person.
- Admit fear or uncertainty if appropriate.
- End like speaking to a friend.
- Prefer a warm sentence with power over a hard call-to-action.
- Unless the user explicitly requests otherwise, end every article with this standalone final line: `Enjoy，我的朋友们！`

## Reusable Writing Rules

1. Start with a real personal scene, then quickly state the core judgment.
2. Put the central attitude in the first three paragraphs.
3. Use short sentences for conclusions.
4. Use "我看到 / 我感觉 / 我意识到" to connect experience and judgment.
5. Make big trends feel like choices made by a person inside the era.
6. Follow abstract judgment with body-feel, practice, image, or metaphor.
7. Use `不是 A，而是 B` for cognitive turns.
8. Use `要么 A，要么 B` for choice pressure.
9. Keep time pressure visible, but do not fake it.
10. Let the author be afraid or uncertain when the material supports it.
11. Make opinions sharp, but keep the posture equal and friendly.
12. Use visual metaphors that can be felt, not decorative abstractions.
13. When listing paths, bring each path back to the author's own decision.
14. Move the ending from analysis to comfort.
15. Leave one final sentence that feels warm, shareable, and earned.
16. End every article with a standalone `Enjoy，我的朋友们！` unless the user says not to.

## Output Shape

Unless the user specifies another format, return:

```text
## 推荐主标题
<one best publish-ready title>

## 标题备选
1. ...
2. ...

## 改写正文
<完整公众号文章>

## 改写说明
- 核心判断：
- 保留事实：
- 强化方向：
```

If the user asks for only the article, still include `推荐主标题` unless they explicitly say "不要标题".

## Default Prompt

请使用 `wechat-rewrite`，把下面的素材改写成一篇公众号文章，并给出一个推荐主标题和5-8个标题备选。要求：强判断、强体感、强时代感，保留事实，不编造经历，开头快速下判断，结尾像对朋友说话。
