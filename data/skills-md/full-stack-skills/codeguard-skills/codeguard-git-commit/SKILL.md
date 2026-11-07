---
name: codeguard-git-commit
description: 根据已暂存差异和仓库历史起草、校验 Conventional Commits、Gitmoji 或 Udacity 风格的提交信息；当用户要写 commit message、执行 git commit、设置 commitlint 或询问提交规范时使用。不凭对话编造改动，不用 --no-verify 绕过门禁。
license: Apache-2.0
compatibility: 需要 Git 仓库和可读的 staged diff；默认只生成/校验文案，不自动提交、推送或改写历史。
---

# Commit 日志规范（三种主流风格整合）

## Capability Boundaries

### ✅ Strengths
1. 团队 wiki 规范落地为可执行门禁（正则/命令）
2. 主流风格全覆盖，AI 代写有据可依
3. 与 pre-commit / CI 集成路径明确

### ⚠️ Prerequisites
1. git；部分工具需按安装说明准备（commitlint / pre-commit 框架）

### ❌ Out of Scope
1. 代码内容评审（lint 层面归对应语言技能）
2. 分支命名与合并方向 → codeguard-git-branch

依据：PartMe.AI Commit 日志规范（Angular 正则）+ 业界主流实践。深度对比见 [references/commit-style-comparison.md](references/commit-style-comparison.md)。

## 一、先识别项目现有风格

`git log --oneline -20` 看团队习惯：多数提交形如 `feat(x): y` 用 **Conventional**；带 `✨`/`🐛` emoji 用 **Gitmoji**；首行 50 字左右空行后正文用 **Udacity**。识别不出按 Conventional（团队 wiki 钦定）执行。

## 二、Conventional Commits（团队钦定，事实标准）

### 格式正则（门禁）

```text
^(feat|fix|docs|style|refactor|test|chore|ci)((.+))?: .{1,100}
```

配套校验脚本：`linters/git/commit-msg`（兼容半角/全角冒号、冒号后空格可选、Gitmoji 前缀剥离）。

### 三要素

| 要素 | 说明 |
|---|---|
| **type** | fix / feat / test / style / docs / refactor / chore / ci（+ 业界常用 perf、revert） |
| **scope** | 影响范围：模块、类库、方法（可省略） |
| **subject** | 简短描述 ≤60 字；关联 Bug ID 建议注明 |

### 完整 type 对照（Conventional Commits 1.0.0）

| type | 含义 | 版本语义 |
|---|---|---|
| `feat` | 新功能 | MINOR +1 |
| `fix` | Bug 修复 | PATCH +1 |
| `perf` | 性能优化 | PATCH +1 |
| `refactor` | 重构（不改行为） | — |
| `style` | 格式/注释（不改逻辑） | — |
| `test` | 测试 | — |
| `docs` | 文档 | — |
| `build` | 构建系统/依赖 | — |
| `ci` | CI 配置 | — |
| `chore` | 杂务 | — |
| `revert` | 回滚 | — |

（`feat`/`fix` 后加 `!` 或 body 含 `BREAKING CHANGE:` 表示破坏性变更 → MAJOR +1）

### 示例

```text
fix(首页模块)：修复弹窗 JS Bug
feat(美团对接)：新增门店 OAuth 授权链接生成
refactor(token)!: 双轨刷新合并为单一入口（升级需重配 cron）
docs(readme)：补充三端安装说明
```

## 三、Gitmoji（emoji 前缀风格）

形如 `:emoji: subject` 或直接 unicode emoji。常用对照：

| emoji | 含义 | 对应 conventional |
|---|---|---|
| ✨ `:sparkles:` | 新功能 | feat |
| 🐛 `:bug:` | 修 Bug | fix |
| 📝 `:memo:` | 文档 | docs |
| 🎨 `:art:` | 格式/结构 | style/refactor |
| ⚡ `:zap:` | 性能 | perf |
| ♻️ `:recycle:` | 重构 | refactor |
| ✅ `:white_check_mark:` | 测试 | test |
| 🔧 `:wrench:` | 配置/杂务 | chore |
| 👷 `:construction_worker:` | CI | ci |
| 🔥 `:fire:` | 删代码/文件 | — |

**codeguard 规则**：Gitmoji 可作前缀（脚本会自动剥离后按 Conventional 校验），如
`✨ feat(美团对接)：新增授权链接生成`——emoji + type 双写，机器可读 + 人类直观。

## 四、Udacity 风格（长描述型）

```text
首行：变更摘要（≤50 字符，祈使句）

正文：解释 what 与 why（而非 how），每行 ≤72 字符。
      可分段说明动机、方案对比、副作用。
```

适合：复杂重构、架构变更等需要向未来读者解释决策的提交。团队日常迭代不强制。

## 五、Workflow（AI 代写提交的标准顺序）

1. `git diff --cached` 看实际改动
2. 按 `git log --oneline -20` 识别团队风格
3. 起草 message（type + scope + subject）
4. 过 `linters/git/commit-msg` 门禁
5. 提交

## 六、工具化

- 门禁脚本：`linters/git/commit-msg`（pre-commit 模板已预置 `stages: [commit-msg]`）
- commitlint（Node 项目）：
  ```bash
  npm install --save-dev @commitlint/cli @commitlint/config-conventional
  echo "module.exports = { extends: ['@commitlint/config-conventional'] };" > commitlint.config.js
  ```
- 手动启用 hook：`cp linters/git/commit-msg .git/hooks/commit-msg && chmod +x .git/hooks/commit-msg`

## 六、AI 代写 commit 的规则

1. 先 `git diff --cached` 看**实际改动**，不凭对话记忆编造
2. type 按改动实质选择；混合改动拆分提交或取主导类型
3. scope 与项目既有 commit 风格一致（`git log --oneline -20` 参考）
4. subject 说清「做了什么」，禁止 `update` / `fix` 等空泛词
5. 提交者与作者邮箱必须使用已验证邮箱
6. 不确定时问用户，**不得**用 `--no-verify` 绕过门禁

## 不适用范围（什么时候不该用）

- 只要求设计分支模型或合并策略，转交 **`codeguard-git-branch`** 技能。
- 没有 staged diff 却要求根据对话直接生成并提交。
- 需要 amend、rebase 或重写已推送历史，但未确认影响范围。

## 数据与安全

默认只读取 staged diff 和本地提交元数据，不收集、上传、发送或存储源码与凭据。提交信息不得包含 token、密码、客户个人数据或未公开漏洞细节。

## 证据化 Workflow

### Step 1：检查 staged 范围

运行 `git diff --cached --stat` 和 `git diff --cached`，确认没有凭据、生成噪声或互不相关改动。

### Step 2：识别仓库风格

读取近期提交、commitlint/hook 配置和 CONTRIBUTING，不把外部风格强加给已有项目。

### Step 3：分类改动

依实际 diff 选择 type/scope；混合无关改动时建议拆分提交。

### Step 4：起草 message

写出简明 subject；对复杂变更补充 what/why、风险和 breaking change。

### Step 5：运行门禁

用仓库现有 commit-msg/commitlint 校验。失败应修正 message，不用 `--no-verify`。

## Gotchas

1. **unstaged 改动不属于当次提交**：不应写入 subject/body。
2. **纯格式不等于 refactor**：遵循项目对 `style` 和 `refactor` 的语义。
3. **breaking change 不能隐藏**：需用 `!` 或 `BREAKING CHANGE:` 并说明迁移。
4. **机器生成文件可掩盖主体变更**：scope 应描述逻辑所属模块。
5. **Gitmoji 支持需以仓库历史为准**：不因个人偏好擅自添加。
6. **验证邮箱与签名是独立门禁**：message 合规不代表身份或 GPG/SSH 签名合规。

## 按需加载资源

- 比较风格时读取 `references/commit-style-comparison.md`。
- 决策或交接时读取 `references/rules/decision-contract.md` 与 `references/operations/evidence-playbook.md`。
- 只打开 `examples/` 中匹配当前任务的示例。
