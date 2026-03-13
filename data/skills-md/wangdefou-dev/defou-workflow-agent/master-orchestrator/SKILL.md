---
name: master-orchestrator
description: 全自动总指挥：串联热点抓取、内容生成与爆款验证的全流程技能。从热点发现到高质量成品的零人工干预自动化流水线。
version: 1.0.0
triggers:
  - "全自动生成"
  - "一键生成内容"
  - "完整流程"
  - "自动化创作"
  - "热点到成品"
---

# Master Orchestrator (全自动总指挥)

## 概述

这个 Skill 是 Defou Workflow Agent 的"大脑"和"指挥中心"。它将原本独立的技能模块串联成一条完整的自动化生产流水线，实现从"全网热点"到"高质量成品"的零人工干预作业。

## 核心功能

- **全流程自动化**：一键完成热点抓取、内容生成、质量验证
- **智能调度**：自动协调多个 Skill 模块的执行顺序
- **双重质检**：内容生成 + 爆款验证的双重 AI 加持
- **零人工干预**：从输入到输出全程自动化

## 工作流程

### 第一阶段：内容生成引擎

**对应技能**：`tophub-defou-stanley-combo`

**执行步骤**：
1. 抓取 TopHub 全网热榜
2. 智能筛选 Top 10 最具爆款潜力的话题
3. 基于 Defou x Stanley 风格生成初稿

**产出位置**：`outputs/defou-stanley-posts/`

### 第二阶段：质量验证引擎

**对应技能**：`viral-verification`

**执行步骤**：
1. 自动读取第一阶段生成的初稿
2. 模拟"增长黑客"进行 6 维爆款要素打分
3. 生成最终优化建议和终稿

**产出位置**：`outputs/viral-verified-posts/`

## 使用方法

### 运行脚本

在项目根目录下运行：

```bash
npm run skill:master
```

或者直接使用 `ts-node`：

```bash
npx ts-node src/master.ts
```

### 执行流程

1. **启动**：运行命令后，系统自动开始工作
2. **热点抓取**：从 TopHub 获取最新热榜
3. **选题筛选**：AI 分析并选出 Top 10 话题
4. **内容生成**：为每个话题生成 Defou x Stanley 风格内容
5. **质量验证**：对生成的内容进行爆款要素评估
6. **优化重写**：生成最终优化版本
7. **完成**：所有成品保存到输出目录

## 输出结果

### 最终产出目录

```
defou-workflow-agent/outputs/viral-verified-posts/
```

这里存放了经过双重 AI 智慧加持的最终文章，可以直接用于发布。

### 文件结构

```
outputs/
├── defou-stanley-posts/          # 初稿（第一阶段产出）
│   ├── post_20260123_topic1.md
│   └── post_20260123_topic2.md
└── viral-verified-posts/         # 终稿（第二阶段产出）
    ├── verified_post_20260123_topic1.md
    └── verified_post_20260123_topic2.md
```

## 前置条件

- 已安装 Node.js 环境
- 已配置 `.env` 文件：
  - `ANTHROPIC_API_KEY`：Anthropic API Key
  - `ANTHROPIC_BASE_URL`：（可选）API Base URL
- 网络连接正常（需要访问 TopHub）

## 依赖配置

无需额外配置，复用项目的全局 `.env` 配置。

## 使用场景

- **日常内容生产**：每天自动生成 10 篇高质量文章
- **热点追踪**：快速响应全网热点，生成相关内容
- **批量创作**：一次性产出多篇经过验证的爆款内容
- **内容储备**：提前准备内容库，随时发布

## 注意事项

1. **API 配额**：会调用多次 Claude API，注意 API 配额
2. **执行时间**：完整流程可能需要几分钟，请耐心等待
3. **网络要求**：需要稳定的网络连接访问 TopHub
4. **输出管理**：定期清理 outputs 目录，避免文件过多

## 示例输出

运行 `npm run skill:master` 后，终端会显示：

```
🚀 Master Orchestrator 启动...
📡 正在抓取 TopHub 热榜...
✅ 获取到 100 条热点
🧠 AI 正在分析并筛选 Top 10 话题...
✅ 已选出 10 个最具潜力的话题
📝 正在生成内容 (1/10)...
✅ 初稿已生成：post_20260123_topic1.md
🔍 正在进行爆款验证...
✅ 终稿已生成：verified_post_20260123_topic1.md
...
🎉 全部完成！共生成 10 篇文章
📂 查看结果：outputs/viral-verified-posts/
```

