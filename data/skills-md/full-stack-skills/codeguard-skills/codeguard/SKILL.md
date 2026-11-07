---
name: codeguard
license: Apache-2.0
description: Codeguard 主入口与路由中心；当用户要求识别仓库语言、执行 lint/格式门禁、受控修复、CVE 扫描、Git 分支或提交治理、接口/代码/数据安全审查，或在 commit/push/release 前需要证据化质量结论时使用。
compatibility: 需要 Codeguard 运行时命令或源码仓库上下文；默认只读检查，不自动安装、改规则、提交或推送。
---

# codeguard 主入口：跨语言代码规范门禁

> 把“看起来没问题”变成有命令、范围、版本和退出码的可重复证据。当前能力快照见 `references/capabilities/registry-summary.md`。

## Capability Boundaries

### ✅ Strengths
1. 项目语言自动检测（扩展名 + 标记文件双重识别）
2. 统一 lint 门禁：`bin/codeguard check`（或 scripts/run_check.py），失败即退出码 2
3. 统一自动修复：`bin/codeguard fix`（spotless / cargo fmt / eslint --fix / ruff --fix），仅 Legacy 引擎可用
4. CVE 依赖漏洞编排：`bin/codeguard cve`（Maven dependency-check / npm audit / pip-audit / cargo audit，附修复指引）
5. 提交门禁：用户表达「提交/push」意图时全量复检（UserPromptSubmit 钩子）
6. 会话总结：Stop 钩子输出本轮 lint 通过/失败/自动修复计数

### ⚠️ Prerequisites
1. 各语言工具链已安装（mvn / cargo / node / ruff），缺失时门禁报告「无法验证」而非通过
2. Redis（仅安全钩子需要；lint 门禁不依赖）

### ❌ Out of Scope（路由表）
1. 语法学习、框架用法、库选型 → 对应语言的官方技能仓（如 full-stack-skills/java-skills）
2. 分支创建与命名 → `codeguard-git-branch`
3. commit message 格式 → `codeguard-git-commit`
4. 泄露/密钥/CVE → `codeguard-security-code`
5. 越权/鉴权注解/文件上传 → `codeguard-security-api`
6. 加密存储/脱敏/国密/等保密评 → `codeguard-security-data`

## When to Use

- "跑一下 lint" / "/check" / "代码规范检查"
- "修一下 style 问题" / "/fix"
- "扫一下依赖漏洞" / "codeguard cve"
- 提交前最后自检

## I. 标准工作流

```bash
# 0. 先判定引擎（必做）
codeguard --version --format json 2>/dev/null && echo ENGINE=rust || echo ENGINE=legacy
```

完整引擎契约见 `references/operations/engine-contract.md`。下面主路径为 Legacy Python 引擎：

```bash
# 1. 检测语言
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/detect_lang.py" "$(pwd)"

# 2. 全量 lint 门禁（主路径）
bin/codeguard check                     # 或 python3 scripts/run_check.py
bin/codeguard check --lang java         # 只跑某语言

# 3. 失败 → 自动修复 → 复扫（fix 仅 Legacy 存在）
bin/codeguard fix --lang <name>

# 4. CVE 扫描（提交前必跑）
bin/codeguard cve --severity HIGH
```

Rust 引擎下改用位置参数（`check all|java`、`cve <rust|python|typescript>`），且 `fix`、`--lang`、`--ecosystem`、`--severity` 均不存在。它是否可签发由自报能力决定：`codeguard capabilities all --format json` 中该类别 `status` 为 `implemented` 才可签发；`gap`、`not_applicable`、读不到或找不到该单元时，一律表述为未完成并回到 Legacy 命令面。

## II. 门禁规则（不可协商）

| 规则 | 说明 |
|---|---|
| lint 失败 = 阻塞 | 严格模式下退出码 2，AI 必须修复后才能继续对话中的写码动作 |
| 无法验证 ≠ 通过 | 工具缺失（exit 127）输出「无法验证」并给出安装命令，不计入通过 |
| 未完成 ≠ 通过 | 退出码 3 表示检查没跑完，只能报告未完成，不得表述为通过或零漏洞 |
| 检查出来得修 | CVE/HIGH 以上发现必须给出修复动作；禁止只报告不处理 |
| 禁止静默豁免 | 不得用 `@SuppressWarnings` / 调高阈值 / 改门禁配置来让失败消失；确需豁免须用户明确同意并在 suppressions 登记理由 |

## III. 修复决策树

```text
lint 失败
├─ 格式类（缩进/import 顺序/行宽）→ 自动修复（fix 命令）→ 复扫
├─ 缺失类（javadoc/@param 缺失）→ 补写注释/文档
└─ 逻辑类（unused 变量有语义/复杂度超标）→ 人工判断，禁止自动改业务代码
```

## Workflow

1. `bin/codeguard detect` 确认语言
2. `bin/codeguard check` 全量扫描
3. 失败项按上方决策树分类处理
4. 处理后复扫至全绿
5. 用户要求提交时，确认 `bin/codeguard cve` 也通过

## Gotchas

1. `mvn javadoc:jar` 的错误在 `mvn compile` 中不出现——不要用 compile 结果当门禁结论
2. 嵌套仓库/子模块会让 detect 扫描超时——对大仓库用 `--lang` 限定范围
3. 工具未装（exit 127）时门禁**不通过也不算漏洞**，先装工具再复扫
4. `npm audit fix` 可能引入破坏性升级——fix 后必须回归测试

## On-Demand Resources

- 能力快照：`references/capabilities/registry-summary.md`。
- 门禁决策契约：`references/rules/decision-contract.md`。
- 证据化操作手册：`references/operations/evidence-playbook.md`。

## Official References

- 各语言工具官方文档见对应语言技能的 Official References 段

## 不适用范围（什么时候不该用）

- 任务是语法学习、框架设计或业务建模，应直接使用对应专业技能。
- 用户要求证明生产可用性，但当前只能获得 lint 或本地扫描证据。
- 任务需要安装、提交、推送、发布或修改安全阈值，却未得到明确授权。

## 数据与安全

本技能不收集、上传、发送或存储用户源码和凭据。默认只读路由；涉及网络扫描、修改文件、Git 写操作或安全例外时，必须交给专用技能并重新核对授权边界。

## 证据化 Workflow

### Step 1：判定用户意图

将请求分为 detect、check、fix、cve、Git 治理或 security，避免一次调用无关能力。

### Step 2：确认作用域和授权

记录仓库/模块、当前 Git 状态、是否允许修改，以及网络、安装、提交和发布边界。

### Step 3：读取能力状态

核对当前语言或功能是 `stable` 还是 `planned`，不把识别能力冒充为可执行门禁。

### Step 4：交给一个主技能

以一个主技能产出结论；只在需要独立证据层时调用其他技能。

### Step 5：验证并报告

将 lint、format、build、test、security、Git 和发布证据分层，明确写 PASS、FAIL、UNVERIFIED 或 PLANNED。

## Rules

1. 每次请求只指定一个主路由，其他为可选证据层。
2. 工具缺失、超时或能力 planned 不等于 PASS。
3. 不删除规则、降低阈值或静默抑制来制造绿灯。
4. 提交、推送和发布需要独立授权，质量检查通过不代表可自动执行。

## 输出模板

```text
Codeguard 路由结果
- 目标：<user intent>
- 作用域：<repo/module/path>
- 主技能：<selected skill>
- 能力状态：<stable/planned>
- 证据：<commands/checkpoints and results>
- 状态：PASS / FAIL / UNVERIFIED / PLANNED
- 未验证：<remaining layers>
```

## 按需加载资源

- 需要核对技能层级与路由时读取 `references/capabilities/registry-summary.md`。
- 需要形成证据包时读取 `references/operations/evidence-playbook.md`。
- 需要决策边界时读取 `references/rules/decision-contract.md`。
- 只打开 `examples/` 中匹配当前任务的示例。
