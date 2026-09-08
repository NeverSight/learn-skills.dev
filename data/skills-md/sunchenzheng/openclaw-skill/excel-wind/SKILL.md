---
name: excel-wind
description: "利用 Excel 作为中间层，通过 Wind Excel 插件（WSD/WSS/WSI 等函数）获取万德金融数据。当用户需要获取 Wind 行情数据、财务指标、板块数据，且 Wind Python API 不可用时（权限问题/网络限制），使用本技能通过 Excel+Wind 插件的路径实现数据获取。触发场景：（1）用户要求从 Wind 获取股票/期货/指数的历史行情 K 线；（2）用户要求获取 Wind 财务指标（PE、PB、EPS、ROE 等）；（3）用户要求获取宏观/行业数据；（4）Wind Python API 连不上但 Excel 插件可用。"
---

# Excel-Wind 插件自动化技能

通过 Excel 的 Wind 金融终端插件（WENDEZHI Add-in）作为数据中间层，实现自动化数据获取。

**核心优势**：不依赖 Wind Python API，直接利用 Excel 内置的 Wind 函数，取数逻辑与终端一致。

---

## 工作流程

```
用户请求 → AI 构建 Wind 公式 → 写入 Excel 单元格 → 触发刷新 → 等待数据返回 → 读取结果
```

### 步骤 1：确认 Wind Excel 插件可用

检查方法：打开 Excel，观察菜单栏是否有「Wind」选项卡。

- **已安装** → 直接进入步骤 2
- **未安装** → 提示用户：打开 Wind 终端 → 开始 → 插件修复 → 修复 Excel 插件

### 步骤 2：构建 Wind 公式

参考 [references/wind_excel_formulas.md](references/wind_excel_formulas.md) 中各函数的语法。

**常用公式速查**：

| 需求 | 公式 |
|------|------|
| 茅台日行情 | `=WSD("600519.SH", "close;open;high;low;volume", "2026-01-01", "2026-04-03", "PriceAdj=F")` |
| 茅台财务指标 | `=WSS("600519.SH", "eps_basic;roe_avg;pb;pe_ttm", "")` |
| 沪深300成分 | `=WSET("CurSectorHS300", "wind_code", "")` |
| 宏观GDP | `=EDI("G00101010000000000", "2020-01-01", "2026-04-03", "")` |

### 步骤 3：执行自动化脚本

使用 `scripts/excel_wind.py`：

```bash
# 获取股票历史K线
python scripts/excel_wind.py wsd --code 600519.SH --fields close,open,high,low --begin 2026-01-01 --end 2026-04-03 --out 茅台行情.xlsx

# 获取财务指标
python scripts/excel_wind.py wss --code 600519.SH,000001.SZ --fields eps_basic,roe_avg,pb,pe_ttm --out 财务指标.xlsx

# 创建空白模板（用于手动埋入公式）
python scripts/excel_wind.py template --out Wind_Template.xlsx
```

**参数说明**：
- `--visible`：显示 Excel 窗口（调试用）
- `--wait`：等待 Wind 数据返回的秒数（默认15秒，网络慢可加大）
- `--options`：Wind 特有选项，如 `PriceAdj=F`（前复权）

### 步骤 4：读取 Excel 数据

数据刷新后，Excel 公式结果会写入单元格。使用 `--read` 模式读取：

```python
# 在 Python 中读取 Excel 结果
import win32com.client
excel = win32com.client.Dispatch("Excel.Application")
wb = excel.Workbooks.Open("茅台行情.xlsx")
ws = wb.Worksheets("WSD_K线")
data = ws.UsedRange.Value  # 读取所有数据
```

---

## 核心脚本

**路径**：`scripts/excel_wind.py`

| 函数 | 作用 |
|------|------|
| `build_wsd_formula()` | 构建 WSD 日时间序列公式 |
| `build_wss_formula()` | 构建 WSS 截面指标公式 |
| `build_wsi_formula()` | 构建 WSI 分钟序列公式 |
| `excel_com("init")` | 启动/创建 Excel 工作簿 |
| `excel_com("write_formulas")` | 批量写入公式到单元格 |
| `excel_com("refresh")` | 触发全量刷新并等待 |
| `excel_com("read_range")` | 读取单元格区域数据 |
| `excel_com("save")` | 另存为文件 |
| `excel_com("close")` | 关闭工作簿退出 Excel |

---

## Excel 手动操作指引（用户可自行操作）

如果 AI 脚本执行困难，用户也可以手动完成：

1. **打开 Excel**，新建工作簿
2. **写入公式**（以 A1 为例）：
   - A1 填证券代码：`600519.SH`
   - B1 填公式：`=WSD(A1,"close","2026-01-01","2026-04-03","PriceAdj=F")`
3. **刷新数据**：按 `Ctrl+Alt+F5`，或点击「Wind」选项卡 → 「刷新数据」
4. **等待返回**：约 5-30 秒
5. **数据读出后**：复制到目标位置，或另存 CSV

---

## 注意事项

1. **Wind 终端必须登录**：Excel 插件依赖本地终端的登录态，断网或未登录会导致 `#WIND_ERR` 错误
2. **等待时间**：Wind 取数涉及网络请求，默认等待 15 秒，网络慢时需加大 `--wait` 参数
3. **复权选项**：历史行情建议加 `PriceAdj=F`（前复权），否则 K 线可能出现跳空
4. **市价数据**：WSS 获取的是截面快照（当日最新），无需刷新等待
5. **权限限制**：部分财务指标（如套保参数）需要单独开通权限

---

## 常见错误处理

| 错误值 | 含义 | 解决方法 |
|--------|------|----------|
| `#WIND_ERR` | Wind终端未连接 | 检查终端是否登录，网络是否正常 |
| `#NAME?` | 插件未加载 | 在 Excel 中重新加载 Wind 插件 |
| `#VALUE!` | 参数类型错误 | 检查证券代码格式、日期格式 |
| `#REF!` | 字段不存在 | 确认字段名在 Wind 支持列表中 |
| `#NUM!` | 日期区间无效 | 检查结束日期是否早于开始日期 |

---

## 文件结构

```
excel-wind/
├── SKILL.md                                    # 本文件
├── scripts/
│   └── excel_wind.py                          # 核心自动化脚本
└── references/
    ├── wind_excel_formulas.md                 # Wind Excel 公式完整参考
    └── query_config.json                      # 通用查询配置模板
```
