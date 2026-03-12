---
name: tqsdk
description: TianQin SDK (tqsdk) - Python量化交易框架，用于期货/期权/股票交易策略开发、回测与实盘交易
---

# TqSdk 开发指南

TqSdk 是由信易科技开发的开源 Python 量化交易库，基于快期交易及行情服务器体系，支持期货、期权、股票的行情获取、策略开发、回测与实盘交易。

## 何时使用本技能

当用户需要以下内容时触发：
- 使用 TqSdk 编写量化交易策略
- 获取期货/期权/股票实时行情、K线、Tick 数据
- 进行策略回测（支持 Tick 级和 K 线级）
- 配置实盘交易、模拟交易账户
- 使用 TargetPosTask 进行目标持仓交易
- 使用技术指标（ta/tafunc）进行策略分析
- 使用算法交易模块（TWAP/VWAP）
- 调试 TqSdk 异步编程模型相关问题

## 安装

```bash
# 安装/升级
pip install tqsdk -U

# 国内镜像（推荐）
pip install tqsdk -U -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host=pypi.tuna.tsinghua.edu.cn
```

**环境要求：** Python 3, Windows 7+ / macOS / Linux
**注意：** TqSdk 使用 asyncio，部分 IDE（如 Spyder）不支持。推荐使用 VS Code、Cursor、Trae 等支持 asyncio 的 IDE。

## 核心概念

### 编程模型

TqSdk 使用**单线程异步模型**，核心循环为：

```python
from tqsdk import TqApi, TqAuth

api = TqApi(auth=TqAuth("快期账户", "账户密码"))

# 1. 获取数据引用对象
quote = api.get_quote("SHFE.rb2401")
klines = api.get_kline_serial("SHFE.rb2401", 60)

# 2. 在循环中等待数据更新
while True:
    api.wait_update()
    # 3. 使用 is_changing() 判断哪个对象更新了
    if api.is_changing(quote):
        print(f"最新价: {quote.last_price}")
    if api.is_changing(klines):
        print(f"最新K线收盘价: {klines.close.iloc[-1]}")

api.close()
```

**关键要点：**
- `get_quote()`、`get_kline_serial()` 等返回的是**引用对象**，值在 `wait_update()` 时自动更新
- 每个引用对象只需调用一次获取函数
- `wait_update()` 是阻塞函数，收到数据包才返回
- `is_changing()` 判断指定对象在最近一次 `wait_update` 中是否被更新

### 合约代码格式

格式：`交易所代码.合约代码`（大小写敏感）

```python
# 期货合约
"SHFE.cu2401"    # 上期所铜
"DCE.m2401"      # 大商所豆粕
"CZCE.SR401"     # 郑商所白糖（注意：郑商所字母大写，三位数字）
"CFFEX.IF2401"   # 中金所沪深300股指
"INE.sc2401"     # 上期能源原油
"GFEX.si2401"    # 广期所工业硅

# 期权合约
"DCE.m2401-C-3500"     # 大商所豆粕看涨期权
"SHFE.au2404C480"      # 上期所黄金看涨期权
"CFFEX.IO2402-C-4000"  # 中金所沪深300股指期权

# 主连/指数
"KQ.m@CFFEX.IF"  # 中金所IF主连合约
"KQ.i@SHFE.bu"   # 上期所沥青指数

# 外盘
"KQD.m@CBOT.ZS"  # 美黄豆主连

# 跨期组合
"CZCE.SPD SR401&SR403"  # 郑商所跨期
"DCE.SP a2409&a2501"    # 大商所跨期

# 股票（专业版）
"SSE.600000"   # 上交所浦发银行
"SZSE.000001"  # 深交所平安银行
```

## 账户类型

### 模拟交易（免费）

```python
from tqsdk import TqApi, TqAuth

# 临时模拟账户（程序结束后数据丢失）
api = TqApi(auth=TqAuth("快期账户", "账户密码"))

# 指定初始资金的模拟账户
from tqsdk import TqSim
api = TqApi(TqSim(init_balance=100000), auth=TqAuth("快期账户", "账户密码"))
```

### 快期模拟交易（持久化）

```python
from tqsdk import TqApi, TqKq, TqAuth
# 快期模拟账户，数据持久保存，与快期APP互通
api = TqApi(TqKq(), auth=TqAuth("快期账户", "账户密码"))
```

### 实盘交易（专业版）

```python
from tqsdk import TqApi, TqAccount, TqAuth
api = TqApi(TqAccount("H海通期货", "账号", "密码"), auth=TqAuth("快期账户", "账户密码"))
```

### 直连 CTP

```python
from tqsdk import TqApi, TqCtp, TqAuth
api = TqApi(TqCtp("tcp://180.168.xxx:41205", "tcp://180.168.xxx:41205", "账号", "密码"),
            auth=TqAuth("快期账户", "账户密码"))
```

### 多账户

```python
from tqsdk import TqApi, TqMultiAccount, TqAccount, TqSim, TqAuth
api = TqApi(TqMultiAccount([TqAccount("H海通期货", "账号1", "密码1"), TqSim()]),
            auth=TqAuth("快期账户", "账户密码"))
```

## 行情数据

### 实时行情

```python
quote = api.get_quote("SHFE.cu2401")
# 主要字段：
# quote.last_price    最新价
# quote.bid_price1    买一价
# quote.ask_price1    卖一价
# quote.volume        成交量
# quote.open_interest 持仓量
# quote.upper_limit   涨停价
# quote.lower_limit   跌停价
# quote.volume_multiple 合约乘数
# quote.price_tick    最小变动价位
```

### K线数据

```python
# K线周期以秒数表示，最多获取最后 8000 根
klines = api.get_kline_serial("SHFE.cu2401", 60)      # 1分钟线
klines = api.get_kline_serial("SHFE.cu2401", 60*60)   # 1小时线
klines = api.get_kline_serial("SHFE.cu2401", 60*60*24) # 日线
klines = api.get_kline_serial("SHFE.cu2401", 10)       # 10秒线

# klines 是 pandas.DataFrame，包含列：
# datetime, open, high, low, close, volume, open_oi, close_oi

# 常见用法
print(klines.close.iloc[-1])              # 最新K线收盘价
ma = klines.close.rolling(20).mean()      # 20周期均线
print(klines.close.iloc[-3:])             # 最近3根K线收盘价

# 检测新K线
while True:
    api.wait_update()
    if api.is_changing(klines.iloc[-1], "datetime"):
        print("新K线产生")
```

### Tick 数据

```python
ticks = api.get_tick_serial("SHFE.cu2401")
# 返回 pandas.DataFrame，包含 datetime, last_price, volume 等列
```

## 交易操作

### 下单/撤单

```python
# 限价单
order = api.insert_order("SHFE.rb2401", "BUY", "OPEN", volume=3, limit_price=4000)

# 市价单
order = api.insert_order("SHFE.rb2401", "BUY", "OPEN", volume=3)

# 等待成交
while order.status != "FINISHED":
    api.wait_update()

# 撤单
api.cancel_order(order)

# 查看委托单状态
# order.status: ALIVE（活跃）/ FINISHED（完成）
# order.volume_orign: 委托手数
# order.volume_left: 未成交手数
```

### 账户与持仓查询

```python
# 账户资金
account = api.get_account()
print(account.balance)       # 账户权益
print(account.available)     # 可用资金

# 持仓查询
position = api.get_position("SHFE.rb2401")
print(position.pos_long)     # 多头持仓
print(position.pos_short)    # 空头持仓
```

### TargetPosTask 目标持仓

自动管理下单撤单，调整到目标仓位：

```python
from tqsdk import TqApi, TqAuth, TargetPosTask

api = TqApi(auth=TqAuth("快期账户", "账户密码"))
target_pos = TargetPosTask(api, "SHFE.rb2401")

# 设置目标持仓
target_pos.set_target_volume(5)   # 多头5手
target_pos.set_target_volume(-3)  # 空头3手
target_pos.set_target_volume(0)   # 平仓

# 价格模式
target_pos = TargetPosTask(api, "SHFE.rb2401", price="PASSIVE")   # 排队价
target_pos = TargetPosTask(api, "SHFE.rb2401", price="ACTIVE")    # 对手价

# 取消和检查完成状态
target_pos.cancel()
while not target_pos.is_finished():
    api.wait_update()
```

## 策略回测

```python
from datetime import date
from tqsdk import TqApi, TqAuth, TqSim, TqBacktest, BacktestFinished

acc = TqSim(init_balance=1000000)  # 可选：自定义初始资金

try:
    api = TqApi(acc,
                backtest=TqBacktest(start_dt=date(2023, 1, 1), end_dt=date(2023, 12, 31)),
                auth=TqAuth("快期账户", "账户密码"))

    quote = api.get_quote("SHFE.rb2401")
    klines = api.get_kline_serial("SHFE.rb2401", 60*60*24)
    target_pos = TargetPosTask(api, "SHFE.rb2401")

    while True:
        api.wait_update()
        if api.is_changing(klines.iloc[-1], "datetime"):
            ma5 = klines.close.iloc[-6:-1].mean()
            if quote.last_price > ma5:
                target_pos.set_target_volume(1)
            else:
                target_pos.set_target_volume(-1)

except BacktestFinished:
    print(acc.trade_log)    # 交易明细
    print(acc.tqsdk_stat)   # 统计指标
    # tqsdk_stat 包含: init_balance, balance, max_drawdown,
    #   winning_rate, ror, annual_yield, sharpe_ratio 等
    api.close()
```

**回测规则：**
- 撮合规则：对价成交，不会部分成交
- 报单后立即做成交判定
- 支持 Tick 级和 K 线级回测
- 支持股票回测（需使用 `TqSimStock`）
- 主连合约不能直接交易，需用 `quote.underlying_symbol` 获取标的

## 技术指标

### 内置指标 (tqsdk.ta)

```python
from tqsdk.ta import MA, MACD, RSI, BOLL, ATR, KDJ

klines = api.get_kline_serial("SHFE.rb2401", 60*60*24)

# 均线
ma = MA(klines, 20)          # ma.ma 列

# MACD
macd = MACD(klines, 12, 26, 9)  # macd.diff, macd.dea, macd.bar

# 布林带
boll = BOLL(klines, 20, 2)  # boll.mid, boll.top, boll.bottom

# RSI
rsi = RSI(klines, 14)       # rsi.rsi

# KDJ
kdj = KDJ(klines, 9, 3, 3)  # kdj.k, kdj.d, kdj.j

# ATR
atr = ATR(klines, 14)       # atr.atr
```

### 序列计算函数 (tqsdk.tafunc)

```python
from tqsdk import tafunc

ema = tafunc.ema(klines.close, 20)
std = tafunc.std(klines.close, 20)
highest = tafunc.highest(klines.high, 20)
lowest = tafunc.lowest(klines.low, 20)
```

## 算法交易

### TWAP 算法

```python
from tqsdk import TqApi
from tqsdk.algorithm import Twap

api = TqApi(auth="快期账户,用户密码")
target_twap = Twap(api, "SHFE.rb2401", "BUY", "OPEN",
                   volume=500, duration=300,
                   min_volume_each_order=10,
                   max_volume_each_order=25)
while True:
    api.wait_update()
    if target_twap.is_finished():
        break
api.close()
```

### VWAP + TargetPosScheduler

```python
from tqsdk import TqApi, TargetPosScheduler
from tqsdk.algorithm import vwap_table

api = TqApi(auth="快期账户,用户密码")
time_table = vwap_table(api, "CZCE.MA401", target_pos=-100, duration=600)
scheduler = TargetPosScheduler(api, "CZCE.MA401", time_table)

while not scheduler.is_finished():
    api.wait_update()
api.close()
```

## 图形化界面 (Web GUI)

```python
from tqsdk import TqApi, TqAuth

api = TqApi(auth=TqAuth("快期账户", "账户密码"), web_gui=True)
# 或指定端口
api = TqApi(auth=TqAuth("快期账户", "账户密码"), web_gui=":9876")
```

启动后在浏览器访问显示的地址，可以查看 K 线图、持仓、委托单等信息。

## 高级特性

### 多策略运行

每个策略是独立进程，可以同时运行多个策略互不影响：

```python
# strategy_a.py - 策略A
api = TqApi(TqAccount("期货公司", "账号", "密码"), auth=TqAuth("快期账户", "密码"))
# ...策略逻辑...

# strategy_b.py - 策略B（独立文件，独立运行）
api = TqApi(TqAccount("期货公司", "账号", "密码"), auth=TqAuth("快期账户", "密码"))
# ...策略逻辑...
```

### 无人值守运行

```python
import logging
from contextlib import closing

logging.basicConfig(filename='strategy.log', level=logging.INFO)

with closing(TqApi(TqAccount("期货公司", "账号", "密码"),
                   auth=TqAuth("快期账户", "密码"))) as api:
    # 策略代码...
    pass
```

### 钉钉消息推送

```python
import requests
from json import dumps

def send_msg(content):
    webhook = "你的钉钉webhook地址"
    msg = {"msgtype": "text", "text": {"content": f"天勤量化\n{content}"}}
    requests.post(webhook, data=dumps(msg),
                  headers={"content-type": "application/json;charset=utf-8"})
```

### 模拟交易自定义手续费/保证金

```python
sim = TqSim()
api = TqApi(sim, auth=TqAuth("快期账户", "账户密码"))
sim.set_commission("SHFE.cu2401", 50)    # 设置每手手续费
sim.set_margin("SHFE.cu2401", 26000)     # 设置每手保证金
```

## 常见策略模式

### 套利策略（价差交易）

```python
q_near = api.get_quote("SHFE.rb2401")
q_far = api.get_quote("SHFE.rb2405")
t_near = TargetPosTask(api, "SHFE.rb2401")
t_far = TargetPosTask(api, "SHFE.rb2405")

while True:
    api.wait_update()
    spread = q_near.last_price - q_far.last_price
    if spread > 250:
        t_near.set_target_volume(-1)  # 空近月
        t_far.set_target_volume(1)    # 多远月
    elif spread < 200:
        t_near.set_target_volume(0)
        t_far.set_target_volume(0)
```

### 均线策略

```python
klines = api.get_kline_serial("SHFE.rb2401", 60*15, data_length=200)
target_pos = TargetPosTask(api, "SHFE.rb2401")

while True:
    api.wait_update()
    if api.is_changing(klines.iloc[-1], "datetime"):
        ma5 = klines.close.iloc[-6:-1].mean()
        ma20 = klines.close.iloc[-21:-1].mean()
        if ma5 > ma20:
            target_pos.set_target_volume(1)
        else:
            target_pos.set_target_volume(-1)
```

## 核心 API 速查

| 函数 | 说明 |
|------|------|
| `TqApi(account, auth, backtest, web_gui)` | 创建 API 实例 |
| `api.get_quote(symbol)` | 获取实时行情 |
| `api.get_kline_serial(symbol, duration, data_length)` | 获取K线序列 |
| `api.get_tick_serial(symbol, data_length)` | 获取Tick序列 |
| `api.insert_order(symbol, direction, offset, volume, limit_price)` | 下单 |
| `api.cancel_order(order)` | 撤单 |
| `api.get_account()` | 获取账户资金 |
| `api.get_position(symbol)` | 获取持仓 |
| `api.get_order(order_id)` | 获取委托单 |
| `api.get_trade(trade_id)` | 获取成交记录 |
| `api.wait_update(deadline)` | 等待数据更新 |
| `api.is_changing(obj, key)` | 判断对象是否更新 |
| `api.close()` | 关闭连接 |
| `TargetPosTask(api, symbol, price)` | 创建目标持仓任务 |
| `target_pos.set_target_volume(volume)` | 设置目标持仓 |

## 参考文件

本技能包含以下详细参考文档（位于 `references/` 目录）：

### 入门
- **getting_started.md** - TqSdk 介绍、安装、十分钟快速入门

### 使用教程
- **usage_1_策略程序回测.md** - 策略回测、合约行情、历史数据、TqSdk整体结构
- **usage_2_tqsdk_与_vnpy_有哪些差别.md** - 与vn.py/CTP对比、交易辅助工具
- **usage_3_批量回测_参数搜索及其它.md** - 批量回测、策略程序结构、TqBacktest
- **usage_4_在_trae_中高效学习和使用_tqsdk.md** - Trae集成、账户与交易、期权基本使用
- **usage_5_在_cursor_中高效学习和使用_tqsdk_p1/p2.md** - Cursor集成、快期账户、多策略手册
- **usage_6_策略程序图形化界面.md** - Web GUI 界面

### API 参考
- **api_ref_1_*.md** - 算法模块(TWAP)、TargetPosTask高级功能、无人值守运行
- **api_ref_2_*.md** - TqSim模拟交易、TqMultiAccount多账户、紧急停止方案
- **api_ref_3_*.md** - tafunc序列计算函数
- **api_ref_4_*.md** - 业务对象(objs)、TqRohon、TqJees
- **api_ref_5_*.md** - 交易策略示例
- **api_ref_6_*.md** - TqSdk专业版
- **api_ref_7_*.md** - ta技术指标计算函数
- **api_ref_8_*.md** - TqCtp直连CTP、TqZq、TqYida
- **api_ref_9_*.md** - TqApi框架及核心业务（完整API文档）
- **api_ref_10_*.md** - 版本变更记录
- **api_ref_11_*.md** - 时间维度目标持仓、GUI库协作
- **api_ref_12_*.md** - lib业务工具库、DataDownloader、高级委托
- **api_ref_13_*.md** - risk_rule风控模块、TqKq、算法模块示例
- **api_ref_14_*.md** - EDB数据服务+Coze自然语言投研

### 策略示例（约50个完整策略，来自 shinnytech.com）

**趋势策略 (15个):**
- **strategies_trend_a_p1~p4.md** - TRIX、分形趋势、CMO动量、涡旋指标、Hull均线、Keltner通道、Qstick、Aroon
- **strategies_trend_b_p1.md** - 动量排名、量价趋势(VPT)
- **strategies_trend_b_p2.md** - Aberration布林带、菲阿里四价、自动扶梯
- **strategies_trend_b_p3.md** - Dual Thrust、R-Breaker

**套利策略 (15个):**
- **strategies_arbitrage_p1~p5.md** - 热卷-不锈钢、玻璃-纯碱、白糖-淀粉、PTA产业链、生猪饲料、焦煤-焦炭、MTO甲醇制烯烃、铜铝比价、大豆压榨、裂解价差、股指跨期、Box期权、多期限套利、钢厂利润、多油脂套利

**均值回归与其他策略 (15个):**
- **strategies_other_p1~p5.md** - 卡尔曼滤波配对、距离法配对、Pivot Point、CCI、RSI超买超卖、Z-Score、均值回归、冰山委托、盘口算法、POV成交量比例、随机森林预测、ATR波动率、海龟交易法、VWAP算法、网格交易

需要详细信息时，请查阅对应的参考文件。

## 资源链接

- 官方文档：https://doc.shinnytech.com/tqsdk/latest/
- 快期账户注册：快期官网
- 用户论坛：天勤用户论坛
- 许可证：Apache License 2.0
