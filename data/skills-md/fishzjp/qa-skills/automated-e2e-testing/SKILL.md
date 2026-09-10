---
name: automated-e2e-testing
slug: automated-e2e-testing
displayName: E2E 自动化测试
version: 0.8.1
description: "Turn manual cases into Playwright E2E automation run in a browser: page objects, helpers, bug evidence, reports. Not for: API tests, exploratory sessions, bug root-cause. 将手动用例转为 Playwright E2E 自动化并真实执行；含写自动化前的业务熟悉踩点、Page Object/Helper、Bug 证据与报告条目。不用于：API 接口测试、独立探索会话（exploratory-testing）、Bug 根因。"
---

# 自动化 E2E 测试（automated-e2e-testing）

本 skill 覆盖 Web 应用自动化测试的完整工作流：将手动测试用例（markmap + Schema）转化为 Playwright spec → 运行并验证 → 发现 Bug → 输出测试报告。

核心原则：
1. **先熟悉业务再写测试** — 对功能不熟悉时，先用自动化脚本主动探索系统，理解实际行为后再动手写测试代码
2. **有疑问就提问，不自行假设** — 编写过程中遇到任何不明确的地方，必须向用户提问澄清，绝不凭猜测写代码
3. **每条自动化用例对应一条手动用例，每条 test 只测一个点**
4. **每个 test 独立**（自建数据 + 自清理）
5. **必须使用 Page Object** — 正式测试中禁止裸写定位器，所有页面交互封装在 Page Object 中

工程约定（脚手架、配置、场景代码模板、Page Object 规范）统一在 `references/playwright-conventions.md`——写代码时加载；通用 Helper（登录、多会话、证据收集）的参考实现在 `references/helpers_reference.md`；类型域三类执行片段（a11y 扫描 / 视觉基线 / 多浏览器矩阵）见工程约定第 12–14 节，type_scope 判入对应轴时按档加载取用

## When to Use

- 给定测试用例（markmap / Schema），需要生成 Playwright spec 文件并执行
- 编写自动化前，需要小规模业务熟悉探索（踩点页面结构、提取选择器）
- 自动化执行中发现 Bug，需要收集证据并记录测试报告条目
- 需要编写新的 Page Object 或 Helper 函数

## When NOT to Use

- 端到端测试整个需求（理解→策略→用例→执行→报告的流水线）→ 用 `qa` skill 编排
- 编写手动测试用例 → 用 `test-case-writing` skill
- 纯 API 接口测试（无 Web UI 流程）→ 用 `api-testing` skill
- 以**理解系统 / 发现风险**为目的的独立探索式测试会话（charter 驱动、产出探索笔记）→ 用 `exploratory-testing` skill；本 skill 的工作流零只做「为写自动化踩点」的小规模探索
- 已确认 Bug 的根因定位、影响分析、回归建议 → 用 `bug-analysis` skill；本 skill 只负责收集 Bug 证据（截图/API/控制台）并记录报告条目
- 代码变更后判断回归范围 → 用 `regression-testing` skill
- 单元测试 → 用 Jest/Vitest；性能压测 → 专业工具（k6、locust）；安全测试 → 安全审计专项（见 `test-strategy` 的 handoff 约定）

## 提问时机（必须遵守）

**核心规则：不确定就问，宁可多问不要瞎猜。** 格式与裁决规则统一按 `../core/clarify-pattern.md`（场景用「执行确认」）。

| 场景 | 应提问的内容 | 不要自行假设 |
|------|-------------|-------------|
| 元素定位失败 | "在{页面}上找不到{元素}，实际页面结构是否与预期一致？" | 不要随意换选择器猜测 |
| 操作路径不明确 | "测试用例说{操作X}，但页面上没有直接的入口" | 不要自行拼凑操作步骤 |
| 预期行为有歧义 | "预期{结果A}，实际{结果B}，应以哪个为准？" | 不要选择性地相信其中一个 |
| 业务规则不清楚 | "规则{X}的具体边界是什么？" | 不要用常见默认值代替 |
| 探索中发现异常 | "发现{异常行为}，这是预期行为还是 Bug？" | 不要自行判定是 Bug 还是特性 |
| 用例反复超时/不稳定 | "{页面}是否存在长连接或轮询推送（WebSocket/SSE/心跳上报）导致页面永不空闲？" | 不要一律套 networkidle 等待，按等待降级阶梯处理 |

## 工作流零：业务熟悉（前置必做，为写自动化踩点的小规模探索）

**何时需要**：从未测试过该功能模块 / 出现不熟悉的页面路由 / 需要编写新的 Page Object / 拿到用例但不知道系统长什么样

> 本工作流是**小规模踩点探索**（理解页面结构、提取选择器、落 Page Object），产出服务于工作流一。以理解系统 / 发现风险为目的的**完整探索会话**（charter 驱动、产出探索笔记）用 `exploratory-testing` skill。

### 步骤

1. **探索页面结构**：登录 → 导航到目标页面 → 截图 → 枚举所有可交互元素
2. **体验核心流程**：按测试用例步骤走一遍完整流程，每步截图，记录 API 调用
3. **记录发现**：页面导航路径、关键元素选择器、API 接口、隐藏行为、**编写或更新 Page Object**

探索代码模板见 `references/playwright-conventions.md` 第 4 节（explore-*.spec.ts）。

### 完成标准

- [ ] 每个涉及的页面都有截图
- [ ] 理解了页面间的导航路径
- [ ] 确认了关键元素的选择器
- [ ] 记录了实际的 API 请求
- [ ] 发现了隐藏行为（隐藏字段、默认值、前置条件）
- [ ] 已编写或更新了对应的 Page Object

---

## 工作流一：手动用例 → 自动化代码

> **前提**：已完成工作流零（业务熟悉），对目标功能有充分认知。

### 用例输入与自动化范围判定

输入是 `test-case-writing` 产出的 markmap 用例文件（如含 `测试用例.schema.yaml` 则一并消费）：

- Schema 的 `execution_model: ui` 且 `automation.supported != no` 的用例 → 本工作流的转换对象
- `execution_model: dev-collab`（无 UI 协作用例）→ 移交 `api-testing` 或保持手动协作执行，不硬造 UI 自动化
- `automation_plan` 存在时（`test-strategy` 产出）按用户的执行策略裁决执行；策略未定时向用户确认哪些用例转自动化

### 步骤

1. **解析测试用例**：从 markmap Markdown 提取场景与预期；test 名沿用用例的 TC 编号（如 `TC-01-03: {用例名称}`），手动用例缺编号时先补编号再转换
2. **选择/新建 Page Object**：检查 `tests/pages/` 下是否已有对应 Page Object，优先复用
3. **编写 spec**：使用 Page Object 封装所有页面交互。每条 test 收笔前过**断言三问**：① 前置里有"不应匹配/应被排除"的数据吗？断言覆盖了"不在"吗？② 被测步骤的触发方式与用例规格一致吗（不得为绕开不稳定换触发路径）？③ 失败时能区分"功能坏了"还是"环境没加载"吗？——判定与反例见工程约定第 15 节
4. **运行验证**：`npx playwright test tests/{文件名}.spec.ts`；**基线零通过禁交付**——首轮运行 0 条通过即视为流程认知错误（选择器/弹窗结构/等待假设与真实页面不符）：回工作流零针对性重踩核实，修订复跑至 ≥1 条通过后才可进入后续步骤，禁止交付基线零通过的规格

脚手架、场景代码模板（CRUD / 表单提交 / 状态流转 / 多用户并发）、Page Object 规范与 spec 命名**此时加载 `references/playwright-conventions.md`**（第 1、5–7 节）。

---

## 工作流二：Bug 探索与记录

在已理解业务逻辑的前提下，系统性验证页面功能，发现 Bug 和不一致。

> 批量失败前置分流：一轮执行结束**失败 ≥3 条**时，先加载 `../core/triage.md` 做四分类定类（A 真缺陷 / B 资产问题 / C 环境 / D 不稳定），仅 A 类进入本工作流的证据收集与报告条目；<3 条维持单条流程不变。
>
> headless 流水线场景（PR 冒烟 / 夜间全量 / 发布卡点）：检查点降级为未决项、产物落盘规范与退出码语义按 `../core/pipeline-integration.md`（此时加载）；其回流闭环中的批量失败同样进入上方分流流程。

> 职责边界：本工作流负责**发现 + 证据收集 + 报告条目**。Bug 被**确认**后的根因定位、影响分析、回归建议移交 `bug-analysis` skill（对应报告条目中根因分析等五个扩展字段留 TODO）。

### Bug 发现策略

| 策略 | 检查方式 | 典型 Bug |
|------|---------|---------|
| UI 预期不一致 | 对比测试用例与实际截图 | 默认值不对、文案错误 |
| 表单校验缺失 | 提交非法数据 | 必填不校验、范围不限制 |
| 网络异常 | 监听 API 响应 | 500 错误、超时 |
| 数据不一致 | 操作后 reload 验证 | 提交成功但数据丢失 |
| 状态流转错误 | 多步操作验证状态 | 状态未更新、卡死 |
| 控制台错误 | `setupConsoleLogging(page)` 持续监听 | 组件崩溃、静默失败 |

### Bug 证据收集（发现 Bug 时必须执行）

```
Bug 发现 → 截图操作前 → 操作触发异常 → 截图操作后 → 收集 API/控制台日志 → 写入报告
```

证据收集代码（`setupBugTracking` / `tracker.collect`）见 `references/playwright-conventions.md` 第 8 节；通用 Helper 落地时**加载 `references/helpers_reference.md`**。

截图命名统一小写 `bug-{序号}-*` 前缀：手动截图记录过程两态（`bug-001-01-操作前.png`、`bug-001-02-异常.png`）；`tracker.collect()` 自动补一张整页汇总截图（`bug-001-汇总.png`）并 attach 到 HTML 报告。Bug 报告标题中的 `BUG-{序号}` 仅为显示格式。

### Bug 报告格式

记录在 `{项目名}/测试报告_{来源}_{日期}.md`，**条目字段与 `../core/report-template.md` §3（测试报告唯一来源模板，此时加载）保持一致**，保证条目可直接拼装进 `qa` 收尾的最终报告；本 skill 的发现方式含「业务熟悉探索」。执行分报告还需包含 §2 执行统计（P0/P1/P2 × 用例数/通过/失败/阻塞/未执行表，同样按 report-template）；条目中根因分析等五个扩展字段留 TODO，由 `bug-analysis` 填写。按 report-template「机读摘要」约定，分报告末节追加机读摘要片段（占位符替换后），供 `qa` 收尾与后续回归编排机读解析。

---

## Explore 文件生命周期管理

业务熟悉探索文件（explore-xxx.spec.ts）是**临时产物**，遵循以下生命周期：

```
创建 explore-xxx.spec.ts → 提取知识到 Page Object → 删除 explore 文件 + 截图
```

### 规则

1. **知识提取后立即删除**：将发现的选择器、API 路径、页面结构写入 Page Object 或 helpers 后，删除 explore 文件
2. **截图清理**：探索产生的 `debug-*.png` 截图是临时调试产物，确认不需要后删除
3. **不积累**：`tests/` 目录下不应存在已完成的 explore 文件。如果存在，说明知识提取步骤被跳过了
4. **Bug 报告截图保留**：`bug-{序号}-*.png` 截图属于 Bug 报告的一部分，不删除

---

## 关键技巧速查表

> 下表方法名（`createDualSession` / `tracker.collect` / `setupBugTracking` / `isServerCrash` 等）为本 skill **脚手架内置 helper 的示例**（定义在 `references/`），不是 Playwright 通用 API——换项目时按 `references/helpers_reference.md` 适配实际脚手架，勿假定这些函数存在。

| 场景 | 方法 | 备注 |
|------|------|------|
| 受控组件输入框（Ant Design 等） | `fill()` 优先，不生效再 `keyboard.type()` | `fill` 会派发 input 事件，多数受控组件可用；`keyboard.type` 逐键最稳但慢 |
| 确认弹窗按钮 | 在 `role=dialog` 作用域内定位（如 `page.getByRole('dialog').getByRole('button', { name: '确定' })`） | 防止与页面同名按钮歧义命中；弹窗外「确定/删除」同名按钮是常见误击源 |
| 隐藏必填字段 | `page.evaluate()` 直接设值 | 阻止表单提交的常见原因 |
| 网络请求验证 | `page.on('request')` 监听 | 必须在操作之前设置 |
| 数据持久化验证 | `page.reload()` + 断言 | 确认数据真正保存 |
| 多用户会话 | `createDualSession(browser, roleA, roleB)` | 两个角色并发 |
| 登录态复用 | `createSession(browser, role)` | 缓存 storageState 免重复 UI 登录（工程约定第 10 节） |
| 等待策略 | ① auto-wait + `expect` 断言 → ② `waitForResponse` → ③ `networkidle`（仅传统 SSR/MPA） | 自上而下优先（工程约定第 9 节）；固定 `waitForTimeout` 仅临时调试；长轮询/心跳页对 networkidle 永不空闲 |
| 并行执行 | 默认串行，独立性达标后开 `workers` | 前提：自建数据 + 自清理 + 唯一命名逐项核对（工程约定第 11 节） |
| flaky 定性 | 首次失败原样重跑通过 → 判 flaky | 重跑只用于定性；定位根因前标 `test.fixme`（工程约定第 11 节） |
| 截图调试 | `page.screenshot({ fullPage: true })` | 每个关键步骤都截图 |
| 服务端崩溃检测 | `isServerCrash(bodyText)` | 检测 500/502 错误 |
| 唯一命名 | `${前缀}-${Date.now()}` | 避免测试间名称冲突 |
| Bug 证据收集 | `tracker.collect(testInfo, id, desc)` | 一键收集截图+API+控制台 |
| Bug 探索前置 | `setupBugTracking(page)` | 注册 API 和控制台监听 |

## Common Mistakes

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 受控组件值不生效仍反复 `fill()` | 测试卡死或断言失败 | `fill` 失效时改用 `keyboard.type()`（见速查表） |
| 网络监听放在 click 之后 | 捕捉不到请求 | 先注册 listener，再执行操作 |
| 不清理测试数据 | 后续测试受影响 | afterEach 中删除创建的资源 |
| 用固定 timeout 等待 | 时序不稳定 | 按等待降级阶梯换用：① auto-wait+expect 断言 → ② `waitForResponse` → ③ `networkidle`（工程约定第 9 节） |
| 不验证持久化 | 数据可能只存在内存 | reload 后重新断言 |
| 正式测试不使用 Page Object | 代码重复，难以维护 | 所有页面交互封装在 Page Object 中 |
| explore 文件不删除 | 上下文污染，AI 每次读大量废代码 | 知识提取后立即删除 |
| 遇到疑问自行假设 | 产出不可靠的测试 | 不确定就向用户提问 |
| Bug 只截图不记录 API/控制台 | 开发无法定位根因 | 用 `setupBugTracking()` + `tracker.collect()` |
| 硬编码环境地址/账号 | 无法跨环境运行、泄露敏感信息 | 统一放 `constants.ts` / `.env`，代码只引用常量 |
| 失败重跑变绿就当没事 | flaky 混入主干，CI 随机红 | 按 flaky 定性流程处理：先定性再修根因，禁止调大重试硬压（工程约定第 11 节） |
| 对长轮询/推送页强套 networkidle | 超时假失败 | 按等待降级阶梯换 `waitForResponse`/断言自动轮询（工程约定第 9 节） |
| 每个 context 都走一遍登录页 | 执行时长翻倍、缓存认证态形同虚设 | 用 `createSession()` 复用 storageState，失效自动回退 UI 登录（工程约定第 10 节） |
| 所有用例永久串行不敢并行 | 全量执行时长线性膨胀 | 独立性核对通过后渐进开启 `workers`（工程约定第 11 节） |
| 手动用例信息不足仍硬造定位器与操作路径 | 幻觉自动化：断言全绿但没测到真实行为 | 先过 `../core/executability.md` 转换闸门 + 工作流零踩点核实页面结构 |

---

## 与其他 skill 配合

- **上游**：`test-case-writing` 产出手动用例（markmap + Schema）→ 本 skill 把 `execution_model: ui` 且可自动化的用例变成可执行代码；端到端流水线由 `qa` 编排
- **旁路**：无文档 / 系统陌生的**完整探索会话**用 `exploratory-testing`，其探索笔记可作为本 skill 踩点的输入
- **下游**：Bug 确认后的根因 / 影响 / 回归分析 → `bug-analysis`；执行报告与 Bug 条目按 `../core/report-template.md` 对齐，供 `qa` 收尾汇总
- **平级**：纯 API 用例的自动化 → `api-testing`
