---
name: excel-parser
description: 支持多种Excel格式的内容提取和写入技能，使用calamine库处理.xls、.xlsx、.xlsm等格式。当用户需要解析Excel文件、提取表格数据、将Excel转换为文本格式、分析Excel内容、批量处理Excel文件、创建新Excel文件或更新现有Excel文件时，务必使用此技能。适用于数据提取、报表分析、内容审核、数据导出等场景。
tags:
  - excel
  - spreadsheet
  - data-extraction
  - data-writing
  - calamine
  - xls
  - xlsx
  - xlsm
  - openpyxl
  - xlrd
---

# Excel Parser Skill

Excel Parser技能用于从Excel文件中提取内容和写入内容，支持多种Excel格式。

## Compatibility

- Python 3.7+
- 依赖: `python-dotenv`, `python-calamine`
- 备选依赖: `xlrd` (用于.xls文件), `openpyxl` (用于.xlsx文件)

## 使用方法

### 基本使用

```python
from excel_parser import ExcelParser, process_excel, write_excel_file, update_excel_file

# 方法1: 使用ExcelParser类
parser = ExcelParser()

# 读取Excel文件
result = parser.parse_excel('path/to/file.xlsx')

# 获取文本格式输出
text = parser.parse_excel_to_text('path/to/file.xlsx')

# 写入Excel文件
write_data = {
    "sheets": [
        {
            "name": "Sheet1",
            "rows": [["A1", "B1"], ["A2", "B2"]],
            "merged_cells": [
                {
                    "start_row": 0,
                    "end_row": 0,
                    "start_col": 0,
                    "end_col": 1
                }
            ]
        }
    ]
}
parser.write_excel('output.xlsx', write_data)

# 更新Excel文件
parser.update_excel('existing_file.xlsx', write_data)

# 方法2: 使用便捷函数
# 读取Excel文件
result = process_excel('path/to/file.xlsx')

# 写入Excel文件
write_result = write_excel_file('output.xlsx', write_data)

# 更新Excel文件
update_result = update_excel_file('existing_file.xlsx', write_data)
```

### 返回结果格式

```python
{
    "text": "格式化的文本内容",
    "sheets": [
        {
            "name": "Sheet1",
            "rows": [["A1", "B1"], ["A2", "B2"]],
            "row_count": 2,
            "column_count": 2
        }
    ],
    "sheet_count": 1,
    "total_cells": 4,
    "engine": "python-calamine"
}
```

## 支持的文件格式

- .xls (Excel 97-2003)
- .xlsx, .xlsm (Excel 2007+)
- .xltx, .xltm (Excel模板)

## 环境变量配置

创建 `.env` 文件:

```env
# 最大行数限制，默认100行
EXCEL_MAX_ROWS=100

# 是否保留空行，默认false
EXCEL_KEEP_EMPTY_ROWS=false
```

## 详细文档

更多使用示例和故障排除信息，参见 [README.md](README.md)。
