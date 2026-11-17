---
name: look-ahead-detection
description: Use when writing or reviewing any strategy code, NAV calculation, position sizing, or backtest engine — detect look-ahead bias at the code level before running backtests
---

# 未来函数检测

## 概述

未来函数检测是在代码层面系统性扫描时间穿越漏洞的流程。它不属于单元测试（那是 constraint-testing），不属于独立审计（那是 bias-audit），而是一种**代码审查方法论**——在代码编写和审查阶段就拦截未来函数，阻止它们进入回测管线。

**核心原则：每一行涉及时间、价格、数据对齐的代码，都必须能回答"在时刻T，这个值已知吗？"**

**违反这个流程的字面规则就是违反其精神。**

## 铁律

```
NO BACKTEST WITHOUT LOOK-AHEAD DETECTION FIRST
NO CODE MERGE WITH UNRESOLVED SEVERE FINDINGS
```

没有通过未来函数检测，不得运行回测。存在未解决的严重发现，不得合并代码。

## 适用范围

此技能应在以下时机触发：

**强制触发：**
- 编写任何涉及时间序列对齐的策略代码时
- 编写资金净值/仓位计算代码时
- 编写因子计算公式时
- 配置回测引擎事件循环时
- 从外部数据源加载数据时
- Code Review 回测相关代码时

**不应跳过的情况：**
- "这只是个简单修改"（单行修改可以引入全局穿越）
- "我用的都是标准库函数"（标准库不知道A股的T+1规则）
- "数据源已经处理好了"（数据源为便利优化，不为时点准确性优化）
- "这个因子不涉及财务数据"（未来函数存在于价格、行业、成分股、停牌等所有维度）

## DETECTION-RED-GREEN-VERIFY 循环

### DETECTION-RED — 扫描已知危险模式

在编写完代码后、运行回测前，系统性地扫描21个维度的危险代码模式（见下方代码模式目录）。记录所有匹配项。

```python
# 示例：扫描财务数据时间错位
grep -n "report_date\|f_ann_date\|report_period" strategy/*.py
# 每个匹配行必须能证明使用的是公告日而非报告期
```

### DETECTION-GREEN — 修复所有严重和重要发现

按严重性分级处理：
- **严重**：立即修复。不要继续。这条管线已受污染。
- **重要**：在运行回测前修复。不要报告任何包含此代码的结果。
- **次要**：记录。合并前修复。

### DETECTION-VERIFY — 验证修复不引入新穿越

每个修复必须通过两个验证：
1. 原危险模式不再出现
2. 修复本身不引入新的时间穿越（例如把 `bfill` 改成 `ffill` 时确认方向正确）

## 严重性分级

| 级别 | 定义 | 示例 | 行动 |
|------|------|------|------|
| **严重** | 因子/净值产生虚假alpha或虚假收益 | 前复权价格含未来除权、随机切分时序数据、全样本StandardScaler | 立即修复，全管线重跑 |
| **重要** | 可能产生有偏结果，方向不确定 | 收盘价当日当成交价、T+0资金复用、行业分类用最新而非时点 | 回测前修复 |
| **次要** | 不影响正确性但影响可审计性 | 交易日历间隙、缺失值静默丢弃、文档未标注时点 | 合并前修复 |

---

# 代码模式目录

以下按**代码操作类型**组织（非按未来函数领域组织），以便在编写和审查代码时直接对照。

## A. 时间戳与日期处理

### A1. 财务数据日期字段

**危险模式：**

```python
# SEVERE — 用报告期作为可用日期
df = load_financials(stock_codes)
df = df[df['report_period'] <= as_of_date]  # report_period 是报告期，不是公告日！

# SEVERE — 用 f_ann_date 代替 ann_date
df['usable_date'] = df['f_ann_date']  # f_ann_date 是报告期结束日

# IMPORTANT — 最新财报用当前日期而非历史公告日
latest = df[df['ann_date'] <= as_of_date].iloc[-1]  # 假设数据已按公告日排序
# 但如果数据按报告期排序，iloc[-1] 可能取到公告日还在未来的报告
```

**安全模式：**

```python
df = load_financials(stock_codes)
# ann_date = 实际公告日期，只有公告日 <= 决策日的数据才可用
df = df[df['ann_date'] <= as_of_date]
# 取公告日最新的那条，不是报告期最新的
latest = df.sort_values('ann_date').groupby('stock_code').last()
```

**扫描命令：**

```bash
grep -nE "report_period|f_ann_date|\breport_date\b" *.py
```

### A2. 分析师预测/一致预期日期

**危险模式：**

```python
# IMPORTANT — 预测数据的 report_date 混同 publish_date
consensus = load_consensus(stock_codes)
consensus = consensus[consensus['report_date'] <= as_of_date]  # 应该是 publish_date
```

**安全模式：**

```python
consensus = load_consensus(stock_codes)
consensus = consensus[consensus['publish_date'] <= as_of_date]
```

### A3. 宏观数据日期

**危险模式：**

```python
# SEVERE — CPI等宏观数据的"统计月份"当成"可得日期"
cpi['date'] = pd.to_datetime(cpi['month'].astype(str) + '-01')
# CPI月度数据通常在次月10号左右才公布！
```

**安全模式：**

```python
cpi = load_macro_data()
cpi['available_date'] = pd.to_datetime(cpi['publish_date'])
cpi = cpi[cpi['available_date'] <= as_of_date]
```

### A4. 公告事件日期（重组/增减持/回购/解禁/大宗交易）

**危险模式：**

```python
# SEVERE — 大宗交易用交易日而非公告日（公告日在T+1）
block_trades = load_block_trades()
block_trades = block_trades[block_trades['trade_date'] <= as_of_date]
# 大宗交易T日发生，T+1公开。应使用T+1

# IMPORTANT — 限售股解禁用解禁日收盘价（事后方知）
unlock = load_unlock_schedule()
unlock_signal = unlock[unlock['unlock_date'] == as_of_date]
# 解禁日市场冲击事前不可知

# IMPORTANT — 增减使用变动日（内幕信息）
insider = load_insider_trades()
insider = insider[insider['change_date'] <= as_of_date]  # change_date 当时不公开
```

**安全模式：**

```python
# 大宗交易用公告日
block_trades = block_trades[block_trades['announce_date'] <= as_of_date]
# 增减持同样用公告日
insider = insider[insider['announce_date'] <= as_of_date]
```

### A5. 另类数据时间戳（新闻/研报/舆情/搜索指数）

**危险模式：**

```python
# SEVERE — 新闻时间戳可能是抓取时间非发布时间
news = load_news()
news = news[news['timestamp'] <= as_of_date]  # timestamp 可能晚于实际发布时间

# IMPORTANT — 研报正式发布日期晚于外发给核心客户的时间
reports = load_analyst_reports()
reports = reports[reports['pub_date'] <= as_of_date]  # 核心客户已提前半天到一天

# IMPORTANT — 盘后社交媒体讨论混入当日信号
social = load_social_media()
social = social[social['post_date'] == as_of_date]
# 盘后讨论包含了当日行情反应→因果倒置
```

**安全模式：**

```python
# 验证时间戳字段含义，使用最早可得时间
# 盘后数据只能用于次日信号
social = load_social_media()
social = social[social['post_date'] < as_of_date]  # 只用前一日的讨论
```

**扫描命令：**

```bash
grep -nE "timestamp.*<=.*as_of|pub_date.*<=.*as_of|post_date.*==.*as_of" *.py
```

---

## B. 价格与复权处理

### B1. 前复权价格

**危险模式：**

```python
# SEVERE — 直接使用数据源的前复权价格（含未来的除权信息）
prices = load_prices(stock_codes, adj='forward')  # 前复权，动态重算！
close = prices['close']

# SEVERE — 用前复权价格算收益率
returns = prices['close'].pct_change()  # 前复权价格含未来除权因子
```

**安全模式：**

```python
# 方案1：用不复权价格 + 显式处理每笔除权事件
prices = load_prices(stock_codes, adj=None)
# 需从除权事件表获取实际除权因子

# 方案2：用固定时点前复权
prices = load_prices_with_fixed_adj(stock_codes, as_of=as_of_date)
# 只使用 as_of_date 之前已知的除权信息

# 方案3（次优但实用）：回测时每个时点用当时可得的前复权
# 即逐日加载数据，而非一次加载全量前复权序列
```

**扫描命令：**

```bash
grep -nE "adj.*forward|前复权|qfq" *.py
```

### B2. 后复权价格

**危险模式：**

```python
# IMPORTANT — 后复权价格算收益包含了未到账的分红再投资
returns = prices_adj_backward['close'].pct_change()
# 后复权假设所有分红即刻再投资——实际分红T+2到T+5才到账
```

**扫描命令：**

```bash
grep -nE "adj.*backward|后复权|hfq" *.py
```

### B3. 收盘价当成交价

**危险模式：**

```python
# IMPORTANT — 信号日用收盘价做成交价
signal = compute_signal(as_of_date)
target_weights = compute_weights(signal)
# 下行以当日收盘价成交
execution_price = prices.loc[as_of_date, 'close']  # 收盘价在收盘前不可知！

# IMPORTANT — 用当日收盘价算目标仓位
total_nav = (positions * prices.loc[as_of_date, 'close']).sum()  # 收盘后才知道
target_value = total_nav * target_weight
```

**安全模式：**

```python
# 日终信号 → 次日开盘价成交；日初信号 → 当日开盘价成交
signal = compute_signal(as_of_date)  # 使用 as_of_date 收盘后可获得的信息
execution_price = prices.loc[next_trading_day, 'open']  # 次日开盘

# 目标仓位基于T-1日收盘已知的市值
total_nav = (positions * prices.loc[prev_trading_day, 'close']).sum()
```

**扫描命令：**

```bash
grep -nE "\.loc\[.*as_of.*close\]|\.at\[.*as_of.*close\]" *.py
```

---

## C. 截面计算与数据变换

### C1. 全样本标准化/归一化

**危险模式：**

```python
# SEVERE — sklearn StandardScaler 全样本 fit
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # fit 用了全样本（含未来）！

# SEVERE — pandas 全样本标准化
df['factor_zscore'] = (df['factor'] - df['factor'].mean()) / df['factor'].std()
# ↑ mean() 和 std() 用了全时间序列（含未来）

# SEVERE — 全样本 Winsorize
from scipy.stats import mstats
df['factor_winsorized'] = mstats.winsorize(df['factor'], limits=[0.01, 0.01])
# ↑ 极值阈值用全样本分布确定
```

**安全模式：**

```python
# 每期截面内标准化
df['factor_zscore'] = df.groupby('trade_date')['factor'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# 或用 expanding window
df['factor_mean'] = df.groupby('stock_code')['factor'].expanding().mean().droplevel(0)
df['factor_std'] = df.groupby('stock_code')['factor'].expanding().std().droplevel(0)
df['factor_zscore'] = (df['factor'] - df['factor_mean']) / df['factor_std']
```

**扫描命令：**

```bash
grep -nE "fit_transform|StandardScaler|MinMaxScaler|\.mean\(\).*\.std\(\)|winsorize" *.py
```

### C2. 行业中性化

**危险模式：**

```python
# SEVERE — 用最新行业分类做中性化
industry = load_industry()  # 默认返回当前行业分类
df['factor_neutral'] = df.groupby(['trade_date', 'industry'])['factor'].transform(
    lambda x: x - x.mean()
)
# ↑ 2018年的股票可能用的是2025年的行业分类
```

**安全模式：**

```python
industry = load_industry(as_of=as_of_date)  # 时点行业分类
# 或者 merge on both stock_code AND trade_date with industry effective date range
```

**扫描命令：**

```bash
grep -nE "industry.*groupby|行业.*中性" *.py
```

### C3. 缺失值填充方向

**危险模式：**

```python
# SEVERE — bfill 用未来值填历史
df['factor_filled'] = df['factor'].fillna(method='bfill')

# IMPORTANT — 全样本均值填充（含未来分布信息）
df['factor_filled'] = df['factor'].fillna(df['factor'].mean())
```

**安全模式：**

```python
# 前向填充（用已知历史填充）
df['factor_filled'] = df.groupby('stock_code')['factor'].fillna(method='ffill')
```

**扫描命令：**

```bash
grep -nE "bfill|backfill|fillna.*mean\(\)|fillna.*median\(\)" *.py
```

### C4. 截面均值/分位数

**危险模式：**

```python
# IMPORTANT — T日盘中用T日全截面均值和分位数
daily_mean = df[df['trade_date'] == as_of_date]['factor'].mean()  # 收盘后才知道
top_20pct = df[df['trade_date'] == as_of_date]['ret'].quantile(0.8)  # 同上
```

**安全模式：**

```python
# T日信号只能用T-1日截面数据
prev_mean = df[df['trade_date'] == prev_trading_day]['factor'].mean()
```

---

## D. 滚动窗口与时序切分

### D1. 滚动窗口边界

**危险模式：**

```python
# IMPORTANT — 滚动窗口中心在信号日之后
df['rolling_factor'] = df.groupby('stock_code')['factor'].rolling(20).mean()
# pd.rolling 默认窗口右对齐——窗口最后一个点是当前行
# 但 rolling(20).shift(0) 的窗口包含当前行及之前19行，不含未来
# 如果实际意图是"过去20天"应显式 shift
df['momentum_20d'] = df.groupby('stock_code')['ret'].rolling(20).mean()
# ↑ 包含当日收益！如果当日收益在信号日不可知→穿越
```

**安全模式：**

```python
# 过去20日动量：不含今日
df['momentum_20d'] = df.groupby('stock_code')['ret'].rolling(20).mean().shift(1)
# 或者
df['momentum_20d'] = df.groupby('stock_code')['ret'].shift(1).rolling(20).mean()
```

**扫描命令：**

```bash
grep -nE "\.rolling\(.*\)\.mean\(\)(?!.*shift)" *.py
```

### D2. 时序数据切分

**危险模式：**

```python
# SEVERE — 随机切分时间序列
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# ↑ 训练集可能包含2023年数据，测试集包含2021年数据！

# SEVERE — K-Fold 应用于时间序列
from sklearn.model_selection import KFold
cv = KFold(n_splits=5, shuffle=True)
```

**安全模式：**

```python
# 严格时序切分
split_date = '2022-12-31'
X_train, X_test = X[X.index <= split_date], X[X.index > split_date]

# 时序交叉验证
from sklearn.model_selection import TimeSeriesSplit
cv = TimeSeriesSplit(n_splits=5)
```

**扫描命令：**

```bash
grep -nE "train_test_split|KFold|ShuffleSplit|StratifiedKFold" *.py
```

### D3. 交叉验证泄露

**危险模式：**

```python
# SEVERE — 在含测试集时段数据上调参
from sklearn.model_selection import GridSearchCV
grid = GridSearchCV(estimator, param_grid, cv=5)
grid.fit(X_all_time, y_all_time)  # 5折中包含来自未来的样本！
best_model = grid.best_estimator_
# 然后在"测试集"上评估→测试集已被调参过程窥探
```

---

## E. 机器学习特有

### E1. 特征工程的全样本穿越

**危险模式：**

```python
# SEVERE — PCA全样本训练
from sklearn.decomposition import PCA
pca = PCA(n_components=10)
X_pca = pca.fit_transform(X)  # 全样本协方差结构含未来信息！

# SEVERE — 特征选择用全样本IC
ic = df.groupby('factor_name').apply(lambda g: g['factor'].corr(g['forward_return']))
selected_factors = ic[ic.abs() > 0.02].index  # 窥探了测试集因子表现
```

**安全模式：**

```python
# PCA在每期截面内做，或者 expanding window
# 特征选择只在训练集上
train_ic = compute_ic(train_data)
selected = select_by_threshold(train_ic, threshold=0.02)
```

### E2. 标签定义的不可交易性

**危险模式：**

```python
# SEVERE — T+N标签忽略中间停牌/涨跌停
df['label'] = df.groupby('stock_code')['close'].shift(-5) / df['close'] - 1
# ↑ 假设T+5日可以自由以收盘价平仓——忽略停牌、涨跌停、退市等
```

**安全模式：**

```python
# 检查T到T+N期间是否可以交易
df['label'] = compute_tradable_forward_return(df, horizon=5)
# 期间有停牌/连续涨跌停→label=np.nan
```

### E3. SMOTE/过采样

**危险模式：**

```python
# IMPORTANT — 全样本SMOTE再切分
from imblearn.over_sampling import SMOTE
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X, y)  # 全样本合成→含未来信息
# 之后再做时序切分→已经污染
```

### E4. 预训练模型

**危险模式：**

```python
# IMPORTANT — 预训练语料时间范围覆盖回测期
from transformers import AutoModel
model = AutoModel.from_pretrained('finbert-zh')  # 训练语料可能含未来文本
```

---

## F. 股票池与成分股

### F1. 幸存者偏差

**危险模式：**

```python
# SEVERE — 用当前上市股票列表倒推
universe = get_listed_stocks()  # 默认只返回当前上市股票
historical_data = load_data(universe, start='2015-01-01', end='2025-12-31')
# ↑ 缺少2015-2025年间退市的股票！

# SEVERE — 数据集导出时刻偏差
# 从数据商导出的"历史全部A股"默认不包含已退市股票
```

**安全模式：**

```python
universe = get_listed_stocks(include_delisted=True, as_of=as_of_date)
```

**扫描命令：**

```bash
grep -nE "get_listed_stocks\(\)|get_all_stocks\(\)|stock_list.*=.*query" *.py
```

### F2. 指数成分股与行业分类

**危险模式：**

```python
# SEVERE — 用当前成分股倒推
idx_members = get_index_members('000300.SH')  # 默认返回最新成分股
# 需要指定 as_of 参数

# SEVERE — 用当前行业分类
industry = get_industry(stock_codes)  # 默认返回最新分类
```

**安全模式：**

```python
idx_members = get_index_members('000300.SH', as_of=as_of_date)
industry = get_industry(stock_codes, as_of=as_of_date)
```

---

## G. A股交易规则

### G1. T+1规则

**危险模式：**

```python
# IMPORTANT — 当日买入当日卖出
trades = generate_trades(signals)
# 处理交易时没有检查持仓是否满1天
portfolio.apply_trades(trades)  # 可能包含同日往返
```

**安全模式：**

```python
# 买入需要T+1日才能卖出
trades = generate_trades(signals)
trades = enforce_t_plus_1(trades, current_positions)
```

### G2. 涨跌停执行

**危险模式：**

```python
# IMPORTANT — 涨停价买入成交、跌停价卖出成交
execution_price = prices.loc[as_of_date, 'close']
# 没有检查涨跌停状态
```

**安全模式：**

```python
limit_status = get_limit_status(as_of_date)
executable = ~limit_status['at_upper']  # 涨停不可买入
```

**扫描命令：**

```bash
grep -nE "at_upper|at_lower|limit_up|limit_down|price_limit" *.py
```

### G3. 停牌处理

**危险模式：**

```python
# IMPORTANT — 停牌股被静默丢弃
df = df[df['volume'] > 0]  # 可能剔除了停牌股
# 停牌股应该在因子中有显式的NaN标记，而非从数据中消失

# IMPORTANT — 停牌期按停牌价估值并累计收益
nav = (positions * prices.loc[as_of_date, 'close']).sum()
# 停牌股价格未变但复牌后可能连续跌停
```

**安全模式：**

```python
suspended = get_suspended_stocks(as_of_date)
df.loc[suspended, 'factor'] = np.nan  # 显式标记
# 停牌股NAV按停牌价冻结，不允许在停牌期间产生"收益"
```

### G4. 整手约束

**危险模式：**

```python
# MINOR — 忽略最小交易单位
target_shares = target_value / execution_price  # 可能是任意小数
```

**安全模式：**

```python
lot_size = 100 if board != '科创板' else 200
target_shares = (target_value // (execution_price * lot_size)) * lot_size
```

### G5. 板块涨跌停限制差异

**危险模式：**

```python
# IMPORTANT — 所有股票统一按10%处理
limit_price = prev_close * 1.10  # 科创/创业板应该是20%
```

**安全模式：**

```python
limit_pct = {'主板': 0.10, '科创板': 0.20, '创业板': 0.20, '北交所': 0.30, 'ST': 0.05}
upper = prev_close * (1 + limit_pct[get_board(stock)])
```

### G6. 交易成本

**危险模式：**

```python
# IMPORTANT — 策略收益不含交易成本
strategy_return = (nav_t1 - nav_t0) / nav_t0  # 无印花税、佣金等
```

**安全模式：**

```python
cost = compute_transaction_cost(trades, stamp_duty_sell=0.0005, commission=0.00025)
strategy_return = (nav_t1 - nav_t0 - cost) / nav_t0
```

---

## H. 资金净值与仓位计算

### H1. 资金交收时间

**危险模式：**

```python
# IMPORTANT — 卖出资金当日复用
cash = cash + sell_proceeds  # T日卖出→T+1资金才到账
target_buy = compute_target_buy_value(signals)
actual_buy = min(cash, target_buy)  # 用未到账的钱买股票
```

**安全模式：**

```python
# A股：卖出资金T日可用（可买入，需T+1才可取出）
available_cash = cash + sell_proceeds  # T日卖出资金可用于T日买入
# 但卖出冻结资金需标记（不能重复使用）
```

### H2. 分红/送转时间

**危险模式：**

```python
# IMPORTANT — 除权日当天持仓即按新股本计算
positions = positions * split_ratio  # 除权日即刻生效
# 实际新增股份T+1才到账

# IMPORTANT — 分红即刻计入可用资金
cash = cash + dividend  # 实际T+2到T+5才到账
```

### H3. 配股/可转债优先配售

**危险模式：**

```python
# IMPORTANT — 配股缴款到上市的时间差被忽略
# 缴款截止日后资金被占用1-2周才到账
subscription_cost = rights_issue_price * eligible_shares
cash = cash - subscription_cost  # 即刻扣除资金但即刻计入新股
positions = positions + rights_issue_new_shares
```

---

## I. 回测引擎配置

### I1. 信号-执行顺序

**危险模式：**

```python
# SEVERE — 回测引擎事件循环顺序错误
class BacktestEngine:
    def next(self):
        bar = self.get_current_bar()          # 1. 获取当前bar（含收盘价）
        signal = self.strategy(bar.close)      # 2. 用收盘价算信号
        self.execute(signal, price=bar.close)  # 3. 以收盘价成交
        # ↑ 信号用收盘价算，执行也在收盘价→双重穿越
```

**安全模式：**

```python
class BacktestEngine:
    def next(self):
        bar = self.get_current_bar()
        signal = self.strategy(self.get_known_data())  # 只用已收盘的已知数据
        next_bar = self.get_next_bar()
        self.execute(signal, price=next_bar.open)  # 次日开盘价成交
```

### I2. VWAP执行模拟

**危险模式：**

```python
# IMPORTANT — 按当日VWAP成交（收盘后才知VWAP）
self.execute(signal, price=bar.vwap)  # bar.vwap在收盘后才知道
```

### I3. 回测框架允许未来bar访问

**危险模式：**

```python
# IMPORTANT — 策略代码访问未来K线
def next(self):
    future_bar = self.datas[0].close[1]  # 访问T+1的收盘价！
    signal = self.compute_signal(future_bar)  # 用未来数据算信号
```

**扫描命令：**

```bash
grep -nE "self\.datas\[.*\]\[[1-9]\]|self\.data\.close\[[1-9]\]|\.iloc\[.*\+[1-9]" *.py
```

---

## J. 跨市场与衍生品

### J1. A股与港股收盘时间差

**危险模式：**

```python
# IMPORTANT — AH股同日收盘价的时间错位
ah_premium = price_A.loc[date, 'close'] / price_H.loc[date, 'close']
# A股15:00收盘，港股16:00——差1小时信息
```

### J2. 汇率基准时点

**危险模式：**

```python
# IMPORTANT — T日官方汇率在T+1日才公布
hk_value_cny = hk_position_value * cny_usd_rate.loc[date]
# 这个"当日"汇率实际T+1日9:15才发布
```

### J3. ETF PCF滞后

**危险模式：**

```python
# SEVERE — T日盘中用T日PCF
pcf = get_pcf(etf_code, date=as_of_date)  # T日PCF在T日收盘后制作，T+1日开盘发布
```

### J4. 期货主力合约切换

**危险模式：**

```python
# IMPORTANT — 事后认定的主力合约切换日
continuous = load_continuous_contract(futures_code)
# 数据商已按事后持仓量交叉日期拼接
```

---

## K. 数据供应商陷阱

### K1. 前复权因子动态更新

```bash
# 验证：同一股票同一日期在不同查询时间的前复权价是否一致
# 如果不一致→数据源实时重算前复权（含未来信息）
```

### K2. 行业分类静默替换

```bash
# 验证：查询2020年某股票的行业分类是否与当前分类一致
# 如果不一致且回测用了默认查询→使用了未来行业分类
```

### K3. 财务数据追溯调整

```bash
# 验证：数据源是否标注了追溯调整
# 如果没有标注→2020年的"调整后"财务数据可能含2022年的会计修正
```

### K4. 预计算因子数据

```bash
# 风险：JoinQuant/RiceQuant等平台的"即用型"因子数据
# 预处理的标准化/去极值/填充方法可能使用全样本信息
# 处理代码不透明→无法审计
```

---

# 检测流程

## 第一步：代码扫描（5分钟）

按以下顺序运行 grep 扫描，记录所有命中：

```bash
# 1. 时间穿越最高危模式
grep -rn "bfill\|backfill" *.py

# 2. 财务数据日期字段
grep -rn "report_period\|f_ann_date\|report_date" *.py

# 3. 前复权价格使用
grep -rn "qfq\|forward.*adj\|前复权" *.py

# 4. 全样本标准化
grep -rn "fit_transform\|StandardScaler\|MinMaxScaler" *.py

# 5. 随机切分时间序列
grep -rn "train_test_split\|KFold\|ShuffleSplit" *.py

# 6. 回测引擎未来bar访问
grep -rn "self\.data.*\[1\]\|\.iloc\[.*\+1" *.py

# 7. 收盘价当成交价
grep -rn "\.loc\[.*date.*close\]\|\.at\[.*date.*close\]" *.py

# 8. 滚动窗口不shift
grep -rn "\.rolling.*\.mean()" *.py

# 9. fillna全样本均值
grep -rn "fillna.*\.mean()\|fillna.*\.median()" *.py

# 10. 板块涨跌停统一处理
grep -rn "1\.10\|0\.10.*limit\|10%\|10\%" *.py
```

## 第二步：人工审查（逐文件）

对每个命中项，回答三个问题：

1. **时间戳**：这个值在决策时刻是否存在于市场上？
2. **数据源**：数据源对该字段做了何种"调整"？这个调整是否引入未来信息？
3. **修复影响**：修改后是否引入新的穿越？

## 第三步：严重性判定与处理

| 发现 | 分级 | 行动 |
|------|------|------|
| 含 `bfill` / `backfill` | **严重** | 立即修复 |
| 前复权价格无 as_of 控制 | **严重** | 立即修复 |
| sklearn 全样本 fit_transform | **严重** | 立即修复 |
| train_test_split 无时序切分 | **严重** | 立即修复 |
| GridSearchCV 在全部数据上 | **严重** | 立即修复 |
| PCA 全样本 fit | **严重** | 立即修复 |
| 全样本 IC 筛选因子 | **严重** | 立即修复 |
| 收盘价当日当日信号+当日成交 | **重要** | 回测前修复 |
| 行业分类无 as_of 参数 | **重要** | 回测前修复 |
| T+1 规则未检查 | **重要** | 回测前修复 |
| 涨跌停未检查 | **重要** | 回测前修复 |
| 停牌股静默丢弃 | **重要** | 回测前修复 |
| 交易成本缺失 | **重要** | 回测前修复 |
| 整手约束忽略 | **次要** | 合并前修复 |
| 交易日历间隙 | **次要** | 合并前修复 |
| 板块涨跌幅统一 | **重要** | 回测前修复 |
| ETF PCF 滞后 | **严重** | 立即修复 |
| 另类数据时间戳未验证 | **重要** | 回测前修复 |

## 第四步：验证修复

对每个修复：

```python
# 方法论：构造一个最小示例，故意引入穿越，确认检测方法能捕获
def test_detection_catches_bfill():
    df = pd.DataFrame({'value': [np.nan, 1.0, 2.0, np.nan, 3.0]})
    # 故意用 bfill
    df['filled'] = df['value'].fillna(method='bfill')
    # 检测代码应能发现此问题
```

---

# 红旗表

| 借口 | 现实 |
|------|------|
| "这个扫描太繁琐了，我就改了一行代码" | 一行 `bfill()` 可以让整个因子失效。扫描是机械的，5分钟的事。 |
| "数据源已经做了时点对齐" | 数据源为便利优化，不为A股时点准确性优化。Wind的前复权每次查询时重算。 |
| "我用的是后复权，没问题" | 后复权假设分红即刻再投资——A股分红T+2到T+5才到账。 |
| "我的因子不涉及财务数据" | 未来函数也存在于行业分类、指数成分、停牌处理、价格复权、涨跌停、另类数据中。 |
| "sklearn 的 StandardScaler 是标准做法" | 在量化回测中，"标准做法"是统计学意义的正确，不是时间序列意义的正确。 |
| "我只是在探索，不需要这么严格" | 探索期引入的穿越会污染整个研究方向。一次"先跑跑看"可以浪费数周工作。 |
| "我的回测框架已经处理了" | 开源回测框架按美股规则设计。检查事件循环源代码。 |
| "这个发现太次要了，先跳过" | 次要发现累积 = 系统性偏差。合并前修复。 |
| "正则表达式太复杂，我手动检查" | 手动检查 = 临时 = 不可复制 = 下次会漏。写进扫描脚本。 |
| "VWAP成交比收盘价成交更保守" | VWAP收盘后才知道——保守的是执行假设，穿越的是信息可得性，两回事。 |
| "这个标签用T+5收益，T+5肯定能平仓" | T到T+5期间可能有停牌、连续涨跌停。检查，不要假设。 |
| "我已经跑完回测了，结果很好，不用回头查" | 回测结果好 = 可能恰好因为未来函数。每次修改后都必须重新扫描。 |

---

# 验证清单

在运行任何回测之前：

- [ ] **A. 时间戳扫描**：财务数据用公告日非报告期 / 宏观数据用发布日期 / 另类数据时间戳已验证
- [ ] **B. 价格复权扫描**：前复权价格有 as_of 控制 / 未混用前后复权 / 收盘价未当日当信号
- [ ] **C. 截面计算扫描**：标准化在截面内或 expanding window / 行业分类用 as_of / 无 bfill / Winsorize 按期
- [ ] **D. 滚动窗口扫描**：rolling 窗口不含未来 / 时序切分严格按时间 / 交叉验证用时序 CV
- [ ] **E. 机器学习扫描**：PCA/降维在截面内 / 特征筛选只在训练集 / 标签检查可交易性 / 无全样本 SMOTE
- [ ] **F. 股票池扫描**：退市股包含 / 指数成分用 as_of / 行业分类用 as_of / IPO排除窗口正确
- [ ] **G. 交易规则扫描**：T+1合规 / 涨跌停检查 / 停牌显式处理 / 板块涨跌幅差异 / 交易成本完整
- [ ] **H. 净值仓位扫描**：资金交收时间正确 / 分红送转到账时滞 / 配股资金占用 / 仓位基于T-1已知信息
- [ ] **I. 回测引擎扫描**：信号-执行顺序正确 / 无VWAP后见之明 / 无未来bar访问 / 交收规则匹配A股
- [ ] **J. 跨市场扫描**：AH收盘时差处理 / 汇率基准时点 / ETF PCF滞后 / 期货主力合约切换
- [ ] **K. 数据源扫描**：前复权动态更新已识别 / 行业分类未静默替换 / 财务追溯调整已标注

无法勾选所有项？你跳过了未来函数检测。从头开始。

**全部通过后**，再运行 constraint-testing 和 bias-audit。三道防线，缺一不可。
