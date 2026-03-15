---
name: markdown-html-ppt
description: 将 Markdown 文档或文本转换为演示文稿。首先通过 reveal.js 转换为交互式 HTML PPT，然后可选择性地转换为 PowerPoint 文件。支持丰富的 Markdown 语法（加粗、斜体、代码、引用、代码块），5个精美主题，智能分页算法。输出格式可选：HTML（reveal.js）或 PowerPoint（.pptx）。版本：v2.4.0
author: skygreen2001
license: MIT
---

# Markdown Html Presentation 转换技能

## 功能概述

本技能用于将 Markdown 格式的文档或文本转换为演示文稿，支持两种输出格式：

1. **HTML 演示文稿**（基于 reveal.js）- 交互式、可在浏览器中演示
2. **PowerPoint 文件**（.pptx）- 可编辑、适合传统演示场景

**转换流程：**
```
Markdown → 解析（增强语法）→ reveal.js HTML → (可选) PowerPoint
```

**核心能力：**
- ✅ 自动解析 Markdown 结构（标题、列表、段落）
- ✅ 丰富的语法支持（**加粗**、*斜体*、`代码`、> 引用、```代码块```）
- ✅ 智能分页：根据内容实际高度自动分页
- ✅ 5 个精美主题：Philosophy, Business, Minimal, Traditional, Dark
- ✅ 双格式输出：HTML（reveal.js）+ PowerPoint（可选）
- ✅ 专业设计：行间距 1.5，清晰排版
- ✅ 灵活输入：支持文件路径或直接文本输入
- ✅ CDN 优化：使用国内可访问的 CDN 源

**触发条件：**
- 用户提供 Markdown 文件路径并要求转换为演示文稿
- 用户直接输入 Markdown 文本并要求生成演示文稿
- 用户要求将笔记、文档转换为幻灯片格式
- 用户明确要求 HTML 或 PPT 格式

## 支持的 Markdown 语法

### 基础语法

| 语法 | 说明 | 转换结果 |
|------|------|---------|
| `# 标题` | 一级标题 | 标题幻灯片 |
| `## 标题` | 二级标题 | 内容幻灯片标题 |
| `### 标题` | 三级标题 | 内容幻灯片标题 |
| `- 列表项` | 无序列表 | 幻灯片要点（带缩进） |
| `1. 列表项` | 有序列表 | 幻灯片要点（带缩进） |
| 段落文本 | 普通段落 | 幻灯片内容 |

### 行内格式

| 语法 | 说明 | 效果 |
|------|------|------|
| `**文本**` | 加粗 | **加粗文本** |
| `*文本*` | 斜体 | *斜体文本* |
| `` `代码` `` | 行内代码 | `代码文本` |

### 块级元素

| 语法 | 说明 | 效果 |
|------|------|------|
| `> 引用` | 块引用 | 引用块样式 |
| ` ```代码块``` ` | 代码块 | 代码块样式 |

### 使用示例

```markdown
## 示例标题

这是一个包含**加粗**、*斜体*和`代码`的段落。

> 这是一段引用文本。
> 可以包含**格式化**内容。

\`\`\`python
def hello():
    print("Hello, World!")
\`\`\`

- 列表项 1：包含**加粗**文本
- 列表项 2：包含*斜体*文本
- 列表项 3：包含`代码`文本
```

## 可用主题

### 主题列表

| 主题 | 配色 | 适用场景 |
|------|------|---------|
| **Philosophy** | 深黑 + 金色 | 哲学、文化 |
| **Business** | 白色 + 蓝色 | 商务、项目 |
| **Minimal** | 白色 + 黑色 | 学术、技术 |
| **Traditional** | 米白 + 红/黑 | 国学、诗词 |
| **Dark** | 深灰 + 青色 | 技术、夜间 |

### 查看所有主题

```bash
python scripts/md2presentation.py --list-themes
```

## 使用流程

### Step 1: 获取 Markdown 内容

**方式 A - 从文件读取：**
```python
markdown_path = "/path/to/document.md"
with open(markdown_path, 'r', encoding='utf-8') as f:
    markdown_content = f.read()
```

**方式 B - 直接输入：**
```python
markdown_content = """
# 标题
## 子标题
- 要点1
- 要点2
"""
```

### Step 2: 转换为演示文稿

**命令行方式：**
```bash
# 生成 HTML（使用哲学主题）
python scripts/md2presentation.py -i input.md -o output.html -f html --theme philosophy

# 生成 PowerPoint（使用商务主题）
python scripts/md2presentation.py -i input.md -o output.pptx -f ppt --theme business

# 同时生成两种格式
python scripts/md2presentation.py -i input.md -o output -f both --theme minimal

# 列出所有主题
python scripts/md2presentation.py --list-themes
```

**Python API 方式：**
```python
from scripts.md2presentation import convert_markdown_to_presentation

# 生成 HTML
html_path = convert_markdown_to_presentation(
    markdown_content=markdown_content,
    output_path="/Users/username/Documents/presentation.html",
    output_format="html",
    theme="philosophy"
)

# 生成 PowerPoint
ppt_path = convert_markdown_to_presentation(
    markdown_content=markdown_content,
    output_path="/Users/username/Documents/presentation.pptx",
    output_format="ppt",
    theme="business"
)

# 同时生成两种格式
html_path, ppt_path = convert_markdown_to_presentation(
    markdown_content=markdown_content,
    output_path="/Users/username/Documents/presentation",
    output_format="both",
    theme="minimal"
)
```

### Step 3: 返回结果

向用户提供：
1. 生成的文件路径（HTML 和/或 PPT）
2. 幻灯片总数
3. 文件位置的可点击链接（使用 desktop-local-file 格式）

**输出示例（HTML）：**
```markdown
HTML 演示文稿创建成功！

\`\`\`desktop-local-file
{
"localPath": "/Users/username/Documents/presentation.html",
"fileName": "presentation.html"
}
\`\`\`

共生成 25 张幻灯片。可在浏览器中打开，使用方向键或空格键翻页。
```

## 智能分页算法

### 动态容量调整

根据文本实际长度动态调整每页容量：

| 文本长度 | 每页最多要点数 | 适用场景 |
|---------|--------------|---------|
| < 50 字符 | 8 个 | 简短要点 |
| 50-100 字符 | 6 个 | 中等长度 |
| > 100 字符 | 4 个 | 详细说明 |

### 高度计算

考虑格式化文本的额外高度：
- 基础高度：文本长度 × 字符高度
- 加粗/斜体：额外 10% 高度
- 代码：额外 20% 高度
- 引用：额外 15% 高度

### 防溢出机制

- 实时计算内容总高度
- 与页面可用高度对比
- 超出时自动分页
- 确保内容不溢出

## 设计规范

### HTML 演示文稿（reveal.js）

**颜色方案：**
- 使用主题的配色方案
- 深色背景，白色文字（或主题指定）
- 清晰的对比度

**布局：**
- 16:9 宽屏比例（1280 x 720）
- 标题幻灯片：居中对齐
- 内容幻灯片：左对齐
- **列表缩进**：`padding-left: 20px`

**行间距：**
- `line-height: 1.5`
- 提高可读性

**CDN 配置：**
- 使用国内可访问的 BootCDN
- 自动加载 reveal.js 库和主题

### PowerPoint 文件

**颜色方案：**
- 根据主题配置
- 默认：深灰色背景 + 白色文字

**字体设置：**
- 标题字体：28-44pt，加粗
- 正文字体：14-16pt，常规
- 行间距：1.5 倍

**布局规范：**
- 幻灯片尺寸：16:9（10 x 5.625 英寸）
- 标题幻灯片：标题居中，副标题可选
- 内容幻灯片：标题在顶部，内容区域占主体
- 边距：左右各 0.5 英寸，上下适当留白

## 资源文件

- **转换脚本**：[scripts/md2presentation.py](scripts/md2presentation.py) - 核心转换逻辑
- **主题配置**：[scripts/themes.py](scripts/themes.py) - 主题配置模块
- **参考文档**：[references/markdown-syntax.md](references/markdown-syntax.md) - 支持的 Markdown 语法
- **示例文件**：[references/example.md](references/example.md) - Markdown 示例
- **格式对比**：[references/format-comparison.md](references/format-comparison.md) - 格式对比说明

## 依赖要求

确保已安装以下 Python 库：

```bash
pip install python-pptx
```

**版本要求：**
- Python 3.7+
- python-pptx >= 0.6.21

## 注意事项

1. **文件编码**：确保 Markdown 文件使用 UTF-8 编码
2. **路径处理**：支持绝对路径和相对路径，建议使用绝对路径
3. **内容长度**：过长的列表会自动分页，避免单张幻灯片内容过多
4. **特殊字符**：自动处理 HTML 特殊字符转义
5. **输出位置**：默认保存到用户工作目录，可自定义输出路径
6. **CDN 访问**：HTML 版本使用国内 CDN，确保网络可访问
7. **格式选择**：根据使用场景选择合适的输出格式

## 更新日志

### v2.4.0 (2026-02-08) - 当前版本

- 修复：HTML 列表添加缩进（padding-left: 20px）
- 修复：增强内容高度计算，更精确防止溢出
- 修复：完善 Markdown 语法解析，正确处理所有格式
- 改进：优化分页算法，考虑实际渲染高度
- 改进：更新 SKILL.md 版本日志

### v2.3.1 (2026-02-08)

- 修复：HTML 标签正确闭合（`<ul>` 和 `</ul>` 配对）
- 修复：列表嵌套错误
- 改进：HTML 结构更清晰

### v2.3.0 (2026-02-08)

- 新增：行内格式支持（加粗、斜体、代码）
- 新增：块引用和代码块支持
- 新增：HTML 特殊字符自动转义
- 改进：行间距优化为 1.5 倍
- 改进：智能分页算法

### v2.2.0 (2026-02-08)

- 新增：完整集成主题系统，5 个精美主题
- 新增：`--theme` 命令行参数
- 新增：`--list-themes` 列出所有主题

### v2.1.0 (2026-02-08)

- 新增：自动分页功能
- 改进：提高演示文稿可读性

### v2.0.0 (2026-02-07)

- 新增：支持 HTML (reveal.js) 和 PowerPoint 双格式输出
- 新增：reveal.js 集成

### v1.0.0 (2026-02-07)

- 初始版本发布
- 支持基础 Markdown 语法

## 最佳实践

1. **结构清晰**：使用明确的标题层级，便于自动分页
2. **内容精简**：每张幻灯片控制在 5-8 个要点以内
3. **标题简洁**：使用简短有力的标题，避免过长
4. **列表优先**：优先使用列表格式，便于阅读
5. **逻辑连贯**：确保内容逻辑清晰，便于演示
6. **格式选择**：
   - 需要在线演示或快速预览 → 选择 HTML
   - 需要编辑或传统演示 → 选择 PowerPoint
   - 两者都需要 → 选择同时生成
7. **充分利用格式**：使用**加粗**突出重点，使用*斜体*表示强调，使用`代码`标记技术术语
