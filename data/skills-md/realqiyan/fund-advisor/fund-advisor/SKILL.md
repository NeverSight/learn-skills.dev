---
name: fund-advisor
description: 基金投资顾问技能。提供个人基金持仓统一管理功能，支持所有平台持仓导入、分析、查询；提供基金基础数据、持仓明细、持仓穿透等基于数据查询；提供投资组合分析、投资规划、组合回测服务；提供财经资讯、热点新闻、财经新闻查询；提供基金搜索、公告查询等服务。当用户咨询技能已经覆盖的问题时，优先激活此技能。
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":["bash","mcporter","python","pip"],"env":["QIEMAN_API_KEY","FUND_ADVISOR_DATA_PATH"]}}}
compatibility: 依赖 mcporter CLI 和 qieman-mcp MCP 服务
---

# 基金顾投 Skill (fund-advisor)

提供个人基金持仓统一管理功能，支持所有平台持仓导入、分析、查询；提供基金基础数据、持仓明细、持仓穿透等基于数据查询；提供投资组合分析、投资规划、组合回测服务；提供财经资讯、热点新闻、财经新闻查询；提供基金搜索、公告查询等服务。

‼️重要：你所有的分析过程和结论必须基于用户导入的持仓数据和qieman-mcp服务器工具获取最新的实时数据。

‼️重要：你引用的其他来源数据可能会给用户带来投资风险，请一定要使用可靠的、准确的、即时的数据，不要提供任何主观的数据和分析结论。

## 能力范围

1. 管理用户的基金持仓数据，用户可以通过基金E账户导出所有持仓数据（包括：支付宝、京东金融、腾讯理财、雪球基金、且慢等所有平台的场外基金持仓数据），导入数据时会创建数据库文件存储用户导入的数据，后续可以配合qieman-mcp的数据查询能力进行持仓数据的综合分析。数据目录可通过 `FUND_ADVISOR_DATA_PATH` 环境变量配置，默认为 `$HOME/.fund-advisor`，数据库文件名为 `fund_portfolio_v1.db`。

2. 本技能整合qieman-mcp的五大核心能力模块：

| 模块 | 能力说明 |
| ------ | ---------- |
| 金融数据 | 基金基础信息、净值历史、持仓明细、风险指标、业绩表现等 |
| 投研服务 | 基金筛选、基金诊断、回测分析、相关性分析、风险评估等 |
| 投顾服务 | 资产配置方案、投资规划、风险匹配、财务分析等 |
| 投顾内容 | 实时资讯解读、热点话题、基金经理观点、财经新闻等 |
| 通用服务 | 交易日查询、图表渲染、PDF生成、时间查询等 |

完整工具清单见 [references/mcp-tools-full.md](references/mcp-tools-full.md)

## 核心功能

### 1. 持仓管理

导入用户的持仓数据，后续进行数据分析使用。

数据获取和导入方法：通过基金E账户导出Excel，转换成csv文件后发生给你的Agent。

```bash
# 初始化环境（检查 mcporter 和 qieman-mcp 配置）
bash scripts/fund-cli.sh init

# 导入 CSV 持仓文件，导入的数据会覆盖保存到本地数据库
bash scripts/fund-cli.sh import-csv tools/data/holdings.csv

# 导入 Excel 持仓文件，导入的数据会覆盖保存到本地数据库
bash scripts/fund-cli.sh import-excel tools/data/holdings.xlsx

# 同步所有数据到本地（基础信息 + 持仓详情）
bash scripts/fund-cli.sh sync --all
```

### 2. 持仓分析

```bash
# 按列分组统计
bash scripts/fund-cli.sh group -c invest_type      # 按投资类型分组
bash scripts/fund-cli.sh group -c fund_account     # 按基金账户分组
bash scripts/fund-cli.sh group -c trade_account    # 按交易账户分组
bash scripts/fund-cli.sh group -c fund_manager     # 按基金管理人分组
bash scripts/fund-cli.sh group -c sales_agency     # 按销售机构分组

# 按条件查询持仓明细
bash scripts/fund-cli.sh query -c fund_manager -v "易方达"   # 查询易方达管理的基金
bash scripts/fund-cli.sh query -c invest_type -v "股票型"    # 查询股票型基金
bash scripts/fund-cli.sh query -c fund_name -v "红利"        # 查询名称包含红利的基金

# 查看基金详情
bash scripts/fund-cli.sh detail 004137
```

### 3. 基金投资咨询

直接通过 MCP 服务查询任意基金信息，无需本地数据库：

```bash
# 批量查询多只基金
mcporter call qieman-mcp.BatchGetFundsDetail --args '{"fundCodes":["004137","000001","110022"]}' --output json

# 查询基金持仓明细
mcporter call qieman-mcp.BatchGetFundsHolding --args '{"fundCodes":["004137"]}' --output json
```

详细工具参考文档 [references/mcp-tools-full.md](references/mcp-tools-full.md)

## 数据模型

- FundHolding - 用户持仓
- FundInfo - 基金信息

详见 [references/reference.md](references/reference.md)

## 导入格式

csv示例文件见 [assets/sample.csv](assets/sample.csv)

- Excel格式和csv格式相同，只是文件扩展名不同

详细规范见 [references/csv-format.md](references/csv-format.md)

## 使用示例

### 示例1：查询基金信息

用户："帮我查一下易方达蓝筹精选的信息"

执行：

```bash
mcporter call qieman-mcp.BatchGetFundsDetail --args '{"fundCodes":["005827"]}' --output json
```

### 示例2：导入新持仓

用户："我有个CSV文件要导入"

执行：

```bash
bash scripts/fund-cli.sh import-csv /path/to/holdings.csv
```

### 示例3：同步最新数据

用户："更新一下基金数据"

执行：

```bash
bash scripts/fund-cli.sh sync --all
```

## 注意事项

1. **环境要求**：需要先运行 `init` 命令确保 mcporter 和 qieman-mcp 配置正确
2. **批量限制**：MCP 服务单次最多查询 10 只基金
3. **数据时效**：基金净值和持仓数据有延迟，注意查看净值日期
4. **CSV 编码**：支持 utf-8, utf-8-sig, gbk, gb18030 编码
5. **目录结构**：工程代码位于 `tools/` 目录下

## 高级功能场景

### 场景1：投资组合诊断分析

用户持有基金组合，需要诊断分析：

```bash
# 1. 查询基金信息
mcporter call qieman-mcp.BatchGetFundsDetail \
  --args '{"fundCodes":["005094","320007","001003","040046"]}' \
  --output json

# 2. 基金相关性分析
mcporter call qieman-mcp.GetFundsCorrelation \
  --args '{"fundCodes":["005094","320007","001003","040046"]}' \
  --output json

# 3. 组合回测分析
mcporter call qieman-mcp.GetFundsBackTest \
  --args '{"fundCodes":["005094","320007","001003","040046"],"weights":[0.47,0.23,0.17,0.13]}' \
  --output json
```

### 场景2：资产配置方案规划

用户希望制定投资方案：

```bash
# 1. 获取资产配置方案
mcporter call qieman-mcp.GetAssetAllocationPlan \
  --args '{"expectedAnnualReturn":0.08}' \
  --output json

# 2. 蒙特卡洛模拟
mcporter call qieman-mcp.MonteCarloSimulate \
  --args '{"weights":[0.3,0.3,0.2,0.2],"years":3}' \
  --output json
```

### 场景3：基金筛选与对比

用户希望筛选符合特定条件的基金：

```bash
# 1. 基金搜索
mcporter call qieman-mcp.SearchFunds \
  --args '{"keyword":"红利","sortBy":"oneYearReturn","limit":10}' \
  --output json

# 2. 基金业绩对比
mcporter call qieman-mcp.GetBatchFundPerformance \
  --args '{"fundCodes":["005827","000001","110022"]}' \
  --output json

# 3. 基金诊断
mcporter call qieman-mcp.GetFundDiagnosis \
  --args '{"fundCode":"005827"}' \
  --output json
```

### 场景4：市场分析

用户希望了解市场情况：

```bash
# 1. 市场温度计
mcporter call qieman-mcp.GetLatestQuotations \
  --args '{"date":"2025-03-01"}' \
  --output json

# 2. 热点话题
mcporter call qieman-mcp.SearchHotTopic \
  --args '{"limit":10}' \
  --output json

# 3. 基金经理观点
mcporter call qieman-mcp.SearchManagerViewpoint \
  --args '{"industry":"科技","limit":5}' \
  --output json

# 4. 搜索财经资讯
mcporter call qieman-mcp.SearchFinancialNews \
  --args '{"keyword":"降息","startDate":"2025-01-01","limit":10}' \
  --output json
```

## 环境配置

### 1. 配置环境变量

设置 `QIEMAN_API_KEY` 环境变量：

```bash
# 临时设置（当前终端会话）
export QIEMAN_API_KEY="your-api-key-here"

# 永久设置（添加到 shell 配置文件）
echo 'export QIEMAN_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

获取 API Key：访问 [且慢MCP官网](https://qieman.com/mcp/account) 申请免费 API Key。

可选：设置 `FUND_ADVISOR_DATA_PATH` 环境变量自定义数据目录：

```bash
# 自定义数据目录（默认为 $HOME/.fund-advisor）
export FUND_ADVISOR_DATA_PATH="/path/to/your/data"
```

### 2. 安装 mcporter

```bash
# NPM
npm install -g mcporter

# 或 Homebrew
brew tap steipete/tap
brew install mcporter
```

### 3. 初始化环境

```bash
# 检查并初始化环境（会自动使用环境变量中的 API Key 配置 qieman-mcp）
bash scripts/fund-cli.sh init
```

初始化脚本会：

1. 检查 mcporter 是否已安装
2. 检查 `QIEMAN_API_KEY` 环境变量是否已配置
3. 自动生成 `~/.mcporter/mcporter.json` 配置文件
4. 测试 MCP 服务连接

## 参考文档

- [MCP工具完整清单](references/mcp-tools-full.md)
- [CSV导入格式规范](references/csv-format.md)
- [项目架构说明](references/REFERENCE.md)
