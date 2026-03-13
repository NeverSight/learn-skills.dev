---
name: tophub-trends
description: 获取并分析 TopHub 热榜数据，提供内容创作灵感。自动抓取实时热点并使用 AI 分析高流量潜力话题。
version: 1.0.0
triggers:
  - "获取热点"
  - "TopHub 热榜"
  - "热点分析"
  - "选题灵感"
  - "当前热门话题"
---

# TopHub Trends Analysis Skill

## 概述

这个 Skill 用于自动化获取 TopHub 热榜数据，并利用 Claude 分析当前最具传播潜力的热点话题，为内容创作者提供选题建议。

## 核心功能

- **实时热榜抓取**：从 TopHub 获取全网最新热点
- **AI 智能分析**：使用 Claude 分析前 30 个热点的传播潜力
- **选题建议**：识别高流量潜力话题并提供创作方向
- **数据存档**：保存原始数据和分析报告

## 使用场景

- 每日选题灵感获取
- 热点追踪和分析
- 内容规划参考
- 趋势研究

## 工作流程

```
抓取热榜 → AI 分析 → 生成报告 → 保存文件
```

### 详细步骤

1. **抓取热榜**：从 TopHub (https://tophub.today/hot) 获取实时数据
2. **数据筛选**：提取前 30 个热点话题
3. **AI 分析**：使用 Claude 评估每个话题的传播潜力
4. **生成报告**：输出包含选题建议的 Markdown 报告
5. **保存文件**：同时保存原始 JSON 和分析报告

## 使用方法

### 运行脚本

在项目根目录下运行：

```bash
npx ts-node .claude/skills/tophub-trends/tophub.ts
```

或者添加到 `package.json` 的 scripts 中：

```json
{
  "scripts": {
    "skill:trends": "ts-node .claude/skills/tophub-trends/tophub.ts"
  }
}
```

然后运行：

```bash
npm run skill:trends
```

## 输出结果

### 文件位置

脚本运行后，会在 `defou-workflow-agent/outputs/trends/` 目录下生成两个文件：

```
outputs/trends/
├── tophub_hot_20260123_143022.json    # 原始热榜数据
└── tophub_analysis_20260123_143022.md # AI 分析报告
```

### 文件内容

#### 1. 原始数据 (JSON)

```json
{
  "timestamp": "2026-01-23T14:30:22.000Z",
  "total": 100,
  "hotList": [
    {
      "rank": 1,
      "title": "某某热点事件",
      "url": "https://...",
      "heat": "1234567",
      "source": "微博"
    },
    ...
  ]
}
```

#### 2. 分析报告 (Markdown)

```markdown
# TopHub 热榜分析报告

**生成时间**：2026-01-23 14:30:22

## 📊 数据概览

- 总热点数：100
- 分析范围：Top 30
- 数据来源：TopHub

## 🔥 高潜力选题推荐

### 1. [热点标题]
- **热度**：⭐⭐⭐⭐⭐
- **传播潜力**：高
- **创作角度**：...
- **推荐理由**：...

### 2. [热点标题]
...

## 💡 创作建议

1. **热点借势**：...
2. **反直觉角度**：...
3. **深度分析**：...
```

## 前置条件

- 已安装 Node.js 环境
- 已配置 `.env` 文件：
  - `ANTHROPIC_API_KEY`：Anthropic API Key
  - `ANTHROPIC_BASE_URL`：（可选）API Base URL
  - `MOCK_MODE`：（可选）设置为 `true` 使用模拟数据测试
- 网络连接正常（需要访问 TopHub）

## 配置选项

在 `.env` 文件中配置：

```env
# 必需配置
ANTHROPIC_API_KEY=your_api_key

# 可选配置
ANTHROPIC_BASE_URL=https://api.anthropic.com
MOCK_MODE=false                    # 测试模式
TOPHUB_URL=https://tophub.today/hot # 自定义热榜 URL
```

## 示例

### 运行输出

```bash
$ npm run skill:trends

🚀 TopHub Trends Analysis 启动...
📡 正在抓取 TopHub 热榜...
✅ 获取到 100 条热点
🧠 AI 正在分析前 30 个热点...
✅ 分析完成
💾 保存原始数据：outputs/trends/tophub_hot_20260123_143022.json
💾 保存分析报告：outputs/trends/tophub_analysis_20260123_143022.md
🎉 完成！
```

### 分析报告示例

```markdown
# TopHub 热榜分析报告

**生成时间**：2026-01-23 14:30:22

## 📊 数据概览

- 总热点数：100
- 分析范围：Top 30
- 数据来源：TopHub

## 🔥 高潜力选题推荐

### 1. AI 大模型价格战升级
- **热度**：⭐⭐⭐⭐⭐
- **传播潜力**：极高
- **创作角度**：
  - 反直觉：价格战背后的真正赢家不是用户
  - 深度分析：从价格战看 AI 行业的底层逻辑
  - 人间清醒：免费的 AI 最贵
- **推荐理由**：科技热点 + 反共识角度 + 与普通人相关

### 2. 年轻人"反向消费"成趋势
- **热度**：⭐⭐⭐⭐
- **传播潜力**：高
- **创作角度**：
  - 扎心算账：算一算"反向消费"能省多少钱
  - 人性洞察：不是年轻人抠，是真的穷
  - 结构分析：消费降级背后的阶层固化
- **推荐理由**：社会现象 + 年轻人痛点 + 易引发共鸣

## 💡 创作建议

1. **热点借势**：选择与目标受众相关的热点，避免纯娱乐八卦
2. **反直觉角度**：不要跟风，找到反共识的切入点
3. **深度分析**：从现象上升到本质，提供独特洞察
4. **时效性**：热点有时效性，建议 24 小时内完成创作
```

## 注意事项

1. **时效性**：热榜数据实时变化，建议定期运行
2. **API 配额**：每次运行会调用 Claude API，注意配额
3. **网络要求**：需要稳定的网络连接访问 TopHub
4. **数据准确性**：AI 分析仅供参考，最终选题需人工判断

## 故障排除

### 问题：抓取失败

**可能原因**：
- TopHub 网站访问受限
- 网络连接问题
- 网站结构变化

**解决方案**：
- 检查网络连接
- 使用 `MOCK_MODE=true` 测试
- 更新爬虫代码适配新结构

### 问题：AI 分析质量不佳

**可能原因**：
- Prompt 需要优化
- 热点数据质量问题

**解决方案**：
- 调整分析 Prompt
- 增加数据筛选条件
- 使用更强大的模型

## 高级用法

### 定时任务

使用 cron 定时运行：

```bash
# 每天早上 8 点运行
0 8 * * * cd /path/to/project && npm run skill:trends
```

### 自定义分析维度

修改脚本中的分析 Prompt，添加自定义维度：

```typescript
const analysisPrompt = `
分析以下热点，评估维度：
1. 传播潜力
2. 与目标受众的相关性
3. 创作难度
4. 时效性
...
`;
```

