---
name: amazon-movers-shakers
description: 亚马逊 Movers & Shakers（飙升榜）数据获取工具。当用户需要查找亚马逊近期销量飙升的热门产品、发现爆款趋势、获取飙升榜商品列表时使用此 skill。支持按类目筛选，输出商品基础信息、价格、排名趋势等数据，为 Temu 选品提供市场源头数据。
---

# 亚马逊飙升榜数据获取 (Amazon Movers & Shakers)

## 核心定位

这是跨境电商选品的数据源头工具。从亚马逊 Movers & Shakers 获取近期飙升商品，发现真实需求和市场趋势。

## 数据来源（优先级从高到低）

### 1. 卖家精灵 API（推荐）

卖家精灵是国内领先的亚马逊数据分析平台，提供专业的 API 接口：

- **API 基础地址**: `https://api.sellersprite.com/v1`
- **MCP 接口**: `https://mcp.sellersprite.com`
- **获取 API Key**: https://open.sellersprite.com/pricing/mcp

**优势**：
- 数据准确、稳定
- 包含月销量、月营收等深度数据
- 无反爬风险
- 支持关键词搜索、类目热销榜等

**API 接口**：
| 接口 | 说明 |
|------|------|
| `/traffic/keyword/stat/{marketplace}/{asin}/` | 关键词流量数据 |
| `/product/info/{marketplace}/{asin}/` | 产品详情 |
| `/bestsellers/{marketplace}/{category_id}/` | 类目热销榜 |
| `/search/{marketplace}/` | 产品搜索 |
| `/market/trends/{marketplace}/{category_id}/` | 市场趋势 |

### 2. 真实爬取

Amazon Movers & Shakers 页面：
- 美国: `https://www.amazon.com/Best-Sellers/zgbs`
- 英国: `https://www.amazon.co.uk/Best-Sellers/zgbs`
- 德国: `https://www.amazon.de/Best-Sellers/zgbs`
- 日本: `https://www.amazon.co.jp/Best-Sellers/zgbs`

### 3. Mock 数据（兜底）

当 API 和爬取都失败时，使用预设的 Mock 数据

## 支持的类目

| 类目代码 | 类目名称 | 说明 |
|----------|----------|------|
| `home-garden` | Home & Kitchen | 家居厨房（Loctek 重点） |
| `electronics` | Electronics | 电子产品 |
| `sports` | Sports & Outdoors | 运动户外 |
| `office` | Office Products | 办公用品 |
| `toys` | Toys & Games | 玩具游戏 |
| `health` | Health & Personal Care | 健康个护 |
| `beauty` | Beauty & Personal Care | 美妆个护 |
| `pet-supplies` | Pet Supplies | 宠物用品 |
| `automotive` | Automotive | 汽车用品 |
| `garden` | Patio, Lawn & Garden | 庭院园艺 |

## 输入参数

```json
{
  "site": "amazon.com",
  "category": "home-garden",
  "limit": 20,
  "min_price": 10.0,
  "max_price": 100.0,
  "exclude_brands": ["Amazon Basics"],
  "time_window": "24h"
}
```

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `site` | string | 否 | amazon.com | 亚马逊站点 |
| `category` | string | 否 | 全类目 | 商品类目 |
| `limit` | int | 否 | 20 | 返回商品数量 |
| `min_price` | float | 否 | 无 | 最低价格筛选 |
| `max_price` | float | 否 | 无 | 最高价格筛选 |
| `exclude_brands` | list | 否 | [] | 排除的品牌 |
| `time_window` | string | 否 | 24h | 时间窗口 |

## 输出格式

```json
{
  "metadata": {
    "site": "amazon.com",
    "category": "Home & Kitchen",
    "scrape_time": "2026-02-26T10:30:00Z",
    "total_products": 100,
    "returned_products": 20
  },
  "products": [
    {
      "rank": 1,
      "rank_change": "+256",
      "asins": "B0XXXXXXXXX",
      "title": "Standing Desk Converter, Height Adjustable...",
      "url": "https://www.amazon.com/dp/B0XXXXXXXXX",
      "image_url": "https://m.media-amazon.com/images/I/xxx.jpg",
      "price": "$89.99",
      "price_value": 89.99,
      "currency": "USD",
      "rating": 4.5,
      "review_count": 1256,
      "prime": true,
      "category_path": "Home & Kitchen > Furniture > Home Office Furniture",
      "sellers_info": {
        "seller": "Brand Name",
        "is_amazon": false
      },
      "trend": {
        "direction": "up",
        "momentum": "strong",
        "change_percentage": "+256%"
      },
      "keywords": ["standing desk", "desk converter", "height adjustable"],
      "suitable_for_temu": true,
      "notes": "家居办公类，适合 Temu 上架"
    }
  ]
}
```

## 数据字段说明

| 字段 | 说明 |
|------|------|
| `rank` | 当前飙升榜排名 |
| `rank_change` | 排名变化（如 +256 表示上升 256 位） |
| `asins` | 亚马逊标准识别号 |
| `title` | 商品标题 |
| `price_value` | 价格数值（用于后续计算） |
| `rating` | 平均评分（1-5） |
| `review_count` | 评论数量 |
| `prime` | 是否 Prime 商品 |
| `trend.direction` | 趋势方向（up/down/stable） |
| `trend.momentum` | 动量强度（strong/medium/weak） |
| `suitable_for_temu` | 是否适合 Temu（初步判断） |

## 筛选逻辑

### 自动过滤条件

以下类型产品自动标记为 `suitable_for_temu: false`：

1. **高资质门槛类**
   - 医疗器械（需 FDA 认证）
   - 婴幼儿食品/用品（严格监管）
   - 药品/保健品（需认证）

2. **品牌垄断类**
   - Apple、Samsung 等大品牌配件
   - 有明显品牌保护的商品

3. **价格过低类**
   - 售价 < $5（利润空间不足）

4. **体积过大类**
   - 大型家具、家电（物流成本高）

### 优先推荐条件

以下类型产品优先标记为 `suitable_for_temu: true`：

1. **家居办公类**（Loctek 主营）
   - 站立桌、桌边架
   - 办公收纳、桌垫
   - 人体工学配件

2. **轻小件类**
   - 重量 < 1kg
   - 体积小、运费低

3. **组合套装类**
   - 多件装
   - 配套产品组合

## 使用方式

### 方式一：卖家精灵 API（推荐）

使用卖家精灵 API 获取数据，稳定可靠：

```bash
# 设置环境变量
export SELLERSPRITE_API_KEY="your_api_key"

# 使用卖家精灵 API
python scripts/scrape_amazon.py --source sellersprite --keyword "standing desk" --limit 20

# 或通过命令行传入 API Key
python scripts/scrape_amazon.py --source sellersprite --api-key YOUR_KEY --keyword "desk converter"
```

**卖家精灵 MCP 配置**（Claude Code）：

```json
{
  "mcpServers": {
    "sellersprite": {
      "url": "https://mcp.sellersprite.com/sse",
      "headers": {
        "secret-key": "YOUR_API_KEY"
      }
    }
  }
}
```

### 方式二：真实爬取

当没有 API Key 时，自动尝试爬取：

```bash
python scripts/scrape_amazon.py --source scrape --category home-garden --limit 20
```

### 方式三：Web 搜索获取

当无法直接爬取时，使用 WebSearch 工具：

```
搜索词: "site:amazon.com Movers and Shakers Home Kitchen"
```

### 方式四：WebFetch 获取

直接获取页面内容：

```
URL: https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden
```

### 方式五：用户手动输入

用户可手动提供飙升榜商品信息，skill 进行结构化处理。

### 方式六：Mock 数据（兜底）

强制使用 Mock 数据：

```bash
python scripts/scrape_amazon.py --source mock --category home-garden --limit 10
```

### 自动模式（默认）

自动选择最佳数据源：

```bash
# 自动模式：卖家精灵 API → 真实爬取 → Mock 数据
python scripts/scrape_amazon.py --source auto --keyword "standing desk"
```

## 与其他 Skills 协作

- 输出数据供 `temu-competitor-search` 搜索竞品
- 输出数据供 `ali1688-sourcing` 查找供应链
- 输出数据供 `temu-pricing-calculator` 进行核价

## 注意事项

1. **爬虫限制**：亚马逊有反爬机制，建议：
   - 控制请求频率
   - 使用代理轮换
   - 模拟真实用户行为

2. **数据时效**：飙升榜数据每小时更新，建议定期刷新

3. **价格波动**：促销期间价格可能异常，需关注历史价格

4. **合规风险**：部分产品可能有专利/版权问题，需进一步核查

## 示例用法

**示例 1：获取家居类飙升产品**
```
用户：帮我看看亚马逊家居类最近有什么飙升的产品

执行：
1. 访问亚马逊 Movers & Shakers 家居类页面
2. 提取前 20 个飙升产品
3. 筛选适合 Temu 的产品
4. 返回结构化数据
```

**示例 2：按价格区间筛选**
```
用户：找亚马逊上 $20-$50 之间飙升的办公产品

执行：
1. 获取办公用品类飙升榜
2. 筛选价格在 $20-$50 之间的产品
3. 返回符合条件的商品列表
```

**示例 3：关键词搜索**
```
用户：看看 "standing desk" 在亚马逊上的趋势

执行：
1. 搜索亚马逊上 standing desk 相关产品
2. 分析销量趋势和排名变化
3. 返回热门产品列表
```
