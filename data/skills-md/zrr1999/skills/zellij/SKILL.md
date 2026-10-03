---
name: zellij
description: >
  使用 Zellij 组织、恢复、观察或自动化持久终端工作区。适用于需要命名 session、detach/attach、pane/tab 编排、可复用 layout、并行开发服务与日志、查询运行状态、等待 pane 命令结果、恢复退出会话、只读 watch，或通过受控 web/remote attach 分享终端的场景。重点根据目标选择 Zellij 能力；精确命令、flags 和版本差异必须从本机 `zellij --help` 及对应子命令 help 获取。不要用于单个普通命令、系统服务管理或 CI 编排。
---

# Zellij

## Goal

把需要持续上下文或多个终端面的工作组织成可恢复、可观察、可验证的工作区，而不是堆一份容易过期的 Zellij 命令手册。

完成时应说明：使用了哪类工作区能力、目标 session 或 layout、如何验证当前状态，以及任何需要用户确认的破坏性或网络暴露动作。

## What it can do

根据用户目标选择最小能力组合：

- **持久工作区**：创建和命名 session，detach 后继续运行，稍后 attach、切换或重命名。
- **恢复上下文**：列出活动或可恢复 session，恢复 pane/tab 布局与可发现的命令；需要时保存当前 session 状态。恢复命令可能有副作用，不默认强制执行。
- **组织终端面**：用 tab 区分工作流，用 tiled、floating 或 stacked pane 放置编辑器、服务、测试、日志与临时工具。
- **可复用环境**：把稳定的 pane/tab 结构写成 KDL layout；一次性工作优先直接操作，重复工作才维护 layout。也可以读取或导出现有布局，再做小范围调整。
- **自动化与取证**：从 CLI 对指定 session 发送 action，查询 pane/tab/client 状态，优先使用可用的结构化输出；运行命令时可按本机支持情况等待成功、失败或退出，再读取状态、屏幕或 scrollback 作为证据。
- **插件集成**：启动、聚焦或向插件发送数据。只有插件确实解决当前目标时才引入，不把插件当默认依赖。
- **观察与分享**：本地只读观察优先使用 watch；浏览器或远程 terminal 可通过内建 web server、认证 token 和 remote attach 实现。网络暴露必须先处理认证、TLS、监听地址和信任边界。

## Discover the local interface

Zellij 的 CLI 会演进。先确认本机版本，再沿命令树查询精确语法：

```text
zellij --version
zellij --help
zellij <subcommand> --help
zellij action --help
zellij action <action> --help
```

只查询与当前目标相关的分支。例如 session 管理看 `attach` / `list-sessions` / 删除或终止相关 help；pane 自动化看 `run` 和 `action`；分享看 `watch`、`web`、`attach`；配置与 layout 检查看 `setup` 和 layout/action help。

若 help 中没有预期能力，说明本机版本不支持，并给出最小替代方案；不要凭文档记忆猜 flags。需要远端最新资料时再读取 Zellij 官方文档或 release notes，本机 help 仍是实际执行依据。

## Workflow

1. **确认结果**：区分临时分屏、长期开发工作区、可复用 layout、恢复、自动化取证或远程分享。
2. **检查现场**：确认 Zellij 是否可用、版本、当前是否已在 session 内，以及已有 session/layout/config；避免无意嵌套或重名。
3. **发现语法**：读取完成目标所需的最小 help 分支。一个结果决定下一步时保持串行；多个独立状态查询可并行。
4. **执行最小动作**：优先复用现有 session 和配置。只有重复使用能收回维护成本时才新增 layout 或持久配置。
5. **验证**：通过 session 列表、pane/tab/client 查询、命令退出状态、screen/scrollback dump、web status 或重新 attach 验证结果。得到足够证据后停止。

## Safety boundaries

以下操作会改变或暴露用户环境，需要明确意图和更谨慎的确认：

- kill 或永久删除 session；
- 向运行中的 pane 写字符、发送按键或关闭/替换 pane；
- 恢复时跳过确认并强制重跑历史命令；
- 应用包含命令的未知或远程 layout；
- 启动对外监听的 web server、创建或撤销 token、保存远程凭据、关闭 TLS 校验。

不要输出、提交或持久化登录 token。只读需求优先 watch 或只读凭据。非 localhost 暴露使用认证与 TLS，并说明 Zellij web server 不等同于完整的互联网边界防护；公开到不可信网络前应由用户确认反向代理、限流和访问策略。

## Boundaries

- 一个普通命令不需要 Zellij；直接运行更简单。
- 长期守护进程和开机服务交给系统 service manager。
- CI、任务 DAG 和资源调度交给对应编排系统。
- Zellij 管理终端工作区，不替代应用日志、健康检查、测试框架或进程监督。

## Output

执行类请求报告：完成的工作区动作、session/layout 名称、验证结果和剩余 blocker。规划或教学请求先讲 Zellij 能满足的能力，再给最小操作路径；只在用户需要时展开具体命令，并以当前 help 输出为准。
