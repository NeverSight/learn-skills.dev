---
name: workitem-driven-development
description: '当用户给出 PingCode 工作项编号（形如 #ABC-42）并要求开发、修复、实现、继续任务，或明确要求按 #编号 走分支、提交、开 PR、合并、评审时使用。整合 PingCode 工作项驱动流程、Conventional Commits、squash 合并与 docs/ 文档沉淀，依赖 use-pingcode-cli skill。没有工作项编号的普通任务不要触发。'
---

# 工作项驱动的 Git 工作流

**触发条件**：任务带 PingCode 工作项编号 `#<Identifier>`（如 `#ABC-42`），且用户要求开发、修复、实现、继续、评审或合并。没有编号的普通代码修改不要套用本 skill 的认领、评论、分支命名规则，按仓库自身规范执行。

PingCode 操作全部依赖 **`use-pingcode-cli` skill**：先按它预检 `pc` 与登录，再使用本流程；不要臆造 `pc` 命令或参数。本 skill 只规定流程和 Git/文档规范，API 细节以 `use-pingcode-cli` 为准。

详细子流程、Feature 拆解、提交类型和反模式见 [`reference.md`](reference.md)。

## 硬规则

- 不在集成分支（常见 `develop`/`main`，以仓库实际保护规则为准）直接改文件、提交或推送；一切变更走工作分支 + PR。
- 不主动 `commit` / `push` / 合并 PR；除非用户明确要求。
- 危险操作（`reset --hard`、`restore`、`clean -fd`、`stash drop`、对已推送历史 rebase/amend、任何 `push --force*`）执行前必须说明影响并征得确认；**任何情况下都不对集成分支强制推送**。
- 不声称执行过未实际运行的检查；CI 失败或缺失要如实说明。
- 需要长期保留的文档统一沉淀到 `docs/`，不散落在源码目录、个人笔记或聊天记录里。

## 0. 识别编号与预检

1. 从用户消息提取 `#<Identifier>`，例如 `#ABC-42`。调用 `pc` 时去掉 `#`：`ABC-42`；分支名和 PR 标题保留 `#`。
2. 加载 `use-pingcode-cli`，按它执行 `pc doctor`；退出码非 0 时按失败项修复，不要继续。
3. 用 `pc whoami --json` 确认当前用户：登录名取 `identity.user.name`，用户 ID 取 `identity.user.id`。后续“当前用户”都以此为准。
4. 记录仓库文件夹名，供缓存和临时 worktree 使用：

   ```bash
   REPO_NAME="$(basename "$(git rev-parse --show-toplevel)")"
   ```

## 1. 取工作项详情

```bash
pc pjm workitem get ABC-42
```

- **必须用完整编号 get**，不要用全局 `pc pjm workitem list --identifier <数字>` 取详情；不带 `--project-id` 时会跨项目命中同号工作项，结果有歧义。只有手里只有数字、拼不出完整编号时，才退回 `pc pjm workitem list --project-id <pid> --identifier <n>` 做项目内精确查询。
- 同时拉取评论与附件：
  ```bash
  pc comments list --principal-type workitem --principal-id <工作项id>
  ```
- 记录返回体的 `id`、`project.id`、`type.id`、`state.id`、`assignee.id`、`parent_id`；后续类型/状态解析和写操作都用这些 id。
- `parent_id` 非空时，拉父工作项的标题和描述，理解上层背景。
- 用 `pc pjm workitem list --project-id <项目ID> --parent-id <工作项ID>` 查子项：**先只读标题**掌握全貌，再按需读相关子项详情，不要一次拉全部。
- Feature 拆解时，用 `pc pjm workitem-relation list <工作项ID>` 查关联工作项，按需读取。

## 2. 判断工作项类型

用 `pc pjm workitem-type list-for-project --project-id <项目ID>` 解析项目内真实类型，按名称匹配，不要硬编码类型 id 或 `story`/`bug` 标签。

- **是 Feature / 产品需求**：不要直接认领或开发，转入 [`reference.md`](reference.md) 的「Feature 拆解流程」，先拆出可独立交付的用户故事。
- **不是 Feature**（用户故事、任务、缺陷等执行类工作项）：继续第 3 步。

## 3. 状态与负责人检查

- 状态不是“打开/待处理”类初始状态时，向用户提示并询问是否继续，不自行继续。状态 id 用 `pc pjm workitem-state list-for-project --project-id <pid> --workitem-type-id <type-id>` 解析，按名称识别，不硬编码。
- 已设置负责人且不是当前用户时，向用户提示并询问是否继续。
- 需求、方案、验收标准不明确时**不猜测**，向用户提问直到明确。

## 4. 认领（幂等）

负责人不是当前用户时，把负责人设为当前用户；状态不在“进行中”时，把状态置为进行中。目标值已就位就跳过对应写入，不要对当前状态重复发起流转（会报“工作项状态不能流转到当前状态”）。

```bash
pc pjm workitem update <工作项id> --data '{"assignee_id":"<当前用户ID>"}'
pc pjm workitem update <工作项id> --data '{"state_id":"<进行中状态ID>"}'
```

- 写操作前先读工作项；写后重新 `get` 验证。
- 403/scope 不足时停下交用户处理，不要反复重试。

## 5. 理解、拆分与方案先行

1. 读标题、描述、评论、附件，结合父/子/关联工作项理解验收意图。
2. 工作量较大（跨模块、多阶段、可并行）时，先提示用户是否创建子工作项（类型为任务），用户同意后再创建；再询问是否按顺序逐个领取执行。
3. 先把方案与要改的文件告知用户，**不要落盘**；用户确认后才开始改代码。
4. 沟通中明确的关键结论、范围边界、实施进展、完成总结，及时以**纯文本**评论发到工作项：
   - 用换行分段、`-`/`1.` 列点，不要写 HTML 标签。
   - 需要 @ 人时用 `[@<用户ID>|<登录名>]`（用户 ID 经 `pc organization user list` 解析）；只写 `@登录名` 不会触发提及。
   - 过程信息只留在工作项评论，不在本地另存副本。

## 6. 创建工作分支

按顺序执行，任一步不满足就停下问用户：

```bash
git rev-parse --abbrev-ref HEAD     # 应在集成分支
git status --porcelain              # 应为空
git fetch origin
git pull --ff-only                  # 落后时
git checkout -b '#ABC-42/(feat)user-login'
```

- 分支名格式：`#<Identifier>/(<type>)<kebab-简述>`，如 `#ABC-42/(feat)user-login`、`#ABC-42/(fix)retry-timeout`。
- Identifier 与分支名之间用 `/`，不要用冒号；`#` 可以出现在分支名中。
- 分支名先给用户确认；拿不准时 `git check-ref-format --branch '<name>'` 验证。
- 不在集成分支时不要自行切换；工作区不干净时让用户决定提交、stash 或丢弃。
- 所有修改与提交都在工作分支进行；切换分支需用户确认。

## 7. 提交与 PR

- 提交前运行仓库文档或 CI 定义的验证；按受影响包/模块跑 lint、typecheck、test、build；不能运行要说明原因。
- 只暂存本任务相关文件；提交前看 `git status`、`git diff`。
- commit message 用 Conventional Commits：`<type>[optional scope]: <description>`，如 `feat: #ABC-42 user-login` 的拆分提交可写 `feat(auth): add login form`。
- PR 标题格式：`<type>: #<Identifier> <简述>`，如 `feat: #ABC-42 user-login`。
- 经用户确认再 `git push -u origin <branch>` 并开 PR 到集成分支；PR 描述写清变更、原因、验证、风险与回滚。
- 默认 squash 合并：`gh pr merge <n> --squash --delete-branch`；不用 `--merge`/`--rebase`/`--auto`，不用 `--admin` 绕过保护。
- PR 落后 base（BEHIND）时：`git fetch origin` 后 rebase 到 `origin/<集成分支>`；不要用 `--admin`，也不要把集成分支 merge 进工作分支。rebase 后复跑验证，经用户确认再 `git push --force-with-lease`。
- 合并后确认 PR 为 MERGED，再切回集成分支 `git pull --ff-only` 并删除本地工作分支。

## 8. 合并后收尾

1. 复查工作项状态：**已是完成态（如“已修复”/“已完成”，常由 PR 合并自动化流转）则不要重复设置**，仅核对结果；否则才把状态置为完成态。
2. 无论是否改状态，都追加一条纯文本总结评论：交付内容、验证结果、后续衔接。
3. 不把过程信息另存本地；需要长期保留的经验按第 10 节沉淀。

## 9. Code Review（按需）

对 `#<Identifier>` 或指定 PR 做评审时：

1. 先查工作项状态与评论，确认没有进行中的评审或已有结论；有则停下告知用户，除非用户明确要求重新评审。
2. 先发一条纯文本评论，注明当前用户开始 Code Review 与 PR 地址，作为占用标记。
3. 在系统临时目录建独立只读 worktree，例如 `<临时目录>/${REPO_NAME}-pr<n>`；不要在当前工作区执行 git 或构建操作。
4. 只做代码与规范检查；是否运行 lint/test/构建按仓库评审策略，未运行不要声称运行过，CI 结果引用 PR status checks。
5. 结论只用「通过 / 拒绝 / 不确定」并附理由，交用户选择。
6. PR 侧只发评审意见，不合并、不推送、不改作者分支；工作项侧只评论，不认领、不改状态、不改负责人。
7. 结束移除 worktree 和临时分支。

## 10. 文档分层与信息沉淀

**`docs/` 是唯一的长期文档根目录。** 按主题建子目录：

| 目录 | 内容 |
|---|---|
| `docs/product/` | 产品目标、用户与场景、需求与交互决策 |
| `docs/tech/` | 跨包/跨组件的架构与技术决策，建议 `DESIGN_<主题>.md` |
| `docs/guide/` | 新人上手指南、操作手册、排障手册 |
| `docs/decisions/` | 需要长期保留的决策记录（ADR） |

- 文档解释 why，不复制接口 schema、字段表或代码可推导的事实；接口事实保持单一事实源。
- 每篇设计文档标注状态、上游文档与修订记录；推翻旧结论时追加修订记录，不静默改写。
- 包/模块 `README.md` 只保留最小入口与用法并链接 `docs/`；不要在 `src/` 下建深层 docs 目录。
- 代码行为变化时，同 PR 更新受影响的 `docs/`；文档未同步视为任务未完成。

信息分三类：

| 类型 | 去向 | 是否提交 |
|---|---|---|
| 可再发现的引用数据（ID、名称映射、状态值） | 本机缓存，仅作提示 | 否 |
| 有团队价值的经验、结论、排障套路 | 询问用户确认后写入 `docs/`，走 PR | 是 |
| 任务过程信息（澄清、进展、总结） | 工作项评论 | 否 |

缓存目录**动态使用当前仓库文件夹名**，不要写死：

```bash
REPO_NAME="$(basename "$(git rev-parse --show-toplevel)")"
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/$REPO_NAME"
```

- 按 host 分文件，条目带 `fetchedAt`；默认 TTL 7 天。
- API 实时结果永远优先；引用失效、状态不能流转、ID 找不到时，丢弃条目重新拉取并重试一次。
- 缓存损坏（非法 JSON）时忽略并重建；token、密钥、个人隐私不得写入。
- 收尾时主动盘点是否产生可复用知识，但**写入前必须询问用户**；用户拒绝则不保存，不得静默落盘。
