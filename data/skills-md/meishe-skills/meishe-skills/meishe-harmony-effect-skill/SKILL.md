---
name: meishe-harmony-effect-skill
description: 生成或修改 HarmonyOS ArkTS 项目中基于 libNvStreamingSdkCore 的美摄/Nv EffectSDK 集成代码。适用于 NvsEffectScheduler 相机预览、NvsEffectRenderCore buffer/离屏/编辑渲染、SDK 初始化、人脸/人体检测模型初始化、素材包安装/升级/卸载、AR Scene、美颜、美妆、道具、滤镜、字幕、贴纸、转场，以及内建特效参数查询。
---

# MeiShe Harmony EffectSDK

在 HarmonyOS ArkTS 项目中通过 `libNvStreamingSdkCore` 集成美摄/Nv EffectSDK 时使用此 skill。

## 起手检查

1. 修改代码前先检查当前工作区中用户明确提供的客户项目：确认 SDK 包名、HAR 依赖、导出的 `.d.ets` 声明、现有 Camera/XComponent 结构，以及资源目录布局。
2. 以客户项目本地 SDK 声明为准。此 skill 的参考资料基于 demo 的 3.16.1 API，但不要把客户的兼容 SDK 版本强行改回 3.16.1。
3. 如果客户项目缺少必需的模型文件或素材包，先暂停实现，并告诉用户应该把文件放到哪里，再生成依赖这些资源的代码。

## 分发使用规则

- 此 skill 必须能在没有参考 demo 的环境使用。默认只依赖 skill 自带的 `references/` 和当前用户明确提供的客户工程文件。
- 不要尝试访问、推断或依赖开发者本机、客户电脑或固定 demo 路径中的文件；任何未由当前用户明确提供的路径，都不能作为生成客户代码的前置条件。
- 如果用户没有提供客户工程，只根据 skill 自带参考资料生成可复制的接入代码、目录建议和待确认项；需要校验 SDK 声明时，请用户提供工程路径、HAR 导出声明或相关 `.d.ets` 文件。
- 只有用户明确提供参考 demo 路径、demo 文件，或明确要求分析 demo 时，才读取该 demo。参考 demo 只作为补充资料，最终仍以客户工程本地 SDK 声明和资源文件为准。

## 参考资料路由

- 处理 `NvsEffectScheduler.Scheduler` 相机预览集成、surface 连接、方法调用顺序、滤镜、字幕、贴纸、转场和释放顺序时，读取 `references/harmony-effectsdk-scheduler.md`。用户只说“拍摄预览、相机预览、实时美颜、实时道具”，且没有说明已有 buffer 数据时，默认走这篇文档。
- 处理已有 buffer、camera buffer、图片 buffer、视频帧 buffer、离屏渲染、编辑渲染、逐帧处理或 `NvsEffectRenderCore.RenderCore` 接入时，读取 `references/harmony-effectsdk-rendercore.md`。
- 处理 `AR Scene` 特技、美颜、美型、微整形、美妆、道具和 `AR Scene` 参数时，读取 `references/harmony-effectsdk-fx-arscene.md`。
- 处理人体/人脸检测模型文件、模型组合、初始化顺序和 rawfile 放置位置时，读取 `references/harmony-effectsdk-models.md`。
- 处理素材包安装、版本升级、卸载、package id 获取、素材类型选择和安装结果判断时，读取 `references/harmony-effectsdk-asset-package.md`。
- 处理 `AR Scene` 常用参数时，优先读取 `references/harmony-effectsdk-fx-arscene.md` 中的 AR Scene 常用参数表。
- 处理其它 SDK 内建特效参数，或 AR Scene 常用参数表没有覆盖的非常规参数时，先读取 `references/内建特效参数索引.md`，再只读取 `references/effects/` 下匹配的文件；该索引和目录只包含可对外提供的内建特技，未列出的特技不要作为客户可用能力生成代码。

## 内建特效参数

设置 SDK 内建特效参数时，不要猜参数名。

- 如果目标特效是 `AR Scene`，先使用 `references/harmony-effectsdk-fx-arscene.md` 中的 AR Scene 常用参数表；该表用于高频美颜、美型、美妆、道具和 AR Scene 包参数查询。
- 如果目标不是 `AR Scene`，或 AR Scene 常用参数表没有覆盖用户要的参数，再在 `references/内建特效参数索引.md` 中定位，并读取 `references/effects/` 下链接到的文件。
- 如果用户只给出参数名，用 `rg` 搜索 `references/effects/`，然后只读取与目标特效相关的命中文件。
- 如果目标特效或参数只出现在内部源文档、历史内部资料，或不在 `references/内建特效参数索引.md` 中，不要向客户输出该特技的接入代码；说明当前可对外资料未覆盖该能力。
- 保留参考文件中的准确特效名、参数名、类型、范围、默认值、拼写、大小写和版本说明。
- 按参考文件中的参数类型生成 `setNumberVal(...)`、`setBooleanVal(...)`、`setStringVal(...)`、`setColorVal(...)` 或 `setPosition2DVal(...)`。

## 美颜需求澄清

用户只说“接美颜”“加美颜”“实时美颜”时，不要直接等同为单个磨皮参数。先按 `harmony-effectsdk-fx-arscene.md` 的“美颜需求澄清”列出能力，让用户选择具体需要哪些：基础磨皮、高级磨皮、美白、红润、锐化、去油光、祛黑眼圈、祛法令纹、亮眼、白牙、人脸/默认 LUT、瘦脸、小脸、窄脸、大眼、瘦鼻、下巴、额头、嘴角等。

如果用户说不清楚、让你先写、或明确要“全套美颜”，按 `harmony-effectsdk-fx-arscene.md` 生成完整美颜控制集合。完整集合应生成可调控制和方法入口，默认强度保持关闭或 `0`，不要把所有强度默认开到最大。

## 代码生成规则

- 用户只说拍摄预览、相机预览、实时美颜、实时美妆、实时道具或实时滤镜，且没有说明已有 buffer 数据时，默认使用 `NvsEffectScheduler.Scheduler`。
- 用户说明已有 buffer、camera buffer、图片 buffer、视频帧 buffer，或明确要离屏渲染、编辑渲染、逐帧处理时，使用 `NvsEffectRenderCore.RenderCore`。
- 在初始化模型、安装素材包或创建 scheduler 前，先初始化 `NvsEffectSdkContext`。
- 涉及人脸、美颜、美妆、形变、道具、分割、手势、Avatar、眼部或人脸检测能力时，创建依赖特效前先查阅 `harmony-effectsdk-models.md`。
- 涉及 `.videofx`、`.arscene`、`.makeup`、`.facemesh`、`.warp`、字幕、贴纸或转场素材包时，先查阅 `harmony-effectsdk-asset-package.md`，并使用返回的非空 `packageId`。
- `.videofx` 滤镜包、校色包、肤色包是独立视频特效，不属于 `AR Scene` 特技；安装后用 scheduler 创建独立 effect，不要写入 `AR Scene` 参数。
- scheduler 预览场景中，将 CameraKit 的 `PreviewOutput` 连接到 scheduler 输入 surface，并将 scheduler 输出 surface 连接到 `XComponent`。
- 创建任何 scheduler 特效对象后，除非目标 SDK 方法明确说明不需要，否则都要通过 `addRenderEffects(...)` 加入渲染。
- Scheduler 实时预览中调用 `createVideoEffect(..., realTimeMode)` 时，`realTimeMode` 传 `true`。

## 验证

修改客户项目后，运行就近可用的 Harmony/ArkTS 构建或分析命令。如果本地无法构建项目，说明已经检查了什么，以及还有哪些内容未验证。
