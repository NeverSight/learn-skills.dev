---
name: asu-resume-skill
description: 基于用户真实经历生成“阿酥式”高密度中文技术履历或小红书展示简历：保留真实姓名、学校、公司、部门、项目与可核验指标，主动检索学校官方 Title，以彩色经历条、背景/指标/职责结构、英文技术名词、架构链路、Benchmark、模块级 Owner、0→1 和大 Scope 叙事增强表达，并输出自包含 HTML、A4 PDF 与发布图片。用户提到阿酥风格、ASU 式简历、专业名词堆叠、技术经历包装、小红书履历长图、学校 Title、Owner/0-1 或要求 HTML/PDF 时使用。不得凭空创造不存在的学历、公司、项目、角色、Offer、指标或成果；夸张必须落在可证明的机构标签、限定模块和真实技术链上。
---

# ASU 式真实技术履历生成 Skill

生成“第一眼信息量爆炸，第二眼仍能逐条对应真实经历”的中文技术履历。默认面向小红书长图、技术主页和内部展示；用户明确要求求职版时，降低戏剧化措辞并保留相同事实

## 默认交付

1. `resume-data.json`：真实来源驱动的结构化履历。
2. `resume.html`：自包含、适合浏览器长图截图的网页。
3. `resume.pdf`：2–3 页 A4 PDF。
4. `xiaohongshu-copy.md`：基于真实经历的发布配文。

## 生成原则

### 真实骨架直接保留

用户授权提供的以下信息可以原样使用：

- 姓名、学校、学位、公司、部门、岗位和日期；
- 真实项目名、技术方案、论文/专利/分享；
- 文档中明确出现且口径可解释的指标；
- 用户本人对内部职责的一手陈述。

不要自动把真实名称改成“某公司”“某学校”，也不要在每项后添加“虚构”。只有用户要求匿名化时才替换。

### 只增强表达，不创造事实

允许：

- 把真实技术过程整理成 `输入 -> 表征 -> 规划 -> 工具 -> 状态 -> 评测` 链路；
- 将同一项目里的真实模型、框架、训练策略和部署组件集中呈现；
- 使用 `Workflow / ReAct / Harness / Context Engineering / Benchmark / ModelOps` 等与项目相符的术语；
- 用“从模型节点到 Agent 系统再到长程续跑”等宏观主线概括真实演进；
- 通过标题、排比、节奏和技术名词密度制造幽默反差。

禁止：

- 增加不存在的学历、Title、Offer、薪资、项目、开源角色或业务结果；
- 把 `参与` 改成 `主导/Owner/核心作者`；
- 把规划中的工作写成已经落地；
- 改写原始分母或把不同指标相加；
- 用公司、项目 Star 或团队成果暗示个人完成全部结果。

### 角色强度按来源写

- 来源写“独立负责” → 优先写 `模块级 Owner / 端到端链路 Owner / 从 0→1`，同时限定到具体模块；
- 来源写“主要负责” → 可写 `策略架构 Owner / 方向负责人`，正文保留具体责任边界；
- 来源写“参与推进/共建” → 写成 `系统级共建者 / 核心参与者`，不伪造为全局 Owner；
- 来源写“计划/未来方向” → 标成 `当前方向 / 规划中`，不能改成上线结果。

每个重点项目都要先做一次“Owner 化拆分”：寻找本人真正独立完成或主要负责的最小闭环，例如 `数据治理链路`、`策略架构`、`量化部署`、`分布诊断`。可对这个闭环使用 Owner 和 0→1，但不能把词的作用域外扩到整个公司平台。

### 学校 Title 增强

对教育经历必须查学校官网、教育主管部门或正式高校联盟页面，提取真实但高势能的机构标签：

- 建设序列：`双一流 / 原 211 / 部市共建 / 研究型大学`；
- 历史定位：`本国第一所大学 / 创校年份`；
- 高校联盟：`Group of Eight / C9 / Russell Group` 等真实成员关系；
- 学位事实：本科、硕士、联合培养和学位授予方必须分开，不能把地理位置或合作项目写成不存在的学位。

标题采用 `学校名｜机构 Title 1｜机构 Title 2｜学位`，把来源 URL 写入 `source_note`。不得将澳洲学历写成“美本”，也不得把部市共建写成“中央部委直属”。

## 视觉与措辞

生成前阅读 `references/style-guide.md`。必须具备：

- 蓝色衬线分区标题、浅红/浅蓝/浅绿经历条；
- 公司、部门、日期、方向标签同一行；
- 项目固定使用“背景 / 指标与效果 / 我的职责 / 技术关键词”；
- 每个重点项目至少 5–10 个与来源一致的专业术语；
- 能从来源成立的项目必须出现限定 Scope 的 `Owner`、`0→1` 与端到端闭环；不能成立时改用 `共建者/核心参与者`；
- 责任 bullet 优先使用技术链、失败分类、数据闭环或架构演进；
- 教育、实习/工作、技术项目与沉淀、奖项与技能等完整分区；
- 不添加水印、免责声明或“虚构”标记。

## 工作流

### 1. 完整读取经历来源

读取用户提供的简历、飞书文档、截图或个人主页。长文档先取目录，再按章节完整读取。对每段经历记录：

- 事实身份：组织、部门、岗位、日期；
- 角色边界：独立负责、主要负责、参与或规划；
- 项目目标、技术难点、方案链路；
- 指标、基线、结果与时间窗口；
- 模型、框架、训练、部署、数据与评测术语；
- 分享、专利、奖项和公开材料。

对每所学校额外检索官网、教育主管部门和正式高校联盟页，形成 `Title -> 官方原文 -> URL` 三列事实表，再选择 2–4 个最强且不重复的标签进入简历。

### 2. 建立来源映射

每个可见 bullet 使用：

```json
{
  "text": "通过结构化短 COT、真实执行 GRPO 与 AWQ 量化构建 NL2SQL 训练部署链路。",
  "verification": "source_grounded",
  "source_note": "晋升文档 / NL2SQL 章节"
}
```

文档中没有的内容不得补写。若是用户口述但无法公开核验，使用 `verification: user_attested`。

### 3. 提炼技术主线

优先选择能覆盖多段经历的真实演进，例如：

> 多模态内容理解 → Workflow 模型节点 → Search/通用 Agent → Context/Memory/Harness → 长程 Coding Agent

主线可以宏大，但每个节点必须在正文中有对应项目。

### 4. 生成 Owner / 0→1 / Scope 叙事

每个项目生成三层表达：

1. `Owner 作用域`：本人独立或主要负责的最小闭环；
2. `0→1 动作`：从无到有建立的模型、策略、训练、部署或评测链路；若只是优化存量系统，改写为 `X→Y 架构演进`；
3. `大 Scope`：列出该闭环真实覆盖的 Data / Model / Training / Serving / Agent / Eval 层，不把邻接团队成果算作个人成果。

示例：

```text
NL2SQL ModelOps 全链路 Owner：从 0→1 打通 Executable SQL Cleaning -> Structured Short COT -> GRPO Execution Reward -> AWQ -> SGLang Serving，覆盖数据、训练、强化学习、量化与推理部署。
```

### 5. 堆叠专业名词

从来源中提取名词，不自行随机添加：

- 模型与表征：CLIP、BERT、LanguageBind、VideoLLaVA；
- 训练：LoRA、Full SFT、DPO、GRPO、Short COT；
- 推理部署：AWQ、vLLM、SGLang、Prefill、Decoding；
- Agent：ReAct、Tool Use、Session、Memory、Context Engine、Checkpoint；
- 评测：Suite、Case、Grader、Transcript、Outcome、Artifact。

同一个 bullet 中术语之间必须有真实逻辑关系，不能只列名词。

### 6. 生成与校验

按 `references/resume-schema.md` 生成 JSON，然后运行：

```bash
python3 scripts/render_resume.py \
  --input /absolute/path/resume-data.json \
  --html /absolute/path/resume.html \
  --pdf /absolute/path/resume.pdf

python3 scripts/validate_resume.py \
  --data /absolute/path/resume-data.json \
  --html /absolute/path/resume.html \
  --pdf /absolute/path/resume.pdf
```

校验后把 PDF 每页转为 PNG，检查中文缺字、裁切、分页失衡和水印残留。网页版需做一次浏览器全页截图检查。

## 附带资料

- `references/style-guide.md`：版式和高密度技术措辞规则。
- `references/resume-schema.md`：来源驱动 JSON 格式。
- `assets/resume_template.html`：自包含中文模板。
- `scripts/render_resume.py`：HTML/PDF 生成器。
- `scripts/validate_resume.py`：来源标记、指标和文件完整性检查。
- `evals/evals.json`：中文测试任务。
