---
name: real-estate-debt-analysis
description: 专业房产债权分析技能，对比安居客中介价格与阿里法拍成交价格，提供投资决策支持
version: 1.0.0
author: yuanqi-ai
license: MIT
tags:
  - real-estate
  - debt-analysis
  - investment
  - auction
  - anjuke
  - alibaba
execution:
  type: script
  script_path: scripts/real_estate_analysis.py
  entry_point: main
# 非业务功能依赖（具体实现由Agent生态提供）
# 1. 网络搜索能力：用于获取安居客和阿里拍卖的价格信息
# 2. 数据处理能力：用于数据清洗和验证
# 3. 报告生成能力：用于生成PDF和HTML报告
dependencies:
  - requests>=2.31.0
  - pandas>=2.2.2
---

# 房产债权分析技能

专业的房产债权分析能力，能够抓取和分析住宅房产的债权信息，对比安居客中介价格和阿里法拍成交价格，为投资决策提供数据支持。

## 能力

### 数据收集
- 从用户提供的表格中提取房产地址信息
- 使用网络搜索工具抓取安居客中介价格
- 使用网络搜索工具抓取阿里法拍成交价格
- 整理债权本金、面积等基础信息

### 数据分析
- 计算安居客估值（均价×面积）
- 计算法拍折扣率（法拍价/评估价）
- 分析价格差异（中介价-法拍价）/中介价
- 评估债权覆盖率（市场价值/债权本金）

### 风险评估
- **法律风险**：产权纠纷、租赁合同等
- **市场风险**：政策变化、市场波动
- **流动性风险**：变现周期、区域差异
- **操作风险**：法拍程序、竞拍风险

### 报告生成
- 创建对比分析表格
- 生成市场分析总结
- 提供投资建议和风险提示
- 输出PDF格式报告

## 使用场景
- 需要分析房产包债权价值时
- 需要对比房产在不同平台的价格表现时
- 需要评估法拍房投资价值时
- 需要生成房产债权分析报告时

## 数据来源
- **安居客**：中介挂牌价格、小区均价
- **阿里拍卖**：法拍起拍价、成交价、评估价
- **幸福里**：二手房成交价格
- **房天下**：房产详细信息、历史价格

## 分析指标

### 价格指标
- `anjuke_average_price`：小区平均挂牌价格
- `anjuke_valuation`：基于均价计算的房产价值
- `auction_starting_price`：阿里拍卖起拍价格
- `auction_transaction_price`：实际成交价格
- `auction_discount_rate`：法拍价与评估价的比率

### 风险指标
- `debt_coverage_ratio`：市场价值/债权本金
- `price_difference_rate`：（中介价-法拍价）/中介价
- `liquidity_score`：基于区域、户型、总价的综合评分
- `investment_value_score`：综合价格、地段、风险的评分

## 投资建议规则

### 优先关注
- 法拍折扣率>30%且地段较好的房产
- 债权覆盖率>100%的优质资产
- 核心区域但价格合理的房产

### 谨慎对待
- 学区房法拍（竞争激烈，容易追高）
- 商住房（政策风险大，流动性差）
- 产权不清或有纠纷的房产

### 长期持有
- 核心区域优质房产
- 地铁沿线、配套完善的房产
- 品质开发商的房产

### 快进快出
- 郊区高折扣法拍房
- 总价较低的小户型
- 短期内有明显升值空间的房产

## 输出格式

### 表格结构
| 序号 | 房产地址 | 债权本金(万元) | 安居客中介价格(元/㎡) | 安居客估值(万元) | 阿里法拍成交价(万元) | 法拍单价(元/㎡) | 法拍折扣率 | 价格差异分析 | 投资建议 |
|------|----------|----------------|----------------------|------------------|----------------------|----------------|------------|--------------|----------|

### 报告章节
1. 债权房产基本信息表
2. 市场分析总结
3. 统计数据分析
4. 关键发现与分析
5. 阿里法拍成交价格分析
6. 价格对比深度分析
7. 风险提示说明
8. 结论与投资建议

### 关键发现与分析
#### 1. 安居客中介价格特点
- **中介费率**: 杭州地区一般为房屋总价的2-3%
- **价格真实性**: 安居客价格多为挂牌价，实际成交价通常有5-10%的议价空间
- **区域差异**: 核心区域（西湖、上城）价格明显高于郊区

#### 2. 阿里法拍成交价格分析
- **平均折扣率**: 70-80%，部分优质资产可达评估价以上
- **热门案例**:
  - 文鼎苑：744万成交，单价约5.09万/㎡，竞争激烈
  - 春江花月：938万成交，较6年前下跌330万
  - 西溪阳光中心：78套商住房7折起拍
- **投资机会**:
  - 海宁启潮府：45-46万起拍，单价约2,900元/㎡
  - 临平蓝庭花园：43万起拍，折扣率44%
  - 富春金秋大道：73万成交，单价约8,600元/㎡

#### 3. 价格对比深度分析
- **安居客vs法拍**: 法拍价格平均比安居客低30-40%
- **债权覆盖情况**: 大部分房产的安居客估值都高于债权本金
- **中介费影响**: 购买法拍房可节省2-3%的中介费

#### 4. 投资建议
1. **优先关注**: 法拍折扣大且地段好的房产（如蓝庭花园44%折扣）
2. **谨慎对待**: 学区房法拍，避免盲目追高（文鼎苑竞争激烈）
3. **成本优势**: 法拍房可节省中介费，实际成本更低
4. **风险评估**: 重点关注产权清晰、无纠纷的法拍房源

## 重要注意事项
1. **数据时效性**：房产价格变化较快，注意数据更新时间
2. **信息准确性**：法拍信息可能存在滞后，需多方验证
3. **法律合规**：法拍房涉及法律程序，建议咨询专业律师
4. **市场风险**：房地产市场存在波动风险，需谨慎评估
5. **成本考虑**：法拍房虽价格低，但需考虑税费、装修等隐性成本

## 技能限制
- 依赖公开网络数据，可能无法获取最新成交信息
- 法拍数据可能不完整，部分房产无成交记录
- 价格预测基于历史数据，实际价格可能有偏差
- 无法替代专业的法律和财务尽职调查

## 扩展配置

### 价格配置文件
技能支持通过配置文件自定义区域价格数据：
1. 复制 `scripts/price_config.json.example` 为 `scripts/price_config.json`
2. 根据实际情况修改价格数据
3. 技能会自动加载配置文件中的价格数据

### 环境变量
技能支持通过环境变量配置外部服务：
- `REPORT_GENERATOR_SERVICE`：报告生成服务地址
- `DATA_PROCESSING_SERVICE`：数据处理服务地址
- `WEB_SEARCH_SERVICE`：网络搜索服务地址

## 通用性说明

该技能设计为通用的房产债权分析工具，具有以下特点：
- **区域通用性**：支持全国主要城市和区域的房产分析
- **配置灵活性**：通过配置文件和环境变量实现个性化设置
- **生态兼容性**：可与不同Agent生态的外部能力集成
- **可扩展性**：模块化设计，易于添加新功能和支持新区域

技能默认内置了全国主要城市的基础价格数据，可根据实际需求进行扩展。

## 最佳实践
1. **多源验证**：使用多个平台数据交叉验证
2. **定期更新**：房产价格变化快，需要定期更新
3. **专业咨询**：重要决策建议咨询专业律师和评估师
4. **风险分散**：不要集中投资单一类型或区域房产
5. **长期视角**：房产投资建议长期持有，短期投机风险较大

## 触发词

### 主要触发词
- 房产债权分析
- 债权价值评估
- 房产包投资分析
- 安居客和阿里拍卖价格对比
- 法拍房投资分析
- 房产价格对比分析
- 债权回收分析
- 房产包处置建议

### 平台相关触发词
- 安居客房产价格
- 阿里拍卖房产分析
- 安居客vs阿里拍卖
- 多平台房产价格对比

### 任务相关触发词
- 生成房产债权报告
- 房产投资建议
- 债权风险评估
- 房产数据分析
- 法拍价格分析

### 上下文触发词
当对话中包含以下关键词时，也会触发此技能：
- 住宅房产、二手房、法拍房、商业用房、别墅
- 安居客、阿里拍卖、幸福里、房天下
- 债权本金、抵押物、债务分析、资产包、不良资产

### 与文件解析SKILL协作触发词
- 分析excel表格里的债权
- 帮我分析这个表格的债权数据
- 从表格中分析债权价值
- 解析excel并进行债权分析
- 表格中的房产债权分析
- 分析csv文件中的债权数据
- 解析json文件并进行债权分析
- 帮我分析这个文件的债权信息
- 从文件中提取债权数据并分析
- 分析文本中的房产债权信息

### 与图片解析SKILL协作触发词
- 分析图片中的债权数据
- 从照片中提取房产信息
- 解析图片里的表格数据
- 帮我分析这张图片的债权信息
- 从图片中识别房产地址和金额
- 分析扫描件中的债权数据
- 解析图片中的房产面积和债务信息

### 与音频解析SKILL协作触发词
- 分析语音中的债权信息
- 从录音中提取房产数据
- 解析音频里的债权本金和面积
- 帮我分析这段录音的房产信息
- 从语音中识别房产地址和债务数据

### 与多模态解析SKILL协作触发词
- 分析文档中的债权信息
- 从资料中提取房产数据
- 解析混合媒体中的债权信息
- 帮我分析这份资料的房产信息
- 从多种格式中提取债权数据

## 输入参数

### 直接输入格式
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| action | string | 是 | 操作类型，支持：analyze_debt_portfolio（分析债权组合）、analyze_single_property（分析单个房产） |
| property_data | array | 是 | 房产数据数组，每个元素包含address（地址）、debt_principal（债权本金）、area（面积） |
| options | object | 否 | 可选参数，包含：include_risk_analysis（是否包含风险分析）、output_format（输出格式：markdown/pdf） |

### 与Excel解析SKILL协作格式
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| action | string | 是 | 操作类型，支持：analyze_debt_portfolio（分析债权组合）、analyze_single_property（分析单个房产） |
| excel_data | object | 是 | Excel解析SKILL传来的数据 |
| excel_data.headers | array | 是 | Excel表格表头 |
| excel_data.rows | array | 是 | Excel表格数据行 |
| options | object | 否 | 可选参数，包含：include_risk_analysis（是否包含风险分析）、output_format（输出格式：markdown/pdf） |

### 与其他文件解析SKILL协作格式
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| action | string | 是 | 操作类型，支持：analyze_debt_portfolio（分析债权组合）、analyze_single_property（分析单个房产） |
| file_data | object | 是 | 文件解析SKILL传来的数据 |
| file_data.content | string | 是 | 文件内容 |
| file_data.file_type | string | 是 | 文件类型，支持：csv、json |
| options | object | 否 | 可选参数，包含：include_risk_analysis（是否包含风险分析）、output_format（输出格式：markdown/pdf） |

### 文本数据格式
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| action | string | 是 | 操作类型，支持：analyze_debt_portfolio（分析债权组合）、analyze_single_property（分析单个房产） |
| text_data | string | 是 | 文本形式的房产数据，每行包含地址、债权本金、面积，用逗号或空格分隔 |
| options | object | 否 | 可选参数，包含：include_risk_analysis（是否包含风险分析）、output_format（输出格式：markdown/pdf） |

### 与图片解析SKILL协作格式
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| action | string | 是 | 操作类型，支持：analyze_debt_portfolio（分析债权组合）、analyze_single_property（分析单个房产） |
| image_data | object | 是 | 图片解析SKILL传来的数据 |
| image_data.extracted_text | string | 否 | 从图片中提取的文本 |
| image_data.extracted_table | object | 否 | 从图片中提取的表格数据 |
| image_data.extracted_table.headers | array | 否 | 表格表头 |
| image_data.extracted_table.rows | array | 否 | 表格数据行 |
| options | object | 否 | 可选参数，包含：include_risk_analysis（是否包含风险分析）、output_format（输出格式：markdown/pdf） |

### 与音频解析SKILL协作格式
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| action | string | 是 | 操作类型，支持：analyze_debt_portfolio（分析债权组合）、analyze_single_property（分析单个房产） |
| audio_data | object | 是 | 音频解析SKILL传来的数据 |
| audio_data.transcript | string | 是 | 音频转写文本 |
| options | object | 否 | 可选参数，包含：include_risk_analysis（是否包含风险分析）、output_format（输出格式：markdown/pdf） |

### 与多模态解析SKILL协作格式
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| action | string | 是 | 操作类型，支持：analyze_debt_portfolio（分析债权组合）、analyze_single_property（分析单个房产） |
| multimodal_data | object | 是 | 多模态解析SKILL传来的数据 |
| multimodal_data.text_content | string | 否 | 提取的文本内容 |
| multimodal_data.table_content | object | 否 | 提取的表格内容 |
| multimodal_data.table_content.headers | array | 否 | 表格表头 |
| multimodal_data.table_content.rows | array | 否 | 表格数据行 |
| options | object | 否 | 可选参数，包含：include_risk_analysis（是否包含风险分析）、output_format（输出格式：markdown/pdf） |

## 输出格式

### 分析结果
```python
{
    "success": true,
    "action": "analyze_debt_portfolio",
    "analysis_results": [
        {
            "address": "杭州市萧山区北干街道广德小区xx幢xx单元xxx室",
            "debt_principal": 208.45,
            "area": 102.35,
            "anjuke_average_price": 22800,
            "anjuke_valuation": 233.36,
            "auction_transaction_price": 198.0,
            "auction_discount_rate": 0.85,
            "debt_coverage_ratio": 1.12,
            "price_difference_rate": 0.15,
            "liquidity_score": 85,
            "investment_value_score": 82,
            "investment_suggestion": "优先关注",
            "risk_assessment": {
                "legal_risk": "低",
                "market_risk": "中",
                "liquidity_risk": "低",
                "operational_risk": "中"
            }
        }
    ],
    "summary": "本次分析了1处房产，其中1处建议优先关注。平均债权覆盖率为112%，平均法拍折扣率为85%。",
    "report_url": "http://localhost:8000/reports/analysis_20260306_123456.pdf"
}
```

## 示例用法

### 分析债权组合
```python
{
    "action": "analyze_debt_portfolio",
    "property_data": [
        {
            "address": "杭州市萧山区北干街道广德小区xx幢xx单元xxx室",
            "debt_principal": 208.45,
            "area": 102.35
        },
        {
            "address": "杭州市余杭区五常街道宏旺西溪阳光中心xx幢xx单元xxx室",
            "debt_principal": 890.0,
            "area": 394.64
        }
    ],
    "options": {
        "include_risk_analysis": true,
        "output_format": "pdf"
    }
}
```

### 分析单个房产
```python
{
    "action": "analyze_single_property",
    "property_data": [
        {
            "address": "杭州市上城区春江花月住宅区晓风苑xx幢xx单元xxx室",
            "debt_principal": 1200.0,
            "area": 161.16
        }
    ]
}
```