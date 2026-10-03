---
name: markitdown
description: 把任何"非纯文本"文件转成 Markdown 喂给 AI 的统一预处理 Skill(微软 MarkItDown CLI 封装)。当用户丢来 / 引用一个文件让你读、总结、提取、翻译、问答、对比时使用——尤其是 .docx / .xlsx / .pptx / .xls(Office 二进制)、.pdf、.epub、.html、.csv / .json / .xml、.zip、.msg(Outlook)、音频(.mp3 / .wav / .m4a 转写),甚至 YouTube 链接。触发词:"读一下这个文件 / pdf / word / excel / ppt"、"把这个文档转成 markdown"、"这个文件讲了啥"、"提取 / 总结 / 翻译这个文档"、"处理一下这个附件"、"convert this file"、"read this docx / xlsx"。**用户长期约定:以后任何丢给 AI 的文件都先用 MarkItDown 处理一下**——见到文件优先想到本 Skill。例外:纯文本 / 代码直接 Read 即可;图片和扫描版 PDF 用原生视觉 Read 更好(MarkItDown 抽不出图里的字)。不要 under-trigger。
---

# MarkItDown — 文件 → Markdown 统一入口

把 PDF / Office / 图片 / 音频 / HTML / EPUB / ZIP 等各种格式统一转成干净的 Markdown,**再喂给 AI 读**。封装微软开源 [MarkItDown](https://github.com/microsoft/markitdown)。跨 Claude Code / Codex / 任何兼容 SKILL.md 的平台可用。

> **用户约定**:以后任何丢给 AI 的文件,默认先过一遍 MarkItDown,而不是直接把二进制塞进上下文或全靠人肉描述。

---

## 何时用 / 何时不用(先判断,别无脑跑)

| 文件类型 | 怎么处理 |
| --- | --- |
| Office 二进制 `.docx .xlsx .pptx .xls` | **MarkItDown**(原生 Read 读不了二进制,必须转) |
| `.pdf`(文本型 / 电子版) | **MarkItDown** 抽文本,快且省 token |
| `.pdf`(扫描件 / 图多 / 图文混排) | **原生视觉 Read 优先**;MarkItDown 抽不出图里的字 |
| 图片 `.png .jpg .jpeg .webp` | **原生视觉 Read 优先**;MarkItDown 只抽 EXIF,不做视觉 OCR |
| 音频 `.mp3 .wav .m4a` | **MarkItDown**(转写;本机 ffmpeg 已装) |
| `.html .epub .msg`(Outlook)`.zip`(递归解包内部文件) | **MarkItDown** |
| `.csv .json .xml .tsv` | 小的直接 Read 即可;要表格化 / 大文件用 MarkItDown |
| 纯文本 / 代码 `.txt .md .py .go .log` … | **直接 Read**,无需转换 |
| YouTube 链接 | **MarkItDown**(抽字幕)`markitdown "https://youtu.be/..."` |

一句话:**二进制文档类一律 MarkItDown;纯视觉内容(图、扫描件)走原生视觉 Read;纯文本直接 Read。**

---

## 标准流程(给 AI 的三步)

1. **转**:`markitdown <文件> -o <输出>.md`(大文件务必落盘成 `.md`,别用 stdout 直接吞进上下文)。
2. **读**:用 Read 工具读那个 `.md`,需要哪段读哪段。
3. **办**:在 Markdown 上做总结 / 提取 / 翻译 / 问答。

```bash
# 单文件 → stdout(小文件、快速瞄一眼)
markitdown report.pdf

# 单文件 → 落盘(推荐:大文件、之后要反复 Read)
markitdown report.pdf -o /tmp/report.md

# stdin(从管道来的文件流)
cat report.pdf | markitdown

# 批量 / 输出到目录(本 skill 的封装脚本)
scripts/mdconvert.sh -o /tmp/out *.docx *.xlsx
scripts/mdconvert.sh -p one.pdf          # 只打印不落盘
```

> 路径里有空格 / 中文 → 一定加引号:`markitdown "我的 报告.pdf" -o /tmp/out.md`。

---

## 支持的格式(MarkItDown 全家桶,本机已装 `[all]` extras)

PDF · Word(.docx)· Excel(.xlsx/.xls)· PowerPoint(.pptx)· HTML · EPUB · Outlook(.msg)· CSV/JSON/XML · ZIP(递归解包)· 图片(EXIF + 可选 LLM 描述)· 音频(EXIF + 语音转写)· YouTube URL。

---

## 坑 & 边界(踩过的)

- **图片 / 扫描 PDF 不是视觉 OCR**:MarkItDown 对图片默认只抽 EXIF 元数据,对扫描版 PDF 只能抽出本就嵌着的文本层——图里的字它读不出来。这类**优先用原生视觉 Read**(模型自带视觉),别指望 MarkItDown 帮你认图。
- **转换产物可能含敏感信息**:文档里常藏 token / 密码 / JWT / 个人信息(实测一个含登录态的 `.docx` 转出来就是整串 accessToken)。**转出来的 Markdown 别整段回显到聊天、别 commit 进仓库、别外传**;落盘优先放 `/tmp`,用完该删就删。
- **大文件**:几十页 PDF / 大 Excel 直接 stdout 会把上下文撑爆。**先 `-o` 落盘成 `.md`,再按需 Read 片段**。
- **音频转写需 ffmpeg**:本机 `~/.local/bin/ffmpeg` 已装,mp3/m4a/wav 都能转写。换机器若没 ffmpeg → `brew install ffmpeg`。
- **图片要"描述"而非只抽 EXIF**:MarkItDown 支持传 LLM client 给图片生成描述,但 CLI 默认不开。要图片内容描述,直接用原生视觉 Read 更省事。
- **不确定能不能转**:直接 `markitdown <文件>` 试一把;失败会非零退出 + 报错,fallback 到原生 Read。

---

## 安装 / 维护(本机已装好,换机才需要)

本机已通过 uv tool 全局安装,CLI 在 `~/.local/bin/markitdown`(已在 PATH):

```bash
# 全新安装(全格式 extras)
uv tool install 'markitdown[all]'

# 升级
uv tool upgrade markitdown

# 自检
which markitdown && markitdown --help | head -3
```

> 没有 uv 就 `brew install uv`;装在 uv 隔离环境里,不污染系统 / 项目 Python。
