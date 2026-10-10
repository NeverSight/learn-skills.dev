---
name: humanize-paper
description: >-
  Reconstruct and humanize academic manuscripts (English or Chinese), especially ML/AI and
  scientific-method papers.
  Use when a draft reads like a structureless technical report: it lacks motivation, lists components before
  explaining why they are needed, follows execution order instead of scientific reasoning, confuses parallel,
  progressive, causal, contrastive, control, and boundary relations, or gives all results equal weight. For a
  complete manuscript, first rebuild the scientific argument from the manuscript's existing evidence, then
  revise prose. Also use for "去 AI 味", "humanize paper", "rebuild the narrative", "improve the logic",
  "润色成人写的", or diagnosing AI-like academic writing. Not for detector evasion, invented evidence,
  pure translation, non-academic text, or deliberate errors.
---

# Humanize Paper

本 skill 的首要任务不是替换 AI 高频词，而是恢复研究者的科学推理路径：为什么提出这个问题，
现有判断为什么不足，方法必须满足什么要求，作者为什么选择这一设计，各组实验分别支持、排除或
限制什么。完整稿先重建论证，再处理句法、节奏和社区用词。技术细节只有在服务科学论证或复现时
才保留，不能依照项目日志、代码调用图或实验执行时间堆砌正文。

## 输入轨道与两个权限维度

先判断输入是否足以构成完整 manuscript。用户明确只要语言校对时服从用户要求，不自动重排。

| 输入轨道 | 可用材料 | 默认结构范围 | 默认 claim 策略 |
|---|---|---|---|
| **excerpt** | 一个或几个段落/小节 | `local` | `locked` |
| **manuscript** | 基本完整的正文，及其依赖的 caption/appendix | `reconstructive` | `locked` |
| **evidence-grounded** | 完整稿 + 支撑 claim 校准的表格、定理、结果摘要或原始记录 | `reconstructive` | `evidence-calibrated` |

### 结构范围

| 范围 | 权限 |
|---|---|
| **local** | 句段级改写；不移动段落，不推断全文 thesis，不输出全文级判断 |
| **reconstructive** | 从原稿已有内容推断工作性 thesis；跨段、跨节移动；拆分、合并、压缩；修复论证关系；重建 section 功能和篇幅层级 |

### Claim 策略

| 策略 | 权限 |
|---|---|
| **locked** | 保留 proposition、事实、否定、modality、scope、novelty、比较方向、聚合口径和证据上限；允许改变 presentation policy 和原稿错误的表面 discourse relation |
| **evidence-calibrated** | 在独立 evidence pack 的上限内调整 claim 强度、作者姿态或未充分表达的证据关系；每处进入 advocacy ledger |

完整稿本身足以授权 source-grounded 结构重建，不要求作者预先写出 thesis、climax 或最强证据。
独立 evidence pack 只用于改变 claim，而不是结构重建的前置条件。若两个有充分原稿支持的候选
thesis 会导向实质不同的科学结论，才询问用户；仅强调程度不同则采用范围更保守、证据覆盖更完整
的版本继续 zero-shot 重构。

**reconstructive 是权限，不是重写义务。** 完整稿授权结构重建，但是否执行由诊断决定。结构经
判定健全的稿子，合法产出是少量路由、一致性和语言级修改，而不是全篇重排（见最小干预原则和
工作流第 10 步）。不得把"完成了一次全面重写"当作任务完成的证据。

## 单一优先级

前项永远压过后项。

| 优先级 | 约束 | 执行规则 |
|---|---|---|
| **C0** | 工件边界 | 编辑说明、模板标签、模型自评、工具残留不进入干净稿；草稿占位符仅在作者明确要求时保留 |
| **C1** | 锁定内容 | 不改变数字、正负号、单位、CI、P 值、公式、代码、citation key、数据集名、模型名和正式专名 |
| **C2** | 命题与认识强度 | `locked` 下不改变事实、否定、因果/相关、scope、novelty、比较方向、聚合口径及 may/could/suggest 等强度 |
| **C3** | 引用与证据归属 | 移动内容后，引用、图表、定理和实验仍支持原来的具体命题；不靠移句扩大 citation scope |
| **C4** | 术语与对象身份 | 一个概念一个 canonical term；不合并不同 artifact、实验、模型、数据或机制 |
| **C5** | 论证有效性 | 锁定证据实际支持的科学关系，不锁定原稿连接词、表面并列结构或实验时间线；依据原稿锚点修复并列、递进、因果、对比、前提、控制、让步和边界关系 |
| **C6** | 章节功能 | Abstract、Introduction、Methods、Results、Discussion 和 SI 各自完成明确 reader question，不能跨节重复同一组件清单 |
| **C7** | 主次与细节路由 | 主科学证据、方法价值证据、机制/control、工程可靠性和复现细节不等权；技术细节按科学功能安排位置和篇幅 |
| **C8** | 清晰与自然 | 论证稳定后才删除空话、重复和模板痕迹，改善具体性、节奏与社区语域 |
| **C9** | 风格统计 | 只定位候选，不规定句长、段长或所谓 burstiness 阈值，不覆盖 C0–C8 |

### 最小干预原则

改动量不是目标，诊断才是。每一处 move、split、merge、compress 或 route 必须能引用 reverse
outline 或 argument graph 中一个已诊断的具体缺陷（关系错误、节功能冲突、细节层级错误、
control 失位等）；没有对应诊断的 span 保持原文。结构 pass 的合法产出包括"确认无结构改动"：
此时 target outline 等同现状，直接进入细节路由与语言 pass。语言 pass 同样不要求每句都变，
只处理已定位的候选，不为制造差异而改写。优先级表约束的是"改的时候不许怎样"，本原则约束
"什么时候不许改"。

### C5 关系准入条件

先判断关系，再选择连接词。不得从 `Furthermore`、`Therefore`、`Because` 或时间顺序反推关系。

| 关系 | 成立条件 |
|---|---|
| **并列** | 两个节点独立回答同一上位问题，彼此不构成依赖或推出 |
| **递进** | 后一节点依赖、扩展、收窄、修复或提高前一节点的证明力度 |
| **因果** | 有受控干预、识别设计、机制证明或形式证明；先发生不等于导致 |
| **对比** | 两端在明确的比较维度、条件和 aggregation unit 上可比 |
| **前提/依赖** | 后一设计、实验、解释或结论需要先接受前一条件 |
| **控制** | 实验明确针对一个已命名的替代解释或混杂因素 |
| **让步** | 不利事实成立，但不否定经过限定的主 claim |
| **边界** | 事实改变 claim 的适用范围、稳定性、外推或解释强度 |

若原稿只是用 `therefore/furthermore` 等表面标记错误连接两个各自独立的命题，而没有把因果本身
作为科学 claim，`reconstructive + locked` 可以改为并列、支持或中性邻接。若 `A causes B` 本身
就是原稿 claim，则 `locked` 不得静默削弱或删除，应保留并标记 claim–evidence audit。任何情况下
都不能把并列观察升级为因果，也不能根据常识补机制。无法判定时保留歧义或标记人工裁决。

## 三类修改不要混用

1. **语义保持型**：改写表面形式，但保留 proposition、modality、scope 和聚合口径。`local`
   只做这一类。例如可把 `seem to suggest that X may improve` 压成 `X may improve`，不能改成
   `X improves`。
2. **论证重建型**：命题节点不变，但依据完整稿重判节点之间的位置、功能、篇幅和未承载独立
   claim 的表面关系。包括移除错误的 `therefore` 邻接、把隐含前提前置、让 control 靠近其替代
   解释、把实现验证路由到 Methods/SI。`reconstructive + locked` 可以执行；每处必须有 source
   span 和关系依据。若因果、比较或 scope 本身就是 content claim，则不能以结构修复名义改变。
3. **证据校准型**：根据独立证据调整 claim 强度、scope 或作者姿态。只在
   `evidence-calibrated` 执行，每处必须有证据锚点并进入 advocacy ledger。

以下仍禁止在 `locked` 下顺口强化：

- `has emerged as transformative` → `has transformed`；
- `is limited in its ability to generalize` → `generalizes poorly`；
- `within 0.5 points` → `matches`；
- `higher mean across tasks` → `consistently better`；
- 观察到相关模式 → 机制导致结果。

把 claim–evidence mismatch 分成三类：

- **真实越界**：claim 超过证据。保留并标记，交内容审计；不要靠降 claim 或修辞隐藏。
- **表达造成的假 gap**：原稿已有 obstacle、control 或结果，但没有建立关系。重构时补齐有锚点的
  动机和关系桥。
- **证据未充分利用**：直接结果被多重 hedge。`locked` 保留强度；只有
  `evidence-calibrated` 才可校准。

## 渐进加载

- **excerpt**：先读 [signal-catalog.md](references/signal-catalog.md)，edit/rewrite 再读
  [rewrite-rules.md](references/rewrite-rules.md)。
- **完整 manuscript**：先读
  [manuscript-reconstruction.md](references/manuscript-reconstruction.md)，再读
  [rewrite-rules.md](references/rewrite-rules.md) 和
  [human-voice.md](references/human-voice.md)；`signal-catalog.md` 只辅助定位问题。
- 只有 `evidence-calibrated` 才读
  [advocacy-voice.md](references/advocacy-voice.md) 执行 claim 校准；其 materiality 和
  reader-belief 原则可用于重构后的复检。
- 遇到社区术语、内部实验代号或 artifact 身份时读
  [community-lexicon.md](references/community-lexicon.md)；**处理中文稿件时必须同时读其中
  中文学术写作 pattern 一节（第 5 节）**，英文 pattern 表不能覆盖中文的否定-对照句架、
  对仗排比、破折号和填充短语。
- excerpt/local 示例见 [worked-example.md](references/worked-example.md)；完整稿重构示例见
  [worked-example-reconstruction.md](references/worked-example-reconstruction.md)。示例展示的
  是存在结构缺陷的稿件；结构健全的稿件按工作流第 10 步判定后可以不做任何结构改动。

## 完整 manuscript 工作流

### 1. 确认完整性

读完正文和正文依赖的 caption、appendix、表格或补充材料。只提供单节时走 excerpt/local，不能
假装推断全文 thesis。多文件 LaTeX 先恢复 `\input`/`\include` 顺序。

### 2. 建 content inventory

给原稿 span 分配内部 ID，记录：命题、数字、公式、引用、图表锚点、modality、scope、aggregation、
设计决定、直接观察、比较、control/ablation、negative result、boundary，以及实现/复现细节。
此阶段不润色。

### 3. 做 reverse outline

逐段说明原稿当前功能，并标记：无 reader question 的技术段、一个段落承担多个认识层次、同一
claim 跨节重复、先给方案后补问题、control 远离替代解释、boundary 被藏入泛化 limitation 清单。
reverse outline 描述现状，不是目标结构。

### 4. 推断工作性 thesis

从 Title、Abstract、Introduction gap、证据最集中的 Results 和 Discussion 交叉生成候选 thesis。
优先选择能解释主要设计选择、覆盖主证据并保持原稿 scope 的版本。方法名、组件数和“做了大量
实验”不能单独构成 thesis。

### 5. 建 motivation chain

使用：

```text
可观察的科学问题或失败
→ 失败为什么重要
→ 现有指标、方法或流程为什么不足
→ 解决方案必须满足什么要求
→ 本文的核心设计选择
→ 哪类实验才能检验该选择
```

每个箭头必须定位到原稿 span、citation 或 experiment。缺桥时标记，不得反向从现有组件编造
动机。

### 6. 建 argument graph

节点至少区分：问题/观察、已有事实、设计要求、设计决定、方法/机制、评价问题、结果证据、替代
解释、control、边界和 thesis。边至少区分：motivates、requires、implements、tests、supports、
rules out、contrasts、depends on、qualifies 和 bounds。每条边记录 source spans、最大合理强度和
`supported | ambiguous | unsupported`。

### 7. 划分证据层级

不要把所有实验等权。区分：

1. **主科学证据**：直接回答论文核心科学问题或 use case；
2. **方法价值证据**：说明核心选择相对固定协议、替代策略或 baseline 增加了什么；
3. **机制/control 证据**：解释结果或排除主要替代解释；
4. **工程可靠性证据**：验证实现、接口、约束或后端行为；
5. **复现细节与运行残留**：支持复现或仅属于开发历史。

层级由其对 thesis 的功能决定，不由实验规模、执行先后或是否称为 ablation/control 决定。

### 8. 定义 section contracts

每节内部记录：`reader question / entry knowledge / required nodes / exit belief / allowed details / routed details`。
章节默认功能见 `manuscript-reconstruction.md`，但不能套成固定句式。

### 9. 路由技术细节

保留能解释核心设计、影响结果解释、决定比较公平性、排除主要替代解释或改变 scope 的细节。
只为复现服务的配方进入 Methods/SI；job ID、绝对路径、内部版本史和调试过程不进入论文。Scientific
control 可属于 Results；implementation validation 通常属于 Methods/SI。不要因为一项内容“很技术”
就隐藏会改变 headline 的 negative result 或 boundary。

### 10. 结构健全性判定

对照 section contracts、argument graph 和证据层级，对现状结构给出显式判定，只有两种合法结论：

- **存在结构缺陷**：逐条列出（span、违反的 contract 或关系、依据），据以生成 target outline；
- **结构确认健全**：target outline 等同现状，结构 pass 跳过，只执行细节路由、一致性修复和
  语言 pass。

禁止为了”更紧凑””更流畅”或追求改动量而移动内容。判定结论（包括”无结构改动”）必须写入
最终报告。

### 11. 生成 target outline

按读者建立主 claim 所需的依赖顺序组织，而不是按项目开发或实验执行时间。内部建立
`source span → target role/location → keep|move|split|merge|compress|route` 映射，并维护 citation、
figure 和 table 归属。每个非 `keep` 操作必须对应第 10 步列出的一条缺陷。

### 12. 先结构重写，再语言改写

先移动、拆分、合并、压缩，补写原稿已明确支持的动机桥和真实关系，使每个主要 Results 单元完成
“为什么需要这个判断、做了什么选择、观察到什么、改变了什么认识”。这是功能检查，不是强制每段
使用同一四句模板。target outline 稳定后，再处理句法、连接词、节奏和术语。语言 pass 同样遵循
最小干预原则，只处理已定位的候选。

### 13. 三重复检

先做 argument audit：

- thesis 是否有直接主证据；
- 每个 design choice 是否回应明确 requirement；
- 每个主要实验是否说明它要区分什么；
- 并列项是否同层，递进是否真有依赖，因果是否有足够设计；
- control 是否靠近被排除的 alternative；
- boundary 是否可见；
- 主结果是否被实现细节淹没；
- 各 section 是否形成不同的 exit belief。

再做 invariant 检查。对文件输入，改写前后运行：

```bash
python3 scripts/verify_invariants.py source.tex revised.tex
```

退出码 1 表示锁定 span 不一致；退出码 2 表示否定、modality、因果、scope 或聚合标记发生变化，
或脚本发出了警告，必须人工逐项核对；退出码 0 只表示脚本未发现这些风险，不表示论证自动正确。
若脚本发出 `$` 定界符配平或可疑数学 span 警告，先修复对应文件中的杂散 `$` 或错配再重新比较，
否则 math span 输出不可信。LaTeX 输入还要重新编译，确认 citation、cross-reference、equation 和
表图引用有效。

invariant 检查只验证”不许变的内容幸存”，最后还要对修订稿做输出端复检，确认该改的确实改了：

- 重跑 detect 类检查（句架、标点形状、术语漂移、语域、跨节复述），残留发现写入报告；中文
  稿件按 community-lexicon 第 5 节核对否定-对照句架、对仗排比、破折号和填充短语的残留频次；
- 一致性核对清单：派生数字（倍数、百分比、差值、占比）可由其原始量复算；图注表注与正文
  数字一致；交叉引用（章节号、图号、表号、方程号）存在且指向正确；移动后的 citation 仍贴在
  原命题上；
- 无法在 `locked` 下解决的异常列为 `uncertain` 交作者，不得靠改写掩盖。

## Evidence-calibrated 前置材料

只有需要改变 claim、modality、scope 或原稿没有明确表达的证据关系时，才要求：一句话 thesis、
最强证据、可压缩内容、不能动的内容、目标 venue，以及相关 evidence pack。按照
[advocacy-voice.md](references/advocacy-voice.md) 记录 evidence floor/ceiling、favorable/adverse、
M0–M3 和 reader-belief change。结构重建不因这些材料缺失而自动降级为 local。

## 输出契约

- **rewrite/edit**：干净稿本身不带模式标签、评分、argument graph、ledger 或编辑前言。交付时
  必须随附简要报告，必报项：结构判定结论（包括"无结构改动"）、干预量统计（结构操作、路由与
  一致性修复、语言改写各自的数量）、未解决的 claim–evidence mismatch、`uncertain` 项和一致性
  核对异常。reverse outline、target outline、完整 change log 和诊断细节仍只在用户明确要求时附上。
- **detect**：按严重度返回 findings；完整稿优先报告动机断裂、关系错误、证据层级和 section 功能，
  词句信号放后。每条给精确原文、理由和 `change | keep | uncertain`。
- 只报告核实过的计数，不输出 AI 概率或 detector 分数。
- 未解决的 claim–evidence mismatch 必须出现在报告中，不能靠改写抹掉，也不得借"默认只给干净稿"
  省略。

## Stop conditions

停止受影响的改动，但继续其他可安全完成的部分：

- 输入不足以判断是完整稿，却要求全文 thesis；
- 两个有充分支持、但会导向不同科学结论的 thesis 无法仲裁；
- 修改需要原稿中不存在的事实、引用、比较、机制或实验；
- citation scope、artifact identity、control 所针对的 alternative 或关键术语无法确认；
- 用户要求制造错误、刻意口语化或以绕过 AI 检测器为目标。

绝不编造细节、个人经历、引用、数据、机制、baseline、限制或实验条件；绝不为了“像人”改变合理
读者对证据的理解。完整稿重构的目标是恢复已有科学论证，不是替作者发明另一篇论文。
