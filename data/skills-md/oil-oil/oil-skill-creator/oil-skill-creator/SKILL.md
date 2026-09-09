---
name: oil-skill-creator
description: 创建、评审、整改和发布 Skill。用户想从零创建 Skill、评审现有 Skill、检查它是否真正有用、修复触发或执行流程，或者改善首次使用、稳定性、Token 开销、文件分层、弱模型可读性与跨平台兼容性时使用。不要用于执行目标 Skill 负责的实际任务，也不要因为普通的编码、设计或写作请求触发。
license: MIT
compatibility: 核心脚本只使用 Python 3 标准库；可选凭据输入页需要 Node.js 22.18+ 和系统凭据服务，已验证 macOS，Windows 与 Linux 待实机验证；独立效果评估需要隔离执行能力。
---

# oil-skill-creator

把 Skill 当作需要长期维护的工具。先确认它解决了重复问题，再让它容易开始、稳定执行、能够验证，并如实说明兼容范围。不要把一次任务的提示词包装成 Skill。

## 先选择模式

| 模式 | 适用情况 | 路径 | 默认停止点 |
| --- | --- | --- | --- |
| 创建 | 还没有 Skill | 产品定义 → 实现 → 校验 → 评估 → 按需发布 | 交付可用 Skill |
| 整改 | 已有 Skill，用户要求修复或优化 | 读取 → 静态检查 → 按需固定基线 → 局部修改 → 复验 | 问题修复且无回归 |
| Review | 用户只要求评审、审计或找问题 | 读取 → 静态检查 → 流程检查 → 报告 | 报告交付后停止 |

Review 默认只读，不创建快照、不修改、不打包。整改禁止用脚手架重建已有目录。用户后续授权整改时，从整改路径重新开始；快照是效果对照需要的固定基线，不是普通编辑的前置步骤。

## 开始前

已有 Skill 时，先完整读取 `SKILL.md`，再按导航只读取当前模式和问题需要的资源。检查相关目录、脚本、测试、评估用例、README 和平台假设；不要重复询问已有信息。

“静默”表示不需要用户选择时直接完成检查，不表示隐藏过程。完成后简要报告检查结果。

只有目标或交付物不清楚、需要新增权限或服务、可能覆盖内容，或者主观方向会改变结果时才询问。将相关问题一次问完。

按以下方式分工：

- Agent 判断价值、边界、架构、例外和主观质量。
- 程序执行确定、重复、可验证、失败敏感的步骤。
- 子 Agent 隔离触发和执行；人类判断审美、文案和整体体验。

默认创建不依赖特定宿主的 Skill。正式指令、参考资料、README、目录名和示例使用“Agent、宿主、能力、隔离执行者”等通用名称，不写当前宿主的品牌、专属目录、专属命令或私有 API。

如果核心能力确实依赖某个宿主，将专用适配器与通用流程分开，并在产品定义和兼容性中说明限制与替代方案。此时不能宣称 Skill 支持所有宿主。

下文的 `<python>` 表示已经找到并确认版本不低于 3.10 的 Python 解释器。程序内调用使用 `sys.executable`；macOS 和 Linux 命令行通常使用 `python3`，Windows 通常使用 `py -3`。不要假设 `python` 命令一定存在。

## 创建路径

先读 [产品设计](references/product-design.md)，确认问题值得做，并明确用户、当前做法、预期改善、输入、输出、边界、风险和任务类型。

如果只是一次性需求、普通 Agent 已能稳定完成，或者无法说明使用 Skill 后会改善什么，就不要强行创建。

需要目录时先预览最小骨架：

```text
<python> <oil-skill-creator>/scripts/scaffold_skill.py <skill-name> --output-root <目录> --description <描述> --public --dry-run
<python> <oil-skill-creator>/scripts/scaffold_skill.py <skill-name> --output-root <目录> --description <描述> --public
```

只通过 `--components` 添加当前确实需要的目录，例如 `--components scripts,tests`。不要为了示例完整而创建空资源。

## Review 与整改路径

先读 [Review 与整改规范](references/review-and-remediation.md)。Review 同时检查静态缺陷和程序无法判断的产品问题，不把“校验器通过”等同于“Skill 有用”。

只有需要把旧版交给隔离执行者做前后效果对照、用户明确要求保留独立基线，或现有版本无法由 Git 等可靠来源复现时，才在第一次编辑前保存不可变快照：

```text
<python> <oil-skill-creator>/scripts/snapshot_skill.py <skill-path>
```

小范围、目标明确、可由 Git 恢复且不需要运行旧版对照的整改，直接局部修改并复验，不创建快照。需要快照时，它默认进入外部 workspace；目标位于名为 `skills` 的扫描目录时，workspace 放到该目录同级的 `skill-workspaces/`，避免快照被识别成重复 Skill。脚本拒绝覆盖已有快照；后续效果基线只能指向该快照，不能指向正在编辑的目录。

按 P0、P1、P2 报告证据、影响、成因、通用修复方法和验证方式。忽略不影响行为的措辞偏好，不把合理取舍当成缺陷。

整改时优先修复导致问题的规则、程序接口或验证流程，再修复当前表现。保留名称、有效结构和用户已有内容；没有必要时不整份重写。

## 设计和编写

### 触发

目标 Skill 的所有触发信息只放在它的 frontmatter `description` 中。写清目标 Skill 做什么、什么时候使用、哪些相似请求不该触发，以及与其他 Skill 如何分工。不要在目标 Skill 的正文重复一套触发规则。

准备真实的正向请求和容易混淆的反向请求。需要测量触发准确性时，按 [评估规范](references/evaluation.md) 的触发评估执行；静态关键词检查不能证明触发可靠。

### 首次使用和恢复

按 [产品设计](references/product-design.md) 的决策表处理首次使用、配置、需要用户确认的操作和失败恢复。能够自动发现、风险低并且可以撤销的准备工作静默完成。

登录、密钥、系统安装、覆盖、删除和外部写入必须先获得授权。

目标 Skill 需要持久化配置或凭据时，按 [兼容性](references/compatibility.md) 分开设计普通配置、凭据引用和密钥存储。不要把密钥值写进 JSON、Skill 文件、日志或 Agent 上下文。

目标 Skill 在本机桌面环境需要用户输入 API Key 等单行凭据、且没有现成安全入口时，读 [可复用凭据输入页](references/credential-ui.md)，用安装脚本接入固定组件。单 Key 与同页多 Key 共用模板，每项独立声明，页面配置控制组合顺序与文案；不要为每个 Skill 重新生成页面。说明 macOS 钥匙串、Windows 凭据管理器与 Linux Secret Service 的前提及安全边界；普通设置、OAuth、CI 和远程服务器不直接套用输入页。保存端、部分失败恢复与业务读取端一起验证。

重复运行初始化或迁移流程时，不能破坏已有配置，也不能产生重复结果。失败时保留仍然可用的中间产物，并说明失败位置、恢复方法和还没有执行的必做步骤。

### 信息架构

拆分文件前读 [信息架构](references/information-architecture.md)。主流程放在 `SKILL.md`，阶段细节放在 `references/`，结果固定的步骤放在 `scripts/`，运行结果和 Review 记录放在 Skill 外部。

如果目标 Skill 会生成难以一次稳定完成或局部修改的大型产物，或者需要复杂配置、反复预览和人工调整，按 [产品设计](references/product-design.md) 设计分段产出、程序组装或可复用操作页面。

一步只表达一个主要动作，分支紧邻对应步骤，术语保持一致。不写具体任务、个人目录、单次候选、Review 记录、修改记录或版本历史；只写能够用于同类任务的规则、程序和回归测试。

Skill 描述目标、判断原则、主流程、必要分支与停止条件，不穷举具体情境组成规则树。有限、稳定、可验证的分支交给程序；依赖语义和上下文的选择留给 Agent 判断。

Skill 不得包含与 description 不一致的隐藏行为、误导能力、越权访问或数据外传。兼容性只能声明实际实现或真实验证过的范围。

## 程序校验

开发过程中运行：

```text
<python> <oil-skill-creator>/scripts/validate_skill.py <skill-path>
```

公开发布或整改完成前运行：

```text
<python> <oil-skill-creator>/scripts/validate_skill.py <skill-path> --public --strict --weak-model --universal
```

校验器只处理能够由程序确认的问题。校验通过后，仍要检查流程含义和真实效果。只有产品明确依赖某个宿主时才省略 `--universal`，并在兼容性中说明原因。

`--weak-model` 使用更严格的结构限制；`--universal` 检查通用 Skill 是否写死了宿主品牌或专属路径。

## 效果评估

当用户要求证明效果、整改涉及难以从静态检查确认的重大行为变化，或准备正式发布并需要效果证据时，先读 [评估规范](references/evaluation.md)。创建模式与普通 Agent 比较；整改模式在需要前后对照时与写入前的 `skill-snapshot` 比较。明确的小范围规则修正可以用静态校验和针对性回归完成，不强制建立效果对照。

稳定流程由程序准备：

```text
<python> <oil-skill-creator>/scripts/prepare_evaluation.py <skill-path> --mode create --iteration 1
<python> <oil-skill-creator>/scripts/prepare_evaluation.py <skill-path> --mode improve --iteration 1
```

程序会检查 `evals/evals.json`，创建固定的 `with_skill`、`without_skill` 或 `old_skill` 目录，并生成 `run_plan.json`。Agent 按计划运行当前版本和基线，不自行增加目录或字段。

运行完成后，程序聚合数据并生成静态评审页：

```text
<python> <oil-skill-creator>/scripts/aggregate_evaluation.py <iteration-path>
<python> <oil-skill-creator>/scripts/generate_review.py <iteration-path>
```

先把候选结果、证据和对比报告交给用户；收到反馈前不要继续修改 Skill。主观结果必须由人判断，AI 只能检查明确要求或整理差异。

没有隔离执行能力时，要说明评估能力受限，不能宣称已经完成独立对照。

效果不好时先按 [评估规范](references/evaluation.md) 查明原因，不直接追加规则。只有 Skill 的流程、判断原则或接口确实导致失败时，才修改适用于同类任务的规则，并用原失败类型复验。

## 兼容与发布

发布前读 [兼容性](references/compatibility.md) 和 [GitHub 发布](references/publishing.md)。README 面向使用者，说明价值、安装、配置、兼容范围、数据边界和输出，不复制 Agent 的内部执行步骤。GitHub 安装部分同时提供“把仓库地址交给 Agent”和 `npx skills add` 两个入口。

严格校验通过后打包：

```text
<python> <oil-skill-creator>/scripts/package_skill.py <skill-path> --public --strict --weak-model --universal
```

打包使用稳定排序和固定时间戳，默认排除 Git、虚拟环境、缓存、evals 和运行 workspace。Review 模式不得执行发布；整改模式只在用户要求交付发布包时执行。

## 完成标准

- 创建：价值成立，主流程可执行，静态校验通过，效果证据与未验证项已说明。
- 整改：P0/P1 已处理或明确接受，相关回归测试完成，没有覆盖无关内容；只有本次需要前后效果对照时，才要求快照和对照评估完整。
- Review：结论有证据，缺陷与取舍分开，给出按优先级排列的最小整改方案，没有修改外部状态。

交付时只报告文件路径、主要能力、程序与测试结果、已确认的兼容范围、效果证据和剩余风险。不要复述整个 Skill，也不要把执行过程写回正式文件。
