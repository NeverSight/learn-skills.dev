---
name: excel-to-markdown
description: 将 Excel 文件转换为 Markdown 表格，支持合并单元格处理、多工作表输出、基础字体语义（粗体/斜体）与超链接转换。适用于将式样书、数据表转为可读的 Markdown 文档。
---

# Excel 转 Markdown

## 任务目标

将 Excel 文件（.xlsx/.xlsm）转换为合法的 Markdown 表格格式，用于式样书阅读、上下文提供等场景。

## 前置依赖

```
openpyxl>=3.0.0
```

使用 `where python` 找到 python 的安装路径，如果 安装路径里包含 `uv`，则使用 `uv run` 命令来执行脚本，确保在虚拟环境中运行。如果无法找到 python，可以提示用户安装 python 或者使用虚拟环境，然后结束程序。

## 最佳实践

将项目式样书 Excel 转为 Markdown 后，可直接作为开发任务的上下文：

```bash
python scripts/excel_to_markdown_general.py ./式様書.xlsx -o ./式様書.md
```

如用户没有其他特殊需求，执行上面格式的命令即可，如果有更具体的要求，再看下面的【其他参数】部分。

## 其他参数

### 基本转换

```bash
python scripts/excel_to_markdown_general.py <excel文件> [-o <md文件>]
```

### 合并单元格处理模式

```bash
python scripts/excel_to_markdown_general.py <excel文件> --merge-mode tl
```

- `tl`（默认）：仅在合并区域左上角保留值
- `fill`：将左上角值填充到合并区域每个子单元格

### 输出详细日志

```bash
python scripts/excel_to_markdown_general.py <excel文件> --verbose
```

## 资源索引

- 核心脚本：[scripts/excel_to_markdown_general.py](scripts/excel_to_markdown_general.py)
