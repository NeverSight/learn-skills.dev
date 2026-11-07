---
name: codeguard-git-branch
description: 识别并执行 Gitflow、GitHub/GitLab Flow、Trunk-Based、OneFlow 和 Release Flow 的分支命名、流向与合并门禁；当用户要创建、切换、合并、rebase 分支，规划发版，或询问分支规范/gitflow 时使用。先识别仓库现行模型，不编造版本、作者或流向。
license: Apache-2.0
compatibility: 需要 Git 仓库上下文；默认只读识别，未经用户授权不创建/切换分支、不 rebase 或 push。
---

# Git 分支规范（7 种主流模型整合）

## Capability Boundaries

### ✅ Strengths
1. 团队 wiki 规范落地为可执行门禁（正则/命令）
2. 主流风格全覆盖，AI 代写有据可依
3. 与 pre-commit / CI 集成路径明确

### ⚠️ Prerequisites
1. git；部分工具需按安装说明准备（commitlint / pre-commit 框架）

### ❌ Out of Scope
1. 代码内容评审（lint 层面归对应语言技能）
2. commit message 格式 → codeguard-git-commit

依据：PartMe.AI Git 规范 wiki（GitLab 分支规范 / Git 工作流程 / Gitflow / Gitflow+）+ 业界主流实践。七模型总对照见 [references/branch-models-comparison.md](references/branch-models-comparison.md)。

## 一、先识别当前项目用哪种模型

`git branch -r` 特征判定：

| 特征 | 模型 |
|---|---|
| 有 `develop` + `release/*` + `hotfix/*` | **Gitflow / Gitflow+**（有 `test` 分支 = 团队 Gitflow+） |
| 只有 `main`（或 master）+ 大量 `feature/*` 短命分支 | **GitHub Flow** 或 **Trunk-Based**（看分支寿命与 PR 频率） |
| 有 `main` + `production` / `staging` / `pre-prod` 等环境分支 | **GitLab Flow（环境分支式）** |
| 有 `main` + `release/v*` 或 `release/x.y` | **Release Flow** 或 **GitLab Flow（发布分支式）** |
| 有 `env/uat`、`env/production`、`*-stable` | **GitLab 分支规范（团队变体）** |

识别不出时问用户；AI 代建分支必须先按第五节的命名门禁执行。

## 二、七种模型速查

### 1. Gitflow（Vincent Driessen 经典）

```text
master ──────────●──────────●────────   （每合并必打 tag）
                   \        /
develop ──●──●──●──●──●──●──────────
            \       │      \
feature ─────●──────●       \── release ──●──→ master
hotfix（线上 Bug）── 从 master 拉出 ── 合回 master + develop
```

- 长期分支：`master`（只收合并，必打 tag）、`develop`
- 临时分支：`feature/*`、`release/*`、`hotfix/*`
- 流向：feature → develop → release → master；hotfix → master + develop
- 适合：版本发布周期明确、多版本并行维护的产品

### 2. Gitflow+（团队在用变体）

标准 Gitflow 基础上 **增加 test 分支**：

```text
master ← release ← test ← develop ← feature
hotfix → master（同时进 develop，升补丁版本打 tag）
```

- `test ← develop 或测试通过的 feature`；提测走 test 分支
- 团队命名惯例：`feature/{version}_{function}_{author}_{datetime}`
  示例：`feature/1.1.0_video_a_20200806`、`fix/1.1.0_video_upload_bug_alicfeng_20200808`

### 3. GitLab 分支规范（团队变体）

| 分支 | 命名 | 环境 |
|---|---|---|
| 主干 | 与默认分支一致 | — |
| 功能 | `feature/*` | — |
| 发布 | `*-stable` | PROD |
| 环境 | `env/uat`、`env/production` | DEV/TEST/PRE |

- 合并方向限制：目前 **feature/* → 主干**；其余以仓库 MR 设置为准

### 4. GitHub Flow（极简）

```text
main ──●──●──●──●──●──   （main 永远可部署）
         \  /
feature ──●──            （短命分支 + PR 评审 + 合并即部署）
```

- 唯一长期分支 `main`，永远保持可部署
- 一切工作：建分支 → 提交 → 开 PR → 评审 → 合并 → 部署
- 适合：Web 持续部署、小团队、SaaS

### 5. GitLab Flow

GitHub Flow + 以下任一扩展：

- **环境分支式**：`main → staging → production`（代码只向下游流动；紧急修复用 cherry-pick）
- **发布分支式**：`main → release/*`（发版前建发布分支，只进 Bug 修复）
- 核心原则 **upstream-first**：任何修复先合入 main（上游），再向下流到环境/发布分支

### 6. Trunk-Based Development（TBD，主干开发）

```text
trunk/main ──●●●●●●●●●●●●●   （所有人高频直接提交或 <2 天短命分支）
                ↘ feature flag 控制未完成功能
```

- 每人每天至少合并一次到 trunk；分支寿命 **< 2 天**
- 未完成功能用 **feature flag** 隐藏，而非分支隔离
- 配套要求：强自动化测试 + 每次提交可发布
- 适合：CI/CD 成熟、高频发布的团队（Google/Meta 风格）

### 7. OneFlow（现代 Gitflow 替代）

```text
main ──●──────●──────●──────   （唯一长期分支）
         \       \
feature ──●       \── release（可选）──→ main + tag
hotfix ──────────────────→ main + tag
```

- 只有 `main` 长期存在；`develop` 被移除
- feature 从 main 拉出；发版可走 release 分支（可选）或直接从 main 打 tag
- 支持 merge 与 rebase 两种风格（团队二选一并统一）

### 8. Release Flow（Microsoft 风格）

```text
main ──●──●──●────────●──   （一切开发在 main）
            \         \
release/v1.0 ──●←cherry-pick
```

- 发版时从 main 建 `release/v{major.minor}`；Bug 修复在 main 做、cherry-pick 回 release 分支
- release 分支仅存活到该版本停止维护

## 三、分支命名门禁（AI 创建分支必须遵守）

| 模型 | 命名 |
|---|---|
| Gitflow / Gitflow+ | `feature/{version}_{function}_{author}_{datetime}`；`fix/...`；`hotfix/...`；`release/{version}` |
| GitHub Flow / TBD | `{type}/{issue号}-{短描述}`，如 `feature/128-user-auth`、`fix/305-null-check` |
| GitLab 分支规范 | `feature/*`、`*-stable`、`env/{name}` |
| Release Flow | 功能同 TBD；发布 `release/v{major.minor}` |

AI 代建分支规则：
1. 先 `git branch -r` 识别模型，再按上表命名
2. 需要 author/datetime 时从用户或 git log 获取，**不得编造**
3. version 取 `git describe --tags --abbrev=0` 或用户指定

## 四、合并方向门禁

| 模型 | 门禁 |
|---|---|
| Gitflow / Gitflow+ | master ← 仅 release/hotfix（必打 tag）；feature → develop；develop → test（Gitflow+） |
| GitHub Flow | feature → main；main 永远可部署 |
| GitLab Flow | 只向下游：main → staging → production；upstream-first |
| TBD | 短命分支 → main；直接 push 需团队约定 |
| OneFlow | feature → main；release → main；hotfix → main |
| Release Flow | 开发全在 main；release/* 只收 cherry-pick |
| GitLab 分支规范 | feature/* → 主干 |

## 五、合并策略（merge vs squash vs rebase）

| 策略 | 历史 | 适用 |
|---|---|---|
| **Merge commit**（`--no-ff`） | 保留分支全貌 + 合并节点 | Gitflow 系（团队默认）；master 合并 |
| **Squash merge** | 压成单提交 | GitHub Flow / TBD（保持 main 一提交一功能） |
| **Rebase + fast-forward** | 线性历史 | OneFlow / TBD；feature 内部同步上游 |

AI 规则：先看项目既有历史（`git log --oneline --graph -20`）识别惯例；不确定时问用户，**不得**擅自 rebase 已推送的共享分支。

## 六、通用工作流习惯

1. 高频细粒度提交；完成即提交，便于定位问题与解冲突
2. 提交前自测/单测通过
3. 有改动至少一天一提交
4. feature 合并后删除分支（谁的分支谁删）
5. hotfix 必须同时回灌主干与开发线，并升补丁版本打 tag
6. master/main 每次发版合并必打 tag，tag 信息写明更新内容

## 七、AI 行为清单

- [ ] 建分支前：识别模型 → 按对应命名格式创建
- [ ] 合并前：确认方向在门禁表内；master/main 合并确认版本号与 tag 计划
- [ ] rebase 前：确认分支未被他人拉取
- [ ] 严禁：直接向 master/main 提交（除非 TBD 且团队允许）；跨模型混用命名；发布分支收 feature 新功能

## 不适用范围（什么时候不该用）

- 只需编写 commit message，转交 **`codeguard-git-commit`** 技能。
- 仓库已有明确模型，但用户要求更换团队工流；这是治理决策，不应由技能擅自完成。
- 目标是已推送的共享历史，却没有团队确认与恢复计划。

## 数据与安全

默认只读取本地 Git 元数据，不收集、上传、发送或存储源码和凭据。创建/切换分支、rebase、merge、push 和 tag 都是独立写操作，必须在用户授权与范围内执行。

## 证据化 Workflow

### Step 1：读取仓库规则

查看 AGENTS/CONTRIBUTING/团队文档、默认分支、保护规则和发布配置。

### Step 2：识别现行模型

使用远程分支、最近历史和发布分支作为证据；无法唯一判定时列出候选与差异。

### Step 3：校验命名输入

从 issue、tag、Git 配置或用户获取 version/author/description，不编造缺失值。

### Step 4：检查流向和历史安全

确认 source/target 符合模型，并在 rebase 前确认分支未被共享。

### Step 5：输出计划或执行已授权动作

报告模型、证据、命名、流向、合并策略和恢复方法。

## Gotchas

1. **存在 develop 不一定是 Gitflow**：需同时核对 release/hotfix 流向。
2. **环境分支可能禁止回流**：GitLab Flow 的代码通常只向下游环境流动。
3. **rebase 会改写 SHA**：已共享分支不得擅自 rebase/force-push。
4. **squash 会丢失细粒度历史**：适用性取决于团队审计与回滚策略。
5. **tag 不是自动结论**：版本号与签名要求必须来自仓库规则。
6. **worktree 和子模块有独立状态**：不要用外层分支推断内层仓库。

## 按需加载资源

- 比较模型时读取 `references/branch-models-comparison.md`。
- 决策或交接时读取 `references/rules/decision-contract.md` 与 `references/operations/evidence-playbook.md`。
- 只打开 `examples/` 中匹配当前任务的示例。
