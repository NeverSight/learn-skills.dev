---
name: "01-start-mathmodel"
description: "工作流入口v2.1。12阶段完整流程+领域知识自动加载，每阶段带审批节点"
---

---
name: "01-start-mathmodel"
description: "数学建模竞赛工作流入口v2.1。启动完整建模流程：询问用户偏好，生成plan.md和todo.md，并按新12阶段顺序调用skills。每阶段完成后必须经用户审批确认再进入下一阶段。"
---

# 数学建模工作流 v2.1（12阶段 + 领域知识）

本 skill 是数学建模竞赛项目的总控入口。负责启动流程、询问偏好、记录决策、生成计划，按顺序调用各阶段 skill。

**核心原则：每阶段完成后必须呈现产出给用户，等待明确审批后再进入下一阶段。**

## 知识加载

- 全程加载：`00-system` 总规则、`knowledge/general.md` 通用知识
- 按需加载：`knowledge/` 下的领域文件（由赛题特征决定）

## 必须产出

- `plan.md`：整体流程方案
- `todo.md`：待办事项列表

## 工作流

### 1. 询问用户偏好

| 优先级 | 问题 | 影响 |
|--------|------|------|
| 1 | 排版引擎：Typst / LaTeX | 决定09-writing模板 |
| 2 | 竞赛类型：国赛/华为杯/MCM/... | 决定模板和知识库 |
| 3 | 论文语言：中文/英文 | MCM/ICM强制英文 |
| 4 | 子问题数量是否已知 | 影响章节文件数量 |

### 2. 自动加载领域知识

| 赛题特征 | 加载文件 |
|---------|--------|
| 医学/生物/临床/药物 | `knowledge/medical.md` |
| 生态/环境/碳排放/污染 | `knowledge/environment.md` |
| 物流/供应链/配送/路径 | `knowledge/transport.md` |
| 制造/生产/排程/调度 | `knowledge/manufacturing.md` |
| 能源/电力/微电网 | `knowledge/energy.md` |
| 金融/投资/风险/定价 | `knowledge/finance.md` |

### 3. 制定方案

workflow:
   step      skills                  审批节点
0. 系统规则  - `00-system`            ← 已加载
1. 启动入口  - `01-start-mathmodel`   ← 当前
2. 赛题分析  - `02-analysis-modeling` → 呈现分析报告
3. 假设设计  - `03-hypothesis`        → 呈现假设报告
4. 编程实现  - `04-coding`            → 呈现结果数据
5. 图表生成  - `05-visualization`     → 呈现图表
6. 实验管理  - `06-experiment-manager` → 呈现实验索引
7. 结果分析  - `07-result-analysis`   → 呈现分析报告
8. 流程图    - `08-drawio`            → 呈现流程图
9. 论文撰写  - `09-writing`           → 呈现论文PDF
10.创新优化  - `10-innovation-engine` → 呈现创新方案报告
11.评委审稿  - `11-reviewer-mode`     → 呈现审查报告
12.最终验收  - `12-verify`            → 呈现验收报告+评分

### 7. 审批节点执行方式

每个阶段完成后：
1. **呈现产出**：通过 `present_files` 展示给用户
2. **总结要点**：2-3句话概括核心结论
3. **等待确认**：明确询问是否进入下一阶段
4. **处理反馈**：确认→下一阶段；修改→重新呈现；重做→重新执行

**不要跳过审批节点。**