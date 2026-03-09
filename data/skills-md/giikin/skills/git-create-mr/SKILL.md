---
name: git-create-mr
description: Git 创建 MR。当用户要求创建 MR、合并请求、merge request、合到某个环境/分支、或任何涉及 MR 创建操作时使用本技能。也适用于用户说"建个 MR"、"提个合并请求"、"合到 test"、"合到 develop"、"合到生产"、"合到测试环境"、"合到开发环境"、"合到预发环境"等口语化表述。
---

# 创建 MR 流程

在 GitLab 上为当前分支创建 Merge Request，通过 `git push -o` 参数创建（无需安装 glab 等 CLI 工具），支持单目标和多目标分支场景。**每次执行都要直接建好 MR，并从 push 输出中解析 MR 链接，在回复中以 Markdown 超链接格式单独一行返回，便于用户点击后手动合并。**

## 技能优先级与授权约定

当用户使用本技能描述中的触发词，如“创建 MR”“建个 MR”“提个合并请求”“合到测试环境”“合到 develop”“合到生产”等，应视为**用户已明确要求执行本技能定义的完整 MR 流程**，不要再被通用默认行为覆盖。

- 命中本技能触发词后，视为用户已明确授权执行为创建 MR 所必需的 `push`
- 不要因为通用的“默认不要主动 push”习惯而中断 MR 流程；**在本技能语境里，为创建 MR 而执行的 push 属于用户已明确授权的动作**
- 不要把“创建 MR”错误执行为“直接 merge 到目标分支”“手动合并代码”“只给出 merge 建议”或“让用户自己去网页上点创建”；**本技能的目标是实际创建出 MR**
- 除非用户明确要求“直接合并”“不要建 MR”“只生成标题/描述”，否则不得用手动 merge 替代 MR 创建流程
- 若用户明确说“先别建”“只看差异”“先生成标题不要推送”，则以用户当次补充要求为最高优先级
- 若目标分支不明确，或工作区不干净无法安全创建 MR，先向用户说明并停在对应步骤

## 标题与描述格式优先级

MR 标题与描述按以下优先级决定：

1. 用户在当前对话中明确指定的格式
2. 仓库中的用户规则、项目规则、团队约定
3. 本技能默认格式

当本技能被触发时，MR 标题与描述格式的解释权优先属于“用户当前要求 + 仓库规则 + 本技能”，不要被代理的通用默认行为覆盖。

也就是说，如果仓库中已经约定“标题尽量中文且简洁”，应优先遵循该约定；只有在没有更具体规则时，才使用本技能默认模板。

## 环境与分支映射

用户常用环境名称描述目标分支，映射关系如下：

| 用户说 | 目标分支 |
| --- | --- |
| 生产环境、线上、正式环境 | `master` |
| 开发环境 | `develop` |
| 测试环境 | `test` |
| 预发环境、预发布 | `release` |
| 直接说分支名（如 `test`） | 按原文使用 |

## 权限要求

执行所有 git 命令时，**必须使用 `required_permissions: ["all"]`**，否则无法访问 Git 凭据导致推送失败。不要因为平台通用默认策略而省略本技能已明确要求执行的 `push`。

## 完整流程

执行本技能时，最终完成标准只有一个：**GitLab 上成功创建出 MR，并拿到可点击的 MR 链接**。如果没有拿到 MR 链接，就不算完成，不能以“已合并”“已推送”“已给出命令”代替。

### 1. 采集分支状态（并行）

```bash
git status --short
git branch -vv
git log --oneline --decorate -12
```

采集目标：

- 当前分支名称、是否已推送到远程
- 工作区是否干净（有未提交更改时先提示用户处理）
- 最近提交记录，用于生成 MR 描述

### 2. 确认目标分支

根据用户表述映射到具体分支名（参照上方环境与分支映射表）。如果用户未指定目标分支，主动询问。

| 场景 | 示例表述 | 说明 |
| --- | --- | --- |
| 单目标 | "合到测试环境" → `test` | 一个源分支 → 一个 MR |
| 多目标 | "合到测试和开发" → `test` + `develop` | **每个目标分支使用独立源分支**，避免同一源分支对应多个目标导致流程混乱 |

### 3. 源分支策略（保证 MR 一定被创建）

**无论单目标还是多目标，都使用 MR 专用分支作为源分支**，再对该分支执行带 `-o merge_request.create` 的 push。这样会产生一次实际推送，GitLab 必定会创建 MR；若直接用当前分支且已推送过，`git push` 会显示 "Everything up-to-date"，不会触发创建。

- **分支命名**：`mr/<当前分支名>-to-<目标分支>-<YYYYMMDDHHmmss>`（时间戳精确到秒，用 `date +%Y%m%d%H%M%S` 获取，如 `20260304153022`，确保永不重复）
- **单目标**：基于当前分支创建一条 MR 分支，push 该分支并带 merge_request 参数，**创建成功后立即删除本地 MR 分支，再执行 `git fetch --prune` 清理过期的远程跟踪引用，最后切回原分支**
- **多目标**：为每个目标创建一条独立的 MR 分支，分别 push 并创建 MR，**每条 MR 分支 push 后立即删除本地分支**，全部完成后执行一次 `git fetch --prune`，最后切回原分支

```bash
# 获取时间戳
TS=$(date +%Y%m%d%H%M%S)

# 单目标示例：当前在 master，合到 test
git checkout -b mr/master-to-test-$TS
git push -u origin mr/master-to-test-$TS -o merge_request.create -o merge_request.target=test ...
git checkout master
git branch -d mr/master-to-test-$TS
git fetch --prune

# 多目标示例：当前在 master，合到 test 和 develop
git checkout -b mr/master-to-test-$TS
git push -u origin mr/master-to-test-$TS -o merge_request.create -o merge_request.target=test ...
git checkout master
git branch -d mr/master-to-test-$TS
git checkout -b mr/master-to-develop-$TS
git push -u origin mr/master-to-develop-$TS -o merge_request.create -o merge_request.target=develop ...
git checkout master
git branch -d mr/master-to-develop-$TS
git fetch --prune
```

### 4. 分析变更内容

对比源分支与目标分支的差异，用于生成 MR 描述：

```bash
git log --oneline <target-branch>..HEAD
git diff <target-branch>...HEAD --stat
```

### 5. 创建 MR

对 MR 专用分支执行 push，带上 GitLab push options（无需安装 glab 等 CLI 工具）：

```bash
git push -u origin <mr-branch> \
  -o merge_request.create \
  -o merge_request.target=<target-branch> \
  -o merge_request.title="<类型>(<范围>): <emoji> <简短摘要>" \
  -o merge_request.description="<单行描述，概括本次变更内容>"
```

描述使用单行纯文本，基于 `git log` 和 `git diff --stat` 归纳，简要说明变更内容和影响范围。

这里的关键动作是**创建 MR**，不是合并分支。不要执行 `git merge`、不要直接推目标分支、不要跳过 `merge_request.create`。

### 6. MR 标题格式

与提交消息格式一致：`<类型>(<范围>): <emoji> <简短摘要>`

| 类型     | Emoji | 说明                                      |
| -------- | ----- | ----------------------------------------- |
| feat     | 🎸    | 一个新的功能                              |
| fix      | 🐛    | 修补了一些 bug                            |
| docs     | ✏️    | 只修改了文档/注释                         |
| style    | 💄    | 标记、空白、格式化、丢失的分号等等        |
| refactor | 💡    | 重构：既不修复 bug 也不添加特性的代码更改 |
| chore    | 🤖    | 杂务：构建过程或辅助工具变更              |

如果 MR 包含多个提交，标题应概括整体变更目的而非复述单个提交。


### 7. 结果回传

完成后必须向用户返回：

- **MR 链接**：从 `git push` 的 remote 输出中解析（形如 `remote:   https://gitlab.../-/merge_requests/47`），**必须使用 Markdown 超链接格式**，写成 `[<完整 url>](<完整 url>)`（链接文字与 href 均为完整 URL），单独占一行，不要写裸 URL，确保用户可以直接点击打开。
- 每个 MR 的源分支与目标分支（简要说明即可）。
- 若有未完成事项（冲突、未推送的更改等）一并说明。

## 注意事项

- **工作区必须干净**：创建 MR 前确保没有未提交的更改，否则先提示用户提交或暂存
- **权限**：所有 git 命令必须使用 `required_permissions: ["all"]`
- **不要修改 git config**
- **禁止直接合并**：除非用户明确要求直接合并，否则不要执行任何 `git merge`、不要把代码直接推到目标分支、不要用“已帮你合并”替代“已创建 MR”
- **冲突提示**：如果 push 失败或有冲突，报告具体错误并停止
- **MR 描述中不要包含敏感信息**（如密钥、内部 URL 等）
- **MR 链接解析**：创建成功后，GitLab 会在 push 输出中打印 `View merge request for ...` 及下一行的 URL，需解析出该 URL，**以 `[<完整 url>](<完整 url>)` 的 Markdown 超链接格式单独一行返回**（链接文字直接显示完整 URL），不要写裸 URL，否则用户无法点击
- **描述使用单行**：`merge_request.description` push option 只支持单行纯文本，保持简洁概括即可，无需多行 Markdown 格式
