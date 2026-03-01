---
name: article-batch-illustration
description: 分析文章结构并批量生成AI配图，调用Gemini API为每个段落创建专业逻辑图/概念图。当用户说"批量配图"、"给文章配图"、"生成文章插图"、"为这篇文章配图"时触发。支持两种风格：简约手绘风和建筑蓝图编辑风。自动保存到Obsidian图片目录并插入文档。
---

# 文章批量配图

分析 Markdown 文章结构，为每个段落/小节生成配图提示词，调用 Gemini API 批量生成图片并插入文档。

## 工作流程

### Phase 1: 分析文章 → 生成提示词

1. **读取文章** - 获取用户提供的文章内容（当前打开文件或指定路径）
2. **结构分析** - 按 H2/H3 标题拆分段落，提取每个段落核心思想
3. **生成风格指令** - 根据文章主题生成全局 STYLE INSTRUCTIONS 代码块
4. **生成提示词** - 为每个段落创建图片提示词大纲（参考 references/style-guide.md）
5. **展示并确认** - 以列表形式展示所有提示词，等待用户确认或修改

### Phase 2: 生成图片 → 插入文档

6. **批量生成** - 调用 `scripts/generate_image.py` 逐个生成图片
7. **保存图片** - 存入 `obsidian/09image/MMDD-主题名称/` 目录
8. **插入文档** - 在每个段落标题后插入 `![[图片路径]]` 引用

## Phase 1 详细指引

### 1. 文章结构分析

读取文章后，按以下规则拆分：

- 以 `## ` (H2) 或 `### ` (H3) 标题作为段落分隔符
- 忽略 frontmatter（YAML）部分
- 忽略纯引用、脚注等辅助内容
- 提取每个段落的：标题、核心观点（1句话）、关键概念（3-5个词）

输出格式：
```
## 文章结构分析

| # | 段落标题 | 核心观点 | 关键概念 |
|---|---------|---------|---------|
| 1 | xxx     | xxx     | A, B, C |
| 2 | xxx     | xxx     | D, E, F |
```

### 2. 生成全局风格指令

在所有提示词之前，必须先生成 STYLE INSTRUCTIONS 块。读取 references/style-guide.md 获取风格模板。

默认使用**风格 1（简约手绘风）**，用户可选择风格 2（建筑蓝图编辑风）。

```
STYLE INSTRUCTIONS:
- 整体风格: 简约手绘风格 / 建筑蓝图编辑风格
- 色彩方案: 白底为主，黑色线条，[主题点缀色]
- 比例: 16:9 横版
- 分辨率: 2K
- 文字量: 极少，仅保留1-3个核心关键词
- 文字语言: 图片中文字以简体中文为主，专业术语/缩写（如 AI、API、LLM）可保留英文
- 视觉语言: 逻辑图、流程图、概念图
- 一致性: 统一线条粗细、留白比例、排版网格
```

### 3. 为每个段落生成提示词

每个提示词结构：
1. **风格前缀** - 来自 STYLE INSTRUCTIONS 的通用描述
2. **图表类型** - 概念图/流程图/对比图/层次图/关系图
3. **内容描述** - 以段落核心思想为主，用叙述性语言描述图表内容
4. **中文标签** - 直接写中文关键词（如 "数据采集"、"智能处理"），1-3个
5. **中文为主指令**（必须） - 每个提示词末尾追加：`ALL text, labels, and annotations in the image MUST be primarily in Chinese (Simplified Chinese, 中文). Use clean Chinese font for main text. Technical terms and abbreviations (e.g. AI, API, LLM, RAG) may remain in English.`
6. **排除项** - "No photography, no realistic elements, no complex gradients"

展示格式（等待用户确认）：
```
## 提示词大纲

### 图 1: [段落标题]
- 图表类型: 概念图
- 提示词:
  """
  [完整英文提示词]
  """

### 图 2: [段落标题]
...
```

**关键**:
- 提示词主体用英文编写（Gemini 对英文提示词理解更好）
- 图片中需要出现的文字标签直接写中文原文（如 `The central node labeled "AI生产力系统"`）
- **每个提示词末尾必须包含中文为主指令**，确保图片中文字以中文为主，专业术语可保留英文

### 4. 等待确认

展示完所有提示词后，询问用户：
- "以上提示词是否满意？是否需要修改某个图的描述？"
- "确认后将开始批量生成图片（共 N 张）"
- 用户可指定某个图使用不同风格或修改描述

## Phase 2 详细指引

### 5. 调用 API 生成图片

确认后逐个调用脚本生成图片：

```bash
python3 scripts/generate_image.py \
  --prompt "提示词内容" \
  --output "/Users/ugreen/Documents/obsidian/09image/MMDD-主题名/01-段落名.png" \
  --api-key "AIzaSyDvvGGRbH4Os3Er0dYi0kE_AzE3_2b_Az8" \
  --api-url "https://generativelanguage.googleapis.com" \
  --model "gemini-3-pro-image-preview" \
  --aspect-ratio "16:9" \
  --resolution "2K"
```

**注意事项**:
- MMDD 取当天日期（如 0206）
- 主题名从文章 H1 标题提取，简化为短名称
- 图片编号两位数字（01, 02, 03...）
- 每张图生成后检查脚本输出确认成功
- 若某张图失败，记录并继续下一张，最后汇报失败项
- 图片间间隔 2-3 秒，避免 API 限流

### 6. 保存路径规范

```
/Users/ugreen/Documents/obsidian/09image/MMDD-主题简称/
├── 01-段落标题简称.png
├── 02-段落标题简称.png
├── 03-段落标题简称.png
└── ...
```

### 7. 插入文档

在文章对应段落标题下方插入图片引用：

```markdown
## 段落标题

![[09image/MMDD-主题简称/01-段落标题简称.png]]

段落正文内容...
```

使用 Obsidian wikilink 格式 `![[路径]]` 插入。

## API 配置

| 配置项 | 值 |
|-------|---|
| API URL | `https://generativelanguage.googleapis.com` |
| API Key | `AIzaSyDvvGGRbH4Os3Er0dYi0kE_AzE3_2b_Az8` |
| Model | `gemini-3-pro-image-preview` |
| 默认比例 | 16:9 |
| 默认分辨率 | 2K |

## 风格选择

| 风格 | 特征 | 适用场景 |
|------|-----|---------|
| 风格 1（默认）| 简约手绘，黑色线条，白底 | 通用、概念解释、流程说明 |
| 风格 2 | 建筑蓝图/技术期刊，精致极简 | 系统架构、技术分析、专业内容 |

用户可在确认阶段选择全局风格，也可为单个图指定不同风格。

## 常见用法

| 用户说 | 操作 |
|-------|-----|
| "给这篇文章配图" | 分析当前打开的文章并批量配图 |
| "批量配图" | 同上 |
| "用风格2给文章配图" | 使用建筑蓝图编辑风格 |
| "修改第3张图的提示词" | 重新生成指定图片 |
| "重新生成第2张" | 用修改后的提示词重新调用 API |
