---
name: oh-story-claudecode-writing
description: 网文写作 skill 包，覆盖长篇与短篇网络小说的扫榜、拆文、写作、去AI味全流程
triggers:
  - help me write a Chinese web novel
  - 帮我开书
  - 这篇太AI了去AI味
  - analyze this novel chapter structure
  - scan trending web novel topics
  - 网文写作
  - write a short story with plot twist
  - set up novel writing workflow
---

# oh-story-claudecode Writing Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A comprehensive Chinese web novel (网文) writing skill pack for AI coding agents, covering the full pipeline: market scanning (扫榜), novel analysis (拆文), writing (写作), and AI-style removal (去AI味) for both long-form and short-form fiction.

## What This Project Does

`oh-story-claudecode` provides structured Claude Code / OpenClaw skills that guide AI agents through every stage of professional web novel production:

1. **扫榜 (Market Scan)** — Analyze trending titles on 起点, 番茄, 晋江, 知乎盐言
2. **拆文 (Novel Analysis)** — Deconstruct golden chapters, pacing, hooks, emotional arcs
3. **写作 (Writing)** — Generate outlines, character sheets, chapter drafts with platform-specific style
4. **去AI味 (De-slop)** — Detect and remove AI writing artifacts, banned word lists, rewrite examples

## Installation

### Via Claude Code / OpenClaw

Feed the repo URL to Claude Code or OpenClaw and say "安装这个 skill":

```
https://github.com/worldwonderer/oh-story-claudecode
```

### Via CLI

```bash
npx skills add worldwonderer/oh-story-claudecode -y
```

To update, re-run the same command.

## Available Skills & Triggers

| Skill | Slash Command | Natural Language Triggers |
|:------|:-------------|:--------------------------|
| `story-long-write` | `/story-long-write`, `/story`, `/网文` | "帮我开书", "写长篇", "搭大纲" |
| `story-long-analyze` | `/story-long-analyze` | "拆这本书", "分析黄金三章" |
| `story-long-scan` | `/story-long-scan` | "扫长篇榜单", "起点趋势" |
| `story-short-write` | `/story-short-write` | "写短篇", "写一个反转故事" |
| `story-short-analyze` | `/story-short-analyze` | "拆短篇结构", "分析情绪曲线" |
| `story-short-scan` | `/story-short-scan` | "知乎盐言风口", "短篇扫榜" |
| `story-deslop` | `/story-deslop`, `/去AI味` | "这篇太AI了", "去掉AI感" |
| `browser-cdp` | `/browser-cdp` | "抓取榜单数据", "登录后爬取" |

## Project File Structure

Writing content is managed on the filesystem, not accumulated in conversation context.

### Long-form Novel (长篇)

```
{书名}/
├── 设定/
│   ├── 世界观/          # 背景设定、力量体系（按主题拆文件）
│   ├── 角色/            # 每个人物一个文件（沈栀.md、陆衍止.md）
│   └── 势力/            # 每个势力/组织一个文件（天机阁.md）
├── 大纲/
│   ├── 大纲.md          # 全书卷级结构
│   ├── 细纲_第001章.md  # 每章一个章纲，与正文一一对应
│   └── ...
├── 正文/
│   ├── 第001章_章名.md
│   └── ...
└── 笔记.md
```

### Short-form Story (短篇)

```
{标题}/
├── 设定.md
├── 正文.md
└── 笔记.md
```

## Key Workflows

### Workflow 1: Start a Long-form Novel from Scratch

```bash
# 1. Scan the market for trending topics
/story-long-scan

# 2. Analyze a top-performing novel
/story-long-analyze

# 3. Begin writing with outline scaffolding
/story-long-write
```

**Example agent interaction:**

```
User: 帮我开书，都市赘婿题材，起点男频

Agent triggers: story-long-write
→ Generates: 书名/设定/世界观/都市背景.md
→ Generates: 书名/设定/角色/主角.md
→ Generates: 书名/大纲/大纲.md  (五步大纲法, 卷级结构)
→ Generates: 书名/大纲/细纲_第001章.md
→ Generates: 书名/正文/第001章_重生归来.md
```

### Workflow 2: Analyze an Existing Novel

```bash
/story-long-analyze
# Paste chapter text or provide file path
# Agent returns: 黄金三章分析, 爽点密度, 钩子类型, 节奏评分
```

### Workflow 3: Write and Polish a Short Story

```bash
# Write
/story-short-write
# Input: genre, emotional arc template, word count target

# Remove AI artifacts
/story-deslop
# Input: draft text file path
# Output: rewritten version with AI-style markers removed
```

### Workflow 4: Scrape Market Data with Browser CDP

```bash
/browser-cdp
# Reuses existing browser login session via CDP protocol
# Scrapes 起点/番茄/晋江/知乎盐言 ranking pages without re-login
```

## Shell Script Examples

### Initialize a novel project directory

```bash
#!/bin/bash
# init_novel.sh - Bootstrap long-form novel file structure

BOOK_NAME="${1:-我的新书}"

mkdir -p "${BOOK_NAME}/设定/世界观"
mkdir -p "${BOOK_NAME}/设定/角色"
mkdir -p "${BOOK_NAME}/设定/势力"
mkdir -p "${BOOK_NAME}/大纲"
mkdir -p "${BOOK_NAME}/正文"

# Create starter files
cat > "${BOOK_NAME}/笔记.md" << 'EOF'
# 创作笔记

## 核心爽点
- 

## 读者画像
- 

## 竞品参考
- 

## 待办
- [ ] 完成世界观设定
- [ ] 完成主角角色卡
- [ ] 完成第一卷大纲
EOF

cat > "${BOOK_NAME}/大纲/大纲.md" << 'EOF'
# 全书大纲

## 核心矛盾

## 第一卷：（卷名）
- 起：
- 承：
- 转：
- 合：

## 第二卷：（卷名）

## 结局方向
EOF

echo "✅ 项目目录已创建: ${BOOK_NAME}/"
echo "📁 结构:"
find "${BOOK_NAME}" -type f | sort
```

### Batch process chapters for de-slop

```bash
#!/bin/bash
# deslop_batch.sh - Run de-slop on all chapter files

BOOK_DIR="${1:-.}"
OUTPUT_DIR="${BOOK_DIR}/精修"

mkdir -p "${OUTPUT_DIR}"

for chapter in "${BOOK_DIR}/正文"/*.md; do
  filename=$(basename "${chapter}")
  echo "🔍 处理: ${filename}"
  
  # Invoke story-deslop skill on each file
  # Agent reads chapter, applies three-pass de-slop method, writes output
  cp "${chapter}" "${OUTPUT_DIR}/${filename}"
  echo "  → 输出: ${OUTPUT_DIR}/${filename}"
done

echo "✅ 批量去AI味完成，共处理 $(ls ${BOOK_DIR}/正文/*.md | wc -l) 章"
```

### Check chapter word count targets

```bash
#!/bin/bash
# wordcount.sh - Report word counts for all chapters

BOOK_DIR="${1:-.}"
TARGET="${2:-3000}"  # Default target: 3000 chars per chapter

echo "📊 章节字数统计 (目标: ${TARGET} 字)"
echo "================================"

total=0
for chapter in "${BOOK_DIR}/正文"/*.md; do
  filename=$(basename "${chapter}")
  count=$(wc -m < "${chapter}")
  total=$((total + count))
  
  if [ "${count}" -lt "${TARGET}" ]; then
    echo "⚠️  ${filename}: ${count} 字 (不足目标)"
  else
    echo "✅ ${filename}: ${count} 字"
  fi
done

echo "================================"
echo "📖 总计: ${total} 字 | 平均: $((total / $(ls ${BOOK_DIR}/正文/*.md | wc -l))) 字/章"
```

## Knowledge Base (References)

Each skill auto-loads relevant knowledge from `references/` — only what's needed for the current task:

| Topic | Content | Skill |
|:------|:--------|:------|
| 大纲排布 | 五步大纲法, 故事结构分级, 节点设计法, 升级感设计 | `long-write` |
| 人物设计 | 角色设定, 人物提取, 关系映射, 动机链, 群像 | `long-write` |
| 钩子技法 | 章尾钩子13式, 章首钩子7式, 段落级钩子, 悬念编排 | `long-write` |
| 情绪设计 | 6种弧形模板, 期待感管理, 题材赛道策略 | `long-write` |
| 去AI味 | 预防, 三遍去AI法, 改写范例库, 禁用词表 | `deslop` |
| 写作公式 | 21大题材写作公式, 三翻四震, 感情线四阶段 | `short-write` |
| 女频写作 | 女读者偏好, 情感描写, 感情线模式, 对标拆书 | `short-write` |
| 市场数据 | 题材趋势, 平台特性, 投稿审核, 推荐安排 | `long-scan` / `short-scan` |
| 高级技法 | 小纲四步法, 高潮逆推, 双线结构, AB交织法 | `long-write` |
| 风格模块 | 对话, 打斗, 智斗, 镜头式写作, 装逼打脸, 白描 | `long-write` |

## Supported Platforms

| Type | Platforms |
|:-----|:----------|
| 长篇 | 起点中文网, 番茄小说, 晋江文学城, 七猫小说, 刺猬猫 |
| 短篇 | 知乎盐言故事, 番茄短篇, 七猫短篇 |

## Common Patterns

### Pattern 1: Market-to-Draft Pipeline

```
/story-long-scan     → identify trending genre + tropes
/story-long-analyze  → paste top 3 chapters of a competitor novel
/story-long-write    → generate outline aligned with market gaps
```

### Pattern 2: Revision Loop

```
Draft chapter → /story-deslop → human review → /story-deslop (second pass)
```

### Pattern 3: Skip Prep, Jump to Writing

If you already have a direction, skip scanning and analysis:

```
User: 我已经有设定了，帮我直接写第一章

Agent: triggers story-long-write with --skip-prep flag
→ Reads existing 设定/ files
→ Generates 大纲/细纲_第001章.md
→ Generates 正文/第001章_*.md
```

### Pattern 4: Short Story with Emotional Arc

```
/story-short-write
→ Select arc template (e.g., "跌入深谷后反弹" / "平稳中突转")
→ Agent scaffolds: 设定.md → 正文.md (with embedded hook + reversal)
→ /story-deslop on 正文.md
```

## Troubleshooting

### Skill not triggering
- Ensure install completed: `npx skills add worldwonderer/oh-story-claudecode -y`
- Try explicit slash command: `/story-long-write` instead of natural language
- Re-run install to pull latest version

### Browser CDP not connecting
- Ensure Chrome/Chromium is running with remote debugging enabled:
  ```bash
  google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
  ```
- Check CDP endpoint: `curl http://localhost:9222/json/version`
- The skill reuses your existing login session — log into the platform manually first

### Output files not being created
- Verify the agent has write permissions to the working directory
- Check that the book name doesn't contain special characters that break directory creation
- Use the init script to pre-create the directory structure

### AI artifacts still present after de-slop
- Run `/story-deslop` a second time (三遍去AI法 = three-pass method)
- Provide specific examples of AI-sounding phrases for the agent to target
- Check `references/禁用词表` is loaded — mention it explicitly if needed

### Chapter too short / pacing issues
- Use `/story-long-analyze` on your own draft to get density scores
- Request "扩写" (expand) with specific scene types: "扩写打斗场景至3000字"
- Reference the 节奏分析 knowledge module explicitly

## Full Pipeline Example

```bash
# Step 1: Initialize project
bash init_novel.sh "天机阁传说"
cd "天机阁传说"

# Step 2: Market research (agent scans 起点 male fantasy rankings)
# /story-long-scan → saves market notes to 笔记.md

# Step 3: Analyze a competitor (paste 3 chapters into agent)
# /story-long-analyze → appends findings to 笔记.md

# Step 4: Generate full outline + first chapter
# /story-long-write → creates 设定/, 大纲/, 正文/第001章.md

# Step 5: Continue chapter by chapter
# /story-long-write → reads existing files, generates next chapter

# Step 6: Polish
# /story-deslop → rewrites 正文/*.md removing AI artifacts

# Step 7: Word count check
bash wordcount.sh . 3000
```
