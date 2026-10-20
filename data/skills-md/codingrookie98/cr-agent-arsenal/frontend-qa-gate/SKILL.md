---
name: frontend-qa-gate
description: "Use when a frontend artifact needs acceptance verification against real runtime evidence: responsive viewports, interaction states (loading/empty/error/disabled/focus), accessibility (keyboard, focus, screen-reader paths), browser coverage, performance regressions - including AI-assisted frontend deliverables before release. Triggers on frontend acceptance, QA gate, a11y check, responsive breakage, keyboard trap, error-state missing, performance regression, pre-release verification."
license: MIT
---

# frontend-qa-gate 前端产物验收

## 概述

补齐「设计收敛」与「代码审查」之间的空缺：**产物级验收**。回答的不是「设计好不好看」（taste-driven-designer 的 Critic 负责），也不是「代码对不对」（dual-round-review 负责），而是「**它在真实浏览器里是否真的能用**」。

```text
taste-driven-designer D1-D3  →  frontend-qa-gate  →  dual-round-review P4
       (品味与方向)                 (产物断言)            (代码正确性)
```

本技能是**路由层**：只声明触发条件、铁律与断言域，检查细则与报告契约见 `references/`。

---

## 何时使用 / 何时不用

**使用**（满足任一）：
- 前端产物（页面/组件/流程）交付前需要验收，尤其是 AI 生成或 AI 辅助产出；
- 用户问询「响应式是否完整 / 手机端能不能用 / 键盘能不能走通 / 无障碍是否达标」；
- 用户问询「错误态、空态、加载态是否实现」「断网、权限失效、重复提交有没有产物表现」；
- 用户问询「目标浏览器是否覆盖」「性能是否回归」「上线前还需要验什么」；
- taste-driven-designer D3 交付后，或 goal-loop P3.5 集成验证阶段。

**不用**：
- 纯设计方向与品味判断（归 taste-driven-designer 的 Critic 与人类创意总监）；
- 代码级正确性审查（归 dual-round-review）；
- 安全与供应链（XSS / 密钥 / 依赖投毒）——归宿主 CI 与权限层，本技能只在报告中标注「超出验收范围」；
- 后端/数据逻辑任务。

---

## 铁律 (Invariants)

1. **证据优先于叙述**：任何断言必须有可复现操作步骤与产物证据（截图 / 日志 / 测量数值 / 命令输出）。自然语言总结不构成证据。
2. **三态诚实**：每项要求必须落到「已实现 / 已运行验证 / 未验证」三态之一；未验证项不得写成通过。
3. **不做分数判据**：不得输出绝对评分、等级或通过率作为验收结论（taste V1.1 反证 E1/E2/E3 已证伪打分式门禁）。结论只有 PASS / FAIL / BLOCKED。
4. **放行权归人类**：本技能只输出证据与结论与建议，不替代 taste 的 Gate C 人类签收，也不替代 dual-round-review 的终审裁决。
5. **产物级边界**：只依据运行中的产物与行为判定；代码级判据显式路由到 dual-round-review，本技能不在其职责范围内评审代码。
6. **能力门控**：宿主缺少某类验证能力时，对应断言记为「未验证」并计入阻断清单，不得降级为通过。
7. **独立可分发**：不得写跨技能相对路径硬链接（独立安装会断链）；引用他技能只允许命名引用与模式编号。
8. **回流有路由**：验收发现的缺陷必须按 references/regression-routing.md 分流，禁止静默就地修补结构性缺陷。

---

## 断言域 (Five Assertion Domains)

| 域 | 回答的问题 | 细则 |
|:---:|---|---|
| **D-R 响应式视口** | 内容和交互在各视口是否连续可用，而非断点数量 | [acceptance-matrix.md](references/acceptance-matrix.md) §2 |
| **D-S 交互状态** | 加载/空/错误/禁用/焦点/重试/返回恢复是否都有产物表现 | [acceptance-matrix.md](references/acceptance-matrix.md) §1 |
| **D-A 无障碍** | 键盘、焦点顺序、可访问名称、读屏路径、减少动态效果 | [acceptance-matrix.md](references/acceptance-matrix.md) §3 |
| **D-B 浏览器覆盖** | 最低支持版本与关键流程在目标浏览器矩阵是否可用 | [acceptance-matrix.md](references/acceptance-matrix.md) §4 |
| **D-P 性能预算** | 构建体积与关键交互是否相对基线回归 | [acceptance-matrix.md](references/acceptance-matrix.md) §5 |

**执行纪律**：五域中任何一项有未验证或失败断言时，报告结论为 BLOCKED / FAIL，不得在存在未验证项时宣称交付完成。

---

## 快速流程清单 (Quick Checklist)

```text
Q1  ┌ 确定验收范围：产物入口、目标设备/浏览器、基线（上一版或设计稿）
    └ 采集探针环境：URL / 构建号 / commit / 测试数据
Q2  ┌ 按 acceptance-matrix 五域逐项执行断言（能力门控：缺能力即记未验证）
    ├ 每项断言记录：操作步骤 + 证据路径 + 三态标记
    └ 状态矩阵与视口矩阵必须逐格填写（缺失态写「未实现」而非留空）
Q3  ┌ 校验报告结构：python3 scripts/check-qa-report.py <报告文件>
    ├ 失败缺陷按 regression-routing.md 分流并登记
    └ 存在未验证项 → 结论 BLOCKED，交人类裁决
Q4  ┌ 人类签收（放行权在用户）
    └ 需要代码级修复时 → 转 dual-round-review；结构类缺陷 → 回 taste D2
```

---

## 能力门控矩阵 (Capability Gating)

| 宿主能力 | 有 | 无 |
|---|---|---|
| 浏览器驱动（截图/点击/输入） | 执行真实断言 | 该域记「未验证 + 阻断」，交人类或换宿主 |
| 键盘仿真 | 键盘路径与焦点顺序实测 | 仅记录人工待办，不允许推断通过 |
| 屏幕阅读器 | 关键流程读屏实测 | 记为未验证；自动扫描结果不得替代读屏验收 |
| 性能测量（体积/时序） | 与基线数值对比 | 记为未验证，禁止用主观「看起来不卡」替代 |

**总原则**：能力有则测、无则记未验证；**永远不假装验证过**。

---

## 安全与合规边界

- 不在报告中写入任何私密凭据、令牌或真实用户数据；测试数据使用合成数据；
- 截图与日志入库前检查是否含敏感信息；
- 发现凭据泄漏、XSS、依赖投毒等安全问题时：记录现象 + 标注「超出本技能范围」+ 升级宿主 CI 与权限流程，不在本技能内修复。

---

## 参考导航

- [acceptance-matrix.md](references/acceptance-matrix.md) — 五域断言矩阵、状态矩阵与视口矩阵填写纪律
- [browser-verification-protocol.md](references/browser-verification-protocol.md) — 能力门控、证据契约、回执与阻断语义
- [regression-routing.md](references/regression-routing.md) — 缺陷分类回流路由表与路由记录格式
- [qa-report-template.md](templates/qa-report-template.md) — 《前端验收报告》模板（结构受脚本校验）
- [check-qa-report.py](scripts/check-qa-report.py) — 报告结构机械门禁（POSIX 下旧 `.sh` 兼容壳仍可用）
