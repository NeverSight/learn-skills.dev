---
name: wechat-style-studio
description: Use when the user wants to choose, browse, recommend, mix, or apply YouMind viral article styles, cover styles, writing styles, “这种风格/那种风格”, “Dan Koe 风格”, “Claude Code 教程风”, or data-ranked WeChat public-account article and cover style references before rewriting or generating a cover.
---

# WeChat Style Studio

Choose and apply YouMind-derived viral writing and cover styles for WeChat public-account articles.

## Core Rule

Use progressive disclosure. Never bulk-read all 830 style cards.

1. Read `references/style-index.json` first.
2. Shortlist 3-5 candidate styles from the index.
3. Ask the user to pick one, unless they already named a specific style.
4. Read only the selected style card from `references/styles/`.
5. Pass the selected article style to `wechat-rewrite` and the selected cover style to `wechat-cover-image`.

## Inputs

The user may provide:

- Source material for a WeChat article.
- A named style, such as `Dan Koe`, `Claude Code 教程`, `黑白寓言`, `浅底信息图`, or a YouMind title.
- A mixing request, such as “文章用 A 风格，封面用 B 风格”.
- No style at all; in that case, recommend styles.

If source material is missing, first help the user choose a style, then ask for the material.

## Style Selection

When recommending styles:

- Prefer topic match first.
- Then prefer high `metrics.bookmarks`, `metrics.likes`, and `metrics.views`.
- Keep visual variety: do not recommend five styles with the same cover class unless the user asked for that class.
- Show 3-5 candidates with title, author, article class, cover class, and why it fits.

Good candidate format:

```text
1. 如何用 1 天时间彻底重塑你的人生 — Dan Koe
   文章：强教练型清单教程；封面：黑白低饱和 editorial
   适合：个人成长、认知重塑、强行动承诺
```

When the user says “这种/那种风格” and points to an existing article or cover, match by:

1. Exact title/slug/author.
2. Article class and cover class.
3. Keywords in title, article hook, and cover hint.
4. Engagement score as tie-breaker.

## Applying A Style

After a style is selected:

1. Read the selected `references/styles/<style-id>.md`.
2. Extract the `文章 Skill` section and reuse its article prompt/fingerprint.
3. Extract the `封面 Skill` section and reuse its cover prompt/fingerprint.
4. If the user mixes two styles, read exactly two style cards: one for article, one for cover.
5. Summarize the selected pairing before writing:

```text
已选风格：
- 文章：<title> / <article class>
- 封面：<title> / <cover class>
```

## Coordination With Other Skills

- For rewriting, use `wechat-rewrite` after selecting the article style.
- For cover generation, use `wechat-cover-image` after selecting the cover style.
- For the full workflow, use `wechat-article-pipeline`; this style studio runs before rewrite and cover generation.

## Useful References

- `references/style-index.json`: compact machine-readable index for all 830 styles.
- `references/representative-styles.md`: recommended styles by score and visual class.
- `references/style-gallery.md`: human-readable gallery and full directory.
- `references/styles/`: full style cards; load only selected cards.

## Output Shape

When only selecting styles:

```text
## 推荐风格
1. ...

## 我建议
<one recommendation and why>

## 下一步
请回复编号，或说“文章用 1，封面用 3”。
```

When applying styles:

```text
## 已选风格
- 文章：
- 封面：

## 风格使用说明
- 写作：
- 封面：

## 交给后续 skill
- Rewrite: use `wechat-rewrite`
- Cover: use `wechat-cover-image`
```
