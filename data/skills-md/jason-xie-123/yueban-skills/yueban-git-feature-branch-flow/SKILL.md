---
name: yueban-git-feature-branch-flow
description: '在带 git submodule 的仓库里按 spec/功能开一条同名分支——父仓库和每个当前维护的 submodule（从 .gitmodules 动态发现，排除 deprecated/ 前缀的历史模块）统一从用户选定的 base 分支（项目实际用的哪条都行，不写死）切出 <change-id> 分支，开发期间用 sync 在多台机器间对齐这个分支（不影响 base 分支本身），提交时编排 yueban-git-commit 按"submodule 先、父仓库后"的顺序逐个提交，收尾时给出合并就绪报告但不自动合并（由用户手动合并/PR），合并完成后可选清理分支。和 yueban-git-safe-sync 的区别：那个管的是当前分支本身的 pull/push，以及"把 base 合进当前分支""对当前分支开 PR"这两个单点动作，这个管的是脱离 base 分支的功能分支全生命周期。**仅显式触发**：只有用户明确输入 `/yueban-git-feature-branch-flow`，或明确点名要用这个 skill 时才调用；用户说"开个分支""切个分支""这个 spec 怎么开发"之类的泛化表述不要自动联想到这里，先按普通 git 操作处理或直接追问，除非用户点名。'
allowed-tools: Bash, Skill, AskUserQuestion
---

# Git Feature Branch Flow（父仓库 + submodule 联动分支）

> ⚠️ **仅手动触发**：只有用户明确输入 `/yueban-git-feature-branch-flow`，或明确点名要用这个 skill 时才执行下面的流程。

## 为什么需要这个 skill

用 git submodule 管理多个当前维护模块的仓库，每个 submodule 日常都签出在同一个约定的分支上（叫什么以项目实际约定为准）。`yueban-git-safe-sync` 保证了"多台机器都在这条分支上直接开发"这种场景下 pull/push 不会把 submodule 切成 detached HEAD——但它假设大家都直接在这条 base 分支上提交，多台机器并发改同一条分支本身仍然容易冲突。

这个 skill 换一种工作方式：**每个 spec/功能都从 base 分支切一条同名子分支去做**（父仓库和涉及的 submodule 各自独立切、靠分支名配对），开发过程中互不干扰 base 分支，做完了人工合并回去。这样多台机器的冲突面从"随时可能撞在一起的 base 分支"缩小到"只在开工/合并这两个时间点需要协调"。

## 适用范围

父仓库 + 每个当前维护的 submodule——从 `.gitmodules` 里排除路径以 `deprecated/` 开头的条目动态发现，**统一处理、不做"这次要不要涉及某个 submodule"的判断**——每次开工所有涉及的仓库都切分支，没实际改动的就是空分支，收尾时怎么处理由用户自己决定。放在 `deprecated/` 之类路径下的历史/冻结模块天然被排除，不参与这套分支流程。

## 核心原则

1. **base 分支可选，由用户在 `start` 时决定**，不写死具体分支名——列出父仓库本地分支，让用户挑，这个选择随后记在每个仓库的 git config 里，`sync`/`finish` 不需要用户重复输入。
2. **所有涉及的仓库统一动作**：`start` 时要么全部切分支成功，要么一个失败全部不做；`sync` 同理，全有或全无。
3. **commit 的实际操作委托给 `yueban-git-commit` skill**，本 skill 只负责编排顺序（`pending` 命令报告谁该先提交），不重新实现 Conventional Commits 生成逻辑或 submodule 脏检测——那些 `yueban-git-commit` 已经做了。
4. **合并收尾必须人工执行**：本地合并还是走 PR、要不要 code review，这些决定权在用户；本 skill 只做前置检查（是否已推送、是否已合并）和报告，不自动执行合并。
5. **任何异常都停下来问用户，绝不自动"修好"**：detached HEAD、未提交改动、本地远程分叉，一律 BLOCKED 报给用户，不自作主张 rebase/合并/强推。

## 怎么用

具体 git 操作都封装在 `scripts/flow.sh`（纯 bash + git plumbing）。子命令：

```bash
scripts/flow.sh branches                       # 只读，列出父仓库本地分支
scripts/flow.sh status                          # 只读，各仓库当前分支/dirty/ahead-behind
scripts/flow.sh start <change-id> <base-branch> # 从 base-branch 切出同名分支
scripts/flow.sh pending <change-id>             # 只读，报告谁有未提交改动、提交顺序
scripts/flow.sh sync <change-id>                # 把各仓库对齐到 <change-id> 的最新状态
scripts/flow.sh finish <change-id>              # 只读，合并就绪报告
scripts/flow.sh finish <change-id> --base <branch>   # base 记录缺失时手动指定
scripts/flow.sh finish <change-id> --cleanup    # 确认已合并后，删除各处的 <change-id> 分支
```

分支名固定用 `<change-id>`——如果项目用 openspec 之类的方式管理变更，建议直接复用对应 change 的目录名（如 `openspec/changes/<change-id>/`），保证父仓库和各 submodule 靠名字配对，同时也方便追溯这条分支对应哪个 change；没有这类约定就用能清楚标识这个 spec/功能的短名字。

### 1. 开工（start）

1. 跑 `scripts/flow.sh branches`，拿到父仓库当前有哪些本地分支。
2. 用 AskUserQuestion 让用户选 base 分支——如果项目里已有一条明显的共享主分支（可从 `git symbolic-ref refs/remotes/origin/HEAD` 或各仓库当前分支推断），把它作为推荐默认选项排第一，除非用户在这轮请求里已经明确说了要基于哪个分支（比如"基于 xxx 开一个新分支"），那就不用再问。
3. 跑 `scripts/flow.sh start <change-id> <base-branch>`。
4. 如果输出 `BLOCKED: ...`（退出码 2）：**不要**自己用别的 git 命令去绕过或"修复"——比如某个仓库当前不在 base 分支上、或者已经存在同名分支。把每条 BLOCKED 原样讲给用户，问清楚想怎么处理，处理完再重新跑。
5. 成功后简要汇报"`<change-id>` 已经在这几个仓库切好了"，不用整段贴脚本输出。

### 2. 开发中提交（pending + 委托 yueban-git-commit）

用户在功能分支上改代码是正常开发过程，不需要这个 skill 介入。但到了要提交的时候：

1. 跑 `scripts/flow.sh pending <change-id>`，看哪些仓库在 `<change-id>` 上有未提交改动，以及给定的提交顺序（submodule 在前、父仓库在后）。
2. 按报告顺序，对每一个 DIRTY 的 submodule：**调用 `yueban-git-commit` skill**，在该 submodule 目录下完成"分析 diff → 生成 Conventional Commits message → 提交 → 推送"。不要绕开这个 skill 自己写 commit 逻辑——它已经处理好了"submodule 本身脏 vs 仅指针变了"这两种情况的区分，也知道不能对脏的 submodule 目录做 `git add -A`。
3. 所有涉及的 submodule 都提交并推送完之后，**最后**对父仓库调用一次 `yueban-git-commit`——这时父仓库工作区应该只剩 submodule 指针变化，它会自动识别出这是指针更新场景，生成类似 `chore: bump <submodule 名字> submodule(s)` 的提交并推送到父仓库的 `<change-id>` 分支。
4. 如果某个 submodule 还没准备好提交（比如改了一半），跳过它即可，不强求每次都所有仓库一起提交。

### 3. 换机器续接 / 日常同步（sync）

1. 跑 `scripts/flow.sh sync <change-id>`。
2. 如果输出 `BLOCKED: ...`：原样报给用户，不要自己 rebase/合并去强行绕过——尤其是"本地和远程分叉"这种情况，需要用户决定怎么处理。
3. 成功后脚本会自动打印一次 `status`，简要汇报即可。

**这个命令绝不会用 `git submodule update`**（带不带 `--remote` 都不用）——那会把 submodule 切成 detached HEAD。全程用 `fetch` + 按分支名 `checkout`/`merge --ff-only`。

### 4. 收尾（finish）

1. 先跑 `scripts/flow.sh finish <change-id>`（不加 `--cleanup`），拿到一份合并就绪报告：每个仓库有没有实际改动（空分支 vs 有 commits）、是否已推送、是否已经合并进本地的 base 分支。
2. 如果某个仓库的报告里出现"no recorded base"，说明这个仓库的 base 分支信息没记录下来（比如 `start` 是在另一台机器跑的，这台机器的 git config 里没有），脚本会退回用该仓库 `origin/HEAD` 指向的分支并提示；如果 `origin/HEAD` 也没设置，脚本会直接 BLOCKED。实际 base 与推断不一致，或被 BLOCKED 时，加 `--base <branch>` 重新跑。base 分支在某个仓库本地不存在（比如名字写错）时同样 BLOCKED，不会当成"空分支"处理。
3. 把报告转述给用户，按这个顺序建议操作（**这几步都是用户手动做，本 skill 不执行**）：
   - 对每个有实际改动的 submodule：把 `<change-id>` 合并/PR 回它自己的 base 分支，推送。
   - 回父仓库：`git add <submodule>` 记录新指针 → 提交（这一步同样可以用 `yueban-git-commit`）→ 把父仓库的 `<change-id>` 合并/PR 回它自己的 base 分支，推送。
   - 空分支（没有实际改动的仓库）要不要合并/删除，由用户自己决定，不用主张。
4. 用户确认上面的合并都做完、推送完之后，如果想清理分支，跑 `scripts/flow.sh finish <change-id> --cleanup`——它会先检查每个仓库的 `<change-id>` 是否真的已经成为本地 base 分支的祖先（即已合并），且 base 分支本身没有领先 origin（避免删掉唯一的远程备份），任何一处没满足就整体 BLOCKED、不删任何分支。**执行清理（删分支）前必须让用户确认**，不要看到报告干净就自动往下跑 `--cleanup`。

## 安全原则（贯穿全部子命令）

1. 任何异常（dirty 工作区、分支缺失、本地远程分叉、base 分支未记录）一律 BLOCKED、原样报给用户，不自作主张修复。
2. 涉及 push、合并、删分支这类会影响远程/其他机器可见状态的操作，执行前必须让用户确认，不能因为检查通过就自动继续。
3. 父仓库 + 各当前维护 submodule 的状态变更是"全有或全无"，不留部分完成的中间态。

## 不在这个 skill 范围内的事

- **实际的合并操作**（本地 `git merge` 还是走 PR、要不要 code review）：`finish` 只做前置检查和报告，合并本身由用户手动执行。
- **commit message 的撰写**：交给 `yueban-git-commit` skill，本 skill 的 `pending` 只负责告诉你该按什么顺序处理哪些仓库。
- **base 分支本身的 pull/push**：那是 `yueban-git-safe-sync` 的职责——如果用户就是想直接在 base 分支上同步（不涉及功能分支），用那个 skill，不要用这个。开发中途想把 base 的新提交合进功能分支，或收尾时想对父仓库+各 submodule 一次性开 PR，可以用 `yueban-git-safe-sync` 的 `merge-base`/`pr` 子命令（需用户显式调用那个 skill），本 skill 不重复实现。
- **`deprecated/` 之类路径下的历史/冻结模块**：不参与这套分支流程（随 `.gitmodules` 动态发现规则自动排除）。
- **新增/删除 submodule、修改 `.gitmodules`**：结构性变更，超出这个 skill 的范围，照常手动处理。
