---
name: spacemit-robot-remote
description: SpacemiT Robot SDK 远程开发基础 skill；用于 SSH 连通性检查、远程 SDK root 检查、板端命令执行，以及 remote/hybrid 模式下的只读诊断。
---

# SpacemiT Robot Remote

先按 `spacemit-robot-shared` 确认 mode、`SROBOTIS_REMOTE` 和 `SROBOTIS_REMOTE_ROOT`。

## Rules

- `remote` 和 `hybrid` 的构建、运行、测试都在板端执行。
- 不写死 host、用户名、端口、target 或 SDK root。
- 不依赖 Python、bash helper 或仓库内脚本；agent 直接使用系统 SSH 客户端执行用户确认后的命令。
- 只读环境检查可以直接执行；会修改板端文件、安装依赖、启动服务、占用设备或移动硬件的命令需要先说明影响并确认。
- 远程 SDK root 必须至少包含 `build/`、`components/`、`application/`、`target/`。

## SSH Identity

SSH 身份来自用户请求、环境变量、项目配置、全局配置或 SSH config，不要假设默认用户名、IP、端口或私钥。

可识别的信息：

- `SROBOTIS_REMOTE`: SSH 目标，可以是 `user@host`，也可以是 `~/.ssh/config` 里的 Host alias。
- `SROBOTIS_REMOTE_PORT`: 可选端口；未指定时使用 SSH 默认端口。
- `SROBOTIS_REMOTE_KEY`: 可选私钥路径；未指定时使用系统 SSH agent、默认私钥或 SSH config。

如果缺少用户名、host 或可用 Host alias，先询问用户。不要把 `bianbu`、固定 IP 或固定 key path 写进命令示例。

## Passwordless SSH

先检查是否已经免密可用：

```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 "<ssh-target>" 'echo ok'
```

如果指定了端口或私钥，把对应参数加到 `ssh` 命令中：

```bash
ssh -i "<private-key>" -p "<port>" -o BatchMode=yes -o ConnectTimeout=5 "<ssh-target>" 'echo ok'
```

检查失败时，先说明当前缺少免密登录，再让用户选择已有 SSH 配置、已有私钥，或创建新 key。不要要求用户把密码写进 prompt，不要保存密码，不要打印私钥内容。

创建新 key 或写入远端 `authorized_keys` 前必须确认。默认新 key 示例：

```bash
ssh-keygen -t ed25519 -f ~/.ssh/spacemit_robot_ed25519 -C "spacemit-robot"
chmod 700 ~/.ssh
chmod 600 ~/.ssh/spacemit_robot_ed25519
chmod 644 ~/.ssh/spacemit_robot_ed25519.pub
```

安装公钥优先使用 `ssh-copy-id`；用户可能需要在终端交互式输入一次远端密码：

```bash
ssh-copy-id -i ~/.ssh/spacemit_robot_ed25519.pub "<ssh-target>"
```

如果端口不是默认端口：

```bash
ssh-copy-id -i ~/.ssh/spacemit_robot_ed25519.pub -p "<port>" "<ssh-target>"
```

`ssh-copy-id` 不可用时，先说明替代方式会修改远端 `~/.ssh/authorized_keys`，经用户确认后再执行等价追加；不要覆盖已有 `authorized_keys`。

远端主机首次连接可能涉及 host key 确认。不要默认关闭 `StrictHostKeyChecking`；如果需要写入 `known_hosts`，先展示目标 host/port 并让用户确认。

## Command Guidance

远程执行前必须先进入 `SROBOTIS_REMOTE_ROOT`，并确认 `build/`、`components/`、`application/`、`target/` 都存在；确认通过后再执行用户请求的构建、运行或诊断命令。下面只是结构示例，实际 host、root 和命令来自 shared 的配置解析结果：

```bash
ssh "<user@host>" '
  cd "<remote-sdk-root>" || exit 1
  test -d build || exit 1
  test -d components || exit 1
  test -d application || exit 1
  test -d target || exit 1
  # run the requested command here
'
```

需要 SDK 环境时，在远端 SDK root 内先执行 `source build/envsetup.sh`，再执行具体任务。Windows PC 场景优先使用系统 OpenSSH、Git Bash、WSL 或 agent 自带的远程执行能力；不要要求用户额外安装 Python。

## Flow

1. 解析配置来源，确认 `SROBOTIS_REMOTE` 和 `SROBOTIS_REMOTE_ROOT`。
2. 解析 SSH target、端口和私钥；缺少用户名、host 或 Host alias 时先询问用户。
3. 用 `BatchMode=yes` 检查免密 SSH 是否可用；不可用时按 Passwordless SSH 规则处理。
4. 检查远端 SDK root 是否完整。
5. 需要 SDK 环境时，进入远端 root 后执行 `source build/envsetup.sh`。
6. 执行用户要求的命令，并返回命令、退出码、关键输出和失败点。

日常开发验证不默认调用 `scripts/test/robot-test`；只有 CI、回归验证或用户明确要求时才使用。
