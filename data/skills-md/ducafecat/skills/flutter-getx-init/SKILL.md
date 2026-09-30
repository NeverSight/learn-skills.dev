---
name: flutter-getx-init
description: Initialize an existing Flutter project into a runnable GetX scaffold with go_router, Dio, Freezed/JSON generation, SharedPreferences, Logger, and AdaptiveTheme. Use when the user asks to bootstrap a Flutter GetX app structure, create common/pages, Global.init, router, storage, network, or update main.dart for a Splash to Welcome/Login to Home flow.
license: MIT
metadata:
  author: ducafecat
  version: "1.0.0"
  compatibility: Requires an existing Flutter project with pubspec.yaml and lib/main.dart. Optional checks require Flutter SDK, Dart SDK, network access for package installation, and writable project files.
---

# Flutter GetX Init

把已有 Flutter 项目初始化为 Splash → Welcome → Login → Home 的可运行脚手架。GetX 管状态与依赖，go_router 管路由；Dio、SharedPreferences、Freezed、AdaptiveTheme 和三语翻译提供基础能力。Home 右上角保留主题与语言按钮，页面保留退出登录。

## 适用条件

目标项目已有 `pubspec.yaml` 和 `lib/main.dart`，且选用 GetX。先读取现有配置和源码，合并已有内容，不覆盖无关代码。需要结构和协作说明时读 [架构说明](references/architecture.md)；生成源码时读 [文件模板](references/file-templates.md)。

## 初始化

1. 根据目标项目的 `pubspec.yaml` 确认包名和 Flutter/Dart 版本。安装运行依赖：`get go_router dio native_dio_adapter freezed_annotation json_annotation shared_preferences logger adaptive_theme:3.7.2 flutter_cache_manager`；开发依赖：`build_runner freezed json_serializable shared_preferences_platform_interface`。补齐 SDK 依赖 `flutter_localizations`。升级 AdaptiveTheme 前检查与当前 Flutter 的兼容性。
2. 按文件模板创建或合并 `lib/common`、四个页面模块、`lib/global.dart`、`lib/main.dart` 和 `test/widget_test.dart`。从 `assets/lib/common/widgets/` 只复制 `button.dart`、`scaffold.dart`、`index.dart`。把所有 `{{package_name}}` 换成目标包名。
3. 入口导出保持同步：`common/index.dart` 只导出存在的子目录入口；页面入口只导出页面与控制器；`pages/index.dart` 汇总四页。公共子目录之间导入目标目录入口，页面及 `main.dart`、`global.dart` 导入 `common/index.dart`。
4. Splash 首帧后停留 0.5 秒再分流。Welcome 是三页 `PageView`，完成后写欢迎标记。Login 预填演示账号，成功时由会话 revision 触发路由进入 Home。Home 右上角通过底部菜单切换浅色、深色、跟随系统主题和 en / zh-CN / zh-TW 语言，页面可退出登录；不含 Tab 壳或组件样式入口。
5. `BASE_URL`、refresh 白名单及代理路径在 `AppConfig`。未配置 `BASE_URL` 时使用本地假登录，不发送 refresh 或代理请求。GetX Controller 在页面 `initState` 注册、`dispose` 删除；刷新用 `GetBuilder` 与 `update([id])`。禁止使用 GetX 路由 API。

此 skill 不生成组件样式页、`lib/common/extension`、DucafeUI 文档或未使用的 widgets。组件库和设计文档由独立的 `flutter-getx-ui-kit` skill 提供。

## 验证

运行：

```sh
dart run build_runner build --delete-conflicting-outputs
dart format lib test
flutter analyze
flutter test
```

确认四页流程、假登录和退出登录可用，Home 顶部右侧主题与语言按钮可用，且没有组件样式页、扩展目录或失效导出。若 SDK、网络或现有项目问题阻塞验证，记录实际结果。不要打印密钥、部署或发布应用。
