---
name: deep-reading
description: Use when reading books, academic papers, or long-form documents from URLs or PDFs and needing structured analysis, comprehension, or comparison
---

# Deep Reading Agent v2

## Overview
深度阅读助手，支持 YouTube 视频、PDF 书籍、播客、网页等内容的深度阅读和笔记管理。基于 Mortimer Adler 的《如何阅读一本书》实现三层阅读：检视阅读、分析阅读、对比阅读。

## When to Use

当用户说以下内容时，自动触发此 skill：
- "帮我看/读/学习这个视频" + YouTube URL
- "深度阅读这个内容"
- "分析这个视频/文章"
- "阅读这本书" + PDF 路径
- "播放 xxx" (已下载的内容)

## Quick Start - AI 操作流程

### 1. YouTube 视频处理

当用户提供 YouTube URL 时：

```bash
# Step 1: 下载内容
cd /Users/liweixin/.claude/skills/deep-reading
python3 -m src.fetcher.cli "YOUTUBE_URL"

# Step 2: 生成检视阅读报告
python3 -m src.processor.cli youtube_VIDEO_ID

# Step 3: 告诉用户笔记已生成，可在 Obsidian 查看
```

### 2. PDF 书籍处理

当用户提供 PDF 文件路径或 Zotero 目录时：

```bash
# Step 1: 处理 PDF（提取文本和元数据）
python3 -m src.fetcher.cli "/path/to/file.pdf"
# 或提供包含 PDF 的目录（如 Zotero storage）
python3 -m src.fetcher.cli "/Users/liweixin/Zotero/storage/VDEZ72XG"

# Step 2: 生成检视阅读报告
python3 -m src.processor.cli pdf_XXXXXX

# Step 3: 告诉用户笔记已生成
```

### 3. 播放已下载内容

```bash
# 列出所有已下载内容
python3 -m src.player.cli -l

# 播放指定内容 (交互式，需要用户操作)
python3 -m src.player.cli SOURCE_ID
```

### 4. 查看生成的笔记

笔记保存在: `~/smart notes/DeepReading/Sources/`

## 完整工作流示例

**用户:** "帮我深度阅读这个视频 https://www.youtube.com/watch?v=RSNuB9pj9P8"

**AI 操作:**
```bash
cd /Users/liweixin/.claude/skills/deep-reading

# 1. 下载视频内容
python3 -m src.fetcher.cli "https://www.youtube.com/watch?v=RSNuB9pj9P8"

# 2. 生成检视阅读报告到 Obsidian
python3 -m src.processor.cli youtube_RSNuB9pj9P8
```

**AI 回复:**
"已完成！
- 📥 下载了视频: [标题]
- 📝 生成了检视阅读报告: ~/smart notes/DeepReading/Sources/[标题].md
- 🎧 如需播放音频，请告诉我

笔记包含：
- 视频元信息
- 快速摘要（待 AI 分析后填充）
- 核心观点
- 关键概念
- 思考问题

是否需要我帮你播放这个视频？"

**用户:** "阅读这本书 /Users/liweixin/Zotero/storage/VDEZ72XG"

**AI 操作:**
```bash
# 1. 处理 PDF
python3 -m src.fetcher.cli "/Users/liweixin/Zotero/storage/VDEZ72XG"

# 2. 生成报告
python3 -m src.processor.cli pdf_XXXXXX
```

**AI 回复:**
"已完成！
- 📖 处理了书籍: [标题]
- 📝 生成了检视阅读报告: ~/smart notes/DeepReading/Sources/[标题].md
- 📄 共 XX 页

笔记包含：
- 书籍元信息（标题、作者、页数）
- 快速摘要（待 AI 分析后填充）
- 核心观点
- 关键概念
- 思考问题"

## 缓存和数据位置

```
~/.deep-reading/
├── cache/
│   ├── youtube/{video_id}/
│   │   ├── audio.mp3        # 音频文件
│   │   ├── transcript.vtt   # 带时间戳的字幕
│   │   ├── transcript.txt   # 纯文本字幕
│   │   └── metadata.json    # 视频元数据
│   └── pdf/{pdf_id}/
│       ├── source.pdf       # PDF 副本
│       ├── content.txt      # 提取的文本
│       └── metadata.json    # PDF 元数据
├── db/deep_reading.db       # SQLite 数据库
└── config.py                # 配置文件

~/smart notes/DeepReading/
└── Sources/                 # Obsidian 笔记
    └── {标题}.md
```

## 播放控制键 (告知用户)

| 按键 | 功能 |
|------|------|
| `空格` | 暂停/播放 |
| `j` | 快进 30 秒 |
| `k` | 后退 10 秒 |
| `J` | 快进 60 秒 |
| `K` | 后退 30 秒 |
| `+` / `=` | 加速 |
| `-` | 减速 |
| `q` | 退出 |

## 错误处理

1. **无字幕**: 某些视频可能没有字幕，会报错
2. **网络问题**: 下载失败时提示用户检查网络
3. **已存在**: 如果内容已下载，会使用缓存
4. **PDF 解析**: 需要安装 PyMuPDF (`pip install PyMuPDF`)

## 后续功能 (M2-M6)

- M2: TUI 播放器 + 字幕同步
- M3: AI 自动章节分割 + 概念卡片
- M4: Obsidian 双链自动生成
- M5: 播客支持
- M6: 网页支持

## 笔记编写规范

### Obsidian 双向链接 [[]] 规则

**重要：只在目标文件已存在时才使用 `[[]]` 链接！**

- ❌ **禁止**：添加指向不存在文件的空链接，如 `[[效价]]`、`[[强化学习]]`
- ✅ **正确**：先创建笔记文件，再在其他笔记中添加 `[[文件名]]` 链接
- ✅ **正确**：对于尚未创建的概念，使用纯文本描述，如 "效价（Valence）"

### 检查链接是否有效

添加 `[[]]` 链接前，确认文件存在：
```bash
ls "~/smart notes/DeepReading/Sources/目标文件名.md"
```

### 示例

```markdown
# 正确做法
- 父笔记：A Brief History of Intelligence.md
- 相关概念：效价(Valence)、两侧对称动物

# 错误做法（目标文件不存在）
- 父笔记：[[A Brief History of Intelligence]]
- 相关概念：[[效价]]、[[两侧对称动物]]
```

