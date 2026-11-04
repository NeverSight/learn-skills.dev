---
name: codeguard-fix
license: Apache-2.0
description: 对 Codeguard 检出的可逆格式和静态规则问题执行受控自动修复；当用户说自动修复、/fix、格式化修复，或 lint 明确给出 autofix 时使用。先 dry-run/保留基线，审查 diff，并用原命令复验；不自动改业务语义。
compatibility: 需要 Codeguard CLI、对应 formatter/linter 和可写工作树；任何破坏性或大范围修改都必须显式授权。
---

# codeguard fix

## Capability Boundaries

### ✅ Strengths
1. 格式类问题一键修复（各语言 format 命令）
2. `--dry-run` 预览将要执行的修复
3. 只跑 format 工具，不触碰业务逻辑

### ⚠️ Prerequisites
1. 对应 format 工具已安装（同 check）

### ❌ Out of Scope
1. javadoc 缺失等需要"写内容"的修复 → 人工/AI 补写（codeguard-java）
2. 安全豁免（改阈值/删规则）→ 禁止，见 codeguard 主入口门禁规则

## 命令

`fix` 只在 Legacy Python 引擎下存在。Rust `codeguard` 组件当前没有自动修复命令，探测到 Rust 引擎时不要凭空构造 `codeguard fix`。

```bash
bin/codeguard fix --dry-run       # 预览（不实际修改）
bin/codeguard fix                 # 执行修复
bin/codeguard fix --lang python   # 只修 Python
```

引擎判定与两套命令面对照见 `codeguard` 技能的 `references/operations/engine-contract.md`。

## Workflow

1. `bin/codeguard check` 确认失败项
2. `bin/codeguard fix --dry-run` 预览
3. `bin/codeguard fix` 执行
4. `bin/codeguard check` 复扫至全绿
5. `git diff` review 自动修复的改动，确认无业务逻辑变更

## Gotchas

1. `npm audit fix` 可能引入破坏性升级——fix 后必须回归测试
2. `eslint --fix` 只修可自动修复规则；复杂度/unused 需人工

## 不适用范围（什么时候不该用）

- 尚未得到可复现的 lint 失败；先用 **`codeguard-check`** 建立基线。
- 违规涉及业务语义、并发、安全或 API 兼容性；应人工评审。
- 修复需升级依赖、删除文件、改规则或大范围重写；必须另行授权。

## 数据与安全

本技能不上传、发送或存储源码和凭据。修复前先检查 Git 状态并保护用户未提交改动；不允许用 reset/checkout 覆盖现有工作，不允许用 suppression 隐藏失败。

## 标准 Workflow

### Step 1：保存基线

记录失败命令、退出码、工具版本、失败数和 `git status --short`。

### Step 2：分类可修复性

区分格式、确定性静态规则、业务语义、配置和环境问题。只将前两类中明确可逆的项交给自动修复。

### Step 3：预览作用域

运行 `bin/codeguard fix --dry-run [--lang <name>]`，核对将执行的工具、目录和排除范围。

### Step 4：执行最小修复

仅对已授权范围执行 formatter/autofix，不顺手重构、升级依赖或改业务代码。

### Step 5：审查差异

使用 `git diff --stat` 和 `git diff -- <scope>` 查看修复量级。出现生成文件、锁文件或超出范围的修改时停止并报告。

### Step 6：复跑原门禁

使用与基线完全相同的 check 命令复验，不用范围更小的命令替代。

### Step 7：回归验证

执行受影响的测试和构建，分开报告 lint、test 和 build 证据。

## Rules

1. 没有失败基线不自动修复。
2. 每次修复都必须审查 diff 并复跑原命令。
3. 工具缺失时输出 `UNVERIFIED`，不静默安装。
4. 不把修复后 lint PASS 扩大为功能正确。
5. 不修改用户既有未提交内容；重叠文件必须逐块审查。

## 输出模板

```text
Codeguard fix 结果
- 基线：<command / exit / count>
- 授权范围：<paths/languages>
- 修复命令：<actual command>
- 改动：<files and categories>
- diff 审查：<safe / stopped / needs decision>
- 复验：<same command / exit>
- 回归：<tests/build or not run>
```

## 更常见的 Gotchas

1. **formatter 可以重写全文件**：小问题也可产生大 diff，需限定范围。
2. **锁文件漂移**：某些工具会触发依赖解析，不应在格式修复中接受未授权的 lockfile 改动。
3. **生成代码**：应修源模板并重新生成，不直接编辑产物。
4. **语义性 autofix**：unused/import 修复可改变副作用，必须查看规则类型与测试。

## 按需加载资源

- 判定当前引擎与可用命令时读取 **`codeguard`** 技能的 `references/operations/engine-contract.md`。安装：`npx skills add full-stack-skills/codeguard-skills --skill codeguard`。
- 判断是否可自动修复时读取 `references/rules/autofix-boundary.md`。
- 设计分批修复时读取 `references/operations/recheck-playbook.md`。
- 根据用户场景只读取 `examples/` 中的对应示例。
