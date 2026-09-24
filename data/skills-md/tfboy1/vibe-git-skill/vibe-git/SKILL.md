---
name: vibe-git
description: 安装并调用 Vibe-Git CLI，协助队长和成员连接协作房间、提交 Markdown 提案、对齐需求、执行任务及审核内部需求变更。用户要求操作 Vibe-Git 时使用；普通 Git/GitHub 操作不适用。
---

# Vibe-Git CLI

Vibe-Git 是 CLI 驱动的多人协作工具。通过终端调用 `vibe-git`；网页由 `vibe-git open` 打开，用于查看团队状态。不要把旧 AgentGit MCP 命令当作本 CLI 的命令。

## 安装或定位 CLI

1. 先运行 `vibe-git --help`。若命令已可用，直接使用；若已在源码仓库且构建产物存在，也可调用 `node <源码目录>/apps/cli/dist/index.js --help`。
2. 需要安装时，检查 Node.js 24+、Git 和 Codex CLI。仓库地址为 `https://github.com/TFboy1/vibe-git.git`。若用户已有源码目录，就使用该目录，不重复克隆。这个仓库的可构建应用位于仓库根目录下的 `vibe-git/` 子目录。
3. 在应用目录依次执行 `npm ci`、`npm run build`、`npm link`；Windows PowerShell 可用 `npm.cmd` 避开脚本执行策略。`npm link` 指向该源码目录，安装后保留目录。用 `vibe-git --help` 验证。不要推荐未发布的 `npm install -g vibe-git`。
4. 安装命令和排障见 [安装参考](references/install.md)。仅在安装、更新或命令不可用时读取它。

## 调用前判断

- 确认当前终端在**使用者自己的 Git 工作区**。`host start` 和 `connect` 会把当前目录记录为该节点工作区；不要在 Vibe-Git 工具源码目录代替用户的项目目录运行它们，除非该目录就是项目。
- 用 `vibe-git status` 读取当前节点身份、任务和后台进程；队长检查 Host 时用 `vibe-git host status`。本机一次只维护一个活跃节点配置，切换房间或工作区前先说明影响。
- 从 CLI 回执或面板取得真实的 `alignment-id`、`task-id`、`node-id`、`review-id`；不要猜测 ID。长时间等待审核时用有超时的阻塞等待脚本，避免频繁手动轮询。
- `--help` 可看当前安装版本的命令。具体工作流见 [命令参考](references/workflows.md)；执行相应角色或阶段前再读。

## 工作流要点

- 队长：`host start` → 将输出的加入命令交给成员 → `open` 看面板；需要审核能力时在各节点分别 `codex bind`；收到至少一份提案后显式 `align start`，审核对齐稿后 `tasks publish <alignment-id>`。
- 成员：在自己的工作区运行队长给出的 `connect <join-url>` → `status` → `open`；用 `plan submit <文件.md>` 提交或更新**自己的**提案。所有节点都能查看团队最新提案，不能修改他人的提案。
- 文件可以是任意名称的 `.md`，须为非空 UTF-8 且不超过 256 KiB。`plan submit` 是提案，`task push` 是任务执行细节，`pr submit` 是内部需求变更；文件名不决定文档种类。
- 成员先 `task list`、`task pull <task-id>`，可用 `task push` 上传执行细节；只在明确决定开工后调用 `task start`。Codex 正常结束进入 `WAITING_CONFIRMATION` 后，先新鲜同步，再由成员确认并调用 `task done`。
- 开发中可以 `pr submit <文件.md>`；普通成员不能发起审核。队长 `review start --force` 会提前通知并暂停受影响任务；`review apply` / `review reject` 需要依据实际审核结果作出决定。

## 凭据与回执

- 加入链接含注册密钥，仅交给预期成员；不要写进仓库、Issue 或公开日志。不要读取、打印或上传 `~/.vibe-git/client.json`、`data/v20/captain.json` 或 `~/.vibe-git/audit-codex` 的凭据。
- `codex bind` 使用交互式 device-auth，专用审核账号保存在本机 `~/.vibe-git/audit-codex`，不替换日常 Codex 配置。遇到登录提示，让使用者完成设备授权。
- 只在 CLI 返回成功回执后报告操作成功。失败时保留错误信息，查看 `vibe-git logs`；队长也可查本机 Host 日志。不要把内部 Vibe-Git Pull Request 说成 GitHub PR。
