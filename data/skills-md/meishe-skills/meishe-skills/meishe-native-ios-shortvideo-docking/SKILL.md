---
name: meishe-native-ios-shortvideo-docking
description: Independently integrate, configure, validate, and troubleshoot the official Meishe ShortVideo native iOS package in an Xcode project. Use for black-box Pods-NvShortVideoEdit integration, generated Swift demo UI and feature configuration, Podfile and Info.plist setup, Bundle Identifier/license/server questions, handoff generation, and version-scoped native iOS fixes; never substitute Flutter, React Native, or Android packages.
---

# 美摄原生 iOS 短视频 Demo 接入

本 skill 只处理原生 iOS 路线。完成输入预检后运行固定脚本、检查报告，并给出 Xcode、CocoaPods、签名、配置和验证步骤。

脚本运行环境要求 Python `3.9+`；结构校验会拒绝未声明兼容性的新版类型语法。

## 修改与操作审批

- 修改本 skill 前，先向用户列出简短中文计划、影响范围和验证方式，获得明确同意后才能写入；扩大范围必须再次获批。用户手动修改的内容不得擅自覆盖或撤销。
- 集成脚本不执行 CocoaPods 下载、`xcodebuild` 或远程依赖解析。到达依赖、构建或设备操作边界时读取 `references/dependency-installation.md`，一次性列出绝对目录、全部命令/操作、执行顺序、用途和成功标志；必须同时列出 Xcode 操作和完整命令行，二者不能互相替代。然后让用户明确选择 `用户执行` 或 `自动执行`；未选择时暂停。
- 展示二选一时，必须在当前轮次的最终可见回复中逐项重复上述完整清单和两个选择。不得把命令只放在 commentary、工具输出、折叠的“处理中”区域或报告文件中，不得让用户回看上一条消息；发送该回复后停止本轮工具调用，等待用户选择。
- `用户执行`：把完成当前阶段所需的全部命令交给用户，不再逐条追问；用户返回结果后继续。`自动执行`：由 Agent 执行已列出的任务内操作，并先明确提示会额外消耗 Token 和时间。
- 受操作系统、工具链版本、依赖缓存、网络、签名和设备环境差异影响，手动接入或运行可能报错。遇到任何报错，要求用户复制执行命令和完整原始报错信息发给当前 Agent 继续处理，不要求用户自行猜测修复，也不能只截取最后一行。
- 默认不控制 iOS 真机。静态信息不足且真机操作确实必要时，也必须使用上述二选一方式列出设备、动作和预期信息，不得改为直接索要权限。

## 固定路线与输入

- 目标必须是原生 iOS 工程，包含根级 `Podfile` 或 `*.xcodeproj`，且不是 Flutter 或 React Native 工程。
- 美摄短视频 Demo 必须连接并运行在真实 iPhone 或 iPad 上；iOS Simulator 和其他虚拟设备不受支持，不能用于运行或验收。
- 唯一 SDK 输入是官方原生 iOS 包，必须包含 `Pods-NvShortVideoEdit/NvShortVideoEdit.podspec`。不得使用 Flutter 插件、React Native 包或 Android AAR 替代。
- 缺少官方包时，在任何项目写入前停止，并在当前轮次最终可见回复中完整说明：打开 `https://www.meishesdk.com/developers`，依次进入「开发者中心」->「产品及DEMO下载」->「移动端」->「短视频Demo」，下载「iOS App」或「iOS&Android」原生 Demo 包，取得 `native/ios/Pods-NvShortVideoEdit/NvShortVideoEdit.podspec`。明确告诉用户可将解压包或 `Pods-NvShortVideoEdit` 复制到目标项目并提供项目内路径，也可保留在其他本地位置并直接提供绝对 `--plugin-path`；不得只写“请提供包或路径”或只引用说明文件。
- 自动发现只搜索 `--target-root`。Project、应用 Target、共享 Scheme 和 Workspace 分别识别；不得用 `.xcodeproj` 文件名代替 Target。存在多个候选且无法唯一映射、或 Pod 结构无效时，在任何目标写入前失败。
- 外部包只作为复制源，最终 Podfile 必须引用 `vendor/meishe/Pods-NvShortVideoEdit`。完成后检查配置和锁文件中不存在 Downloads、父目录或其他外部绝对路径。
- 读取 `references/native-ios.md`、`references/native-ios-feature-configuration.md`、`references/packages/native-ios.md`、`references/verified/native-ios.md`；遇到问题再读取 `references/native-ios-troubleshooting.md`。

## 执行

```shell
python scripts/integrate_native_ios.py \
  --target-root <ios-project> \
  --plugin-path <official-native-ios-package>
```

- 可选参数：`--license-path`、`--ios-target`、`--ios-bundle-identifier`、`--dry-run`。固定入口拒绝 `--platform`。
- 当前任务新建的原生 iOS 项目，接入命令必须默认追加 `--ios-bundle-identifier com.meishe.duanshipindemo`。脚本只修改已确认 App Target 的构建配置，不修改测试 Target 或 Extension。
- 用户已有项目未显式要求改身份时不静默修改 Bundle Identifier；先读取 App Target 的现有值。若不是 `com.meishe.duanshipindemo`，必须在接入前和报告中醒目说明官方 Demo 服务请求无法走通，并给出“临时验证改为官方 Demo 身份”或“保留现有身份并配置客户服务器、匹配 License 和服务白名单”两条路径。
- 脚本生成 Swift 首页、功能配置、Podfile/Info.plist 修改、项目本地 SDK、自检交接和报告，不自动执行 `pod install`、签名或设备操作。

## Demo 启动页硬性要求

- 当前任务新建或临时 Demo 工程时，把 `MeisheShortVideoHomeViewController` 设为 App 实际根页面：检查 `AppDelegate`/`SceneDelegate` 的 `rootViewController`、生成 Swift/资源的 Target Membership，以及共享 Scheme 的 Run executable；不得让默认 Storyboard、空白控制器、Hello World 或仅构建不启动的空 Run 动作成为交付结果。
- 已有业务项目默认保留原根控制器和导航；只有用户明确要求创建 Demo 或替换主页时，才把美摄首页设为根页面。
- 交付前检查实际启动代码和 Scheme，而不只确认 ViewController 文件存在。未完成主页接线时不得宣称接入完成，也不得只在报告中留下“present/push 到首页”的提示。

## 配置查询与修改

先确认官方包版本，再运行：

```shell
python scripts/query_feature_config.py \
  --track native-ios \
  --platform ios \
  --version <version> \
  --query "<中文或英文字段、菜单或自然语言操作>"
```

- 唯一业务配置入口是生成项目中的 `MeisheFeatureConfig.swift`，服务器入口按生成报告定位到 `ServerConfig`。
- 查询必须以 `references/config-capabilities/native-ios.json` 的中英文字段和值映射定位。组合请求返回多个配置组时全部处理。
- 查询结果必须直接给出 Swift 文件、字段、建议操作、合法边界和 Product > Run 生效步骤；`--json` 返回同等信息的 `suggestedMutation`，查询本身不写项目。
- `verified`、`boundary_verified` 可按 `mutationTarget` 修改；`partial` 要说明未生效部分；`ineffective`、`unsupported` 不生成不存在的 Swift 属性；`limited` 要求真实资源、服务或人工条件。
- 未精确匹配验证版本时保持 `unverified`，只检查当前 Pod 公开 API，不继承旧补丁或猜测属性。
- 菜单裁剪必须修改有序数据源并校验默认项、依赖项、索引和布局重排，禁止只隐藏控件留下空位。

增强文档查询必须固定 native/iOS：

```shell
python scripts/query_shortvideo_docs.py --track native --platform ios --language zh
```

## 交付与生效

- 必须生成 `meishe_configuration_handoff.md` 和 `meishe_docking_report.md`，列出 Swift 配置、服务器、License、Bundle Identifier、Team/签名和 CocoaPods 边界。
- 最终回复必须给出目标项目根目录 `README.md` 的绝对路径，并明确说明其中包含项目依赖安装、构建、真机运行和配置生效的详细说明。
- 最终回复设置独立醒目的“配置修改与生效”章节，以表格列出绝对配置路径、最快生效方式、重建条件和无需执行的步骤，并把准确命令和 Xcode 操作分别放入独立代码块。明确推荐使用 Xcode 打开实际 `.xcworkspace` 运行，同时必须完整提供 `xcodebuild`、`devicectl device install app` 和 `devicectl device process launch` 命令行；不得把命令行称为备选或省略。
- Swift、License、Bundle Identifier、签名、Info.plist 和资源变化必须重新构建安装；只有 Pod 声明变化才重新执行 CocoaPods。
- 客户服务器读取 `references/customer-server.md`；没有真实接口、凭据、白名单和预期素材时，不宣称服务验证完成。
- 生成 UI 使用 `references/demo-ui-style.md`。不创建假 License；缺少正式 License 时明确说明水印及身份边界。

## 验证边界

- 运行 `python scripts/quick_validate.py` 验证完整接入、缺包失败、客户身份、未知 API 形状、自包含和配置映射。
- quick validate 通过只证明静态生成和失败边界，不代表 Pods、Xcode、签名或真机通过。
- 未经用户选择 `自动执行`，不执行依赖下载、真机安装、点击、截图或录屏；选择 `用户执行` 时必须提供完成当前阶段所需的全部指令。
