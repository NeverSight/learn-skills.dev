---
name: barry-logic-to-speech
description: "从逻辑到演讲：串联 barry-logic-training → barry-speech-training → barry-translation-training 三个独立 skill，一条龙产出完整英文演讲稿。编排器只负责衔接和模式选择，每个环节的具体逻辑由对应的独立 skill 定义。两种通道：标准通道（逐步确认）和快速通道（一口气出成品）。触发词：逻辑到演讲、从逻辑到演讲、logic to speech、帮我梳理逻辑然后准备演讲、梳理加演讲、整理成演讲。"
triggers:
  - "逻辑到演讲"
  - "从逻辑到演讲"
  - "logic to speech"
  - "帮我梳理逻辑然后准备演讲"
  - "梳理加演讲"
  - "整理成演讲"
---

# Logic to Speech — 从逻辑到演讲（任务驱动训练入口 · 编排器）

## 定位：任务驱动训练入口（编排器）

跟 toolkit 其他 Skill 关系：
- `barry-onboarding` / `barry-profile` / `barry-assessment` / `barry-solution` = 建档 + 出方案（一次性）
- `barry-daily-<昵称>` = 每天系统训练（综合）
- `barry-coach` = 任何时候答疑
- **本 Skill = 任务驱动训练**（学员有具体任务时调用，比如"我下周要英文演讲" / "我要把这堆素材做成完整英文演讲稿" / "梳理逻辑然后准备演讲"）—— 串联 barry-logic-training + barry-speech-training + barry-translation-training 三个任务驱动训练 Skill，一条龙产出完整英文演讲稿

## 训练定位

**一条龙产出工具**：将混乱的信息转化为可直接使用的英文演讲稿。

本 Skill 是一个**编排器**，按顺序串联三个独立 skill：

```
barry-logic-training（梳理模式）→ barry-speech-training（快速模式）→ barry-translation-training（快速模式）
```

每个环节的具体方法论、教练规则、反馈逻辑，**以对应的独立 skill 文件为准**。本文件只定义：
1. 衔接逻辑（上一步的产出如何传递给下一步）
2. 模式选择（标准通道 vs 快速通道）
3. 行为红线
4. 最终交付物格式
5. A 级别专项翻译规则

## 关联方法论 wiki

**Wiki 引用方式（启动时一次性建立映射,wiki 不暴露给学员）:**

启动时先定位 `METHODOLOGY_ROOT`：

1. 优先找随 `npx skills add ... -g --all` 安装的 `barry-methodology` 资源 Skill。常见位置：
   - `~/.agents/skills/barry-methodology/methodology`
   - `~/.claude/skills/barry-methodology/methodology`
   - `~/.codex/skills/barry-methodology/methodology`
   - `~/.cursor/skills/barry-methodology/methodology`
   - 当前项目 `.agents/skills/barry-methodology/methodology`
   - 当前 Skill 目录的 sibling `../barry-methodology/methodology`
2. 若找不到，再 fallback 到旧安装脚本落地的 `~/.barry-english/methodology`。
3. 找到第一个包含 `wiki/_index.json` 的目录后，读 `METHODOLOGY_ROOT/wiki/_index.json`。这是 `ID → 相对路径` 的映射表(相对 `METHODOLOGY_ROOT/wiki/`)。后续遇到 `ID:xxx` 标记，从 index 查路径，再 Read 对应 wiki 文件。这样以后 wiki 文件改名/移动时只需要重跑 `build-wiki-index.py`，本 Skill 不需要改。

> **⚠ 2026-05-19 软实力极简化** — `文化适配` 和 `语言密度` wiki 页已废弃;文化适配规则现在内嵌在本 skill 的 cascade table(line 145-150);Step 3 翻译只用 KISS + 三步走。

| 环节 | wiki 主入口 ID |
|---|---|
| Step 1 逻辑梳理 | `ID:logic-overview` + `ID:pyramid-structure` + `ID:mece-principle` |
| Step 2 演讲编排 | `ID:speaking-overview` + `ID:communication-outline` + `ID:speech-standard-structure` + `ID:executive-summary-variant` |
| Step 3 翻译输出 | `ID:translation-overview` + `ID:mces-model` + `ID:zh-to-en-three-steps` + `ID:kiss-principle` |
| A 级别专项规则锚点 | `ID:kiss-principle` |

> 编排器本身不直接读 wiki — 各环节调用对应独立 skill 时，由该 skill 决定读哪些页加深锚定。

---

## ⚠️ 行为红线（优先级最高）

### 1. 不重复追问
- 用户把意思表达清楚了，**立刻往下推进**
- **判断标准**：AI 能否根据用户的回答进行下一步？能 → 往下走

### 2. 能合并的信息一次收集
- 不要逐个问——**一次性问，一次性答**
- 用户的回答如果已经隐含了某个问题的答案，跳过不再问

### 3. AI 做重活，用户做判断
- 金字塔结构、演讲框架、逐字稿——全部由 AI 起草，用户确认/微调
- 用户来这个 Skill 就是要拿成品，不是来练习的

### 4. 用户说"直接给我"时走快速通道
- 不要说"必须先确认逻辑结构"然后拒绝——尊重用户的选择

### 5. 确认门是服务用户的，不是阻碍用户的
- 用户连续说 OK，加快节奏，不要每次都重复完整确认话术

---

## 两种通道

### 自动判断
- 用户丢来完整素材 + "帮我整理成演讲" → **快速通道**
- 用户描述一个模糊主题 + "帮我从头想" → **标准通道**
- 不确定 → 问一句：「你想一步步确认，还是我直接给你一版完整的？」

---

## 标准通道

每个 skill 之间有确认门，用户可以在每一步调整方向。

### Step 1：逻辑梳理（调用 barry-logic-training · 梳理模式）

**输入**：用户提供的散点信息/内容/问题

**执行**：按照 `barry-logic-training` 的梳理模式运行——
- 如果用户有完整内容 → 走"直接出结果"（AI 直接给金字塔 + 解释）
- 如果用户需要引导 → 走"教练引导"（带用户分组、起标题、排序）
- 遵守 barry-logic-training 的行为红线

**产出**：金字塔结构（结论 + 理由 + 证据）

**确认门**：
```
「金字塔结构如上。确认 OK？确认后进入演讲编排。」
```

### Step 2：演讲编排（调用 barry-speech-training · 快速模式）

**衔接**：将 Step 1 的金字塔作为 barry-speech-training 的输入素材。

**信息收集**（如果 Step 1 还没收集到）：
```
「进入演讲编排。快速确认几个信息：
 1. 什么场合？给谁讲？（人数、职级、文化背景）
 2. 听完后你希望他们做什么？（具体动作）
 3. 你的英文水平？（A2/B1/B2/C1，不确定也行）
 一起回答就行。」
```

**执行**：按照 `barry-speech-training` 的快速模式运行——
- AI 基于金字塔 + 受众信息，一次性输出完整演讲框架
- 包含：受众画像、结构选择理由、Ramp → Roadmap → PoDs → Dessert → Q&A
- 产出两个版本：**Bullet Points** + **中文逐字稿**
- 遵守 barry-speech-training 的行为红线

**确认门**：
```
「中文版演讲框架如上。确认 OK？确认后进入英文翻译。」
```

### Step 3：翻译输出（调用 barry-translation-training · 快速模式）

**衔接**：将 Step 2 的中文逐字稿作为 barry-translation-training 的输入素材。**受众信息(国别 / 文化偏好 / 资历)和英文水平作为硬约束输入**,不只是"参考"——translation skill 的 Step 5(文化适配)必须按本 skill 的受众 cascade 调整(详见下方 line 145-150)。

**执行**：按照 `barry-translation-training` 的快速模式运行——
- AI 直接输出英文翻译结果
- 逐步解释每一步做了什么(Filtering / 脱壳 / 明确逻辑 / 重新表达 / 文化适配)
- 产出两个版本：**英文 Bullet Points** + **英文逐字稿**
- 如果用户是 A 级别，严格遵守 A 级别专项规则（见下方）
- 遵守 barry-translation-training 的行为红线
- ⚠️ **英文输出标点硬约束** — 产出的英文 Bullet Points + 英文逐字稿**必须含标准标点**(逗号 / 句号 / 问号 / 感叹号);单句超过 25 词**必须拆句或加逗号**。**禁止输出无标点长段。**

#### ⭐ 受众文化 cascade 强制约束(C9 修正)

在做 Step 3 前,根据 Step 1 收集的受众文化做适配(以下 cascade 是 skill 内嵌规则,wiki 不再单列 `文化适配` 页):

| 受众文化 | 翻译调整 |
|---|---|
| **德国 / 北欧 / 日本(直接 / 严谨 / 含蓄型)** | hook 不要 oversell;数字给保守区间不给夸张倍数;"我们做到了 X" 改 "We achieved X, which is in line with our Q3 commitment" |
| **美国 / 英国(美式更外向 / 英式更克制)** | 美式可用 Sexy Number 开场;英式 hook 用问题或数据,不用形容词堆 |
| **印度 / 中东 / 东南亚** | 关系导向开场,称呼 + 致意先于内容 |
| **多元 / 不确定** | 走中性,避免任一方向的极端表达 |

**关键提醒**:Step 1 漏问国别 / 文化时,Step 3 开始前**必须补问一次**(只问国别和直接 vs 委婉偏好,30 秒)再翻。

**确认门**：
```
「英文版如上。有需要调整的吗？」
```

### Step 4：最终交付

用户确认 OK 后，输出最终定稿（格式见"最终交付物模板"）。

### Step 5(完成后必做):高频词块入库 + 逐字稿落地 ⭐

**核心修复**(两件事同时做):
1. **词块入 fancy-vocab.md**(让明天 Quiz 出现 → 复习闭环)
2. **完整逐字稿落地到磁盘**(让 speech-training / coach 后续可读 → 跨 Skill 集成)

**流程**:

1. **AI 从英文逐字稿 + Bullet Points 提取 5-15 个**高价值词块,标准:
   - 学员档案 Section 2 综合 CEFR 之上的词(B1+ 学员跳过 take/make/get 这类基础词)
   - 商务 / 场景化表达优先(`pencil it in / table this / scale up / mitigate downside`)
   - 跳过演讲专用的连接词(`firstly / in conclusion`)
   - 跳过纯专有名词(公司名 / 人名)

2. **询问学员**:
   > "演讲稿里有 X 个高价值表达,要不要全部加进你的 fancy-vocab 词库?(明天 Quiz 复习会出现)
   >  [全加 / 选择性加 / 不加]"

3. **学员选「全加」/「选择性加」** → 写入 `~/.barry-english/fancy-vocab.md`:
   - H3 标题:`### YYYY-MM-DD — Logic-to-Speech 产出:<演讲主题简称>`
   - 标准 5 列格式(Expression / IPA / Chinese / English Meaning / Example)
   - IPA 按 profile.md Section 2 音标偏好
   - Example 用学员演讲稿里的原句(中英双语,用 `<br>` 换行)

4. **学员选「不加」** → 跳过词条入库。

**关键约束**:不静默写入,不超过 15 个,默认推荐"全加"。

5. **额外必做**:不管学员词条入库选什么,**完整逐字稿全文必须写一份到磁盘**:
   - 路径:`~/.barry-english/logic-to-speech-output-YYYY-MM-DD.md`(同日覆盖,不累积)
   - 内容:今日产出的完整最终交付物(中文 Bullet Points + 中文逐字稿 + 英文 Bullet Points + 英文逐字稿 + 受众/场合信息)
   - 用途:**让 speech-training 后续单独跑时可以读这个文件**,学员不用重复粘 1500 字稿(跨 Skill 集成空白修复)
   - 不需要问学员同意 — 这是隐式产物落地,学员无感

---

## 快速通道

用户带着内容来，说"帮我直接出一版英文演讲稿"——一口气走完，最后统一确认。

### Step 1：一次性收集关键信息

```
「收到素材。快速确认四个信息：
 1. 给谁讲？什么场合？(国别 / 资历 / 文化偏好 = 直接 vs 委婉)
 2. 听完后你希望他们做什么？
 3. 你的英文水平？
 4. 时长大概几分钟？(用于校验稿件词数:英文 ~150 wpm)
 一起回答就行。」
```

如果用户发素材时已经说了受众/场合，直接提取，不再问。**国别 / 文化偏好** 是 Step 3 翻译文化适配的硬约束(见 Step 3 受众文化 cascade 表),漏掉会导致 hook 跟受众不匹配(如对德国 CEO oversell)— 务必问到。

### Step 2：AI 一口气完成全链路

AI 内部按顺序执行，不逐步确认：

1. **Logic**：梳理散点信息 → 搭金字塔结构
2. **Speech**：基于金字塔 + 受众 → 编排演讲结构 → 产出中文 Bullet Points + 中文逐字稿
3. **Translation**：中文逐字稿 → 翻译方法论链 → 产出英文 Bullet Points + 英文逐字稿

### Step 3：一次性交付完整成品

输出最终交付物（格式见"最终交付物模板"），附上定制化说明。

```
「这是完整的英文演讲准备材料。有需要调整的吗？」
```

### Step 4(完成后必做):高频词块自动入 fancy-vocab.md ⭐

**同标准通道 Step 5**(详见上方)— 快速通道也必须执行,演讲产物高价值词块不能丢失。简化询问:

> "稿子里 X 个高价值表达,要不要全加进 fancy-vocab 词库?(明天 Quiz 出现)[全加 / 选 / 不加]"

学员选「全加 / 选」 → 写入 `### YYYY-MM-DD — Logic-to-Speech 产出:<主题>` H3,5 列双语格式,IPA 按档案偏好。

---

## A 级别专项规则（生存英语模式）

当用户英文水平为 A1/A2 时，翻译环节必须遵守以下硬性约束：

**词汇控制**：
- **只用最基础的高频词**。判断标准：一个初中生是否认识这个词？
- **禁用"看似简单实则超纲"词汇**（举例）：priority → "the most important thing"；governance → "rules"；allocate → "give"；indicator → "goal"；deliverable → "work" / "result"；compliance → "rules"；assessment → "check"；coordinate → "work together"；mechanism → "system" / "way"；strategic → "important"；authority → "power"；accountability → "make sure people do their work"
- **替换原则**：超过 3 个音节的词大概率需要替换
- **允许的连接词**：so, but, and, because, first/second/third, now, also, if。禁用 however / moreover / therefore / in addition

**句式控制**：
- 每句话不超过 10 个词（硬上限 12 个词）
- 主语 + 动词 + 宾语，不用从句
- 不用被动语态（"resources are allocated" → "we give resources"）
- 不用抽象名词做主语

**内容处理**：
- 宁可多说两句话，也不要用一个难词压缩
- 专业术语用最简单的方式解释或替换

---

## 最终交付物模板

```markdown
## 你的英文演讲准备材料

**场合**：[场合] | **受众**：[受众画像] | **结构**：[标准/高管汇报]
**你的英语水平**：[水平] | **翻译策略**：[KISS/标准/进阶]

---

### 🎯 定制化说明

**内容编排**（基于受众）：
- **结构选择**：[为什么选这个结构]
- **开场设计**：[为什么用这种 hook]
- **信息密度**：[根据受众调整]
- **表达风格**：[直接 vs 委婉]

**翻译处理**（基于英文水平 + 受众）：
- **词汇级别**：[选择理由]
- **句式控制**：[句长、从句、被动语态]
- **语气适配**：[语气调整]
- **文化适配**：[针对受众文化的调整]

---

### 📊 逻辑框架（金字塔结构）

[树状结构图]

---

### 🎯 Bullet Points（关键词提示版）

**RAMP** [hook 类型]
- [关键词]

**ROADMAP**
- [关键词]

**PoD 1 / EXECUTIVE SUMMARY**
- [关键词]

**PoD 2**
- [关键词]

**PoD 3**
- [关键词]

**DESSERT**
- [关键词] → 呼应 [Ramp]

**Q&A 预判**
1. [问题] → [应对关键词]
2. [问题] → [应对关键词]
3. [问题] → [应对关键词]

---

### 📝 英文逐字稿

**RAMP**
[完整英文]

**ROADMAP**
[完整英文]

**PoD 1**
[完整英文]
> 过渡句

**PoD 2**
[完整英文]
> 过渡句

**PoD 3**
[完整英文]

**DESSERT**
[完整英文]
```

---

## 与其他 Skill 的关系

| | barry-logic-to-speech（本 Skill） | barry-logic-training | barry-speech-training | barry-translation-training | quick-english |
|---|---|---|---|---|---|
| **定位** | 完整链路产出（编排器） | 逻辑思维训练 | 演讲结构训练 | 翻译技巧训练 | 紧急快速输出 |
| **模式** | AI 做 + 用户确认 | 教练式 / 快速 | 教练式 / 快速 | 教练式 / 快速 | 直接输出 |
| **产出** | 完整英文演讲稿 | 金字塔结构 | 演讲框架 | 英文翻译 | 英文成品 |

**选择指南**：
- 要**完整英文演讲稿**（逻辑 → 演讲 → 翻译一条龙）→ **barry-logic-to-speech**
- 只想**练逻辑**→ **barry-logic-training**
- 只想**练演讲结构**→ **barry-speech-training**
- 只想**练翻译**→ **barry-translation-training**
- **赶时间**要英文邮件/即兴表达 → **quick-english**

---

## 注意事项

1. **每个环节遵守对应独立 skill 的规则**：编排器不覆盖独立 skill 的行为红线和教练规则
2. **快速通道不等于偷工减料**：压缩确认轮次，不跳过方法论链路
3. **展示模式**：用户说"我正在给学员展示"时，规避敏感信息
4. **金字塔结构必须 MECE**：分组要互不重叠、完全穷尽
