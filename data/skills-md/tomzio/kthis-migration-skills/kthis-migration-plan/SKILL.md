---
name: kthis-migration-plan
description: 为遗留系统功能生成新一代系统（WebHIS：React + antd 前端 / Spring Boot + MyBatis 后端）的迁移设计文档。当用户要求「写 / 生成 / 补充 / 整理 / 修订 迁移文档、迁移设计文档、功能迁移计划、实施计划、界面（UI）设计文档、详细设计、分册文档、开发前设计」，或提到迁移文档目录 docs/migration、按界面 / 页签拆分文档、把遗留功能整理成设计文档、参照既有迁移文档的写法、生成迁移计划 / 阶段门禁 / 手测清单，或要对已有迁移文档做多轮修改优化时，都应使用本 skill —— 即使用户没有明说「生成文档」二字。
---

# 迁移文档生成（kthis-migration-plan）

把遗留系统（Eclipse RCP + SWT，Java 6 / GBK）的某个功能，整理为目标系统**可直接照着实现的迁移设计文档**，输出到迁移文档根目录（默认 `docs/migration/`，可用脚本 `--root` / `--docs-dir` 覆盖）。

产物形态：**按界面聚合、弹窗的每个页签单独一册、共享内容单独一册**，配合模板与脚本搭建骨架，再**逐册多轮与被指派人对话确认、迭代修订**。

> 本技能只规定「**通用形态与流程**」：目录结构、册划分原则、模板、脚本、多轮对话协议。**具体模块名、编号、遗留入口、截图、源码路径一律由使用者在每轮对话中提供，不写死在技能里。**
>
> **用法**：本文件只给「何时用 + 协作流程 + 脚本命令」；目录结构、册划分、写作口径等细节都在 `references/*`，**按需读取**，不要一次全读。

## 何时使用 / 不使用

- **用**：「把 XX 功能写成迁移文档 / 设计文档 / 详细设计」「参照已有迁移文档的格式整理 XX」；「补充 / 修订迁移文档里的某册」「新增一个页签册」「把 XX 弹窗拆成册」；「生成迁移计划 / 实施计划 / 阶段门禁 / 手测清单」「整理界面截图并按功能命名」；任何「开发前先出设计文档」的诉求。
- **不用**：直接写代码（本技能只产文档；动代码用 `kthis-migration` 技能）；后端接口文档（本技能只引用后端接口清单作为权威，不在此生成）。

## 与其他技能的关系（迁移分两段）

迁移按「**先设计文档，后编码实现**」两段推进；本技能负责**第一段：设计文档**，第二段（编码实现）用 `kthis-migration` 技能。

- **分工口径**：说「写 / 生成 / 整理迁移文档、详细设计、分册、实施计划」→ 用本技能；说「实现 / 迁移 / 还原这个功能、写页面 / 弹窗 / 接口」→ 用 `kthis-migration`。
- 本技能产出的文档是实现的**唯一依据**：文档定稿后再交给实现；实现中发现与遗留源码不符，回本技能修订对应册。
- 本技能只做文档，**不读改业务代码**（读遗留源码取业务事实除外）。

> 本技能只描述「要重实现成什么样」；**代码层面一切以 `webhis-front` 技能 + 仓库 `.agents/rules/*` 为准**（本技能与编码技能都只是**可选**加速器）。

## 三条硬约束

1. **一切以遗留源码为准**。截图只作视觉基准、可能不完整；文档之间冲突时以源码为准。发现不一致 → 先修订文档。
2. **遗留 GBK / 文档 UTF-8**：**不要直接复制字节**，中文需转码或重录（遗留中文可用 `iconv -f GB18030`）。
3. **单一维护**：共用页签 / 共享分区只在**一册**维护，其它册只引用（复用矩阵册）；本册索引 / 册名 / 链接一处定义、他处引用。

## 路径与仓库

本机三仓库（遗留 / 前端 / 后端）的绝对路径见**项目根** `.agents/paths.env`（每个开发者不同；缺失时运行 `kthis-migration` 技能的 `scripts/setup-paths.sh`，或直接询问用户）；技能内不写死任何绝对路径。

## 产物形态

```text
<迁移文档根目录>/            # 默认 docs/migration/
├── README.md                # 全局索引（多模块按模块分节）
├── 00-前端布局规范.md        # 跨模块只一份（可选）
├── images/                  # 共享截图，命名 <功能序号>-<模块代号>-<界面英文名>.png
└── <NN>-<模块名>/            # 每个功能模块一个目录
    ├── _进度台账.md          # 多轮协作台账（非正式册，不进索引）
    └── 00-总览与通用约定.md → 01-主页面.md → 02-<X>编辑弹窗外壳.md → 03..N-<X>页签.md → 独立/辅助弹窗、数据流程与接口、迁移实施计划、共享分区与复用矩阵（按需）
```

每册固定：H1 `# <册号> · <册名>` → 导航行 `> 返回索引：[README](../README.md) ｜ 上一册：[..](..) ｜ 下一册：[..](..)` → 范围说明 blockquote → 正文章节。**册集按档位裁剪**（轻量 / 标准 / 完整）：`overview`/`main`/`shell`/`tab` 是核心，`dialog`/`aux`/`data`/`plan`/`matrix` 按需，**没有内容就不建**（`matrix` 仅当确有跨界面共用内容；`aux` 仅当有辅助弹窗 / 码表；简单功能 `00 + 01` 两册即可）。目录 / 册划分 / 命名 / 索引 / 导航 / 截图约定 → **[references/doc-structure.md](references/doc-structure.md)**（档位判定见其 §2.1）。

## 写文档前先读（UI 相关）

分册里的**骨架 / 栅格 / 分区顺序 / 控件选型 / 按钮**都要和实现规则对得上 —— 否则实现阶段只能二选一（照文档写违背规范，或照规范写偏离文档）。动笔前先读这三份：

1. **仓库 `.agents/rules/*`**（页面 / 样式 / 组件 / 表格）与 `docs/FrontNormalize.md` —— 文档里写的做法**不得与它们冲突**。
2. **迁移文档的 `00-前端布局规范.md`**（已存在就读；没有则用本技能 `templates/00-前端布局规范.md.tpl` 先落一版）—— 骨架 / 栅格 / 分区 / 尺寸的**数值口径以它为准**；各分册**只引用、不复述**。
3. 本技能 `references/writing-rules.md` —— 线框 / 字段表 / 事件表怎么写、栅格密度怎么表述。

## 多轮协作流程（核心）

> 迁移文档是**反复迭代**出来的，不是一次写完。**任何一轮都不许把「我猜的」当「确认的」**；未确认处留 `<!-- TODO -->` 并在台账登记。

| 轮次 | 做什么 | 产出 / 确认点 |
| --- | --- | --- |
| R0 · 定界 | 确认模块（新侧代号）、范围、遗留入口、界面单元数量，并**定档位**（轻量 / 标准 / 完整，见 doc-structure §2.1） | 范围、遗留入口与档位（问用户） |
| R1 · 册规划 | 按档位盘点界面单元 → 排出「册规划表」（**宁少勿多**，没有对应内容的册不建） | **先给册规划表，等用户确认**再动手 |
| R2 · 搭骨架 | 用脚本生成骨架，写 `_进度台账.md` | 目录 + 空册 + 台账 |
| R3+ · 逐册起草 / 修订 | **一次一册**：读遗留源码 → 按模板填 → 交付 → 收批注后修订（必要时用 `new-volume.sh` 插入 / 重排册） | 每册后**请用户批注**；更新台账「修订记录」 |
| Rn · 横向册 | 数据流程与接口 / 复用矩阵 / 实施计划 | 交叉校对前后册 |
| Rn · 索引与截图 | README 索引、截图表与命名 | 链接可达 |
| Rn · 收口 | 跑审计脚本，清零错误 | `audit-docs.sh` 通过 |

**提问纪律**：每轮只问**真正阻塞**的问题（≤3 个），能自己从源码查证的不要问；把「已定 / 待定」在台账里显式区分。用户在任一轮给出的新约束，要回填到受影响的所有册。逐册提问模板、确认话术、台账格式 → 读 **[references/dialogue-workflow.md](references/dialogue-workflow.md)**。

## 册类型与模板

类型与模板一一对应（都在 `templates/`）：`overview` 总览与通用约定（自动置于首册）、`main` 主列表页 / WPB 页、`shell` 编辑弹窗外壳（页签挂载点）、`tab` 某个页签（共用页签只写一册）、`dialog` 独立弹窗、`aux` 辅助弹窗 + 码表总表、`data` 数据流程与接口、`plan` 迁移实施计划 / 阶段门禁、`matrix` 共享分区与复用矩阵。

对应模板（按上述类型顺序）：`00-总览与通用约定.md.tpl`、`01-主页面.md.tpl`、`02-编辑弹窗外壳.md.tpl`、`03-页签.md.tpl`、`04-独立弹窗.md.tpl`、`05-辅助弹窗与码表.md.tpl`、`06-数据流程与接口.md.tpl`、`07-迁移实施计划.md.tpl`、`08-共享分区与复用矩阵.md.tpl`。

写作口径（以「功能行为」而非遗留实现为准：字段表 / 线框 / 事件表写法）→ **[references/writing-rules.md](references/writing-rules.md)**。

## 脚本

```sh
S=<本技能目录>/scripts          # 即 .agents/skills/kthis-migration-plan/scripts

# 1) 搭建模块骨架（册序 = --volume 顺序；--no/--name/--code/--volume 由 R1 结论填入）
$S/scaffold-docs.sh --no <NN> --name <模块名> --code <模块代号> [--legacy-ui <遗留入口>] \
  --volume "<主页面>:main" --volume "<弹窗外壳>:shell" --volume "<页签>:tab" …
#   轻量档（简单功能）加 --lite：只生成 00-总览与通用约定.md + 01-功能说明.md，后续用 new-volume.sh 增册；
#   首次可加 --global-layout 生成跨模块的 00-前端布局规范.md

# 2) 迭代中插入一册（自动重排册号 + 重写导航与引用）
$S/new-volume.sh --module-dir <迁移文档根目录>/<NN>-<模块名> --title "<册名>" --type tab --at 3

# 3) 体检（册号连续性 / 导航链 / 索引 / 链接 / 截图命名 / 占位符 / 跨册重复 / 篇幅预算）
$S/audit-docs.sh                                         # 全量（跨册重复仅提示）；可加 --module <NN>-<模块名>
$S/audit-docs.sh --strict --dup-strict --max-lines 450    # 收口前严格一遍

# 4) 截图整理（截图丢进 images/ 后：识别 → 按功能改名 → 同步引用）
$S/rename-screenshots.sh --audit <迁移文档根目录>/images <迁移文档根目录>           # 审计：不合规命名 / 失效引用 / 未引用
$S/rename-screenshots.sh <迁移文档根目录>/images <迁移文档根目录> "<旧名>=<新名>" …  # 机械改名 + 改全部文档引用（加 --dry-run 只打印）
```

> 脚本只做机械搭建与校验；**内容由你必须逐册从遗留源码核实后填写**。截图改名只做机械部分，**「看图识别是哪个页面 / 页签 / 弹窗」由模型完成**，流程见 [references/screenshots.md](references/screenshots.md)。

## 遗留侧盘点（写文档前）

定位 Editor/Page → 枚举 `CTabItem`/分区/弹窗 → 事件与 `I*Service` → server impl → iBATIS map → 表；界面文案在遗留工程的 `i18n/messages.properties`（GBK）。方法与命令（含 GBK 检索）→ 读 **[references/legacy-recon.md](references/legacy-recon.md)**。

## 验收

收口前逐项过 **[references/quality-gates.md](references/quality-gates.md)**，并确保 `audit-docs.sh` 零错误、零占位符残留（`--strict` 通过）。

## 参考文件

- [references/doc-structure.md](references/doc-structure.md) —— 目录结构、册划分原则与档位、命名、索引、导航、截图约定
- [references/writing-rules.md](references/writing-rules.md) —— 写作口径（功能行为 / 字段表 / 线框 / 事件 / 反例）
- [references/dialogue-workflow.md](references/dialogue-workflow.md) —— 多轮对话协议、提问模板、进度台账、冲突处理
- [references/legacy-recon.md](references/legacy-recon.md) —— 遗留侧端到端盘点与 GBK 检索
- [references/quality-gates.md](references/quality-gates.md) —— 验收门禁清单（自动 + 人工）
- [references/screenshots.md](references/screenshots.md) —— 截图识别、按功能命名与引用更新（命名规范在此）；批量改名脚本 [scripts/rename-screenshots.sh](scripts/rename-screenshots.sh)（`--audit` 审计命名 / 失效引用 / 未引用）

> **跨工具（OpenCode / Claude Code / Trae IDE）**：本技能是**项目级技能**，唯一原始目录 `.agents/skills/kthis-migration-plan/`，其它工具目录均为指向它的软链接（勿另存副本）；接入方式与 Windows 软链接注意事项见仓库 `.agents/README.md`。
