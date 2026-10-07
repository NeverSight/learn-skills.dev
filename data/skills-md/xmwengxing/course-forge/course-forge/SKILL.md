---
name: course-forge
description: 把知识文档或口播稿做成可交互的课程/课件——规划大纲章节、撰写与扩展口播稿、计算课时；课件含演示舞台(画布)+大纲章节导航+字幕+音频+播放/暂停/全屏控制+章节进度条。每屏内容逐步揭示、含动画、每3屏至少1处互动、禁止纯文字、口播对齐画面/字幕/音频。流程：立项(确认课时量/单课时长) → 口播稿撰写(大课可走立项→子代理逐章剧本→画面设计流程，剧本文字描述动画与互动) → 一次对齐5件事(稿子/outline/主题/素材/开发模式) → 逐章网页开发(第1章为锚点) → 可选TTS音频 → 部署/嵌入(视频录制为可选项)。动画默认基于 animejs + CSS/SVG/Canvas，高阶视觉可通过渐进式披露加载设计类 skill 或 MCP。本 Skill 沉淀设计方法论 + 协作流程，不绑定任何样式，可复用于任意主题。
---

# Course Forge — Interactive Courseware Builder

把一份知识文档或口播稿，一步步做成**可交互的课程 / 课件**：带演示舞台、章节导航、
字幕、音频、播放控制与章节进度条。产出物 = Vite + React + TS 项目，可嵌入任意 Web 应用，
也可选合成口播音频、可选录制成视频。

本 Skill **以方法论 + 协作流程为核心**。脚手架模板提供 token 和原语，但每个美学决策
（配色、字型、动效气质）都应针对你的主题重新设计——不要照搬。

## 适用场景

- 把口播稿 / 文章 / 课程大纲做成**可交互的教学课件**
- 需要大纲章节规划、口播稿撰写与扩展、课时估算
- 16:9 横屏、大字留白、每屏有动效、学员能动手互动
- 教学 / 产品演示 / 培训课件，想要电影感但不止于「视频」

---

## 术语表（唯一口径，全仓统一）

项目曾混用 `画面 / 章 / 屏 / 步 / section / segment / chapter`，造成 agent 误判。现统一如下（**屏 ≠ 步**：屏是画框容器，步是屏内揭示节拍）：

| 术语 | 含义 | 运行时对应 |
|---|---|---|
| **课程 Course** | 一次交付的完整课件，可是一门课或一整套体系 | `course.json` 根（`courseId` / `title`） |
| **大纲·分段 Outline Segment（原 S1~S5）** | 一级导航菜单项；按内容主题划分的块（如 导入/精讲/案例/收官），**段数依内容而定，不必是 5 段** | `course.json` 的 segment 条目（目标模型） |
| **章节 Chapter（章 / 课）** | 二级导航菜单项，一个独立教学单元/知识点，如「1.1 你好，数字世界！」。一个章节由 1 屏或多屏组成 | `course.json` 章节条目 + `chapters.ts` 注册 |
| **屏 Screen（画面）** | 章节内的 1920×1080 视觉画框（容器），承载多个步；1 章 = 1 屏 或 多屏讲完 | 章节 `.tsx` 内按屏切换的视图 |
| **步 Step** | 屏内**原子揭示单元**：**1 步 = 1 口播节拍 = 1 字幕窗 = 1 音频段**；逐步揭示 = 一屏内逐个点亮各步 | 章节 `.tsx` 的 `step` + `narrations.ts` 的一项 |

辅助（非结构单元）：**Stage** = 1920×1080 画框；**Canvas** = 渲染技法；**卡片** = 内容元素。

🚫 **禁用**：`slide` / `PPT`。**屏 ≠ 步**——屏是画框容器，步是屏内揭示节拍。详情见 `references/COURSE-STRUCTURE.md`。

---

## 工作流总览

```
Phase 0   立项（课时量大时必做；见 references/SCRIPT-WRITING.md）
   0.1  确认课时量（几节课）+ 每节课平均时长
   0.2  产出 brief.md（基础课程大纲：一级=课、二级=小节）→ 用户确认冻结
   ▼
Phase 1   口播稿撰写（剧本）
   1.1  识别用户输入（文章 / 口播稿 / 仅主题→反问）
   1.2  短视频小课：一次产出 script.md + outline.md（inline）
        大课 / 需分工：按 references/SCRIPT-WRITING.md 逐课写"剧本"（按课并行子代理，课内单代理）
   ▼
[Checkpoint Plan]      ← 必须停。一次对齐 5 件事：
                         稿子 / outline / 主题 / 素材 / 开发模式
   ▼
Phase 2   网页开发（逐章）
   2.1  脚手架（按选定主题）
   2.2  第 1 章 = 主线程 + 完整版本（强制 anchor）
        ▼  [硬节点] 用户验收第 1 章 ← 不可跳过
   2.3  第 2~N 章（模式：A 逐章 / B 顺序 / C 并行）
   2.4  实现单章（每章必走：逐步揭示 / 动画 / 互动 / 双源）
   ▼
[Checkpoint Audio]     ← 必须停。是否合成音频
   ▼
Phase 3   音频合成与字幕（可选）
   ▼
Phase 4   部署嵌入 / 可选录屏
```

> 没有「模式判断」步骤——本 skill **只有一种产出：交互式课程 / 课件**。视频录制
> （`references/RECORDING.md`）只是 Phase 4 的**可选项**，不影响主流程。

---

## 文件读取指南

**长会话里 agent 容易遗忘原则**，尤其 Phase 2.4 会重复 N 次。按下表**只读必需文件**。

| 阶段 | 必读（每次都看） | 按需查 |
|---|---|---|
| Phase 0 立项 / Phase 1.1-1.2 内容编写 | `references/SCRIPT-STYLE.md` + `references/OUTLINE-FORMAT.md` + `article.md`（用户原文，如有） | 大课 / 需分工 → `references/SCRIPT-WRITING.md`（立项 + 逐课剧本 + 按课子代理分工 + 跨课衔接） |
| **Checkpoint Plan 选主题** | —— | `themes/*/theme.json`（动态读全部，列清单 + `bestFor` 推荐 + `descriptionZh`）；`references/THEMES.md`；`references/COURSE-STRUCTURE.md`（课程结构） |
| Phase 2.1 脚手架 | —— | 本文件 § Phase 2.1 看一次 |
| **Phase 2.4 实现单章（×N）** | **`references/CHAPTER-CRAFT.md`** 单一入口 + 当前主题 `themes/<id>/theme.json` + 本章 outline.md 段落 + `article.md` 本章段落 + 素材清单 | `references/THEMES.md` 完整 token 契约；`references/ANIMEJS-GUIDE.md`（需真动画时，材质 8 手法为硬约束） |
| Phase 3 音频合成 | `references/AUDIO.md`（narrations.ts → segments.json → 任意 provider） | `scripts/tts-providers/README.md`（换 / 自带 provider 时） |
| Phase 4 部署 | `references/DEPLOYMENT.md`（嵌入） | `references/RECORDING.md`（可选录屏） |

> **写章节时只读一份 `CHAPTER-CRAFT.md`**：十条原则 / 开工 self-prompting / 决策树 /
> 反 AI 味 / 完工自检全部并入这一份。

---

## 硬性自检协议

每个产物（`script.md` / `outline.md` / 单章）完成后**必须**走 **自检 → 修复 → 汇报**。
直接汇报原始结论 = 违规。

| 产物 | 自检清单出处 |
|---|---|
| `script.md` | `references/SCRIPT-STYLE.md` 三层自检 |
| `outline.md` | `references/OUTLINE-FORMAT.md` 自检 |
| 单章实现完成 | `references/CHAPTER-CRAFT.md` § 完工自检 + 课件内容硬规则（见下） |

**执行方式**（按能力降级，优先更隔离的方式）：
1. **Agent Teams**：开独立 reviewer agent，给它产物路径 + 对应清单 + 关键上下文，逐项核查
2. **subAgent**：开 subagent 走同样流程
3. **自检**：自己严格逐项核查，不允许目测一遍就放行

---

## 各阶段产出文件

agent 在用户当前目录下创建 / 编辑：

```
my-course/
├── article.md          # 用户给原文时必有——不删！开发阶段画面信息源
├── brief.md            # 大课立项产出：课时量 / 单课时长 / 一级=课二级=小节的基础大纲（用户确认后冻结）
├── script.md           # 短视频小课：保持原文语言的平台化口播稿（决定节拍）
├── script/             # 大课：逐课"剧本"（每课 1 子代理写全部小节；口播 + 画面意图 + 互动意图 + 主题小节 + 字数/时长）
│   └── NN-id.md        #   每小节一份，详见 references/SCRIPT-WRITING.md
├── course-bible.md     # 大课：跨课交接物（已完成课的主题/术语/课末钩子），子代理写新课前必读
├── outline.md          # 短视频小课：开发计划（大纲·分段切分 + 章节切分 + 每屏/每步内容 + 信息池）
└── presentation/       # 脚手架产出的 Vite + React + TS 项目
    ├── src/chapters/<NN>-<id>/
    │   ├── <Chapter>.tsx     # 视觉实现（按 屏/step 逐步揭示）
    │   ├── <Chapter>.css
    │   └── narrations.ts     # ★ 步数（口播节拍）+ 口播文本的唯一真相源；屏数由各章结构推导
    ├── src/registry/chapters.ts    # 章节注册（含可选 quizzes 数据驱动交互）
    ├── course.json                 # 课程结构（大纲·分段 + 章节菜单，放项目根）
    ├── scripts/
    │   ├── extract-narrations.ts   # 扫所有 narrations.ts → audio-segments.json
    │   ├── synthesize-audio.sh     # provider-agnostic runner
    │   ├── subtitle-timing.py      # --chapters 可过滤
    │   ├── regenerate-course-json.py  # 校验 + 格式化 course.json
    │   ├── lint-course.py          # 校验 5 条硬规则（npm run lint）
    │   └── tts-providers/          # 每 provider 一个 .sh（minimax 默认 / openai 内置）
    ├── audio-segments.json         # extract 产出（合成前 review）
    └── public/audio/<id>/<N>.mp3   # 可选：合成的音频
```

> **关键不变量**：`narrations.ts` 是**步数（口播节拍）**和音频合成的**唯一真相源**；**屏数由各章结构（屏边界）推导，不手填**。章节 `.tsx` 里
> `if (step === N)` 的最大 N + 1 必须等于 `narrations.length`（步数）。这保证 5 处
> （script / outline / 章节代码 / chapters.ts / 音频文件）永远不漂。

---

## 核心不变量 + 课件内容硬规则

### 3 条架构不变量

1. **`narrations.ts` 是单一真相源** —— 数组长度 = 章节**步数（口播节拍）** = `max(if (step === N)) + 1`；**屏数由各章结构推导（1 章可 1 屏或多屏），不手填**。
2. **主题 = CSS token + JSON 元数据** —— 切主题只覆盖 `tokens.css`，组件不引入主题专属值。
3. **每章渲染进固定 1920×1080 舞台** —— `useStageScale` + `transform: scale()`，不用视口像素。

### 5 条课件内容硬规则（每章完工必须全过）

1. **逐步揭示**：每屏内内容随 **步(step)** 推进逐项亮起，禁止一次性全展示。一个清单/多想法的展开 = 多步，**清单 1 项 = 1 步**（不是 1 屏）；一屏可含多步。
2. **动效必具**：每屏至少 1 处动态元素或动画（CSS / SVG / Canvas / JS）；静止屏 = 不合格。
3. **互动密度**：每 **3 屏** 内至少 1 处**真互动**（点击 / 拖拽 / 选择 / 输入触发 `useState`）；
   `hover` / 翻页导航 ≠ 互动。无互动 = 回去加。
4. **禁止纯文字**：每屏不得仅为文字；必须有视觉演示 / 图形 / 媒体。
5. **口播对齐**：口播文本、屏上元素、字幕、音频（若合成）必须一一对应；守 `narrations.ts` 不变量。

> 这 5 条是「交互式课程」区别于「视频」的核心。已由 `scripts/lint-course.py`
> （脚手架接入 `npm run lint`）在每章完工后自动拦截。

---

## Phase 1 —— 内容编写

### 1.0 立项（课时量大时必做）

当课程进入"多节课 / 每课数十分钟"区间，先走 `references/SCRIPT-WRITING.md` Phase 0：
确认 **课时量（几节课）** 与 **每节课平均时长**，产出 `brief.md`（一级=课、二级=小节的基础大纲），
**停下让用户确认冻结**，再进入 1.1 / 1.2。短视频小课可跳过本步。

### 1.1 识别用户输入

| 用户给的 | 该做的 |
|---|---|
| 原始文章（书面语 / 公众号 / 论文 / 博客） | 一次产出 `script.md` + `outline.md`（1.2），过 Checkpoint Plan |
| 口播稿 / 视频脚本 | 落盘成 `script.md`，产出 `outline.md`（1.2 简化版），过 Checkpoint Plan |
| 啥都没有，只说「做个 X 主题的课程」 | **反问**：先给素材或大纲。Skill 不替用户构思内容 |

### 1.2 一次产出 script.md + outline.md（同一次思考中完成）

1. **`script.md`**：按 `references/SCRIPT-STYLE.md` 把 article 转成保持原文语言的平台化口播稿。
   **保留 `article.md` 不删** —— 它是画面细节源（双源原则）。
2. **`outline.md`**：按 `references/OUTLINE-FORMAT.md` 切**章节** + 切**屏** + 每章首段抽**信息池**。

**outline 的边界**：

| outline 必须写 | outline 不要写 |
|---|---|
| 章节切分 / 每章屏数 / 估时 | 具体动画类型（blur / wipe / 弹簧） |
| 每屏内容（hero / 数据 / 标语 / 列表项） | CSS 实现手段（filter / SVG / clip-path） |
| 章节级**信息池**（从 article 抽的数字 / 引用 / 案例） | 时长数值 |
| 屏级关系名前缀（「反差对照」/「金句」等可选 hint） | 持续微动 / 错峰量等微观节奏 |

> 理由与展开见 `references/CHAPTER-CRAFT.md` § 这是课件不是 PPT / § 双源原则。

**落盘后先走「硬性自检协议」再进 Checkpoint Plan。**

> **大课 / 需分工**：课时量大时，不要一次性憋出整课 `script.md`，改按
> `references/SCRIPT-WRITING.md` 把口播稿拆成**逐课剧本**（`script/NN-id.md`，每课 1 子代理写全部小节）——
> 可**按课分配子代理并行**写（课内单代理保证连贯）、用 `course-bible.md` 保证跨课衔接、剧本里**用文字描述动画与互动意图**
> （不写具体实现代码）。剧本阶段就完成"画面/互动设计"的脚本化，主代理 Phase 2 直接按剧本实现。

---

## Checkpoint Plan —— 5 件事一次对齐（**硬节点**）

`script.md` + `outline.md` 写完必须停。**用户在这一个节点同时确认 5 件事**：

1. 稿子（script.md）
2. 开发计划（outline.md）
3. 主题（从 `themes/*/theme.json` 读出，按 `bestFor` 推荐 2~3 套）
4. 素材（列粗略清单 → a) 我帮你挑 b) 你提供 c) 全 placeholder）
5. 开发模式（A 逐章 / B 顺序 / C 并行）

**agent 预备**：动态读所有 `themes/*/theme.json`（不硬编码清单）；按 script 内容 / 语气挑
2~3 套 `bestFor` 命中的；扫 `outline.md` 末尾「素材清单」。

**模式说明**：

| 模式 | 节奏 | 何时用 |
|---|---|---|
| **A · 逐章确认（默认）** | 每章做完 → 暂停验收 → OK → 下一章 | 用户不明确选模式时默认 |
| B · 第 1 章后顺序开发 | 第 2~N 章主线程顺序做完，最后统一验收 | 不支持并行任务的环境 |
| C · 第 1 章后并行开发（subagent） | subagent 并行做第 2~N 章，并行数由用户控制 | 最快，但各章风格有差异 |

**第 1 章无论哪种模式都必须主线程做完 + 用户验收**（强制 anchor）。

收到反馈后：稿子 / outline 要改直接编辑；**主题必须明确**才进 Phase 2（用户说「你帮我选」
→ 取推荐第 1 个并说明理由，给反悔机会）；模式选定 → 进 Phase 2。

---

## Phase 2 —— 网页开发

### 2.1 脚手架

```bash
bash <path-to-course-forge>/scripts/scaffold.sh ./presentation --theme=<id>
bash <path-to-course-forge>/scripts/scaffold.sh --list-themes
```

> ⚠️ **`course.json` 单一源**：放**项目根**（`./course.json`），**不要**拷到 `public/course.json`。
> `useCourseLoader` 走 vite **静态 import**，不发网络请求；手动拷到 `public/` 后源文件改动不同步。
> CI 阶段跑 `scripts/check-course-json-sync.sh` 会自动检测这个错。
>
> 自定义主题 → 先按 `references/THEMES.md`「创作新主题」做一个 `themes/<my-theme>/`，再 `--theme=<my-theme>`。

本模板**不带示例章节**（避免风格固化）。从零创建第一章：`mkdir src/chapters/01-<id>` →
写 `<Chapter>.tsx` + `.css` + `narrations.ts`（见 `references/CHAPTER-CRAFT.md`，含「视觉焦点与着重渲染」四大支柱）→
在 `registry/chapters.ts` 注册 → 在 `course.json` 加章节条目。

### 2.2 第 1 章 —— 主线程 + 强制验收

**核心**：第 1 章 = 完整版本一次到位（节奏 + 视觉 + 真素材齐全）。**没有「骨架版」** ——
第一章就要做出用户能直接验收的样板。

必须主线程的理由：它是 `CHAPTER-CRAFT.md` 在当前主题 + 题材下的第一次落地，若指引有盲区 /
token 不够用会立刻暴露，早改成本最低；后续章节都参考它的代码模式。

做完后停下等验收，给 dev server 链接（默认 `http://localhost:5174/`，多课程 `?course=<id>`）。

**验收重点**：
- □ 视觉气质 / 节奏对不对？某些屏太快 / 太慢 / 信息太薄？
- □ 内容驱动动画是否到位？还是有几屏是无脑入场动画？
- □ 双源原则：画面有没有「口播没念但 article 能挂」的细节？
- □ **逐步揭示**：除开场 hook 屏外，**每屏独立槽位 ≥ 2**？屏内仅 1 个独立信息 = 反模式，回去拆
- □ **互动点**（每 3 屏内 ≥ 1 处真互动）：onClick / onChange / drag / 切 tab 触发 `useState` = 合格；
  hover / transition / 「看完点下一屏」的导航 **≠ 互动**。无互动 = 回去加
- □ **禁止纯文字**：每屏是否有视觉演示 / 图形 / 媒体？
- □ 反 AI 味（视觉）：紫粉渐变 / 圆角彩边 / 假插画 / emoji？
- □ 反 AI 味（内容）：假共情 / 万能模板 / 自我标榜 / 排比堆砌？见 `references/SCRIPT-STYLE.md` § 去 AI 味五类
- □ DevTools 切 1920×1080 / 1280×720 两视口：内容不被裁切
- □ **`?auto=1` 验收需音频**：若要用自动播放（`?auto=1`，音频+字幕+自动推进）验收，**必须先合成该章音频**（提前走 Phase 3 的 extract→synthesize→subtitle 三步），否则只能手动点击推进验收（无音频时 Auto 模式退化为字数估时，听不到口播）

### 2.3 第 2~N 章 —— 按选定模式

每章独立按 `references/CHAPTER-CRAFT.md`（单一必读入口）开发。**风格不强求章节间完全一致** ——
主题颜色 / 字体 token 兜底统一，动画 / 节奏 / 视觉演示由章节自由发挥是设计预期。

> **默认「逐节开发」**：除非用户明确要求「多节」或「全部」，单次只实现 / 渲染 / 验证**一个小节**（= 二级章节）。用户显式点名多个小节（如「开发 01 和 02」）才是多节请求。这样改动范围小、易审查、可逐步回滚。

### 2.4 实现单章（每章必走）

**核心要点**（详见 `references/CHAPTER-CRAFT.md`）：
- **每章必须有 CSS / SVG / Canvas / JS 视觉演示**，禁纯文字章节
- **逐步揭示**：清单 / 列表 1 项 = 1 步，禁一次全展示；一屏含多步逐步亮起
- **每 3 屏至少 1 处真互动**（点击 / 拖拽 / 选择 / 输入）
- **双源原则**：节奏跟口播稿（顺序不乱），细节回原文章抽（信息池 + 本章 article 段落）
- **动画 / 交互设计能力（渐进式披露）**：见下
- **完工自检逐项过**，按「硬性自检协议」+ 课件内容硬规则执行，改完再向用户汇报本章交付

#### 动画与交互设计能力（渐进式披露）

本 skill 的动画默认基于 **animejs v4 + CSS / SVG / Canvas**（详见
`references/ANIMEJS-GUIDE.md`），足以覆盖多数章节的逐步揭示与动态元素。

当某章需要**更高阶的视觉 / 交互设计**（复杂动效编排、专业级交互原型、设计系统级质感）时，
agent **应**通过**渐进式披露**按需加载现成的**设计类 skill 或 MCP**：

- 在对话中调用对应的设计 skill / MCP 获取专业能力，再把结果落回本 skill 的章节实现约定
  （仍守 `narrations.ts` 不变量与 5 条硬规则）；
- **本仓库不硬编码具体依赖**——要加载哪个设计 skill / MCP，由运行时按可用环境决定；
- 具体常用组合会在后续课件开发测试中逐步迭代确定，并回填到本段。

> 这是本项目最难的部分。先保证「每屏有动画 + 每 3 屏有互动 + 口播对齐」的基线，
> 再借设计 skill / MCP 提升上限，通过真实课件测试持续打磨。

**基线工具已内置，优先用**：
- **元素级逐步揭示**优先用 `Reveal` 组件（`templates/src/components/Reveal.tsx`，支持
  `rise / scale / pop / fade` 变体 + `delay`/`duration`），不止文字——包裹卡片 / SVG 组 /
  图片 / 按钮即可随 `step` 逐元素进场，避免手写重复 CSS。
- 每章完工跑 **`npm run lint`**（`templates/scripts/lint-course.py`）——静态校验 5 条硬规则
  （视觉演示 / 互动密度 / 逐步揭示 / 口播对齐），0 FAIL 才向用户汇报。

### 2.5 大改后 bump STORAGE_KEY

改动 `chapters.ts`（增删 / 重排章节，或某章 `narrations.ts` 长度变化）后，**bump**
`hooks/useStepper.ts` 的 `STORAGE_KEY`（如 `v4`→`v5`），避免持久化游标落到不存在的屏。

---

## Checkpoint Audio —— 是否合成音频（**硬节点**）

Phase 2 结束后必须停，问用户是否合成音频（自动播放 / 字幕对齐）。
**合成** → Phase 3；**不合成** → 直接 Phase 4（手动播放 + 可选后期配音）。

> **anchor 验收的特殊性**：第 1 章 anchor 验收（Phase 2.2）若用户想用 `?auto=1`（自动播放 + 字幕），
> 需在验收前先合成该章音频（提前走 Phase 3 的 extract→synthesize→subtitle 三步）。即 anchor 的音频
> 合成可前移到 Phase 2.2 验收前，不必等 Phase 2 全部完成——这是唯一允许 Phase 3 提前的场景。
> 不合成音频时，anchor 只能手动点击推进验收。

---

## Phase 3 —— 音频合成与字幕（可选）

详见 `references/AUDIO.md`。

---

## Phase 4 —— 部署嵌入 / 可选录屏

课件 `dist/` 是纯静态文件，两种分发任选或并用：
- **嵌入 Web 应用** —— `references/DEPLOYMENT.md`
- **录制为视频（可选）** —— `references/RECORDING.md`，仅作后期分发，不影响主流程

---

## 十条原则（一句话索引）

完整展开见 `references/CHAPTER-CRAFT.md` § 这是课件，不是 PPT —— 写章节时回那里查。

| # | 原则 | 一句话 |
|---|---|---|
| 1 | 16:9 固定舞台 | 内容 1920×1080 + transform scale，没有响应式 |
| 2 | 全局 step 计数器 | 章节是 step 的纯函数，无定时器 |
| 3 | 每步独占整屏 | `if (step === N) return <FullScene />` |
| 4 | 口播节拍 = step（步） | 一节拍 = 一步 = 一聚焦想法；一屏 = 多步 |
| 5 | 隐藏的边角控件 | 进度条 / 翻页器默认 opacity 0 |
| 6 | 舞台无 chrome | 没有 header / footer / 页码 / 品牌条 |
| 7 | 内容驱动动画 | 先找内在动作，找不到才入场动画兜底；持续微动慎用 |
| 8 | 逐步揭示（同屏多槽位、步推进逐项亮） | 1 项 = 1 步 = 该项在屏内某槽位被激活。**一屏含多个步**，步 N 激活第 N 个，其余灰化保留作上下文；**除开场 hook 屏外，每屏 ≥ 2 步（≥ 2 独立槽位）**。屏内仅 1 步（1 个独立信息）= 反模式 |
| 9 | 整片同一主题 | 章节间不翻表面色；颜色 / 字体走 token，其它尺度章节自由 |
| 10 | 双源原则 | script 定节拍，article 定画面密度（落到信息池） |

---

## 参考文档速查

按「何时读」标注，避免一次性全读。各文件对应阶段已见上文「文件读取指南」，此处按文件角度补充：

| 文件 | 何时读 |
|---|---|
| `references/SCRIPT-STYLE.md` | Phase 1.2 必读 — 文章→口播稿规则、平台变体、去 AI 味五类 |
| `references/OUTLINE-FORMAT.md` | Phase 1.2 必读 — outline.md 字段 spec、章节切分、信息池 |
| `references/SCRIPT-WRITING.md` | 大课 / 需分工 — 立项 + 逐课剧本(按课并行子代理/课内单代理) + 字数/时长公式 + 跨课衔接(course-bible) |
| `references/CHAPTER-CRAFT.md` | **Phase 2.4 每章单一入口** — 十条原则 / 视觉演示 / 逐步揭示 / 双源 / 反 AI 味 / 代码红线 / 完工自检 / animejs 升级 |
| `references/ANIMEJS-GUIDE.md` | 需要「真动画」或「物理级拖拽」时 |
| `references/ANIMATION-RECIPES.md` | Phase 2.4 做画面时 — 原子动画配方（glow/对比/聚焦/描线/粒子/弹性/count-up/字符级/组装，每条映射四大支柱），从 heygen-com/hyperframes 移植为 anime.js v4.4.1 |
| `references/SCENE-BLUEPRINTS.md` | Phase 2.4 做画面时 — 多阶段场景编排骨架（开场/对比/数据/概念墙/关系网/逐字/放大揭幕） |
| `references/PALETTES.md` | Phase 2.4 做画面时 — 按章节情绪选配色（9 套 mood → theme token 映射） |
| `references/COURSE-STRUCTURE.md` | 课程结构（课程 > 大纲·分段 > 章节 > 屏 > 步）、密度约束、chrome 组件 |
| `references/THEMES.md` | 选 / 造 / 切主题 — token 契约 + 内置主题 + 创作流程 |
| `references/AUDIO.md` | Phase 3 — provider-agnostic 音频合成、故障排查 |
| `references/RECORDING.md` | Phase 4 — 可选录屏工具 + 后期合成 |
| `references/DEPLOYMENT.md` | Phase 4 — 部署嵌入决策树 + 方案范本 |
| `themes/` | Checkpoint Plan / Phase 1.2 — 内置主题（`theme.json` + `tokens.css`） |
| `scripts/scaffold.sh` | Phase 2.1 — 一键项目脚手架 |
