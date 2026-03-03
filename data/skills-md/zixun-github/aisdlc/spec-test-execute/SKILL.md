---
name: spec-test-execute
description: Use when 需要在 Spec Pack 的 verification 阶段产出 `{FEATURE_DIR}/verification/report-{date}-{version}.md`（测试报告），给出可交付结论并可追溯到用例与缺陷引用。
---

# Spec 测试执行与报告（V4：Execute + Report）

本技能产出“结论性测试报告”：回答 **是否满足 AC、是否可交付、阻断点是什么、下一步动作是什么**。

**权威口径：** `design/aisdlc_spec_verification.md`

---

## 硬门禁（必须遵守）

- **先定位再读写**：必须先运行 `spec-context` 得到并回显 `FEATURE_DIR=...`；失败即停止，禁止猜路径。
- **必读项目级 memory**：`project/memory/product.md`、`project/memory/tech.md`、`project/memory/glossary.md`；读不到必须写 `CONTEXT GAP`。
- **输入依赖**：`verification/test-plan.md` 与 `verification/usecase.md` 必须存在；`verification/suites.md` 若存在则纳入覆盖统计。
- **缺陷不在 Spec Pack 落盘**：禁止新建 `verification/bugs/**`；报告只做“缺陷编号/链接/状态/严重程度”的引用清单。
- **禁止越权路由**：完成后只输出 `ROUTER_SUMMARY`，下一步由 `using-aisdlc` 决策。

---

## 红旗清单（出现任一条就停止）

- 想在缺少 `test-plan.md` / `usecase.md` 的情况下写“结论性报告”
- 想把缺陷细节落盘到 `verification/bugs/**`（本阶段只允许引用外部缺陷系统）
- 想在版本未知时写固定版本号或用 `TBD` 代替（必须用 `unknown` 并显式 `CONTEXT GAP`）

---

## 唯一做法（PowerShell）

### 1) 获取 `FEATURE_DIR`

```powershell
. ".\skills\spec-context\scripts\spec-common.ps1"
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

### 2) 命名规则（强制）

- `date`：`YYYY-MM-DD`
- `version`：构建/发布可追溯标识（版本号、build id、git sha）
- 若版本未知：使用 `report-{date}-unknown.md`，并在报告中写明 `CONTEXT GAP: version/build unknown`

### 3) 目标输出路径（示例）

```powershell
$date = "2026-03-02"
$version = "unknown"
$out = Join-Path $FEATURE_DIR ("verification/report-{0}-{1}.md" -f $date, $version)
Write-Host "OUTPUT=$out"
```

---

## 报告最小结构（建议）

写入 `{FEATURE_DIR}/verification/report-{date}-{version}.md`，至少包含：

- 测试摘要
  - 结论：通过 / 不通过 / 有条件通过
  - 版本/构建/环境（未知必须写 `CONTEXT GAP`）
- 覆盖统计
  - 按套件/优先级：总数、执行数、通过、失败、阻塞、未执行
- 关键失败与阻断项
  - **必须可追溯到用例编号（TC-...）**
- 缺陷清单（仅引用）
  - 缺陷系统/Issue 编号 + 链接 + 状态 + 严重程度
- 遗留风险与建议
  - 下一步动作必须可执行（返工/补测/灰度/加监控/回滚建议）
- 追溯链接
  - `requirements/*`、`verification/test-plan.md`、`verification/usecase.md`、（可选）`verification/suites.md`

---

## DoD 自检（V4-DoD）

- [ ] 报告有明确结论（不是“已测完”）
- [ ] 所有失败/阻断项都能定位到 `TC-*` 与外部缺陷编号（如有）
- [ ] 风险与建议可执行（下一步动作明确）

---

## 完成后输出与自动路由（必须执行）

`report-{date}-{version}.md` 落盘后，**必须**完成以下动作（按顺序，不可省略）：

1. **输出 ROUTER_SUMMARY**（YAML 形态，供 Router 决策）：
```yaml
ROUTER_SUMMARY:
  stage: V4
  artifacts:
    - "{FEATURE_DIR}/verification/report-{date}-{version}.md"
  needs_human_review: true
  blocked: false
  block_reason: ""
  notes: "测试报告为结论性产物：建议评审结论/阻断项后再进入发布/merge-back 等后续动作"
```

2. **立即执行 `using-aisdlc`**：将上述 `ROUTER_SUMMARY` 作为路由输入传递给 using-aisdlc，由 Router 判定下一步并**自动推进**（无需等待用户说「继续」）。  
   - 若 Router 判定可自动续跑：在同一轮对话内继续执行下一步 worker skill（如 Finish、MergeBack 等）
   - 若 Router 触发硬中断：停下并输出阻断原因、需要的输入、候选下一步

3. **对话输出**：在调用 using-aisdlc 前，可简短说明「本阶段产物已落盘，正在调用 using-aisdlc 路由下一步。」

---
name: spec-test-execute
description: Use when 需要在 sdlc-dev 的 Spec Pack 中执行 verification 阶段验证（V4），记录执行结果并产出报告输出物 report-{date}-{version}.md（作为执行的证据与结论载体）。
---

# Spec 测试执行（V4：执行验证并产出报告）

## 概览

本技能是 **verification 阶段 worker skill**，只负责：

- 门禁校验（先定位 `{FEATURE_DIR}`，再读必要输入）
- 执行验证（可为手工执行/自动化执行的记录；不绑定框架）
- 产出**执行输出物**：`{FEATURE_DIR}/verification/report-{date}-{version}.md`
- 按 V4-DoD 自检（结论性 + 可追溯）
- 输出 `ROUTER_SUMMARY` 后回到 `using-aisdlc`

本技能 **不** 决定下一步做什么（由 `using-aisdlc` 路由）。

## 报告命名规则（强制）

- 文件名：`report-{date}-{version}.md`
- `date`：`YYYY-MM-DD`
- `version`：构建/发布版本号或可追溯标识（例如 `v1.7.3`、`build-20260302.1`、`sha-abc1234`）

若 `version` 无法获得：仍可生成报告，但必须：

- 文件名使用 `report-{date}-unknown.md`
- 在报告内写 `CONTEXT GAP: version/build unknown`，并在结论中降低置信度（通常为有条件通过/不通过，取决于准出标准与阻断项）

## 硬门禁（不得绕过）

### 1) 先定位 FEATURE_DIR（禁止猜路径）

```powershell
. ".\skills\spec-context\scripts\spec-common.ps1"
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

失败即停止。

### 2) 必读项目级 Memory（缺失写 CONTEXT GAP）

- `.aisdlc/project/memory/product.md`
- `.aisdlc/project/memory/tech.md`
- `.aisdlc/project/memory/glossary.md`

任一缺失：在报告中显式写 `CONTEXT GAP`，并说明它如何影响结论可信度。

### 3) 必须读取 verification 输入

执行前必须读取：

- `{FEATURE_DIR}/verification/test-plan.md`
- `{FEATURE_DIR}/verification/usecase.md`
- `{FEATURE_DIR}/verification/suites.md`（如存在）

若缺失：停止并回到 `using-aisdlc`（因为无法证明范围/口径/覆盖）。

## 执行记录要求（最小）

- 以 `usecase.md` 的用例编号（`TC-...`）为最小统计单位
- 每条用例必须给出结果：Pass / Fail / Blocked / Not Run
- Fail/Blocked 必须给出：
  - 对应 `TC-...`
  - 外部缺陷编号/链接（或明确写“尚未提缺陷”的阻断原因与下一步动作）
- 禁止在 Spec Pack 内新增 `verification/bugs/**`

## 输出（落盘）

- `{FEATURE_DIR}/verification/report-{date}-{version}.md`

## 报告最小结构（必须包含）

- 测试摘要
  - 结论：**通过 / 不通过 / 有条件通过**（三选一）
  - 版本/构建/环境
  - 执行日期（与文件名 date 一致）
- 覆盖统计
  - 按优先级与（如存在）套件：总数、执行数、通过、失败、阻塞、未执行
- 用例结果清单
  - `TC-...` → Pass/Fail/Blocked/Not Run
- 关键失败与阻断项
  - 每条必须可追溯到 **TC 编号**
- 缺陷清单（仅引用外部系统）
  - 缺陷编号/链接/状态/严重度
  - 必须关联到对应 TC 编号
- 遗留风险与建议（可执行下一步动作）
- 追溯链接（requirements/design/implementation 的关键入口）
- CONTEXT GAP（如有）

## V4-DoD 自检

- [ ] 报告给出明确结论（不是“已测完”）
- [ ] 所有失败/阻断项均可定位到 TC 编号与外部缺陷编号/链接
- [ ] 统计口径可解释（为何未执行/为何阻断）
- [ ] 风险与建议可执行（下一步动作明确）

## 红旗 STOP

- 未回显 `FEATURE_DIR=...` 就开始执行/落盘报告
- 结论写“通过”，但存在未执行/阻断项且未解释
- Fail/Blocked 没有关联 TC 编号或外部缺陷引用

## 完成后输出与自动路由（必须执行）

`report-{date}-{version}.md` 落盘后，**必须**完成以下动作（按顺序，不可省略）：

1. **输出 ROUTER_SUMMARY**（YAML 形态，供 Router 决策）：
```yaml
ROUTER_SUMMARY:
  stage: V4
  artifacts:
    - "{FEATURE_DIR}/verification/report-{date}-{version}.md"
  needs_human_review: true
  blocked: false
  block_reason: ""
  notes: "测试报告为结论性产物：建议评审结论/阻断项后再进入发布/merge-back 等后续动作"
```

2. **立即执行 `using-aisdlc`**：将上述 `ROUTER_SUMMARY` 作为路由输入传递给 using-aisdlc，由 Router 判定下一步并**自动推进**（无需等待用户说「继续」）。  
   - 若 Router 判定可自动续跑：在同一轮对话内继续执行下一步 worker skill（如 Finish、MergeBack 等）
   - 若 Router 触发硬中断：停下并输出阻断原因、需要的输入、候选下一步

3. **对话输出**：在调用 using-aisdlc 前，可简短说明「本阶段产物已落盘，正在调用 using-aisdlc 路由下一步。」

