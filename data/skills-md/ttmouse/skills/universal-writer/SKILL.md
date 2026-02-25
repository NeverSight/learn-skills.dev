---
name: universal-writer
description: |
  通用写作技能：从数据到文章的自动化写作工作流。
  支持多种写作模板（专题、教程、分析、总结、文档），可根据数据源或交互式生成文章。
  当用户说"写作"、"生成文章"、"写文档"、"universal-writer"时触发。
type: workflow
triggers:
  - 写作
  - 生成文章
  - 写文档
  - universal-writer
  - create article
  - write documentation
---

# Universal Writer - 通用写作技能

> 从数据到文章的自动化写作工作流

## 技能位置

```
~/.claude/skills/universal-writer/
```

## 核心功能

### 1. 多模板支持

| 模板 | 适用场景 |
|------|---------|
| 专题深度拆解 | designprompt 专题文章 |
| 技术教程 | 技能使用、工具教程 |
| 案例分析 | Twitter 案例研究 |
| 经验总结 | 工作复盘、方法论 |
| 产品文档 | 技能文档、使用指南 |

### 2. 三种使用方式

#### 方式 1: 直接生成

```bash
cd ~/.claude/skills/universal-writer
./venv/bin/python3 scripts/writer.py \
  --template "专题深度拆解" \
  --topic "液体飞溅摄影" \
  --output "article.md"
```

#### 方式 2: 数据驱动

```bash
./venv/bin/python3 scripts/writer.py \
  --template "专题深度拆解" \
  --data "cases.json" \
  --auto-generate \
  --output "article.md"
```

#### 方式 3: 交互式

```bash
./venv/bin/python3 scripts/writer.py --interactive
```

## 依赖安装

```bash
cd ~/.claude/skills/universal-writer
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

## 完整工作流

```
数据采集 → 内容生成 → 图片处理 → 发布
    ↓           ↓           ↓         ↓
twitter-   universal-  twitter-   qiaomu-x-
collector    writer     image-    article-
                       downloader publisher
```

---

**创建时间**：2026-02-01
**版本**：v1.0
**状态**：MVP 实现
