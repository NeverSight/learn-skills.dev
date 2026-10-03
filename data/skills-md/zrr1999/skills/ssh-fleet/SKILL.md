---
name: ssh-fleet
description: >
  管理私有 SSH 设备清单、连接元数据和已验证 host key，并通过 auto-config 安全校验和渲染 SSH、Ansible、DDNS 或 hosts 输出。只要用户要求新增、修改、查找、审计、退役远程机器，维护 devices.toml/known_hosts，处理 SSH alias/hostname/user/port/ForwardAgent，或生成、比较、应用 fleet 配置，就应使用。默认只读且不连接远端；inventory、trust、连接和 apply 权限在本 skill 内彼此独立，Git 拓扑与交付统一交给 git-workstreams，二者权限互不推导。
---

# SSH Fleet

## Goal

维护一个私有、可 diff、严格校验的设备事实源；生成配置只是可审阅输出。完成时说明使用的 inventory 路径、涉及的设备名、做过的校验，以及哪些连接、应用或信任动作没有获得授权而保持未执行；仓库修改的 Git 交付由 `git-workstreams` 另行判定和报告。

需要字段定义或 TOML 示例时读取 `references/device-schema.md`。

## Resolve the fact source

按以下优先级解析根目录：

1. 用户明确给出的路径；
2. `SSH_FLEET_ROOT`；
3. `~/workspace/zrr1999/fleet-config`。

根目录内只有两个权威事实面：

- `devices.toml`：活动设备、连接能力与地址来源；
- `trust/known_hosts`：经过独立渠道核验的 SSH host key。

生成的 `~/.ssh/config`、Ansible inventory、DNS manager JSON、hosts 文件和命令输出都不是事实源。不要在别处维护第二份设备清单。

## Authorization boundaries

把领域动作拆开，不用一个许可推导另一个许可。Git 拓扑与交付由 `git-workstreams` 按用户显式终点和仓库现场判断；本节的 inventory、trust、连接和 apply 权限不授予 Git 权限，Git 交付也不授予这些领域权限。

- **本地读取和审计**：可检查 inventory、生成器代码、Git 状态、现有 SSH 配置和 `ssh -G` 解析结果；不连接设备。
- **编辑 inventory**：用户要求新增、修改、迁移或退役设备时，才修改 `devices.toml`。这不授权连接或应用生成文件。
- **信任更新**：只有用户要求新增或轮换 host key，且指纹已通过独立可信渠道核验时，才修改 `trust/known_hosts`。`ssh-keyscan` 只能采集候选 key，不能单独建立信任。
- **远程连接**：只有用户明确要求连接、调查或操作目标设备时才执行 SSH；先解析精确 alias、目标与信任状态，不用 `StrictHostKeyChecking=no` 绕过缺口。
- **应用生成配置**：只有用户明确要求 apply 时，才把已审阅输出写入 live 路径。render 或 diff 不等于 apply。
- **Git 交付**：交给 `git-workstreams`，不在本 skill 另设 commit/push 默认值。领域授权与 Git 交付互不推导。用户明确要求不提交、不推送或仅本地时，仍停在该边界；否则由 `git-workstreams` 按显式终点和仓库现场决定仅本地、commit、push 或 Draft PR。

任何阶段都不得输出或提交私钥、密码、token、agent socket、`.env`、临时命令输出或未筛选的密钥材料。

## Inspect before change

1. 确认根目录是预期的 private Git 仓库，并检查 branch、upstream、dirty/untracked 状态；保留用户已有改动。
2. 读取完整 `devices.toml` 和与目标相关的 `known_hosts` 行，确认设备 `name`、hostname、group 和引用关系。
3. 检查本机 `auto-config --help`、`validate --help` 与 `render --help`；精确 CLI 语法以当前版本为准。
4. 若用户只要求审计或设计，到这里保持只读；不要顺带修复、连接或应用。

## Add or update a device

1. 使用稳定的 `name`；hostname、地址、操作系统或用途变化时不要改名。`name` 同时是生成的 OpenSSH `Host` alias。
2. `group` 只表示一个主运维边界。只有生成器确实需要筛选时才添加 `tags`，不要恢复 `roles`、Ansible aliases 或多个布尔角色字段。
3. 只写存在的能力：不可 SSH 的设备省略 `ssh`，没有受管地址的设备省略 `addresses`。默认端口 `22` 和 `forward_agent = false` 不重复写。
4. 先完成整文件编辑，再运行严格校验。重复 name、未知字段、非法地址或域名、坏引用必须让整个操作失败；不能跳过单台设备继续。
5. render 到 `mktemp -d` 或仓库忽略的目录，审阅全部输出。对受影响 alias 使用 `ssh -G -F <rendered-ssh-config> <name>` 验证解析；这个命令不建立网络连接。
6. 报告 diff 和验证结果。没有 apply 授权时停在这里。

## Retire a device

从活动 `devices.toml` 删除完整记录；Git 历史承担审计，不为简单 active/retired 状态保留 `lifecycle` 字段。然后严格校验和 render，确认所有预期输出都移除该设备。

不要因为删除设备记录就自动删除分支、DNS 记录、live SSH 配置、远端账号或 `trust/known_hosts` 条目。每种外部状态由对应 apply/远程/信任动作单独授权和验证。

## Trust changes

新增或轮换 host key 时记录精确 hostname 与 key 类型，核对是否存在 hashed、带端口或旧算法形式。通过控制台、设备管理面、供应商面板或另一个已信任通道比对 fingerprint 后再编辑 `trust/known_hosts`。

若只能获得 `ssh-keyscan` 结果，保存为临时候选并报告待核验 fingerprint；不要提交为已信任 key，也不要通过关闭检查来连接。轮换时保留变更前后的证据和受影响 alias，避免把连接劫持误认为正常换钥。

## Apply and verify

获得 apply 授权后，也只应用刚刚严格校验和审阅的 render 结果。应用前再次确认目标路径、现有文件来源和备份/回滚方式；使用原子替换，保持 SSH 配置权限，并避免覆盖不属于 auto-config 的手写 block。

应用后先运行语法和展开检查，再在用户已授权连接时做真实连接验证。`ssh -G` 成功只证明配置解析，不证明网络、凭据或 host key 正确。

## Output

更新类请求报告：事实源、设备 name、字段变化、整文件校验、render 目录、受影响输出与 `ssh -G` 结果。审计类请求报告：现状、风险和建议，不制造改动。明确列出未执行的远程连接、live apply 和 trust 变更；Git 交付终点及未执行的 commit/push/PR 由 `git-workstreams` 报告。
