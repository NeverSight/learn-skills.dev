---
name: pdf-translate
description: Translates PDF documents to Chinese with professional typography. Extracts text, translates section-by-section into well-structured Markdown, then generates PDF via weasyprint with full CJK support. Use when user asks to translate a PDF, says "翻译PDF", "translate this document", or "pdf translate".
---

# PDF Translation Skill

翻译 PDF 文档并生成排版精美的中文文档。输出 Markdown + PDF 双格式。

## 版本信息

**当前版本**: v4.0.0
**发布日期**: 2026-02-21

### v4.0.0 变更

- 采用 Markdown-first 工作流：先生成结构化 Markdown，再转 PDF
- PDF 引擎从 reportlab 切换为 weasyprint（支持完整 HTML/CSS 排版）
- 修复代码块中文乱码问题（添加 CJK 字体 fallback）
- 完整支持：标题层级、代码块、表格、列表、引用、粗体斜体
- 新增 `scripts/md2pdf.py` 通用转换脚本

## 核心工作流

### Step 1: 提取 PDF 文本

```python
import pdfplumber

pdf = pdfplumber.open("输入文件.pdf")
for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    if text:
        print(f"--- Page {i+1} ---")
        print(text)
```

长文档（>20 页）先提取前几页了解结构，再分批提取。

### Step 2: 分析文档结构

通读全文，识别以下元素并规划 Markdown 映射：

| 原文元素 | Markdown 映射 |
|---------|-------------|
| 文档标题 | `#` |
| 章节（Chapter） | `##` |
| 小节（Section） | `###` |
| 子小节（Subsection） | `####` |
| 目录 | 链接列表 `- [章节名](#锚点)` |
| 正文段落 | 段落（空行分隔） |
| 代码块 | ` ``` ` 围栏（**不翻译**内容） |
| 表格 | `\| 列1 \| 列2 \|` 语法 |
| 有序列表 | `1. ` 开头 |
| 无序列表 | `- ` 开头 |
| 引用/提示框 | `> ` 语法 |
| 页脚/页码 | 丢弃 |

### Step 3: 逐章节翻译为中文 Markdown

**必须逐章节翻译**，不要一次输出全文。每完成一个章节就追加写入文件。

#### 翻译规则

1. **专有名词保留英文**：首次出现时括号附英文，如"渐进式披露（Progressive Disclosure）"
2. **代码块不翻译**：` ``` ` 内代码保持原文，只翻译围栏外说明文字
3. **行内代码不翻译**：反引号内标识符、命令、文件名保持英文
4. **保持层级结构**：`#` → `##` → `###` → `####` 不跳级
5. **段落间必须空行**：每个段落、列表、代码块、表格前后都要有空行
6. **列表格式**：`- ` 或 `1. ` 开头，嵌套用 2 空格缩进
7. **表格格式**：`| 列1 | 列2 |` 语法，必须有 `|---|---|` 分隔行
8. **引用格式**：`> ` 开头

#### 翻译质量标准

参见 [translation-standards.md](references/translation-standards.md)

- 三步翻译工作流：重写初稿 → 问题诊断 → 润色定稿
- 四大语言转换策略：形合→意合、被动→主动、抽象→具体、精简冗余
- 杜绝"欧化表达"和"翻译腔"

#### 必须避免的格式错误

- ❌ 段落之间没有空行 → 文字挤在一起
- ❌ 列表项前没有空行 → 不被识别为列表
- ❌ 表格前后没有空行 → 表格无法渲染
- ❌ 代码块 ` ``` ` 前后没有空行 → 代码块不显示
- ❌ 标题 `##` 前后没有空行 → 标题不识别
- ❌ 翻译代码块内的代码
- ❌ 一次性输出全部内容导致截断

### Step 4: 输出 Markdown 文件

写入 `.md` 文件，路径与原 PDF 同目录，文件名：`原文件名_中文翻译.md`

### Step 5: 生成 PDF

使用 `scripts/md2pdf.py` 将 Markdown 转为排版精美的 PDF：

```bash
python3 ${SKILL_DIR}/scripts/md2pdf.py "输入.md" "输出.pdf"
```

macOS 上如果报 gobject 找不到：

```bash
DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib" python3 ${SKILL_DIR}/scripts/md2pdf.py "输入.md" "输出.pdf"
```

也可以使用项目目录下的副本：

```bash
python3 scripts/md2pdf.py "输入.md" "输出.pdf"
```

PDF 排版特性：
- A4 版面，自动分页，页码
- 中文字体（苹方/黑体/雅黑）+ 英文字体 fallback
- 深色背景代码块（支持中文注释）
- 专业表格样式（交替行色、边框）
- 蓝色左边框引用块
- 标题层级样式（蓝色边线、字号递减）

### Step 6: 确认输出

翻译完成后告知用户：
1. `.md` 文件路径
2. `.pdf` 文件路径
3. 文档概况（页数、字数）

## 依赖安装

```bash
# macOS
brew install pango
pip3 install pdfplumber markdown weasyprint

# 旧方案依赖（仍可用）
pip3 install reportlab pypdf
```

## 脚本目录

| 脚本 | 用途 |
|------|------|
| `scripts/md2pdf.py` | **推荐** Markdown → PDF（weasyprint 引擎） |
| `scripts/translate_pdf.py` | 旧版：基础 PDF 提取和生成（reportlab） |
| `scripts/generate_complete_pdf.py` | 旧版：完整工作流（reportlab） |

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| 代码块中文乱码 | 使用 `md2pdf.py`（v4.0，已修复 CJK font fallback） |
| weasyprint 报 gobject 找不到 | `DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib"` |
| 中文字体不显示 | 确认系统有苹方或黑体字体 |
| Markdown 格式错乱 | 检查块级元素前后是否有空行 |

更多问题参见 [troubleshooting.md](references/troubleshooting.md)

---

**参考文档**：
- [翻译标准](references/translation-standards.md)
- [字体配置](references/font-configuration.md)
- [故障排除](references/troubleshooting.md)
- [完整示例](references/complete-example.md)
