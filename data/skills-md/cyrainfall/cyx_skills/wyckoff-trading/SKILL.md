---
name: wyckoff-trading
description: 威科夫操盘法交易技能。基于威科夫方法分析股票走势，识别吸筹/派发阶段，判断买卖点（Spring、JAC、UT等信号）。当用户提及股票交易、威科夫、Wyckoff、炒股、股票分析、买入信号、卖出信号时触发此技能。
---

# 威科夫操盘法交易技能

本技能帮助用户基于威科夫方法（Wyckoff Method）分析股票走势，识别市场阶段，判断买卖点。

## 核心能力

1. **数据获取** - 通过 REST API 或 WebSocket 获取实时/历史行情数据
2. **结构识别** - 识别吸筹区（Accumulation）、派发区（Distribution）、震荡区间（Trading Range）
3. **信号判断** - 识别 Spring、JAC、UT、Shakeout 等经典威科夫信号
4. **买卖决策** - 结合九大买入检验给出交易建议

---

## 数据获取模块

> 本技能使用 [Baostock](http://baostock.com/) 库获取A股股票数据

### 安装

```bash
pip install baostock pandas
```

### 数据获取

Baostock 是专为A股设计的开源数据库，无需注册，数据稳定。

```python
import baostock as bs
import pandas as pd

def get_kline_data(stock_code, period='daily', limit=200):
    """获取历史K线数据用于威科夫分析
    
    Args:
        stock_code: 股票代码，如 '300435'（深圳创业板）或 '600519'（上海主板）
        period: 日('daily')/周('weekly')/月('monthly')
        limit: 获取天数
    
    Returns:
        list: K线数据字典列表
    """
    # 转换股票代码格式
    if stock_code.startswith('6'):
        code = f'sh.{stock_code}'
    else:
        code = f'sz.{stock_code}'
    
    # 计算日期范围
    end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    start_date = (pd.Timestamp.now() - pd.Timedelta(days=limit*2)).strftime('%Y-%m-%d')
    
    # 登录获取数据
    bs.login()
    rs = bs.query_history_k_data_plus(
        code,
        'date,code,open,high,low,close,volume,amount,pctChg',
        start_date=start_date,
        end_date=end_date,
        frequency='d'
    )
    
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    
    bs.logout()
    
    if data_list:
        df = pd.DataFrame(data_list, columns=rs.fields)
        df = df.rename(columns={
            'date': 'trade_time', 'open': 'open', 'close': 'close',
            'high': 'high', 'low': 'low', 'volume': 'volume',
            'amount': 'amount', 'pctChg': 'pct_chg'
        })
        # 转换数据类型
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        return df.to_dict('records')
    return []

def get_index_data(index_code='sh.000001', limit=200):
    """获取大盘指数数据
    
    Args:
        index_code: 指数代码，如 'sh.000001'（上证指数）、'sz.399001'（深证成指）
        limit: 获取天数
    """
    end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    start_date = (pd.Timestamp.now() - pd.Timedelta(days=limit*2)).strftime('%Y-%m-%d')
    
    bs.login()
    rs = bs.query_history_k_data_plus(
        index_code,
        'date,code,open,high,low,close,volume,amount,pctChg',
        start_date=start_date,
        end_date=end_date,
        frequency='d'
    )
    
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    
    bs.logout()
    
    if data_list:
        df = pd.DataFrame(data_list, columns=rs.fields)
        return df.to_dict('records')
    return []

def get_stock_basics():
    """获取所有A股股票基本信息"""
    bs.login()
    rs = bs.query_stock_basic()
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    bs.logout()
    return pd.DataFrame(data_list, columns=rs.fields)
```

---

## 威科夫分析框架

### 市场阶段识别

| 阶段 | 特征 | 交易方向 |
|------|------|----------|
| 吸筹 (Accumulation) | 价格低位横盘，成交量萎缩后放大 | 准备买入 |
| 上涨 (Markup) | 趋势向上，成交量配合 | 持有/加仓 |
| 派发 (Distribution) | 价格高位横盘，成交量放大后萎缩 | 准备卖出 |
| 下跌 (Markdown) | 趋势向下，成交量放大 | 观望/做空 |

### 关键概念

- **SC (Selling Climax)** - 恐慌抛售低点，通常伴随巨量
- **BC (Buying Climax)** - 疯狂买入高点，通常伴随巨量
- **AR (Automatic Rally)** - 自动反弹，测试卖压
- **ST (Secondary Test)** - 二次测试，验证支撑/阻力
- **SOS (Sign of Strength)** - 强势信号，放量上涨突破
- **SOW (Sign of Weakness)** - 弱势信号，放量下跌
- **LPS (Last Point of Support)** - 最后支撑点，回调低点
- **UT (Upthrust)** - 上冲回落，测试阻力后下跌
- **UTAD (Upthrust After Distribution)** - 派发后的上冲回落

---

## 威科夫阶段详解

### 吸筹阶段（Accumulation）详细步骤

```
Phase A（初始阶段）
├── SC：恐慌抛售，成交量放大，价格创新低
├── AR：自动反弹，测试卖压
├── ST：二次测试，验证SC支撑
└── 特征：成交量逐渐萎缩

Phase B（建仓阶段）
├── 区间震荡：价格在上轨和SC低点之间波动
├── ST测试：多次测试SC支撑位
├── 缩量回调：每次回调成交量萎缩
└── 特征：波动幅度逐渐收窄

Phase C（测试阶段）
├── Spring：快速下破支撑后迅速收回（核心买入信号）
├── Shakeout：震仓，打压吸筹
└── 特征：出现明显买入信号

Phase D（突破阶段）
├── SOS：放量突破区间上轨（强势信号）
├── 回踩：缩量回落至区间上轨附近
├── LPS：最后的支撑点，回调不破前低
└── 特征：趋势向上确立

Phase E（离开阶段）
├── 价格上涨：离开吸筹区
├── 成交量放大：需求主导
└── 特征：进入上涨趋势
```

### 派发阶段（Distribution）详细步骤

```
Phase A（初始阶段）
├── BC：疯狂买入，成交量放大，价格创新高
├── AR：自动回落，测试买压
├── ST：二次测试，验证BC阻力
└── 特征：成交量开始萎缩

Phase B（派发阶段）
├── 区间震荡：价格在下轨和BC高点之间波动
├── UT：上冲回落，测试阻力
├── UTAD：派发后的上冲回落
└── 特征：波动幅度逐渐收窄

Phase C（派发确认）
├── UT：价格短暂突破区间上轨后回落
├── SOW：弱势信号，放量下跌
└── 特征：跌破区间下沿

Phase D（下跌确认）
├── SOS：放量下跌（假突破后反转）
├── 反弹无力：每次反弹高点降低
└── 特征：趋势向下确立

Phase E（离开阶段）
├── 价格下跌：离开派发区
├── 成交量放大：供应主导
└── 特征：进入下跌趋势
```

---

## 威科夫信号系统详解

### 买入信号详解

#### 1. 弹簧效应 (Spring)

吸筹阶段末期的经典买入信号：

```
判断条件：
1. 背景：价格处于横盘交易区下半部分或支撑位
2. 下破：价格短暂、快速跌破支撑区低点（制造恐慌）
3. 收回：价格迅速被拉回区间内，收盘价站稳支撑之上
4. 成交量：下跌时可能放量（恐慌盘），收回后不再创新低
5. 确认：随后缩量回调得到支撑

验证标准：
- 收盘价必须回到支撑位上方
- 随后3-5天内不再创新低
- 成交量在收回后萎缩
```

#### 2. 跳跃小溪 (JAC - Jump Across the Creek)

突破阻力位后的回踩买入点：

```
判断条件：
1. 识别"小溪"：前期高点形成的水平阻力位
2. 突破：出现长阳线且成交量显著放大（需求吸收所有供应）
3. 回踩：价格缩量回落至突破前的平台附近
4. 确认：回踩时成交量极度萎缩（供应枯竭）
```

#### 3. 震仓 (Shakeout)

与 Spring 类似，但更激进：

```
判断条件：
1. 背景：长期横盘后的吸筹阶段
2. 快速下跌：短期内的急剧下挫，制造"派发"假象
3. 迅速收回：很快拉回并创新高
4. 成交量：下跌时巨量，收回后缩量
```

#### 4. 自动反弹 (AR)

SC之后的反弹测试：

```
判断条件：
1. 背景：SC之后出现
2. 反弹幅度：通常反弹幅度较大
3. 成交量：可能放大
4. 意义：测试卖压强度
```

#### 5. 二次测试 (ST)

验证支撑/阻力的重要信号：

```
判断条件：
1. 背景：AR之后，价格再次测试SC或BC
2. 位置：接近SC低点或BC高点
3. 成交量：应该萎缩（验证支撑/阻力有效）
4. 意义：确认供需关系转变
```

### 强势/弱势信号

#### SOS (Sign of Strength) - 强势信号

```
判断条件：
1. 放量上涨：成交量明显放大
2. 收盘价：收在日内高点或接近高点
3. 背景：出现在回调之后
4. 意义：需求强劲，看涨
```

#### SOW (Sign of Weakness) - 弱势信号

```
判断条件：
1. 放量下跌：成交量明显放大
2. 收盘价：收在日内低点或接近低点
3. 背景：出现在反弹之后
4. 意义：供应强劲，看跌
```

#### LPS (Last Point of Support) - 最后支撑点

```
判断条件：
1. 位置：上涨趋势中的回调低点
2. 成交量：萎缩
3. 不破前低：高于前期低点
4. 意义：可能再次上涨
```

### 卖出信号详解

#### UT (Upthrust)

派发阶段的卖出信号：

```
判断条件：
1. 背景：长期上涨后或高位横盘区间
2. 上冲：价格短暂突破区间上轨或前期高点
3. 回落：价格迅速跌回区间内，收盘价疲软
4. 成交量：突破时可能伴随巨量（主力派发）
5. 确认：后续跌破区间下沿（SOW）→ 卖出或做空
```

#### UTAD (Upthrust After Distribution)

派发完成后的上冲回落：

```
判断条件：
1. 背景：派发区形成后
2. 上冲：价格突破派发区上轨
3. 回落：收盘价收在低位
4. 确认：随后跌破派发区下沿
5. 意义：趋势反转信号
```

#### 派发区特征

- 价格在区间内来回震荡
- 每次上涨的高点逐渐降低（趋势线下降）
- 成交量在高位放大，低位缩量
- 出现 UT 信号后跌破区间下沿

---

## 趋势线分析

### 趋势线绘制原则

```
上涨趋势线：
- 连接两个或以上依次抬高的低点
- 价格应在趋势线上方运行
- 跌破趋势线可能预示回调

下跌趋势线：
- 连接两个或以上依次降低的高点
- 价格应在趋势线下方运行
- 突破趋势线可能预示反转
```

### 趋势线在威科夫中的应用

```
吸筹区趋势线特征：
- 上涨时突破下降趋势线
- 回踩不跌破前期低点
- 趋势线角度逐渐陡峭

派发区趋势线特征：
- 下跌时突破上升趋势线
- 反弹不过前期高点
- 趋势线角度逐渐平缓
```

---

## 量价关系分析

### 成交量确认原则

```
量价配合（健康信号）：
├── 上涨时放量：需求跟进
├── 下跌时缩量：供应枯竭
├── 突破时放量：有效突破
└── 回调时缩量：回调可能结束

量价背离（危险信号）：
├── 上涨时缩量：需求不足
├── 下跌时放量：供应强劲
├── 突破时缩量：假突破
└── 反弹时放量：可能继续下跌
```

### 成交量形态

```
吸筹区成交量特征：
├── 初期：SC时巨量
├── 中期：逐渐萎缩
├── 后期：突破时放量
└── 整体：低位缩量，高位放量

派发区成交量特征：
├── 初期：BC时巨量
├── 中期：高位放大
├── 后期：下跌时放量
└── 整体：高位放量，低位缩量
```

---

## 九大买入检验

在买入前尽可能满足更多检验标准：

1. **趋势检验** - 大盘趋势向上（利用指数数据判断）
2. **相对强势** - 个股强于大盘（RS 线向上）
3. **区间横盘** - 个股正在形成横盘区间（吸筹区）
4. **因果法则** - 区间盘整时间足够长
5. **最终震仓** - 出现了 Spring 或震仓洗盘
6. **转强信号** - 出现了放量上涨的 SOS
7. **最后支撑** - 出现了缩量回调的 LPS
8. **无利空** - 市场无突发重大利空
9. **大盘同步** - 大盘指数也处于吸筹或上涨初期

每满足一个检验，买入胜率提高。

---

## 风险管理

### 止损设置

- **Spring 买入**：止损放在 Spring 低点下方
- **JAC 买入**：止损放在"小溪"（阻力位）下方
- **UT 卖出**：止损放在 UT 高点上方

### 仓位管理

- 满足 5-6 个买入检验：仓位 30%
- 满足 7-8 个买入检验：仓位 50%
- 满足全部 9 个买入检验：仓位 70%

### 退出策略

- 出现 SOW 信号减仓
- 跌破重要支撑位清仓
- 达到预期收益目标分批卖出

---

## 输出格式

分析完成后，按以下格式输出：

```
## 股票分析报告：[股票代码]

### 一、市场阶段判断
- 当前阶段：吸筹/上涨/派发/下跌
- 置信度：高/中/低

### 二、关键信号
[列出识别到的信号及日期]

### 三、买入/卖出建议
- 信号类型：Spring / JAC / UT / ...
- 入场价：XXX
- 止损价：XXX
- 止盈价：XXX
- 仓位建议：X%

### 四、九大检验结果
1. 趋势检验：✓/✗
2. 相对强势：✓/✗
...

### 五、风险提示
[说明当前风险]
```

---

## 注意事项

1. **数据优先** - 威科夫分析基于客观的量价数据，不要依赖主观猜测
2. **顺势而为** - 优先选择与大盘趋势一致的股票
3. **耐心等待** - 好的买入点需要等待，不要频繁交易
4. **严格执行** - 设定止损后必须执行，不要临时调整
5. **持续学习** - 威科夫方法需要大量实践才能熟练掌握
6. **数据来源** - 本技能使用 Baostock 获取数据，支持历史K线分析；实时行情可配合其他接口使用
