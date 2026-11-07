---
name: codeguard-check
license: Apache-2.0
description: 对 Codeguard 支持的仓库执行只读 lint 门禁并解释结果；当用户说 check、跑检查、lint 报告、提交前检查，或 CI 的 Codeguard 检查失败时使用。必须区分 PASS、FAIL、UNVERIFIED、INCOMPLETE 与 PLANNED，并写明结果由 legacy 还是 rust 引擎签发。
compatibility: 需要 Codeguard CLI 和目标语言工具链；默认不修改源码、不安装工具。
---

# codeguard check

> 只读质量门禁：识别真实作用域，调用仓库已配置的检查器，并保留可重复的失败证据。

## 30 秒开始

先判定引擎（`codeguard --version --format json`），再选择命令面。完整对照见 `codeguard` 技能的 `references/operations/engine-contract.md`。

Legacy Python 引擎：

```bash
bin/codeguard detect .
bin/codeguard check .
bin/codeguard check --lang java,python --timeout 60 .
```

Rust 组件（当前对质量路径固定返回未完成）：

```bash
codeguard detect . --format json
codeguard plan check all .
codeguard check all . --format json
```

Rust 侧的 `check` 只接受位置参数 `all|java`，没有 `--lang`；`--timeout` 接受 duration（如 `30m`）而非裸秒数。Rust 组件返回退出码 3，只能表述为局部原生观察或未完成，**不能作为门禁通过结论**。

执行前记录工作目录、当前分支、目标模块和工具版本，并写明结果由哪个引擎签发。若 `bin/codeguard` 不存在，不要猜测命令或声称通过；改用仓库的权威 CI/lint 命令或报告 `UNVERIFIED`。

## 能力边界

### ✅ Strengths

1. 自动检测项目语言，一次跑多语言 lint。
2. 表格化报告每种语言的命令、退出码、耗时和状态。
3. Legacy 下用 `--lang` 和 `--timeout` 缩小故障范围；Rust 下先用 `plan` 看只读计划。
4. 区分代码违规、配置错误、工具缺失、未完成和执行器错误。
5. 为修复与 CI 复现产出结构化证据。

### ⚠️ Prerequisites

1. Codeguard CLI 或对应的源码脚本可用。
2. 对应语言工具链和仓库配置已准备。
3. 执行目录是真实仓库或模块根，而不是任意上级目录。
4. 需要网络或私服的检查已获得明确授权。

### ❌ Out of Scope

1. 自动修复交给 **`codeguard-fix`** 技能。安装：`npx skills add full-stack-skills/codeguard-skills --skill codeguard-fix`。
2. CVE 扫描交给 **`codeguard-cve`** 技能。安装：`npx skills add full-stack-skills/codeguard-skills --skill codeguard-cve`。
3. 不把 lint 通过扩大为编译、测试、安全或发布通过。
4. 不在检查任务中修改 ignore、suppression 或规则阈值。

## 什么时候使用

- 用户要求“跑 lint”、“检查代码规范”或提交前自检。
- CI 报告 Codeguard/linter 失败，需要本地复现。
- 跨语言仓库需要统一结果摘要。
- 需要判断当前状态是 FAIL 还是 UNVERIFIED。

## 不适用范围（什么时候不该用）

- 用户只问语法或框架设计，应使用语言/框架专业技能。
- 主要问题是依赖漏洞、凭据泄露或数据合规。
- 没有仓库上下文却要求证明“整仓全绿”。

## 数据与安全

本技能不收集、上传、发送或存储用户源码与凭据。默认只读执行本地工具；命令可能访问网络、私服或缓存时，必须先说明。报告应对 token、路径中的用户名和业务数据做必要脱敏。

## 命令契约

Legacy Python 引擎：

```bash
bin/codeguard check                        # 全量
bin/codeguard check --lang java,python     # 限定语言
bin/codeguard check --timeout 60 path/     # 指定项目与超时（裸秒数）
```

Rust 引擎（`--lang` 不存在，`--timeout` 用 duration，退出码 3 表示未完成）：

```bash
codeguard check all path/ --timeout 30m --format json
codeguard check java path/ --format json
```

实际 CLI 参数以 `bin/codeguard check --help`（Legacy）或 `codeguard --help`（Rust）为准。技能包只提供操作知识，不假装包含 Codeguard 运行时。

## 状态语义

| 状态 | 证据 | 后续动作 |
|---|---|---|
| `PASS` | 权威检查命令在明确范围内退出 0 | 可报告该 lint 门禁通过 |
| `FAIL` | 工具成功运行并发现违规 | 按格式/规则/配置分类修复 |
| `UNVERIFIED` | 工具、配置、权限、版本、超时或环境不足 | 补齐前置条件，不得写通过 |
| `INCOMPLETE` | 检查按契约未跑完（Rust 引擎退出码 3、必需检查缺失、部分模块未覆盖） | 列出未完成项，**不得写通过**，也不得表述为零违规 |
| `PLANNED` | 注册表仅有识别能力，没有可执行门禁 | 列出待接入工具与验收条件 |

## 标准 Workflow

### Step 1：确定范围

读取仓库指令、检查 Git 状态，确认 monorepo 模块、生成目录、vendor 与子模块。

### Step 2：识别语言

运行 `bin/codeguard detect <path>`，将检测结果与项目标记文件交叉验证。

### Step 3：核对权威命令

读取仓库配置和 CI；若 CI 使用的命令比 Codeguard 默认命令更严格，以 CI 为准。

### Step 4：探测工具

记录 Codeguard 和语言工具版本。`command not found`、配置无法加载或版本不兼容均是 `UNVERIFIED`。

### Step 5：执行只读检查

保存完整命令、工作目录、语言范围、退出码和首个可操作错误。

### Step 6：分类失败

| 类型 | 信号 | 处理 |
|---|---|---|
| 格式 | 缩进、空白、import 顺序 | 可交给受控 formatter |
| 静态规则 | unused、命名、复杂度、危险 API | 最小语义修复 |
| 配置 | schema/parser/config 报错 | 先修复接入，不改代码充数 |
| 环境 | 工具缺失、版本冲突、超时 | 报告前置条件 |
| 工具崩溃 | traceback、panic、解析器异常 | 缩小复现，保留原始证据 |

### Step 7：输出结果

按语言列出 PASS/FAIL/UNVERIFIED/INCOMPLETE/PLANNED，并将 lint、test、build、security 证据分开。

## Rules

1. 工具缺失、超时和配置错误不等于通过。
2. 不使用 `--no-verify`、ignore 或降低阈值来伪造绿灯。
3. 同一个结论必须带命令、范围和退出码。
4. 检查阶段不修改用户文件。
5. 不用一种语言的通过掩盖另一种语言的失败。

## 输出模板

```text
Codeguard check 结果
- 引擎：<legacy | rust>
- 范围：<repo/module/path>
- 检测语言：<list>
- 命令：<actual command>
- 工具：<versions>
- 结果：<language -> PASS/FAIL/UNVERIFIED/INCOMPLETE/PLANNED>
- 发现：<categorized findings>
- 未验证：<test/build/security/platform gaps>
- 未完成：<required checks not run>
```

## Gotchas

1. **错误根目录**：在 monorepo 上级目录执行可能加载错误配置或漏掉模块。
2. **工具自动下载**：Maven/npm 等可能在检查时访问网络；不应把网络失败认作代码失败。
3. **生成文件噪声**：遵循仓库 ignore，不要擅自扫描 vendor 或生成产物。
4. **工具版本漂移**：本地和 CI 版本不同时，本地 PASS 不能预测 CI PASS。
5. **超时语义**：超时是 UNVERIFIED，不是零发现。
6. **编译与 lint 分层**：`compile` 退出 0 不代表 javadoc、style 或安全门禁通过。

## 按需加载资源

- 解释退出码和状态时读取 `references/rules/result-semantics.md`。
- 复现 CI 或设计证据包时读取 `references/operations/check-playbook.md`。
- 需要可复制场景时只打开 `examples/` 中匹配的一个文件。
