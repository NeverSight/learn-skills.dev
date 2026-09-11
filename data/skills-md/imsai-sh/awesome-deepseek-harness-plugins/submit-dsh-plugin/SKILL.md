---
name: submit-dsh-plugin
description: 验证并提交 DeepSeek Harness 插件到 imsai-sh/awesome-deepseek-harness-plugins 社区目录。适用于插件作者要求收录、发布或提交自己的插件，创建目录 JSON，修复目录提交 PR，或者发起合规 PR。检查公开仓库、dsh-plugin topic、dsh.bundle.patch、作者测试证据、双语元数据和单文件差异，并在获得授权后执行 fork、push 和创建 PR。
---

# 提交 DSH 插件

从插件作者的仓库准备一份聚焦的目录收录 PR。始终把 `catalog/plugins/*.json` 视为贡献者唯一可以编辑的目录源数据。

## 安全与范围

- 不得在插件提交 PR 中编辑 `README.md`、`catalog/README.md`、工作流或脚本。两个 README 是 bot 生成的目录投影，合并后由 CI 自动刷新。
- 不得仅为了检查插件而安装依赖、运行生命周期脚本、构建或执行插件代码。运行作者代码前必须先征得同意。
- 保留所有无关的本地改动。如果目录仓库工作区不干净，应停止操作；除非用户指定一个干净 worktree，或明确界定现有改动的范围。
- 将“准备”或“起草”理解为仅做本地修改。只有用户明确要求“提交”“推送”或“创建 PR”时，才视为已授权在展示准确目标后执行 fork、push 和创建 PR。
- 不得手动合并 PR，也不得修改生成投影。合规的非草稿新增类目录 PR 会在可信静态审查通过后自动合并；修改或删除既有条目的 PR 即使静态审查通过也不会自动合并，必须等待目录仓库维护者人工审核后手动合并。合并进入 `main` 后，CI 自动把目录条目同步到网站数据库（D1）并重新生成两个 README，即自动同步，无任何维护者手工步骤。

## 1. 明确提交信息

确定以下内容：

- 插件 ID：仓库级插件为 `owner/repository`；monorepo 子包插件为 `owner/repository/sub/dir`，前两段之后的路径段指向仓库内的子目录
- 插件名称：仓库级插件通常与仓库名一致，子目录 ID 默认取最后一个路径段（子包目录名）
- 一个主要目录分类
- 客观的英文与中文简介
- 作者实际执行的测试命令和结果

ID 各段仅限 `A-Za-z0-9_.-` 字符，路径段不得是 `.` 或 `..`，总长不超过 201 字符。无论 ID 是否携带路径，条目的 `repository` 字段始终是由前两段推导的仓库根 URL `https://github.com/owner/repository`。ID 的路径段锁定插件源码位置：子目录 ID 的 `<sub/dir>/package.json` 必须恰好是插件的 manifest。安装入口只来自发布到 npm 的包（1024 Store 仅提供 npm 安装），目录条目本身只记录源码仓库。

目录仓库固定使用 `https://github.com/imsai-sh/awesome-deepseek-harness-plugins`。创建文件前，读取其当前 checkout 中的 `CONTRIBUTING.md` 和 `catalog/categories.json`；如果线上仓库规范与本 Skill 不同，以线上规范为准。

选择分类或编写 PR 时，读取 [references/submission-reference.md](references/submission-reference.md)。

## 2. 检查插件仓库

先完成只读检查：

1. 确认仓库公开且存在默认分支。
2. 确认仓库包含 `dsh-plugin` GitHub topic。如果缺少 topic、用户拥有该仓库且已授权外部写入，才可执行 `gh repo edit owner/repository --add-topic dsh-plugin`。topic 作用于仓库本身：`gh repo edit` 的参数只取 ID 的前两段 `owner/repository`，子目录 ID 的路径段不参与。
3. 定位插件的 manifest：两段 ID 可使用根目录或任意嵌套的 `package.json`（排除 `node_modules`）；子目录 ID 则必须在 `<sub/dir>/package.json` 恰好找到 manifest——ID 的路径就是插件在仓库中的位置，仓库里其他位置的 manifest 不算数。
4. 确认其中声明了非空字符串 `dsh.bundle.patch`。
5. 相对于声明该字段的 `package.json` 解析补丁路径；拒绝绝对路径、反斜杠以及跳出仓库的路径。
6. 确认 manifest 和引用的补丁都存在于 GitHub 默认分支，而不只是尚未推送的本地提交。
7. 向作者说明**安装可用性**：1024 Store 只提供 npm 安装，不再提供 GitHub 源码安装。
   网站会自动探测 manifest 中声明的 npm 包名；只要 npm 上的 latest manifest 声明 `dsh.bundle`，插件即可安装（`repository` 回链缺失或不一致不影响验证）。
   **未发布 npm 包不影响收录**：插件照常收录，以浏览模式展示（有仓库链接，无安装命令），PR 评论会提示作者发布 npm 包后目录自动检测、无需追加 PR。
8. 记录作者实际执行的兼容性测试。如果尚未测试，应停止并要求作者先测试；目录自动审查不会执行第三方代码。

使用 GitHub 或 `gh` 获取远程默认分支证据。不得用仅存在于本地的文件作为证明。

## 3. 准备干净的目录分支

优先复用干净的目录 checkout。仅本地准备时，直接克隆上游目录仓库，不创建 fork。已授权正式提交时，使用 GitHub CLI fork 并克隆，或者把用户已有的 fork 添加为推送 remote。保留上游仓库 remote，拉取其默认分支，然后基于完整插件 ID 创建聚焦分支，例如：

```text
add-owner-repository
add-owner-repository-sub-dir
```

子目录 ID 的分支名包含 slug 化的路径段，这样同一仓库的两个子包提交不会撞到同一个分支名。

不得把目录条目放进插件仓库。不得基于另一个尚未合并的贡献分支创建本次分支。

## 4. 创建目录条目

解析本 Skill 目录的绝对路径，然后运行其中的确定性创建脚本：

```bash
node <skill-directory>/scripts/create-catalog-entry.mjs \
  --catalog-root <catalog-checkout> \
  --id owner/repository \
  --category skill \
  --description-en "A factual English description." \
  --description-zh "客观、具体的中文说明。"
```

monorepo 子包传入完整 ID，例如 `--id owner/repository/packages/foo`；脚本会保持 `repository` 为仓库根 URL，并把路径段编入文件名。

仅当展示名称需要不同于默认值（两段 ID 为仓库名，子目录 ID 为最后一个路径段）时传入 `--name`。仅当需要覆盖当天 UTC 日期时传入 `--added YYYY-MM-DD`。

脚本必须拒绝未知分类、重复 ID（不区分大小写，含路径段）、无效 ID 和已存在的目标文件。同一仓库以不同子目录路径提交多个条目是允许的，只要每个完整 ID 唯一。不得绕过这些错误手工创建文件。

## 5. 验证单文件约束

要求当前分支相对上游最新默认分支的完整差异只包含一个新增文件：

```text
A catalog/plugins/<owner>--<repository>.json
```

文件名由完整 ID 推导：每个 `/` 分隔的段转为全小写、把连续非字母数字字符替换成 `-`，再用 `--` 连接。子目录 ID 的路径段同样编入文件名，例如 `owner/repository/packages/foo` → `A catalog/plugins/owner--repository--packages--foo.json`。文件始终平铺在 `catalog/plugins/` 下，不创建子目录。

然后执行以下检查：

1. 再次解析 JSON。
2. 确认文件名与规范化后的 `id` 一致。
3. 确认中英文简介客观、中性、具体，且有仓库证据支持。
4. 确认 `added` 是提交日期。
5. 只暂存该 JSON 文件，并运行 `git diff --cached --check`。
6. 检查暂存差异是否包含凭据、私有路径、邮箱、token 或无关数据。

如果可以针对已提交分支在本地运行目录仓库的可信审查脚本，应传入上游基础 SHA、当前分支 HEAD SHA、作为 `PLUGIN_REVIEW_ROOT` 的目录 checkout，以及已认证的 GitHub token。不得把该静态审查描述成插件运行测试。

## 6. 提交并创建 PR

使用聚焦的提交信息，写入完整插件 ID，例如：

```text
catalog: add owner/repository
catalog: add owner/repository/packages/foo
```

推送前，说明 fork、分支、上游仓库和唯一暂存的文件。只有获得授权后才可推送并创建 PR。

使用 [references/submission-reference.md](references/submission-reference.md) 中的模板编写 PR，填写真实的测试命令和结果，并保持“允许维护者修改”开启。
仓库根 PR 模板只包含插件与目录提交确认清单，逐项如实完成即可。

## 7. 跟进自动检查

创建 PR 后：

1. 返回 PR URL。
2. 检查 `Plugin submission review / static-review` 及其机器人评论。
3. 如果检查失败，PR 会保持打开且不会被工作流自动关闭；仅通过修改目录 JSON 修复。不得为了通过检查而加入 README 或其他生成投影。
4. 非草稿新增类 PR 检查通过后会自动 squash merge，GitHub 随后将其记录为已合并（因此不再保持打开）；草稿 PR 会在标记 ready for review 后重新检查并自动合并。
5. 修改或删除既有条目的 PR 检查通过后，机器人会评论说明需要维护者人工审核；此时无须任何贡献者操作，等待维护者手动合并即可，不要催促或自行合并。
6. 不要请求维护者批准 fork CI，也不要手动合并；目录 PR 不运行贡献者分支上的通用 CI。

静态审查通过即表示该目录元数据符合收录规则；新增类 PR 随之触发自动合并，修改/删除类 PR 则进入维护者人工审核。合并进入 `main` 后，catalog-sync 工作流会自动把条目同步到线上目录数据库并刷新 `README.md` 与 `catalog/README.md`（github-actions[bot] 提交），插件随即出现在 [deepseek1024.com](https://deepseek1024.com/) 与两个 README 目录中。该结果仍不代表对第三方插件行为、安全性或质量的背书。

## 已存在的条目与更新

如果完整插件 ID 已经存在（不区分大小写），不得创建重复条目。唯一性按完整 ID 判断：同一仓库已存在其他条目（例如仓库级条目或另一个子目录条目）并不阻止提交一个新的、不同的 ID。需要修正或下架既有条目时，可以提交只修改或删除对应 `catalog/plugins/*.json` 文件的 PR：静态审查照常运行并逐个校验修改后的条目，但此类 PR 不会自动合并，必须由维护者人工审核后手动合并。提交前应向用户说明这一等待环节。
