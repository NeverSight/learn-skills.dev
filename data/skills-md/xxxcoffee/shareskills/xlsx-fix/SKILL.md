---
name: xlsx-fix
description: |
  当处理 .xlsx, .xlsm 文件时，如果使用 openpyxl 读取遇到 'expected <class \'openpyxl.styles.fills.Fill\'>' 错误，使用此 skill 修复。
  在读取 .xlsx 文件失败并出现 Fill 相关错误时，自动调用修复脚本修复空 fill 标签问题，然后重新尝试读取。
  适用于：使用 openpyxl 读取 Excel 文件时报错的情况，特别是 styles.xml 中存在空 <fill/> 标签导致的解析错误。
---

# Fix Excel Skill

## 用途

此 skill 用于修复损坏或格式不规范的 Excel (.xlsx) 文件，特别是当 openpyxl 库在读取时出现以下错误时：

```
expected <class 'openpyxl.styles.fills.Fill'>
```

## 错误原因

这个错误通常发生在 Excel 文件的 `xl/styles.xml` 中存在空的 `<fill/>` 或 `<fill></fill>` 标签。某些工具（包括一些 Claude skills）生成的 Excel 文件可能包含这种不规范的格式，导致 openpyxl 无法正确解析。

## 修复原理

修复脚本会：
1. 将 xlsx 文件作为 zip 解压
2. 找到 `xl/styles.xml` 文件
3. 将空的 `<fill/>` 或 `<fill></fill>` 标签替换为有效的 `<fill><patternFill patternType="none"/></fill>`
4. 重新打包为 xlsx 文件
5. 自动创建 .bak 备份文件

## 使用方法

当使用 openpyxl 读取 Excel 文件时，如果捕获到 `expected <class 'openpyxl.styles.fills.Fill'>` 错误：

1. **调用修复脚本**

   ```python
   import subprocess
   import sys

   # 获取修复脚本路径（相对于 skill 目录）
   fix_script = "<skill_path>/scripts/fix_excel.py"

   # 调用修复脚本
   result = subprocess.run(
       [sys.executable, fix_script, excel_file_path],
       capture_output=True,
       text=True
   )

   if result.returncode == 0:
       # 修复成功，重新尝试读取
       wb = openpyxl.load_workbook(excel_file_path)
   ```

2. **或者直接使用 Python 函数**

   ```python
   import sys
   sys.path.insert(0, "<skill_path>/scripts")
   from fix_excel import fix_xlsx_empty_fills

   # 修复文件
   fixed_path = fix_xlsx_empty_fills(excel_file_path)

   # 重新读取
   wb = openpyxl.load_workbook(fixed_path)
   ```

## 完整示例代码

```python
import openpyxl
import subprocess
import sys
import os

def load_workbook_with_fix(file_path: str):
    """
    加载 Excel 文件，如果遇到 Fill 错误则自动修复
    """
    try:
        return openpyxl.load_workbook(file_path)
    except Exception as e:
        error_msg = str(e)
        if "expected <class 'openpyxl.styles.fills.Fill'>" in error_msg:
            print(f"检测到 Excel 文件格式错误，正在修复: {file_path}")

            # 获取 skill 脚本路径
            skill_scripts_dir = os.path.join(
                os.path.dirname(__file__), "..", "scripts"
            )
            fix_script = os.path.join(skill_scripts_dir, "fix_excel.py")

            # 调用修复脚本
            result = subprocess.run(
                [sys.executable, fix_script, file_path],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("修复成功，重新加载文件...")
                return openpyxl.load_workbook(file_path)
            else:
                raise RuntimeError(f"修复失败: {result.stderr}")
        else:
            raise

# 使用示例
wb = load_workbook_with_fix("data.xlsx")
```

## 注意事项

1. 修复脚本会自动创建 `.bak` 备份文件
2. 只支持 `.xlsx` 格式，不支持 `.xls` 或 `.xlsm`
3. 修复后的文件应该能被 openpyxl 正常读取
4. 如果修复后仍有问题，可以尝试手动检查 styles.xml 文件

## 脚本路径

修复脚本位于：`scripts/fix_excel.py`
