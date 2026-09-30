---
name: brainstorming
description: >
  设计脑暴 / 实现前方案校准：当用户想把已基本成立的想法、功能方向或产品问题，在写 PRD、画 mockup
  或进入开发计划前，先比较方案、确认取舍、对齐 UI/视觉约束，并收敛成可执行设计 spec 时使用。
  可用中文唤起：“先脑暴一下方案”“先不要写 PRD，帮我设计几种路径”“参考 brainstorming 把这个需求变成设计 spec”
  “实现前先讨论设计”。问题还没定义清楚时先用 ai-collaboration-calibration；已有方案要压力测试时用 grill-me；
  直接写 PRD 时用 prd-architect；grill-me 返回精确设计 gap 时，本 Skill 只输出 Design Delta。
---

# 设计脑暴（brainstorming）

## 中文速查

- 中文名：设计脑暴 / 实现前方案校准
- 英文稳定名：`brainstorming`
- 分类：产品与 PRD / 认知与协作之间的方案收敛桥
- 状态：`core`
- 你可以这样叫我：`先脑暴一下方案`、`先不要写 PRD，帮我设计几种路径`、`参考 brainstorming 把这个需求变成设计 spec`、`实现前先讨论设计`
- 适合：问题基本成立，但还没确定产品方案、信息架构、交互路径、技术切分或交付 spec，需要先探索 2-3 个可选设计并得到用户确认
- 不适合：问题还没定义清楚，改用 `ai-collaboration-calibration`；已有明确方案要被拷问，改用 `grill-me`；已经要写正式 PRD，改用 `prd-architect`

## Overview

使用这个 Skill 把“可讨论的想法”推进成“可交付给 PRD、mockup 或开发计划的设计 spec”。它强调先理解上下文、逐步澄清、提出多个方案、确认设计，再进入下游 artifact。

它的默认下游可以是 `prd-architect`、`ui-mockup-desktop-workbench`、`prd-to-issues` 或实现计划；如果方案涉及 UI/mockup/HTML 可视化，必须先对齐项目已有视觉语言，避免生成与真实产品割裂的通用页面。需要反复压测时显式进入 `$solution-loop`，而不是创建新的方案 mega Skill。

本 Skill 是方案 Maker：拥有真实备选、推荐与取舍、scope、流程、状态、风险和 Design Delta；不拥有 Critic clearance、PRD/实现 readiness 或发布审批。

## Boundary

先判断用户当前阶段：

- 问题、目标用户、成功标准或约束还不清楚：转 `ai-collaboration-calibration`，不要急着给方案。
- 问题已基本成立，但方案、路径、范围、交互或系统设计还没定：使用 `brainstorming`。
- 用户已经有一个具体方案，想找漏洞、压测失败模式或挑战取舍：转 `grill-me`。
- 用户明确要 PRD 文档、PRD 模板、PRD 图示或正式需求章节：转 `prd-architect`。
- 用户已有 PRD/handoff，要判断能否开发、可测试、可交付：转 `prd-review`。
- 用户已有 PRD 和 UI 规范，要真实桌面端 mockup：转 `ui-mockup-desktop-workbench`。
- Product Work Graph 的方案发散节点：使用 PUBLIC unqualified `brainstorming`。只有用户显式调用完整名称 `superpowers:brainstorming` 时才走该 plugin Skill；不得从未限定的 “brainstorming” 推断它。

## Hard Gate

在用户确认设计前，不要做以下事情：

- 不写生产代码。
- 不创建完整 PRD。
- 不生成正式 GitHub issues。
- 不把方案包装成已经确定的结论。
- 不进入 Superpowers `writing-plans` 或其他实现计划。

简单需求也要经过轻量设计确认。确认可以很短，例如：“我建议按方案 B 做，范围只包含 X/Y，不做 Z。你确认后我再写 PRD-lite。”

## Workflow

1. **复述目标和阶段**：用一句话说明用户想解决的问题，以及当前是“方案脑暴”而不是执行。
2. **读取可发现上下文**：如果有 PRD、调研文档、代码、截图、UI 规范或历史讨论，先读；不要把可查信息问给用户。UI/mockup 相关任务还要读取 `references/visual-design-standards.md`。
3. **判断是否需要转路由**：按 `Boundary` 决定是否继续本 Skill。
4. **澄清关键缺口**：一次只问一个会改变方案的问题。优先问目标用户、成功标准、边界、约束、已有资产和不可接受方案。
5. **提出 2-3 个方案**：每个方案必须包含适用前提、优点、代价、失败风险和不选理由。
6. **给出推荐方案**：明确推荐哪一个，或者推荐组合方案，并说明理由。
7. **分段确认设计**：按“范围 / 核心流程 / 信息结构或系统结构 / 异常与人工介入 / 验收口径”拆开确认。复杂设计可以逐段问用户是否认可。
8. **输出设计 spec**：根据任务复杂度输出轻量或标准 spec。需要写文件时，先确认保存位置；默认不强制创建特定目录。UI/mockup 相关 spec 必须包含项目视觉规范发现摘要，或说明启用的默认视觉标准。
9. **自检 spec**：检查 TBD、矛盾、范围漂移、双关要求、缺少验收标准和未关闭待确认项。
10. **交接下游**：按用户目标建议下一步：写 PRD、做 mockup、压测方案、拆 issues 或进入实现计划。

## Context Intake

开始脑暴前，优先从已有材料提取输入，不要重复问用户已经给过的信息：

- 用户原始表达：想解决什么、为什么现在讨论、希望先不要做什么。
- 目标对象：用户角色、业务场景、当前产品阶段、上下游协作者。
- 已有材料：PRD、调研结果、竞品截图、代码路径、UI 规范、历史会话和本地文档。
- 决策边界：本轮要选方案、定范围、定流程、定技术路径，还是准备 PRD / mockup / implementation plan。
- 约束条件：时间、人力、平台、权限、数据、合规、离线/在线、移动端/桌面端、是否必须兼容现有能力。
- 输出期待：口头讨论结论、设计 spec、文件落地、下游 Skill handoff，或只是帮用户继续想清楚。

如果以上信息缺失，只问会改变方案分支的问题。缺失但不阻塞的问题写入假设或待确认项。

## Question Discipline

- 一次只问一个问题。
- 如果能从本地文件、网页截图、已有会话或用户提供材料中查到，先查证。
- 每个问题都要说明它会影响哪个设计分支。
- 多选优先，但不能把真实开放问题伪装成多选题。
- 如果用户要求“先不要问，直接给方向”，可以基于显式假设给第一版方案，但要标记假设。

## Design Options

提出方案时用这个最小结构：

```markdown
### 方案 A：<名称>
- 适合前提：
- 核心做法：
- 优点：
- 代价：
- 主要风险：
- 不选它的理由：
```

推荐方案必须回答：

- 为什么它更贴合当前目标。
- 它舍弃了什么。
- 哪些前提一旦变化，推荐会被推翻。

## Output

轻量场景输出：

```markdown
**Brainstorming Summary**
- 当前问题：
- 推荐方案：
- 不做范围：
- 关键流程：
- 主要风险：
- 待确认：
- 下一步：
```

复杂场景输出正式设计 spec。读取 `references/design-spec-contract.md`，按任务规模选择章节，不要机械展开所有章节。

## Visual Companion

如果接下来讨论的是 UI、信息架构、流程图、布局、页面状态或 HTML mockup，先判断可视化是否真的能帮助决策。不要把“视觉 companion”当成默认模式；概念、取舍、范围和问题定义仍然用文字更高效。

适合可视化的情况：

- 页面布局、导航结构、表单状态、工作台布局。
- 多方案 UI 对比。
- 流程图、状态机、系统边界图。
- 已经要把设计 spec 交给 `ui-mockup-desktop-workbench` 或原型实现。

不适合可视化的情况：

- 目标用户、成功标准、范围边界、商业取舍。
- 单纯列需求、写 PRD、审 PRD。

进入 UI/mockup/HTML 可视化前，必须执行 Design Discovery Gate：

1. 先查项目内已有视觉语言：框架配置、全局样式、设计 token、主题文件、组件库、图标系统、目标 route/page shell、相邻页面状态、已有截图或 mockup。
2. 在生成视觉稿前，用 5-8 条 bullet 摘要已经发现的约束，例如色彩、字体、间距、圆角、导航结构、组件库、深浅色策略和状态样式。
3. 优先复用项目本地 token、组件、布局比例、图标风格和状态模式；不要从空白通用模板重新发明一套视觉语言。
4. 如果找不到项目本地规范，选择一个默认标准：`SaaS/Admin Workbench`、`Desktop Agent Workbench`、`Research Dashboard` 或 `Marketing/Consumer`，并说明为什么选它。
5. 生成 mockup 时必须覆盖真实状态：empty、loading/busy、streaming/progress、success/result、error/retry、disabled/permission 中与场景相关的状态。
6. 不生成泛 AI 风格的装饰性页面：避免无业务含义的大渐变、装饰 blob、过度 hero、巨型嵌套卡片和只为好看而存在的元素。

需要可视化落地时，读取 `references/visual-design-standards.md`，并把其中的质量门禁作为完成前自检。

## Handoff

需要把版本化方案交给 `grill-me`，或消费 Critic 返回的单一设计 gap 时，先读取 `references/maker-handoff-contract.md`。

- 单点调用输出方案或 Design Spec 后停止；`next_owner` 只是建议，不自动运行 Critic、PRD、issues 或实现计划。
- Maker 只输出 `design-confirmation-needed`、`critic-ready`、`revision-required` 或 `owner-confirmed`；不得自称 `clear`、`ready`、`approved` 或已经通过压力测试。
- Critic return 必须引用准确 artifact/version、一个 gap、closure criterion、preserved items 和 resume point；只修改受影响部分并返回 Design Delta。
- 同一 challenge 完成两轮回流后仍未关闭或缩小时，停止自动回流并进入 Human Gate。

根据设计成熟度选择下游：

- 要写正式需求文档：交给 `prd-architect`。
- 要挑战已经选定的方案：交给 `grill-me`。
- 要评审已有 PRD：交给 `prd-review`。
- 要做桌面端真实页面 mockup：交给 `ui-mockup-desktop-workbench`。
- PRD 已 ready，要拆 implementation issues：交给 `prd-to-issues`。
- 要进入代码实现计划：交给 Superpowers `writing-plans`。

不要自称已经完成下游交付物，除非真的执行了对应 Skill 或产物流程。

## Definition of Done

- 用户的问题阶段被正确识别，没有把模糊问题误当成已确认方案。
- 已探索 2-3 个合理方案，或明确说明为什么只有一个合理方案。
- 推荐方案写清了取舍、风险和可推翻前提。
- 用户已确认设计，或待确认项被明确列出且没有伪装成确定结论。
- 已给出适合当前阶段的下一步 Skill 或 artifact。

## Evaluation

Smoke prompts:

- `先不要写 PRD，帮我把这个功能脑暴成几个设计方案。`
- `参考 brainstorming，把这个桌面端需求先变成设计 spec。`
- `实现前先讨论下这个功能怎么设计比较好。`
- `这个想法基本成立，帮我比较 2-3 个落地路径。`

Non-trigger prompts:

- `我还没想清楚真正问题是什么，先帮我想想。`
- `拷问一下这个已经定好的方案。`
- `直接帮我写 PRD。`
- `基于这个 PRD 生成 GitHub issues。`

Regression checks:

- 不应跳过用户确认直接写代码或实现计划。
- 不应和 `ai-collaboration-calibration` 重复做问题定义校准。
- 不应和 `grill-me` 混淆，把成熟方案压测当成方案脑暴。
- 不应把轻量方案讨论机械扩展成重型 PRD。

## Resources

- `references/design-spec-contract.md`：正式设计 spec 的结构、轻重选择和自检清单。
- `references/maker-handoff-contract.md`：Maker 单点停止、Critic handoff、Design Delta 与 Human Gate 合同。
- `references/visual-design-standards.md`：UI/mockup/HTML 可视化前的项目规范发现、默认视觉标准和质量门禁。
- `scripts/check_design_spec.py`：检查设计 spec 是否包含当前问题、推荐方案、不做范围、风险和待确认项。
