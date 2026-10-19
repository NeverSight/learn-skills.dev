---
name: fnos-cli
description: "使用 fnos-cli 授权并管理 fnOS 设备的文件、照片、应用、Docker、下载、日志、监控、网络、存储、用户和百度网盘。用户提到 fnOS、飞牛系统或国内版设备时使用；不适用于国际版设备或 Media API。"
---

# fnOS

使用 `fnos-cli` 管理设备。安装与升级都是显式操作；执行前检查实际版本和命令帮助。

<!-- standalone:start -->
## 独立 Skill 启动器

从当前加载的 Skill 目录定位 `scripts/fnos-cli`（macOS/Linux）或 `scripts/fnos-cli.cmd`（Windows），使用绝对路径。将本 Skill 示例中的 `fnos-cli` 替换为该路径，保留每个参数及其引号。先执行 `--version` 和相关 `--help`。

首次执行自动下载本机所需的一份固定版本 CLI；提示写入 stderr，成功后复用当前用户缓存。独立执行无需 Node/npm 或全局 CLI。macOS/Linux 需要系统的 curl、gzip、SHA-256 工具（sha256sum 或 shasum）及常用 shell 工具。下载失败、缓存损坏或镜像配置请读[首次运行指南](runtime-setup.md)，按其中步骤恢复后重试原命令。更新 Skill 是显式操作，已有入口不自动升级。

Windows 可在 PowerShell 5.1 或 7 中调用 `scripts/fnos-cli.ps1`；`.cmd` 入口使用系统 Windows PowerShell。按当前 shell 规则传递参数，PowerShell 的 JSON 参数建议用单引号。Windows 使用系统 .NET 下载和解压，不需要 Unix 工具；缺少 PowerShell 或执行策略阻止启动时先处理本机环境，再重试原入口。
<!-- standalone:end -->

## 授权与连接

登录、profile、连接失败及授权恢复先读[连接入口](entries/trim-shared.md)和 [OAuth 指南](reference/oauth.md)。字段约定见[公共约定](reference/_conventions.md)，模块使用方式见[索引](reference/_index.md)。

1. Agent 在用户指定的目标和 profile 执行 `login --authorize-only`，把返回链接交给用户。
2. 用户自行在浏览器登录并授权，把一次性 code 主动发回。用户无需运行终端。
3. Agent 在同一执行主机、系统用户、配置环境、profile 和连接参数下执行 `login --code`。确认令牌已保存并执行只读验证后才报告连接成功。

```bash
fnos-cli --profile home --host <host> --port <port> login --authorize-only
fnos-cli --profile home --host <host> --port <port> login --code '<code>'
fnos-cli --profile home system info
```

用户密码、2FA 和浏览器确认由用户处理。只接收用户主动发来的 code，不复述、额外落盘或转发。code 可能留在聊天、工具调用和进程参数中；不能承诺无留存。token 与 PKCE verifier 留在 CLI 受控存储，不输出到聊天。

## 使用规则

- 两产品的命令、配置、profile 与登录状态独立。新版需重新授权，不读取或迁移旧登录数据，也不自动删除旧凭据。
- 只使用本产品的 `FNOS_CLI_*` 配置变量。没有显式连接参数时，仅恢复当前产品、当前 profile 的目标；无记录时使用 `localhost:5666`。
- 文件写操作默认使用具体 `/vol{n}/...` 路径。高风险操作须核实用户意图及命令的 `--yes` 要求；不把设备验收变成默认写操作。
- `raw` 仅对内置审计过的只读端点免除 `--yes`；未知端点名称不能证明只读。
- CLI 和 Skill 来自同一版本的包。首次安装、升级或公开文档变化后检查实际 `--version` 和相关 `--help`，不假定 `latest` 已完成传播。

## 命令与任务一览

- [连接与授权](entries/trim-shared.md): 登录、选择连接目标或 profile、排查登录状态和连接问题，以及应用通用安全规则时使用。
- [文件](entries/trim-file.md): 列出或搜索文件、上传本地文件、检查共享目录和 ACL，或判断当前用户目录与 NAS 路径语义时使用。
- [照片](entries/trim-photos.md): 浏览相册扫描目录、搜索照片、查看详情，以及获取缩略图或原图预览地址时使用。
- [应用中心](entries/trim-app.md): 管理已安装应用、应用中心安装、FPK 软件包、更新、应用入口与生命周期操作。
- [Docker](entries/trim-docker.md): 查看和管理 Docker 镜像、容器、Compose 项目及长时间运行的生命周期操作。
- [下载](entries/trim-download.md): 列出、搜索、创建和控制下载任务，查看任务文件、统计和状态变化。
- [百度网盘](entries/trim-baidu-netdisk.md): 检查百度网盘授权、容量、云端文件、分享保存、NAS 传输和定时同步。
- [日志](entries/trim-log.md): 浏览筛选日志、列举日志模块、清除或导出记录、配置归档，并复制或取消诊断日志。
- [监控](entries/trim-monitor.md): 查看 CPU、内存、网络、磁盘、进程、服务、电池、风扇、GPU/NPU 与蜂鸣器告警等运行时指标。
- [网络](entries/trim-network.md): 管理网络服务开关，包括开启或关闭 SSH，并确认写操作的授权要求。
- [存储](entries/trim-storage.md): 查看存储池、磁盘与 SMART 数据，或执行挂载、扩容、磁盘替换、格式化等高风险存储写操作。
- [系统与电源](entries/trim-system.md): 查看静态系统标识、机型、版本、卷、硬件和电源计划，或重启、关闭设备。
- [用户与权限](entries/trim-user.md): 查看用户、组、登录设备和当前权限，管理用户，或选择正确的已授权 profile。
