---
name: meishe-native-android-shortvideo-docking
description: Independently integrate, configure, validate, and troubleshoot the official Meishe ShortVideo native Android AAR in an existing Android Studio project. Use for black-box NvShortVideoCore.aar integration, generated Java/Kotlin demo UI and feature configuration, Gradle and manifest setup, applicationId/license/server questions, handoff generation, and version-scoped native Android fixes; never substitute Flutter, React Native, or iOS packages.
---

# 美摄原生 Android 短视频 Demo 接入

本 skill 只处理原生 Android 路线。目标工程必须先由用户在 Android Studio 创建，完成输入预检后再运行固定脚本、检查报告，并给出 Gradle、配置和验证步骤。

脚本运行环境要求 Python `3.9+`；结构校验会拒绝未声明兼容性的新版类型语法。

## 修改与操作审批

- 修改本 skill 前，先向用户列出简短中文计划、影响范围和验证方式，获得明确同意后才能写入；扩大范围必须再次获批。用户手动修改的内容不得擅自覆盖或撤销。
- 集成脚本不执行 Gradle Sync、依赖下载或远程构建。到达依赖、构建或设备操作边界时读取 `references/dependency-installation.md`，一次性列出绝对目录、全部命令/操作、执行顺序、用途和成功标志；适用时必须同时列出 Android Studio 操作和完整命令行，二者不能互相替代。然后让用户明确选择 `用户执行` 或 `自动执行`；未选择时暂停。
- 展示二选一时，必须在当前轮次的最终可见回复中逐项重复上述完整清单和两个选择。不得把命令只放在 commentary、工具输出、折叠的“处理中”区域或报告文件中，不得让用户回看上一条消息；发送该回复后停止本轮工具调用，等待用户选择。
- `用户执行`：把完成当前阶段所需的全部命令交给用户，不再逐条追问；用户返回结果后继续。`自动执行`：由 Agent 执行已列出的任务内操作，并先明确提示会额外消耗 Token 和时间。
- 受操作系统、工具链版本、依赖缓存、网络、签名和设备环境差异影响，手动接入或运行可能报错。遇到任何报错，要求用户复制执行命令和完整原始报错信息发给当前 Agent 继续处理，不要求用户自行猜测修复，也不能只截取最后一行。
- 默认不控制 Android 真机。静态信息不足且真机操作确实必要时，也必须使用上述二选一方式列出设备、动作和预期信息，不得改为直接索要权限。

## 固定路线与输入

- 目标必须是现有原生 Android Studio 工程，根目录或 `android/` 包含 `settings.gradle[.kts]`，且不是 Flutter 或 React Native 工程。没有工程时停止并要求用户先创建，不伪造 Gradle 工程。
- 美摄短视频 Demo 必须连接并运行在真实 Android 设备上；Android Emulator 和其他虚拟设备不受支持，不能用于运行或验收。
- 唯一 SDK 输入是官方原生 Android `NvShortVideoCore.aar`。不得使用 Flutter AAR、React Native 包或 iOS Pod 替代。
- 缺少官方包时，在任何项目写入前停止，并在当前轮次最终可见回复中完整说明：打开 `https://www.meishesdk.com/developers`，依次进入「开发者中心」->「产品及DEMO下载」->「移动端」->「短视频Demo」，下载「iOS&Android」原生 Demo 包，取得 `native/android/ShortVideo/app/libs/NvShortVideoCore.aar`。明确告诉用户可将 AAR 复制到目标项目并提供项目内路径，也可保留在其他本地位置并直接提供绝对 `--aar-path`；不得只写“请提供 AAR 或路径”或只引用说明文件。
- 自动发现只搜索 `--target-root`。AAR 无效、应用 module 不明确、Gradle 结构不支持时，在任何目标写入前失败。
- 外部 AAR 只作为复制源，最终依赖必须指向应用 module 的 `libs/NvShortVideoCore.aar`。完成后检查 Gradle 和配置中不存在 Downloads、父目录或其他外部绝对路径。
- 读取 `references/native-android.md`、`references/native-android-feature-configuration.md`、`references/packages/native-android.md`、`references/verified/native-android.md`；AAR 获取读取 `references/aar-acquisition.md`，遇到问题再读取 `references/native-android-troubleshooting.md`。

## 执行

```shell
python scripts/integrate_native_android.py \
  --target-root <android-project> \
  --aar-path <NvShortVideoCore.aar>
```

- 可选参数：`--license-path`、`--package-name`、`--demo-launcher`、`--dry-run`。固定入口拒绝 `--platform`。
- `--demo-launcher` 仅用于新建临时 Demo；已有产品工程默认不替换 launcher。
- 脚本生成 Java/Kotlin 接入、Demo 首页、功能配置、Manifest/Gradle 修改、项目本地 AAR、配置交接和报告，不自动执行 Gradle Sync、构建或设备操作。

## Demo 启动页硬性要求

- 当前任务新建或临时 Demo 工程时，运行接入命令时传入 `--demo-launcher`，并检查最终 `AndroidManifest.xml` 只有 `.meishe.MeisheShortVideoDemoActivity` 持有 `MAIN`/`LAUNCHER`；不得让原 `MainActivity`、Hello World、Compose Greeting 或其他 Android 模板继续作为启动主页。
- 已有业务项目默认保留原 launcher 和导航；只有用户明确要求创建 Demo 或替换主页时，才提升美摄 Demo Activity 为 launcher。
- 交付前检查合并后的实际 Manifest，而不只确认 Demo Activity 文件存在。未完成主页接线时不得宣称接入完成，也不得只在报告中留下“从业务页面打开 Demo”的提示。

## 配置查询与修改

先确认官方 AAR 版本，再运行：

```shell
python scripts/query_feature_config.py \
  --track native-android \
  --platform android \
  --version <version> \
  --query "<中文或英文字段、菜单或自然语言操作>"
```

- 唯一业务配置入口是生成项目中的 `MeisheFeatureConfig.java` 或对应 Kotlin 文件；示例 JSON 和服务器入口按生成报告定位。
- 查询必须以 `references/config-capabilities/native-android.json` 的中英文字段和值映射定位。组合请求返回多个配置组时全部处理。
- 查询结果必须直接给出 Java/Kotlin 文件、字段、建议操作、合法边界和重新构建命令；`--json` 返回同等信息的 `suggestedMutation`，查询本身不写项目。
- `verified`、`boundary_verified` 可按 `mutationTarget` 修改；`partial` 要说明未生效部分；`ineffective`、`unsupported` 不制造无效调用；`limited` 要求真实资源、服务或人工条件。
- 未精确匹配验证版本时保持 `unverified`，只检查当前 AAR 公开 API，不继承旧补丁。
- 在调用 SDK 前阻止 `maxVolume=0` 和当前已验证 AAR 不接受的单元素 `supportedEditModes`；菜单裁剪必须同步校验默认项、依赖项、索引和布局重排。

增强文档查询必须固定 native/Android：

```shell
python scripts/query_shortvideo_docs.py --track native --platform android --language zh
```

## 交付与生效

- 必须生成 `meishe_configuration_handoff.md` 和 `meishe_docking_report.md`，列出 Java/Kotlin 配置、服务器、License、applicationId、Gradle 和资源边界。
- 最终回复必须给出目标项目根目录 `README.md` 的绝对路径，并明确说明其中包含项目依赖安装、构建、真机运行和配置生效的详细说明。
- 最终回复设置独立醒目的“配置修改与生效”章节，以表格列出绝对配置路径、最快生效方式、重建条件和无需执行的步骤，并把准确命令或 Android Studio 操作放入独立代码块。
- Java/Kotlin、License、applicationId、Manifest、Gradle 和资源变化必须重新构建安装；只有依赖声明变化才重新解析依赖。
- 客户服务器读取 `references/customer-server.md`；没有真实接口、凭据、白名单和预期素材时，不宣称服务验证完成。
- 生成 UI 使用 `references/demo-ui-style.md`。不创建假 License；缺少正式 License 时明确说明水印及身份边界。

## 验证边界

- 运行 `python scripts/quick_validate.py` 验证完整接入、不支持 compileSdk、封面 API 形状、AAR 自包含和配置映射。
- quick validate 通过只证明静态生成和失败边界，不代表 Gradle、Android Studio 或真机通过。
- 未经用户选择 `自动执行`，不执行依赖下载、真机安装、点击、截图或录屏；选择 `用户执行` 时必须提供完成当前阶段所需的全部指令。
