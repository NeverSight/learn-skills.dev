---
name: add-memory-trace-tags
description: Use when adding new resource tracking types to memory profiling in developtools_profiler and third_party_musl repositories. Triggered by requests to add trace tags, resource labels, or memory tracking types.
---

# 内存跟踪标签添加

自动在 developtools_profiler 和 third_party_musl 仓库中添加新的资源跟踪类型标签。

## 概述

此 skill 自动跨两个仓库的多个文件添加内存跟踪标签，确保定义一致、协议更新和测试覆盖。

## 使用场景

适用于以下情况：
- 添加新的资源跟踪类型（COMMON_* 或特定类型）
- 更新内存分析功能
- 扩展跟踪标签系统

## 快速参考

| 组件 | 修改文件数 | 主要变更 |
|------|-----------|---------|
| **third_party_musl** | 2 个文件 | TAG 和 MASK 定义 |
| **developtools_profiler** | 9 个文件 | 协议、逻辑、测试 |

## 使用方法

在对话中直接调用：

```
请添加一个新的资源跟踪标签 <标签名称>
```

或

```
使用 add-res-trace-tag 添加 <标签名>
```

## 参数说明

此 skill 会提示输入：

1. **标签名称**（必填）
   - 格式：大写字母和下划线
   - 风格：`COMMON_<类型名>` 或描述性名称
   - 示例：`COMMON_PIXELMAP`、`CREATE_NATIVE_WINDOW_FROM_SURFACE`

2. **描述**（可选）
   - 用途说明

3. **是否绕过大小过滤**（可选，默认：是）
   - 通用资源类型通常需要绕过大小过滤

## 修改内容

### third_party_musl（2 个文件）
- `src/hook/linux/memory_trace.h` - TAG、MASK、位域布局
- `porting/linux/user/src/hook/memory_trace.h` - 重复定义

### developtools_profiler（9 个文件）

**协议：**
- `protos/types/plugins/native_hook/native_hook_result.proto` - TraceType、MemoryType 枚举

**常量：**
- `device/plugins/native_daemon/include/hook_common.h` - 索引常量

**业务逻辑：**
- `device/plugins/native_hook/src/hook_guard.cpp` - TagId 映射
- `device/plugins/native_daemon/src/hook_manager.cpp` - 掩码转换
- `device/plugins/native_daemon/src/stack_preprocess.cpp` - 统计映射
- `device/plugins/native_daemon/src/hook_record.cpp` - TraceType 设置
- `device/plugins/native_hook/src/hook_client.cpp` - 过滤条件（仅 COMMON_* 类型）

**测试：**
- `device/plugins/native_daemon/test/unittest/common/native/hook_record_test.cpp`
- `device/plugins/native_daemon/test/unittest/common/native/stack_preprocess_test.cpp`

## 常见错误

### MASK 定义规则

**每个资源类型必须定义两个宏：**

```c
// ✅ 正确：同时定义两个宏
#define RES_COMMON_WINDOW          (1ULL << 33)
#define RES_COMMON_WINDOW_MASK     (1ULL << 33)

// ❌ 错误：缺少 _MASK 后缀
#define RES_COMMON_WINDOW          (1ULL << 33)
// 缺少 RES_COMMON_WINDOW_MASK！
```

**为什么需要两个定义：**
1. `RES_<NAME>` - 基础掩码值
2. `RES_<NAME>_MASK` - 统一接口的别名

**常见错误场景：**
```
错误 1：忘记添加 _MASK 后缀
#define RES_COMMON_SURFACE (1ULL << 34)     // ✅ 有这个
// ❌ 缺少：#define RES_COMMON_SURFACE_MASK (1ULL << 34)

错误 2：只复制了第一行
#define RES_COMMON_TEXTURE (1ULL << 35)     // ✅ 有这个
#define RES_COMMON_TEXTURE    // ❌ 这行是错的！应该是 (1ULL << 35)
```

**Skill 自动验证：**
此 skill 会自动检查是否两个定义都存在，如果缺失会自动添加。

## 验证清单

添加新标签后检查：

- [ ] musl 主文件：TAG 已定义
- [ ] musl 主文件：MASK 已定义（**两个都要**）
- [ ] musl porting 文件：TAG 已定义
- [ ] musl porting 文件：MASK 已定义（**两个都要**）
- [ ] proto：TraceType 枚举值已添加
- [ ] proto：MemoryType 枚举值已添加
- [ ] hook_common.h：索引已定义
- [ ] hook_common.h：RESTRACE_TYPE_COUNT 已更新
- [ ] hook_guard.cpp：映射已添加
- [ ] hook_manager.cpp：转换逻辑已添加
- [ ] stack_preprocess.cpp：SaveMemTag 和 AddAllocStatistics 已添加
- [ ] hook_record.cpp：SetTraceType 分支已添加
- [ ] hook_client.cpp：过滤条件已更新（仅 COMMON_* 类型）
- [ ] 测试：测试用例已添加

## 约束条件

- **标签命名**：大写字母和下划线
- **比特位分配**：从 bit 34 开始（当前用到 bit 33）
- **索引分配**：从 23 开始（当前最大索引 22）
- **枚举值**：自动递增，不与现有值冲突
- **仓库路径**：假设为 `d:\Code\tools_develop\`
- **RESTRACE_TYPE_COUNT**：必须等于最大索引 + 1


## 注意事项

1. **编译顺序**：修改 musl 后需要重新编译，profiler 才能使用新宏定义
2. **协议兼容性**：protobuf 修改后需要重新生成 C++ 代码
3. **测试覆盖**：所有修改都会添加相应的测试用例
4. **COMMON_* 类型**：只有 COMMON_* 前缀的类型才需要更新 `hook_client.cpp` 的过滤条件

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| 标签已存在 | 使用不同的标签名称 |
| 文件未找到 | 验证仓库路径 |
| 权限被拒绝 | 检查文件写入权限 |
| 格式无效 | 标签名称必须是大写字母和下划线 |
| 缺少 MASK | Skill 自动添加 RES_*_MASK 定义 |
| 定义不匹配 | RES_* 和 RES_*_MASK 的值必须相同 |

