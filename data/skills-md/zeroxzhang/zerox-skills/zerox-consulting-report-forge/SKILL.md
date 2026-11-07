---
name: zerox-consulting-report-forge
description: >-
  Create evidence-led consulting reports for strategy, market research, operating reviews, investment analysis, and qualitative research. Combine business analysis, a coherent argument, precise visual exhibits, and reading-oriented layouts. Use for Chinese or bilingual decision reports and thoughtful restructuring of approved content. Produce self-contained HTML plus matching PDF with the bundled toolchain. Do not use for a single chart, poster, pure copyediting, PPTX, or mechanical format conversion.
---

# 咨询报告制作

目标是可核查、可阅读、能支持判断的报告。默认中文、16:9、阅读模式、自包含 HTML + 同版 PDF；用户指定的语言、画幅、品牌、页数和范围优先。不要承诺“完美”或把检查通过等同于咨询质量。

## 固定前置约束

1. **图表多样性：必须尽可能多地使用不同类型的图表。** 在证据适配、表达准确、阅读清晰的前提下执行。必须主动探索适用形式，不能因为少数常用图型已经能够表达内容，就停止考虑其他合适的图型；不能仅因熟悉、已有组件或实现方便而反复套用。
2. **版式布局多样性：必须尽可能多地采用不同的版式来组织每一页的内容。** 在内容适配、阅读顺畅、视觉规范统一的前提下执行。必须从整册角度统筹空间组织与阅读节奏，让主辅关系、空间组织和阅读路径产生有意义的变化，不能因为某种布局方便复用就反复套用。
3. **模块填充：必须逐一检查正文每页的每个模块及每一栏，尤其是文字模块；没有明确设计功能的大块留白必须修复，裁切和溢出必须消除。** 同时检查上下与左右空白；预留空白须说明位置、用途与依据。不能用整页看起来饱满、模块背景铺满或一句“合理留白”代替检查。按 [模块填充协议](references/module-fill.md) 规划、修复并留下当前 HTML 与实际 PDF 的逐区域记录。

**“尽可能多”是必须主动追求的目标，适配性是边界。** 保留重复须有具体的比较、内容或阅读需要；“内容适配”“保持统一”不能成为回避多样性的笼统理由。不设统一种数配额，不为增加种数虚构数据、重复证据或损害可读性；改颜色、换实现名称和微调尺寸不算实质变化。这两条贯穿蓝图规划、制作与最终验收，整册多样性不等于每页堆更多图。

## 工作方式

主笔负责总判断、方法选择、整篇标题链和最终成稿。仅在研究、计算、领域知识出现明确缺口时启用相应专家；复杂或重大材料另需实际独立实例审查。分工、输入输出和隔离要求见 [协作协议](references/collaboration.md)。没有可用的独立实例时，继续完成可做的工作并如实报告未独立验收，不能以换角色提示词冒充。

开始时简要说明目标、材料缺口、预计页数范围及验收方式，然后直接工作。已知信息不重复问，阶段节点不要求用户批准。只在答案会改变任务方向且无法从材料确定时提问。**发现重要缺口时，必须按 [缺口与询问协议](references/analysis-workflow.md#3-缺口触发与路由每一阶段都执行) 登记并路由；需要用户补充的信息，调用当前模式允许的输入工具，或用普通消息提问并等待实际答案。暂停依赖分支，同时推进无依赖工作。空回复、超时与默认选项未提交都不能当成答案。**记录主要阶段实际耗时、返工原因及可得的资源消耗；未测量不承诺固定用时。长报告先做代表页，不要求每完成一页都重建整册。

## 强制执行清单

所有新任务用 `node scripts/report.cjs init /任务/新报告 --work-mode analytical` 创建（模式按任务选择 editorial、analytical 或 exploratory），采用 schema3 / task3 / semantic-v2。目标、范围、交付要求与报告路线足以确定下一步时，**先按 [执行清单协议](references/execution-checklist.md) 激活持久 Checklist，再开展实质研究、委派与制作**；未知事项保留，不等待所有研究结论齐备才建清单。`execution-plan.json` 是跨阶段进度的权威记录，宿主 todo 仅为可选镜像。

主 Agent 在分派、接收、阶段完成、返工和交付前更新计划，核对当前 attempt 与证据后接收子任务，不能凭完成通知勾选。中断或上下文压缩后先运行 `node scripts/report.cjs resume task.json`，核对产物、待办、阻塞、未知运行状态及固定要求。

新建任务使用 `execution-plan-2`，将 `chart-diversity`、`layout-diversity`、`module-fill` 三项固定约束独立展示，不能删除、取消、跳过、标记不适用或合并隐藏。规划、代表页及最终整册审查分别提供依据；短报告、定性材料和 editorial 模式也不豁免。发生输入或证据变化时重新核实，不沿用失效勾选。历史 `execution-plan-1` 继续按原双约束合同核验。正式制作门禁检查清单前置条件；打包后归档执行状态，实际交付后再记录交付完成。

## 1. 确定问题与证据边界

确认读者、用途、核心问题、期间、对象、可用证据及限制。三种工作模式：

- `editorial`：已确认内容的组织与重排，保留原意，不擅自增加新结论。
- `analytical`：需要计算、比较、建模或判断，先校验方法及口径。
- `exploratory`：开放研究，允许以有限发现、未知和下一步验证收束，不强造投资建议或行动页。

用户材料先核对原文；本地材料已提供不等于外部事实已核实。公开信息出现重要缺口时，在用户范围内自动启动外部调研；内部数据、目标或取舍缺口向用户询问，机制贯穿研究、分析与审查。把影响判断的主张区分为事实、估计、预测、假设、建议，记录来源、期间、对象、分母、单位、计算与限制。未知不填零，样本不当市场，相关性不当因果。

## 2. 选方法，完成分析

分析与探索先读 [统一分析流程](references/analysis-workflow.md)，登记 brief、issues、workItems、gaps；按[方法路由](references/analysis-methods.md)选择解决问题的最少方法组合，核对其前提、口径与推论边界。产出须是可检验的关系，不只列框架名称。必要计算可复算，预测及情景不冒充历史事实，描述性比较不自动证明因果、生产率或盈利。

## 3. 形成标题链与统一蓝图

先把有条件的核心答案写在全局 claims，并以 `analysis.synthesis.answerClaimRefs` 引用；schema3 的 `governingThought` 由它派生。再按 [叙事方法](references/consulting-storyline.md) 形成“问题—证据—判断—边界”的推进。标题连读应有完整论证；每页 `proves` 对应画面能证明的关系。证据不够就缩小结论，不用强词弥补。

按[内容制作合同](references/content-authoring.md)填写 init 生成的蓝图；[研究模板](templates/research-blueprint.json)可先无页面，[蓝图模板](templates/deck-blueprint.json)提供字段示例。蓝图是标题、主张、来源、计算、密度和页面意图的权威源；`pages.json` 由编译器生成，不维护第二套内容。

标题链确定后、ready 与代表页制作前，必须按[整册图表与版式规划](references/content-authoring.md#整册图表与版式规划)核对证明任务、图型、布局及重复理由，主动寻找尚未使用且适配的表达与阅读结构，落实两项多样性要求；不能逐页选完就直接批量制作。

同步按[模块填充协议](references/module-fill.md)完成 `module-fill-plan`：逐模块、逐栏匹配真实内容与容量，说明弹性图形、固定锚点及预留空白。基线填充率只辅助选型，不从拉伸后的容器高度反推。

新稿按[严格合同](docs/strict-analysis-contract.md)执行，前置审查 v2、最终审查 v5。旧稿继续原合同，不自动改算法、补签或转换版本。统一入口、任务锁、多页参考资料和审查包见[生产入口](docs/upgrade-production-entry.md)。

analytical / exploratory 先校验综合，再按[签署步骤](references/analysis-review.md)完成前置审查并绑定 task；editorial 免此前置记录。复杂或重大材料须实际独立实例复核。完成三项规划后运行正式生产门：

```sh
node scripts/deck_blueprint.cjs /任务/deck-blueprint.json --task /任务/task.json --stage synthesis
# 完成适用的前置分析审查并绑定 task.analysisReview 后：
node scripts/deck_blueprint.cjs /任务/deck-blueprint.json --task /任务/task.json --ready
node scripts/report.cjs compile /任务/task.json
```

正文页必须登记关键主张；标题、身份、口径限制、来源和指标以可见 `data-content-key` 叶节点进入成稿，由装配填值、最终 QA 复核。未完成适用的前置审查时，ready 用 `--preview`、统一编译入口用 `--preview true`，产物仅称预览。前置审查不是用户审批，也不替代最终审查。

## 4. 从证据关系选择表达与布局

先说明本页证明什么、各证据的贡献及其对照、拆解、递进或互补关系，再展开图形与布局候选，结合整册已用形式主动增加有效多样性；容量不足就重排。只有证明分工变化才增加展品，单图仍有效；不为格子或结构字段补造证据，也不找到第一个可用模板就停止选型。

在 `visual.selection` 写证据关系与具体选型理由；实质备选用 `alternative/tradeoff` 成对记录。已登记容量规则的形式须填 `visual.capacity` 计划计数，ready 与最终 QA 核对关系、上限及实际容量；理由是否成立仍须看图判断。字段和允许值查询见[内容制作合同](references/content-authoring.md#编译并填充叶节点)。

- 目录布局是经过测量的原型：按需读 `assets/layout-atlas/catalog.json`，用 `layout_contract.measure()` 检查尺寸；选择后保留其模块和几何合同。
- `visual.layout: "custom"` 是正常路线：声明阅读区域，自己写 CSS，接受相同的可读性、溢出、证据和打印检查。
- 自绘 SVG 必须说明实际语义。瀑布统一从权威原始输入经内核诊断，起点、增量、终点必须闭合；示意图也不能出现错误加减关系。
- `diagram.*` 按[图示语义合同](references/diagram-semantics.md)声明并核对节点、边和角色。
- 同类分面、连续同型图和表格可用于真实比较，但须写具体理由；无必要重复及遗漏适配变化机会仍须修订，不能以没有种数门槛为由跳过多样性。

高级视觉策略按需显式启用，均不改变默认策略与历史合同：

- `evidence-composition-1`：登记逐展品证明分工、组合关系与跨图量尺；单图也是有效组合，阅读入口与布局 primary 独立。
- `narrative-focus-1`：继承组合合同，另核对 `deck.arc`、逐页新增理解 `adds`、核心答案承载页与唯一 `data-reading-role="takeaway"`。一页只讲一件事；副标题给口径，正文不大过标题，声明的重点须与画面一致。

新建用 `node scripts/report.cjs init <目录> --visual <策略名>`；已有任务用 `node scripts/migrate_strict_analysis.cjs <task.json> <新目录> --to-policy <策略名>` 生成待审稿。启用前读[单页系统](references/consulting-page-system.md)、[叙事方法](references/consulting-storyline.md)及[前置审查覆盖](references/analysis-review.md)；字段、量尺和最终审查合同由这些文档定义。

选型见[表达指南](references/expression-guide.md)与[形式容量目录](references/form-capacity.md)，区域、密度和类名见[单页系统](references/consulting-page-system.md)。用 `node scripts/sweep_forms.cjs` 查询组件；也可写原生 HTML 表格、自绘或生成静态 SVG。目录不是能力白名单，组件上限不是全局禁令。禁止伪 3D、无意义色条、未说明截轴、仅靠颜色或悬停传达关键内容，以及微字塞页。

## 5. 代表页收敛后批量生产

先做 2–3 张能够暴露不同风险的代表页：核心定量页、最密或最复杂页、定性/行动页。少于此规模时直接做全部。实际预览确认主图、支持证据、口径、字号、留白与来源安全区，并逐一检查文字模块和子栏的内容分布，再扩展全篇；保留合理重复的视觉语言。

依 [静态 HTML/PDF 路线](references/static-html-pdf.md) 使用 init 已生成的 `task.json`，核对 blueprint 与编译 pages 的绑定；不要另建任务覆盖计划身份。首次环境运行或依赖变化时完成字体与能力探测；可复用已验证环境。制作期只预览受影响页，整册成形后做 smoke；不为每页导出一遍完整 PDF。

## 6. 验收和修订

工程验证与判断审查各有边界，二者都要完成：

1. **分析**：标题是否被支持，方法前提、分母、身份、边界与反证是否正确。字段齐全不能证明结论成立。
2. **视觉**：实际查看最终 HTML/PDF 每页，确认关系、限定与来源可读。按[整册多样性验收](references/visual-qa.md#整册多样性验收)和[模块填充协议](references/module-fill.md)分别审查三项固定要求，处置重复及遗漏的变化机会，逐模块、逐栏记录空白用途、缺陷与复检，补齐自动枚举遗漏。重点重看最密、最大空白、最复杂图、来源最多与最强结论页。
3. **工程**：`qa_deck.cjs --tier acceptance` 核对绑定、布局、溢出、字体、打印、离线和最终证据；自动检查不替代读图。
4. **交付**：作者记录实际所见；复杂或重大材料另由独立实例记录审查，简单且无重大结论的任务可仅作者审查。处置 warnings；合并 review 后打包。未解决 major/blocking 问题不称完成，需要独立审查但未完成时不冒充正式交付。

具体命令与记录格式见 [静态路线](references/static-html-pdf.md) 和 [视觉验收](references/visual-qa.md)。首次完成审查后，使用 [审查快照与复用](references/review-reuse.md) 冻结原稿、证据与审查链。局部修订可准备继承草稿；变化页和全局判断仍须真实复核，工具不会预填 PASS。

完成时给出 HTML/PDF、主要结论或变更、验证范围与尚存限制。没有做同题同模型对照实验，不声称未经测量的提速比例或总体优势。

## 按需参考

| 任务 | 文件 |
|---|---|
| 分阶段分析与询问暂停恢复 | [analysis-workflow](references/analysis-workflow.md) |
| 前置审查与版本绑定 | [analysis-review](references/analysis-review.md) |
| 业务方法与适用边界 | [analysis-methods](references/analysis-methods.md) |
| 专家分工与独立审查 | [collaboration](references/collaboration.md) |
| 总判断、标题链、有限结论 | [consulting-storyline](references/consulting-storyline.md) |
| 蓝图、计算、可见内容绑定 | [content-authoring](references/content-authoring.md) |
| 来源与主张身份 | [evidence-ledger](references/evidence-ledger.md) |
| 瀑布数据与诊断 | [waterfall-bridge](references/waterfall-bridge.md) |

## 归因

运行时基于 Zerox Zhang 的 `consulting_deck_skill_concise` 重组，遵循 Apache-2.0，保留 [LICENSE](LICENSE)。瀑布数据判据端口自 `aeolus-period-waterfall` 的诊断逻辑；是规则移植，不依赖其目录。
