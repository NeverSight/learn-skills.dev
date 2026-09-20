---
name: qa-testcase-designer
description: >
  在风险分析完成后、写测试代码之前，生成中文业务用例并等待用户确认。这是整个 QA 流程中唯一的强制人工门禁——确认后不可回头改用例。
  从 context、risk-analysis、已有用例索引出发，生成只含业务行为的 test-cases.json（不含技术检查如 Maven/build/安装），
  渲染 test-cases.html 供用户审阅，运行三模型交叉审查，合成反馈修改后提交确认。确认后 promote 到长期 knowledge base。
  不适用：写测试代码、执行测试、代码审查。
---

# QA Testcase Designer — 用例设计与确认

> **CLI 调用约定**：本工具包的 CLI 是 `quality-assurance-agent/scripts/qa_agent.py`。
> 它**不以 PATH 命令的形式分发**——命令由你（agent）执行，人不必手敲。
> 开工前解析一次 skill 目录，之后所有命令一律写成
> `python "$QA_AGENT_DIR/scripts/qa_agent.py" <cmd>`：
>
>     QA_AGENT_DIR="${QA_AGENT_CLI:-$(dirname "$(find ~/.claude/skills ~/.agents/skills ~/.codex/skills .claude/skills .agents/skills .codex/skills -maxdepth 2 -name SKILL.md -path '*quality-assurance-agent/*' 2>/dev/null | head -1)")}"
>
> 运行环境若已告知本 skill 目录（Claude Code 会），直接用，不必跑上面的查找。
> 完整命令语法见 `$QA_AGENT_DIR/references/cli-reference.md`。

## 你的定位

这是 QA 管道中**唯一需要人工确认的环节**。你前面的 `qa-risk-analyzer` 告诉你哪里危险，你后面的 `qa-test-script-generator` 把你的用例变成可执行任务——但你这里卡住，整条线不会推进。

你的任务是：**把风险分析转成可验证的中文业务用例，交给用户看，用户说可以了才放行。** 用户没点头之前，不生成哪怕一行测试代码。

## CLI 命令

本阶段所有命令的完整语法、参数说明见**主 skill（quality-assurance-agent）→ CLI 命令参考 → 阶段 2**。这里不重复维护命令语法。

## 前置条件（缺一不可）

1. `.qa-agent/current/context.json` 存在
2. `.qa-agent/current/existing-case-index.json` 存在
3. `.qa-agent/current/risk-analysis.json` 存在

如果缺失，退回上游阶段补齐。读 `manifest.json` 可以快速确认各阶段完成状态。

## 用例的语言规则

- **用例描述使用简体中文**：title、preconditions、steps、expected、businessActor、operationPath、businessStateBefore、businessAction、businessStateAfter、businessAssertions、risk——所有人类可读字段用中文写。
- **保持原样不翻译的**：API 路径、代码标识符、枚举值、命令、URL、文件路径、账号名、模型名、具体的技术参数值。
- **用例只写业务行为**：谁、在什么状态下、做什么操作、期望看到什么结果。不写"编译成功""Maven 测试全量通过""Playwright 安装完成"——这些放在 environment-checks 或 quality-gates 里。
- **不要用 "200/400" 这种不确定的预期结果**，不确定就去读代码或写进 open question。

## 用例优先级规则

- **P0**：涉及资金损失、数据不一致、越权、主流程阻塞、状态损坏、结算/支付/奖励计算错误。P0 用例必须在任何验收轮次中全部覆盖。
- **P1**：核心业务规则和重要回归场景。
- **P2**：边界值、非法输入、重试/超时、非关键异常路径。
- **P3**：展示细节、文案、视觉打磨、非阻塞兼容性。

每条 P0/P1 风险（来自 risk-analysis.json）必须映射到至少一条用例或一条明确记录的 open question。做不到就是你的工作没完成。

映射必须落进用例的 `riskIds` 字段（风险编号数组，如 `["RISK-P0-001"]`）——**这是覆盖投影唯一读取的来源**。
只在 `risk`、`traceability` 或行文里提到风险编号不算关联，报告会把它算作未覆盖的缺口。
`riskIds` 为空而风险实际已被覆盖时，报告会输出与事实相反的结论。

## 工作流

### 1. 加载上游材料

读三个文件：
- `.qa-agent/current/context.json`——知道改了哪些代码、接口路径、数据表结构
- `.qa-agent/current/existing-case-index.json`——知道已有用例，避免重复生成
- `.qa-agent/current/risk-analysis.json`——知道危险在哪里，需要什么断言

### 2. 加载项目经验

读 `.qa-agent/knowledge/` 下与本次 scope 相关的经验，指导用例设计：

```bash
python "$QA_AGENT_DIR/scripts/qa_agent.py"show-knowledge --repo . --module <module> --category data-prep
python "$QA_AGENT_DIR/scripts/qa_agent.py"show-knowledge --repo . --module <module> --category api-quirk
python "$QA_AGENT_DIR/scripts/qa_agent.py"show-knowledge --repo . --module <module> --category test-pattern
```

- `data-prep` 经验指导你设计用例的前置数据准备（怎么构造余额不足、已过期资产等）
- `api-quirk` 经验指导你写预期结果（null 字段被省略、业务错误码在响应体等）
- `test-pattern` 经验指导你设计可复用的验证方式

### 3. 生成用例

先读取 `$QA_AGENT_DIR/references/test-case-schema.md` 确认用例 JSON 的完整字段规范（优先级规则、验证规则、quality gate shape、environment check shape）。

- 优先复用已有用例（相同 ID 和历史执行记录保持不变）
- 增量生成只覆盖新增或变更的业务操作路径
- 每条 P0/P1 风险必须有一条用例或一个 open question
- 草稿写入 `.qa-agent/current/test-cases.generated.json`

### 4. 合并+校验

运行 `merge-existing-cases` 把生成内容与已有用例合并到 `test-cases.json`。
运行 `validate-cases --summary --check-mojibake --strict-language`。校验报错必须修到归零。

### 5. 渲染+审查

运行 `render-cases` 生成 HTML 确认页。
先读取 `$QA_AGENT_DIR/references/model-review.md` 了解三模型审查的具体流程和输出格式。

运行 `review-cases` 做三模型交叉审查。审查反馈中的有效发现要**合成后修改 test-cases.json**——不能只跑一遍 review 就原样提交。review 的边界值缺失、优先级评级、模糊断言、缺失负向路径这些建议，你要逐条判断是否采纳，采纳的改到用例里，不采纳的记录理由。

### 6. 编码检查

运行 `check-mojibake` 对所有产物做编码完整性扫描。Windows 下 AI Write/Edit 工具写中文 JSON 偶发 U+FFFD 替换字符——如果检出问题，用 `python "$QA_AGENT_DIR/scripts/qa_agent.py"safe-write-json --from-stdin` 通过 Python 管道重写受损文件。

### 7. 用户确认——这是硬门禁

把 `test-cases.html` 展示给用户审阅。确认不是流程性的"过一下"，而是让用户逐条看到：

- 每条用例的标题、优先级、层级、前置条件、操作步骤、预期结果、覆盖的风险编号
- 哪些 P0/P1 风险被覆盖了、哪些变成了 open question
- scope 锁定的四要素：scope / business main path / blockers / oracles

**不要替用户做确认决策。** 你必须等待用户给出明确肯定（"通过""确认""可以""继续"）。
在用户确认前：
- 不运行 `promote-cases`
- 不调用 `qa-test-script-generator`
- 不写任何测试脚本

### 8. 确认后固化

用户确认后立即运行 `promote-cases`，把确认后的用例复制到 `.qa-agent/cases/<module>.json`。
这是长期 knowledge base，供后续轮次复用。`test-cases.json` 保留为当前运行的 working copy。

### 9. 移交

确认固化的用例移交 `qa-test-script-generator`。注意：**P0/P1 风险和 risk-analysis.json 必须一并传下去**，spec-task 的 oracle 和 assertions 要从这里派生。

## 编码安全

- `test-cases.json`、`test-cases.html`、`model-review.json` 全部要通过 `check-mojibake --strict`
- 如果你用 AI 的 Write 工具直接写 `test-cases.json` 内容，写完后必须立即做 U+FFFD 检查
- 多次出现编码损坏时改用 `python "$QA_AGENT_DIR/scripts/qa_agent.py"safe-write-json --from-stdin`（通过 Python 管道写入）

## 容错与降级

- **上游产物缺失**：`context.json`、`existing-case-index.json`、`risk-analysis.json` 任一缺失 → 退回对应阶段补齐，不回退到更上游。
- **三模型审查不可用**：若某模型调用失败，用剩余模型完成交叉审查，在 `model-review.json` 中标注缺失。
- **编码损坏**：所有 JSON/HTML 产物必须通过 `check-mojibake --strict`。U+FFFD → `safe-write-json` 重写。
- **验证失败**：`validate-cases --strict-language` 失败 → 修正后重跑，不绕过校验。

## 禁令

- **确认前不写测试代码**。这包括不创建测试文件、不手写 spec-task、不生成 Playwright 脚本。确认是硬门禁。
- **不用 Maven/build/install/编译/工具查询等纯技术检查来充当业务用例**。技术检查放 quality-gates 或 environment-checks。
- **不复制已有用例**。已有用例扩展或复用，不创建新 ID 的重复用例。
- **不忽略 risk-analysis.json 的 P0/P1 风险**。每一条必须有归宿。
- **不要把 draft 用例和 confirmed 用例混在同一文件**。
- **不要把 `test-cases.json` 当作长期真相来源**。确认后必须 promote 到 `cases/` 目录。
