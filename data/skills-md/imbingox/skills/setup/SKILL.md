---
name: setup
description: "每个 repo 运行一次：按 provider 模板配置项目 issue tracker 与领域文档位置，并幂等检查 Codex / Claude CLI statusline，不覆盖已有用户配置。"
disable-model-invocation: true
---

# Setup

每个 repo 首次使用本套 skills 时运行一次：

`/setup`

它只有一个入口，但处理两个层次：

1. **Project setup**：当前 repo 的 tracker、workflow 和 domain docs，必须完成。
2. **CLI environment check**：当前机器的 Codex / Claude 配置，幂等检查；已有用户配置优先，缺失时才提议补齐。

不要把这两层拆成两个用户命令。重复运行必须安全；更换 tracker 或换新机器时可重新运行校验。

## 1. Explore first

先读取当前 repo，不假设：

- `git remote -v`、`.git/config` 和 repo root；
- `AGENTS.md` / `CLAUDE.md`，以及其中已有的 tracker / domain 配置指针及对应文件，包括自定义位置；没有明确指针时再查默认 `docs/agents/issue-tracker.md` / `domain.md`；
- `CONTEXT.md`、`CONTEXT-MAP.md`、已有 ADR 目录；
- tracker 线索：GitHub / GitLab remote、`.scratch/` 等本地 issue 目录、Linear 等其他配置；
- `gh` / `glab` 是否可用及登录状态（`gh auth status`、`glab auth status`）。

优先沿用现有配置位置。若指针失效或多个文件互相冲突，先说明差异并确认 authoritative source，不静默新建第二套配置。

同时只读检查本机：

- `command -v codex`、`codex --version`、`~/.codex/config.toml`；
- `command -v claude`、`claude --version`、`~/.claude/settings.json`；
- 已有 statusline / TUI 配置。

不要读取、打印或写入 API key、token、cookie 等 secrets。

## 2. Project setup: issue tracker

项目 tracker 配置是 `to-spec` 和 `implement` 唯一的 tracker 来源：它们按其中的操作发布、读取、推进状态，不自己推断 provider 或命令。

确定 provider：

1. 已有配置：原位保留，对照下面的必需内容只补缺项。
2. 用户已经明确指定：使用用户选择。
3. remote 指向 GitHub / GitLab：推荐对应 provider，请用户确认。
4. 仍不明确：只问 provider / target 这一项，不猜。

新建配置时按 provider 复制模板，替换占位并删除不适用的行：

- GitHub：[issue-tracker-github.md](references/issue-tracker-github.md)
- GitLab：[issue-tracker-gitlab.md](references/issue-tracker-gitlab.md)
- 本地 markdown：[issue-tracker-local.md](references/issue-tracker-local.md)
- 其他（Linear、Jira 等）：请用户用一段话描述工作方式，参照 GitHub 模板的结构写成自然语言。

默认写入 `docs/agents/issue-tracker.md`；用户指定其他路径时使用其路径。

必需内容：

- provider 与明确 target。fork 同时有 origin / upstream 时核对写入目标；不把本 skills 仓库当业务 tracker。
- 操作：读取、查重、新建、更新正文、评论、挂子票 / 列子票、加 / 读 blocker、推进状态、关闭、重新打开；原生父子或依赖关系不可用时的文本表达。
- workflow：项目已有的状态、labels 或 project 字段；ready 标签或“不使用”；**completion condition**（什么状态代表 issue 已满足 blocker）；Controller 可执行和需要人工确认的动作。

只记录项目真实存在的状态和 labels，不为适配本 skill 发明 workflow vocabulary；tracker 只有 open / closed 就记录 open / closed。本地 markdown 没有既有约定时使用模板中的 `Status` 值。
能只读验证的就验证，例如 `gh repo view <owner/repo>`；不为验证创建测试 issue，配置中不写 credentials。

## 3. Project setup: domain docs

优先读取并更新项目说明指向的已有 domain 配置，其次使用已有 `docs/agents/domain.md`。只有尚无配置时才默认创建 `docs/agents/domain.md`，不迁移已有等价配置。记录：

- glossary / domain context 的位置；
- ADR 位置与编号约定；
- single-context 或 multi-context。

读取 [domain-layout.md](references/domain-layout.md)，按其中的单 / 多 context 目录树和 `domain.md` 示例记录实际位置。已有约定优先，不强制套用示例路径。

默认 single-context；只有 repo 已经呈现明显多 context 结构时才使用 map。
不要为了 setup 创建空 `CONTEXT.md` 或空 ADR 目录；需要记录第一个术语 / 决策时再创建。

## 4. Add a small project pointer

在 repo 已有的 `CLAUDE.md` 或 `AGENTS.md` 中维护一个简短的 `## Agent workflow` 区块，指向本次确认的 tracker 配置和 domain 配置的实际路径。

保留已有有效指针及其组织形式，不为固定区块名重复添加，不把自定义路径改指向默认目录。
两个文件都存在时，修改项目已作为主说明文件使用的那个；不能判断时让用户选一个。两个都不存在时让用户选择创建哪一个。
不要复制整份 tracker 配置到这里，也不要覆盖周围人工内容。

## 5. CLI environment check

CLI 设置是**用户 / 机器级**，不是 repo 配置。每次 `/setup` 都检查，但仅在缺失时提议写入。

- Codex：`~/.codex/config.toml` 已有 `[tui].status_line` 时保留原值；Codex 已安装且未配置时，提议原生 TUI status line。
- Claude Code：`~/.claude/settings.json` 已有 `statusLine` 时保留原值；Claude 已安装且缺失时，提议把本 skill 的 [claude-statusline.py](references/claude-statusline.py) 复制到 `~/.claude/statusline.py` 并 merge `statusLine` 字段。

推荐值、字段映射和 Codex item 的核对方式见 [cli-config.md](references/cli-config.md)；提议写入前读取。

对 `~/.codex` / `~/.claude` 的任何写入：

- 先展示将修改的文件和最小 diff，取得用户一次明确确认；
- 写前创建 timestamped backup；
- parse 后 merge 本 skill 管理的 key，不用字符串替换，不替换整个文件或 `[tui]` 表；
- 写后重新 parse 并核对；
- 已有 statusline 永不自动替换，用户明确要求替换时才按其授权范围更新。

用户拒绝机器级修改时，Project setup 仍然可以完成。

## 6. Confirm and write

在第一次实际写入前，用一个紧凑摘要展示：

- tracker provider / target，以及原生或文本关系；
- workflow completion condition 与 ready 标签；
- domain docs layout；
- Codex statusline：existing / proposed / unavailable；
- Claude statusline：existing / proposed / unavailable。

用户确认后执行写入。如果全部已有且一致，不要为了流程重复询问，报告 no-op 即可。

## 7. Done

完成后报告：

- 创建 / 更新了哪些 repo 文件；
- tracker target 与完成状态语义；
- Codex / Claude 哪些用户级配置被保留、补齐或跳过；
- backup 路径（如发生用户级写入）；
- 未完成项。

后续需求开发流程：`grill → to-spec → implement`。配置可以直接手动编辑，之后不必重跑 setup。
