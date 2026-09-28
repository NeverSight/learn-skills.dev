---
name: mxcat-commit
description: |
  分析整棵未提交工作树（staged、unstaged、untracked），先出示预览再按逻辑分批提交；仅当用户明确要求合为一条（或不要拆、就提交一条）时走 single。标题用 cz-emoji shortcode 且必写 (scope)，subject 默认简体中文。
  当用户要求：mxcat-commit, commit code, generate commit message, auto commit, 帮我提交, 自动提交, 生成 commit, write commit message, 代码提交, 提交代码, split commits, batch commit，或表达“看看 git 里没提交的代码并分类后分批提交”时使用此技能。
---

# mxcat-commit

## 安装

安装与验证见本技能目录 [README.md](README.md)。

## 默认路由

先看完整工作区：

```bash
git status --short
```

出预览前看一眼：明显是密钥、个人信息、且尚未进入 HEAD 的路径，仍编进预览并提醒。默认分批时细节见 [batch-commit.md](references/batch-commit.md)；合为一条时见 [single-commit.md](references/single-commit.md)。

默认走 **Batch commit**（按逻辑分批）。

- **Batch commit**（默认）：按逻辑拆分当前未提交变更。输入默认是整棵工作树（staged + unstaged + untracked）。用户要求 `split commits` / `batch commit` / 「按逻辑分批提交」时也走这条。即使工作区只剩 staged，只要用户没说「合为一个 commit」，仍默认分批。
- **Single commit**：仅当用户明确要求「合为一个 commit」（或「合成一条」「不要拆」「就提交一条」）。把当前输入范围打成 **一条** commit。输入默认仍是整棵工作树；若用户同时要求「只提交暂存区」，则只用 staged。

判定之后再读对应 guide；未判定前不要展开执行细节。

## 预览门禁

single 与 batch 都先出示预览，等人确认，再提交。确认按**本轮对话里是否已完整输出**预览卡 + 固定收尾来判定，不要靠与阶段无关的词表，也不要因为句子里出现「提交」或「push」就执行。

- 确认前禁止运行 `git commit`（含 `--file`、`-m`、会创建提交对象的 amend）与 `git push`。该次回复只批准提交、未要求 push 时，不要运行 `git push`。提交成功后用户再说「帮我 push」「推一下」或 `git push`，可以对当前上游再推一次（不要 `--force`，没有上游不要擅自 `-u`）。
- **尚未出示预览**（含用户**第一句**就说）：「提交」「帮我提交」「可以提交」「提交并 push」「提交并push」「commit and push」「自动提交」「commit」「split commits」等——一律只分析变更、出示预览与固定收尾，**不等于**确认，**禁止**同轮 `git commit` / `git push`。收尾里举例的「提交并 push」是**预览之后**才有效的确认语，不能反向当成首轮可跳过预览的口令。
- **已经出示预览**（同一轮或上一轮已输出完整预览 + 固定收尾）：这句话的主要动作是下令做 commit（独立的「提交」）才批准，不要求等于「提交」两个字。算批准：「提交」「确认提交」「帮我提交」「提交吧」「那就提交」「好的，提交吧」「可以提交」，以及预览后的 `commit`（不要因此 push）。「提交并 push」视为批准 commit，且全部预定（含点名子集）成功后再 `git push` 一次。不要把单独的「确认」「可以」「好的」「行」「ok」「lgtm」「就这样」当成确认；「可以提交吗」「提交吗」也不算。「不要提交」「先别提交」里的「提交」不是独立的「提交」。
- 点名只提交某几条（「只提交 commit 1」「提交 1 和 3，2 先留着」）当场做被点名的条；没点名的当丢掉：文件留工作区，不要 `git restore` / `checkout` / `reset`，不必再出剩余预览。只说「不要提交 commit N」则重出剩余整单再等；「不要 2，其余提交」当场做剩余。认 `## commit N`；「第一条」对不上就问，不要猜。
- 只改标题、emoji、scope、正文且没说提交：更新预览再等。同一句改这些并含独立的「提交」：按新稿提交，不要再出一轮。拆开、合并、或「合为一条」即使带「提交」也先重出。丢掉的那条对应文件留在工作区。没有剩余条目则停止并说明。
- 仅当用户强调不需要预览（「不需要预览」「跳过预览」「不要预览」）时，才允许跳过预览卡。只说「直接提交」、只给完整标题、或启动语里带「提交」，仍须预览。
- 「合为一条」是改走 single 并重出预览，不是跳过预览。

预览卡至少包含：拟用标题、拟用正文（若有）、以及解释。每条预览用 `## commit N` 起头；编号是身份，丢掉后不滑动，不要写成 `待确认 · 1/N`。解释必须覆盖：为何选该 emoji、为何选该 scope、**改动了哪些部分**。点到模块/文件/行为即可；**改动部分列出的每个文件须用仓库相对路径写在反引号里**（便于跳转到对应文件），需要定位改动行时可用 `` `startLine:endLine:path` `` 代码引用；不要只写裸文件名、不要逐行复述 diff。

全部预览条目之后必须另起一段，**原样**输出下面这句（不得改字、换序或增删分句；不要写进某条的解释里）：

尚未提交 commit 和 push，请回复「提交」「提交并 push」等进行提交、push，也可以合并 commit 或不要提交某个 commit

提交或 push 成功后，按对应 guide 的回执样例汇报，不要临场改结构。同一组字段（`Commit：` / `标题：` / `变更：`，或 `分支：` / `仓库地址：`）写成 Markdown 无序列表，组内不要空行；开头句与工作区句仍是段落。

确认之后，按当前 shell 创建每条 commit：sh、bash、zsh 用本技能目录的 `scripts/commit_one`，Windows PowerShell 用 `scripts/commit_one.ps1`。写法见对应 guide 第 5 步。同一文件要分属多条时，由入口按该条 hunk 提交。

## 默认结果约束

完整标题、语言、footer 禁令与示例以 [commit-convention.md](references/commit-convention.md) 为准。主文档只保留最小硬结果：

### Header

- 允许的标题骨架：
  - `:emoji: (scope) subject`
  - `:emoji: (scope) ! subject`
- Header 中的 emoji 必须使用 shortcode，例如 `:bug:`，不要使用 Unicode emoji。
- `scope` **必写**，必须写成 `(scope)`。
- `!` 是独立的 breaking marker，位于 `(scope)` 之后、subject 之前。
- 默认语言只影响 subject 的描述，不改变 header 骨架。

### Body

- Body 保持 bullet 风格，并尽量简洁。
- Header 和正文之间必须保留一个空行。
- 若存在 footer，正文和 footer 之间必须保留一个空行。
- 未声明时 subject 与 body 使用简体中文；用户本轮明确要求英文时再覆盖。

### Footer

- 禁止输出 `AI-Co-Authored-By:`、`Co-authored-by:`、`Co-Authored-By:`、`Jira-Refs:`。
- 若存在 `BREAKING CHANGE:`，字段名保持英文；其后的描述文本遵循当前语言（默认中文）。

## 何时读取哪份 Reference

| Reference | 何时读取 | 主要内容 |
|---|---|---|
| [single-commit.md](references/single-commit.md) | 已确定当前是 single commit 时 | 分析变更、预览卡、确认后提交、自检、成功回执 |
| [batch-commit.md](references/batch-commit.md) | 已确定当前是 batch commit 时 | 分组、整单预览、按序提交、中途失败、成功回执 |
| [commit-convention.md](references/commit-convention.md) | 需要 canonical 规范时 | header、必写 scope、语言、footer 禁令、完整示例 |
| [cz-emoji-types.md](references/cz-emoji-types.md) | 常用类型不足以覆盖当前语义时 | 完整 emoji 类型表 |
| [troubleshooting.md](references/troubleshooting.md) | 遇到异常或恢复场景时 | 自检失败、hook、空行、push 无上游、丢掉预览后无剩余项 |
