---
name: re-sample-acquire
description: >
  样本现场采集（从现象到可用样本）：目标没有独立进程、样本不落盘时，以「异常执行内存 + 到达该内存的执行上下文」为核心定位载体并运行时提取。
  覆盖四种观测模型：Windows（VAD/线程/ETW）、Linux（VMA/BPF LSM）、macOS（Mach VM/Endpoint Security）、seL4（capability provenance）。
  触发词：样本获取、现场采集、没有样本、只有现象、不落盘、无文件、注入、内存马、运行时捕获、内存提取样本。
  English triggers: sample acquisition, live acquisition, no sample, fileless, injected code, memory-resident, runtime capture.
capabilities: [sample-acquisition]
---

# 样本现场采集（从现象到可用样本）

<CORE RULE>
**不猜进程名、不以「找到进程」为第一目标**——找「异常执行内存」+「到达这块内存的执行上下文」。
检测基于**最终的内存 artifact**，不依赖"样本用了哪个注入 API"（未知注入方法也可能被 artifact 检出；hook 到某个 API 不等于覆盖了全部注入方式）。
**先问 provenance：这块可执行内存是谁创建的、通过什么路径进来的、谁持有映射权限**——再谈它属于哪个进程。
</CORE RULE>

## 任务分类器（intent → 路径）

| 用户目的 | 路径 |
|---|---|
| 只有现象描述（"某程序不落盘""行为异常"），没有样本文件 | → 步骤 1（异常执行区扫描）→ 2（执行上下文归属）→ 4（dump 整区） |
| 已知进程，但磁盘上没有样本文件（注入/内存驻留） | → 步骤 2 → 4 |
| 服务端常驻载荷（Web 中间件/Java 等，请求触发） | → 平台分支的"服务端"节（内存马） |
| 载荷疑似驱动/内核态（读写内存类外挂/rootkit） | → [[platform-windows]] 内核侧 |
| 嵌入式/微内核目标（seL4 系统） | → [[platform-sel4]]（capability provenance 路线） |
| 有回连/下载行为，想拿原始样本 | → 步骤 7（网络与落盘侧） |

## 入口判定（Decision Gate）—— 平台 × 形态

```
现场采集
├─ 已有样本文件（磁盘上有）→ 不需要本技能，直接 [[re-triage]] 初勘
├─ Windows 目标 → [[platform-windows]]（VAD/region + 线程 + 模块链 + ETW/Sysmon）
├─ Linux 目标   → [[platform-linux]]（VMA + mmap/mprotect 追踪 + process_vm_readv）
├─ macOS 目标   → [[platform-macos]]（Mach task VM + Endpoint Security）
├─ seL4 目标    → [[platform-sel4]]（capability/VSpace 审计，不是"扫描进程"）
└─ 不知平台/跨平台 → 先按步骤 1 的平台无关判据走，再进对应分支
```

**平台观测模型不同，方法不能机械翻译**（下表是各分支的分工，不是同义替换）：

| 平台 | 观测对象 | 事件源（trigger） | 读取（ground truth） | 权限模型 |
|---|---|---|---|---|
| Windows | 进程 VAD/region + 线程 + 模块链 | Sysmon 8/10/25、ETW（含 Threat-Intelligence）、内核回调 | `VirtualQueryEx` / `ReadProcessMemory` / PE-sieve | 管理员 + 调试权限 |
| Linux | 进程 VMA（`/proc/<pid>/maps`） | tracepoint/kprobe、**BPF LSM**（`file_mprotect` 等 hook） | `process_vm_readv()` / ptrace / gcore | ptrace access check（含 Yama） |
| macOS | Mach task + VM region | **Endpoint Security**（MMAP/MPROTECT/REMOTE_THREAD_CREATE/GET_TASK） | `mach_vm_read` / `mach_vm_read_overwrite`（需 task port） | SIP / Hardened Runtime / task port 授权 |
| seL4 | capability（VSpace / frame / TCB） | **fault endpoint** + 系统构造期记录 | 无 capability 即无访问权 | capability 制（不存在"root 全读"模型） |

## 何时使用 / 何时不用

- 用：分析目标**没有可分析的文件**——只有现象（不落盘、内存驻留、寄生在别的进程里），需要先把它变成"能分析的样本"
- 用：载荷只在内存、时机很短（一次性解密、用后自清除、缓冲复用）
- **适用场景（不限外挂）**：无文件恶意软件 / 反射加载载荷 / 内存马（服务端）/ APT 内存驻留 / 勒索与窃密的前置加载阶段 / 游戏外挂（用户态与驱动）/ 微内核与嵌入式系统上的未授权可执行页
- 不用：已有样本文件（[[re-triage]]）；整机镜像取证（[[re-mem-forensics]]，离线镜像的 malfind 式排查属那边）；设备备份解析（[[re-mobile-forensics]]）；"给定 PID 怎么转储"（[[re-memdump]]）
- **授权边界（红线）**：只对**自有或已获书面授权**的设备/系统采集（`RE_AUTH` = `owned` / `research`）。采集动作本身（枚举、hook、读内存、dump、加载监控组件）痕迹明显，会触发反作弊 / EDR / 业务监控；生产环境或他人设备上执行属越权，先确认授权与停止条件
- 边界：本技能只做**采集**，不做对目标检测系统的隐匿（隐匿属 [[re-evasion]] 域，且仅限授权场景）

## 工具准备

### Windows

- **PE-sieve / HollowsHunter**（本技能的参考实现：按内存 artifact 检测 injected/replaced PE、shellcode、inline hooks、patches，支持线程调用栈扫描）——GitHub releases（`hasherezade/pe-sieve`、`hasherezade/hollows_hunter`），核对 release 页 sha256；验证 `pe-sieve.exe /help`
- **System Informer**（原 Process Hacker）/ **Process Explorer**：全进程 region/线程/句柄视图
- **procdump**（Sysinternals）：`procdump -ma <pid> out.dmp`；验证 `procdump -?`
- **Sysmon**（Event 8/10/25，见 [[re-behavior]] 行为监控一节）；**frida**（[[re-frida]]，脚本模板 [[re-frida/frida-scripts]]）
- 详见 [[platform-windows]]

### Linux

- `/proc` 解析（python3，[[re-python]]）、`gdb`/`gcore`（[[re-memdump]]）、`bpftrace`/`perf`/BPF LSM（[[re-ebpf]]）、`frida`
- 验证: `cat /proc/<pid>/maps | head` 能看到 VMA 的地址/权限/backing pathname
- 详见 [[platform-linux]]

### macOS

- `lldb` / `vmmap` / `otool`（[[re-lldb]]、[[re-format-macho]]）；Mach VM API（`mach_vm_region*` / `mach_vm_read*`，需 task port）；Endpoint Security 客户端（需 entitlement 与用户授权）
- 注意：**SIP + Hardened Runtime 下不是 root 就能读**——见 [[platform-macos]] 权限边界
- 详见 [[platform-macos]]

### seL4 / 微内核

- 无通用现成工具：需在系统构造期由 security monitor 记录 provenance（capability 路线），方法与检查清单见 [[platform-sel4]]

## 操作步骤（平台无关主干）

各步的平台对应实现见对应平台分支；此处只列**做什么与判据**。

1. **扫描异常执行区**（不猜 PID，先扫面）：
   - 枚举目标的执行内存单元并筛"可执行"：Windows = VAD/region（`VirtualQueryEx`/`NtQueryVirtualMemory`）；Linux = VMA（`/proc/<pid>/maps`，6.11+ 可用 `PROCMAP_QUERY` ioctl 高效过滤）；macOS = VM region（`vm_region_recurse_64`/`mach_vm_region*`）；seL4 = VSpace 映射审计（见分支）
   - 优先特征：**无 backing（匿名/私有）且可执行**；**保护属性转换**（W→X、RW→RWX→RX——转换瞬间即最佳捕获时机）；高熵 / 可执行格式特征（PE/Mach-O/ELF）；无已知 JIT/运行时来源
   - **不要只查"私有/无背书"**：文件背书的内存同样可被利用（Windows `MEM_IMAGE` + module stomping/DLL hollowing、COW 页仍报 `MEM_IMAGE`；Linux 文件背书映射被改写；macOS 文件背书 region 被 patch）
   - **映射来源 vs 结构记录交叉**：Windows 用 `VirtualQueryEx`+`NtQueryVirtualMemory` 取映射路径与 PEB 模块链比对（"有映射无模块条目"= 被摘链隐藏）；Linux 用 maps 的 pathname/inode 与 ELF 磁盘副本比对；macOS 用 dyld 记录与 VM region 比对
2. **执行上下文归属**（线程是第二强信号，且要看栈不只入口）：
   - 取每个线程的执行位置：起点（Windows `NtQueryInformationThread` + `ThreadQuerySetWin32StartAddress`；macOS thread backtrace）→ 归属到执行区；Linux 用 `/proc/<pid>/task/` 枚举线程，`stat` 的 `wchan`/`state` 作辅助线索，PC 与返回地址靠**栈回溯**（`eu-stack`/gdb）取
   - **起点正常也可能是 trampoline**：从合法模块起步后跳入无背书可执行区的做法会绕过"只看起点"的检测
   - 补三层证据：**当前 PC/RIP**、**调用栈返回地址**、**region ownership**——任一级落入异常区都提高评分
3. **运行时相关性（trigger 与 ground truth 分工）**：
   - **事件源只作「何时 dump」的触发器**：内存分配/写入/保护转换 + 可疑线程创建 + 异常模块加载——**组合判断**，不做单点告警
   - **内存扫描是「dump 什么」的 ground truth**：直系统调用、共享段映射、覆盖已有可执行区等路径都能绕过用户态 hook
   - 平台事件源：Windows = Sysmon 8/10/25 与 ETW；Linux = tracepoint/kprobe/BPF LSM；macOS = Endpoint Security；seL4 = fault endpoint
   - **顺带抓注入方/构造方**：执行注入或映射的来源（进程/驱动/构造路径）往往比被寄生的载荷更有分析价值
4. **Snapshot / Dump（不要只找 MZ/PE 头）**：
   - **保存整个可疑区域**：载荷可能本就没有可执行格式头，或**故意擦除头部**（经典：注入后擦 PE 头，靠区域定位再重建）
   - 内容分类（决定后续分析路径）：完整 PE/Mach-O/ELF / 手工映射的镜像 / 裸 shellcode / JIT 代码 / 解密后的 code blob
   - 每区记：基址 / 大小 / 保护属性及**变更历史** / 类型 / 映射来源 / 采集时间
   - **内存副本 vs 磁盘副本差异**：同名映像的磁盘文件与内存内容比对（发现 stomping、patch、擦头、代码替换）
5. **重建 / 误报评估 / 报告**：
   - 重建：手工映射镜像按节表重建；擦头载荷按区域内容恢复（标注"重建自内存，非原始文件"）
   - **误报白名单与降权**（必做）：JIT（.NET/V8/JVM/Mono）、浏览器、Wine/Proton、QEMU TCG、**安全软件自身的 hook 与 patch**、profiler、overlay、shim/hotpatch —— 它们同样产生无背书可执行内存
   - **评分而非二元判定**：无背书可执行 + 线程/PC/栈命中 + 近期 W→X + 高熵/格式特征 + 无已知运行时来源 → 高置信；单项特征不足以定性
   - 报告按 [[re-analyze/analysis-contract]] 核心字段（target_id / sha256 / evidence）——**采集方法本身也是证据**（"该区在 T 时刻为 RWX""该线程起点不在任何映射来源内"）

## 平台分支（references）

- [[platform-windows]] —— VAD/region 扫描、线程与调用栈归属、Sysmon/ETW/内核回调、PE-sieve 与 PE 重建、内核与驱动载体
- [[platform-linux]] —— VMA 枚举（`/proc/<pid>/maps`、`PROCMAP_QUERY`）、mmap/mprotect 追踪（tracepoint/kprobe/BPF LSM）、`process_vm_readv` 与 ptrace dump、ELF 内存-磁盘 diff、memfd 与 deleted 映射、JIT 误报
- [[platform-macos]] —— Mach task 与 VM region、`mach_vm_read`、Endpoint Security（MMAP/MPROTECT/REMOTE_THREAD_CREATE/GET_TASK）、Mach-O/dyld provenance、task port 与 SIP/Hardened Runtime 边界
- [[platform-sel4]] —— capability provenance、VSpace 映射审计、可执行页策略、TCB debug 与 fault endpoint——**设计期即保留 provenance**，与前三者的"事后重建"是两条路线

## 跨域联合

- [[re-memdump]]：给定 PID 的转储执行（本技能负责"扫哪个、dump 什么"）
- [[re-mem-forensics]]：离线整机镜像的排查（本技能是在线/现场侧）；[[re-fileless]] / [[re-loader]]：采集产物的分析
- [[re-frida]]：跨平台执行层；[[re-java]]：服务端内存马；[[re-kernel]] / [[re-ebpf]]：内核与内核态观测
- [[re-evasion]]：样本侧反检测（采集侧要知道自己会被看见）；[[re-malware]]：产物分析网关；[[re-triage]]：产物初勘入口
- [[re-rtos]] / [[re-tee]] / [[re-firmware]]：嵌入式与可信执行目标的相关分析（seL4 分支的系统构造视角与它们互补）

## 常见坑与陷阱（跨平台共性）

- **只 hook 用户态 API 就以为全覆盖**：直系统调用、共享段、覆盖已有可执行区都可绕过——事件源只当 trigger，内存扫描当 ground truth
- **把"无背书可执行"直接当恶意**：JIT、浏览器、Wine/Proton、QEMU TCG、安全软件自身的 hook 都产生同类区域——**是 signal 不是 verdict**，要 provenance + 执行史 + 评分
- **只查"私有/无背书"内存**：文件背书的内存同样会被利用（Windows `MEM_IMAGE`+COW，Linux/macOS 文件背书映射被改写）
- **只按可执行格式头找载荷**：载荷可能无头或**故意擦头**——保存整个区域再分类，必要时重建
- **只看线程入口**：trampoline、`SetThreadContext`、借模块内跳转指令等会绕过——PC 与调用栈一起看
- **平台权限模型误判**：macOS 不是 root 就能读（SIP/Hardened Runtime/task port）；seL4 根本没有"root 全读"这回事——按平台分支的权限边界设计采集方案
- **采集晚了**：一次性解密/用后自清除——触发点命中的**瞬间** dump，不要"先记地址、回头再读"
- **采集动作本身暴露**：枚举/hook/读内存会被反作弊、反调试与监控发现（[[re-game]] / [[re-evasion]]）——授权范围内作业，先在隔离环境做准备，动态采集一次完成
- **无痕 hook 让内存视图不可信**：影子页/硬件断点实现的无痕 hook 使"读取视图"与"执行视图"分离——多视图交叉，**视图差异本身就是证据**
- **清除早于取证**（服务端高发）：重启/杀进程会一并丢失证据——先 dump 取证，再阻断植入途径与清除
