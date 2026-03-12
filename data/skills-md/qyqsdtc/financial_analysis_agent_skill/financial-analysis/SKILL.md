---
name: financial-analysis
description: 专业的上市公司财务报表分析技能。用于分析PDF格式的财务报告（季报、半年报、年报），提取三大报表数据，计算盈利能力、偿债能力、运营能力、现金流质量、成长性等多维度财务指标，进行杜邦分析和趋势分析，生成投资评级和建议。支持生成Markdown和Excel格式的专业分析报告。当用户请求分析财报、计算ROE/ROA等财务指标、评估公司财务健康状况、生成投资建议时使用此技能。
---

# 财务报表分析技能

专业的上市公司财务报表分析工具，支持：
- 读取PDF财务报告并提取三大报表数据
- 计算30+核心财务指标（盈利、偿债、运营、现金流、成长性、估值）
- **杜邦分析**: ROE三因素分解及驱动因素分析
- **成长性评分**: 收入、利润、资产增长率评估
- **趋势分析**: 多期数据趋势、转折点检测、预警生成
- **增强估值**: PE、PB、PS、EV/EBITDA等指标
- 生成综合评分和投资评级
- 输出Markdown和Excel格式分析报告

## 分析流程

当用户提供财报PDF时，按以下流程执行：

1. **读取PDF** - 使用 PDF 工具读取PDF文件内容
2. **提取数据** - 从文本中识别资产负债表、利润表、现金流量表数据
3. **计算指标** - 使用 `scripts/calculator.py` 计算财务指标
4. **杜邦分析** - 使用 `scripts/dupont_analyzer.py` 分解ROE驱动因素
5. **趋势分析** - 使用 `scripts/trend_analyzer.py` 分析多期数据趋势
6. **深度分析** - 使用 `scripts/financial_analyzer.py` 进行专业分析
7. **生成报告** - 使用 `scripts/report_generator.py` 生成报告

## 核心脚本

### 指标计算器 (`scripts/calculator.py`)

```python
from scripts.calculator import FinancialIndicatorCalculator

calculator = FinancialIndicatorCalculator()

# 基础用法
indicators = calculator.calculate_all_indicators(
    balance_sheet=balance_sheet_data,
    income_statement=income_statement_data,
    cashflow_statement=cashflow_statement_data,
    metadata={'company_name': '公司名称', 'total_shares': 1000000000, 'stock_price': 25.5}
)

# 带成长性分析（需要上期数据）
indicators = calculator.calculate_all_indicators(
    balance_sheet=current_balance_sheet,
    income_statement=current_income_statement,
    cashflow_statement=current_cashflow_statement,
    metadata=metadata,
    previous_balance_sheet=prev_balance_sheet,
    previous_income_statement=prev_income_statement,
    previous_cashflow_statement=prev_cashflow_statement
)

# 获取评分摘要（包含成长性评分）
summary = calculator.get_summary()
# 返回: {'综合评分': 85.5, '盈利能力评分': 90, '偿债能力评分': 80, '成长性评分': 75, ...}
```

### 杜邦分析器 (`scripts/dupont_analyzer.py`)

```python
from scripts.dupont_analyzer import DuPontAnalyzer

dupont = DuPontAnalyzer()

# ROE分解
decomposition = dupont.calculate_dupont_decomposition(balance_sheet, income_statement)
# 返回: net_profit_margin, asset_turnover, equity_multiplier, roe

# ROE质量评估
quality = dupont.evaluate_roe_quality()
# 返回: driver_type, quality, risk_level, sustainability, details

# ROE变动驱动因素分析（对比上期）
driver_analysis = dupont.analyze_roe_drivers(
    current_balance_sheet, current_income_statement,
    previous_balance_sheet, previous_income_statement
)
# 返回: changes, contributions, main_driver, interpretation
```

### 趋势分析器 (`scripts/trend_analyzer.py`)

```python
from scripts.trend_analyzer import MultiPeriodTrendAnalyzer

trend = MultiPeriodTrendAnalyzer()

# 添加多期数据
for period_data in historical_data:
    trend.add_period_data(
        period=period_data['period'],
        balance_sheet=period_data['balance_sheet'],
        income_statement=period_data['income_statement'],
        cashflow_statement=period_data['cashflow_statement'],
        indicators=period_data.get('indicators')
    )

# 分析指标趋势
roe_trend = trend.analyze_metric_trend('profitability.roe')
# 返回: direction, values, turning_points, statistics

# 计算CAGR
revenue_cagr = trend.calculate_cagr('income_statement.operating_revenue')

# 生成预警
alerts = trend.generate_alerts()

# 获取趋势摘要
summary = trend.get_trend_summary()
```

### 财务分析器 (`scripts/financial_analyzer.py`)

```python
from scripts.financial_analyzer import FinancialAnalyzer

analyzer = FinancialAnalyzer()

# 基础财务健康分析
analysis = analyzer.analyze_financial_health(
    company_name="公司名称",
    indicators=indicators,
    report_type="年报",
    report_period="2023-12-31"
)
# 返回: overall_rating, strengths, weaknesses, risks, opportunities, detailed_analysis

# 增强版分析（含杜邦和趋势分析）
analysis = analyzer.analyze_financial_health_enhanced(
    company_name="公司名称",
    indicators=indicators,
    report_type="年报",
    report_period="2023-12-31",
    balance_sheet=balance_sheet,
    income_statement=income_statement,
    previous_balance_sheet=prev_balance_sheet,
    previous_income_statement=prev_income_statement,
    period_data_list=historical_periods  # 多期数据用于趋势分析
)
# 返回: 基础分析 + dupont_analysis + trend_analysis

# 单独执行杜邦分析
dupont_result = analyzer.perform_dupont_analysis(
    balance_sheet, income_statement,
    prev_balance_sheet, prev_income_statement
)

# 单独执行趋势分析
trend_result = analyzer.perform_trend_analysis(period_data_list)

# 生成投资建议
recommendation = analyzer.generate_investment_recommendation(
    analysis=analysis,
    indicators=indicators,
    stock_price=25.8,  # 可选
    target_investor_type="稳健型"
)
# 返回: rating, action, target_price, entry_price, stop_loss, reasons
```

### 报告生成器 (`scripts/report_generator.py`)

```python
from scripts.report_generator import AnalysisReportGenerator

generator = AnalysisReportGenerator()

# Markdown报告（含杜邦和趋势分析）
generator.generate_markdown_report(
    company_name="公司名称",
    report_period="2023-12-31",
    report_type="年报",
    statement_data=data,
    indicators=indicators,
    analysis=analysis,
    recommendation=recommendation,
    output_path="分析报告.md",
    dupont_analysis=dupont_result,  # 可选
    trend_analysis=trend_result     # 可选
)

# Excel报告
generator.generate_excel_report(
    company_name="公司名称",
    report_period="2023-12-31",
    statement_data=data,
    indicators=indicators,
    output_path="财务数据.xlsx"
)
```

## 数据结构

### 资产负债表 (balance_sheet)

```python
{
    'total_assets': 100000000,        # 总资产
    'current_assets': 50000000,       # 流动资产
    'cash_and_equivalents': 20000000, # 货币资金
    'accounts_receivable': 15000000,  # 应收账款
    'inventory': 10000000,            # 存货
    'total_liabilities': 40000000,    # 总负债
    'current_liabilities': 25000000,  # 流动负债
    'accounts_payable': 8000000,      # 应付账款
    'shareholders_equity': 60000000,  # 股东权益
}
```

### 利润表 (income_statement)

```python
{
    'operating_revenue': 80000000,       # 营业收入
    'operating_cost': 50000000,          # 营业成本
    'operating_profit': 25000000,        # 营业利润
    'total_profit': 24000000,            # 利润总额
    'net_profit': 20000000,              # 净利润
    'financial_expenses': 1000000,       # 财务费用
    'depreciation_amortization': 2000000, # 折旧摊销（用于EBITDA）
    'basic_eps': 0.5,                    # 基本每股收益（可选）
}
```

### 现金流量表 (cashflow_statement)

```python
{
    'operating_cashflow': 22000000,   # 经营活动现金流
    'investing_cashflow': -5000000,   # 投资活动现金流
    'financing_cashflow': -3000000,   # 筹资活动现金流
    'net_cashflow': 14000000,         # 现金净增加额
}
```

### 元数据 (metadata)

```python
{
    'company_name': '公司名称',
    'total_shares': 1000000000,  # 总股本
    'stock_price': 25.5,         # 当前股价（用于PE、PB、EV计算）
}
```

## 新增功能说明

### 杜邦分析

ROE三因素分解，帮助理解盈利驱动来源：

- **净利率**: 反映盈利能力（定价权、成本控制）
- **资产周转率**: 反映运营效率（资产使用效率）
- **权益乘数**: 反映财务杠杆（负债水平）

ROE质量评价：
- 高净利率驱动：优质，可持续性高
- 高周转驱动：良好，适合薄利多销模式
- 高杠杆驱动：风险较高，需关注财务风险

### 成长性评分

新增20%权重的成长性维度评分：
- 营业收入增长率 (35分)
- 净利润增长率 (35分)
- 总资产增长率 (15分)
- 股东权益增长率 (15分)

### 增强估值指标

- **PE (市盈率)**: 股价/EPS
- **PB (市净率)**: 股价/BVPS
- **PS (市销率)**: 市值/营业收入
- **EV/EBITDA**: 企业价值/息税折旧摊销前利润
- **EBITDA**: 营业利润 + 财务费用 + 折旧摊销

### 趋势分析与预警

- 多期数据趋势方向识别
- 转折点检测
- CAGR（复合年增长率）计算
- 自动预警生成：
  - 严重：流动比率<0.8、资产负债率>80%
  - 警告：ROE连续下滑、经营现金流为负
  - 注意：现金净利比偏低

## 参考文档

- **详细代码示例**: 见 [references/code-examples.md](references/code-examples.md)
- **评分标准**: 见 [references/scoring-standards.md](references/scoring-standards.md)

## 依赖

```bash
pip install pandas numpy openpyxl matplotlib seaborn openai
```

## 注意事项

1. **数据准确性**: 解析结果依赖PDF质量，建议人工复核关键数据
2. **行业差异**: 不同行业的财务指标标准差异较大，分析时需考虑行业特点
3. **投资风险**: 本工具仅供参考，不构成投资建议
