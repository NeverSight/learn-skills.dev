---
name: literary-ghostwriter
version: "3.1.0"
description: |
  Literary ghostwriter skill that mimics the writing style of seven literary masters for creative writing.
  Extended with long-form novel project management, multi-role writing workflow, and consistency tracking.

  Triggers when: Writing in a specific author's style, creative writing, script writing, novel writing,
  long-form fiction planning, chapter continuation, or style imitation exercises.

  Commands:
  - /文豪 <作家> <选题> — Single-shot style imitation (7 authors)
  - /literary <author> <topic> — English single-shot style imitation
  - /文豪 迁移 <源→目标> <文本> — Style transfer: re-voice existing text into another author's style
  - /文豪 迁移 校核 <文本> <目标作家> — Verify a transfer against its source
  - /文豪 迁移 矩阵 — Show the inter-author transfer matrix
  - /literary transfer <src->target> <text> — English style transfer
  - /文豪 新建 <项目名> — Create novel project with world-building
  - /文豪 打开 <项目名> — Open existing project
  - /文豪 项目 — Show project status
  - /文豪 规划 — Analyze novel position, plan next moves
  - /文豪 大纲 [操作] — Generate/modify plot outline
  - /文豪 章纲 <章节号> — Generate chapter-level outline
  - /文豪 设定 <世界观元素> — View/modify world-building
  - /文豪 人物 [角色名] — View/modify character card
  - /文豪 伏笔 — View foreshadowing tracker
  - /文豪 续写 — Smart continuation from current position
  - /文豪 润色 <文本> — Style optimization
  - /文豪 审稿 [章节] — Editor review
  - /文豪 去AI味 <文本> — AI-trace reduction
  - /文豪 回收站 — Recycle bin for deleted content

  Capabilities: Deep analysis of author's spiritual core, providing concrete methods for authentic imitation,
  bilingual Chinese-English creation, multiple genre support, inter-author style transfer with four-layer
  re-voicing and plot-preserving constraints, long-form novel project management,
  multi-role writing workflow (planner/character-dev/stylist/editor), consistency tracking,
  chapter-by-chapter smart continuation, foreshadowing management.
author: cycleuser
license: MIT
status: Beta
---

## Safety Rules

参见 [_shared/core/safety-rules.md](../_shared/core/safety-rules.md) — 所有安全规则从共享层加载。

## Shared Memory

本技能通过共享记忆系统持久化状态。详见 `../_shared/memory/README.md`。

**存储键值**：`current_project`, `progress`, `preferred_authors`, `last_project_path`

每次会话开始时，LLM 应自动加载记忆系统中的当前状态。用户操作后应保存。

```bash
# 加载当前状态（会话启动时）
python ../_shared/memory/cli.py export literary-ghostwriter

# 保存当前项目
echo '"<项目名>"' | python ../_shared/memory/cli.py set literary-ghostwriter current_project

# 保存进度
echo '{"ch": 15, "words": 45000, "last_action": "续写"}' | python ../_shared/memory/cli.py set literary-ghostwriter progress

# 保存用户偏好
echo '{"preferred_authors": ["鲁迅", "金庸"], "default_genre": "武侠"}' | python ../_shared/memory/cli.py set literary-ghostwriter preferred_authors
```

# Literary Ghostwriter 文豪代笔

模仿七位文学大师风格的创作技能，支持短篇单次创作与长篇项目管理两种工作流。
七位作家：莎士比亚、茨维格、卡尔维诺、鲁迅、老舍、金庸、古龙。

## Quick Commands

### 单次创作 / Single-Shot Creation

| Command | Description |
|---------|-------------|
| `/文豪 <作家> <选题>` | 以指定作家风格进行中文创作 |
| `/literary <author> <topic>` | Write in English with a master's style |

### 风格迁移 / Style Transfer

| Command | Description |
|---------|-------------|
| `/文豪 迁移 <源→目标> <文本>` | 把已有文本改成目标作家的声部，只换语言不改情节 |
| `/文豪 迁移 <目标作家> <文本>` | 省略源作家，由系统判断并声明 |
| `/文豪 迁移 校核 <文本> <目标作家>` | 逐句回对原文，检查情节是否走样并评分 |
| `/文豪 迁移 矩阵` | 查看中文四家的互相迁移要点 |
| `/literary transfer <src->target> <text>` | English style transfer |

### 长篇项目管理 / Novel Project Management

| Command | Description |
|---------|-------------|
| `/文豪 新建 <项目名>` | 创建长篇项目，录入世界观、人物卡、大纲 |
| `/文豪 打开 <项目名>` | 打开已有项目，恢复上次进度 |
| `/文豪 项目` | 查看当前项目状态、进度、统计 |
| `/文豪 保存` | 保存项目当前状态 |

### 规划与大纲 / Planning & Outline

| Command | Description |
|---------|-------------|
| `/文豪 规划` | 分析当前位置，规划写作方向与节奏 |
| `/文豪 大纲 [操作]` | 生成/修改/查看完整情节大纲（操作: 生成/修改/查看） |
| `/文豪 章纲 <章节号>` | 为目标章节生成详细章纲（目标/人物/冲突/伏笔/钩子） |

### 世界观与人物 / World & Characters

| Command | Description |
|---------|-------------|
| `/文豪 设定 [世界观元素]` | 查看/修改世界观设定（时代/地域/势力/力量体系） |
| `/文豪 人物 [角色名]` | 查看/修改人物卡（性格/外貌/背景/关系/发展弧线） |
| `/文豪 关系图` | 查看人物关系图谱 |
| `/文豪 伏笔` | 查看伏笔追踪器（已埋/已回收/待回收） |

### 写作与工具 / Writing & Tools

| Command | Description |
|---------|-------------|
| `/文豪 续写` | 智能续写：分析上下文 → 规划本章 → 执笔创作 |
| `/文豪 润色 <文本>` | 风格优化：强化指定作家的精神内核 |
| `/文豪 审稿 [章节]` | 编辑审稿：一致性/节奏/人物/伏笔/去AI化五维审查 |
| `/文豪 去AI味 <文本>` | AI痕迹专项消除 |
| `/文豪 回收站` | 查看/恢复已删除的段落 |

### 写作角色 / Writer Roles

| Command | Description |
|---------|-------------|
| `/文豪 策划` | 剧情策划角色：设计冲突、转折、节奏 |
| `/文豪 人物设计` | 人物开发角色：深度塑造角色弧线 |
| `/文豪 网文` | 网文专家角色：快节奏、爽点、断章钩子 |
| `/文豪 润色` | 风格优化师角色：提升文学质感 |
| `/文豪 审稿` | 编辑审稿角色：全面审查与修改建议 |

---

## 核心原则：神似而非形似

### 形似 vs 神似

形似是表面模仿：使用作家的标志性词汇、句式、风格特征。

神似是内核把握：理解作家的精神世界，像他一样思考，用他的方式追问人生。

```
【形似示例】鲁迅风格（形似）：
"我翻开历史一查，发现这历史里写的都是欺骗。"
→ 只是模仿句式，没有鲁迅的精神内核

【神似示例】鲁迅风格（神似）：
"那本书躺在旧书摊的角落，封面已经泛黄。
他翻了几页，看到的是一个又一个熟悉的名字——
曾经意气风发的改革者，如今都在体制里找到了安稳的位置。
他没有说话，只是把书放回去，走了。

这沉默里有什么？失望？理解？还是习惯了？

他说不上来。他只知道，那些曾经批判的人，
后来都成了被批判的对象。批判者和被批判者，原来只隔着一层窗户纸。"

→ 不只是句式，是对"批判者变成被批判者"这一现象的追问
→ 这是鲁迅式的社会观察和精神拷问
```

### 神似的三层境界

```
第一层：语言特征
- 词汇、句式、节奏
- 这是表层的模仿，容易做到

第二层：精神内核
- 作家的核心价值观
- 他追问什么问题？他如何回答？
- 这是中层的把握，需要深入理解

第三层：创作机制
- 他如何观察世界？
- 他如何处理素材？
- 他如何构建意义？
- 这是深层的掌握，需要反复练习

【核心原则】
真正神似的作品，读者感受到的是"这很像他写的"，
而不是"这是在模仿他的风格"。
```

---

## 七位大师的精神内核

### 西方作家

#### 威廉·莎士比亚 (William Shakespeare, 1564-1616)

**精神内核**：对人性的深刻洞察，追问"人是什么？"

**核心母题**：人是矛盾的——伟大与渺小、理性与疯狂、爱与恨并存。

**神似要点**：不评判只展示矛盾；用独白追问存在问题；诗意语言触及真相而非装饰。

**创作机制**：确定核心矛盾 → 通过人物选择展示 → 让命运体现选择的代价 → 结尾不留答案。

**长篇适配**：莎士比亚式戏剧结构天然适合长篇——五幕结构（开端/上升/高潮/下降/结局），每"幕"对应一个叙事区块。长篇中可让不同人物负载不同的人性矛盾，形成对比复调。

#### 斯蒂芬·茨维格 (Stefan Zweig, 1881-1942)

**精神内核**：对人类情感的极致探索，追问"在命运面前，人能做什么？"

**核心母题**：命运的偶然性与人的尊严。

**神似要点**：心理描写如显微镜剥开表层；用克制表达最强烈的情感；长句累积情感最后释放。

**长篇适配**：茨维格式长篇以"情感聚焦"推进——每章深入一个人物的一次心理转折点。情感浪潮式推进：积累→爆发→退潮→再积累。长篇中可交替使用不同人物的内心视角。

#### 伊塔洛·卡尔维诺 (Italo Calvino, 1923-1985)

**精神内核**：对存在的轻盈追问，"如何用轻逸面对沉重？"

**核心母题**：存在的可能性与不可能性。

**神似要点**：精确描述奇幻意象；数学逻辑与想象结合；结构实验打破线性。

**长篇适配**：卡尔维诺式长篇以"结构游戏"驱动——章节可以是塔罗牌、城市目录、宇宙公式。长篇不是一条线而是一张网。每章可探索同一主题的不同"可能性"，用几何对称组织章节。

### 中国作家

#### 鲁迅 (1881-1936)

**精神内核**：对国民性的诊断，追问"中国人是什么？病在哪里？"

**核心母题**：中国人的精神困境——麻木、自欺、看客心态。

**神似要点**：批判来自悲悯不是优越；白描不加形容词和解释；反语让对方的话杀死对方；冷的表面下是深切的热。

**长篇适配**：鲁迅式长篇以"诊断式"推进——不是连续故事而是系列切片。每章是一个社会切面（教育/医疗/官场/家族），人物在不同切面中反复出现。长篇中"看客"可作为反复出现的集体角色。

#### 老舍 (1899-1966)

**精神内核**：对小人物的悲悯，追问"底层人如何活着？"

**核心母题**：小人物的挣扎与无奈。

**神似要点**：京味儿语言是身份不是装饰；幽默来自对生活的观察；口语化叙事像聊天；议论穿插叙事。

**长篇适配**：老舍式长篇以"命运沉浮"推进——一个或一群小人物的命运长河。时间跨度是天然结构（如《骆驼祥子》的三起三落）。章节间用命运转折点分隔，每个转折点让读者看到更深的社会底色。

#### 金庸 (1924-2018)

**精神内核**：用江湖写人生，追问"人如何选择？选择的代价是什么？"

**核心母题**：侠义、命运、选择。

**神似要点**：武功是性格的延伸不是技能；家国情怀通过选择体现；文白相间创造距离感；四字词语服务于意境。

**长篇适配**：金庸式长篇以"成长弧线"推进——主角从懵懂到成熟，武功从粗浅到精深，人格从单纯到复杂。章回体天然适合长篇连载。每回有独立看点（武打/情缘/揭秘），回尾留悬念。

#### 古龙 (1938-1985)

**精神内核**：对孤独的书写，追问"人活着为了什么？"

**核心母题**：孤独、友情、选择。

**神似要点**：极简不是目的是留白；短句控制节奏和情绪；不写武功过程只写结果；孤独中寻找温暖。

**长篇适配**：古龙式长篇以"悬念序列"推进——每卷是一个独立案件/对决，卷与卷之间由人物关系和更大的谜团串联。短章节天然适合（每章像电影一场戏）。长篇中"友情"可逐步深化，从陌生人到生死之交。

---

## 长篇创作工作流 / Long-Form Novel Workflow

### 项目模型 / Project Model

长篇项目以目录形式持久化存储，包含以下组件：

```
项目目录结构：
<项目名>/
├── project.yaml          # 项目元信息（标题/状态/字数/章节数/作者风格分配）
├── world-building.md     # 世界观设定（时代/地域/势力/规则/历史）
├── outline.md            # 完整情节大纲（三幕/五幕结构）
├── characters/           # 人物卡目录
│   └── <角色名>.md       # 单个人物卡（基本信息/性格/外貌/背景/关系/弧线/声线）
├── chapters/             # 已完成的章节
│   └── ch001.md          # 章节正文 + 章节元信息
├── foreshadowing.md      # 伏笔追踪器
├── recycle-bin.md        # 回收站（已删除内容备份）
└── review-log.md         # 审稿记录
```

### 第一步：创建项目 / Project Creation

使用 `/文豪 新建 <项目名>` 创建项目。

创建时至少录入：
1. **作品信息**：标题、类型、目标字数、叙事风格（可指定多位作家分配不同角色）
2. **世界观核心**：时代背景、核心设定（如力量体系/社会结构/关键规则）
3. **核心人物**：至少3-5个主要角色的人物卡（姓名/身份/性格/动机）
4. **情节大纲**：三幕或五幕结构（起承转合）

风格分配示例：
```
叙述者视角：老舍（市井温度 + 口语化叙事）
男主角内心独白：鲁迅（冷峻自省）
女主角对话：茨维格（克制深情）
战斗场景：古龙（极简 + 留白）
政治博弈：莎士比亚（戏剧冲突 + 人性复杂）
```

### 第二步：规划阶段 / Planning Phase

使用 `/文豪 规划` 进入规划模式，系统分析：

1. **当前位置分析**：
   - 上一章发生了什么？
   - 当前人物状态（物理位置/情绪/关系）
   - 已埋下的伏笔有哪些？

2. **本章目标设定**：
   - 本章必须推动哪条情节线？
   - 本章必须完成的人物弧线推进？
   - 本章的核心情绪是什么？

3. **人物出场计划**：
   - 谁必须出场？以谁的视角叙述？
   - 出场人物的当前状态是否与上次一致？

4. **冲突设计**：
   - 本章的核心冲突是什么？（内/外/人际）
   - 冲突如何升级或转折？

5. **伏笔管理**：
   - 本章需要埋下哪些新伏笔？
   - 本章需要回收哪些旧伏笔？
   - 回收时机是否恰当？

6. **钩子设计**：
   - 开篇钩子（300字内抓住读者）
   - 结尾钩子（让读者必须翻下一章）

### 第三步：章纲生成 / Chapter Outline

使用 `/文豪 章纲 <章节号>` 生成详细章纲。

章纲模板：
```markdown
## 第X章章纲

### 章节目标
- 必须完成：<具体情节目标>
- 情感目标：<读者读完后的感受>

### 出场人物
| 角色 | POV? | 状态 | 本章作用 |
|------|------|------|---------|
| ... | ... | ... | ... |

### 场景序列
1. [场景名称]
   - 地点/时间
   - 参与人物
   - 核心冲突/事件
   - 输出结果（进入下一个场景的原因）

### 伏笔
- 需回收：<伏笔编号及内容>
- 新埋设：<新伏笔内容和回收计划>

### 钩子
- 开篇：<钩子策略>
- 结尾：<悬念设计>
```

### 第四步：智能续写 / Smart Continuation

使用 `/文豪 续写` 进行章节创作。

续写流程：
1. **上下文加载**：自动加载项目状态、最近章节、相关人物卡、待回收伏笔
2. **章纲确认**：如果未生成章纲，自动生成并请用户确认
3. **风格分配**：根据项目配置，为不同段落/人物分配对应作家风格
4. **执笔创作**：以指定的作家精神内核驱动写作
5. **元信息记录**：章节完成后自动更新伏笔追踪器、人物状态

### 第五步：审稿与润色 / Review & Polish

使用 `/文豪 审稿` 进行全面编辑审查，五大维度：

| 维度 | 权重 | 检查要点 |
|------|------|---------|
| 一致性 | 25% | 人物性格/关系/状态是否与人物卡一致；世界观设定是否前后矛盾 |
| 节奏 | 20% | 场景长度变化、情绪曲线、信息密度分布 |
| 人物 | 20% | 人物行为是否有动机支撑；对话是否符合人物声线 |
| 伏笔 | 20% | 新伏笔是否合理；旧伏笔回收是否自然；是否有遗忘的伏笔 |
| 去AI化 | 15% | AIGC痕迹检测（参见 anti-aigc.md）；风格神似度评估 |

使用 `/文豪 润色 <文本>` 进行风格专项优化。

---

## 写作角色体系 / Writer Role System

### 策划 / Plot Planner
**职责**：设计情节结构、冲突升级、节奏控制
**使用**：`/文豪 策划`
**输出**：情节建议、冲突设计方案、节奏调整建议
**工作流**：分析当前大纲 → 识别薄弱环节 → 提出强化方案

### 人物设计 / Character Developer
**职责**：深度塑造角色，确保人物立体且有成长弧线
**使用**：`/文豪 人物设计`
**输出**：人物卡扩充、关系推演、弧线检查
**工作流**：审查现有人物卡 → 提出深化建议 → 更新人物发展轨迹

### 网文专家 / Web-Novel Specialist
**职责**：快节奏创作，爽点设计，断章钩子优化
**使用**：`/文豪 网文`
**输出**：爽点节奏建议、章节钩子强化、黄金三章检查
**工作流**：分析节奏 → 识别爽点密度 → 强化开篇和断章

### 风格优化师 / Style Optimizer
**职责**：提升文学质感，强化指定作家风格特征
**使用**：`/文豪 润色`
**输出**：润色后的文本 + 修改说明
**工作流**：读原文 → 识别风格薄弱处 → 以神似原则优化

### 编辑审稿 / Editor Reviewer
**职责**：全面审查，提出具体修改建议
**使用**：`/文豪 审稿`
**输出**：五维审查报告 + 逐段修改建议
**工作流**：通读全文 → 逐维审查 → 汇总报告

---

## 长篇一致性管理 / Consistency Management

### 人物一致性

长篇最大的挑战是人物性格在多章节中的一致性。核心原则：

1. **人物卡是锚点**：每次续写前必须回顾相关人物卡
2. **声线必须一致**：每个角色的对话风格（词汇/句式/节奏）在整部作品中保持稳定
3. **性格成长有迹可循**：人物变化必须有明确的触发事件，不能跳跃
4. **关系演变有因果链**：感情变化必须有持续的互动积累

人物弧线追踪模板：
```
弧线阶段：天真 → 受挫 → 觉醒 → 成熟
当前阶段：受挫（第12章，触发事件：背叛）
下次转折条件：第18章（计划：发现真相）
```

### 伏笔管理 / Foreshadowing Management

伏笔追踪器（`foreshadowing.md`）格式：
```markdown
| ID | 类型 | 内容 | 埋设章节 | 计划回收章节 | 状态 | 回收方式 |
|----|------|------|---------|-------------|------|---------|
| F01 | 人物 | 老管家右手的伤疤 | CH03 | CH15 | 已埋 | 揭示真实身份 |
| F02 | 物品 | 失踪的玉佩 | CH05 | CH20 | 已埋 | 关键证据 |
| F03 | 对话 | "三年前那场大火" | CH08 | CH22 | 已埋 | 真相揭露 |
```

伏笔操作规则：
- 每章至少埋1个新伏笔（短篇除外）
- 每章至少回收0-2个旧伏笔
- 连续5章未回收的伏笔标记为"⚠待处理"
- 回收伏笔时必须说明"前文回顾"（在哪一章埋的）

### 世界观一致性

1. **规则不可变**：核心设定（力量体系规则/社会制度/地理）不可前后矛盾
2. **规则可深化**：随着叙事展开，世界观可以"由浅入深"但不可"由A变B"
3. **检查点**：每10章做一次世界观一致性排查

---

## 单次创作流程（原有流程保留）

### 第一步：理解选题

在开始创作前，必须深入理解：选题的核心情感是什么？哪位作家的精神内核最契合？用什么体裁最合适？

### 第二步：深入作家

不只是阅读规则文件，而是：阅读作家的代表作感受他的节奏；理解他的精神内核——他追问什么？他如何回答？分析他的创作机制——他如何处理素材？

### 第三步：神似创作

核心原则：不是使用作家的词汇，是像他一样思考；不是模仿句式，是追问同类问题；不是堆砌意象，是让意象服务于主题。

### 第四步：自我审视

完成初稿后：这段文字，读者能感受到"像某位作家"吗？是形似还是神似？精神内核是否准确？创作机制是否运用得当？

---

## 风格迁移工作流 / Style Transfer Workflow

把一段已有的文本改写成另一位作家的声部，只换语言，不动情节、人物、场景。与单次创作的区别在于：单次创作是自由发挥，迁移必须守住原文的信息。

### 四层迁移法

按「声部 → 句法 → 结构 → 标记」依次施工，上一层没定，下一层不动笔。

| 层 | 做什么 | 关键项 |
|----|--------|--------|
| 声部 | 定叙述距离、温度、语体、介入度 | 贴身/旁观/介入；热/温/冷；口语/书面/文白 |
| 句法 | 换节奏与虚词 | 句长分布、虚词替换、标点密度、打断排比 |
| 结构 | 重切段落与信息节奏 | 段落长度方差、开场、收尾、议论位置 |
| 标记 | 换意象域与比喻来源 | 意象域、比喻密度、感官偏好、禁用词表 |

### 硬约束

1. 事件与因果、人物与关系、场景与关键数字，一律不得增删。
2. 目标文本长度与原文相当，允许上下浮动三成。
3. 迁移完成后必须逐句回对原文，列出信息对照。

### 执行步骤

1. 读原文，抽出一份「信息清单」（谁、做了什么、结果）。
2. 为目标作家写一份四层工艺档案。
3. 动笔改写，边写边守信息清单。
4. 回对原文，做节奏与去 AI 检查。
5. 出具校核评分。

### 分阶段路线

作者间迁移（可复核，如古龙→老舍）→ AI 文本与人文本互迁 → 检测评估对照。
详细的迁移矩阵、失败模式、可复现样例见 [rules/style-transfer.md](rules/style-transfer.md)。

---

## Rules

### 西方作家:
- [rules/shakespeare-style.md](rules/shakespeare-style.md) - 莎士比亚风格详解（含神似创作方法）
- [rules/zweig-style.md](rules/zweig-style.md) - 茨维格风格详解
- [rules/calvino-style.md](rules/calvino-style.md) - 卡尔维诺风格详解

### 中国作家:
- [rules/luxun-style.md](rules/luxun-style.md) - 鲁迅风格详解（含神似创作方法）
- [rules/laoshe-style.md](rules/laoshe-style.md) - 老舍风格详解
- [rules/jinyong-style.md](rules/jinyong-style.md) - 金庸风格详解（含神似创作方法）
- [rules/gulong-style.md](rules/gulong-style.md) - 古龙风格详解（含神似创作方法）

### 通用:
- [rules/vocabulary.md](rules/vocabulary.md) - 风格词汇库
- [rules/anti-aigc.md](rules/anti-aigc.md) - 文学创作反AIGC检测规则

### 风格迁移:
- [rules/style-transfer.md](rules/style-transfer.md) - 风格迁移规范（四层迁移法、作者间迁移矩阵、可复现样例）

### 长篇创作:
- [rules/novel-workflow.md](rules/novel-workflow.md) - 长篇创作工作流详解
- [rules/project-structure.md](rules/project-structure.md) - 项目文件格式规范
- [rules/character-consistency.md](rules/character-consistency.md) - 长篇人物一致性指南
- [rules/foreshadowing.md](rules/foreshadowing.md) - 伏笔管理规则
- [rules/editor-review.md](rules/editor-review.md) - 编辑审稿清单
- [rules/web-novel.md](rules/web-novel.md) - 网文创作专项规则

---

## Style Verification / 风格验证

### Shakespeare Style Check
- Does the text use iambic pentameter rhythm?
- Is the vocabulary Elizabethan-era appropriate?
- Are metaphors woven through the prose, not bolted on?
- Check: Read aloud — if it doesn't sound like a soliloquy, keep revising.

### Lu Xun Style Check / 鲁迅风格检查
- 语言是否有冷峻之感？
- 是否有"哀其不幸，怒其不争"的批判视角？
- 是否使用了鲁迅式比喻（如"铁屋子"）而非泛泛比喻？
- 检查：读完有无"寒到心里"的感觉？

### General Authenticity Check / 通用真伪检查
- Does the text reveal the author's spiritual core, not just surface mannerisms?
- Are the character voices consistent with the author's character archetypes?
- Would a well-read fan of this author know it's an imitation within the first 3 paragraphs?

### Style Transfer Check / 风格迁移检查
- 情节、人物、场景、关键数字是否与原文一一对应，无增无删？
- 段落长度是否有明显参差，还是被拉成一个节奏？
- 是否残留源作家的句法或对仗排比？
- 是否有为了贴目标作家标签而堆砌的意象？
- 情感是否通过细节传达，而非直接宣告？
- 目标作家的禁用词是否清干净？
- 逐句回对原文后，迁移评分是否达到合格线（60 以上）？

### Long-Form Consistency Check / 长篇一致性检查
- 人物性格在当前章节中是否与人物卡一致？（逐角色对照）
- 人物关系演变是否有充足的章节铺垫？（至少3章）
- 世界观设定是否前后自洽？（规则/地理/历史）
- 伏笔追踪器中有无连续5章以上未回收的伏笔？
- 人物对话声线是否在多章节中保持稳定？
- 章节间情绪曲线和节奏是否有过度跳跃？

---

## Edge Cases / 边界情况

- **Multi-author mashup**: When combining two styles (e.g., Shakespeare + Lu Xun), clearly label which sections use which style
- **Style transfer across languages**: 迁移到目标语言时保留语言的逻辑结构，把典故与俗语换成目标语言里对等的东西，不要直译
- **Style transfer of copyrighted source**: 源文本若仍在版权保护期（如古龙 1985 年逝世），样例中只作短摘并注明，成篇发表前确认授权
- **Style transfer with poetry source**: 诗歌迁移时优先保节奏与意象结构，允许信息密度适度重排，但要保留核心意象
- **Style transfer to the same author**: 目标与源相同，退化为「润色」，走 `/文豪 润色`，不走迁移
- **Modern topics in classical style**: Balance authenticity with readability; use footnotes for archaic terms when writing about contemporary subjects
- **Poetry vs Prose**: Different verification criteria for verse (rhythm + rhyme + imagery) vs prose (voice + structure + pacing)
- **Dialogue-heavy scenes**: Each character can have a different author style (e.g., Hamlet as Shakespeare, Horatio as Zweig)
- **Translation layer**: When writing in English mimicking a Chinese author (or vice versa), maintain the author's logic structure but adapt idioms to target language
- **长篇断更恢复**: 如果项目长期未续写，用 `/文豪 规划` 重新加载上下文和人物状态
- **角色数量过多**: 10个以上主要角色时，建议标注"核心/重要/次要"三级优先级，审稿时优先检查核心角色一致性
- **跨卷人物变化**: 人物经历重大事件后的性格转变，必须在人物卡上更新"当前阶段"和"触发事件"
- **伏笔遗忘**: 伏笔追踪器中超过10章未回收的伏笔，审稿时提示考虑删除或重新规划回收
- **风格疲劳**: 长篇创作中同一种风格篇幅过大可能导致读者审美疲劳，建议每5-8章切换一次叙述视角或插入"风格断点"（如一首诗/一封信/一段日记）
- **多作者协作**: 如果不同章节使用不同作家风格，在 `project.yaml` 中明确声明每章/每个人的风格分配
- **回收站清理**: 回收站内容建议按章归档，手动清理时间由用户决定

---

## Troubleshooting / 排查

- **Style too superficial**: If only surface-level vocabulary matches but spirit doesn't, re-read the author's seminal work before rewriting
- **Voice inconsistency**: If voice shifts mid-text, mark each paragraph's intended author style before writing
- **Anachronism**: If modern expressions leak into classical styles, maintain a "forbidden words" list per author
- **Over-imitation**: If the text becomes parody rather than homage, reduce signature phrases to 1-2 per page
- **长篇人物漂移**: 如发现人物行为与人物卡不一致 → 用 `/文豪 人物 <角色名>` 重新确认人物卡 → 对照审稿 → 必要时回退章节
- **情节前后矛盾**: 如发现本章事件与前文冲突 → 用 `/文豪 规划` 检查情节时间线 → 查阅大纲和章节目录
- **节奏拖沓**: 如连续3章无实质情节推进 → 用 `/文豪 网文` 检查爽点密度 → 合并或删减章节
- **伏笔线断裂**: 如果伏笔回收时机错误 → 用 `/文豪 伏笔` 检查追踪器 → 调整回收计划
- **项目文件丢失**: 项目目录下的文件如被误删 → 用 `/文豪 回收站` 查找备份 → 从审稿记录中重建草稿
- **迁移变成照抄**: 若生成结果与原文措辞几乎一致 → 在指令里明确要求「措辞与句式都要换掉，绝不照抄」→ 重跑
- **迁移后情节走样**: 若人物动作或结局被改动 → 用 `/文豪 迁移 校核` 逐句回对 → 回到信息清单重改
- **迁移后节奏被拉平**: 若各段长短接近 → 手工打断长句，制造一处三字短句的断裂
- **迁移出语法破碎或重复词**: 多出现在小参数量模型上（实测 8B 量级的文本扩散模型会产出「白银白银」「寒风像一把一样锋利的」）→ 换更强模型，或改由人执笔

---

## Usage Examples / 使用示例

### 单次创作 / Single-Shot
```
/文豪 鲁迅 "故乡的冬天，雪花无声地落在青瓦上"
/文豪 金庸 "大漠孤烟，一剑西来"
/文豪 老舍 "胡同里的早晨，豆汁儿的香气飘过"
/literary shakespeare "The tempest raged against the castle walls"
/literary calvino "The city unfolded like a page in an invisible book"
/literary zweig "She walked through the crowded station, a stranger among thousands"
```

### 风格迁移 / Style Transfer
```
/文豪 迁移 古龙→老舍 "冷风如刀，以大地为砧板，视众生为鱼肉。"
/文豪 迁移 老舍→鲁迅 src.md
/文豪 迁移 鲁迅 "他说这话的时候，脸上没什么表情。"
/文豪 迁移 校核 out.md 以鲁迅 原文 src.md
/文豪 迁移 矩阵
/literary transfer gulong->laoshe "The cold wind cut like a blade."
```

### 长篇创建 / Novel Project Creation
```
/文豪 新建 "长安雪"                                  # 创建项目
/文豪 设定 "唐玄宗天宝年间，长安城，江湖与朝堂双线"     # 录入世界观
/文豪 人物 "李白：青年剑客，豪放不羁，追求侠义之道"    # 创建人物卡
/文豪 大纲                                           # 生成三幕结构大纲
```

### 长篇续写 / Novel Continuation
```
/文豪 规划                    # 分析当前位置，确认下一章方向
/文豪 章纲 15                 # 生成第15章详细章纲
/文豪 续写                    # 基于章纲智能续写
/文豪 审稿                    # 审查一致性、节奏、人物、伏笔
/文豪 去AI味 "..."            # 专项消除AI痕迹
```

### 写作角色 / Writer Roles
```
/文豪 策划                    # 剧情策划：本章冲突不够，建议增加男二背叛线
/文豪 人物设计                # 人物开发：反派动机太单薄，建议补充童年创伤背景
/文豪 网文                    # 网文优化：黄金三章爽点密度不足，开篇钩子太弱
/文豪 润色                    # 风格优化：本章叙述偏平淡，建议切换为茨维格式心理描写
/文豪 审稿                    # 全面审查：发现3个人物一致性问题和2个伏笔回收时机问题
```

---

## AIGC-Aware Output

Literary works face the most sensitive AIGC detection. Each author's spiritual core must be authentically captured, not surface-level vocabulary imitation. Literary text must not show AI-typical patterns: uniform rhythm, direct emotion declaration, mechanical structure, or excessive transitional words. See `rules/anti-aigc.md` for writer-specific anti-AIGC strategies.

Key requirements per author:
- Luxun: Cold observation over hot declaration; irony over exposition; omission over explanation
- Laoshe: Beijing dialect as identity not decoration; humor from life observation not jokes
- Jinyong: Martial arts as character extension not skill listing; four-character phrases serve atmosphere not stacking
- Gulong: Extreme brevity is deliberate blankness; short sentences create rhythm not mechanical triplet
- Shakespeare: Soliloquy shows inner contradiction not conclusion; poetic language reaches truth not decoration
- Zweig: Microscopic psychological detail not panoramic; long sentences accumulate toward emotional release
- Calvino: Precise fantasy not exhaustive description; mathematical logic meets imagination genuinely

### 长篇反AIGC附加规则

长篇创作特有的AI痕迹模式：
- **人物行为模式化**：AI生成长篇时倾向让人物行为可预测——每次冲突都用同一模式解决。反制：引入意外选择，让读者感到"没想到但合理"。
- **情绪弧度均一化**：AI倾向每章情绪起伏曲线相同。反制：设计"平静章"穿插在"高潮章"之间，制造阅读节奏变化。
- **过渡词依赖放大**：长篇中AI对过渡词的依赖会被放大（"与此同时""另一方面"反复出现）。反制：长篇各章使用不同的过渡策略（动作过渡/场景切换/对话引入/完全不过渡）。
- **伏笔过于工整**：AI埋的伏笔通常在"恰好"的时机回收，缺乏生活的不规则感。反制：让部分伏笔提前回收（让读者意外），部分伏笔延后回收（让读者等待），避免所有伏笔均匀分布。

---

## Version History / 版本历史

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-04-01 | Expanded to 7 authors |
| 2.1.0 | 2026-05-09 | Added safety rules, style verification, edge cases, troubleshooting, vocabulary.md |
| 3.0.0 | 2026-07-14 | Major upgrade: long-form novel project management, multi-role writer system, planning-before-writing workflow, consistency management, foreshadowing tracker, smart continuation, editor review. 7-author system extended with long-form adaptation notes. Added 15 new commands, 6 new rules files. |
| 3.1.0 | 2026-10-13 | 新增风格迁移功能：`/文豪 迁移` 支持作者间声部改写，含四层迁移法、作者间迁移矩阵、分阶段研究路线与两组可复现样例（新增 rules/style-transfer.md）。补齐 6 个此前被引用但缺失的长篇规则文件（novel-workflow / project-structure / character-consistency / foreshadowing / editor-review / web-novel）。修正 skills.json 的版本与规则清单。 |

---

## See Also / 相关技能

- `/简写` from **brief-write** — 互补的简洁写作风格 / Complementary concise writing style
- `/人话` from **humanizer** — 检测文学模仿中的 AI 痕迹 / Detect AI patterns in literary imitation
- `/强力迭代` from **power-iterate** — 长篇项目的持续迭代创作 / Continuous iteration for long-form projects
