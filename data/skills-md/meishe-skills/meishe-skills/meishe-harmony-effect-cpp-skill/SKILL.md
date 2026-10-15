---
name: meishe-harmony-effect-cpp-skill
description: 生成或修改 HarmonyOS C++/NAPI 项目中基于美摄/Nv EffectSDK 的原生集成代码。适用于 CNvsEffectSdkContext 初始化、CNvsEffectRenderCore buffer/GPU texture/离屏/拍摄预览渲染、EGL 和 XComponent NativeWindow 输出、ArkTS 到 C++ NAPI 桥接、CameraKit/ImageReceiver 设备旋转监听、frame.rotation/sensorOrientation/displayRotation/physicalOrientation 区分、旋转后 AR Scene 人脸类效果消失排查、模型初始化、素材包安装/升级/卸载、AR Scene、美颜、美型、美妆、道具、滤镜、字幕、贴纸、转场，以及内建特效参数查询。
---

# MeiShe Harmony EffectSDK C++ Skill

在 HarmonyOS 项目中通过 C++/NAPI 集成美摄/Nv EffectSDK 时使用此 skill。C++ 版默认围绕 `CNvsEffectSdkContext`、`CNvsEffectRenderCore`、NAPI、EGL/NativeWindow 和业务 buffer/texture 渲染链路组织代码。

## 起手检查

1. 修改代码前先检查用户明确提供的客户项目：`oh-package.json5`、`build-profile.json5`、`CMakeLists.txt`、`src/main/cpp`、`src/main/ets/cpp`、`src/main/cpp/types`、SDK 头文件、SDK `.so`、rawfile 资源和现有 NAPI 注册入口。
2. 以客户项目本地 C++ 头文件和工程结构为准。参考资料提供 C++ 集成基线，但不要把客户工程的 SDK 版本、库路径、模块名或资源目录强行改成示例写法。
3. 如果客户项目缺少必需的 SDK C++ 头文件、运行库、授权文件、模型文件或素材包，先暂停生成依赖这些资源的代码，明确列出缺失项和建议放置目录，并提示用户补齐。尤其缺少 C++ 头文件时，不要凭记忆写 `CNvs*`、`Nvs*` 或 SDK enum/struct/function 调用。
4. C++ 版不要默认走 ArkTS `NvsEffectScheduler.Scheduler`。拍摄预览默认按 CameraKit/ImageReceiver 或业务已有 buffer 进入 NAPI，再由 `CNvsEffectRenderCore` 渲染到 `XComponent` 对应的 NativeWindow。
5. 拍摄预览涉及 AR Scene 人脸类能力时，先确认 ArkTS 监听设备方向，并逐帧向 native 传入 `rotation`、`mirrored`、`sensorOrientation`；不要只把固定的 `cameraDevice.cameraOrientation` 当作 `sensorOrientation`。

## 分发使用规则

- 不要尝试访问、推断或依赖开发者本机、客户电脑或固定参考工程路径中的文件；任何未由当前用户明确提供的路径，都不能作为生成客户代码的前置条件。
- 不要自行扩大文件搜索范围来发现客户代码、demo 或 SDK，例如不要从父目录、下载目录、历史项目目录、客户代码仓库集合或固定 demo 路径中查找。只读取用户明确给出的工程路径、文件路径或当前任务已确认的路径范围。
- 如果用户没有提供客户工程，只根据 skill 自带参考资料生成可复制的接入代码、目录建议和待确认项；需要校验 SDK 声明时，请用户提供工程路径、C++ 头文件、`.so` 路径或 NAPI 类型声明。

## 参考资料路由

- 处理 Harmony native 工程配置、`CMakeLists.txt`、`libentry.so` 类型包、`oh-package.json5`、`build-profile.json5`、头文件和 `.so` 链接时，读取 `references/harmony-effectsdk-cpp-project-setup.md`。
- 处理 ArkTS 到 C++ 的 NAPI 导出、`.d.ts` 声明、wrapper/controller、payload/status 类型、`ArrayBuffer`/TypedArray 解析和错误返回时，读取 `references/harmony-effectsdk-cpp-napi-bridge.md`。
- 处理 SDK 授权、rawfile 授权读取、writable root、`CNvsEffectSdkContext::InitWithLicData`、`SetWritableRootLocation`、`CloseHumanDetection` 和 `Close` 时，读取 `references/harmony-effectsdk-cpp-sdk-runtime.md`。
- 处理 `CNvsEffectRenderCore`、EGL、NativeWindow、RGBA buffer 上传、GPU texture、`RenderMultiInstanceWithOglTexture`、HostBuffer buddy info、`frame.rotation`/`frame.sensorOrientation`/`displayRotation`/`physicalOrientation`、离屏/逐帧/拍摄预览渲染和释放顺序时，读取 `references/harmony-effectsdk-cpp-rendercore.md`。
- 处理人脸/人体/手势/Avatar/眼球/高级美颜/分割模型初始化、模型文件和 `.dat` 数据包时，读取 `references/harmony-effectsdk-cpp-models.md`。
- 处理 `.videofx`、`.arscene`、`.makeup`、`.facemesh`、`.warp`、字幕、贴纸、转场素材包安装、升级、卸载、package id 获取和素材类型选择时，读取 `references/harmony-effectsdk-cpp-asset-package.md`。
- 处理 `AR Scene` 特技、美颜、美型、微整形、美妆、道具和 `AR Scene` 高频参数时，读取 `references/harmony-effectsdk-cpp-fx-arscene.md`。
- 处理旋转手机后美颜、美型、美妆、口红、道具等 `AR Scene` 人脸相关效果整体消失时，先读取 `references/harmony-effectsdk-cpp-rendercore.md` 检查方向链路，再检查素材包、参数或 effect chain。
- 处理 C++ 参数 setter 选择、颜色/位置参数构造、general/time 参数和普通内建特效参数写入时，读取 `references/harmony-effectsdk-cpp-param-setters.md`。
- 处理其它 SDK 内建特效参数，或 AR Scene 常用参数表没有覆盖的非常规参数时，先读取 `references/内建特效参数索引.md`，再只读取 `references/effects/` 下匹配的文件；该索引和目录只包含可对外提供的内建特技，未列出的特技不要作为客户可用能力生成代码。

## 内建特效参数

设置 SDK 内建特效参数时，不要猜参数名。

- 如果目标特效是 `AR Scene`，先使用 `references/harmony-effectsdk-cpp-fx-arscene.md` 中的 AR Scene 常用参数表。
- 如果目标不是 `AR Scene`，或 AR Scene 常用参数表没有覆盖用户要的参数，再在 `references/内建特效参数索引.md` 中定位，并读取 `references/effects/` 下链接到的文件。
- 如果用户只给出参数名，用 `rg` 搜索 `references/effects/`，然后只读取与目标特效相关的命中文件。
- 如果目标特效或参数只出现在内部源文档、历史内部资料，或不在 `references/内建特效参数索引.md` 中，不要向客户输出该特技的接入代码；说明当前可对外资料未覆盖该能力。
- 保留参考文件中的准确特效名、参数名、类型、范围、默认值、拼写、大小写和版本说明。
- 按 `references/harmony-effectsdk-cpp-param-setters.md` 生成 C++ setter，例如 `SetFloatGeneralParamVal(...)`、`SetBooleanGeneralParamVal(...)`、`SetStringGeneralParamVal(...)`、`SetColorGeneralParamVal(...)` 或 `SetPosition2DGeneralParamVal(...)`。不要为 C++ 代码生成 ArkTS 的 `setNumberVal(...)`、`setStringVal(...)` 等调用。

## 美颜需求澄清

用户只说“接美颜”“加美颜”“实时美颜”时，不要直接等同为单个磨皮参数。先按 `harmony-effectsdk-cpp-fx-arscene.md` 的“美颜需求澄清”列出能力，让用户选择具体需要哪些：基础磨皮、高级磨皮、美白、红润、锐化、去油光、祛黑眼圈、祛法令纹、亮眼、白牙、人脸/默认 LUT、瘦脸、小脸、窄脸、大眼、瘦鼻、下巴、额头、嘴角等。

如果用户说不清楚、让你先写、或明确要“全套美颜”，按 `harmony-effectsdk-cpp-fx-arscene.md` 生成完整美颜控制集合。完整集合应生成可调控制和方法入口，默认强度保持关闭或 `0`，不要把所有强度默认开到最大。

## 代码生成规则

- 用户说“拍摄预览、相机预览、实时美颜、实时道具、已有 camera buffer、图片 buffer、视频帧 buffer、离屏渲染、编辑渲染、逐帧处理”时，默认使用 C++ `CNvsEffectRenderCore` 链路。
- 拍摄预览场景中，ArkTS 负责权限、CameraKit、`XComponent`、`ImageReceiver`、重力传感器方向监听或其它帧来源；C++ 负责 SDK runtime、EGL、RenderCore、effect chain、NativeWindow 输出和状态返回。
- ArkTS 每帧传入的 `rotation` 只用于输入纹理归一化；`sensorOrientation` 必须结合设备当前方向动态计算并传给 C++，最终赋给 `HostBufferInfo.physicalOrientation`；`displayRotation` 只在 SDK 头文件或当前输入格式确认需要时设置，不要和前两者混用。
- 如果画面能正常显示，但美颜、美型、美妆、口红、道具等 `AR Scene` 人脸相关效果在旋转后整体消失，优先检查方向链路：ArkTS 是否监听重力传感器并维护 `deviceRotationDegrees`、逐帧 payload 是否更新 `sensorOrientation`、C++ 是否写入 `hostInfo.physicalOrientation = frame.sensorOrientation`、`frame.rotation` 是否只用于纹理归一化、`displayRotation` 是否被误改。
- 在初始化模型、安装素材包或创建 effect 前，先初始化 `CNvsEffectSdkContext`。
- 涉及人脸、美颜、美妆、形变、道具、分割、手势、Avatar、眼部或人脸检测能力时，创建依赖特效前先查阅 `harmony-effectsdk-cpp-models.md`。
- 涉及 `.videofx`、`.arscene`、`.makeup`、`.facemesh`、`.warp`、字幕、贴纸或转场素材包时，先查阅 `harmony-effectsdk-cpp-asset-package.md`，并使用返回的非空 `packageId`。
- `.videofx` 滤镜包、校色包、肤色包是独立视频特效，不属于 `AR Scene` 特技；安装后通过 `CNvsEffectSdkContext::CreateVideoFx(packageId, ratio, true)` 创建辅助 effect，并加入 RenderCore 的 effect chain。
- `AR Scene`、滤镜、字幕、贴纸、转场等效果对象应复用；逐帧路径只更新 buffer/texture 和参数，不要反复创建同一套 effect。

## 验证

修改客户项目后，运行就近可用的 Harmony native 构建或分析命令。如果本地无法构建项目，说明已经检查了什么，以及还有哪些内容未验证。
