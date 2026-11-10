---
name: article-rewrite
description: 改写（总结）：把一篇文章读透、重组成一份和风格无关的结构化改写稿 content.json——核心主张、分页分节、每节的判断式标题、要点、金句、两张图表（柱状、流程、对比、结构等 20 多种）和数据面板，可选执行清单、核对数字、AI 插画；还能导出成一篇文章 rewrite.md（图表转成图片）。改写稿交给长图、卡片出图，rewrite.md 交给公众号排版。Use when the user wants an article summarized / restructured / 提炼 / 改写 / 整理成要点 for visual content, wants a 总结 before 长图、小红书卡片 or 公众号, or another article2media skill needs content.json; also when the user wants a structured summary article (总结稿) of a long post.
argument-hint: <article.md|目录> [--pages N] [--lang zh|en] [--verify] [--illustrate] [--style 主题名]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
version: "2.0.1"
---

# 改写（article-rewrite）

把一篇文章**重组**成改写稿 `content.json`：你负责读懂、规划、改写、选图、核对数字；脚本负责校验。改写稿只写内容，不含颜色和字体，换风格不用重写。改写和总结是同一件事。

参数：`$ARGUMENTS`

| 产出 | 给谁用 |
|---|---|
| `content.json`（改写稿） | `long-image`（杂志长图）、`image-cards`（总结卡片）、`explainer-video`（参考事实与结构） |
| `rewrite.md` + `rewrite-assets/`（改写稿的文章形态，`export.mjs` 导出） | `wechat-layout`（公众号总结），也可以直接给人读 |

## 输入

`article.md`（原文、译文或逐字稿）。给的是链接或文件时，先用 `article-fetch`（视频用 `video-transcript`）取原文；调用方式和工作目录见 `../article2media/references/pipeline.md`。同一篇已有 `content.json` 时**不要重写**：只补新版式需要的字段。

逐字稿是**口语**：去掉口头禅和重复，事实、数字、人名以视频为准；识别可能出错的专有名词对照 `transcript/segments.md` 判断，拿不准的交付时说明。来源写成「内容整理自 <作者> 的<平台>视频《标题》」。

第一次使用先跑 `node ${CLAUDE_SKILL_DIR}/scripts/doctor.mjs`（校验和导出要用到 Node 22+、Chrome；`ai-illustration` 一行是出图能力）。

## 1. 规划
**完整读一遍** `article.md`，再读 `references/writing-guide.md`，然后确定：
- 核心主张（一句话）；
- 页数和每页的 `part`，按 `references/content-schema.md` 末尾的密度表定（`--pages` 可强制 1–4 页）；
- 每节的标题、两张图的类型、面板类型；
- 主题：用户没指定时，按 `../article2media/references/styles.md` 选一个，写进 `theme`。

不需要先把大纲给用户确认，除非用户要求先看大纲。

## 2. 核对数字（只在 `--verify` 或用户要求时）
- 对文中 3–8 个关键数字或事实，用 WebSearch / WebFetch 查原始出处。
- 在对应面板里写明结论，例如"与 IAB 一致；2026 年为预测值""未找到出处"，面板标题写"· 编者核对"。
- 没核对时，任何地方都不能出现"核对"字样。

## 3. 写 content.json
写之前**必须**读 `references/content-schema.md` 和 `references/figures.md`（每种图表、面板的完整写法见 `examples/gallery.json`；一篇 3,700 词长文的完整示例见 `examples/dan-koe.json`）。写到原文同目录的 `content.json`，然后校验：
```bash
node ${CLAUDE_SKILL_DIR}/scripts/check.mjs <目录>/content.json                 # 长图
node ${CLAUDE_SKILL_DIR}/scripts/check.mjs <目录>/content.json --ratio 3:4     # 还要出卡片时，同时检查卡片
```
- 要出卡片时，再读 `../image-cards/references/xhs-guide.md`，写上 `cover`、`xhs`，需要时给个别节加 `card` 提示。
- 要出公众号总结时，再读 `../wechat-layout/references/wechat-guide.md`，写上 `wechat.title`、`wechat.digest`。
- ✗ 必须修完；⚠ 长度提示尽量处理（缩短文字）。
- 讲概念、机制的内容，按 writing-guide 第 6 节把具体情形、判别依据、关系和结果接起来。

## 4. AI 插画（只在用户要插画或传了 `--illustrate` 时）
1. 按 `figures.md` 的 illustration 一节写：`cover.illustration.prompt`（封面），再挑 1–2 个故事性强、缺数据的节，把其中一张图换成 `{"type": "illustration", "prompt": "…"}`。
2. 生成：`node ${CLAUDE_SKILL_DIR}/scripts/illustrate.mjs <目录>/content.json`。脚本按 content.json 的主题选画风；之后换主题要画风一致，就加 `--theme 新主题` 再生成一次。
3. 生成失败（没有出图能力、免费层没有图像额度等）时，把报错原话告诉用户，然后**去掉插画字段**照常继续。不要交付带"插画待生成"占位框的图。
4. 打开生成的图看一眼：有没有画出文字、主体是否清楚、和主题搭不搭。不满意就改 prompt，加 `--force` 重新生成。

## 5. 导出文章（公众号总结、或用户要一篇总结稿时）
```bash
node ${CLAUDE_SKILL_DIR}/scripts/export.mjs <目录>/content.json                 # → <目录>/rewrite.md + rewrite-assets/
node ${CLAUDE_SKILL_DIR}/scripts/export.mjs <目录>/content.json --theme quiet   # 图表按指定主题截图
```
- 图表截成图片，颜色跟主题走，主题写进 `rewrite.md` 的 front matter；公众号排版默认用同一个主题。换主题要重新导出。
- 导出后会把 `rewrite.md` 解析回来校验；有 ✗ 说明 content.json 里有会被当成 Markdown 结构的文字，按提示改 content.json 后重导，**不要手改 rewrite.md**。

## 6. 交付
- 单独使用时：`content.json`（和 `rewrite.md`）的绝对路径、一行大纲（每页的 part）、主题和理由，以及：要出图用 `long-image` / `image-cards`，要发公众号用 `wechat-layout` 排 `rewrite.md`。
- 在组合里：把目录交给下一个能力。
- 需要用户留意的：未核对的数字、抓取不全的段落、编者补的节、插画用的服务商和张数。
