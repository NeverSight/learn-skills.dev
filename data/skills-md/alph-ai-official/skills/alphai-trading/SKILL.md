---
name: alphai-trading
description: Alph.ai 交易相关 API - 买卖交易（含完整下单参数和响应）、挂单、跟单、订单查询、手续费等。当用户询问下单、买币、卖币、交易、挂单、跟单、订单相关问题时使用。
argument-hint: [查询内容/功能名称]
allowed-tools: Bash(python *), Bash(pip install requests)
---

# Alph.ai 交易模块 API

本模块包含 **54 个交易相关 API**，涵盖：
- 特殊手续费 (8个)
- 用户买单/卖单设置 (21个)
- 挂单服务与查询 (7个)
- 下单服务 (3个)
- 订单查询 (5个)
- 跟单服务与查询 (9个)
- 交易统计数据 (1个)

---

## 核心接口：下单（重要）

### 请求

```
POST https://b.alph.ai/smart-web-gateway/order/create
Content-Type: application/json;charset=UTF-8
Cookie: dex_cookie=<your_dex_cookie>
```

### 请求参数

```json
{
    "chain": "bsc",
    "buyCoin": "黑马",
    "buyContract": "0x360a6f80f92985506e1ba485e2f63ad46cfb4444",
    "sellCoin": "bnb",
    "sellContract": "BNB",
    "slippage": 0.275,
    "clientOrderId": "persistent-1772014659641-xkoyxab",
    "priorityFee": 0.2,
    "antiMev": true,
    "sniper": false,
    "source": "web",
    "side": "BUY",
    "type": "MARKET",
    "volume": "0.001",
    "waitTime": 10
}
```

**字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `chain` | string | 是 | 链名称：`sol`、`bsc`、`eth` 等 |
| `side` | string | 是 | 方向：`BUY` 买入 / `SELL` 卖出 |
| `type` | string | 是 | 订单类型：`MARKET` 市价 |
| `buyCoin` | string | 是 | 买入币种名称 |
| `buyContract` | string | 是 | 买入币种合约地址 |
| `sellCoin` | string | 是 | 卖出币种名称（如 `bnb`、`sol`、`eth`） |
| `sellContract` | string | 是 | 卖出币种合约地址（主链币用大写如 `BNB`、`SOL`） |
| `volume` | string | 是 | 交易量（卖出币种的数量） |
| `slippage` | number | 是 | 滑点容忍度（0.275 = 27.5%） |
| `priorityFee` | number | 否 | 优先费（加速交易，单位为链原生币） |
| `antiMev` | boolean | 否 | 是否开启防 MEV 攻击（防夹子） |
| `sniper` | boolean | 否 | 是否狙击模式 |
| `clientOrderId` | string | 否 | 客户端自定义订单ID（用于幂等去重） |
| `source` | string | 否 | 来源标识（如 `web`、`bot`、`api`） |
| `waitTime` | number | 否 | 等待时间（秒），超时取消 |

### 响应

```json
{
    "code": "200",
    "data": {
        "code": 200,
        "orderId": 781328037879316480,
        "clientOrderId": "persistent-1772014659641-xkoyxab",
        "success": true,
        "orderVo": {
            "id": 48835,
            "clientOrderId": "persistent-1772014659641-xkoyxab",
            "chain": "bsc",
            "uid": 67932,
            "orderId": 781328037879316480,
            "sellCoin": "bnb",
            "sellContract": "BNB",
            "buyCoin": "黑马",
            "buyContract": "0x360a6f80f92985506e1ba485e2f63ad46cfb4444",
            "sellVolume": 0.001,
            "buyVolume": 16710.320347955,
            "price": 0.0000000598432573,
            "slippage": 0.275,
            "priorityFee": 0.2,
            "antiMev": true,
            "platformFeeRate": 0.01,
            "platformFee": 0.00001,
            "platformFeeCoin": "",
            "platformContract": "BNB",
            "gasFee": 0.0000508044,
            "gasFeeCoin": "bnb",
            "antiMevFee": 0,
            "antiMevFeeCoin": "",
            "bribeFee": 0,
            "hash": "0x9165d5449fe250bf2335fb661cc8a5bf54c0807db591bf271c42104c0895d006",
            "source": "web"
        }
    }
}
```

**响应关键字段：**

| 字段 | 说明 |
|------|------|
| `data.success` | 下单是否成功 |
| `data.orderId` | 订单ID |
| `data.orderVo.hash` | 链上交易哈希（可用于区块浏览器查询） |
| `data.orderVo.price` | 实际成交价格 |
| `data.orderVo.buyVolume` | 实际买入数量 |
| `data.orderVo.sellVolume` | 实际卖出数量 |
| `data.orderVo.platformFee` | 平台手续费 |
| `data.orderVo.platformFeeRate` | 平台手续费率（0.01 = 1%） |
| `data.orderVo.gasFee` | Gas 费 |
| `data.orderVo.gasFeeCoin` | Gas 费币种 |
| `data.orderVo.antiMevFee` | 防 MEV 费用 |
| `data.orderVo.bribeFee` | 贿赂费（矿工小费） |

### 买入/卖出的区别

**买入（BUY）**：用主链币买入代币
```json
{
    "side": "BUY",
    "sellCoin": "bnb",
    "sellContract": "BNB",
    "buyCoin": "代币名",
    "buyContract": "0x合约地址",
    "volume": "0.001"
}
```
- `volume` = 花多少主链币去买（如 0.001 BNB）

**卖出（SELL）**：卖出代币换回主链币
```json
{
    "side": "SELL",
    "sellCoin": "代币名",
    "sellContract": "0x合约地址",
    "buyCoin": "bnb",
    "buyContract": "BNB",
    "volume": "1000"
}
```
- `volume` = 卖出多少代币

### 不同链的主链币

| 链 | sellCoin（买入时） | sellContract |
|----|-------------------|--------------|
| `sol` | `sol` | `SOL` |
| `bsc` | `bnb` | `BNB` |
| `eth` | `eth` | `ETH` |

---

## 代码示例

### Python：市价买入

```python
import requests
import time
import uuid

DEX_COOKIE = "你的dex_cookie值"
BASE_URL = "https://b.alph.ai/smart-web-gateway"

headers = {
    "Cookie": f"dex_cookie={DEX_COOKIE}",
    "Content-Type": "application/json;charset=UTF-8"
}

def buy_token(chain, buy_coin, buy_contract, amount, slippage=0.275):
    """市价买入代币"""
    # 根据链确定主链币
    native = {"sol": ("sol", "SOL"), "bsc": ("bnb", "BNB"), "eth": ("eth", "ETH")}
    sell_coin, sell_contract = native.get(chain, ("sol", "SOL"))

    order = {
        "chain": chain,
        "side": "BUY",
        "type": "MARKET",
        "buyCoin": buy_coin,
        "buyContract": buy_contract,
        "sellCoin": sell_coin,
        "sellContract": sell_contract,
        "volume": str(amount),
        "slippage": slippage,
        "priorityFee": 0.2,
        "antiMev": True,
        "sniper": False,
        "source": "api",
        "clientOrderId": f"api-{int(time.time()*1000)}-{uuid.uuid4().hex[:8]}",
        "waitTime": 10
    }

    resp = requests.post(f"{BASE_URL}/order/create", headers=headers, json=order)
    result = resp.json()

    if result.get("code") == "200" and result.get("data", {}).get("success"):
        vo = result["data"]["orderVo"]
        print(f"✅ 买入成功！")
        print(f"   订单ID: {result['data']['orderId']}")
        print(f"   买入: {vo['buyVolume']} {vo['buyCoin']}")
        print(f"   花费: {vo['sellVolume']} {vo['sellCoin']}")
        print(f"   价格: {vo['price']}")
        print(f"   Gas费: {vo['gasFee']} {vo['gasFeeCoin']}")
        print(f"   手续费: {vo['platformFee']} ({vo['platformFeeRate']*100}%)")
        print(f"   交易哈希: {vo['hash']}")
        return result["data"]
    else:
        print(f"❌ 买入失败: {result}")
        return None

def sell_token(chain, sell_coin, sell_contract, amount, slippage=0.275):
    """市价卖出代币"""
    native = {"sol": ("sol", "SOL"), "bsc": ("bnb", "BNB"), "eth": ("eth", "ETH")}
    buy_coin, buy_contract = native.get(chain, ("sol", "SOL"))

    order = {
        "chain": chain,
        "side": "SELL",
        "type": "MARKET",
        "sellCoin": sell_coin,
        "sellContract": sell_contract,
        "buyCoin": buy_coin,
        "buyContract": buy_contract,
        "volume": str(amount),
        "slippage": slippage,
        "priorityFee": 0.2,
        "antiMev": True,
        "sniper": False,
        "source": "api",
        "clientOrderId": f"api-{int(time.time()*1000)}-{uuid.uuid4().hex[:8]}",
        "waitTime": 10
    }

    resp = requests.post(f"{BASE_URL}/order/create", headers=headers, json=order)
    result = resp.json()

    if result.get("code") == "200" and result.get("data", {}).get("success"):
        vo = result["data"]["orderVo"]
        print(f"✅ 卖出成功！")
        print(f"   卖出: {vo['sellVolume']} {vo['sellCoin']}")
        print(f"   获得: {vo['buyVolume']} {vo['buyCoin']}")
        print(f"   交易哈希: {vo['hash']}")
        return result["data"]
    else:
        print(f"❌ 卖出失败: {result}")
        return None


# 使用示例

# 在 BSC 上花 0.001 BNB 买入代币
buy_token(
    chain="bsc",
    buy_coin="黑马",
    buy_contract="0x360a6f80f92985506e1ba485e2f63ad46cfb4444",
    amount=0.001,
    slippage=0.275
)

# 在 SOL 上花 0.1 SOL 买入代币
buy_token(
    chain="sol",
    buy_coin="PEPE",
    buy_contract="合约地址",
    amount=0.1
)

# 卖出代币
sell_token(
    chain="bsc",
    sell_coin="黑马",
    sell_contract="0x360a6f80f92985506e1ba485e2f63ad46cfb4444",
    amount=16710
)
```

### JavaScript：市价买入

```javascript
const DEX_COOKIE = "你的dex_cookie值";

async function buyToken(chain, buyCoin, buyContract, amount, slippage = 0.275) {
    const native = { sol: ["sol", "SOL"], bsc: ["bnb", "BNB"], eth: ["eth", "ETH"] };
    const [sellCoin, sellContract] = native[chain] || ["sol", "SOL"];

    const resp = await fetch("https://b.alph.ai/smart-web-gateway/order/create", {
        method: "POST",
        headers: {
            "Cookie": `dex_cookie=${DEX_COOKIE}`,
            "Content-Type": "application/json;charset=UTF-8"
        },
        body: JSON.stringify({
            chain, side: "BUY", type: "MARKET",
            buyCoin, buyContract, sellCoin, sellContract,
            volume: String(amount), slippage,
            priorityFee: 0.2, antiMev: true, sniper: false,
            source: "api",
            clientOrderId: `api-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`,
            waitTime: 10
        })
    });

    const result = await resp.json();
    if (result.code === "200" && result.data?.success) {
        const vo = result.data.orderVo;
        console.log(`✅ 买入成功！`);
        console.log(`   买入: ${vo.buyVolume} ${vo.buyCoin}`);
        console.log(`   花费: ${vo.sellVolume} ${vo.sellCoin}`);
        console.log(`   交易哈希: ${vo.hash}`);
        return result.data;
    } else {
        console.log(`❌ 买入失败:`, result);
        return null;
    }
}

// 使用示例
buyToken("bsc", "黑马", "0x360a6f80f92985506e1ba485e2f63ad46cfb4444", 0.001);
```

---

## 使用方式

### 1. 查询 API
```
查找下单相关的 API
查询挂单接口
我想找跟单的接口
```

### 2. 查看 API 详情
```
显示 /smart-web-gateway/order/create 的详细信息
这个接口需要什么参数？
```

### 3. 生成调用代码
```
生成调用下单接口的 Python 代码
用 JavaScript 调用挂单接口
帮我写一个在 SOL 链上买入代币的脚本
```

## 工作流程

当你询问交易相关问题时，我会：
1. 从 `apis.json` 和本文档中搜索相关 API
2. 展示 API 的路径、方法、参数、响应格式
3. 根据需要生成调用代码示例（含完整的认证和错误处理）
4. 区分买入/卖出场景，正确设置 side 和合约地址
5. 提供交易安全建议（滑点设置、防 MEV 等）

## API 数据来源

按功能分类存储在 `apis/` 目录，按需查阅：

| 功能 | 文件 | 包含 |
|------|------|------|
| 下单与订单 | `apis/order.json` | 下单服务、订单查询、交易统计 (9个) |
| 挂单 | `apis/pending.json` | 挂单服务、挂单查询 (7个) |
| 跟单 | `apis/follow.json` | 跟单服务、跟单查询 (9个) |
| 交易设置 | `apis/settings.json` | 买单设置、卖单设置 (21个) |
| 手续费 | `apis/fee.json` | 特殊手续费 (8个) |

> 查找 API 时请直接读取对应的分类文件，不要读取 apis.json 全量文件。

---

**参数占位符**: $ARGUMENTS
