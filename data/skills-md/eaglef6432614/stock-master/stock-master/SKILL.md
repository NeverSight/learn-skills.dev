---
name: stock-master
description: 综合性股票技术分析工具，小白友好。采用混合数据源（Yahoo Finance + Alpha Vantage MCP），提供交互式HTML可视化报告（Lightweight Charts K线图+技术叠加+Swing标注+趋势线+S/R色带）和通俗易懂的分析文字、买卖点建议、Excel持仓管理。支持港股本地计算、ATR动态止损、KDJ随机指标、MACD/RSI背离检测、OBV量能分析、斐波那契支撑阻力位、K线形态识别（锤子线/吞没/十字星）、趋势形态识别（双底/头肩/三角形）。支持TradingView跳转、飞书多维表格同步。当用户请求股票分析、技术指标、交易建议、持仓分析时激活。
---
# Stock Master v4.3 - 小白友好版

面向普通投资者的技术分析工具，用日常语言解释指标，给出明确买卖建议。

> v4.3 更新：大盘数据看板 — 从 Day1 Global 拉取美股+加密市场数据，生成卡片式 HTML 仪表板（市场全景、情绪面板、BTC链上信号、AI分析、Top10新闻）。
> v4.2 更新：图表交互 + 文字分析增强 — 指标 Toggle 开关（默认只显示K线+均线）、评分明细表、小白技术解读卡片、关键价位表、操作建议区、报告结构重排（结论在前图表在后）。
> v4.1: 图表可视化升级 — 图例、Swing 标注、趋势线、S/R色带、布林带填充、PriceLine、趋势徽章。
> v4.0: 交互式 HTML 可视化报告（Lightweight Charts K线图 + MACD/RSI/成交量子图）、TradingView 跳转、评分仪表盘。

## 快速参考

### 数据源策略
| 数据 | 美股 | 港股/A股 |
|------|------|----------|
| 价格 | Yahoo Finance | Yahoo Finance |
| RSI/布林带 | Alpha Vantage MCP | 本地计算 |
| MACD/KDJ/ATR/均线/OBV/形态 | 本地计算 | 本地计算 |

### 指标小白解读

**RSI** (相对强弱):
- <30 超卖 → "大甩卖，可能捡便宜"
- >70 超买 → "被抢购一空，小心回调"

**MACD**:
- 金叉 → "踩油门加速，买入信号"
- 死叉 → "松油门减速，卖出警告"

**KDJ** (随机指标):
- 金叉/J<0 → "绿灯亮了，短期买入"
- 死叉/J>100 → "红灯亮了，短期卖出"

**布林带**:
- 跌破下轨 → "橡皮筋拉太长，可能反弹"
- 突破上轨 → "涨过头了，可能回落"

**背离信号**:
- 底背离 → "价格创新低但动能减弱，反弹信号"
- 顶背离 → "价格创新高但动能减弱，回调信号"

**K线形态** [v3.4]:
- 锤子线/早晨之星/看涨吞没 → 底部反转信号
- 上吊线/黄昏之星/看跌吞没 → 顶部反转信号
- 三只白兵/三只乌鸦 → 强趋势确认

**趋势形态** [v3.4]:
- 双底(W底)/头肩底 → 底部反转，看涨
- 双顶(M头)/头肩顶 → 顶部反转，看跌
- 上升三角形 → 通常向上突破
- 下降三角形 → 通常向下突破

### 异常量价信号 [v3.7 - EvoMap Capsule: Median Anomaly Detection]

基于近 20 个交易日的中位数，用 3 倍阈值检测异常：

| 检测项 | 公式 | 小白解读 |
|--------|------|----------|
| 放量异常 | 当日成交量 > 20日成交量中位数 × 3 | "今天成交量是平时的N倍，有大资金进场" |
| 缩量异常 | 当日成交量 < 20日成交量中位数 × 0.3 | "今天几乎没人交易，市场观望" |
| 波动异常 | 当日涨跌幅 > 20日振幅中位数 × 3 | "今天波动剧烈，是平时的N倍，注意风险" |

**规则**:
- 数据不足 20 日时跳过检测
- 中位数为 0 时跳过该项
- 异常信号在报告中单独标注，不参与评分，仅作提醒

### 交易建议评分 (v3.4)
| 分数 | 建议 | 仓位 |
|------|------|------|
| ≥6 | 强烈买入 | 30% |
| 3-5 | 建议买入 | 20% |
| -2~2 | 观望 | - |
| -3~-5 | 建议卖出 | - |
| ≤-6 | 强烈卖出 | - |

### 形态信号权重 [v3.4]
| 形态类型 | 权重 |
|----------|------|
| 三只白兵/乌鸦、早晨/黄昏之星、头肩、双底双顶 | ±3 |
| 看涨/看跌吞没、上升/下降三角形 | ±2 |
| 锤子线、十字星等单K线形态 | ±1 |

## 使用流程

### 1. 分析单只股票
```
用户: "分析 TSLA" / "看看苹果" / "0700.HK 能买吗"
```

**执行步骤**:
1. 获取 Yahoo Finance 实时价格和历史数据（超时 10s，失败重试 2 次，指数退避 2s/4s）
2. 美股: 调用 Alpha Vantage MCP 获取 RSI/布林带（容错策略见下方）
3. 港股/A股或API失败: 使用 `scripts/indicators.py` 本地计算
4. 计算全部指标 (RSI/MACD/KDJ/OBV/背离/支撑阻力/形态)
5. 异常量价检测（见下方异常信号模块）
6. **[v4.2]** 在 Claude Code 中**完整输出文字分析报告**（`format_detailed_report()` 或 `format_simple_report()`），保证用户在对话中直接看到所有分析内容
7. **[v4.2]** 同时调用 `generate_html_report()` 生成交互式 HTML 报告（自动打开浏览器），将报告链接附在文字回复的末尾
   - 格式示例：`📊 交互式报告已生成：[点击查看](file:///path/to/report.html)`
   - HTML 报告是**补充**，不替代文字输出
   - 失败时不影响文字输出，仅跳过 HTML 生成

**API 容错策略** [v3.7 - EvoMap Capsule: HTTP Retry + Circuit Breaker]:

Alpha Vantage MCP 调用链：
```
调用 → 失败? → 等 2s 重试 1 次 → 仍失败? → 自动降级到本地计算
```
- 识别 429/限流响应：标记当天 Alpha Vantage 已限流，后续分析直接走本地计算，不浪费剩余请求额度
- Yahoo Finance 超时：重试 2 次（间隔 2s → 4s 指数退避），仍失败则报错并说明原因
- 降级时在报告中注明："数据来源：本地计算（API 暂时不可用）"

### 2. 持仓管理
```
用户: "创建持仓表格" / "分析我的持仓" / "更新持仓价格"
```

**默认 Excel 路径**: `/Users/liyanda/Desktop/AI编程/stock master/my_portfolio.xlsx`

### 3. 对比多只股票
```
用户: "对比 AAPL 和 GOOGL" / "这几只哪个好: TSLA, NVDA"
```

**并行分析策略** [v3.7 - EvoMap Capsule: Swarm Task Decomposition]:
- 2 只股票：串行分析即可
- 3 只及以上：使用 Task 工具并行派发子 Agent，每个 Agent 独立分析一只股票，最后汇总对比
- 汇总时统一格式：评分、关键指标、异常信号，生成对比表格

### 4. 飞书同步 [v3.5]
```
用户: "同步分析结果到飞书" / "更新飞书持仓"
```

**飞书多维表格结构**:
| 表名 | 用途 | Table ID |
|------|------|----------|
| 数据表 (技术信号) | 股票分析结果 | tbldtKCoANcpvitS |
| 持仓管理 | 持仓记录 | tblHkx30pGT1QzOq |
| 交易记录 | 买卖历史 | tblTnlPDFmr5gmSV |

**配置文件**: `/Users/liyanda/Desktop/AI编程/stock master/feishu_config.json`

**同步逻辑**: 本地分析 → 飞书（单向，飞书为主库）

**飞书同步容错** [v3.7 - EvoMap Capsule: Format Fallback Chain]:
```
富文本/结构化数据写入 → 失败? → 降级为纯文本表格写入 → 仍失败? → 保存到本地 JSON 备份并报错
```
- 飞书 API 返回 400/格式错误时，自动将 markdown 表格转为纯文本再试
- 连续 3 次失败触发熔断，跳过飞书同步，数据备份到 `feishu_sync_backup.json`
- 在报告中注明同步状态："飞书同步成功" / "飞书暂不可用，数据已本地备份"

### 5. HTML 可视化报告 [v4.0 ~ v4.2]

分析完成后自动生成交互式 HTML 报告并在浏览器中打开。

**报告结构** [v4.2 — 结论在前、图表在后]:
1. 评分仪表盘（-10 到 +10 可视化弧形表盘）+ 一句话结论
2. 买卖建议价格卡片（买入/止损/止盈/风险收益比/仓位）
3. **评分明细表** [v4.2] — 每个指标的信号和得分贡献（从 `signal.score_breakdown` 读取）
4. **小白技术解读** [v4.2] — 卡片网格，每个指标用通俗比喻解释（"踩油门加速"、"弹簧压太紧"）
5. **关键价位表** [v4.2] — 止损/支撑/阻力/目标价格 + 说明
6. **操作建议区** [v4.2] — 根据信号强度给出具体策略步骤
7. **指标 Toggle 工具栏** [v4.2] — 药丸按钮切换图表叠加层（默认只开启均线）
8. K线图 + 均线/布林带/支撑阻力/Swing/趋势线/斐波那契（可切换）
9. 成交量/MACD/RSI 子图 — 联动缩放
10. 风险提示
11. "在 TradingView 中打开" 跳转按钮

**图表 Toggle 开关** [v4.2]:
| 按钮 | 控制内容 | 默认状态 |
|------|----------|----------|
| 均线 | MA5/10/20/60 | 开启 |
| 布林带 | 上轨/下轨/中轨填充 | 关闭 |
| 支撑阻力 | S/R 色带 + PriceLine | 关闭 |
| Swing标注 | 高低点 Marker | 关闭 |
| 趋势线 | 上升/下降趋势线 | 关闭 |
| 斐波那契 | Fib 回撤/扩展 PriceLine | 关闭 |

**报告保存路径**: `~/Desktop/AI编程/stock master/reports/TICKER_YYYYMMDD_HHMM.html`

**技术实现**: `scripts/html_report.py` — HTMLReportGenerator 类
- 使用 TradingView Lightweight Charts v4 (CDN, Apache 2.0 开源)
- 自包含 HTML（内嵌 CSS/JS，CDN 加载图表库）
- 暗色主题，与 TradingView 风格一致
- Canvas overlay 绘制 S/R 色带（跟随缩放重绘）
- 失败时自动回退到 Markdown 输出

**可视化数据源** [v4.1]: `scripts/indicators.py` 新增函数
- `find_swing_points()` — 识别 Swing 高低点坐标
- `calculate_trend_lines()` — 计算上升/下降趋势线 + 通道类型
- `calculate_sr_zones()` — 支撑阻力扩展为 ATR 色带区域

**TradingView 跳转**: 报告中的按钮直链到 `tradingview.com/chart/?symbol=EXCHANGE:TICKER`
- `.HK` → `HKEX:`, `.SS` → `SSE:`, `.SZ` → `SZSE:`, 其他 → 直接使用 ticker

**调用方式**:
```python
from beginner_analyzer import generate_html_report, TradingSignal
# signal = generate_trading_recommendation(...)  # 先生成信号
# stock_data = get_stock_data(ticker, '3mo')      # 原始 OHLCV
path = generate_html_report(ticker, name, analysis_result, signal, stock_data)
# path 为 HTML 文件路径，已自动在浏览器中打开
```

### 6. 大盘数据看板 [v4.3]
```
用户: "大盘数据" / "看看大盘" / "市场看板" / "今日市场"
```

**执行步骤**:
1. 调用 `scripts/market_dashboard.py` 的 `generate_market_dashboard()` 函数
2. 自动从 Day1 Global API 拉取最新市场数据和 AI 分析
3. 生成 HTML 仪表板并在浏览器中打开
4. 在 Claude Code 中输出简要市场摘要

**包含内容**:
- 市场全景（VOO/QQQM/VIX/Gold/BTC/ETH）
- 个股 & 加密行情表（NVDA/TSLA/GOOG/RKLB/CRCL/HOOD/COIN + XAUT/VIRTUAL/HYPE）
- 情绪面板（加密恐慌贪婪指数 + CNN 恐慌贪婪指数）
- BTC 链上信号（周线RSI/成交量/SOPR/长期供应/200周均线）
- AI 核心判断（宏观 + 加密 + 操作建议）
- Top 10 新闻（带分类标签、摘要、操作建议、原文链接）

**报告保存路径**: `~/Desktop/AI编程/stock master/reports/market_dashboard_YYYYMMDD.html`

**调用方式**:
```python
from market_dashboard import generate_market_dashboard
path = generate_market_dashboard()
# path 为 HTML 文件路径，已自动在浏览器中打开
```

**数据来源**: Day1 Global (brief.day1global.xyz) — Finnhub, Yahoo Finance, OKX, CoinGlass, Claude AI
**注意**: 数据源为第三方非公开 API，如不可用会提示错误，不影响其他功能。

## 风险提示（必须包含）

每份报告必须包含:
1. 仅供参考，不构成投资建议
2. 股市有风险，投资需谨慎
3. 建议分批建仓，设置止损

## 投资智慧模块 [v3.6]

用户个人投资感悟汇总，在分析和沟通时可作为智慧佐证。

**核心内容**: [references/investment-wisdom.md](references/investment-wisdom.md)
- 股民的十大境界（从新手到财务自由的成长路径）
- 交易核心原则（止损、仓位管理、交易纪律）
- 技术分析智慧（K线形态、成交量、主力逻辑）
- 心态与纪律（心法、牛熊市智慧、复盘）
- 人生哲学（财富、吃苦、学习、人性）

**使用场景**:
- 给出买卖建议时，引用相关智慧作为佐证
- 用户迷茫或亏损时，引用"十大境界"帮助定位和鼓励
- 讨论心态问题时，引用心态与纪律章节
- 风险提示时，引用风险警示内容

**源文件**: `/Users/liyanda/Desktop/AI编程/stock master/股票交易智慧精粹.docx`
（用户可持续更新此文档，添加新感悟）

## 详细文档

- 投资智慧与哲学: [references/investment-wisdom.md](references/investment-wisdom.md)
- MCP 工具调用: [references/mcp-tools.md](references/mcp-tools.md)
- 脚本详细说明: [references/scripts-guide.md](references/scripts-guide.md)
- 更新日志: [references/changelog.md](references/changelog.md)
