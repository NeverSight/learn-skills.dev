---
name: "tushare-complete"
description: "Tushare Pro完整接口库，包含266个数据接口。当用户需要获取任何A股、港股、美股、基金、期货、债券、宏观经济数据时使用。"
---

# Tushare Complete - 完整接口库

Tushare Pro最完整的数据接口库，包含266个数据接口，覆盖A股、港股、美股、基金、期货、债券、宏观经济等所有领域。

## 适用场景

- 需要获取任何金融市场数据
- 量化投资研究
- 财务分析
- 行业研究
- 宏观经济分析
- 资金流向分析
- 两融数据分析

## 接口分类索引

### 一、股票数据 (14个)

| 接口 | 方法 | 说明 |
|------|------|------|
| 股票列表 | pro.stock_basic() | 获取所有股票基本信息 |
| 每日股本（盘前） | pro.daily_basic() | 每日股本变动 |
| 交易日历 | pro.trade_calendar() | 交易日历查询 |
| ST股票列表 | pro.st_stock_list() | ST股票列表 |
| 沪深港通股票列表 | pro.hs_const() | 沪深港通成分股 |

### 二、行情数据 (23个)

| 接口 | 方法 | 说明 |
|------|------|------|
| 历史日线 | pro.daily() | 日线行情数据 |
| 实时日线 | pro.daily_now() | 实时日线 |
| 历史分钟 | pro.stk_mins() | 分钟线数据 |
| 周线行情 | pro.weekly() | 周线数据 |
| 月线行情 | pro.monthly() | 月线数据 |

### 三、财务数据 (10个)

| 接口 | 方法 | 说明 |
|------|------|------|
| 利润表 | pro.income() | 营业收入、净利润 |
| **资产负债表** | pro.balancesheet() | **在建工程、总资产** |
| **现金流量表** | pro.cashflow() | **资本开支、现金流** |
| 财务指标数据 | pro.fina_indicator() | ROE、ROA等 |

**重要字段说明**：

**资产负债表 (balancesheet)**：
- `cip` - 在建工程（重要！）
- `fix_assets` - 固定资产
- `total_assets` - 资产总计

**现金流量表 (cashflow)**：
- `c_pay_acq_const_fiolta` - 购建固定资产、无形资产和其他长期资产支付的现金（资本开支）
- `n_cashflow_act` - 经营活动现金流净额

### 四、宏观经济 (28个)

| 接口 | 方法 | 说明 |
|------|------|------|
| Shibor利率 | pro.shibor() | Shibor利率 |
| LPR贷款基础利率 | pro.lpr() | LPR利率 |
| 国内生产总值（GDP） | pro.gdp() | GDP数据 |
| 居民消费价格指数（CPI） | pro.cpi() | CPI数据 |
| 工业生产者出厂价格指数（PPI） | pro.ppi() | PPI数据 |
| 货币供应量 | pro.m2() | M2数据 |
| 采购经理指数（PMI） | pro.pmi() | PMI数据 |

## 快速开始

### Token配置

```python
import tushare as ts
pro = ts.pro_api('your_token_here')
```

### 常用接口示例

#### 获取股票列表
```python
df = pro.stock_basic(exchange='', list_status='L',
                  fields='ts_code,symbol,name,area,industry,list_date')
```

#### 获取日线行情
```python
df = pro.daily(ts_code='000001.SZ',
             start_date='20240101',
             end_date='20241231')
```

#### 获取资产负债表（含在建工程）
```python
df = pro.balancesheet(ts_code='600000.SH',
                    start_date='20240101',
                    end_date='20241231')
cip_data = df[['ts_code', 'end_date', 'cip', 'fix_assets', 'total_assets']]
```

#### 获取现金流量表（含资本开支）
```python
df = pro.cashflow(ts_code='600000.SH',
                start_date='20240101',
                end_date='20241231')
capex_data = df[['ts_code', 'end_date', 'c_pay_acq_const_fiolta']]
```

#### 获取宏观GDP
```python
df = pro.gdp(start_date='20220101', end_date='20221231')
```

#### 获取CPI
```python
df = pro.cpi(start_date='20220101', end_date='20221231')
```

#### 获取PMI
```python
df = pro.pmi(start_date='20220101', end_date='20221231')
```

#### 获取Shibor
```python
df = pro.shibor(start_date='20240101', end_date='20240131')
```

## 数据质量检验规则

根据规则3，调取100组完整数据后需要检验：

```python
def validate_data_quality(df, required_fields):
    """
    数据质量检验
    
    参数:
        df: DataFrame
        required_fields: 必需字段列表
    
    返回:
        dict: 检验结果
    """
    result = {
        'total_records': len(df),
        'missing_values': {},
        'zero_values': {},
        'valid_records': 0
    }
    
    for field in required_fields:
        missing = df[field].isna().sum()
        zeros = (df[field] == 0).sum()
        result['missing_values'][field] = missing
        result['zero_values'][field] = zeros
    
    result['valid_records'] = len(df.dropna(subset=required_fields))
    
    return result

# 使用示例
required_fields = ['cip', 'c_pay_acq_const_fiolta', 'revenue', 'n_income_attr_p']
quality = validate_data_quality(df, required_fields)
print(quality)
```

## 接口调用频率限制

- 免费用户：每分钟120次
- 积分用户：根据积分等级提升

## 积分要求

部分接口需要特定积分：
- 基础数据：免费
- 财务数据：2000积分
- 高级数据：5000积分

## 参考资源

- Tushare官方文档：https://tushare.pro/document/2
- API测试工具：https://tushare.pro/document/1
- 积分说明：https://tushare.pro/document/1?doc_id=108

---
*最后更新时间：2026-02-02 10:51*