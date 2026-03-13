---
name: debugging
description: iOS 调试与问题排查技能。当用户遇到 crash、异常、运行时错误、内存泄漏、内存增长、ViewController 未释放、UI 卡顿、掉帧、启动慢等问题需要排查诊断时使用。提供 crash 类型识别、根因分析、LLDB 命令和修复方案。
---

# iOS 调试与问题排查

## Crash 类型识别

| 异常类型 | 常见原因 | 排查方向 |
|---------|---------|---------|
| EXC_BAD_ACCESS | 野指针、force unwrap nil、数组越界 | 检查可选值解包、数组边界、多线程访问 |
| EXC_BAD_INSTRUCTION | fatalError、preconditionFailure | 检查 force unwrap、数组越界 |
| SIGABRT | NSException、unrecognized selector | 查看异常信息、检查 ObjC 互操作 |
| Watchdog | 主线程阻塞超时 | 检查主线程同步 I/O、死锁 |

## Crash 排查流程
1. **看异常类型和信息** → 初步定位方向
2. **看崩溃线程调用栈** → 定位具体代码位置
3. **看相关上下文** → 联系前后逻辑推断根因
4. **提出修复方案** → 给出具体代码修复

## 常见修复模式
- force unwrap crash → `guard let` / `if let` / `??` 默认值
- 数组越界 → 安全下标 `array[safe: index]`
- 主线程卡死 → 耗时操作移到 `Task {}` 或后台队列
- 线程竞争 → 用 actor 或同步机制保护

## LLDB 调试命令
- `po <变量>` 打印对象
- `bt` 查看当前调用栈
- `bt all` 查看所有线程
- `expr <表达式>` 运行时求值
- Symbolic Breakpoint: `UIViewAlertForUnsatisfiableConstraints`, `objc_exception_throw`

## Crash 输出格式
```
🔍 Crash 类型: [类型]
📍 崩溃位置: [文件:方法:行]
💡 根因分析: [分析]
🔧 修复方案: [代码]
🛡️ 防御建议: [如何预防]
```

## 专项调试指南
- **内存泄漏排查**: 参见 [references/memory-leak.md](references/memory-leak.md) — 6 大泄漏模式检查清单、Memory Graph 使用
- **性能问题诊断**: 参见 [references/performance-debugging.md](references/performance-debugging.md) — 按症状诊断卡顿/启动慢/内存高

## ✅ Sentinel（Skill 使用自检）
当且仅当你确定本 Skill 已被加载并用于当前任务时，在回复末尾追加：
`// skill-used: debugging`

规则：
- 只能输出一次
- 如果不确定是否加载，禁止输出 sentinel
- 输出 sentinel 代表你已遵守本 Skill 的硬性规则与交付格式
- 只有当任务与本 skill 的 description 明显匹配时才允许输出 sentinel