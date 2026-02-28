---
name: temu-competitor-search
description: Temu 竞品与卷王价查询工具。当用户需要在 Temu 平台查找竞品、获取最低价格（卷王价）、分析竞争格局时使用此 skill。输入产品关键词，输出竞品列表、最低价、核心卖点摘要，为核价计算提供卷王价数据。
---

# Temu 竞品与卷王价查询

## 核心定位

这是 Temu 选品的竞品分析工具。查找 Temu 上的同类产品，获取"卷王价"（最低竞品价），分析竞争格局和差异化机会。

## 核心概念

**卷王价**：Temu 平台上同类产品的最低售价，是核价计算的关键输入参数。

## 数据来源

Temu 网站：
- 美国: `https://www.temu.com`
- 英国: `https://www.temu.com/uk`
- 欧盟: `https://www.temu.com/eu`

## 输入参数

```json
{
  "keyword": "standing desk converter",
  "category": "Home & Kitchen",
  "site": "us",
  "limit": 20,
  "sort_by": "price_asc",
  "min_rating": 3.5
}
```

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keyword` | string | 是 | - | 搜索关键词 |
| `category` | string | 否 | 全类目 | 商品类目 |
| `site` | string | 否 | us | 站点（us/uk/eu） |
| `limit` | int | 否 | 20 | 返回商品数量 |
| `sort_by` | string | 否 | price_asc | 排序方式 |
| `min_rating` | float | 否 | 无 | 最低评分筛选 |

## 排序选项

| 值 | 说明 |
|------|------|
| `price_asc` | 价格从低到高（找卷王价） |
| `price_desc` | 价格从高到低 |
| `sales_desc` | 销量从高到低 |
| `rating_desc` | 评分从高到低 |
| `newest` | 最新上架 |

## 输出格式

```json
{
  "metadata": {
    "keyword": "standing desk converter",
    "site": "temu.com (US)",
    "search_time": "2026-02-26T10:30:00Z",
    "total_results": 156,
    "returned_results": 20
  },
  "summary": {
    "lowest_price": 29.99,
    "lowest_price_currency": "USD",
    "highest_price": 189.99,
    "average_price": 67.50,
    "median_price": 55.00,
    "price_range": "$29.99 - $189.99",
    "competition_level": "high",
    "opportunity_score": 6.5
  },
  "king_price": {
    "price": 29.99,
    "currency": "USD",
    "product_id": "temu_123456",
    "title": "Height Adjustable Standing Desk Converter...",
    "image_url": "https://img.temu.com/xxx.jpg",
    "rating": 3.8,
    "review_count": 456,
    "sold_count": "1k+",
    "shipping": "Free shipping",
    "seller": "Factory Direct",
    "notes": "基础款，无品牌，价格最低"
  },
  "competitors": [
    {
      "rank": 1,
      "product_id": "temu_123456",
      "title": "Height Adjustable Standing Desk Converter...",
      "url": "https://www.temu.com/product-123456.html",
      "image_url": "https://img.temu.com/xxx.jpg",
      "price": 29.99,
      "original_price": 59.99,
      "discount": "50% off",
      "rating": 3.8,
      "review_count": 456,
      "sold_count": "1k+",
      "shipping": "Free shipping",
      "seller": {
        "name": "Factory Direct",
        "rating": 4.2,
        "followers": "5k+"
      },
      "specifications": {
        "material": "Steel + MDF",
        "color": "Black",
        "size": "80cm x 40cm"
      },
      "selling_points": [
        "Height adjustable",
        "Easy assembly",
        "Space saving"
      ],
      "differentiation": {
        "is_bundle": false,
        "is_premium": false,
        "is_lightweight": true,
        "quality_level": "budget"
      }
    }
  ],
  "market_insights": {
    "price_distribution": [
      {"range": "$20-40", "count": 45, "percentage": "29%"},
      {"range": "$40-60", "count": 67, "percentage": "43%"},
      {"range": "$60-100", "count": 32, "percentage": "21%"},
      {"range": "$100+", "count": 12, "percentage": "7%"}
    ],
    "common_features": [
      "Height adjustable",
      "Easy assembly",
      "Free shipping"
    ],
    "premium_features": [
      "Electric motor",
      "Memory presets",
      "Cable management"
    ],
    "gap_opportunities": [
      {
        "type": "bundle",
        "description": "桌板+桌腿+支架套装",
        "potential_price": "$49.99",
        "estimated_margin": "35%"
      },
      {
        "type": "premium",
        "description": "实木材质，高端设计感",
        "potential_price": "$89.99",
        "estimated_margin": "45%"
      }
    ]
  },
  "recommendation": {
    "market_status": "红海竞争激烈",
    "suggested_strategy": "bundle",
    "suggested_price_range": "$45-65",
    "notes": "建议做套装组合，避免直接价格竞争"
  }
}
```

## 关键输出字段

### 卷王价 (king_price)

这是核价计算的核心输入：

```json
{
  "price": 29.99,
  "currency": "USD"
}
```

### 竞争程度评估

| 竞争级别 | 竞品数量 | 价格区间 | 建议 |
|----------|----------|----------|------|
| `low` | < 20 | 分散 | 蓝海机会，可进入 |
| `medium` | 20-50 | 中等 | 需差异化策略 |
| `high` | 50-100 | 集中低价 | 红海，需强差异化 |
| `very_high` | > 100 | 极低 | 避免或做高端 |

### 机会评分 (opportunity_score)

综合评分（1-10分），考虑因素：
- 竞争密度
- 价格空间
- 差异化机会
- 市场规模

## 差异化策略识别

根据竞品分析，自动识别适合的差异化策略：

### 1. 组合拳策略 (Bundle)

当检测到以下情况时推荐：
- 单品竞争激烈
- 存在配套产品需求
- 组合后可提升客单价

示例：
```
单品：桌垫 $15
组合：桌垫+鼠标垫+键盘托 $35
```

### 2. 视觉溢价策略 (Premium)

当检测到以下情况时推荐：
- 现有产品品质感差
- 存在高端用户需求
- 材质/设计可升级

示例：
```
现有：塑料材质，基础设计 $20
升级：实木材质，设计感 $50
```

### 3. 极致轻小策略 (Lightweight)

当检测到以下情况时推荐：
- 大件产品运费高
- 存在小件配件需求
- 可拆分销售

示例：
```
大件：站立桌 $100
小件：桌腿配件 $25
```

## 使用方式

### 方式一：Web 搜索获取

```
搜索词: "site:temu.com standing desk converter"
```

### 方式二：WebFetch 获取

```
URL: https://www.temu.com/search_result.html?search_key=standing+desk+converter
```

### 方式三：用户手动输入

用户可手动提供 Temu 竞品信息，skill 进行结构化处理。

## 与其他 Skills 协作

- 接收 `amazon-movers-shakers` 的产品关键词
- 输出卷王价给 `temu-pricing-calculator`
- 输出竞品分析给 `ecom-product-orchestrator`

## 注意事项

1. **价格波动**：Temu 价格变动频繁，建议多次采样取最低值

2. **促销影响**：大促期间价格可能异常低，需关注日常价格

3. **品质差异**：低价产品可能品质较差，差异化产品可适当溢价

4. **数据准确性**：Temu 页面结构可能变化，需定期更新解析逻辑

## 示例用法

**示例 1：查找卷王价**
```
用户：帮我查一下 "desk mat" 在 Temu 上的最低价

执行：
1. 搜索 Temu 上的 desk mat 产品
2. 按价格排序，找到最低价
3. 返回卷王价和产品详情
```

**示例 2：竞争分析**
```
用户：分析 "standing desk" 在 Temu 上的竞争情况

执行：
1. 搜索 Temu 上的 standing desk 产品
2. 分析价格分布、竞品数量
3. 识别差异化机会
4. 返回竞争分析报告
```

**示例 3：批量查询**
```
用户：帮我查这几个产品的 Temu 卷王价：
- desk converter
- monitor stand
- cable management box

执行：
1. 依次搜索每个关键词
2. 提取各自的卷王价
3. 返回批量结果
```
