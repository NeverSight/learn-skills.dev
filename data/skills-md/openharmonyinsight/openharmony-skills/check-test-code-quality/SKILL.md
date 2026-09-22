---
name: check-test-code-quality
description: OpenHarmony XTS测试代码质量检查工具。扫描23条检查规则（Critical+Warning），自动生成Excel报告，检测低级问题和编码规范违规。使用此技能检查XTS测试代码质量、扫描编码规范问题、验证测试用例、发现低级问题、检查getSync接口使用、验证错误码断言格式、检查用例重复、检查HAP命名规范、扫描BUILD.gn配置问题、检查签名证书APL等级等。触发关键词：XTS、测试质量、代码检查、编码规范、测试用例检查、ACTS、DCTS、HATS。
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# XTS测试代码质量检查 - 编排器

本文件是模型执行指令，负责调度23个独立规则技能完成扫描。

## 模型执行指令

当用户触发此技能时（如 `/check-test-code-quality /path/to/code --level all`），按以下步骤执行：

### 步骤1: 解析参数

从用户输入中提取扫描路径（必填）和选项参数。完整参数定义见 `skill_config.json` 的 `usage` 字段。

**参数互斥说明**: `--rules` 与 `--level` 建议不要同时使用。两者功能重叠（都是筛选执行规则），同时使用容易产生混淆。优先使用 `--rules` 指定具体规则，或使用 `--level` 按严重级别批量选择。如果同时指定，`--rules` 先生效，`--level` 再从中过滤（不推荐此用法）。

**--level 过滤规则**（定义见 `skill_config.json` 的 `rules` 字段）：
- `critical`: R001-R004,R006,R007,R010-R012,R014,R017-R023（17个）
- `warning`: R005,R008,R009,R013,R015,R016（6个）
- `all`: 全部23个

### 步骤2: 环境准备（文件收集 + 独立XTS工程识别）

本步骤是后续所有规则扫描的**前置依赖**，必须在规则扫描之前完成。

#### 2a. 文件收集

使用Glob工具遍历扫描路径，按文件类型分桶收集，并输出统计信息：

| 类别 | 文件模式 | 相关规则 | 说明 |
|------|---------|---------|------|
| 源代码文件 | `**/*.ets`, `**/*.ts`, `**/*.js`（排除.test后缀） | R001-R006,R019,R020,R022,R023 | 所有源代码，包括页面/模块/Ability文件 |
| 测试文件 | `**/*.test.ets`, `**/*.test.ts`, `**/*.test.js` | R004,R008,R009,R011,R013,R015,R016,R018 | **重要**: 使用 `endswith('.test.ets')` 等识别多后缀文件 |
| 构建文件 | `**/BUILD.gn` | R010,R014 | GN构建配置 |
| 配置文件 | `**/Test.json` | R007 | 测试配置 |
| 签名文件 | `**/*.p7b` | R012 | DER二进制签名证书 |
| 能力配置 | `**/syscap.json` | R017 | 系统能力声明 |
| 包配置 | `**/oh-package.json5` | R021 | hypium版本检测 |

**输出示例**:
```
[文件收集]
  源代码文件: 86647
  测试文件: 29074
  BUILD.gn: 4028
  Test.json: 3386
  p7b: 3223
  syscap.json: 5269
  oh-package.json5: 6960
```

#### 2b. 识别独立XTS工程

部分规则（R011 testsuite重复、R019 .key重复、R020 .id重复、R021 hypium版本）的检测范围是**工程级**，需要先识别独立XTS工程边界。

**识别逻辑**（详见 [references/ENGINE_IDENTITY.md](references/ENGINE_IDENTITY.md)）：
1. 找到所有包含 `BUILD.gn` 的目录
2. 过滤包含子 `BUILD.gn` 的父目录（仅非group类型）
3. 排除 `group()` 类型的 BUILD.gn 本身
4. 剩余目录即为独立XTS工程

**输出示例**:
```
[独立XTS工程]
  识别到 3624 个独立XTS工程
```

### 步骤3: 逐规则扫描

**预置脚本规则**（仅1条）：
- R004: 测试用例缺少断言（实现在 `scripts/r004_scanner.py`）

**R004 必须使用预置脚本**: R004（测试用例缺少断言）是 L5 最复杂规则，涉及递归函数调用链追踪、类方法提取、跨文件 import 解析、辅助函数 try-catch 缺陷检测等。**必须**使用 `scripts/r004_scanner.py` 预置脚本执行 R004 扫描，模型手动实现极易导致严重误报（历史教训：v1 版 23,152 个误报）。注意：R004当前存在误报问题，需要优化间接断言追踪算法。

**动态生成规则**（共22条，根据各规则的 `rules/Rxxx/SKILL.md` 动态生成扫描代码）：
- R001: 禁止使用getSync系统接口
- R002: 错误码断言必须是number类型
- R003: 禁止恒真断言
- R005: 组件尺寸使用固定值
- R006: 禁止基于设备类型差异化
- R007: Test.json禁止配置项
- R008: 用例声明格式不规范
- R009: @tc.number命名不规范
- R010: part_name/subsystem_name不匹配
- R011: testsuite重复
- R012: 签名证书APL等级和app-feature配置错误
- R013: 注释的废弃代码
- R014: 测试HAP命名不规范
- R015: Level参数缺省
- R016: testcase命名规范
- R017: syscap.json配置多个能力
- R018: testcase重复
- R019: .key重复
- R020: .id重复
- R021: hypium版本号>=1.0.26
- R022: errcode值断言使用==而非===
- R023: 禁止errcode值类型强转后断言

除R004外，所有规则的扫描代码由模型在运行时根据 `rules/Rxxx/SKILL.md` 中的检测逻辑和正则模式动态生成并执行。生成代码应：
1. 严格遵循规则文件中的检测逻辑
2. 使用规则文件中定义的正则模式
3. 注意规则文件中的"已知陷阱"章节，避免常见误报
4. 返回标准格式的问题列表

**R010 外部数据依赖**: R010需要从远程仓库获取3个配置文件构建子系统-部件映射表。如果因网络原因无法获取映射表数据，URL不可达时需明确告警，不可静默返回0个问题。

**共性工具库**: `scripts/common.py` 包含所有规则共享的工具函数（文件收集、it()/describe()块解析、独立XTS工程识别、子系统映射、报告生成等）。当对应 `references/` 下的文档更新时，`common.py` 中的代码也需同步更新（每个函数头部标注了同步来源）。

**动态生成规则执行流程**：

1. 读取 `rules/Rxxx/SKILL.md` 获取该规则的完整检测逻辑
2. 严格按照规则文件中的检测逻辑、正则模式生成扫描代码
3. **特别注意**: 读取规则文件中的"已知陷阱"章节，避免常见误报
4. 执行生成的扫描代码
5. 每条issue必须包含以下字段：

```python
{
    'rule': 'R004',
    'type': '测试用例缺少断言',
    'severity': 'Critical',
    'file': 'rel/path.test.ets',
    'line': 25,
    'testcase': 'testName',
    'snippet': '...',
    'suggestion': '...',
    'subsystem': '元能力',
}
```

**testcase字段**: 解析it()块范围（算法见 [references/SCAN_ALGORITHMS.md](references/SCAN_ALGORITHMS.md)），判断问题行号所属it()块。非测试文件或不在it()块内填 `-`。

**subsystem字段**: 使用 `references/subsystem_mapping.md` 映射表，按最长目录前缀匹配（算法见 [references/SCAN_ALGORITHMS.md](references/SCAN_ALGORITHMS.md)）。未匹配到填 `-`。

### 步骤4: 生成报告

汇总所有规则结果，生成：

**强制要求**: 本次实际执行的规则扫描结果**必须全部展示**，即使问题数为0也不能省略。未在本次扫描范围内的规则不得出现在报告中。

1. **Markdown统计报告**: 终端输出本次执行规则的扫描结果，格式如下：

   **示例**（`--level warning`）:
   ```
   | 规则编号 | 问题类型 | 严重级别 | 问题数量 |
   |---------|---------|---------|---------|
   | R005 | 组件尺寸使用固定值 | Warning | 120 |
   | R008 | 用例声明格式不规范 | Warning | 0 |
   | R009 | @tc.number命名不规范 | Warning | 45 |
   | R013 | 注释的废弃代码 | Warning | 0 |
   | R015 | Level参数缺省 | Warning | 88 |
   | R016 | testcase命名规范 | Warning | 0 |
   ```

   **示例**（`--level critical`）:
   ```
   | 规则编号 | 问题类型 | 严重级别 | 问题数量 |
   |---------|---------|---------|---------|
   | R001 | 禁止使用getSync系统接口 | Critical | 300 |
   | R002 | 错误码断言必须是number类型 | Critical | 0 |
   ...（仅展示本次执行的17个Critical规则）
   | R023 | 禁止errcode值类型强转后断言 | Critical | 0 |
   ```

   **示例**（`--rules R001,R003`）:
   ```
   | 规则编号 | 问题类型 | 严重级别 | 问题数量 |
   |---------|---------|---------|---------|
   | R001 | 禁止使用getSync系统接口 | Critical | 300 |
   | R003 | 禁止恒真断言 | Critical | 0 |
   ```

   **禁止**:
   - 省略问题数量为0的规则
   - 只显示有问题的规则
   - 展示不在本次扫描范围内的规则

2. **Excel报告**: UTF-8 BOM编码，包含两个sheet页：
   - **Sheet 1 - "代码质量检查报告"**: 12列问题明细（详见 [references/REPORT_FORMAT.md](references/REPORT_FORMAT.md)）
   - **Sheet 2 - "问题扫描结果汇总"**: 仅列出本次实际执行的规则统计，表头为 `规则编号 | 问题类型 | 严重级别 | 问题数量`，所有本次执行的规则必须全部列出（问题数量为0的也必须显示）

### 步骤5: 完整性检查

确认本次扫描范围内的所有规则都已执行，报告统计无遗漏。未在本次扫描范围内的规则无需检查。

### 步骤6: 自动修复（仅当用户指定 `--fix` 时执行）

当用户命令包含 `--fix` 参数时，在步骤5完成后，对扫描发现的问题按以下流程执行自动修复。

**重要**: `--fix` 仅支持以下6条规则。其余17条规则（R001-R007,R009,R010,R013,R015,R017,R019-R023）不支持自动修复，即使用户指定了这些规则，也仅执行扫描不执行修复。

1. **筛选可修复规则**: 仅修复本次扫描中以下6条规则的问题，忽略不支持的规则
2. **按规则逐个修复**: 对每条规则，按对应修复指南执行修复
3. **修复后验证**: 修复完成后重新扫描已修复的规则，确认问题数减少

**支持自动修复的规则**（共6条）:

| 规则 | 修复指南 | 修复内容 |
|------|---------|---------|
| R008 | `guides/R008_testcase_format/R008_FIX_GUIDE.md` | @tc.xxx冒号改空格、删除多余空行 |
| R011 | `guides/R011_testsuite_duplicate/R011_FIX_GUIDE.md` | describe名称追加Adapt后缀 |
| R012 | `guides/R012_p7b_signature/R012_FIX_GUIDE.md` | p7b签名证书重新生成（需hap-sign-tool.jar） |
| R014 | `guides/R014_hap_naming/R014_HAP_NAMING_GUIDE.md` | BUILD.gn hap命名修正+Test.json同步 |
| R016 | `guides/R016_testcase_naming/R016_FIX_GUIDE.md` | 特殊字符移除+Adapt后缀+同步@tc.name |
| R018 | `guides/R018_testcase_duplicate/R018_FIX_GUIDE.md` | testcase名称去重+Adapt后缀+同步@tc.name |

**修复执行要求**:
- 执行修复前，读取对应 `guides/` 下的修复指南，严格按照指南中的修复规则执行
- R012修复需要使用签名工具（`guides/R012_p7b_signature/signature_tools/`），如果工具不可用则提示用户手动修复
- 修复会直接修改源文件，修复前必须提示用户确认或建议提交代码到版本控制系统
- 修复完成后，对已修复的规则重新扫描验证，输出修复前后的问题数量对比

**使用示例**:
```
/check-test-code-quality /path/to/code --rules R008,R016 --fix
/check-test-code-quality /path/to/code --level all --fix
```

## 规则总览

完整规则列表（名称、扫描范围、详细实现路径）见 `skill_config.json` 的 `rules` 和 `rule_descriptions` 字段。各规则检测逻辑见 `rules/Rxxx/SKILL.md`。

## 高频陷阱速查（扫描时必须注意）

| 陷阱 | 影响规则 | 要点 |
|------|---------|------|
| 字符串中大括号干扰it()块提取 | R004,R015,R016,R018,R019,R020 | 用状态机追踪字符串内/外状态 |
| 反引号模板字符串中撇号干扰 | R004,R018 | 追踪in_backtick状态 |
| p7b是DER二进制，json.loads必失败 | R012 | 用容错解码+正则提取 |
| R001/R005/R006须扫描所有源文件 | R001,R005,R006 | 不能只扫描.test文件 |
| R016只检查字符集，不限制命名格式 | R016 | 用`^[a-zA-Z0-9_-]+$`，不用格式正则 |
| R016检测it()参数，不是@tc.name | R016 | 严禁用@tc.name值作为检测源 |
| R006只检测条件判断 | R006 | 赋值和日志打印不是问题 |
| group父BUILD.gn不阻止子工程 | R011,R019,R020 | 陷阱10，见references/TRAPS.md |
| R010依赖远程映射表，静默返回0 | R010 | 必须从远程获取3个配置文件构建映射表，URL不可达时需明确告警，见陷阱11 |

详细陷阱说明见 [references/TRAPS.md](references/TRAPS.md)。

## 详细文档索引

| 文档 | 说明 |
|------|------|
| [references/TRAPS.md](references/TRAPS.md) | 11个已知扫描陷阱的详细说明和修复代码 |
| [references/REPORT_FORMAT.md](references/REPORT_FORMAT.md) | Excel/CSV报告格式规范（12列表头、修复建议格式） |
| [references/ENGINE_IDENTITY.md](references/ENGINE_IDENTITY.md) | 独立XTS工程识别规范（group类型处理） |
| [references/SCAN_ALGORITHMS.md](references/SCAN_ALGORITHMS.md) | it()/describe()块提取与子系统映射算法规范 |
| [references/subsystem_mapping.md](references/subsystem_mapping.md) | 97条子系统路径映射表 |
| [references/project_level_scan.md](references/project_level_scan.md) | 工程级检测共享逻辑（R011/R019/R020/R021） |
| [references/VERSION_HISTORY.md](references/VERSION_HISTORY.md) | 版本变更记录 |
| [skill_config.json](skill_config.json) | 技能配置中心（规则定义、参数、输出格式） |
| [scripts/r004_scanner.py](scripts/r004_scanner.py) | R004预置扫描脚本（递归断言追踪，必须使用） |
| [scripts/simple_rules.py](scripts/simple_rules.py) | 共性扫描工具函数和正则模式（供动态生成代码参考） |
| [scripts/common.py](scripts/common.py) | 共性工具库（文件收集、块解析、工程识别、报告生成） |
| [scripts/main.py](scripts/main.py) | 扫描入口（参数解析、规则调度、报告输出） |
| [guides/FIX_GUIDE.md](guides/FIX_GUIDE.md) | 问题修复指南 |
