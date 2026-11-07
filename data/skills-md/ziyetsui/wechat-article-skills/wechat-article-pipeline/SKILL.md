---
name: wechat-article-pipeline
description: Use when the user says "@公众号流水线", "公众号全流程", "wechat-article-pipeline", "改写生成封面排版推草稿箱", asks to use “这种风格/那种风格”, YouMind/Dan Koe/Claude Code style, or wants one coordinated workflow that chooses a style, rewrites source material into a Chinese WeChat article with titles, generates a cover image, formats WeChat-ready HTML, and uploads it to the WeChat Official Account draft box.
---

# WeChat Article Pipeline

Coordinate the full WeChat public-account production workflow from raw material to draft-box upload. This skill is an orchestrator: use the child skills for the actual work, keep artifacts organized under the current "今日公众号 项目", and avoid duplicating their detailed instructions.

## Child Skills

Use these skills in order when the requested scope includes the step. Read each child skill's `SKILL.md` before acting on that step.

- `wechat-style-studio`: recommend, select, or mix YouMind-derived article and cover styles.
- `wechat-rewrite`: rewrite source material into a publish-ready article and title set.
- `wechat-cover-image`: generate a WeChat cover image from the rewritten article.
- `wechat-layout`: convert the rewritten article into clean WeChat-ready HTML and plain text.
- `wechat-publish-draft`: upload the HTML and cover to the WeChat Official Account draft box only.

If the user asks for only one stage, use the matching child skill instead of forcing the full pipeline.

## Default Workspace

Unless the user gives another target directory, create one folder per article under the current "今日公众号 项目":

```text
/Users/ziye/Library/Mobile Documents/com~apple~CloudDocs/wiki/40-49 Brand and Content Operations/41 Personal Brand Assets/41.19 今日公众号 项目
```

Folder naming:

```text
YYYY-MM-DD-<short-slug>
```

Preferred artifact names must follow the project `.rule`:

```text
source.md
rewritten.md
cover-900x383.jpg
cover-square.jpg
article.html
article.txt
draft-result.json
```

Use ASCII slugs for filenames. Chinese titles can stay inside the Markdown, HTML, and JSON files. Keep all generated article artifacts in the article folder; do not scatter intermediate files elsewhere.

## Workflow

### Step 1: Clarify Scope And Style

Determine which stages are requested:

1. Rewrite only.
2. Rewrite + cover.
3. Rewrite + cover + layout.
4. Rewrite + cover + layout + draft-box upload.

For `wechat-article-pipeline`, the default scope is all four stages, including draft-box upload. The upload step creates a backend draft only; it must not publish publicly or mass-send.

If the user mentions style selection, YouMind, Dan Koe, Claude Code 教程风, “这种风格/那种风格”, or asks for recommendations, use `wechat-style-studio` before rewriting:

- Read `wechat-style-studio/SKILL.md`.
- Read `references/style-index.json` first.
- Recommend 3-5 styles if the user has not already chosen one.
- Load only the selected `references/styles/<style-id>.md` card.
- Save the selected article style and cover style names in the production notes.

If the user asks to mix styles, allow one selected card for the article style and one selected card for the cover style. If no style is requested, proceed with the default `wechat-rewrite` and `wechat-cover-image` styles.

If the source material is missing, ask for it. Otherwise proceed.

### Step 2: Create Article Folder

Create the article folder before generating files. Save the user's original material as `source.md` unless it already exists in a user-provided file.

Slug rules:

- Prefer a short lowercase English slug from the topic.
- Use `article` if the topic is unclear.
- If the folder exists, append `-2`, `-3`, etc.

### Step 3: Rewrite

Use `wechat-rewrite` on the source material. If a YouMind style was selected, pass the selected style card's `文章 Skill` as the writing-style override. Save the complete output as `rewritten.md`.

Required rewrite output:

- Recommended main title.
- 5-8 title candidates.
- Full article body.
- Short rewrite notes.

Do not move to cover generation until the recommended title and article body are present.

### Step 4: Generate Cover

Use `wechat-cover-image` with the recommended title and rewritten article. If a YouMind style was selected, pass the selected style card's `封面 Skill` as the visual-style override. Save or rename outputs to:

- `cover-900x383.jpg`
- `cover-square.jpg`

Validate that the main cover is exactly `900x383` and the square cover is exactly `500x500`.

### Step 5: Layout

Use `wechat-layout` on `rewritten.md`. Save:

- `article.html`
- `article.txt`

Validate that the HTML contains only the final article body, not title candidates or rewrite notes. Keep the recommended title separately for draft upload.

### Step 6: Draft-Box Upload

Run this step as part of the full pipeline.

Use `wechat-publish-draft` with:

- `article.html`
- recommended title from `rewritten.md`
- `cover-900x383.jpg`

Start with `--dry-run` only if the user asks for a trial, setup check, or validation. Otherwise create a real draft in the Official Account backend draft box.

Never publish publicly, mass-send, call freepublish APIs, or click a UI publish button as part of this pipeline.

Always save `draft-result.json`. If upload was not attempted because of an error in an earlier stage, set `status` to `failed` or `pending` and explain why in `notes`.

## Failure Handling

- If rewrite succeeds but cover generation fails, keep `rewritten.md` and `cover-prompt.md`, report the image API error, and stop before layout only if the cover is required for the next step.
- If layout succeeds but draft upload fails, keep `article.html`, `article.txt`, and the cover files, then report the WeChat `errcode` and next action.
- If WeChat returns an IP whitelist error such as `40164`, tell the user to add the current outbound IP to the Official Account backend IP whitelist.
- Do not expose API keys, AppSecret, access tokens, or full credentials in the final response.

## Output Shape

Return a compact production summary:

```text
## 公众号流水线结果
- 状态：
- 标题：
- 风格：
- 文章目录：

## 产物
- 改写稿：
- 封面：
- 排版 HTML：
- 草稿箱：

## 下一步
- 后台检查项或失败后的处理动作。
```

When upload succeeds, report that the backend draft was created and ask the user to inspect it in the WeChat Official Account backend before any public publishing.
