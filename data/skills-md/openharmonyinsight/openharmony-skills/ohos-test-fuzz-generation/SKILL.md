---
name: ohos-test-fuzz-generation
description: >
  为 C/C++ 项目生成 LLVM libFuzzer FUZZ 测试用例、执行 26 条安全规范审查、生成语义化种子数据。
  兼容 OpenHarmony / Linux / Android 构建系统。

  触发关键词：fuzz 测试、生成 fuzzer、创建 fuzz 用例、fuzz 规范检查、fuzz_test、LLVMFuzzerTestOneInput、种子数据/corpus
metadata:
  author: openharmony
  scope: common
  stage: testing
  domain: fuzz
  capability: test-generation
  version: 0.2.0
  status: production
  triggers:
    - fuzz 测试
    - 生成 fuzzer
    - 创建 fuzz 用例
    - fuzz 规范检查
    - fuzz_test
    - LLVMFuzzerTestOneInput
    - 种子数据
    - corpus
  tags:
    - fuzz
    - testing
    - security
    - c++
---

# FUZZ 测试生成引擎

## 核心工作流

```
用户输入需求
      ↓
[决策点] 用户意图是什么？
    ├─ 给类名要求生成测试 → 进入完整工作流
    ├─ 给现有文件要求检查 → 跳至阶段 5（规范审查）
    ├─ 要求生成种子 → 跳至阶段 4（种子语义生成）
    └─ 要求生成报告 → 跳至阶段 5 后生成报告
      ↓
[阶段 1] 代码分析 —— 解析目标 API 类结构、方法签名、参数类型
      ↓
[阶段 2] 骨架生成 —— 创建 5 文件标准化工程（.cpp/.h/BUILD.gn/project.xml/corpus）
      ↓
[阶段 3] 实现填充 —— 模板替换为实际 API 职责与数据构造逻辑
      ↓
[阶段 4] 种子语义生成 —— 基于参数类型/名称特征生成高价值初始 corpus
      ↓
[阶段 5] 规范审查 —— 26 条规则逐一验证，输出合规报告
    **加载触发**：仅加载违规规则的 rules/SecurityCodeReview_FuzzCheck_XXX.md
    **必须加载**：规则 005 详细说明（复杂参数构造，误报高发区）
    **不要加载**：未违规规则、规则速查表（`references/rules-overview.md` 仅在审查时加载）
      ↓
[阶段 6] 自动修复 —— 可自动修复规则执行修复（最多 3 轮）
      ↓
交付生成文件 + 审查报告 + 人工确认项清单
```

**异常处理决策树**：
- 阶段 1 解析失败（找不到类/头文件）→ 检查类名拼写 → 提供头文件路径 → 手动解析
- 阶段 5 发现不可自动修复违规 → 输出人工修复指南 → 标记 BLOCK → 跳过修复
- 阶段 6 修复 3 轮后仍失败 → 停止修复 → 输出剩余违规清单 → 建议人工审查

## 工具入口

| 工具 | 用途 | 命令示例 |
|------|------|----------|
| `tools/fuzz_generator.py` | 生成 FUZZ 测试用例 | `python tools/fuzz_generator.py -n XxxXxx_fuzzer -N Namespace -c ClassName -H header.h -p output_path` |
| `tools/fuzz_check.py` | 规范审查（26 条规则） | `python tools/fuzz_check.py --dir fuzzer_dir [--fix]` |
| `tools/seed_generator.py` | 生成语义化种子 | `python tools/seed_generator.py --dir fuzzer_dir [--api ApiName]` |
| `tools/generate_report.py` | 生成合规报告 | `python tools/generate_report.py --dir fuzzer_dir` |

## 关键决策

### 生成前的自检

开始生成前，先确认：
1. **目标 API 是否有参数？** 无参数 → 拒绝生成，建议单元测试（规则 001）
2. **是 IPC 接口吗？** 继承 `IRemoteBroker` / 含 `DECLARE_INTERFACE_DESCRIPTOR` → 必须生成 IPC stub fuzzer（`LLVMFuzzerInitialize` 初始化全局 `g_stub`，`LLVMFuzzerTestOneInput` 用 `code % CODE_MAX` 驱动），`sptr<T>` 参数写入 `WriteRemoteObject(nullptr)`（规则 007）
3. **单文件接口数量？** >10 个 → 拆分为多个 fuzzer（规则 006）
4. **参数是否全为输出类型？** 非 const 引用/指针 → 跳过，无需 fuzz 输入

### 类型映射决策

| 类型类别 | 消费代码 | 说明 |
|----------|----------|------|
| 标识符类型（大驼峰非枚举） | `fdp.ConsumeIntegral<uint64_t>()` | 如 `ScreenId`/`NodeId`，底层是 `uint64_t` typedef |
| 进程/用户标识 | `fdp.ConsumeIntegral<uint32_t>()` | 如 `ProcessId`/`Uid` |
| 文件描述符 | `fdp.ConsumeIntegral<int32_t>()` | 如 `Fd` |
| 枚举类型 | `static_cast<EnumType>(fdp.ConsumeIntegral<uint8_t>() % ENUM_SIZE)` | **必须用 uint8_t**（规则 013） |
| 字符串 | `fdp.ConsumeRandomLengthString(256)` | 限制最大长度防止内存爆炸 |
| 容器 | 先消费长度 `uint8_t count = fdp.ConsumeIntegral<uint8_t>() % 32`，再循环消费 | 适用于 `std::vector<T>` |

**关键区分**：大驼峰命名不一定是枚举，可能是 typedef 别名。必须检查 `ENUM_SIZE_MAP` 确认是否为枚举。

**未知类型处理策略**：
- 类型在 `TYPE_CONSUMER_MAP` 中 → 直接使用映射
- 类型不在映射中但为大驼峰 → 检查 `ENUM_SIZE_MAP` → 是枚举则 `uint8_t % ENUM_SIZE`
- 类型不在映射中且非大驼峰 → 检查是否为 `std::vector<T>` → 是则循环消费
- 以上都不匹配 → **必须加载** `tools/fuzz_generator.py` 查看 `COMPLEX_TYPE_MAP` 或构造自定义消费逻辑

### NEVER 列表

- **NEVER** 使用 `rand()` / `random()` —— 不可重现，丧失覆盖率追踪意义（规则 017）
- **NEVER** 将 `size` 参数当作变异数据传入 API —— fuzz 引擎无法有效变异长度（规则 010）
- **NEVER** 直接解引用 `data` 指针 —— 可能包含非法地址，100% 触发 SIGSEGV（规则 018）
- **NEVER** 使用未初始化全局指针 —— fuzz 引擎会误判为稳定崩溃而停止探索（规则 019）
- **NEVER** 对无参数 API 生成 FUZZ —— 覆盖率永远为 0（规则 001）
- **NEVER** 单文件测试超过 10 个接口 —— 变异预算不足，覆盖率下降（规则 006）
- **NEVER** 使用 `auto` 声明 fuzz 变量 —— 无法人工验证类型匹配性（规则 016）
- **NEVER** 跳过 Verify 循环 —— 无法发现状态机相关 bug（资源泄漏、顺序依赖）
- **NEVER** 对枚举使用 `uint32_t` —— 1 字节变异效率远高于 4 字节（规则 013）

## References

**根据任务按需加载：**

- **`references/rules-overview.md`** — 26 条规则速查表（名称/严重度/自动检查/自动修复）
  - **加载时机**：仅阶段 5 规范审查时
  - **不要加载**：生成阶段

- **`rules/SecurityCodeReview_FuzzCheck_XXX.md`** — 违规规则详细说明（正误示例 + 豁免条件）
  - **加载时机**：阶段 5 规范审查发现违规时
  - **不要加载**：未违规规则

- **`rules/SecurityCodeReview_FuzzCheck_005.md`** — 复杂参数构造规则详解
  - **加载时机**：涉及结构体/指针/回调/容器参数时
  - **原因**：规则 005 是误报高发区，需仔细核对豁免条件

- **`tools/fuzz_generator.py`** — 用例生成器源码
  - **加载时机**：需要了解生成逻辑或自定义类型映射时
  - **关键查看**：`TYPE_CONSUMER_MAP`、`ENUM_SIZE_MAP`、`COMPLEX_TYPE_MAP`

- **`templates/fuzzer.cpp`** — 代码生成模板
  - **加载时机**：需要自定义 fuzzer 代码结构时
  - **不要加载**：正常使用生成器时

**官方文档：**

- **OpenHarmony Fuzz测试规范** — https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/test/fuzz-test.md
- **LLVM LibFuzzer 官方文档** — https://llvm.org/docs/LibFuzzer.html
- **FuzzedDataProvider API** — https://llvm.org/docs/LibFuzzer.html#fuzzed-data-provider
