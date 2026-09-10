---
name: core
slug: core
displayName: QA 共享知识库
version: 0.8.1
description: "qa-skills shared knowledge base — dependency, NOT triggerable: executability standards, evidence grading, risk model, type matrix, templates, scripts. Never invoke standalone; always install with the skills, or references break. 共享知识库（依赖单元，非触发 skill）：承载全系列引用的方法/模板/脚本。任何测试任务不要独立触发；装其他 skill 必须连装。"
---

# qa-skills 共享知识库（core）

本目录是框架的公共层：不定义工作流、不面向用户触发，仅被 `skills/` 下其余
12 个 skill（qa / requirement-analysis / test-strategy / …）以相对路径
`../core/<file>` 按需引用。单一维护源，多 skill 复用。

## 共享文档

| 文件 | 内容 |
|------|------|
| `evidence.md` | 证据分级标准（E0–E4）与状态标注 |
| `risk-model.md` | 风险评级模型（评级强制挂证据） |
| `executability.md` | 用例可执行性硬标准（8 条，一票否决项） |
| `testing-principles.md` | 测试原则 |
| `case-format.md` | 用例编号与格式规范 |
| `coverage.md` | 覆盖评估口径 |
| `schema-extraction.md` | schema.yaml 抽取规则 |
| `clarify-pattern.md` | 澄清检查点模式 |
| `test-type-matrix.md` | 类型决策矩阵（十轴全轴必答） |
| `triage.md` | 失败分流规范（四分类判定树 + G/S 信号 + 反吞没条款，失败 ≥3 条触发） |
| `pipeline-integration.md` | 流水线集成与非交互运行约定（⏸ 检查点降级、产物落盘、退出码语义、CI 触发分层与失败回流） |
| `report-template.md` | 测试报告模板 |
| `methods/*.md` | 设计方法细则（边界 / 数据驱动 / 权限 / 状态机）与执行层造数模式（数据工厂） |
| `scripts/*.py` | Schema 校验器、类型信号扫描器 |

## When NOT to Use

- 任何具体测试任务（写用例、定策略、查 Bug 等）**都不要触发本 skill**：
  它不包含工作流，独立使用没有产出。对应任务请用其余 12 个 skill 之一。
- 本 skill 仅在两种情况下被触及：① 其余 skill 工作流按需引用上述文件；
  ② 安装/校验场景（作为安装依赖单元被安装器识别）。
