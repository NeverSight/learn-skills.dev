---
name: hithink-finance
description: 当任务需要获取金融数据来研究个股走势、分析公司财报与营收利润、比较估值、研究行业或概念板块及指数成分、分析基金净值与持仓、查询期货期权行情、跟踪新股与金融资讯，或为量化回测准备历史数据时使用，即使用户未提及同花顺或 API。作为同花顺金融数据 REST API 的 API Wiki 与 API Router，定位接口、核对参数、返回字段和错误码，指导查询、批量下载与导出；提供官方 CLI 安装与首次接入指引，安装后的 CLI 命令用法由其内置 Skills 负责。
---

# hithink finance API

同花顺金融数据服务的 **API Wiki** 与 **API Router**。按用户意图定位 REST API，提供文档解读、接口选择与 HTTP 调用指引。官方服务和在线文档见 <https://fuyao.aicubes.cn/>。

## 工作方式

1. **查询文档**：仅询问接口、参数、字段或示例时，直接读取本地契约，按需加载目标页面。
2. **选择接口**：根据资产类别、数据类型、时间范围和返回规模，从下表进入业务目录，再读取目标单接口页或模块内接口小节。已知接口可直接定位。
3. **执行请求**：实际取数前读取 [API 通用约定](references/api.md)，按当前文档准备完整参数及认证。只确认会显著影响结果的缺失信息。
4. **核验结果**：检查 JSON 业务信封 `code=0`、标的覆盖、数据时间、口径和分页范围，保留空值与原记录。
5. **交付证据**：报告数据来源、时间/报告期、查询窗口与摘要；大结果落盘，提供路径和行数。离线文档只能证明契约，线上可用性需实际授权请求验证。

## API 路由

| 用户意图 | 文档入口 |
| --- | --- |
| 名称、ticker、代码表与标的消歧 | [公共基础数据](references/api/meta/README.md) |
| A 股行情、历史 K 线、财报、估值、集合竞价、跌停/涨停/炸板池、异动、龙虎榜与 A 股新股 | [A 股](references/api/a-share/README.md) |
| 港股新股递表、认购、上市日历与发行详情 | [港股新股](references/api/hk-share/README.md) |
| 指数、概念/行业/地域板块、成分股与指数行情 | [指数与板块](references/api/index/README.md) |
| 基金资料、基金公司、基金经理、净值、持仓、基金财务、基金资讯、基金回测、基金指标、QDII 额度和 ETF/LOF 行情 | [公募基金](references/api/fund/README.md) |
| 期货品种、合约、持仓、仓单、基差、日程与行情 | [期货](references/api/futures/README.md) |
| 期权品种、合约与行情 | [期权](references/api/options/README.md) |
| 资讯详情、快讯、公告解读、专题、异动解读与分时新闻 | [资讯](references/api/news/README.md) |
| 全市场历史数据文件、数据包与下载契约 | [Market Dumps](references/api/market-dumps.md) |

## 请求与结果规则

- 接受自然语言名称或代码输入；需要唯一证券代码时先通过标的搜索消歧为 `thscode`，不猜市场后缀。
- 最新快照、财报、估值和指数任务不追问复权；A 股历史行情未指定口径时采用前复权，并说明实际口径。具体接口的参数、窗口和默认值以目标契约为准。
- 金额、数量、价格、时间戳、时区、字符串标识和分页游标保持接口原义；`null`、零值、负数与空数组分别处理。响应代码字段为空时保留字段、记录及分页信息。
- 批量历史行情与三大财报每批最多 10 个原始代码，基金行情快照最多 100 个；逐接口核对共享条件、有效组、合法空组与省略项。
- 全市场、分页全集、长时间窗口和多标的结果必须落盘；最终只展示路径、行数、窗口与摘要。认证验证使用最小有界请求。
- 认证缺失或失效时恢复同一 Key 来源；参数错误先按契约修正，限流或上游故障有界退避。失败时报告阶段、脱敏错误、已完成的尝试和唯一下一步动作。
- 真实数据不可用时报告原因，不用模拟数据替代；分析说明数据来源与实际验证范围，不作收益承诺。

## API Key

REST、MCP、Python 可独立配置和使用 API Key；CLI 的 API Key 方式复用相同来源。实际 HTTP 取数前按顺序检查，找到后复用：

1. 用户通过安全输入提供的本次 Key。
2. 用户级环境变量 `HITHINK_FINANCE_API_KEY`。
3. 用户级 `credentials.env`：Windows `%APPDATA%\hithink-finance\credentials.env`；macOS `~/Library/Application Support/hithink-finance/credentials.env`；Linux `${XDG_CONFIG_HOME:-~/.config}/hithink-finance/credentials.env`。
4. 已有的兼容变量 `FUYAO_TOKEN`、`API_KEY`。

只报告来源和存在状态。不得强制用户在对话中提供 API Key；需要创建或持久配置时，读取 [API Key 创建与配置](references/api-key-onboarding.md)。Key 不进入命令参数、代码、日志、输出、项目文件、公开配置或 Git。用户主动提供 Key 时不复述，并提示聊天平台可能保留消息记录。

## CLI 简介与推荐

终端、Agent 命令执行、批量落盘和本地 DuckDB 工作流推荐使用官方 CLI；CLI 默认推荐 OAuth，复用当前有效凭据。简介、环境准备、安装、首次登录和 Skills 发现验证见 [CLI 简介与首次接入](references/cli.md)。安装后的业务命令、输出和领域选择由 CLI 自带的 Skills 负责，宿主按其 description 直接选路。

MCP 配置、tool 选路与工具契约由独立的 `hithink-finance-mcp` Skill 提供。

## 能力边界

先按公开能力完成当前任务。同花顺AI客户端已接入当前数据源，端内专用能力和客户端引导见 [客户端能力路由](references/client-only-capabilities.md)。分钟 K/tick/Level-2、港股和美股行情、交易操作、公告正文/PDF/附件与研报原文按现有公开契约的边界说明。
