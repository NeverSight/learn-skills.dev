---
name: stackharbor
description: Use when a repository or subproject needs StackHarbor integration, YAML registration, workspace onboarding, migration from an older protocol, Docker readiness troubleshooting, or installation and upgrade of StackHarbor on macOS/Linux from GitHub releases. 适用于安装栈港、工程接入、Docker 未启动排查、服务编排与技能升级。
---

# StackHarbor installation and workspace integration

从工程实际启动契约生成 registration；技能和协议参考由 StackHarbor 代码库共同维护。支持 macOS/Linux 本地前台进程，资源、任务和服务具有不同生命周期。

## Install the application

When the user asks to install StackHarbor, follow [GitHub release installation](references/installation.md). Skill installation and binary installation are separate. Detect macOS/Linux and architecture, install a checksum-verified release without sudo, verify `--version` and `--help`, and report the actual binary path. Do not assume a skill downloaded by `npx skills add` includes the repository's root scripts.

## Docker readiness — do not skip this for Docker-backed apps

Before reporting that a Docker-backed app is ready to start, follow [Docker preflight and recovery](references/docker.md). Check the CLI, Compose plugin, selected context/endpoint, reachable engine, and required containers separately. `docker --version` does not prove the engine is running. `validate` and `plan` do not prove Docker readiness; `doctor` only runs project-declared checks.

When the user has requested starting the local app and its established runtime is Docker Desktop on macOS, starting that existing runtime is part of the requested prerequisite work: launch it, wait for a successful bounded engine probe, then proceed with the declared dependencies. Registration-only work stays read-only. Do not repeatedly ask for the same already-authorized prerequisite. Missing installation, first-run agreements, a remote endpoint, or an unknown runtime must be reported and resolved explicitly. A stopped container and a stopped Docker engine are different failures.

## 接入步骤

1. 确定目标工程根目录，读取工程指令、已有 workspace/registration、manifest、启动脚本和 Compose 配置。定位 PATH 中或用户指定的二进制，运行 `--version`、`--help` 核实能力。缺少二进制时仍可准备 YAML，但明确校验未完成；安装工具依赖需要对应授权。
2. 运行 discover，检查 diagnostics、已注册节点及待注册候选。读取命令真实调用链，确认包管理器、前台入口、cwd、端口来源、健康路径、停止信号和依赖。只记录环境变量名/文件路径，避免读取或输出秘密值；未知模块、端口或迁移状态保持待确认。
3. **新接入默认 v2**：先读 [v2 完整契约](references/v2.md)，再写 YAML。已有 v1 按 [v1 参考](references/registration.md) 保留协议和 ID；整体迁移时更新所有依赖引用。v2 节点为 `project/service/key`、`project/task/key`、`resource/key`，分别依赖 ready/started、succeeded、available。
4. 子工程优先使用旁置 `stackharbor.yaml`；集中配置放在根 `.stackharbor/` 并用 workspace 显式导入。cwd 相对注册文件且位于目标根内；workspace root/registrations 相对 workspace 文件。保留已有导入、排除项和 discover 策略；`discover: false` 必须追加新注册路径。配置默认纳入目标工程版本控制，只有用户要求本机专用时才排除。
5. 拆分混合脚本前核实独立的前台服务、Compose 身份和检查入口。仅当真实 check/run/verify、required_scope、inputs 和 PostgreSQL 目标锁契约齐全时注册 schema-write task。若缺失，列出适配缺口；保留已有 wrapper（启动时仍有原副作用），或仅接入已核实的独立服务，不编造迁移检查、不顺带改启动脚本。观察外部进程/容器使用 observe，管理资源明确 control/lifetime。
6. 对使用 Docker 的工程执行 [Docker 前置检查](references/docker.md)，明确引擎和容器状态；先把数据库、Redis 等真实前置依赖接入 DAG，再验证应用服务。非 Docker 工程跳过。
7. 执行 validate；v2 再对目标执行 plan，逐项核对闭包、依赖条件和动作，修正配置错误。报告文件变更、节点/命令/端口、校验结果、Docker 引擎与依赖就绪状态、未解决项、TUI 启动命令。配置校验成功只证明声明有效；实际启动/就绪未经执行时标明未验证。

## 快速参考

| 目的 | 命令（ROOT、NODE 替换为实际值） |
|---|---|
| 发现 | `stackharbor discover --root ROOT --json` |
| 候选草案 | `stackharbor init --root ROOT --project DIR --dry-run` |
| 声明校验 | `stackharbor validate --root ROOT --json` |
| v2 只读计划 | `stackharbor plan start --root ROOT --target NODE --json` |
| 交互入口 | `stackharbor --root ROOT`，或在工程根运行 `stackharbor` |

使用非默认 workspace 时，所有命令加 `--workspace FILE`，ROOT 与 workspace root 必须一致。init 当前生成 v1 草案；只有用户接受 v1 且候选明确时才用 `--write`，不覆盖已有文件。新 v2 接入手工生成后校验。

注册工作保持只读：执行 discover/init --dry-run/validate/plan，以及需要时的 Docker 前置观测。doctor 会执行检查脚本，task run 会执行任务及资源前置项；服务启动、迁移、依赖安装、外部端口释放需要相应操作授权。StackHarbor 不提供权限沙箱。

## 最小 v2 示例

已核实工程使用 `pnpm dev`，应用自身配置监听 3000；以下文件放在应用目录：

```yaml
version: 2
project: {id: web, name: Web}
context: {cwd: .}
services:
  dev:
    run: {command: [pnpm, dev]}
    ports: [{name: http, port: 3000}]
    ready: {tcp: "127.0.0.1:3000"}
    open: "http://127.0.0.1:3000/"
```

`web/service/dev` 是计划目标。命令使用 argv 数组；shell 语法必须显式使用 shell。

## 安装与升级

在 StackHarbor 源码或固定解压的发行目录执行 `sh scripts/install-skill.sh`，链接整目录到 `~/.agents/skills/stackharbor`；新会话发现技能。具体入口、冲突处理、升级及维护检查见 [维护参考](references/maintenance.md)。

## 常见错误

| 错误 | 正确契约 |
|---|---|
| Docker CLI 存在就认为可以启动 | 验证 Compose 插件、当前引擎可达和已声明容器健康 |
| Docker Desktop 已打开就立即启动应用 | 等待引擎探测成功，再按 DAG 启动资源并等待就绪 |
| 数据库/Redis 只写在文档里 | v2 显式注册 resource 并连接 requires，v1 使用 docker_depends_on |
| ports 声明被当成应用配置 | 应用参数/环境真正决定端口 |
| 候选脚本直接变成可执行节点 | 先读真实调用链、注册并校验 |
| 将迁移当常驻服务或臆造 checker | 使用已核实的 v2 task 契约，缺口明确报告 |
| 自动发现关闭却只添加旁置 YAML | 更新已有 workspace 的显式导入 |
| 复制技能后期待源码升级自动同步 | 安装整目录软链接并保留源目录 |
