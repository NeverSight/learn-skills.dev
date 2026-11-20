---
name: study-buddy
description: 帮同时修多门晦涩课程的大学生，用最少时间让每门课的考核达到及格线，也可以按课程设目标分冲高分。它能把老师发的大量课件和资料转写成按知识点排布的讲义，规划全学期每周要准备什么，按讲义逐节带学，考前根据剩余时间和往年题速通全部考点，并完整完成个人或小组的presentation、课程论文、case study、task和其他作业。当用户说“这门课怎么及格”“这门课想冲90”“老师发了一堆课件”“带我学下一节”“后天考试”“下周要做pre”“要交一篇论文”“这个case study怎么写”时使用，即使用户没有提到“学习”。用户说“更新study-buddy”时也使用。不用于深入研究，不在考试或限时测验进行中代答，也不做选课咨询和职业规划。
version: 3.12.1
---

# 学习搭子（study-buddy）

## 背景

大学生一个学期要修很多门互不相关的课，课程晦涩，课本知识又和产业实践脱节，学习的实际目的只是通过考核。本skill帮用户用最少的时间让每门课的考核都达到及格线：把资料整理成好懂的讲义，规划每周该做什么，带着学，考前速通，作业和论文直接产出完整成品。用户的学校允许用AI完成学业任务，所以作业类一律尽力帮；只有考试进行中不代答。

## 文件结构

```
study-buddy/
├── SKILL.md
├── CHANGELOG.md
├── workflows/
│   ├── first-time-setup.md               # 首次使用
│   ├── organize-materials.md             # 资料整理
│   ├── plan-semester.md                  # 学期规划
│   ├── design-learning-style.md          # 设计学习风格
│   ├── study-with-notes.md               # 跟课学习
│   ├── cram-for-exam.md                  # 期末速通
│   ├── make-exam-notes.md                # 考试提纲（开卷提纲、小抄、教材查阅指南、闭卷背诵稿）
│   ├── prepare-presentation.md           # Presentation
│   ├── write-course-paper.md             # 课程论文
│   └── complete-assignment.md            # 完成作业
├── references/
│   ├── introduction.md                   # 使用指南
│   ├── qa.md                             # 疑难问题处理
│   ├── setup.md                          # 各平台的Python依赖、Office COM与LibreOffice检查、OCR接口检查、config.json的填写方法、ocr_cli.py的参数与退出码
│   ├── data-layout.md                    # 数据目录、课程与chapter编号、命名与覆写规则
│   ├── score-strategy.md                 # 目标（保过/高分）、差距计算、考核性价比、保过方案和高分方案
│   ├── material-processing.md            # 范围确认、草稿与图片转写的读法、知识结构重排、考点信号、讲义写法
│   ├── semester-planning.md              # 截止时间倒排、风险排序、每周负荷
│   ├── guided-study.md                   # 讲解深度、看不懂时怎么换讲法、小测题型、错题记录
│   ├── style-guide.md                    # 学习风格的格式、位置、不能改的边界、怎么引导用户设计
│   ├── styles/
│   │   ├── textbook.md                   # 教科书式（默认）
│   │   ├── socratic.md                   # 苏格拉底式
│   │   └── story.md                      # 故事式
│   ├── exam-cramming.md                  # 诊断、时间分配、检索/间隔/交错练习、往年题、模拟
│   ├── exam-notes.md                     # 考试规则对应的产出、各提纲怎么写、tex写法、编译失败怎么改
│   ├── community.md                      # 什么时候给赞赏码和反馈群二维码、怎么给、群二维码的有效期
│   ├── presentation.md                   # 评分维度、结构、页数与时长、讲稿、Q&A
│   ├── course-paper.md                   # 论文结构、GB/T 7714、文献检索与核实
│   ├── assignment.md                     # 作业要求拆解、case study结构、task与习题交付
│   ├── group-work.md                     # 分工方式、RACI、衔接与整合检查
│   └── deliverables.md                   # 提交语言与翻译、图表由agent构建、底稿与提交文件的关系、格式转换
├── assets/
│   ├── templates/
│   │   ├── semester.template.md          # 学期规划.md（跨课总览）
│   │   ├── course-info.template.md       # 课程信息.md（单课考核信息）
│   │   ├── index.template.md             # 讲义目录.md
│   │   ├── chapter.template.md           # 一节讲义（讲解 + 查阅两部分）
│   │   ├── preference.template.md        # 学习偏好.md
│   │   ├── project-rules.template.md     # 空目录初始化时写入 CLAUDE.md 和 AGENTS.md 的项目规则
│   │   ├── exam-open.template.tex        # 开卷提纲（目录、术语/公式/题型速查表）
│   │   ├── exam-sheet.template.tex       # 小抄（三栏，限页数时自动缩放）
│   │   ├── exam-textbook.template.tex    # 教材查阅指南（考点对应教材页码）
│   │   ├── exam-closed.template.tex      # 闭卷背诵稿，同源可编译填空版
│   │   ├── mistakes.template.md          # 错题本
│   │   ├── cram-plan.template.md         # 速通计划
│   │   ├── presentation.template.md      # pre结构、PPT大纲、讲稿、Q&A
│   │   ├── paper.template.md             # 论文骨架
│   │   ├── assignment.template.md        # 作业要求拆解和交付物骨架
│   │   ├── group-plan.template.md        # 小组分工表
│   │   ├── submission-check.template.md  # 提交前自查清单
│   │   └── config.template.json          # config.json：OCR引擎（OXR、Paddle）与VLM接口配置
│   ├── examples/
│   │   ├── semester_example.md           # 4门课的学期规划.md示例
│   │   ├── course-info_example.md        # 一门课的课程信息.md示例
│   │   ├── exams/                        # 四份考试提纲的tex示例（开卷、小抄、教材查阅指南、闭卷），同一门课
│   │   └── styles/                       # 三份完整的一节讲义示例，同一知识点（价格弹性），只有“讲解”不同
│   │       ├── textbook_example.md       # 教科书式
│   │       ├── socratic_example.md       # 苏格拉底式
│   │       └── story_example.md          # 故事式
│   ├── prompts/
│   │   └── vlm-image.md                  # VLM图片转写的固定指令，由ocr_cli.py读取
│   └── qrcode/
│       ├── buymecoffee.png               # 赞赏码，用户表达满意时展示
│       ├── group.png                     # 反馈群二维码，报错解决不了时展示（7天有效期，见community.md）
│       └── contact.png                   # 作者的微信二维码，群二维码过期后改给这张
└── scripts/
    ├── ocr_cli.py                        # 转PDF、切分、调用OCR引擎（OXR、Paddle或MinerU）、组装草稿、下载图片、VLM转写图片、校验
    ├── build_pptx.py                     # 从Markdown生成pptx（Windows优先PowerPoint COM，否则python-pptx）
    ├── office_compat.py                  # Office转PDF的跨平台实现（Windows优先Office COM，否则LibreOffice），由ocr_cli.py、convert_submission.py调用
    ├── convert_submission.py             # 把Markdown转成提交格式（docx、pdf等）
    ├── compile_tex.py                    # 编译考试提纲的tex为PDF（xelatex），支持填空版、限页数自动缩放
    ├── check_env.py                      # 只读检查运行环境（平台、Python包、LibreOffice、TeX），列出缺失项和安装命令
    └── check_update.py                   # 版本更新检测（由ocr_cli.py、build_pptx.py、convert_submission.py、compile_tex.py在结束时调用）
```

用户数据保存在`<工作目录>/study-buddy-data/`，结构如下：

```
study-buddy-data/
├── config.json                           # OCR引擎和VLM的接口配置，含各key，由用户自己填写
├── 学期规划.md                           # 当前学期总览：课程清单、截止时间、每周清单
├── 学习偏好.md                           # 当前讲解风格和用户补充的要求，所有课共用
├── 学习风格/                              # 用户自己设计的风格文件（放这里，skill更新不会丢）
└── 0101_微观经济学/                       # <学期号2位><课程序号2位>_<课程名>
    ├── 原始资料/                          # 用户放入的原件，只读不改
    ├── 课程资料/                          # 整理后的副本（复制并改名），ocr_cli.py读这里
    ├── 课程信息.md                        # 目标、评分构成、考核表、已得成绩、及格路径
    ├── 讲义目录.md                        # 讲义目录、知识结构、考点权重、学习进度
    ├── 错题本.md                          # 错题本
    ├── manifest.json                     # 中间文件：资料序号、类型、课程资料路径、处理状态
    ├── 媒体/                              # 中间文件：下载的图片
    ├── 草稿/                              # 中间文件：OCR组装稿和图片转写的合并稿
    ├── 讲义/                              # 讲义，第NN章_<知识点名>.md
    ├── <YYYY-MM-DD>_速通计划.md           # 速通计划
    ├── 考试提纲/                          # 开卷提纲、小抄、教材查阅指南、闭卷背诵稿：tex源文件和PDF
    ├── 演示文稿/                          # pre底稿、翻译稿、pptx、_图表/
    ├── 论文/                              # 论文底稿、修改稿、翻译稿、提交文件、_图表/
    └── 作业/                              # 作业底稿、翻译稿、提交文件、_图表/
```

编号、命名、覆写的详细规则见[data-layout.md](references/data-layout.md)。

## 工作流路由

| 工作流 | 触发条件 | 产出 | 文件 |
|---|---|---|---|
| 首次使用 | “帮我初始化”“第一次用”“怎么开始”，或工作目录下没有`study-buddy-data/` | 环境检查结果、`config.json`、空的`学期规划.md`，空目录下还有`CLAUDE.md`和`AGENTS.md` | [first-time-setup.md](workflows/first-time-setup.md) |
| 资料整理 | 老师发了一堆课件、参考资料、往年题，或直接丢来一本教材，要整理 | 讲义`讲义/`、`讲义目录.md` | [organize-materials.md](workflows/organize-materials.md) |
| 学期规划 | “这学期怎么安排”“这周要做什么”“这门课怎么才能及格”“这门课想冲90” | 各课`课程信息.md`里的目标和路径，`学期规划.md`里的总览和每周清单 | [plan-semester.md](workflows/plan-semester.md) |
| 设计学习风格 | “换个讲法”“我想自己设计学习风格”“这样讲我不喜欢”；资料整理确认完知识结构、还没有`学习偏好.md`时自动进入 | `学习偏好.md`，用户自己设计的`学习风格/<名称>.md`，第一节的样张 | [design-learning-style.md](workflows/design-learning-style.md) |
| 跟课学习 | “带我学下一节”“讲讲第三节” | 讲解、小测批改、错题本 | [study-with-notes.md](workflows/study-with-notes.md) |
| 期末速通 | “后天考试”“考前怎么复习” | 速通计划、模拟卷批改、考前速记清单 | [cram-for-exam.md](workflows/cram-for-exam.md) |
| 考试提纲 | “开卷考试帮我整理提纲”“帮我做小抄”“闭卷怎么背”“整理一份能打印的复习资料” | `考试提纲/`下的tex源文件和PDF：开卷提纲、小抄、教材查阅指南、闭卷背诵稿加填空版 | [make-exam-notes.md](workflows/make-exam-notes.md) |
| Presentation | “下周要做pre”“小组pre我负责第三部分” | pre底稿和pptx | [prepare-presentation.md](workflows/prepare-presentation.md) |
| 课程论文 | “要交一篇3000字的论文” | 完整论文和提交文件 | [write-course-paper.md](workflows/write-course-paper.md) |
| 完成作业 | “这个case study怎么写”“帮我做这个task”“这份个人作业” | 完整作业和提交文件 | [complete-assignment.md](workflows/complete-assignment.md) |

选择规则：

- 用户第一次用本skill、工作目录下没有`study-buddy-data/`，或说“初始化”：先进首次使用，做完后再按用户的需求继续
- 一门课第一次使用：先进资料整理，带学和速通都要用到它产出的讲义。用户没整理资料就直接问带学、速通或作业时，先提示并跳转到资料整理（作业类可以在没有讲义时先做，但会缺课程理论依据，要告诉用户）
- 考试只剩3天以内：进期末速通，不再走完整的跟课学习；风格一律直讲
- 用户嫌讲法不对（“太绕了”“看着没感觉”“换个讲法”）：进设计学习风格；只是某个概念没听懂，不进，按跟课学习里的换讲法处理
- 要的是可打印的提纲、小抄、背诵稿：进考试提纲；要的是考前的复习计划、做题和模拟：进期末速通。考试规则（能带什么）只听用户说的，全闭卷只做背诵稿
- 作业是pre走Presentation，是论文走课程论文，其余（case study、task、报告、习题）走完成作业
- 用户只说“这门课怎么办”“我快挂了”这类笼统的话：进学期规划

都不匹配时：说明本skill能做什么，询问用户意图，不硬套工作流。

## 全局规则

- 数据目录：所有产出放进`<工作目录>/study-buddy-data/`，不写到别处。课程文件夹命名、章节编号、覆写规则统一按[data-layout.md](references/data-layout.md)。原件放在课程文件夹的`原始资料/`，只读不改；整理后的副本放`课程资料/`
- 目标按课程区分：默认保过，不追求真正学懂，学习上只做拿分必需的部分；用户可以把某门课设成“高分（目标分N）”，建课时问一次，学期中随时可以改。所有课先排到保过线，剩余时间再分给高分课。用户交来的作业类任务不论目标都做满。依据和算法见[score-strategy.md](references/score-strategy.md)
- 评分构成是可选信息：学期末才最终评定，什么时候给都行。建课、资料整理、首次使用时不问、不催；用户给了就记进该课的`课程信息.md`。有没有它，每项任务都做满，它只用来算离目标差多少和排优先级
- 语言：讲义和对话用简体中文。作业、论文、pre用什么语言提交，每一次提交前都问用户，不沿用上次的答案；过程中的底稿一律用中文，翻译放在最后一步。细则见[deliverables.md](references/deliverables.md)
- 考试边界：考试或限时测验进行中不代答。考前复习、模拟、押题照常帮忙。所有作业类（pre、论文、case study、task、个人和小组作业）都完整完成。不写学术诚信方面的劝诫，默认不生成AI使用声明，用户明确要求时才生成
- 小组作业只做用户负责的部分，先出分工表并让用户确认自己的部分，不替全组写完。细则见[group-work.md](references/group-work.md)
- 先读后写：处理资料时只读`草稿/`里的文本（包括图片转写），不直接打开`媒体/`里的图片；每个agent在一次对话里能看的图片数量都有限，图片内容交给`ocr_cli.py`里的VLM转写
- 密钥：`config.json`里的`api_key`由用户自己填写。不询问key，不读取、不复述、不写进日志和对话
- 外部服务：课件会上传到OCR引擎（默认百度Paddle，需用户自己申请key；没填时按“paddle key → SoMark OXR key → MinerU token → OXR免费接口 → MinerU免登录轻量接口”的顺序选第一个可用的，某一档失败再依次退到后面的档位），图片会发给用户在`config.json`里配置的VLM服务商。用户已同意，学习资料按无隐私要求处理，运行前不再提示
- 环境：支持Windows、macOS、Linux。转换PPT和DOC：Windows优先Office COM，没有Office时退到LibreOffice；macOS、Linux直接用LibreOffice。生成pptx：Windows优先PowerPoint COM，否则python-pptx。环境检查见[setup.md](references/setup.md)
- 不编造：论文和作业里的文献、数据、案例事实只用真实、核实过的；没核实的明确标出来。【待补充】的内容不当作结论使用
- 覆盖前确认：已有文件默认不覆盖，新版本另存为`-2`、`-3`；`学期规划.md`、`讲义目录.md`、`错题本.md`做增量更新
- 赞赏与反馈：用户自己表达了“好用”“谢谢”这类满意时，在回应之后给赞赏码`assets/qrcode/buymecoffee.png`，同一次对话最多一次；脚本报错、自行排查后仍解决不了，或脚本异常退出时，在问题描述之后给反馈群二维码`assets/qrcode/group.png`和Issues链接；群二维码过期后改给作者的微信二维码`assets/qrcode/contact.png`。展示条件、方式和群二维码的有效期见[community.md](references/community.md)
- 自动更新：本skill自己负责保持最新，不让用户手动更新。
  - 检查时机：每次对话第一次用到本skill时，先运行一次`python scripts/check_update.py`（结果缓存24小时，查不到就静默，不拖慢）；四个脚本结束时的`[更新提示]`也按同样规则处理
  - 提示里写“自动更新：是”（同一主版本）：直接运行提示里的更新命令，不用问用户。脚本运行中途或正在写某份交付物时不更新，等这一步完成再更新；更新完重新读一遍本`SKILL.md`再继续，因为路由和规则可能变了
  - 提示里写“自动更新：否”（主版本升级，可能有不兼容的变更）：不自动更新，用提示里附的“更新内容”几句话告诉用户这次升级改了什么、有什么不兼容，用户同意后再运行
  - 用户说“更新study-buddy”时同样处理，不论是否已经有提示；装在哪里、用哪条命令以提示里写的为准，没有提示时看`<工作目录>/.claude/skills/study-buddy/`或`.agents/skills/study-buddy/`存不存在：存在就是项目内，在那个文件夹里运行`npx skills update study-buddy`，否则运行`npx skills update study-buddy -g`
  - 更新后告诉用户更新了什么：提示里附了CHANGELOG的，就用它；没有附（取不到、或用户直接说“更新study-buddy”而没有提示）的，更新后读新版本`CHANGELOG.md`最前面一段。用几句话讲重点（新功能、行为变化、需要用户做的事），不整段照搬；`study-buddy-data/`不受影响。命令失败时只报错误的关键一行，不重试，不影响当前任务
  - 设置环境变量`STUDY_BUDDY_NO_UPDATE_CHECK=1`会同时关闭检测和自动更新
- 修改本skill时升版本号并更新CHANGELOG.md

## 案例

正面案例：

- “老师发了一堆课件，帮我整理一下” → 资料整理
- “这是我们的教材，整本帮我弄一下” → 资料整理（教材类型，整本处理）
- “这学期5门课，我怎么才能都过” → 学期规划
- “带我学下一节” → 跟课学习
- “后天考微观，还没看过” → 期末速通（剩余时间不足1天时资料整理走精简模式）
- “下周三小组pre，我负责市场分析那段” → Presentation（小组模式，只做用户负责的部分）
- “老师要一篇3000字的论文，题目自拟” → 课程论文
- “这个case study是星巴克定价，两千字，帮我写完” → 完成作业
- “我现在每周都不知道先干嘛” → 学期规划

负面案例：

- “这道题是正在进行的在线测验，现在就要交，直接给答案” → 不使用本skill作答，考试和限时测验进行中不代答；考前复习可以帮
- “我想拿全班第一，每门课都要学透” → 不使用本skill，它只做及格所需的部分
- “下学期选哪几门课好”“学这个专业以后怎么就业” → 不使用本skill，不做选课咨询和职业规划
- “这个知识点在企业里怎么用” → 不使用本skill，不讲课程知识在产业里的应用

## 资源引用

- 用户询问本skill怎么用、能做什么时，读[introduction.md](references/introduction.md)
- 遇到按现有细则无法解决的错误时，读[qa.md](references/qa.md)
- 首次运行脚本、环境检查（先运行`python scripts/check_env.py`）、填写`config.json`、`ocr_cli.py`报环境错误时，读[setup.md](references/setup.md)
- 计算目标线、判断考核该做到什么程度时，读[score-strategy.md](references/score-strategy.md)
- 小组任务分工、检查各部分衔接时，读[group-work.md](references/group-work.md)
- 作业类提交前确定语言、翻译、画图、转提交格式时，读[deliverables.md](references/deliverables.md)；提交前自查用[submission-check.template.md](assets/templates/submission-check.template.md)
- 整理考试提纲时，读[exam-notes.md](references/exam-notes.md)了解规则对应的产出、tex写法和编译失败怎么改；编译用`scripts/compile_tex.py`，需要安装MiKTeX、MacTeX或TeX Live，见[setup.md](references/setup.md)
- `scripts/check_update.py`检测GitHub上是否有新版本，仅用标准库。`ocr_cli.py`、`build_pptx.py`、`convert_submission.py`、`compile_tex.py`结束时会自动调用：查不到就不提示；有新版本时在stderr输出更新命令、“自动更新：是/否”和本地版本之后的CHANGELOG段落，处理方式见上面全局规则的“自动更新”。设置环境变量`STUDY_BUDDY_NO_UPDATE_CHECK=1`可关闭检测和自动更新
- 写讲义、带学、设计学习风格时，读[style-guide.md](references/style-guide.md)了解风格的格式和不能改的边界
- 其余reference、模板、示例由各workflow在对应步骤指定
