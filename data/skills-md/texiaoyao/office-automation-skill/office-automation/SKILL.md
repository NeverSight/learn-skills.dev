---
name: office-automation
description: 自动化处理 Word 和 Excel 文件。使用 Python 脚本读取、写入、格式化文档和表格。支持批量处理、模板填充、数据提取和格式转换。
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["python3"], "python_packages": ["python-docx", "openpyxl", "pandas"] },
        "install":
          [
            {
              "id": "office-deps",
              "kind": "pip",
              "packages": ["python-docx", "openpyxl", "pandas"],
              "label": "安装 Office 处理依赖 (pip)",
            },
          ],
      },
  }
---

# Office 自动化技能

使用 Python 脚本自动化处理 Word (.docx) 和 Excel (.xlsx/xlsm) 文件。

## 快速开始

### 1. 安装依赖

```bash
pip install python-docx openpyxl pandas
```

### 2. 基本用法

**处理 Word 文档：**
```bash
python scripts/word_processor.py read document.docx
python scripts/word_processor.py write output.docx --content "Hello World"
python scripts/word_processor.py template fill.docx --data '{"name": "张三", "date": "2026-02-22"}'
```

**处理 Excel 表格：**
```bash
python scripts/excel_processor.py read data.xlsx
python scripts/excel_processor.py write output.xlsx --sheet "Sheet1"
python scripts/excel_processor.py merge folder/ --output merged.xlsx
```

---

## 脚本说明

### word_processor.py

| 命令 | 说明 | 示例 |
|------|------|------|
| `read` | 读取 Word 文档内容 | `read file.docx` |
| `write` | 创建新文档 | `write out.docx --content "文本"` |
| `template` | 填充模板（替换 {{变量}}） | `template doc.docx --data '{"key": "value"}'` |
| `extract` | 提取表格到 CSV | `extract file.docx --table 1` |
| `format` | 格式化文档 | `format file.docx --style heading` |

### excel_processor.py

| 命令 | 说明 | 示例 |
|------|------|------|
| `read` | 读取 Excel 数据 | `read data.xlsx --sheet Sheet1` |
| `write` | 写入数据到 Excel | `write out.xlsx --data data.json` |
| `merge` | 合并多个 Excel 文件 | `merge folder/ --output all.xlsx` |
| `convert` | Excel ↔ CSV 转换 | `convert file.xlsx --to csv` |
| `analyze` | 数据分析（统计、透视） | `analyze sales.xlsx --pivot` |

---

## 使用场景

### Word 处理
- 📝 批量生成报告/合同
- 📋 填充模板文档
- 📊 提取文档中的表格数据
- 🎨 统一文档格式

### Excel 处理
- 📈 数据汇总和合并
- 🔄 格式转换（Excel ↔ CSV）
- 📊 数据分析和统计
- 📋 批量处理多个表格

---

## 注意事项

1. **Word 格式**：仅支持 .docx 格式（不支持旧版 .doc）
2. **Excel 格式**：支持 .xlsx 和 .xlsm
3. **编码**：默认使用 UTF-8 编码
4. **大文件**：超过 100MB 的文件建议分批次处理

---

## 脚本位置

所有脚本位于 `skills/office-automation/scripts/` 目录。

使用时请确保从技能目录或 workspace 根目录运行。
