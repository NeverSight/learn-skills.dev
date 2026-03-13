---
name: fund-screener
description: 中国公募基金全市场筛选与深度分析工具，支持夏普/索提诺/卡玛等量化指标筛选
user-invocable: yes
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "os": ["darwin", "linux", "win32"],
        "requires": {
          "anyBins": ["python3", "python"]
        },
        "install": [
          {
            "id": "pip",
            "kind": "uv",
            "package": "akshare pandas numpy",
            "bins": ["python3"],
            "label": "pip install akshare pandas numpy"
          }
        ]
      }
  }
---

# 基金分析技能 (Fund Screener)

通过 AkShare 获取中国公募基金实时数据，基于量化指标筛选优质基金产品。

## 功能

1. **单基金深度分析**: 对单只基金进行全方位诊断，包括风险指标、阶段收益、年度收益、资产配置、基金经理、持仓信息
2. **全市场批量筛选**: 从全市场开放式基金中智能筛选，支持多种模式
3. **结果导出**: 自动保存 CSV 文件

## 使用方法

运行此技能需要 Python 3.8+ 和依赖: `pip install akshare pandas numpy`

```bash
# 单基金分析
python fund_screener.py <基金代码> [基金名称]

# 纯债基金筛选（低风险）
python fund_screener.py --bond

# 固收+基金筛选
python fund_screener.py --gushou-plus

# 股票类基金筛选
python fund_screener.py --stock

# Alpha策略筛选（卡玛比率）
python fund_screener.py --stock-alpha

# 自定义参数
python fund_screener.py --bond --min-sharpe 1.0 --max-dd 2 --min-return 2.5
python fund_screener.py --gushou-plus --min-sortino 1.5
python fund_screener.py --stock-alpha --min-calmar 0.8 --min-return 10

# 数量控制
python fund_screener.py --bond --max 50
```

## 筛选模式与指标

| 模式 | 参数 | 核心指标 | 默认筛选标准 |
|------|------|----------|------------|
| 纯债基金 | `--bond` | 夏普比率 | 夏普>=1.0, 回撤<2%, 收益>2.5% |
| 固收+ | `--gushou-plus` | 索提诺比率 | 夏普>=0.8, 索提诺>=1.2, 回撤<5%, 收益>3.5% |
| 股票Alpha | `--stock-alpha` | 卡玛比率 | 卡玛>=1.2, 回撤<30%, 收益>10% |
| 默认/股票 | 无/`--stock` | 夏普比率 | 夏普>=0.5, 回撤<15%, 收益>3% |

## 自定义参数

| 参数 | 说明 |
|------|------|
| `--min-sharpe <value>` | 最小夏普比率 |
| `--min-sortino <value>` | 最小索提诺比率 |
| `--min-calmar <value>` | 最小卡玛比率 |
| `--max-dd <value>` | 最大回撤百分比（正数，如5表示<5%） |
| `--min-return <value>` | 最小年化收益率(%) |
| `--max <value>` | 最大分析数量（50-500） |

## 作为 Python 模块使用

```python
from fund_screener import get_fund_metrics, analyze_single_fund, calculate_sharpe_ratio

# 分析单只基金
metrics = get_fund_metrics('004010', '华泰柏瑞鼎利混合A')

# 深度分析
analysis = analyze_single_fund('004010')
```

## 数据来源

- 基金净值: 东方财富网 (via AkShare)
- 基金经理/规模: 基金经理持仓数据
- 资产配置: 基金季度持仓报告
- **数据验证**: 百度股市通 (via BrowserMCP，可选增强)

## 浏览器数据验证（BrowserMCP）

AkShare的部分数据存在已知偏差（基金规模为经理总规模而非单只基金规模、持仓数据可能滞后、收益率计算口径差异）。当BrowserMCP可用时，应在Python筛选生成CSV后，自动通过浏览器访问**百度股市通**进行数据交叉验证和修正。

### 前置条件

- `.mcp.json` 中已配置 BrowserMCP

### 完整工作流

```
Step 1: 运行Python筛选 → 生成初始CSV
Step 2: 读取CSV，识别A/C份额对，去重
Step 3: 逐只基金通过BrowserMCP访问百度股市通
Step 4: 验证并修正三大数据：规模、持仓、收益
Step 5: 更新CSV + 保存验证缓存JSON
Step 6: 输出修正摘要
```

### Step 2: A/C份额去重

同一基金的A/C份额共享相同的持仓和规模，无需重复验证。去重规则：
- 去掉基金名称末尾的A/B/C/E/H后缀进行分组
- 每组只验证一个份额（代码数字较小的优先）
- 验证后的持仓和规模数据复制到同组所有份额
- 近1年收益因费率差异不同，每个份额单独取值（或仅验证A份额）

### Step 3: 浏览器验证协议

对每只唯一基金，访问两个页面：

#### 3a. 持仓页 — 获取前5大持仓

**URL**: `https://gushitong.baidu.com/fund/ab-{code}?mainTab=%E6%8C%81%E4%BB%93`

使用 `browser_navigate` 访问后 `browser_snapshot` 获取快照。在快照文本中查找：

```
十大重仓股票  更新日期：YYYY-MM-DD
股票A名 X.XX% 股票B名 X.XX% 股票C名 X.XX% ...
```

提取前5个股票名称，用 `, ` 连接作为"前5大持仓"。

**异常处理**：
- 若显示 `十大重仓股票 暂无数据` → 保留CSV原值（港股通基金常见）
- 若页面超时 → 重试1次，仍失败则跳过
- 若显示 `服务异常` → 等待2秒后重试

#### 3b. 简况页 — 获取规模和近1年收益

**URL**: `https://gushitong.baidu.com/fund/ab-{code}?mainTab=%E7%AE%80%E5%86%B5`

使用 `browser_navigate` 访问后 `browser_snapshot` 获取快照。在快照文本中查找：

- **近1年收益**: 寻找 `近一年` 附近的百分比数值，如 `+53.47% 近一年` → 提取 `53.47`
- **基金规模**: 寻找 `规模` 附近的数值，格式如 `X.XX亿` → 提取 `X.XX`

> 注意：部分基金的规模在简况页未直接显示数值，可尝试从持仓页的快照中查找。

### Step 4: 修正CSV

对每只验证过的基金：
- 若百度的"前5大持仓"与CSV不同 → 用百度数据覆盖CSV
- 若百度的"基金规模"与CSV不同 → 用百度数据覆盖CSV
- 若百度的"近1年收益"与CSV不同 → 用百度数据覆盖CSV
- 对A/C份额对：将A份额的持仓和规模数据同步到C份额

### Step 5: 保存验证缓存

更新 `baidu_fund_data.json` 文件，Schema如下：

```json
{
  "004814": {
    "规模": "189.25",
    "近1年": "53.63",
    "前5大持仓": "紫金矿业, 徐工机械, 新华保险, 中国重汽, 三一重工",
    "持仓更新日期": "2025-12-31",
    "验证时间": "2026-02-24"
  }
}
```

### Step 6: 输出修正摘要

验证完成后打印汇总表：

```
=== 数据验证摘要 ===
总计检查: 25 只（去重后）
规模修正: 18 只
持仓修正: 14 只
收益修正: 4 只
跳过(暂无数据): 2 只
```

### 性能优化

- 每次页面加载后等待1-2秒，避免触发反爬
- 25只唯一基金约需50次页面加载，预计耗时5-8分钟
- 可利用缓存JSON：若当天已验证过，跳过重复验证

## 风险提示

历史业绩不代表未来表现。本工具仅供学习研究，不构成投资建议。
