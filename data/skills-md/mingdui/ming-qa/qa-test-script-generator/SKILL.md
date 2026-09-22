---
name: qa-test-script-generator
description: >
  在用户确认用例之后，把已确认的业务用例展开为可执行的 spec-task 和测试脚本。你产出的是 test-spec-tasks.json——后续执行阶段通过它逐条运行并收集证据。
  你只负责"生成可执行的东西"，不负责"执行"。pass/fail/ready 的判断由后续的执行阶段来做。
  不适用：执行测试、标记 pass/fail、就绪判定。
---

# QA Test Script Generator — 脚本生成

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

你是用例到执行之间的转换层。`qa-testcase-designer` 产出的是人在看的用例，你产出的是执行阶段在跑的 task。
你的 spec-task 写得不精确，后面的执行阶段就没法可靠地判断 pass/fail。

你**不执行**任务、**不标记 pass/fail**、**不判断就绪**。实现状态只到 `implemented`，执行状态留 `not-run`。

## CLI 命令

本阶段所有命令的完整语法、参数说明见**主 skill（quality-assurance-agent）→ CLI 命令参考 → 阶段 3**。这里不重复维护命令语法。

## 生成层级约定

脚本层走**完整测试金字塔**（`generate-spec-tasks` 默认行为）：每条用例按「单元 > 集成 > API > E2E」逐级递减拆解。验收同样要有单元测试（测资金计算、状态机、校验逻辑等白盒行为）——不要把任何一层砍成 0。

默认最小 task 数：P0=8、P1=5、P2=3、P3=1；默认比例 unit 60% / integration 20% / api 15% / e2e 5%。纯后端 scope（无前端 UI）自动跳过 E2E。

## 工作流

### 1. 校验用例

先跑 `validate-cases` 确保用例本身没有 schema 问题。只有 `confirmed` 状态的用例才生成 task。

### 2. 生成 spec-task

先读取 `$QA_AGENT_DIR/references/spec-task-planning.md` 了解 spec-task 的字段契约、覆盖规则和 completion 门禁规则。

运行 `generate-spec-tasks`。确保：
- 每条 task 有 `oracle.ui/api/db/sideEffects/negativeAssertions` 字段
- 每条 P0/P1 风险（来自 risk-analysis.json）出现在对应 task 的 assertions 或 oracle 中

### 3. 校验覆盖率

跑 `coverage-balance --strict`。如果失败，修 spec-task 计划而不是强行通过。

### 3.5 校验脚本实现真实性（映射 ≠ 实现）

```bash
python "$QA_AGENT_DIR/scripts/qa_agent.py"assert-script-implementation --spec-tasks .qa-agent/current/test-spec-tasks.json --repo .
```

门禁校验：每个 `targetFile` 的文件存在、非占位 stub、**可发现的测试方法数 ≥ 映射到它的 task 数**。

- 一个 `targetFile` 映射 54 个 task，但只有 7 个 `@Test` 方法 → 门禁 fail（虚标实现）。
- 占位 stub 脚本（`echo "BLOCKED"; exit 0`）→ 门禁 fail（未真正实现）。

### 4. 实现测试文件

按照 spec-task 逐条实现测试脚本：

- **api 层 task**：bash 脚本（curl + python3 解析 JSON 断言）或 JUnit 集成测试类，直接调后端 API
- **integration 层 task**：需要查库验证的，脚本 + MySQL MCP `read_query` 结合
- **e2e 层 task**：spec 文件路径为 `tests/e2e/<module>/<case-id>.spec.ts`（`@playwright/test` 格式），执行命令为 `npx playwright test <targetFile>`。spec 文件内容由 Playwright Test Agent（planner → generator）生成或手写。团队共享的 fixture 在 `tests/e2e/lib/e2e-fixture.js`（`init-project` 自动部署），提供 `loginAsQA()` 等可复用操作
- **复用已有测试**：精确映射 targetFile/testName/command/assertions/oracle/evidence 到 spec-task

测试脚本的通用约定：
- 用 `python "$QA_AGENT_DIR/scripts/qa_agent.py"run-with-env --repo . --script <path>` 执行，自动加载环境变量
- 入参通过 `--extra KEY=VAL` 传递（不硬编码密码和路径）
- 退出码 0 = pass，非 0 = fail
- 每个 task 实现后更新 `implementationStatus=implemented`，`executionStatus` 保持 `not-run`

### 5. 编写 spec-task 的必需字段

每条 task 必须包含：
- `sourceCaseId`——追溯到用例
- `priority`——必须与对应用例一致（否则 `assert-completion` 会过滤掉并报 filter 诊断）
- `layer`——unit / integration / api / e2e
- `targetFile`——测试文件路径
- `testName`——可读的测试名称
- `command`——可复制粘贴执行的命令
- `assertions`——从用例 `businessAssertions` 派生，去重（不得用模板占位）
- `oracle`——ui / api / db / sideEffects / negativeAssertions 分类，**每项是结构化对象** `{"type","assertion","sourceRiskId"?,...}`，不是字符串
- `traceability`——关联的 risk ID 列表
- `dataBindings`——从用例 `data` 派生的脚本参数（禁止硬编码业务 ID）
- `implementationStatus`——implemented 或 not-implemented
- `executionStatus`——**你这里永远是 not-run**，留给执行阶段来改

根级字段：`generationProfile`（固定为 development，即完整金字塔）、`minSpecsByPriority`、`targetRatio`——`coverage-balance` 会读这些元数据自动匹配配比。

### oracle 结构化契约

```json
{
  "type": "db",
  "assertion": "t_user.virtual_usd_balance 减少 totalDeducted",
  "sourceRiskId": "RISK-P0-001",
  "tableHint": "t_user"
}
```

- DB oracle 必须含具体查询对象和期望，不允许「核心状态一致」这类泛化文字。
- 数据完整性用例（如概率表 gap 校验）生成 `verificationMode: direct-db` 的 task，oracle.db 必须非空。
- `requiresE2E=true` 的风险，即使配比里 e2e 被挤成 0，也必须强制补生成至少一个 e2e task。

## E2E 层输出约定

统一使用 `@playwright/test` 格式，通过 Playwright Test Agent（planner → generator）或手写生成 spec 文件。

| 项 | 约定 |
|---|---|
| `targetFile` | `tests/e2e/<module>/<case-id>.spec.ts`（小写 ID，如 `tc-p1-011.spec.ts`） |
| `command` | `npx playwright test <targetFile>` |
| 共享 fixture | `require('../lib/e2e-fixture')`（`init-project` 自动部署 `e2e-fixture.js`） |
| 配置来源 | `config/env.shared`（团队共享）→ `local/.env`（个人密钥） |
| 浏览器驱动 | `@playwright/test`（`test()`、`expect()`、`page` fixture） |

E2E fixture（`tests/e2e/lib/e2e-fixture.js`）由 `init-project` 首次部署，提供 `loginAsQA()`、`getTestValue()` 等可复用操作。团队后续可一起维护此 fixture。

## 容错与降级

- **上游产物缺失**：`test-cases.json` 不存在或未确认时，退回 `qa-testcase-designer` 阶段，不生成 task。
- **用例 schema 校验失败**：`validate-cases` 不通过 → 退回修正，不强行生成 spec-task。
- **coverage-balance 失败**：修 spec-task 计划而非强行通过门禁。
- **编码损坏**：`test-spec-tasks.json` 写完必须跑 `check-mojibake --strict`。U+FFFD → `safe-write-json` 重写。
- **测试文件写入冲突**：路径已存在且有内容时，先读已有文件，做增量合并而非盲目覆盖。

## 禁令

- **不标记 task 为 passed/failed**。执行才能做这件事。
- **不为了好过 completion 而减少 task 数量**。
- **不绕过 P0/P1 最小 task 数约束和风险衍生的 oracle 要求**。
- **不把已有测试套件的整体通过等同于 spec-task 映射**。必须有精确的文件/命令/断言映射。
- **不创建过量 E2E task**，除非 scope 明确配置了 E2E 覆盖。保持 unit > integration > api > e2e 倒金字塔。
- **不能因为"生成完了"就说工作完成**。你的工作在上游用例确认后才开始，到 spec-task 和测试文件落地才结束。完成判断不在你这里。
- **禁止生成占位 stub 脚本**。任何脚本不得以 `echo "BLOCKED: ..."; exit 0` 形式存在。如果数据准备确实无法自动化（需破坏性 DB 操作等），应在 `test-spec-tasks.json` 中将 task 标记为 `blocked`，写清楚 `blocker`/`owner`/`nextAction`；不要用一个假脚本掩盖阻塞状态。

## DB 断言固化与 MCP 数据准备规范

DB 断言不得「外包」给执行 runner 手工核对——必须固化为可执行的结构化校验。bash 脚本无法直接调用 MySQL MCP（MCP 是 Claude 的工具而非 shell 命令），因此分两类：

### 数据完整性用例（direct-db）

对「数据完整性」类用例（如概率表 gap 校验），生成 `verificationMode: direct-db` 的 task，`oracle.db` 必含「具体 SQL + 期望值」，由 runner 逐条执行并记录结果，不作为自由手工核对项。

```json
{
  "verificationMode": "direct-db",
  "oracle": {
    "db": [
      {
        "type": "db",
        "assertion": "每个概率表首条 outcome_from=0，末条 outcome_to=1",
        "query": "SELECT product_id, MIN(outcome_from) f, MAX(outcome_to) t FROM t_product_prize GROUP BY product_id",
        "expect": "f=0 且 t=1.0",
        "sourceRiskId": "RISK-P1-005"
      }
    ]
  }
}
```

### API 调用类用例（数据准备 PRE/POST）

脚本包含完整 API 调用 + 断言逻辑；数据准备用注释标注，由 runner 通过 MCP 在脚本前后完成。数据准备是**输入准备**，DB 断言仍必须进 `oracle.db` 结构化字段。

```bash
#!/usr/bin/env bash
# Test: TC-P2-032 - Exchange软删除
# MCP 数据准备（执行 runner 在脚本前后完成）：
#   PRE:  mcp__mysql_mcp__write_query "UPDATE t_user_open_record SET is_deleted=1 WHERE id=<PENDING_ID>"
#   POST: mcp__mysql_mcp__write_query "UPDATE t_user_open_record SET is_deleted=0 WHERE id=<SAME_ID>"
set -u
# ... login, API call, assertions ...
```

### 错误模式（禁止）

```bash
#!/usr/bin/env bash
echo "BLOCKED: Requires data preparation"
exit 0  # ← 永远禁止！这是在伪造"执行过"
```

### 执行 runner 的职责

`qa-test-runner` 遇到 `verificationMode: direct-db` 的 task 或标注 `PRE:`/`POST:` 的脚本时：
1. 通过 MySQL MCP 执行 PRE 数据准备
2. 运行脚本（API 调用 + 断言）
3. 通过 MCP 执行 `oracle.db` 逐条校验，记录「查询摘要 + 期望 + 实际 + 状态」到 evidence
4. 通过 MCP 执行 POST 数据还原
5. 所有 MCP 操作失败也记录在 evidence 中；oracle.db 为空视为 spec-task 未完成，不得进入执行阶段
