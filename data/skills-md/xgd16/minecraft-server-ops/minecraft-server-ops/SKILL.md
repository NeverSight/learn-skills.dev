---
name: minecraft-server-ops
description: Minecraft 服务器运维专家。涵盖 Java 版（Paper/Purpur/Fabric/Forge）和基岩版（BDS/LiteLoader）服务器的搭建、插件与模组管理、性能调优、备份恢复、安全防护、常见问题排查，以及 RCON 远程操控脚本。当用户需要搭建 Minecraft 服务器、配置插件/模组、优化服务器性能、排查崩溃/延迟问题、设置自动备份、防御外挂/DDoS、进行服务器迁移、管理 Minecraft 服务端文件、通过 RCON 远程控制服务器时，使用此 skill。
---

# Minecraft 服务器运维

## 核心原则

- 优先推荐 Paper/Purpur（Java 版）或官方 BDS（基岩版），它们是性能和稳定性最好的选择
- 所有配置修改前先备份原文件
- 生产环境务必开启自动备份和日志监控
- 性能参数应基于实际硬件配置调整，不要盲目套用
- 排查问题时优先使用 RCON 或 PlugMan 软重载，避免频繁重启服务器

## 快速导航

| 任务 | 参考文件 |
|------|---------|
| Java 版服务器搭建（Paper/Purpur/Fabric/Forge） | [java-server-setup.md](references/java-server-setup.md) |
| 基岩版服务器搭建（BDS/LiteLoader） | [bedrock-server-setup.md](references/bedrock-server-setup.md) |
| 插件与模组管理 | [plugins-management.md](references/plugins-management.md) |
| 性能调优 | [performance-tuning.md](references/performance-tuning.md) |
| 备份与恢复 | [backup-recovery.md](references/backup-recovery.md) |
| 安全防护 | [security.md](references/security.md) |
| 常见问题排查 | [troubleshooting.md](references/troubleshooting.md) |
| RCON 远程控制 | [scripts/mc-rcon.py](scripts/mc-rcon.py) — 纯标准库 RCON 客户端 |

## Paper 1.21+ 配置文件结构

Paper 1.21 将配置文件拆分到 `config/` 目录：

```
server.properties          # 基础服务端配置
config/
  paper-global.yml         # 全局设置（数据包限制、代理、spark）
  paper-world-defaults.yml # 世界默认设置（实体、区块、漏斗）
spigot.yml                 # Spigot 兼容配置（视距、实体激活范围）
bukkit.yml                 # Bukkit 兼容配置
```

### 关键配置速查

**packet-limiter**（`config/paper-global.yml`）— 数据包限速，配置不当会误伤投影 mod 等辅助工具：
```yaml
packet-limiter:
  all-packets:
    action: KICK
    interval: 7.0
    max-packet-rate: 500.0        # 生存服 500-800，建筑服可放宽到 1000+
  overrides:
    minecraft:place_recipe:
      action: DROP
      interval: 4.0
      max-packet-rate: 5.0
```

**chunk-loading**（`config/paper-global.yml`）：
```yaml
chunk-loading-advanced:
  player-max-concurrent-chunk-generates: 2  # 生存服 2-4，建筑服可到 8
  player-max-concurrent-chunk-loads: 4
chunk-loading-basic:
  player-max-chunk-generate-rate: -1.0      # -1 不限速
  player-max-chunk-load-rate: 100.0
  player-max-chunk-send-rate: 75.0
```

## 快速诊断工作流

当用户报告服务器问题时，按以下顺序排查：

1. **收集信息**：服务器版本、核心类型、插件列表、近期变更
2. **查看日志**：检查 `logs/latest.log`，定位报错或警告
3. **性能分析**：运行 `/mspt` 或 timings 报告，找出延迟源
4. **内存检查**：确认堆内存分配和 GC 状态
5. **逐个排除**：二分法禁用插件/模组定位问题源
6. **反外挂兼容性**：检查 GrimAC/Spartan 是否误伤辅助 mod（见下文专节）

### GrimAC + 投影 Mod（Litematica）兼容性问题

如果玩家反馈轻松放置/自动放置无法使用，按优先级排查 GrimAC：

| 检查项 | 配置位置 | 推荐值 | 原因 |
|--------|---------|--------|------|
| `disable-default-resync-handler` | `config.yml` | **`true`** | 防止 Grim 清除 Litematica 的投影虚拟方块 |
| `TimerA.drift` | `config.yml` | **`500-800`** | 轻松放置快速发送方块包，默认 120ms 太紧 |
| `distance-to-check-if-ghostblocks` | `config.yml` | **`4`**（最大值） | 扩大 Ghost Block 检测范围 |
| `packet-spam-threshold` | `config.yml` | **`200-300`** | 100 过低时大量 Cancel 包会导致踢出 |

GrimAC 配置变更后使用 `plugman reload GrimAC` 软重载即可生效，无需重启。

## JVM 参数通用模板

Aikar 风格的 JVM 启动参数，适用于大多数 Paper/Purpur 服务器：

```bash
java -Xms8G -Xmx8G -XX:+UseG1GC -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC -XX:+AlwaysPreTouch \
  -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 \
  -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 \
  -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 \
  -XX:InitiatingHeapOccupancyPercent=15 \
  -XX:G1MixedGCLiveThresholdPercent=90 \
  -XX:G1RSetUpdatingPauseTimePercent=5 \
  -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem \
  -XX:MaxTenuringThreshold=1 \
  -jar server.jar nogui
```

- `-Xms` 和 `-Xmx` 设为相同值，避免动态扩容开销
- 堆内存建议不超过 12GB（G1GC 在大堆下效率下降）
- 始终保留 2-4GB 给操作系统
- 生产环境建议添加 GC 日志：`-Xlog:gc*:file=gc.log:time,uptime:filecount=5,filesize=10M`

## 必要插件清单

| 用途 | 推荐插件 | 备注 |
|------|---------|------|
| 权限管理 | LuckPerms | 支持多服同步 |
| 地皮保护 | WorldGuard + WorldEdit | 生存服必备 |
| 经济系统 | Vault + EssentialsX | 插件生态基石 |
| 反外挂 | GrimAC | 开源免费，预测式反作弊 |
| 登录验证 | AuthMe | 离线模式必装 |
| 区块预生成 | Chunky | 新服必须先预生成 |
| 插件热管理 | PlugManX | 支持软重载，避免重启 |
| 性能分析 | Spark | Timings + CPU 分析 + 健康报告 |
| 互通 | Geyser + Floodgate | 基岩版玩家接入 Java 服 |
| 备份 | eBackup 或自定义脚本 | 自动定时备份 |

## RCON 远程控制脚本

`scripts/mc-rcon.py` — 纯 Python 标准库实现的标准 RCON 客户端，无需第三方依赖，兼容 Java 版和基岩版。

### 快速使用

```bash
# 设置连接信息（推荐通过环境变量）
export MC_RCON_HOST=127.0.0.1
export MC_RCON_PORT=25575
export MC_RCON_PASSWORD=your_password

# 查看在线玩家
python scripts/mc-rcon.py online

# 服务器状态概览
python scripts/mc-rcon.py status

# 广播消息
python scripts/mc-rcon.py say "服务器即将重启"

# 执行任意命令
python scripts/mc-rcon.py "whitelist add Steve"

# 进入交互模式
python scripts/mc-rcon.py -i

# JSON 输出（便于脚本集成）
python scripts/mc-rcon.py --json online

# 批量执行命令文件
python scripts/mc-rcon.py -f commands.txt
```

### 支持的快捷命令

| 命令 | 说明 |
|------|------|
| `online` | 在线玩家列表 |
| `status` | 服务器状态概览（TPS/MSPT/内存/运行时间） |
| `gc` | 强制 GC + 性能报告 |
| `backup` | 保存世界并准备备份 |
| `plugins` | 插件/模组列表 |
| `say <msg>` | 广播消息 |
| `kick <player> [reason]` | 踢出玩家 |
| `ban <player> [reason]` | 封禁玩家 |
| `pardon <player>` | 解封玩家 |
| `tp <player> <target>` | 传送玩家 |
| `give <player> <item> [count]` | 给予物品 |
| `time set\|add\|query [value]` | 时间控制 |
| `weather <type>` | 天气设置 |
| `difficulty <level>` | 难度设置 |
| `gamerule <rule> [value]` | 游戏规则 |
| `whitelist add\|remove <player>` | 白名单管理 |
| `op\|deop <player>` | OP 管理 |

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MC_RCON_HOST` | `127.0.0.1` | RCON 主机地址 |
| `MC_RCON_PORT` | `25575` | RCON 端口 |
| `MC_RCON_PASSWORD` | (必填) | RCON 密码 |
| `MC_RCON_TIMEOUT` | `10` | 连接超时秒数 |

### 启用服务器 RCON

**Java 版** (`server.properties`):
```properties
enable-rcon=true
rcon.port=25575
rcon.password=your_secure_password
```

**基岩版** (`server.properties`):
```properties
enable-lan-visibility=false
server-port=19132
```
基岩版需额外安装 RCON 插件或使用 BDS 自带 RCON。

### 远端服务器 RCON 使用

当 RCON 绑定在服务器 localhost 时，可先 SSH 登录后将脚本传到服务器执行：

```bash
# 将脚本传上服务器
scp scripts/mc-rcon.py user@server:/tmp/mc-rcon.py

# SSH 执行
ssh user@server "MC_RCON_PASSWORD=xxx python3 /tmp/mc-rcon.py list"
```

或直接在 SSH 会话中用 Python 构建 RCON 连接（标准协议 type 3 认证 + type 2 命令）。
