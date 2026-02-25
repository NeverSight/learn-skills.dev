---
name: android-to-harmonyos-migration-workflow
description: 多 agent 协作的 Android 到 HarmonyOS 代码迁移工作流（迭代式）。当用户需要将 Android 项目迁移到 HarmonyOS 时触发，提供：1) Analyzer Agent 扫描代码结构 2) Planner Agent 制定迁移计划 3) Translator Agent 执行代码转换 4) **Validator Agent（验证代理）** 使用 **ohos-app-build-debug** skill 进行编译验证、应用打包和上板验证首界面 5) Tester Agent 验证功能（每个模块迁移完成后执行） 6) 所有模块迁移完成后，执行 Feature Comparator Agent 检查遗漏功能 7) UI Comparator Agent 验证界面一致性 8) 将未完成部分反馈给 Planner Agent 继续迭代。包含代码分析脚本、API映射表、组件转换模式和自动化验证工具。触发关键词：迁移Android到鸿蒙、Android迁移、HarmonyOS迁移、Java/Kotlin转ArkTS、Activity转Page、功能比对、UI比对。
---

# Android 到 HarmonyOS 迁移工作流（迭代式）

本技能提供系统化的 Android 到 HarmonyOS 代码迁移流程，使用 **7 个专业 agent**协作完成迁移任务。

## 快速开始

1. **用户提供源码和目标路径**后，启动 [Analyzer Agent](#1-analyzer-agent分析代理)
2. [Planner Agent](#2-planner-agent规划代理) 制定初始迁移计划

3. **模块迁移循环**（逐个模块执行）：
   - 选择一个模块 → [Translator Agent](#3-translator-agent翻译代理) 转换代码
   - → [Validator Agent](#4-validator-agent验证代理) 使用 **ohos-app-build-debug** skill 进行编译验证、应用打包和上板验证首界面
   - → [Tester Agent](#5-tester-agent测试代理) 测试功能
   - → 标记模块为已完成，继续下一个模块
4. 重复步骤 3，**直到所有计划模块完成迁移**

5. **全局比对阶段**（所有模块完成后）：
   - [Feature Comparator Agent](#6-feature-comparator-agent功能比对代理) 比对遗漏功能
   - [UI Comparator Agent](#7-ui-comparator-agentui-比对代理) 比对界面
   - → 将未完成项反馈给 [Planner Agent](#2-planner-agent规划代理)
   6. **迭代循环**：
   - Planner Agent 根据比对结果制定补充迁移计划
   - 重复步骤 3-5，直到无遗漏项

## 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│              Android 到 HarmonyOS 迁移工作流（迭代式）             │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │ Analyzer │  扫描源码，生成结构报告
    │   Agent  │
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │ Planner  │  制定初始迁移计划（模块清单、优先级）
    │   Agent  │
    └────┬─────┘
         │
         ▼
    ╔═══════════════════════════════════════════════════════════════╗
    ║                     模块迁移循环                              ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  ║
    ║   │ Translator   │───▶│  Validator   │───▶│   Tester     │  ║
    ║   │    Agent     │    │    Agent     │    │    Agent     │  ║
    ║   │  代码转换     │    │  质量验证     │    │  功能测试     │  ║
    ║   └──────────────┘    └──────────────┘    └──────┬───────┘  ║
    ║                                                     │          ║
    ║                                                     ▼          ║
    ║                                          ┌──────────────┐     ║
    ║                                          │  模块完成    │     ║
    ║                                          │  标记状态    │     ║
    ║                                          └──────┬───────┘     ║
    ║                                                 │             ║
     ║                                        ┌────────┴────────┐    ║
    ║                                        │                 │    ║
    ║                                        ▼                 ▼    ║
    ║                                  有更多模块？      所有模块完成  ║
    ║                                        │                 │    ║
    ║                                        ▼                 │    ║
    ║                              ┌──────────────────┐        │    ║
    ║                              │   下一模块 N+1   │────────┘    ║
    ║                              └────────┬─────────┘             ║
    ║                                       │                       ║
    ╚═══════════════════════════════════════╪═══════════════════════╝
                                            │ 所有模块完成
                                            ▼
    ╔═══════════════════════════════════════════════════════════════╗
    ║                     全局比对阶段                              ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║   ┌─────────────────────────────────────────────────┐        ║
    ║   │            比对阶段（并行执行）                    │        ║
    ║   ├────────────────────────────┬─────────────────────┤        ║
    ║   │ Feature Comparator         │   UI Comparator     │        ║
    ║   │       Agent                │      Agent          │        ║
    ║   │    功能比对                 │      UI 比对         │        ║
    ║   └─────────┬──────────────────┴────────────┬────────┘        ║
    ║             │                               │                  ║
    ║             └──────────┬────────────────────┘                  ║
    ║                        ▼                                     ║
    ║              ┌──────────────────┐                             ║
    ║              │   遗漏项收集     │                             ║
    ║              │  (未完成功能/UI) │                             ║
    ║              └────────┬─────────┘                             ║
    ║                       │                                       ║
    ╚════════════════════════╪═════════════════════════════════════╝
                            │
                            ▼
                  ┌──────────────────┐
                  │     Planner      │◀────────┐
                  │      Agent       │         │
                  │  制定补充计划    │         │
                  └────────┬─────────┘         │
                           │                   │
          ┌────────────────┴───────────────────┤
          │                                    │
          ▼                                    ▼
    有遗漏项？                              无遗漏项
          │                                    │
          ▼                                    ▼
    ┌──────────────┐                    ┌──────────────┐
    │  迭代下一轮   │                    │  迁移完成    │
    │ (回到模块循环) │                    └──────────────┘
    └──────────────┘
```

### 1. Analyzer Agent（分析代理）

**任务**：扫描 Android 源码，生成代码结构报告

**执行步骤**：
```bash
# 运行分析脚本
python scripts/analyze.py <source-path>
```

**输出**：
- 文件统计（总数、语言分布）
- 组件类型分布（Activity、Fragment、Service等）
- 依赖关系图
- 复杂度评分

### 2. Planner Agent（规划代理）

**任务**：制定和更新模块化迁移计划（初始 + 迭代）

**规划原则**：
- 每个模块约 5000 行代码
- 迁移顺序：数据层 → 业务逻辑 → UI 层
- 优先迁移低风险、高复用的模块

**初始规划**：模块清单和迁移检查清单

**迭代规划**（全局比对后触发）：
- 接收来自 Feature Comparator Agent 的遗漏功能清单
- 接收来自 UI Comparator Agent 的界面差异清单
- 制定补充迁移计划（遗漏项作为新模块）
- 动态调整待迁移模块优先级
- 追踪整体迁移进度

**详细规划方法**：见 [PLANNING.md](references/PLANNING.md)

**状态追踪**：
```yaml
migration_state:
  iteration: 1  # 迭代轮次
  completed_modules: []
  in_progress: null
  pending_modules:
    - name: "数据层模块"
      priority: 1
      status: "pending"
  missing_features: []  # 全局比对后填充
  ui_differences: []     # 全局比对后填充
```

### 3. Translator Agent（翻译代理）

**任务**：执行代码转换

**输入**：来自 Planner Agent 的待迁移模块

**转换映射**：见 [API_MAPPING.md](references/API_MAPPING.md)

**核心转换规则**：
- Activity → `@Entry @Component` Page
- Fragment → `@Component`
- RecyclerView → `LazyForEach`
- Room → RelationalDB
- ViewModel → `@Observed + @ObjectLink`

**执行转换**：
```bash
python scripts/migrate.py <source-file> <target-file> --mode <component-type>
```

**输出**：
- 转换后的 ArkTS 代码文件
- 转换报告（成功/失败/警告）
- 传递给 Validator Agent 进行质量检查

### 4. Validator Agent（验证代理）

**任务**：验证迁移质量

**输入**：来自 Translator Agent 的转换后代码

**检查项**：
- ArkTS 语法合规性
- API 版本 <= 22
- 编译无错误
- 类型安全

**执行验证**：

#### 方式1：使用 ohos-app-build-debug skill（推荐）

使用 [ohos-app-build-debug](../ohos-app-build-debug/) skill 进行编译验证、应用打包和上板验证首界面：

```bash
# 切换到项目目录
cd <project-path>

# 1. 编译验证（构建 HarmonyOS 应用）
python $SKILL_DIR/scripts/build.py

# 2. 应用打包（生成 HAP 安装包）
python $SKILL_DIR/scripts/install.py -f entry/build/default/outputs/default/entry-default-signed.hap

# 3. 上板验证首界面
python $SKILL_DIR/scripts/launch.py

# 4. 验证应用已启动
python $SKILL_DIR/scripts/screenshot.py -o ./screenshots/launched.png
```

#### 方式2：使用原生 DevEco Studio 工具（备选）

如果需要更详细的调试或使用 DevEco Studio 内置工具：

```bash
# 设置 DevEco Studio 环境变量
set "HUAWEI_DEV_HOME=C:\Program Files\Huawei\DevEcoStudio"
set "PATH=%HUAWEI_DEV_HOME%\tools\hvigor\bin;%PATH%"

# 使用 hvigorw 编译
cd <project-path> && hvigorw assembleApp

# 安装 HAP
hdc install entry/build/default/outputs/default/entry-default-signed.hap

# 启动应用
hdc shell aa start -b <bundle-name> -a <ability-name>
```

**输出**：
- 验证报告（通过/失败/警告）
- 问题清单（需修复项）
- 通过则传递给 Tester Agent，失败则返回 Translator Agent 修复

### 5. Tester Agent（测试代理）

**任务**：功能验证

**输入**：来自 Validator Agent 的已验证代码

**测试清单**：见 [TESTING.md](references/TESTING.md)

**输出**：
- 功能测试报告
- 测试用例通过率
- 失败用例清单
- **模块标记为已完成**，继续下一个模块
- **所有模块完成后**，触发 Feature Comparator Agent 和 UI Comparator Agent 进行全局比对

### 6. Feature Comparator Agent（功能比对代理）

**任务**：对比 Android 源码与迁移后的 HarmonyOS 代码，找出遗漏的功能

**执行时机**：**所有模块迁移完成后执行**（非每个模块后执行）

**执行步骤**：
```bash
# 运行功能比对脚本
python scripts/compare_features.py <android-source> <harmonyos-target>
```

**比对维度**：
- **功能清单对比**：扫描 Android 源码中的 Activity、Fragment、Service、BroadcastReceiver，对照 HarmonyOS 中的对应实现
- **API 调用覆盖**：检查 Android 中使用的系统 API 是否在 HarmonyOS 中都有对应实现
- **业务逻辑完整性**：比对核心业务类和方法是否完整迁移
- **资源文件覆盖**：检查字符串、图片、布局等资源是否完整迁移

**输出**：
- 功能覆盖率报告（已迁移/总数）
- 遗漏功能清单（含优先级标注）
- 部分迁移功能清单（需补充的内容）
- **反馈给 Planner Agent 的未完成项，用于制定下一轮补充迁移计划**

**详细比对方法**：见 [FEATURE_COMPARE.md](references/FEATURE_COMPARE.md)

### 7. UI Comparator Agent（UI 比对代理）

**任务**：比对 Android 和 HarmonyOS 应用的 UI 界面，确保视觉和交互一致性

**执行时机**：**所有模块迁移完成后执行**（非每个模块后执行）

**执行步骤**：
#### 方式1：自动化 UI 比对（推荐）

使用 Hypium 自动化框架启动应用并进行 UI 截图比对：

```bash
# 运行自动化 UI 比对脚本
迁移前Android 应用：
应用包名:com.simplemobiletools.gallery.pro
启动 Activity:com.simplemobiletools.gallery.pro.activities.SplashActivity.Orange
迁移后鸿蒙 应用：
应用包名:com.example.myapplication
启动 Activity:EntryAbility

python scripts/compare_ui_auto.py --android <android-package> --harmonyos <harmonyos-package>
```

#### 方式2：手动截图比对

```bash
# 运行 UI 比对脚本
python scripts/compare_ui.py <android-screenshots-dir> <harmonyos-screenshots-dir>

# 或比对布局文件
python scripts/compare_ui.py --layout <android-xml-dir> <harmonyos-ets-dir>
```

**比对维度**：
- **布局结构**：页面层级结构、组件排列方式
- **视觉样式**：颜色、字体、间距、圆角、阴影
- **尺寸适配**：在不同屏幕尺寸下的显示效果
- **交互元素**：按钮、输入框、列表等交互组件的一致性
- **动画效果**：转场动画、加载动画等

**输入要求**：
| 输入类型 | Android | HarmonyOS |
|----------|---------|-----------|
| 应用包名 | com.simplemobiletools.gallery.pro | com.example.myapplication |
| 启动 Activity | com.simplemobiletools.gallery.pro.activities.SplashActivity.Orange | EntryAbility |
| 截图 | PNG/JPG 文件 | PNG/JPG 文件 |
| 布局文件 | XML (res/layout/) | ETS (@Component) |
| 样式文件 | styles.xml | 主题配置 |

**比对维度**：
- **布局结构**：页面层级结构、组件排列方式
- **视觉样式**：颜色、字体、间距、圆角、阴影
- **尺寸适配**：在不同屏幕尺寸下的显示效果
- **交互元素**：按钮、输入框、列表等交互组件的一致性
- **动画效果**：转场动画、加载动画等
- **交互行为**：通过 Hypium 模拟用户操作，验证交互响应一致性

**输出**：
- UI 差异热力图（标注差异位置）
- 布局差异报告（缺失/多余的组件）
- 样式差异清单（颜色、字体、间距等）
- 交互差异说明
- **反馈给 Planner Agent 的 UI 未完成项，用于制定下一轮补充迁移计划**
- 修复建议和优先级

**详细比对方法**：见 [UI_COMPARE.md](references/UI_COMPARE.md)

## 参考文档

| 文档 | 用途 | 何时读取 |
|------|------|----------|
| [API_MAPPING.md](references/API_MAPPING.md) | Android/HarmonyOS API 对照表 | 执行转换时 |
| [COMPONENT_MAPPING.md](references/COMPONENT_MAPPING.md) | 组件转换模式 | 转换 UI 组件时 |
| [COMMON_PATTERNS.md](references/COMMON_PATTERNS.md) | 常见代码模式转换 | 遇到特定模式时 |
| [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) | 问题排查指南 | 出现错误时 |
| [FEATURE_COMPARE.md](references/FEATURE_COMPARE.md) | 功能比对方法和检查项 | 功能比对时 |
| [UI_COMPARE.md](references/UI_COMPARE.md) | UI比对方法和检查项 | UI比对时 |

## 当前项目配置

- **源码路径**：`C:\xxj\code\Simple-Gallery-master`
- **目标路径**：`C:\workspace\0210`
- **API 限制**：<= API 22
- **鸿蒙语法参考文档**：`C:\xxj\code\docs`
- **鸿蒙API接口参考文档**：`C:\xxj\code\zh-cn\application-dev`

## 迭代循环总结

### 第一阶段：模块迁移循环

```
┌─────────────────────────────────────────────────────────────────┐
│                     模块迁移循环                                │
│                  (逐个处理所有计划模块)                          │
└─────────────────────────────────────────────────────────────────┘

  模块N ──▶ Translator ──▶ Validator ──▶ Tester ──▶ 模块完成 ✓
           Agent           Agent          Agent
         (代码转换)      (质量验证)      (功能测试)
                                              │
                                    ┌─────────┴─────────┐
                                    ▼                   ▼
                              有更多模块？      所有模块完成
                                    │                   │
                                    ▼                   │
                              ┌──────────┐             │
                              │ 模块N+1  │             │
                              └──────────┘             │
                                    │                   │
                                    └───────────────────┘
                                                       │ 所有模块完成
                                                       ▼
                                        ┌──────────────────────────┐
                                        │   进入全局比对阶段        │
                                        └──────────────────────────┘
```

### 第二阶段：全局比对循环

```
┌─────────────────────────────────────────────────────────────────┐
│                     全局比对阶段                                │
│              (所有模块迁移完成后执行一次)                        │
└─────────────────────────────────────────────────────────────────┘

  Feature Comparator ──┐
       Agent          │ 并行执行
                       ├──▶ 遗漏项收集 ──▶ Planner Agent ──┬─▶ 有遗漏项？
  UI Comparator ──────┘       (合并)       (制定补充计划)   │
       Agent                                                  │
                                                             ▼
                                                    ┌──────────────────┐
                                                    │  回到模块迁移循环 │
                                                    │  处理遗漏项模块   │
                                                    └──────────────────┘
                                                             │
                                    ┌────────────────────────┴────────┐
                                    ▼                                 ▼
                              有遗漏项？                        无遗漏项
                                    │                                 │
                                    ▼                                 ▼
                            ┌──────────────┐                  ┌──────────────┐
                            │ 继续迭代     │                  │  迁移完成    │
                            │ (下一轮)     │                  └──────────────┘
                            └──────────────┘
```

### 完整迭代流程说明

1. **初始规划**：Planner Agent 分析源码，制定模块化迁移计划
2. **模块迁移循环**：
   - 对每个模块依次执行：Translator → Validator → Tester
   - 完成一个模块后标记为已完成，继续下一个
   - 直到所有计划模块迁移完成
3. **全局比对**：
   - 所有模块完成后，执行 Feature Comparator 和 UI Comparator
   - 收集遗漏的功能和 UI 差异项
4. **迭代判断**：
   - 如果有遗漏项：Planner Agent 制定补充计划，回到步骤2
   - 如果无遗漏项：迁移完成

### 完成标准

迁移工作完成需满足以下所有条件：

| 检查项 | 标准 | 负责代理 |
|--------|------|----------|
| 代码转换率 | 100% 文件已转换 | Translator Agent |
| 语法验证 | 0 错误，< 10 警告 | Validator Agent |
| 编译状态 | 编译通过 | Validator Agent |
| 功能测试 | 核心功能 100% 通过 | Tester Agent |
| 功能覆盖率 | ≥ 95% | Feature Comparator Agent |
| UI 一致性 | 核心页面 100% 匹配 | UI Comparator Agent |
| 性能对比 | 响应时间差异 < 20% | Tester Agent |

### 状态文件格式

每次迭代后，Planner Agent 更新 `migration_status.yaml`：

```yaml
# migration_status.yaml
project:
  name: "SimpleGallery"
  source: "C:\\xxj\\code\\Simple-Gallery-master"
  target: "C:\\workspace\\0210"

# 迭代信息
iteration:
  current: 2  # 当前迭代轮次
  phase: "module_migration"  # 模块迁移阶段 | 全局比对阶段

overall_progress:
  total_modules: 8
  completed_modules: 3
  in_progress: "数据模型模块"
  completion_percentage: 37.5%

modules:
  - name: "数据模型模块"
    status: "completed"
    files:
      - "Photo.ets ✓"
      - "Album.ets ✓"
    issues: []

  - name: "数据访问层模块"
    status: "completed"
    files:
      - "PhotoRepository.ets ✓"
      - "AlbumRepository.ets ✓"
    issues: []

  - name: "业务逻辑层模块"
    status: "in_progress"
    files:
      - "MainViewModel.ets ⚠ (部分API未实现)"
      - "SettingsViewModel.ets ✓"
    issues:
      - type: "missing_api"
        description: "批量删除API未实现"
        priority: "high"

  - name: "UI层模块"
    status: "pending"
    files: []

# 全局比对结果（所有模块完成后填充）
global_comparison:
  status: "pending"  # pending | in_progress | completed
  missing_features:
    - feature: "照片批量删除"
      module: "业务逻辑层模块"
      priority: "high"
      found_by: "Feature Comparator Agent"
      status: "待实现"

    - feature: "照片分享功能"
      module: "业务逻辑层模块"
      priority: "medium"
      found_by: "Feature Comparator Agent"
      status: "待实现"

  ui_differences:
    - page: "MainPage"
      differences:
        - type: "missing_component"
          description: "缺少滑动删除手势"
          priority: "medium"
      found_by: "UI Comparator Agent"
      status: "待修复"

last_update: "2026-02-07T17:15:00"
next_step: "继续迁移 业务逻辑层模块"
```

