---
name: wechat-layout
description: 公众号排版：把一篇文章（Markdown）排成能直接粘贴进公众号编辑器的图文——内联样式、图片内嵌、21 套主题配色，附 2.35:1 头图、1:1 封面和发布信息（标题、摘要、步骤）；正文一字不改，逐块读回校验。只接受文章：原文（article.md）、译文（article.zh.md）或改写稿导出的文章（rewrite.md，即"总结后发公众号"）。可以单独用，也可以接在抓取、翻译、改写后面。Use when the user wants 公众号排版, 微信公众号文章排版, 推文排版, gzh, mp.weixin formatting, "排成公众号/发公众号", or to paste a Markdown article into the WeChat editor.
argument-hint: <article.md|rewrite.md|目录> [--theme 主题名] [--title 标题] [--digest 摘要] [--cover-title "两行\n标题"] [--out 目录]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
version: "2.0.1"
---

# 公众号排版（wechat-layout）

把一篇**文章**排成可粘贴的公众号图文。正文一字不改；改不改写、译不译，在排版之前决定。

参数：`$ARGUMENTS`

## 0. 先确定排哪篇文章

| 情况 | 做法 |
|---|---|
| 给了 `.md` 文章，或说"排版 / 原文" | 直接排它 |
| 给的是链接、文件、粘贴的正文或视频 | 先用 `article-fetch` / `video-transcript` 取原文 |
| 说"总结 / 提炼 / 改写后发公众号" | 先用 `article-rewrite` 写 content.json（加 `wechat.title`、`wechat.digest`），再用它的 `export.mjs` 导出 `rewrite.md`，排 `rewrite.md` |
| 原文是外文，读者是中文 | 先用 `article-translate` 出 `article.zh.md`，排译文 |
| 只说"发公众号"，没说原文还是总结 | 默认**原文排版**；一篇别人的长文、结果差别又大时，问一句"原文排版还是总结后再排" |

给的是 `content.json` 时脚本会拒绝：公众号排版只吃文章，先导出 `rewrite.md`。判断规则和工作目录见 `../article2media/references/pipeline.md`。

第一次使用先跑 `node ${CLAUDE_SKILL_DIR}/scripts/doctor.mjs`（Node 22+、Chrome）。

## 1. 排版
```bash
node ${CLAUDE_SKILL_DIR}/scripts/wechat.mjs <目录>/article.md --check                # 只校验：解析、标题长度
node ${CLAUDE_SKILL_DIR}/scripts/wechat.mjs <目录>/article.md --theme quiet          # → <目录>/quiet-wechat/
node ${CLAUDE_SKILL_DIR}/scripts/wechat.mjs <目录>/rewrite.md                        # 主题默认用 rewrite.md 里记录的（图表按它截的图）
node ${CLAUDE_SKILL_DIR}/scripts/wechat.mjs <目录>/article.md --title "公众号标题" --digest "摘要" --cover-title "两行\n标题"
```
- 主题：用户指定 > 文章 front matter 的 `theme` > 按 `../article2media/references/styles.md` 选（没选时是 editorial）。`rewrite.md` 的图表是按导出时的主题截的图，换主题要先重新导出。
- 标题、摘要、封面标题的写法和限制见 `references/wechat-guide.md`。

## 2. 检查（最多 2 轮）
1. 版面检查：✗ 全文校验（逐块不一致）、图片没加载、标题超长、封面标题放不下，都必须修。正文问题改源头（article.md / content.json），不改 HTML。
2. **亲眼看**：打开 `cover-2.35x1.png`、`cover-1x1.png`；用浏览器或截图看一遍 `article.html` 的手机宽度效果。

## 3. 交付
- `article.html` 的绝对路径，告诉用户："浏览器打开 → 点「复制到公众号」→ 在编辑器正文里粘贴"；
- 贴出标题、摘要，以及两张封面的路径（`wechat.md` 里有完整发布步骤）；
- 排的是哪篇（原文 / 译文 / 改写稿）、全文校验结果（"44 / 44 块逐字一致"）、主题和理由；
- 有图片没能下载、仍是外链的，提醒粘贴后检查。
