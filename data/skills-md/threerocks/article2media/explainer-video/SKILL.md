---
name: explainer-video
description: 口播视频：把一篇文章做成 1080×1920 竖屏讲解视频——你当导演写分镜脚本 video.json（黄金 5 秒钩子、每镜一个意思、回收要点），脚本完成配音（本地 VoxCPM2 / edge-tts / 系统语音，6 款公开音色）、逐字对齐、数字滚动和清单逐条出现等动画、主题样式字幕、封面、混音和自动审片。输入是文章（原文、译文、逐字稿），已有改写稿 content.json 时参考它的事实和结构。可以单独用，也可以接在抓取、视频转文字、改写后面。Use when the user wants a 口播视频, 短视频, 讲解视频, 视频号 / 抖音竖屏视频, 文字转视频, text-to-video or "把这篇文章做成视频".
argument-hint: <article.md|目录|video.json> [--voice 音色] [--theme 主题名] [--no-images]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
version: "2.0.1"
---

# 口播视频（explainer-video）

文章 → 竖屏讲解视频。**你是导演**：读懂内容、决定讲什么和怎么讲，写 `video.json`；脚本负责配音、对齐、动画、渲染、混音和审片。

参数：`$ARGUMENTS`

## 0. 输入
- 文章 `article.md`（原文、译文、逐字稿）。给的是链接、文件或视频时，先用 `article-fetch` / `video-transcript` 取原文（见 `../article2media/references/pipeline.md`）。
- 同目录已有 `content.json` 时，直接用它的事实、数字和结构，不必重新提炼。没有也不需要先改写：口播稿本身就是一种改写，由你在 video.json 里完成。
- 外文原文直接写中文口播即可，不需要先全文翻译。

## 1. 流程
1. `node ${CLAUDE_SKILL_DIR}/scripts/video.mjs doctor` 看本机能力（配音、对齐、插画、ffmpeg），按 `references/video-guide.md` 第 1 节决定要不要问用户（通常不用问）。
2. **完整读一遍**文章，再读 `references/video-guide.md`，写 `<目录>/video/video.json`：定调（受众、核心、开场策略）→ 封面 → 每镜口播和画面 → 选音色、选主题（按 `../article2media/references/styles.md`）。首句 ≤ 19 字、5 秒内说完；解说最忌急，说不完就删字，不加快语速。
3. `video.mjs check` 修完提示，再 `video.mjs make`（配音、可选插画、渲染、混音、审片一步完成；配音按句缓存，改口播只重配改动的句子）。
4. 按指南第 4 节审片：看 `contact-sheet.jpg` 和检查项，改 `video.json` 重渲，最多 2 轮。
5. 按指南第 5 节交付：视频、封面、镜头大纲、音色（公开 / 本机个人）、缺了哪些能力、发布前的 AI 声明提醒。

音色：默认用随包公开音色（`video.mjs voices` 查看）。克隆自他人或平台的音色只能进本机个人音色库，不能放进 skill 的公开音色目录；用了本机个人音色时，提醒公开发布前确认授权。
