---
name: codebase-graph-business-rules
description: Use this skill when a user asks to scan project code, build a Graphify graph, and produce whole-project business rules; triggers include 项目业务规则、全量功能梳理、代码建图谱 and codebase business rules.
---

# 全项目图谱化业务规则

从项目代码建立 Graphify 图谱、复核源码，并生成面向非开发者的全量业务规则文档。仅分析和写文档，除非用户另行授权，不改业务代码、数据或外部系统。

## 何时使用

- 用户要求扫描整个项目、整理全部功能、模块、状态、数据关系或端到端链路。
- 用户要求先建代码图谱，再基于图谱生成业务规则、流程图、测试范围或 PRD 基线。
- 已有规则文档需要用代码和图谱做全量补漏或追溯。

不用于只分析一个明确模块；该场景使用 `codebase-graph-module-rules`。

## 输出格式选项

- 默认：项目本地 `docs/` 下的一份 Markdown 业务规则基线。
- 用户明确要求时：附加规则账本 CSV/JSON；仍保留 Markdown 作为业务阅读主稿。

## 如何使用

1. 必须先读 [完整执行规范](prompts/codebase-graph-business-rules.md)，再确认项目根、源码范围和已有文档。
2. 建/刷新 Graphify 图谱后，读取 [图谱操作与证据边界](references/graphify-and-evidence.md)；图谱负责发现关系，源码、SQL/XML、配置才确认事实。
3. 按 [文档与测试契约](references/document-contract.md) 生成一份集成文档；相同模块合并到同一节，不在末尾重复追加。
4. 需要输出骨架或核对成稿结构时，参考 [示例](examples/project-rules-example.md)。
5. 交付前运行 `scripts/verify_skill_package.py .` 验证 Skill 包；实际项目文档还须运行项目已有校验或按 Prompt 执行最小引用校验。

## 参考文件

- 需要建图、查询、语义提取或处理无可用 LLM 凭据时，读 `references/graphify-and-evidence.md`。
- 需要决定模块目录、表格、流程图、测试矩阵及证据格式时，读 `references/document-contract.md`。
- 需要回归 Skill 行为时，读 `evals/eval.yaml` 与匹配 case；Eval 配置不代表真实项目已被分析。

## 常见误区

- 把图谱推断边当作业务事实，或仅凭类名/注释下结论。
- 将资格过滤、候选排序和实际执行/回滚混成“优先级”。
- 因同一功能有多个链路而在文档最后新增重复模块；应合并为同一模块的分支。
- 把静态文档校验写成真实接口、任务、数据库或生产环境已验证。

## 最佳实践

- 以入口点、核心实体、任务、消息、持久化和外部边界建立完整链路，再按业务模块组织内容。
- 每条关键规则记录来源文件/行号、事实状态、例外和可验证测试点。
- 对未检视的外部协议、运行配置、调度表达式和数据库数据明确写“待确认/未验证”。
