---
name: ctp-api
description: CTP (Comprehensive Transaction Platform) 6.7.8 API documentation for futures and options trading in China. Use this skill for understanding CTP trading interfaces, market data subscription, order execution, position management, and account queries.
---

# CTP 6.7.8 API Skill

CTP（综合交易平台）是中国期货市场最广泛使用的交易接口。本技能涵盖 CTP 6.7.8 版本的完整 API 文档，包括交易接口、行情接口、数据结构和错误处理。

## When to Use This Skill

This skill should be triggered when:
- 使用 CTP API 进行期货/期权交易开发
- 实现行情订阅和数据处理
- 处理订单提交、撤单、查询操作
- 理解 CTP 回调机制和事件处理
- 调试 CTP 连接、登录、交易问题
- 查询账户资金、持仓、成交记录

## Quick Reference

### 核心类

| 类名 | 用途 |
|------|------|
| `CThostFtdcTraderApi` | 交易接口主类，处理订单、查询 |
| `CThostFtdcMdApi` | 行情接口主类，订阅市场数据 |
| `CThostFtdcTraderSpi` | 交易回调接口，接收交易响应 |
| `CThostFtdcMdSpi` | 行情回调接口，接收行情数据 |

### 常用请求方法 (TraderApi)

```cpp
// 登录
ReqUserLogin(CThostFtdcReqUserLoginField *pReqUserLoginField, int nRequestID);

// 报单
ReqOrderInsert(CThostFtdcInputOrderField *pInputOrder, int nRequestID);

// 撤单
ReqOrderAction(CThostFtdcInputOrderActionField *pInputOrderAction, int nRequestID);

// 查询持仓
ReqQryInvestorPosition(CThostFtdcQryInvestorPositionField *pQryInvestorPosition, int nRequestID);

// 查询资金
ReqQryTradingAccount(CThostFtdcQryTradingAccountField *pQryTradingAccount, int nRequestID);
```

### 常用回调方法 (TraderSpi)

```cpp
// 登录响应
OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

// 报单回报
OnRtnOrder(CThostFtdcOrderField *pOrder);

// 成交回报
OnRtnTrade(CThostFtdcTradeField *pTrade);

// 报单错误
OnErrRtnOrderInsert(CThostFtdcInputOrderField *pInputOrder, CThostFtdcRspInfoField *pRspInfo);
```

### 行情接口 (MdApi)

```cpp
// 订阅行情
SubscribeMarketData(char *ppInstrumentID[], int nCount);

// 行情回调
OnRtnDepthMarketData(CThostFtdcDepthMarketDataField *pDepthMarketData);
```

### 关键数据结构

```cpp
// 报单输入
struct CThostFtdcInputOrderField {
    TThostFtdcBrokerIDType BrokerID;          // 经纪公司代码
    TThostFtdcInvestorIDType InvestorID;      // 投资者代码
    TThostFtdcInstrumentIDType InstrumentID;  // 合约代码
    TThostFtdcDirectionType Direction;         // 买卖方向
    TThostFtdcCombOffsetFlagType CombOffsetFlag; // 开平标志
    TThostFtdcVolumeType VolumeTotalOriginal; // 数量
    TThostFtdcPriceType LimitPrice;           // 限价
    // ...
};

// 深度行情
struct CThostFtdcDepthMarketDataField {
    TThostFtdcInstrumentIDType InstrumentID;  // 合约代码
    TThostFtdcPriceType LastPrice;            // 最新价
    TThostFtdcVolumeType Volume;              // 成交量
    TThostFtdcPriceType BidPrice1;            // 买一价
    TThostFtdcVolumeType BidVolume1;          // 买一量
    TThostFtdcPriceType AskPrice1;            // 卖一价
    TThostFtdcVolumeType AskVolume1;          // 卖一量
    // ...
};
```

### 常见错误码

| 错误码 | 含义 |
|--------|------|
| 0 | 成功 |
| 3 | 不合法的登录 |
| 5 | 用户未登录 |
| 13 | 资金不足 |
| 14 | 报单数量不合法 |
| 22 | 合约代码错误 |
| 25 | 平仓量超过持仓量 |
| 30 | CTP未初始化 |
| 31 | 前置不活跃 |

## Reference Files

This skill includes comprehensive documentation in `references/` (52 files, ~1.1MB total):

| 类别 | 文件 | 描述 |
|------|------|------|
| **入门** | `getting_started_*.md` | 入门指南、阅读指引 (3 files) |
| **交易接口** | `trader_api.md` | CThostFtdcTraderApi 类 |
| **行情接口** | `md_api.md` | CThostFtdcMdApi 类 |
| **交易回调** | `trader_spi.md` | CThostFtdcTraderSpi 回调 |
| **行情回调** | `md_spi.md` | CThostFtdcMdSpi 回调 |
| **请求方法** | `requests_*.md` | Req* 方法 (5 files) |
| **回调方法** | `callbacks_*.md` | OnRsp*/OnRtn* (10 files) |
| **交易功能** | `trading_*.md` | 交易相关 (5 files) |
| **行情功能** | `market_data_*.md` | 行情相关 (5 files) |
| **API参考** | `api_reference_*.md` | 完整 API (14 files) |
| **版本记录** | `changelog_*.md` | 更新日志 (4 files) |
| **监管** | `monitoring.md` | 看穿式监管说明 |

## Working with This Skill

### 交易流程

1. **初始化**: `CreateFtdcTraderApi()` 创建 API 实例
2. **注册**: `RegisterSpi()` 注册回调，`RegisterFront()` 注册前置地址
3. **连接**: `Init()` 启动连接，等待 `OnFrontConnected()` 回调
4. **认证**: `ReqAuthenticate()` 客户端认证（看穿式监管）
5. **登录**: `ReqUserLogin()` 用户登录
6. **交易**: 发送报单、查询等请求
7. **释放**: `Release()` 释放资源

### 行情流程

1. **初始化**: `CreateFtdcMdApi()` 创建行情 API
2. **注册**: 注册 Spi 和前置地址
3. **连接**: `Init()` 启动，等待 `OnFrontConnected()`
4. **登录**: `ReqUserLogin()` 登录行情服务器
5. **订阅**: `SubscribeMarketData()` 订阅合约行情
6. **接收**: 通过 `OnRtnDepthMarketData()` 接收行情推送

### 注意事项

- 所有请求都是异步的，通过回调返回结果
- 每个请求需要唯一的 RequestID
- 登录前需要先完成看穿式客户端认证
- 流控限制：每秒最多 1-2 个请求
- 注意处理断线重连逻辑

## Source

- **PDF**: CTP 6.7.8 API接口说明
- **Pages**: 2466
- **Version**: 6.7.8
- **Date**: 2024-12

## Notes

- 本技能从官方 PDF 文档自动提取
- 包含完整的 API 方法、回调、数据结构
- 代码示例为 C++ 风格，Python 绑定方法名相同
- 详细信息请参考 references/ 目录下的分类文档
