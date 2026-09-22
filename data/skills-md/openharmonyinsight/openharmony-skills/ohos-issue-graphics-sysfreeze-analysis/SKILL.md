---
name: ohos-issue-graphics-sysfreeze-analysis
description: Use when analyzing OpenHarmony sysfreeze/appfreeze logs to diagnose process freeze and thread blocking issues. Triggers on SERVICE_BLOCK, THREAD_BLOCK_6S, IPC deadlock, task queue blocking, or when user requests sysfreeze/process stuck analysis.
metadata:
  author: openharmony
  scope: domain
  stage: issue
  domain: graphics
  capability: sysfreeze-analysis
  version: 0.1.0
  status: trial
---

# 任务与边界

## 解决的问题

分析 OpenHarmony 图形相关模块的 Sysfreeze 日志，诊断进程冻结和线程阻塞问题的根本原因。

## 输入

- Sysfreeze/Appfreeze 日志文件
- 相关源码（code/ 目录）
- 带符号表的 so 文件（lib.unstripped/ 目录）
- 可选：hilog 和 hilog_kmsg 日志

## 输出

- 故障类型确认
- 阻塞链路径
- 根本原因分析
- 优化建议

## 不适用情形

- 纯性能优化问题（无阻塞）
- 应用层逻辑错误（无系统级阻塞）
- 非图形模块相关调用栈的freeze问题
- 日志信息严重缺失无法分析

## 前置条件

用户环境提供 llvm 工具（llvm-readelf/llvm-addr2line/llvm-objdump 等）。

# 触发信号

- 用户要求分析 sysfreeze、appfreeze 日志
- 出现 SERVICE_BLOCK 或 THREAD_BLOCK 故障
- 需要追踪线程阻塞链和死锁
- 需要解析任务队列和资源状态
- 关键词：进程卡住、线程阻塞、死锁、freeze、block

# 前置检查

**确认日志完整性**
- 检查是否存在两次抓栈信息（SERVICE_WARNING/SERVICE_BLOCK 或 THREAD_BLOCK_3S/THREAD_BLOCK_6S）
- 确认 TIMESTAMP、TID 等关键字段存在

**确认符号表可用**
- 检查 lib.unstripped/ 目录是否存在带符号表的 so
- 解析命令：`llvm-addr2line -Cfpie path/to/so offset`
- 注意：`ld-musl-xxx.so` 即 `libc.so`

# 执行策略

## 1. 基本信息分析

**确认故障类型**
- 检查 `Reason` 字段，确认是 `SERVICE_BLOCK` 还是 `THREAD_BLOCK`
- 理解对应问题的检测原理和阈值

**记录关键信息**
- `TIMESTAMP`：故障发生时刻，用于在 hilog 日志中锁定时间范围
- `TID`：发生问题的线程 ID，问题分析从此线程开始

**查看整机资源状态**
- `ReclaimAvailBuffer`：整机剩余可用内存，判断是否低内存问题
  - 注意内存信息抓取时间，如果在 freeze 时间后则不具参考价值
- `ThermalLevel info`：热等级 ≥ 5 时，系统可能受热限频影响性能
- 如果存在整机资源问题且业务分析无异常，可优先考虑问题与之相关

## 2. 任务队列分析

**分析当前任务**

查看两次检测（SERVICE_WARNING/SERVICE_BLOCK，或 THREAD_BLOCK_3S/THREAD_BLOCK_6S）的 `Current Running` 任务：
- 如果两次检测任务相同：同一任务阻塞
- 如果两次检测任务不同：根据任务队列信息分析耗时较长的任务

**验证时间合理性**

假设最后一个 watchdog 任务在 T 时刻提交：
- 第一次抓栈：SERVICE_WARNING 预期时间 T+5s，THREAD_BLOCK_3S 预期时间 T+3s
- 第二次抓栈：SERVICE_BLOCK 预期时间 T+10s，THREAD_BLOCK_6S 预期时间 T+6s
- 如果实际时间与预期时间差异较大：DFX 抓取有时间偏差，可能存在低内存/高负载等整机问题

**分析任务队列**

检查各优先级任务队列（VIP、Immediate、High、Low、Idle），重点关注：
- 任务提交时间
- 任务执行时间（trigger time 开始，completeTime 完成）
- 任务优先级
- 任务提交者
- 任务名称

## 3. 阻塞链跟踪

**分析前先问自己三个问题**：
1. **阻塞类型是什么？** — 栈顶函数是等锁、等信号量、还是 IPC 调用？
2. **阻塞源头在哪里？** — 资源被谁持有，IPC 对端是谁？
3. **阻塞链是否闭合？** — 能追溯到不阻塞的最终线程吗？

根据两次抓取的调用栈分析线程阻塞关系，**分析时必须解栈**。

**重要**：分析从基本信息中的 `Tid:<TID>` 线程开始。

### 调用栈对比

**对比两次抓栈**
- 两次抓栈一致：卡在同一业务
- 两次抓栈不一致：可能抓到不同任务的两次瞬时栈，或者未卡住但执行时间长的同一任务

**分析线程状态**（如果有）
- 查看线程状态字段：`state`、`utime`、`stime`、`priority`、`nice`、`clk`
- 关键判断：
  - 如果线程栈顶未等待资源/陷入内核但未处于执行状态（state=S）：可能是整机问题（低内存/IO 问题等）导致
  - 结合 `utime`/`stime` 和抓栈时间间隔，确定线程在用户态和内核态的执行时长
  - 对比两次抓栈的运行时间，如果无变化则说明线程未被调度

**分析堆栈阻塞模式**

识别栈顶的阻塞函数，参考 [常见阻塞模式](references/blocking-patterns.md)

### 阻塞链分析

**识别阻塞类型**
- 根据栈顶函数判断阻塞原因（等锁、信号量、IPC 调用等）

**查找阻塞源头**
- 栈顶等锁/信号量/条件变量：找到当前等待资源的持有线程或触发线程
- 栈顶为 IPC 调用：找到 IPC 对端线程
- 阻塞线程通常与被阻塞栈顶在同一 so 或同一个类的业务中

**递归分析阻塞**
- 如果阻塞线程也处于阻塞条件，继续分析阻塞其的线程
- 直到找到不处于阻塞状态的线程，作为最终问题线程

**如果是IPC 阻塞处理**
- 查看 `BinderCatcher` 信息，获取源为 `当前进程号:当前线程号` 的同步调用
- 查看阻塞时间
- 查看 `对端进程号:对端线程号` 信息，查找 `PeerBinder Stacktrace` 中对应的进程抓栈
- 从对端线程号对应的线程开始分析阻塞情况

## 4. 流水日志分析（如果有日志）

**获取流水日志**
- 检查是否存在 `hilog` 和 `hilog_kmsg` 文件

**分析流水日志**
- 分析在 `TIMESTAMP` 问题发生时间附近的日志
- 识别可能相关的异常日志，参考 [常见流水日志](references/hilog-refernce.md)
- 识别业务场景和操作流程

## 5. 综合分析与报告

**确定根本原因**
- 综合堆栈信息、任务队列、线程状态、资源状态
- 判断问题的相关业务信息，或者相关的整机问题

**绘制阻塞路径**
- 描述从阻塞线程开始到最终问题线程的完整调用链
- 标注关键阻塞点和等待的资源

**分析业务信息**
- 解析堆栈对应的业务代码
- 结合关键日志，说明卡住的业务场景和操作流程

**生成分析报告**
- 故障分析总结
- 阻塞路径分析
- 问题根本原因（如果结果不完整，则给出下一步排查方向）
- 建议优化方向

**重要**：完成分析后生成报告并保存到文档。

# 禁止做法

**不要跳过解栈步骤**
- 错误做法：直接根据 so 名称和偏移猜测业务逻辑
- 原因：函数名和偏移对应的代码行号是定位问题的关键，不解栈会导致分析方向错误

**不要忽略整机资源状态**
- 错误做法：只关注业务堆栈，忽略内存、温度等资源信息
- 原因：低内存、过热等整机问题可能是真正的根因

**不要孤立分析单个线程**
- 错误做法：只分析问题线程的堆栈，不追溯阻塞链
- 原因：阻塞通常是由锁竞争或 IPC 调用链导致，需要找到最终的问题线程

**不要在信息不足时强行下结论**
- 错误做法：缺少符号表或日志时仍给出确定的根因
- 原因：错误的分析结论会误导后续排查方向

**不要忽略时间信息**
- 错误做法：忽略两次抓栈的时间差、任务提交时间
- 原因：时间信息可判断是否为瞬时阻塞、DFX 抓取是否正常

# 异常与回退

**信息不足时的处理**

| 缺失信息 | 处理方式 |
|----------|----------|
| 符号表不存在 | 指出需要哪些 so 的符号表，无法精确定位代码行号 |
| 只有一次抓栈 | 说明缺少对比信息，无法判断是否同一任务阻塞 |
| hilog 缺失 | 仅依赖堆栈和任务队列分析，报告中标注日志缺失 |
| BinderCatcher 缺失 | IPC 阻塞分析受限，尝试从堆栈推断对端 |

**解栈失败时的处理**

- 检查 so 文件路径是否正确
- 确认偏移量是否有效（十六进制格式）
- 使用 `llvm-readelf` 验证 so 是否包含符号表
- 如果确认无符号表，在报告中明确标注

**阻塞链无法闭合时的处理**

- 检查是否有 IPC 跨进程调用（需要查看对端进程）
- 考虑内核态阻塞（如 IO 等待）
- 在报告中说明阻塞链在哪个节点中断，给出下一步排查方向

**整机问题优先级判断**

当同时存在业务问题和整机问题时：
- 如果整机资源严重异常（如内存接近耗尽），优先报告整机问题
- 如果整机资源轻微异常但业务有明显阻塞逻辑，优先分析业务问题
- 如果无法确定，在报告中同时列出两种可能性

# 参考资料

**何时读取**：
- [常见阻塞模式](references/blocking-patterns.md)：识别栈顶阻塞函数时读取（如 pthread_mutex_timedlock_inner、pthread_cond_timedwait）
- [常见流水日志](references/hilog-refernce.md)：分析 hilog 异常日志时读取（如 GetSaWrap、vsync signal）

**何时不要读取**：
- 仅做基本信息分析（故障类型、整机资源），不需要加载任何参考文件
- 阻塞链已明确且无需识别阻塞模式，不要加载 blocking-patterns.md
- 无 hilog 文件或日志分析已完成，不要加载 hilog-refernce.md
