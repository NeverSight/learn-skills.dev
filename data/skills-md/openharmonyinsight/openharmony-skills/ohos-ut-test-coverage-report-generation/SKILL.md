---
name: ohos-ut-test-coverage-report-generation
description: "为OpenHarmony C/C++提供基于UT用例的代码覆盖率报告生成，支持全量和增量覆盖率分析，需要通过 hdc 连接测试设备。Use when: (1) 用户请求为子系统/部件/模块/测试套/测试用例生成全量代码覆盖率，如果提供报告路径时,解析为--output路径； (2) 用户请求为部件/模块/测试套/测试用例生成增量代码覆盖率，需要 git diff 文件，如果提供报告路径时,解析为--output路径；注意：增量覆盖率不支持子系统级别。当需要连接 OpenHarmony 设备执行测试时激活。"
Keywords: full_coverage, incremental_coverage, code_coverage, hdc, test_coverage, 覆盖率报告生成, 测试覆盖率, 设备连接
---

# OpenHarmony - 代码覆盖率分析

---

## 文档导航

- 🚀 **快速开始**: 详见 `references/quick-start.md` - 环境配置、设备连接、执行示例
- ⚡ **性能说明**: 详见 `references/performance-guide.md` - 预期耗时、资源占用、优化建议
- 📚 **使用示例**: 详见 `references/usage-examples.md` - 全量/增量场景、参数匹配规则
- 📖 **参数指南**: 详见 `references/parameter-guide.md` - 参数解析规则、验证规则、匹配规则详解
- 💡 **最佳实践**: 详见 `references/best-practices.md` - 场景选择、优化建议、安全建议
- 🔧 **问题排查**: 详见 `references/troubleshooting.md` - 常见问题排查步骤、错误恢复策略

---

## 快速开始

**必须配置**: `{SKILL_DIR}/config/user-config.json`（必须包含 `code_root` 字段）

**执行示例**:
- 全量: "为 ability_base 部件生成全量代码覆盖率报告"
- 增量: "为 ability_base 部件生成增量代码覆盖率报告"
> 📖 详见 `references/quick-start.md`（环境配置、设备连接）

---

## Anti-Patterns - 绝对禁止事项

NEVER 做以下操作，否则会导致测试无法编译、运行：

| 禁止项 | 原因 | 正确做法 |
|--------------------------------------------|---------------------------------------------------|------------------------------------------------|
| **NEVER 修改源码** | 我们只负责编译和执运行生成报告，不涉及修改源码与用例内容 | 所有c/c++代码、skill内容禁止修改 |
| **NEVER 跳出预设流程** | 预设流程以外的操作禁止，防止使用错误的命令和覆盖率工具 | 按照执行流程并只能加载当前流程涉及的md和错误处理流程md |
| **NEVER 在命令执行过程中检查状态** | 同步阻塞命令必须等待完成 | 禁止在命令执行时检查日志、进程等，必须等待命令自然返回或超时 |
| **NEVER 中断或轮询长时间运行的命令** | 必须使用timeout并等待自然完成 | 禁止主动中断或轮询检查命令状态，让timeout机制处理超时 |
| **NEVER 在编译中断后直接重试** | 必须先清理编译缓存 | 执行 `rm -rf out/` 后再重试 |
| **NEVER 在多部件并行时使用相同输出目录** | 会导致报告冲突 | 每个部件使用独立的输出目录 |
| **NEVER 修改 lcov 分支覆盖率参数后不重新编译** | gcno 文件会不匹配 | 修改参数后必须重新编译 |

---

## 执行前决策检查清单

**在开始执行前，先问自己**：

### 💭 思考框架
- **目标**: 用户想要评估什么？（整个部件、变更部分、特定模块？）
- **范围**: 用户提供了哪些参数？（subsystem、part、module、testsuite、testcase？）
- **场景**: 适合使用全量还是增量？（日常开发用增量，定期检查用全量）
- **资源**: 磁盘空间和设备状态是否满足要求？

**✅ 必须确认的3个关键问题**:

1. **目标范围正确性**
   - [ ] 是全量（subsystem/part/module 支持）还是增量（仅支持 part）？
   - [ ] 如果是增量，确认没有传入 subsystem（会报错 `INCREMENTAL_NOT_SUPPORT_SUBSYSTEM`）

2. **输入完整性**
   - [ ] 全量：subsystem、part、module 至少提供一个
   - [ ] 增量：part 必须提供（不能为空）

3. **资源可用性**
   - [ ] 磁盘空间充足？（全量需50GB+，增量需20GB+，详见 `references/performance-guide.md`）
   - [ ] 设备已连接？（`hdc list targets` 可验证）

### 全量 vs 增量决策表

| 场景 | 推荐类型 | 预期耗时 | 资源需求 | 详见 |
|------|---------|---------|---------|------|
| PR 合并前验证 | 增量 | 30分-2小时 | 20GB 磁盘 | references/best-practices.md |
| 每周质量检查 | 全量 | 3-5小时 | 50GB 磁盘 | references/performance-guide.md |
| 重构后验证 | 全量 | 3-5小时 | 50GB 磁盘 | references/best-practices.md |
| 日常开发调试 | 增量 | 30分-2小时 | 20GB 磁盘 | references/best-practices.md |

---

## 执行流程

```
用户输入
    ↓
[1] 主入口 (SKILL.md)
    - 解析关键词和参数
    - 确认覆盖率类型 (全量/增量)
    ↓
[2] 配置检查 ⚠️ **MANDATORY - READ ENTIRE FILE**
在进入此步骤前，你必须完整读取 `references/01-config-checker.md` 
的所有内容（约414行），不要设置任何行数限制。
**DO NOT Load**: 在完成此步骤前，不要加载后续参考文档。
执行内容:
    ├──[1] 获取基础变量 (SKILL_DIR、CODE_ROOT)
    ├──[2] 检查项目结构 (developer_test、xdevice、pr_local_coverage)
    ├──[3] 检查用户输入参数 (全量/增量覆盖率参数)
    ├──[4] 检查配置文件 (user-config.json内容、/etc/lcovrc)
    ├──[5] 解析部件名称 (subsystem/part)
    ├──[6] 检查设备连接配置
    └──[7] 返回配置和参数信息
    ↓
[3] 环境检查 ⚠️ **MANDATORY - READ ENTIRE FILE**
完成配置检查后，读取 `references/02-env-checker.md` 的所有内容（约150行）。
**DO NOT Load**: 在完成此步骤前，不要加载 03-dependency-installer.md。
执行内容:
    ├──[1] 操作系统检测 (仅支持Linux)
    ├──[2] 检查Python 版本 (需要3.8+)
    ├──[3] 检查工具依赖
    ├──[4] 检查Python依赖包
    ├──[5] 检查是否存在可执行编译命令的全仓根目录 (build_system.sh)
    ├──[6] 权限检查
    ├──[7] 磁盘空间检查
    └──[8] 返回环境状态,如果出现错误进入错误处理流程
    ↓
[4] 依赖安装 ⚠️ **MANDATORY - READ ENTIRE FILE**
完成环境检查后，读取 `references/03-dependency-installer.md` 的所有内容（约100行）。
**DO NOT Load**: 在完成此步骤前，不要加载执行模块。
执行内容:
    ├──[1] 安装系统依赖 (仅支持Linux)
    ├──[2] 安装Python包依赖 (需要3.8+)
    ├──[3] 验证安装结果
    ├──[4] 返回依赖安装状态,如果出现错误进入错误处理流程
    ↓
[5] 覆盖率执行流程
    ├── 全量：⚠️ **MANDATORY - READ ENTIRE FILE**
    当 `taskType = "full_coverage"` 时，读取 `references/04-full-coverage-executor.md` 
    的所有内容（约472行）。**DO NOT Load**: 增量模式下不要加载此文档。
    │  ├── [1] 修改developer_test中的 user_config.xml 配置文件
    │  ├── [2] 执行 build_before_generate.py (如果用户已经编译完成则跳过)
    │  ├── [3] 编译用例 (检查skip_compile、预编译、构建命令、执行、验证)
    │  ├── [4] 启动框架并执行命令 (构建命令、拼接命令、执行、验证)
    │  ├── [5] 执行 after_lcov_branch.py (恢复源码)
    │  ├── [6] 移动报告到输出目录
    │  ├── [7] 解析报告
    │  └── [8] 清理环境
    └── 增量: ⚠️ **MANDATORY - READ ENTIRE FILE**
    当 `taskType = "incremental_coverage"` 时，读取 `references/05-incremental-coverage-executor.md` 
    的所有内容。**DO NOT Load**: 全量模式下不要加载此文档。
        ├── [1] 执行本地编译脚本 (script/pr_local_coverage/local_build)
        ├── [2] 执行覆盖率流程脚本 (script/pr_local_coverage/pr_coverage)
        ├── [3] 移动报告到输出结果目录
        ├── [4] 恢复环境
        └── [5] 清理临时文件
    ↓
[6] 错误处理 ❌ **DO NOT LOAD（仅在错误时触发）**
在任何步骤出现错误时，读取 `references/06-error-handler.md` 的相关错误处理部分。
在步骤 [2]-[5] 期间，不要加载此文档。
        ├──[1] 识别错误类型
        ├──[2] 查找解决方案
        ├──[3] 提供用户友好的错误信息
        └──[4] 返回错误信息
```

---

## 参数说明
### 参数来源
- **code_root**: 从 `{SKILL_DIR}/config/user-config.json` 的 `code_root` 字段获取
- **其他参数**: 从用户输入解析
### 参数详解
📖 **详细的参数解析规则、验证规则和匹配规则请见**:
→ `references/parameter-guide.md` - 完整的参数指南
### 快速参考
- **全量覆盖率参数**: subsystem、part、module、testsuite、testcase（至少提供一个）
- **增量覆盖率参数**: part（必须）、diff（可选，不提供则自动生成）
- **通用参数**: output（可选，默认 `{CODE_ROOT}/coverage_result`）、skip_compiler（可选，仅全量）
### 参数验证规则
📖 **详见**: `references/parameter-guide.md` - 参数验证规则部分

---

## 核心使用示例
详见 `references/usage-examples.md` - 全量/增量场景、参数匹配规则、错误示例（第1-389行）

---

## 错误恢复策略

| 错误类型 | 恢复方法 | 是否需要清理 | 详见 |
|---------|---------|-------------|------|
| 配置错误 | 修改 user-config.json 后重试 | 否 | references/troubleshooting.md |
| 环境缺失 | 运行 pip install / apt-get | 否 | references/quick-start.md |
| 编译失败 | 清理编译缓存后重试 | 是：`rm -rf out/` | references/troubleshooting.md |
| 测试超时 | 检查设备状态，重试 | 否 | references/troubleshooting.md |
| 报告生成失败 | 检查 lcov 数据完整性 | 是：重新生成 gcda | references/troubleshooting.md |
| 设备连接失败 | 检查 hdc 配置，重新连接 | 否 | references/quick-start.md |

---

## 模块说明

所有模块位于 `references/` 目录:
- **01-config-checker.md** - 配置与参数检查模块
- **02-env-checker.md** - 环境与依赖检查模块
- **03-dependency-installer.md** - 依赖安装模块
- **04-full-coverage-executor.md** - 全量覆盖率执行模块
- **05-incremental-coverage-executor.md** - 增量覆盖率执行模块
- **06-error-handler.md** - 错误处理模块

脚本位于 `scripts/` 目录:
- **check_gcno_files.py** - gcno文件检查脚本
- **parse_coverage_report.py** - 全量覆盖率报告数据解析脚本
- **run_test_with_monitor.sh** - 后台执行全量覆盖率测试命令并监控hdc链接脚本
- **pr_local_coverage** - 增量覆盖率报告脚本
- **addlcov** - 备用工具

配置文件: `config/user-config.json`

---

## 变量定义

由 01-config-checker.md 获取并传递给后续模块:
- **SKILL_DIR**: 当前SKILL所在目录(通过向上查找 SKILL.md 获取)
- **CODE_ROOT**: 从 {SKILL_DIR}/config/user-config.json 的 code_root 字段获取

---

## 模块间传参信息

### 整体参数传输流程
```
主入口
  ↓
[01] config-checker
  ├──→ [02] env-checker
  ├──→ [04] full-coverage-executor (全量模式)
  ├──→ [05] incremental-coverage-executor (增量模式)
  └──→ [06] error-handler (错误时)

[02] env-checker
  ├──→ [03] dependency-installer
  └──→ [06] error-handler (错误时)

[03] dependency-installer
  └──→ [06] error-handler (错误时)

[04/05] 执行模块
  └──→ [06] error-handler (错误时)
```

### 01-config-checker.md 传入后续模块的参数
**传递给 02-env-checker.md**:
- `skill_dir`: {SKILL_DIR}
- `code_root`: {CODE_ROOT}
- `output_path`: {output_path}
- `taskType`: 任务类型
- `config.deviceInfo`: 设备配置信息（完整）

**传递给 04-full-coverage-executor.md (全量模式)**:
- `skill_dir`: {SKILL_DIR}
- `code_root`: {CODE_ROOT}
- `taskType`: 任务类型
- `userInput.parameters`: 用户解析的参数对象
- `config.deviceInfo`: 设备配置信息（完整）

**传递给 05-incremental-coverage-executor.md (增量模式)**:
- `skill_dir`: {SKILL_DIR}
- `code_root`: {CODE_ROOT}
- `taskType`: 任务类型
- `userInput.parameters`: 用户解析的参数对象
- `config.deviceInfo`: 设备配置信息（完整）

### 02-env-checker.md 传入后续模块的参数
**传递给 03-dependency-installer.md**:
- `skill_dir`: {SKILL_DIR}
- `code_root`: {CODE_ROOT}
- `output_path`: {output_path}
- `taskType`: 任务类型
- `tools`: 工具依赖状态
- `pythonPackages`: Python包依赖状态
- `permissions`: 权限状态

### 03-dependency-installer.md 传入后续模块的参数
**传递给 04/05 执行模块**:
- `isAllInstalled`: 所有依赖是否已安装
- `dependencies`: 依赖安装状态

---

## 模块调用规范

调用 references 下的模块时遵循以下规范：

### 调用顺序与参数传递
- **01-config-checker.md**：
  - 步骤 [2] 调用
  - 输入：解析后的用户参数
  - 输出：完整配置信息 + 设备信息
  - 传递给：02、04、05

- **02-env-checker.md**：
  - 步骤 [3] 调用
  - 输入：skill相关路径 + 设备信息
  - 输出：环境检查状态
  - 传递给：03

- **03-dependency-installer.md**：
  - 步骤 [4] 调用
  - 输入：02的检查结果
  - 输出：依赖安装状态
  - 传递给：04/05

- **04-full-coverage-executor.md**：
  - 步骤 [5] 调用（全量模式）
  - 输入：01的完整配置
  - 输出：覆盖率报告

- **05-incremental-coverage-executor.md**：
  - 步骤 [5] 调用（增量模式）
  - 输入：01的完整配置
  - 输出：覆盖率报告

- **06-error-handler.md**：
  - 任何错误时调用
  - 输入：错误信息
  - 输出：用户友好的错误信息

### 重要原则
- **单向传递**：只按流程顺序传递信息，禁止反向引用
- **完整性**：01提供完整配置，02/03不再重复检查
- **一致性**：所有序号和流程图保持一致