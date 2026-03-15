---
name: xlsx
description: "当用户任务以电子表格文件为核心输入或输出时必须使用本技能。涵盖 .xlsx/.xlsm/.csv/.tsv 的读取、清洗、修复、建模、公式计算、格式化、图表、模板更新与格式转换。用户只要提到某个表格文件路径并要求处理或产出表格，都应触发本技能。若主要交付物不是电子表格（如 Word/HTML/数据库流水线/Google Sheets API 集成），则不应触发。"
license: Proprietary. LICENSE.txt has complete terms
---

# 输出要求

## 所有 Excel 文件

### 专业字体

- 除非用户另有要求，统一使用专业字体（如 Arial、Times New Roman）

### 公式错误为零

- 交付前必须无 `#REF!/#DIV/0!/#VALUE!/#N/A/#NAME?`

### 更新现有模板时

- 必须严格继承模板既有风格、结构与约定
- 不得把“统一标准样式”强压到已有模板上
- 模板既有规范优先级高于本文件默认建议

## 财务模型补充规范

### 颜色约定（用户或模板未指定时）

- 蓝字 `(0,0,255)`：可调输入/硬编码假设
- 黑字 `(0,0,0)`：公式计算
- 绿字 `(0,128,0)`：同工作簿跨表引用
- 红字 `(255,0,0)`：外部文件链接
- 黄底 `(255,255,0)`：关键假设或待更新单元格

### 数值格式

- 年份用文本显示：`"2024"`（避免 `2,024`）
- 金额：`$#,##0`，并在表头写明单位（如 `($mm)`）
- 零值显示为 `-`（含百分比）
- 百分比默认 `0.0%`
- 倍数默认 `0.0x`
- 负数用括号 `(123)`，不用 `-123`

### 公式构造

- 所有假设放在独立假设区单元格
- 公式用引用，不写硬编码常数
- 例：`=B5*(1+$B$6)`，不要 `=B5*1.05`

### 硬编码来源注释

对硬编码值写明来源（旁注/批注均可）：

`Source: [System/Document], [Date], [Reference], [URL]`

---

# XLSX 创建、编辑与分析

## 概览

任务通常分为：

- 数据分析与清洗（优先 pandas）
- 公式、样式、结构化建模（优先 openpyxl）
- 回算与错误扫描（必须 `scripts/recalc.py`）

## 关键要求

若文件包含公式，交付前必须执行：

```bash
python scripts/recalc.py output.xlsx
```

说明：

- `openpyxl` 只写入公式字符串，不会计算结果
- `scripts/recalc.py` 会调用 LibreOffice 回算并扫描错误
- 沙箱环境由 `scripts/office/soffice.py` 自动做兼容配置

## 读取与分析（pandas）

```python
import pandas as pd

df = pd.read_excel("file.xlsx")                    # 首个 sheet
all_sheets = pd.read_excel("file.xlsx", sheet_name=None)  # 全部 sheet

df.head()
df.info()
df.describe()

df.to_excel("output.xlsx", index=False)
```

---

## 核心原则：计算必须写在 Excel 公式里

不要先在 Python 里算完再把值写回去。  
正确做法是把公式写入单元格，让工作簿可持续重算。

### 错误示例（禁止）

```python
total = df["Sales"].sum()
sheet["B10"] = total

growth = (df.iloc[-1]["Revenue"] - df.iloc[0]["Revenue"]) / df.iloc[0]["Revenue"]
sheet["C5"] = growth
```

### 正确示例

```python
sheet["B10"] = "=SUM(B2:B9)"
sheet["C5"] = "=(C4-C2)/C2"
sheet["D20"] = "=AVERAGE(D2:D19)"
```

---

## 通用工作流

1. 选工具：数据处理用 `pandas`，公式/格式用 `openpyxl`
2. 新建或加载工作簿
3. 修改数据、公式、样式
4. 保存文件
5. 若含公式，必须执行 `scripts/recalc.py`
6. 读取 JSON 报告，修复错误后再次回算，直到零错误

常见错误：

- `#REF!`：引用失效
- `#DIV/0!`：分母为零
- `#VALUE!`：类型不匹配
- `#NAME?`：函数名或命名范围不识别

---

## 新建文件（openpyxl）

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

sheet["A1"] = "Hello"
sheet["B1"] = "World"
sheet.append(["Row", "of", "data"])

sheet["B2"] = "=SUM(A1:A10)"

sheet["A1"].font = Font(bold=True, color="FF0000")
sheet["A1"].fill = PatternFill("solid", start_color="FFFF00")
sheet["A1"].alignment = Alignment(horizontal="center")
sheet.column_dimensions["A"].width = 20

wb.save("output.xlsx")
```

## 编辑现有文件（openpyxl）

```python
from openpyxl import load_workbook

wb = load_workbook("existing.xlsx")
sheet = wb.active

for sheet_name in wb.sheetnames:
    s = wb[sheet_name]
    print(sheet_name)

sheet["A1"] = "New Value"
sheet.insert_rows(2)
sheet.delete_cols(3)

new_sheet = wb.create_sheet("NewSheet")
new_sheet["A1"] = "Data"

wb.save("modified.xlsx")
```

---

## 公式回算与结果校验

```bash
python scripts/recalc.py <excel_file> [timeout_seconds]
python scripts/recalc.py output.xlsx 30
```

脚本输出 JSON，核心字段示例：

```json
{
  "status": "success",
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## 公式检查清单

- [ ] 先抽查 2-3 个关键引用是否正确
- [ ] 检查列号映射（例如 BL/BK 易错）
- [ ] 注意 Excel 行列是 1-based
- [ ] 处理空值 `NaN`
- [ ] 远端列（50+ 列）不要漏
- [ ] 跨表引用格式正确（`Sheet1!A1`）
- [ ] 避免分母为 0
- [ ] 先小范围试算，再全量铺公式

---

## 最佳实践

### 工具选择

- `pandas`：批量数据处理、分析、导出
- `openpyxl`：公式、样式、工作簿结构控制

### openpyxl 注意事项

- 单元格索引是 1-based
- `data_only=True` 可读计算值，但保存后会丢公式（高风险）
- 大文件可用 `read_only=True` / `write_only=True`
- 公式不会自动计算，必须跑 `scripts/recalc.py`

### pandas 注意事项

- 显式指定 dtype，避免推断错误
- 大文件按列读取减少内存
- 日期列用 `parse_dates` 明确解析

## 代码风格

- 生成 Python 代码应简洁、最小化
- 不写多余打印和冗长注释
- 对复杂公式、关键假设、硬编码来源要在工作簿内留注释

