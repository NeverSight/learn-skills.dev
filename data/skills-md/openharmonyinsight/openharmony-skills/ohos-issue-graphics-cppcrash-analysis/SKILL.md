---
name: ohos-issue-graphics-cppcrash-analysis
description: Use when analyzing OpenHarmony cppcrash faultlogs to locate root cause of native process crashes, investigating SIGSEGV/SIGABRT signals, memory corruption patterns, or call stack anomalies.
metadata:
  author: openharmony
  scope: domain
  stage: issue
  domain: graphics
  capability: cppcrash-analysis
  version: 0.1.0
  status: trial
---

# 任务与边界

## 解决的问题

分析OpenHarmony系统图形模块相关cppcrash日志文件，定位进程崩溃的根本原因。

## 输入

- cppcrash日志文件
- `code/`目录下的相关源码
- `lib.unstripped/`目录下的带符号表so文件

## 输出

- 崩溃根因分析报告
- 精确的代码行号定位
- 修复建议

## 不适用情形

- 纯ArkTS/JS层崩溃（无native调用栈）
- 无cppcrash日志文件
- 无符号表so文件（无法解栈）

# 触发信号

## 任务触发词

- 分析cppcrash
- 解析cppcrash日志
- 定位native崩溃

## 症状词

- SIGSEGV、SIGABRT
- Use-After-Free
- 野指针
- 内存踩踏
- 0x6b6b地址

## 场景词

- 图形模块崩溃
- render_service崩溃

# 前置检查

## 开始分析前，先问自己

1. **崩溃类型是什么？** → 决定优先分析路径
   - SIGSEGV → 内存访问异常，优先地址模式匹配
   - SIGABRT → 主动终止，优先调用栈业务分析
   
2. **地址模式有何特征？** → 决定是否需要深度数据流追踪
   - `0x6b6b...`开头 → 必须做Use-After-Free分析
   - 高位字节异常 → 必须做地址模式匹配
   
3. **是否有多线程上下文？** → 决定是否需要竞争分析
   - 若有`Other thread info` → 必须检查锁竞争和竞态条件

## 1. 检查输入完整性

按以下顺序检查：

1. cppcrash文件是否存在
2. `lib.unstripped/`目录是否存在
3. `code/`目录是否存在

若缺失必要输入，终止并报告用户。

## 2. 检查崩溃类型

从cppcrash头部读取`Reason`：

- 若signal为SIGSEGV：内存访问异常
- 若signal为SIGABRT：主动终止或异常
- 若地址以`0x6b6b`开头：Use-After-Free

## 3. 检查buildId匹配

解栈前必须验证so的buildId与cppcrash中一致，否则终止。

# 执行策略

## 分析流程

根据崩溃类型选择分析路径：

| 崩溃类型 | 优先路径 | 原因 |
|----------|----------|------|
| SIGSEGV + `0x6b6b`地址 | 解栈 → 数据流追踪 → 地址匹配 | Use-After-Free需追溯释放点 |
| SIGSEGV + 高位字节异常 | 解栈 → 地址匹配 → 内存分析 | 踩内存需定位踩踏源 |
| SIGABRT + abort/raise | 解栈 → 业务代码分析 | 主动退出需理解退出原因 |
| 包含`cfi_slowpath_comm` | 优先踩内存分析路径 | CFI失败指示内存破坏 |

完整流程如下（按需要执行）：

1. **元数据分析**：读取Device Info、Module name、Reason、LastFatalMessage
2. **调用栈解栈**：详见 `references/stack-unwinding.md`
3. **代码定位与读取**：根据解栈结果定位源码
4. **反汇编分析**：详见 `references/disassembly-analysis.md`
5. **深度数据流追踪**：详见 `references/memory-pattern-analysis.md`
6. **调用链回溯分析**：详见 `references/call-chain-backtrace.md`
7. **多线程竞争分析**：详见 `references/thread-competition-analysis.md`
8. **内存数据分析**：详见 `references/memory-data-analysis.md`
9. **特殊情况判断**：详见 `references/special-cases.md`
10. **生成分析报告**：详见 `references/report-template.md`

## 关键判断点

### 崩溃地址特征判断

- `0x6b6b...`开头 → Use-After-Free（已释放内存被访问）
- 地址为0或接近0 → 空指针或野指针
- 地址与合法地址高位字节不同 → 越界写入踩踏

### 多线程问题判断

查看`Other thread info`：
- 若其它线程持有相同锁 → 锁竞争
- 若其它线程修改相同对象 → 竞态条件
- 若崩溃线程正在遍历容器而其它线程修改 → 迭代器失效

## 代码排查重点

详见 `references/code-review-checklist.md`，重点检查：

- 多线程锁使用
- 类型强转安全
- lambda捕获生命周期
- 智能指针生命周期

# 禁止做法

## 不要猜测根因

- 禁止在没有证据的情况下推断根因
- 禁止跳过数据流追溯直接给出结论
- 禁止使用模糊表述如"可能是"、"也许是"

常见错误做法：
- 看到SIGSEGV就断定是空指针 → 必须先验证fault_addr是否真的是0或接近0
- 看到0x6b6b地址就断定是UAF → 必须追溯数据流找到是谁释放了该对象
- 看到崩溃线程代码有问题就断定是该代码导致 → 必须检查是否其它线程在并发修改相同对象

原因：会导致错误的修复方向，浪费调试时间。

## 不要跳过解栈验证

- 禁止使用buildId不匹配的so解栈
- 禁止不验证buildId直接解栈

常见错误做法：
- 用不同版本so解栈（buildId不匹配） → 解出的行号对应不同版本代码，定位完全错误

原因：会导致错误的代码行号定位。

## 不要忽略多线程分析

- 禁止只分析崩溃线程而忽略其它线程
- 禁止忽略锁竞争和竞态条件

常见错误做法：
- 发现崩溃线程代码"看起来没问题"就认为不是代码问题 → 可能是其它线程并发修改导致崩溃线程访问失效对象

原因：多线程问题是图形模块崩溃的常见根因。

## 不要跳过地址模式匹配

- 禁止不对比崩溃地址与合法地址的差异

常见错误做法：
- 只检查崩溃地址是否在Maps中 → 忽略了高位字节被踩的细微差异（如0x59→0x09）
- 不计算崩溃指令的实际访问地址 → 无法验证地址模式是否匹配

原因：地址模式匹配是识别内存踩踏的关键手段。

# 异常与回退

## 信息不足时

- 若无法找到对应so → 报告用户需要提供正确的符号表文件
- 若无法定位源码 → 报告用户需要提供完整的代码目录
- 若buildId不匹配 → 报告用户版本不一致，终止分析

## 证据不足时

- 若无法确定单一根因 → 列出所有可能的根因并说明判断依据
- 明确标注哪些结论是确定的，哪些是推断的
- 说明需要进一步分析的方向

## 特殊调用栈处理

- 若栈顶是abort/raise → 结合业务代码分析主动退出原因
- 若栈顶是terminate → 分析异常抛出原因，注意踩内存也可能导致异常不匹配
- 若包含`cfi_slowpath_comm` → 优先按踩内存问题分析

# 参考资料

按以下条件读取对应文件：

| 条件 | 文件 | 注意 |
|------|------|------|
| 执行解栈步骤时 | `references/stack-unwinding.md` | 仅解栈时加载 |
| 执行反汇编分析时 | `references/disassembly-analysis.md` | 仅需确认崩溃指令时加载 |
| 执行调用链回溯分析时 | `references/call-chain-backtrace.md` | 仅追溯参数来源时加载 |
| 执行数据流追踪或地址模式匹配时 | `references/memory-pattern-analysis.md` | 仅地址异常时加载 |
| 执行多线程竞争分析时 | `references/thread-competition-analysis.md` | 仅有多线程上下文时加载 |
| 执行内存数据分析时 | `references/memory-data-analysis.md` | 仅需分析内存dump时加载 |
| 判断特殊情况时 | `references/special-cases.md` | 仅调用栈特征匹配时加载 |
| 排查代码问题时 | `references/code-review-checklist.md` | 仅定位到代码后加载 |
| 生成分析报告时 | `references/report-template.md` | 仅最后生成报告时加载 |

**Do NOT Load**: 不要在分析开始时一次性加载所有references文件，按需加载以节省上下文空间。

## 前置信息

用户提供了相关源码在`code/`目录。

用户提供了相关带符号表信息的so在`lib.unstripped/`目录。

用户环境提供llvm工具（llvm-readelf/llvm-addr2line/llvm-objdump等）。

分析时使用中文交互，涉及文件均为UTF-8编码。