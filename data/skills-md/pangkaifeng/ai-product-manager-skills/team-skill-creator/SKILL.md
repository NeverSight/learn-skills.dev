---
name: team-skill-creator
description: >
  Skill 生命周期治理 / 能力沉淀判断：当用户要新建、导入、合并、发布、更新、弃用、退役或删除一个
  可复用 Skill，或要决定它应进入统一公开仓、项目、本地 Agent 或 Multica 时使用。
  可用中文唤起：“帮我创建一个 Skill”“把这个流程固化成 Skill”“导入这个 GitHub Skill”
  “这个 Skill 应该放哪里”“把 Skill 发布到多个 Agent”。只评审现有 SKILL.md 时改用 skill-reviewer。
---

# Skill 生命周期治理（team-skill-creator）

## 中文速查

- 中文名：Skill 生命周期治理 / 能力沉淀判断
- 英文稳定名：`team-skill-creator`
- 适合：新建、导入、合并、发布、更新、弃用、退役、删除 Skill，并治理来源与分发目标
- 不适合：只评审已有 Skill，改用 `skill-reviewer`；一次性任务不要强行沉淀为 Skill

## 核心原则

这个 Skill 是治理编排层，不是新的复制工具。先确定能力是否值得沉淀，再确定唯一权威来源、生命周期和目标，最后调用已有工具完成发布与分发。

| 层级 | 唯一职责 | 不负责 |
| --- | --- | --- |
| `team-skill-creator` | 能力判断、查重、仓库选择、生命周期、验证和发布计划 | 自己实现所有 Agent 的复制协议 |
| GitHub 仓库 | 版本事实源、评审、回滚和公开披露边界 | 直接让每个 Agent 立即可用 |
| Skillshare | 从聚合目录同步到 Codex、Claude、OpenCode、Qoder、WorkBuddy 等本地目标 | 选择权威仓库或发布 Multica |
| Multica publisher | 通过白名单和稳定 ID 发布 Multica Skill 内容 | 管理本地 Agent，或自动决定项目/Agent/小队绑定 |

**禁止对 `$SKILLSHARE_SKILLS_ROOT` 聚合目录运行 `skillshare push`。** 该目录可能汇集多个来源，不能被当作单一 GitHub 仓库整体发布。GitHub 发布必须在选定的权威 checkout 中精确暂存目标 Skill。

不要替换系统 `.system/skill-creator`；把它作为结构和脚手架基线。

## 权威来源决策

先选来源，再写文件：

| 来源 | 适用条件 | 标准仓库 |
| --- | --- | --- |
| 统一公开仓 | 通用、可复用、来源和许可证允许公开，且通过披露检查 | `PANGKAIFENG/ai-product-manager-skills` |
| 项目级 | 只服务单个仓库，依赖其架构、命令或领域约束 | 项目仓库内 `.skillshare/skills` 或约定目录 |
| 本地受限 | 包含客户数据、内部 URL、凭据、个人绝对路径或不可公开来源 | 受控本地目录；先去敏或拆分，不进入公开 catalog |
| 本地草稿 | 尚未通过验证或用户明确要求不发布 | 独立草稿目录，不进入正式分发 |

通用能力默认以统一公开仓为候选权威源，但公开性不确定时必须停在项目级或本地受限状态。公开发布前检查 secrets、内部 URL、客户数据、许可证和 provenance。不要从 Skillshare 聚合目录反推权威仓库；以 catalog、Git remote 和 Skill provenance 为准。

## 生命周期

| 动作 | 处理方式 |
| --- | --- |
| 新增 | 查重后选择来源，创建、验证、评审、合并，再分发 |
| 导入 | 记录来源和许可证，决定 new / merge / replace / reject |
| 更新 | 在权威仓库分支修改；`skill-creator` 负责行为优化，`skill-reviewer` 负责发布门禁 |
| 弃用 | 标记替代项和迁移说明，停止新绑定，保留旧引用 |
| 退役 | 停止维护和自动发布，保留墓碑记录与稳定 ID |
| 删除 | 先查引用和影响面，经明确批准后依次处理仓库、catalog、Skillshare 目标和 Multica 映射；必须有回滚方案 |

默认先弃用或退役，不直接删除。重命名按“新增稳定名称 + 弃用旧名称”处理，避免破坏引用。

## Workflow

1. 用一句话复述要沉淀的能力，并识别本次动作：新增、导入、合并、更新、弃用、退役或删除。
2. 检查统一公开仓、用户指定项目和本地候选来源的 remote、默认分支、ahead/behind 和 dirty 状态。存在用户改动时使用独立 worktree，不清理或覆盖。
3. 扫描相似 Skill。至少包含统一公开仓、Skillshare 聚合源、系统 Skills、当前项目和导入来源：

```bash
python3 <this-skill>/scripts/inspect_existing_skills.py \
  --name "<candidate-name>" \
  --description "<request summary>" \
  --catalog-root /path/to/ai-product-manager-skills \
  --root /path/to/current-project \
  --import-root /path/to/imported/skills \
  --fetch-catalog --json
```

4. 对非平凡或模糊请求先读取 `references/assetization-gate.md`，再按需读取 `references/creation-rubric.md`，在 Prompt、Context Pack、Loop、Workflow、Tool、Plugin、App 和 Skill 之间选择最小可靠形态。
   - 先判断是不是一次性工作；重复 AI 协作优先选择 Workflow/Loop，只有稳定原子职责才进入 Skill。
   - 资产化判断和失败归因作为本 Skill 的前置治理阶段，不再提供同触发的独立入口。
5. 认知类 Skill 在决策前调研经过验证的方法、常见失败模式和 AI 场景可操作性；技术操作类可跳过，但要记录原因。
6. 选择统一公开仓、项目级、本地受限或本地草稿来源；再确定 category、status、稳定英文名和 provenance。
7. 读取 `skillshare target list --json` 动态确认本地目标，不把 Agent 名称硬编码成固定清单。Multica 需求单独记录 workspace 和项目/Agent/小队范围。
8. 缺少会改变方案的信息时最多问 5 个问题；能从文件、Git 或工具发现的信息不要再问用户。
9. 写文件前输出 `Lifecycle Decision`，包含来源、目标、验证、发布、回滚和所需批准。
10. 获得明确确认后，在选定 Git checkout 的 feature branch 或 worktree 中创建或修改；禁止先写 runtime 副本。
11. 完成结构校验、行为 eval、前向测试和 `skill-reviewer` CR。修复 P0/P1；P2 可记录为 backlog，但要说明风险。
12. 推送 feature branch，通过 PR 或等价评审合并默认分支，并从远端默认分支回读验证。
13. 只把已合并版本同步到 Skillshare 聚合源，再运行 `skillshare sync --json` 并验证实际目标。Multica 按独立流程处理。

## Context Intake

从对话、catalog、Git 和工具结果中收集：目标用户与复用频率、期望产物、触发与非触发示例、失败成本、公开性、provenance、目标 Agent/项目/Multica workspace、外部写入和回滚要求。只有缺失信息会改变来源、结构、权限或删除决策时才提问；其余内容用明确假设继续。

## 创建与更新

创建脚手架时必须显式传入选定 Git checkout，避免误写 Codex runtime：

```bash
python3 <this-skill>/scripts/create_team_skill.py \
  --name "<skill-name>" \
  --description "<trigger description>" \
  --resources scripts,references \
  --path /path/to/selected-github-checkout \
  --expected-remote git@github.com:<owner>/<repo>.git
```

更新现有 Skill 时，先保存旧版本和失败证据，按 `skill-creator` 的 old/new eval 做最小通用改动。最终用 `skill-reviewer` 审查，不让 Reviewer 代替 Creator 决定产品范围。

## 导入与合并

对 Git 仓库、市场下载、插件或另一个 Agent 目录中的候选 Skill：

1. 记录 repo、commit/version、原路径、license 和 import date。
2. 比较 trigger、workflow、resources、eval、context budget 和维护成本。
3. 选择 `new`、`merge-into-existing`、`replace-with-source` 或 `do-not-import`。
4. 有重叠时优先合并，不制造同触发空间的重复 Skill。
5. 将 provenance 写入 `references/provenance.md` 或等价 metadata。

## Catalog 与状态

更新与统一公开仓实际 schema 一致的 `README.md`、`SKILL_REGISTRY.md`、`SKILL_ROUTING.md`、`catalog/skills.yaml` 和必要的安装文档。本地受限能力不进入公开 catalog，也不得通过自造状态值伪装为已发布 Skill。

扫描器无法解析 catalog、remote 不符或默认分支状态未知时，决策必须标记为 blocked，不得把空结果解释为“没有重复 Skill”。

## 发布门禁

1. 在 feature branch 上精确暂存目标 Skill、测试和必要 catalog 文件，禁止 `git add .`。
2. 运行结构校验、团队 checker、行为测试和 `git diff --cached --check`。
3. 推送 feature branch，完成 CR 后合并默认分支；不要绕过审查直接把工作分支推成 `main`。
4. fetch 远端并验证默认分支中的 Skill 内容、catalog 和 routing。
5. 记录 merge commit 和回滚 commit。外部副作用已发生时，回滚代码不等于恢复下游数据，必须单独验证分发回滚。

## 本地 Agent 分发

GitHub 合并后，先确认本地权威 checkout 已 fast-forward 到远端默认分支，再通过 Skillshare 的安装元数据把已合并 Skill 引入 `$SKILLSHARE_SKILLS_ROOT/<skill-name>`。不要裸复制：首次安装要登记来源，后续更新要验证登记来源仍指向同一权威 checkout。保留聚合目录中的其他用户改动，不做仓库级 reset、pull 或整体 push。

```bash
git -C /path/to/selected-github-checkout fetch origin main
git -C /path/to/selected-github-checkout merge --ff-only origin/main

# 首次进入聚合源：写入 .metadata.json 的 source 与 file_hashes
skillshare install /path/to/selected-github-checkout/<skill-name> --json

# 后续更新：先核对 .metadata.json 中的 source，再预演和更新
jq -e '.entries["<skill-name>"].source == "/path/to/selected-github-checkout/<skill-name>"' \
  "$SKILLSHARE_SKILLS_ROOT/.metadata.json"
skillshare update <skill-name> --dry-run --json
skillshare update <skill-name> --json

# 内容一致后才向 Agent 目标分发
diff -qr /path/to/selected-github-checkout/<skill-name> \
  "$SKILLSHARE_SKILLS_ROOT/<skill-name>"
skillshare target list --json
skillshare sync --dry-run
skillshare sync --json
skillshare status --json
```

正式同步前必须检查非 JSON dry-run 明细，逐项核对所有 create / update / prune 项列出的 Skill 名称均等于本次目标 Skill。不要用只返回 target 级数量的 JSON 汇总代替名称检查。若出现目标 Skill 之外的变更，或预览无法列出具体 Skill 名称，立即停止，不得执行全量 `skillshare sync`。先确认当前 CLI 是否支持单 Skill sync；若不支持单 Skill sync，明确报告工具限制，不得通过临时隐藏、覆盖其他 Skill 或扩大同步范围来绕过。

多 Skill 仓库不能把 `--skill` 与 `--track` 混用。对单个 Skill 使用上面的 metadata-backed `install/update`；只有整个仓库本身就是一个允许整体跟踪和分发的专用来源时，才使用 `skillshare install <repo> --track`。来源不匹配、更新发生冲突或 hash/diff 不一致时停止，不得继续 `sync`。

以命令返回的真实 targets 为准。当前或未来新增 Agent 通过 Skillshare target 配置接入，不修改 Creator 的业务逻辑。

`skillshare sync` 会同步全部已配置目标。若用户只允许部分目标，在目标 Skill frontmatter 中声明 `metadata.targets: [codex, claude, qoder]` 等明确策略，先用 dry-run 验证只有声明目标会变化，再正式同步。若当前 Skillshare 版本或目标适配器不支持该策略，停止并说明限制，不得静默扩大到未授权 Agent。

删除时先 dry-run/影响检查，再使用 Skillshare 的 uninstall/disable/trash 能力并同步；不要直接 `rm -rf` runtime symlink。

## Multica 分发

Multica 是独立 registry；`skillshare sync --json` 不会更新它。只有存在经过审计的独立 `tools/multica-skill-publisher` 时才进入该流程：

```bash
python3 tools/multica-skill-publisher/publisher.py validate
python3 tools/multica-skill-publisher/publisher.py plan --only <skill-name>
python3 tools/multica-skill-publisher/publisher.py sync --only <skill-name>
```

- 新 Skill：先新增 manifest 条目，`multica_id: null`，执行 `--allow-create` 计划并获取人工批准；创建后写回稳定 ID。
- 更新：原位更新同一 ID并回读验证。
- 引用文件删除：计划中明确 stale files；只有显式批准后才启用 prune，避免静默残留或误删。
- 弃用/退役：更新 lifecycle，不自动删除远端对象。
- 项目/Agent/小队绑定：publisher 当前只管理 Skill 内容和 ID。另行输出 `workspace -> Skill -> project/agent/squad` 部署映射，通过 Multica 支持的 UI/API 执行并回读；没有绑定证据时不得声称部署完成。

## 输出格式

```markdown
**Lifecycle Decision**
- Action: <create / import / merge / update / deprecate / retire / delete>
- Recommended shape: <Prompt / Context Pack / Workflow / Tool / Plugin / App / Skill>
- Candidate and overlap: <name, similar Skills, merge decision>
- Authoritative source: <public/private/project/local, repo, branch, clean/ahead/behind>
- Visibility and provenance: <public checks or private reason, source/license>
- Lifecycle/status: <current -> target>
- Catalog plan: <README, registry, routing>
- Local targets: <from skillshare target list>
- Multica scope: <none or workspace/project/agent/squad + manifest action>
- Eval and CR: <baseline, regression, transfer, negative, holdout, reviewer>
- Publish and rollback: <branch, PR/merge, remote verification, rollback>
- Confirmation needed: <exact write/create/delete approval>
```

完成后输出 `Lifecycle Result`，逐项报告 GitHub merge commit、验证命令、Skillshare 各 target、Multica ID/绑定证据、未完成项和回滚点。

## Definition of Done

满足以下条件才算完成：

- 能力形态、重叠处理、公开/私有/项目来源和生命周期已明确。
- 修改发生在选定权威仓库，结构、eval、前向测试和 CR 有新鲜证据。
- feature branch 已合并，远端默认分支回读一致。
- 需要本地使用时，已从合并版本更新 Skillshare 聚合源并验证所有声明目标。
- 需要 Multica 时，manifest、稳定 ID、内容回读和项目/Agent/小队绑定分别有证据。
- 弃用、退役或删除已完成引用检查、用户批准、迁移说明和回滚验证。

## Resource Guide

- 形态、查重和来源决策：`references/creation-rubric.md`
- 是否资产化以及 Skill/Loop/Workflow/Tool 分层：`references/assetization-gate.md`
- Skill 内容结构和质量门槛：`references/skill-template-standards.md`
- 相似度与 catalog 扫描：`scripts/inspect_existing_skills.py`
- 已确认后的脚手架：`scripts/create_team_skill.py`
