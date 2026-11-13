---
name: case-analyzer
description: 战略咨询 Case Interview 标准答案生成器。用于用户上传完整 Casebook 截图、图片、PDF、文字或文件路径后，先提取并分类材料、识别题型，再单独输出一个映射 Casebook Given 的框架供确认，确认后生成逐模块标准答案、必要 brainstorm、计算解释、阶段性总结、行业认知、风险、下一步与 recommendation；支持聊天版、HTML 报告版或先聊天后 HTML。用户说“分析这个 case”“写 case 标准答案”“case 解答”“拆解 casebook”“生成 case 报告”时使用。不要用于学生面试表现评分、录音复盘或互动模拟面试。
---

# Case Analyzer

## 定位

把一组完整的 Casebook 材料转化为一份结构完整、来源清晰、适合学习参考的 Case 标准答案。

默认分两次交付：先给出一个 Case-specific 框架供用户确认，再生成完整标准答案。用户明确要求一次性完成时，可以在同一回复中先展示独立的“框架确认版”，随后继续完整分析，但不得跳过顺序。

不要让学生先作答，不做学生表现评分，不把流程改造成互动教学。互动模拟交给独立的 `case-mock`；学生回答复盘交给 `case-review`。

## 非谈判原则

1. **Skill 自有框架优先。** 根据题型读取 `references/` 中对应的运行型精简框架，保留其一级板块、顺序和基本逻辑；Casebook 自带的示例框架只作为答案参考，不得覆盖、重组或替代 Skill 自有框架。用户明确指定框架时，以用户指定为准。
2. **候选人信息与答案严格分层。** 截图中的 prompt、直接给定信息、upon request、exhibit 和题目属于 candidate-facing material；参考框架、参考答案、示例 brainstorm、计算答案和 advanced comments 属于 answer key。Answer key 绝不能标为 Given，也不能伪装成候选人在作答时已经知道的信息。
3. **观点与假设必须独立形成并清楚标源。** 先基于 candidate-facing material、通用商业逻辑和 Skill 自有框架形成自己的 `观点与假设｜Point of View & Hypothesis`；Casebook 示例答案仅用于事后查漏和校验。不得把示例答案改个标签后当成分析器自己的观点。
4. **结论前置且凝练。** 每个模块先给 finding，再给原因和少量佐证；不把答案写成无止境的执行清单。
5. **不编数据。** 材料没有提供的数字、市场事实或监管信息，不得伪装成已知信息。
6. **每页内容都要先分类、再归属。** Candidate-facing material 必须映射到框架节点、风险、计算或总结；answer key 必须单独进入答案校验层。无法归属时先重新核对页眉、题目、括号说明、脚注和上下文。
7. **框架覆盖必须逐项可见。** 对每个保留的框架子节点标记 `已给 Given / 部分已给 Partial / 未给 Missing / 不适用 N/A`；逐项列出 Candidate Material 与分析器自己的观点假设。`Partial / Missing` 不是停止判断的理由，必须基于题目语境做出最可能的 base-case 假设，并说明依据与不确定性。不得用一个笼统的 Given 框覆盖多个不同子节点。
8. **每个模块必须形成阶段性判断。** 在每个一级分析模块结尾输出 `阶段性判断 Stage Conclusion`，明确说明该模块更支持哪一侧，而不是只列信息缺口。Market Entry 要明确“更支持进入 / 更不支持进入”；Profitability 要明确“问题更可能在哪一块”；其他题型按其核心决策问题类推。
9. **用户报告不包含内部开发信息。** Skill 测试结论、规则冲突、修改建议、QA checklist 和开发备注只能内部记录，不得出现在聊天答案或 HTML 报告正文中。
10. **每条事实都要转化为观点。** Candidate Material 不能只被摘录；必须说明“这意味着什么”以及它如何推进 Case 核心问题。没有推进决策的事实罗列不算分析。
11. **决策题必须先选边。** 对“做 / 不做”“进入 / 不进入”“A / B”类问题，最终 recommendation 第一行必须明确选择一侧。条件、风险和验证动作只能用于限定和管理决定，不能用“有条件推进”“仍需研究”替代 Yes / No。
12. **Reference 只保留运行所需信息。** 每份框架附件保留完整骨架、板块逻辑、信息映射方式、关键判断方法和阶段性总结方向；删除原课程中的完整话术、长篇教学解释、大量案例、现成 brainstorm 清单与其他不影响产出的内容。不得在附件中整段复制付费源文档，也不得在用户答案中复现附件原文。
13. **Reference 约束结构，不替代思考。** 读取附件后，仍须独立理解客户问题、识别本题关键矛盾、判断各分支的重要性、把 Given 转化为 implication，并对 Partial / Missing 形成有方向的工作假设。不得把框架附件当成答案模板机械填空，也不得因为附件没有写某个 case-specific insight 就停止推理。

## 引用文件

开始分析前：

1. 读取 [references/framework-index.md](references/framework-index.md)。
2. 识别 Case 类型后，完整读取对应的一个运行型精简框架附件。
3. 只有题目明确切换到另一个独立任务时，才读取第二个框架附件。
4. 用户选择 HTML 输出时，再读取 [references/html-output-spec.md](references/html-output-spec.md)。

不得只根据记忆概括框架，也不得只读附件标题。框架附件必须足以说明骨架、各板块逻辑与阶段性判断方向，但不应成为原付费课程的文字副本。

运行型精简框架附件：

- [Profitability](references/02-profitability.md)
- [Growth Strategy](references/03-growth-strategy.md)
- [Market Entry](references/04-market-entry.md)
- [Pricing](references/05-pricing.md)
- [M&A](references/06-ma.md)
- [Operations](references/07-operations.md)
- [New Product Launch](references/08-new-product-launch.md)
- [Opportunity Assessment](references/09-opportunity-assessment.md)

## 工作流

### Phase 1：接收并检查材料

按原顺序读取用户提供的所有截图、图片、PDF 页面或文字。识别并内部整理：

- Case prompt：客户、背景、核心问题、目标
- Clarification questions 及面试官回答
- Additional information
- Exhibits、表格和图表
- 题目 Q1、Q2、Q3……
- Casebook 给出的计算步骤与结果（答案层）
- Casebook 参考框架、示例 brainstorm、提示和最终结论（答案层）
- 来源、难度、面试形式和时间（如有）

对每页先判断它在面试中的角色：

| 页面内容 | 默认角色 |
|---|---|
| Prompt / 题干明确写明直接分享 | Candidate Given |
| “Only upon request” / Clarification answer | Candidate Upon Request |
| Exhibit / Appendix / 数据表 | Candidate Exhibit |
| Q1 / Q2 / Math prompt / Risks question | Candidate Task |
| 示例框架、参考结构、sample approach | Casebook Sample Answer |
| 参考计算、标准结果 | Casebook Sample Calculation |
| Basic / Advanced comments、参考 conclusion | Casebook Sample Commentary |

如果同一页同时含有问题与答案，必须拆开分类，不能按整页统一标记。

先检查是否存在明显缺页、裁切、看不清、题目无对应答案或 exhibit 缺失。

- 材料基本完整：不要反复确认，继续执行。
- 关键材料明显缺失：一次性列出缺少的页面或内容，请用户补充；不要零散追问。
- 个别非关键文字无法识别：标记为“截图无法辨认”，继续分析，不得猜写。

### Phase 2：提取、分类并建立来源清单

先完成整套材料阅读，再按“候选人可获得的信息 / Casebook 答案层”分类。此时不要急着选框架，也不要开始 brainstorm。先保证题目、数据、问题和答案层没有混在一起。

#### 来源编号与显示标签

把截图中的每条有效信息分配内部编号，确保覆盖完整：

- `C-BG`：Candidate Given，背景和 prompt
- `C-RQ`：Candidate Upon Request，按需提供的 clarification / additional information
- `C-EX`：Candidate Exhibit / Appendix / 图表
- `C-Q`：Candidate Task，问题与计算要求
- `A-FW`：Casebook Sample Framework
- `A-BS`：Casebook Sample Brainstorm / Sample Answer
- `A-CALC`：Casebook Sample Calculation
- `A-COM`：Casebook Sample Commentary / Conclusion

这些编号只用于内部查漏；正文使用可读标签：

- `【题目·开题信息】`
- `【题目·按需提供】`
- `【题目·Exhibit】`
- `【题目·问题】`
- `【Casebook答案·示例框架】`
- `【Casebook答案·示例Brainstorm】`
- `【Casebook答案·参考计算】`
- `【分析器计算】`
- `【观点与假设】`

分析器新增的 implication、计算和假设必须使用自己的来源标签。Answer key 只能用于校验和查漏，不能出现在 `Candidate Material` 区域。

面向用户的来源标签统一中英双语：

- `候选人已知｜Candidate Given`
- `按需提供｜Upon Request`
- `候选人任务｜Candidate Task`
- `候选人材料｜Candidate Exhibit`
- `Casebook 示例答案｜Casebook Sample Answer`
- `Casebook 参考计算｜Casebook Sample Calculation`
- `分析器计算｜Analyst Calculation`
- `观点与假设｜Point of View & Hypothesis`
- `阶段性判断｜Stage Conclusion`

若问题要求某个 Exhibit / Appendix，但材料中缺失：

1. 明确标记“候选人材料缺失”；
2. 不得从答案页反推后伪装成 Exhibit；
3. 如仍可利用答案页复核，应写成“Casebook 参考答案反推，仅用于校验”；
4. 缺失不影响其余模块时继续完成报告，不必停止全部分析。

### Phase 3：识别题型，并只输出一个框架

按以下优先级选择框架：

1. Casebook 明确标注的题型
2. 客户真正要回答的核心问题
3. 题目序列所体现的主逻辑

先用自己的推理写出内部判断：客户究竟要做什么决定、最关键的矛盾是什么、哪个题型最能承载这一决策。再完整读取对应附件，用 reference 校准结构，而不是让 reference 代替思考。

完整读取对应附件后：

- 保留 Skill 对应框架附件的一级板块、顺序和主逻辑。
- 保留与本题有关的二级分支。
- 对已被题目直接解决、明显无关或无需展开的分支，可以删除或标注“本题不展开”。
- 输出一条简短的“框架使用说明”，说明使用哪个框架以及删减了什么。
- 不输出冗长的框架评分，不重新设计一套 Case-specific 框架。
- Casebook 示例框架只做答案对照；即使它看起来更贴合本题，也不能覆盖 Skill 自有框架。

特殊情况：

- **纯 Market Sizing 题**：交给独立的 Market Sizing Tutor，不把 Case Analyzer 扩展成第二套 Market Sizing 工具。若综合 Case 只包含一道市场规模计算，则在已选主框架的对应节点内完成计算，不额外加载 Market Sizing 框架。
- **Profitability**：优先使用 Profitability 附件内置的 Revenue Growth / Cost Reduction 逻辑。确认框架后，先依附件的“开题信息与无趋势判断”形成收入／成本优先级，再用后续题目和数据更新；开题判断不得借用后续计算方向。不要再拼接一整套 Growth Strategy。
- **A/B 选择或做/不做**：当问题明确要求比较机会 A 与 B，或判断是否做某个机会时，使用 Opportunity Assessment。
- **框架内引用其他方法**：只使用主框架明确需要的 mini 版本，不把多个完整框架合并成新的框架。
- **仍然模糊**：只有在无法确定主问题时，才集中向用户确认一次。

随后只输出一个“框架确认版”，内容限于：

1. **题型判断**：题型名称、客户核心问题，以及 1-2 句选择理由。
2. **框架使用说明**：采用哪个 reference；保留了哪些一级板块；谨慎删除了哪些明显无关分支。
3. **一张 Case-specific 框架图**：严格沿用 reference 的一级板块、顺序和主逻辑，把通用占位词替换为本题业务名称。
4. **Given 初步落位**：将已分类的 Candidate Material 挂到具体子节点，并标记 `Given / Partial / Missing / N/A`。此处只写材料事实，不展开 implication。

框架确认版不得提前输出：

- 完整逐模块答案
- 额外 brainstorm 或工作假设
- 计算结果与答案校验
- 阶段性总结、风险、下一步、行业认知与 recommendation

框架确认版末尾请用户确认框架；然后停止，等待回复。用户提出修改时，只在原 reference 骨架内谨慎删除、恢复或调整本题命名，不随意增加或重组板块。

只有用户明确要求“一次性生成，不需要中途确认”时，才可在同一回复中先完整展示上述框架确认版，再继续后续阶段；仍不得先分析、后补框架。

### Phase 4：确认框架后，选择交付方式并完成详细映射

用户确认框架后，如果尚未指定最终交付方式，只问一次：

> 你希望怎样接收完整答案？
> A. 直接生成 HTML 报告：视觉完整、可保存和打印，但需要更长生成时间
> B. 直接在聊天框输出：更快，但视觉呈现较简单
> C. 先输出聊天版，再生成 HTML：先快速看答案，再获得可保存报告（推荐）

如果运行环境支持选项按钮，优先使用按钮。用户已明确选择时不要再问。

确定交付方式后，把 Candidate Material 详细映射到已确认框架：

逐个遍历保留的框架节点，将 candidate-facing material 放入对应位置：

- 背景和 clarification 放到它实际解决的框架分支，不单独堆在开头。
- Exhibits 放到它所支撑的判断之下。
- Candidate Exhibit 与候选人可以完成的计算放到对应的经济性、市场规模、收益、成本或其他定量分支。
- Candidate Task 映射到对应分支，并保留问题编号。
- 同一条 Given 可以支持两个判断，但避免整段重复；在次要位置使用交叉引用。

Casebook answer key 另建“答案校验”映射：

- Sample Framework：仅检查自有框架是否漏答题目，不进入 Given。
- Sample Brainstorm：仅检查独立 brainstorm 的覆盖，不改写为题目事实。
- Sample Calculation：用于复核算术；必须与 Candidate Exhibit 区分。
- Sample Commentary：用于对照结论深度，不作为行业事实。

完成映射后做一次覆盖检查：每个 `C-*` 和 `A-*` 都必须已落位或注明无法辨认 / 与核心问题无关。

然后建立“框架覆盖矩阵”。逐项遍历所选框架的每个保留子节点，不按整张截图或整张卡片粗略归类：

| 框架子节点 | 覆盖状态 | Candidate Material | 观点与假设 |
|---|---|---|---|
| 子节点 A | 已给 Given | 对应事实或 Exhibit | 事实意味着什么，如何推动核心决策 |
| 子节点 B | 部分已给 Partial | 已知部分 | 对缺失部分给出最可能的 base-case 假设、依据与不确定性 |
| 子节点 C | 未给 Missing | — | 基于题目语境和通用商业逻辑形成有方向的观点假设 |

规则：

- 一个来源框内可以有多条事实，但每条事实必须挂到具体子节点名称下。
- `没有目标`、`没有成本数据`等明确的缺失本身可以是 Given，但对应框架节点仍标为 `部分已给 Partial` 或 `未给 Missing`，不能误标为完整覆盖。
- 对 `Partial / Missing` 节点，必须补回答 Case 必要的 1-3 个观点假设；仍需外部验证的内容写成假设，不写成事实。
- 观点假设中的潜在不确定性直接写在同一段内，不另设“风险与验证”子模块；跨节点最重要的风险统一在“风险与下一步”中收束。
- HTML 的框架房子组件必须直接展示此覆盖矩阵，让读者一眼看出“题目给了什么、缺了什么、自己要补什么”。

### Phase 5：形成观点与假设

按框架分支逐项判断：

| Candidate Material 覆盖情况 | 处理方式 |
|---|---|
| Candidate Given 充分，已能回答问题 | 把每条事实转化为 implication，并给出明确观点 |
| Candidate Given 部分覆盖，但仍有关键缺口 | 对缺失部分形成 1-2 个 base-case 假设，不能只列待问问题 |
| 没有 Candidate Given，但分支对回答问题必要 | 基于题目语境和通用商业逻辑形成 2-3 个凝练假设 |
| 没有 Candidate Given，且分支与本题无关 | 谨慎删除或标注本题不展开 |

先独立形成观点与假设，再查看 Casebook Sample Answer 做覆盖检查。若观点来自 sample answer 且不是由题目信息或通用商业逻辑独立推出，必须保留 `【Casebook答案·示例Brainstorm】` 标签，不得改标为 `【观点与假设】`。

每个重要观点都使用“强观点”结构：

1. **明确立场**：一句话先说最可能的判断，不用“可能 A、也可能 B”回避选边。
2. **因果关系**：说明为什么，以及它如何影响 Case 核心问题。
3. **Brainstorm 佐证**：给出 1-3 条来自题目、通用商业逻辑或行业机制的支撑。
4. **不确定性**：在同一段最后点明该判断最可能错在哪里；不单独建立风险卡片。

执行规则：

- `Missing` 表示“题目没有直接给”，不表示“分析器不能判断”。先给工作假设，再把最关键的不确定性留到风险与下一步。
- 不编造具体数字、公司事实或监管事实；但必须大胆使用模型已有的商业常识、行业机制和题目上下文进行定性推断。
- 默认不为形成工作假设而搜索网络。只有用户要求或判断依赖时效性外部事实时才搜索，并把结果标为外部研究，不得混入 Candidate Given。
- 每个框架节点至少产出一个推动核心决策的 implication；对关键 `Partial / Missing` 节点至少产出一个有方向的工作假设。

深度边界：

- 只展开到能回答面试问题、支撑判断的程度。
- 不继续拆成三级、四级执行清单。
- 涉及落地方法时，只选最有代表性的 1-2 个例子。
- 例如“建立品牌形象”只需补“统一核心价值主张”和“选择关键客户触点持续强化”；除非题目明确要求，不继续设计 App 页面、活动流程、素材和排期。
- 没有推进 Case 核心问题的内容不要输出。

如果额外观点无法放入任何现有框架节点，不要为它新建框架分支；放到最接近的节点，或舍弃不重要内容。

### Phase 5.5：形成阶段性判断

完成每个一级模块后，强制写一句阶段性判断：

1. **先投票**：当前模块更支持哪一侧？
2. **再说明关键依据**：只保留最重要的 1-2 个事实或观点假设。
3. **最后限定判断**：用一句话说明最关键的不确定性，但不得退回“无法判断”。

示例方向：

- Market Entry · 市场分析：市场是否有吸引力，更支持进入还是不进入。
- Market Entry · 自身分析：客户是否初步具有 Right to Win，更支持进入还是不进入。
- Market Entry · 进入方式：优先选择哪种方式，为什么，什么条件下切换。
- Profitability · Revenue / Cost：利润问题更可能来自哪一侧，哪个驱动最关键。
- Growth Strategy：哪条增长路径优先，主要价值来源与约束是什么。

阶段性判断不得只复述数据，不得写成“还需要进一步分析”的空结论，也不得因为存在 Missing 就拒绝投票。

### Phase 6：核对计算与答案

对 Case 中的计算：

1. 先确认每个输入是否来自 Candidate Given / Upon Request / Exhibit。
2. 使用 candidate-facing inputs 独立完成公式、步骤、单位和结果。
3. 再与 Casebook Sample Calculation 对照，复核算术、单位、时间口径和分母分子。
4. 如有错误，分别写清“Casebook 原答案”和“核对后的结果”，不要悄悄改写。
5. 每个结果都补一句 business implication：数字对客户决策意味着什么。
6. 缺少关键 Exhibit 或数字时，只写公式、所需数据和判断方向；可以用答案页反推做校验，但必须显式标为“答案反推，非 Given”。

### Phase 7：补充行业认知

行业补充保持简洁，重点回答“这个行业如何运作，以及为什么影响本题”。

1. 判断核心产品是实体、服务还是 TMT / 虚拟产品。
2. 还原基本流程：投入 / 原材料 → 生产或服务交付 → 销售 → 使用。
3. 根据研究视角说明上游、中游、下游和关键参与者。
4. 实体行业重点看产品形态、使用场景和销售地点。
5. 服务行业重点看价值定位、人 + 工具 + 资源、服务交付、获客和客户评价。
6. 提炼 1-2 个本题最关键的行业命门或特殊逻辑。
7. 明确说明这些认知如何影响框架、计算或 recommendation。

不要把行业补充写成百科。涉及具体、时效性强或不确定的外部事实时，使用可用的网络搜索并引用来源；一般性流程认知不必搜索。

### Phase 8：输出与收尾

#### 聊天版结构

完成框架确认后，按以下顺序输出完整答案：

1. **Case 基本信息与一句话判断**
2. **框架使用说明**：框架名称、保留逻辑、删减项
3. **完整框架导图与 Candidate Given 落位**
4. **逐模块完整分析**
5. **风险与下一步**
6. **行业认知补充**
7. **Case 总结与 Recommendation**

每个模块统一使用：

```markdown
### [原框架模块名称]

**关键结论：** [一句话 finding]

**Candidate Material**
- 【题目·开题信息 / 按需提供 / Exhibit / 问题】...
- **Implication：** ...

**框架覆盖｜Framework Coverage**
| 子节点 | 状态 | Candidate Material | 观点与假设 |
|---|---|---|---|
| ... | 已给 / 部分已给 / 未给 | ... | ... |

**观点与假设｜Point of View & Hypothesis**
- **观点：** [明确立场]
  - **因果与佐证：** ...
  - **不确定性：** ...

**阶段性判断｜Stage Conclusion：** [明确投票 + 关键依据 + 最重要的不确定性]
```

如需要展示答案对照，另设：

```markdown
**Casebook Answer Check**
- 【Casebook答案·示例框架 / 示例Brainstorm / 参考计算】...
- **校验结果：** 覆盖 / 缺失 / 算术差异；不得写成 Given。
```

风险与下一步只保留 2-4 个真正影响 recommendation 的点。风险必须来自前文观点假设中的关键不确定性；下一步说明如何降低这些风险，不要展开成大量数据需求或计算任务。

最终总结严格遵循：

1. 第一行明确回答总问题，决策题必须选择 Yes / No 或 A / B
2. 按原框架顺序总结各板块核心 finding
3. 单独总结 2-4 个最关键风险
4. 单独给出按优先级排序的下一步

#### 聊天版导图

默认至少输出一张 Mermaid 总览图。保留原框架层级，使用文字标签区分来源：

```mermaid
mindmap
  root((客户核心问题))
    原框架板块一
      子模块A
        【题目】候选人可获得的信息
        【观点与假设】基于材料形成的判断
      子模块B
    原框架板块二
```

- 信息较少：用一张完整导图。
- 信息较多：使用“一张框架总览 + 每个一级板块一张详细导图”。
- 不要为了塞进一张图而省略 Candidate Given；也不要把 Sample Answer 塞进 Given 节点。
- 聊天版优先保证结构和完整性，不强求真实手写纹理。

#### HTML 版

读取 [references/html-output-spec.md](references/html-output-spec.md)，生成单文件、UTF-8、无外部依赖、响应式并可打印为 PDF 的 HTML。

- 以 [assets/case-report-template.html](assets/case-report-template.html) 为固定视觉骨架；保留其页面尺寸、左侧粘性目录、主内容宽度、卡片层级、移动端和打印样式，只替换内容与必要的网格数量。
- 标题、章节名、来源标签、状态标签和关键按钮使用“中文｜English”双语；中文为主，英文为辅。正文不要求逐句翻译，但核心框架节点和结论标题必须双语。
- 每个框架房子卡片逐项展示 `Framework Coverage`，并在 Candidate Material 旁直接展示 `观点与假设｜Point of View & Hypothesis`。
- 每个一级模块结束处使用统一的 `Stage Conclusion` 高亮组件。
- 最终 Recommendation 必须包含明确选择、核心依据、核心风险与下一步四部分。
- 不得输出“Skill 测试结论”“Skill 改进建议”“内部 QA”等面向开发者的章节。

- 用户选择 A：直接生成 HTML，不先输出完整聊天答案。
- 用户选择 C：先完成聊天版，再生成内容一致的 HTML；不得在两版中改变结论或遗漏信息。
- 默认文件名：`[Case名称]_Case分析_[YYYYMMDD].html`。
- 用户没有指定保存目录时，保存到当前工作目录，并返回绝对路径。

## 质量检查

交付前逐项确认：

- [ ] Casebook 页面和题目没有明显漏读
- [ ] 已先完成 Candidate Material / Casebook Answer Key 分类，再识别题型
- [ ] 只选择并读取了一个主框架；若读取第二个附件，题目确实切换到了独立任务
- [ ] 已先单独输出框架确认版，且确认版没有提前泄露 brainstorm、计算、阶段性结论或 recommendation
- [ ] Reference 只用于约束结构；关键矛盾、节点优先级和 case-specific insight 均经过独立推理
- [ ] 已完整读取对应框架附件
- [ ] Skill 自有框架一级板块、顺序和主逻辑没有被 Casebook 示例框架覆盖
- [ ] 所有删减都有简短理由
- [ ] 每页内容已拆分为 Candidate Material 与 Casebook Answer Key
- [ ] 每条 Candidate Given 已落位或被明确说明
- [ ] Sample Framework / Brainstorm / Calculation 没有被误标为 Given
- [ ] Candidate Given、Casebook Answer Check 与观点假设有清晰标签
- [ ] 缺失 Exhibit / Appendix 没有通过答案反推伪装成题目材料
- [ ] 每个保留的框架子节点都有 Given / Partial / Missing / N/A 覆盖状态
- [ ] 每个关键 Partial / Missing 节点都有明确的 base-case 观点假设，而不是只列待问问题
- [ ] Profitability 的初始优先级仅依据开题与当时可获得的信息；缺少趋势时已比较收入／成本的改善空间、约束与推翻条件，后续任务方向没有被倒用为开题依据
- [ ] 每个重要观点都包含立场、因果、brainstorm 佐证和同段不确定性
- [ ] 每条关键 Given 都已转化为推动核心问题的 implication
- [ ] Casebook 计算已复核，并给出 implication
- [ ] 每个一级模块都有直接回答核心问题的 Stage Conclusion
- [ ] 风险和下一步没有过度细化
- [ ] 行业补充包含流程 / 产业链，并服务于本题
- [ ] 决策题的最终 recommendation 第一行已明确选择一侧，没有用“有条件推进”代替决定
- [ ] 最终 recommendation 按框架汇总关键结论，并单独包含核心风险与下一步
- [ ] HTML 使用固定模板尺寸和双语标签，且不含 Skill 测试或开发建议

## 语言与风格

- 用户使用中文时正文用中文，HTML 标题、框架节点、标签和按钮中英双语；用户使用英文时正文用英文，关键标签仍可保留中英双语。
- 中文正文保留常用专业英文术语，如 contribution margin、patient adherence、ROI。
- 每段结论前置；用短段落、清晰小标题和必要表格。
- 直接给判断，不写空泛铺垫、鸡汤或自我表扬。
