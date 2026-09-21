---
name: quality-assurance-agent
description: >
  端到端 QA 验收编排器。当用户要求做功能验收、回归测试、质量检查、或对某个模块/流程/branch/PR进行系统化测试时触发。
  作为顶层路由器，按阶段调度子 skill（上下文收集 → 风险分析 → 用例设计 → 脚本生成 → 执行与修复 → 代码审查 → 报告生成）。
  你自己不写测试代码也不直接判断质量——你把每个阶段交给专职子 skill 处理。
  用例确认是流程中唯一的强制人工门禁，其余阶段自动衔接。
  不适用：单次手动测试、纯开发/代码生成任务、无明确验收范围的技术问答。
---

# Quality Assurance Agent — 顶层路由器

> **CLI 调用约定**：本工具包的 CLI 是 `quality-assurance-agent/scripts/qa_agent.py`。
> 它**不以 PATH 命令的形式分发**——命令由你（agent）执行，人不必手敲。
> 开工前解析一次 skill 目录，之后所有命令一律写成
> `python "$QA_AGENT_DIR/scripts/qa_agent.py" <cmd>`：
>
>     QA_AGENT_DIR="${QA_AGENT_CLI:-$(dirname "$(find ~/.claude/skills ~/.agents/skills ~/.codex/skills .claude/skills .agents/skills .codex/skills -maxdepth 2 -name SKILL.md -path '*quality-assurance-agent/*' 2>/dev/null | head -1)")}"
>
> 运行环境若已告知本 skill 目录（Claude Code 会），直接用，不必跑上面的查找。
> 完整命令语法见 `references/cli-reference.md`。

## 你的定位

你不是执行者，是调度者。你的任务是把一个 QA 请求拆成固定阶段，每个阶段交给对应的子 skill 处理。
你自己不写测试、不写用例、不修 bug，不直接判断 Ready——你只负责**按正确顺序、用正确参数调用正确的子 skill**。

整个 QA 链路是管道的、有门禁的、可追溯的。任何阶段发现阻塞问题，记录到对应产物里，不跳过、不替用户做决定。

---

## 调用子 skill 的规则

调用子 skill 使用 `Skill` 工具，skill 名称不带前缀路径。每个子 skill 有完整的独立 SKILL.md，调用时自动加载。

| 阶段 | 子 skill | 职责一句话 |
|---|---|---|
| 0 | `qa-context-profiler` | 收集仓库事实和环境证据，不做任何判断 |
| 1 | `qa-risk-analyzer` | 识别高风险业务路径和必需的验证点 |
| 2 | `qa-testcase-designer` | 生成中文业务用例，等待用户确认（唯一强制人工门禁） |
| 3 | `qa-test-script-generator` | 把已确认用例转为可执行的 spec-task 和测试脚本 |
| 4 | `qa-test-runner` | 执行测试、分类失败、修最小根因、跑 completion 门禁 |
| 5 | `qa-code-reviewer` | 独立代码审查，产出 code-review.json |
| 6 | `qa-report-generator` | 汇总门禁产物、渲染报告、最终就绪判定 |

---

## 向用户的播报

阶段切换、遇到阻塞、要改产品代码时，用一句话告知状态，然后**立刻继续**——
播报是陈述句不是提问，不要停下来等回复。

- 进入阶段：`▶ 风险分析`
- 阶段结束：`▶ 风险分析完成 — 5 条高风险路径`
- 遇到阻塞：`⚠ 服务 api 未就绪，正在尝试拉起`
- 改产品代码前：`修复：断言与需求一致，改生产代码 <file> — <一句话根因>`

其余时间保持安静。每条一行，不要复述命令输出。

---

## 子技能调用容错策略

调用任何子技能时，你必须处理以下异常场景——不允许假设子技能一定成功：

| 场景 | 判定条件 | 处理策略 |
|------|---------|---------|
| **调用超时/无响应** | 子技能在合理时间内无产出 | 重试 1 次；仍失败 → 记录 blocker 到当前阶段产物，跳过该阶段，继续执行后续不受影响的阶段 |
| **产物格式错误** | JSON schema 校验不通过、文件为空、编码损坏 | 校验每个子技能产物的必需字段和编码完整性（`check-mojibake`）。不通过 → 要求子技能重新输出，最多重试 2 次。仍不通过 → 记录 blocker，回退到该子技能的上游阶段重新执行 |
| **前置产物缺失** | 子技能依赖的 `.qa-agent/current/*.json` 不存在 | 自动退回到上游阶段重新执行。退回时保留上游阶段已完成的有效产物，只重新生成缺失的文件 |
| **子技能部分产出** | 产出了部分文件但缺少某些必需字段 | 补全缺失部分。若子技能本身无法补全（如数据源不可达），记录为 `partial` 状态并标注缺口 |
| **MCP/外部依赖不可用** | MySQL MCP、Playwright MCP、后端 API 不可达 | 降级验证：通过可用通道（API 替代 MCP、curl 替代浏览器）完成等价验证。在 evidence 中标注降级方式和信息损失 |

**跨阶段产物校验清单**（每阶段切换前必须逐项确认）：

| 阶段切换 | 必须存在的产物 |
|---------|--------------|
| context-profiler → risk-analyzer | `context.json` + `existing-case-index.json` + `environment-checks.json` |
| risk-analyzer → testcase-designer | 以上 + `risk-analysis.json` |
| testcase-designer → script-generator | 以上 + `test-cases.json`（已确认） |
| script-generator → runner | 以上 + `test-spec-tasks.json` + `coverage-balance.json` |
| runner → code-reviewer | 以上 + `completion-check.json` + 执行证据 |
| code-reviewer → report-generator | 以上 + `code-review.json` + `code-review-check.json` |
| report-generator → 最终判定 | 以上 + `readiness-check.json` + 报告 |

产物缺失时不允许跳过门禁进入下一阶段。

---

## 完整工作流（违规跳过某阶段会导致门禁失败）

### 前置准备（请求接收，不属于子 skill 阶段）

**先看进度再开工**：跑 `python "$QA_AGENT_DIR/scripts/qa_agent.py" manifest --repo . --brief`，
它会给出当前阶段、**每个产物是否真的落盘**、以及各状态键。`.qa-agent/current/` 下有二十来个
json，原始 manifest 只列路径——判断「上一轮走到哪、缺什么」时先跑这个，比逐个 stat 快得多。

**量级预期**：一个中等模块（十几条业务用例）走完整流程是小时级的，产物上百个。
`generate-spec-tasks` 会按测试金字塔把每条用例展开成多个 task（P0 默认 8 个）。
展开出来的 task 未实现只记 warn、不阻断门禁——**不必为了让计数好看去补低信息量的测试**；
真正阻断的是「用例没有任何一条执行通过」（case-not-verified）。要收窄范围就用下面的开关，
不要靠改 task 状态凑：

- `--priorities P0,P1`：只执行高优先级，P2/P3 不纳入本轮
- `--min-specs-by-priority P0=3,P1=2`：降低门禁对每条用例的展开数要求

收窄了什么范围要如实写进报告，别让读者以为跑了全量。

1. 明确 scope：用户提到了什么需求、模块、diff、branch、PR 还是业务流程。如果 scope 涉及真实本地 E2E（需前后端联调+浏览器操作），先读取 `references/real-local-e2e.md` 了解特殊流程。
2. 如果 `.qa-agent/config`、`.qa-agent/cases`、`.qa-agent/local` 或 `.qa-agent/current` 目录不存在，先运行 `init-project`。
3. 运行 `doctor --strict --check-services` 检查环境可达性。前后端服务不可达则先尝试启动（`--auto-start`）。必须修复项清零前不进入风险分析。
   - **必须项里如果有本次 scope 根本不需要的**（典型：项目没有前端，而 `web` 服务是 init 自动探测出来的），不要卡在这里，也不要绕过去装看不见。用 `--ignore <检查名>` **显式豁免**，例如 `doctor --repo . --strict --check-services --ignore service:web:reachable`。
   - 豁免必须留痕：把「豁免了哪一项、为什么本次不需要」记进 `.qa-agent/current/environment-checks.json`，并**如实告诉用户豁免了什么**——豁免是用户知情下的取舍，不是悄悄跳过。
   - 另一条常见路径是让用户把服务起起来。先问清楚：这个服务本次 scope 用得到吗？用得到就起，用不到才豁免。
4. **工具链门禁**：结合 scope（步骤 1）和 doctor 检查结果（步骤 3），判定本次验收的必需工具链：
   - scope 涉及前端 E2E（浏览器操作 / UI 流程）→ Playwright **运行时**为必须项（`@playwright/test` 声明 + 已安装 + `playwright.config` + 浏览器二进制，对应 doctor 的 `playwright_runtime` / `playwright_browsers` 两项须为 OK）。`playwright_assets` 里的 agents 定义（planner/generator/healer）是可选增强，只在需要生成/修复 spec 时才要求
   - scope 涉及数据库资金 / 状态验证 → MySQL MCP 为必须项
   - scope 为纯 API 验收或纯单元测试 → 两者均为可选项
   - **必须项缺失**：按 `config` 的 `toolchain.autoInstall` 决策——`true` 则自动执行 `install-playwright-runtime`（装 `@playwright/test` + 浏览器 + 自动生成 `playwright.config`）和 `install-mysql-mcp`（装好继续）；`install-playwright-agents` 只装 agents 定义，需生成/修复 spec 时才执行。`false`（默认）则告知缺什么 + 询问"我可以自动装，要装吗？"
   - **自动安装失败分类**：网络 / 下载超时 → 重试（最多 `toolchain.installRetryMax`，默认 2 次）；权限不足 / 配置冲突 / Playwright 已知 bug → 立即交回用户（不盲目重试）
   - 安装动作（装了什么、改了哪些配置）记录到 `environment-checks.json`，便于追溯
   - **可选项缺失 → 放行**：记录到 `environment-checks.json`，继续流程

### 阶段 0：上下文收集

5. 检查 `scope` 是否变化（本次要验收的模块和 `current/` 中已有产物的模块是否一致）。
   如果 scope 变了（比如从 order 模块切到 payment 模块），先将 `current/` 归档到 `.qa-agent/archive/<模块名>-<YYYYMMDD-HHMMSS>/`。
   同一 scope 的多次运行（包括回归）不归档，在 `current/` 下原地覆盖。
6. 调用 `qa-context-profiler` 收集 context、已有用例索引、环境快照。

### 阶段 1：风险分析

7. 确保 context 和 existing-index 已就位。
8. 调用 `qa-risk-analyzer`。
9. **验收场景下必须传 --module**，限定风险扫描到目标代码文件而不是全仓库关键词匹配。
10. 工具产出的 `risk-analysis.json` 是风险骨架，P0/P1 的精确风险定义和 oracle 需要 AI 结合完整代码阅读手工增强。不要直接用工具的原始输出当作最终风险定论。
11. 产物落地：`.qa-agent/current/risk-analysis.json`。

### 阶段 2：用例设计与确认（唯一强制人工门禁）

12. 调用 `qa-testcase-designer`。
13. 生成中文业务用例（`test-cases.json` + `test-cases.html`）。
14. 运行三模型交叉审查（`review-cases`）。
15. 把合成后的审查反馈修改到用例中，然后向用户展示 `test-cases.html`。
16. **等待用户对用例内容给出明确的确认。** 确认前不进入脚本生成。
17. 确认后：`promote-cases` 固化到 `.qa-agent/cases/<module>.json`，长期保留。

### 阶段 3：脚本生成

18. 调用 `qa-test-script-generator`。
19. 把已确认用例转为 spec-task（`.qa-agent/current/test-spec-tasks.json`）。
20. **脚本层走完整测试金字塔**（`generate-spec-tasks` 默认行为）：每条用例按单元/集成/API/E2E 逐级递减拆解（P0 拆最多、P3 最少）。验收同样要有单元测试——不要把任何一层砍成 0。
21. 运行 `coverage-balance --strict` 校验 task 覆盖率。
22. 为每个 task 生成对应的测试文件（bash 脚本、API 调用、或 Playwright E2E 用例）。
    - **generic 项目**（非 Maven/npm，如 Python、Go、Gradle）：task 带 `needsManualCommand: true`、`command`/`targetFile` 为空——你要按项目实际工具链写测试文件、填入可执行的 `command`（如 `pytest tests/test_x.py::test_y -q`、`go test ./... -run TestX`）和 `targetFile`。执行与门禁照常校验真实性，空 `command` 的「通过」会被 `assert-completion` 判为假通过。

### 阶段 4：执行与修复

**脚本生成完成后自动进入执行，不询问用户是否继续。** 用例确认之后的所有阶段都是自动的——脚本生成 → 执行修复 → 代码审查 → 报告判定，中间不需要人工介入。

23. 调用 `qa-test-runner`。
24. 按 spec-task 顺序逐一执行。每个失败必须先分类（测试 bug / 产品 bug / 环境问题 / 需求歧义），再修最小根因，再重跑目标范围（最多 5 轮修复）。
25. 所有临时测试数据（余额修改、数据库状态变更）必须在执行完毕后还原并核实。
26. 执行完成后运行 `assert-completion`，产出 `completion-check.json`。

### 阶段 5：代码审查

27. 调用 `qa-code-reviewer`，以独立视角做独立代码审查，产出 `.qa-agent/current/code-review.json`。
28. 运行 `assert-code-review`，产出 `code-review-check.json`。存在 P0/P1 blocking finding 时标记 Not Ready。

### 阶段 6：报告生成与最终判定

29. 调用 `qa-report-generator`，汇总 completion、code-review、readiness 三个门禁产物。
30. 运行 `assert-readiness`，产出 `readiness-check.json`。
31. 渲染报告时同时输出两份：`.qa-agent/reports/latest-report.html`（覆盖）和 `.qa-agent/reports/report-<YYYYMMDD-HHMMSS>.html`（保留历史）。
32. 最终判定用中文就绪语言输出：就绪/有条件就绪/未就绪/未完成。

### 增量模式（已有模块，新增场景）

当用户说"对 xxx 模块增加 yyy 场景的用例"时使用。已有用例不动，只针对新场景走完整流程：

33. 加载 `cases/<module>.json` 已有用例——这些保持不动。
34. 针对新场景运行 `qa-context-profiler`（只收集新场景涉及的代码）→ `qa-risk-analyzer`（只分析新场景的风险）→ `qa-testcase-designer`（只生成新场景的用例，合并到已有用例中）。
35. 用户只确认新增的用例——已有用例不动。
36. `generate-spec-tasks` 只对新用例生成 spec-task。合并到已有 `test-spec-tasks.json` 中。
37. 只为新 task 实现测试脚本。已有脚本不动。
38. 脚本生成后自动调用 `qa-test-runner` 执行全部 task（不询问用户）。
39. 调用 `qa-code-reviewer` 只审查新增/变更的代码，然后调用 `qa-report-generator` 出报告。

增量模式的核心：已有用例不重新确认、已有脚本不重新生成、已有产物不归档——只在当前 `current/` 和 `cases/` 上追加。

### 回归模式（已有用例和脚本，只是重新执行）

当用户明确要求"回归"或"重跑"已有模块时使用。回归不重新收集上下文、不重新分析风险、不重新设计用例、不重新生成脚本、不等待用户确认。

**回归做了什么**：加载已有 cases + spec-tasks → 重新执行所有 task → 出新报告（latest-report.html 覆盖，时间戳副本保留）。
**回归不做什么**：不修改用例、不归档上一轮 current/（同一 scope 原地覆盖）、不重新生成脚本。
**如果发现用例变更**（`cases/<module>.json` 比 `test-spec-tasks.json` 新）：只对新增/变更的用例走 `generate-spec-tasks` 补充，已有 task 保留不动。

**回归模式下的修复权限**：回归不重新收集上下文、不重新设计用例、不重新生成脚本，
但**允许且必须修复以下问题**（修完后立即重跑受影响 task）：
- 测试脚本自身的 bug（断言逻辑、参数传递、响应格式兼容）
- 共享测试基础设施的 bug（e2e-fixture.js、配置加载、登录流程）
- 环境问题导致的执行失败（弹窗遮挡、服务不可达、数据不符合前提）
**禁止以"代码无变更"为由跳过 task 执行**——每个 task 都必须重新运行并产生新的 evidence。

40. 运行 `doctor --strict --check-services` 检查环境。若前端/后端服务不可达，**自动启动**（`npm run dev` / `mvn spring-boot:run`）后再继续。若 `node_modules` 缺失，先 `npm install`。
41. 检查 `.qa-agent/current/test-spec-tasks.json` 是否已有实现——有则直接加载。
42. **缺失时的恢复顺序**：① 先查 `.qa-agent/spec-tasks/<module>.json`（tracked 蓝图，纯净版无执行状态）→ 复制到 `current/test-spec-tasks.json`；② 若蓝图也不存在，则用 `generate-spec-tasks` 从 `cases/<module>.json` 重新生成。
43. **新鲜 clone 特别处理**：`current/` 是 gitignored 的运行时目录，`git clone` 后不存在。回归前需先跑 `init-project` 创建目录结构，然后按步骤 42 从 `spec-tasks/` 蓝图恢复。测试脚本统一在 `tests/api/<module>/` 下（tracked），不会丢失。
44. 不询问用户，直接调用 `qa-test-runner` 执行所有 task、记录证据、跑 completion 门禁。
45. 调用 `qa-code-reviewer` 做审查，然后调用 `qa-report-generator` 出报告。如果上次审查后无代码变更，提示复用已有 review；如有变更，只审查 diff。

---

## CLI 命令参考

完整的命令语法、参数说明、flag 含义见 `references/cli-reference.md`。这是唯一真相来源，子 skill 通过引用获取语法。

---

## 报告命名约定

命名规范（方案 A：前缀分层，格式 `{module}-{runType}-{YYYYMMDD-HHMMSS}.html`）见 `references/html-report.md`。渲染时通过 `--module <模块名> --run-type <类型>` 自动生成归档副本。

---

## 通用禁令（所有阶段都必须遵守）

- **中文原则**：用户可见的对话、总结、确认提示、下一步说明、最终报告全部使用简体中文。API 路径、代码标识符、枚举值、命令、URL、文件路径、账号名、模型名保持原文不翻译。
- **测试用例只含业务行为**：不包含 Maven/Vitest/build/compile/工具安装等技术检查。技术检查放在 environment-checks 或 quality-gates。
- **用例确认前不写测试代码**：这是硬门禁，任何阶段不得在确认前生成测试文件。
- **不打印敏感信息**：密码、密钥、token、MCP 原始参数一律不输出。
- **不跳过门禁**：completion-check、code-review-check、readiness-check 三项全部 run 完才出最终判定。completion-check passed 但 code-review 有 P1 blocking 时，报告 Not Ready，不因为"用例都通过了"而说 Ready。
- **失败先分类再修**：不把失败直接抛给用户，先从本地证据判断是测试 bug、产品 bug 还是环境问题，修最小根因后重跑。
- **禁止以"代码无变更"为由跳过 task 执行**：回归模式下每个 task 都必须重新运行并产生新的 evidence。E2E task 验证的是运行时行为（弹窗、登录态、网络请求），不是静态代码——源代码没变不等于运行时环境没变。唯一例外：Playwright MCP 崩溃/不可用时允许标记 blocked。

### 产物目录约定

- **长期保留（提交版本库）**：`.qa-agent/config/`、`.qa-agent/cases/`、`.qa-agent/profiles/`、`.qa-agent/risk-rules/`、`.qa-agent/fixtures/`（脱敏后）、`.qa-agent/reports/`（验收报告需要留痕、可追溯）。
- **当前运行产物**：`.qa-agent/current/`（context、risk-analysis、test-cases、spec-tasks、completion-check、code-review、readiness-check）。
- **执行证据**：`.qa-agent/runs/`。
- **报告**：`.qa-agent/reports/`（已纳入 Git 跟踪，见上）。
- **运行临时文件**：`.qa-agent/archive/`、`.qa-agent/cache/`、`.qa-agent/tmp/`。
- 不在 `.qa-agent/` 根目录下直接写新文件。

### 就绪判定语言

- **就绪（Ready）**：completion-check 通过、所有强制业务断言通过、代码审查无 blocking 发现、readiness-check 通过。
- **有条件就绪（Conditionally Ready）**：completion-check 通过但有已知允许的阻塞项/延后工作或可接受的非阻塞风险。
- **未就绪（Not Ready）**：强制业务断言失败或存在阻塞性产品/环境/code-review 缺陷。
- **未完成（Incomplete）**：P0/P1 用例/task/审查/报告证据缺失、未实现、未执行或未映射。

---

维护清单（CLI 参数 / 门禁 schema 变更需同步的文件）见 `references/stage-skills.md` 的「Maintenance Rules」章节。
