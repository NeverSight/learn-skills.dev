---
name: article-fetch
description: 文章抓取：把一篇文章转成干净的 Markdown（article.md，带标题、作者、平台、日期、链接的 front matter）。支持 X/Twitter 长文、帖子与线程（FxTwitter，不需要登录）、普通网页、微信公众号文章、本地 Markdown / 文本 / HTML 文件。article2media 的第一步，也可以单独用。Use when the user wants an article, X post or thread, web page or 公众号文章 fetched / saved / converted to Markdown (抓取文章、把这篇存成 markdown、提取正文、导出原文), or when another article2media skill needs the original text from a URL.
argument-hint: <url|文件> [--out 目录] [--no-proxy] [--title 标题] [--author 作者]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
version: "2.0.1"
---

# 文章抓取（article-fetch）

把任意文章变成 `article.md`：后面所有能力（改写、翻译、长图、卡片、公众号、口播、白板、漫画）都从这份文件开始。视频不归这里管，用 `video-transcript`。

参数：`$ARGUMENTS`

## 1. 环境检查（本会话第一次）
```bash
node ${CLAUDE_SKILL_DIR}/scripts/doctor.mjs
```
需要 Node 22+；网页和公众号要用到本机 Chrome。失败时把修复建议转告用户，然后停下。

## 2. 抓取
```bash
node ${CLAUDE_SKILL_DIR}/scripts/fetch.mjs "<url 或文件>"            # 默认输出到 ./article2media-out/<slug>/
node ${CLAUDE_SKILL_DIR}/scripts/fetch.mjs "<url>" --out <目录>      # 指定目录
```
- **X / Twitter**：通过 FxTwitter 公开 API，长文、帖子、线程都支持，不需要登录。`x.com/i/article/…` 这种内部链接解析不了，请用户给发布文章的那条推文链接。
- **普通网页**：依次尝试 r.jina.ai、defuddle.md，最后用本地 Chrome 提取。加 `--no-proxy` 不经过第三方服务。
- **微信公众号**：直接用本地 Chrome 提取。
- **本地文件**：Markdown / 文本直接读，HTML 用 Chrome 提取正文。`--title`、`--author` 可以补标题和作者。
- **用户直接粘贴正文**：不用抓取，自己写 `./article2media-out/<简短英文 slug>/article.md`：front matter 写 `title`、`author`、`platform`、`date`，正文第一行 `# 标题`，其余原样粘贴，不改字。
- 给的是视频链接、音视频或字幕文件时，脚本会拒绝并提示：改用 `video-transcript`。

输出：`<目录>/article.md`、`meta.json`；终端打印一段 JSON（目录、标题、作者、平台、字数）。

## 3. 检查
**完整读一遍** `article.md`：
- 正文明显不全（只有摘要、被登录墙截断、只抓到评论区）时，告诉用户，请对方粘贴正文；
- 标了 `<!-- 未识别的内容块 -->` 的地方可能缺内容，交付时说明。
- 脚本提示「⚠ 正文只有 N 字，主要内容可能在视频 / 图里」时（常见于图解帖、短视频帖）：X 帖子的视频写成了「封面图 + ▶ 视频链接」。先看图；视频用 ffmpeg 抽帧（第一帧常是带标注的完整图解）看画面。有配音的交给 `video-transcript`；只有画面文字的，把文字按原语言逐字整理进 `article.md`（放在对应的图 / 视频后面，用原文的分组做小标题），交付时说明哪些内容来自画面。

## 4. 交付
单独使用时：给出 `article.md` 的绝对路径、标题、作者、平台、字数，以及上面发现的缺漏。
在组合里：把目录交给下一个能力（见 `../article2media/references/pipeline.md`）。
