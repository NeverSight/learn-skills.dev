---
name: academic-research-skills
description: >
  Academic Research Skills (ARS) — 学术研究全流程 AI 助手，38.7k⭐ 开源项目。
  4 个技能覆盖从文献调研到论文发表：Deep Research (13 agents 文献调研/系统综述)、
  Academic Paper (12 agents 写作流水线/LaTeX PDF 输出)、
  Academic Paper Reviewer (7 agents 多视角审稿/反谄媚协议)、
  Academic Pipeline (10 阶段编排器/引文验证/完整性闸门)。
  核心理念：AI 是副驾驶，不是飞行员——帮你查文献、管引用、校格式，研究判断由你做主。
  Trigger keywords: 学术研究, 写论文, 论文写作, 文献综述, 系统综述, 投稿, 审稿,
  毕业论文, academic research, paper writing, literature review, systematic review,
  PRISMA, peer review, 发表论文, 学术写作, 论文润色, 期刊投稿, 会议投稿,
  引文检查, 参考文献, LaTeX论文, 博士研究, 硕士论文, 科研全流程, ARS,
  academic pipeline, deep research paper, 论文审稿, rebuttal, 审稿回复,
  学术引用, citation check, 论文格式, APA, IEEE, Chicago, 科研流水线.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - WebFetch
  - WebSearch
metadata:
  category: thinking
  source: https://github.com/Imbad0202/academic-research-skills
  install: /plugin install academic-research-skills@Imbad0202
  version: "3.18.0"
  license: CC-BY-NC 4.0
  stars: 38700
---

# Academic Research Skills — 学术研究全流程 AI 助手

> 38.7k⭐，Cheng-I Wu（吳政宜）开发。从文献调研到论文发表，一条命令搞定全流程。
> 核心理念：**AI 是副驾驶，不是飞行员**——帮你省掉机械劳动，研究判断由你做主。

## 技能体系

ARS 包含 **4 个技能**，覆盖学术研究的完整生命周期：

```
┌─────────────────────────────────────────────────────────────┐
│                  Academic Research Skills                    │
│                                                             │
│  Deep Research        Academic Paper      Paper Reviewer    │
│  (13 agents)          (12 agents)         (7 agents)        │
│  文献调研·系统综述    写作流水线·LaTeX     多视角审稿·反谄媚   │
│       │                    │                    │           │
│       └────────────────────┼────────────────────┘           │
│                            │                                │
│                   Academic Pipeline                         │
│                   10 阶段编排器                               │
│                   完整性闸门·引文验证·格式输出                 │
└─────────────────────────────────────────────────────────────┘
```

### 1. Deep Research（13 agents）— 文献调研引擎

| 模式 | 说明 |
|------|------|
| Full Research | 完整调研：背景→研究问题→方法论→文献→综合 |
| Quick Brief | 快速简报，30 分钟出结果 |
| Literature Review | 文献综述，多数据库并行检索 |
| Systematic Review | PRISMA 标准系统综述流程 |
| Fact-Check | 事实核查模式 |
| Socratic Guided | AI 苏格拉底式引导你理清研究问题 |
| Multi-Artifact | 多维度并行调研 |

- **Semantic Scholar API 验证**：每篇引用自动校验
- **Devil's Advocate**：内置反对者角色，挑战你的假设
- **知识缺口标注**：明确告知"这个方向目前缺少证据"

### 2. Academic Paper（12 agents）— 论文写作流水线

| 模式 | 说明 |
|------|------|
| Full Writing | 完整论文：大纲→论证→初稿→格式化 |
| Plan/Guided | 先出大纲，逐节确认后再写 |
| Outline Only | 只生成详细大纲 |
| Revision | 修改润色已有稿件 |
| Revision Coach | 教你如何修改（不给具体文字） |
| Abstract Only | 生成/优化摘要 |
| Literature Review | 文献综述章节 |
| Citation Check | 逐条校验引用真实性 |
| Format Conversion | Markdown↔DOCX↔LaTeX 互转 |
| Disclosure Statement | 自动生成利益冲突/数据可用性声明 |
| Rebuttal Audit | 审稿回复策略审计 |

**输出格式**：Markdown + DOCX + LaTeX/PDF（APA 7 / IEEE / Chicago）

**独有特性**：
- **Style Calibration**：先读你的旧论文，学习你的写作风格，再动笔
- **VLM Figure Verification**：用视觉模型检查图表质量
- **Writing Quality Check**：自动检查逻辑流、术语一致性、论证强度

### 3. Academic Paper Reviewer（7 agents）— 多视角审稿模拟

```
主编 (Editor-in-Chief)
  ├── 审稿人 A（方法学专家）
  ├── 审稿人 B（领域专家）
  ├── 审稿人 C（统计/数据专家）
  └── Devil's Advocate（专职挑刺）
         │
         ▼
    综合评审报告 + 修改路线图
```

**评分体系**：0-100 分，明确决策阈值
- ≥80：Accept
- 65-79：Minor Revision
- 50-64：Major Revision
- <50：Reject

**反谄媚协议**：Devil's Advocate 有让步阈值——只有你的反驳得分 ≥4/5 才让步，防止"你说啥都对"的讨好行为。

### 4. Academic Pipeline（10 阶段编排器）

端到端流水线，可中途加入：

```
Stage 1: 研究问题定义
Stage 2: 文献调研 ──→ Stage 2.5: 🔒 完整性闸门 1
Stage 3: 方法论设计
Stage 4: 论文初稿 ──→ Stage 4.5: 🔒 完整性闸门 2
Stage 5: 自我审稿
Stage 6: 修改润色
Stage 7: 格式输出
Stage 8: 最终检查
```

**完整性闸门**基于 Lu et al. 2026 *Nature* 的 7 种 AI 论文失败模式：
引文幻觉检测 · 数据虚构检测 · 方法论虚构检测 · 逻辑断裂检测 · 统计误用检测 · 图表一致性检查 · 利益冲突声明完整性

## 安装

需要 Claude Code v3.7.0+。两条命令：

```
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills
```

安装后验证：

```
/ars-plan                      # 开始 Socratic 对话，帮你理清论文结构
/ars-lit-review "你的课题"      # 一键生成文献综述
```

## 使用示例

```
"用 ARS 帮我写一篇关于 Transformer 架构演进的综述论文"
"帮我审一下这篇准备投 CVPR 的论文"
"检查这篇稿件的引用有没有幻觉"
"帮我把这篇 Markdown 论文转成 LaTeX IEEE 格式"
"用 Deep Research 调研一下 retrieval-augmented generation 的最新进展"
"帮我写审稿回复信，审稿人说我的 baseline 不够强"
```

## 成本估算

完整 10 阶段流水线，15000 字论文：约 **$4-6**（API 费用）  
推荐配置：Claude Opus 4.7 + Max 订阅（$100-200/月）

## 三层数据隔离

ARS 严格分离三层数据，防止评分标准泄露给写作 Agent：

| 层 | 内容 | 谁能读 |
|----|------|--------|
| Layer 1 | 原始输入（你的稿件、数据、笔记） | 全体 Agent |
| Layer 2 | 验证后的内容（经引文校验的数据） | 写作 + 审稿 Agent |
| Layer 3 | 评分量表、参考数据、审稿意见 | 仅审稿 Agent |

## 与仓库其他技能的关系

| 技能 | 定位 | 与 ARS 的关系 |
|------|------|--------------|
| `scientific-research` | 139 个科研技能 + 78 个数据库，偏实验/数据分析 | **互补**：ARS 管文献+写作，scientific-research 管实验+数据 |
| `gpt-researcher` | 快速深度调研，20+ 来源并行抓取 | 轻量替代：日常调研用 gpt-researcher，正式论文用 ARS |
| `storm-research` | Stanford STORM 方法论，4 个 Prompt 手动研究 | 轻量替代：快速结构化研究用 STORM |
| `ljg-paper` | 单篇论文速读，浓缩为一句话命题 | **互补**：ARS 写论文，ljg-paper 读论文 |
| `scientific-writing-editor` | 学术写作编辑（论文/基金/推荐信） | 轻量替代：单篇润色用它，全流程写作用 ARS |
| `Dog-Project-Evaluate` | 三通道项目评估（课程/论文/开源） | **互补**：ARS 写+审，Dog-Project-Evaluate 评估项目水平 |

## 推荐组合

### 完整学术流水线
```
scientific-research（实验/数据分析）
       │
       ▼
ljg-paper（精读关键论文）
       │
       ▼
academic-research-skills（文献综述→写作→审稿→发表）
       │
       ▼
Dog-Project-Evaluate（投稿前项目水平评估）
```

### 轻量科研
```
storm-research（快速结构化研究）
       │
       ▼
scientific-writing-editor（论文润色）
```

## 参考

- GitHub: https://github.com/Imbad0202/academic-research-skills
- 安装: `/plugin install academic-research-skills@Imbad0202`
- 许可: CC-BY-NC 4.0（免费共享和改编，需署名，不可商用）
- 署名格式: "Based on Academic Research Skills by Cheng-I Wu" + GitHub URL
