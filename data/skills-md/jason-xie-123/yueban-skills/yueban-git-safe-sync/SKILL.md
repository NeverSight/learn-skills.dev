---
name: yueban-git-safe-sync
description: '在带 git submodule 的仓库里执行 pull、push、把 base 分支合并进当前分支、或对父仓库+全部 submodule 开 GitHub PR，保证每个当前维护的 submodule（从 .gitmodules 动态发现，排除 deprecated/ 前缀的历史/冻结模块）始终停留在其原有分支上（具体叫什么以项目实际约定为准），绝不因为这些操作而把 submodule 变成游离 HEAD（detached HEAD）或强制签出到父仓库记录的 SHA。pull/push 适合"在多台机器上跑同一套项目、submodule 分支状态必须跨机器保持一致"的场景；merge-base/pr 适合"当前在一条从 base 切出的功能分支上，要把 base 的新提交合进来，或者要把这条分支开 PR 合回 base"的场景。**仅显式触发**：只有用户明确输入 `/yueban-git-safe-sync`，或明确说要用这个 skill 时才调用；用户只是随口说"pull 一下""push 一下""同步一下代码""合并一下 develop""开个 PR"这类泛化表述，不要自作主张联想到这个 skill——先按普通 git 操作处理或直接追问，除非用户点名。'
allowed-tools: Bash
---

# Submodule 安全同步（pull / push / merge-base / pr）

> ⚠️ **仅手动触发**：只有用户明确输入 `/yueban-git-safe-sync`，或明确点名要用这个 skill 时才执行下面的流程。普通的"帮我 pull/push 一下"不要自动联想到这里。

## 为什么需要这个 skill

用 git submodule 管理多个当前维护模块的仓库（哪些 submodule 算"当前维护"，从 `.gitmodules` 里排除路径以 `deprecated/` 开头的条目动态判断——项目如果没有这个约定，就是全部 submodule 都算）。每个 submodule 平时都签出在一个具体分支上（叫什么以项目实际约定为准），而不是 git submodule 的默认状态。

如果项目里存在已停止维护、冻结在某个分支上只作历史参考的 submodule（放在 `deprecated/` 之类的目录下），这类 submodule 天然被上面的动态发现规则排除，不需要本 skill 的"保持分支不掉 detached HEAD"这套保护逻辑，pull/push 时按普通只读参考对待即可——具体某个 submodule 为什么被冻结、后续要不要读它做同步比对，是项目自己的业务判断，不属于本 skill 关心的范围。

风险在于：git 处理 submodule 的默认命令是"按父仓库记录的 SHA 签出"，而不是"按分支拉取"：

- `git submodule update`（以及开了 `submodule.recurse` 之后 `git pull` 隐式触发的那次 update）会把每个 submodule 签出到父仓库索引里记录的那个 commit —— **这个操作本身就会把 submodule 切成 detached HEAD**，哪怕现在正停在某个分支上。
- 父仓库记录的 submodule 指针经常落后于 submodule 自己分支的最新提交（这是正常现象：你在一台机器上给某个 submodule 提交了新代码，还没来得及回到父仓库 `git add` 记录新指针）。如果直接 `git push` 父仓库而 submodule 的提交还没 push 到它自己的远程，另一台机器 pull 下来后会指向一个远程都没有的 commit。

用户同时在家和公司两台电脑上跑全部功能，一旦某个 submodule 在其中一台变成 detached HEAD 或指向了本地才有的 commit，另一台机器上跑起来的代码版本就对不上，且不容易第一时间发现。这个 skill 就是为了在 pull/push 时主动规避这两类问题。

同样的"不假设、不代劳、异常就停下"的原则，也适用于另外两个场景：从 base 分支切出的功能分支需要跟进 base 的新提交（`merge-base`），以及功能分支做完了要开 GitHub PR 合回 base（`pr`）。这两个都是对"父仓库 + 全部当前维护 submodule"统一生效的操作，理由同上——一条功能分支往往横跨父仓库和几个 submodule，逐个仓库手动重复同一套 merge/PR 步骤既繁琐又容易漏掉某个仓库。

## 核心原则

1. **submodule 的分支永远是唯一真相来源，父仓库记录的 SHA 只是一个滞后的快照。** 更新 submodule 时按分支 `fetch` + 快进（fast-forward），绝不按 SHA 签出。
2. **遇到任何异常都停下来问用户，绝不自动"修好"。** 包括：submodule 已经处于 detached HEAD、有未提交的改动、本地分支与远程分支出现分叉（既有本地独有提交又落后远程）。这些都是需要人来决定怎么合并/变基的场景，脚本不会替用户做这个决定。
3. **push 之前，先把每个 submodule 自己的提交推到它自己的远程分支，再推父仓库。** 顺序反过来就会出现父仓库记录了一个远程还没有的 commit。
4. **一次同步操作对所有 submodule 是"全部可以就全部做，有一个卡住就全部不做"**，不会出现部分 submodule 已经变了、另一些还没变的中间状态。这一条对 `pull`/`push`/`pr` 严格成立（它们的"能不能做"在动手前就能查清楚，查完再统一动手）；对 `merge-base` 只在预检阶段成立——合并冲突只有真的执行合并才能发现，所以 `merge-base` 遇到冲突时会停在那个仓库、如实报告"这之前的仓库已经合完了、这个冲突了、后面的没碰"，而不是假装整体原子。
5. **`pr` 开 PR 前必须让用户看到标题/描述再确认**：标题/描述从 commit history 自动生成，但创建 PR 是对外可见、别人能看到的操作，跟 push 一样不能因为检查通过就自动执行——先用 `--dry-run` 出计划，用户确认后再真正创建。

## 怎么用

具体的 git 操作都封装在 `scripts/sync.sh` 里（纯 bash + git plumbing，确定性强，不需要每次重新推理怎么写 git 命令）。五个子命令：

```bash
scripts/sync.sh status        # 只读，展示每个 submodule 当前分支/是否 dirty/ahead-behind
scripts/sync.sh pull          # 安全 pull
scripts/sync.sh push          # 安全 push
scripts/sync.sh push --dry-run   # 只打印计划，不实际推送

scripts/sync.sh merge-base <base-branch>            # 把 origin/<base-branch> 合并进父仓库+全部 submodule 各自的当前分支
scripts/sync.sh pr <base-branch>                     # 对父仓库+全部 submodule 开 PR，head=当前分支，base=<base-branch>
scripts/sync.sh pr <base-branch> --dry-run           # 只打印每个仓库的 PR 标题/描述计划，不实际创建
scripts/sync.sh pr <base-branch> --draft             # 创建为 draft PR
```

`pull`/`push`/`status` 三个针对的是"当前签出的分支本身要不要跟它自己的远程同步"，不关心这条分支是不是 base 分支；`merge-base`/`pr` 针对的是"当前分支要不要吸收 base 分支的新提交"或"当前分支要不要开 PR 合回 base"，`<base-branch>` 由用户指定（比如 `develop`），脚本假定父仓库和各 submodule 里这个分支名一致——这是本项目一直以来的约定（父仓库和 submodule 统一走 `develop`/`main`），不是脚本硬编码某个具体分支名。

### 判断用户想做哪个操作

用户调用 `/yueban-git-safe-sync` 时可能直接说明意图（"我要 pull"/"我要 push"/"把 develop 合进来"/"开 PR"），也可能什么都不加。按下面顺序判断：

1. 用户消息里明确提到 pull（拉取/同步最新代码/换了台机器）、push（推送/提交上去/同步给另一台机器）、merge-base（把 base 分支的新提交合进当前分支）或 pr（开 PR 合回 base），就按对应模式走。
2. 都没提到：先跑 `scripts/sync.sh status`，看当前是 ahead（有本地未推送的提交，倾向于 push 场景）还是 behind（远程有新提交，倾向于 pull 场景），据此提出一个判断并跟用户确认，而不是自己悄悄二选一执行有副作用的操作。merge-base/pr 需要一个 base 分支名，用户没提就不要主动推断成这两个操作。

### pull 流程

1. 运行 `scripts/sync.sh pull`。
2. 如果它输出了 `BLOCKED: ...`（退出码 2）：**不要**尝试自己用别的 git 命令去强行绕过或"修复"这个 submodule（比如手动 checkout、reset、rebase）。把每一条 BLOCKED 原样讲给用户听，问清楚想怎么处理，处理完再重新跑一遍。
3. 成功后脚本会自动打印一次 `status`，确认所有 submodule 仍然停在原来的分支上——把这个结果简要汇报给用户即可，不用整段贴输出。

### push 流程

1. 先运行 `scripts/sync.sh push --dry-run`，看计划里哪些 submodule 有待推送的提交、父仓库是否也需要推送。
2. 把这个计划 summarize 给用户看（比如"某个 submodule 有 2 个提交要推，其余 up to date，父仓库也要推 1 个提交"），**推送属于会影响远程/对方机器可见的操作，执行前要让用户确认**，不要看到 dry-run 干净就直接自动继续推。
3. 用户确认后，再运行不带 `--dry-run` 的 `scripts/sync.sh push` 真正执行。
4. 如果出现 `BLOCKED`，处理方式同 pull：原样反馈给用户，不自作主张强推（脚本本身也不会做 force push——分叉的情况会直接 BLOCKED，需要用户先手动 pull/rebase）。

### merge-base 流程（把 base 分支的新提交合进当前分支）

用户场景："我基于 develop 切了个分支，develop 后来又有新提交，把这些新提交合到我这条分支上。"

1. 确认要合并的 base 分支名（用户没说清楚就问一句，比如"develop"），运行 `scripts/sync.sh merge-base <base-branch>`。
2. 脚本会先对父仓库和每个 submodule 做预检（当前分支非 detached、无未提交改动、`origin/<base-branch>` 能 fetch 到），预检有任何 `BLOCKED` 就整体不动手，原样把 BLOCKED 内容讲给用户、问清楚怎么处理。
3. 预检通过后逐个仓库执行 `git merge origin/<base-branch>`。如果某个仓库合并冲突，脚本会在**那个仓库**停下并报告 `BLOCKED`，同时说明这之前哪些仓库已经合并成功、后面的仓库完全没碰。**不要**自己用 `git merge --abort`、手动 resolve、或者跳过冲突仓库继续处理其它仓库——把冲突信息原样转达给用户，问清楚想怎么解决冲突（自己 resolve 再 commit，还是 abort 放弃这次合并），处理完再重新跑一遍命令去处理剩下的仓库。父仓库最先合并，它的冲突常常落在 submodule 指针（gitlink）上：这类冲突脚本会额外提示"用 `git add <submodule-path>` 记录该 submodule 当前 HEAD"，同样转达给用户、由用户决定，不要代为执行。
4. 全部成功后脚本只会在本地完成合并，**不会自动 push**——提醒用户接下来想同步给远程/另一台机器就跑 `scripts/sync.sh push`，想直接开 PR 就跑 `scripts/sync.sh pr <base-branch>`。

### pr 流程（对父仓库 + 全部 submodule 开 PR）

用户场景："这条功能分支做完了，帮我开 PR 合回 develop。"

1. 确认 base 分支名，先运行 `scripts/sync.sh pr <base-branch> --dry-run`。
2. 脚本会对父仓库和每个 submodule 做预检：当前分支非 detached、无未提交改动、当前分支已经和它自己的 `origin/<分支>` 完全同步（不多不少）、`gh` 能从该仓库的 remote 解析出对应的 GitHub 仓库（remote 不是 GitHub 或没有权限会 BLOCKED）。**任何仓库有未推送或落后的提交都会 BLOCKED**，提示先跑 `scripts/sync.sh push`（或 `pull`）——这是为了保证 PR 里看到的内容和本地看到的完全一致，不会出现"本地改了但 PR 没体现"或反过来的情况。同理，父仓库里有未提交的 submodule 指针更新（submodule 已经前进、父仓库还没 commit 新指针）也会 BLOCKED，否则父仓库的 PR 引用的还是旧的 submodule commit。
3. 通过预检的仓库会打印一个 `PLAN`：目标仓库、`<当前分支> -> <base-branch>`、自动生成的标题和正文预览（正文是这条分支相对 `origin/<base-branch>` 的 commit 列表；只有一个 commit 时标题就用那条 commit message，多个 commit 时标题用分支名）。这条分支已经有 open 状态 PR 的仓库会标成 `SKIP` 并带上已有 PR 链接，不会重复开（同一分支以前开过、已经 merged/closed 的 PR 不算，会照常计划新开）；相对 base 没有新 commit 的仓库同样 `SKIP`。
4. **把这份 PLAN 转述给用户确认**（标题、正文、涉及哪些仓库），确认没问题再运行不带 `--dry-run` 的同一条命令（需要 draft PR 就加 `--draft`）真正创建。这一步依赖 `gh` CLI 且要求本机已 `gh auth login`；`gh` 不存在或没登录会在预检阶段就 `BLOCKED`。
5. 父仓库的 PR 里记录的 submodule 指针，指向的是各 submodule **功能分支**上的 commit。如果 submodule 的 PR 之后用 squash/rebase 方式合并、再删掉功能分支，这些 commit 就不在任何分支上了——这种情况下提醒用户：submodule PR 合并后，要在父仓库里把指针更新到 base 分支上的新 commit，再合并父仓库的 PR。
6. 如果某个仓库 `gh pr create` 失败，脚本会停下并报告"这之前已经开了哪些 PR、这个失败了、后面的仓库没创建"，不会自动重试或用不同参数硬凑一次创建。把失败信息和已创建的 PR 列表都转达给用户。

## 不在这个 skill 范围内的事

- 给 submodule 里的实际代码改动做 commit（脚本只处理"已经 commit 好、要不要 pull/push/merge/PR"这一层，不会替用户想 commit message 或决定要不要提交某些文件改动；commit 本身用 `yueban-git-commit` skill）。
- 已停止维护、放在 `deprecated/` 之类路径下的历史 submodule：不参与"跨机器保持分支一致"的诉求，`scripts/sync.sh` 已经把它们排除在外（通过过滤 `.gitmodules` 里 `deprecated/` 开头的路径）。
- 新增/删除 submodule、修改 `.gitmodules`：这些是结构性变更，超出"安全同步"的范围，照常手动处理。
- **功能分支的全生命周期管理**（从 base 切分支、多机器间对齐这条功能分支本身、收尾报告、清理分支）：那是 `yueban-git-feature-branch-flow` 的职责。这个 skill 的 `merge-base`/`pr` 只做两个具体动作——"把 base 的新提交吸收进当前分支"和"把当前分支开 PR 合回 base"，不管这条分支是怎么切出来的、要不要清理，也不像 `yueban-git-feature-branch-flow` 那样把父仓库和各 submodule 按同一个 `<change-id>` 分支名配对（`merge-base`/`pr` 只要求每个仓库当前分支各自跟自己的 base 分支比较，不关心各仓库当前分支叫什么名字）。两者可以配合使用，也可以单独用：只是想让当前分支追上 base、或只是想开个 PR，不需要先跑一遍 `yueban-git-feature-branch-flow`。
- **合并到 base 之后的收尾**（PR 被 review、合并进 base、之后要不要删分支）：这些是 GitHub 上人工评审和合并的过程，本 skill 不介入，也不会去检查 PR 的 review/合并状态。
