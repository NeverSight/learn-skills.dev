---
name: maafw-debug
description: 调试与验收 MaaFramework（MaaFW）应用（开发态、设备在线）——节点识别失败、点击不落点（识别成功 ≠ 点击生效）、ROI 校准与阈值调参、单节点运行验证、流程卡死与 controller 连接排查、端到端验收与 pipeline_override 生效验证；按配置/识别/动作/流程/验收五层分诊，产出定位结论与证据，修复交接回 maafw-pipeline / maafw-interface / maafw-custom。Use when debugging or acceptance-testing a MaaFW application with a device attached — node recognition failures, clicks that miss, ROI calibration and threshold tuning, single-node run verification, stuck flows and controller connection issues, end-to-end acceptance, or pipeline_override effect checks; triage by layer (config / recognition / action / flow / acceptance), then hand the fix back to maafw-pipeline / maafw-interface / maafw-custom.
---

# MaaFW 调试与验收

> 标注 TODO 的节为**实践待补的经验样本**（增量内容，不影响可用性）；分诊状态见 skills/README.md。

定位：**开发态、设备在线的实时调试与验收**（验收环节的冷启动 / 重连 / 断线恢复由开发者主动制造离线与重连窗口，属验收手段而非离开开发态）。字段精确语义（字段名、参数、默认值、版本支持）与调试命令一律路由 [MaaLLMWiki](https://github.com/Windsland52/MaaLLMWiki) 版本锁定的协议原文（2.4-控制方式说明、3.1-任务流水线协议、3.3-ProjectInterfaceV2）；**运行工具的命令与结果字段**路由所选运行工具自身文档（Agent 自主默认 maafw-live，见 [references/tooling.md](references/tooling.md)）——协议原文不含工具命令。两类来源不可达时标记"未验证"。事后日志与证据诊断（用户日志、Sentry、历史记录）归 [MaaEvidenceKit](https://github.com/Windsland52/MaaEvidenceKit) 的 `maa-evidence`，不是本 skill。

## 硬护栏

1. **证据优先**：每个诊断结论必须有实时观测证据——当前帧、识别命中/未命中与得分、日志、box 与落点比对；「可能是」必须转成可验证假设再测，不许凭猜下结论（与 maafw-pipeline 的探索优先同源）。
2. **一次一个变量**：阈值 / ROI / 模板 / 参数每次只改一个，改完立即复测并留记录；多处同时改后结果变化无法归因——调试态第一纪律。
3. **走框架链路**：诊断用截图与点击必须走框架截图链路（观测底座 / 框架截图 API / 运行工具），不用外部截图工具——分辨率与图像空间必须与识别输入一致（像素空间一致原则继承 maafw-pipeline 素材标准）。
4. **只定位不修复**：本 skill 产出「定位结论 + 证据」。边界：**为验证假设可临时改并立即复测**（硬护栏 2「一次一个变量」正是此用法），但交付物仍是结论 + 证据，**修复落盘走交接**（识别/流程 → maafw-pipeline，接线/选项 → maafw-interface，custom → maafw-custom；修改轨已含 ROI 微调这类小修）——不边定位边做结构性改动。
5. **判定分级**：区分**调用成功**（命令是否执行完）、**任务成功**（任务级结果 + 实际识别命中）、**业务验收成功**（功能行为符合预期）——三层互不顶替，调用层信号（外层 ok / 退出码）不能当任务或验收结论；具体判定字段与退出码语义随工具（maafw-live 见 tooling.md 判定要点）。一次跑通 ≠ 稳定——验收要重复、含冷启动与重连。
6. **调试现场及时留存**：调试过程中的关键帧及时升格进关键帧库（观测底座留存），现场过了就过了；脱机的事后分析转 `maa-evidence`。

## 工作流

### 0. 分诊（先分层再动手）

按症状定位到五层之一再进对应层流程；跨层症状按最外层先排查：

| 症状 | 层 |
| :--- | :--- |
| 设备连不上 / 任务起不来 / 启动即失败 / 选项没生效 | 配置层 |
| 某节点不命中 / 命中错 | 识别层 |
| 识别命中但点击没落地 / 滑动没动 / 落点偏移 | 动作层 |
| 卡死 / 死循环 / 走到不该走的节点 / 提前终止 | 流程层 |
| 跑通了但功能行为不对 / 交付前检查 | 验收层 |

排障树（症状 → 检查项 → 常见根因）见 [references/diagnosis-tree.md](references/diagnosis-tree.md)；各层检查的取证手段与工具见 [references/tooling.md](references/tooling.md)——硬要求不随工具变，工具可替换。

进层之前先定**执行工具**（tooling.md「工作模式」）：Agent 自主默认 maafw-live，动手前 `version` / `env` / `probe` 自检；未安装或不可用时按「工具替换判定」选定替代、并在定位结论里明说缺哪项能力——工具选择先于任何层内动作。

### 1. 配置层（设备与启动链路）

先静态后动态：有 dev-tools 的项目先 `pnpm check` 清结构错误，再谈运行时行为。「选项没生效」先查 option 适用性过滤（头号原因，经验值；机制见 maafw-interface），再查接线。设备连通、任务入口、子进程双日志等检查项、协议字段核对与常见根因见排障树配置层细节。

### 2. 识别层（单节点验证）

单节点验证 + 截图 + hits/box 期望——命令查所选工具文档（默认 maafw-live：`reco` 识别单测、`--act` 真机执行动作半；`run` 从 entry 起跑会继续走 next / on_error、不是单节点验证——隔离与副作用边界见 tooling.md 默认执行路径），节点字段语义查 3.1 协议。第一问永远是**目标在不在帧里**，再谈 ROI / 阈值 / 模板；一次一个变量（硬护栏 2）。判据、经验值与识别类型适配见排障树识别层细节。

### 3. 动作层（识别成功 ≠ 点击生效）

第一问永远是「点到哪了」：识别 box vs 实际落点逐像素比对，再谈 target / offset。target 语义、inverse 陷阱、两坑治法与重试门控见排障树动作层细节。

### 4. 流程层（卡死归因）

用执行模型归因（执行模型全文见 maafw-pipeline SKILL.md，这是归因的唯一地图）。最常见归因错误：想调某节点被识别的等待时长，改的是它**上一节点**的 `timeout` / `on_error`。死循环三查、提前终止与改名失联面清单见排障树流程层细节。

### 5. 验收层（端到端）

完备性四问（尤其「不在目标场景时的行为已显式定义」）+ 判定分级（硬护栏 5）+ 重复跑（含冷启动 / 重连 / 断线恢复）；验收分两档——Pipeline 业务流程验收（运行工具可承担，结论须记录前置条件与 Agent 状态）与目标 Client 集成验收（实际经 Client 的 pretask、装配、Agent 启动与任务入口，工具跑通不能替代——边界见 tooling.md）。override 生效验证与测试沉淀见排障树验收层细节。

### 6. 交接

定位结论必须包含：**症状 → 层 → 根因假设 → 证据（帧/日志/得分/比对）→ 建议修复方向 → 交接目标 skill**。修复转 maafw-pipeline / maafw-interface / maafw-custom；离线证据分析转 maa-evidence。

## 深入阅读（按需）

- [references/diagnosis-tree.md](references/diagnosis-tree.md) — 排障树：症状 → 检查项 → 常见根因（配置层细节、静默失联面清单、阈值与 ROI 经验值）
- [references/tooling.md](references/tooling.md) — 取证手段与工具矩阵：工作模式、maafw-live 默认执行路径与判定要点、替代工具能力对应、各层检查要点与工具替换判定

## TODO（实践待补——经验样本类增量，唯一清单）

- 排障树各分支的日志判读细则（日志片段 → 结论的判读样本）
- 识别慢（性能）排查分支；ColorMatch / And / Or / 自训模型节点的调试要点
- 各层最小复现标准流程与取证快照清单（含流程层「最小取证序列」模板）
- 验收记录模板（验证对象、范围、实际结果、证据、实现指纹——对齐 state-plan 的 tested 语义，待其 schema 冻结）

> 排障树 / 工具文档中的内联 TODO 仅为位置标记，以本节为唯一清单与完成判据。
