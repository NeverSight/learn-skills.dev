---
name: meishe-effect-kit-ios
description: 将美摄 NveEffectKit 3.16.1 系接入、扩展、修复、优化或升级现有 Objective-C/Swift iOS 工程。用于客户已有相机、录制、直播、视频帧或单图链中按需接入完整美颜大模块（美肤、美型、微整形）或其任一子模块，以及完整美妆（组合妆容、九类单妆与美瞳）、滤镜、人脸道具、背景分割、自定义动画贴纸和 CVPixelBuffer/OpenGL 纹理渲染，并将效果结果安全接入预览、录制或 RTC/直播消费者；也用于按任务类型检查 framework/core 配对、Bundle-ID 授权、模型、素材证书、方向、生命周期、交互 smoke 和性能。不要用它创建新的 demo 工程。
---

# Meishe Effect Kit iOS

将 NveEffectKit 的目标能力最小化接入客户现有工程。本 skill 以客户提供的同版本商业 SDK、模型、素材和授权为前提，不携带、不下载这些资产。

## 首次版本提示

每个新任务首次使用本 skill 时，先输出一次以下提示；同一任务后续响应不重复。
不要求用户确认，提示后继续执行本次需求：

> 版本提示：当前 Skill 基于美摄 SDK 3.16.1，并向后兼容；若目标项目使用更高版本 SDK，可能存在效果差异，请从[美摄官网开发者中心](https://www.meishesdk.com/downloads/)获取对应版本的 Skill。

## 任务路由与门禁

先根据请求分类；分类或功能范围依赖工程现状时，只读项目源码和配置后再确定：

- `first-integration`：无可用 NVE 基础链，执行完整基础门禁和功能门禁。
- `add-feature`：已有授权、单例和渲染链，只执行新增功能门禁；未检测到基础链时提升为 `first-integration`。
- `repair`：先复现和定位，只为复现或验证所需的缺失依赖重开专项门禁。
- `optimize`：先建立性能基线；缺少设备或真实输入只阻塞对应测量。
- `upgrade`：要求新版交付包并执行版本漂移审计。
- `audit`：保持只读；只有运行时结论需要对应运行环境。

只读工程检查可以用于识别现有基础链和产品配置，但不能搜索商业依赖、运行依赖门禁或修改代码。范围仍含糊且会改变依赖清单时，只问一个最小问题；完整分类、功能 profile、范围选择和阻塞输出见 [任务路由与专项门禁](references/task-routing-and-gates.md)。

以下范围规则在主流程中固定：

- `first-integration`/`add-feature` 的美颜范围不明确时，一次性收集“完整美颜、美肤、美型、微整形、自定义具体”；用户已明确范围时直接映射，不重复询问。其他任务只有同时新增或重定义范围时才触发选择。
- “完整美妆”“全量美妆”“全部美妆功能”直接映射为 `makeup-suite`，不得缩减为单项 `makeup`。
- 录制、预览和 RTC/直播是输出消费者，不是效果 profile。

商业依赖只接受用户提供的精确路径，或在用户明确授权的 `--sdk-root`/`--resource-root` 内查找。`--project-root` 只授权读取客户源码和配置，不授权搜索 framework、core、授权、模型或素材；缺失时列出用途、阻塞原因和合法获取路径，不扩大搜索范围，也不用 Demo 资产替代。

范围确认后，对 `first-integration`/`add-feature` 运行只读门禁；完整参数见路由 reference：

```text
python3 -B <skill>/scripts/preflight_gate.py \
  --project-root <项目根目录> --task <任务ID> --features <功能profile> \
  [用户明确提供或授权的依赖参数]
```

退出 `2` 时在改代码前报告任务分类、已确认事实、缺失项、阻塞原因和获取路径；退出 `1` 时只询问输出中的最小未知项。

## 按需加载

- 首次接入、授权、模型、SDK 配对、生命周期：读 [integration-and-lifecycle.md](references/integration-and-lifecycle.md)。已有基础链的单纯 UI/状态修复不加载。
- 修改帧处理、单图、方向、输出所有权或销毁：读 [rendering-pipelines.md](references/rendering-pipelines.md)。
- 任何实时相机接入、预览/录制镜像、摄像头切换或方向修复：必须读并执行 [帧方向与镜像契约](references/frame-geometry-contract.md)；它是独立分发时的完整方向事实来源，不等待任何未由用户提供的外部工程。
- 修改实时 UI 状态提交、摄像头切换，增加美颜/美妆/滤镜/道具等效果模块，或把结果接入预览、录制、RTC/直播等消费者：读 [realtime-state-and-output.md](references/realtime-state-and-output.md)。
- 新增、修复或审计录制输出、音视频时基、前摄成片镜像、writer 停止顺序、保存结果或录制 UI：同时读 [recording-output.md](references/recording-output.md)。
- 用户未提供设计且工程没有现有效果面板，或任务涉及默认底部入口栏、入口扩容、文字换行：读 [default-ui.md](references/default-ui.md)。
- 美颜、美型、微整形：只读 [beauty-and-shaping.md](references/beauty-and-shaping.md)。
- 美妆、组合妆容、滤镜、道具、背景分割、自定义动画贴纸：完整读取 [makeup-filter-prop.md](references/makeup-filter-prop.md)。
- 资源错误、兼容、性能或崩溃排障：完整读取 [resources-performance-troubleshooting.md](references/resources-performance-troubleshooting.md)。
- 接入后验收：只在代码发生变化或用户要求验证时读 [acceptance-testing.md](references/acceptance-testing.md)。
- 精确属性/模型映射或版本升级：查询 [baseline-3.16.1.json](references/baseline-3.16.1.json) 的相关键；普通任务不要整体加载。

## 实施流程

### 1. 发现工程事实

```text
python3 -B <skill>/scripts/inspect_project.py \
  --project-root <项目根目录> [--sdk-root <用户明确授权的SDK目录>]
```

定位 app target、依赖方式、最低 iOS、语言、帧入口、串行队列、输入输出类型、EAGLContext、输出消费者和生命周期 owner。不要询问能从工程读取的事实，不引入第二套媒体架构、页面或 NVE 单例管理器。

实时帧链保存 geometry 摘要，并按 [帧方向与镜像契约](references/frame-geometry-contract.md) 写出输入、SDK、预览和录制的方向/镜像 owner；存在未知项时先标记验证阻塞，不通过叠加 transform 试错。

实现语言跟随被修改 owner。SDK 符号和行为以客户公共头文件、实际二进制和同版本基线为准；Swift 导入名称以客户 framework 的编译结果为准。

### 2. 定义最小改动

在修改前写清功能 profile、输入/输出模式、改动 owner、用户入口、typed state、资源准备和验收入口。只改现有帧入口、效果状态层和生命周期 owner，复用客户 UI、队列、命名、录制器和资源定位器。

按现有链选择渲染模式：

- buffer 输入、buffer 下游：`buffer-buffer`。
- buffer 输入、OpenGL 下游：`buffer-texture`。
- texture 输入：`texture-texture`。
- 单图：复用 renderer，不引入相机或录制模块。

UI 按“用户设计 → 工程现有体系 → [默认 UI](references/default-ui.md)”选择。采用默认 UI 时必须让共享底栏、全部面板和状态控件从同一个 `NVEEffectTheme`/`nve.default-theme.v1` 实例读取语义颜色，禁止各面板独立硬编码主题色。效果模块保留独立入口和状态；录制、RTC/直播等输出消费者复用客户现有实现，不并入效果 profile。

### 3. 准备、提交和回收

首次接入保持：验证 SDK 授权 → 初始化请求功能的全部必需模型 → 获取单例 → 帧外安装素材并构造长生命周期效果对象 → 接通帧流。属性、模型、package 类型和 container 映射只从 [3.16.1 基线](references/baseline-3.16.1.json) 与目标功能 reference 读取。

实时链统一执行 [状态与输出消费规范](references/realtime-state-and-output.md) 的 `desired → pending latest → delta apply → render → per-consumer ownership`，不得为不同效果模块复制 capture/render coordinator。实施中保持：

- NveEffectKit 与供应方匹配的 core 变体成对使用；授权和每个必需模型成功后才能首次访问单例。
- 初始 typed state 作为第一份 pending state，在首帧 render 前应用。
- 每个效果对象、container 项和 package ID 有唯一 owner；切换、重置和移除只修改该 owner 的对象。
- package 类型来自基线映射，真实 package ID 来自安装结果或匹配 core manager；安装和解析不阻塞 frame queue。
- 效果 mutation、camera transition 和 render 在同一稳定串行时序提交；主线程与 render queue 不互相同步等待。
- 每个 rotation/mirror 维度只有一个 owner；preview 只消费 presentation-ready 帧。
- 保留客户工程已经真机验证的 mirror owner；首次接入默认使用 NVE-owned mirror。只有按方向契约复现并隔离出 SDK mirror 输出全零时，才切换到 capture-owned 兼容策略，不能全局替换或逐帧自动回退。
- `config.isFromFrontCamera` 始终使用本帧 camera position 快照；它与 mirror owner 独立，兼容策略也不能省略。
- 每个非空 `NveRenderOutput` 在所有路径恰好回收一次；每个异步消费者在回收前取得自己的 copy、retain 或 lease。
- preview 可 latest-wins；录制沿用客户 writer、源 PTS 和既定背压策略，preview mailbox/flush 不影响录制。
- 销毁顺序固定为：停止帧源 → 停止接收并排空有序消费者 → 排空 render queue → 释放效果/GL 状态 → 唯一 owner 销毁单例。

`makeup-suite` 没有既有产品规则时，执行 [美妆 reference](references/makeup-filter-prop.md) 的“组合妆基底 + 单妆覆盖”状态机，不从 SDK 当前对象状态或属性写入顺序推断产品语义。

Objective-C 生命周期与 render 以 [session 模板](assets/templates/objective-c/) 为基准；Swift 只按需裁剪 [互操作模板](assets/templates/swift/NVESwiftSDKInterop.swift) 和 realtime reference 列出的薄模板，不整包复制。

### 4. 自动验收后交付

代码发生变化后至少运行：

```text
python3 -B <skill>/scripts/validate_integration.py \
  --project-root <项目根目录> --features <接入功能profile> \
  [采用无设计默认 UI 时 --default-ui] [请求默认录制 UI 时 --recording-ui] \
  [用户明确提供或授权的依赖参数]

bash <skill>/scripts/macos_smoke_test.sh \
  (--workspace <workspace> | --project <project>) --scheme <scheme> \
  [--derived-data <隔离目录> --require-resource <app内相对路径>]
```

改动用户入口且存在可运行 destination 时，复用或新增最小 UI smoke，并通过 `--test --only-testing` 执行。静态验证、编译、启动/UI、真机效果/性能分别报告 `通过/失败/未执行` 和证据；构建通过不能替代功能、方向或性能验收。完整命令、矩阵和阻塞报告见 [接入后自动验收](references/acceptance-testing.md)。

## 不可违反

- 不创建新 demo，不复制 demo 的完整相机/UI/录制代码，不替换客户媒体架构。
- 不内置、提交、打印或推断 SDK/素材授权内容，不复用 demo 授权。
- 不硬编码本仓库路径；外部位置来自客户工程、参数或配置。
- 不把本地文档示例置于公共头文件和实际交付资源之上；不复制已知错误、旧模型名或非法 JSON。
- 不声称 Xcode、UI、真机、视觉或性能已验证，除非对应命令/设备实际运行并记录结果。

## 维护新版本

收到供应方新资料先运行：

```text
python3 -B <skill>/scripts/audit_vendor_drop.py --source-root <新版资料根目录> \
  --baseline <skill>/references/baseline-3.16.1.json
```

先审阅 API、最低系统、core 配对、模型、素材类型和平台 slice 漂移，再依次更新基线、门禁、功能 reference、验证器和受影响模板。效果能力更新 module adapter；预览、录制、RTC/直播和导出更新 output consumer 契约。

只有已复现、跨模块或消费者可复用且无法由规范消除的语言/API 陷阱，才增加薄模板；不为每个功能复制 Swift/Objective-C 大模板，也不在没有跨项目证据时增加通用录制器。

每次修改后运行 `python3 -B <skill>/scripts/self_test.py` 和 skill quick validation。测试只使用 skill 内文件或运行时生成的脱敏 fixture。所有 Python 脚本用 `python3 -B` 运行，交付前确认 `scripts/` 中没有 `__pycache__`/`.pyc`。
