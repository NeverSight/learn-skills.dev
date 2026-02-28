---
name: ali1688-sourcing
description: 1688 工厂与拿货价查询工具。当用户需要在 1688 查找工厂、获取批发价格、寻找供应链资源时使用此 skill。输入产品关键词和特征，输出工厂列表、起批价区间、MOQ 等信息，为核价计算提供成本数据。
---

# 1688 工厂与拿货价查询

## 核心定位

这是跨境电商选品的供应链工具。在 1688 找到核心工厂和起批价，为核价计算提供成本数据。

## 数据来源

1688 网站：
- 主站: `https://www.1688.com`
- 找工厂: `https://gongsi.1688.com`
- 找货源: `https://s.1688.com`

## 输入参数

```json
{
  "keyword": "升降桌 转换器",
  "category": "办公家具",
  "material": "钢木",
  "min_order": 10,
  "price_range": {
    "min": 50,
    "max": 200
  },
  "province": "浙江",
  "certification": ["CE", "FCC"],
  "limit": 20
}
```

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keyword` | string | 是 | - | 搜索关键词 |
| `category` | string | 否 | 全类目 | 商品类目 |
| `material` | string | 否 | 无 | 材质要求 |
| `min_order` | int | 否 | 1 | 最小起订量 |
| `price_range` | object | 否 | 无 | 价格区间（人民币） |
| `province` | string | 否 | 无 | 省份筛选 |
| `certification` | list | 否 | 无 | 认证要求 |
| `limit` | int | 否 | 20 | 返回结果数量 |

## 输出格式

```json
{
  "metadata": {
    "keyword": "升降桌 转换器",
    "search_time": "2026-02-26T10:30:00Z",
    "total_results": 1256,
    "returned_results": 20
  },
  "summary": {
    "lowest_price": 85.00,
    "highest_price": 350.00,
    "average_price": 156.00,
    "median_price": 145.00,
    "price_range": "¥85 - ¥350",
    "main_production_areas": ["浙江安吉", "广东佛山", "江苏苏州"],
    "recommended_starting_price": 120.00
  },
  "wholesale_price": {
    "min_price": 85.00,
    "max_price": 350.00,
    "recommended_price": 120.00,
    "currency": "CNY",
    "unit": "件",
    "note": "建议以 ¥120 作为核价参考价"
  },
  "factories": [
    {
      "rank": 1,
      "company_name": "安吉县XX家具有限公司",
      "company_url": "https://xxx.1688.com",
      "verified": true,
      "verification_type": "深度验厂",
      "location": {
        "province": "浙江",
        "city": "安吉",
        "address": "浙江省湖州市安吉县..."
      },
      "main_products": ["升降桌", "站立桌", "办公桌"],
      "factory_info": {
        "established": "2015",
        "employees": "50-100人",
        "production_capacity": "10000件/月",
        "export_experience": true
      },
      "products": [
        {
          "product_id": "123456789",
          "title": "升降桌转换器 站立式办公桌 可折叠",
          "url": "https://detail.1688.com/offer/123456789.html",
          "image_url": "https://cbu01.alicdn.com/xxx.jpg",
          "price_tiers": [
            {"quantity": "1-9", "price": 145.00},
            {"quantity": "10-49", "price": 125.00},
            {"quantity": "50+", "price": 105.00}
          ],
          "starting_price": 105.00,
          "moq": 10,
          "material": "冷轧钢+环保板材",
          "colors": ["黑色", "白色", "木纹"],
          "size": "80*40*10-50cm",
          "weight": "8.5kg",
          "packaging": "纸箱包装",
          "lead_time": "7-15天",
          "certifications": ["CE", "FCC"],
          "customization": true,
          "sample_available": true,
          "sample_price": 150.00
        }
      ],
      "trade_info": {
        "min_order": 10,
        "payment_terms": ["支付宝", "银行转账"],
        "shipping": "支持物流配送",
        "return_policy": "7天无理由退换"
      },
      "ratings": {
        "overall": 4.8,
        "quality": 4.9,
        "service": 4.7,
        "delivery": 4.8
      },
      "transaction_history": {
        "total_orders": "500+",
        "repeat_buyers": "35%",
        "response_rate": "98%"
      },
      "contact": {
        "contact_person": "王经理",
        "phone": "138****8888",
        "wechat": "xxx8888",
        "online_status": "在线"
      },
      "notes": "安吉家具产业带核心工厂，出口经验丰富，建议优先联系"
    }
  ],
  "sourcing_guide": {
    "recommended_factories": [
      {
        "factory_name": "安吉县XX家具有限公司",
        "reason": "价格合理，质量稳定，出口经验丰富"
      }
    ],
    "negotiation_tips": [
      "起订量 50+ 可谈价格，预计可降 10-15%",
      "长期合作可申请账期",
      "定制包装需额外费用"
    ],
    "quality_checklist": [
      "检查板材环保等级（E0/E1）",
      "确认升降机构质保期",
      "要求提供 CE/FCC 认证证书"
    ],
    "shipping_options": [
      {
        "method": "国内物流",
        "cost": "¥15-30/件",
        "time": "3-5天"
      },
      {
        "method": "快递",
        "cost": "¥50-80/件",
        "time": "1-2天"
      }
    ]
  },
  "price_for_calculator": {
    "ali1688_price": 105.00,
    "currency": "CNY",
    "source": "安吉县XX家具有限公司",
    "moq": 50,
    "note": "50件起批价，用于核价计算"
  }
}
```

## 关键输出字段

### 核价参考价 (price_for_calculator)

这是核价计算的核心输入：

```json
{
  "ali1688_price": 105.00,
  "currency": "CNY"
}
```

### 价格阶梯 (price_tiers)

不同起订量的价格：

```json
[
  {"quantity": "1-9", "price": 145.00},
  {"quantity": "10-49", "price": 125.00},
  {"quantity": "50+", "price": 105.00}
]
```

### 工厂验证状态

| 状态 | 说明 |
|------|------|
| `verified: true` | 已验证工厂 |
| `verification_type: "深度验厂"` | 实地验厂认证 |
| `verification_type: "企业认证"` | 基础企业认证 |

## 主要产业带

根据产品类型，推荐主要产业带：

| 产品类型 | 主要产业带 | 特点 |
|----------|----------|------|
| 办公家具 | 浙江安吉、广东佛山 | 产业集群，价格优势 |
| 小家电 | 广东顺德、浙江慈溪 | 供应链完善 |
| 箱包 | 浙江平湖、广东花都 | 款式多样 |
| 玩具 | 广东澄海、浙江云和 | 出口导向 |
| 纺织品 | 浙江绍兴、江苏南通 | 面料丰富 |
| 五金工具 | 浙江永康、广东东莞 | 品质稳定 |

## 采购员找货指令模板

根据产品特征生成精准找货指令：

```
【采购找货指令】

产品名称：升降桌转换器
关键词：站立式办公桌、升降桌架、可折叠桌架

材质要求：
- 桌面：环保板材（E0/E1级），厚度≥18mm
- 支架：冷轧钢，壁厚≥1.2mm
- 升降机构：气弹簧或电动推杆

功能要求：
- 高度可调节：10-50cm
- 承重：≥15kg
- 稳定性：无明显晃动

认证要求：
- CE 认证（出口欧洲）
- FCC 认证（如有电动部件）

起订量：50件起
目标价格：¥100-120/件（50件起批价）

避坑提示：
1. 注意板材环保等级，避免甲醛超标
2. 确认升降机构质保期（建议≥2年）
3. 检查焊接点是否牢固
4. 要求提供实物样品确认品质

推荐产业带：浙江安吉（办公家具产业集群）
```

## 使用方式

### 方式一：Web 搜索获取

```
搜索词: "site:1688.com 升降桌 转换器 批发"
```

### 方式二：WebFetch 获取

```
URL: https://s.1688.com/selloffer/offer_search.htm?keywords=升降桌+转换器
```

### 方式三：用户手动输入

用户可手动提供 1688 商品信息，skill 进行结构化处理。

## 与其他 Skills 协作

- 接收 `amazon-movers-shakers` 的产品关键词
- 接收 `temu-competitor-search` 的产品特征
- 输出拿货价给 `temu-pricing-calculator`
- 输出供应链信息给 `ecom-product-orchestrator`

## 注意事项

1. **价格真实性**：1688 价格可能虚高，建议实际询价确认

2. **起订量影响**：不同起订量价格差异大，核价时使用实际起订量对应价格

3. **品质差异**：同款产品可能有不同品质等级，需确认具体规格

4. **认证要求**：出口产品需确认认证证书是否齐全

5. **样品确认**：建议先拿样品确认品质再批量采购

## 示例用法

**示例 1：查找工厂和价格**
```
用户：帮我找 "desk mat" 在 1688 上的工厂和价格

执行：
1. 搜索 1688 上的 desk mat 产品
2. 筛选工厂店
3. 提取价格区间和工厂信息
4. 返回结构化结果
```

**示例 2：按产业带筛选**
```
用户：找浙江安吉的升降桌工厂

执行：
1. 搜索升降桌产品
2. 筛选浙江安吉地区
3. 返回当地工厂列表
```

**示例 3：生成采购指令**
```
用户：帮我生成 "standing desk converter" 的采购找货指令

执行：
1. 分析产品特征
2. 确定材质、功能、认证要求
3. 生成标准化采购指令
4. 提供避坑提示
```
