---
name: twitter-image-downloader
description: |
  从 Markdown 文件中自动提取并下载 Twitter 图片，生成可直接发布的版本。
  当用户说"下载推文图片"、"提取Twitter图片"、"download twitter images"时触发。
type: workflow
triggers:
  - 下载推文图片
  - 提取Twitter图片
  - 下载 pbs.twimg.com 图片
  - download twitter images
  - extract twitter images
---

# Twitter 图片下载技能

> 从 Markdown 文件中自动提取并下载 Twitter 图片

## 用途

当你的 Markdown 文章中包含 Twitter 图片链接（`https://pbs.twimg.com/media/...`），需要将这些图片下载到本地并替换路径时使用。

## 核心价值

- **效率提升**：从 5-10 分钟缩短到 15-20 秒
- **自动化**：一行命令完成所有操作
- **可靠性**：使用系统自带 curl 工具，100% 可用

## 使用方式

### 基本用法

```bash
~/.claude/skills/twitter-image-downloader/scripts/download.sh "文章.md"
```

### 指定输出目录

```bash
~/.claude/skills/twitter-image-downloader/scripts/download.sh "文章.md" "custom_images"
```

## 工作流程

1. **自动提取图片 URL**：从 Markdown 中提取所有 `pbs.twimg.com` 图片链接
2. **创建图片目录**：自动创建 `[文件名]_images/` 目录
3. **批量下载图片**：使用 curl 批量下载，文件命名为 `01.jpg`, `02.jpg`...
4. **生成发布版文件**：自动替换 Markdown 中的图片路径
5. **输出报告**：显示成功/失败统计和图片清单

## 技术细节

- User-Agent 模拟浏览器，避免被拦截
- 30秒连接超时 + 120秒下载超时
- 自动检查文件有效性
- 跨平台兼容（macOS/Linux）

---

**创建时间**：2026-02-01
**版本**：v1.0
**状态**：已实现
