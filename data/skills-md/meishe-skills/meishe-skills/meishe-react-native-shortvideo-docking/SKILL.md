---
name: meishe-react-native-shortvideo-docking
description: Independently integrate, configure, validate, and troubleshoot the official Meishe ShortVideo React Native package for Android-only, iOS-only, or dual-platform React Native projects. Use for black-box RN demo integration, generated TypeScript configuration, native bridge compatibility, package/license/server setup, configuration questions, and version-scoped fixes; never use Flutter or native-only packages as substitutes.
---

# 美摄 React Native 短视频 Demo 接入

本 skill 只处理 React Native 路线。完成输入预检后运行固定脚本、检查报告，并给出 Android/iOS 实际目标对应的依赖、配置和验证步骤。

## 修改与操作审批

- 修改本 skill 前，先向用户列出简短中文计划、影响范围和验证方式，获得明确同意后才能写入；扩大范围必须再次获批。用户手动修改的内容不得擅自覆盖或撤销。
- 集成脚本不执行 npm/Yarn/pnpm、CocoaPods、Gradle 下载或远程构建。到达依赖、构建或设备操作边界时读取 `references/dependency-installation.md`，一次性列出绝对目录、全部命令/操作、执行顺序、用途和成功标志；适用时必须同时列出 IDE 操作和完整命令行，二者不能互相替代。然后让用户明确选择 `用户执行` 或 `自动执行`；未选择时暂停。
- 展示二选一时，必须在当前轮次的最终可见回复中逐项重复上述完整清单和两个选择。不得把命令只放在 commentary、工具输出、折叠的“处理中”区域或报告文件中，不得让用户回看上一条消息；发送该回复后停止本轮工具调用，等待用户选择。
- `用户执行`：把完成当前阶段所需的全部命令交给用户，不再逐条追问；用户返回结果后继续。`自动执行`：由 Agent 执行已列出的任务内操作，并先明确提示会额外消耗 Token 和时间。
- 受操作系统、工具链版本、依赖缓存、网络、签名和设备环境差异影响，手动接入或运行可能报错。遇到任何报错，要求用户复制执行命令和完整原始报错信息发给当前 Agent 继续处理，不要求用户自行猜测修复，也不能只截取最后一行。
- 默认不控制 Android/iOS 真机。静态信息不足且真机操作确实必要时，也必须使用上述二选一方式列出设备、动作和预期信息，不得改为直接索要权限。

## 固定路线与输入

- 目标根目录必须有 `package.json` 且声明 React Native；至少存在 `android/` 或 `ios/`。两个目录都存在时执行双端路线，单端项目不运行、不报告另一端。
- 美摄短视频 Demo 必须连接并运行在真实 Android/iOS 设备上；Android Emulator、iOS Simulator 和其他虚拟设备不受支持，不能用于运行或验收。
- 唯一 SDK 输入是官方 `react_native/react-native-nvshortvideo` npm 包。必须存在有效 `package.json` 和对应原生目录；不得使用 Flutter 插件、原生 AAR 或原生 iOS Pod 包代替。
- 缺少官方包时，在任何项目写入前停止，并在当前轮次最终可见回复中完整说明：打开 `https://www.meishesdk.com/developers`，依次进入「开发者中心」->「产品及DEMO下载」->「移动端」->「短视频Demo」，下载「React Native工程」，取得 `react_native/react-native-nvshortvideo/package.json`。明确告诉用户可将解压包或 `react-native-nvshortvideo` 复制到目标项目并提供项目内路径，也可保留在其他本地位置并直接提供绝对 `--plugin-path`；不得只写“请提供包或路径”或只引用说明文件。
- 自动发现只搜索 `--target-root`。输入缺失、结构无效、锁文件冲突或目标平台缺失时，在任何目标写入前失败。
- 外部包只作为复制源，最终依赖必须指向 `vendor/meishe/react-native-nvshortvideo`。完成后检查锁文件和配置中不存在 Downloads、父目录或其他外部绝对路径。
- 读取顺序：`references/react-native.md`、`references/react-native/common.md`、`references/react-native/feature-configuration.md`、`references/packages/react-native.md`、`references/verified/react-native.md`；再按实际目标读取 `android.md`、`ios.md`，排障时只读对应平台 troubleshooting。

## 执行

```shell
python scripts/integrate_react_native.py \
  --target-root <react-native-project> \
  --plugin-path <official-react-native-package>
```

- 可选参数：`--license-path`、`--package-name`、`--android-package-name`、`--ios-bundle-identifier`、`--dry-run`。固定入口拒绝 `--platform`。
- `--package-name` 继续用于双端相同身份；双端身份不同时分别使用两个平台专属参数。公共参数与平台专属参数对同一平台给出不同值时，脚本在写入前失败。
- 当前任务新建且包含 iOS 的 RN 项目，接入命令必须默认追加 `--ios-bundle-identifier com.meishe.duanshipindemo`。这是官方 Demo 素材服务能够请求成功的精确身份，不得使用近似值。
- 用户已有项目未显式要求改身份时，先读取 App Target 的现有 Bundle Identifier 并保持不变；若不是 `com.meishe.duanshipindemo`，必须在接入前和报告中醒目说明官方服务请求无法走通，并给出“临时验证改为官方 Demo 身份”或“保留现有身份并配置客户服务器、匹配 License 和服务白名单”两条路径。
- Demo License 只能用于精确匹配的官方 Demo 身份；自定义身份必须使用匹配的真实 License。
- 脚本只生成项目代码、项目本地 SDK、配置交接和报告，不自动安装依赖或控制设备。

## Demo 启动页硬性要求

- 当前任务新建或临时 Demo 工程时，把生成的 `MeisheShortVideoDemo` 接入实际启动链路，检查 `App.tsx`/`App.jsx`/`App.js` 的根组件或导航器的初始路由；不得把 Welcome、New App Screen、Hello World 或其他 React Native 默认模板保留为启动主页。
- 已有业务项目默认保留原导航结构；只有用户明确要求创建 Demo 或替换主页时，才把美摄首页设为根组件或初始路由。
- 交付前检查实际入口组件，而不只确认 `src/MeisheShortVideoDemo.*` 文件存在。未完成主页接线时不得宣称接入完成，也不得只在报告中留下“加入导航”的提示。

## 配置查询与修改

先确认官方包版本和目标平台，再运行：

```shell
python scripts/query_feature_config.py \
  --track react-native \
  --platform <android|ios> \
  --version <version> \
  --query "<中文或英文字段、菜单或自然语言操作>"
```

- 唯一业务配置入口是生成项目的 `src/meisheFeatureConfig.ts` 或 `.js`；不得把业务配置散落到 `android/` 或 `ios/`。
- 查询必须以 `references/config-capabilities/react-native.json` 的中英文字段和值映射定位。组合请求返回多个配置组时全部处理。
- 查询结果必须直接给出目标配置文件、字段、建议操作、合法边界和修改后生效命令；`--json` 返回同等信息的 `suggestedMutation`，查询本身不写项目。
- `verified`、`boundary_verified` 可按 `mutationTarget` 修改；`partial` 要说明未生效部分；`ineffective`、`unsupported` 不生成无效代码；`limited` 要求真实资源、服务或人工条件。
- 未精确匹配验证版本时保持 `unverified`，只检查当前官方包公开 API，不继承旧补丁。
- 菜单裁剪必须修改有序数据源并校验默认项、依赖项、索引和布局重排，禁止只隐藏控件留下空位。

增强文档查询必须固定 React Native track：

```shell
python scripts/query_shortvideo_docs.py --track react-native --platform <android|ios> --language zh
```

## 交付与生效

- 必须生成 `meishe_configuration_handoff.md` 和 `meishe_docking_report.md`，只列实际存在的平台。
- 最终回复必须给出目标项目根目录 `README.md` 的绝对路径，并明确说明其中包含项目依赖安装、构建、真机运行和配置生效的详细说明。
- 最终回复设置独立醒目的“配置修改与生效”章节，以表格列出绝对配置路径、适用平台、最快生效方式、重建条件和无需执行的步骤，并把准确命令放入独立代码块。涉及 iOS 时明确推荐使用 Xcode 打开实际 `.xcworkspace` 运行，同时必须完整提供 Metro 和 `npm`/Yarn/pnpm iOS 命令行；不得把命令行称为备选或省略。
- TS/JS 配置变化在 Debug 环境执行完整 Metro Reload，不能只依赖 Fast Refresh；原生桥接、License、包名、签名和原生资源变化必须重新构建安装。
- 只有依赖声明变化才重新执行 npm/Yarn/pnpm 或 CocoaPods。不得把 clean、清缓存或重新下载作为默认生效步骤。
- 客户服务器读取 `references/customer-server.md`；没有真实接口、凭据、白名单和预期素材时，不宣称服务验证完成。
- 生成 UI 使用 `references/demo-ui-style.md`。不创建假 License；缺少正式 License 时明确说明水印及身份边界。

## 验证边界

- Skill 脚本支持 Python 3.9 及以上；命令中的 `python` 必须解析到满足版本要求的解释器。
- 运行 `python scripts/quick_validate.py` 验证 Android 单端、iOS 单端、双端、缺包失败、自包含、配置映射及已验证补丁。
- 项目依赖已安装时，可运行 `python scripts/toolchain_validate.py --target-root <project>`，在不下载依赖的前提下执行可用的 Jest/ESLint 深度校验。
- quick validate 通过只证明静态生成和失败边界，不代表 npm、Pods、Gradle、Xcode 或真机通过。
- 未经用户选择 `自动执行`，不执行依赖下载、真机安装、点击、截图或录屏；选择 `用户执行` 时必须提供完成当前阶段所需的全部指令。
