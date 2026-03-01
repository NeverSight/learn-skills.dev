---
name: dingtalk-sheet-scripts
description: 钉钉表格脚本开发专家。用于编写在钉钉表格中运行的 JavaScript 自动化脚本，支持工作簿、工作表、单元格操作，以及用户交互和网络请求。
---

# 钉钉表格脚本开发

## 运行环境

- 语言：JavaScript (ES6+)
- 运行在钉钉表格的沙箱环境中
- 使用 `Output.log()` 输出日志（不是 `console.log`）
- 支持 `async/await` 和 `fetch` API

## 核心对象

| 对象 | 说明 | 获取方式 |
|------|------|----------|
| Workbook | 工作簿（顶级对象） | 直接使用 |
| Sheet | 工作表 | `Workbook.getActiveSheet()` |
| Range | 单元格区域 | `sheet.getRange('A1:B10')` |
| Input | 用户输入（异步） | `await Input.textAsync()` |
| Output | 日志输出 | `Output.log()` |

## 快速示例

```javascript
// 基础数据写入
const sheet = Workbook.getActiveSheet();
sheet.getRange('A1:B2').setValues([
  ['姓名', '分数'],
  ['张三', 95]
]);

// 异步用户输入
const name = await Input.textAsync('请输入姓名：');
Output.log(`你好，${name}`);

// 网络请求
const response = await fetch('https://api.example.com/data');
const data = await response.json();
```

## 关键规范

### 异步编程

所有异步操作必须使用 `async/await`：

```javascript
// 正确
async function process() {
  const input = await Input.textAsync('输入：');
  const response = await fetch(url);
  const data = await response.json();
}
await process();

// 错误：缺少 async/await
function process() {
  const input = Input.textAsync('输入：'); // 错误
}
process(); // 错误
```

### 数据更新策略

**避免全量回写，只更新变更部分：**

```javascript
// 正确：只更新需要修改的行
const values = sheet.getRange('A2:D100').getValues();
for (let i = 0; i < values.length; i++) {
  if (values[i][2] === '待处理') {
    sheet.getRange(i + 1, 2, 1, 1).setValues([['已处理']]);
  }
}

// 错误：读取整表后全量回写
const allValues = sheet.getRange('A1:D100').getValues();
allValues[5][2] = '已处理';
sheet.getRange('A1:D100').setValues(allValues); // 避免这样做
```

### getRange 参数

- A1 表示法：`sheet.getRange('A1:B10')`
- 数字索引：`sheet.getRange(row, col, rowCount, colCount)` - **行列从 0 开始**

```javascript
sheet.getRange(0, 0, 1, 1)  // A1
sheet.getRange(0, 0, 10, 2) // A1:B10
sheet.getRange(1, 0, 5, 3)  // A2:C6
```

### 错误处理

```javascript
try {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  const data = await response.json();
} catch (error) {
  Output.error(`失败：${error.message}`);
}
```

## 常用模式

### 设置表头样式

```javascript
const header = sheet.getRange('A1:D1');
header.setValues([['ID', '名称', '状态', '金额']]);
header.setFontWeight('bold');
header.setBackgroundColor('#4285F4');
header.setFontColor('#FFFFFF');
```

### 条件格式

```javascript
for (let i = 0; i < values.length; i++) {
  const cell = sheet.getRange(i + 1, 2, 1, 1);
  const score = values[i][2];

  if (score >= 90) cell.setBackgroundColor('#C8E6C9');
  else if (score >= 60) cell.setBackgroundColor('#FFF9C4');
  else cell.setBackgroundColor('#FFCDD2');
}
```

### 用户选择操作

```javascript
const action = await Input.selectAsync('选择操作：', [
  { text: '导入数据', value: 'import' },
  { text: '导出数据', value: 'export' },
  { text: '生成报表', value: 'report' }
]);

if (action === 'import') { /* ... */ }
```

### 文件导入

```javascript
const files = await Input.filesAsync('上传 CSV', {
  multiple: false,
  fileType: '.csv'
});

if (files && files.length > 0) {
  const content = await files[0].text();
  const rows = content.split('\n').map(row => row.split(','));
  sheet.getRange(0, 0, rows.length, rows[0].length).setValues(rows);
}
```

## API 参考

详细 API 文档位于 `docs/api/` 目录：

| API | 说明 | 文档 |
|-----|------|------|
| Workbook | 工作簿 | [docs/api/Workbook.md](docs/api/Workbook.md) |
| Sheet | 工作表 | [docs/api/Sheet.md](docs/api/Sheet.md) |
| Range | 单元格区域 | [docs/api/Range.md](docs/api/Range.md) |
| RangeList | 多选区 | [docs/api/RangeList.md](docs/api/RangeList.md) |
| Input | 用户输入 | [docs/api/Input.md](docs/api/Input.md) |
| Output | 输出日志 | [docs/api/Output.md](docs/api/Output.md) |
| Filter | 筛选 | [docs/api/Filter.md](docs/api/Filter.md) |

## 示例代码

查看 `examples/` 目录获取更多示例：

- [examples/fetch-demo.js](examples/fetch-demo.js) - 网络请求示例（GET/POST、批量请求、错误处理）

## 更新 API 文档

使用 `scripts/update_api_docs.py` 从钉钉官方 OSS 获取最新的 API 文档。

### 依赖安装

```bash
pip install markitdown requests
```

### 用法

```bash
# 更新所有 API 文档
python scripts/update_api_docs.py

# 更新指定的 API 文档
python scripts/update_api_docs.py --api Workbook Sheet Range

# 列出所有可用的 API
python scripts/update_api_docs.py --list
```

### 可用的 API 列表

- **核心对象**: Workbook, Sheet, Range, RangeList
- **用户交互**: Input, Output
- **筛选相关**: Filter, FilterCriteria, FilterCriteriaBuilder, FilterCondition
- **数据格式**: SetValueOptions, DropdownListOption, BorderType, Color, SearchOptions, SortField
- **其他**: Hyperlink
