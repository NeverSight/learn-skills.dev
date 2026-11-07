---
name: pdlc-ship
description: 发布工作流（收评审通过的功能 → 跑测试 → bump VERSION → 更 CHANGELOG → tag）
argument-hint: "[--version <x.y.z>] [--skip-tests (仅 hotfix)] | --tag-after-merge [v<x.y.z>]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
layer: 2
stage: ship
produces:
  - VERSION
  - CHANGELOG.md
  - docs/05_deployment/releases/v<version>-release-notes.md
  - .git/refs/tags/v<version>
requires:
  - docs/.pdlc-state/
next_step: pdlc-deploy
terminal_state: ship_done
---

# 发布工作流

串联发布一个版本所需的所有步骤：收评审通过的功能 → 跑测试 → 升级 VERSION → 更新 CHANGELOG → 写发布说明草稿 → 创建 tag。CI 配置默认不动（见 §1.6）。

<!-- @include templates/prompts/iron-law.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁**

以下规则为**不可协商**的执行约束：

1. **文件必须落盘**：所有带编号（功能ID / 缺陷ID）的文档，必须作为实际文件写入磁盘，不可仅在对话中输出。
2. **阶段必须落章**：每个阶段完成后必须在状态机 `docs/.pdlc-state/<feature-id>.json` 追加 history，不可跳过。
3. **测试必须存在**：进入 `/pdlc-implement` 前，对应测试必须存在且处于红灯状态。违反则中止。
4. **自检必须执行**：段二自检为强制步骤，不得以"已经很好了"为由跳过。
5. **防循环**：段三修复为单次，不递归。无法自动修复的问题记录到报告，继续往下走。
6. **状态必推进**：成功执行某 phase 后 `current_stage` 必须变更。收尾时若发现 `current_stage` 未推进，视为失败并报错，**不得静默返回**（防止外层循环拿滞后的状态空转烧额度）。唯一例外：命中人工点主动 block 时，`current_stage` 保持不变但必须写 `last_phase_result.ok=false` + `blocked_reason`。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law.md -->

> ⛔ **发布是破坏性·不可逆操作**：打 tag / bump 版本 / 触发 CI/CD 属破坏性范畴。**`--autonomous` 对本命令无效**——即使带该参数，§1.1（未完成功能）与 §1.2（测试门）的人工确认仍必须真实由人应答。自主循环（`/pdlc-loop-run`）停在「评审通过、`next_step` 为 `pdlc-ship`」（循环文档里称 `review_done`），永不进入本命令。

## 段一：执行

> 参数带 `--tag-after-merge`：只做「合并后补打」（见 1.5 末尾），跳过下面全部步骤。

### 1.1 前置检查

1. 确认当前分支不是 `master` / `main`（参考 CLAUDE.md §5）
2. 确认工作区干净（`git status` clean）
3. 盘点 `docs/.pdlc-state/` 下的功能（跳过 `_` 前缀的索引文件与 `statusline.json`），逐个归入四类：
   - **可发布**：`next_step` 为 `pdlc-ship`，且 `last_phase_result.ok` 不是 `false`——评审（或功能编排）已通过、等着发布。这一类**纳入本次发布**
   - **已发布**：`current_stage` 为 `ship_done` 或 `deploy_done`——上一次发布已纳入，本次不再收
   - **旧版终态写法**：`current_stage` 以 `_done` 结尾但不是上面两个（如 `feature_done` / `fix_done` / `review_done`）——旧版本写入，分不清是「已发布」还是「评审通过、待发布」。逐个列出，**请人确认**归入可发布还是已发布；`--autonomous` 也不替人判
   - **进行中**：其余全部（含 `last_phase_result.ok` 为 `false` 的阻塞功能）
   - 有进行中的功能 → 列出来并询问是否继续（用户明确同意才继续；进行中的功能不纳入本次发布）
   - 可发布为空 → 告知「没有评审通过、待发布的功能」，询问是否仍要发布（如只发文档 / 依赖升级）
4. **质量闸门检查**（若项目有 `docs/00_standards/quality-targets.yml`）：
   读 `docs/07_reviews/quality/` 下**最近一份 `.md` 报告**（同名 `.html` 只是视图，
   闸门一律以 `.md` 为准——两者若不一致，信 `.md`）：
   - 无任何报告 → 提示先跑 `/pdlc-quality`，询问是继续还是先出报告
   - 报告**总判定未达标** → **默认不放行**；要发必须由人**显式 override 并写明理由**，
     该理由需记入本次发布的 CHANGELOG 或发布说明（不允许无声跳过）
   - 报告**过期**——分两档处理，**不是所有过期都等价**（见下）
   - 达标且未过期 → 在发布报告里引用该报告路径、日期与 commit SHA 作为质量证据

   #### 过期判定：按「改动了什么」分两档

   报告头部记着生成时的 `<!-- 仓库版本: <commit SHA> -->`（由 `/pdlc-quality` 落盘时写入）。
   取该 SHA，跑 `git diff --name-only <SHA>..HEAD` 看这期间动了什么：

   | 这期间改动命中 | 判定 | 理由 |
   |---|---|---|
   | `docs/01_requirements/prd/`、`docs/00_standards/quality-targets.yml`、`docs/00_standards/e2e-flow-map.yml`、`docs/00_standards/test-commands.yml` | **硬闸·不放行** | 报告里的 PRD ↔ `core_flows` 对账与 E2E 覆盖矩阵的**输入变了**，结论不再成立。重跑单测补不回对账——必须重跑 `/pdlc-quality` |
   | 只有其它代码 / 文档 | 提示已过期，**建议**重跑 | 对账仍成立，测量数字可能略旧 |
   | 报告里没有 `仓库版本` 字段，或该 SHA 在本仓库解析不了 | **按「不可判」处理**：明确告知无法核对新鲜度，建议重跑 | 与三态语义同一条纪律——「查不了」不等于「没问题」，不得静默当作未过期 |

   > ⛔ 硬闸同样允许人**显式 override 并写明理由**（与「总判定未达标」同一条通道，理由须记入
   > CHANGELOG 或发布说明），但**不得无声跳过**。

   #### `quality-targets.yml` 变动要单独看一眼「闸门是不是被调松了」

   若上表命中的文件里**包含 `quality-targets.yml`**，除了要求重跑，还必须把
   `git diff <SHA>..HEAD -- docs/00_standards/quality-targets.yml` **原样展示给人**，
   并逐条点出下列「变松」信号——**命中任何一条都要人明确确认，不得只当作普通过期**：

   - 覆盖率目标数字**下降**（如 85 → 70）
   - `core_flows` 条目**减少**（核心流被移出闸门视野）
   - lint 策略**放宽**（如 zero-warnings 改为允许若干 warning）
   - 新增了**豁免声明**（把某些 PRD / 流程排除在对账之外）

   > **为什么单列**：报告达标之后把目标调低，重跑一次照样是绿的——日期新、SHA 新、结论"达标"，
   > 但**尺子本身变短了**。这与 `/pdlc-test-setup --refresh` 的「严向自动、松向人确认」是同一条
   > 原则换个位置：**放松闸门永远是人的决定，不能由流程默默吸收。**

### 1.2 发布前测试门（参考 CLAUDE.md §6）

**必须主动询问用户**（不得默认跳过，也不得默认强制跑）：

```
📦 发布前测试门检查：是否先跑全量单测 + E2E 测试？

[选项 A] 跑测试（推荐）
  → 后端：./gradlew test 或 mvn test
  → 前端：pnpm test 或 npm test
  → E2E：pnpm exec playwright test（如有）

[选项 B] 跳过测试 —— 仅适用于生产 hotfix
  → 理由：<请说明>
  → 自动记录到 commit 消息

请选择 A 或 B。
```

若选 B：本命令的参数必须含 `--skip-tests` 且有理由说明，否则中止。

### 1.3 版本号处理

1. 读取当前 `VERSION` 文件
2. 若本命令的参数带 `--version x.y.z`，用指定值；否则按语义化规则建议：
   - 本次发布含 fix 且无 feature → 补丁号 +1
   - 含 feature 且无 breaking → 次版本号 +1
   - 含 breaking → 主版本号 +1
3. 写回 `VERSION`

### 1.4 更新 CHANGELOG.md

1. 取 §1.1 盘点出的**可发布**功能（含人工确认归入可发布的旧版终态写法）
2. 分组：缺陷（`B` 开头的 ID）→ "修复"；history 里有 `refactor` 阶段的功能 → "重构"；其余 → "新增"
3. 每条用"- <简要描述>（<feature-id>）"格式写入 CHANGELOG 的 `[未发布]` 段（开发各阶段可能已按同一格式为该功能追加过条目——`[未发布]` 段里已有同一 ID 的，不重复写）
4. 把 `[未发布]` 改为 `[<new-version>] - <今日日期>`

### 1.4.1 发布说明草稿（可直接作 PR 描述）

按 `assets/release-notes-template.md` 写 `docs/05_deployment/releases/v<new-version>-release-notes.md`，把这次发布散在各处的结论汇到一页，
开 PR 时直接 `gh pr create --body-file <这个文件>`，发 Release 时也能用。**只写这个文件，不开 PR、不合 PR、不推送。**

- **来源**：本次纳入的功能（§1.1 的可发布清单）各自的 PRD「背景与目标」、`docs/07_reviews/code/<ID>-*-review.md` 的评审总结与「需人工处理」项、
  状态文件里 `last_phase_result.checks`（读的是推进到 `ship_done` **之前**的那份，即评审阶段的结果），以及 §1.1 的质量报告结论、§1.2 测试门的选择、§1.5 的 tag 去向
- **数字照抄**：问题数、`checks` 的值原样搬，不重算、不美化；`null` 照写 `null`。某项产物不存在就写「无」，不要补写一份
- **「需要人跟进」不能省**：评审里的需人工项、质量闸门 override、过期提示，本次发布交给人的事都列在这里；真的一项都没有才写「无」
- **不加工具署名**：草稿是给人发出去的文字，不写「由某某工具生成」之类的署名或链接
- tag 去向此时还没定（§1.5 才判断）：先写「待定」，§1.5 判断完回来改成「已打 v<new-version>」或「待合并后打」，再一起提交

### 1.5 提交，按合并方式决定何时打 Tag

**先推进状态机，再提交**：对每个纳入的功能按段四的规则运行状态推进脚本（`--stage ship --next pdlc-deploy --done`），让 `ship_done`
随发布提交一起进库。先提交后推进的话，状态文件的改动留在发布提交之外——squash 合并时就丢了，主干上这些功能会一直显示「待发布」。

```bash
git add VERSION CHANGELOG.md docs/05_deployment/releases/v<new-version>-release-notes.md docs/.pdlc-state/<纳入的功能ID>.json
git commit -m "release: v<new-version>"
```

若选项 B（跳过测试）：commit 消息末尾追加 `[skip-tests: <理由>]`。

**tag 必须指向最终留在主干上的那个提交。**本命令跑在发布分支上，分支怎么合进主干决定了现在打的 tag 还算不算数：

| 合并方式 | 发布分支上的提交会不会原样进主干 | 本命令的做法 |
|---|---|---|
| 普通合并（merge commit）/ 快进 | 会 | **当场打** tag |
| squash 合并 / rebase 合并 | 不会——主干上是新提交 | **不在分支上打**，标为「待合并后打」 |
| 判断不了 | — | 问人（本命令不接受 `--autonomous`，见上） |

判断合并方式，按顺序取，命中即停：

1. 项目规范里写了（`CLAUDE.md`、`CONTRIBUTING.md`、`docs/00_standards/` 中关于合并的约定）
2. 托管平台的仓库设置，例如 GitHub 用 `gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed`：只开了一种就是它；开了多种不算命中
3. 主干最近的历史：近 10 个提交几乎都是单亲、标题以 `(#<编号>)` 结尾 → squash；有带两个父提交的合并提交 → 普通合并。两种迹象都有、或历史太短 → 不算命中
4. 以上都没命中 → 问人

当场打：

```bash
git tag -a "v<new-version>" -m "Release v<new-version>"
```

待合并后打：不建 tag，交接里写明「tag 待合并后打」，并给出下面的补打命令。

#### 合并后补打：`/pdlc-ship --tag-after-merge [v<x.y.z>]`

分支合并后，在主干上运行本命令的这个模式。它只打 tag，**不跑 1.1–1.4、不改状态机**（`ship_done` 已在发布时写过）。
所以本模式下「分支不是 main/master」的检查与自检项不适用，IRON LAW 的状态写入与「状态必推进」两条也不适用——它不是一次阶段推进。
参数带 `--tag-after-merge` 时，直接从这里开始，做完按下面的交接收尾：

1. 切到主干并拉取最新（`git switch <主干> && git pull --ff-only`）
2. 版本号：取参数里的；没给就取主干上 `VERSION` 的值
3. 若 `v<x.y.z>` 已存在：指向主干上的提交 → 告知已打过，结束；指向主干之外 → 列出它指向的提交，**问人**是否删掉重打（删 tag 属破坏性操作，不自动做）
4. 找发布提交：主干上**第一个**让 `VERSION` 变成该版本号的提交。不要用 `git log -S`，它也会命中把版本号改走的那个提交：

   ```bash
   git log --reverse --format=%H <主干> -- VERSION | while read -r c; do
     [ "$(git show "$c:VERSION" | tr -d '[:space:]')" = "<x.y.z>" ] && { echo "$c"; break; }
   done
   ```

   找不到 → 问人（可能是版本号写在别的文件里，由人指定提交）
5. 核对它在主干上：`git merge-base --is-ancestor <提交> <主干>` 退出码为 0 才继续
6. 打 tag：`git tag -a "v<x.y.z>" <提交> -m "Release v<x.y.z>"`，**不推送**（推送 tag 会触发按 tag 运行的 CI，由人决定）

```
✅ 已补打 tag：v<x.y.z> → <提交短 SHA>（<提交标题>），已核对在 <主干> 上
👉 下一步：git push origin v<x.y.z>（有按 tag 触发的 CI 时会随之运行），再 /pdlc-deploy v<x.y.z>
```

### 1.6 CI/CD 配置（默认不动）

本命令**默认不生成、不修改任何 CI 配置**。日常检查（lint / test / build）在本地跑（§1.2 已跑过），CI 按次计费，
每次 push / PR 都触发会很快烧掉额度。项目已有 CI 配置时只读不改：检查它是否覆盖本次新增的测试路径，没覆盖就在交接里提示，由人决定是否修改。

仅当用户**明确要求**生成或修改 CI 配置时才动手，且先确认再写：

1. 先给出用量估算并请人确认：`月预计用量 = 触发次数/月 × 单次时长（分钟）× runner 倍率`（Linux 1× / Windows 2× / macOS 10×）
2. 触发方式默认只用手动触发 + 发布 tag，**不用** push 到分支、PR、定时触发（用户明确要求才改）

**GitHub Actions**（`.github/workflows/release.yml`）：
- 触发：`workflow_dispatch` + `push: tags: ['v*']`
- runner：默认 `ubuntu-latest`；只有必须在 macOS / Windows 上构建或签名时才用对应 runner
- 步骤：checkout → setup 运行时 → install → test → build → 上传产物
- 按项目技术栈选模板（Node/Python/Java/Go）
- 敏感信息通过 Secrets 注入，不硬编码（never hardcode secrets — use Secrets / env vars）

**GitLab CI**（`.gitlab-ci.yml`）：
- stages: build / test / deploy
- cache: 依赖目录
- jobs: 对应各 stage 的执行命令
- 触发：`rules` 只放行 tag 与手动（`when: manual`）
- 生产环境：手动审批后部署

**Jenkins**（`Jenkinsfile`）/ **云效 / 其他**：按项目已有约定生成，同样只用手动 + tag 触发。

生成后在 `docs/05_deployment/ci-cd/` 下记录流水线使用说明。

## 段二：自检

<!-- @include templates/prompts/self-audit.md（已内联于下方，无需另读） -->
## 段二：自检（强制）

重新阅读本次产出物，按质量关卡清单逐项检查。勾选已通过，标注未通过原因。

> **注意**：自检清单的具体内容由各命令自行定义，本片段只规定结构。

## 段三：修复（单次，不递归）

针对自检段标注为未通过的项：

- **可自动修复**：直接修复（如补缺字段、修正格式、补齐缺失段落）
- **修复后回验**：再次运行自检，确认被修复项现在通过
- **无法自动修复**：记录到自审报告，不再尝试，流程继续

⚠️ 单次修复原则：若一轮修复后仍有项未通过，**不再递归修复**，防止死循环。
<!-- @include-end templates/prompts/self-audit.md -->

**发布自检清单：**
- [ ] VERSION 已更新到新版本号
- [ ] CHANGELOG 有本次发布条目
- [ ] 发布说明草稿已写入并随发布提交：纳入的每个功能都有一行，数字与评审记录 / 状态文件一致，tag 去向不是「待定」，没有工具署名
- [ ] 合并方式已判明（或已问人），tag 与之相符：当场打的，`git tag -l v<new-version>` 返回非空；待合并后打的，没有在分支上建 tag，交接里给了补打命令
- [ ] 若选 A，测试已全绿
- [ ] 若选 B，commit 消息含 `[skip-tests]` 标记
- [ ] 分支不是 main/master
- [ ] 本次纳入的每个功能状态机已写 `ship_done`；未纳入的功能没被改动
- [ ] 未经用户明确要求，没有新增或修改 CI 配置

<!-- @include templates/prompts/loop-prevention.md（已内联于下方，无需另读） -->
## 防循环规则

本命令所有的自检-修复循环均受以下约束：

1. **单次检查**：同一个自检清单在本次命令执行中只跑一次（起始 + 修复后验证共两次读）
2. **单次修复**：发现的问题只尝试修复一轮
3. **不递归**：修复后不再重新触发自检的全量重跑
4. **失败降级**：无法自动修复的问题 → 记录到自审报告 → 流程继续 → 最终报告标注待人工处理

这是为了防止 agent 在"修完再查、查完再修"的往返中陷入死循环。
<!-- @include-end templates/prompts/loop-prevention.md -->

## 段三：修复（若需）

针对未通过项：
- VERSION 未更新 → 重跑 1.3
- CHANGELOG 缺失 → 重跑 1.4
- 应当场打的 tag 未创建 → 重跑 1.5 的打 tag 一步；squash / rebase 合并却在分支上建了 tag → 删掉这个刚建、还没推送的 tag（`git tag -d v<new-version>`），改为待合并后打
- 分支错误 → 立即中止（不可自动修复）

## 段四：更新状态机 + 交接

> 状态推进已在 §1.5 提交之前做过（下面是它要遵守的规则）。这里只核对：纳入的每个功能 `current_stage` 都是 `ship_done`，且状态文件已在发布提交里（`git show --stat HEAD` 能看到）。

<!-- pdlc:meta 由 frontmatter 生成（adapters/sync_skills.py），勿手改 -->
> **本命令的状态机取值**：阶段短名 `ship`（写进 `history[].stage` 与 `last_phase_result.stage`）；下一跳 `pdlc-deploy`（写进 `next_step`，交接时提示）。
<!-- pdlc:meta-end -->
<!-- @include templates/prompts/state-update.md（已内联于下方，无需另读） -->
## 状态机更新（段四必须执行）

本命令完成主产出后，必须推进状态机文件 `docs/.pdlc-state/<feature-id>.json`。

### 用脚本推进，不要手写状态 JSON

```bash
bash scripts/pdlc-advance.sh <功能ID> --stage <本阶段短名> --next <下一跳命令名|null> \
  [--produced <产物路径，逗号分隔>] [--autonomous] [--decision "<确认点>=<所选默认>"]... \
  [--name <kebab-case>（状态文件还不存在时）] <项目根>
```

- 脚本是本 skill 自带的 `scripts/pdlc-advance.sh`。阶段短名与下一跳就是本命令正文里「本命令的状态机取值」那两个值；带了 `--autonomous` 就照传
- **检查由脚本自己跑**：它按阶段调用同目录的 `scripts/pdlc-checks.sh`（tdd 验红灯；impl / fix / refactor 跑 unit、coverage、lint；
  review 再加 e2e；e2e 只跑 e2e；文档类阶段不跑），据此判 `ok`、整段写入 history 与 `last_phase_result`，
  写完调用 `scripts/pdlc-state-lint.sh` 体检。**不要**自己先写 `checks`，也不要挑检查项
- tdd 阶段的 `--produced` 必须列出写的测试文件：脚本记下它们的指纹，之后 impl / refactor / review 推进时比对
- 主动交还人类（命中人工点、评审有阻塞项、测试本身有矛盾等）→ 加 `--blocked "<原因>"`：脚本照跑检查、如实记录，但不推进，原因写进 `blocked_reason`
- `/pdlc-ship` 写 `ship_done`、`/pdlc-deploy` 写 `deploy_done` → 加 `--done`（只有这两个命令能用）

脚本的退出码决定怎么收尾：

| 退出码 | 含义 | 你要做的 |
|---|---|---|
| `0` | 已推进 | 交接里引用 stdout 那行 JSON（`checks`、`current_stage`、`next_step`） |
| `3` | 未推进：检查没过 / 红灯没验证 / 主动 block / tdd 写的测试被改 | 把 stdout 里的 `blocked_reason` 原样写进报告，按阻塞收尾。**不要为了让它推进去改测试或改检查命令** |
| `2` | 脚本跑不了（参数错、缺 jq、状态文件损坏） | 参数错就改正重跑；缺 jq 才按下面的格式手写，并在报告里写明「状态机未经脚本写入」 |

> 退出码 `3` 且原因是「tdd 阶段写的测试被改动」：实现阶段不改测试。测试是否真的写错了（与设计 / PRD 矛盾），**只有人能判断**：
> - 交互模式：先把矛盾讲清楚、问人；人同意后再带 `--tests-changed "<理由>"` 重跑，理由记进 `auto_decisions`
> - `--autonomous`：没有人可问，**不要改测试**，带 `--blocked "<矛盾在哪>"` 收尾。自主模式下带 `--tests-changed` 脚本也不推进
>
> 项目开了 PDLC 护栏（`docs/00_standards/pdlc-hooks.yml`）时，用 Write / Edit 直接写状态文件会被拦下。

### 状态文件格式（读状态时参考；只有脚本跑不了时才照它手写）

```json
{
  "feature_id": "<F/B ID>",
  "feature_name": "<kebab-case>",
  "created_at": "<首次创建时间 ISO 8601>",
  "current_stage": "<当前阶段名>",
  "run_mode": "interactive | autonomous",
  "history": [
    {
      "stage": "<阶段名>",
      "done_at": "<ISO 8601>",
      "produced": ["<相对路径 1>", "<相对路径 2>"],
      "self_audit": { "passed": <N>, "failed": <N>, "manual": <N> },
      "auto_decisions": [
        { "point": "<autonomous 下自动前进的确认点>", "chose": "<所选默认>", "at": "<ISO 8601>" }
      ]
    }
  ],
  "last_phase_result": {
    "stage": "<本次阶段名>",
    "ok": true,
    "advanced_to": "<推进到的下一阶段 | null>",
    "checks": {},
    "self_audit": { "failed": 0 },
    "blocked_reason": null,
    "run_mode": "interactive | autonomous",
    "at": "<ISO 8601>"
  },
  "relations": {
    "extends": [],
    "depends_on": [],
    "supersedes": [],
    "resolves": [],
    "conflicts_with": [],
    "relates_to": [],
    "_updated_at": "<ISO 8601 | 省略>"
  },
  "next_step": "<下一跳命令名，如 pdlc-design；若流程结束则为 null>"
}
```

> ⛔ 示例里的 `"checks": {}` 是「本阶段没有命令可跑」的样子，**不是键名示范**——键名与取值见下方 §1。

> **`relations` 块（RFC#6，Phase 1 可选，Phase 2 推荐）**：6 个 key 对应 6 种关系类型，各为 ID 数组，存**出边**。其中 `conflicts_with` / `relates_to` 是对称类型，两端都要写；其余四种有向，只写在源 feature 上。拿不准时用 `/pdlc-relate set` 写入，它会按规则校验。旧状态文件无此块时视为全空，向后兼容。入边由 `/pdlc-relate rebuild` 派生到 `_relations.json`，不在此块手维护。

> ⛔ **写状态机的四条硬约束**——读侧（`/pdlc-status`、`/pdlc-retro`、`/pdlc-relate`）会逐条体检，
> 违反的每一处都会出现在它们输出的最前面：
>
> 1. **实例里不写 `terminal_state`**。skill frontmatter 的 `terminal_state:` 是「这个命令走完后应到达的终态名」，
>    不是状态字段。判终态只看 `current_stage` 是否以 `_done` 结尾。
> 2. **`history[].stage` 写本命令的阶段短名**（见本命令正文里「本命令的状态机取值」）——`pdlc-implement` 写 `impl`，
>    不写 `implement` / `implementation`；`pdlc-prd` 写 `requirements`，不写 `prd`。
> 3. **时间戳必须带时刻**：`created_at` / `done_at` / `at` 一律写完整 ISO 8601（如 `2026-07-28T10:40:00+08:00`）。
>    只写日期，同一天内的阶段耗时就全部算成 0——读侧只能记「不可测」。
> 4. **`next_step` 只写命令名或 `null`**，不附说明文字（如「pdlc-ship（等评审通过）」）。
>    要说明原因，阻塞时写进 `last_phase_result.blocked_reason`。

> ⛔ **`_done` 的含义是「已发布」，只由 `/pdlc-ship`（写 `ship_done`）与 `/pdlc-deploy`（写 `deploy_done`）写入。**
> 其它命令的 `current_stage` 一律写本命令的阶段短名，走完整条链路的编排命令（`/pdlc-feature`）也一样——
> 它收尾时 `current_stage` 是最后一个阶段的短名，`next_step` 是 `pdlc-ship`。
>
> - 「评审通过、等待发布」就是 `current_stage` 为 `review` 且 `next_step` 为 `pdlc-ship`（`/pdlc-e2e` 在评审之前，它的下一跳是 `pdlc-review`）。
>   循环相关文档里说的 `review_done` 指的就是这个状态，**不是**要写进 `current_stage` 的值。
> - 为什么：读侧判「已抵达终态」只看 `current_stage` 是否以 `_done` 结尾。评审通过就写 `_done`，
>   `/pdlc-ship` 就分不清哪些功能已经发布过，发布说明会重复或漏收。
> - 旧版本写入的 `feature_done` / `fix_done` / `review_done` 分不清是否已发布，`/pdlc-ship` 会列出来请人确认。

### 手写回退（仅脚本退出码 2 且无法修正时）

1. **文件不存在** → 创建文件，写入初始结构（`history` 为含当前阶段的数组）
2. **文件存在** → 读取 JSON，追加当前阶段到 `history`，更新 `current_stage` 和 `next_step`
3. **写回文件**：用 `jq` 或等效工具保持格式化
4. **写完体检**：运行 `bash scripts/pdlc-state-lint.sh <项目根>`，属于本功能状态文件的偏差当场改正。退出码 `2`（缺 jq 等）= 没体检，报告里写明「未体检」，不得当作通过。

⚠️ 若更新失败（文件损坏/权限问题），必须中止命令并在最终报告中报错。状态机不可跳过。

### `last_phase_result`（机器可读阶段结果；脚本按下面的规则写，手写回退时照做）

顶层 `last_phase_result` 是循环判停的**唯一真源**，外层只需 `jq '.last_phase_result.ok'` 即可决定 继续 / 停止 / 交还人类。规则：

1. **`checks` 只放真跑命令的退出码结果**（`scripts/pdlc-checks.sh` 的 stdout 原样），键名只能是 `tests_pass` / `coverage_pass` /
   `lint_clean` / `e2e_pass`（tdd 段 `red_verified`），值只能是布尔或 `null`（无法判定）。不照抄 `test-commands.yml` 的 `unit` / `lint`，
   不写 `"4 passed, 1 failed"` 这类摘要。没有检查可跑的阶段（文档类阶段、项目无 `test-commands.yml`）→ `checks: {}`，
   绝不因为「本阶段成功」就填 `true`——schema 示例里 `checks` 是空的，正是这个意思。
2. **`self_audit` 单列**：只放自检未通过数，**仅供参考，不作循环判停依据**。
3. **`ok` 的定义**：没有命中 `blocked_reason`，且 tdd 段 `red_verified` 为 `true`、其它阶段没有任何检查为 `false`（`null` 不拦）→ `true`；否则 `false`。
4. **命名空间**：`advanced_to` = **下一阶段的短名**，**不是命令名、也不是本阶段的 `current_stage`**。三者关系：`stage`=本阶段短名、`current_stage`=本阶段完成后的当前短名、`advanced_to`=下一阶段短名、`next_step`=下一跳命令名。

   ⛔ **短名不是「命令名去掉 `pdlc-` 前缀」**——`pdlc-implement` 的短名是 **`impl`**，不是 `implement`。别推导，查下表：

<!-- stage-map:start -->
   | `next_step`（下一跳命令名） | `advanced_to`（下一阶段短名） |
   |---|---|
   | `pdlc-tdd` | `tdd` |
   | `pdlc-implement` | `impl` |
   | `pdlc-review` | `review` |
   | `pdlc-design` | `design` |
   | `pdlc-ship` | `ship` |
   | `pdlc-deploy` | `deploy` |
<!-- stage-map:end -->

   `next_step` 为 `null`（终态或无后续）时 `advanced_to` 也是 `null`。

   > 📌 **本表是唯一真源，且是被断言钉住的**：每行的短名必须等于该 skill 自己 frontmatter
   > 里声明的 `stage:`，且任何 skill 的非 `null` `next_step` 都必须在表里有行——两个方向
   > 都由 `tests/frontmatter-check.sh` 检查，所以表不会和实现各自漂移。
   >
   > 写错短名的后果与键名写错同类：消费方按契约名匹配，认不出就当没这个阶段。
5. **推进一致**：`ok=true` 时本阶段必须真的推进了 `current_stage`（与第 6 条 IRON LAW 呼应）；到达终态或无后续时 `advanced_to=null`。`ok=false`（含 blocked）时 `current_stage` 不变、`advanced_to=null`、`blocked_reason` 写明原因。
6. **`run_mode`**：镜像本次调用是否带 `--autonomous`（带了写 `autonomous`，没带写 `interactive`）。
<!-- @include-end templates/prompts/state-update.md -->

**本阶段状态机更新**：对本次纳入发布的每个功能（§1.1 的可发布 + 人工确认归入的），各运行一次 `bash scripts/pdlc-advance.sh <功能ID> --stage ship --next pdlc-deploy --done --produced VERSION,CHANGELOG.md <项目根>`：脚本追加 ship 到 history，写 `current_stage: ship_done`、`next_step: pdlc-deploy`（发布阶段不跑检查，测试门已在 §1.2 由人决定）。`_done` 的含义是「已发布」，只由本命令与 `/pdlc-deploy` 写入。
- 人工确认为「已发布」的旧版终态写法：不追加 history、不改动，保持原样
- 进行中的功能：不动

<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->

**本命令的 handoff 输出：**

```
✅ 发布准备完成：v<new-version>
  - VERSION：已更新
  - CHANGELOG：已追加
  - 发布说明草稿：docs/05_deployment/releases/v<new-version>-release-notes.md（开 PR 时 gh pr create --body-file 这个文件）
  - Tag：<v<new-version> 已创建 / 待合并后打（合并方式：squash 或 rebase）>
  - 测试：<通过 / [skip-tests: 理由]>
📦 状态机：<N> 个功能已推进到 ship_done（<ID 列表>）
👉 下一步：/pdlc-deploy v<new-version>（部署本次发布；项目有 tag 触发的 CI 时，也可手动 git push origin v<new-version>）
```

tag 待合并后打时，下一步改为：

```
👉 下一步：开 PR 合并发布分支；合并后在主干上运行 /pdlc-ship --tag-after-merge v<new-version>，再 /pdlc-deploy v<new-version>
```

---

**参数**：$ARGUMENTS
