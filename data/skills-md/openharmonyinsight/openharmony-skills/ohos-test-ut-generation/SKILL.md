---
name: ohos-test-ut-generation

description: "为OpenHarmony C/C++代码生成单元测试用例。Use when: (1) 用户请求为子系统/模块/文件/函数生成单元测试；(2) 编写HWTEST/HWTEST_F测试用例；(3) 创建ohos_unittest；(4) 用户提到'生成测试用例'、'写单元测试'、HWTEST、ohos_unittest。Keywords: HWTEST, ohos_unittest,  unit test, C++ testing, 单元测试生成"

---

# OpenHarmony 单元测试生成

为 OpenHarmony C/C++ 代码生成符合 testfwk_developer_test 框架规范的单元测试用例。

---

## Anti-Patterns - 绝对禁止事项

NEVER 做以下操作，否则会导致测试无法编译、运行：

| 禁止项                                          | 原因                                                | 正确做法                                            |
| -------------------------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| **NEVER 省略 `using namespace testing::ext;`** | HWTEST/HWTEST_F等宏定义在此命名空间，缺失会导致编译失败               | 文件头必须包含该语句                                      |
| **NEVER 使用GTest原生 `TEST()` 或 `TEST_F()`**    | OpenHarmony门禁无法识别，缺少测试等级参数                        | 统一使用 `HWTEST` 或 `HWTEST_F`                      |
| **NEVER 在HWTEST宏中忘记测试等级参数**                  | TestSize.Level1-4是门禁判断依据，缺失会被拒绝                   | 必须指定如 `TestSize.Level1`                         |
| **NEVER 省略 `import("//build/test.gni")`**    | ohos_unittest模板在此文件定义，缺失会报"template not found"    | BUILD.gn第一行必须import                             |
| **NEVER 在module_out_path使用绝对路径**             | 输出路径格式必须为 `子系统名/模块名`，GN路径会导致错误                    | 使用如 `hiviewdfx/hiview_test`                     |
| **NEVER 访问private成员时忘记cflags_cc绕过**          | private成员无法直接访问，会报"is private"错误                  | 添加 `-Dprivate=public -Dprotected=public`        |
| **NEVER 混用测试类型概念**                           | OpenHarmony有FUNC/PERF/RELI/SECU/FUZZ类型，与GTest概念不同 | 在@tc.type中使用OH定义的类型                             |
| **NEVER 在SetUp中忘记初始化测试对象**                   | 未初始化指针会导致SEGFAULT或NULL pointer错误                  | 确保SetUp中创建detector_等对象                          |
| **NEVER 省略gtest_main依赖**                     | 缺失会导致链接错误"undefined reference to main"            | deps中必须包含 `//third_party/googletest:gtest_main` |

---

## 执行流程

```
环境确认 → 分析源码 → 测试策略 → 测试设计 → 用例规划 → 编写测试文件 → BUILD.gn → 验证
```

---

## 步骤零：环境确认

**目标**：确认测试文件放置位置和编译环境配置。

**MANDATORY - READ ENTIRE FILE**: Before环境确认，MUST read [`test-framework.md`](references/test-framework.md) completely to understand:

- ohos_unittest/ohos_moduletest/ohos_fuzztest区别与选择
- API版本对应关系
- 测试框架目录结构

**Light Loading** (read only if needed):

- [`framework-quickref.md`](references/framework-quickref.md) - 测试框架速查表（宏+等级+注释+命名）

**Do NOT Load**: build-rules.md, error-matrix.md (此步骤不涉及)

### 检查清单（必完成）

| 检查项        | 规范                                    | 示例                                   |
| ---------- | ------------------------------------- | ------------------------------------ |
| 测试文件位置     | 模块根目录/test/unittest/                  | base/hiviewdfx/hiview/test/unittest/ |
| Mock文件位置   | test/mock/                            | base/hiviewdfx/hiview/test/mock/     |
| BUILD.gn位置 | test/目录下                              | base/hiviewdfx/hiview/test/BUILD.gn  |
| BUILD.gn入口 | group("unittest") { testonly = true } | --                                   |
| 源码路径格式     | GN风格 //base/xxx                       | //base/hiviewdfx/hiview              |

### 输出格式

确认完成后输出：

```markdown
## 环境确认完成
- 模块根目录: base/xxx/yyy
- 测试目录: base/xxx/yyy/test/unittest/
- 测试输出路径: subsystem/module_test
- 源码GN路径: //base/xxx/yyy
```

---

### 存量测试分析（可选）

**目标**：如果目标模块已有存量测试代码，先分析现有风格，确保新生成的测试与之一致。

使用 [`analyze-existing-tests.py`](scripts/analyze-existing-tests.py) 脚本分析存量测试：

```bash
python scripts/analyze-existing-tests.py <test_directory> --output style_report.md [--encoding utf-8] [--verbose]
```

**参数说明**：

| 参数               | 说明                     |
| ---------------- | ---------------------- |
| `directory`      | 测试用例目录路径（必填）           |
| `--output, -o`   | 输出报告文件路径（可选，不指定则输出到终端） |
| `--encoding, -e` | 文件读取编码（默认 utf-8）       |
| `--verbose, -v`  | 输出详细调试信息               |

**使用时机**：

- 目标模块已有 `test/unittest/` 目录下存在测试文件时，**推荐**先运行此脚本
- 全新模块无存量代码时，跳过此步骤

**分析结果用途**：

1. **宏选择**：参考存量代码主要使用 HWTEST 还是 HWTEST_F
2. **等级格式**：参考存量代码使用 `TestSize.Level1` 还是 `Level1`
3. **命名风格**：参考存量代码的用例命名模式（`FuncName_001` vs `TestSuite_FuncName_001`）
4. **注释风格**：参考存量代码的 @tc 注释格式

---

## 步骤一：分析待测源码

**目标**：解析源码，提取测试所需的结构化信息。

**Light Loading** (read only if needed):

- [`test-framework.md`](references/test-framework.md) - 未在步骤0完成时继续读
- [`framework-quickref.md`](references/framework-quickref.md) - 参考命名规范时
- [`real-patterns.md`](references/real-patterns.md) - 需要参考真实代码示例时

**Do NOT Load**: build-rules.md, error-matrix.md, assertion-gmock-guide.md (此步骤不涉及)

### 解析要点

| 解析类别 | 关键信息           | 方法                  |
| ---- | -------------- | ------------------- |
| 类结构  | 类名、继承关系、成员变量   | 提取class定义块          |
| 公开方法 | 函数签名、返回类型、参数列表 | 分析public段函数声明       |
| 函数逻辑 | 分支条件、异常处理、边界检查 | 提取if/try/return逻辑   |
| 数据类型 | 枚举、常量、结构体定义    | 提取enum/const/struct |

### 输出格式（结构化报告）

```markdown
## 源码分析报告
### 文件信息
- 源文件: //base/xxx/src/file.cpp
- 头文件: //base/xxx/include/file.h
- 命名空间: OHOS::XXX
### 公开方法列表
| 方法 | 签名 | 分支逻辑 | 边界条件 |
| GetSectionInfo | bool GetSectionInfo(const string&, Info&) | 空字符串返回false | 空字符串 |
| ResetSection | bool ResetSection(const string&) | 空字符串返回false | 空字符串 |
```

---

## 步骤二：制定测试策略

**目标**：基于源码分析，制定测试范围、类型、优先级和覆盖率目标。

**Light Loading** (read only if needed):

- [`test-strategy-method.md`](references/test-strategy-method.md) - 代码特征→测试策略映射表
- [`framework-quickref.md`](references/framework-quickref.md) - 参考测试等级选择决策树

**Do NOT Load**: build-rules.md, error-matrix.md, test-case-spec.md

### 策略决策表

| 方法类型      | 测试范围判定      | 优先级建议         |
| --------- | ----------- | ------------- |
| public方法  | 必须测试        | 核心功能P1，辅助功能P2 |
| static方法  | 必须测试（独立可测）  | P1            |
| virtual方法 | 必须测试（覆盖派生类） | P1/P2         |
| private方法 | 不直接测试       | 通过public间接覆盖  |
| 逻辑特征      | 测试类型选择      |               |
| ----      | ----------- |               |
| 计算逻辑      | FUNC（功能测试）  |               |
| 性能敏感      | PERF（性能测试）  |               |
| 异常处理      | RELI（可靠性测试） |               |
| 安全检查      | SECU（安全测试）  |               |

### 输出格式

```markdown
## 测试策略
| 方法 | 测试判定 | 测试类型 | 优先级 |
| GetSectionInfo | 必测（核心功能） | FUNC | P1 |
| ResetSection | 必测（含状态处理） | FUNC | P1 |
### 覆盖率目标
- 语句覆盖率: ≥80%
- 分支覆盖率: ≥70%
- 函数覆盖率: 100%
```

---

## 步骤三：进行测试设计

**目标**：结合黑盒与白盒测试方法将测试策略转化为具体的测试场景设计。

**Light Loading** (read only if needed):

- [`test-strategy-method.md`](references/test-strategy-method.md) - 参数边界值设计参考
- [`framework-quickref.md`](references/framework-quickref.md) - 参考测试等级分配

**Do NOT Load**: build-rules.md, error-matrix.md, test-case-spec.md

### 测试场景设计模板（必使用）

为每个方法填写以下表格：

```markdown
## [函数名] 测试场景设计

| 编号 | 场景类型 | 场景描述 | 输入数据 | 预期输出 | 测试等级 |
| T01 | 正常 | [具体场景] | [参数值] | [返回值/状态] | Level1 |
| T02 | 异常 | [错误场景] | [触发错误的输入] | [错误码/false] | Level2 |
| T03 | 边界 | [边界值] | [INT_MAX/空字符串等] | [预期行为] | Level2 |
| T04 | 状态 | [状态依赖] | [前置状态描述] | [状态变化结果] | Level2 |
```

### 场景设计要点

| 参数类型     | 正常输入设计     | 边界测试点                   |
| -------- | ---------- | ----------------------- |
| int/long | 典型正值、负值、零值 | INT_MIN, INT_MAX, 0, -1 |
| string   | 非空字符串      | 空字符串、超长字符串              |
| 指针       | 有效对象指针     | nullptr                 |
| 容器       | 非空容器       | 空容器、单元素                 |

---

## 步骤四：规划测试用例

**目标**：将测试场景映射为具体的测试用例，确定命名和等级分配。

**MANDATORY - READ ENTIRE FILE**: Before规划用例，MUST read [`naming-convention.md`](references/naming-convention.md) to understand:

- 推荐新生成规则：`[FunctionName]_[001-999]`
- 兼容历史存量风格（仅分析时参考）
- @tc.name命名规范

**Light Loading** (read only if needed):

- [`framework-quickref.md`](references/framework-quickref.md) - 测试等级选择决策树
- [`real-patterns.md`](references/real-patterns.md) - 参考历史存量命名格式（分析时）

**Do NOT Load**: build-rules.md, error-matrix.md

### 用例规划模板（必使用）

```markdown
## [函数名] 用例规划

| 用例编号 | 用例名称 | 对应场景 | 测试等级 | 测试宏 |
| 001 | GetSectionInfo_001 | T01 正常获取 | Level1 | HWTEST_F |
| 002 | GetSectionInfo_002 | T02 空字符串 | Level2 | HWTEST_F |
```

### 测试宏选择决策表

| 情况        | 测试宏选择                             | 原因                   |
| --------- | --------------------------------- | -------------------- |
| 无需初始化/清理  | `HWTEST(A, B, TestSize.Level1)`   | 独立测试，无Setup/Teardown |
| 需要测试前后初始化 | `HWTEST_F(A, B, TestSize.Level1)` | 需要SetUp/TearDown     |
| 多线程测试     | `HWMTEST_F(A, B, C, D)`           | D为线程数                |
| 参数化测试     | `HWTEST_P(A, B, C)`               | 多组数据测试               |

---

## 步骤五：编写测试文件

**目标**：生成符合规范的测试代码文件。

**MANDATORY - READ ENTIRE FILE**: Before编写代码，MUST read:

- [`test-case-spec.md`](references/test-case-spec.md) - 测试文件完整结构、Anti-Patterns禁止清单
- [`framework-quickref.md`](references/framework-quickref.md) - HWTEST宏用法、测试等级、@tc注释格式
- [`assertion-gmock-guide.md`](references/assertion-gmock-guide.md) - Mock配置（如需使用Mock）

**Light Loading** (read only if needed):

- [`real-patterns.md`](references/real-patterns.md) - 需要参考真实代码示例时
- [`naming-convention.md`](references/naming-convention.md) - 命名规范详细说明

**Do NOT Load**: build-rules.md, error-matrix.md (此步骤不涉及BUILD.gn和错误排查)

### 测试文件结构模板

**MANDATORY - READ ENTIRE FILE**: 参考完整模板 [`test-template.cpp`](examples/test-template.cpp)（~75行），包含：

- 版权声明、头文件包含、命名空间声明
- Test类定义（SetUpTestCase/TearDownTestCase/SetUp/TearDown）
- @tc注释格式、HWTEST_F宏示例、断言使用

**关键要素**：

- `using namespace testing::ext;` → MUST包含（HWTEST宏在此命名空间）
- `SetUp()`初始化测试对象 → MUST完成（否则SEGFAULT）
- 命名格式：推荐 `[FunctionName]_[001]`，详见 naming-convention.md

**命名要点**（详见 naming-convention.md）：

- 推荐：`[FunctionName]_[001]`（如 `GetSectionInfo_001`）
- 历史：`TestSuiteFunction_001`（如 `BBoxDetectorUnitTest001`，不推荐新生成模仿）

### 断言使用规则

详见 [`test-case-spec.md`](references/test-case-spec.md) Anti-Patterns禁止清单。

**核心原则**：

- 前置条件检查（指针非空、状态验证）→ MUST用 `ASSERT_*`（失败终止）
- 结果验证（输出/状态验证）→ MUST用 `EXPECT_*`（失败继续）

---

## 步骤六：编写 BUILD.gn

**目标**：配置测试目标编译规则。

**MANDATORY - READ ENTIRE FILE**: Before编写BUILD.gn，MUST read [`build-rules.md`](references/build-rules.md) to understand:

- 测试模板类型选择（ohos_unittest vs ohos_moduletest）
- deps vs external_deps决策规则
- cflags_cc访问控制绕过配置
- 完整BUILD.gn模板

**Do NOT Load**: framework-quickref.md, error-matrix.md, real-patterns.md (此步骤不涉及测试代码和示例)

### BUILD.gn模板

**MANDATORY - READ ENTIRE FILE**: 参考完整模板 [`build-template.gn`](examples/build-template.gn)（~45行），包含：

- import语句、module_output_path配置
- config块、ohos_unittest定义、group定义
- deps/external_deps/cflags_cc/defines完整示例

**关键配置项**：

| 配置项                          | 说明               | 必填性            | 常见错误                                     |
| ---------------------------- | ---------------- | -------------- | ---------------------------------------- |
| `import("//build/test.gni")` | 测试模板定义           | 必填（第一行）        | 缺少→template not found                    |
| `module_out_path`            | 输出路径，格式 `子系统/模块` | 必填             | 使用绝对路径→错误                                |
| `deps`                       | 内部依赖，含gtest_main | 必填             | 缺少gtest_main→undefined reference to main |
| `external_deps`              | 跨子系统依赖           | 按需             | 格式错误→链接失败                                |
| `cflags_cc`                  | 访问控制绕过           | 按需（测试private时） | 缺少→'xxx' is private                      |

---

## 步骤七：验证与调试

**目标**：确认测试用例可以正确编译和运行。

**MANDATORY - READ ENTIRE FILE**: Before验证，MUST read [`error-matrix.md`](references/error-matrix.md) to understand:

- 编译错误矩阵（症状→原因→修复）
- 运行错误矩阵
- 门禁拒绝类错误
- 错误排查流程

**Do NOT Load**: framework-quickref.md, build-rules.md, real-patterns.md (已在前步骤加载)

### 编译命令

```bash
./build.sh --product-name <product> --build-target BBoxDetectorUnitTest
```

### 常见编译错误快速排查

| 错误                                   | 原因             | 解决方案                               |
| ------------------------------------ | -------------- | ---------------------------------- |
| `fatal error: xxx.h: No such file`   | include_dirs缺失 | 在config块中添加include_dirs            |
| `undefined reference to xxx`         | deps缺失         | 检查deps和external_deps               |
| `'xxx' is private`                   | 访问控制           | 添加cflags_cc: `-Dprivate=public`    |
| `template 'ohos_unittest' not found` | 缺少import       | 第一行添加 `import("//build/test.gni")` |

---

## 快速参考

测试等级、测试宏、注释格式的完整速查表详见 [`framework-quickref.md`](references/framework-quickref.md)，包含：

- Level0-Level4等级定义、选择决策树、常见场景等级分配
- HWTEST/HWTEST_F宏语法与门禁强制要求
- @tc.type测试类型速查（FUNC/PERF/RELI/SECU/FUZZ）
- 命名规范速查（推荐新生成规则 vs 兼容历史存量风格）

---

## References导航

详细文档位于 `references/` 目录，按步骤需求加载：

| 文件                         | 内容                      | 加载时机                      |
| -------------------------- | ----------------------- | ------------------------- |
| `test-framework.md`        | 测试框架概述、API版本对应          | **步骤0 MANDATORY**         |
| `framework-quickref.md`    | 测试框架速查表（宏+等级+注释+命名）     | **步骤0-5 MANDATORY/Light** |
| `test-case-spec.md`        | 测试文件完整结构、Anti-Patterns  | **步骤5 MANDATORY**         |
| `naming-convention.md`     | 命名规范（推荐新规则vs历史兼容）       | **步骤4 MANDATORY**         |
| `build-rules.md`           | BUILD.gn决策规则、完整模板       | **步骤6 MANDATORY**         |
| `error-matrix.md`          | 错误排查矩阵（编译+运行+门禁）        | **步骤7 MANDATORY**         |
| `assertion-gmock-guide.md` | Mock配置（BUILD.gn集成+真实示例） | **步骤5 Light**（需Mock时）     |
| `real-patterns.md`         | 真实仓库示例（标注历史格式）          | 步骤1-5 Light Loading       |
| `test-strategy-method.md`  | 测试策略设计方法                | 步骤2-3 Light Loading       |

---

## Examples导航

完整模板示例位于 `examples/` 目录：

| 文件                  | 内容                                        | 用途          |
| ------------------- | ----------------------------------------- | ----------- |
| `test-template.cpp` | 完整测试文件示例（版权+类定义+测试用例）                     | 步骤5参考完整代码结构 |
| `build-template.gn` | 完整BUILD.gn示例（import+config+ohos_unittest） | 步骤6参考完整配置结构 |

**加载时机**：MANDATORY - READ ENTIRE FILE（步骤5、步骤6）

---

## 输入信息要求

| 信息           | 必需性 | 说明                        |
| ------------ | --- | ------------------------- |
| 源码位置         | 必需  | 文件路径或函数名称                 |
| 需求编号         | 可选  | @tc.require填写内容，无需求编号时则为空 |
| 测试等级         | 可选  | 默认Level1                  |
| 是否生成BUILD.gn | 可选  | 默认生成                      |

---

## 开始使用

当用户请求生成测试时，按工作流程执行：

1. 环境确认 → read test-framework.md + framework-quickref.md
2. 分析源码 → 输出源码分析报告
3. 测试策略 → read test-strategy-method.md + framework-quickref.md → 输出策略表格
4. 测试设计 → 输出场景设计表格
5. 用例规划 → read naming-convention.md + framework-quickref.md → 输出用例规划
6. 编写测试文件 → read test-case-spec.md + framework-quickref.md + assertion-gmock-guide.md → 生成.cpp
7. 编写BUILD.gn → read build-rules.md → 生成.gn
8. 验证 → read error-matrix.md → 提供编译命令
