---
name: re-forensics
type: gateway
description: >
  内存取证/威胁情报网关。编排：转储来源 → 内存取证 → 线索提取 → 情报关联。
  子技能：[[re-mem-forensics]] [[re-disk-forensics]] [[re-ti]]、[[re-attribution]]、[[re-hunting]]、[[re-mobile-forensics]]。
  触发词：内存取证、memdump分析、威胁情报、样本背景、VirusTotal、MISP、forensics、threat intelligence。
capabilities: [memory-forensics, threat-intel, mobile-forensics]
---

# 内存取证与威胁情报

## 完整工作流

1. 转储来源：默认转储优先——先确认有没有现成 dump。**按取证层级分流**：整机镜像（LiME/AVML/崩溃转储等，Volatility 可解析）→ 内存取证分支；进程级 `gcore` 产物是单进程 ELF core（无内核结构，Volatility 整机插件不可解析）→ 只走进程级复盘（gdb/`eu-stack`，见 [[re-memdump]]（能力：`memory-dump`） 步骤 3），不进 [[re-mem-forensics]]（能力：`memory-forensics`）。转储按 [[re-memdump]]（能力：`memory-dump`） 执行（脱壳样本须等 OEP 解密后，转储前按 `/proc/<pid>/maps` 过滤 `[vsyscall]`/`[vdso]`，见 [[re-analyze/platform-tips]]「直读 vs 转储」决策表与 Linux 内存转储极端段）
2. 内存取证：[[re-mem-forensics]]（能力：`memory-forensics`） —— 确认 dump 来源与架构 → 进程列表（pslist）→ 网络连接（netscan）→ 注入/异常（dlllist/malfind）→ 凭据线索（hashdump/lsadump）与可疑对象提取
3. 线索提取：从内存取证产物里整理线索——可疑进程/注入地址/网络回连/凭据哈希/提取出的对象（模块、shellcode、明文密钥），每项记证据路径与时间戳（取证要求可追溯，见 [[re-analyze/platform-tips]]）
4. 情报关联：[[re-ti]]（能力：`threat-intel`） —— 用线索中的哈希/域名/IP 查 VirusTotal / Any.run / hybrid-analysis，家族与团伙关联，结果进 [[re-ioc]]（能力：`threat-intel`） 的 IOC 列表与报告

每步产物（dump、插件输出、提取对象）按 sha256 + 路径存档，供报告与 [[re-ioc]]（能力：`threat-intel`） 引用。

## 何时用哪个原子技能（选择树）

按输入特征/目标分支：

- **已有 dump 或进程已死（有 .raw/.mem/.core）** → [[re-mem-forensics]]（能力：`memory-forensics`；进程/网络/注入/凭据线索）
- **没有 dump 需要现场取** → 先 [[re-memdump]]（能力：`memory-dump`；默认转储优先）→ 回 [[re-mem-forensics]]（能力：`memory-forensics`）
- **要查样本背景（"这个 hash/域名/IP 是什么""哪个家族"）** → [[re-ti]]（能力：`threat-intel`；VT/Any.run/hybrid-analysis/MISP）
- **磁盘/文件系统取证（删除恢复、时间线、可疑文件定位）** → [[re-disk-forensics]]（能力：`disk-forensics`；磁盘侧取证，与 [[re-mem-forensics]]（能力：`memory-forensics`） 内存侧并列）
- **内存分析找到可疑对象/回连后需要深挖** → 可疑模块/shellcode 转 [[re-binary-core]]（能力：`decompilation`、`debugging`、`memory-dump`、`elf-parser`、`pe-parser`、`macho-parser`；[[re-ghidra]]（能力：`decompilation`、`debugging`） / [[re-ida]]（能力：`decompilation`、`debugging`） 静态）；回连行为验证转 [[re-malware]]（能力：`malware-behavior`、`document-malware`、`evasion-analysis`、`key-extraction`、`threat-intel`；沙箱）
- **只做文件静态分析，不涉及内存** → 不是本网关，转 [[re-binary-core]]（能力：`decompilation`、`debugging`、`memory-dump`、`elf-parser`、`pe-parser`、`macho-parser`） / [[re-malware]]（能力：`malware-behavior`、`document-malware`、`evasion-analysis`、`key-extraction`、`threat-intel`）
- **容器镜像（docker save/skopeo 导出的镜像 tar）** → 下方「容器镜像取证」章节

## 容器镜像取证

- **镜像结构**：tar 归档 + 分层（每层 = 文件系统快照差异；`docker save` / `skopeo copy` 导出）
- **层提取**：解包层归档 → 逐层文件系统分析（复用 [[re-disk-forensics]] / [[re-fw-rootfs]] 的方法：文件枚举、删除文件恢复）
- **分析重点**：配置与密钥（环境变量、挂载点、entrypoint/CMD 脚本）、历史层残留（删除的文件在旧层仍可恢复）、恶意镜像判定（启动命令、网络行为、可疑二进制）
- **输出**：镜像内容清单 + 可疑项列表（与 [[re-ioc]] 的指标提取衔接）

## 跨域联合

- 本网关被 [[re-malware]] 深度分析路径引用——行为分析后需查内存残留（注入、内存中的载荷、凭据）时转 [[re-forensics]]；情报关联结果回传 [[re-malware]] 佐证家族判定
- 磁盘侧取证 [[re-disk-forensics]] 与内存侧 [[re-mem-forensics]] 并列——磁盘证据（删除文件/时间线）与内存证据（进程/网络/凭据）互相佐证
- 转储产物来自 [[re-memdump]]（默认转储优先，见 [[re-analyze/platform-tips]]）
- 情报衔接 [[re-ioc]]——[[re-ti]] 的查询结果与 [[re-mem-forensics]] 的线索汇总成 IOC 列表与报告
- 可疑对象（提取的模块/shellcode）深挖 → [[re-binary-core]]（[[re-ghidra]] / [[re-ida]] 反编译）
- 本网关被 [[re-analyze]] 的 triage「内存取证 / 情报查询」路径调用

## 常见坑与陷阱

- 跳过转储来源确认直接跑分析 → 工具与 dump 架构不匹配全错——先 [[re-memdump]] 确认来源，按 [[re-analyze/platform-tips]] 默认转储优先取完整 dump
- dump 被 vsyscall/vdso 垃圾页污染 → 分析结果偏差——转储前必须过滤极端段（[[re-analyze/platform-tips]] Linux 内存转储极端段）
- 取证结果不留证据链 → 报告不可复现——每步产物存档（路径 + sha256 + 时间戳）
- 内存线索不上报验证就下结论 → 误判——可疑对象先静态深挖（[[re-binary-core]]），背景查证走 [[re-ti]] 多重确认
