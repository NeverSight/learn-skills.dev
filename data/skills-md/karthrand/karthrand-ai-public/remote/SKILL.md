---
name: remote
description: 当用户需要远程访问 Linux 服务器、复用本地保存的服务器信息、执行单条或并行远程命令，或首次连接/登录失败后需要补齐服务器地址与凭据时使用。
---

# Remote 技能

## 概述

用于远程访问 Linux 服务器，并在本地状态目录维护 setup 状态与服务器信息。`remote` 只识别执行环境，不识别 code agent；执行环境统一按 `references/setup.md` 判定为 `windows-msys`、`linux-wsl`、`linux-native`、`macos-native`。

本地状态目录跨平台统一为 `~/.local/share/remote`（即 `$XDG_DATA_HOME/remote`，未设置 XDG 时回落到 `$HOME/.local/share/remote`）。PowerShell 的 `$HOME` 与 git bash 的 `$HOME` 指向同一物理目录，因此 ps1 与 sh 入口读写同一份状态，不再使用 `AppData\Local\remote`。

密码传递机制：
- Windows（`windows-msys`）：使用 `SSH_ASKPASS` 环境变量机制（OpenSSH 原生支持，无需额外安装）
- Linux/macOS/WSL：使用 `sshpass`

## 何时使用

- 需要连接 Linux 服务器执行只读查询
- 需要对同一台服务器并行采集多条命令输出
- 需要复用之前保存过的服务器地址、端口、用户名和密码
- 第一次访问某台服务器，或旧记录登录失败后需要重新确认连接信息
- 不适用于批量写操作、重启、删文件、改配置等高风险运维动作

## 核心流程

0. 入口选择（两级判定，先 OS 再 shell）：
   - 第 1 级 — OS 判定：`linux-wsl`、`linux-native`、`macos-native` 一律走 `remote.sh` / `setup.sh`，**不要查 `$BASH_VERSION`**（macOS zsh 下它也为空，会误判）。
   - 第 2 级 — 仅 `windows-msys` 下，用 `echo "${BASH_VERSION:-}"` 区分 shell：
     - 非空 → 当前是 git bash → 走 `scripts/remote.sh` / `scripts/setup.sh`
     - 为空 → 当前是 pwsh/cmd → 走 `scripts/remote.ps1` / `scripts/setup.ps1`
   - 原则：已在 git bash 里就**直接用 remote.sh**，不要绕 `powershell -File remote.ps1` 再转回 bash，否则会引入 PowerShell↔bash 的路径/转义桥接问题。`remote.ps1` 仅作为纯 PowerShell 环境的入口。

1. 通过标准脚本检查 bootstrap 状态（不要直接读取或猜测状态文件路径）：
   - bash 环境：`bash ./skills/remote/scripts/remote.sh --check-bootstrap`
   - pwsh 环境：`powershell -ExecutionPolicy Bypass -File .\skills\remote\scripts\remote.ps1 -CheckBootstrap`
   退出码 0 表示环境已就绪；退出码非 0 表示需要 setup。
2. 若退出码非 0，必须读取 `references/setup.md`，并只通过标准脚本完成环境 setup；不要手工探测认证工具或裸跑 SSH。setup 入口同样按第 0 步的两级判定选择（bash 走 `setup.sh`，pwsh 走 `setup.ps1`）。
3. 再检查 `servers.json` 是否已有目标服务器记录：用 `-Show -Address <目标>` / `--show "<目标>"` 查找特定服务器，或用 `-Show` / `--show`（不带地址）列出所有已保存记录。命中记录时直接复用；未命中记录时，立即向用户询问服务器地址、用户名、密码，端口默认 `22`。
4. 标准入口固定如下（按第 0 步两级判定）：
   - bash 环境（含 Windows git bash、Linux、macOS、WSL）：通过 `scripts/remote.sh` 与 `scripts/setup.sh`
   - pwsh 环境（仅 Windows）：通过 `scripts/remote.ps1` 与 `scripts/setup.ps1`
   - `remote.ps1` 提供命名参数：`-Address`、`-Port`、`-Username`、`-Password`、`-Command`、`-Commands`、`-Save`、`-Show`、`-Parallel`
5. 诊断类任务遵循 `references/remote-guidelines.md`：首轮完整采集、优先并行、不提前过滤、不做破坏性动作。
6. 连接成功后更新 `servers.json`；连接失败时按”结论 / 证据 / 推断 / 下一步”输出，最多只允许一次基于标准主链的最小重试。
7. 远端返回 `Permission denied` 时，只能下结论为”密码认证被拒绝”；不能直接解释为密码中的特殊字符或兼容性问题。
8. `windows-msys` 下使用 `SSH_ASKPASS` 机制自动提供密码，保持纯非交互；若凭据错误，应直接失败。

## 按需继续加载

出现以下场景时再读对应文档：

- 需要安装、修复或验证环境：`references/setup.md`
- 需要确认 `bootstrap-state.json` 或 `servers.json` 的结构（如调试状态不一致）：`references/state.md`
- 需要执行诊断采集、并行命令或高风险判断边界：`references/remote-guidelines.md`

## 输出要求

- 先说明使用的是本地已保存记录，还是本轮新录入的信息
- 连接失败时明确指出是地址、端口、用户名、密码还是环境问题待确认
- 诊断类回答按”结论 / 证据 / 推断 / 下一步”输出
- 不要在失败后依次试错不同的密码传递参数（仅适用于 Linux/macOS 下的 sshpass）
- 不默认执行高风险命令；涉及写操作、重启、删除、停止服务时必须先征求用户确认
- 本地状态文件统一按无 BOM UTF-8 写入；读取时兼容历史 BOM 文件，不能因编码头导致主链中断
