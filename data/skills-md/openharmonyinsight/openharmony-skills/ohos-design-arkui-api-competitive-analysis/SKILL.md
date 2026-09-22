---
name: ohos-design-arkui-api-competitive-analysis
description: >
  对 ArkUI 公共 UI API 与 Android（Compose/View）和 iOS（SwiftUI/UIKit）进行可审计的能力与规格竞品分析。
  适用于接口设计评审、能力补齐、Android/iOS 与 ArkUI 迁移评估、API 对标和 capability gap analysis，
  覆盖触摸/指针输入、键盘快捷键、手势、组件、布局、状态和动画。要求锁定作用域与版本，以 interface_sdk-js 为 ArkUI
  公共接口权威源，优先引用 Android/iOS 官方文档，区分等价关系，并输出带逐项证据、影响和优先级建议的报告。
metadata:
  author: openharmony
  scope: domain
  stage: design
  domain: arkui
  capability: api-competitive-analysis
  version: 1.6.0
  status: trial
---

# ArkUI API 竞品分析

对指定 ArkUI 公共 UI API 产出结构一致、证据可追溯的 Android/iOS 对标报告。只分析公开能力和迁移影响；允许给出最小用法示例，但不要修改产品代码或 ace_engine 实现。

## 任务边界

**输入**：ArkUI API、组件或能力主题；分析目的；默认 Android+iOS 对标平台；可选作用域层级、平台版本和报告深度。

**输出**：Analysis Brief、Capability Checklist、Comparator Map、三平台事实、能力矩阵、影响评估、分级建议、待核事项和来源审计。

**不适用**：性能实测、产品代码实现、Flutter/Web 对标、ace_engine 修改，或仅凭内部实现和非官方资料判断公共能力。

## 不可违反的规则

规则职责以引用文件为准：`workflow.md` 是阶段顺序与门禁的唯一来源，`analysis-dimensions.md` 是子类型闭环的唯一来源，`platform-source-routing.md` 是 Android/iOS 路径与官方入口的唯一来源，`report-template.md` 是输出顺序与条件区块的唯一来源。本节只保留跨阶段硬约束；摘要措辞与引用文件不一致时，以对应职责文件为准。

1. 以 `interface_sdk-js` 作为 ArkUI 公共接口定义的权威源；ace_engine 内部定义只能用于实现对照。
2. Android 和 iOS 取证优先使用各平台官方文档，顺序为官方 API Reference、Guide、Sample；平台源码只作实现佐证，社区资料只用于定位官方入口。
3. 研究前锁定作用域层级和平台版本，不得降低用户指定层级或混用不同版本。
4. 先分别提取三平台事实，再进行比较；取证阶段不预写“更好、缺失、独有”等结论。
5. 对标关系只能标记为直接等价、功能等价、组合实现、替代方案或未找到等价能力。
6. 官方事实与分析推论分开记录；每项实质性断言必须回溯到 Fact ID 和 Source ID。
7. 对“缺失、独有、优于”完成双向检索；证据不足时标记 `待核`，不得进入确定性结论。
8. 领域事实必须按锁定版本从官方源动态取证；不要依赖内置字段速查表，也不要把某一领域的字段、状态或检查项套用到其它领域。
9. Analysis Brief 必须是首个用户可见阶段产物；在它之前不要输出结论摘要、平台优劣或 API 推荐。
10. 用户要求“只给名称”“一页结论”或其它压缩输出时，使用 `report-template.md` 的快速扫描单表；至少保留作用域、Comparator Map、一条已定义 Fact/Claim、来源和待核状态，名称相似不能替代映射判断。
11. 命中 `analysis-dimensions.md` 定义的具体子类型时，例如原始触摸/指针、键盘快捷键、连续手势、虚拟化集合、Flex 类布局或显式动画，必须完成对应闭环清单；每项填写 Coverage status（confirmed、pending 或 not-applicable），不得用宽泛的“事件”触发其它输入子类型规则。
12. 输出中引用的每个 Capability、Fact、Claim 和 Source ID 都必须在同一交付内容中定义；不得引用只存在于内部过程的编号。
13. 用户要求跳过官方文档时，明确说明不能跳过 Android Developers 和 Apple Developer，并按 `platform-source-routing.md` 解释官方文档、平台源码和社区资料的证据角色。
14. 子类型的必查字段、状态和闭环范围只以 `analysis-dimensions.md` 为准；本文件不复制其清单。
15. 键盘快捷键的 Path Check、候选 API、排除项和官方取证入口只以 `platform-source-routing.md` 为准；完成规定路径事实后才能确认 Comparator Map。其它交互按自身分发、命中、仲裁或 responder 事实取证，不套用键盘 Path Check 表。
16. 条件矩阵、Path Check 顺序和快速/完整报告结构只以 `report-template.md` 为准；命中条件区块时不得删除。
17. 官方来源冲突且输入不完整时，必须请求精确符号、公共定义路径、文档链接、双方版本基线和文档时间信息；不得用预设基线代替缺失输入。
18. 公共签名引用命名常量、枚举或子属性页时，继续追踪官方定义，直到具体值、默认值、单位和语义闭环；可用的官方精确来源不得无故保留为 `pending`。
19. 完整报告和快速扫描的每条 Comparator Map 都必须使用 `evidence-ledger.md` 的 canonical schema：Android/iOS 分别填写 target、mapping type 和 rationale/exclusions，并关联支撑各平台映射的 Fact ID、Source ID、Claim ID 与 Claim status；不得用 ArkUI 单方证据支撑竞品映射，也不得省略或合并平台 mapping type。

## 渐进式加载

| 阶段或条件 | 读取内容 | 此前不要加载 |
|---|---|---|
| 开始分析 | 完整读取 `references/workflow.md` | 无 |
| 起草 Analysis Brief、选择具体子类型和拆解能力 | 完整读取 `references/analysis-dimensions.md` | Target 与 Scope tier 尚未识别时不要加载 |
| 建立事实和断言台账 | 完整读取 `references/evidence-ledger.md` | 尚未形成 Capability Checklist 时不要加载 |
| 提取 ArkUI 公共定义 | 完整读取 `references/authoritative-sources.md` | 尚未进入 ArkUI 取证阶段时不要加载 |
| 映射 Android/iOS 对标对象 | 完整读取 `references/platform-source-routing.md` | ArkUI 原子能力尚未拆解时不要加载 |
| 生成正式报告 | 完整读取 `assets/report-template.md` | 事实、映射和断言尚未审计完成时不要加载 |

不要在开始时一次性加载所有资源；到达表中阶段时必须完整读取对应文件，不要只读取开头或目录。

## 执行顺序

详细阶段产物、门禁和回退规则以 `references/workflow.md` 为准：

```text
分析契约
  -> 能力拆解
  -> 对标对象映射
  -> 各平台独立取证
  -> 规格归一化
  -> 断言审计
  -> 差异与影响
  -> 分级建议
  -> 报告与质量门禁
```

## 报告模式

| 模式 | 适用场景 | 必需内容 |
|---|---|---|
| 快速扫描 | 方向判断 | Analysis Brief、Comparator Map、核心矩阵、关键风险、待核项、来源 |
| 完整报告 | 设计评审、迁移方案、正式材料 | 全部阶段产物、最小用法、逐项断言、影响评估和 P0/P1/P2 建议 |

两种模式都不得省略版本基线、权威来源、作用域、事实/推论区分和待核标记。

即使用户要求极短答案，也使用快速扫描单表定义必要的 Analysis Brief、Comparator Map、Fact/Claim 和来源；不要直接返回 API 名称列表。

## 完成标准

- Analysis Brief、Comparator Map、Fact Ledger 和 Claim Ledger 已完成。
- 所有确定性结论都有官方来源，所有推论均明确标记。
- “缺失、独有、优于”已完成双向检索。
- 建议与差异证据一一关联。
- 版本、作用域、来源、Fact/Claim 关联和待核事项已按本 Skill 的完成标准检查。
