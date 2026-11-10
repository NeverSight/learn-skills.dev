---
name: article-comic
description: 漫画：把一篇文章讲的机制做成黑白漫画分镜——你写认知因果拍点和固定角色（comic.json），生成图负责角色、场景和动作，HTML 负责旁白、对白、音效字（图里不画字）；同时输出一张长漫画和一组小红书 3:4 卡片。需要出图能力（Codex CLI 登录，或 OpenAI / Gemini 付费 key）。输入是文章（原文、译文、逐字稿）。可以单独用，也可以接在抓取、视频转文字后面。Use when the user wants a 漫画, 连环画, 四格, 分镜, comic strip, "把这篇做成漫画", or -c.
argument-hint: <article.md|目录|comic.json> [--theme 主题名]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
version: "2.0.1"
---

# 漫画（article-comic）

生成图让角色、场景、动作和结果可见；HTML 把文字写准确。同时输出长漫画和 3:4 卡片。

参数：`$ARGUMENTS`

## 0. 输入与能力
- 文章 `article.md`（原文、译文或逐字稿）。给的是链接、文件或视频时，先用 `article-fetch` / `video-transcript` 取原文（见 `../article2media/references/pipeline.md`）。
- **先确认有出图能力**：`node ${CLAUDE_SKILL_DIR}/scripts/doctor.mjs` 的 `ai-illustration` 一行。没有就告诉用户做不了漫画，建议改用长图（`long-image`）或白板（`logic-whiteboard`）。

## 1. 流程
1. **完整读一遍**文章，读 `references/mode-comic.md`，写 `<目录>/comic.json`（认知因果拍点 + 固定角色）。
2. `node ${CLAUDE_SKILL_DIR}/scripts/comic.mjs check <目录>/comic.json`，修完提示。
3. `node ${CLAUDE_SKILL_DIR}/scripts/comic.mjs make <目录>/comic.json`：出图（约 1–1.5 分钟一格，3 格并行）+ 排版。只改文字时用 `comic.mjs render`（分格已缓存）。
4. 讲概念、机制的内容，按 `../article-rewrite/references/writing-guide.md` 第 6 节把具体情形、判别依据、关系和结果接起来。

## 2. 审片与交付
- `comic/review/` 里有覆盖全部高度的重叠切片，逐张看完；也看每一格生成图里有没有画出文字、角色是否一致。
- 报告：PNG 路径与像素尺寸、来源、格数与因果链、生成图张数、用的出图服务；3:4 卡片目录。制作范围写在交付回复里，不写进图里。
