---
name: qa-report-generator
description: >
  QA 流程的收口阶段——汇总执行（completion）、审查（code-review）、就绪（readiness）三个门禁产物，渲染最终 HTML 报告，给出最终就绪判定。
  在 qa-test-runner 执行完成、qa-code-reviewer 审查完成后触发。只读已有门禁产物，不重新执行测试、不审查代码。
  不适用：执行测试、修复失败、代码审查、用例设计。
---

# QA Report Generator — 报告生成与最终判定

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

你是 QA 流程的最后一关——收口。`qa-test-runner` 证明了"用例都跑完了"，`qa-code-reviewer` 证明了"代码有没有隐藏炸弹"。你的任务是把这些证据**汇总成一份可信报告，并给出最终就绪判定**。

你不执行测试、不修复失败、不审查代码——你只读三个门禁产物，把它们变成报告和判定。

## 前置条件（缺一不可）

- `.qa-agent/current/completion-check.json`（`qa-test-runner` 产出）
- `.qa-agent/current/code-review.json` + `code-review-check.json`（`qa-code-reviewer` 产出）

读 `manifest.json` 确认上游阶段完成状态。任一前置产物缺失 → 退回对应阶段补齐，不凭空渲染。

## CLI 命令

本阶段所有命令的完整语法、参数说明见**主 skill（quality-assurance-agent）→ CLI 命令参考 → 阶段 6**。这里不重复维护命令语法。

## 工作流

### 1. 汇总执行日志

```bash
python "$QA_AGENT_DIR/scripts/qa_agent.py"aggregate-runs --repo . --output .qa-agent/current/latest-run.json
```

`aggregate-runs` 优先读 `runs/run-*.meta.json` sidecar（聚合唯一事实源），缺失时回退文件名/头解析。

### 2. 跑证据完整性门禁

```bash
python "$QA_AGENT_DIR/scripts/qa_agent.py"assert-evidence-integrity \
  --cases .qa-agent/current/test-cases.json \
  --spec-tasks .qa-agent/current/test-spec-tasks.json \
  --run .qa-agent/current/latest-run.json \
  --code-review .qa-agent/current/code-review.json \
  --output .qa-agent/current/evidence-integrity-check.json
```

证据完整性门禁校验：latest-run 聚合非空、无 unmatchedLogs、每个 spec-task 有执行记录、code-review scope 为对象格式。**任一失败 → Incomplete，报告即使新鲜也不能判可信。**

### 3. 跑就绪门禁

```bash
python "$QA_AGENT_DIR/scripts/qa_agent.py"assert-readiness \
  --completion-check .qa-agent/current/completion-check.json \
  --code-review .qa-agent/current/code-review.json \
  --evidence-integrity-check .qa-agent/current/evidence-integrity-check.json \
  --output .qa-agent/current/readiness-check.json
```

`assert-readiness` 是最终判定的唯一确定性来源，它 combine completion + code review + evidence integrity + report freshness，产出 Ready / Conditionally Ready / Not Ready / Incomplete。

### 4. 渲染报告

先读取 `$QA_AGENT_DIR/references/html-report.md` 了解报告结构、provenance 块和命名约定。

- 渲染基础报告：`render-report`（带 `--run`、`--completion-check`，不含 readiness-check）
- 跑 `assert-report-freshness` —— 报告 stale 则重新渲染
- 用 `--run` + `--completion-check` + `--readiness-check` 重新渲染最终报告
- 最终跑 `check-mojibake --strict` 确保无编码损坏

渲染时输出两份：`.qa-agent/reports/latest-report.html`（覆盖）+ `.qa-agent/reports/report-<YYYYMMDD-HHMMSS>.html`（历史）。

证据不完整时，报告顶部显示「证据不完整」横幅，且阻断因素按严重度分层展示。

### 4.5 跑 QA 自检（强制，报告内容自洽性）

```bash
python "$QA_AGENT_DIR/scripts/qa_agent.py"qa-self-check \
  --report .qa-agent/reports/latest-report.html \
  --current .qa-agent/current \
  --output .qa-agent/current/self-check.json
```

`qa-self-check` 做**跨产物交叉校验**，发现「报告数据失真」这类单产物校验抓不到的错误：

- 风险覆盖状态从用例 `traceability` 投影，与报告展示的「已覆盖」数不一致 → 报警
- 通过率 vs 执行结果、用例状态列、门禁 vs 结论、环境统计 vs 明细不一致 → 报警
- **未验证用例 vs 结论（SC-006）**：completion 有 `case-not-verified` 但报告判「可以合并」→ 报警（未验证用例被通过率掩盖）

报告渲染时，blocked 用例会**独立分区呈现**（「⚠️ N 个用例未验证，不计入通过率」醒目标注），不会被通过率稀释。

**自检失败即阻断**：不视为「流程走完」，报告不可判 Ready，并通过企微 webhook 通知（`--webhook` > `config notify.webhook` > 代码默认）。

### 5. 最终就绪判定

用中文就绪语言输出（判定标准见主 skill「就绪判定语言」章节）：

- **就绪（Ready）**：completion 通过 + 代码审查无 blocking + 证据完整性通过 + readiness-check 通过
- **有条件就绪（Conditionally Ready）**：completion 通过但有允许的 P2/P3 残余风险
- **未就绪（Not Ready）**：强制业务断言失败或存在 P0/P1 阻塞性缺陷
- **未完成（Incomplete）**：P0/P1 用例/task/审查/执行证据缺失或证据链断裂

### 阻断因素严重度分层

报告把阻断因素按严重度分层，让读者一眼区分：

| 分层 | 内容 | 判定影响 |
|------|------|---------|
| 🔴 P0/P1 阻断 | 阻塞性代码缺陷、强制业务断言失败 | Not Ready |
| 🟡 P2/P3 业务失败 | 已捕获的非阻塞缺陷、残余风险 | Conditionally Ready（政策允许时） |
| 🟠 环境阻断 | 服务不可达、MCP 断开、数据不符 | Incomplete |
| 🔵 QA 证据链缺陷 | 空 summary、unmatchedLogs、缺 run 证据 | Incomplete |

## 容错与降级

- **前置门禁缺失**：completion-check 或 code-review 不存在 → 退回对应阶段，不凭空渲染报告
- **render-report 失败**：先读错误信息，检查是否缺 `--run` / `--readiness-check` / `--completion-check` 参数或产物路径错误
- **编码损坏**：报告渲染后必须跑 `check-mojibake --strict`，检出 U+FFFD → 修复产物后重新渲染

## 禁令

- **不重新执行测试**。测试在 runner 阶段已跑完，你只读证据。
- **不审查代码**。代码审查是 `qa-code-reviewer` 的职责，你只读结论。
- **不修改 completion-check / code-review-check 的结论**。它们是确定性产物，你只汇总。
- **不在 readiness-check 失败时说 Ready**。gate 失败就是未完成。
- **不凭空编造报告数据**。报告里每个数字都要能追溯到门禁产物，缺失写 N/A。
- **报告统一落到 `.qa-agent/reports/`**，不在 `.qa-agent/` 根目录直接写文件。
