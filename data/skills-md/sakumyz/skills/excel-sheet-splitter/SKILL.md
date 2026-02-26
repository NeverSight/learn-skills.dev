---
name: excel-sheet-splitter
description: 将Excel工作簿按工作表拆分为独立的Excel文件，每个工作表生成一个单独的文件。适用场景：(1) 将多工作表Excel文件拆分为单独文件，(2) 提取特定工作表为独立文件，(3) 分发合并工作簿中的工作表，(4) 为单独处理或分发创建工作表副本。
---

# Excel工作表拆分工具

## 任务目标

- 本Skill用于：将Excel工作簿(.xlsx, .xlsm)按工作表拆分为独立的Excel文件
- 能力包含：保留所有单元格值和公式、保持原始格式、维护列宽行高、保留合并单元格
- 触发条件：用户需要将多工作表Excel文件拆分为独立文件时

## 前置准备

- 依赖说明：scripts脚本所需的Python包
  ```
  openpyxl>=3.0.0
  ```
- Python版本：3.7或更高版本

## 操作步骤

### 第一步：准备拆分

将需要拆分的Excel文件准备好，确保文件格式为.xlsx或.xlsm。

### 第二步：执行拆分

#### 基本用法

使用默认设置拆分Excel文件（输出到相同目录）：

```bash
python scripts/split_excel_sheets.py input_file.xlsx
```

这将创建名为`input_file_Sheet1.xlsx`、`input_file_Sheet2.xlsx`等的文件。

#### 高级选项

**指定输出目录：**

```bash
python scripts/split_excel_sheets.py input_file.xlsx -o ./output_folder
```

**自定义文件名前缀：**

```bash
python scripts/split_excel_sheets.py data.xlsx -p "2024年报表"
```

生成：`2024年报表_Sheet1.xlsx`、`2024年报表_Sheet2.xlsx`等。

**JSON格式输出（用于程序化调用）：**

```bash
python scripts/split_excel_sheets.py input_file.xlsx --json
```

返回包含文件路径和状态的结构化JSON数据。

### 第三步：查看结果

拆分完成后，在输出目录查看生成的Excel文件。每个工作表都会生成一个独立的Excel文件。

## Python API调用

可以直接在Python代码中导入并使用函数：

```python
from scripts.split_excel_sheets import split_excel_sheets

result = split_excel_sheets(
    input_file='data.xlsx',
    output_dir='./output',
    prefix='自定义前缀'
)

print(f"状态: {result['status']}")
print(f"创建了 {len(result['files'])} 个文件")
```

## 输出格式说明

脚本返回一个字典，包含以下字段：

- `status`: 状态码 ('success'成功, 'partial_success'部分成功, 'error'错误)
- `message`: 人类可读的摘要信息
- `input_file`: 原始文件路径
- `output_directory`: 文件创建位置
- `files`: 创建的文件路径列表
- `errors`: 错误信息列表（如有）
- `total_sheets`: 原始文件中的工作表数量
- `successful`: 成功创建的文件数量
- `failed`: 失败的工作表数量

## 文件命名规则

输出文件命名格式：`{前缀}_{工作表名}.xlsx`

- 默认前缀：输入文件名（不含扩展名）
- 工作表名会被清理（仅保留字母数字、空格、连字符、下划线）
- 文件系统不兼容的字符（如`/`、`\`、`*`、`?`）会被移除

## 保留内容说明

拆分后的每个文件将保留：

- 所有单元格值和公式
- 原始格式（字体、颜色、边框、填充、数字格式）
- 列宽和行高
- 合并单元格
- 工作表结构

## 错误处理

脚本能处理常见问题：

- **文件不存在**：报告文件未找到
- **无工作表**：报告工作簿为空
- **工作表处理错误**：继续处理其余工作表，逐个报告错误
- **工作表名中的非法字符**：自动清理为有效文件名

退出代码：

- `0`: 成功或部分成功
- `1`: 完全失败

## 局限性说明

- **外部引用公式**：如果公式引用其他工作表的单元格，在独立文件中可能显示错误
- **工作表间依赖**：引用其他工作表的图表或数据验证可能无法正常工作
- **宏代码**：.xlsm文件的VBA代码会被保留，但引用其他工作表的宏可能失败

## 使用示例

### 示例1：拆分报表用于分发

**功能**：将月度报表按部门工作表拆分
**执行方式**：脚本执行

```bash
python scripts/split_excel_sheets.py monthly_report.xlsx -o ./team_reports -p "2024年1月"
```

**输出**：在team_reports目录生成以"2024年1月"为前缀的独立Excel文件

### 示例2：提取所有工作表用于单独处理

**功能**：将合并数据文件的每个工作表提取为独立文件
**执行方式**：脚本执行

```bash
python scripts/split_excel_sheets.py consolidated_data.xlsx
```

**输出**：每个工作表成为独立的Excel文件，可用于单独分析

### 示例3：程序化批量处理

**功能**：批量处理多个Excel文件
**执行方式**：Python代码

```python
import glob
from scripts.split_excel_sheets import split_excel_sheets

for file in glob.glob('*.xlsx'):
    result = split_excel_sheets(file, output_dir='./split_files')
    if result['status'] != 'success':
        print(f"{file}处理遇到问题: {result['message']}")
```

**输出**：所有Excel文件的工作表都被拆分到split_files目录

## 测试建议

在处理重要文件之前，建议使用样本工作簿进行测试：

```bash
# 使用测试文件进行拆分
python scripts/split_excel_sheets.py test_file.xlsx -o ./test_output
# 验证所有工作表都被正确拆分并保留格式
```

## 资源索引

- 核心脚本：见 [scripts/split_excel_sheets.py](scripts/split_excel_sheets.py)（Excel工作表拆分工具）

## 注意事项

- 确保Excel文件路径正确，文件格式为.xlsx或.xlsm
- 拆分后的文件中，跨工作表引用的公式可能需要手动调整
- 工作表名中的特殊字符会被自动清理为文件系统兼容的字符
- 建议先用测试文件验证功能，再处理重要数据
