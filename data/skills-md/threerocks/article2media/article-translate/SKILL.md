---
name: article-translate
description: 全文翻译：把一篇外文文章（多为英文 X 长文、网页、逐字稿）完整译成中文 article.zh.md——不删减、不总结、不改写结构，标题、段落、列表、引用、表格、图片与原文逐块对应，代码和链接原样保留；脚本检查块数和结构是否一致、有没有漏译、没翻译或丢了数字。译文可以直接交付，也可以接原文长图、原文卡片、公众号排版（外文搬运）。Use when the user wants an article translated in full (翻译这篇、全文翻译、译成中文、搬运外文文章、英文转中文发公众号/小红书), or when an article2media original-text layout gets a source in another language than the reader's.
argument-hint: <article.md|目录> [--to zh|en]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
version: "2.0.1"
---

# 全文翻译（article-translate）

把 `article.md` 译成 `article.zh.md`。这是**翻译**，不是改写：一句不删、一句不加，结构与原文逐块对应。要提炼、总结，用 `article-rewrite`。

参数：`$ARGUMENTS`

## 输入

`article.md`。给的是链接、文件或视频时，先用 `article-fetch` / `video-transcript` 取原文（见 `../article2media/references/pipeline.md`）。默认译成简体中文；用户要别的语言时，文件名用对应代码（`article.en.md`），规则相同。

## 1. 看清原文
```bash
node ${CLAUDE_SKILL_DIR}/scripts/translate.mjs stats <目录>/article.md
```
告诉你一共多少块（段落、标题、列表项、表格单元、图注……）、多少词。然后**完整读一遍**原文。

## 2. 翻译
读 `references/translate-guide.md`，然后写 `<目录>/article.zh.md`：
- **front matter**：复制原文的全部字段；`title` 换成中文标题；加 `lang: "zh"`、`translated_from: "article.md"`、`source_title: "<原标题>"`。
- **正文**：逐块翻译，块的种类和顺序不变——原文一段就是译文一段，一个列表项就是一个列表项，表格行列不变，`# 标题` 那行换成中文标题。
- **原样保留**：代码块、图片 `![…](地址)`、链接地址、人名和品牌名的原文写法（可以首次出现时括注中文）。
- 原文里粗体、斜体在哪，译文对应的词也加上。
- 长文分几次写完没关系（先写前半，再用编辑追加），但不能为了省事概括。

## 3. 检查
```bash
node ${CLAUDE_SKILL_DIR}/scripts/translate.mjs check <目录>/article.md <目录>/article.zh.md
```
- ✗（块数不一致、某块类型变了、代码或图片地址被改）必须修，直到 0 个错误。
- ⚠ 逐条看：「像是没翻译」「比其他段短很多（可能漏译）」「数字没找到」。确实是名字、链接或把数字写成了汉字的，可以保留，交付时说明。

## 4. 交付
- 单独使用时：`article.zh.md` 的绝对路径、块数（"42 / 42 块对应"）、检查结果，以及你保留原文的专有名词。
- 在组合里（外文搬运、原文卡片）：把 `article.zh.md` 交给下一个能力——它对排版来说就是"原文"，按一字不改的规则排。来源写明「译自 <作者> 的<平台>文章《原标题》」。
- 翻译他人文章公开发布前，提醒用户确认授权。
