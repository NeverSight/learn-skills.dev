---
name: dsoftbus_safety_guard
description: |
  OpenHarmony软总线代码安全检视专家 - 全面检查C/C++代码的安全编码规范和日志规范。
  涵盖40+条安全规则，包括指针安全、内存管理、锁管理、敏感信息保护等关键领域。
  提供跨文件调用分析和控制流分析，生成详细的代码审查报告。
  仅在用户输入包含"软总线安全卫士"时触发。
  ⚠️ 重要：此技能为只读审查工具，不修改源文件。
---

# 软总线安全卫士 - 代码审查技能

## 触发条件

⚠️ **此技能仅在用户输入包含"软总线安全卫士"时才会被调用**

**触发示例**：
- `软总线安全卫士 请审查这个文件：D:\code\example.c`
- `请使用软总线安全卫士检查这个目录`
- `软总线安全卫士 检视lnn_lane_dfx.c文件`

## 技能概述

本技能是 OpenHarmony distributed soft bus (dsoftbus) 通信组件的专用代码审查工具，涵盖：

- **日志规范检查**：1条核心规则
- **安全编码检查**：40+条规则，覆盖11大类别
- **通用代码质量检查**：代码复杂度、可读性、并发安全等
- **跨文件调用分析**：调用链追踪、资源传递、数据流分析
- **控制流分析**：路径敏感分析、不可达代码检测

⚠️ **核心原则**：本技能为**只读代码审查工具**，仅分析代码并生成报告，**不修改任何源文件**。

## 适用场景

- OpenHarmony dsoftbus 组件代码
- C/C++ 系统级通信代码
- 涉及 IPC、网络通信、多线程的代码
- 需要严格日志规范和安全编码的代码

---

## 快速参考：关键规则索引

根据代码特征快速定位相关规则：

| 代码特征 | 相关规则 |
|---------|---------|
| 函数返回 SOFTBUS_ERR | 日志规范-1 |
| 指针位运算 (`&`, `\|`, `^`, `~`, `<<`, `>>`) | 指针安全-1, 整数运算-2 |
| `*ptr` 或 `ptr->` 使用 | 指针安全-3, 临时变量-1 |
| `arr[index]` 访问 | 数组下标-1,2 |
| `SoftBusMutexLock`/`SoftBusMutexUnlock` | 锁管理-1,2,3 |
| `SoftBusSocketCreate`/`SoftBusSocketClose` | fd管理-1,2 |
| `malloc`/`free`, `new`/`delete` | 内存管理-1~11 |
| `HILOG_INFO` 打印敏感信息 | 敏感信息-1,2,3 |
-| 无符号数递减 (`i--`) | 循环变量-1 |
| `memcpy_s`, `strcpy_s` 等 | 安全函数-1,2 |
| 路径操作 (`.`, `..`) | 外部输入-1 |
| IPC 接口新增 | 权限校验-1 |

---

## 📚 详细规则说明

**每个规则的详细解释、代码示例和修复方案请查看**：
- **[规则详解与示例](references/security_rules_explained.md)** - 40+条规则的完整文档
  - 每条规则的问题描述、风险等级、问题示例、修复方案、检查要点
  - 包含完整代码示例和最佳实践
  - 包含格式化打印类型匹配表和常用安全函数列表

---

## 🏷️ 规则分类（快速索引）

> 💡 **快速定位**: 点击每个规则后的链接可查看详细说明和代码示例

### 1. 日志规范（1条）
- 禁止返回 SOFTBUS_ERR → [详细说明](references/security_rules_explained.md#规则-11-禁止返回-softbus_err)

### 2. 指针安全（4条）
- 禁止指针位运算 → [详细说明](references/security_rules_explained.md#规则-21-禁止指针位运算)
- 检查 sizeof 使用 → [详细说明](references/security_rules_explained.md#规则-22-检查-sizeof-使用)
- 空指针解引用检查 → [详细说明](references/security_rules_explained.md#规则-23-空指针解引用检查)
- IPC 结果判空 → [详细说明](references/security_rules_explained.md#规则-24-ipc-结果判空)

### 3. 临时变量（3条）
- 指针变量初始化 → [详细说明](references/security_rules_explained.md#规则-31-指针变量初始化)
- 资源描述符初始化 → [详细说明](references/security_rules_explained.md#规则-32-资源描述符变量初始化)
- bool 变量初始化 → [详细说明](references/security_rules_explained.md#规则-33-bool-变量初始化)

### 4. 数组下标（2条）
- 数组越界风险 → [详细说明](references/security_rules_explained.md#规则-41-数组越界风险)
- 外部输入下标校验 → [详细说明](references/security_rules_explained.md#规则-42-外部输入下标合法性校验)

### 5. 锁管理（3条）
- Lock/Unlock 成对使用 → [详细说明](references/security_rules_explained.md#规则-51-softbusmutexlock-与-softbusmutexunlock-成对使用)
- 锁变量一致性 → [详细说明](references/security_rules_explained.md#规则-52-锁变量一致性)
- 所有返回路径释放锁 → [详细说明](references/security_rules_explained.md#规则-53-所有返回路径释放锁)

### 6. fd 管理（2条）
- SocketCreate/Close 成对使用 → [详细说明](references/security_rules_explained.md#规则-61-softbussocketcreate-与-softbussocketclosesoftbussocketshutdown-成对使用)
- fd 正确关闭 → [详细说明](references/security_rules_explained.md#规则-62-fd-是否正确关闭)

### 7. 内存管理（11条）
- 申请前大小合法性校验 → [详细说明](references/security_rules_explained.md#规则-71-内存申请前大小合法性校验)
- SoftBusMalloc/SoftBusCalloc 与 SoftBusFree 成对使用 → [详细说明](references/security_rules_explained.md#规则-72-softbusmallocsoftbuscalloc-与-softbusfree-成对使用)
- new 与 delete 成对使用 → [详细说明](references/security_rules_explained.md#规则-73-new-与-delete-成对使用)
- 内存申请后判空 → [详细说明](references/security_rules_explained.md#规则-74-内存申请后判空)
- 全局变量释放后置空 → [详细说明](references/security_rules_explained.md#规则-75-全局变量释放后置空)
- 循环体释放后置空 → [详细说明](references/security_rules_explained.md#规则-76-循环体释放后置空)
- 特定资源管理（regcomp/regfree, cJSON_Parse/Delete等） → [详细说明](references/security_rules_explained.md#规则-77-711-特定资源管理)

### 8. 敏感信息（3条）
- 禁止打印密钥、路径、地址等 → [详细说明](references/security_rules_explained.md#规则-81-禁止打印密钥文件路径内存地址udidhash设备名称账号-id)
- 堆栈密钥使用后清零 → [详细说明](references/security_rules_explained.md#规则-82-堆栈密钥使用后是否清零)
- 匿名化打印敏感标识符 → [详细说明](references/security_rules_explained.md#规则-83-udidnetworkiduuidipmac-等匿名化打印)

### 9. 整数运算（2条）
- 溢出、反转、除零风险 → [详细说明](references/security_rules_explained.md#规则-91-整数溢出反转除0风险)
- 有符号整数位运算禁止 → [详细说明](references/security_rules_explained.md#规则-92-有符号整数位操作符运算)

### 10. 循环变量（2条）
- 无符号数死循环 → [详细说明](references/security_rules_explained.md#规则-101-无符号数死循环)
- 外部数据控制循环校验 → [详细说明](references/security_rules_explained.md#规则-102-外部数据控制循环的合法性校验)

### 11. 安全函数（2条）
- 安全函数返回值检查 → [详细说明](references/security_rules_explained.md#规则-111-安全函数返回值处理)
- 缓冲区大小一致性 → [详细说明](references/security_rules_explained.md#规则-112-目标缓冲区大小入参与实际大小一致性)

### 12. 权限校验（1条）
- 新增 SDK IPC 接口权限校验 → [详细说明](references/security_rules_explained.md#规则-121-新增-sdk-ipc-接口权限校验)

### 13. 外部输入校验（4条）
- 路径规范化 → [详见](references/security_rules_explained.md#13-外部输入校验检查)
- TLV 解析长度合法性 → [详见](references/security_rules_explained.md#13-外部输入校验检查)
- 源 buffer 实际大小检查 → [详见](references/security_rules_explained.md#13-外部输入校验检查)
- 完整校验方案 → [详见](references/security_rules_explained.md#13-外部输入校验检查)

### 14. 外部数据有效性（3条）
- 基于外部输入的加减法/内存申请校验 → [详见](references/security_rules_explained.md#14-外部数据有效性检查)
- 默认长度校验 → [详见](references/security_rules_explained.md#14-外部数据有效性检查)
- TLV 格式长度校验 → [详见](references/security_rules_explained.md#14-外部数据有效性检查)

### 15. 常见问题（5条）
- 异常分支资源释放 → [详见](references/security_rules_explained.md#15-常见问题检查)
- 宏定义资源泄漏 → [详见](references/security_rules_explained.md#15-常见问题检查)
- 函数返回值一致性 → [详见](references/security_rules_explained.md#15-常见问题检查)
- 格式化打印类型匹配 → [详见](references/security_rules_explained.md#15-常见问题检查)
- 结构体字节对齐 → [详见](references/security_rules_explained.md#15-常见问题检查)

---

## 代码审查工作流

### 第一步：交互式选择检视范围

#### 场景A：用户指定路径

1. 检查该路径下是否有修改：`git status --porcelain <path>`
2. 如果有修改，提供选项：
   - 全量检视该路径所有代码
   - 增量检视修改的代码（共N个文件）
3. 如果无修改，直接执行全量检视

#### 场景B：用户未指定路径

1. 检查当前仓库是否有修改：`git status --porcelain`
2. 提供选项：
   - 检视全仓代码
   - 指定检视路径
   - 检视本地修改的代码（共N个文件）
3. 根据用户选择执行

### 第二步：代码规范检查

按照40+条规则逐项检查，参考：
- **[规则详解文档](references/security_rules_explained.md)** - 每条规则的详细说明和代码示例
- 使用 Grep 工具搜索违规模式
- 结合上下文分析，避免误报

### 第三步：跨文件调用分析

**核心能力**：分析函数调用链，追踪跨文件的数据流和资源传递

- 调用图构建
- 跨文件资源追踪（malloc/free分离）
- 跨文件数据流分析
- 跨文件错误处理
- 全局变量跨文件访问

### 第四步：控制流分析

**核心能力**：分析代码执行路径，识别不可达代码和路径敏感问题

- 控制流图构建
- 不可达代码检测
- 路径敏感分析
- 未初始化变量分析
- 资源释放路径分析

### 第五步：生成修复建议

⚠️ **重要限制**：**仅生成修复建议代码到报告中，严禁直接修改源文件**

对每个问题提供：
- 完整的函数或代码块修复示例
- 修改原因注释
- 多种修复方案（如有）

### 第六步：生成检视报告

创建报告目录：`d:/code-review-YYYYMMDD-HHMMSS/`

**报告文件**：
- `code_review_report.md` - 完整审查报告
- `code_fixes.patch` - 所有修复代码（Git patch格式）
- `statistics.json` - 统计数据

---

## 常见错误速查表

> 💡 **详细检查方法**: 每种错误模式的详细检查方法、代码示例和修复方案，请查看 [检查清单](references/security_rules_explained.md#检查清单)

| 错误模式 | 危险等级 | 快速检测 | 详见章节 |
|---------|---------|---------|---------|
| 空指针解引用 | 🔴 严重 | `*ptr` 或 `ptr->` 前无NULL检查 | [指针安全-3](references/security_rules_explained.md#规则-23-空指针解引用检查) |
| 锁未释放 | 🔴 严重 | return前未调用Unlock | [锁管理-1](references/security_rules_explained.md#规则-51-softbusmutexlock-与-softbusmutexunlock-成对使用) |
| 内存泄漏 | 🔴 严重 | malloc未配对free | [内存管理-2](references/security_rules_explained.md#规则-72-softbusmallocsoftbuscalloc-与-softbusfree-成对使用) |
| 敏感信息泄露 | 🔴 严重 | 日志打印密钥/udid | [敏感信息-1](references/security_rules_explained.md#规则-81-禁止打印密钥文件路径内存地址udidhash设备名称账号-id) |
| 数组越界 | 🔴 严重 | `arr[index]` 未验证范围 | [数组下标-1](references/security_rules_explained.md#规则-41-数组越界风险) |
| 无符号死循环 | 🔴 严重 | `uint32_t i--` | [循环变量-1](references/security_rules_explained.md#规则-101-无符号数死循环) |
| 指针位运算 | 🟡 警告 | `ptr & mask` | [指针安全-1](references/security_rules_explained.md#规则-21-禁止指针位运算) |
| 整数溢出 | 🟡 警告 | size + offset 未检查 | [整数运算-1](references/security_rules_explained.md#规则-91-整数溢出反转除0风险) |
| 返回SOFTBUS_ERR | 🟡 警告 | return SOFTBUS_ERR | [日志规范-1](references/security_rules_explained.md#规则-11-禁止返回-softbus_err) |
| 未初始化变量 | 🟡 警告 | 声明未赋初值 | [临时变量-1](references/security_rules_explained.md#规则-31-指针变量初始化) |

---

## 检查原则

### 上下文分析
- 检查时要看上下文，确认是否已有防护措施
- 避免误报（如：全局变量可能在别处初始化）

### 灵活运用
- 除40+条明确定义规则外，还需进行通用代码质量检查
- 代码复杂度、可读性、并发安全、性能问题等

### 重点关注
- 处理外部输入的代码路径
- 宏定义中的资源使用
- 条件编译中的问题代码
- 高风险安全问题（空指针、内存泄漏、敏感信息泄露）

### 优先级排序
```
安全编码问题 > 日志规范问题
严重问题 > 警告问题 > 提示问题
```

---

## 核心限制

⚠️ **严禁修改源代码**：
- 本技能**只读取和分析代码**
- 生成修复建议**仅用于报告**
- 绝不直接修改任何源文件
- **只读操作**：仅使用 Read、Grep、Glob 等只读工具

---

## 📖 参考文档

### 详细规则说明
- **[规则详解与示例](references/security_rules_explained.md)** - 40+条规则的详细解释和代码示例
  - 每条规则的问题描述、风险等级、问题示例、修复方案、检查要点
  - 包含完整代码示例和最佳实践
  - 包含格式化打印类型匹配表和常用安全函数列表

### 附加资源
- **[常见错误速查表](#常见错误速查表)** - 快速定位错误模式
- **[使用技巧](#使用技巧)** - 如何有效使用本技能

---

## 使用技巧

1. **快速定位问题**：使用"快速参考"表格根据代码特征查找相关规则
2. **深入学习规则**：阅读 `references/security_rules_explained.md` 了解每条规则的详细说明和代码示例
3. **分类审查**：根据"规则分类"按类别逐项检查，避免遗漏
4. **优先处理严重问题**：参考"常见错误速查表"优先修复高危问题
5. **使用工作流程**：按照"代码审查工作流"系统性进行审查

---

## 报告要求

- **报告自动生成**：审查完成后自动在 `d:/code-review-时间戳/` 目录生成报告
- **报告目录格式**：使用 `YYYYMMDD-HHMMSS` 格式的时间戳
- **文件编码**：报告文件使用 UTF-8 编码，确保中文正常显示
- **修复代码仅供参考**：所有修复代码只出现在报告文件的代码块中，不写入源代码目录
