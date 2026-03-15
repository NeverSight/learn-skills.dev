---
name: lyxy-document-reader
description: 统一文档解析工具 - 将 DOCX、XLSX、PPTX、PDF、HTML/URL 转换为 Markdown。支持全文输出、字数统计、行数统计、标题提取、章节提取、正则搜索。当用户要求"读取/解析/打开文档"、上传 .docx/.xlsx/.pptx/.pdf/.html 文件、或提供 URL 时使用。
license: MIT
metadata:
  version: "20260311_142456"
  author: "lanyuanxiaoyao <lanyuanxiaoyao@gmail.com>"
compatibility: Requires Python 3.11+。优先使用 lyxy-runner-python skill，次选 uv run --with，降级到主机 Python。
---

# 统一文档解析 Skill

## 🔴 重要：执行路径优先级（必须遵守）

### 执行路径选择（按优先级顺序）
1. **lyxy-runner-python skill（首选）** - 自动管理依赖
2. **uv run --with** - 按需加载依赖
3. **主机 Python + pip install** - 手动安装依赖

### 第一步：获取执行建议
```bash
PYTHONPATH=. uv run --with pyarmor python scripts/lyxy_document_reader.py --advice <文件路径或URL>
```
这会输出准确的执行命令，包含所需的依赖配置。

*也可以使用：`python scripts/lyxy_document_reader.py --advice <文件路径或URL>`*

## Purpose

**支持格式**
- DOCX（Word 文档）
- XLSX（Excel 表格）
- PPTX（PowerPoint 演示文稿）
- PDF（PDF 文档，支持 OCR）
- HTML / URL（网页内容）

## When to Use

### 触发场景
- 文档转换：将各类文档转为 Markdown
- 文档元数据：字数、行数统计
- 标题分析：提取标题结构
- 章节提取：提取特定章节
- 内容搜索：关键词或正则搜索

### 触发词
- 中文："读取/解析/打开 文档/Word/Excel/PPT/PDF/网页"
- 英文："read/parse/extract document/docx/xlsx/pptx/pdf/html"
- 文件扩展名：`.docx`、`.xlsx`、`.pptx`、`.pdf`、`.html`、`.htm`
- URL：`http://`、`https://`

## Quick Reference

| 参数 | 说明 |
|------|------|
| `-a/--advice` | 仅显示执行建议（**必须先运行此命令**） |
| (无) | 输出完整 Markdown |
| `-c/--count` | 字数统计 |
| `-l/--lines` | 行数统计 |
| `-t/--titles` | 提取所有标题（1-6级） |
| `-tc <name>` | 提取指定标题的章节内容 |
| `-s <pattern>` | 正则表达式搜索 |
| `-n <num>/--context <num>` | 与 `-s` 配合，指定上下文行数（默认 2） |

## 参数使用示例

```bash
# 获取执行建议
PYTHONPATH=. uv run --with pyarmor python scripts/lyxy_document_reader.py --advice document.docx

# 读取全文
PYTHONPATH=. uv run --with pyarmor python scripts/lyxy_document_reader.py document.docx

# 统计字数
PYTHONPATH=. uv run --with pyarmor python scripts/lyxy_document_reader.py document.docx -c

# 提取标题
PYTHONPATH=. uv run --with pyarmor python scripts/lyxy_document_reader.py document.docx -t

# 提取指定章节
PYTHONPATH=. uv run --with pyarmor python scripts/lyxy_document_reader.py document.docx -tc "第三章"

# 搜索内容
PYTHONPATH=. uv run --with pyarmor python scripts/lyxy_document_reader.py document.docx -s "关键词"

# 正则搜索
PYTHONPATH=. uv run --with pyarmor python scripts/lyxy_document_reader.py document.docx -s "\d{4}-\d{2}-\d{2}"

# 指定搜索上下文行数
PYTHONPATH=. uv run --with pyarmor python scripts/lyxy_document_reader.py document.docx -s "关键词" -n 5
```

*也可以使用纯 python 命令：`python scripts/lyxy_document_reader.py ...`*

## 错误处理

| 错误 | 原因 | 解决 |
|------|------|------|
| 错误: input_path 不能为空 | 未提供输入 | 提供 file_path 或 URL |
| 错误: 不支持的文件类型 | 无对应 reader | 检查文件扩展名 |
| 所有解析方法均失败 | 所有解析器失败 | 检查文件是否损坏 |
| 错误: 无效的正则表达式 | 正则语法错误 | 检查正则语法 |
| 错误: 未找到匹配 | 搜索无结果 | 检查搜索词或正则 |
| ModuleNotFoundError | 缺少依赖 | 使用 --advice 获取正确的依赖命令 |
