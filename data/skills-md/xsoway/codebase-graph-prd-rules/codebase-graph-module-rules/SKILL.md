---
name: codebase-graph-module-rules
description: Use this skill when a user provides a feature description or module name and needs Graphify-backed detailed rules, links, sorting, flows, and test coverage; triggers include 模块业务规则、功能规则梳理、线索包规则 and feature business rules.
---

# 模块图谱化业务规则

针对用户指定的需求或功能模块，先建立 Graphify 图谱，再由源码确认业务事实，输出详细规则、依赖链路、排序、流程图与测试说明。仅分析和生成文档，不改业务系统。

## 何时使用

- 用户给出具体需求描述、业务名、领域对象或功能模块，要求从代码讲清“它到底怎么工作”。
- 用户要求专项梳理排序、限额、状态、分发、结算、审批、风控等复杂业务规则。
- 用户需要某模块可交付给产品、运营、测试人员阅读的规则与测试专项文档。

不用于无模块边界的全项目盘点；该场景使用 `codebase-graph-business-rules`。

## 输出格式选项

- 默认：项目本地 `docs/` 下的模块专项 Markdown。
- 用户明确要求时：附加测试用例表、决策表或来源账本 CSV/JSON。

## 如何使用

1. 必须先读 [完整执行规范](prompts/codebase-graph-module-rules.md)，将用户术语映射为代码候选，再确认最小依赖边界。
2. 建/刷新图谱后，按 [模块图谱检索规则](references/module-discovery.md) 运行邻域与路径查询；图谱只定位，源码/SQL/配置确认规则。
3. 按 [专项文档与测试契约](references/module-document-contract.md) 写一个合并模块章节，区分过滤、排序和运行时控制。
4. 需要核对最小交付结构时，读 [示例](examples/module-rules-example.md)。
5. 交付前运行 `scripts/verify_skill_package.py .` 验证 Skill 包；再运行项目文档的来源/结构校验。

## 参考文件

- 需要将自然语言需求映射到入口、实体、任务、Mapper、配置和外部系统时，读 `references/module-discovery.md`。
- 需要写规则表、排序决策、状态图或测试矩阵时，读 `references/module-document-contract.md`。
- 需要回归 Skill 行为时，读 `evals/eval.yaml` 和对应 case；Eval 不代替真实项目分析。

## 常见误区

- 只查一个类，遗漏消息入口、定时任务、Mapper/SQL、配置或专属分支。
- 把“未通过条件”写成排序低，或把排序靠前写成必然发送/执行。
- 声称并列排序有稳定业务优先级，但比较器/SQL没有最终键。
- 未经授权调用真实下游、修改数据或在文档中泄露凭据。

## 最佳实践

- 用“触发 → 编排 → 决策 → 数据/日志 → 外部结果”的路径定义模块边界。
- 为每一条关键规则准备条件、结论、例外、来源和可观察测试断言。
- 对外部协议、动态配置、数据库真实数据和调度频率保持证据边界。
