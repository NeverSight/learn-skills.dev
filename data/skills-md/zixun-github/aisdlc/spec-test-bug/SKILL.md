---
name: spec-test-bug
description: Use when 需要在 Spec Pack 的 verification 阶段创建“可直接粘贴到外部缺陷系统”的缺陷报告（不在 Spec Pack 内落盘 bug 文件），并将缺陷引用回写到 `{FEATURE_DIR}/verification/report-*.md`。
---

# Spec 缺陷报告（Vx：Bug Report Drafting）

本技能用于在 verification 阶段生成 **结构化缺陷报告正文**（面向 Jira/禅道/Linear/GitHub Issue 等外部系统），并确保缺陷信息可以回流到 Spec Pack 的 `report-*.md`（作为交付阻断与风险证据）。

> 重要边界：
>
> - **禁止**在 Spec Pack 内新增 `verification/bugs/**` 或任何 bug 文件/目录。
> - 本技能的输出主要是“对话输出”，用于粘贴到外部缺陷系统；外部缺陷创建后，需把编号/链接等信息回写到 `report-*.md` 的“缺陷清单”。

---

## 输入与门禁（必须遵守）

**REQUIRED SUB-SKILL：正在执行 `spec-context` 获取上下文，并在对话中回显 `FEATURE_DIR=...`（允许 `(reuse)`）。**

- **先定位再回写**：若需要把缺陷编号/链接回写到 `report-*.md`，必须先通过 `spec-context` 获取 `FEATURE_DIR`；失败即停止，禁止猜路径。
- **必读项目级 memory**：`project/memory/product.md`、`project/memory/tech.md`、`project/memory/glossary.md`；缺失必须写 `CONTEXT GAP`。
- **最小事实输入**（用户需提供，或从上下文提取）：
  - 现象描述（实际 vs 期望）
  - 复现步骤（可由他人复现）
  - 环境信息（OS/浏览器/设备/环境/版本或构建）
  - 影响评估（用户影响/频率/业务影响/数据影响/安全影响）
  - 证据（截图/录屏/日志/网络请求摘要；可为空但需说明原因）
  - 关联用例编号：至少 1 条 `TC-*`（来自 `verification/usecase.md`）

---

## 输出（对话输出，不落盘 bug 文件）

本技能输出两部分：

1. **缺陷报告正文（Markdown）**：按模板生成，可直接粘贴到外部缺陷系统。
2. **Report 回写片段（Markdown）**：用于粘贴到 `{FEATURE_DIR}/verification/report-{date}-{version}.md` 的“缺陷清单 / 阻断项”区，字段包含：
   - 外部缺陷编号 + 链接 + 状态 + 严重程度/优先级
   - 关联 `TC-*`
   - 是否阻断交付（与 `test-plan.md` 的 Exit Criteria 对齐）

模板来源（强制使用）：

- `assets/bug_report_templates.md`

---

## 执行要点（强制）

- **标题必须具体**：`[模块/能力] 在 [条件/操作] 下出现 [错误]`（避免“有 bug/不行了”）。
- **复现步骤必须可执行**：每一步都应具体，避免“点击按钮然后报错”。
- **环境必须可追溯**：至少包含 OS、浏览器/设备、环境（Dev/Staging/Prod）与版本/构建。
- **敏感信息处理**：日志/截图必须脱敏；安全类问题避免给出可直接利用的攻击代码。
- **与用例绑定**：缺陷必须关联到至少一个 `TC-*`，否则会导致 `report` 无法可追溯。

---

## DoD 自检

- [ ] 标题具体且可检索
- [ ] 复现步骤可由第三方复现
- [ ] 期望 vs 实际清晰
- [ ] 环境信息完整且可追溯
- [ ] 已给出 Severity / Priority
- [ ] 已关联 `TC-*`
- [ ] 已提供证据或写明缺失原因
- [ ] 已给出对交付的影响与是否阻断

